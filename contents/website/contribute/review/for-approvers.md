---
title: 评阅人和批准人文档
linktitle: 评阅人和批准人
slug: for-approvers
content_type: concept
weight: 20
---

SIG Docs
[评阅人（Reviewers）](/zh-cn/docs/contribute/participate/#reviewers)
和[批准人（Approvers）](/zh-cn/docs/contribute/participate/#approvers)
在对变更进行评审时需要做一些额外的事情。

每周都有一个特定的文档批准人自愿负责对 PR 进行分类和评阅。
此角色称作该周的“PR 管理者（PR Wrangler）”。
相关信息可参考 [PR Wrangler 排班表](https://github.com/kubernetes/website/wiki/PR-Wranglers)。
要成为 PR Wangler，需要参加每周的 SIG Docs 例会，并自愿报名。
即使当前这周排班没有轮到你，你仍可以评阅那些尚未被积极评阅的 PRs。

除了上述的轮值安排，后台机器人也会为基于所影响的文件来为 PR
指派评阅人和批准人。

## 评阅 PR

Kubernetes 文档遵循 [Kubernetes 代码评阅流程](https://github.com/kubernetes/community/blob/master/contributors/guide/owners.md#the-code-review-process)。

[评阅 PR](/zh-cn/docs/contribute/review/reviewing-prs/) 文档中所描述的所有规程都适用，
不过评阅人和批准人还要做以下工作：

- 根据需要使用 Prow 命令 `/assign` 指派特定的评阅人。如果某个 PR
  需要来自代码贡献者的技术审核时，这一点非常重要。

  {{< note >}}
  你可以查看 Markdown 文件的文件头，其中的 `reviewers` 字段给出了哪些人可以为文档提供技术审核。
  {{< /note >}}

- 确保 PR 遵从[内容指南](/zh-cn/docs/contribute/style/content-guide/)和[样式指南](/zh-cn/docs/contribute/style/style-guide/)；
  如果 PR 没有达到要求，指引作者阅读指南中的相关部分。
- 适当的时候使用 GitHub **Request Changes** 选项，建议 PR 作者实施所建议的修改。
- 当你所提供的建议被采纳后，在 GitHub 中使用 `/approve` 或 `/lgtm` Prow 命令，改变评审状态。

## 提交到他人的 PR

为 PR 留下评语是很有用的，不过有时候你需要向他人的 PR 提交内容。

除非他人明确请求你的帮助或者你希望重启一个被放弃很久的 PR，不要“接手”他人的工作。
尽管短期看来这样做可以提高效率，但是也剥夺了他人提交贡献的机会。

你所要遵循的流程取决于你需要编辑已经在 PR 范畴的文件，还是 PR 尚未触碰的文件。

如果处于下列情况之一，你不可以向别人的 PR 提交内容：

- 如果 PR 作者是直接将自己的分支提交到
  [https://github.com/kubernetes/website/](https://github.com/kubernetes/website/)
  仓库。只有具有推送权限的评阅人才可以向他人的 PR 提交内容。

  {{< note >}}
  我们应鼓励作者下次将分支推送到自己的克隆副本之后再发起 PR。
  {{< /note >}}

- PR 作者明确地禁止批准人编辑他/她的 PR。

## 评阅用的 Prow 命令

[Prow](https://github.com/kubernetes/test-infra/blob/master/prow/README.md)
是基于 Kubernetes 的 CI/CD 系统，基于拉取请求（PR）的触发运行不同任务。
Prow 使得我们可以使用会话机器人一样的命令跨整个 Kubernetes 组织处理 GitHub
动作，例如[添加和删除标签](#adding-and-removing-issue-labels)、关闭 Issues
以及指派批准人等等。你可以使用 `/<命令名称>` 的形式以 GitHub 评论的方式输入
Prow 命令。

评阅人和批准人最常用的 Prow 命令有：

{{< table caption="评阅用 Prow 命令" >}}
Prow 命令 | 角色限制 | 描述
:------------|:------------------|:-----------
`/lgtm` | 组织成员 | 用来表明你已经完成 PR 的评阅并对其所作变更表示满意
`/approve` | 批准人 | 批准某 PR 可以合并
`/assign` |任何人 | 指派某人来评阅或批准某 PR
`/close` | 组织成员 | 关闭 Issue 或 PR
`/hold` | 任何人 | 添加 `do-not-merge/hold` 标签，用来表明 PR 不应被自动合并
`/hold cancel` | 任何人 | 去掉 `do-not-merge/hold` 标签
{{< /table >}}

要查看可以在 PR 中使用的命令，请参阅
[Prow 命令指南](https://prow.k8s.io/command-help?repo=kubernetes%2Fwebsite)。

## 对 Issue 进行诊断和分类

一般而言，SIG Docs 遵从 [Kubernetes issue 判定](https://github.com/kubernetes/community/blob/master/contributors/guide/issue-triage.md) 流程并使用相同的标签。

此 GitHub Issue
[过滤器](https://github.com/kubernetes/website/issues?q=is%3Aissue+is%3Aopen+-label%3Apriority%2Fbacklog+-label%3Apriority%2Fimportant-longterm+-label%3Apriority%2Fimportant-soon+-label%3Atriage%2Fneeds-information+-label%3Atriage%2Fsupport+sort%3Acreated-asc)
可以用来查找需要评判的 Issues。


### 评判 Issue {#triaging-an-issue}

1. 验证 Issue 的合法性

  - 确保 Issue 是关于网站文档的。某些 Issue 可以通过回答问题或者为报告者提供
    资源链接来快速关闭。
    参考[请求支持或代码缺陷报告](#support-requests-or-code-bug-reports)
    节以了解详细信息。
  - 评估该 Issue 是否有价值。
  - 如果 Issue 缺少足够的细节以至于无法采取行动，或者报告者没有通过模版提供
    足够信息，可以添加 `triage/needs-information` 标签。
  - 如果 Issue 同时标注了 `lifecycle/stale` 和 `triage/needs-information`
    标签，可以直接关闭。

2. 添加优先级标签（
  [Issue 判定指南](https://github.com/kubernetes/community/blob/master/contributors/guide/issue-triage.md#define-priority)中有优先级标签的详细定义)

  {{< table caption="Issue 标签" >}}
  标签         | 描述
  :------------|:------------------
  `priority/critical-urgent` | 应马上处理
  `priority/important-soon` | 应在 3 个月内处理
  `priority/important-longterm` | 应在 6 个月内处理
  `priority/backlog` | 可无限期地推迟，可在人手充足时处理
  `priority/awaiting-more-evidence` | 占位符，标示 Issue 可能是一个不错的 Issue，避免该 Issue 被忽略或遗忘
  `help` or `good first issue` | 适合对 Kubernetes 或 SIG Docs 经验较少的贡献者来处理。更多信息可参考[需要帮助和入门候选 Issue 标签](https://kubernetes.dev/docs/guide/help-wanted/)。
  {{< /table >}}

   基于你自己的判断，你可以选择某 Issue 来处理，为之发起 PR
   （尤其是那些可以很快处理或与你已经在做的工作相关的 Issue）。

如果你对 Issue 评判有任何问题，可以在 `#sig-docs` Slack 频道或者
[kubernetes-sig-docs 邮件列表](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)
中提问。

## 添加和删除 Issue 标签 {#adding-and-removing-issue-labels}

要添加标签，可以用以下形式对 PR 进行评论：

- `/<要添加的标签>` （例如, `/good-first-issue`）
- `/<标签类别> <要添加的标签>` （例如，`/triage needs-information` 或 `/language ja`）

要移除某个标签，可以用以下形式对 PR 进行评论：

- `/remove-<要移除的标签>` （例如，`/remove-help`）
- `/remove-<标签类别> <要移除的标签>` （例如，`/remove-triage needs-information`）

在以上两种情况下，标签都必须合法存在。如果你尝试添加一个尚不存在的标签，
对应的命令会被悄悄忽略。

关于所有标签的完整列表，可以参考
[Website 仓库的标签节](https://github.com/kubernetes/website/labels)。
实际上，SIG Docs 并没有使用全部标签。

### Issue 生命周期标签

Issues 通常都可以快速创建并关闭。
不过也有些时候，某个 Issue 被创建之后会长期处于非活跃状态。
也有一些时候，即使超过 90 天，某个 Issue 仍应保持打开状态。

{{< table caption="Issue 生命周期标签" >}}
标签         | 描述
:------------|:------------------
`lifecycle/stale` | 过去 90 天内某 Issue 无人问津，会被自动标记为停滞状态。如果 Issue 没有被 `/remove-lifecycle stale` 命令重置生命期，就会被自动关闭。
`lifecycle/frozen` | 对应的 Issue 即使超过 90 天仍无人处理也不会进入停滞状态。用户手动添加此标签给一些需要保持打开状态超过 90 天的 Issue，例如那些带有 `priority/important-longterm` 标签的 Issue。
{{< /table >}}

## 处理特殊的 Issue 类型 {#handling-special-issue-types}

SIG Docs 常常会遇到以下类型的 Issue，因此对其处理方式描述如下。

### 重复的 Issue {#duplicate-issues}

如果针对同一个问题有不止一个打开的 Issue，可以将其合并为一个 Issue。
你需要决定保留哪个 Issue 为打开状态（或者重新登记一个新的 Issue），
然后将所有相关的信息复制过去并提供对关联 Issues 的链接。
最后，将所有其他描述同一问题的 Issue 标记为 `triage/duplicate` 并关闭之。
保持只有一个 Issue 待处理有助于减少困惑，避免在同一问题上发生重复劳动。

### 失效链接 Issues {#dead-link-issues}

如果失效链接是关于 API 或者 `kubectl` 文档的，可以将其标记为
`/priority critical-urgent`，直到问题原因被弄清楚为止。
对于其他的链接失效问题，可以标记 `/priority important-longterm`，
因为这些问题都需要手动处理。

### 博客问题  {#blog-issues}

我们预期 [Kubernetes 博客](/zh-cn/blog/)条目随着时间推移都会过期。
因此，我们只维护一年内的博客条目。
如果某个 Issue 是与某个超过一年的博客条目有关的，可以直接关闭
Issue，不必修复。

### 请求支持或代码缺陷报告  {#support-requests-or-code-bug-reports}

某些文档 Issues 实际上是关于底层代码的 Issue 或者在某方面请求协助的问题，
例如某个教程无法正常工作。
对于与文档无关的 Issues，关闭它并打上标签 `kind/support`，可以通过评论
告知请求者其他支持渠道（Slack、Stack Overflow）。
如果有相关的其他仓库，可以告诉请求者应该在哪个仓库登记与功能特性相关的 Issues
（通常会是 `kubernetes/kubernetes`）。

下面是对支持请求的回复示例：

```none
This issue sounds more like a request for support and less
like an issue specifically for docs. I encourage you to bring
your question to the `#kubernetes-users` channel in
[Kubernetes slack](https://slack.k8s.io/). You can also search
resources like
[Stack Overflow](https://stackoverflow.com/questions/tagged/kubernetes)
for answers to similar questions.

You can also open issues for Kubernetes functionality in
https://github.com/kubernetes/kubernetes.

If this is a documentation issue, please re-open this issue.
```

对代码缺陷 Issue 的回复示例：

```none
This sounds more like an issue with the code than an issue with
the documentation. Please open an issue at
https://github.com/kubernetes/kubernetes/issues.

If this is a documentation issue, please re-open this issue.
```

### 压缩（Squashing）提交

作为一名 Approver，当你评审 PR 时，可能会遇到以下几种情况：

- 建议贡献者压缩他们的提交。
- 协助贡献者压缩提交。
- 建议贡献者先不要压缩提交。
- 阻止压缩提交。

**建议贡献者压缩提交**：新贡献者可能不知道要压缩 PR 中的提交。
如果是这种情况，Approver 要给出压缩提交的建议，并贴附有用的链接，
并在贡献者需要帮助时伸出援手。这里有一些有用的链接：

- 协助文档贡献者[提 PR 和压缩提交](/zh-cn/docs/contribute/new-content/open-a-pr#squashing-commits)。
- 面向开发者包括插图在内的 [GitHub 工作流程](https://www.k8s.dev/docs/guide/github-workflow/)。

**协助贡献者压缩提交**：如果贡献者压缩提交遇到难题或合并 PR 的时间紧迫，
你可以协助贡献者执行压缩提交的操作。

- kubernetes/website
  仓库[被配置为允许压缩提交后合并 PR](https://docs.github.com/zh/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests)。
  你只需选择 **Squash commits** 按钮。
- 在 PR 中，如果贡献者允许 Maintainer 们管理 PR，你就可以为他们压缩提交并将其 fork 更新为最新结果。
  在你执行压缩提交之后，请建议贡献者将压缩后的提交拉到他们本地的克隆副本。
- 你可以使用标签让 GitHub 压缩提交，这样 Tide / GitHub 就会对提交执行压缩；
  你还可以在合并 PR 时点选 **Squash commits** 按钮。

**建议贡献者避免压缩提交**

- 如果一个提交做了一些破坏性或不明智的修改，那最后一个提交可用于回滚错误，这种情况不要压缩提交。
  即使通过 GitHub 上 PR 中的 "Files changed" 页签以及 Netlify 预览看起来都正常，
  合并这种 PR 可能会在其他 fork 中造成 rebase 或合并冲突。
  你看到这种情况要进行合理的干预，避免对其他贡献者造成麻烦。

**千万不要压缩提交**

- 如果你为新版本发起了一次本地化批量作业或为新版发布许多文档，那你要合并到的分支将与用户 fork 的分支不同，
  这种情况**千万不要压缩提交**。之所以不压缩提交，是因为你必须保持这些文件的提交历史记录。
