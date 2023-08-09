---
title: 调试 StatefulSet
content_type: task
weight: 30
---

此任务展示如何调试 StatefulSet。

## {{% heading "prerequisites" %}}

* 你需要有一个 Kubernetes 集群，已配置好的 kubectl 命令行工具与你的集群进行通信。
* 你应该有一个运行中的 StatefulSet，以便用于调试。


## 调试 StatefulSet   {#debugging-a-statefulset}

StatefulSet 在创建 Pod 时为其设置了 `app.kubernetes.io/name=MyApp` 标签，列出仅属于某 StatefulSet
的所有 Pod 时，可以使用以下命令：

```shell
kubectl get pods -l app.kubernetes.io/name=MyApp
```

如果你发现列出的任何 Pod 长时间处于 `Unknown` 或 `Terminating` 状态，请参阅
[删除 StatefulSet Pod](/zh-cn/docs/tasks/run-application/delete-stateful-set/)
了解如何处理它们的说明。
你可以参考[调试 Pod](/zh-cn/docs/tasks/debug/debug-application/debug-pods/)
来调试 StatefulSet 中的各个 Pod。

## {{% heading "whatsnext" %}}

进一步了解如何[调试 Init 容器](/zh-cn/docs/tasks/debug/debug-application/debug-init-containers/)。

