---
title: Pod 优先级（Pod Priority）
id: pod-priority
date: 2019-01-31
full_link: /zh-cn/docs/concepts/scheduling-eviction/pod-priority-preemption/#pod-priority
short_description: >
  Pod 优先级表示一个 Pod 相对于其他 Pod 的重要性。

aka:
tags:
- operation
---


 Pod 优先级表示一个  {{< glossary_tooltip term_id="pod" >}} 相对于其他 Pod 的重要性。


[Pod 优先级](/zh-cn/docs/concepts/scheduling-eviction/pod-priority-preemption/#pod-priority)
允许用户为 Pod 设置高于或低于其他 Pod 的优先级 -- 这对于生产集群
工作负载而言是一个重要的特性。

