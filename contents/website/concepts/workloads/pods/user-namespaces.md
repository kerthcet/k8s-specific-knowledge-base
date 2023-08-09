---
title: 用户命名空间
content_type: concept
weight: 160
min-kubernetes-server-version: v1.25
---

{{< feature-state for_k8s_version="v1.25" state="alpha" >}}
本页解释了在 Kubernetes Pod 中如何使用用户命名空间。
用户命名空间将容器内运行的用户与主机中的用户隔离开来。

在容器中以 root 身份运行的进程可以在主机中以不同的（非 root）用户身份运行；
换句话说，该进程在用户命名空间内的操作具有完全的权限，
但在命名空间外的操作是无特权的。

你可以使用这个功能来减少被破坏的容器对主机或同一节点中的其他 Pod 的破坏。
有[几个安全漏洞][KEP-vulns]被评为 **高** 或 **重要**，
当用户命名空间处于激活状态时，这些漏洞是无法被利用的。
预计用户命名空间也会减轻一些未来的漏洞。

[KEP-vulns]: https://github.com/kubernetes/enhancements/tree/217d790720c5aef09b8bd4d6ca96284a0affe6c2/keps/sig-node/127-user-namespaces#motivation

## {{% heading "prerequisites" %}}

{{% thirdparty-content %}}

这是一个只对 Linux 有效的功能特性，且需要 Linux 支持在所用文件系统上挂载 idmap。
这意味着：

* 在节点上，你用于 `/var/lib/kubelet/pods/` 的文件系统，或你为此配置的自定义目录，
  需要支持 idmap 挂载。
* Pod 卷中使用的所有文件系统都必须支持 idmap 挂载。

在实践中，这意味着你最低需要 Linux 6.3，因为 tmpfs 在该版本中开始支持 idmap 挂载。
这通常是需要的，因为有几个 Kubernetes 功能特性使用 tmpfs
（默认情况下挂载的服务账号令牌使用 tmpfs、Secret 使用 tmpfs 等等）。

Linux 6.3 中支持 idmap 挂载的一些比较流行的文件系统是：btrfs、ext4、xfs、fat、
tmpfs、overlayfs。


