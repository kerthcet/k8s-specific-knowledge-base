---
title: 为 Pod 或容器配置安全上下文
content_type: task
weight: 110
---


安全上下文（Security Context）定义 Pod 或 Container 的特权与访问控制设置。
安全上下文包括但不限于：

* 自主访问控制（Discretionary Access Control）：
  基于[用户 ID（UID）和组 ID（GID）](https://wiki.archlinux.org/index.php/users_and_groups)
  来判定对对象（例如文件）的访问权限。

* [安全性增强的 Linux（SELinux）](https://zh.wikipedia.org/wiki/%E5%AE%89%E5%85%A8%E5%A2%9E%E5%BC%BA%E5%BC%8FLinux)：
  为对象赋予安全性标签。

* 以特权模式或者非特权模式运行。

* [Linux 权能](https://linux-audit.com/linux-capabilities-hardening-linux-binaries-by-removing-setuid/): 
  为进程赋予 root 用户的部分特权而非全部特权。

* [AppArmor](/zh-cn/docs/tutorials/security/apparmor/)：使用程序配置来限制个别程序的权能。

* [Seccomp](/zh-cn/docs/tutorials/security/seccomp/)：过滤进程的系统调用。

* `allowPrivilegeEscalation`：控制进程是否可以获得超出其父进程的特权。
  此布尔值直接控制是否为容器进程设置
  [`no_new_privs`](https://www.kernel.org/doc/Documentation/prctl/no_new_privs.txt)标志。
  当容器满足一下条件之一时，`allowPrivilegeEscalation` 总是为 true：

  - 以特权模式运行，或者
  - 具有 `CAP_SYS_ADMIN` 权能

* `readOnlyRootFilesystem`：以只读方式加载容器的根文件系统。

以上条目不是安全上下文设置的完整列表 -- 请参阅
[SecurityContext](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#securitycontext-v1-core)
了解其完整列表。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


## 为 Pod 设置安全性上下文   {#set-the-security-context-for-a-pod}

要为 Pod 设置安全性设置，可在 Pod 规约中包含 `securityContext` 字段。`securityContext` 字段值是一个
[PodSecurityContext](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podsecuritycontext-v1-core)
对象。你为 Pod 所设置的安全性配置会应用到 Pod 中所有 Container 上。
下面是一个 Pod 的配置文件，该 Pod 定义了 `securityContext` 和一个 `emptyDir` 卷：

{{< codenew file="pods/security/security-context.yaml" >}}

在配置文件中，`runAsUser` 字段指定 Pod 中的所有容器内的进程都使用用户 ID 1000
来运行。`runAsGroup` 字段指定所有容器中的进程都以主组 ID 3000 来运行。
如果忽略此字段，则容器的主组 ID 将是 root（0）。
当 `runAsGroup` 被设置时，所有创建的文件也会划归用户 1000 和组 3000。
由于 `fsGroup` 被设置，容器中所有进程也会是附组 ID 2000 的一部分。
卷 `/data/demo` 及在该卷中创建的任何文件的属主都会是组 ID 2000。

创建该 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/security/security-context.yaml
```

检查 Pod 的容器处于运行状态：

```shell
kubectl get pod security-context-demo
```

开启一个 Shell 进入到运行中的容器：

```shell
kubectl exec -it security-context-demo -- sh
```

在你的 Shell 中，列举运行中的进程：

```shell
ps
```

输出显示进程以用户 1000 运行，即 `runAsUser` 所设置的值：

```none
PID   USER     TIME  COMMAND
    1 1000      0:00 sleep 1h
    6 1000      0:00 sh
...
```

在你的 Shell 中，进入 `/data` 目录列举其内容：

```shell
cd /data
ls -l
```

输出显示 `/data/demo` 目录的组 ID 为 2000，即 `fsGroup` 的设置值：

```none
drwxrwsrwx 2 root 2000 4096 Jun  6 20:08 demo
```

在你的 Shell 中，进入到 `/data/demo` 目录下创建一个文件：

```shell
cd demo
echo hello > testfile
```

列举 `/data/demo` 目录下的文件：

```shell
ls -l
```

输出显示 `testfile` 的组 ID 为 2000，也就是 `fsGroup` 所设置的值：

```none
-rw-r--r-- 1 1000 2000 6 Jun  6 20:08 testfile
```

运行下面的命令：

```shell
id
```

输出类似于：

```none
uid=1000 gid=3000 groups=2000
```

从输出中你会看到 `gid` 值为 3000，也就是 `runAsGroup` 字段的值。
如果 `runAsGroup` 被忽略，则 `gid` 会取值 0（root），而进程就能够与 root
用户组所拥有以及要求 root 用户组访问权限的文件交互。

退出你的 Shell：

```shell
exit
```

## 为 Pod 配置卷访问权限和属主变更策略

{{< feature-state for_k8s_version="v1.23" state="stable" >}}

默认情况下，Kubernetes 在挂载一个卷时，会递归地更改每个卷中的内容的属主和访问权限，
使之与 Pod 的 `securityContext` 中指定的 `fsGroup` 匹配。
对于较大的数据卷，检查和变更属主与访问权限可能会花费很长时间，降低 Pod 启动速度。
你可以在 `securityContext` 中使用 `fsGroupChangePolicy` 字段来控制 Kubernetes
检查和管理卷属主和访问权限的方式。

**fsGroupChangePolicy** - `fsGroupChangePolicy` 定义在卷被暴露给 Pod 内部之前对其
内容的属主和访问许可进行变更的行为。此字段仅适用于那些支持使用 `fsGroup` 来
控制属主与访问权限的卷类型。此字段的取值可以是：

* `OnRootMismatch`：只有根目录的属主与访问权限与卷所期望的权限不一致时，
  才改变其中内容的属主和访问权限。这一设置有助于缩短更改卷的属主与访问
  权限所需要的时间。
* `Always`：在挂载卷时总是更改卷中内容的属主和访问权限。

例如：

```yaml
securityContext:
  runAsUser: 1000
  runAsGroup: 3000
  fsGroup: 2000
  fsGroupChangePolicy: "OnRootMismatch"
```

{{< note >}}
此字段对于 [`secret`](/zh-cn/docs/concepts/storage/volumes/#secret)、
[`configMap`](/zh-cn/docs/concepts/storage/volumes/#configmap)
和 [`emptydir`](/zh-cn/docs/concepts/storage/volumes/#emptydir)
这类临时性存储无效。
{{< /note >}}

## 将卷权限和所有权更改委派给 CSI 驱动程序
{{< feature-state for_k8s_version="v1.26" state="stable" >}}

如果你部署了一个[容器存储接口 (CSI)](https://github.com/container-storage-interface/spec/blob/master/spec.md)
驱动，而该驱动支持 `VOLUME_MOUNT_GROUP` `NodeServiceCapability`，
在 `securityContext` 中指定 `fsGroup` 来设置文件所有权和权限的过程将由 CSI
驱动而不是 Kubernetes 来执行。在这种情况下，由于 Kubernetes 不执行任何所有权和权限更改，
`fsGroupChangePolicy` 不会生效，并且按照 CSI 的规定，CSI 驱动应该使用所指定的
`fsGroup` 来挂载卷，从而生成了一个对 `fsGroup` 可读/可写的卷.

## 为 Container 设置安全性上下文  {#set-the-security-context-for-a-container}

若要为 Container 设置安全性配置，可以在 Container 清单中包含 `securityContext` 
字段。`securityContext` 字段的取值是一个
[SecurityContext](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#securitycontext-v1-core)
对象。你为 Container 设置的安全性配置仅适用于该容器本身，并且所指定的设置在与
Pod 层面设置的内容发生重叠时，会重写 Pod 层面的设置。Container 层面的设置不会影响到 Pod 的卷。

下面是一个 Pod 的配置文件，其中包含一个 Container。Pod 和 Container 都有
`securityContext` 字段：

{{< codenew file="pods/security/security-context-2.yaml" >}}

创建该 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/security/security-context-2.yaml
```

验证 Pod 中的容器处于运行状态：

```shell
kubectl get pod security-context-demo-2
```

启动一个 Shell 进入到运行中的容器内：

```shell
kubectl exec -it security-context-demo-2 -- sh
```

在你的 Shell 中，列举运行中的进程：

```shell
ps aux
```

输出显示进程以用户 2000 运行。该值是在 Container 的 `runAsUser` 中设置的。
该设置值重写了 Pod 层面所设置的值 1000。

```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
2000         1  0.0  0.0   4336   764 ?        Ss   20:36   0:00 /bin/sh -c node server.js
2000         8  0.1  0.5 772124 22604 ?        Sl   20:36   0:00 node server.js
...
```

退出你的 Shell：

```shell
exit
```

## 为 Container 设置权能   {#set-capabilities-for-a-container}

使用 [Linux 权能](https://man7.org/linux/man-pages/man7/capabilities.7.html)，
你可以赋予进程 root 用户所拥有的某些特权，但不必赋予其全部特权。
要为 Container 添加或移除 Linux 权能，可以在 Container 清单的 `securityContext`
节包含 `capabilities` 字段。

首先，看一下不包含 `capabilities` 字段时候会发生什么。
下面是一个配置文件，其中没有添加或移除容器的权能：

{{< codenew file="pods/security/security-context-3.yaml" >}}

创建该 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/security/security-context-3.yaml
```

验证 Pod 的容器处于运行状态：

```shell
kubectl get pod security-context-demo-3
```

启动一个 Shell 进入到运行中的容器：

```shell
kubectl exec -it security-context-demo-3 -- sh
```

在你的 Shell 中，列举运行中的进程：

```shell
ps aux
```

输出显示容器中进程 ID（PIDs）：

```
USER  PID %CPU %MEM    VSZ   RSS TTY   STAT START   TIME COMMAND
root    1  0.0  0.0   4336   796 ?     Ss   18:17   0:00 /bin/sh -c node server.js
root    5  0.1  0.5 772124 22700 ?     Sl   18:17   0:00 node server.js
```

在你的 Shell 中，查看进程 1 的状态：

```shell
cd /proc/1
cat status
```

输出显示进程的权能位图：

```
...
CapPrm:	00000000a80425fb
CapEff:	00000000a80425fb
...
```

记下进程权能位图，之后退出你的 Shell：

```shell
exit
```

接下来运行一个与前例中容器相同的容器，只是这个容器有一些额外的权能设置。

下面是一个 Pod 的配置，其中运行一个容器。配置为容器添加 `CAP_NET_ADMIN` 和
`CAP_SYS_TIME` 权能：

{{< codenew file="pods/security/security-context-4.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/security/security-context-4.yaml
```

启动一个 Shell，进入到运行中的容器：

```shell
kubectl exec -it security-context-demo-4 -- sh
```

在你的 Shell 中，查看进程 1 的权能：

```shell
cd /proc/1
cat status
```

输出显示的是进程的权能位图：

```
...
CapPrm:	00000000aa0435fb
CapEff:	00000000aa0435fb
...
```

比较两个容器的权能位图：

```
00000000a80425fb
00000000aa0435fb
```

在第一个容器的权能位图中，位 12 和 25 是没有设置的。在第二个容器中，位 12
和 25 是设置了的。位 12 是 `CAP_NET_ADMIN` 而位 25 则是 `CAP_SYS_TIME`。
参见 [capability.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/capability.h)
了解权能常数的定义。

{{< note >}}
Linux 权能常数定义的形式为 `CAP_XXX`。但是你在 container 清单中列举权能时，
要将权能名称中的 `CAP_` 部分去掉。例如，要添加 `CAP_SYS_TIME`，
可在权能列表中添加 `SYS_TIME`。
{{< /note >}}

## 为容器设置 Seccomp 配置 

若要为容器设置 Seccomp 配置（Profile），可在你的 Pod 或 Container 清单的
`securityContext` 节中包含 `seccompProfile` 字段。该字段是一个 
[SeccompProfile](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#seccompprofile-v1-core)
对象，包含 `type` 和 `localhostProfile` 属性。
`type` 的合法选项包括 `RuntimeDefault`、`Unconfined` 和 `Localhost`。
`localhostProfile` 只能在 `type: Localhost` 配置下才可以设置。
该字段标明节点上预先设定的配置的路径，路径是相对于 kubelet 所配置的
Seccomp 配置路径（使用 `--root-dir` 设置）而言的。

下面是一个例子，设置容器使用节点上容器运行时的默认配置作为 Seccomp 配置：

```yaml
...
securityContext:
  seccompProfile:
    type: RuntimeDefault
```

下面是另一个例子，将 Seccomp 的样板设置为位于
`<kubelet-根目录>/seccomp/my-profiles/profile-allow.json`
的一个预先配置的文件。

```yaml
...
securityContext:
  seccompProfile:
    type: Localhost
    localhostProfile: my-profiles/profile-allow.json
```

## 为 Container 赋予 SELinux 标签

若要给 Container 设置 SELinux 标签，可以在 Pod 或 Container 清单的
`securityContext` 节包含 `seLinuxOptions` 字段。
`seLinuxOptions` 字段的取值是一个
[SELinuxOptions](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#selinuxoptions-v1-core)
对象。下面是一个应用 SELinux 标签的例子：

```yaml
...
securityContext:
  seLinuxOptions:
    level: "s0:c123,c456"
```

{{< note >}}
要指定 SELinux，需要在宿主操作系统中装载 SELinux 安全性模块。
{{< /note >}}

### 高效重打 SELinux 卷标签

{{< feature-state for_k8s_version="v1.27" state="beta" >}}

默认情况下，容器运行时递归地将 SELinux 标签赋予所有 Pod 卷上的所有文件。
为了加快该过程，Kubernetes 使用挂载可选项 `-o context=<label>` 可以立即改变卷的 SELinux 标签。

要使用这项加速功能，必须满足下列条件：

* 必须启用 `ReadWriteOncePod` 和 `SELinuxMountReadWriteOncePod`
  [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)。

* Pod 必须以 `accessModes: ["ReadWriteOncePod"]` 模式使用 PersistentVolumeClaim。

* Pod（或其中使用 PersistentVolumeClaim 的所有容器）必须设置 `seLinuxOptions`。

* 对应的 PersistentVolume 必须是：
  * 使用传统树内（In-Tree） `iscsi`、`rbd` 或 `fs` 卷类型的卷。
  * 或者是使用 {< glossary_tooltip text="CSI" term_id="csi" >}} 驱动程序的卷
    CSI 驱动程序必须能够通过在 CSIDriver 实例中设置 `spec.seLinuxMount: true`
    以支持 `-o context` 挂载。

对于所有其他卷类型，重打 SELinux 标签的方式有所不同：
容器运行时为卷中的所有节点（文件和目录）递归地修改 SELinux 标签。
卷中的文件和目录越多，重打标签需要耗费的时间就越长。

{{< note >}}
如果你的 Kubernetes 版本是 v1.25，请参阅此任务页面的 v1.25 版本：
[为 Pod 或 Container 配置安全上下文](https://v1-25.docs.kubernetes.io/docs/tasks/configure-pod-container/security-context/)（v1.25）。
该文档中有一个重要的说明：kubelet 在重启后会丢失对卷标签的追踪记录。
这个缺陷已经在 Kubernetes 1.26 中修复。
{{< /note >}}

## 讨论   {#discussion}

Pod 的安全上下文适用于 Pod 中的容器，也适用于 Pod 所挂载的卷（如果有的话）。
尤其是，`fsGroup` 和 `seLinuxOptions` 按下面的方式应用到挂载卷上：

* `fsGroup`：支持属主管理的卷会被修改，将其属主变更为 `fsGroup` 所指定的 GID，
  并且对该 GID 可写。进一步的细节可参阅
  [属主变更设计文档](https://git.k8s.io/design-proposals-archive/storage/volume-ownership-management.md)。

* `seLinuxOptions`：支持 SELinux 标签的卷会被重新打标签，以便可被 `seLinuxOptions`
  下所设置的标签访问。通常你只需要设置 `level` 部分。
  该部分设置的是赋予 Pod 中所有容器及卷的
  [多类别安全性（Multi-Category Security，MCS)](https://selinuxproject.org/page/NB_MLS)标签。

{{< warning >}}
在为 Pod 设置 MCS 标签之后，所有带有相同标签的 Pod 可以访问该卷。
如果你需要跨 Pod 的保护，你必须为每个 Pod 赋予独特的 MCS 标签。
{{< /warning >}}

## 清理

删除之前创建的所有 Pod：

```shell
kubectl delete pod security-context-demo
kubectl delete pod security-context-demo-2
kubectl delete pod security-context-demo-3
kubectl delete pod security-context-demo-4
```

## {{% heading "whatsnext" %}}

* [PodSecurityContext](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podsecuritycontext-v1-core) API 定义
* [SecurityContext](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#securitycontext-v1-core) API 定义
* [使用最新的安全性增强来调优 Docker（英文）](https://github.com/containerd/containerd/blob/main/docs/cri/config.md)
* [安全上下文的设计文档（英文）](https://github.com/kubernetes/design-proposals-archive/blob/main/auth/security_context.md)
* [属主管理的设计文档（英文）](https://github.com/kubernetes/design-proposals-archive/blob/main/storage/volume-ownership-management.md)
* [Pod 安全性准入](/zh-cn/docs/concepts/security/pod-security-admission/)
* [AllowPrivilegeEscalation 的设计文档（英文）](https://github.com/kubernetes/design-proposals-archive/blob/main/auth/no-new-privs.md)
* 关于在 Linux 系统中的安全机制的更多信息，可参阅
  [Linux 内核安全性能力概述](https://www.linux.com/learn/overview-linux-kernel-security-features)（注意：部分信息已过时）。

