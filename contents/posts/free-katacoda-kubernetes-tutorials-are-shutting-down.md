---
layout: blog
title: "免费的 Katacoda Kubernetes 教程即将关闭"
date: 2023-02-14
slug: kubernetes-katacoda-tutorials-stop-from-2023-03-31
evergreen: true
---

**作者**：Natali Vlatko，Kubernetes SIG Docs 联合主席

**译者**：Michael Yao (DaoCloud)

[Katacoda](https://katacoda.com/kubernetes) 是 O’Reilly 开设的热门学习平台，
帮助人们学习 Java、Docker、Kubernetes、Python、Go、C++ 和其他更多内容，
这个学习平台于 [2022 年 6 月停止对公众开放](https://www.oreilly.com/online-learning/leveraging-katacoda-technology.html)。
但是，从 Kubernetes 网站为相关项目用户和贡献者关联的 Kubernetes 专门教程在那次变更后仍然可用并处于活跃状态。
遗憾的是，接下来情况将发生变化，Katacoda 上有关学习 Kubernetes 的教程将在 2023 年 3 月 31 日之后彻底关闭。

Kubernetes 项目感谢 O'Reilly Media 多年来通过 Katacoda 学习平台对 Kubernetes 社区的支持。
你可以在 O'Reilly 自有的网站上阅读
[the decision to shutter katacoda.com](https://www.oreilly.com/online-learning/leveraging-katacoda-technology.html)
有关的更多信息。此次变更之后，我们将专注于移除指向 Katacoda 各种教程的链接。
我们通过 [Issue #33936](https://github.com/kubernetes/website/issues/33936)
和 [GitHub 讨论](https://github.com/kubernetes/website/discussions/38878)跟踪此主题相关的常规问题。
我们也有兴趣调研其他哪些学习平台可能对 Kubernetes 社区有益，尝试将 Katacoda 链接替换为具有类似用户体验的平台或服务。
然而，这项调研需要时间，因此我们正在积极寻觅志愿者来协助完成这项工作。
如果找到替代的平台，需要得到 Kubernetes 领导层的支持，特别是
SIG Contributor Experience、SIG Docs 和 Kubernetes Steering Committee。

Katacoda 的关闭会影响 25 个英文教程页面、对应的多语言页面以及 Katacoda Scenario仓库：
[github.com/katacoda-scenarios/kubernetes-bootcamp-scenarios](https://github.com/katacoda-scenarios/kubernetes-bootcamp-scenarios)。
我们建议你立即更新指向 Katacoda 学习平台的所有链接、指南或文档，以反映这一变化。
虽然我们还没有找到替代这个学习平台的解决方案，但 Kubernetes 网站本身就包含了大量有用的文档可助你继续学习和成长。
你可以在 https://k8s.io/docs/tutorials/ 找到所有可用的 Kubernetes 文档教程。

如果你对 Katacoda 关闭或后续从 Kubernetes 教程页面移除相关链接有任何疑问，
请在 [general issue tracking the shutdown](https://github.com/kubernetes/website/issues/33936)
上发表评论，或加入 Kubernetes Slack 的 #sig-docs 频道。
