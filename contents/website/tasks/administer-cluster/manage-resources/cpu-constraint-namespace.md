---
title: 为命名空间配置 CPU 最小和最大约束
content_type: task
weight: 40
description: >-
  为命名空间定义一个有效的 CPU 资源限制范围，使得在该命名空间中所有新建
  Pod 的 CPU 资源是在你所设置的范围内。
---



本页介绍如何为{{< glossary_tooltip text="命名空间" term_id="namespace" >}}中的容器和 Pod
设置其所使用的 CPU 资源的最小和最大值。你可以通过 [LimitRange](/zh-cn/docs/reference/kubernetes-api/policy-resources/limit-range-v1/)
对象声明 CPU 的最小和最大值.
如果 Pod 不能满足 LimitRange 的限制，就无法在该命名空间中被创建。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} 

在你的集群里你必须要有创建命名空间的权限。

集群中的每个节点都必须至少有 1.0 个 CPU 可供 Pod 使用。

请阅读 [CPU 的含义](/zh-cn/docs/concepts/configuration/manage-resources-containers/#meaning-of-cpu)
理解 "1 CPU" 在 Kubernetes 中的含义。


## 创建命名空间

创建一个命名空间，以便本练习中创建的资源和集群的其余资源相隔离。

```shell
kubectl create namespace constraints-cpu-example
```

## 创建 LimitRange 和 Pod

以下为 {{< glossary_tooltip text="LimitRange" term_id="limitrange" >}} 的示例清单：

{{< codenew file="admin/resource/cpu-constraints.yaml" >}}

创建 LimitRange:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-constraints.yaml --namespace=constraints-cpu-example
```

查看 LimitRange 详情：

```shell
kubectl get limitrange cpu-min-max-demo-lr --output=yaml --namespace=constraints-cpu-example
```

输出结果显示 CPU 的最小和最大限制符合预期。但需要注意的是，尽管你在 LimitRange 
的配置文件中你没有声明默认值，默认值也会被自动创建。

```yaml
limits:
- default:
    cpu: 800m
  defaultRequest:
    cpu: 800m
  max:
    cpu: 800m
  min:
    cpu: 200m
  type: Container
```


现在，每当你在 constraints-cpu-example 命名空间中创建 Pod 时，或者某些其他的
Kubernetes API 客户端创建了等价的 Pod 时，Kubernetes 就会执行下面的步骤：

* 如果 Pod 中的任何容器未声明自己的 CPU 请求和限制，控制面将为该容器设置默认的 CPU 请求和限制。

* 确保该 Pod 中的每个容器的 CPU 请求至少 200 millicpu。

* 确保该 Pod 中每个容器 CPU 请求不大于 800 millicpu。

{{< note >}}
当创建 LimitRange 对象时，你也可以声明大页面和 GPU 的限制。
当这些资源同时声明了 'default' 和 'defaultRequest' 参数时，两个参数值必须相同。
{{< /note >}}

以下为某个仅包含一个容器的 Pod 的清单。
该容器声明了 CPU 请求 500 millicpu 和 CPU 限制 800 millicpu 。
这些参数满足了 LimitRange 对象为此名字空间规定的 CPU 最小和最大限制。

{{< codenew file="admin/resource/cpu-constraints-pod.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-constraints-pod.yaml --namespace=constraints-cpu-example
```

确认 Pod 正在运行，并且其容器处于健康状态：

```shell
kubectl get pod constraints-cpu-demo --namespace=constraints-cpu-example
```

查看 Pod 的详情：

```shell
kubectl get pod constraints-cpu-demo --output=yaml --namespace=constraints-cpu-example
```

输出结果显示该 Pod 的容器的 CPU 请求为 500 millicpu，CPU 限制为 800 millicpu。
这些参数满足 LimitRange 规定的限制范围。

```yaml
resources:
  limits:
    cpu: 800m
  requests:
    cpu: 500m
```

## 删除 Pod

```shell
kubectl delete pod constraints-cpu-demo --namespace=constraints-cpu-example
```

## 尝试创建一个超过最大 CPU 限制的 Pod

这里给出了包含一个容器的 Pod 清单。容器声明了 500 millicpu 的 CPU 
请求和 1.5 CPU 的 CPU 限制。

{{< codenew file="admin/resource/cpu-constraints-pod-2.yaml" >}}

尝试创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-constraints-pod-2.yaml --namespace=constraints-cpu-example
```

输出结果表明 Pod 没有创建成功，因为其中定义了一个无法被接受的容器。
该容器之所以无法被接受是因为其中设定了过高的 CPU 限制值：

```
Error from server (Forbidden): error when creating "examples/admin/resource/cpu-constraints-pod-2.yaml":
pods "constraints-cpu-demo-2" is forbidden: maximum cpu usage per Container is 800m, but limit is 1500m.
```

## 尝试创建一个不满足最小 CPU 请求的 Pod

以下为某个只有一个容器的 Pod 的清单。该容器声明了 CPU 请求 100 millicpu 和 CPU 限制 800 millicpu。

{{< codenew file="admin/resource/cpu-constraints-pod-3.yaml" >}}

尝试创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-constraints-pod-3.yaml --namespace=constraints-cpu-example
```

输出结果显示 Pod 没有创建成功，因为其中定义了一个无法被接受的容器。
该容器无法被接受的原因是其中所设置的 CPU 请求小于最小值的限制：

```
Error from server (Forbidden): error when creating "examples/admin/resource/cpu-constraints-pod-3.yaml":
pods "constraints-cpu-demo-3" is forbidden: minimum cpu usage per Container is 200m, but request is 100m.
```

## 创建一个没有声明 CPU 请求和 CPU 限制的 Pod

以下为一个只有一个容器的 Pod 的清单。该容器没有声明 CPU 请求，也没有声明 CPU 限制。

{{< codenew file="admin/resource/cpu-constraints-pod-4.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-constraints-pod-4.yaml --namespace=constraints-cpu-example
```

查看 Pod 的详情：

```
kubectl get pod constraints-cpu-demo-4 --namespace=constraints-cpu-example --output=yaml
```

输出结果显示 Pod 的唯一容器的 CPU 请求为 800 millicpu，CPU 限制为 800 millicpu。

容器是怎样获得这些数值的呢？


```yaml
resources:
  limits:
    cpu: 800m
  requests:
    cpu: 800m
```

因为这一容器没有声明自己的 CPU 请求和限制，
控制面会根据命名空间中配置 LimitRange
设置[默认的 CPU 请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/)。

此时，你的 Pod 可能已经运行起来也可能没有运行起来。
回想一下我们本次任务的先决条件是你的每个节点都至少有 1 CPU。
如果你的每个节点都只有 1 CPU，那将没有一个节点拥有足够的可分配 CPU 来满足 800 millicpu 的请求。
如果你在用的节点恰好有 2 CPU，那么有可能有足够的 CPU 来满足 800 millicpu 的请求。

删除你的 Pod：

```
kubectl delete pod constraints-cpu-demo-4 --namespace=constraints-cpu-example
```

## CPU 最小和最大限制的强制执行

只有当 Pod 创建或者更新时，LimitRange 为命名空间规定的 CPU 最小和最大限制才会被强制执行。
如果你对 LimitRange 进行修改，那不会影响此前创建的 Pod。

## 最小和最大 CPU 限制范围的动机

作为集群管理员，你可能想设定 Pod 可以使用的 CPU 资源限制。例如：

* 集群中的每个节点有两个 CPU。你不想接受任何请求超过 2 个 CPU 的 Pod，
  因为集群中没有节点可以支持这种请求。
* 你的生产和开发部门共享一个集群。你想允许生产工作负载消耗 3 个 CPU，
  而开发部门工作负载的消耗限制为 1 个 CPU。
  你可以为生产和开发创建不同的命名空间，并且为每个命名空间都应用 CPU 限制。

## 清理

删除你的命名空间：

```shell
kubectl delete namespace constraints-cpu-example
```

## {{% heading "whatsnext" %}}


### 集群管理员参考：

* [为命名空间配置默认内存请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)
* [为命名空间配置默认 CPU 请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/)
* [为命名空间配置内存限制的最小值和最大值](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/)
* [为命名空间配置内存和 CPU 配额](/zh-cn/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)
* [为命名空间配置 Pod 配额](/zh-cn/docs/tasks/administer-cluster/manage-resources/quota-pod-namespace/)
* [为 API 对象配置配额](/zh-cn/docs/tasks/administer-cluster/quota-api-object/)


### 应用开发者参考：

* [为容器和 Pod 分配内存资源](/zh-cn/docs/tasks/configure-pod-container/assign-memory-resource/)
* [为容器和 Pod 分配 CPU 资源](/zh-cn/docs/tasks/configure-pod-container/assign-cpu-resource/)
* [为 Pod 配置服务质量](/zh-cn/docs/tasks/configure-pod-container/quality-service-pod/)

