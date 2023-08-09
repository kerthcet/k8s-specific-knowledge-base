---
title: Pod 调度就绪态
content_type: concept
weight: 40
---


{{< feature-state for_k8s_version="v1.26" state="alpha" >}}

Pod 一旦创建就被认为准备好进行调度。
Kubernetes 调度程序尽职尽责地寻找节点来放置所有待处理的 Pod。
然而，在实际环境中，会有一些 Pod 可能会长时间处于"缺少必要资源"状态。
这些 Pod 实际上以一种不必要的方式扰乱了调度器（以及 Cluster AutoScaler 这类下游的集成方）。

通过指定或删除 Pod 的 `.spec.schedulingGates`，可以控制 Pod 何时准备好被纳入考量进行调度。


## 配置 Pod schedulingGates  {#configuring-pod-schedulinggates}

`schedulingGates` 字段包含一个字符串列表，每个字符串文字都被视为 Pod 在被认为可调度之前应该满足的标准。
该字段只能在创建 Pod 时初始化（由客户端创建，或在准入期间更改）。
创建后，每个 schedulingGate 可以按任意顺序删除，但不允许添加新的调度门控。


## 用法示例  {#usage-example}

要将 Pod 标记为未准备好进行调度，你可以在创建 Pod 时附带一个或多个调度门控，如下所示：

{{< codenew file="pods/pod-with-scheduling-gates.yaml" >}}

Pod 创建后，你可以使用以下方法检查其状态：

```bash
kubectl get pod test-pod
```

输出显示它处于 `SchedulingGated` 状态：

```none
NAME       READY   STATUS            RESTARTS   AGE
test-pod   0/1     SchedulingGated   0          7s
```

你还可以通过运行以下命令检查其 `schedulingGates` 字段：

```bash
kubectl get pod test-pod -o jsonpath='{.spec.schedulingGates}'
```

输出是：

```none
[{"name":"example.com/foo"},{"name":"example.com/bar"}]
```

要通知调度程序此 Pod 已准备好进行调度，你可以通过重新应用修改后的清单来完全删除其 `schedulingGates`：

{{< codenew file="pods/pod-without-scheduling-gates.yaml" >}}

你可以通过运行以下命令检查 `schedulingGates` 是否已被清空：

```bash
kubectl get pod test-pod -o jsonpath='{.spec.schedulingGates}'
```

预计输出为空，你可以通过运行下面的命令来检查它的最新状态：

```bash
kubectl get pod test-pod -o wide
```

鉴于 test-pod 不请求任何 CPU/内存资源，预计此 Pod 的状态会从之前的
`SchedulingGated` 转变为 `Running`：

```none
NAME       READY   STATUS    RESTARTS   AGE   IP         NODE  
test-pod   1/1     Running   0          15s   10.0.0.4   node-2
```

## 可观测性  {#observability}

指标 `scheduler_pending_pods` 带有一个新标签 `"gated"`，
以区分 Pod 是否已尝试调度但被宣称不可调度，或明确标记为未准备好调度。
你可以使用 `scheduler_pending_pods{queue="gated"}` 来检查指标结果。

## 可变 Pod 调度指令    {#mutable-pod-scheduling-directives}

{{< feature-state for_k8s_version="v1.27" state="beta" >}}

当 Pod 具有调度门控时，你可以在某些约束条件下改变 Pod 的调度指令。
在高层次上，你只能收紧 Pod 的调度指令。换句话说，更新后的指令将导致
Pod 只能被调度到它之前匹配的节点子集上。
更具体地说，更新 Pod 的调度指令的规则如下：

1. 对于 `.spec.nodeSelector`，只允许增加。如果原来未设置，则允许设置此字段。

2. 对于 `spec.affinity.nodeAffinity`，如果当前值为 nil，则允许设置为任意值。

3. 如果 `NodeSelectorTerms` 之前为空，则允许设置该字段。
   如果之前不为空，则仅允许增加 `NodeSelectorRequirements` 到 `matchExpressions`
   或 `fieldExpressions`，且不允许更改当前的 `matchExpressions` 和 `fieldExpressions`。
   这是因为 `.requiredDuringSchedulingIgnoredDuringExecution.NodeSelectorTerms`
   中的条目被执行逻辑或运算，而 `nodeSelectorTerms[].matchExpressions` 和
   `nodeSelectorTerms[].fieldExpressions` 中的表达式被执行逻辑与运算。

4. 对于 `.preferredDuringSchedulingIgnoredDuringExecution`，所有更新都被允许。
   这是因为首选条目不具有权威性，因此策略控制器不会验证这些条目。

## {{% heading "whatsnext" %}}

* 阅读 [PodSchedulingReadiness KEP](https://github.com/kubernetes/enhancements/blob/master/keps/sig-scheduling/3521-pod-scheduling-readiness)
  了解更多详情
