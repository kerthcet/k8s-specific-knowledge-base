---
title: 控制器
content_type: concept
weight: 30
---


在机器人技术和自动化领域，控制回路（Control Loop）是一个非终止回路，用于调节系统状态。

这是一个控制环的例子：房间里的温度自动调节器。

当你设置了温度，告诉了温度自动调节器你的**期望状态（Desired State）**。
房间的实际温度是**当前状态（Current State）**。
通过对设备的开关控制，温度自动调节器让其当前状态接近期望状态。

{{< glossary_definition term_id="controller" length="short">}}

## 控制器模式 {#controller-pattern}

一个控制器至少追踪一种类型的 Kubernetes 资源。这些
{{< glossary_tooltip text="对象" term_id="object" >}}
有一个代表期望状态的 `spec` 字段。
该资源的控制器负责确保其当前状态接近期望状态。

控制器可能会自行执行操作；在 Kubernetes 中更常见的是一个控制器会发送信息给
{{< glossary_tooltip text="API 服务器" term_id="kube-apiserver" >}}，这会有副作用。
具体可参看后文的例子。

{{< comment >}}
一些内置的控制器，比如名字空间控制器，针对没有指定 `spec` 的对象。
为了简单起见，本文没有详细介绍这些细节。
{{< /comment >}}


### 通过 API 服务器来控制 {#control-via-API-server}

{{< glossary_tooltip text="Job" term_id="job" >}} 控制器是一个 Kubernetes 内置控制器的例子。
内置控制器通过和集群 API 服务器交互来管理状态。

Job 是一种 Kubernetes 资源，它运行一个或者多个 {{< glossary_tooltip term_id="pod" >}}，
来执行一个任务然后停止。
（一旦[被调度了](/zh-cn/docs/concepts/scheduling-eviction/)，对 `kubelet` 来说 Pod
对象就会变成了期望状态的一部分）。

在集群中，当 Job 控制器拿到新任务时，它会保证一组 Node 节点上的 `kubelet`
可以运行正确数量的 Pod 来完成工作。
Job 控制器不会自己运行任何的 Pod 或者容器。Job 控制器是通知 API 服务器来创建或者移除 Pod。
{{< glossary_tooltip text="控制面" term_id="control-plane" >}}中的其它组件
根据新的消息作出反应（调度并运行新 Pod）并且最终完成工作。

创建新 Job 后，所期望的状态就是完成这个 Job。Job 控制器会让 Job 的当前状态不断接近期望状态：创建为 Job 要完成工作所需要的 Pod，使 Job 的状态接近完成。

控制器也会更新配置对象。例如：一旦 Job 的工作完成了，Job 控制器会更新 Job 对象的状态为 `Finished`。

（这有点像温度自动调节器关闭了一个灯，以此来告诉你房间的温度现在到你设定的值了）。


### 直接控制 {#direct-control}

相比 Job 控制器，有些控制器需要对集群外的一些东西进行修改。

例如，如果你使用一个控制回路来保证集群中有足够的
{{< glossary_tooltip text="节点" term_id="node" >}}，那么控制器就需要当前集群外的
一些服务在需要时创建新节点。

和外部状态交互的控制器从 API 服务器获取到它想要的状态，然后直接和外部系统进行通信
并使当前状态更接近期望状态。

（实际上有一个[控制器](https://github.com/kubernetes/autoscaler/)
可以水平地扩展集群中的节点。）

这里的重点是，控制器做出了一些变更以使得事物更接近你的期望状态，
之后将当前状态报告给集群的 API 服务器。
其他控制回路可以观测到所汇报的数据的这种变化并采取其各自的行动。

在温度计的例子中，如果房间很冷，那么某个控制器可能还会启动一个防冻加热器。
就 Kubernetes 集群而言，控制面间接地与 IP 地址管理工具、存储服务、云驱动
APIs 以及其他服务协作，通过[扩展 Kubernetes](/zh-cn/docs/concepts/extend-kubernetes/)
来实现这点。

## 期望状态与当前状态 {#desired-vs-current}

Kubernetes 采用了系统的云原生视图，并且可以处理持续的变化。

在任务执行时，集群随时都可能被修改，并且控制回路会自动修复故障。
这意味着很可能集群永远不会达到稳定状态。

只要集群中的控制器在运行并且进行有效的修改，整体状态的稳定与否是无关紧要的。

## 设计 {#design}

作为设计原则之一，Kubernetes 使用了很多控制器，每个控制器管理集群状态的一个特定方面。
最常见的一个特定的控制器使用一种类型的资源作为它的期望状态，
控制器管理控制另外一种类型的资源向它的期望状态演化。
例如，Job 的控制器跟踪 Job 对象（以发现新的任务）和 Pod 对象（以运行 Job，然后查看任务何时完成）。
在这种情况下，新任务会创建 Job，而 Job 控制器会创建 Pod。

使用简单的控制器而不是一组相互连接的单体控制回路是很有用的。
控制器会失败，所以 Kubernetes 的设计正是考虑到了这一点。

{{< note >}}
可以有多个控制器来创建或者更新相同类型的对象。
在后台，Kubernetes 控制器确保它们只关心与其控制资源相关联的资源。

例如，你可以创建 Deployment 和 Job；它们都可以创建 Pod。
Job 控制器不会删除 Deployment 所创建的 Pod，因为有信息
（{{< glossary_tooltip term_id="label" text="标签" >}}）让控制器可以区分这些 Pod。
{{< /note >}}

## 运行控制器的方式 {#running-controllers}

Kubernetes 内置一组控制器，运行在 {{< glossary_tooltip term_id="kube-controller-manager" >}} 内。
这些内置的控制器提供了重要的核心功能。

Deployment 控制器和 Job 控制器是 Kubernetes 内置控制器的典型例子。
Kubernetes 允许你运行一个稳定的控制平面，这样即使某些内置控制器失败了，
控制平面的其他部分会接替它们的工作。

你会遇到某些控制器运行在控制面之外，用以扩展 Kubernetes。
或者，如果你愿意，你也可以自己编写新控制器。
你可以以一组 Pod 来运行你的控制器，或者运行在 Kubernetes 之外。
最合适的方案取决于控制器所要执行的功能是什么。

## {{% heading "whatsnext" %}}
* 阅读 [Kubernetes 控制平面组件](/zh-cn/docs/concepts/overview/components/#control-plane-components)
* 了解 [Kubernetes 对象](/zh-cn/docs/concepts/overview/working-with-objects/)
  的一些基本知识
* 进一步学习 [Kubernetes API](/zh-cn/docs/concepts/overview/kubernetes-api/)
* 如果你想编写自己的控制器，请看 Kubernetes 的
  [扩展模式](/zh-cn/docs/concepts/extend-kubernetes/#extension-patterns)。
