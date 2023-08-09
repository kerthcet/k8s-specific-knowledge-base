---
title: "为开发指南做贡献"
linkTitle: "为开发指南做贡献"
Author: Erik L. Arneson
Description: "一位新的贡献者描述了编写和提交对 Kubernetes 开发指南的修改的经验。"
date: 2020-10-01
canonicalUrl: https://www.kubernetes.dev/blog/2020/09/28/contributing-to-the-development-guide/
resources:
- src: "jorge-castro-code-of-conduct.jpg"
  title: "Jorge Castro 正在 SIG ContribEx 的周例会上宣布 Kubernetes 的行为准则。"
---




当大多数人想到为一个开源项目做贡献时，我猜想他们可能想到的是贡献代码修改、新功能和错误修复。作为一个软件工程师和一个长期的开源用户和贡献者，这也正是我的想法。
虽然我已经在不同的工作流中写了不少文档，但规模庞大的 Kubernetes 社区是一种新型 "客户"。我只是不知道当 Google 要求我和 [Lion's Way](https://lionswaycontent.com/) 的同胞们对 Kubernetes 开发指南进行必要更新时会发生什么。

*本文最初出现在 [Kubernetes Contributor Community blog](https://www.kubernetes.dev/blog/2020/09/28/contributing-to-the-development-guide/)。*


## 与社区合作的乐趣

作为专业的写手，我们习惯了受雇于他人去书写非常具体的项目。我们专注于技术服务，产品营销，技术培训以及文档编制，范围从相对宽松的营销邮件到针对 IT 和开发人员的深层技术白皮书。
在这种专业服务下，每一个可交付的项目往往都有可衡量的投资回报。我知道在从事开源文档工作时不会出现这个指标，但我不确定它将如何改变我与项目的关系。


我们的写作和传统客户之间的关系有一个主要的特点，就是我们在一个公司里面总是有一两个主要的对接人。他们负责审查我们的文稿，并确保文稿内容符合公司的声明且对标于他们正在寻找的受众。
这随之而来的压力--正好解释了为什么我很高兴我的写作伙伴、鹰眼审稿人同时也是嗜血编辑的 [Joel](https://twitter.com/JoelByronBarker) 处理了大部分的客户联系。



在与 Kubernetes 社区合作时，所有与客户接触的压力都消失了，这让我感到惊讶和高兴。


"我必须得多仔细？如果我搞砸了怎么办？如果我让开发商生气了怎么办？如果我树敌了怎么办？"。
当我第一次加入 Kubernetes Slack 上的  "#sig-contribex "  频道并宣布我将编写 [开发指南](https://github.com/kubernetes/community/blob/master/contributors/devel/development.md) 时，这些问题都在我脑海中奔腾，让我感觉如履薄冰。


{{< imgproc jorge-castro-code-of-conduct Fit "800x450" >}}
"Kubernetes 编码准则已经生效，让我们共同勉励。" &mdash; Jorge
Castro, SIG ContribEx co-chair
{{< /imgproc >}}


事实上我的担心是多虑的。很快，我就感觉到自己是被欢迎的。我倾向于认为这不仅仅是因为我正在从事一项急需的任务，而是因为 Kubernetes 社区充满了友好、热情的人们。
在每周的 SIG ContribEx 会议上，我们关于开发指南进展情况的报告会被立即纳入其中。此外，会议的领导会一直强调 [Kubernetes](https://www.kubernetes.dev/resources/code-of-conduct/) 编码准则，我们应该像 Bill 和 Ted 一样，相互进步。



## 这并不意味着这一切都很简单

开发指南需要一次全面检查。当我们拿到它的时候，它已经捆绑了大量的信息和很多新开发者需要经历的步骤，但随着时间的推移和被忽视，它变得相当陈旧。
文档的确需要全局观，而不仅仅是点与点的修复。结果，最终我向这个项目提交了一个巨大的 pull 请求。[社区仓库](https://github.com/kubernetes/community)：新增 267 行，删除 88 行。


pull 请求的周期需要一定数量的 Kubernetes 组织成员审查和批准更改后才能合并。这是一个很好的做法，因为它使文档和代码都保持在相当不错的状态，
但要哄骗合适的人花时间来做这样一个赫赫有名的审查是很难的。
因此，那次大规模的 PR 从我第一次提交到最后合并，用了 26 天。 但最终，[它是成功的](https://github.com/kubernetes/community/pull/5003).


由于 Kubernetes 是一个发展相当迅速的项目，而且开发人员通常对编写文档并不十分感兴趣，所以我也遇到了一个问题，那就是有时候，
描述 Kubernetes 子系统工作原理的秘密珍宝被深埋在 [天才工程师的迷宫式思维](https://github.com/amwat) 中，而不是用单纯的英文写在 Markdown 文件中。
当我要更新端到端（e2e）测试的入门文档时，就一头撞上了这个问题。


这段旅程将我带出了编写文档的领域，进入到一些未完成软件的全新用户角色。最终我花了很多心思与新的 [kubetest2`框架](https://github.com/kubernetes-sigs/kubetest2) 的开发者之一合作，
记录了最新 e2e 测试的启动和运行过程。
你可以通过查看我的 [已完成的 pull request](https://github.com/kubernetes/community/pull/5045) 来自己判断结果。


## 没有人是老板，每个人都给出反馈。

但当我暗自期待混乱的时候，为 Kubernetes 开发指南做贡献以及与神奇的 Kubernetes 社区互动的过程却非常顺利。
没有争执，我也没有树敌。每个人都非常友好和热情。这是令人*愉快的*。


对于一个开源项目，没人是老板。Kubernetes 项目，一个近乎巨大的项目，被分割成许多不同的特殊兴趣小组（SIG）、工作组和社区。
每个小组都有自己的定期会议、职责分配和主席推选。我的工作与 SIG ContribEx（负责监督并寻求改善贡献者体验）和 SIG Testing（负责测试）的工作有交集。
事实证明，这两个 SIG 都很容易合作，他们渴望贡献，而且都是非常友好和热情的人。


在 Kubernetes 这样一个活跃的、有生命力的项目中，文档仍然需要与代码库一起进行维护、修订和测试。
开发指南将继续对 Kubernetes 代码库的新贡献者起到至关重要的作用，正如我们的努力所显示的那样，该指南必须与 Kubernetes 项目的发展保持同步。


Joel 和我非常喜欢与 Kubernetes 社区互动并为开发指南做出贡献。我真的很期待，不仅能继续做出更多贡献，还能继续与过去几个月在这个庞大的开源社区中结识的新朋友进行合作。
