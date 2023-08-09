---
layout: blog
title: '动态 Kubelet 配置'
date: 2018-07-11
slug: dynamic-kubelet-configuration
---

**作者**: Michael Taufen (Google)

**编者注：在 1.22 版本弃用后，该功能已在 1.24 版本中删除。**

**编者注：这篇文章是[一系列深度文章](https://kubernetes.io/blog/2018/06/27/kubernetes-1.11-release-announcement/) 的一部分，这个系列介绍了 Kubernetes 1.11 中的新增功能**

## 为什么要进行动态 Kubelet 配置？

Kubernetes 提供了以 API 为中心的工具，可显着改善用于管理应用程序和基础架构的工作流程。
但是，在大多数的 Kubernetes 安装中，kubelet 在每个主机上作为本机进程运行，因此
未被标准 Kubernetes API 覆盖。

过去，这意味着集群管理员和服务提供商无法依靠 Kubernetes API 在活动集群中重新配置 Kubelets。
实际上，这要求操作员要 SSH 登录到计算机以执行手动重新配置，要么使用第三方配置管理自动化工具，
或创建已经安装了所需配置的新 VM，然后将工作迁移到新计算机上。
这些方法是特定于环境的，并且可能很耗时费力。

动态 Kubelet 配置使集群管理员和服务提供商能够通过 Kubernetes API 在活动集群中重新配置 Kubelet。

## 什么是动态 Kubelet 配置？

Kubernetes v1.10 使得可以通过 Beta 版本的[配置文件](/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/)
API 配置 kubelet。
Kubernetes 已经提供了用于在 API 服务器中存储任意文件数据的 ConfigMap 抽象。

动态 Kubelet 配置扩展了 Node 对象，以便 Node 可以引用包含相同类型配置文件的 ConfigMap。
当节点更新为引用新的 ConfigMap 时，关联的 Kubelet 将尝试使用新的配置。

## 它是如何工作的？

动态 Kubelet 配置提供以下核心功能：

* Kubelet 尝试使用动态分配的配置。
* Kubelet 将其配置已检查点的形式保存到本地磁盘，无需 API 服务器访问即可重新启动。
* Kubelet 在 Node 状态中报告已指定的、活跃的和最近已知良好的配置源。
* 当动态分配了无效的配置时，Kubelet 会自动退回到最后一次正确的配置，并在 Node 状态中报告错误。

要使用动态 Kubelet 配置功能，集群管理员或服务提供商将首先发布包含所需配置的 ConfigMap，
然后设置每个 Node.Spec.ConfigSource.ConfigMap 引用以指向新的 ConfigMap。
运营商可以以他们喜欢的速率更新这些参考，从而使他们能够执行新配置的受控部署。

每个 Kubelet 都会监视其关联的 Node 对象的更改。
更新 Node.Spec.ConfigSource.ConfigMap 引用后，
Kubelet 将通过将其包含的文件通过检查点机制写入本地磁盘保存新的 ConfigMap。
然后，Kubelet 将退出，而操作系统级进程管理器将重新启动它。
请注意，如果未设置 Node.Spec.ConfigSource.ConfigMap 引用，
则 Kubelet 将使用其正在运行的计算机本地的一组标志和配置文件。

重新启动后，Kubelet 将尝试使用来自新检查点的配置。
如果新配置通过了 Kubelet 的内部验证，则 Kubelet 将更新 
Node.Status.Config 用以反映它正在使用新配置。
如果新配置无效，则 Kubelet 将退回到其最后一个正确的配置，并在 Node.Status.Config 中报告错误。

请注意，默认的最后一次正确配置是 Kubelet 命令行标志与 Kubelet 的本地配置文件的组合。
与配置文件重叠的命令行标志始终优先于本地配置文件和动态配置，以实现向后兼容。

有关单个节点的配置更新的高级概述，请参见下图：

![kubelet-diagram](/images/blog/2018-07-11-dynamic-kubelet-configuration/kubelet-diagram.png)

## 我如何了解更多？

请参阅/docs/tasks/administer-cluster/reconfigure-kubelet/上的官方教程，
其中包含有关用户工作流，某配置如何成为“最新的正确的”配置，Kubelet 如何对配置执行“检查点”操作等，
更多详细信息，以及可能的故障模式。
