---
title: 开发云控制器管理器
content_type: task
weight: 190
---


{{< feature-state for_k8s_version="v1.11" state="beta" >}}

{{< glossary_definition term_id="cloud-controller-manager" length="all">}}


## 背景   {#background}

由于云驱动的开发和发布与 Kubernetes 项目本身步调不同，将特定于云环境的代码抽象到
`cloud-controller-manager` 二进制组件有助于云厂商独立于 Kubernetes
核心代码推进其驱动开发。

Kubernetes 项目提供 cloud-controller-manager 的框架代码，其中包含 Go 语言的接口，
便于你（或者你的云驱动提供者）接驳你自己的实现。这意味着每个云驱动可以通过从
Kubernetes 核心代码导入软件包来实现一个 cloud-controller-manager；
每个云驱动会通过调用 `cloudprovider.RegisterCloudProvider` 接口来注册其自身实现代码，
从而更新一个用来记录可用云驱动的全局变量。

## 开发   {#developing}

### 树外（Out of Tree）

要为你的云环境构建一个树外（Out-of-Tree）云控制器管理器：

1. 使用满足 [`cloudprovider.Interface`](https://github.com/kubernetes/cloud-provider/blob/master/cloud.go)
   接口的实现来创建一个 Go 语言包。
2. 使用来自 Kubernetes 核心代码库的
   [cloud-controller-manager 中的 `main.go`](https://github.com/kubernetes/kubernetes/blob/master/cmd/cloud-controller-manager/main.go)
   作为 `main.go` 的模板。如上所述，唯一的区别应该是将导入的云包不同。
3. 在 `main.go` 中导入你的云包，确保你的包有一个 `init` 块来运行
   [`cloudprovider.RegisterCloudProvider`](https://github.com/kubernetes/cloud-provider/blob/master/plugins.go)。

很多云驱动都将其控制器管理器代码以开源代码的形式公开。
如果你在开发一个新的 cloud-controller-manager，你可以选择某个树外（Out-of-Tree）
云控制器管理器作为出发点。

### 树内（In Tree）

对于树内（In-Tree）驱动，你可以将树内云控制器管理器作为集群中的
{{< glossary_tooltip term_id="daemonset" text="DaemonSet" >}} 来运行。
有关详细信息，请参阅[云控制器管理器管理](/zh-cn/docs/tasks/administer-cluster/running-cloud-controller/)。
