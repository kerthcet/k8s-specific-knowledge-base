---
layout: blog
title: "Kubernetes 1.25：应用滚动上线所用的两个特性进入稳定阶段"
date: 2022-09-15
slug: "app-rollout-features-reach-stable"
---

**作者：** Ravi Gudimetla (Apple)、Filip Křepinský (Red Hat)、Maciej Szulik (Red Hat)

这篇博客描述了两个特性，即用于 StatefulSet 的 `minReadySeconds` 以及用于 DaemonSet 的 `maxSurge`，
SIG Apps 很高兴宣布这两个特性在 Kubernetes 1.25 进入稳定阶段。

当 `.spec.updateStrategy` 字段设置为 `RollingUpdate` 时，
你可以设置 `minReadySeconds`， 通过让每个 Pod 等待一段预期时间来减缓 StatefulSet 的滚动上线。

当 `.spec.updateStrategy` 字段设置为 `RollingUpdate` 时，
`maxSurge` 允许 DaemonSet 工作负载在滚动上线期间在一个节点上运行同一 Pod 的多个实例。
这对于消费者而言有助于将 DaemonSet 的停机时间降到最低。

这两个特性也可用于 Deployment 和其他工作负载。此功能的提级有助于将这一功能在所有工作负载上对齐。

## 这两个特性能解决什么问题？   {#what-problems-do-these-features-solve}

### 针对 StatefulSet 的 minReadySeconds   {#solved-problem-statefulset-minreadyseconds}

`minReadySeconds` 确保 StatefulSet 工作负载在给定的秒数内处于 `Ready`，
然后才会将该 Pod 报告为 `Available`。
处于 `Ready` 和 `Available` 状况的这种说法对工作负载相当重要。
例如 Prometheus 这些工作负载有多个 Alertmanager 实例，
只有 Alertmanager 的状态转换完成后才应该被视为 `Available`。
`minReadySeconds` 还有助于云驱动确定何时使用负载均衡器。
因为 Pod 应在给定的秒数内处于 `Ready`，所以这就提供了一段缓冲时间，
防止新 Pod 还没起来之前就在轮转过程中杀死了旧 Pod。

### 针对 DaemonSet 的 maxSurge     {#how-use-daemonset-maxsurge}

CNI、CSI 这类 Kubernetes 系统级别的组件通常以 DaemonSet 方式运行。如果这些 DaemonSet 在升级期间瞬间挂掉，
对应的组件可能会影响工作负载的可用性。此特性允许 DaemonSet Pod 临时增加数量，以此确保 DaemonSet 的停机时间为零。

请注意在 DaemonSet 中不允许同时使用 `hostPort` 和 `maxSurge`，
因为 DaemonSet Pod 被捆绑到了一个节点，所以两个活跃的 Pod 无法共享同一节点上的相同端口。

## 工作原理    {#how-does-it-work}

### 针对 StatefulSet 的 minReadySeconds  {#how-does-statefulset-minreadyseconds-work}

StatefulSet 控制器监视 StatefulSet Pod 并统计特定的 Pod 已处于 `Running` 状态多长时间了，
如果这个值大于或等于 StatefulSet 的 `.spec.minReadySeconds` 字段中指定的时间，
StatefulSet 控制器将更新 StatefulSet 的状态中的 `AvailableReplicas` 字段。

### 针对 DaemonSet 的 maxSurge  {#how-does-daemonset-maxsurge-work}

DaemonSet 控制器根据 `.spec.strategy.rollingUpdate.maxSurge` 中给出的值创建额外 Pod
（超出 DaemonSet 规约所设定的预期数量）。
这些 Pod 将运行在旧 DaemonSet Pod 运行所在的同一节点上，直到这个旧 Pod 被杀死为止。

- 默认值为 0。
- 当 `MaxUnavailable` 为 0 时此值不能为 `0`。
- 此值可以指定为一个绝对的 Pod 个数或预期 Pod 总数的百分比（向上取整）。

## 我如何使用它？   {#how-do-i-use-it}

### 针对 StatefulSet 的 minReadySeconds   {#how-use-statefulset-minreadyseconds}

执行以下命令为任意 StatefulSet 指定一个 `minReadySeconds` 值，
通过检验 `AvailableReplicas` 字段查看这些 Pod 是否可用：

```
kubectl get statefulset/<StatefulSet 名称> -o yaml
```

请注意 `minReadySeconds` 的默认值为 0。

### 针对 DaemonSet 的 maxSurge  {#how-use-daemonset-maxsurge}

为 `.spec.updateStrategy.rollingUpdate.maxSurge` 指定一个值并将
`.spec.updateStrategy.rollingUpdate.maxUnavailable` 设置为 `0`。

然后观察下一次滚动上线是不是更快，同时运行的 Pod 数量是不是更多。

```
kubectl rollout restart daemonset <name_of_the_daemonset>
kubectl get pods -w
```

## 我如何才能了解更多？   {#how-can-i-learn-more}

### 针对 StatefulSet 的 minReadySeconds   {#learn-more-statefulset-minreadyseconds}

- 文档： https://k8s.io/zh-cn/docs/concepts/workloads/controllers/statefulset/#minimum-ready-seconds
- KEP： https://github.com/kubernetes/enhancements/issues/2599
- API 变更： https://github.com/kubernetes/kubernetes/pull/100842

### 针对 DaemonSet 的 maxSurge   {#learn-more-daemonset-maxsurge}

- 文档： https://k8s.io/zh-cn/docs/tasks/manage-daemon/update-daemon-set/
- KEP： https://github.com/kubernetes/enhancements/issues/1591
- API 变更： https://github.com/kubernetes/kubernetes/pull/96375

## 我如何参与？   {#how-do-i-get-involved}

请通过 Slack [#sig-apps](https://kubernetes.slack.com/archives/C18NZM5K9) 频道或通过 SIG Apps
邮件列表 [kubernetes-sig-apps@googlegroups.com](https://groups.google.com/g/kubernetes-sig-apps) 联系我们。
