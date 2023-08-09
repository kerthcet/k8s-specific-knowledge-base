---
title: Finalizer
id: finalizer
date: 2021-07-07
full_link: /zh-cn/docs/concepts/overview/working-with-objects/finalizers/
short_description: >
  一个带有命名空间的键，告诉 Kubernetes 等到特定的条件被满足后，
  再完全删除被标记为删除的资源。
aka: 
tags:
- fundamental
- operation
---

Finalizer 是带有命名空间的键，告诉 Kubernetes 等到特定的条件被满足后，
再完全删除被标记为删除的资源。
Finalizer 提醒{{<glossary_tooltip text="控制器" term_id="controller">}}清理被删除的对象拥有的资源。


当你告诉 Kubernetes 删除一个指定了 Finalizer 的对象时，
Kubernetes API 通过填充 `.metadata.deletionTimestamp` 来标记要删除的对象，
并返回 `202` 状态码(HTTP "已接受") 使其进入只读状态。
此时控制平面或其他组件会采取 Finalizer 所定义的行动，
而目标对象仍然处于终止中（Terminating）的状态。
这些行动完成后，控制器会删除目标对象相关的 Finalizer。
当 `metadata.finalizers` 字段为空时，Kubernetes 认为删除已完成并删除对象。

你可以使用 Finalizer 控制资源的{{<glossary_tooltip text="垃圾收集" term_id="garbage-collection">}}。
例如，你可以定义一个 Finalizer，在删除目标资源前清理相关资源或基础设施。
