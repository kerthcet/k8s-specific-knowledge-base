---
title: 节点指标数据
content_type: reference
weight: 50
description: >-
  访问 kubelet 所观测到的节点、卷、Pod 和容器级别指标的机制。
---

[kubelet](/zh-cn/docs/reference/command-line-tools-reference/kubelet/)
在节点、卷、Pod 和容器级别收集统计信息，并在
[概要 API](https://github.com/kubernetes/kubernetes/blob/7d309e0104fedb57280b261e5677d919cb2a0e2d/staging/src/k8s.io/kubelet/pkg/apis/stats/v1alpha1/types.go)
中输出这些信息。

你可以通过 Kubernetes API 服务器将代理的请求发送到 stats 概要 API。

下面是一个名为 `minikube` 的节点的概要 API 请求示例：

```shell
kubectl get --raw "/api/v1/nodes/minikube/proxy/stats/summary"
```

下面是使用 `curl` 所执行的相同 API 调用：

```shell
# 你需要先运行 "kubectl proxy"
# 更改 8080 为 "kubectl proxy" 指派的端口
curl http://localhost:8080/api/v1/nodes/minikube/proxy/stats/summary
```

{{< note >}}
从 `metrics-server` 0.6.x 开始，`metrics-server` 查询 `/metrics/resource` kubelet 端点，
不查询 `/stats/summary`。
{{< /note >}}

## 概要指标 API 源  {#summary-api-source}

默认情况下，Kubernetes 使用 kubelet 内运行的嵌入式 [cAdvisor](https://github.com/google/cadvisor)
获取节点概要指标数据。如果你在自己的集群中启用 `PodAndContainerStatsFromCRI`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)，
且你通过{{< glossary_tooltip term_id="cri" text="容器运行时接口">}} (CRI) 使用支持统计访问的容器运行时，
则 kubelet [将使用 CRI 来获取 Pod 和容器级别的指标数据](/zh-cn/docs/reference/instrumentation/cri-pod-container-metrics)，
而不是 cAdvisor 来获取。
## {{% heading "whatsnext" %}}

[集群故障排查](/zh-cn/docs/tasks/debug/debug-cluster/)任务页面讨论了如何使用依赖这些数据的指标管道。
