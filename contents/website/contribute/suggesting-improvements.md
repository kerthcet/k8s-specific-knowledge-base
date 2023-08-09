---
title: 提出内容改进建议
content_type: concept
weight: 10
card:
  name: contribute
  weight: 20
---


如果你发现 Kubernetes 文档中存在问题或者你有一个关于新内容的想法，
可以考虑提出一个问题（issue）。你只需要具有 [GitHub 账号](https://github.com/join)和 Web
浏览器就可以完成这件事。

在大多数情况下，Kubernetes 文档的新工作都是开始于 GitHub 上的某个问题。
Kubernetes 贡献者会审阅这些问题并根据需要对其分类、打标签。
接下来，你或者别的 Kubernetes 社区成员就可以发起一个带有变更的拉取请求，
以解决这一问题。


## 创建问题 {#opening-an-issue}

如果你希望就改进已有内容提出建议或者在文档中发现了错误，请创建一个问题（issue）。

1. 点击右侧边栏的 **提交文档问题** 按钮。浏览器会重定向到一个 GitHub 问题页面，
   其中包含了一些预先填充的内容。
1. 请描述遇到的问题或关于改进的建议。尽可能提供细节信息。
1. 点击 **Submit new issue**。

提交之后，偶尔查看一下你所提交的问题，或者开启 GitHub 通知。
评审人（reviewers）和其他社区成员可能在针对所提问题采取行动之前，问一些问题。

## 关于新内容的建议 {#suggesting-new-content}

如果你对新内容有想法，但是你不确定这些内容应该放在哪里，你仍可以提出问题。

- 在预期的节区中选择一个现有页面，点击 **提交文档问题**。
- 前往 [GitHub Issues 页面](https://github.com/kubernetes/website/issues/new/)，
  直接记录问题。


## 如何更好地记录问题 {#how-to-file-great-issues}

在记录问题时，请注意以下事项：

- 提供问题的清晰描述，描述具体缺失的内容、过期的内容、错误的内容或者需要改进的文字。
- 解释该问题对用户的特定影响。
- 将给定问题的范围限定在一个工作单位范围内。如果问题牵涉的领域较大，可以将其分解为多个小一点的问题。
  例如："Fix the security docs" 是一个过于宽泛的问题，而
  "Add details to the 'Restricting network access' topic"
  就是一个足够具体的、可操作的问题。
- 搜索现有问题的列表，查看是否已经有相关的或者类似的问题已被记录。
- 如果新问题与某其他问题或 PR 有关联，可以使用其完整 URL 或带 `#` 字符的 PR 编号来引用之。
  例如：`Introduced by #987654`。
- 遵从[行为准则](/zh-cn/community/code-of-conduct/)。尊重同行贡献者。
  例如，"The docs are terrible" 就是无用且无礼的反馈。

