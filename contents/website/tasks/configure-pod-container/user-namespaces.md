---
title: 为 Pod 配置用户名字空间
reviewers:
content_type: task
weight: 210
min-kubernetes-server-version: v1.25
---


{{< feature-state for_k8s_version="v1.25" state="alpha" >}}

本页展示如何为无状态 Pod 配置用户名字空间。可以将容器内的用户与主机上的用户隔离开来。

在容器中以 root 用户运行的进程可以以不同的（非 root）用户在宿主机上运行；换句话说，
进程在用户名字空间内部拥有执行操作的全部特权，但在用户名字空间外部并没有执行操作的特权。

你可以使用这个特性来减少有害的容器对同一宿主机上其他容器的影响。
[有些安全脆弱性问题][KEP-vulns]被评为 **HIGH** or **CRITICAL**，但当用户名字空间被启用时，
它们是无法被利用的。相信用户名字空间也能减轻一些未来的漏洞的影响。

在不使用用户名字空间的情况下，对于以 root 用户运行的容器而言，发生容器逃逸时，
容器将拥有在宿主机上的 root 特权。如果容器被赋予了某些权限，则这些权限在宿主机上同样有效。
当使用用户名字空间时这些都不可能发生。

[KEP-vulns]: https://github.com/kubernetes/enhancements/tree/217d790720c5aef09b8bd4d6ca96284a0affe6c2/keps/sig-node/127-user-namespaces#motivation

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

{{% thirdparty-content single="true" %}}

* 节点上的操作系统必须为 Linux
* 你需要在宿主机上执行命令
* 你需要能够通过 exec 操作进入 Pod
* 特性 `UserNamespacesStatelessPodsSupport` 需要被启用。

你所使用的集群**必须**包括至少一个符合
[要求](/zh-cn/docs/concepts/workloads/pods/user-namespaces/#before-you-begin)
的节点，以便为 Pod 配置用户名字空间。

如果你有混合节点，并且只有部分节点支持为 Pod 配置用户名字空间，
你还需要确保配置了用户名字空间的 Pod
被[调度](/zh-cn/docs/concepts/scheduling-eviction/assign-pod-node/)到合适的节点。

* CRI-O: v1.25 支持用户名字空间。

请注意 **如果你的容器运行时环境不支持用户名字空间，那么 Pod 规约中的 `hostUsers` 字段将被静默忽略，
并且系统会在没有用户名字空间的环境中创建 Pod。**


## 运行一个使用用户名字空间的 Pod {#create-pod}

为一个无状态的 Pod 启用用户名字空间需要设置 `.spec` 的 `hostUsers` 字段
为 `false`. 例如:

{{< codenew file="pods/user-namespaces-stateless.yaml" >}}

1. 在你的集群上创建 Pod：

   ```shell
   kubectl apply -f https://k8s.io/examples/pods/user-namespaces-stateless.yaml
   ```

2. 挂接到容器上并执行 `readlink /proc/self/ns/user`：

   ```shell
   kubectl attach -it userns bash
   ```

执行命令的输出类似于：

```none
readlink /proc/self/ns/user
user:[4026531837]
cat /proc/self/uid_map
0          0 4294967295
```

然后，在主机中打开一个 Shell 并运行相同的命令。

输出一定是不同的。这意味着主机和 Pod 使用不同的用户名字空间。当未启用用户名字空间时，
宿主机和 Pod 使用相同的用户名字空间。

如果你在用户名字空间中运行 kubelet，则需要将在 Pod 中运行命令的输出与在主机中运行的输出进行比较：

```none
readlink /proc/$pid/ns/user
user:[4026534732]
```

使用 kubelet 的进程号代替 `$pid`