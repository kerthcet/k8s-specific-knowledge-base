---
layout: blog
title: "Kubernetes 即将移除 Dockershim：承诺和下一步"
date: 2022-01-07
slug: kubernetes-is-moving-on-from-dockershim
---

**作者：** Sergey Kanzhelev (Google), Jim Angel (Google), Davanum Srinivas (VMware), Shannon Kularathna (Google), Chris Short (AWS), Dawn Chen (Google)

Kubernetes 将在即将发布的 1.24 版本中移除 dockershim。我们很高兴能够通过支持开源容器运行时、支持更小的
kubelet 以及为使用 Kubernetes 的团队提高工程速度来重申我们的社区价值。
如果你[使用 Docker Engine 作为 Kubernetes 集群的容器运行时](/zh-cn/docs/tasks/administer-cluster/migrating-from-dockershim/find-out-runtime-you-use/)，
请准备好在 1.24 中迁移！要检查你是否受到影响，
请参考[检查移除 Dockershim 对你的影响](/zh-cn/docs/tasks/administer-cluster/migrating-from-dockershim/check-if-dockershim-removal-affects-you/)。

## 为什么我们要离开 dockershim  {#why-we-re-moving-away-from-dockershim}

Docker 是 Kubernetes 使用的第一个容器运行时。
这也是许多 Kubernetes 用户和爱好者如此熟悉 Docker 的原因之一。
对 Docker 的支持被硬编码到 Kubernetes 中——一个被项目称为 dockershim 的组件。
随着容器化成为行业标准，Kubernetes 项目增加了对其他运行时的支持。
最终实现了容器运行时接口（CRI），让系统组件（如 kubelet）以标准化的方式与容器运行时通信。
因此，dockershim 成为了 Kubernetes 项目中的一个异常现象。
对 Docker 和 dockershim 的依赖已经渗透到 CNCF 生态系统中的各种工具和项目中，这导致了代码脆弱。

通过删除 dockershim CRI，我们拥抱了 CNCF 的第一个价值：
“[快比慢好](https://github.com/cncf/foundation/blob/master/charter.md#3-values)”。
请继续关注未来关于这个话题的交流!

## 弃用时间线  {#deprecation-timeline}

我们[正式宣布](/zh-cn/blog/2020/12/08/kubernetes-1-20-release-announcement/)于
2020 年 12 月弃用 dockershim。目标是在 2022 年 4 月，
Kubernetes 1.24 中完全移除 dockershim。
此时间线与我们的[弃用策略](/zh-cn/docs/reference/using-api/deprecation-policy/#deprecating-a-feature-or-behavior)一致，
即规定已弃用的行为必须在其宣布弃用后至少运行 1 年。

包括 dockershim 的 Kubernetes 1.23 版本，在 Kubernetes 项目中将再支持一年。
对于托管 Kubernetes 的供应商，供应商支持可能会持续更长时间，但这取决于公司本身。
无论如何，我们相信所有集群操作都有时间进行迁移。如果你有更多关于 dockershim 移除的问题，
请参考[弃用 Dockershim 的常见问题](/zh-cn/blog/2020/12/02/dockershim-faq/)。

在这个[你是否为 dockershim 的删除做好了准备](/blog/2021/11/12/are-you-ready-for-dockershim-removal/)的调查中，
我们询问你是否为 dockershim 的迁移做好了准备。我们收到了 600 多个回复。
感谢所有花时间填写调查问卷的人。

结果表明，在帮助你顺利迁移方面，我们还有很多工作要做。
存在其他容器运行时，并且已被广泛推广。但是，许多用户告诉我们他们仍然依赖 dockershim，
并且有时需要重新处理依赖项。其中一些依赖项超出控制范围。
根据收集到的反馈，我们采取了一些措施提供帮助。

## 我们的下一个步骤 {#our-next-steps}

根据提供的反馈：

- CNCF 和 1.24 版本团队致力于及时交付 1.24 版本的文档。这包括像本文这样的包含更多信息的博客文章，
  更新现有的代码示例、教程和任务，并为集群操作人员生成迁移指南。
- 我们正在联系 CNCF 社区的其他成员，帮助他们为这一变化做好准备。

如果你是依赖 dockershim 的项目的一部分，或者如果你有兴趣帮助参与迁移工作，请加入我们！
无论是我们的迁移工具还是我们的文档，总是有更多贡献者的空间。
作为起步，请在 [Kubernetes Slack](https://slack.kubernetes.io/) 上的
[#sig-node](https://kubernetes.slack.com/archives/C0BP8PW9G) 频道打个招呼！

## 最终想法  {#final-thoughts}

作为一个项目，我们已经看到集群运营商在 2021 年之前越来越多地采用其他容器运行时。
我们相信迁移没有主要障碍。我们为改善迁移体验而采取的步骤将为你指明更清晰的道路。

我们知道，从 dockershim 迁移是你可能需要执行的另一项操作，以保证你的 Kubernetes 基础架构保持最新。
对于你们中的大多数人来说，这一步将是简单明了的。在某些情况下，你会遇到问题。
社区已经详细讨论了推迟 dockershim 删除是否会有所帮助。
例如，我们最近在 [11 月 11 日的 SIG Node 讨论](https://docs.google.com/document/d/1Ne57gvidMEWXR70OxxnRkYquAoMpt56o75oZtg-OeBg/edit#bookmark=id.r77y11bgzid)和
[12 月 6 日 Kubernetes Steering 举行的委员会会议](https://docs.google.com/document/d/1qazwMIHGeF3iUh5xMJIJ6PDr-S3bNkT8tNLRkSiOkOU/edit#bookmark=id.m0ir406av7jx)谈到了它。
我们已经在 2021 年[推迟](https://github.com/kubernetes/enhancements/pull/2481/)它一次，
因为其他运行时的采用率低于我们的预期，这也给了我们更多的时间来识别潜在的阻塞问题。

在这一点上，我们相信你（和 Kubernetes）从移除 dockershim 中获得的价值可以弥补你将要进行的迁移工作。
现在就开始计划以避免出现意外。在 Kubernetes 1.24 发布之前，我们将提供更多更新信息和指南。

