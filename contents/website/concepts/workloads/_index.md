---
title: "工作负载"
weight: 55
description: 理解 Pods，Kubernetes 中可部署的最小计算对象，以及辅助它运行它们的高层抽象对象。
---


{{< glossary_definition term_id="workload" length="short" >}}

在 Kubernetes 中，无论你的负载是由单个组件还是由多个一同工作的组件构成，
你都可以在一组 [**Pod**](/zh-cn/docs/concepts/workloads/pods) 中运行它。
在 Kubernetes 中，Pod 代表的是集群上处于运行状态的一组
{{< glossary_tooltip text="容器" term_id="container" >}} 的集合。

Kubernetes Pod 遵循[预定义的生命周期](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/)。
例如，当在你的集群中运行了某个 Pod，但是 Pod 所在的
{{< glossary_tooltip text="节点" term_id="node" >}} 出现致命错误时，
所有该节点上的 Pod 的状态都会变成失败。Kubernetes 将这类失败视为最终状态：
即使该节点后来恢复正常运行，你也需要创建新的 `Pod` 以恢复应用。

不过，为了减轻用户的使用负担，通常不需要用户直接管理每个 `Pod`。
而是使用**负载资源**来替用户管理一组 Pod。
这些负载资源通过配置 {{< glossary_tooltip term_id="controller" text="控制器" >}}
来确保正确类型的、处于运行状态的 Pod 个数是正确的，与用户所指定的状态相一致。

Kubernetes 提供若干种内置的工作负载资源：

* [`Deployment`](/zh-cn/docs/concepts/workloads/controllers/deployment/) 和
  [`ReplicaSet`](/zh-cn/docs/concepts/workloads/controllers/replicaset/)
  （替换原来的资源 {{< glossary_tooltip text="ReplicationController" term_id="replication-controller" >}}）。
  `Deployment` 很适合用来管理你的集群上的无状态应用，`Deployment` 中的所有
  `Pod` 都是相互等价的，并且在需要的时候被替换。
* [StatefulSet](/zh-cn/docs/concepts/workloads/controllers/statefulset/)
  让你能够运行一个或者多个以某种方式跟踪应用状态的 Pod。
  例如，如果你的负载会将数据作持久存储，你可以运行一个 `StatefulSet`，将每个
  `Pod` 与某个 [`PersistentVolume`](/zh-cn/docs/concepts/storage/persistent-volumes/)
  对应起来。你在 `StatefulSet` 中各个 `Pod` 内运行的代码可以将数据复制到同一
  `StatefulSet` 中的其它 `Pod` 中以提高整体的服务可靠性。
* [DaemonSet](/zh-cn/docs/concepts/workloads/controllers/daemonset/)
  定义提供节点本地支撑设施的 `Pod`。这些 Pod 可能对于你的集群的运维是
  非常重要的，例如作为网络链接的辅助工具或者作为网络
  {{< glossary_tooltip text="插件" term_id="addons" >}}
  的一部分等等。每次你向集群中添加一个新节点时，如果该节点与某 `DaemonSet`
  的规约匹配，则控制平面会为该 `DaemonSet` 调度一个 `Pod` 到该新节点上运行。
* [Job](/zh-cn/docs/concepts/workloads/controllers/job/) 和
  [CronJob](/zh-cn/docs/concepts/workloads/controllers/cron-jobs/)。
  定义一些一直运行到结束并停止的任务。`Job` 用来执行一次性任务，而
  `CronJob` 用来执行的根据时间规划反复运行的任务。

在庞大的 Kubernetes 生态系统中，你还可以找到一些提供额外操作的第三方工作负载相关的资源。
通过使用[定制资源定义（CRD）](/zh-cn/docs/concepts/extend-kubernetes/api-extension/custom-resources/)，
你可以添加第三方工作负载资源，以完成原本不是 Kubernetes 核心功能的工作。
例如，如果你希望运行一组 `Pod`，但要求**所有** Pod 都可用时才执行操作
（比如针对某种高吞吐量的分布式任务），你可以基于定制资源实现一个能够满足这一需求的扩展，
并将其安装到集群中运行。

## {{% heading "whatsnext" %}}

除了阅读了解每类资源外，你还可以了解与这些资源相关的任务：

* [使用 `Deployment` 运行一个无状态的应用](/zh-cn/docs/tasks/run-application/run-stateless-application-deployment/)
* 以[单实例](/zh-cn/docs/tasks/run-application/run-single-instance-stateful-application/)或者[多副本集合](/zh-cn/docs/tasks/run-application/run-replicated-stateful-application/)
  的形式运行有状态的应用；
* [使用 `CronJob` 运行自动化的任务](/zh-cn/docs/tasks/job/automated-tasks-with-cron-jobs/)

要了解 Kubernetes 将代码与配置分离的实现机制，可参阅[配置部分](/zh-cn/docs/concepts/configuration/)。

关于 Kubernetes 如何为应用管理 Pod，还有两个支撑概念能够提供相关背景信息：

* [垃圾收集](/zh-cn/docs/concepts/architecture/garbage-collection/)机制负责在
  对象的**属主资源**被删除时在集群中清理这些对象。
* [**Time-to-Live** 控制器](/zh-cn/docs/concepts/workloads/controllers/ttlafterfinished/)会在 Job
  结束之后的指定时间间隔之后删除它们。

一旦你的应用处于运行状态，你就可能想要以
[`Service`](/zh-cn/docs/concepts/services-networking/service/)
的形式使之可在互联网上访问；或者对于 Web 应用而言，使用
[`Ingress`](/zh-cn/docs/concepts/services-networking/ingress) 资源将其暴露到互联网上。
