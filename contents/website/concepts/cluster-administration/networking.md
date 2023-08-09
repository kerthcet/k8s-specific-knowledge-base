---
title: 集群网络系统
content_type: concept
weight: 50
---

集群网络系统是 Kubernetes 的核心部分，但是想要准确了解它的工作原理可是个不小的挑战。
下面列出的是网络系统的的四个主要问题：

1. 高度耦合的容器间通信：这个已经被 {{< glossary_tooltip text="Pod" term_id="pod" >}}
   和 `localhost` 通信解决了。
2. Pod 间通信：这是本文档讲述的重点。
3. Pod 与 Service 间通信：涵盖在 [Service](/zh-cn/docs/concepts/services-networking/service/) 中。
4. 外部与 Service 间通信：也涵盖在 Service 中。


Kubernetes 的宗旨就是在应用之间共享机器。
通常来说，共享机器需要两个应用之间不能使用相同的端口，但是在多个应用开发者之间
去大规模地协调端口是件很困难的事情，尤其是还要让用户暴露在他们控制范围之外的集群级别的问题上。

动态分配端口也会给系统带来很多复杂度 - 每个应用都需要设置一个端口的参数，
而 API 服务器还需要知道如何将动态端口数值插入到配置模块中，服务也需要知道如何找到对方等等。
与其去解决这些问题，Kubernetes 选择了其他不同的方法。

要了解 Kubernetes 网络模型，请参阅[此处](/zh-cn/docs/concepts/services-networking/)。
## 如何实现 Kubernetes 的网络模型    {#how-to-implement-the-kubernetes-network-model}

网络模型由每个节点上的容器运行时实现。最常见的容器运行时使用
[Container Network Interface](https://github.com/containernetworking/cni) (CNI) 插件来管理其网络和安全功能。
许多不同的 CNI 插件来自于许多不同的供应商。其中一些仅提供添加和删除网络接口的基本功能，
而另一些则提供更复杂的解决方案，例如与其他容器编排系统集成、运行多个 CNI 插件、高级 IPAM 功能等。

请参阅[此页面](/zh-cn/docs/concepts/cluster-administration/addons/#networking-and-network-policy)了解
Kubernetes 支持的网络插件的非详尽列表。

## {{% heading "whatsnext" %}}

网络模型的早期设计、运行原理以及未来的一些计划，
都在[联网设计文档](https://git.k8s.io/design-proposals-archive/network/networking.md)里有更详细的描述。
