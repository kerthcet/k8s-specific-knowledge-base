---
title: 关于 cgroup v2
content_type: concept
weight: 50
---


在 Linux 上，{{< glossary_tooltip text="控制组" term_id="cgroup" >}}约束分配给进程的资源。

{{< glossary_tooltip text="kubelet" term_id="kubelet" >}} 和底层容器运行时都需要对接 cgroup
来强制执行[为 Pod 和容器管理资源](/zh-cn/docs/concepts/configuration/manage-resources-containers/)，
这包括为容器化工作负载配置 CPU/内存请求和限制。

Linux 中有两个 cgroup 版本：cgroup v1 和 cgroup v2。cgroup v2 是新一代的 `cgroup` API。


## 什么是 cgroup v2？  {#cgroup-v2}

{{< feature-state for_k8s_version="v1.25" state="stable" >}}

cgroup v2 是 Linux `cgroup` API 的下一个版本。cgroup v2 提供了一个具有增强资源管理能力的统一控制系统。

cgroup v2 对 cgroup v1 进行了多项改进，例如：

- API 中单个统一的层次结构设计
- 更安全的子树委派给容器
- 更新的功能特性，
  例如[压力阻塞信息（Pressure Stall Information，PSI）](https://www.kernel.org/doc/html/latest/accounting/psi.html)
- 跨多个资源的增强资源分配管理和隔离
  - 统一核算不同类型的内存分配（网络内存、内核内存等）
  - 考虑非即时资源变化，例如页面缓存回写

一些 Kubernetes 特性专门使用 cgroup v2 来增强资源管理和隔离。
例如，[MemoryQoS](/blog/2021/11/26/qos-memory-resources/) 特性改进了内存 QoS 并依赖于 cgroup v2 原语。

## 使用 cgroup v2  {#using-cgroupv2}

使用 cgroup v2 的推荐方法是使用一个默认启用 cgroup v2 的 Linux 发行版。

要检查你的发行版是否使用 cgroup v2，请参阅[识别 Linux 节点上的 cgroup 版本](#check-cgroup-version)。

### 要求  {#requirements}

cgroup v2 具有以下要求：

* 操作系统发行版启用 cgroup v2
* Linux 内核为 5.8 或更高版本
* 容器运行时支持 cgroup v2。例如：
  * [containerd](https://containerd.io/) v1.4 和更高版本
  * [cri-o](https://cri-o.io/) v1.20 和更高版本
* kubelet 和容器运行时被配置为使用
  [systemd cgroup 驱动](/zh-cn/docs/setup/production-environment/container-runtimes#systemd-cgroup-driver)

### Linux 发行版 cgroup v2 支持  {#linux-distribution-cgroup-v2-support}

有关使用 cgroup v2 的 Linux 发行版的列表，
请参阅 [cgroup v2 文档](https://github.com/opencontainers/runc/blob/main/docs/cgroup-v2.md)。

* Container-Optimized OS（从 M97 开始）
* Ubuntu（从 21.10 开始，推荐 22.04+）
* Debian GNU/Linux（从 Debian 11 Bullseye 开始）
* Fedora（从 31 开始）
* Arch Linux（从 2021 年 4 月开始）
* RHEL 和类似 RHEL 的发行版（从 9 开始）

要检查你的发行版是否使用 cgroup v2，
请参阅你的发行版文档或遵循[识别 Linux 节点上的 cgroup 版本](#check-cgroup-version)中的指示说明。

你还可以通过修改内核 cmdline 引导参数在你的 Linux 发行版上手动启用 cgroup v2。
如果你的发行版使用 GRUB，则应在 `/etc/default/grub` 下的 `GRUB_CMDLINE_LINUX`
中添加 `systemd.unified_cgroup_hierarchy=1`，
然后执行 `sudo update-grub`。不过，推荐的方法仍是使用一个默认已启用 cgroup v2 的发行版。

### 迁移到 cgroup v2   {#migrating-cgroupv2}

要迁移到 cgroup v2，需确保满足[要求](#requirements)，然后升级到一个默认启用 cgroup v2 的内核版本。

kubelet 能够自动检测操作系统是否运行在 cgroup v2 上并相应调整其操作，无需额外配置。

切换到 cgroup v2 时，用户体验应没有任何明显差异，除非用户直接在节点上或从容器内访问 cgroup 文件系统。

cgroup v2 使用一个与 cgroup v1 不同的 API，因此如果有任何应用直接访问 cgroup 文件系统，
则需要将这些应用更新为支持 cgroup v2 的版本。例如：

* 一些第三方监控和安全代理可能依赖于 cgroup 文件系统。你要将这些代理更新到支持 cgroup v2 的版本。
* 如果以独立的 DaemonSet 的形式运行 [cAdvisor](https://github.com/google/cadvisor) 以监控 Pod 和容器，
  需将其更新到 v0.43.0 或更高版本。
* 如果你部署 Java 应用程序，最好使用完全支持 cgroup v2 的版本：
    * [OpenJDK / HotSpot](https://bugs.openjdk.org/browse/JDK-8230305): jdk8u372、11.0.16、15 及更高的版本
    * [IBM Semeru Runtimes](https://www.eclipse.org/openj9/docs/version0.33/#control-groups-v2-support): jdk8u345-b01、11.0.16.0、17.0.4.0、18.0.2.0 及更高的版本
    * [IBM Java](https://www.ibm.com/docs/en/sdk-java-technology/8?topic=new-service-refresh-7#whatsnew_sr7__fp15): 8.0.7.15 及更高的版本
* 如果你正在使用 [uber-go/automaxprocs](https://github.com/uber-go/automaxprocs) 包，
  确保你使用的版本是 v1.5.1 或者更高。

## 识别 Linux 节点上的 cgroup 版本 {#check-cgroup-version}

cgroup 版本取决于正在使用的 Linux 发行版和操作系统上配置的默认 cgroup 版本。
要检查你的发行版使用的是哪个 cgroup 版本，请在该节点上运行 `stat -fc %T /sys/fs/cgroup/` 命令：

```shell
stat -fc %T /sys/fs/cgroup/
```

对于 cgroup v2，输出为 `cgroup2fs`。

对于 cgroup v1，输出为 `tmpfs`。

## {{% heading "whatsnext" %}}

- 进一步了解 [cgroups](https://man7.org/linux/man-pages/man7/cgroups.7.html)
- 进一步了解[容器运行时](/zh-cn/docs/concepts/architecture/cri)
- 进一步了解 [cgroup 驱动](/zh-cn/docs/setup/production-environment/container-runtimes#cgroup-drivers)

