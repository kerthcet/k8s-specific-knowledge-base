---
title: 安全地清空一个节点
content_type: task
weight: 310
---

本页展示了如何在确保 PodDisruptionBudget 的前提下，
安全地清空一个{{< glossary_tooltip text="节点" term_id="node" >}}。

## {{% heading "prerequisites" %}}

此任务假定你已经满足了以下先决条件：

1. 在节点清空期间，不要求应用具有高可用性
2. 你已经了解了 [PodDisruptionBudget 的概念](/zh-cn/docs/concepts/workloads/pods/disruptions/)，
   并为需要它的应用[配置了 PodDisruptionBudget](/zh-cn/docs/tasks/run-application/configure-pdb/)。


## （可选）配置干扰预算 {#configure-poddisruptionbudget}

为了确保你的负载在维护期间仍然可用，你可以配置一个
[PodDisruptionBudget](/zh-cn/docs/concepts/workloads/pods/disruptions/)。
如果可用性对于正在清空的该节点上运行或可能在该节点上运行的任何应用程序很重要，
首先 [配置一个 PodDisruptionBudgets](/zh-cn/docs/tasks/run-application/configure-pdb/) 并继续遵循本指南。

建议为你的 PodDisruptionBudgets 设置 `AlwaysAllow` 
[不健康 Pod 驱逐策略](/zh-cn/docs/tasks/run-application/configure-pdb/#healthiness-of-a-pod)，
以在节点清空期间支持驱逐异常的应用程序。 
默认行为是等待应用程序的 Pod 变为 [健康](/zh-cn/docs/tasks/run-application/configure-pdb/#healthiness-of-a-pod)后，
才能进行清空操作。

## 使用 `kubectl drain` 从服务中删除一个节点 {#use-kubectl-drain-to-remove-a-node-from-service}

在对节点执行维护（例如内核升级、硬件维护等）之前，
可以使用 `kubectl drain` 从节点安全地逐出所有 Pod。
安全的驱逐过程允许 Pod 的容器[体面地终止](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)，
并确保满足指定的 `PodDisruptionBudgets`。

{{< note >}}
默认情况下，`kubectl drain` 将忽略节点上不能杀死的特定系统 Pod；
有关更多细节，请参阅
[kubectl drain](/docs/reference/generated/kubectl/kubectl-commands/#drain) 文档。
{{< /note >}}

`kubectl drain` 的成功返回，表明所有的 Pod（除了上一段中描述的被排除的那些），
已经被安全地逐出（考虑到期望的终止宽限期和你定义的 PodDisruptionBudget）。
然后就可以安全地关闭节点，
比如关闭物理机器的电源，如果它运行在云平台上，则删除它的虚拟机。

{{< note >}}
如果存在新的、能够容忍 `node.kubernetes.io/unschedulable` 污点的 Pod，
那么这些 Pod 可能会被调度到你已经清空的节点上。
除了 DaemonSet 之外，请避免容忍此污点。

如果你或另一个 API 用户（绕过调度器）直接为 Pod 设置了
[`nodeName`](/zh-cn/docs/concepts/scheduling-eviction/assign-pod-node/#nodename)字段，
则即使你已将该节点清空并标记为不可调度，Pod 仍将被绑定到这个指定的节点并在该节点上运行。
{{< /note >}}

首先，确定想要清空的节点的名称。可以用以下命令列出集群中的所有节点:

```shell
kubectl get nodes
```

接下来，告诉 Kubernetes 清空节点：

```shell
kubectl drain --ignore-daemonsets <节点名称>
```

如果存在 DaemonSet 管理的 Pod，你将需要为 `kubectl` 设置 `--ignore-daemonsets` 以成功地清空节点。
`kubectl drain` 子命令自身实际上不清空节点上的 DaemonSet Pod 集合：
DaemonSet 控制器（作为控制平面的一部分）会立即用新的等效 Pod 替换缺少的 Pod。
DaemonSet 控制器还会创建忽略不可调度污点的 Pod，这种污点允许在你正在清空的节点上启动新的 Pod。

一旦它返回（没有报错），
你就可以下线此节点（或者等价地，如果在云平台上，删除支持该节点的虚拟机）。
如果要在维护操作期间将节点留在集群中，则需要运行：

```shell
kubectl uncordon <node name>
```
然后告诉 Kubernetes，它可以继续在此节点上调度新的 Pod。

## 并行清空多个节点  {#draining-multiple-nodes-in-parallel}

`kubectl drain` 命令一次只能发送给一个节点。
但是，你可以在不同的终端或后台为不同的节点并行地运行多个 `kubectl drain` 命令。
同时运行的多个 drain 命令仍然遵循你指定的 `PodDisruptionBudget`。

例如，如果你有一个三副本的 StatefulSet，
并设置了一个 `PodDisruptionBudget`，指定 `minAvailable: 2`。
如果所有的三个 Pod 处于[健康（healthy）](/zh-cn/docs/tasks/run-application/configure-pdb/#healthiness-of-a-pod)状态，
并且你并行地发出多个 drain 命令，那么 `kubectl drain` 只会从 StatefulSet 中逐出一个 Pod，
因为 Kubernetes 会遵守 PodDisruptionBudget 并确保在任何时候只有一个 Pod 不可用
（最多不可用 Pod 个数的计算方法：`replicas - minAvailable`）。
任何会导致处于[健康（healthy）](/zh-cn/docs/tasks/run-application/configure-pdb/#healthiness-of-a-pod)
状态的副本数量低于指定预算的清空操作都将被阻止。

## 驱逐 API {#the-eviction-api}

如果你不喜欢使用
[kubectl drain](/docs/reference/generated/kubectl/kubectl-commands/#drain)
（比如避免调用外部命令，或者更细化地控制 Pod 驱逐过程），
你也可以用驱逐 API 通过编程的方式达到驱逐的效果。
更多信息，请参阅 [API 发起的驱逐](/zh-cn/docs/concepts/scheduling-eviction/api-eviction/)。

## {{% heading "whatsnext" %}}

* 执行[配置 PDB](/zh-cn/docs/tasks/run-application/configure-pdb/) 中的各个步骤，
  保护你的应用。
