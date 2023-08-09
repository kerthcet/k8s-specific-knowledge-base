---
title: Pod 生命周期
id: pod-lifecycle
date: 2019-02-17
full-link: /zh-cn/docs/concepts/workloads/pods/pod-lifecycle/
related:
 - pod
 - container
tags:
 - fundamental
short_description: >
  关于 Pod 在其生命周期中处于哪个阶段的更高层次概述。
---


关于 Pod 在其生命周期中处于哪个阶段的更高层次概述。


[Pod 生命周期](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/) 是关于 Pod
处于哪个阶段的概述。包含了下面 5 种可能的阶段：Running、Pending、Succeeded、
Failed、Unknown。关于 Pod 的阶段的更高级描述请查阅
[PodStatus](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podstatus-v1-core) `phase` 字段。
