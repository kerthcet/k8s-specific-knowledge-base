---
title: 抢占（Preemption）
id: preemption
date: 2019-01-31
full_link: /zh-cn/docs/concepts/scheduling-eviction/pod-priority-preemption/#preemption
short_description: >
  Kubernetes 中的抢占逻辑通过驱逐节点上的低优先级 Pod 来帮助悬决的
  Pod 找到合适的节点。

aka:
tags:
- operation
---

Kubernetes 中的抢占逻辑通过驱逐{{< glossary_tooltip term_id="node" >}}
上的低优先级{{< glossary_tooltip term_id="pod" >}}
来帮助悬决的 Pod 找到合适的节点。


如果一个 Pod 无法调度，调度器会尝试
[抢占](/zh-cn/docs/concepts/scheduling-eviction/pod-priority-preemption/#preemption)
较低优先级的 Pod，以使得悬决的 Pod 有可能被调度。

