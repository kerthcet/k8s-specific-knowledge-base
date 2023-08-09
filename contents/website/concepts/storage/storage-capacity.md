---
title: 存储容量
content_type: concept
weight: 80
---

存储容量是有限的，并且会因为运行 Pod 的节点不同而变化：
网络存储可能并非所有节点都能够访问，或者对于某个节点存储是本地的。

{{< feature-state for_k8s_version="v1.24" state="stable" >}}

本页面描述了 Kubernetes 如何跟踪存储容量以及调度程序如何为了余下的尚未挂载的卷使用该信息将
[Pod 调度](/zh-cn/docs/concepts/scheduling-eviction/)到能够访问到足够存储容量的节点上。
如果没有跟踪存储容量，调度程序可能会选择一个没有足够容量来提供卷的节点，并且需要多次调度重试。

## {{% heading "prerequisites" %}}

Kubernetes v{{< skew currentVersion >}} 包含了对存储容量跟踪的集群级 API 支持。
要使用它，你还必须使用支持容量跟踪的 CSI 驱动程序。请查阅你使用的 CSI 驱动程序的文档，
以了解此支持是否可用，如果可用，该如何使用它。如果你运行的不是
Kubernetes v{{< skew currentVersion >}}，请查看对应版本的 Kubernetes 文档。

## API

这个特性有两个 API 扩展接口：
- [CSIStorageCapacity](/zh-cn/docs/reference/kubernetes-api/config-and-storage-resources/csi-storage-capacity-v1/) 对象：这些对象由
  CSI 驱动程序在安装驱动程序的命名空间中产生。
  每个对象都包含一个存储类的容量信息，并定义哪些节点可以访问该存储。
- [`CSIDriverSpec.StorageCapacity` 字段](/zh-cn/docs/reference/kubernetes-api/config-and-storage-resources/csi-driver-v1/#CSIDriverSpec)：
  设置为 true 时，Kubernetes 调度程序将考虑使用 CSI 驱动程序的卷的存储容量。

## 调度  {#scheduling}

如果有以下情况，存储容量信息将会被 Kubernetes 调度程序使用：
- Pod 使用的卷还没有被创建，
- 卷使用引用了 CSI 驱动的 {{< glossary_tooltip text="StorageClass" term_id="storage-class" >}}，
  并且使用了 `WaitForFirstConsumer` [卷绑定模式](/zh-cn/docs/concepts/storage/storage-classes/#volume-binding-mode)，
- 驱动程序的 `CSIDriver` 对象的 `StorageCapacity` 被设置为 true。

在这种情况下，调度程序仅考虑将 Pod 调度到有足够存储容量的节点上。这个检测非常简单，
仅将卷的大小与 `CSIStorageCapacity` 对象中列出的容量进行比较，并使用包含该节点的拓扑。

对于具有 `Immediate` 卷绑定模式的卷，存储驱动程序将决定在何处创建该卷，而不取决于将使用该卷的 Pod。
然后，调度程序将 Pod 调度到创建卷后可使用该卷的节点上。

对于 [CSI 临时卷](/zh-cn/docs/concepts/storage/ephemeral-volumes/#csi-ephemeral-volumes)，
调度总是在不考虑存储容量的情况下进行。
这是基于这样的假设：该卷类型仅由节点本地的特殊 CSI 驱动程序使用，并且不需要大量资源。

## 重新调度  {#rescheduling}

当为带有 `WaitForFirstConsumer` 的卷的 Pod 来选择节点时，该决定仍然是暂定的。
下一步是要求 CSI 存储驱动程序创建卷，并提示该卷在被选择的节点上可用。

因为 Kubernetes 可能会根据已经过时的存储容量信息来选择一个节点，因此可能无法真正创建卷。
然后就会重置节点选择，Kubernetes 调度器会再次尝试为 Pod 查找节点。

## 限制  {#limitations}

存储容量跟踪增加了调度器第一次尝试即成功的机会，但是并不能保证这一点，因为调度器必须根据可能过期的信息来进行决策。
通常，与没有任何存储容量信息的调度相同的重试机制可以处理调度失败。

当 Pod 使用多个卷时，调度可能会永久失败：一个卷可能已经在拓扑段中创建，而该卷又没有足够的容量来创建另一个卷，
要想从中恢复，必须要进行手动干预，比如通过增加存储容量或者删除已经创建的卷。

## {{% heading "whatsnext" %}}

- 想要获得更多该设计的信息，查看
  [Storage Capacity Constraints for Pod Scheduling KEP](https://github.com/kubernetes/enhancements/blob/master/keps/sig-storage/1472-storage-capacity-tracking/README.md)。
