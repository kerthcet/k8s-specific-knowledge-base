---
layout: blog
title: "弃用 PodSecurityPolicy：过去、现在、未来"
date: 2021-04-06
slug: podsecuritypolicy-deprecation-past-present-and-future
---

作者：Tabitha Sable（Kubernetes SIG Security）

{{% pageinfo color="primary" %}}
**更新：随着 Kubernetes v1.25 的发布，PodSecurityPolicy 已被删除。**

**你可以在 [Kubernetes 1.25 发布说明](/zh-cn/blog/2022/08/23/kubernetes-v1-25-release/#pod-security-changes)
中阅读有关删除 PodSecurityPolicy 的更多信息。**

{{% /pageinfo %}}

PSP 日后会被移除，但目前不会改变任何其他内容。在移除之前，PSP 将继续在后续多个版本中完全正常运行。
与此同时，我们正在开发 PSP 的替代品，希望可以更轻松、更可持续地覆盖关键用例。

什么是 PSP？为什么需要 PSP？为什么要弃用，未来又将如何发展？
这对你有什么影响？当我们准备告别 PSP，这些关键问题浮现在脑海中，
所以让我们一起来讨论吧。本文首先概述 Kubernetes 如何移除一些特性。

## Kubernetes 中的弃用是什么意思？

每当 Kubernetes 决定弃用某项特性时，我们会遵循[弃用策略](/zh-cn/docs/reference/using-api/deprecation-policy/)。
首先将该特性标记为已弃用，然后经过足够长的时间后，最终将其移除。

Kubernetes 1.21 启动了 PodSecurityPolicy 的弃用流程。与弃用任何其他功能一样，
PodSecurityPolicy 将继续在后续几个版本中完全正常运行。目前的计划是在 1.25 版本中将其移除。

在彻底移除之前，PSP 仍然是 PSP。至少在未来一年时间内，最新的 Kubernetes
版本仍将继续支持 PSP。大约两年之后，PSP 才会在所有受支持的 Kubernetes 版本中彻底消失。

## 什么是 PodSecurityPolicy？

[PodSecurityPolicy](/zh-cn/docs/concepts/security/pod-security-policy/)
是一个内置的[准入控制器](/blog/2019/03/21/a-guide-to-kubernetes-admission-controllers/)，
允许集群管理员控制 Pod 规约中涉及安全的敏感内容。

首先，在集群中创建一个或多个 PodSecurityPolicy 资源来定义 Pod 必须满足的要求。
然后，创建 RBAC 规则来决定为特定的 Pod 应用哪个 PodSecurityPolicy。
如果 Pod 满足其 PSP 的要求，则照常被允许进入集群。
在某些情况下，PSP 还可以修改 Pod 字段，有效地为这些字段创建新的默认值。
如果 Pod 不符合 PSP 要求，则被拒绝进入集群，并且无法运行。

关于 PodSecurityPolicy，还需要了解：它与
[PodSecurityContext](/zh-cn/docs/reference/kubernetes-api/workload-resources/pod-v1/#security-context) 不同。

作为 Pod 规约的一部分，PodSecurityContext（及其每个容器对应的 `SecurityContext`）
是一组字段的集合，这些字段为 Pod 指定了与安全相关的许多设置。
安全上下文指示 kubelet 和容器运行时究竟应该如何运行 Pod。
相反，PodSecurityPolicy 仅约束可能在安全上下文中设置的值（或设置默认值）。

弃用 PSP 不会以任何方式影响 PodSecurityContext。

## 以前为什么需要 PodSecurityPolicy？

在 Kubernetes 中，我们定义了 Deployment、StatefulSet 和 Service 等资源。
这些资源代表软件应用程序的构建块。Kubernetes 集群中的各种控制器根据这些资源做出反应，
创建更多的 Kubernetes 资源或配置一些软件或硬件来实现我们的目标。

在大多数 Kubernetes 集群中，由 RBAC（基于角色的访问控制）[规则](/zh-cn/docs/reference/access-authn-authz/rbac/#role-and-clusterrole)
控制对这些资源的访问。 `list`、`get`、`create`、`edit` 和 `delete` 是 RBAC 关心的 API 操作类型，
但 **RBAC 不考虑其所控制的资源中加入了哪些设置**。例如，
Pod 几乎可以是任何东西，例如简单的网络服务器，或者是特权命令提示（提供对底层服务器节点和所有数据的完全访问权限）。
这对 RBAC 来说都是一样的：Pod 就是 Pod 而已。

要控制集群中定义的资源允许哪些类型的设置，除了 RBAC 之外，还需要准入控制。
从 Kubernetes 1.3 开始，内置 PodSecurityPolicy 一直被作为 Pod 安全相关字段的准入控制机制。
使用 PodSecurityPolicy，可以防止“创建 Pod”这个能力自动变成“每个集群节点上的 root 用户”，
并且无需部署额外的外部准入控制器。

## 现在为什么 PodSecurityPolicy 要消失？

自从首次引入 PodSecurityPolicy 以来，我们已经意识到 PSP 存在一些严重的可用性问题，
只有做出断裂式的改变才能解决。

实践证明，PSP 应用于 Pod 的方式让几乎所有尝试使用它们的人都感到困惑。
很容易意外授予比预期更广泛的权限，并且难以查看某种特定情况下应用了哪些 PSP。
“更改 Pod 默认值”功能很方便，但仅支持某些 Pod 设置，而且无法明确知道它们何时会或不会应用于的 Pod。
如果没有“试运行”或审计模式，将 PSP 安全地改造并应用到现有集群是不切实际的，并且永远都不可能默认启用 PSP。

有关这些问题和其他 PSP 困难的更多信息，请查看
KubeCon NA 2019 的 SIG Auth 维护者频道会议记录：{{< youtube "SFtHRmPuhEw?start=953" youtube-quote-sm >}}

如今，你不再局限于部署 PSP 或编写自己的自定义准入控制器。
有几个外部准入控制器可用，它们结合了从 PSP 中吸取的经验教训以提供更好的用户体验。
[K-Rail](https://github.com/cruise-automation/k-rail)、
[Kyverno](https://github.com/kyverno/kyverno/)、
[OPA/Gatekeeper](https://github.com/open-policy-agent/gatekeeper/) 都家喻户晓，各有粉丝。

尽管现在还有其他不错的选择，但我们认为，提供一个内置的准入控制器供用户选择，仍然是有价值的事情。
考虑到这一点，以及受 PSP 经验的启发，我们转向下一步。

## 下一步是什么？

Kubernetes SIG Security、SIG Auth 和其他社区成员几个月来一直在倾力合作，确保接下来的方案能令人惊叹。
我们拟定了 Kubernetes 增强提案（[KEP 2579](https://github.com/kubernetes/enhancements/issues/2579)）
以及一个新功能的原型，目前称之为“PSP 替代策略”。
我们的目标是在 Kubernetes 1.22 中发布 Alpha 版本。

PSP 替代策略始于，我们认识到已经有一个强大的外部准入控制器生态系统可用，
所以，PSP 的替代品不需要满足所有人的所有需求。与外部 Webhook 相比，
部署和采用的简单性是内置准入控制器的关键优势。我们专注于如何最好地利用这一优势。

PSP 替代策略旨在尽可能简单，同时提供足够的灵活性以支撑大规模生产场景。
它具有柔性上线能力，以便于将其改装到现有集群，并且新的策略是可配置的，可以设置为默认启用。
PSP 替代策略可以被部分或全部禁用，以便在高级使用场景中与外部准入控制器共存。

## 这对你意味着什么？

这一切对你意味着什么取决于你当前的 PSP 情况。如果已经在使用 PSP，那么你有足够的时间来计划下一步行动。
请查看 PSP 替代策略 KEP 并考虑它是否适合你的使用场景。

如果你已经在通过众多 PSP 和复杂的绑定规则深度利用 PSP 的灵活性，你可能会发现 PSP 替代策略的简单性有太多限制。
此时，建议你在接下来的一年中评估一下生态系统中的其他准入控制器选择。有些资源可以让这种过渡更容易，
比如 [Gatekeeper Policy Library](https://github.com/open-policy-agent/gatekeeper-library)。

如果只是使用 PSP 的基础功能，只用几个策略并直接绑定到每个命名空间中的服务帐户，
你可能会发现 PSP 替代策略非常适合你的需求。
对比 Kubernetes [Pod 安全标准](/zh-cn/docs/concepts/security/pod-security-standards/) 评估你的 PSP，
了解可以在哪些情形下使用限制策略、基线策略和特权策略。
欢迎关注或为 KEP 和后续发展做出贡献，并在可用时试用 PSP 替代策略的 Alpha 版本。

如果刚刚开始 PSP 之旅，你可以通过保持简单来节省时间和精力。
你可以使用 Pod 安全标准的 PSP 来获得和目前 PSP 替代策略相似的功能。
如果你将基线策略或限制策略绑定到 `system:serviceaccounts` 组来设置集群默认值，
然后[使用 ServiceAccount 绑定](/zh-cn/docs/concepts/policy/pod-security-policy/#run-another-pod)
在某些命名空间下根据需要制定更宽松的策略，就可以避免许多 PSP 陷阱并轻松迁移到 PSP 替代策略。
如果你的需求比这复杂得多，那么建议将精力花在采用比上面提到的功能更全的某个外部准入控制器。

我们致力于使 Kubernetes 成为我们可以做到的最好的容器编排工具，
有时这意味着我们需要删除长期存在的功能，以便为更好的特性腾出空间。
发生这种情况时，Kubernetes 弃用策略可确保你有足够的时间来计划下一步行动。
对于 PodSecurityPolicy，有几个选项可以满足一系列需求和用例。

**致谢：** 研发优秀的软件需要优秀的团队。感谢为 PSP 替代工作做出贡献的所有人，
尤其是（按字母顺序）Tim Allclair、Ian Coldwater 和 Jordan Liggitt。
和你们共事非常愉快。
