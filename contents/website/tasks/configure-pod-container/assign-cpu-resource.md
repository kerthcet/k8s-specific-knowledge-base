---
title: 为容器和 Pods 分配 CPU 资源
content_type: task
weight: 20
---



本页面展示如何为容器设置 CPU **request（请求）** 和 CPU **limit（限制）**。
容器使用的 CPU 不能超过所配置的限制。
如果系统有空闲的 CPU 时间，则可以保证给容器分配其所请求数量的 CPU 资源。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

你的集群必须至少有 1 个 CPU 可用才能运行本任务中的示例。

本页的一些步骤要求你在集群中运行
[metrics-server](https://github.com/kubernetes-sigs/metrics-server)
服务。如果你的集群中已经有正在运行的 metrics-server 服务，可以跳过这些步骤。

如果你正在运行 {{< glossary_tooltip term_id="minikube" >}}，请运行以下命令启用 metrics-server：

```shell
minikube addons enable metrics-server
```

查看 metrics-server（或者其他资源指标 API `metrics.k8s.io` 服务提供者）是否正在运行，
请键入以下命令：

```shell
kubectl get apiservices
```

如果资源指标 API 可用，则会输出将包含一个对 `metrics.k8s.io` 的引用。

```
NAME
v1beta1.metrics.k8s.io
```


## 创建一个名字空间 {#create-a-namespace}

创建一个{{< glossary_tooltip text="名字空间" term_id="namespace" >}}，以便将
本练习中创建的资源与集群的其余部分资源隔离。

```shell
kubectl create namespace cpu-example
```

## 指定 CPU 请求和 CPU 限制 {#specify-a-CPU-request-and-a-CPU-limit}

要为容器指定 CPU 请求，请在容器资源清单中包含 `resources: requests` 字段。
要指定 CPU 限制，请包含 `resources:limits`。

在本练习中，你将创建一个具有一个容器的 Pod。容器将会请求 0.5 个 CPU，而且最多限制使用 1 个 CPU。
这是 Pod 的配置文件：

{{< codenew file="pods/resource/cpu-request-limit.yaml" >}}

配置文件的 `args` 部分提供了容器启动时的参数。
`-cpus "2"` 参数告诉容器尝试使用 2 个 CPU。

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/resource/cpu-request-limit.yaml --namespace=cpu-example
```

验证所创建的 Pod 处于 Running 状态

```shell
kubectl get pod cpu-demo --namespace=cpu-example
```

查看显示关于 Pod 的详细信息：

```shell
kubectl get pod cpu-demo --output=yaml --namespace=cpu-example
```

输出显示 Pod 中的一个容器的 CPU 请求为 500 milliCPU，并且 CPU 限制为 1 个 CPU。

```yaml
resources:
  limits:
    cpu: "1"
  requests:
    cpu: 500m
```

使用 `kubectl top` 命令来获取该 Pod 的指标：

```shell
kubectl top pod cpu-demo --namespace=cpu-example
```

此示例输出显示 Pod 使用的是 974 milliCPU，即略低于 Pod 配置中指定的 1 个 CPU 的限制。

```
NAME                        CPU(cores)   MEMORY(bytes)
cpu-demo                    974m         <something>
```

回想一下，通过设置 `-cpu "2"`，你将容器配置为尝试使用 2 个 CPU，
但是容器只被允许使用大约 1 个 CPU。
容器的 CPU 用量受到限制，因为该容器正尝试使用超出其限制的 CPU 资源。

{{< note >}}
CPU 使用率低于 1.0 的另一种可能的解释是，节点可能没有足够的 CPU 资源可用。
回想一下，此练习的先决条件需要你的集群至少具有 1 个 CPU 可用。
如果你的容器在只有 1 个 CPU 的节点上运行，则容器无论为容器指定的 CPU 限制如何，
都不能使用超过 1 个 CPU。
{{< /note >}}

## CPU 单位  {#cpu-units}

CPU 资源以 **CPU** 单位度量。Kubernetes 中的一个 CPU 等同于：

* 1 个 AWS vCPU 
* 1 个 GCP核心
* 1 个 Azure vCore
* 裸机上具有超线程能力的英特尔处理器上的 1 个超线程

小数值是可以使用的。一个请求 0.5 CPU 的容器保证会获得请求 1 个 CPU 的容器的 CPU 的一半。
你可以使用后缀 `m` 表示毫。例如 `100m` CPU、100 milliCPU 和 0.1 CPU 都相同。
精度不能超过 1m。

CPU 请求只能使用绝对数量，而不是相对数量。0.1 在单核、双核或 48 核计算机上的 CPU 数量值是一样的。

删除 Pod：

```shell
kubectl delete pod cpu-demo --namespace=cpu-example
```

## 设置超过节点能力的 CPU 请求 {#specify-a-CPU-request-that-is-too-big-for-your-nodes}

CPU 请求和限制与都与容器相关，但是我们可以考虑一下 Pod 具有对应的 CPU 请求和限制这样的场景。
Pod 对 CPU 用量的请求等于 Pod 中所有容器的请求数量之和。
同样，Pod 的 CPU 资源限制等于 Pod 中所有容器 CPU 资源限制数之和。

Pod 调度是基于资源请求值来进行的。
仅在某节点具有足够的 CPU 资源来满足 Pod CPU 请求时，Pod 将会在对应节点上运行：

在本练习中，你将创建一个 Pod，该 Pod 的 CPU 请求对于集群中任何节点的容量而言都会过大。
下面是 Pod 的配置文件，其中有一个容器。容器请求 100 个 CPU，这可能会超出集群中任何节点的容量。

{{< codenew file="pods/resource/cpu-request-limit-2.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/resource/cpu-request-limit-2.yaml --namespace=cpu-example
```
查看该 Pod 的状态：

```shell
kubectl get pod cpu-demo-2 --namespace=cpu-example
```

输出显示 Pod 状态为 Pending。也就是说，Pod 未被调度到任何节点上运行，
并且 Pod 将无限期地处于 Pending 状态：

```
NAME         READY     STATUS    RESTARTS   AGE
cpu-demo-2   0/1       Pending   0          7m
```


查看有关 Pod 的详细信息，包含事件：

```shell
kubectl describe pod cpu-demo-2 --namespace=cpu-example
```

输出显示由于节点上的 CPU 资源不足，无法调度容器：

```
Events:
  Reason                        Message
  ------                        -------
  FailedScheduling      No nodes are available that match all of the following predicates:: Insufficient cpu (3).
```

删除你的 Pod： 

```shell
kubectl delete pod cpu-demo-2 --namespace=cpu-example
```

## 如果不指定 CPU 限制 {#if-you-do-not-specify-a-cpu-limit}

如果你没有为容器指定 CPU 限制，则会发生以下情况之一：

* 容器在可以使用的 CPU 资源上没有上限。因而可以使用所在节点上所有的可用 CPU 资源。

* 容器在具有默认 CPU 限制的名字空间中运行，系统会自动为容器设置默认限制。
  集群管理员可以使用
  [LimitRange](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#limitrange-v1-core/)
  指定 CPU 限制的默认值。

## 如果你设置了 CPU 限制但未设置 CPU 请求 {#if-you-specify-a-CPU-limit-but-do-not-specify-a-CPU-request}

如果你为容器指定了 CPU 限制值但未为其设置 CPU 请求，Kubernetes 会自动为其
设置与 CPU 限制相同的 CPU 请求值。类似的，如果容器设置了内存限制值但未设置
内存请求值，Kubernetes 也会为其设置与内存限制值相同的内存请求。

## CPU 请求和限制的初衷 {#motivation-for-CPU-requests-and-limits}

通过配置你的集群中运行的容器的 CPU 请求和限制，你可以有效利用集群上可用的 CPU 资源。
通过将 Pod CPU 请求保持在较低水平，可以使 Pod 更有机会被调度。
通过使 CPU 限制大于 CPU 请求，你可以完成两件事：

* Pod 可能会有突发性的活动，它可以利用碰巧可用的 CPU 资源。

* Pod 在突发负载期间可以使用的 CPU 资源数量仍被限制为合理的数量。	

## 清理 {#clean-up}

删除名字空间：

```shell
kubectl delete namespace cpu-example
```

## {{% heading "whatsnext" %}}


### 针对应用开发者 {#for-app-developers}

* [将内存资源分配给容器和 Pod](/zh-cn/docs/tasks/configure-pod-container/assign-memory-resource/)

* [配置 Pod 服务质量](/zh-cn/docs/tasks/configure-pod-container/quality-service-pod/)

### 针对集群管理员 {for-cluster-administrators}

* [配置名字空间的默认内存请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)
* [为名字空间配置默认 CPU 请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/)
* [为名字空间配置最小和最大内存限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/)
* [为名字空间配置最小和最大 CPU 约束](/zh-cn/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/)
* [为名字空间配置内存和 CPU 配额](/zh-cn/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)
* [为名字空间配置 Pod 配额](/zh-cn/docs/tasks/administer-cluster/manage-resources/quota-pod-namespace/)
* [配置 API 对象的配额](/zh-cn/docs/tasks/administer-cluster/quota-api-object/)
* [调整分配给容器的 CPU 和内存资源](/zh-cn/docs/tasks/configure-pod-container/resize-container-resources/)
 