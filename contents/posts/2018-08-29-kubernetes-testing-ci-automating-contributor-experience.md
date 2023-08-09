---
layout: blog
title: '机器可以完成这项工作，一个关于 kubernetes 测试、CI 和自动化贡献者体验的故事'
date: 2019-08-29
slug: the-machines-can-do-the-work-a-story-of-kubernetes-testing-ci-and-automating-the-contributor-experience
---



**作者**：Aaron Crickenberger（谷歌）和 Benjamin Elder（谷歌）


_”大型项目有很多不那么令人兴奋，但却很辛苦的工作。比起辛苦工作，我们更重视把时间花在自动化重复性工作上，如果这项工作无法实现自动化，我们的文化就是承认并奖励所有类型的贡献。然而，英雄主义是不可持续的。“_ - [Kubernetes Community Values](https://git.k8s.io/community/values.md#automation-over-process)


像许多开源项目一样，Kubernetes 托管在 GitHub 上。 如果项目位于在开发人员已经工作的地方，使用的开发人员已经知道的工具和流程，那么参与的障碍将是最低的。 因此，该项目完全接受了这项服务：它是我们工作流程，问题跟踪，文档，博客平台，团队结构等的基础。


这个策略奏效了。 它运作良好，以至于该项目迅速超越了其贡献者的人类能力。 接下来是一次令人难以置信的自动化和创新之旅。 我们不仅需要在飞行途中重建我们的飞机而不会崩溃，我们需要将其转换为火箭飞船并发射到轨道。 我们需要机器来完成这项工作。


## 工作


最初，我们关注的事实是，我们需要支持复杂的分布式系统（如 Kubernetes）所要求的大量测试。 真实世界中的故障场景必须通过端到端（e2e）测试来执行，确保正确的功能。 不幸的是，e2e 测试容易受到薄片（随机故障）的影响，并且需要花费一个小时到一天才能完成。


进一步的经验揭示了机器可以为我们工作的其他领域：


* Pull Request 工作流程
  * 贡献者是否签署了我们的 CLA？
  * Pull Request 通过测试吗？
  * Pull Request 可以合并吗？
  * 合并提交是否通过了测试？
* 鉴别分类
  * 谁应该审查 Pull Request？
  * 是否有足够的信息将问题发送给合适的人？
  * 问题是否依旧存在？
* 项目健康
  * 项目中发生了什么？
  * 我们应该注意什么？


当我们开发自动化来改善我们的情况时，我们遵循了以下几个指导原则：


* 遵循适用于 Kubernetes 的推送/拉取控制循环模式
* 首选无状态松散耦合服务
* 更倾向于授权整个社区权利，而不是赋予少数核心贡献者权力
* 做好自己的事，而不要重新造轮子


## 了解 Prow


这促使我们创建 [Prow](https://git.k8s.io/test-infra/prow) 作为我们自动化的核心组件。 Prow有点像 [If This, Then That](https://ifttt.com/) 用于 GitHub 事件， 内置 [commands](https://prow.k8s.io/command-help)， [plugins](https://prow.k8s.io/plugins)， 和实用程序。 我们在  Kubernetes 之上建立了 Prow，让我们不必担心资源管理和日程安排，并确保更愉快的运营体验。


Prow 让我们做以下事情：


* 允许我们的社区通过评论诸如“/priority critical-urgent”，“/assign mary”或“/close”之类的命令对 issues/Pull Requests 进行分类
* 根据用户更改的代码数量或创建的文件自动标记 Pull Requests
* 标出长时间保持不活动状态 issues/Pull Requests
* 自动合并符合我们PR工作流程要求的 Pull Requests
* 运行定义为[Knative Builds](https://github.com/knative/build)的 Kubernetes Pods或 Jenkins jobs的 CI 作业
* 实施组织范围和重构 GitHub 仓库策略，如[Knative Builds](https://github.com/kubernetes/test-infra/tree/master/prow/cmd/branchprotector)和[GitHub labels](https://github.com/kubernetes/test-infra/tree/master/label_sync)


Prow最初由构建 Google Kubernetes Engine 的工程效率团队开发，并由 Kubernetes SIG Testing 的多个成员积极贡献。 Prow 已被其他几个开源项目采用，包括 Istio，JetStack，Knative 和 OpenShift。 [Getting started with Prow](https://github.com/kubernetes/test-infra/tree/master/prow#getting-started)需要一个 Kubernetes 集群和 `kubectl apply starter.yaml`（在 Kubernetes 集群上运行 pod）。


一旦我们安装了 Prow，我们就开始遇到其他的问题，因此需要额外的工具以支持 Kubernetes 所需的规模测试，包括：


- [Boskos](https://github.com/kubernetes/test-infra/tree/master/boskos): 管理池中的作业资源（例如 GCP 项目），检查它们是否有工作并自动清理它们 ([with monitoring](http://velodrome.k8s.io/dashboard/db/boskos-dashboard?orgId=1))
- [ghProxy](https://github.com/kubernetes/test-infra/tree/master/ghproxy): 优化用于 GitHub API 的反向代理 HTTP 缓存，以确保我们的令牌使用不会达到 API 限制 ([with monitoring](http://velodrome.k8s.io/dashboard/db/github-cache?refresh=1m&orgId=1))
- [Greenhouse](https://github.com/kubernetes/test-infra/tree/master/greenhouse): 允许我们使用远程 bazel 缓存为 Pull requests 提供更快的构建和测试结果 ([with monitoring](http://velodrome.k8s.io/dashboard/db/bazel-cache?orgId=1))
- [Splice](https://github.com/kubernetes/test-infra/tree/master/prow/cmd/splice): 允许我们批量测试和合并 Pull requests，确保我们的合并速度不仅限于我们的测试速度
- [Tide](https://github.com/kubernetes/test-infra/tree/master/prow/cmd/tide): 允许我们合并通过 GitHub 查询选择的 Pull requests，而不是在队列中排序，允许显着更高合并速度与拼接一起


##　关注项目健康状况


随着工作流自动化的实施，我们将注意力转向了项目健康。我们选择使用 Google Cloud Storage (GCS)作为所有测试数据的真实来源，允许我们依赖已建立的基础设施，并允许社区贡献结果。然后，我们构建了各种工具来帮助个人和整个项目理解这些数据，包括：


* [Gubernator](https://github.com/kubernetes/test-infra/tree/master/gubernator): 显示给定 Pull Request 的结果和测试历史
* [Kettle](https://github.com/kubernetes/test-infra/tree/master/kettle): 将数据从 GCS 传输到可公开访问的 bigquery 数据集
* [PR dashboard](https://k8s-gubernator.appspot.com/pr): 一个工作流程识别仪表板，允许参与者了解哪些 Pull Request 需要注意以及为什么
* [Triage](https://storage.googleapis.com/k8s-gubernator/triage/index.html): 识别所有作业和测试中发生的常见故障
* [Testgrid](https://k8s-testgrid.appspot.com/): 显示所有运行中给定作业的测试结果，汇总各组作业的测试结果


我们与云计算本地计算基金会（CNCF）联系，开发 DevStats，以便从我们的 GitHub 活动中收集见解，例如：


* [Which prow commands are people most actively using](https://k8s.devstats.cncf.io/d/5/bot-commands-repository-groups?orgId=1)
* [PR reviews by contributor over time](https://k8s.devstats.cncf.io/d/46/pr-reviews-by-contributor?orgId=1&var-period=d7&var-repo_name=All&var-reviewers=All)
* [Time spent in each phase of our PR workflow](https://k8s.devstats.cncf.io/d/44/pr-time-to-approve-and-merge?orgId=1)


## Into the Beyond


今天，Kubernetes 项目跨越了5个组织125个仓库。有31个特殊利益集团和10个工作组在项目内协调发展。在过去的一年里，该项目有 [来自13800多名独立开发人员的参与](https://k8s.devstats.cncf.io/d/13/developer-activity-counts-by-repository-group?orgId=1&var-period_name=Last%20year&var-metric=contributions&var-repogroup_name=All)。


在任何给定的工作日，我们的 Prow 实例[运行超过10,000个 CI 工作](http://velodrome.k8s.io/dashboard/db/bigquery-metrics?panelId=10&fullscreen&orgId=1&from=now-6M&to=now); 从2017年3月到2018年3月，它有430万个工作岗位。 这些工作中的大多数涉及建立整个 Kubernetes 集群，并使用真实场景来实施它。 它们使我们能够确保所有受支持的 Kubernetes 版本跨云提供商，容器引擎和网络插件工作。 他们确保最新版本的 Kubernetes 能够启用各种可选功能，安全升级，满足性能要求，并跨架构工作。


今天[来自CNCF的公告](https://www.cncf.io/announcement/2018/08/29/cncf-receives-9-million-cloud-credit-grant-from-google) - 注意到    Google Cloud 有开始将 Kubernetes 项目的云资源的所有权和管理权转让给 CNCF 社区贡献者，我们很高兴能够开始另一个旅程。 允许项目基础设施由贡献者社区拥有和运营，遵循对项目其余部分有效的相同开放治理模型。 听起来令人兴奋。 请来 kubernetes.slack.com 上的 #sig-testing on kubernetes.slack.com 与我们联系。


想了解更多？ 快来看看这些资源：


* [Prow: Testing the way to Kubernetes Next](https://elder.dev/posts/prow)
* [Automation and the Kubernetes Contributor Experience](https://www.youtube.com/watch?v=BsIC7gPkH5M)
