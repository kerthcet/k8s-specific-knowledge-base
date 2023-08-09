---
title: 集群管理
weight: 100
content_type: concept
description: >
  关于创建和管理 Kubernetes 集群的底层细节。
no_list: true
---

集群管理概述面向任何创建和管理 Kubernetes 集群的读者人群。
我们假设你大概了解一些核心的 Kubernetes [概念](/zh-cn/docs/concepts/)。


## 规划集群   {#planning-a-cluster}

查阅[安装](/zh-cn/docs/setup/)中的指导，获取如何规划、建立以及配置 Kubernetes
集群的示例。本文所列的文章称为**发行版**。

{{< note >}}
并非所有发行版都是被积极维护的。
请选择使用最近 Kubernetes 版本测试过的发行版。
{{< /note >}}

在选择一个指南前，有一些因素需要考虑：

- 你是打算在你的计算机上尝试 Kubernetes，还是要构建一个高可用的多节点集群？
  请选择最适合你需求的发行版。
- 你正在使用类似 [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/)
  这样的**被托管的 Kubernetes 集群**, 还是**管理你自己的集群**？
- 你的集群是在**本地**还是**云（IaaS）** 上？Kubernetes 不能直接支持混合集群。
  作为代替，你可以建立多个集群。
- **如果你在本地配置 Kubernetes**，
  需要考虑哪种[网络模型](/zh-cn/docs/concepts/cluster-administration/networking/)最适合。
- 你的 Kubernetes 在**裸机**上还是**虚拟机（VM）** 上运行？
- 你是想**运行一个集群**，还是打算**参与开发 Kubernetes 项目代码**？
  如果是后者，请选择一个处于开发状态的发行版。
  某些发行版只提供二进制发布版，但提供更多的选择。
- 让你自己熟悉运行一个集群所需的[组件](/zh-cn/docs/concepts/overview/components/)。

## 管理集群   {#managing-a-cluster}

* 学习如何[管理节点](/zh-cn/docs/concepts/architecture/nodes/)。

* 学习如何设定和管理集群共享的[资源配额](/zh-cn/docs/concepts/policy/resource-quotas/)。

## 保护集群  {#securing-a-cluster}

* [生成证书](/zh-cn/docs/tasks/administer-cluster/certificates/)描述了使用不同的工具链生成证书的步骤。
* [Kubernetes 容器环境](/zh-cn/docs/concepts/containers/container-environment/)描述了
  Kubernetes 节点上由 Kubelet 管理的容器的环境。
* [控制对 Kubernetes API 的访问](/zh-cn/docs/concepts/security/controlling-access/)描述了 Kubernetes
  如何为自己的 API 实现访问控制。
* [身份认证](/zh-cn/docs/reference/access-authn-authz/authentication/)阐述了 Kubernetes
  中的身份认证功能，包括许多认证选项。
* [鉴权](/zh-cn/docs/reference/access-authn-authz/authorization/)与身份认证不同，用于控制如何处理 HTTP 请求。
* [使用准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers)阐述了在认证和授权之后拦截到
  Kubernetes API 服务的请求的插件。
* [在 Kubernetes 集群中使用 sysctl](/zh-cn/docs/tasks/administer-cluster/sysctl-cluster/)
  描述了管理员如何使用 `sysctl` 命令行工具来设置内核参数。
* [审计](/zh-cn/docs/tasks/debug/debug-cluster/audit/)描述了如何与 Kubernetes 的审计日志交互。

### 保护 kubelet   {#securing-the-kubelet}

* [节点与控制面之间的通信](/zh-cn/docs/concepts/architecture/control-plane-node-communication/)
* [TLS 启动引导](/zh-cn/docs/reference/access-authn-authz/kubelet-tls-bootstrapping/)
* [Kubelet 认证/鉴权](/zh-cn/docs/reference/access-authn-authz/kubelet-authn-authz/)

## 可选集群服务   {#optional-cluster-services}

* [DNS 集成](/zh-cn/docs/concepts/services-networking/dns-pod-service/)描述了如何将一个 DNS
  名解析到一个 Kubernetes service。
* [记录和监控集群活动](/zh-cn/docs/concepts/cluster-administration/logging/)阐述了 Kubernetes
  的日志如何工作以及怎样实现。

