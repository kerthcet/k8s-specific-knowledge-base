---
layout: blog
title: "Frontiers, fsGroups and frogs: Kubernetes 1.23 发布采访"
date: 2022-04-29
---

**作者**: Craig Box (Google)

举办每周一次的[来自 Google 的 Kubernetes 播客](https://kubernetespodcast.com/) 
的亮点之一是与每个新 Kubernetes 版本的发布经理交谈。发布团队不断刷新。许多人从小型文档修复开始，逐步晋升为影子角色，然后最终领导发布。

在我们为下周发布的 1.24 版本做准备时，[按照长期以来的传统](https://www.google.com/search?q=%22release+interview%22+site%3Akubernetes.io%2Fblog)，
很高兴带大家回顾一下 1.23 的故事。该版本由 SUSE 的现场工程师 [Rey Lejano](https://twitter.com/reylejano) 领导。
在 12 月[我与 Rey 交谈过](https://kubernetespodcast.com/episode/167-kubernetes-1.23/)，当时他正在等待他的第一个孩子的出生。

请确保你[订阅，无论你在哪里获得你的播客](https://kubernetespodcast.com/subscribe/)，
以便你听到我们所有来自云原生社区的故事，包括下周 1.24 的故事。

**为清晰起见本稿件经过了简单的编辑和浓缩。**

---
**CRAIG BOX：我想从现在每个人最关心的问题开始。让我们谈谈非洲爪蛙！**

REY LEJANO：[笑]哦，你是说 [Xenopus lavis](https://en.wikipedia.org/wiki/African_clawed_frog)，非洲爪蛙的学名？

**CRAIG BOX：当然。**

REY LEJANO：知道的人不多，但我曾就读于戴維斯加利福尼亚大学的微生物学专业。
我在生物化学实验室做了大约四年的生物化学研究，并且我[确实发表了一篇研究论文](https://www.sciencedirect.com/science/article/pii/)。
它实际上是在糖蛋白上，特别是一种叫做“皮质颗粒凝集素”的东西。我们使用青蛙，因为它们会产生大量的蛋，我们可以从中提取蛋白质。
这种蛋白质可以防止多精症。当精子进入卵子时，卵子会向细胞膜释放一种糖蛋白，即皮质颗粒凝集素，并阻止任何其他精子进入卵子。

**CRAIG BOX：你是否能够从我们对青蛙进行的测试中汲取任何东西并将其推广到更高阶的哺乳动物？**

REY LEJANO：是的。由于哺乳动物也有皮质颗粒凝集素，我们能够分析收敛和进化模式，不仅来自多种青蛙，还包括哺乳动物。

**CRAIG BOX：现在，这里有几个不同的线索需要解开。当你年轻的时候，是什么引导你进入生物学领域，可以侧重介绍技术方面的内容吗？**

REY LEJANO：我认为这主要来自家庭，因为我在医学领域确实有可以追溯到几代人的家族史。所以我觉得那是进入大学的自然路径。

**CRAIG BOX：现在，你正在一个更抽象的技术领域工作。是什么让你离开了微生物学？**

REY LEJANO：[笑]嗯，我一直对科技很感兴趣。我年轻的时候自学了一点编程，在高中之前，做了一些网络开发的东西。
只是在实验室里有点焦头烂额了，实际上是在地下室。我有一个很好的机会加入了一家专门从事 [ITIL](https://www.axelos.com/certifications/itil-service-management/what-is-itil) 
的咨询公司。实际上，我从应用性能管理开始，进入监控，进入运营管理和 ITIL，也就是把你的 IT 资产管理和服务管理与商业服务结合起来。实际上，我在这方面做了很多年。

**CRAIG BOX：这很有趣，当人们描述他们所经历的事情以及他们所从事的技术时，你几乎可以确定他们的年龄。
现在有很多人进入科技行业，但从未听说过 ITIL。他们不知道那是什么。它基本上和 SRE 类似，只是过程更加复杂。**

REY LEJANO：是的，一点没错。它不是非常云原生的。[笑]

**CRAIG BOX：一点也不。**

REY LEJANO：在云原生环境中，你并没有真正听说过它。毫无疑问，如果有人专门从事过 ITIL 工作或之前曾与 ITIL 合作过，你肯定可以看出他们已经在该领域工作了一段时间。

**CRAIG BOX：你提到你想离开地下室。这的确是程序员常待的地方。他们只是在新的地下室里给了你一点光吗？**

REY LEJANO：[笑]他们确实给了我们更好的照明。有时也能获得一些维生素 D。

**CRAIG BOX：总结一下你的过往职业经历：在过去的一年里，随着全球各地的发展变化，我认为如今微生物学技能可能比你在校时更受欢迎？**

REY LEJANO：哦，当然。我肯定能看到进入这个领域的人数大增。此外，阅读当前世界正在发生的事情也会带回我过去所学的所有教育。

**CRAIG BOX：你和当时的同学还在保持联系吗？**

REY LEJANO：只是一些亲密的朋友，但不是在微生物学领域。

**CRAIG BOX：我认为，这次的全球疫情可能让人们对科学、技术、工程和数学领域重新产生兴趣。
看看这对整个社会有什么影响，将是很有趣的。**

REY LEJANO：是的。我认为那会很棒。

**CRAIG BOX：你提到在一家咨询公司工作，从事 IT 管理、应用程序性能监控等工作。Kubernetes 是什么时候进入你的职业生涯的？**

REY LEJANO：在我工作的公司，我的一位好朋友于 2015 年年中离职。他去了一家非常热衷于 Docker 的公司。
他教了我一点东西。我在 2015 年左右，也许是 2016 年，做了我的第一次 “docker run”。
然后，我们用于 ITIL 框架的一个应用程序在 2018 年左右被容器化了，也在 Kubernetes 中。
那个时候，它是有些问题的。那是我第一次接触 Kubernetes 和容器化应用程序。

然后我离开了那家公司，实际上我加入了我在 [RX-M](https://rx-m.com/) 的朋友，这是一家云原生咨询和培训公司。
他们专门从事 Docker 和 Kubernetes 的工作。我能够让我脚踏实地。我拿到了 CKD 和 CKA 证书。
他们在鼓励我们学习更多关于 Kubernetes 的知识和参与社区活动方面真的非常棒。

**CRAIG BOX：然后，你将看到人们采用 Kubernetes 和容器化的整个生命周期，通过你自己的初始旅程，然后通过帮助客户。你如何描述这段旅程从早期到今天的变化？**

REY LEJANO：我认为早期有很多问题，为什么我必须容器化？为什么我不能只使用虚拟机？

**CRAIG BOX：这是你的简历上的一个条目。**

REY LEJANO：[笑]是的。现在，我认为人们知道使用容器的价值，以及使用 Kubernetes 编排容器的价值。我不想说“赶上潮流”，但它已经成为编排容器的事实标准。

**CRAIG BOX：这不是咨询公司需要走出去向客户推销他们应该做的事情。他们只是把它当作会发生的事情，并开始在这条路上走得更远一些，也许。**

REY LEJANO：当然。

**CRAIG BOX：在这样的咨询公司工作，你有多少时间致力于改善流程，也许是为多个客户，然后研究如何将这项工作推向上游，而不是每次只为单个客户做有偿工作？**


REY LEJANO：那时，情况会有所不同。他们帮我介绍了自己，我也了解了很多关于云原生环境和 Kubernetes 本身的情况。
他们帮助我了解如何将云原生环境及其周围的工具一起使用。我在那家公司的老板，Randy，实际上他鼓励我们开始向上游做贡献，
并鼓励我加入发布团队。他只是说，这是个很好的机会。这对我在早期就开始做贡献有很大的帮助。

**CRAIG BOX：发布团队是你参与上游 Kubernetes 贡献的方式吗？**

REY LEJANO：实际上，没有。我的第一个贡献是 SIG Docs。我认识了 Taylor Dolezal——他是 1.19 的发布团队负责人，但他也参与了 SIG Docs。
我在 KubeCon 2019 遇到了他，在午餐时我坐在他的桌子旁。我记得 Paris Pittman 在万豪酒店主持了这次午餐会。
Taylor 说他参与了 SIG Docs。他鼓励我加入。我开始参加会议，开始做一些路过式的 PR。
这就是我们所说的 - 驱动式 - 小错字修复。然后做更多的事情，开始发送更好或更高质量的拉取请求，并审查 PR。

**CRAIG BOX：你第一次正式担任发布团队的角色是什么时候？**

REY LEJANO：那是在 12月的 [1.18](https://github.com/kubernetes/sig-release/blob/master/releases/release-1.18/release_team.md)。
当时我的老板鼓励我去申请。我申请了，很幸运地被录取了，成为发布说明的影子。然后从那里开始，我在发布说明中呆了几个周期，
然后去了文档，自然而然地领导了文档，然后去了增强版，现在我是 1.23 的发行负责人。

**CRAIG BOX：我不知道很多人都会考虑到一个好的发行说明需要什么。你说什么才是呢？**

REY LEJANO：[笑]你必须告诉最终用户发生了什么变化，或者他们在发行说明中可能看到什么效果。
它不必是高度技术性的。它可以只是几行字，只是说有什么变化，如果他们也必须做任何事情，他们必须做什么。

**CRAIG BOX：我不知道很多人会考虑一个好的发布说明的内容。你会说什么？**

REY LEJANO：当我是这个周期的发布负责人时，我说过几次。你从发布团队得到的东西和你投入的东西一样多，或者说它直接与你投入的东西相一致。
我学到了很多东西。我在进入发布团队时就有这样的心态：向角色领导学习，也向其他影子学习。
这实际上是我的第一个角色负责人告诉我的一句话。我仍然铭记于心，那是在 1.18 中。那是 Eddie，在我们第一次见面时，我仍然牢记在心。

**CRAIG BOX：当然，你是 [1.23 的发布负责人](https://github.com/kubernetes/sig-release/tree/master/releases/release-1.23)。首先，祝贺发布。**

REY LEJANO：非常感谢。

**CRAIG BOX：这个版本的主题是[最后战线](https://kubernetes.io/blog/2021/12/07/kubernetes-1-23-release-announcement/)。
请告诉我我们是如何确定主题和标志的故事。**

REY LEJANO：最后战线代表了几件事。它不仅代表了此版本的下一个增强功能，而且 Kubernetes 本身也有《星际迷航》的参考历史。
Kubernetes 的原始代号是 Project Seven，指的是最初来自《星际迷航》中的 Seven of Nine。
在 Kubernetes 的 logo 中掌舵的七根辐条也是如此。当然，还有 Kubernetes 的前身 Borg。

最后战线继续星际迷航参考。这是星际迷航宇宙中两个标题的融合。一个是[星际迷航 5：最后战线](https://en.wikipedia.org/wiki/Star_Trek_V:_The_Final_Frontier)，还有星际迷航：下一代。

**CRAIG BOX：你对《星际迷航 5》是一部奇数电影有什么看法，而且它们[通常被称为比偶数电影票房少](https://screenrant.com/star-trek-movies-odd-number-curse-explained/)？**

REY LEJANO：我不能说，因为我是一个科幻书呆子，我喜欢他们所有的人，尽管他们很糟糕。即使是《下一代》系列之后的电影，我仍然喜欢所有的电影，尽管我知道有些并不那么好。

**CRAIG BOX：我记得星际迷航 5 是由 William Shatner 执导对吗？**

REY LEJANO：是的，对的。

**CRAIG BOX：我认为这说明了一切。**

REY LEJANO：[笑]是的。

**CRAIG BOX：现在，我明白了，主题来自于 [SIG 发布章程](https://github.com/kubernetes/community/blob/master/sig-release/charter.md)？**

REY LEJANO：是的。SIG 发布章程中有一句话，“确保有一个一致的社区成员小组来支持不同时期的发布过程。”
在发布团队中，我们每一个发布周期都有新的影子加入。有了这个，我们与这个社区一起成长。我们正在壮大发布团队的成员。
我们正在增加 SIG 版本。我们正在发展 Kubernetes 社区本身。对于很多人来说，这是他们第一次为开源做出贡献，所以我说这是他们新的开源前沿。

**CRAIG BOX：而这个标志显然是受《星际迷航》的启发。让我感到惊讶的是，花了那么长时间才有人走这条路**

REY LEJANO：我也很惊讶。我不得不重新学习 Adobe Illustrator 来创建标志。

**CRAIG BOX：这是你自己的作品，是吗？**

REY LEJANO：这是我自己的作品。

**CRAIG BOX：非常好。**

REY LEJANO：谢谢。有趣的是，相对于飞船，银河系实际上花了我最长的时间。我花了几天时间才把它弄正确。
我一直在对它进行微调，所以在真正发布时可能会有最后的改变。

**CRAIG BOX：没有边界是真正的终结。**

REY LEJANO：是的，非常正确。

**CRAIG BOX：现在从发布的主题转到实质内容，也许，1.23 中有什么新内容？**

REY LEJANO：我们有 47 项增强功能。我将运行大部分稳定的，甚至全部的，一些关键的 Beta 版，以及一些 1.23 版的 Alpha 增强。

其中一个关键的改进是[双堆栈 IPv4/IPv6](https://github.com/kubernetes/enhancements/issues/563)，它在 1.23 版本中采用了 GA。

一些背景信息：双堆栈在 1.15 中作为 Alpha 引入。你可能在 KubeCon 2019 上看到了一个主题演讲。
那时，双栈的工作方式是，你需要两个服务--你需要每个IP家族的服务。你需要一个用于 IPv4 的服务和一个用于 IPv6 的服务。
它在 1.20 版本中被重构了。在 1.21 版本中，它处于测试阶段；默认情况下，集群被启用为双堆栈。

然后在 1.23 版本中，我们确实删除了 IPv6 双栈功能标志。这不是强制性的使用双栈。它实际上仍然不是 "默认"的。
Pod，服务仍然默认为单栈。要使用双栈，有一些要求。节点必须可以在 IPv4 和 IPv6 网络接口上进行路由。
你需要一个支持双栈的 CNI 插件。Pod 本身必须被配置为双栈。而服务需要 ipFamilyPolicy 字段来指定喜欢双栈或要求双栈。


**CRAIG BOX：这听起来暗示仍然需要 v4。你是否看到了一个我们实际上可以转移到仅有 v6 的集群的世界？？**

REY LEJANO：我认为在未来很多很多年里，我们都会谈论 IPv4 和 IPv6。我记得很久以前，他们一直在说 "这将全部是 IPv6"，而那是几十年前的事了。

**CRAIG BOX：我想我之前可能在节目中提到过，Vint Cerf [在伦敦参加了一个会议](https://www.youtube.com/watch?v=AEaJtZVimqs)，
他当时做了一个公开演讲说，现在是v6的时代了。那是至少 10 年前的事了。现在还不是 v6 的时代，我的电脑桌面上还没有一天拥有 Linux。**

REY LEJANO：[笑]在我看来，这是 1.23 版稳定的一大关键功能。

1.23 版的另一个亮点是 [Pod 安全许可进入 Beta 版](/blog/2021/12/09/pod-security-admission-beta/)。
我知道这个功能将进入 Beta 版，但我强调这一点是因为有些人可能知道，PodSecurityPolicy 在 1.21 版本中被废弃，目标是在 1.25 版本中被移除。
Pod 安全接纳取代了 Pod 安全策略。它是一个准入控制器。它根据预定义的 Pod 安全标准集对 Pod 进行评估，以接纳或拒绝 Pod 的运行。

Pod 安全标准分为三个级别。特权，这是完全开放的。基线，已知的特权升级被最小化。或者 限制级，这是强化的。而且你可以将 Pod 安全标准设置为以三种模式运行，
即强制：拒绝任何违规的 Pod；审计：允许创建 Pod，但记录违规行为；或警告：它会向用户发送警告消息，并且允许该 Pod。

**CRAIG BOX：你提到 PodSecurityPolicy 将在两个版本的时间内被弃用。我们是否对这些功能进行了排列，以便届时 Pod 安全接纳将成为 GA？**

REY LEJANO：是的。当然可以。我稍后也会为另一个功能谈谈这个问题。还有另一个功能也进入了 GA。这是一个归入 GA 的 API，
因此 Beta 版的 API 现在被废弃了。我稍稍讲一下这个问题。

**CRAIG BOX：好吧。让我们来谈谈名单上的下一个问题。**

REY LEJANO：让我们继续讨论更稳定的增强功能。一种是 [TTL 控制器](https://github.com/kubernetes/enhancements/issues/592)。
它在作业完成后清理作业和 Pod。有一个 TTL 计时器在作业或 Pod 完成后开始计时。此 TTL 控制器监视所有作业，
并且需要设置 ttlSecondsAfterFinished。该控制器将查看 ttlSecondsAfterFinished，结合最后的过渡时间，如果它大于现在。
如果是，那么它将删除该作业和该作业的 Pod。

**CRAIG BOX：粗略地说，它可以称为垃圾收集器吗？**

REY LEJANO：是的。用于 Pod 和作业，或作业和 Pod 的垃圾收集器。

**CRAIG BOX：如果 Kubernetes 真正成为一种编程语言，它当然必须实现垃圾收集器。**

REY LEJANO：是的。还有另一个，也将在 Alpha 中出现。[笑]

**CRAIG BOX：告诉我。**

REY LEJANO： 那个是在 Alpha 中出现的。这实际上是我最喜欢的功能之一，今天我只想强调几个。
[StafeulSet 的 PVC 将被清理](https://github.com/kubernetes/enhancements/issues/1847)。
当你删除那个 StatefulSet 时，它将自动删除由 StatefulSets 创建的 PVC。


**CRAIG BOX：我们的稳定功能之旅的下一步是什么？**

REY LEJANO：下一个是，[跳过卷所有权更改进入稳定状态](https://github.com/kubernetes/enhancements/issues/695)。
这是来自 SIG 存储。有的时候，当你运行一个有状态的应用程序时，就像许多数据库一样，它们对下面的权限位变化很敏感。
目前，当一个卷被绑定安装在容器内时，该卷的权限将递归更改。这可能需要很长时间。
-->

现在，有一个字段，即 fsGroupChangePolicy，它允许你作为用户告诉 Kubernetes 你希望如何更改该卷的权限和所有权。
你可以将其设置为总是、始终更改权限，或者只是在不匹配的情况下，只在顶层的权限所有权变化与预期不同的情况下进行。

**CRAIG BOX：确实感觉很多这些增强功能都来自一个非常特殊的用例，有人说，“嘿，这对我来说不起作用，我已经研究了一个功能，它可以完全满足我需要的东西”**

REY LEJANO：当然可以。人们为这些问题创建问题，然后创建 Kubernetes 增强提案，然后被列为发布目标。

**CRAIG BOX：此版本中的另一个 GA 功能--临时卷。**

REY LEJANO：我们一直能够将空目录用于临时卷，但现在我们实际上可以拥有[临时内联卷] (https://github.com/kubernetes/enhancements/issues/1698)，
这意味着你可以使用标准 CSI 驱动程序并能够与它一起使用临时卷。

**CRAIG BOX：而且，很长一段时间，[CronJobs](https://github.com/kubernetes/enhancements/issues/19)。**

REY LEJANO：CronJobs 很有趣，因为它在 1.23 之前是稳定的。对于 1.23，它仍然被跟踪，但它只是清理了一些旧控制器。
使用 CronJobs，有一个 v2 控制器。1.23 中清理的只是旧的 v1 控制器。

**CRAIG BOX：在这个版本中，是否有任何其他的重复或重大的清理工作值得注意？**

REY LEJANO：是的。有几个你可能会在主要的主题中看到。其中一个有点棘手，围绕 FlexVolumes。这是 SIG 存储公司的努力之一。
他们正在努力将树内插件迁移到 CSI 驱动。这有点棘手，因为 FlexVolumes 实际上是在 2020 年 11 月被废弃的。我们
[在 1.23 中正式宣布](https://github.com/kubernetes/community/blob/master/sig-storage/volume-plugin-faq.md#kubernetes-volume-plugin-faq-for-storage-vendors)。

**CRAIG BOX：在我看来，FlexVolumes 比 CSI 这个概念还要早。所以现在是时候摆脱它们了。**

REY LEJANO：是的。还有另一个弃用，只是一些 [klog 特定标志](https://kubernetes.io/docs/concepts/cluster-administration/system-logs/#klog)，但除此之外，1.23 中没有其他大的弃用。

**CRAIG BOX：上一届 KubeCon 的流行语，在某种程度上也是过去 12 个月的主题，是安全的软件供应链。Kubernetes 在这一领域做了哪些改进工作？**

REY LEJANO：对于 1.23 版本，Kubernetes 现在符合 SLSA 的 1 级标准，这意味着描述发布过程中分期和发布阶段的证明文件对于 SLSA 框架来说是令人满意的。

**CRAIG BOX：需要做什么才能提升到更高的水平？**

REY LEJANO：级别 1 意味着一些事情——构建是脚本化的；出处是可用的，这意味着工件是经过验证，并且已从一个阶段移交到下一个阶段；
并描述了工件是如何产生的。级别 2 意味着源是受版本控制的，也就是说，源是经过身份验证的，源是服务生成的，并且存在构建服务。SLSA 的合规性分为四个级别。

**CRAIG BOX：看起来这些水平在很大程度上受到了建立这样一个大型安全项目的影响。例如，似乎不需要很多额外的工作来提升到可验证的出处。
可能只需要几行脚本即可满足其中许多要求。**

REY LEJANO：当然。我觉得我们就快成功了；我们会看到 1.24 版本会出现什么。我确实想对 SIG 发布和发布工程部大加赞赏，
主要是 Adolfo García Veytia，他在 GitHub 和 Slack 上又名 Puerco。 他一直在推动这一进程。

**CRAIG BOX：你提到了一些 API 正在及时升级以替换其已弃用的版本。告诉我有关新 HPA API 的信息。**

REY LEJANO：[horizontal pod autoscaler v2 API](https://github.com/kubernetes/enhancements/issues/2702)，
现已稳定，这意味着 v2beta2 API 已弃用。众所周知，v1 API 并未被弃用。不同之处在于 v2 添加了对用于 HPA 的多个和自定义指标的支持。

**CRAIG BOX：现在还可以使用表达式语言验证我的 CRD。**

REY LEJANO：是的。你可以使用 [通用表达式语言，或 CEL](https://github.com/google/cel-spec)
来验证你的 CRD，因此你不再需要使用 webhook。这也使 CRD 更加自包含和声明性，因为规则现在保存在 CRD 对象定义中。

**CRAIG BOX：哪些新功能（可能是 Alpha 版或 Beta 版）引起了你的兴趣？**

REY LEJANO：除了 Pod 安全策略，我真的很喜欢支持 kubectl 调试的[临时容器](https://github.com/kubernetes/enhancements/issues/277)。
它启动一个临时容器和一个正在运行的 Pod，共享这些 Pod 命名空间，你只需运行 kubectl debug 即可完成所有故障排除。

**CRAIG BOX：使用 kubectl 处理事件的方式也发生了一些有趣的变化。**

REY LEJANO：是的。kubectl events 总是有一些问题，比如事情没有排序。
[kubectl 事件得到了改进](https://github.com/kubernetes/enhancements/issues/1440)，
所以现在你可以使用 `--watch`，它也可以使用 `--watch` 选项进行排序。那是新事物。
你实际上可以组合字段和自定义列。此外，你可以在时间线中列出最后 N 分钟的事件。你还可以使用其他标准对事件进行排序。

**CRAIG BOX：你是 SUSE 的一名现场工程师。有什么事情是你所处理的个别客户所要注意的吗？**

REY LEJANO：更多我期待帮助客户的东西。

**CRAIG BOX：好吧。**

REY LEJANO：我真的很喜欢 kubectl 事件。真的很喜欢用 StatefulSets 清理的 PVC。其中大部分是出于自私的原因，它将改进故障排除工作。[笑]

**CRAIG BOX：我一直希望发布团队负责人对我说：“是的，我有自私的理由。我终于得到了我想要的东西。”**

REY LEJANO：[大笑]

**CRAIG BOX：也许我应该竞选发布团队的负责人，这样我就可以最终让 Init 容器一劳永逸地得到修复。**

REY LEJANO：哦，Init 容器，我一直在寻找它。实际上，我已经制作了 GIF 动画，介绍了 Init 容器将如何与那个 Kubernetes 增强提案一起运行，但目前已经停止了。

**CRAIG BOX：有一天。**

REY LEJANO：总有一天。也许我不应该停下来。

**CRAIG BOX：你提到的显然是你所关注的事情。是否有任何即将推出的东西，可能是 Alpha 功能，甚至可能只是你最近看到的建议，你个人真的很期待看到它们的发展方向？**

REY LEJANO：是的。Oone 是一个非常有趣的问题，它影响了整个社区，所以这不仅仅是出于个人原因。
正如你可能已经知道的，Dockershim 已经被废弃了。而且我们确实发布了一篇博客，说它将在 1.24 中被删除。

**CRAIG BOX：吓坏了一群人。**

REY LEJANO：吓坏了一群人。从一项调查中，我们看到很多人仍在使用 Docker 和 Dockershim。
1.23 的增强功能之一是 [kubelet CRI 进入 Beta 版](https://github.com/kubernetes/enhancements/issues/2040)。 
这促进了 CRI API 的发展，而这是必需的。 这必须是 Beta 版才能在 1.24 中删除 Dockershim。

**CRAIG BOX：现在，在最后一次发布团队领导访谈中，[我们与 Savitha Raghunathan 进行了交谈](https://kubernetespodcast.com/episode/157-kubernetes-1.22/)，
她谈到了作为她的继任者她会给你什么建议。她说要关注团队成员的心理健康。你是如何采纳这个建议的？

REY LEJANO：Savitha 的建议很好。我在每次发布团队会议上都记录了一些事情。 
每次发布团队会议后，我都会停止录制，因为我们确实会录制所有会议并将其发布到 YouTube 上。
我向任何想要说任何未记录的内容的人开放发言，这不会出现在议程上。此外，我告诉人们不要在周末工作。
我曾经打破过这个规则，但除此之外，我告诉人们它可以等待。只要注意你的心理健康。

**CRAIG BOX：刚刚宣布[来自 Jetstack 的 James Laverack](https://twitter.com/JamesLaverack/status/1466834312993644551)
将成为 1.24 的发布团队负责人。James 和我在 San Diego 的最后一届 KubeCon 上分享了一顿有趣的墨西哥晚餐。**

REY LEJANO：哦，不错。我不知道你认识 James。

**CRAIG BOX：英国科技界。我们是一个非常小的世界。你对 James 的建议是什么？**

REY LEJANO：对于 1.24，我要告诉 James 的是在发布团队会议中使用教学时刻。当你第一次成为影子时，这是非常令人生畏的。
这非常困难，因为你不知道存储库。你不知道发布过程。周围的每个人似乎都知道发布过程，并且非常熟悉发布过程是什么。 
但作为第一次出现的影子，你并不了解社区的所有白话。我只是建议使用教学时刻。在发布团队会议上花几分钟时间，让新影子更容易上手并熟悉发布过程。

**CRAIG BOX：在你参与的这段时间里，这个过程是否有重大演变？或者你认为它正在有效地做它需要做的事情？**

REY LEJANO：它总是在不断发展。我记得我第一次做发布说明时，1.18，我们说我们的目标是自动化和编程，这样我们就不再有发行说明团队了。
这改变了很多[笑]。尽管 Adolfo 和 James 在发布说明过程中取得了重大进展，但他们在 krel 中创建了一个子命令来生成发行说明。

但如今，他们所有的发行说明都更加丰富了。在自动化过程中，仍然没有达到。每个发布周期，都有一点不同的东西。
对于这个发布周期，我们有一个生产就绪审查截止日期。这是一个软期限。生产就绪审查是社区中几个人的审查。
实际上从 1.21 开始就需要它，它确保增强是可观察的、可扩展的、可支持的，并且在生产中运行是安全的，也可以被禁用或回滚。 
在 1.23 中，我们有一个截止日期，要求在特定日期之前完成生产就绪审查。

**CRAIG BOX：你如何发现每年发布三个版本，而不是四个版本？**

REY LEJANO：从一年四个版本转为三个版本，在我看来是一种进步，因为我们支持最后三个版本，
现在我们实际上可以支持在一个日历年内的最后一个版本，而不是在 12 个月中只有 9 个月。

**CRAIG BOX：日历上的下一个活动是下周一开始的 [Kubernetes 贡献者庆典](https://www.kubernetes.dev/events/kcc2021/)。我们可以从活动中期待什么？**

REY LEJANO：这是我们第二次举办这个虚拟活动。这是一个虚拟的庆祝活动，以表彰整个社区和我们今年的所有成就，以及贡献者。
在这周的庆典中有许多活动。它从 12 月 13 日的那一周开始。

有像 Kubernetes 贡献者奖这样的活动，SIG 对社区和贡献者的辛勤工作进行表彰和奖励。
也有一个 DevOps 聚会游戏。还有一个云原生的烘烤活动。我强烈建议人们去
[kubernetes.dev/celebration](https://www.kubernetes.dev/events/past-events/2021/kcc2021/)
了解更多。

**CRAIG BOX： 究竟如何评判一个虚拟的烘焙比赛呢？**

REY LEJANO：那我不知道。[笑]

**CRAIG BOX：我尝了尝我的烤饼。我认为他们是最好的。我给他们打了 10 分（满分 10 分）。**

REY LEJANO：是的。这是很难做到的。我不得不说，这道菜可能是什么，它与 Kubernetes 或开源或与 CNCF 的关系有多密切。
有几个评委。我知道 Josh Berkus 和 Rin Oliver 是主持烘焙比赛的几个评委。

**CRAIG BOX：是的。我们与 Josh 谈到了他对厨房的热爱，因此他似乎非常适合这个角色。**

REY LEJANO：他是。

**CRAIG BOX：最后，你的妻子和你自己将在一月份迎来你们的第一个孩子。你是否为此进行过生产准备审查？**

REY LEJANO：我认为我们没有通过审查。[笑]

**CRAIG BOX：还有时间。**

REY LEJANO：我们正在努力重构。我们将在 12 月进行一些重构，然后再次使用 `--apply`。

---

**[Rey Lejano](https://twitter.com/reylejano) 是 SUSE 的一名现场工程师，来自 Rancher Labs，并且是 Kubernetes 1.23 的发布团队负责人。
他现在也是 SIG Docs 的联合主席。他的儿子 Liam 现在 3 个半月大。**

**你可以在 Twitter 上的 [@KubernetesPod](https://twitter.com/KubernetesPod)
找到[来自谷歌的 Kubernetes 播客](http://www.kubernetespodcast.com/)，
你也可以[订阅](https://kubernetespodcast.com/subscribe/)，这样你就不会错过任何一集。**
