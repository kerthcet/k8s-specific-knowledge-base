---
title: 角色与责任
content_type: concept
weight: 10
---


任何人都可以为 Kubernetes 作出贡献。随着你对 SIG Docs 的贡献增多，你可以申请
社区内不同级别的成员资格。
这些角色使得你可以在社区中承担更多的责任。
每个角色都需要更多的时间和投入。具体包括：

- 任何人（Anyone）：为 Kubernetes 文档作出贡献的普通贡献者。
- 成员（Members）：可以对 Issue 进行分派和判别，对 PR 提出无约束性的评审意见。
- 评审人（Reviewers）：可以领导对文档 PR 的评审，可以对变更的质量进行判别。
- 批准人（Approvers）：可以领导对文档的评审并合并变更。


## 任何人（Anyone）  {#anyone}

任何拥有 GitHub 账号的人都可以对 Kubernetes 作出贡献。SIG Docs
欢迎所有新的贡献者。

任何人都可以：

- 在任何 [Kubernetes](https://github.com/kubernetes/) 仓库，包括
  [`kubernetes/website`](https://github.com/kubernetes/website) 上报告 Issue。
- 对某 PR 给出无约束力的反馈信息
- 为本地化提供帮助
- 在 [Slack](https://slack.k8s.io/) 或
  [SIG Docs 邮件列表](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)
  上提出改进建议。

在[签署了 CLA](https://github.com/kubernetes/community/blob/master/CLA.md) 之后，任何人还可以：

- 发起拉取请求（PR），改进现有内容、添加新内容、撰写博客或者案例分析
- 创建示意图、图形资产或者嵌入式的截屏和视频内容

进一步的详细信息，可参见[贡献新内容](/zh-cn/docs/contribute/new-content/)。

## 成员（Members）  {#members}

成员是指那些对 `kubernetes/website` 提交很多拉取请求（PR）的人。
成员都要加入 [Kubernetes GitHub 组织](https://github.com/kubernetes)。

成员可以：

- 执行[任何人](#anyone)节区所列举操作
- 使用 `/lgtm` 评论添加 LGTM (looks good to me（我觉得可以）) 标签到某个 PR

  {{< note >}}
  使用 `/lgtm` 会触发自动化机制。如果你希望提供非约束性的批准意见，
  直接回复 "LGTM" 也是可以的。
  {{< /note >}}

- 利用 `/hold` 评论来阻止某个 PR 被合并
- 使用 `/assign` 评论为某个 PR 指定评审人
- 对 PR 提供非约束性的评审意见
- 使用自动化机制来对 Issue 进行判别和分类
- 为新功能特性撰写文档

### 成为一个成员 {#becoming-a-member}

在你成功地提交至少 5 个 PR 并满足
[相关条件](https://github.com/kubernetes/community/blob/master/community-membership.md#member)
之后：

1. 找到两个[评审人](#reviewers)或[批准人](#approvers)为你的成员身份提供
   [担保](/zh-cn/docs/contribute/advanced#sponsor-a-new-contributor)。

   通过 [Kubernetes Slack 上的 #sig-docs 频道](https://kubernetes.slack.com) 或者
   [SIG Docs 邮件列表](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)
   来寻找为你担保的人。

   {{< note >}}
   不要单独发送邮件给某个 SIG Docs 成员或在 Slack 中与其私聊。
   在提交申请之前，一定要先确定担保人。
   {{< /note >}}

2. 在 [`kubernetes/org`](https://github.com/kubernetes/org/) 仓库
   使用 **Organization Membership Request** Issue 模板登记一个 Issue。

3. 告知你的担保人你所创建的 Issue，你可以：

   - 在 Issue 中 `@<GitHub-username>` 提及他们的 GitHub 用户名
   - 通过 Slack 或 email 直接发送给他们 Issue 链接
 
   担保人会通过 `+1` 投票来批准你的请求。一旦你的担保人批准了该请求，
   某个 Kubernetes GitHub 管理员会将你添加为组织成员。恭喜！

   如果你的成员请求未被接受，你会收到一些反馈。
   当处理完反馈意见之后，可以再次发起申请。

4. 登录你的邮件账户，接受来自 Kubernetes GitHub 组织发出的成员邀请。

    {{< note >}}
    GitHub 会将邀请发送到你的账户中所设置的默认邮件地址。
    {{< /note >}}

## 评审人（Reviewers）  {#reviewers}

评审人负责评审悬决的 PR。
与成员所给的反馈不同，身为 PR 作者必须处理评审人的反馈。
评审人是 [@kubernetes/sig-docs-{language}-reviews](https://github.com/orgs/kubernetes/teams?query=sig-docs) GitHub 团队的成员。

评审人可以：

- 执行[任何人](#anyone)和[成员](#members)节区所列举的操作
- 评审 PR 并提供具约束性的反馈信息

    {{< note >}}
    要提供非约束性的反馈，可以在你的评语之前添加 "Optionally: " 这样的说法。
    {{< /note >}}

- 编辑代码中用户可见的字符串
- 改进代码注释

你可以是 SIG Docs 的评审人，也可以是某个主题领域的文档的评审人。

### 为 PR 指派评审人  {#assigning-reviewers-to-pull-requests}

自动化引擎会为每个 PR 自动指派评审人。
你可以通过为 PR 添加评论 `/assign [@_github_handle]` 来请求某个特定评审人来评审。

如果所指派的评审人未能及时评审，其他的评审人也可以参与进来。
你可以根据需要指派技术评审人。

### 使用 `/lgtm`   {#using-lgtm}

LGTM 代表的是 “Looks Good To Me （我觉得可以）”，用来标示某个 PR
在技术上是准确的，可以被合并。
所有 PR 都需要来自某评审人的 `/lgtm` 评论和来自某批准人的 `/approve`
评论。

来自评审人的 `/lgtm` 评论是具有约束性的，会触发自动化引擎添加 `lgtm` 标签。

### 成为评审人   {#becoming-a-reviewer}

当你满足[相关条件](https://github.com/kubernetes/community/blob/master/community-membership.md#reviewer)时，
你可以成为一个 SIG Docs 评审人。
来自其他 SIG 的评审人必须为 SIG Docs 单独申请评审人资格。

申请流程如下：

1. 发起 PR，将你的 GitHub 用户名添加到 `kubernetes/website` 仓库中
   [OWNERS_ALIASES](https://github.com/kubernetes/website/blob/main/OWNERS_ALIASES)
   文件的对应节区。

   {{< note >}}
   如果你不确定要添加到哪个位置，可以将自己添加到 `sig-docs-en-reviews`。
   {{< /note >}}

2. 将 PR 指派给一个或多个 SIG Docs 批准人（`sig-docs-{language}-owners`
   下列举的用户名）。

申请被批准之后，SIG Docs Leads 之一会将你添加到合适的 GitHub 团队。
一旦添加完成，[@k8s-ci-robot](https://github.com/kubernetes/test-infra/tree/master/prow#bots-home)
会在处理未来的 PR 时，将 PR 指派给你或者建议你来评审某 PR。

## 批准人（Approvers）   {#approvers}

批准人负责评审和批准 PR 以将其合并。
批准人是 [@kubernetes/sig-docs-{language}-owners](https://github.com/orgs/kubernetes/teams/?query=sig-docs) GitHub 团队的成员。

批准人可以执行以下操作：

- 执行列举在[任何人](#anyone)、[成员](#members)和[评审人](#reviewers)节区的操作
- 通过使用 `/approve` 评论来批准、合并 PR，发布贡献者所贡献的内容。
- 就样式指南给出改进建议
- 对文档测试给出改进建议
- 对 Kubernetes 网站或其他工具给出改进建议

如果某个 PR 已有 `/lgtm` 标签，或者批准人再回复一个 `/lgtm`，则这个 PR 会自动合并。
SIG Docs 批准人应该只在不需要额外的技术评审的情况下才可以标记 `/lgtm`。

### 批准 PR   {#approving-pull-requests}

只有批准人和 SIG Docs Leads 可以将 PR 合并到网站仓库。
这意味着以下责任：

- 批准人可以使用 `/approve` 命令将 PR 合并到仓库中。

    {{< warning >}}
    不小心的合并可能会破坏整个站点。在执行合并操作时，务必小心。
    {{< /warning >}}

- 确保所提议的变更满足[文档内容指南](/zh-cn/docs/contribute/style/content-guide/)要求。

    如果有问题或者疑惑，可以根据需要请他人帮助评审。

- 在 `/approve` PR 之前，须验证 Netlify 测试是否正常通过。

    <img src="/images/docs/contribute/netlify-pass.png" width="75%" alt="批准之前必须通过 Netlify 测试" />

- 在批准之前，请访问 Netlify 的页面预览来确保变更内容可正常显示。

- 参与 [PR 管理者轮值排班](https://github.com/kubernetes/website/wiki/PR-Wranglers)
  执行时长为一周的 PR 管理。SIG Docs 期望所有批准人都参与到此轮值工作中。
  更多细节可参见 [PR 管理者](/zh-cn/docs/contribute/participate/pr-wranglers/)。

### 成为批准人  {#becoming-an-approver}

当你满足[一定条件](https://github.com/kubernetes/community/blob/master/community-membership.md#approver)时，可以成为一个 SIG Docs 批准人。
来自其他 SIG 的批准人也必须在 SIG Docs 独立申请批准人资格。

申请流程如下：

1. 发起一个 PR，将自己添加到 `kubernetes/website` 仓库中
   [OWNERS_ALIASES](https://github.com/kubernetes/website/blob/main/OWNERS_ALIASES)
   文件的对应节区。

   {{< note >}}
   如果你不确定要添加到哪个位置，可以将自己添加到 `sig-docs-en-owners` 中。
   {{< /note >}}

2. 将 PR 指派给一个或多个 SIG Docs 批准人。

请求被批准之后，SIG Docs Leads 之一会将你添加到对应的 GitHub 团队。
一旦添加完成，[K8s-ci-robot](https://github.com/kubernetes/test-infra/tree/master/prow#bots-home)
会在处理未来的 PR 时，将 PR 指派给你或者建议你来评审某 PR。

## {{% heading "whatsnext" %}}

- 阅读 [PR 管理者](/zh-cn/docs/contribute/participate/pr-wranglers/)，了解所有批准人轮值的角色。

