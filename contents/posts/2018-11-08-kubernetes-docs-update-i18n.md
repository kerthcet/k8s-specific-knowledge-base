---
layout: blog
title: 'Kubernetes 文档更新，国际版'
date: 2018-11-08
slug: kubernetes-docs-updates-international-edition
---

**作者**：Zach Corleissen （Linux 基金会）

作为文档特别兴趣小组（SIG Docs）的联合主席，我很高兴能与大家分享 Kubernetes 文档在本地化（l10n）方面所拥有的一个完全成熟的工作流。

## 丰富的缩写

L10n 是 _localization_ 的缩写。

I18n 是 _internationalization_ 的缩写。

I18n 定义了[做什么](https://www.w3.org/International/questions/qa-i18n) 能让 l10n 更容易。而 L10n 更全面，相比翻译（ _t9n_ ）具备更完善的流程。

## 为什么本地化很重要

SIG Docs 的目标是让 Kubernetes 更容易为尽可能多的人使用。

一年前，我们研究了是否有可能由一个独立翻译 Kubernetes 文档的中国团队来主持文档输出。经过多次交谈（包括 OpenStack l10n 的专家），[多次转变](https://kubernetes.io/blog/2018/05/05/hugo-migration/)，以及[重新致力于更轻松的本地化](https://github.com/kubernetes/website/pull/10485)，我们意识到，开源文档就像开源软件一样，是在可能的边缘不断进行实践。

整合工作流程、语言标签和团队级所有权可能看起来像是十分简单的改进，但是这些功能使 l10n 可以扩展到规模越来越大的 l10n 团队。随着 SIG Docs 不断改进，我们已经在单一工作流程中偿还了大量技术债务并简化了 l10n。这对未来和现在都很有益。

## 整合的工作流程

现在，本地化已整合到 [kubernetes/website](https://github.com/kubernetes/website) 存储库。我们已经配置了 Kubernetes CI/CD 系统，[Prow](https://github.com/kubernetes/test-infra/tree/master/prow) 来处理自动语言标签分配以及团队级 PR 审查和批准。

### 语言标签

Prow 根据文件路径自动添加语言标签。感谢 SIG Docs 贡献者 [June Yi](https://github.com/kubernetes/test-infra/pull/9835)，他让人们还可以在 pull request（PR）注释中手动分配语言标签。例如，当为 issue 或 PR 留下下述注释时，将为之分配标签 `language/ko`（Korean）。

```
/language ko
```


这些存储库标签允许审阅者按语言过滤 PR 和 issue。例如，您现在可以过滤 kubernetes/website 面板中[具有中文内容的 PR](https://github.com/kubernetes/website/pulls?utf8=%E2%9C%93&q=is%3Aopen+is%3Apr+label%3Alanguage%2Fzh)。

### 团队审核

L10n 团队现在可以审查和批准他们自己的 PR。例如，英语的审核和批准权限在位于用于显示英语内容的顶级子文件夹中的 [OWNERS 文件中指定](https://github.com/kubernetes/website/blob/main/content/en/OWNERS)。

将 `OWNERS` 文件添加到子目录可以让本地化团队审查和批准更改，而无需由可能并不擅长该门语言的审阅者进行批准。

## 下一步是什么

我们期待着[上海的 doc sprint](https://kccncchina2018english.sched.com/event/HVb2/contributor-summit-doc-sprint-additional-registration-required) 能作为中国 l10n 团队的资源。

我们很高兴继续支持正在取得良好进展的日本和韩国 l10n 队伍。

如果您有兴趣将 Kubernetes 本地化为您自己的语言或地区，请查看我们的[本地化 Kubernetes 文档指南](https://kubernetes.io/docs/contribute/localization/)，并联系 [SIG Docs 主席团](https://github.com/kubernetes/community/tree/master/sig-docs#leadership)获取支持。

### 加入SIG Docs

如果您对 Kubernetes 文档感兴趣，请参加 SIG Docs [每周会议](https://github.com/kubernetes/community/tree/master/sig-docs#meetings)，或在 [Kubernetes Slack 加入 #sig-docs](https://kubernetes.slack.com/messages/C1J0BPD2M/details/)。
