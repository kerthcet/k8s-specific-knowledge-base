---
title: Kubernetes 安全和信息披露
aliases: [/zh-cn/security/]
content_type: concept
weight: 20
---


本页面介绍 Kubernetes 安全和信息披露相关的内容。


## 安全公告 {#security-announcements}

加入 [kubernetes-security-announce](https://groups.google.com/forum/#!forum/kubernetes-security-announce) 组，以获取关于安全性和主要 API 公告的电子邮件。

## 报告一个漏洞 {#report-a-vulnerability}

我们非常感谢向 Kubernetes 开源社区报告漏洞的安全研究人员和用户。
所有的报告都由社区志愿者进行彻底调查。

如需报告，请将你的漏洞提交给 [Kubernetes 漏洞赏金计划](https://hackerone.com/kubernetes)。
这样做可以使得社区能够在标准化的响应时间内对漏洞进行分类和处理。

你还可以通过电子邮件向私有 [security@kubernetes.io](mailto:security@kubernetes.io)
列表发送电子邮件，邮件中应该包含
[所有 Kubernetes 错误报告](https://github.com/kubernetes/kubernetes/blob/master/.github/ISSUE_TEMPLATE/bug-report.yaml)
所需的详细信息。

你可以使用[安全响应委员会成员](https://git.k8s.io/security/README.md#product-security-committee-psc)的
GPG 密钥加密你的发往邮件列表的邮件。揭示问题时不需要使用 GPG 来加密。

### 我应该在什么时候报告漏洞？ {#when-should-i-report-a-vulnerability}

- 你认为在 Kubernetes 中发现了一个潜在的安全漏洞
- 你不确定漏洞如何影响 Kubernetes
- 你认为你在 Kubernetes 依赖的另一个项目中发现了一个漏洞
  - 对于具有漏洞报告和披露流程的项目，请直接在该项目处报告

### 我什么时候不应该报告漏洞？ {#when-should-i-not-report-a-vulnerability}

- 你需要调整 Kubernetes 组件安全性的帮助
- 你需要应用与安全相关更新的帮助
- 你的问题与安全无关

## 安全漏洞响应 {#security-vulnerability-response}

每个报告在 3 个工作日内由安全响应委员会成员确认和分析，这将启动[安全发布过程](https://git.k8s.io/sig-release/security-release-process-documentation/security-release-process.md#disclosures)。

与安全响应委员会共享的任何漏洞信息都保留在 Kubernetes 项目中，除非有必要修复该问题，否则不会传播到其他项目。

随着安全问题从分类、识别修复、发布计划等方面的进展，我们将不断更新报告。

## 公开披露时间 {#public-disclosure-timing}

公开披露日期由 Kubernetes 安全响应委员会和 bug 提交者协商。
我们倾向于在能够为用户提供缓解措施之后尽快完全披露该 bug。

当 bug 或其修复还没有被完全理解，解决方案没有经过良好的测试，或者为了处理供应商协调问题时，延迟披露是合理的。

信息披露的时间范围从即时（尤其是已经公开的）到几周不等。
对于具有直接缓解措施的漏洞，我们希望报告日期到披露日期的间隔是 7 天。
在设置披露日期方面，Kubernetes 安全响应委员会拥有最终决定权。
