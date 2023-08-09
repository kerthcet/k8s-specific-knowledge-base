---
title: "服务、负载均衡和联网"
weight: 60
description: Kubernetes 网络背后的概念和资源。
---

## Kubernetes 网络模型   {#the-kubernetes-network-model}

集群中每一个 [`Pod`](/zh-cn/docs/concepts/workloads/pods/) 都会获得自己的、
独一无二的 IP 地址，
这就意味着你不需要显式地在 `Pod` 之间创建链接，你几乎不需要处理容器端口到主机端口之间的映射。
这将形成一个干净的、向后兼容的模型；在这个模型里，从端口分配、命名、服务发现、
[负载均衡](/zh-cn/docs/concepts/services-networking/ingress/#load-balancing)、
应用配置和迁移的角度来看，`Pod` 可以被视作虚拟机或者物理主机。

Kubernetes 强制要求所有网络设施都满足以下基本要求（从而排除了有意隔离网络的策略）：

* Pod 能够与所有其他[节点](/zh-cn/docs/concepts/architecture/nodes/)上的 Pod 通信，
  且不需要网络地址转译（NAT）
* 节点上的代理（比如：系统守护进程、kubelet）可以和节点上的所有 Pod 通信

说明：对于支持在主机网络中运行 `Pod` 的平台（比如：Linux），
当 Pod 挂接到节点的宿主网络上时，它们仍可以不通过 NAT 和所有节点上的 Pod 通信。

这个模型不仅不复杂，而且还和 Kubernetes 的实现从虚拟机向容器平滑迁移的初衷相符，
如果你的任务开始是在虚拟机中运行的，你的虚拟机有一个 IP，
可以和项目中其他虚拟机通信。这里的模型是基本相同的。

Kubernetes 的 IP 地址存在于 `Pod` 范围内 —— 容器共享它们的网络命名空间 ——
包括它们的 IP 地址和 MAC 地址。
这就意味着 `Pod` 内的容器都可以通过 `localhost` 到达对方端口。
这也意味着 `Pod` 内的容器需要相互协调端口的使用，但是这和虚拟机中的进程似乎没有什么不同，
这也被称为“一个 Pod 一个 IP”模型。

如何实现以上需求是所使用的特定容器运行时的细节。

也可以在 `Node` 本身请求端口，并用这类端口转发到你的 `Pod`（称之为主机端口），
但这是一个很特殊的操作。转发方式如何实现也是容器运行时的细节。
`Pod` 自己并不知道这些主机端口的存在。

Kubernetes 网络解决四方面的问题：

- 一个 Pod 中的容器之间[通过本地回路（loopback）通信](/zh-cn/docs/concepts/services-networking/dns-pod-service/)。
- 集群网络在不同 Pod 之间提供通信。
- [Service](/zh-cn/docs/concepts/services-networking/service/) API
  允许你[向外暴露 Pod 中运行的应用](/zh-cn/docs/tutorials/services/connect-applications-service/)，
  以支持来自于集群外部的访问。
  - [Ingress](/zh-cn/docs/concepts/services-networking/ingress/)
    提供专门用于暴露 HTTP 应用程序、网站和 API 的额外功能。
- 你也可以使用 Service
  来[发布仅供集群内部使用的服务](/zh-cn/docs/concepts/services-networking/service-traffic-policy/)。

[使用 Service 连接到应用](/zh-cn/docs/tutorials/services/connect-applications-service/)教程通过一个实际的示例让你了解
Service 和 Kubernetes 如何联网。

[集群网络](/zh-cn/docs/concepts/cluster-administration/networking/)解释了如何为集群设置网络，
还概述了所涉及的技术。
