---
layout: blog
title: 'Kubernetes 1.24: StatefulSet 的最大不可用副本数'
date: 2022-05-27
slug: maxunavailable-for-statefulset
---
**作者：** Mayank Kumar (Salesforce)

**译者：** Xiaoyang Zhang（Huawei）

Kubernetes [StatefulSet](/zh-cn/docs/concepts/workloads/controllers/statefulset/)，
自 1.5 版本中引入并在 1.9 版本中变得稳定以来，已被广泛用于运行有状态应用。它提供固定的 Pod 身份标识、
每个 Pod 的持久存储以及 Pod 的有序部署、扩缩容和滚动更新功能。你可以将 StatefulSet
视为运行复杂有状态应用程序的原子构建块。随着 Kubernetes 的使用增多，需要 StatefulSet 的场景也越来越多。
当 StatefulSet 的 Pod 管理策略为 `OrderedReady` 时，其中许多场景需要比当前所支持的一次一个 Pod
的更新更快的滚动更新。

这里有些例子：

- 我使用 StatefulSet 来编排一个基于缓存的多实例应用程序，其中缓存的规格很大。
  缓存冷启动，需要相当长的时间才能启动容器。所需要的初始启动任务有很多。在应用程序完全更新之前，
  此 StatefulSet 上的 RollingUpdate 将花费大量时间。如果 StatefulSet 支持一次更新多个 Pod，
  那么更新速度会快得多。

- 我的有状态应用程序由 leader 和 follower 或者一个 writer 和多个 reader 组成。
  我有多个 reader 或 follower，并且我的应用程序可以容忍多个 Pod 同时出现故障。
  我想一次更新这个应用程序的多个 Pod，特别是当我的应用程序实例数量很多时，这样我就能快速推出新的更新。
  注意，我的应用程序仍然需要每个 Pod 具有唯一标识。

为了支持这样的场景，Kubernetes 1.24 提供了一个新的 alpha 特性。在使用新特性之前，必须启用
`MaxUnavailableStatefulSet` 特性标志。一旦启用，就可以指定一个名为 `maxUnavailable` 的新字段，
这是 StatefulSet `spec` 的一部分。例如：

```
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
  namespace: default
spec:
  podManagementPolicy: OrderedReady  # 你必须设为 OrderedReady
  replicas: 5
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      # 镜像自发布以来已更改（以前使用的仓库为 "k8s.gcr.io"）
      - image: registry.k8s.io/nginx-slim:0.8
        imagePullPolicy: IfNotPresent
        name: nginx
  updateStrategy:
    rollingUpdate:
      maxUnavailable: 2 # 这是 alpha 特性的字段，默认值是 1
      partition: 0
    type: RollingUpdate
```

如果你启用了新特性，但没有在 StatefulSet 中指定 `maxUnavailable` 的值，Kubernetes
会默认设置 `maxUnavailable: 1`。这与你不启用新特性时看到的行为是一致的。

我将基于该示例清单做场景演练，以演示此特性是如何工作的。我将部署一个有 5 个副本的 StatefulSet，
`maxUnavailable` 设置为 2 并将 `partition` 设置为 0。

我可以通过将镜像更改为 `registry.k8s.io/nginx-slim:0.9` 来触发滚动更新。一旦开始滚动更新，
就可以看到一次更新 2 个 Pod，因为 `maxUnavailable` 的当前值是 2。
下面的输出显示了一个时间段内的结果，但并不是完整过程。`maxUnavailable` 可以是绝对数值（例如 2）或所需 Pod
的百分比（例如 10%），绝对数是通过百分比计算结果进行四舍五入到最接近的整数得出的。

```
kubectl get pods --watch 
```

