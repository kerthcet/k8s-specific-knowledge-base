---
title: 删除 StatefulSet
content_type: task
weight: 60
---


本任务展示如何删除 {{< glossary_tooltip text="StatefulSet" term_id="StatefulSet" >}}。

## {{% heading "prerequisites" %}}

- 本任务假设在你的集群上已经运行了由 StatefulSet 创建的应用。


## 删除 StatefulSet   {#deleting-a-statefulset}

你可以像删除 Kubernetes 中的其他资源一样删除 StatefulSet：
使用 `kubectl delete` 命令，并按文件或者名字指定 StatefulSet。

```shell
kubectl delete -f <file.yaml>
```

```shell
kubectl delete statefulsets <statefulset 名称>
```

删除 StatefulSet 之后，你可能需要单独删除关联的无头服务。

```shell
kubectl delete service <服务名称>
```

当通过 `kubectl` 删除 StatefulSet 时，StatefulSet 会被缩容为 0。
属于该 StatefulSet 的所有 Pod 也被删除。
如果你只想删除 StatefulSet 而不删除 Pod，使用 `--cascade=orphan`。

```shell
kubectl delete -f <file.yaml> --cascade=orphan
```

通过将 `--cascade=orphan` 传递给 `kubectl delete`，在删除 StatefulSet 对象之后，
StatefulSet 管理的 Pod 会被保留下来。如果 Pod 具有标签 `app.kubernetes.io/name=MyApp`，
则可以按照如下方式删除它们：

```shell
kubectl delete pods -l app.kubernetes.io/name=MyApp
```

### 持久卷  {#persistent-volumes}

删除 StatefulSet 管理的 Pod 并不会删除关联的卷。这是为了确保你有机会在删除卷之前从卷中复制数据。
在 Pod 已经终止后删除 PVC 可能会触发删除背后的 PV 持久卷，具体取决于存储类和回收策略。
永远不要假定在 PVC 删除后仍然能够访问卷。

{{< note >}}
删除 PVC 时要谨慎，因为这可能会导致数据丢失。
{{< /note >}}

### 完全删除 StatefulSet  {#complete-deletion-of-a-statefulset}

要删除 StatefulSet 中的所有内容，包括关联的 Pod，
你可以运行如下所示的一系列命令：

```shell
grace=$(kubectl get pods <stateful-set-pod> --template '{{.spec.terminationGracePeriodSeconds}}')
kubectl delete statefulset -l app.kubernetes.io/name=MyApp
sleep $grace
kubectl delete pvc -l app.kubernetes.io/name=MyApp
```

在上面的例子中，Pod 的标签为 `app.kubernetes.io/name=MyApp`；适当地替换你自己的标签。

### 强制删除 StatefulSet 的 Pod   {#force-deletion-of-statefulset-pods}

如果你发现 StatefulSet 的某些 Pod 长时间处于 'Terminating' 或者 'Unknown' 状态，
则可能需要手动干预以强制从 API 服务器中删除这些 Pod。这是一项有点危险的任务。
详细信息请阅读[强制删除 StatefulSet 的 Pod](/zh-cn/docs/tasks/run-application/force-delete-stateful-set-pod/)。

## {{% heading "whatsnext" %}}

进一步了解[强制删除 StatefulSet 的 Pod](/zh-cn/docs/tasks/run-application/force-delete-stateful-set-pod/)。
