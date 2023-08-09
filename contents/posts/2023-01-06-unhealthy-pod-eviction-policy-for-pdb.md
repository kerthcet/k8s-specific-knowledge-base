---
layout: blog
title: "Kubernetes 1.26：PodDisruptionBudget 守护的不健康 Pod 所用的驱逐策略"
date: 2023-01-06
slug: "unhealthy-pod-eviction-policy-for-pdbs"
---

**作者：** Filip Křepinský (Red Hat), Morten Torkildsen (Google), Ravi Gudimetla (Apple)

**译者：** Michael Yao (DaoCloud)

确保对应用的干扰不影响其可用性不是一个简单的任务。
上个月发布的 Kubernetes v1.26 允许针对
[PodDisruptionBudget](/zh-cn/docs/concepts/workloads/pods/disruptions/#pod-disruption-budgets) (PDB)
指定**不健康 Pod 驱逐策略**，这有助于在节点执行管理操作期间保持可用性。

## 这解决什么问题？  {#what-problem-does-this-solve}

API 发起的 Pod 驱逐尊重 PodDisruptionBudget (PDB) 约束。这意味着因驱逐 Pod
而请求的[自愿干扰](/zh-cn/docs/concepts/scheduling-eviction/#pod-disruption)不应干扰守护的应用且
PDB 的 `.status.currentHealthy` 不应低于 `.status.desiredHealthy`。
如果正在运行的 Pod 状态为 [Unhealthy](/zh-cn/docs/tasks/run-application/configure-pdb/#healthiness-of-a-pod)，
则该 Pod 不计入 PDB 状态，只有在应用不受干扰时才可以驱逐这些 Pod。
这有助于尽可能确保受干扰或还未启动的应用的可用性，不会因驱逐造成额外的停机时间。

不幸的是，对于想要腾空节点但又不进行任何手动干预的集群管理员而言，这种机制是有问题的。
若一些应用因 Pod 处于 `CrashLoopBackOff` 状态（由于漏洞或配置错误）或 Pod 无法进入就绪状态而行为异常，
会使这项任务变得更加困难。当某应用的所有 Pod 均不健康时，所有驱逐请求都会因违反 PDB 而失败。
在这种情况下，腾空节点不会有任何作用。

另一方面，有些用户依赖于现有行为，以便：

- 防止因删除守护基础资源或存储的 Pod 而造成数据丢失
- 让应用达到最佳可用性

Kubernetes 1.26 为 PodDisruptionBudget API 引入了新的实验性字段：
`.spec.unhealthyPodEvictionPolicy`。启用此字段后，将允许你支持上述两种需求。

## 工作原理   {#how-does-it-work}

API 发起的驱逐是触发 Pod 优雅终止的一个进程。
这个进程可以通过直接调用 API 发起，也能使用 `kubectl drain` 或集群中的其他主体来发起。
在这个过程中，移除每个 Pod 时将与对应的 PDB 协商，确保始终有足够数量的 Pod 在集群中运行。

以下策略允许 PDB 作者进一步控制此进程如何处理不健康的 Pod。

有两个策略可供选择：`IfHealthyBudget` 和 `AlwaysAllow`。

前者，`IfHealthyBudget` 采用现有行为以达到你默认可获得的最佳的可用性。
不健康的 Pod 只有在其应用中可用的 Pod 个数达到 `.status.desiredHealthy` 即最小可用个数时才会被干扰。

通过将 PDB 的 `spec.unhealthyPodEvictionPolicy` 字段设置为 `AlwaysAllow`，
可以表示尽可能为应用选择最佳的可用性。采用此策略时，始终能够驱逐不健康的 Pod。
这可以简化集群的维护和升级。

我们认为 `AlwaysAllow` 通常是一个更好的选择，但是对于某些关键工作负载，
你可能仍然倾向于防止不健康的 Pod 被从节点上腾空或其他形式的 API 发起的驱逐。

## 如何使用？  {#how-do-i-use-it}

这是一个 Alpha 特性，意味着你必须使用命令行参数 `--feature-gates=PDBUnhealthyPodEvictionPolicy=true`
为 kube-apiserver 启用 `PDBUnhealthyPodEvictionPolicy`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)。

以下是一个例子。假设你已在集群中启用了此特性门控且你已定义了运行普通 Web 服务器的 Deployment。
你已为 Deployment 的 Pod 打了标签 `app: nginx`。
你想要限制可避免的干扰，你知道对于此应用而言尽力而为的可用性也是足够的。
你决定即使这些 Web 服务器 Pod 不健康也允许驱逐。
你创建 PDB 守护此应用，使用 `AlwaysAllow` 策略驱逐不健康的 Pod：

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: nginx-pdb
spec:
  selector:
    matchLabels:
      app: nginx
  maxUnavailable: 1
  unhealthyPodEvictionPolicy: AlwaysAllow
```

## 查阅更多资料   {#how-can-i-learn-more}

- 阅读 KEP：[Unhealthy Pod Eviction Policy for PDBs](https://github.com/kubernetes/enhancements/tree/master/keps/sig-apps/3017-pod-healthy-policy-for-pdb)
- 阅读针对 PodDisruptionBudget
  的[不健康 Pod 驱逐策略](/zh-cn/docs/tasks/run-application/configure-pdb/#unhealthy-pod-eviction-policy)文档
- 参阅 [PodDisruptionBudget](/zh-cn/docs/concepts/workloads/pods/disruptions/#pod-disruption-budgets)、
  [腾空节点](/zh-cn/docs/tasks/administer-cluster/safely-drain-node/)和[驱逐](/zh-cn/docs/concepts/scheduling-eviction/api-eviction/)等 Kubernetes 文档

## 我如何参与？   {#how-do-i-get-involved}

如果你有任何反馈，请通过 Slack [#sig-apps](https://kubernetes.slack.com/archives/C18NZM5K9) 频道
（如有需要，请访问 https://slack.k8s.io/ 获取邀请）或通过 SIG Apps 邮件列表
[kubernetes-sig-apps@googlegroups.com](https://groups.google.com/g/kubernetes-sig-apps) 联系我们。
