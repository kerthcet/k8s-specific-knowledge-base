---
layout: blog
title: 'Kubernetes v1.12: RuntimeClass 简介'
date: 2018-10-10
slug: kubernetes-v1.12-introducing-runtimeclass
---

**作者**: Tim Allclair (Google)

Kubernetes 最初是为了支持在 Linux 主机上运行本机应用程序的 Docker 容器而创建的。
从 Kubernetes 1.3 中的 [rkt](https://kubernetes.io/blog/2016/07/rktnetes-brings-rkt-container-engine-to-kubernetes/) 开始，更多的运行时间开始涌现，
这导致了[容器运行时接口（Container Runtime Interface）](https://kubernetes.io/blog/2016/12/container-runtime-interface-cri-in-kubernetes/)（CRI）的开发。
从那时起，备用运行时集合越来越大：
为了加强工作负载隔离，[Kata Containers](https://katacontainers.io/) 和 [gVisor](https://github.com/google/gvisor) 等项目被发起，
并且 Kubernetes 对 Windows 的支持正在[稳步发展](https://kubernetes.io/blog/2018/01/kubernetes-v19-beta-windows-support/)。

由于存在诸多针对不同用例的运行时，集群对混合运行时的需求变得明晰起来。
但是，所有这些不同的容器运行方式都带来了一系列新问题要处理：

- 用户如何知道哪些运行时可用，并为其工作负荷选择运行时？
- 我们如何确保将 Pod 被调度到支持所需运行时的节点上？
- 哪些运行时支持哪些功能，以及我们如何向用户显示不兼容性？
- 我们如何考虑运行时的各种资源开销？

**RuntimeClass** 旨在解决这些问题。

## Kubernetes 1.12 中的 RuntimeClass

最近，RuntimeClass 在 Kubernetes 1.12 中作为 alpha 功能引入。
最初的实现侧重于提供运行时选择 API，并为解决其他未解决的问题铺平道路。

RuntimeClass 资源代表 Kubernetes 集群中支持的容器运行时。
集群制备组件安装、配置和定义支持 RuntimeClass 的具体运行时。
在 RuntimeClassSpec 的当前形式中，只有一个字段，即 **RuntimeHandler**。
RuntimeHandler 由在节点上运行的 CRI 实现解释，并映射到实际的运行时配置。
同时，PodSpec 被扩展添加了一个新字段 **RuntimeClassName**，命名应该用于运行 Pod 的 RuntimeClass。

为什么 RuntimeClass 是 Pod 级别的概念？
Kubernetes 资源模型期望 Pod 中的容器之间可以共享某些资源。
如果 Pod 由具有不同资源模型的不同容器组成，支持必要水平的资源共享变得非常具有挑战性。
例如，要跨 VM 边界支持本地回路（localhost）接口非常困难，但这是 Pod 中两个容器之间通信的通用模型。

## 下一步是什么？

RuntimeClass 资源是将运行时属性显示到控制平面的重要基础。
例如，要对具有支持不同运行时间的异构节点的集群实施调度程序支持，我们可以在 RuntimeClass 定义中添加
[NodeAffinity](/zh-cn/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) 条件。
另一个需要解决的领域是管理可变资源需求以运行不同运行时的 Pod。
[Pod Overhead 提案](https://docs.google.com/document/d/1EJKT4gyl58-kzt2bnwkv08MIUZ6lkDpXcxkHqCvvAp4/preview)是一项较早的尝试，与
RuntimeClass 设计非常吻合，并且可能会进一步推广。

人们还提出了许多其他 RuntimeClass 扩展，随着功能的不断发展和成熟，我们会重新讨论这些提议。
正在考虑的其他扩展包括：

- 提供运行时支持的可选功能，并更好地查看由不兼容功能导致的错误。
- 自动运行时或功能发现，支持无需手动配置的调度决策。
- 标准化或一致的 RuntimeClass 名称，用于定义一组具有相同名称的 RuntimeClass 的集群应支持的属性。
- 动态注册附加的运行时，因此用户可以在不停机的情况下在现有集群上安装新的运行时。
- 根据 Pod 的要求“匹配” RuntimeClass。
  例如，指定运行时属性并使系统与适当的 RuntimeClass 匹配，而不是通过名称显式分配 RuntimeClass。

至少要到 2019 年，RuntimeClass 才会得到积极的开发，我们很高兴看到从 Kubernetes 1.12 中的 RuntimeClass alpha 开始，此功能得以形成。

## 学到更多


- 试试吧！作为 Alpha 功能，还有一些其他设置步骤可以使用 RuntimeClass。
  有关如何使其运行，请参考 [RuntimeClass 文档](/zh-cn/docs/concepts/containers/runtime-class/#runtime-class)。
- 查看 [RuntimeClass Kubernetes 增强建议](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/runtime-class.md)以获取更多细节设计细节。
- [沙盒隔离级别决策](https://docs.google.com/document/d/1fe7lQUjYKR0cijRmSbH_y0_l3CYPkwtQa5ViywuNo8Q/preview)记录了最初使
  RuntimeClass 成为 Pod 级别选项的思考过程。
- 加入讨论，并通过 [SIG-Node 社区](https://github.com/kubernetes/community/tree/master/sig-node)帮助塑造 RuntimeClass 的未来。
