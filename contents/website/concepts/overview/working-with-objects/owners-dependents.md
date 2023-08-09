---
title: 属主与附属
content_type: concept
weight: 90
---



在 Kubernetes 中，一些{{< glossary_tooltip text="对象" term_id="Object" >}}是其他对象的“属主（Owner）”。
例如，{{<glossary_tooltip text="ReplicaSet" term_id="replica-set">}} 是一组 Pod 的属主。
具有属主的对象是属主的“附属（Dependent）”。

属主关系不同于一些资源使用的[标签和选择算符](/zh-cn/docs/concepts/overview/working-with-objects/labels/)机制。
例如，有一个创建 `EndpointSlice` 对象的 Service，
该 Service 使用{{<glossary_tooltip text="标签" term_id="label">}}来让控制平面确定哪些
`EndpointSlice` 对象属于该 Service。除开标签，每个代表 Service 所管理的
`EndpointSlice` 都有一个属主引用。属主引用避免 Kubernetes
的不同部分干扰到不受它们控制的对象。

## 对象规约中的属主引用   {#owner-references-in-object-specifications}

附属对象有一个 `metadata.ownerReferences` 字段，用于引用其属主对象。一个有效的属主引用，
包含与附属对象同在一个{{<glossary_tooltip text="命名空间" term_id="namespace">}}下的对象名称和一个
{{<glossary_tooltip text="UID" term_id="uid">}}。
Kubernetes 自动为一些对象的附属资源设置属主引用的值，
这些对象包含 ReplicaSet、DaemonSet、Deployment、Job、CronJob、ReplicationController 等。
你也可以通过改变这个字段的值，来手动配置这些关系。
然而，通常不需要这么做，你可以让 Kubernetes 自动管理附属关系。

附属对象还有一个 `ownerReferences.blockOwnerDeletion` 字段，该字段使用布尔值，
用于控制特定的附属对象是否可以阻止垃圾收集删除其属主对象。
如果{{<glossary_tooltip text="控制器" term_id="controller">}}（例如 Deployment 控制器）
设置了 `metadata.ownerReferences` 字段的值，Kubernetes 会自动设置
`blockOwnerDeletion` 的值为 `true`。
你也可以手动设置 `blockOwnerDeletion` 字段的值，以控制哪些附属对象会阻止垃圾收集。

Kubernetes 准入控制器根据属主的删除权限控制用户访问，以便为附属资源更改此字段。
这种控制机制可防止未经授权的用户延迟属主对象的删除。

{{< note >}}
根据设计，kubernetes 不允许跨名字空间指定属主。
名字空间范围的附属可以指定集群范围的或者名字空间范围的属主。
名字空间范围的属主**必须**和该附属处于相同的名字空间。
如果名字空间范围的属主和附属不在相同的名字空间，那么该属主引用就会被认为是缺失的，
并且当附属的所有属主引用都被确认不再存在之后，该附属就会被删除。

集群范围的附属只能指定集群范围的属主。
在 v1.20+ 版本，如果一个集群范围的附属指定了一个名字空间范围类型的属主，
那么该附属就会被认为是拥有一个不可解析的属主引用，并且它不能够被垃圾回收。

在 v1.20+ 版本，如果垃圾收集器检测到无效的跨名字空间的属主引用，
或者一个集群范围的附属指定了一个名字空间范围类型的属主，
那么它就会报告一个警告事件。该事件的原因是 `OwnerRefInvalidNamespace`，
`involvedObject` 属性中包含无效的附属。
你可以运行 `kubectl get events -A --field-selector=reason=OwnerRefInvalidNamespace`
来获取该类型的事件。
{{< /note >}}

## 属主关系与 Finalizer   {#ownership-and-finalizers}

当你告诉 Kubernetes 删除一个资源，API 服务器允许管理控制器处理该资源的任何
[Finalizer 规则](/zh-cn/docs/concepts/overview/working-with-objects/finalizers/)。
{{<glossary_tooltip text="Finalizer" term_id="finalizer">}}
防止意外删除你的集群所依赖的、用于正常运作的资源。
例如，如果你试图删除一个仍被 Pod 使用的 `PersistentVolume`，该资源不会被立即删除，
因为 [PersistentVolume](/zh-cn/docs/concepts/storage/persistent-volumes/) 有
`kubernetes.io/pv-protection` Finalizer。
相反，[数据卷](/zh-cn/docs/concepts/storage/volumes/)将进入 `Terminating` 状态，
直到 Kubernetes 清除这个 Finalizer，而这种情况只会发生在 `PersistentVolume`
不再被挂载到 Pod 上时。

当你使用[前台或孤立级联删除](/zh-cn/docs/concepts/architecture/garbage-collection/#cascading-deletion)时，
Kubernetes 也会向属主资源添加 Finalizer。
在前台删除中，会添加 `foreground` Finalizer，这样控制器必须在删除了拥有
`ownerReferences.blockOwnerDeletion=true` 的附属资源后，才能删除属主对象。
如果你指定了孤立删除策略，Kubernetes 会添加 `orphan` Finalizer，
这样控制器在删除属主对象后，会忽略附属资源。

## {{% heading "whatsnext" %}}

* 了解更多关于 [Kubernetes Finalizer](/zh-cn/docs/concepts/overview/working-with-objects/finalizers/)。
* 了解关于[垃圾收集](/zh-cn/docs/concepts/architecture/garbage-collection)。
* 阅读[对象元数据](/zh-cn/docs/reference/kubernetes-api/common-definitions/object-meta/#System)的 API 参考文档。
