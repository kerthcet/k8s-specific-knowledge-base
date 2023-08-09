---
title: Kubernetes 中的 Windows 容器
content_type: concept
weight: 65
---

在许多组织中，所运行的很大一部分服务和应用是 Windows 应用。
[Windows 容器](https://aka.ms/windowscontainers)提供了一种封装进程和包依赖项的方式，
从而简化了 DevOps 实践，令 Windows 应用程序同样遵从云原生模式。

对于同时投入基于 Windows 应用和 Linux 应用的组织而言，他们不必寻找不同的编排系统来管理其工作负载，
使其跨部署的运营效率得以大幅提升，而不必关心所用的操作系统。


## Kubernetes 中的 Windows 节点 {#windows-nodes-in-k8s}

若要在 Kubernetes 中启用对 Windows 容器的编排，可以在现有的 Linux 集群中包含 Windows 节点。
在 Kubernetes 上调度 {{< glossary_tooltip text="Pod" term_id="pod" >}} 中的 Windows 容器与调度基于 Linux 的容器类似。

为了运行 Windows 容器，你的 Kubernetes 集群必须包含多个操作系统。
尽管你只能在 Linux 上运行{{< glossary_tooltip text="控制平面" term_id="control-plane" >}}，
你可以部署运行 Windows 或 Linux 的工作节点。

支持 Windows {{< glossary_tooltip text="节点" term_id="node" >}}的前提是操作系统为 Windows Server 2019。

本文使用术语 **Windows 容器**表示具有进程隔离能力的 Windows 容器。
Kubernetes 不支持使用
[Hyper-V 隔离能力](https://docs.microsoft.com/zh-cn/virtualization/windowscontainers/manage-containers/hyperv-container)来运行
Windows 容器。

## 兼容性与局限性 {#limitations}

某些节点层面的功能特性仅在使用特定[容器运行时](#container-runtime)时才可用；
另外一些特性则在 Windows 节点上不可用，包括：

* 巨页（HugePages）：Windows 容器当前不支持。
* 特权容器：Windows 容器当前不支持。
  [HostProcess 容器](/zh-cn/docs/tasks/configure-pod-container/create-hostprocess-pod/)提供类似功能。
* TerminationGracePeriod：需要 containerD。

Windows 节点并不支持共享命名空间的所有功能特性。
有关更多详细信息，请参考 [API 兼容性](#api)。

有关 Kubernetes 测试时所使用的 Windows 版本的详细信息，请参考 [Windows 操作系统版本兼容性](#windows-os-version-support)。

从 API 和 kubectl 的角度来看，Windows 容器的行为与基于 Linux 的容器非常相似。
然而，在本节所概述的一些关键功能上，二者存在一些显著差异。

### 与 Linux 比较 {#comparison-with-Linux-similarities}

Kubernetes 关键组件在 Windows 上的工作方式与在 Linux 上相同。
本节介绍几个关键的工作负载抽象及其如何映射到 Windows。

* [Pod](/zh-cn/docs/concepts/workloads/pods/)

  Pod 是 Kubernetes 的基本构建块，是可以创建或部署的最小和最简单的单元。
  你不可以在同一个 Pod 中部署 Windows 和 Linux 容器。
  Pod 中的所有容器都调度到同一 Node 上，每个 Node 代表一个特定的平台和体系结构。
  Windows 容器支持以下 Pod 能力、属性和事件：
  * 每个 Pod 有一个或多个容器，具有进程隔离和卷共享能力
  * Pod `status` 字段
  * 就绪、存活和启动探针
  * postStart 和 preStop 容器生命周期回调
  * ConfigMap 和 Secret：作为环境变量或卷
  * `emptyDir` 卷
  * 命名管道形式的主机挂载
  * 资源限制
  * 操作系统字段：

    `.spec.os.name` 字段应设置为 `windows` 以表明当前 Pod 使用 Windows 容器。

    如果你将 `.spec.os.name` 字段设置为 `windows`，
    则你必须不能在对应 Pod 的 `.spec` 中设置以下字段：

    * `spec.hostPID`
    * `spec.hostIPC`
    * `spec.securityContext.seLinuxOptions`
    * `spec.securityContext.seccompProfile`
    * `spec.securityContext.fsGroup`
    * `spec.securityContext.fsGroupChangePolicy`
    * `spec.securityContext.sysctls`
    * `spec.shareProcessNamespace`
    * `spec.securityContext.runAsUser`
    * `spec.securityContext.runAsGroup`
    * `spec.securityContext.supplementalGroups`
    * `spec.containers[*].securityContext.seLinuxOptions`
    * `spec.containers[*].securityContext.seccompProfile`
    * `spec.containers[*].securityContext.capabilities`
    * `spec.containers[*].securityContext.readOnlyRootFilesystem`
    * `spec.containers[*].securityContext.privileged`
    * `spec.containers[*].securityContext.allowPrivilegeEscalation`
    * `spec.containers[*].securityContext.procMount`
    * `spec.containers[*].securityContext.runAsUser`
    * `spec.containers[*].securityContext.runAsGroup`

    在上述列表中，通配符（`*`）表示列表中的所有项。
    例如，`spec.containers[*].securityContext` 指代所有容器的 SecurityContext 对象。
    如果指定了这些字段中的任意一个，则 API 服务器不会接受此 Pod。

* [工作负载资源](/zh-cn/docs/concepts/workloads/controllers/)包括：
  
  * ReplicaSet
  * Deployment
  * StatefulSet
  * DaemonSet
  * Job
  * CronJob
  * ReplicationController

* {{< glossary_tooltip text="Services" term_id="service" >}}

  有关更多详细信息，请参考[负载均衡和 Service](/zh-cn/docs/concepts/services-networking/windows-networking/#load-balancing-and-services)。

Pod、工作负载资源和 Service 是在 Kubernetes 上管理 Windows 工作负载的关键元素。
然而，它们本身还不足以在动态的云原生环境中对 Windows 工作负载进行恰当的生命周期管理。

* `kubectl exec`
* Pod 和容器度量指标
* {{< glossary_tooltip text="Pod 水平自动扩缩容" term_id="horizontal-pod-autoscaler" >}}
* {{< glossary_tooltip text="资源配额" term_id="resource-quota" >}}
* 调度器抢占

### kubelet 的命令行选项 {#kubelet-compatibility}

某些 kubelet 命令行选项在 Windows 上的行为不同，如下所述：

* `--windows-priorityclass` 允许你设置 kubelet 进程的调度优先级
  （参考 [CPU 资源管理](/zh-cn/docs/concepts/configuration/windows-resource-management/#resource-management-cpu)）。
* `--kube-reserved`、`--system-reserved` 和 `--eviction-hard` 标志更新
  [NodeAllocatable](/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable)。
* 未实现使用 `--enforce-node-allocable` 驱逐。
* 未实现使用 `--eviction-hard` 和 `--eviction-soft` 驱逐。
* 在 Windows 节点上运行时，kubelet 没有内存或 CPU 限制。
  `--kube-reserved` 和 `--system-reserved` 仅从 `NodeAllocatable` 中减去，并且不保证为工作负载提供的资源。
  有关更多信息，请参考 [Windows 节点的资源管理](/zh-cn/docs/concepts/configuration/windows-resource-management/#resource-reservation)。
* 未实现 `MemoryPressure` 条件。
* kubelet 不会执行 OOM 驱逐操作。

### API 兼容性 {#api}

由于操作系统和容器运行时的缘故，Kubernetes API 在 Windows 上的工作方式存在细微差异。
某些工作负载属性是为 Linux 设计的，无法在 Windows 上运行。

从较高的层面来看，以下操作系统概念是不同的：

* 身份 - Linux 使用 userID（UID）和 groupID（GID），表示为整数类型。
  用户名和组名是不规范的，它们只是 `/etc/groups` 或 `/etc/passwd` 中的别名，
  作为 UID+GID 的后备标识。
  Windows 使用更大的二进制[安全标识符](https://docs.microsoft.com/zh-cn/windows/security/identity-protection/access-control/security-identifiers)（SID），
  存放在 Windows 安全访问管理器（Security Access Manager，SAM）数据库中。
  此数据库在主机和容器之间或容器之间不共享。
* 文件权限 - Windows 使用基于 SID 的访问控制列表，
  而像 Linux 使用基于对象权限和 UID+GID 的位掩码（POSIX 系统）以及**可选的**访问控制列表。
* 文件路径 - Windows 上的约定是使用 `\` 而不是 `/`。
  Go IO 库通常接受两者，能让其正常工作，但当你设置要在容器内解读的路径或命令行时，
  可能需要用 `\`。

* 信号 - Windows 交互式应用处理终止的方式不同，可以实现以下一种或多种：
  * UI 线程处理包括 `WM_CLOSE` 在内准确定义的消息。
  * 控制台应用使用控制处理程序（Control Handler）处理 Ctrl-C 或 Ctrl-Break。
  * 服务会注册可接受 `SERVICE_CONTROL_STOP` 控制码的服务控制处理程序（Service Control Handler）函数。

容器退出码遵循相同的约定，其中 0 表示成功，非零表示失败。
具体的错误码在 Windows 和 Linux 中可能不同。
但是，从 Kubernetes 组件（kubelet、kube-proxy）传递的退出码保持不变。

#### 容器规约的字段兼容性 {#compatibility-v1-pod-spec-containers}

以下列表记录了 Pod 容器规约在 Windows 和 Linux 之间的工作方式差异：

* 巨页（Huge page）在 Windows 容器运行时中未实现，且不可用。
  巨页需要不可为容器配置的[用户特权生效](https://docs.microsoft.com/zh-cn/windows/win32/memory/large-page-support)。
* `requests.cpu` 和 `requests.memory` -
  从节点可用资源中减去请求，因此请求可用于避免一个节点过量供应。
  但是，请求不能用于保证已过量供应的节点中的资源。
  如果运营商想要完全避免过量供应，则应将设置请求作为最佳实践应用到所有容器。
* `securityContext.allowPrivilegeEscalation` -
  不能在 Windows 上使用；所有权能字都无法生效。
* `securityContext.capabilities` - POSIX 权能未在 Windows 上实现。
* `securityContext.privileged` - Windows 不支持特权容器，
  可使用 [HostProcess 容器](/zh-cn/docs/tasks/configure-pod-container/create-hostprocess-pod/)代替。
* `securityContext.procMount` - Windows 没有 `/proc` 文件系统。
* `securityContext.readOnlyRootFilesystem` -
  不能在 Windows 上使用；对于容器内运行的注册表和系统进程，写入权限是必需的。
* `securityContext.runAsGroup` - 不能在 Windows 上使用，因为不支持 GID。
* `securityContext.runAsNonRoot` -
  此设置将阻止以 `ContainerAdministrator` 身份运行容器，这是 Windows 上与 root 用户最接近的身份。
* `securityContext.runAsUser` - 改用 [`runAsUserName`](/zh-cn/docs/tasks/configure-pod-container/configure-runasusername)。
* `securityContext.seLinuxOptions` - 不能在 Windows 上使用，因为 SELinux 特定于 Linux。
* `terminationMessagePath` - 这个字段有一些限制，因为 Windows 不支持映射单个文件。
  默认值为 `/dev/termination-log`，因为默认情况下它在 Windows 上不存在，所以能生效。

#### Pod 规约的字段兼容性 {#compatibility-v1-pod}

以下列表记录了 Pod 规约在 Windows 和 Linux 之间的工作方式差异：

* `hostIPC` 和 `hostpid` - 不能在 Windows 上共享主机命名空间。
* `hostNetwork` - [参见下文](#compatibility-v1-pod-spec-containers-hostnetwork)
* `dnsPolicy` - Windows 不支持将 Pod `dnsPolicy` 设为 `ClusterFirstWithHostNet`，
  因为未提供主机网络。Pod 始终用容器网络运行。
* `podSecurityContext` [参见下文](#compatibility-v1-pod-spec-containers-securitycontext)
* `shareProcessNamespace` - 这是一个 beta 版功能特性，依赖于 Windows 上未实现的 Linux 命名空间。
  Windows 无法共享进程命名空间或容器的根文件系统（root filesystem）。
  只能共享网络。
* `terminationGracePeriodSeconds` - 这在 Windows 上的 Docker 中没有完全实现，
  请参考 [GitHub issue](https://github.com/moby/moby/issues/25982)。
  目前的行为是通过 CTRL_SHUTDOWN_EVENT 发送 ENTRYPOINT 进程，然后 Windows 默认等待 5 秒，
  最后使用正常的 Windows 关机行为终止所有进程。
  5 秒默认值实际上位于[容器内](https://github.com/moby/moby/issues/25982#issuecomment-426441183)的 Windows 注册表中，
  因此在构建容器时可以覆盖这个值。
* `volumeDevices` - 这是一个 beta 版功能特性，未在 Windows 上实现。
  Windows 无法将原始块设备挂接到 Pod。
* `volumes`
  * 如果你定义一个 `emptyDir` 卷，则你无法将卷源设为 `memory`。
* 你无法为卷挂载启用 `mountPropagation`，因为这在 Windows 上不支持。

#### hostNetwork 的字段兼容性 {#compatibility-v1-pod-spec-containers-hostnetwork}

{{< feature-state for_k8s_version="v1.26" state="alpha" >}}

现在，kubelet 可以请求在 Windows 节点上运行的 Pod 使用主机的网络命名空间，而不是创建新的 Pod 网络命名空间。
要启用此功能，请将 `--feature-gates=WindowsHostNetwork=true` 传递给 kubelet。

{{< note >}}
此功能需要支持该功能的容器运行时。
{{< /note >}}

#### Pod 安全上下文的字段兼容性 {#compatibility-v1-pod-spec-containers-securitycontext}

Pod 的 [`securityContext`](/docs/reference/kubernetes-api/workload-resources/pod-v1/#security-context)
中只有 `securityContext.runAsNonRoot` 和 `securityContext.windowsOptions` 字段在 Windows 上生效。

## 节点问题检测器 {#node-problem-detector}

节点问题检测器（参考[节点健康监测](/zh-cn/docs/tasks/debug/debug-cluster/monitor-node-health/)）初步支持 Windows。
有关更多信息，请访问该项目的 [GitHub 页面](https://github.com/kubernetes/node-problem-detector#windows)。

## Pause 容器 {#pause-container}

在 Kubernetes Pod 中，首先创建一个基础容器或 “pause” 容器来承载容器。
在 Linux 中，构成 Pod 的 cgroup 和命名空间维持持续存在需要一个进程；
而 pause 进程就提供了这个功能。
属于同一 Pod 的容器（包括基础容器和工作容器）共享一个公共网络端点
（相同的 IPv4 和/或 IPv6 地址，相同的网络端口空间）。
Kubernetes 使用 pause 容器以允许工作容器崩溃或重启，而不会丢失任何网络配置。

Kubernetes 维护一个多体系结构的镜像，包括对 Windows 的支持。
对于 Kubernetes v{{< skew currentPatchVersion >}}，推荐的 pause 镜像为 `registry.k8s.io/pause:3.6`。
可在 GitHub 上获得[源代码](https://github.com/kubernetes/kubernetes/tree/master/build/pause)。

Microsoft 维护一个不同的多体系结构镜像，支持 Linux 和 Windows amd64，
你可以找到的镜像类似 `mcr.microsoft.com/oss/kubernetes/pause:3.6`。
此镜像的构建与 Kubernetes 维护的镜像同源，但所有 Windows 可执行文件均由
Microsoft 进行了[验证码签名](https://docs.microsoft.com/zh-cn/windows-hardware/drivers/install/authenticode)。
如果你正部署到一个需要签名可执行文件的生产或类生产环境，
Kubernetes 项目建议使用 Microsoft 维护的镜像。

## 容器运行时 {#container-runtime}

你需要将{{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}安装到集群中的每个节点，
这样 Pod 才能在这些节点上运行。

以下容器运行时适用于 Windows：

{{% thirdparty-content %}}

### ContainerD {#containerd}

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

对于运行 Windows 的 Kubernetes 节点，你可以使用
{{< glossary_tooltip term_id="containerd" text="ContainerD" >}} 1.4.0+ 作为容器运行时。

学习如何[在 Windows 上安装 ContainerD](/zh-cn/docs/setup/production-environment/container-runtimes/#install-containerd)。

{{< note >}}
将 GMSA 和 containerd 一起用于访问 Windows
网络共享时存在[已知限制](/zh-cn/docs/tasks/configure-pod-container/configure-gmsa/#gmsa-limitations)，
这需要一个内核补丁。
{{< /note >}}

### Mirantis 容器运行时 {#mcr}

[Mirantis 容器运行时](https://docs.mirantis.com/mcr/20.10/overview.html)（MCR）
可作为所有 Windows Server 2019 和更高版本的容器运行时。

有关更多信息，请参考[在 Windows Server 上安装 MCR](https://docs.mirantis.com/mcr/20.10/install/mcr-windows.html)。

## Windows 操作系统版本兼容性 {#windows-os-version-support}

在 Windows 节点上，如果主机操作系统版本必须与容器基础镜像操作系统版本匹配，
则会应用严格的兼容性规则。
仅 Windows Server 2019 作为容器操作系统时，才能完全支持 Windows 容器。

对于 Kubernetes v{{< skew currentVersion >}}，Windows 节点（和 Pod）的操作系统兼容性如下：

Windows Server LTSC release
: Windows Server 2019
: Windows Server 2022

Windows Server SAC release
:  Windows Server version 20H2

也适用 Kubernetes [版本偏差策略](/zh-cn/releases/version-skew-policy/)。

## 获取帮助和故障排查 {#troubleshooting}

对 Kubernetes 集群进行故障排查的主要帮助来源应始于[故障排查](/zh-cn/docs/tasks/debug/)页面。

本节包括了一些其他特定于 Windows 的故障排查帮助。
日志是解决 Kubernetes 中问题的重要元素。
确保在任何时候向其他贡献者寻求故障排查协助时随附了日志信息。
遵照 SIG Windows
[日志收集贡献指南](https://github.com/kubernetes/community/blob/master/sig-windows/CONTRIBUTING.md#gathering-logs)中的指示说明。

### 报告问题和功能请求 {#report-issue-and-feature-request}

如果你发现疑似 bug，或者你想提出功能请求，请按照
[SIG Windows 贡献指南](https://github.com/kubernetes/community/blob/master/sig-windows/CONTRIBUTING.md#reporting-issues-and-feature-requests)
新建一个 Issue。
你应该先搜索 issue 列表，以防之前报告过这个问题，凭你对该问题的经验添加评论，
并随附日志信息。
Kubernetes Slack 上的 SIG Windows 频道也是一个很好的途径，
可以在创建工单之前获得一些初始支持和故障排查思路。

## {{% heading "whatsnext" %}}

## 部署工具 {#deployment-tools}

kubeadm 工具帮助你部署 Kubernetes 集群，提供管理集群的控制平面以及运行工作负载的节点。

Kubernetes [集群 API](https://cluster-api.sigs.k8s.io/) 项目也提供了自动部署 Windows 节点的方式。

## Windows 分发渠道 {#windows-distribution-channels}

有关 Windows 分发渠道的详细阐述，请参考
[Microsoft 文档](https://docs.microsoft.com/zh-cn/windows-server/get-started-19/servicing-channels-19)。

有关支持模型在内的不同 Windows Server 服务渠道的信息，请参考
[Windows Server 服务渠道](https://docs.microsoft.com/zh-cn/windows-server/get-started/servicing-channels-comparison)。
