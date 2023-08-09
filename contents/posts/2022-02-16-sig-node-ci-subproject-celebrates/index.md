---
layout: blog
title: 'SIG Node CI 子项目庆祝测试改进两周年'
date: 2022-02-16
slug: sig-node-ci-subproject-celebrates
canonicalUrl: https://www.kubernetes.dev/blog/2022/02/16/sig-node-ci-subproject-celebrates-two-years-of-test-improvements/
---

**作者：** Sergey Kanzhelev (Google), Elana Hashman (Red Hat)

保证 SIG 节点上游代码的可靠性是一项持续的工作，需要许多贡献者在幕后付出大量努力。
Kubernetes、基础操作系统、容器运行时和测试基础架构的频繁发布，导致了一个复杂的矩阵，
需要关注和稳定的投资来“保持灯火通明”。2020 年 5 月，Kubernetes Node 特殊兴趣小组
（“SIG Node”）为节点相关代码和测试组织了一个新的持续集成（CI）子项目。自成立以来，SIG Node CI
子项目每周举行一次会议，即使一整个小时通常也不足以完成对所有缺陷、测试相关的 PR 和问题的分类，
并讨论组内所有相关的正在进行的工作。

在过去两年中，我们修复了阻塞合并和阻塞发布的测试，由于减少了测试缺陷，缩短了合并 Kubernetes 
贡献者的拉取请求的时间。通过我们的努力，任务通过率由开始时 42% 提高至稳定大于 90% 。我们已经解决了 144 个测试失败问题，
并在 kubernetes/kubernetes 中合并了 176 个拉取请求。
我们还帮助子项目参与者提升了 Kubernetes 贡献者的等级，新增了 3 名组织成员、6 名评审员和 2 名审批员。


Node CI 子项目是一个可入门的第一站，帮助新参与者开始使用 SIG Node。对于新贡献者来说，
解决影响较大的缺陷和测试修复的门槛很低，尽管贡献者要攀登整个贡献者阶梯还有很长的路要走：
为该团队培养了两个新的审批人花了一年多的时间。为 Kubernetes 节点及其测试基础设施提供动力的所有
不同组件的复杂性要求开发人员在很长一段时间内进行持续投资，
以深入了解整个系统，从宏观到微观。

虽然在我们的会议上有几个比较固定的贡献者；但是我们的评审员和审批员仍然很少。
我们的目标是继续增加贡献者，以确保工作的可持续分配，而不仅仅是少数关键批准者。

SIG 中的子项目如何形成、运行和工作并不总是显而易见的。每一个都是其背后的 SIG 所独有的，
并根据该小组打算支持的项目量身定制。作为一个欢迎了许多第一次 SIG Node 贡献者的团队，
我们想分享过去两年的一些细节和成就，帮助揭开我们内部工作的神秘面纱，并庆祝我们所有专注贡献者的辛勤工作！

## 时间线

