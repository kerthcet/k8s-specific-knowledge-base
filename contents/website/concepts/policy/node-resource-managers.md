---
title: 节点资源管理器
content_type: concept
weight: 50
---


Kubernetes 提供了一组资源管理器，用于支持延迟敏感的、高吞吐量的工作负载。
资源管理器的目标是协调和优化节点资源，以支持对 CPU、设备和内存（巨页）等资源有特殊需求的 Pod。


主管理器，也叫拓扑管理器（Topology Manager），是一个 Kubelet 组件，
它通过[策略](/zh-cn/docs/tasks/administer-cluster/topology-manager/)，
协调全局的资源管理过程。

各个管理器的配置方式会在专项文档中详细阐述：

- [CPU 管理器策略](/zh-cn/docs/tasks/administer-cluster/cpu-management-policies/)
- [设备管理器](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-integration-with-the-topology-manager)
- [内存管理器策略](/zh-cn/docs/tasks/administer-cluster/memory-manager/)
