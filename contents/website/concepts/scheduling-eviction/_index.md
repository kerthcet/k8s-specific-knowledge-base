---
title: 调度、抢占和驱逐
weight: 95
content_type: concept
description: >
  在 Kubernetes 中，调度 (scheduling) 指的是确保 Pod 匹配到合适的节点，
  以便 kubelet 能够运行它们。抢占 (Preemption) 指的是终止低优先级的 Pod 以便高优先级的 Pod
  可以调度运行的过程。驱逐 (Eviction) 是在资源匮乏的节点上，主动让一个或多个 Pod 失效的过程。
no_list: true
---


在 Kubernetes 中，调度 (scheduling) 指的是确保 {{<glossary_tooltip text="Pod" term_id="pod">}}
匹配到合适的{{<glossary_tooltip text="节点" term_id="node">}}，
以便 {{<glossary_tooltip text="kubelet" term_id="kubelet">}} 能够运行它们。
抢占 (Preemption) 指的是终止低{{<glossary_tooltip text="优先级" term_id="pod-priority">}}的 Pod
以便高优先级的 Pod 可以调度运行的过程。
驱逐 (Eviction) 是在资源匮乏的节点上，主动让一个或多个 Pod 失效的过程。


## 调度

* [Kubernetes 调度器](/zh-cn/docs/concepts/scheduling-eviction/kube-scheduler/)
* [将 Pod 指派到节点](/zh-cn/docs/concepts/scheduling-eviction/assign-pod-node/)
* [Pod 开销](/zh-cn/docs/concepts/scheduling-eviction/pod-overhead/)
* [Pod 拓扑分布约束](/zh-cn/docs/concepts/scheduling-eviction/topology-spread-constraints/)
* [污点和容忍度](/zh-cn/docs/concepts/scheduling-eviction/taint-and-toleration/)
* [动态资源分配](/zh-cn/docs/concepts/scheduling-eviction/dynamic-resource-allocation)
* [调度框架](/zh-cn/docs/concepts/scheduling-eviction/scheduling-framework)
* [调度器性能调试](/zh-cn/docs/concepts/scheduling-eviction/scheduler-perf-tuning/)
* [扩展资源的资源装箱](/zh-cn/docs/concepts/scheduling-eviction/resource-bin-packing/)
* [Pod 调度就绪](/zh-cn/docs/concepts/scheduling-eviction/pod-scheduling-readiness/)


## Pod 干扰

{{<glossary_definition term_id="pod-disruption" length="all">}}

* [Pod 优先级和抢占](/zh-cn/docs/concepts/scheduling-eviction/pod-priority-preemption/)
* [节点压力驱逐](/zh-cn/docs/concepts/scheduling-eviction/node-pressure-eviction/)
* [API 发起的驱逐](/zh-cn/docs/concepts/scheduling-eviction/api-eviction/)