***2020 年 5 月*** SIG Node CI 组于 2020 年 5 月 11 日成立，超过
[30 名志愿者](https://docs.google.com/document/d/1fb-ugvgdSVIkkuJ388_nhp2pBTy_4HEVg5848Xy7n5U/edit#bookmark=id.vsb8pqnf4gib)
注册，以改进 SIG Node CI 信号和整体可观测性。
Victor Pickard 专注于让 [testgrid 可以运行](https://testgrid.k8s.io/sig-node) ，
当时 Ning Liao 建议围绕这项工作组建一个小组，并提出 
[最初的小组章程文件](https://docs.google.com/document/d/1yS-XoUl6GjZdjrwxInEZVHhxxLXlTIX2CeWOARmD8tY/edit#heading=h.te6sgum6s8uf) 。
SIG Node 赞助成立以 Victor 作为子项目负责人的小组。Sergey Kanzhelev 不久后就加入 Victor，担任联合领导人。

在启动会议上，我们讨论了应该首先集中精力修复哪些测试，并讨论了阻塞合并和阻塞发布的测试，
其中许多测试由于基础设施问题或错误的测试代码而失败。

该子项目每周召开一小时的会议，讨论正在进行的工作会谈和分类。

***2020 年 6 月*** Morgan Bauer 、 Karan Goel 和 Jorge Alarcon Ochoa 
因其贡献而被公认为 SIG Node CI 小组的评审员，为该子项目的早期阶段提供了重要帮助。
David Porter 和 Roy Yang 也加入了 SIG 检测失败的 GitHub 测试团队。

***2020 年 8 月*** 所有的阻塞合并和阻塞发布的测试都通过了，伴有一些逻辑问题。
然而，只有 42% 的 SIG Node 测试作业是绿色的，
因为有许多逻辑错误和失败的测试。

***2020 年 10 月*** Amim Knabben 因对子项目的贡献成为 Kubernetes 组织成员。

***2021 年 1 月*** 随着健全的预提交和关键定期工作的通过，子项目讨论了清理其余定期测试并确保其顺利通过的目标。

Elana Hashman 加入了这个子项目，在 Victor 离开后帮助领导该项目。

***2021 年 2 月*** Artyom Lukianov 因其对子项目的贡献成为 Kubernetes 组织成员。

***2021 年 8 月*** 在 SIG Node 成功运行 [bug scrub](https://groups.google.com/g/kubernetes-dev/c/w2ghO4ihje0/m/VeEql1LJBAAJ)
以清理其累积的缺陷之后，会议的范围扩大到包括缺陷分类以提高整体可靠性，
在问题影响 CI 信号之前预测问题。

子项目负责人 Elana Hashman 和 Sergey Kanzhelev 都被认为是所有节点测试代码的审批人，由 SIG node 和 SIG Testing 支持。

***2021 年 9 月*** 在 Francesco Romani 牵头的 1.22 版本系列测试取得重大进展后，
该子项目设定了一个目标，即在 1.23 发布日期之前让串行任务完全通过。

Mike Miranda 因其对子项目的贡献成为 Kubernetes 组织成员。

***2021 年 11 月*** 在整个 2021 年， SIG Node 没有合并或发布的测试失败。
过去版本中的许多古怪测试都已从阻止发布的仪表板中删除，因为它们已被完全清理。

Danielle Lancashire 被公认为 SIG Node 子组测试代码的评审员。

最终节点系列测试已完全修复。系列测试由许多中断性和缓慢的测试组成，这些测试往往是碎片化的，很难排除故障。
到 1.23 版本冻结时，最后一次系列测试已修复，作业顺利通过。

[![宣布系列测试为绿色](serial-tests-green.png)](https://kubernetes.slack.com/archives/C0BP8PW9G/p1638211041322900)

1.23 版本在测试质量和 CI 信号方面得到了特别的关注。SIG Node CI 子项目很自豪能够为这样一个高质量的发布做出贡献，
部分原因是我们在识别和修复节点内外的碎片方面所做的努力。

[![Slack 大声宣布发布的版本大多是绿色的](release-mostly-green.png)](https://kubernetes.slack.com/archives/C92G08FGD/p1637175755023200)

***2021 年 12 月*** 在 1.23 版本发布时，估计有 90% 的测试工作通过了测试（2020 年 8 月为 42%）。

Dockershim 代码已从 Kubernetes 中删除。这影响了 SIG Node 近一半的测试作业，
SIG Node CI 子项目反应迅速，并重新确定了所有测试的目标。
SIG Node 是第一个完成 dockershim 外测试迁移的 SIG ，为其他受影响的 SIG 提供了示例。
绝大多数新工作在引入时都已通过，无需进一步修复。
从 Kubernetes 中[将 dockershim 除名的工作](https://k8s.io/dockershim) 正在进行中。
随着我们发现 dockershim 对 dockershim 的依赖性越来越大，dockershim 的删除仍然存在一些问题，
但我们计划在 1.24 版本之前确保所有测试任务稳定。

## 统计数据

我们过去几个月的定期会议与会者和子项目参与者：

- Aditi Sharma
- Artyom Lukianov
- Arnaud Meukam
- Danielle Lancashire
- David Porter
- Davanum Srinivas
- Elana Hashman
- Francesco Romani
- Matthias Bertschy
- Mike Miranda
- Paco Xu
- Peter Hunt
- Ruiwen Zhao
- Ryan Phillips
- Sergey Kanzhelev
- Skyler Clark
- Swati Sehgal
- Wenjun Wu

[kubernetes/test-infra](https://github.com/kubernetes/test-infra/) 源代码存储库包含测试定义。该存储库中的节点 PR 数：
- 2020 年 PR（自 5 月起）：[183](https://github.com/kubernetes/test-infra/pulls?q=is%3Apr+is%3Aclosed+label%3Asig%2Fnode+created%3A2020-05-01..2020-12-31+-author%3Ak8s-infra-ci-robot+)
- 2021 年 PR：[264](https://github.com/kubernetes/test-infra/pulls?q=is%3Apr+is%3Aclosed+label%3Asig%2Fnode+created%3A2021-01-01..2021-12-31+-author%3Ak8s-infra-ci-robot+)


CI 委员会上的问题和 PRs 分类（包括子组范围之外的分类）：

- 2020 年（自 5 月起）：[132](https://github.com/issues?q=project%3Akubernetes%2F43+created%3A2020-05-01..2020-12-31)
- 2021 年：[532](https://github.com/issues?q=project%3Akubernetes%2F43+created%3A2021-01-01..2021-12-31+)

## 未来


只是“保持灯亮”是一项大胆的任务，我们致力于改善这种体验。
我们正在努力简化 SIG Node 的分类和审查流程。

具体来说，我们正在致力于更好的测试组织、命名和跟踪：


- https://github.com/kubernetes/enhancements/pull/3042
- https://github.com/kubernetes/test-infra/issues/24641
- [Kubernetes SIG Node CI 测试网格跟踪器](https://docs.google.com/spreadsheets/d/1IwONkeXSc2SG_EQMYGRSkfiSWNk8yWLpVhPm-LOTbGM/edit#gid=0)

我们还在改进测试的可调试性和去剥落方面不断取得进展。

如果你对此感兴趣，我们很乐意您能加入我们！
在调试测试失败中有很多东西需要学习，它将帮助你熟悉 SIG Node 维护的代码。


你可以在 [SIG Node](https://github.com/kubernetes/community/tree/master/sig-node) 页面上找到有关该组的信息。
我们在我们的维护者轨道会议上提供组更新，例如：
[KubeCon + CloudNativeCon Europe 2021](https://kccnceu2021.sched.com/event/iE8E/kubernetes-sig-node-intro-and-deep-dive-elana-hashman-red-hat-sergey-kanzhelev-google) 和
[KubeCon + CloudNative North America 2021](https://kccncna2021.sched.com/event/lV9D/kubenetes-sig-node-intro-and-deep-dive-elana-hashman-derek-carr-red-hat-sergey-kanzhelev-dawn-chen-google?iframe=no&w=100%&sidebar=yes&bg=no)。
加入我们的使命，保持 kubelet 和其他 SIG Node 组件的可靠性，确保顺顺利利发布！
