---
content_type: concept
title: 资源监控工具
weight: 15
---


要扩展应用程序并提供可靠的服务，你需要了解应用程序在部署时的行为。
你可以通过检测容器、[Pod](/zh-cn/docs/concepts/workloads/pods)、
[Service](/zh-cn/docs/concepts/services-networking/service/)
和整个集群的特征来检查 Kubernetes 集群中应用程序的性能。
Kubernetes 在每个级别上提供有关应用程序资源使用情况的详细信息。
此信息使你可以评估应用程序的性能，以及在何处可以消除瓶颈以提高整体性能。


在 Kubernetes 中，应用程序监控不依赖单个监控解决方案。在新集群上，
你可以使用[资源度量](#resource-metrics-pipeline)或[完整度量](#full-metrics-pipeline)管道来收集监视统计信息。

## 资源度量管道  {#resource-metrics-pipeline}

资源指标管道提供了一组与集群组件，例如
[Horizontal Pod Autoscaler](/zh-cn/docs/tasks/run-application/horizontal-pod-autoscale/)
控制器以及 `kubectl top` 实用程序相关的有限度量。
这些指标是由轻量级的、短期、内存存储的
[metrics-server](https://github.com/kubernetes-sigs/metrics-server) 收集，
并通过 `metrics.k8s.io` 公开。

metrics-server 发现集群中的所有节点，并且查询每个节点的
[kubelet](/zh-cn/docs/reference/command-line-tools-reference/kubelet/)
以获取 CPU 和内存使用情况。
kubelet 充当 Kubernetes 主节点与节点之间的桥梁，管理机器上运行的 Pod 和容器。
kubelet 将每个 Pod 转换为其组成的容器，并通过容器运行时接口从容器运行时获取各个容器使用情况统计信息。
如果某个容器运行时使用 Linux cgroups 和名字空间来实现容器。
并且这一容器运行时不发布资源用量统计信息，
那么 kubelet 可以直接查找这些统计信息（使用来自 [cAdvisor](https://github.com/google/cadvisor) 的代码）。
无论这些统计信息如何到达，kubelet 都会通过 metrics-server Resource Metrics API 公开聚合的
Pod 资源用量统计信息。
该 API 在 kubelet 的经过身份验证和只读的端口上的 `/metrics/resource/v1beta1` 中提供。

## 完整度量管道  {#full-metrics-pipeline}

一个完整度量管道可以让你访问更丰富的度量。
Kubernetes 还可以根据集群的当前状态，使用 Pod 水平自动扩缩器等机制，
通过自动调用扩展或调整集群来响应这些度量。
监控管道从 kubelet 获取度量值，然后通过适配器将它们公开给 Kubernetes，
方法是实现 `custom.metrics.k8s.io` 或 `external.metrics.k8s.io` API。

Kubernetes 在设计上保证能够与 [OpenMetrics](https://openmetrics.io/) 一同使用，
OpenMetrics 是 
[CNCF 可观测性和分析 - 监控项目](https://landscape.cncf.io/card-mode?category=monitoring&project=graduated,incubating,member,no&grouping=category&sort=stars)之一，
它构建于 [Prometheus 暴露格式](https://prometheus.io/docs/instrumenting/exposition_formats/)之上，
并对其进行了扩展，这些扩展几乎 100% 向后兼容。

如果你浏览 [CNCF Landscape](https://landscape.cncf.io/card-mode?category=monitoring&project=graduated,incubating,member,no&grouping=category&sort=stars)，
你可以看到许多监控项目，它们可以用在 Kubernetes 上，**抓取**指标数据并利用这些数据来观测你的集群，
选择哪种工具或哪些工具可以满足你的需求，这完全取决于你自己。 
CNCF 的可观测性和分析景观包括了各种开源软件、付费的软件即服务（SaaS）以及其他混合商业产品。

当你设计和实现一个完整的指标监控数据管道时，你可以将监控数据反馈给 Kubernetes。
例如，HorizontalPodAutoscaler 可以使用处理过的指标数据来计算出你的工作负载组件运行了多少个 Pod。

将完整的指标管道集成到 Kubernetes 实现中超出了 Kubernetes
文档的范围，因为可能的解决方案具有非常广泛的范围。

监控平台的选择在很大程度上取决于你的需求、预算和技术资源。
Kubernetes 不推荐任何特定的指标管道；
可使用[许多选项](https://landscape.cncf.io/card-mode?category=monitoring&project=graduated,incubating,member,no&grouping=category&sort=stars)。
你的监控系统应能够处理 [OpenMetrics](https://openmetrics.io/) 指标传输标准，
并且需要选择最适合基础设施平台的整体设计和部署。

## {{% heading "whatsnext" %}}

了解其他调试工具，包括：

* [日志记录](/zh-cn/docs/concepts/cluster-administration/logging/)
* [监控](/zh-cn/docs/tasks/debug/debug-cluster/resource-usage-monitoring/)
* [通过 `exec` 进入容器](/zh-cn/docs/tasks/debug/debug-application/get-shell-running-container/)
* [通过代理连接到容器](/zh-cn/docs/tasks/extend-kubernetes/http-proxy-access-api/)
* [通过端口转发连接到容器](/zh-cn/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)
* [使用 crictl 检查 Kubernetes 节点](/zh-cn/docs/tasks/debug/debug-cluster/crictl/)
