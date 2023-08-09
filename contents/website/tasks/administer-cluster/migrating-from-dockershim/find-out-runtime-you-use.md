---
title: 查明节点上所使用的容器运行时
content_type: task
weight: 30
---


本页面描述查明集群中节点所使用的[容器运行时](/zh-cn/docs/setup/production-environment/container-runtimes/)
的步骤。

取决于你运行集群的方式，节点所使用的容器运行时可能是事先配置好的，
也可能需要你来配置。如果你在使用托管的 Kubernetes 服务，
可能存在特定于厂商的方法来检查节点上配置的容器运行时。
本页描述的方法应该在能够执行 `kubectl` 的场合下都可以工作。

## {{% heading "prerequisites" %}}

安装并配置 `kubectl`。参见[安装工具](/zh-cn/docs/tasks/tools/#kubectl) 节了解详情。

## 查明节点所使用的容器运行时 {#find-out-the-container-runtime-used-on-a-node}

使用 `kubectl` 来读取并显示节点信息：

```shell
kubectl get nodes -o wide
```

输出如下面所示。`CONTAINER-RUNTIME` 列给出容器运行时及其版本。

对于 Docker Engine，输出类似于：
```none
NAME         STATUS   VERSION    CONTAINER-RUNTIME
node-1       Ready    v1.16.15   docker://19.3.1
node-2       Ready    v1.16.15   docker://19.3.1
node-3       Ready    v1.16.15   docker://19.3.1
```
如果你的容器运行时显示为 Docker Engine，你仍然可能不会被 v1.24 中 dockershim 的移除所影响。
通过[检查运行时端点](#which-endpoint)，可以查看你是否在使用 dockershim。
如果你没有使用 dockershim，你就不会被影响。

对于 containerd，输出类似于这样：

```none
# For containerd
NAME         STATUS   VERSION   CONTAINER-RUNTIME
node-1       Ready    v1.19.6   containerd://1.4.1
node-2       Ready    v1.19.6   containerd://1.4.1
node-3       Ready    v1.19.6   containerd://1.4.1
```

你可以在[容器运行时](/zh-cn/docs/setup/production-environment/container-runtimes/)
页面找到与容器运行时相关的更多信息。

## 检查当前使用的运行时端点  {#which-endpoint}


容器运行时使用 Unix Socket 与 kubelet 通信，这一通信使用基于 gRPC 框架的
[CRI 协议](/zh-cn/docs/concepts/architecture/cri/)。kubelet 扮演客户端，运行时扮演服务器端。
在某些情况下，你可能想知道你的节点使用的是哪个 socket。
如若集群是 Kubernetes v1.24 及以后的版本，
或许你想知道当前运行时是否是使用 dockershim 的 Docker Engine。

{{< note >}}
如果你的节点在通过 `cri-dockerd` 使用 Docker Engine，
那么集群不会受到 Kubernetes 移除 dockershim 的影响。
{{< /note >}}

可以通过检查 kubelet 的参数得知当前使用的是哪个 socket。

1. 查看 kubelet 进程的启动命令

   ```
    tr \\0 ' ' < /proc/"$(pgrep kubelet)"/cmdline
   ```
   如有节点上没有 `tr` 或者 `pgrep`，就需要手动检查 kubelet 的启动命令

2. 在命令的输出中，查找 `--container-runtime` 和 `--container-runtime-endpoint` 标志。

   * 如果你的节点使用 Kubernetes v1.23 或更早的版本，这两个参数不存在，
     或者 `--container-runtime` 标志值不是 `remote`，则你在通过 dockershim 套接字使用
     Docker Engine。
     在 Kubernetes v1.27 及以后的版本中，`--container-runtime` 命令行参数不再可用。
   * 如果设置了 `--container-runtime-endpoint` 参数，查看套接字名称即可得知当前使用的运行时。
     如若套接字 `unix:///run/containerd/containerd.sock` 是 containerd 的端点。

如果你将节点上的容器运行时从 Docker Engine 改变为 containerd，可在
[迁移到不同的运行时](/zh-cn/docs/tasks/administer-cluster/migrating-from-dockershim/change-runtime-containerd/)
找到更多信息。或者，如果你想在 Kubernetes v1.24 及以后的版本仍使用 Docker Engine，
可以安装 CRI 兼容的适配器实现，如 [`cri-dockerd`](https://github.com/Mirantis/cri-dockerd)。

