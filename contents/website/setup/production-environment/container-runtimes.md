---
title: 容器运行时
content_type: concept
weight: 20
---


{{% dockershim-removal %}}

你需要在集群内每个节点上安装一个
{{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}
以使 Pod 可以运行在上面。本文概述了所涉及的内容并描述了与节点设置相关的任务。

Kubernetes {{< skew currentVersion >}}
要求你使用符合{{<glossary_tooltip term_id="cri" text="容器运行时接口">}}（CRI）的运行时。

有关详细信息，请参阅 [CRI 版本支持](#cri-versions)。
本页简要介绍在 Kubernetes 中几个常见的容器运行时的用法。

- [containerd](#containerd)
- [CRI-O](#cri-o)
- [Docker Engine](#docker)
- [Mirantis Container Runtime](#mcr)


{{< note >}}
v1.24 之前的 Kubernetes 版本直接集成了 Docker Engine 的一个组件，名为 **dockershim**。
这种特殊的直接整合不再是 Kubernetes 的一部分
（这次删除被作为 v1.20 发行版本的一部分[宣布](/zh-cn/blog/2020/12/08/kubernetes-1-20-release-announcement/#dockershim-deprecation)）。

你可以阅读[检查 Dockershim 移除是否会影响你](/zh-cn/docs/tasks/administer-cluster/migrating-from-dockershim/check-if-dockershim-removal-affects-you/)以了解此删除可能会如何影响你。
要了解如何使用 dockershim 进行迁移，
请参阅[从 dockershim 迁移](/zh-cn/docs/tasks/administer-cluster/migrating-from-dockershim/)。

如果你正在运行 v{{< skew currentVersion >}} 以外的 Kubernetes 版本，查看对应版本的文档。
{{< /note >}}


## 安装和配置先决条件  {#install-and-configure-prerequisites}

以下步骤将通用设置应用于 Linux 上的 Kubernetes 节点。

如果你确定不需要某个特定设置，则可以跳过它。

有关更多信息，请参阅[网络插件要求](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/#network-plugin-requirements)或特定容器运行时的文档。

### 转发 IPv4 并让 iptables 看到桥接流量

执行下述指令：

```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# 设置所需的 sysctl 参数，参数在重新启动后保持不变
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

# 应用 sysctl 参数而不重新启动
sudo sysctl --system
```

通过运行以下指令确认 `br_netfilter` 和 `overlay` 模块被加载：

```bash
lsmod | grep br_netfilter
lsmod | grep overlay
```

通过运行以下指令确认 `net.bridge.bridge-nf-call-iptables`、`net.bridge.bridge-nf-call-ip6tables`
和 `net.ipv4.ip_forward` 系统变量在你的 `sysctl` 配置中被设置为 1：

```bash
sysctl net.bridge.bridge-nf-call-iptables net.bridge.bridge-nf-call-ip6tables net.ipv4.ip_forward
```

## cgroup 驱动  {#cgroup-drivers}

在 Linux 上，{{<glossary_tooltip text="控制组（CGroup）" term_id="cgroup" >}}用于限制分配给进程的资源。

{{< glossary_tooltip text="kubelet" term_id="kubelet" >}} 和底层容器运行时都需要对接控制组来强制执行
[为 Pod 和容器管理资源](/zh-cn/docs/concepts/configuration/manage-resources-containers/)
并为诸如 CPU、内存这类资源设置请求和限制。若要对接控制组，kubelet 和容器运行时需要使用一个 **cgroup 驱动**。
关键的一点是 kubelet 和容器运行时需使用相同的 cgroup 驱动并且采用相同的配置。

可用的 cgroup 驱动有两个：

* [`cgroupfs`](#cgroupfs-cgroup-driver)
* [`systemd`](#systemd-cgroup-driver)

### cgroupfs 驱动 {#cgroupfs-cgroup-driver}

`cgroupfs` 驱动是 [kubelet 中默认的 cgroup 驱动](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1)。
当使用 `cgroupfs` 驱动时， kubelet 和容器运行时将直接对接 cgroup 文件系统来配置 cgroup。

当 [systemd](https://www.freedesktop.org/wiki/Software/systemd/) 是初始化系统时，
**不** 推荐使用 `cgroupfs` 驱动，因为 systemd 期望系统上只有一个 cgroup 管理器。
此外，如果你使用 [cgroup v2](/zh-cn/docs/concepts/architecture/cgroups)，
则应用 `systemd` cgroup 驱动取代 `cgroupfs`。

### systemd cgroup 驱动 {#systemd-cgroup-driver}

当某个 Linux 系统发行版使用 [systemd](https://www.freedesktop.org/wiki/Software/systemd/)
作为其初始化系统时，初始化进程会生成并使用一个 root 控制组（`cgroup`），并充当 cgroup 管理器。

systemd 与 cgroup 集成紧密，并将为每个 systemd 单元分配一个 cgroup。
因此，如果你 `systemd` 用作初始化系统，同时使用 `cgroupfs` 驱动，则系统中会存在两个不同的 cgroup 管理器。

同时存在两个 cgroup 管理器将造成系统中针对可用的资源和使用中的资源出现两个视图。某些情况下，
将 kubelet 和容器运行时配置为使用 `cgroupfs`、但为剩余的进程使用 `systemd`
的那些节点将在资源压力增大时变得不稳定。

当 systemd 是选定的初始化系统时，缓解这个不稳定问题的方法是针对 kubelet 和容器运行时将
`systemd` 用作 cgroup 驱动。

要将 `systemd` 设置为 cgroup 驱动，需编辑 [`KubeletConfiguration`](/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/)
的 `cgroupDriver` 选项，并将其设置为 `systemd`。例如：

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
...
cgroupDriver: systemd
```

{{< note >}}
从 v1.22 开始，在使用 kubeadm 创建集群时，如果用户没有在
`KubeletConfiguration` 下设置 `cgroupDriver` 字段，kubeadm 默认使用 `systemd`。
{{< /note >}}

如果你将 `systemd` 配置为 kubelet 的 cgroup 驱动，你也必须将 `systemd`
配置为容器运行时的 cgroup 驱动。参阅容器运行时文档，了解指示说明。例如：

*  [containerd](#containerd-systemd)
*  [CRI-O](#cri-o)

{{< caution >}}
注意：更改已加入集群的节点的 cgroup 驱动是一项敏感的操作。
如果 kubelet 已经使用某 cgroup 驱动的语义创建了 Pod，更改运行时以使用别的
cgroup 驱动，当为现有 Pod 重新创建 PodSandbox 时会产生错误。
重启 kubelet 也可能无法解决此类问题。

如果你有切实可行的自动化方案，使用其他已更新配置的节点来替换该节点，
或者使用自动化方案来重新安装。
{{< /caution >}}

### 将 kubeadm 管理的集群迁移到 `systemd` 驱动

如果你希望将现有的由 kubeadm 管理的集群迁移到 `systemd` cgroup 驱动，
请按照[配置 cgroup 驱动](/zh-cn/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver/)操作。

## CRI 版本支持 {#cri-versions}

你的容器运行时必须至少支持 v1alpha2 版本的容器运行时接口。

Kubernetes [从 1.26 版本开始](/blog/2022/11/18/upcoming-changes-in-kubernetes-1-26/#cri-api-removal)**仅适用于**
v1 版本的容器运行时（CRI）API。早期版本默认为 v1 版本，
但是如果容器运行时不支持 v1 版本的 API，
则 kubelet 会回退到使用（已弃用的）v1alpha2 版本的 API。

## 容器运行时

{{% thirdparty-content %}}

### containerd

本节概述了使用 containerd 作为 CRI 运行时的必要步骤。

要在系统上安装 containerd，请按照[开始使用 containerd](https://github.com/containerd/containerd/blob/main/docs/getting-started.md)
的说明进行操作。创建有效的 `config.toml` 配置文件后返回此步骤。

{{< tabs name="找到 config.toml 文件" >}}
{{% tab name="Linux" %}}
你可以在路径 `/etc/containerd/config.toml` 下找到此文件。
{{% /tab %}}
{{% tab name="Windows" %}}
你可以在路径 `C:\Program Files\containerd\config.toml` 下找到此文件。
{{% /tab %}}
{{< /tabs >}}

在 Linux 上，containerd 的默认 CRI 套接字是 `/run/containerd/containerd.sock`。
在 Windows 上，默认 CRI 端点是 `npipe://./pipe/containerd-containerd`。

#### 配置 `systemd` cgroup 驱动 {#containerd-systemd}

结合 `runc` 使用 `systemd` cgroup 驱动，在 `/etc/containerd/config.toml` 中设置：

```
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
  ...
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
    SystemdCgroup = true
```

如果你使用 [cgroup v2](/zh-cn/docs/concepts/architecture/cgroups)，则推荐 `systemd` cgroup 驱动。

{{< note >}}
如果你从软件包（例如，RPM 或者 `.deb`）中安装 containerd，你可能会发现其中默认禁止了
CRI 集成插件。

你需要启用 CRI 支持才能在 Kubernetes 集群中使用 containerd。
要确保 `cri` 没有出现在 `/etc/containerd/config.toml` 文件中 `disabled_plugins`
列表内。如果你更改了这个文件，也请记得要重启 `containerd`。

如果你在初次安装集群后或安装 CNI 后遇到容器崩溃循环，则随软件包提供的 containerd
配置可能包含不兼容的配置参数。考虑按照
[getting-started.md](https://github.com/containerd/containerd/blob/main/docs/getting-started.md#advanced-topics)
中指定的 `containerd config default > /etc/containerd/config.toml` 重置 containerd
配置，然后相应地设置上述配置参数。
{{< /note >}}

如果你应用此更改，请确保重新启动 containerd：

```shell
sudo systemctl restart containerd
```

当使用 kubeadm 时，请手动配置
[kubelet 的 cgroup 驱动](/zh-cn/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver/#configuring-the-kubelet-cgroup-driver)。

#### 重载沙箱（pause）镜像    {#override-pause-image-containerd}

在你的 [containerd 配置](https://github.com/containerd/containerd/blob/main/docs/cri/config.md)中，
你可以通过设置以下选项重载沙箱镜像：

```toml
[plugins."io.containerd.grpc.v1.cri"]
  sandbox_image = "registry.k8s.io/pause:3.2"
```

一旦你更新了这个配置文件，可能就同样需要重启 `containerd`：`systemctl restart containerd`。

请注意，声明匹配的 `pod-infra-container-image` 是 kubelet 的最佳实践。
如果未配置，kubelet 可能会尝试对 `pause` 镜像进行垃圾回收。
[containerd 固定 pause 镜像](https://github.com/containerd/containerd/issues/6352)的工作正在进行中，
将不再需要在 kubelet 上进行此设置。

### CRI-O

本节包含安装 CRI-O 作为容器运行时的必要步骤。

要安装 CRI-O，请按照 [CRI-O 安装说明](https://github.com/cri-o/cri-o/blob/main/install.md#readme)执行操作。

#### cgroup 驱动   {#cgroup-driver}

CRI-O 默认使用 systemd cgroup 驱动，这对你来说可能工作得很好。
要切换到 `cgroupfs` cgroup 驱动，请编辑 `/etc/crio/crio.conf` 或在
`/etc/crio/crio.conf.d/02-cgroup-manager.conf` 中放置一个插入式配置，例如：

```toml
[crio.runtime]
conmon_cgroup = "pod"
cgroup_manager = "cgroupfs"
```

你还应该注意当使用 CRI-O 时，并且 CRI-O 的 cgroup 设置为 `cgroupfs` 时，必须将 `conmon_cgroup` 设置为值 `pod`。
通常需要保持 kubelet 的 cgroup 驱动配置（通常通过 kubeadm 完成）和 CRI-O 同步。

对于 CRI-O，CRI 套接字默认为 `/var/run/crio/crio.sock`。

#### 重载沙箱（pause）镜像   {#override-pause-image-cri-o}

在你的 [CRI-O 配置](https://github.com/cri-o/cri-o/blob/main/docs/crio.conf.5.md)中，
你可以设置以下配置值：

```toml
[crio.image]
pause_image="registry.k8s.io/pause:3.6"
```

这一设置选项支持动态配置重加载来应用所做变更：`systemctl reload crio`。
也可以通过向 `crio` 进程发送 `SIGHUP` 信号来实现。

### Docker Engine {#docker}

{{< note >}}
以下操作假设你使用 [`cri-dockerd`](https://github.com/Mirantis/cri-dockerd) 适配器来将
Docker Engine 与 Kubernetes 集成。
{{< /note >}}

1. 在你的每个节点上，遵循[安装 Docker Engine](https://docs.docker.com/engine/install/#server)
   指南为你的 Linux 发行版安装 Docker。

2. 按照源代码仓库中的说明安装 [`cri-dockerd`](https://github.com/Mirantis/cri-dockerd)。

对于 `cri-dockerd`，默认情况下，CRI 套接字是 `/run/cri-dockerd.sock`。

### Mirantis 容器运行时 {#mcr}

[Mirantis Container Runtime](https://docs.mirantis.com/mcr/20.10/overview.html) (MCR)
是一种商用容器运行时，以前称为 Docker 企业版。
你可以使用 MCR 中包含的开源 [`cri-dockerd`](https://github.com/Mirantis/cri-dockerd)
组件将 Mirantis Container Runtime 与 Kubernetes 一起使用。

要了解有关如何安装 Mirantis Container Runtime 的更多信息，
请访问 [MCR 部署指南](https://docs.mirantis.com/mcr/20.10/install.html)。

检查名为 `cri-docker.socket` 的 systemd 单元以找出 CRI 套接字的路径。

#### 重载沙箱（pause）镜像   {#override-pause-image-cri-dockerd-mcr}

`cri-dockerd` 适配器能够接受指定用作 Pod 的基础容器的容器镜像（“pause 镜像”）作为命令行参数。
要使用的命令行参数是 `--pod-infra-container-image`。

## {{% heading "whatsnext" %}}

除了容器运行时，你的集群还需要有效的[网络插件](/zh-cn/docs/concepts/cluster-administration/networking/#how-to-implement-the-kubernetes-networking-model)。
