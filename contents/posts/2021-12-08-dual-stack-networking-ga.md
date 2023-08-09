---
layout: blog
title: 'Kubernetes 1.23：IPv4/IPv6 双协议栈网络达到 GA'
date: 2021-12-08
slug: dual-stack-networking-ga
---

**作者:** Bridget Kromhout (微软)

“Kubernetes 何时支持 IPv6？” 自从 k8s v1.9 版本中首次添加对 IPv6 的 alpha 支持以来，这个问题的讨论越来越频繁。
虽然 Kubernetes 从 v1.18 版本开始就支持纯 IPv6 集群，但当时还无法支持 IPv4 迁移到 IPv6。
[IPv4/IPv6 双协议栈网络](https://github.com/kubernetes/enhancements/tree/master/keps/sig-network/563-dual-stack/)
在 Kubernetes v1.23 版本中进入正式发布（GA）阶段。

让我们来看看双协议栈网络对你来说意味着什么？

## 更新 Service API

[Services](/zh-cn/docs/concepts/services-networking/service/) 在 1.20 版本之前是单协议栈的，
因此，使用两个 IP 协议族意味着需为每个 IP 协议族创建一个 Service。在 1.20 版本中对用户体验进行简化，
重新实现了 Service 以支持两个 IP 协议族，这意味着一个 Service 就可以处理 IPv4 和 IPv6 协议。
对于 Service 而言，任意的 IPv4 和 IPv6 协议组合都可以实现负载均衡。

Service API 现在有了支持双协议栈的新字段，取代了单一的 ipFamily 字段。
* 你可以通过将 `ipFamilyPolicy` 字段设置为 `SingleStack`、`PreferDualStack` 或
`RequireDualStack` 来设置 IP 协议族。Service 可以在单协议栈和双协议栈之间进行转换(在某些限制内)。
* 设置 `ipFamilies` 为指定的协议族列表，可用来设置使用协议族的顺序。
* 'clusterIPs' 的能力在涵盖了之前的 'clusterIP'的情况下，还允许设置多个 IP 地址。
所以不再需要运行重复的 Service，在两个 IP 协议族中各运行一个。你可以在两个 IP 协议族中分配集群 IP 地址。

请注意，Pods 也是双协议栈的。对于一个给定的 Pod，不可能在同一协议族中设置多个 IP 地址。

## 默认行为仍然是单协议栈

从 1.20 版本开始，重新实现的双协议栈服务处于 Alpha 阶段，无论集群是否配置了启用双协议栈的特性标志，
Kubernetes 的底层网络都已经包括了双协议栈。

Kubernetes 1.23 删除了这个特性标志，说明该特性已经稳定。
如果你想要配置双协议栈网络，这一能力总是存在的。
你可以将集群网络设置为 IPv4 单协议栈 、IPv6 单协议栈或 IPV4/IPV6 双协议栈 。

虽然 Service 是根据你的配置设置的，但 Pod 默认是由 CNI 插件设置的。
如果你的 CNI 插件分配单协议栈 IP，那么就是单协议栈，除非 `ipFamilyPolicy` 设置为 `PreferDualStack` 或 `RequireDualStack`。
如果你的 CNI 插件分配双协议栈 IP，则 `pod.status.PodIPs` 默认为双协议栈。

尽管双协议栈是可用的，但并不强制你使用它。
在[双协议栈服务配置](/zh-cn/docs/concepts/services-networking/dual-stack/#dual-stack-service-configuration-scenarios)
文档中的示例列出了可能出现的各种场景.

## 现在尝试双协议栈

虽然现在上游 Kubernetes 支持[双协议栈网络](/zh-cn/docs/concepts/services-networking/dual-stack/)
作为 GA 或稳定特性，但每个提供商对双协议栈 Kubernetes 的支持可能会有所不同。节点需要提供可路由的 IPv4/IPv6 网络接口。
Pod 需要是双协议栈的。[网络插件](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
是用来为 Pod 分配 IP 地址的，所以集群需要支持双协议栈的网络插件。一些容器网络接口（CNI）插件支持双协议栈，例如 kubenet。

支持双协议栈的生态系统在不断壮大；你可以使用
[kubeadm 创建双协议栈集群](/zh-cn/docs/setup/production-environment/tools/kubeadm/dual-stack-support/),
在本地尝试用 [KIND 创建双协议栈集群](https://kind.sigs.k8s.io/docs/user/configuration/#ip-family)，
还可以将双协议栈集群部署到云上（在查阅 CNI 或 kubenet 可用性的文档之后）

## 加入 Network SIG

SIG-Network 希望从双协议栈网络的社区体验中学习，以了解更多不断变化的需求和你的用例信息。
[SIG-network 更新了来自 KubeCon 2021 北美大会的视频](https://www.youtube.com/watch?v=uZ0WLxpmBbY&list=PLj6h78yzYM2Nd1U4RMhv7v88fdiFqeYAP&index=4)
总结了 SIG 最近的更新，包括双协议栈将在 1.23 版本中稳定。

当前 SIG-Network 在 GitHub 上的 [KEPs](https://github.com/orgs/kubernetes/projects/10) 和
[issues](https://github.com/kubernetes/kubernetes/issues?q=is%3Aopen+is%3Aissue+label%3Asig%2Fnetwork)
说明了该 SIG 的重点领域。[双协议栈 API 服务器](https://github.com/kubernetes/enhancements/issues/2438)
是一个考虑贡献的方向。

[SIG-Network 会议](https://github.com/kubernetes/community/tree/master/sig-network#meetings)
是一个友好、热情的场所，你可以与社区联系并分享你的想法。期待你的加入！

## 致谢

许多 Kubernetes 贡献者为双协议栈网络做出了贡献。感谢所有贡献了代码、经验报告、文档、代码审查以及其他工作的人。
Bridget Kromhout 在 [Kubernetes的双协议栈网络](https://containerjournal.com/features/dual-stack-networking-in-kubernetes/)
中详细介绍了这项社区工作。Tim Hockin 和 Khaled (Kal) Henidak 在 2019 年的 KubeCon 大会演讲
（[Kubernetes 通往 IPv4/IPv6 双协议栈的漫漫长路](https://www.youtube.com/watch?v=o-oMegdZcg4)）
和 Lachlan Evenson 在 2021 年演讲（[我们来啦，Kubernetes 双协议栈网络](https://www.youtube.com/watch?v=o-oMegdZcg4)）
中讨论了双协议栈的发展旅程，耗时 5 年和海量代码。
