---
title: Pod QoS 类
content_type: concept
weight: 85
---


本页介绍 Kubernetes 中的 **服务质量（Quality of Service，QoS）** 类，
阐述 Kubernetes 如何根据为 Pod 中的容器指定的资源约束为每个 Pod 设置 QoS 类。
Kubernetes 依赖这种分类来决定当 Node 上没有足够可用资源时要驱逐哪些 Pod。


## QoS 类   {#qos-class}

Kubernetes 对你运行的 Pod 进行分类，并将每个 Pod 分配到特定的 **QoS 类**中。
Kubernetes 使用这种分类来影响不同 Pod 被处理的方式。Kubernetes 基于 Pod
中{{< glossary_tooltip text="容器" term_id="container" >}}的[资源请求](/zh-cn/docs/concepts/configuration/manage-resources-containers/)进行分类，
同时确定这些请求如何与资源限制相关。
这称为{{< glossary_tooltip text="服务质量" term_id="qos-class" >}} (QoS) 类。
Kubernetes 基于每个 Pod 中容器的资源请求和限制为 Pod 设置 QoS 类。Kubernetes 使用 QoS
类来决定从遇到[节点压力](/zh-cn/docs/concepts/scheduling-eviction/node-pressure-eviction/)的
Node 中驱逐哪些 Pod。可选的 QoS 类有 `Guaranteed`、`Burstable` 和 `BestEffort`。
当一个 Node 耗尽资源时，Kubernetes 将首先驱逐在该 Node 上运行的 `BestEffort` Pod，
然后是 `Burstable` Pod，最后是 `Guaranteed` Pod。当这种驱逐是由于资源压力时，
只有超出资源请求的 Pod 才是被驱逐的候选对象。

### Guaranteed

`Guaranteed` Pod 具有最严格的资源限制，并且最不可能面临驱逐。
在这些 Pod 超过其自身的限制或者没有可以从 Node 抢占的低优先级 Pod 之前，
这些 Pod 保证不会被杀死。这些 Pod 不可以获得超出其指定 limit 的资源。这些 Pod 也可以使用
[`static`](/zh-cn/docs/tasks/administer-cluster/cpu-management-policies/#static-policy)
CPU 管理策略来使用独占的 CPU。

#### 判据   {#criteria}

Pod 被赋予 `Guaranteed` QoS 类的几个判据：

* Pod 中的每个容器必须有内存 limit 和内存 request。
* 对于 Pod 中的每个容器，内存 limit 必须等于内存 request。
* Pod 中的每个容器必须有 CPU limit 和 CPU request。
* 对于 Pod 中的每个容器，CPU limit 必须等于 CPU request。

### Burstable

`Burstable` Pod 有一些基于 request 的资源下限保证，但不需要特定的 limit。
如果未指定 limit，则默认为其 limit 等于 Node 容量，这允许 Pod 在资源可用时灵活地增加其资源。
在由于 Node 资源压力导致 Pod 被驱逐的情况下，只有在所有 `BestEffort` Pod 被驱逐后
这些 Pod 才会被驱逐。因为 `Burstable` Pod 可以包括没有资源 limit 或资源 request 的容器，
所以 `Burstable` Pod 可以尝试使用任意数量的节点资源。

#### 判据   {#criteria-1}

Pod 被赋予 `Burstable` QoS 类的几个判据：

* Pod 不满足针对 QoS 类 `Guaranteed` 的判据。
* Pod 中至少一个容器有内存或 CPU 的 request 或 limit。

### BestEffort

`BestEffort` QoS 类中的 Pod 可以使用未专门分配给其他 QoS 类中的 Pod 的节点资源。
例如若你有一个节点有 16 核 CPU 可供 kubelet 使用，并且你将 4 核 CPU 分配给一个 `Guaranteed` Pod，
那么 `BestEffort` QoS 类中的 Pod 可以尝试任意使用剩余的 12 核 CPU。

如果节点遇到资源压力，kubelet 将优先驱逐 `BestEffort` Pod。

#### 判据   {#criteria-2}

如果 Pod 不满足 `Guaranteed` 或 `Burstable` 的判据，则它的 QoS 类为 `BestEffort`。
换言之，只有当 Pod 中的所有容器没有内存 limit 或内存 request，也没有 CPU limit 或
CPU request 时，Pod 才是 `BestEffort`。Pod 中的容器可以请求（除 CPU 或内存之外的）
其他资源并且仍然被归类为 `BestEffort`。

## 使用 cgroup v2 的内存 QoS   {#memory-qos-with-cgroup-v2}

{{< feature-state for_k8s_version="v1.22" state="alpha" >}}

内存 QoS 使用 cgroup v2 的内存控制器来保证 Kubernetes 中的内存资源。
Pod 中容器的内存请求和限制用于设置由内存控制器所提供的特定接口 `memory.min` 和 `memory.high`。
当 `memory.min` 被设置为内存请求时，内存资源被保留并且永远不会被内核回收；
这就是内存 QoS 确保 Kubernetes Pod 的内存可用性的方式。而如果容器中设置了内存限制，
这意味着系统需要限制容器内存的使用；内存 QoS 使用 `memory.high` 来限制接近其内存限制的工作负载，
确保系统不会因瞬时内存分配而不堪重负。

内存 QoS 依赖于 QoS 类来确定应用哪些设置；它们的机制不同，但都提供对服务质量的控制。

## 某些行为独立于 QoS 类 {#class-independent-behavior}

某些行为独立于 Kubernetes 分配的 QoS 类。例如：

* 所有超过资源 limit 的容器都将被 kubelet 杀死并重启，而不会影响该 Pod 中的其他容器。
* 如果一个容器超出了自身的资源 request，且该容器运行的节点面临资源压力，则该容器所在的 Pod
  就会成为被[驱逐](/zh-cn/docs/concepts/scheduling-eviction/node-pressure-eviction/)的候选对象。
  如果出现这种情况，Pod 中的所有容器都将被终止。Kubernetes 通常会在不同的节点上创建一个替代的 Pod。
* Pod 的资源 request 等于其成员容器的资源 request 之和，Pod 的资源 limit 等于其成员容器的资源 limit 之和。
* kube-scheduler 在选择要[抢占](/zh-cn/docs/concepts/scheduling-eviction/pod-priority-preemption/#preemption)的
  Pod 时不考虑 QoS 类。当集群没有足够的资源来运行你所定义的所有 Pod 时，就会发生抢占。

## {{% heading "whatsnext" %}}

* 进一步了解[为 Pod 和容器管理资源](/zh-cn/docs/concepts/configuration/manage-resources-containers/)。
* 进一步了解[节点压力驱逐](/zh-cn/docs/concepts/scheduling-eviction/node-pressure-eviction/)。
* 进一步了解 [Pod 优先级和抢占](/zh-cn/docs/concepts/scheduling-eviction/pod-priority-preemption/)。
* 进一步了解 [Pod 干扰](/zh-cn/docs/concepts/workloads/pods/disruptions/)。
* 进一步了解如何[为容器和 Pod 分配内存资源](/zh-cn/docs/tasks/configure-pod-container/assign-memory-resource/)。
* 进一步了解如何[为容器和 Pod 分配 CPU 资源](/zh-cn/docs/tasks/configure-pod-container/assign-cpu-resource/)。
* 进一步了解如何[配置 Pod 的服务质量](/zh-cn/docs/tasks/configure-pod-container/quality-service-pod/)。
