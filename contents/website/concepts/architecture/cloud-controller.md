---
title: 云控制器管理器
content_type: concept
weight: 40
---



{{< feature-state state="beta" for_k8s_version="v1.11" >}}

使用云基础设施技术，你可以在公有云、私有云或者混合云环境中运行 Kubernetes。
Kubernetes 的信条是基于自动化的、API 驱动的基础设施，同时避免组件间紧密耦合。

{{< glossary_definition term_id="cloud-controller-manager" length="all" prepend="组件 cloud-controller-manager 是指云控制器管理器，">}}

`cloud-controller-manager` 组件是基于一种插件机制来构造的，
这种机制使得不同的云厂商都能将其平台与 Kubernetes 集成。

## 设计  {#design}

![Kubernetes 组件](/images/docs/components-of-kubernetes.svg)

云控制器管理器以一组多副本的进程集合的形式运行在控制面中，通常表现为 Pod
中的容器。每个 `cloud-controller-manager`
在同一进程中实现多个{{< glossary_tooltip text="控制器" term_id="controller" >}}。

{{< note >}}
你也可以用 Kubernetes {{< glossary_tooltip text="插件" term_id="addons" >}}
的形式而不是控制面中的一部分来运行云控制器管理器。
{{< /note >}}

## 云控制器管理器的功能 {#functions-of-the-ccm}

云控制器管理器中的控制器包括：

### 节点控制器   {#node-controller}

节点控制器负责在云基础设施中创建了新服务器时为之更新{{< glossary_tooltip text="节点（Node）" term_id="node" >}}对象。
节点控制器从云提供商获取当前租户中主机的信息。节点控制器执行以下功能：

1. 使用从云平台 API 获取的对应服务器的唯一标识符更新 Node 对象；
2. 利用特定云平台的信息为 Node 对象添加注解和标签，例如节点所在的区域
   （Region）和所具有的资源（CPU、内存等等）；
3. 获取节点的网络地址和主机名；
4. 检查节点的健康状况。如果节点无响应，控制器通过云平台 API
   查看该节点是否已从云中禁用、删除或终止。如果节点已从云中删除，
   则控制器从 Kubernetes 集群中删除 Node 对象。

某些云驱动实现中，这些任务被划分到一个节点控制器和一个节点生命周期控制器中。

### 路由控制器   {#route-controller}

Route 控制器负责适当地配置云平台中的路由，以便 Kubernetes 集群中不同节点上的容器之间可以相互通信。

取决于云驱动本身，路由控制器可能也会为 Pod 网络分配 IP 地址块。

### 服务控制器   {#service-controller}

{{< glossary_tooltip text="服务（Service）" term_id="service" >}}与受控的负载均衡器、
IP 地址、网络包过滤、目标健康检查等云基础设施组件集成。
服务控制器与云驱动的 API 交互，以配置负载均衡器和其他基础设施组件。
你所创建的 Service 资源会需要这些组件服务。

## 鉴权   {#authorization}

本节分别讲述云控制器管理器为了完成自身工作而产生的对各类 API 对象的访问需求。

### 节点控制器  {#authorization-node-controller}

节点控制器只操作 Node 对象。它需要读取和修改 Node 对象的完全访问权限。

`v1/Node`：

- get
- list
- create
- update
- patch
- watch
- delete

### 路由控制器 {#authorization-route-controller}

路由控制器会监听 Node 对象的创建事件，并据此配置路由设施。
它需要读取 Node 对象的 Get 权限。

`v1/Node`：

- get

### 服务控制器 {#authorization-service-controller}

服务控制器监测 Service 对象的 **create**、**update** 和 **delete** 事件，
并配置对应服务的 Endpoints 对象
（对于 EndpointSlices，kube-controller-manager 按需对其进行管理）。

为了访问 Service 对象，它需要 **list** 和 **watch** 访问权限。
为了更新 Service 对象，它需要 **patch** 和 **update** 访问权限。

为了能够配置 Service 对应的 Endpoints 资源，
它需要 **create**、**list**、**get**、**watch** 和 **update** 等访问权限。

`v1/Service`：

- list
- get
- watch
- patch
- update

### 其他  {#authorization-miscellaneous}

在云控制器管理器的实现中，其核心部分需要创建 Event 对象的访问权限，
并创建 ServiceAccount 资源以保证操作安全性的权限。

`v1/Event`:

- create
- patch
- update

`v1/ServiceAccount`:

- create

用于云控制器管理器 {{< glossary_tooltip term_id="rbac" text="RBAC" >}}
的 ClusterRole 如下例所示：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cloud-controller-manager
rules:
- apiGroups:
  - ""
  resources:
  - events
  verbs:
  - create
  - patch
  - update
- apiGroups:
  - ""
  resources:
  - nodes
  verbs:
  - '*'
- apiGroups:
  - ""
  resources:
  - nodes/status
  verbs:
  - patch
- apiGroups:
  - ""
  resources:
  - services
  verbs:
  - list
  - patch
  - update
  - watch
- apiGroups:
  - ""
  resources:
  - serviceaccounts
  verbs:
  - create
- apiGroups:
  - ""
  resources:
  - persistentvolumes
  verbs:
  - get
  - list
  - update
  - watch
- apiGroups:
  - ""
  resources:
  - endpoints
  verbs:
  - create
  - get
  - list
  - watch
  - update
```

## {{% heading "whatsnext" %}}

* [云控制器管理器的管理](/zh-cn/docs/tasks/administer-cluster/running-cloud-controller/#cloud-controller-manager)
给出了运行和管理云控制器管理器的指南。

* 要升级 HA 控制平面以使用云控制器管理器，
请参见[将复制的控制平面迁移以使用云控制器管理器](/zh-cn/docs/tasks/administer-cluster/controller-manager-leader-migration/)。

* 想要了解如何实现自己的云控制器管理器，或者对现有项目进行扩展么？

  - 云控制器管理器使用 Go 语言的接口（具体指在
    [kubernetes/cloud-provider](https://github.com/kubernetes/cloud-provider)
    项目中 [`cloud.go`](https://github.com/kubernetes/cloud-provider/blob/release-1.26/cloud.go#L43-L69)
    文件中所定义的 `CloudProvider` 接口），从而使得针对各种云平台的具体实现都可以接入。

  - 本文中列举的共享控制器（节点控制器、路由控制器和服务控制器等）的实现以及其他一些生成具有
    CloudProvider 接口的框架的代码，都是 Kubernetes 的核心代码。
    特定于云驱动的实现虽不是 Kubernetes 核心成分，仍要实现 `CloudProvider` 接口。

  - 关于如何开发插件的详细信息，
    可参考[开发云控制器管理器](/zh-cn/docs/tasks/administer-cluster/developing-cloud-controller-manager/)文档。
