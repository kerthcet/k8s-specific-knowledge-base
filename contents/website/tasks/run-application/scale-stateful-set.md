---
title: 扩缩 StatefulSet
content_type: task
weight: 50
---

本文介绍如何扩缩 StatefulSet。StatefulSet 的扩缩指的是增加或者减少副本个数。

## {{% heading "prerequisites" %}}

- StatefulSets 仅适用于 Kubernetes 1.5 及以上版本。
  要查看你的 Kubernetes 版本，运行 `kubectl version`。
- 不是所有 Stateful 应用都能很好地执行扩缩操作。
  如果你不是很确定是否要扩缩你的 StatefulSet，可先参阅
  [StatefulSet 概念](/zh-cn/docs/concepts/workloads/controllers/statefulset/)
  或者 [StatefulSet 教程](/zh-cn/docs/tutorials/stateful-application/basic-stateful-set/)。

- 仅当你确定你的有状态应用的集群是完全健康的，才可执行扩缩操作.


## 扩缩 StatefulSet   {#scaling-statefulset}

### 使用 `kubectl` 扩缩 StatefulSet    {#use-kubectl-to-scale-statefulsets}

首先，找到你要扩缩的 StatefulSet。

```shell
kubectl get statefulsets <statefulset 名称>
```

更改 StatefulSet 中副本个数：

```shell
kubectl scale statefulsets <statefulset 名称> --replicas=<新的副本数>
```

### 对 StatefulSet 执行就地更新    {#make-in-place-updates-on-statefulset}

另外, 你可以[就地更新](/zh-cn/docs/concepts/cluster-administration/manage-deployment/#in-place-updates-of-resources) StatefulSet。

如果你的 StatefulSet 最初通过 `kubectl apply` 或 `kubectl create --save-config` 创建，
你可以更新 StatefulSet 清单中的 `.spec.replicas`，然后执行命令 `kubectl apply`：

```shell
kubectl apply -f <更新后的 statefulset 文件>
```

否则，可以使用 `kubectl edit` 编辑副本字段：

```shell
kubectl edit statefulsets <statefulset 名称>
```

或者使用 `kubectl patch`：

```shell
kubectl patch statefulsets <statefulset 名称> -p '{"spec":{"replicas":<new-replicas>}}'
```

## 故障排查  {#troubleshooting}

### 缩容操作无法正常工作   {#scaling-down-does-not-work}

当 Stateful 所管理的任何 Pod 不健康时，你不能对该 StatefulSet 执行缩容操作。
仅当 StatefulSet 的所有 Pod 都处于运行状态和 Ready 状况后才可缩容。

如果 `spec.replicas` 大于 1，Kubernetes 无法判定 Pod 不健康的原因。
Pod 不健康可能是由于永久性故障造成也可能是瞬态故障。
瞬态故障可能是节点升级或维护而引起的节点重启造成的。

如果该 Pod 不健康是由于永久性故障导致，则在不纠正该故障的情况下进行缩容可能会导致
StatefulSet 进入一种状态，其成员 Pod 数量低于应正常运行的副本数。
这种状态也许会导致 StatefulSet 不可用。

如果由于瞬态故障而导致 Pod 不健康并且 Pod 可能再次变为可用，那么瞬态错误可能会干扰你对
StatefulSet 的扩容/缩容操作。一些分布式数据库在同时有节点加入和离开时会遇到问题。
在这些情况下，最好是在应用级别进行分析扩缩操作的状态，并且只有在确保
Stateful 应用的集群是完全健康时才执行扩缩操作。

## {{% heading "whatsnext" %}}

- 进一步了解[删除 StatefulSet](/zh-cn/docs/tasks/run-application/delete-stateful-set/)
