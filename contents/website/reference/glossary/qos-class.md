---
title: QoS 类（QoS Class）
id: qos-class
date: 2019-04-15
full_link: /zh-cn/docs/concepts/workloads/pods/pod-qos/
short_description: >
  QoS 类（Quality of Service Class）为 Kubernetes 提供了一种将集群中的 Pod 分为几个类并做出有关调度和驱逐决策的方法。

aka: 
tags:
- core-object
- fundamental
- architecture
related:
 - pod

---

 QoS Class（Quality of Service Class）为 Kubernetes 提供了一种将集群中的 Pod
 分为几个类并做出有关调度和驱逐决策的方法。


Pod 的 QoS 类是基于 Pod 在创建时配置的计算资源请求和限制。QoS 类用于制定有关 Pod 调度和逐出的决策。
Kubernetes 可以为 Pod 分配以下 QoS 类：`Guaranteed`，`Burstable` 或者 `BestEffort`。