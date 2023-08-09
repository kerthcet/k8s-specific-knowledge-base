---
title: 文档内容指南
linktitle: 内容指南
content_type: concept
weight: 10
---

本页包含 Kubernetes 文档的一些指南。

如果你不清楚哪些事情是可以做的，请加入到
[Kubernetes Slack](https://slack.k8s.io/) 的 `#sig-docs` 频道提问！
你可以在 https://slack.k8s.io 注册到 Kubernetes Slack。

关于为 Kubernetes 文档创建新内容的更多信息，
可参考[样式指南](/zh-cn/docs/contribute/style/style-guide)。


## 概述  {#overview}

Kubernetes 网站（包括其文档）源代码位于
[kubernetes/website](https://github.com/kubernetes/website) 仓库中。

在 `kubernetes/website/content/<语言代码>/docs` 目录下, 绝大多数 Kubernetes
文档都是特定于 [Kubernetes 项目](https://github.com/kubernetes/kubernetes)的。

## 可以发布的内容  {#what-s-allowed}

只有当以下条件满足时，Kubernetes 文档才允许第三方项目的内容：

- 内容所描述的软件在 Kubernetes 项目内
- 内容所描述的软件不在 Kubernetes 项目内，却是让 Kubernetes 正常工作所必需的
- 内容是被 kubernetes.io 域名收编的，或者是其他位置的标准典型内容

### 第三方内容    {#third-party-content}

Kubernetes 文档包含 Kubernetes 项目下的多个项目的应用示例。
这里的 Kubernetes 项目指的是 [Kubernetes](https://github.com/kubernetes) 和
[Kubernetes SIGs](https://github.com/kubernetes-sigs) GitHub 组织下的那些项目。

链接到 Kubernetes 项目中活跃的内容是一直允许的。

Kubernetes 需要某些第三方内容才能正常工作。例如容器运行时（containerd、CRI-O、Docker）、
[联网策略](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)（CNI 插件）、
[Ingress 控制器](/zh-cn/docs/concepts/services-networking/ingress-controllers/)
以及[日志](/zh-cn/docs/concepts/cluster-administration/logging/)等。

只有对应的第三方开源软件（OSS）是运行 Kubernetes 所必需的，
才可以在文档中包含指向这些 Kubernetes 项目之外的软件的链接。

### 双重来源的内容  {#dual-sourced-content}

只要有可能，Kubernetes 文档就应该指向标准典型的信息源而不是直接托管双重来源的内容。

双重来源的内容需要双倍（甚至更多）的投入才能维护，而且通常很快就会变得停滞不前。

{{< note >}}
如果你是一个 Kubernetes 项目的维护者，需要帮忙托管你自己的文档，
请在 Kubernetes 的 [#sig-docs 频道](https://kubernetes.slack.com/messages/C1J0BPD2M/)提出请求。
{{< /note >}}

### 更多信息  {#more-information}

如果你对允许出现的内容有疑问，请加入到 [Kubernetes Slack](https://slack.k8s.io/)
的 `#sig-docs` 频道提问！

## {{% heading "whatsnext" %}}

* 阅读[样式指南](/zh-cn/docs/contribute/style/style-guide)。
