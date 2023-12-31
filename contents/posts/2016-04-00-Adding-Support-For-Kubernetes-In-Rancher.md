---
title: " 在 Rancher 中添加对 Kuernetes 的支持 "
date: 2016-04-08
slug: adding-support-for-kubernetes-in-rancher
---
_今天的来宾帖子由 Rancher Labs（用于管理容器的开源软件平台）的首席架构师 Darren Shepherd  撰写。_ 


在过去的一年中，我们看到希望在其软件开发和IT组织中利用容器的公司数量激增。
为了实现这一目标，组织一直在研究如何构建集中式的容器管理功能，该功能将使用户可以轻松访问容器，同时集中管理IT组织的可见性和控制力。
2014年，我们启动了开源 Rancher 项目，通过构建容器管理平台来解决此问题。

最近，我们发布了 Rancher v1.0。
在此最新版本中，用于管理容器的开源软件平台 [Rancher](http://www.rancher.com/) 现在在创建环境时支持 Kubernetes 作为容器编排框架。
现在，使用 Rancher 启动 Kubernetes 环境是完全自动化的，只需 5 至 10 分钟即可交付运行正常的集群。

我们创建 Rancher 的目的是为组织提供完整的容器管理平台。
作为其中的一部分，我们始终支持使用 Docker API 和 Docker Compose 在本地部署 Docker 环境。
自成立以来， Kubernetes 的运营成熟度给我们留下了深刻的印象，而在此版本中，我们使得其可以在同一管理平台上部署各种容器编排和调度框架。

添加 Kubernetes 使用户可以访问增长最快的平台之一，用于在生产中部署和管理容器。
我们将在 Rancher 中提供一流的 Kubernetes 支持，并将继续支持本机 Docker 部署。

**将 Kubernetes 带到 Rancher**  

 ![Kubernetes deployment-3.PNG](https://lh6.googleusercontent.com/bhmC1-XO5T-itFN3ZsCQmrxUSSEcnezaL-qch6ILWvJRnbhEBZZlAMEj-RcNgkM9XVEUzsRMsvDGc7u8f-M19Jdk_J0GCoO-gZTCZDtgkokgqNkCgP98o8W29xD0kmKiMPeLN-Tt)
 
我们的平台已经可以扩展为各种不同的包装格式，因此我们对拥抱 Kubernetes 感到乐观。
没错，作为开发人员，与 Kubernetes 项目一起工作是一次很棒的经历。
该项目的设计使这一操作变得异常简单，并且我们能够利用插件和扩展来构建 Kubernetes 发行版，从而利用我们的基础架构和应用程序服务。
例如，我们能够将 Rancher 的软件定义的网络，存储管理，负载平衡，DNS 和基础结构管理功能直接插入 Kubernetes，而无需更改代码库。


更好的是，我们已经能够围绕 Kubernetes 核心功能添加许多服务。
例如，我们在 Kubernetes 上实现了常用的 [应用程序目录](https://github.com/rancher/community-catalog/tree/master/kubernetes-templates) 。
过去，我们曾使用 Docker Compose 定义应用程序模板，但是在此版本中，我们现在支持 Kubernetes 服务、副本控制器和和 Pod 来部署应用程序。
使用目录，用户可以连接到 git 仓库并自动部署和升级作为 Kubernetes 服务部署的应用。
然后，用户只需单击一下按钮，即可配置和部署复杂的多节点企业应用程序。
升级也是完全自动化的，并集中向用户推出。


**回馈**

与 Kubernetes 一样，Rancher 是一个开源软件项目，任何人均可免费使用，并且不受任何限制地分发给社区。
您可以在 [GitHub](http://www.github.com/rancher/rancher) 上找到 Rancher 的所有源代码，即将发布的版本和问题。
我们很高兴加入 Kubernetes 社区，并期待与所有其他贡献者合作。
在Rancher [here](http://rancher.com/kubernetes/) 中查看有关 Kubernetes 新支持的演示。&nbsp;

_-- Rancher Labs 首席架构师 Darren Shepherd_
