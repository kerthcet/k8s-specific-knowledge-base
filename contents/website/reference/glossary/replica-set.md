---
title: ReplicaSet
id: replica-set
date: 2018-04-12
full_link: /zh-cn/docs/concepts/workloads/controllers/replicaset/
short_description: >
  ReplicaSet 是下一代副本控制器。

aka: 
tags:
- fundamental
- core-object
- workload
---



ReplicaSet 是下一代副本控制器。



ReplicaSet 就像 ReplicationController 那样，确保一次运行指定数量的 Pod 副本。ReplicaSet 支持新的基于集合的选择器需求（在标签的用户指南中有相关描述），而副本控制器只支持基于等值的选择器需求。
