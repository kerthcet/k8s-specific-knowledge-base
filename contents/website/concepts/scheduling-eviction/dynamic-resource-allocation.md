---
title: 动态资源分配
content_type: concept
weight: 65
---


{{< feature-state for_k8s_version="v1.27" state="alpha" >}}

动态资源分配是一个用于在 Pod 之间和 Pod 内部容器之间请求和共享资源的新 API。
它是对为通用资源所提供的持久卷 API 的泛化。第三方资源驱动程序负责跟踪和分配资源。
不同类型的资源支持用任意参数进行定义和初始化。

## {{% heading "prerequisites" %}}

Kubernetes v{{< skew currentVersion >}} 包含用于动态资源分配的集群级 API 支持，
但它需要被[显式启用](#enabling-dynamic-resource-allocation)。
你还必须为此 API 要管理的特定资源安装资源驱动程序。
如果你未运行 Kubernetes v{{< skew currentVersion>}}，
请查看对应版本的 Kubernetes 文档。


## API {#api}
`resource.k8s.io/v1alpha2`
{{< glossary_tooltip text="API 组" term_id="api-group" >}}提供四种新类型：

ResourceClass
: 定义由哪个资源驱动程序处理某种资源，并为其提供通用参数。
  集群管理员在安装资源驱动程序时创建 ResourceClass。

ResourceClaim
: 定义工作负载所需的特定资源实例。
  由用户创建（手动管理生命周期，可以在不同的 Pod 之间共享），
  或者由控制平面基于 ResourceClaimTemplate 为特定 Pod 创建
  （自动管理生命周期，通常仅由一个 Pod 使用）。

ResourceClaimTemplate
: 定义用于创建 ResourceClaim 的 spec 和一些元数据。
  部署工作负载时由用户创建。

PodSchedulingContext
: 供控制平面和资源驱动程序内部使用，
  在需要为 Pod 分配 ResourceClaim 时协调 Pod 调度。

ResourceClass 和 ResourceClaim 的参数存储在单独的对象中，
通常使用安装资源驱动程序时创建的 {{< glossary_tooltip
term_id="CustomResourceDefinition" text="CRD" >}} 所定义的类型。

`core/v1` 的 `PodSpec` 在新的 `resourceClaims` 字段中定义 Pod 所需的 ResourceClaim。
该列表中的条目引用 ResourceClaim 或 ResourceClaimTemplate。
当引用 ResourceClaim 时，使用此 PodSpec 的所有 Pod
（例如 Deployment 或 StatefulSet 中的 Pod）共享相同的 ResourceClaim 实例。
引用 ResourceClaimTemplate 时，每个 Pod 都有自己的实例。

容器资源的 `resources.claims` 列表定义容器可以访问的资源实例，
从而可以实现在一个或多个容器之间共享资源。

下面是一个虚构的资源驱动程序的示例。
该示例将为此 Pod 创建两个 ResourceClaim 对象，每个容器都可以访问其中一个。

```yaml
apiVersion: resource.k8s.io/v1alpha2
kind: ResourceClass
name: resource.example.com
driverName: resource-driver.example.com
---
apiVersion: cats.resource.example.com/v1
kind: ClaimParameters
name: large-black-cat-claim-parameters
spec:
  color: black
  size: large
---
apiVersion: resource.k8s.io/v1alpha2
kind: ResourceClaimTemplate
metadata:
  name: large-black-cat-claim-template
spec:
  spec:
    resourceClassName: resource.example.com
    parametersRef:
      apiGroup: cats.resource.example.com
      kind: ClaimParameters
      name: large-black-cat-claim-parameters
–--
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-cats
spec:
  containers:
  - name: container0
    image: ubuntu:20.04
    command: ["sleep", "9999"]
    resources:
      claims:
      - name: cat-0
  - name: container1
    image: ubuntu:20.04
    command: ["sleep", "9999"]
    resources:
      claims:
      - name: cat-1
  resourceClaims:
  - name: cat-0
    source:
      resourceClaimTemplateName: large-black-cat-claim-template
  - name: cat-1
    source:
      resourceClaimTemplateName: large-black-cat-claim-template
```
## 调度  {#scheduling}

与原生资源（CPU、RAM）和扩展资源（由设备插件管理，并由 kubelet 公布）不同，
调度器不知道集群中有哪些动态资源，
也不知道如何将它们拆分以满足特定 ResourceClaim 的要求。
资源驱动程序负责这些任务。
资源驱动程序在为 ResourceClaim 保留资源后将其标记为“已分配（Allocated）”。
然后告诉调度器集群中可用的 ResourceClaim 的位置。

ResourceClaim 可以在创建时就进行分配（“立即分配”），不用考虑哪些 Pod 将使用它。
默认情况下采用延迟分配，直到需要 ResourceClaim 的 Pod 被调度时
（即“等待第一个消费者”）再进行分配。

在这种模式下，调度器检查 Pod 所需的所有 ResourceClaim，并创建一个 PodScheduling 对象，
通知负责这些 ResourceClaim 的资源驱动程序，告知它们调度器认为适合该 Pod 的节点。
资源驱动程序通过排除没有足够剩余资源的节点来响应调度器。
一旦调度器有了这些信息，它就会选择一个节点，并将该选择存储在 PodScheduling 对象中。
然后，资源驱动程序为分配其 ResourceClaim，以便资源可用于该节点。
完成后，Pod 就会被调度。

作为此过程的一部分，ResourceClaim 会为 Pod 保留。
目前，ResourceClaim 可以由单个 Pod 独占使用或不限数量的多个 Pod 使用。

除非 Pod 的所有资源都已分配和保留，否则 Pod 不会被调度到节点，这是一个重要特性。
这避免了 Pod 被调度到一个节点但无法在那里运行的情况，
这种情况很糟糕，因为被挂起 Pod 也会阻塞为其保留的其他资源，如 RAM 或 CPU。

## 监控资源  {#monitoring-resources}

kubelet 提供了一个 gRPC 服务，以便发现正在运行的 Pod 的动态资源。
有关 gRPC 端点的更多信息，请参阅[资源分配报告](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources)。

## 限制 {#limitations}

调度器插件必须参与调度那些使用 ResourceClaim 的 Pod。
通过设置 `nodeName` 字段绕过调度器会导致 kubelet 拒绝启动 Pod，
因为 ResourceClaim 没有被保留或甚至根本没有被分配。
未来可能[去除该限制](https://github.com/kubernetes/kubernetes/issues/114005)。

## 启用动态资源分配 {#enabling-dynamic-resource-allocation}

动态资源分配是一个 **alpha 特性**，只有在启用 `DynamicResourceAllocation`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
和 `resource.k8s.io/v1alpha1` {{< glossary_tooltip text="API 组"
term_id="api-group" >}} 时才启用。
有关详细信息，参阅 `--feature-gates` 和 `--runtime-config`
[kube-apiserver 参数](/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver/)。
kube-scheduler、kube-controller-manager 和 kubelet 也需要设置该特性门控。

快速检查 Kubernetes 集群是否支持该功能的方法是列出 ResourceClass 对象：

```shell
kubectl get resourceclasses
```

如果你的集群支持动态资源分配，则响应是 ResourceClass 对象列表或：
```
No resources found
```

如果不支持，则会输出如下错误：
```
error: the server doesn't have a resource type "resourceclasses"
```

kube-scheduler 的默认配置仅在启用特性门控且使用 v1 配置 API 时才启用 "DynamicResources" 插件。
自定义配置可能需要被修改才能启用它。

除了在集群中启用该功能外，还必须安装资源驱动程序。
欲了解详细信息，请参阅驱动程序的文档。

## {{% heading "whatsnext" %}}

- 了解更多该设计的信息，
  参阅[动态资源分配 KEP](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/3063-dynamic-resource-allocation/README.md)。