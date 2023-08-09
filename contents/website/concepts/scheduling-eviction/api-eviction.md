---
title: API 发起的驱逐
content_type: concept
weight: 110
---
{{< glossary_definition term_id="api-eviction" length="short" >}} </br>

你可以通过直接调用 Eviction API 发起驱逐，也可以通过编程的方式使用
{{<glossary_tooltip term_id="kube-apiserver" text="API 服务器">}}的客户端来发起驱逐，
比如 `kubectl drain` 命令。
此操作创建一个 `Eviction` 对象，该对象再驱动 API 服务器终止选定的 Pod。

API 发起的驱逐将遵从你的
[`PodDisruptionBudgets`](/zh-cn/docs/tasks/run-application/configure-pdb/)
和 [`terminationGracePeriodSeconds`](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle#pod-termination)
配置。

使用 API 创建 Eviction 对象，就像对 Pod 执行策略控制的
[`DELETE` 操作](/zh-cn/docs/reference/kubernetes-api/workload-resources/pod-v1/#delete-delete-a-pod)

## 调用 Eviction API   {#calling-eviction-api}

你可以使用 [Kubernetes 语言客户端](/zh-cn/docs/tasks/administer-cluster/access-cluster-api/#programmatic-access-to-the-api)
来访问 Kubernetes API 并创建 `Eviction` 对象。
要执行此操作，你应该用 POST 发出要尝试的请求，类似于下面的示例：

{{< tabs name="Eviction_example" >}}
{{% tab name="policy/v1" %}}
{{< note >}}
`policy/v1` 版本的 Eviction 在 v1.22 以及更高的版本中可用，之前的发行版本使用 `policy/v1beta1` 版本。
{{< /note >}}

```json
{
  "apiVersion": "policy/v1",
  "kind": "Eviction",
  "metadata": {
    "name": "quux",
    "namespace": "default"
  }
}
```
{{% /tab %}}
{{% tab name="policy/v1beta1" %}}
{{< note >}}
在 v1.22 版本废弃以支持 `policy/v1`。
{{< /note >}}

```json
{
  "apiVersion": "policy/v1beta1",
  "kind": "Eviction",
  "metadata": {
    "name": "quux",
    "namespace": "default"
  }
}
```
{{% /tab %}}
{{< /tabs >}}

或者，你可以通过使用 `curl` 或者 `wget` 来访问 API 以尝试驱逐操作，类似于以下示例：

```bash
curl -v -H 'Content-type: application/json' https://your-cluster-api-endpoint.example/api/v1/namespaces/default/pods/quux/eviction -d @eviction.json
```

## API 发起驱逐的工作原理   {#how-api-initiated-eviction-works}

当你使用 API 来请求驱逐时，API 服务器将执行准入检查，并通过以下方式之一做出响应：

* `200 OK`：允许驱逐，子资源 `Eviction` 被创建，并且 Pod 被删除，
  类似于发送一个 `DELETE` 请求到 Pod 地址。
* `429 Too Many Requests`：当前不允许驱逐，因为配置了
  {{<glossary_tooltip term_id="pod-disruption-budget" text="PodDisruptionBudget">}}。
  你可以稍后再尝试驱逐。你也可能因为 API 速率限制而看到这种响应。
* `500 Internal Server Error`：不允许驱逐，因为存在配置错误，
  例如存在多个 PodDisruptionBudgets 引用同一个 Pod。

如果你想驱逐的 Pod 不属于有 PodDisruptionBudget 的工作负载，
API 服务器总是返回 `200 OK` 并且允许驱逐。

如果 API 服务器允许驱逐，Pod 按照如下方式删除：

1. API 服务器中的 `Pod` 资源会更新上删除时间戳，之后 API 服务器会认为此 `Pod` 资源将被终止。
   此 `Pod` 资源还会标记上配置的宽限期。
1. 本地运行状态的 Pod 所处的节点上的 {{<glossary_tooltip term_id="kubelet" text="kubelet">}}
   注意到 `Pod` 资源被标记为终止，并开始优雅停止本地 Pod。
1. 当 kubelet 停止 Pod 时，控制面从 {{<glossary_tooltip term_id="endpoint" text="Endpoint">}}
   和 {{<glossary_tooltip term_id="endpoint-slice" text="EndpointSlice">}}
   对象中移除该 Pod。因此，控制器不再将此 Pod 视为有用对象。
1. Pod 的宽限期到期后，kubelet 强制终止本地 Pod。
1. kubelet 告诉 API 服务器删除 `Pod` 资源。
1. API 服务器删除 `Pod` 资源。

## 解决驱逐被卡住的问题   {#troubleshooting-stuck-evictions}

在某些情况下，你的应用可能进入中断状态，
在你干预之前，驱逐 API 总是返回 `429` 或 `500`。
例如，如果 ReplicaSet 为你的应用程序创建了 Pod，
但新的 Pod 没有进入 `Ready` 状态，就会发生这种情况。
在最后一个被驱逐的 Pod 有很长的终止宽限期的情况下，你可能也会注意到这种行为。

如果你注意到驱逐被卡住，请尝试以下解决方案之一：

* 终止或暂停导致问题的自动化操作，重新启动操作之前，请检查被卡住的应用程序。
* 等待一段时间后，直接从集群控制平面删除 Pod，而不是使用 Eviction API。

## {{% heading "whatsnext" %}}

* 了解如何使用 [Pod 干扰预算](/zh-cn/docs/tasks/run-application/configure-pdb/)保护你的应用。
* 了解[节点压力引发的驱逐](/zh-cn/docs/concepts/scheduling-eviction/node-pressure-eviction/)。
* 了解 [Pod 优先级和抢占](/zh-cn/docs/concepts/scheduling-eviction/pod-priority-preemption/)。
