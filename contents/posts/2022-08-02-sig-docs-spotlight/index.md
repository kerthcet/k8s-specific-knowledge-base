---
layout: blog
title: "聚光灯下的 SIG Docs"
date: 2022-08-02
slug: sig-docs-spotlight-2022
---

**作者：** Purneswar Prasad

## 简介

官方文档是所有开源项目的首选资料源。对于 Kubernetes，它是一个持续演进的特别兴趣小组 (SIG)，
人们持续不断努力制作详实的项目资料，让新贡献者和用户更容易取用这些文档。
SIG Docs 在 [kubernetes.io](https://kubernetes.io) 上发布官方文档，
包括但不限于 Kubernetes 版本发布时附带的核心 API 文档、核心架构细节和 CLI 工具文档。

为了了解 SIG Docs 的工作及其在塑造社区未来方面的更多信息，我总结了自己与联合主席
[Divya Mohan](https://twitter.com/Divya_Mohan02)（下称 DM）、
[Rey Lejano](https://twitter.com/reylejano)（下称 RL）和 Natali Vlatko（下称 NV）的谈话，
他们讲述了 SIG 的目标以及其他贡献者们如何从旁协助。

## 谈话汇总

### 你能告诉我们 SIG Docs 具体做什么吗？

SIG Docs 是 kubernetes.io 上针对 Kubernetes 项目文档的特别兴趣小组，
为 Kubernetes API、kubeadm 和 kubectl 制作参考指南，并维护官方网站的基础设施和数据分析。
他们的工作范围还包括文档发布、文档翻译、改进并向现有文档添加新功能特性、推送和审查官方 Kubernetes 博客的内容，
并在每个发布周期与发布团队合作以审查文档和博客。

### Docs 下有 2 个子项目：博客和本地化。社区如何从中受益？你想强调的这些团队是否侧重于某些贡献？

**博客**：这个子项目侧重于介绍新的或毕业的 Kubernetes 增强特性、社区报告、SIG 更新或任何与 Kubernetes
社区相关的新闻，例如思潮引领、教程和项目更新，例如即将在 1.25 版本中移除 Dockershim 和 PodSecurityPolicy。
Tim Bannister 是 SIG Docs 技术负责人之一，他做得工作非常出色，是推动文档和博客贡献的主力人物。

**本地化**：通过这个子项目，Kubernetes 社区能够在用户和贡献者之间实现更大的包容性和多样性。
自几年前以来，这也帮助该项目获得了更多的贡献者，尤其是学生们。
主要亮点之一是即将到来的本地化版本：印地语和孟加拉语。印地语的本地化工作目前由印度的学生们牵头。

除此之外，还有另外两个子项目：[reference-docs](https://github.com/kubernetes-sigs/reference-docs) 和
[website](https://github.com/kubernetes/website)，后者采用 Hugo 构建，是 Kubernetes 拥有的一个重要阵地。

### 最近有很多关于 Kubernetes 生态系统以及业界对最新 1.24 版本中移除 Dockershim 的讨论。SIG Docs 如何帮助该项目确保最终用户们平滑变更？ {#dockershim-removal}

与 Dockershim 移除有关的文档工作是一项艰巨的任务，需要修改现有文档并就弃用工作与各种利益相关方进行沟通。
这需要社区的努力，因此在 1.24 版本发布之前，SIG Docs 与 Docs and Comms 垂直行业、来自发布团队的发布负责人以及
CNCF 建立合作关系，帮助在全网宣传。设立了每周例会和 GitHub 项目委员会，以跟踪进度、审查问题和批准 PR，
并保持更新 Kubernetes 网站。这也有助于新的贡献者们了解这次弃用，因此如果出现任何 good-first-issue，
新的贡献者也可以参与进来。开通了专用的 Slack 频道用于交流会议更新、邀请反馈或就悬而未决的问题和 PR 寻求帮助。
每周例会在 1.24 发布后也持续了一个月，以审查并修复相关问题。
非常感谢 [Celeste Horgan](https://twitter.com/celeste_horgan)，与他的顺畅交流贯穿了这个弃用过程的前前后后。

### 为什么新老贡献者都应该考虑加入这个 SIG？

Kubernetes 是一个庞大的项目，起初可能会让很多人难以找到切入点。
任何开源项目的优劣总能从文档质量略窥一二，SIG Docs 的目标是建设一个欢迎新贡献者加入并对其有帮助的地方。
希望所有人可以轻松参与该项目的文档，并能从阅读中受益。他们还可以带来自己的新视角，以制作和改进文档。
从长远来看，如果他们坚持参与 SIG Docs，就可以拾阶而上晋升成为维护者。
这将有助于使 Kubernetes 这样的大型项目更易于解析和导航。

### 你如何帮助新的贡献者入门？加入有什么前提条件吗？

开始为 Docs 做贡献没有这样的前提条件。但肯定有一个很棒的对文档做贡献的指南，这个指南始终尽可能保持更新和贴合实际，
希望新手们多多阅读并将其放在趁手的地方。此外，社区 Slack 频道
[#sig-docs](https://kubernetes.slack.com/archives/C1J0BPD2M) 中有很多有用的便贴和书签。
kubernetes/website 仓库中带有 good-first-issue 标签的那些 GitHub 问题是创建你的第一个 PR 的好地方。
现在，SIG Docs 在每月的第一个星期二配合第一任 New Contributor Ambassador（新贡献者大使）角色
[Arsh Sharma](https://twitter.com/RinkiyaKeDad) 召开月度 New Contributor Meet and Greet（新贡献者见面会）。
这有助于在 SIG 内为新的贡献者建立一个更容易参与的联络形式。

### 你是否有任何真正自豪的 SIG 相关成绩？

**DM & RL** ：鉴于来自不同国家的贡献者们做出的所有出色工作，
过去几个月本地化子项目的正式推行对 SIG Docs 来说是一个巨大的胜利。
早些时候，本地化工作还没有任何流水线的流程，过去几个月的重点是通过起草一份 KEP 为本地化正式成为一个子项目提供一个框架，
这项工作计划在第三个季度结束时完成。

**DM**：另一个取得很大成功的领域是 New Contributor Ambassador（新贡献者大使）角色，
这个角色有助于为新贡献者参与项目提供更便捷的联系形式。

**NV**：对于每个发布周期，SIG Docs 都必须在短时间内评审突出介绍发布更新的发布文档和功能特性博客。
这对于文档和博客审阅者来说，始终需要付出巨大的努力。

### 你是否有一些关于 SIG Docs 未来令人兴奋的举措想让社区知道？

SIG Docs 现在期望设计一个路线图，建立稳定的人员流转机制以期推动对文档的改进，
简化社区参与 Issue 评判和已提交 PR 的评审工作。
为了建立一个这样由贡献者和 Reviewer 组成的群体，我们正在设立一项辅导计划帮助当前的贡献者们成为 Reviewer。
这绝对是一项值得关注的举措！

## 结束语

SIG Docs 在 KubeCon + CloudNativeCon North America 2021
期间举办了一次[深度访谈](https://www.youtube.com/watch?v=GDfcBF5et3Q)，涵盖了他们很棒的 SIG 主题。
他们非常欢迎想要为 Kubernetes 项目做贡献的新人，对这些新人而言 SIG Docs 已成为加入 Kubernetes 的起跳板。
欢迎加入 [SIG 会议](https://github.com/kubernetes/community/blob/master/sig-docs/README.md)，
了解最新的研究成果、来年的计划以及如何作为贡献者参与上游 Docs 团队！
