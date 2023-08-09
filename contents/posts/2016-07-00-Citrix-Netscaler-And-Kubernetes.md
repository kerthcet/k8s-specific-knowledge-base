---
title: " Citrix + Kubernetes = 全垒打 "
date: 2016-07-14
slug: citrix-netscaler-and-kubernetes
---


编者按：今天的客座文章来自 Citrix Systems 的产品管理总监 Mikko Disini，他分享了他们在 Kubernetes 集成上的合作经验。&nbsp;_

技术合作就像体育运动。如果你能像一个团队一样合作，你就能在最后关头取得胜利。这就是我们对谷歌云平台团队的经验。

最近，我们与 Google 云平台（GCP）联系，代表 Citrix 客户以及更广泛的企业市场，希望就工作负载的迁移进行协作。此迁移需要将 [NetScaler Docker 负载均衡器]https://www.citrix.com/blogs/2016/06/20/the-best-docker-load-balancer-at-dockercon-in-seattle-this-week/) CPX 包含到 Kubernetes 节点中，并解决将流量引入 CPX 代理的任何问题。


**为什么是 NetScaler 和 Kubernetes**


1. Citrix 的客户希望他们开始使用 Kubernetes 部署他们的容器和微服务体系结构时，能够像当初迁移到云计算时一样，享有 NetScaler 所提供的第 4 层到第 7 层能力&nbsp;
2. Kubernetes 提供了一套经过验证的基础设施，可用来运行容器和虚拟机，并自动交付工作负载；
3. NetScaler CPX 提供第 4 层到第 7 层的服务，并为日志和分析平台 [NetScaler 管理和分析系统](https://www.citrix.com/blogs/2016/05/24/introducing-the-next-generation-netscaler-management-and-analytics-system/) 提供高效的度量数据。

我希望我们所有与技术合作伙伴一起工作的经验都能像与 GCP 一起工作一样好。我们有一个列表，包含支持我们的用例所需要解决的问题。我们能够快速协作形成解决方案。为了解决这些问题，GCP 团队提供了深入的技术支持，与 Citrix 合作，从而使得 NetScaler CPX 能够在每台主机上作为客户端代理启动运行。

接下来，需要在 GCP 入口负载均衡器的数据路径中插入 NetScaler CPX，使 NetScaler CPX 能够将流量分散到前端 web 服务器。NetScaler 团队进行了修改，以便 NetScaler CPX 监听 API 服务器事件，并配置自己来创建 VIP、IP 表规则和服务器规则，以便跨前端应用程序接收流量和负载均衡。谷歌云平台团队提供反馈和帮助，验证为克服技术障碍所做的修改。完成了!

NetScaler CPX 用例在 [Kubernetes 1.3](https://kubernetes.io/blog/2016/07/kubernetes-1-3-bridging-cloud-native-and-enterprise-workloads/) 中提供支持。Citrix 的客户和更广泛的企业市场将有机会基于 Kubernetes 享用 NetScaler 服务，从而降低将工作负载转移到云平台的阻力。&nbsp;

您可以在[此处](https://www.citrix.com/networking/microservices.html)了解有关 NetScaler CPX 的更多信息。

_&nbsp;-- Mikko Disini，Citrix Systems NetScaler 产品管理总监