```
NAME    READY   STATUS    RESTARTS   AGE
web-0   1/1     Running   0          85s
web-1   1/1     Running   0          2m6s
web-2   1/1     Running   0          106s
web-3   1/1     Running   0          2m47s
web-4   1/1     Running   0          2m27s
web-4   1/1     Terminating   0          5m43s ----> start terminating 4
web-3   1/1     Terminating   0          6m3s  ----> start terminating 3
web-3   0/1     Terminating   0          6m7s
web-3   0/1     Pending       0          0s
web-3   0/1     Pending       0          0s
web-4   0/1     Terminating   0          5m48s
web-4   0/1     Terminating   0          5m48s
web-3   0/1     ContainerCreating   0          2s
web-3   1/1     Running             0          2s
web-4   0/1     Pending             0          0s
web-4   0/1     Pending             0          0s
web-4   0/1     ContainerCreating   0          0s
web-4   1/1     Running             0          1s
web-2   1/1     Terminating         0          5m46s ----> start terminating 2 (only after both 4 and 3 are running)
web-1   1/1     Terminating         0          6m6s  ----> start terminating 1
web-2   0/1     Terminating         0          5m47s
web-1   0/1     Terminating         0          6m7s
web-1   0/1     Pending             0          0s
web-1   0/1     Pending             0          0s
web-1   0/1     ContainerCreating   0          1s
web-1   1/1     Running             0          2s
web-2   0/1     Pending             0          0s
web-2   0/1     Pending             0          0s
web-2   0/1     ContainerCreating   0          0s
web-2   1/1     Running             0          1s
web-0   1/1     Terminating         0          6m6s ----> start terminating 0 (only after 2 and 1 are running)
web-0   0/1     Terminating         0          6m7s
web-0   0/1     Pending             0          0s
web-0   0/1     Pending             0          0s
web-0   0/1     ContainerCreating   0          0s
web-0   1/1     Running             0          1s
```
注意，滚动更新一开始，4 和 3（两个最高序号的 Pod）同时开始进入 `Terminating` 状态。
Pod 4 和 3 会按照自身节奏进行更新。一旦 Pod 4 和 3 更新完毕后，Pod 2 和 1 会同时进入
`Terminating` 状态。当 Pod 2 和 1 都准备完毕处于 `Running` 状态时，Pod 0 开始进入 `Terminating` 状态

在 Kubernetes 中，StatefulSet 更新 Pod 时遵循严格的顺序。在此示例中，更新从副本 4 开始，
然后是副本 3，然后是副本 2，以此类推，一次更新一个 Pod。当一次只更新一个 Pod 时，
副本 3 不可能在副本 4 之前准备好进入 `Running` 状态。当 `maxUnavailable` 值
大于 1 时（在示例场景中我设置 `maxUnavailable` 值为 2），副本 3 可能在副本 4 之前准备好并运行，
这是没问题的。如果你是开发人员并且设置 `maxUnavailable` 值大于 1，你应该知道可能出现这种情况，
并且如果有这种情况的话，你必须确保你的应用程序能够处理发生的此类顺序问题。当你设置 `maxUnavailable`
值大于 1 时，更新 Pod 的批次之间会保证顺序。该保证意味着在批次 0（副本 4 和 3）中的 Pod
准备好之前，更新批次 2（副本 2 和 1）中的 Pod 无法开始更新。

尽管 Kubernetes 将这些称为**副本**，但你的有状态应用程序可能不这样理解，StatefulSet 的每个
Pod 可能持有与其他 Pod 完全不同的数据。重要的是，StatefulSet 的更新是分批进行的，
你现在让批次大小大于 1（作为 alpha 特性）。

还要注意，上面的行为采用的 Pod 管理策略是 `podManagementPolicy: OrderedReady`。
如果你的 StatefulSet 的 Pod 管理策略是 `podManagementPolicy: Parallel`，
那么不仅是 `maxUnavailable` 数量的副本同时被终止，还会导致 `maxUnavailable` 数量的副本同时在
`ContainerCreating` 阶段。这就是所谓的突发（Bursting）。

因此，现在你可能有很多关于以下方面的问题：
- 当设置 `podManagementPolicy:Parallel` 时，会产生什么行为？
- 将 `partition` 设置为非 `0` 值时会发生什么？

自己试试看可能会更好。这是一个 alpha 特性，Kubernetes 贡献者正在寻找有关此特性的反馈。
这是否有助于你实现有状态的场景？你是否发现了一个 bug，或者你认为实现的行为不直观易懂，
或者它可能会破坏应用程序或让他们感到吃惊？请[登记一个 issue](https://github.com/kubernetes/kubernetes/issues)
告知我们。

## 进一步阅读和后续步骤 {#next-steps}
- [最多不可用 Pod 数](/zh-cn/docs/concepts/workloads/controllers/statefulset/#maximum-unavailable-pods)
- [KEP for MaxUnavailable for StatefulSet](https://github.com/kubernetes/enhancements/tree/master/keps/sig-apps/961-maxunavailable-for-statefulset)
- [代码实现](https://github.com/kubernetes/kubernetes/pull/82162/files)
- [增强跟踪 Issue](https://github.com/kubernetes/enhancements/issues/961)