---
title: StatefulSet
id: statefulset
date: 2018-04-12
full_link: /zh-cn/docs/concepts/workloads/controllers/statefulset/
short_description: >
  StatefulSet 用来管理某 Pod 集合的部署和扩缩，并为这些 Pod 提供持久存储和持久标识符。
aka: 
tags:
- fundamental
- core-object
- workload
- storage
---


StatefulSet 用来管理某 {{< glossary_tooltip text="Pod" term_id="pod" >}} 集合的部署和扩缩，
并为这些 Pod 提供持久存储和持久标识符。 


和 {{< glossary_tooltip text="Deployment" term_id="deployment" >}} 类似，
StatefulSet 管理基于相同容器规约的一组 Pod。但和 Deployment 不同的是，
StatefulSet 为它们的每个 Pod 维护了一个有粘性的 ID。这些 Pod 是基于相同的规约来创建的，
但是不能相互替换：无论怎么调度，每个 Pod 都有一个永久不变的 ID。

如果希望使用存储卷为工作负载提供持久存储，可以使用 StatefulSet 作为解决方案的一部分。
尽管 StatefulSet 中的单个 Pod 仍可能出现故障，
但持久的 Pod 标识符使得将现有卷与替换已失败 Pod 的新 Pod 相匹配变得更加容易。