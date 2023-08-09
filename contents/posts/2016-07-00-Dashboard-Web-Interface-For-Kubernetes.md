---
title: " Dashboard - Kubernetes 的全功能 Web 界面 "
date: 2016-07-15
slug: dashboard-web-interface-for-kubernetes
---



_编者按：这篇文章是[一系列深入的文章](https://kubernetes.io/blog/2016/07/five-days-of-kubernetes-1-3) 中关于Kubernetes 1.3的新内容的一部分_
[Kubernetes Dashboard](http://github.com/kubernetes/dashboard)是一个旨在为 Kubernetes 世界带来通用监控和操作 Web 界面的项目。三个月前，我们[发布](https://kubernetes.io/blog/2016/04/building-awesome-user-interfaces-for-kubernetes)第一个面向生产的版本，从那时起 dashboard 已经做了大量的改进。在一个 UI 中，您可以在不离开浏览器的情况下，与 Kubernetes 集群执行大多数可能的交互。这篇博客文章分解了最新版本中引入的新功能，并概述了未来的路线图。


**全功能的 Dashboard**

由于社区和项目成员的大量贡献，我们能够为[Kubernetes 1.3发行版](https://kubernetes.io/blog/2016/07/kubernetes-1-3-bridging-cloud-native-and-enterprise-workloads/)提供许多新功能。我们一直在认真听取用户的反馈(参见[摘要信息图表](http://static.lwy.io/img/kubernetes_dashboard_infographic.png))，并解决了最高优先级的请求和难点。
-->


Dashboard UI 现在处理所有工作负载资源。这意味着无论您运行什么工作负载类型，它都在 web 界面中可见，并且您可以对其进行操作更改。例如，可以使用[Pet Sets](/docs/user-guide/petset/)修改有状态的 mysql 安装，使用部署对 web 服务器进行滚动更新，或使用守护程序安装集群监视。



 [![](https://lh3.googleusercontent.com/p9bMGxPx4jE6_Z2KB-MktmyuAxyFst-bEk29M_Bn0Bj5ul7uzinH6u5WjHsMmqhGvBwlABZt06dwQ5qkBZiLq_EM1oddCmpwChvXDNXZypaS5l8uzkKuZj3PBUmzTQT4dgDxSXgz) ](https://lh3.googleusercontent.com/p9bMGxPx4jE6_Z2KB-MktmyuAxyFst-bEk29M_Bn0Bj5ul7uzinH6u5WjHsMmqhGvBwlABZt06dwQ5qkBZiLq_EM1oddCmpwChvXDNXZypaS5l8uzkKuZj3PBUmzTQT4dgDxSXgz)


除了查看资源外，还可以创建、编辑、更新和删除资源。这个特性支持许多用例。例如，您可以杀死一个失败的 pod，对部署进行滚动更新，或者只组织资源。您还可以导出和导入云应用程序的 yaml 配置文件，并将它们存储在版本控制系统中。



 ![](https://lh6.googleusercontent.com/zz-qjNcGgvWXrK1LIipUdIdPyeWJ1EyPVJxRnSvI6pMcLBkxDxpQt-ObsIiZsS_X0RjVBWtXYO5TCvhsymb__CGXFzKuPUnUrB4HKnAMsxtYdWLwMmHEb8c9P9Chzlo5ePHRKf5O)


这个版本包括一个用于管理和操作用例的集群节点的 beta 视图。UI 列出集群中的所有节点，以便进行总体分析和快速筛选有问题的节点。details 视图显示有关该节点的所有信息以及指向在其上运行的 pod 的链接。



 ![](https://lh6.googleusercontent.com/3CSTUy-8Tz-yAL9tCqxNUqMcWJYKK0dwk7kidE9zy-L-sXFiD4A4Y2LKEqbJKgI6Fl6xbzYxsziI8dULVXPJbu6eU0ci7hNtqi3tTuhdbVD6CG3EXw151fvt2MQuqumHRbab6g-_)


我们随发行版提供的还有许多小范围的新功能，即：支持命名空间资源、国际化、性能改进和许多错误修复(请参阅[发行说明](https://github.com/kubernetes/dashboard/releases/tag/v1.1.0)中的更多内容)。所有这些改进都会带来更好、更简单的产品用户体验。


**Future Work**



该团队对跨越多个用例的未来有着雄心勃勃的计划。我们还对所有功能请求开放，您可以在我们的[问题跟踪程序](https://github.com/kubernetes/dashboard/issues)上发布这些请求。


以下是我们接下来几个月的重点领域：

- [Handle more Kubernetes resources](https://github.com/kubernetes/dashboard/issues/961) - 显示集群用户可能与之交互的所有资源。一旦完成，dashboard 就可以完全替代cli。
- [Monitoring and troubleshooting](https://github.com/kubernetes/dashboard/issues/962) - 将资源使用统计信息/图表添加到 Dashboard 中显示的对象。这个重点领域将允许对云应用程序进行可操作的调试和故障排除。
- [Security, auth and logging in](https://github.com/kubernetes/dashboard/issues/964) - 使仪表板可从集群外部的网络访问，并使用自定义身份验证系统。


**联系我们**



我们很乐意与您交谈并听取您的反馈！

- 请在[SIG-UI邮件列表](https://groups.google.com/forum/向我们发送电子邮件！论坛/kubernetes sig ui)
- 在 kubernetes slack 上与我们聊天。[#SIG-UI channel](https://kubernetes.slack.com/messages/sig-ui/)
- 参加我们的会议：东部时间下午4点。请参阅[SIG-UI日历](https://calendar.google.com/calendar/embed?src=google.com_52lm43hc2kur57dgkibltqc6kc%40group.calendar.google.com&ctz=Europe/Warsaw)了解详细信息。
