---
title: PR 管理者
content_type: concept
weight: 20
---

SIG Docs 的[批准人（Approvers）](/zh-cn/docs/contribute/participate/roles-and-responsibilities/#approvers)们每周轮流负责
[管理仓库的 PR](https://github.com/kubernetes/website/wiki/PR-Wranglers)。

本节介绍 PR 管理者的职责。关于如何提供较好的评审意见，
可参阅[评审变更](/zh-cn/docs/contribute/review/)。


## 职责 {#duties}
在为期一周的轮值期内，PR 管理者要：

- 每天对新增的 Issues 判定和打标签。参见
  [对 Issues 进行判定和分类](/zh-cn/docs/contribute/review/for-approvers/#triage-and-categorize-issues)
  以了解 SIG Docs 如何使用元数据的详细信息。
- 检查[悬决的 PR](https://github.com/kubernetes/website/pulls) 的质量并确保它们符合
  [样式指南](/zh-cn/docs/contribute/style/style-guide/)和
  [内容指南](/zh-cn/docs/contribute/style/content-guide/)要求。

  - 首先查看最小的 PR（`size/XS`），然后逐渐扩展到最大的
    PR（`size/XXL`），尽可能多地评审 PR。
- 确保贡献者完成 [CLA](https://github.com/kubernetes/community/blob/master/CLA.md) 签署。
  - 使用[此脚本](https://github.com/zparnold/k8s-docs-pr-botherer)自动提醒尚未签署
    CLA 的贡献者签署 CLA。
- 针对提供提供反馈，请求其他 SIG 的成员进行技术审核。
  - 为 PR 所建议的内容更改提供就地反馈。
  - 如果你需要验证内容，请在 PR 上发表评论并要求贡献者提供更多细节。
  - 设置相关的 `sig/` 标签。
  - 如果需要，根据文件开头的 `reviewers:` 块来指派评审人。
  - 你也可以通过在 PR 上作出 `@kubernetes/<sig>-pr-reviews` 的评论以标记需要某个
    [SIG](https://github.com/kubernetes/community/blob/master/sig-list.md) 来评审。
- 使用 `/approve` 评论来批准可以合并的 PR，在 PR 就绪时将其合并。
  - PR 在被合并之前，应该有来自其他成员的 `/lgtm` 评论。
  - 可以考虑接受那些技术上准确，但文风上不满足
    [风格指南](/zh-cn/docs/contribute/style/style-guide/)要求的 PR。
    批准变更时，可以登记一个新的 Issue 来解决文档风格问题。
    你通常可以将这些风格修复问题标记为 `good first issue`。
  - 将风格修复事项标记为 `good first issue` 可以很好地确保向新加入的贡献者分派一些比较简单的任务，
    这有助于接纳新的贡献者。

### 对管理者有用的 GitHub 查询

执行管理操作时，以下查询很有用。完成以下这些查询后，剩余的要审阅的 PR 列表通常很小。
这些查询都不包含本地化的 PR，并仅包含主分支上的 PR（除了最后一个查询）。

- [未签署 CLA，不可合并的 PR](https://github.com/kubernetes/website/pulls?q=is%3Aopen+is%3Apr+label%3A%22cncf-cla%3A+no%22+-label%3A%22do-not-merge%2Fwork-in-progress%22+-label%3A%22do-not-merge%2Fhold%22+label%3Alanguage%2Fen)：
  提醒贡献者签署 CLA。如果机器人和审阅者都已经提醒他们，请关闭 PR，并提醒他们在签署 CLA 后可以重新提交。

  **在作者没有签署 CLA 之前，不要审阅他们的 PR！**

- [需要 LGTM](https://github.com/kubernetes/website/pulls?q=is%3Aopen+is%3Apr+-label%3A%22cncf-cla%3A+no%22+-label%3Ado-not-merge%2Fwork-in-progress+-label%3Ado-not-merge%2Fhold+label%3Alanguage%2Fen+-label%3Algtm)：
  列举需要来自成员的 LGTM 评论的 PR。
  如果需要技术审查，请告知机器人所建议的审阅者。
  如果 PR 继续改进，就地提供更改建议或反馈。

- [已有 LGTM标签，需要 Docs 团队批准](https://github.com/kubernetes/website/pulls?q=is%3Aopen+is%3Apr+-label%3Ado-not-merge%2Fwork-in-progress+-label%3Ado-not-merge%2Fhold+label%3Alanguage%2Fen+label%3Algtm+)：
  列举需要 `/approve` 评论来合并的 PR。

- [快速批阅](https://github.com/kubernetes/website/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+base%3Amain+-label%3A%22do-not-merge%2Fwork-in-progress%22+-label%3A%22do-not-merge%2Fhold%22+label%3A%22cncf-cla%3A+yes%22+label%3A%22size%2FXS%22+label%3A%22language%2Fen%22)：
  列举针对主分支的、没有明确合并障碍的 PR。
  在浏览 PR 时，可以将 "XS" 尺寸标签更改为 "S"、"M"、"L"、"XL"、"XXL"。

- [非主分支的 PR](https://github.com/kubernetes/website/pulls?q=is%3Aopen+is%3Apr+label%3Alanguage%2Fen+-base%3Amain): 
  如果 PR 针对 `dev-` 分支，则表示它适用于即将发布的版本。
  请添加带有 `/assign @<负责人的 github 账号>`，将其指派给 
  [发行版本负责人](https://github.com/kubernetes/sig-release/tree/master/release-team#kubernetes-release-team-roles)。
  如果 PR 是针对旧分支，请帮助 PR 作者确定是否所针对的是最合适的分支。

### 对管理者有用的 Prow 命令  {#helpful-prow-commands-for-wranglers}

```
# 添加 English 标签
/language en

# 如果 PR 包含多个提交（commits），添加 squash 标签
/label tide/merge-method-squash

# 使用 Prow 来为 PR 重设标题（例如一个正在处理 [WIP] 的 PR 或为 PR 提供更好的细节信息）
/retitle [WIP] <TITLE>
```

### 何时关闭 PR     {#when-to-close-pull-requests}

审查和批准是缩短和更新我们的 PR 队列的一种方式；另一种方式是关闭 PR。

当以下条件满足时，可以关闭 PR：

- 作者两周内未签署 CLA。
  PR 作者可以在签署 CLA 后重新打开 PR，因此这是确保未签署 CLA 的 PR 不会被合并的一种风险较低的方法。

- 作者在两周或更长时间内未回复评论或反馈。

不要害怕关闭 PR。贡献者可以轻松地重新打开并继续工作。
通常，关闭通知会激励作者继续完成其贡献。

要关闭 PR，请在 PR 上输入 `/close` 评论。

{{< note >}}
一个名为 [`k8s-ci-robot`](https://github.com/k8s-ci-robot) 的自动服务会在 Issue 停滞 90
天后自动将其标记为过期；然后再等 30 天，如果仍然无人过问，则将其关闭。
PR 管理者应该在 issues 处于无人过问状态 14-30 天后关闭它们。
{{< /note >}}

## PR 管理者影子计划

2021 下半年，SIG Docs 推出了 PR 管理者影子计划（PR Wrangler Shadow Program）。
该计划旨在帮助新的贡献者们了解 PR 管理流程。

### 成为一名影子

- 如果你有兴趣成为一名 PR 管理者的影子，请访问 [PR 管理者维基页面](https://github.com/kubernetes/website/wiki/PR-Wranglers)查看今年的 
  PR 管理轮值表，然后注册报名。

- Kubernetes 组织成员可以编辑 [PR 管理者维基页面](https://github.com/kubernetes/website/wiki/PR-Wranglers)，
  注册成为一名现有 PR 管理者一周内的影子。

- 其他人可以通过 [#sig-docs Slack 频道](https://kubernetes.slack.com/messages/sig-docs)申请成为指定 
  PR 管理者某一周的影子。可以随时咨询 (`@bradtopol`) 或某一位
  [SIG Docs 联席主席/主管](https://github.com/kubernetes/community/tree/master/sig-docs#leadership)。

- 注册成为一名 PR 管理者的影子时，
  请你在 [Kubernetes Slack](https://slack.k8s.io) 向这名 PR 管理者做一次自我介绍。
