---
layout: blog
title: "Kueue 介绍"
date: 2022-10-04
slug: introducing-kueue
---

**作者：** Abdullah Gharaibeh（谷歌），Aldo Culquicondor（谷歌）

无论是在本地还是在云端，集群都面临着资源使用、配额和成本管理方面的实际限制。
无论自动扩缩容能力如何，集群的容量都是有限的。
因此，用户需要一种简单的方法来公平有效地共享资源。

在本文中，我们介绍了 [Kueue](https://github.com/kubernetes-sigs/kueue/tree/main/docs#readme)，
这是一个开源作业队列控制器，旨在将批处理作业作为一个单元进行管理。
Kueue 将 Pod 级编排留给 Kubernetes 现有的稳定组件。
Kueue 原生支持 Kubernetes [Job](/zh-cn/docs/concepts/workloads/controllers/job/) API，
并提供用于集成其他定制 API 以进行批处理作业的钩子。

## 为什么是 Kueue?
作业队列是在本地和云环境中大规模运行批处理工作负载的关键功能。
作业队列的主要目标是管理对多个租户共享的有限资源池的访问。
作业排队决定了哪些作业应该等待，哪些可以立即启动，以及它们可以使用哪些资源。

一些最需要的作业队列要求包括：
- 用配额和预算来控制谁可以使用什么以及达到什么限制。
  这不仅在具有静态资源（如本地）的集群中需要，而且在云环境中也需要控制稀缺资源的支出或用量。
- 租户之间公平共享资源。
  为了最大限度地利用可用资源，应允许活动租户公平共享那些分配给非活动租户的未使用配额。
- 根据可用性，在不同资源类型之间灵活放置作业。
  这在具有异构资源的云环境中很重要，例如不同的架构（GPU 或 CPU 模型）和不同的供应模式（即用与按需）。
- 支持可按需配置资源的自动扩缩容环境。

普通的 Kubernetes 不能满足上述要求。
在正常情况下，一旦创建了 Job，Job 控制器会立即创建 Pod，并且 kube-scheduler 会不断尝试将 Pod 分配给节点。
大规模使用时，这种情况可能会使控制平面死机。
目前也没有好的办法在 Job 层面控制哪些 Job 应该先获得哪些资源，也没有办法标明顺序或公平共享。
当前的 ResourceQuota 模型不太适合这些需求，因为配额是在资源创建时强制执行的，并且没有请求排队。
ResourceQuotas 的目的是提供一种内置的可靠性机制，其中包含管理员所需的策略，以防止集群发生故障转移。

在 Kubernetes 生态系统中，Job 调度有多种解决方案。但是，我们发现这些替代方案存在以下一个或多个问题：
- 它们取代了 Kubernetes 的现有稳定组件，例如 kube-scheduler 或 Job 控制器。
  这不仅从操作的角度看是有问题的，而且重复的 Job API 也会导致生态系统的碎片化并降低可移植性。
- 它们没有集成自动扩缩容，或者
- 它们缺乏对资源灵活性的支持。 

## Kueue 的工作原理 {#overview}
借助 Kueue，我们决定采用不同的方法在 Kubernetes 上进行 Job 排队，该方法基于以下方面：
- 不复制已建立的 Kubernetes 组件提供的用于 Pod 调度、自动扩缩容和 Job 生命周期管理的现有功能。
- 将缺少的关键特性添加到现有组件中。例如，我们投资了 Job API 以涵盖更多用例，像 [IndexedJob](/blog/2021/04/19/introducing-indexed-jobs)，
  并[修复了与 Pod 跟踪相关的长期存在的问题](/zh-cn/docs/concepts/workloads/controllers/job/#job-tracking-with-finalizers)。
  虽然离特性落地还有很长一段路，但我们相信这是可持续的长期解决方案。
- 确保与具有弹性和异构性的计算资源云环境兼容。

为了使这种方法可行，Kueue 需要旋钮来影响那些已建立组件的行为，以便它可以有效地管理何时何地启动一个 Job。
我们以两个特性的方式将这些旋钮添加到 Job API：
- [Suspend 字段](/zh-cn/docs/concepts/workloads/controllers/job/#suspending-a-job)，
  它允许在 Job 启动或停止时，Kueue 向 Job 控制器发出信号。
- [可变调度指令](/zh-cn/docs/concepts/workloads/controllers/job/#mutable-scheduling-directives)，
  允许在启动 Job 之前更新 Job 的 `.spec.template.spec.nodeSelector`。
  这样，Kueue 可以控制 Pod 放置，同时仍将 Pod 到节点的实际调度委托给 kube-scheduler。

请注意，任何自定义的 Job API 都可以由 Kueue 管理，只要该 API 提供上述两种能力。

### 资源模型
Kueue 定义了新的 API 来解决本文开头提到的需求。三个主要的 API 是：
- ResourceFlavor：一个集群范围的 API，用于定义可供消费的资源模板，如 GPU 模型。
  ResourceFlavor 的核心是一组标签，这些标签反映了提供这些资源的节点上的标签。
- ClusterQueue: 一种集群范围的 API，通过为一个或多个 ResourceFlavor 设置配额来定义资源池。
- LocalQueue: 用于分组和管理单租户 Jobs 的命名空间 API。
  在最简单的形式中，LocalQueue 是指向集群队列的指针，租户（建模为命名空间）可以使用它来启动他们的 Jobs。

有关更多详细信息，请查看 [API 概念文档](https://sigs.k8s.io/kueue/docs/concepts)。
虽然这三个 API 看起来无法抗拒，但 Kueue 的大部分操作都以 ClusterQueue 为中心；
ResourceFlavor 和 LocalQueue API 主要是组织包装器。

### 用例样例
想象一下在云上的 Kubernetes 集群上运行批处理工作负载的以下设置：
- 你在集群中安装了 [cluster-autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) 以自动调整集群的大小。
- 有两种类型的自动缩放节点组，它们的供应策略不同：即用和按需。
  分别对应标签：`instance-type=spot` 或者 `instance-type=ondemand`。
  此外，并非所有作业都可以容忍在即用节点上运行，节点可以用 `spot=true:NoSchedule` 污染。
- 为了在成本和资源可用性之间取得平衡，假设你希望 Jobs 使用最多 1000 个核心按需节点，最多 2000 个核心即用节点。

作为批处理系统的管理员，你定义了两个 ResourceFlavor，它们代表两种类型的节点：

```yaml
---
apiVersion: kueue.x-k8s.io/v1alpha2
kind: ResourceFlavor
metadata:
  name: ondemand
  labels:
    instance-type: ondemand 
---
apiVersion: kueue.x-k8s.io/v1alpha2
kind: ResourceFlavor
metadata:
  name: spot
  labels:
    instance-type: spot
taints:
- effect: NoSchedule
  key: spot
  value: "true"
```
然后通过创建 ClusterQueue 来定义配额，如下所示：
```yaml
apiVersion: kueue.x-k8s.io/v1alpha2
kind: ClusterQueue
metadata:
  name: research-pool
spec:
  namespaceSelector: {}
  resources:
  - name: "cpu"
    flavors:
    - name: ondemand
      quota:
        min: 1000
    - name: spot
      quota:
        min: 2000
```

注意 ClusterQueue 资源中的模板顺序很重要：Kueue 将尝试根据该顺序为 Job 分配可用配额，除非这些 Job 与特定模板有明确的关联。

对于每个命名空间，定义一个指向上述 ClusterQueue 的 LocalQueue：

```yaml
apiVersion: kueue.x-k8s.io/v1alpha2
kind: LocalQueue
metadata:
  name: training
  namespace: team-ml
spec:
  clusterQueue: research-pool
```

管理员创建一次上述配置。批处理用户可以通过在他们的命名空间中列出 LocalQueues 来找到他们被允许提交的队列。
该命令类似于：`kubectl get -n my-namespace localqueues`

要提交作业，需要创建一个 Job 并设置 `kueue.x-k8s.io/queue-name` 注解，如下所示：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  annotations:
    kueue.x-k8s.io/queue-name: training
spec:
  parallelism: 3
  completions: 3
  template:
    spec:
      tolerations:
      - key: spot
        operator: "Exists"
        effect: "NoSchedule"
      containers:
      - name: example-batch-workload
        image: registry.example/batch/calculate-pi:3.14
        args: ["30s"]
        resources:
          requests:
            cpu: 1
      restartPolicy: Never
```

Kueue 在创建 Job 后立即进行干预以暂停 Job。
一旦 Job 位于 ClusterQueue 的头部，Kueue 就会通过检查 Job 请求的资源是否符合可用配额来评估它是否可以启动。 

在上面的例子中，Job 容忍了 Spot 资源。如果之前承认的 Job 消耗了所有现有的按需配额，
但不是所有 Spot 配额，则 Kueue 承认使用 Spot 配额的 Job。Kueue 通过向 Job 对象发出单个更新来做到这一点：
- 更改 `.spec.suspend` 标志位为 false 
- 将 `instance-type: spot` 添加到 Job 的 `.spec.template.spec.nodeSelector` 中，
以便在 Job 控制器创建 Pod 时，这些 Pod 只能调度到 Spot 节点上。

最后，如果有可用的空节点与节点选择器条件匹配，那么 kube-scheduler 将直接调度 Pod。
如果不是，那么 kube-scheduler 将 pod 初始化标记为不可调度，这将触发 cluster-autoscaler 配置新节点。

## 未来工作以及参与方式
上面的示例提供了 Kueue 的一些功能简介，包括支持配额、资源灵活性以及与集群自动缩放器的集成。
Kueue 还支持公平共享、Job 优先级和不同的排队策略。
查看 [Kueue 文档](https://github.com/kubernetes-sigs/kueue/tree/main/docs)以了解这些特性以及如何使用 Kueue 的更多信息。

我们计划将许多特性添加到 Kueue 中，例如分层配额、预算和对动态大小 Job 的支持。
在不久的将来，我们将专注于增加对 Job 抢占的支持。

最新的 [Kueue 版本](https://github.com/kubernetes-sigs/kueue/releases)在 Github 上可用；
如果你在 Kubernetes 上运行批处理工作负载（需要 v1.22 或更高版本），可以尝试一下。
这个项目还处于早期阶段，我们正在搜集大大小小各个方面的反馈，请不要犹豫，快来联系我们吧！
无论是修复或报告错误，还是帮助添加新特性或编写文档，我们欢迎一切形式的贡献者。
你可以通过我们的[仓库](http://sigs.k8s.io/kueue)、[邮件列表](https://groups.google.com/a/kubernetes.io/g/wg-batch)或者 
[Slack](https://kubernetes.slack.com/messages/wg-batch) 与我们联系。

最后是很重要的一点，感谢所有促使这个项目成为可能的[贡献者们](https://github.com/kubernetes-sigs/kueue/graphs/contributors)！
