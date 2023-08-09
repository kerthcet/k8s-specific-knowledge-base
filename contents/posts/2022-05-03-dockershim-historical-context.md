---
layout: blog
title: "Dockershim：历史背景"
date: 2022-05-03
slug: dockershim-historical-context
---


**作者：** Kat Cosgrove

自 Kubernetes v1.24 起，Dockershim 已被删除，这对项目来说是一个积极的举措。
然而，背景对于充分理解某事很重要，无论是社交还是软件开发，这值得更深入的审查。
除了 Kubernetes v1.24 中的 dockershim 移除之外，
我们在社区中看到了一些混乱（有时处于恐慌级别）和对这一决定的不满，
主要是由于缺乏有关此删除背景的了解。弃用并最终从 Kubernetes 中删除
dockershim 的决定并不是迅速或轻率地做出的。
尽管如此，它已经工作了很长时间，以至于今天的许多用户都比这个决定更新，
更不用提当初为何引入 dockershim 了。

那么 dockershim 是什么，为什么它会消失呢？

在 Kubernetes 的早期，我们只支持一个容器运行时，那个运行时就是 Docker Engine。
那时，并没有太多其他选择，而 Docker 是使用容器的主要工具，所以这不是一个有争议的选择。
最终，我们开始添加更多的容器运行时，比如 rkt 和 hypernetes，很明显 Kubernetes
用户希望选择最适合他们的运行时。因此，Kubernetes 需要一种方法来允许集群操作员灵活地使用他们选择的任何运行时。

[容器运行时接口](/blog/2016/12/container-runtime-interface-cri-in-kubernetes/) (CRI) 
已发布以支持这种灵活性。 CRI 的引入对项目和用户来说都很棒，但它确实引入了一个问题：Docker Engine
作为容器运行时的使用早于 CRI，并且 Docker Engine 不兼容 CRI。 为了解决这个问题，在 kubelet
组件中引入了一个小型软件 shim (dockershim)，专门用于填补 Docker Engine 和 CRI 之间的空白，
允许集群操作员继续使用 Docker Engine 作为他们的容器运行时基本上不间断。

然而，这个小软件 shim 从来没有打算成为一个永久的解决方案。 多年来，它的存在给
kubelet 本身带来了许多不必要的复杂性。由于这个 shim，Docker
的一些集成实现不一致，导致维护人员的负担增加，并且维护特定于供应商的代码不符合我们的开源理念。
为了减少这种维护负担并朝着支持开放标准的更具协作性的社区迈进，
[引入了 KEP-2221](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/2221-remove-dockershim)，
建议移除 dockershim。随着 Kubernetes v1.20 的发布，正式弃用。

我们没有很好地传达这一点，不幸的是，弃用公告在社区内引起了一些恐慌。关于这对
Docker作为一家公司意味着什么，Docker 构建的容器镜像是否仍然可以运行，以及
Docker Engine 究竟是什么导致了社交媒体上的一场大火，人们感到困惑。
这是我们的错；我们应该更清楚地传达当时发生的事情和原因。为了解决这个问题，
我们发布了[一篇博客](/zh-cn/blog/2020/12/02/dont-panic-kubernetes-and-docker/)和[相应的 FAQ](/zh-cn/blog/2020/12/02/dockershim-faq/)
以减轻社区的恐惧并纠正对 Docker 是什么以及容器如何在 Kubernetes 中工作的一些误解。
由于社区的关注，Docker 和 Mirantis 共同决定继续以
[cri-dockerd](https://www.mirantis.com/blog/the-future-of-dockershim-is-cri-dockerd/)
的形式支持 dockershim 代码，允许你在需要时继续使用 Docker Engine 作为容器运行时。
对于想要尝试其他运行时（如 containerd 或 cri-o）的用户，
[已编写迁移文档](/zh-cn/docs/tasks/administer-cluster/migrating-from-dockershim/change-runtime-containerd/)。

我们后来[调查了社区](https://kubernetes.io/blog/2021/11/12/are-you-ready-for-dockershim-removal/)[发现还有很多用户有疑问和顾虑](/zh-cn/blog/2022/01/07/kubernetes-is-moving-on-from-dockershim)。 
作为回应，Kubernetes 维护人员和 CNCF 承诺通过扩展文档和其他程序来解决这些问题。
事实上，这篇博文是这个计划的一部分。随着如此多的最终用户成功迁移到其他运行时，以及改进的文档，
我们相信每个人现在都为迁移铺平了道路。

Docker 不会消失，无论是作为一种工具还是作为一家公司。它是云原生社区的重要组成部分，
也是 Kubernetes 项目的历史。没有他们，我们就不会是现在的样子。也就是说，从 kubelet
中删除 dockershim 最终对社区、生态系统、项目和整个开源都有好处。
这是我们所有人齐心协力支持开放标准的机会，我们很高兴在 Docker 和社区的帮助下这样做。
