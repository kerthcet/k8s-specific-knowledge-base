---
title: 事件（Event）
id: event
date: 2022-01-16
full_link: /zh-cn/docs/reference/kubernetes-api/cluster-resources/event-v1/
short_description: >
   对集群中某处所发生事件的报告。通常用来表述系统中某种状态变更。
aka: 
tags:
- core-object
- fundamental
---

每个 Event 是{{< glossary_tooltip text="集群" term_id="cluster" >}}中某处所发生事件的报告。
它通常用来表述系统中的某种状态变更。


事件的保留时间有限，随着时间推进，其触发方式和消息都可能发生变化。
事件用户不应该对带有给定原因（反映下层触发源）的时间特征有任何依赖，
也不要寄希望于该原因所造成的事件会一直存在。

事件应该被视为一种告知性质的、尽力而为的、补充性质的数据。

在 Kubernetes 中，[审计](/zh-cn/docs/tasks/debug/debug-cluster/audit/)
机制会生成一种不同类别的 Event 记录（API 组为 `audit.k8s.io`）。
