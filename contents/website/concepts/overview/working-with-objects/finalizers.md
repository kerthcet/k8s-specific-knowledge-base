---
title: Finalizers
content_type: concept
weight: 80
---


{{<glossary_definition term_id="finalizer" length="long">}}

你可以使用 Finalizers 来控制{{< glossary_tooltip text="对象" term_id="object" >}}的{{<glossary_tooltip text="垃圾回收" term_id="garbage-collection">}}，
方法是在删除目标资源之前提醒{{<glossary_tooltip text="控制器" term_id="controller">}}执行特定的清理任务。

Finalizers 通常不指定要执行的代码。
相反，它们通常是特定资源上的键的列表，类似于注解。
Kubernetes 自动指定了一些 Finalizers，但你也可以指定你自己的。

## Finalizers 如何工作   {#how-finalizers-work}

当你使用清单文件创建资源时，你可以在 `metadata.finalizers` 字段指定 Finalizers。
当你试图删除该资源时，处理删除请求的 API 服务器会注意到 `finalizers` 字段中的值，
并进行以下操作：

  * 修改对象，将你开始执行删除的时间添加到 `metadata.deletionTimestamp` 字段。
  * 禁止对象被删除，直到其 `metadata.finalizers` 字段为空。
  * 返回 `202` 状态码（HTTP "Accepted"）。

管理 finalizer 的控制器注意到对象上发生的更新操作，对象的 `metadata.deletionTimestamp`
被设置，意味着已经请求删除该对象。然后，控制器会试图满足资源的 Finalizers 的条件。
每当一个 Finalizer 的条件被满足时，控制器就会从资源的 `finalizers` 字段中删除该键。
当 `finalizers` 字段为空时，`deletionTimestamp` 字段被设置的对象会被自动删除。
你也可以使用 Finalizers 来阻止删除未被管理的资源。

一个常见的 Finalizer 的例子是 `kubernetes.io/pv-protection`，
它用来防止意外删除 `PersistentVolume` 对象。
当一个 `PersistentVolume` 对象被 Pod 使用时，
Kubernetes 会添加 `pv-protection` Finalizer。
如果你试图删除 `PersistentVolume`，它将进入 `Terminating` 状态，
但是控制器因为该 Finalizer 存在而无法删除该资源。
当 Pod 停止使用 `PersistentVolume` 时，
Kubernetes 清除 `pv-protection` Finalizer，控制器就会删除该卷。

## 属主引用、标签和 Finalizers {#owners-labels-finalizers}

与{{<glossary_tooltip text="标签" term_id="label">}}类似，
[属主引用](/zh-cn/docs/concepts/overview/working-with-objects/owners-dependents/)
描述了 Kubernetes 中对象之间的关系，但它们作用不同。
当一个{{<glossary_tooltip text="控制器" term_id="controller">}}
管理类似于 Pod 的对象时，它使用标签来跟踪相关对象组的变化。
例如，当 {{<glossary_tooltip text="Job" term_id="job">}} 创建一个或多个 Pod 时，
Job 控制器会给这些 Pod 应用上标签，并跟踪集群中的具有相同标签的 Pod 的变化。

Job 控制器还为这些 Pod 添加了“属主引用”，指向创建 Pod 的 Job。
如果你在这些 Pod 运行的时候删除了 Job，
Kubernetes 会使用属主引用（而不是标签）来确定集群中哪些 Pod 需要清理。

当 Kubernetes 识别到要删除的资源上的属主引用时，它也会处理 Finalizers。

在某些情况下，Finalizers 会阻止依赖对象的删除，
这可能导致目标属主对象被保留的时间比预期的长，而没有被完全删除。
在这些情况下，你应该检查目标属主和附属对象上的 Finalizers 和属主引用，来排查原因。

{{< note >}}
在对象卡在删除状态的情况下，要避免手动移除 Finalizers，以允许继续删除操作。
Finalizers 通常因为特殊原因被添加到资源上，所以强行删除它们会导致集群出现问题。
只有了解 finalizer 的用途时才能这样做，并且应该通过一些其他方式来完成
（例如，手动清除其余的依赖对象）。
{{< /note >}}

## {{% heading "whatsnext" %}}

* 在 Kubernetes 博客上阅读[使用 Finalizers 控制删除](/blog/2021/05/14/using-finalizers-to-control-deletion/)。
