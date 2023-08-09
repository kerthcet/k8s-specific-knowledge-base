---
layout: blog
title: 'Kubernetes 1.23: StatefulSet PVC 自动删除 (alpha)'
date: 2021-12-16
slug: kubernetes-1-23-statefulset-pvc-auto-deletion
---

**作者:** Matthew Cary (谷歌)

Kubernetes v1.23 为 [StatefulSets](/zh-cn/docs/concepts/workloads/controllers/statefulset/)
引入了一个新的 alpha 级策略，用来控制由 StatefulSet 规约模板生成的
[PersistentVolumeClaims](/zh-cn/docs/concepts/storage/persistent-volumes/) (PVCs) 的生命周期，
用于当删除 StatefulSet 或减少 StatefulSet 中的 Pods 数量时 PVCs 应该被自动删除的场景。

## 它解决了什么问题？

StatefulSet 规约中可以包含 Pod 和 PVC 的模板。当副本先被创建时，如果 PVC 还不存在，
Kubernetes 控制面会为该副本自动创建一个 PVC。在 Kubernetes 1.23 版本之前，
控制面不会删除 StatefulSet 创建的 PVCs——这依赖集群管理员或你需要部署一些额外的适用的自动化工具来处理。
管理 PVC 的常见模式是通过手动或使用 Helm 等工具，PVC 的具体生命周期由管理它的工具跟踪。
使用 StatefulSet 时必须自行确定 StatefulSet 创建哪些 PVC，以及它们的生命周期应该是什么。

在这个新特性之前，当一个 StatefulSet 管理的副本消失时，无论是因为 StatefulSet 减少了它的副本数，
还是因为它的 StatefulSet 被删除了，PVC 及其下层的卷仍然存在，需要手动删除。
当存储数据比较重要时，这样做是合理的，但在许多情况下，这些 PVC 中的持久化数据要么是临时的，
要么可以从另一个源端重建。在这些情况下，删除 StatefulSet 或减少副本后留下的 PVC 及其下层的卷是不必要的，
还会产生成本，需要手动清理。

## 新的 StatefulSet PVC 保留策略

如果你启用这个新 alpha 特性，StatefulSet 规约中就可以包含 PersistentVolumeClaim 的保留策略。
该策略用于控制是否以及何时删除基于 StatefulSet 的 `volumeClaimTemplate` 属性所创建的 PVCs。
保留策略的首次迭代包含两种可能删除 PVC 的情况。

第一种情况是 StatefulSet 资源被删除时（这意味着所有副本也被删除），这由 `whenDeleted` 策略控制的。
第二种情况是 StatefulSet 缩小时，即删除 StatefulSet 部分副本，这由 `whenScaled` 策略控制。
在这两种情况下，策略即可以是 `Retain` 不涉及相应 PVCs 的改变，也可以是 `Delete` 即删除对应的 PVCs。
删除是通过普通的[对象删除](/zh-cn/docs/concepts/architecture/garbage-collection/)完成的，
因此，的所有保留策略都会被遵照执行。

该策略形成包含四种情况的矩阵。我将逐一介绍，并为每一种情况给出一个例子。

  * **`whenDeleted` 和 `whenScaled` 都是 `Retain`。** 这与 StatefulSets 的现有行为一致，
    即不删除 PVCs。 这也是默认的保留策略。它适用于 StatefulSet
    卷上的数据是不可替代的且只能手动删除的情况。
 
  * **`whenDeleted` 是 `Delete` 但 `whenScaled` 是 `Retain`。** 在这种情况下，
    只有当整个 StatefulSet 被删除时，PVCs 才会被删除。
    如果减少 StatefulSet 副本，PVCs 不会删除，这意味着如果增加副本时，可以从前一个副本重新连接所有数据。
    这可能用于临时的 StatefulSet，例如在 CI 实例或 ETL 管道中，
    StatefulSet 上的数据仅在 StatefulSet 生命周期内才需要，但在任务运行时数据不易重构。
    任何保留状态对于所有先缩小后扩大的副本都是必需的。

  * **`whenDeleted` 和 `whenScaled` 都是 `Delete`。** 当其副本不再被需要时，PVCs 会立即被删除。
    注意，这并不包括 Pod 被删除且有新版本被调度的情况，例如当节点被腾空而 Pod 需要迁移到别处时。
    只有当副本不再被需要时，如按比例缩小或删除 StatefulSet 时，才会删除 PVC。
    此策略适用于数据生命周期短于副本生命周期的情况。即数据很容易重构，
    且删除未使用的 PVC 所节省的成本比快速增加副本更重要，或者当创建一个新的副本时，
    来自以前副本的任何数据都不可用，必须重新构建。

  * **`whenDeleted` 是 `Retain` 但 `whenScaled` 是 `Delete`。** 这与前一种情况类似，
    在增加副本时用保留的 PVCs 快速重构几乎没有什么益处。例如 Elasticsearch 集群就是使用的这种方式。
    通常，你需要增大或缩小工作负载来满足业务诉求，同时确保最小数量的副本（例如：3）。
    当减少副本时，数据将从已删除的副本迁移出去，保留这些 PVCs 没有任何用处。
    但是，这对临时关闭整个 Elasticsearch 集群进行维护时是很有用的。
    如果需要使 Elasticsearch 系统脱机，可以通过临时删除 StatefulSet 来实现，
    然后通过重新创建 StatefulSet 来恢复 Elasticsearch 集群。
    保存 Elasticsearch 数据的 PVCs 不会被删除，新的副本将自动使用它们。
  
查阅[文档](/zh-cn/docs/concepts/workloads/controllers/statefulset/#persistentvolumeclaim-policies)
获取更多详细信息。

## 下一步是什么？

启用该功能并尝试一下！在集群上启用 `StatefulSetAutoDeletePVC` 功能，然后使用新策略创建 StatefulSet。
测试一下，告诉我们你的体验！

我很好奇这个属主引用机制在实践中是否有效。例如，我们意识到 Kubernetes 中没有可以知道谁设置了引用的机制，
因此 StatefulSet 控制器可能会与设置自己的引用的自定义控制器发生冲突。
幸运的是，维护现有的保留行为不涉及任何新属主引用，因此默认行为是兼容的。

请用标签 `sig/apps` 标记你报告的任何问题，并将它们分配给 Matthew Cary
(在 GitHub上 [@mattcary](https://github.com/mattcary))。

尽情体验吧！

