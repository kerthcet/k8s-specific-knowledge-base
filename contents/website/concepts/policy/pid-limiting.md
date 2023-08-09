---
title: 进程 ID 约束与预留
content_type: concept
weight: 40
---



{{< feature-state for_k8s_version="v1.20" state="stable" >}}

Kubernetes 允许你限制一个 {{< glossary_tooltip term_id="Pod" text="Pod" >}}
中可以使用的进程 ID（PID）数目。
你也可以为每个{{< glossary_tooltip term_id="node" text="节点" >}}预留一定数量的可分配的 PID，
供操作系统和守护进程（而非 Pod）使用。


进程 ID（PID）是节点上的一种基础资源。很容易就会在尚未超出其它资源约束的时候就已经触及任务个数上限，
进而导致宿主机器不稳定。

集群管理员需要一定的机制来确保集群中运行的 Pod 不会导致 PID 资源枯竭，
甚而造成宿主机上的守护进程（例如
{{< glossary_tooltip text="kubelet" term_id="kubelet" >}} 或者
{{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}}
乃至包括容器运行时本身）无法正常运行。
此外，确保 Pod 中 PID 的个数受限对于保证其不会影响到同一节点上其它负载也很重要。

{{< note >}}
在某些 Linux 安装环境中，操作系统会将 PID 约束设置为一个较低的默认值，例如
`32768`。这时可以考虑提升 `/proc/sys/kernel/pid_max` 的设置值。
{{< /note >}}

你可以配置 kubelet 限制给定 Pod 能够使用的 PID 个数。
例如，如果你的节点上的宿主操作系统被设置为最多可使用 `262144` 个 PID，
同时预期节点上会运行的 Pod 个数不会超过 `250`，那么你可以为每个 Pod 设置 `1000` 个 PID
的预算，避免耗尽该节点上可用 PID 的总量。
如果管理员系统像 CPU 或内存那样允许对 PID 进行过量分配（Overcommit），他们也可以这样做，
只是会有一些额外的风险。不管怎样，任何一个 Pod 都不可以将整个机器的运行状态破坏。
这类资源限制有助于避免简单的派生炸弹（Fork Bomb）影响到整个集群的运行。

在 Pod 级别设置 PID 限制使得管理员能够保护 Pod 之间不会互相伤害，
不过无法确保所有调度到该宿主机器上的所有 Pod 都不会影响到节点整体。
Pod 级别的限制也无法保护节点代理任务自身不会受到 PID 耗尽的影响。

你也可以预留一定量的 PID，作为节点的额外开销，与分配给 Pod 的 PID 集合独立。
这有点类似于在给操作系统和其它设施预留 CPU、内存或其它资源时所做的操作，
这些任务都在 Pod 及其所包含的容器之外运行。

PID 限制是与[计算资源](/zh-cn/docs/concepts/configuration/manage-resources-containers/)
请求和限制相辅相成的一种机制。不过，你需要用一种不同的方式来设置这一限制：
你需要将其设置到 kubelet 上而不是在 Pod 的 `.spec` 中为 Pod 设置资源限制。
目前还不支持在 Pod 级别设置 PID 限制。

{{< caution >}}
这意味着，施加在 Pod 之上的限制值可能因为 Pod 运行所在的节点不同而有差别。
为了简化系统，最简单的方法是为所有节点设置相同的 PID 资源限制和预留值。
{{< /caution >}}

## 节点级别 PID 限制   {#node-pid-limits}

Kubernetes 允许你为系统预留一定量的进程 ID。为了配置预留数量，你可以使用
kubelet 的 `--system-reserved` 和 `--kube-reserved` 命令行选项中的参数
`pid=<number>`。你所设置的参数值分别用来声明为整个系统和 Kubernetes
系统守护进程所保留的进程 ID 数目。

## Pod 级别 PID 限制   {#pod-pid-limits}

Kubernetes 允许你限制 Pod 中运行的进程个数。你可以在节点级别设置这一限制，
而不是为特定的 Pod 来将其设置为资源限制。每个节点都可以有不同的 PID 限制设置。
要设置限制值，你可以设置 kubelet 的命令行参数 `--pod-max-pids`，或者在 kubelet
的[配置文件](/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/)中设置
`PodPidsLimit`。

## 基于 PID 的驱逐    {#pid-based-eviction}

你可以配置 kubelet 使之在 Pod 行为不正常或者消耗不正常数量资源的时候将其终止。这一特性称作驱逐。
你可以针对不同的驱逐信号[配置资源不足的处理](/zh-cn/docs/concepts/scheduling-eviction/node-pressure-eviction/)。
使用 `pid.available` 驱逐信号来配置 Pod 使用的 PID 个数的阈值。
你可以设置硬性的和软性的驱逐策略。不过，即使使用硬性的驱逐策略，
如果 PID 个数增长过快，节点仍然可能因为触及节点 PID 限制而进入一种不稳定状态。
驱逐信号的取值是周期性计算的，而不是一直能够强制实施约束。

Pod 级别和节点级别的 PID 限制会设置硬性限制。
一旦触及限制值，工作负载会在尝试获得新的 PID 时开始遇到问题。
这可能会也可能不会导致 Pod 被重新调度，取决于工作负载如何应对这类失败以及
Pod 的存活性和就绪态探测是如何配置的。
可是，如果限制值被正确设置，你可以确保其它 Pod 负载和系统进程不会因为某个
Pod 行为不正常而没有 PID 可用。

## {{% heading "whatsnext" %}}

- 参阅 [PID 约束改进文档](https://github.com/kubernetes/enhancements/blob/097b4d8276bc9564e56adf72505d43ce9bc5e9e8/keps/sig-node/20190129-pid-limiting.md)
  以了解更多信息。
- 关于历史背景，请阅读
  [Kubernetes 1.14 中限制进程 ID 以提升稳定性](/blog/2019/04/15/process-id-limiting-for-stability-improvements-in-kubernetes-1.14/)
  的博文。
- 请阅读[为容器管理资源](/zh-cn/docs/concepts/configuration/manage-resources-containers/)。
- 学习如何[配置资源不足情况的处理](/zh-cn/docs/concepts/scheduling-eviction/node-pressure-eviction/)。