此外，需要在{{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}提供支持，
才能在 Kubernetes 无状态 Pod 中使用这一功能：

* CRI-O：1.25（及更高）版本支持配置容器的用户命名空间。

请注意，containerd v1.7 支持配置容器的用户命名空间，与 Kubernetes {{< skew currentPatchVersion >}}
兼容。它不应与 Kubernetes 1.27（及更高）版本一起使用。

目前 [cri-dockerd 没有计划][CRI-dockerd-issue]支持此功能。

[CRI-dockerd-issue]: https://github.com/Mirantis/cri-dockerd/issues/74

## 介绍 {#introduction}

用户命名空间是一个 Linux 功能，允许将容器中的用户映射到主机中的不同用户。
此外，在某用户命名空间中授予 Pod 的权能只在该命名空间中有效，在该命名空间之外无效。

一个 Pod 可以通过将 `pod.spec.hostUsers` 字段设置为 `false` 来选择使用用户命名空间。

kubelet 将挑选 Pod 所映射的主机 UID/GID，
并将以保证同一节点上没有两个无状态 Pod 使用相同的映射的方式进行。

`pod.spec` 中的 `runAsUser`、`runAsGroup`、`fsGroup` 等字段总是指的是容器内的用户。
启用该功能时，有效的 UID/GID 在 0-65535 范围内。这以限制适用于文件和进程（`runAsUser`、`runAsGroup` 等）。

使用这个范围之外的 UID/GID 的文件将被视为属于溢出 ID，
通常是 65534（配置在 `/proc/sys/kernel/overflowuid和/proc/sys/kernel/overflowgid`）。
然而，即使以 65534 用户/组的身份运行，也不可能修改这些文件。

大多数需要以 root 身份运行但不访问其他主机命名空间或资源的应用程序，
在用户命名空间被启用时，应该可以继续正常运行，不需要做任何改变。

## 了解无状态 Pod 的用户命名空间 {#understanding-user-namespaces-for-stateless-pods}

一些容器运行时的默认配置（如 Docker Engine、containerd、CRI-O）使用 Linux 命名空间进行隔离。
其他技术也存在，也可以与这些运行时（例如，Kata Containers 使用虚拟机而不是 Linux 命名空间）结合使用。
本页适用于使用 Linux 命名空间进行隔离的容器运行时。

在创建 Pod 时，默认情况下会使用几个新的命名空间进行隔离：
一个网络命名空间来隔离容器网络，一个 PID 命名空间来隔离进程视图等等。
如果使用了一个用户命名空间，这将把容器中的用户与节点中的用户隔离开来。

这意味着容器可以以 root 身份运行，并将该身份映射到主机上的一个非 root 用户。
在容器内，进程会认为它是以 root 身份运行的（因此像 `apt`、`yum` 等工具可以正常工作），
而实际上该进程在主机上没有权限。
你可以验证这一点，例如，如果你从主机上执行 `ps aux` 来检查容器进程是以哪个用户运行的。
`ps` 显示的用户与你在容器内执行 `id` 命令时看到的用户是不一样的。

这种抽象限制了可能发生的情况，例如，容器设法逃逸到主机上时的后果。
鉴于容器是作为主机上的一个非特权用户运行的，它能对主机做的事情是有限的。

此外，由于每个 Pod 上的用户将被映射到主机中不同的非重叠用户，
他们对其他 Pod 可以执行的操作也是有限的。

授予一个 Pod 的权能也被限制在 Pod 的用户命名空间内，
并且在这一命名空间之外大多无效，有些甚至完全无效。这里有两个例子：

- `CAP_SYS_MODULE` 若被授予一个使用用户命名空间的 Pod 则没有任何效果，这个 Pod 不能加载内核模块。
- `CAP_SYS_ADMIN` 只限于 Pod 所在的用户命名空间，在该命名空间之外无效。

在不使用用户命名空间的情况下，以 root 账号运行的容器，在容器逃逸时，在节点上有 root 权限。
而且如果某些权能被授予了某容器，这些权能在宿主机上也是有效的。
当我们使用用户命名空间时，这些都不再成立。

如果你想知道关于使用用户命名空间时的更多变化细节，请参见 `man 7 user_namespaces`。

## 设置一个节点以支持用户命名空间 {#set-up-a-node-to-support-user-namespaces}

建议主机的文件和主机的进程使用 0-65535 范围内的 UID/GID。

kubelet 会把高于这个范围的 UID/GID 分配给 Pod。
因此，为了保证尽可能多的隔离，主机的文件和主机的进程所使用的 UID/GID 应该在 0-65535 范围内。

请注意，这个建议对减轻 [CVE-2021-25741][CVE-2021-25741] 等 CVE 的影响很重要；
在这些 CVE 中，Pod 有可能读取主机中的任意文件。
如果 Pod 和主机的 UID/GID 不重叠，Pod 能够做的事情就会受到限制：
Pod 的 UID/GID 不会与主机的文件所有者/组相匹配。

[CVE-2021-25741]: https://github.com/kubernetes/kubernetes/issues/104980

## 限制 {#limitations}

当 Pod 使用用户命名空间时，不允许 Pod 使用其他主机命名空间。
特别是，如果你设置了 `hostUsers: false`，那么你就不可以设置如下属性：

* `hostNetwork: true`
* `hostIPC: true`
* `hostPID: true`


Pod 完全不使用卷是被允许的；如果使用卷，只允许使用以下卷类型：

* configmap
* secret
* projected
* downwardAPI
* emptyDir

## {{% heading "whatsnext" %}}

* 查阅[为 Pod 配置用户命名空间](/zh-cn/docs/tasks/configure-pod-container/user-namespaces/)
