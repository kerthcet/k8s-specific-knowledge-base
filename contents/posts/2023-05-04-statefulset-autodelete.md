---
layout: blog
title: 'Kubernetes 1.27: StatefulSet PVC 自动删除(beta)'
date: 2023-05-04
slug: kubernetes-1-27-statefulset-pvc-auto-deletion-beta
---

**作者**：Matthew Cary (Google)

**译者**：顾欣 (ICBC)

Kubernetes v1.27 将一种新的策略机制升级到 Beta 阶段，这一策略用于控制
[`StatefulSets`](/zh-cn/docs/concepts/workloads/controllers/statefulset/)
的 [`PersistentVolumeClaims`](/zh-cn/docs/concepts/storage/persistent-volumes/)（PVCs）的生命周期。
这种新的 PVC 保留策略允许用户指定当删除 `StatefulSet` 或者缩减 `StatefulSet` 中的副本时，
是自动删除还是保留从 `StatefulSet` 规约模板生成的 PVC。

## 所解决的问题

`StatefulSet` 规约可以包含 `Pod` 和 PVC 模板。
当首次创建副本时，Kubernetes 控制平面会为该副本创建一个 PVC （如果不存在）。
在 PVC 保留策略出现之前，控制平面不会清理为 `StatefulSets` 创建的 PVC，
该任务通常由集群管理员负责，或者通过一些附加的自动化工具来处理。
你需要寻找这些工具，并检查其适用性，然后进行部署。
通常管理 PVC 的常见模式，无论是手动管理还是通过诸如 Helm 等工具进行管理，
都是由负责管理它们的工具跟踪，具有明确的生命周期。
使用 `StatefulSets` 的工作流必须自行确定由 `StatefulSet` 创建的 PVC，
并确定其生命周期。

在引入这个新特性之前，当一个由 StatefulSet 管理的副本消失时，
无论是因为 `StatefulSet` 正在减少其副本数量，还是因为其 `StatefulSet` 被删除，
PVC 及其支持卷仍然存在，必须手动删除。尽管在数据至关重要时这种行为是合适的，
但在许多情况下，这些 PVC 中的持久数据要么是临时的，要么可以从其他来源重建。
在这些情况下，删除 `StatefulSet` 或副本后仍保留 PVC 及其支持卷是不必要的，
这会产生成本，并且需要手动清理。

## 新的 `StatefulSet` PVC 保留策略

新的 `StatefulSet` PVC 保留策略用于控制是否以及何时删除从 `StatefulSet` 
的 `volumeClaimTemplate` 创建的 PVC。有两种情况可能需要就此作出决定。

第一种是当删除 `StatefulSet` 资源时（意味着所有副本也会被删除）。
这时的行为由 `whenDeleted` 策略控制。第二种场景由 `whenScaled` 控制，
即当 `StatefulSet` 缩减规模时，它会移除一部分而不是全部副本。在这两种情况下，
策略可以是 `Retain`，表示相应的 PVC 不受影响，或者是 `Delete`，表示 PVC 将被删除。
删除操作是通过普通的[对象删除](/zh-cn/docs/concepts/architecture/garbage-collection/)完成的，
这样可以确保对底层 PV 的所有保留策略都得到遵守。

这个策略形成了一个矩阵，包括四种情况。接下来，我将逐一介绍每种情况并给出一个示例。

  * **`whenDeleted` 和 `whenScaled` 都是 `Retain`。**

    这与现有的 `StatefulSets` 行为相匹配，所有 PVC 都不会被删除。这也是默认的保留策略。
    当 `StatefulSet` 卷上的数据可能是不可替代的，并且应该仅在手动情况下删除时，这种策略是适当的。

  * **`whenDeleted` 是 `Delete`，`whenScaled` 是 `Retain`。**
    
    在这种情况下，只有在整个 `StatefulSet` 被删除时，PVC 才会被删除。
    如果 `StatefulSet` 进行缩减操作，PVC 将不会受到影响，这意味着如果缩减后再进行扩展，
    并且使用了来自之前副本的任何数据，PVC 可以被重新关联。这种情况适用于临时的 `StatefulSet`，
    例如在 CI 实例或 ETL 流水线中，`StatefulSet` 上的数据只在其生命周期内需要，
    但在任务运行时，数据不容易重建。对于先被缩容后被扩容的副本而言，所有已保留的状态都是需要的。


  * **`whenDeleted` 和 `whenScaled` 都是 `Delete`。**

    当副本不再需要时，PVC 会立即被删除。需要注意的是，
    这不包括当删除一个 Pod 并重新调度一个新版本时的情况，
    例如当一个节点被排空并且 Pods 需要迁移到其他地方时。只有在副本不再被需要时，
    即通过缩减规模或删除 `StatefulSet` 时，PVC 才会被删除。
    这种情况适用于数据不需要在其副本的生命周期之外存在的情况。也许数据很容易重建，
    删除未使用的 PVC 可以节省成本比快速扩展更重要，或者当创建一个新副本时，
    来自前一个副本的任何数据都无法使用，必须进行重建。

  * **`whenDeleted` 是 `Retain`，`whenScaled` 是 `Delete`。**

    这与前面的情况类似，保留 PVC 以便在扩容时进行快速重用的好处微乎其微。
    一个使用这种策略的例子是 Elasticsearch 集群。通常，你会根据需求调整该工作负载的规模，
    同时确保有一定数量的副本（例如：3个）一直存在。在缩容时，数据会从被删除的副本迁移走，
    保留这些 PVC 没有好处。然而，如果需要临时关闭整个 Elasticsearch 集群进行维护，
    可以通过暂时删除 `StatefulSet` 然后重建 `StatefulSet` 来恢复 Elasticsearch 集群。
    持有 Elasticsearch 数据的 PVC 仍然存在，新的副本将自动使用它们。

请访问[文档](/zh-cn/docs/concepts/workloads/controllers/statefulset/#persistentvolumeclaim-policies)
以查看所有详细信息。

## 下一步是什么？

试一试吧！在 Kubernetes 1.27 的集群中，`StatefulSetAutoDeletePVC` 特性门控是 Beta 阶段，
使用新的策略创建一个 `StatefulSet`，进行测试并告诉我们你的想法！

我非常好奇这个所有者引用机制在实践中是否运行良好。例如，
我意识到在 Kubernetes 中没有机制可以知道是谁设置了引用，
因此 `StatefulSet` 控制器可能会与设置自己引用的自定义控制器产生冲突。
幸运的是，保持现有的保留行为不涉及任何新的所有者引用，因此默认行为将是兼容的。

请在你报告的任何 issue 上标记标签 sig/apps，
并将它们指派给 Matthew Cary (@mattcary at GitHub)。

祝您使用愉快！
