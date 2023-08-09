---
title: 为命名空间配置默认的内存请求和限制
content_type: task
weight: 10
description: >-
  为命名空间定义默认的内存资源限制，这样在该命名空间中每个新建的 Pod 都会被配置上内存资源限制。
---



本章介绍如何为{{< glossary_tooltip text="命名空间" term_id="namespace" >}}配置默认的内存请求和限制。

一个 Kubernetes 集群可被划分为多个命名空间。
如果你在具有默认内存[限制](/zh-cn/docs/concepts/configuration/manage-resources-containers/#requests-and-limits)
的命名空间内尝试创建一个 Pod，并且这个 Pod 中的容器没有声明自己的内存资源限制，
那么{{< glossary_tooltip text="控制面" term_id="control-plane" >}}会为该容器设定默认的内存限制。

Kubernetes 还为某些情况指定了默认的内存请求，本章后面会进行介绍。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

在你的集群里你必须要有创建命名空间的权限。

你的集群中的每个节点必须至少有 2 GiB 的内存。


## 创建命名空间

创建一个命名空间，以便本练习中所建的资源与集群的其余资源相隔离。

```shell
kubectl create namespace default-mem-example
```

## 创建 LimitRange 和 Pod

以下为 {{< glossary_tooltip text="LimitRange" term_id="limitrange" >}} 的示例清单。
清单中声明了默认的内存请求和默认的内存限制。

{{< codenew file="admin/resource/memory-defaults.yaml" >}}

在 default-mem-example 命名空间创建限制范围：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/memory-defaults.yaml --namespace=default-mem-example
```

现在如果你在 default-mem-example 命名空间中创建一个 Pod，
并且该 Pod 中所有容器都没有声明自己的内存请求和内存限制，
{{< glossary_tooltip text="控制面" term_id="control-plane" >}}
会将内存的默认请求值 256MiB 和默认限制值 512MiB 应用到 Pod 上。

以下为只包含一个容器的 Pod 的清单。该容器没有声明内存请求和限制。

{{< codenew file="admin/resource/memory-defaults-pod.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/memory-defaults-pod.yaml --namespace=default-mem-example
```

查看 Pod 的详情：

```shell
kubectl get pod default-mem-demo --output=yaml --namespace=default-mem-example
```

输出内容显示该 Pod 的容器有 256 MiB 的内存请求和 512 MiB 的内存限制。
这些都是 LimitRange 设置的默认值。

```shell
containers:
- image: nginx
  imagePullPolicy: Always
  name: default-mem-demo-ctr
  resources:
    limits:
      memory: 512Mi
    requests:
      memory: 256Mi
```

删除你的 Pod：

```shell
kubectl delete pod default-mem-demo --namespace=default-mem-example
```

## 声明容器的限制而不声明它的请求会怎么样？

以下为只包含一个容器的 Pod 的清单。该容器声明了内存限制，而没有声明内存请求。

{{< codenew file="admin/resource/memory-defaults-pod-2.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/memory-defaults-pod-2.yaml --namespace=default-mem-example
```

查看 Pod 的详情：

```shell
kubectl get pod default-mem-demo-2 --output=yaml --namespace=default-mem-example
```

输出结果显示容器的内存请求被设置为它的内存限制相同的值。注意该容器没有被指定默认的内存请求值 256MiB。

```
resources:
  limits:
    memory: 1Gi
  requests:
    memory: 1Gi
```

## 声明容器的内存请求而不声明内存限制会怎么样？

以下为只包含一个容器的 Pod 的清单。该容器声明了内存请求，但没有内存限制：

{{< codenew file="admin/resource/memory-defaults-pod-3.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/memory-defaults-pod-3.yaml --namespace=default-mem-example
```

查看 Pod 声明：

```shell
kubectl get pod default-mem-demo-3 --output=yaml --namespace=default-mem-example
```

输出结果显示所创建的 Pod 中，容器的内存请求为 Pod 清单中声明的值。
然而同一容器的内存限制被设置为 512MiB，此值是该命名空间的默认内存限制值。

```
resources:
  limits:
    memory: 512Mi
  requests:
    memory: 128Mi
```

{{< note >}}

`LimitRange` **不会**检查它应用的默认值的一致性。 这意味着 `LimitRange` 设置的 _limit_ 的默认值可能小于客户端提交给
API 服务器的声明中为容器指定的 _request_ 值。如果发生这种情况，最终会导致 Pod 无法调度。更多信息，
请参阅[资源限制的 limit 和 request](/zh-cn/docs/concepts/policy/limit-range/#constraints-on-resource-limits-and-requests)。

{{< /note >}}

## 设置默认内存限制和请求的动机

如果你的命名空间设置了内存 {{< glossary_tooltip text="资源配额" term_id="resource-quota" >}}，
那么为内存限制设置一个默认值会很有帮助。
以下是内存资源配额对命名空间的施加的三条限制：

* 命名空间中运行的每个 Pod 中的容器都必须有内存限制。
  （如果为 Pod 中的每个容器声明了内存限制，
  Kubernetes 可以通过将其容器的内存限制相加推断出 Pod 级别的内存限制）。

* 内存限制用来在 Pod 被调度到的节点上执行资源预留。
  预留给命名空间中所有 Pod 使用的内存总量不能超过规定的限制。

* 命名空间中所有 Pod 实际使用的内存总量也不能超过规定的限制。

当你添加 LimitRange 时：

如果该命名空间中的任何 Pod 的容器未指定内存限制，
控制面将默认内存限制应用于该容器，
这样 Pod 可以在受到内存 ResourceQuota 限制的命名空间中运行。

## 清理

删除你的命名空间：

```shell
kubectl delete namespace default-mem-example
```

## {{% heading "whatsnext" %}}

### 集群管理员参考

* [为命名空间配置默认的 CPU 请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/)
* [为命名空间配置最小和最大内存限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/)
* [为命名空间配置最小和最大 CPU 限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/)
* [为命名空间配置内存和 CPU 配额](/zh-cn/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)
* [为命名空间配置 Pod 配额](/zh-cn/docs/tasks/administer-cluster/manage-resources/quota-pod-namespace/)
* [为 API 对象配置配额](/zh-cn/docs/tasks/administer-cluster/quota-api-object/)

### 应用开发者参考

* [为容器和 Pod 分配内存资源](/zh-cn/docs/tasks/configure-pod-container/assign-memory-resource/)
* [为容器和 Pod 分配 CPU 资源](/zh-cn/docs/tasks/configure-pod-container/assign-cpu-resource/)
* [为 Pod 配置服务质量](/zh-cn/docs/tasks/configure-pod-container/quality-service-pod/)

