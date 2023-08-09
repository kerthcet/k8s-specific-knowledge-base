---
title: Kubernetes 组件
content_type: concept
description: >
  Kubernetes 集群由控制平面的组件和一组称为节点的机器组成。
weight: 30
card:
  name: concepts
  weight: 20
---

当你部署完 Kubernetes，便拥有了一个完整的集群。

{{< glossary_definition term_id="cluster" length="all" >}}

本文档概述了一个正常运行的 Kubernetes 集群所需的各种组件。

{{< figure src="/images/docs/components-of-kubernetes.svg" alt="Kubernetes 的组件" caption="Kubernetes 集群的组件" class="diagram-large" >}}


## 控制平面组件（Control Plane Components）    {#control-plane-components}

控制平面组件会为集群做出全局决策，比如资源的调度。
以及检测和响应集群事件，例如当不满足部署的 `replicas` 字段时，
要启动新的 {{< glossary_tooltip text="pod" term_id="pod">}}）。

控制平面组件可以在集群中的任何节点上运行。
然而，为了简单起见，设置脚本通常会在同一个计算机上启动所有控制平面组件，
并且不会在此计算机上运行用户容器。
请参阅[使用 kubeadm 构建高可用性集群](/zh-cn/docs/setup/production-environment/tools/kubeadm/high-availability/)
中关于跨多机器控制平面设置的示例。

### kube-apiserver

{{< glossary_definition term_id="kube-apiserver" length="all" >}}

### etcd

{{< glossary_definition term_id="etcd" length="all" >}}

### kube-scheduler

{{< glossary_definition term_id="kube-scheduler" length="all" >}}

### kube-controller-manager

{{< glossary_definition term_id="kube-controller-manager" length="all" >}}

有许多不同类型的控制器。以下是一些例子：

* 节点控制器（Node Controller）：负责在节点出现故障时进行通知和响应
* 任务控制器（Job Controller）：监测代表一次性任务的 Job 对象，然后创建 Pods 来运行这些任务直至完成
* 端点分片控制器（EndpointSlice controller）：填充端点分片（EndpointSlice）对象（以提供 Service 和 Pod 之间的链接）。
* 服务账号控制器（ServiceAccount controller）：为新的命名空间创建默认的服务账号（ServiceAccount）。

以上并不是一个详尽的列表。
### cloud-controller-manager

{{< glossary_definition term_id="cloud-controller-manager" length="short" >}}

`cloud-controller-manager` 仅运行特定于云平台的控制器。
因此如果你在自己的环境中运行 Kubernetes，或者在本地计算机中运行学习环境，
所部署的集群不需要有云控制器管理器。

与 `kube-controller-manager` 类似，`cloud-controller-manager`
将若干逻辑上独立的控制回路组合到同一个可执行文件中，
供你以同一进程的方式运行。
你可以对其执行水平扩容（运行不止一个副本）以提升性能或者增强容错能力。

下面的控制器都包含对云平台驱动的依赖：

  * 节点控制器（Node Controller）：用于在节点终止响应后检查云提供商以确定节点是否已被删除
  * 路由控制器（Route Controller）：用于在底层云基础架构中设置路由
  * 服务控制器（Service Controller）：用于创建、更新和删除云提供商负载均衡器

## Node 组件  {#node-components}

节点组件会在每个节点上运行，负责维护运行的 Pod 并提供 Kubernetes 运行环境。

### kubelet

{{< glossary_definition term_id="kubelet" length="all" >}}

### kube-proxy

{{< glossary_definition term_id="kube-proxy" length="all" >}}

### 容器运行时（Container Runtime）    {#container-runtime}

{{< glossary_definition term_id="container-runtime" length="all" >}}

## 插件（Addons）    {#addons}

插件使用 Kubernetes 资源（{{< glossary_tooltip text="DaemonSet" term_id="daemonset" >}}、
{{< glossary_tooltip text="Deployment" term_id="deployment" >}} 等）实现集群功能。
因为这些插件提供集群级别的功能，插件中命名空间域的资源属于 `kube-system` 命名空间。

下面描述众多插件中的几种。有关可用插件的完整列表，请参见
[插件（Addons）](/zh-cn/docs/concepts/cluster-administration/addons/)。

### DNS   {#dns}

尽管其他插件都并非严格意义上的必需组件，但几乎所有 Kubernetes
集群都应该有[集群 DNS](/zh-cn/docs/concepts/services-networking/dns-pod-service/)，
因为很多示例都需要 DNS 服务。

集群 DNS 是一个 DNS 服务器，和环境中的其他 DNS 服务器一起工作，它为 Kubernetes 服务提供 DNS 记录。

Kubernetes 启动的容器自动将此 DNS 服务器包含在其 DNS 搜索列表中。

### Web 界面（仪表盘）   {#web-ui-dashboard}

[Dashboard](/zh-cn/docs/tasks/access-application-cluster/web-ui-dashboard/)
是 Kubernetes 集群的通用的、基于 Web 的用户界面。
它使用户可以管理集群中运行的应用程序以及集群本身，
并进行故障排除。

### 容器资源监控   {#container-resource-monitoring}

[容器资源监控](/zh-cn/docs/tasks/debug/debug-cluster/resource-usage-monitoring/)
将关于容器的一些常见的时间序列度量值保存到一个集中的数据库中，
并提供浏览这些数据的界面。

### 集群层面日志   {#cluster-level-logging}

[集群层面日志](/zh-cn/docs/concepts/cluster-administration/logging/)机制负责将容器的日志数据保存到一个集中的日志存储中，
这种集中日志存储提供搜索和浏览接口。

### 网络插件   {#network-plugins}

[网络插件](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins)
是实现容器网络接口（CNI）规范的软件组件。它们负责为 Pod 分配 IP 地址，并使这些 Pod 能在集群内部相互通信。

## {{% heading "whatsnext" %}}

进一步了解以下内容：
   * [节点](/zh-cn/docs/concepts/architecture/nodes/)及其与[控制平面](/zh-cn/docs/concepts/architecture/control-plane-node-communication/)的通信。
   * Kubernetes 中的[控制器](/zh-cn/docs/concepts/architecture/controller/)。
   * Kubernetes 的默认调度程序 [kube-scheduler](/zh-cn/docs/concepts/scheduling-eviction/kube-scheduler/)。
   * etcd 的官方[文档](https://etcd.io/docs/)。
   * Kubernetes 中的几个[容器运行时](/zh-cn/docs/setup/production-environment/container-runtimes/)。
   * 使用 [cloud-controller-manager](/zh-cn/docs/concepts/architecture/cloud-controller/) 与云提供商进行集成。
   * [kubectl](/docs/reference/generated/kubectl/kubectl-commands) 命令。
