---
layout: blog
title: 'Kubernetes 1.18: Fit & Finish'
date: 2020-03-25
slug: kubernetes-1-18-release-announcement
evergreen: true
---

**作者:** [Kubernetes 1.18 发布团队](https://github.com/kubernetes/sig-release/blob/master/releases/release-1.18/release_team.md)

我们很高兴宣布 Kubernetes 1.18 版本的交付，这是我们 2020 年的第一版！Kubernetes
1.18 包含 38 个增强功能：15 项增强功能已转为稳定版，11 项增强功能处于 beta
阶段，12 项增强功能处于 alpha 阶段。

Kubernetes 1.18 是一个近乎 “完美” 的版本。为了改善 beta 和稳定的特性，已进行了大量工作，
以确保用户获得更好的体验。我们在增强现有功能的同时也增加了令人兴奋的新特性，这些有望进一步增强用户体验。

对 alpha、beta 和稳定版进行几乎同等程度的增强是一项伟大的成就。它展现了社区在提高
Kubernetes 的可靠性以及继续扩展其现有功能方面所做的巨大努力。


## 主要内容

### Kubernetes 拓扑管理器（Topology Manager）进入 Beta 阶段 - 对齐！

Kubernetes 在 1.18 版中的 Beta 阶段功能[拓扑管理器特性](https://github.com/nolancon/website/blob/f4200307260ea3234540ef13ed80de325e1a7267/content/en/docs/tasks/administer-cluster/topology-manager.md)启用
CPU 和设备（例如 SR-IOV VF）的 NUMA 对齐，这将使你的工作负载在针对低延迟而优化的环境中运行。
在引入拓扑管理器之前，CPU 和设备管理器将做出彼此独立的资源分配决策。
这可能会导致在多处理器系统上非预期的资源分配结果，从而导致对延迟敏感的应用程序的性能下降。

### Serverside Apply 推出 Beta 2

Serverside Apply 在1.16 中进入 Beta 阶段，但现在在 1.18 中进入了第二个 Beta 阶段。
这个新版本将跟踪和管理所有新 Kubernetes 对象的字段更改，从而使你知道什么更改了资源以及何时发生了更改。


### 使用 IngressClass 扩展 Ingress 并用 IngressClass 替换已弃用的注释

在 Kubernetes 1.18 中，Ingress 有两个重要的补充：一个新的 `pathType` 字段和一个新的
`IngressClass` 资源。`pathType` 字段允许指定路径的匹配方式。除了默认的
`ImplementationSpecific` 类型外，还有新的 `Exact` 和 `Prefix` 路径类型。

`IngressClass` 资源用于描述 Kubernetes 集群中 Ingress 的类型。Ingress 对象可以通过在
Ingress 资源类型上使用新的 `ingressClassName` 字段来指定与它们关联的类。
这个新的资源和字段替换了不再建议使用的 `kubernetes.io/ingress.class` 注解。

### SIG-CLI 引入了 kubectl alpha debug

SIG-CLI 一直在争论着调试工具的必要性。随着[临时容器](https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/)的发展，
我们如何使用基于 `kubectl exec` 的工具来支持开发人员的必要性变得越来越明显。
[`kubectl alpha debug` 命令](https://github.com/kubernetes/enhancements/blob/master/keps/sig-cli/20190805-kubectl-debug.md)的增加，
（由于是 alpha 阶段，非常欢迎你反馈意见），使开发人员可以轻松地在集群中调试 Pod。
我们认为这个功能的价值非常高。此命令允许创建一个临时容器，该容器在要尝试检查的
Pod 旁边运行，并且还附加到控制台以进行交互式故障排除。

### 为 Kubernetes 引入 Windows CSI 支持（Alpha）

用于 Windows 的 CSI 代理的 Alpha 版本随 Kubernetes 1.18 一起发布。CSI 代理通过允许
Windows 中的容器执行特权存储操作来启用 Windows 上的 CSI 驱动程序。

## 其它更新

### 毕业转为稳定版

- [基于污点的逐出操作](https://github.com/kubernetes/enhancements/issues/166)
- [`kubectl diff`](https://github.com/kubernetes/enhancements/issues/491)
- [CSI 块存储支持](https://github.com/kubernetes/enhancements/issues/565)
- [API 服务器 dry run](https://github.com/kubernetes/enhancements/issues/576)
- [在 CSI 调用中传递 Pod 信息](https://github.com/kubernetes/enhancements/issues/603)
- [支持树外 vSphere 云驱动](https://github.com/kubernetes/enhancements/issues/670)
- [对 Windows 负载支持 GMSA](https://github.com/kubernetes/enhancements/issues/689)
- [对不可挂载的CSI卷跳过挂载](https://github.com/kubernetes/enhancements/issues/770)
- [PVC 克隆](https://github.com/kubernetes/enhancements/issues/989)
- [移动 kubectl 包代码到 staging](https://github.com/kubernetes/enhancements/issues/1020)
- [Windows 的 RunAsUserName](https://github.com/kubernetes/enhancements/issues/1043)
- [服务和端点的 AppProtocol](https://github.com/kubernetes/enhancements/issues/1507)
- [扩展 Hugepage 特性](https://github.com/kubernetes/enhancements/issues/1539)
- [client-go signature refactor to standardize options and context handling](https://github.com/kubernetes/enhancements/issues/1601)
- [Node-local DNS cache](https://github.com/kubernetes/enhancements/issues/1024)


### 主要变化

- [EndpointSlice API](https://github.com/kubernetes/enhancements/issues/752)
- [Moving kubectl package code to staging](https://github.com/kubernetes/enhancements/issues/1020)
- [CertificateSigningRequest API](https://github.com/kubernetes/enhancements/issues/1513)
- [Extending Hugepage Feature](https://github.com/kubernetes/enhancements/issues/1539)
- [client-go 的调用规范重构来标准化选项和管理上下文](https://github.com/kubernetes/enhancements/issues/1601)


### 发布说明

在我们的[发布文档](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.18.md)中查看
Kubernetes 1.18 发行版的完整详细信息。


### 下载安装

Kubernetes 1.18 可以在 [GitHub](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.0)
上下载。要开始使用 Kubernetes，请查看这些[交互教程](https://kubernetes.io/docs/tutorials/)或通过
[kind](https://kind.sigs.k8s.io/) 使用 Docker 容器运行本地 kubernetes 集群。你还可以使用
[kubeadm](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/) 轻松安装 1.18。

### 发布团队

通过数百位贡献了技术和非技术内容的个人的努力，使本次发行成为可能。
特别感谢由 Searchable AI 的网站可靠性工程师 Jorge Alarcon Ochoa
领导的[发布团队](https://github.com/kubernetes/sig-release/blob/master/releases/release-1.18/release_team.md)。
34 位发布团队成员协调了发布的各个方面，从文档到测试、验证和功能完整性。

随着 Kubernetes 社区的发展壮大，我们的发布过程很好地展示了开源软件开发中的协作。
Kubernetes 继续快速获取新用户。这种增长创造了一个积极的反馈回路，
其中有更多的贡献者提交了代码，从而创建了更加活跃的生态系统。迄今为止，Kubernetes 已有
[40,000 独立贡献者](https://k8s.devstats.cncf.io/d/24/overall-project-statistics?orgId=1)和一个超过 3000 人的活跃社区。

### 发布 logo

![Kubernetes 1.18 发布图标](/images/blog/2020-03-25-kubernetes-1.18-release-announcement/release-logo.png)

#### 为什么是 LHC

LHC 是世界上最大，功能最强大的粒子加速器。它是由来自世界各地成千上万科学家合作的结果，
所有这些合作都是为了促进科学的发展。以类似的方式，Kubernetes
已经成为一个聚集了来自数百个组织的数千名贡献者–所有人都朝着在各个方面改善云计算的相同目标努力的项目！
发布名称 “A Bit Quarky” 的意思是提醒我们，非常规的想法可以带来巨大的变化，对开放性保持开放态度将有助于我们进行创新。


#### 关于设计者

Maru Lango 是目前居住在墨西哥城的设计师。她的专长是产品设计，她还喜欢使用 CSS + JS
进行品牌、插图和视觉实验，为技术和设计社区的多样性做贡献。你可能会在大多数社交媒体上以
@marulango 的身份找到她，或查看她的网站： https://marulango.com

### 高光用户

- 爱立信正在使用 Kubernetes 和其他云原生技术来交付[高标准的 5G 网络](https://www.cncf.io/case-study/ericsson/)，
  这可以在 CI/CD 上节省多达 90％ 的支出。
- Zendesk 正在使用 Kubernetes [运行其现有应用程序的约 70％](https://www.cncf.io/case-study/zendesk/)。
  它还正在使所构建的所有新应用都可以在 Kubernetes 上运行，从而节省时间、提高灵活性并加快其应用程序开发的速度。
- LifeMiles 因迁移到 Kubernetes 而[降低了 50% 的基础设施开支](https://www.cncf.io/case-study/lifemiles/)。
  Kubernetes 还使他们可以将其可用资源容量增加一倍。

### 生态系统更新

- CNCF 发布了[年度调查](https://www.cncf.io/blog/2020/03/04/2019-cncf-survey-results-are-here-deployments-are-growing-in-size-and-speed-as-cloud-native-adoption-becomes-mainstream/)的结果，
  表明 Kubernetes 在生产中的使用正在飞速增长。调查发现，有 78％ 的受访者在生产中使用 Kubernetes，而去年这一比例为 58％。
- CNCF 举办的 “Kubernetes 入门” 课程有[超过 100,000 人注册](https://www.cncf.io/announcement/2020/01/28/cloud-native-computing-foundation-announces-introduction-to-kubernetes-course-surpasses-100000-registrations/)。

### 项目速度

CNCF 继续完善 DevStats。这是一个雄心勃勃的项目，旨在对项目中的无数贡献数据进行可视化展示。
[K8s DevStats](https://k8s.devstats.cncf.io/d/12/dashboards?orgId=1) 展示了主要公司贡献者的贡献细目，
以及一系列令人印象深刻的预定义的报告，涉及从贡献者个人的各方面到 PR 生命周期的各个方面。

在过去的一个季度中，641 家不同的公司和超过 6,409 个个人为 Kubernetes 作出贡献。
[查看 DevStats](https://k8s.devstats.cncf.io/d/11/companies-contributing-in-repository-groups?orgId=1&var-period=m&var-repogroup_name=All)
以了解有关 Kubernetes 项目和社区发展速度的信息。

### 活动信息

Kubecon + CloudNativeCon EU 2020 已经推迟 - 有关最新信息，
请查看[新型肺炎发布页面](https://events.linuxfoundation.org/kubecon-cloudnativecon-europe/attend/novel-coronavirus-update/)。

### 即将到来的发布的线上会议

在 2020 年 4 月 23 日，和 Kubernetes 1.18 版本团队一起了解此版本的主要功能，
包括 kubectl debug、拓扑管理器、Ingress 毕业为 V1 版本以及 client-go。
在此处注册： https://www.cncf.io/webinars/kubernetes-1-18/ 。

### 如何参与

参与 Kubernetes 的最简单方法是加入众多与你的兴趣相关的[特别兴趣小组](https://github.com/kubernetes/community/blob/master/sig-list.md)（SIGs）之一。
你有什么想向 Kubernetes 社区发布的内容吗？参与我们的每周[社区会议](https://github.com/kubernetes/community/tree/master/communication)，
并通过以下渠道分享你的声音。感谢你一直以来的反馈和支持。

- 在 Twitter 上关注我们 [@Kubernetesio](https://twitter.com/kubernetesio)，了解最新动态
- 在 [Discuss](https://discuss.kubernetes.io/) 上参与社区讨论 
- 加入 [Slack](http://slack.k8s.io/) 上的社区
- 在 [Stack Overflow](http://stackoverflow.com/questions/tagged/kubernetes) 提问（或回答）
- 分享你的 Kubernetes [故事](https://docs.google.com/a/linuxfoundation.org/forms/d/e/1FAIpQLScuI7Ye3VQHQTwBASrgkjQDSS5TP0g3AXfFhwSM9YpHgxRKFA/viewform)
- 通过 [blog](https://kubernetes.io/blog/) 了解更多关于 Kubernetes 的新鲜事
- 了解更多关于 [Kubernetes 发布团队](https://github.com/kubernetes/sig-release/tree/master/release-team)的信息
