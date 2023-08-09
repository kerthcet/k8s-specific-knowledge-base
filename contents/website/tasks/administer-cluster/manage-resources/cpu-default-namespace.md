---
title: 为命名空间配置默认的 CPU 请求和限制
content_type: task
weight: 20
description: >-
  为命名空间定义默认的 CPU 资源限制，在该命名空间中每个新建的 Pod 都会被配置上 CPU 资源限制。
---


本章介绍如何为{{< glossary_tooltip text="命名空间" term_id="namespace" >}}配置默认的 CPU 请求和限制。

一个 Kubernetes 集群可被划分为多个命名空间。
如果你在具有默认 CPU[限制](/zh-cn/docs/concepts/configuration/manage-resources-containers/#requests-and-limits)
的命名空间内创建一个 Pod，并且这个 Pod 中任何容器都没有声明自己的 CPU 限制，
那么{{< glossary_tooltip text="控制面" term_id="control-plane" >}}会为容器设定默认的 CPU 限制。

Kubernetes 在一些特定情况还可以设置默认的 CPU 请求，本文后续章节将会对其进行解释。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

在你的集群里你必须要有创建命名空间的权限。

如果你还不熟悉 Kubernetes 中 1.0 CPU 的含义，
请阅读 [CPU 的含义](/zh-cn/docs/concepts/configuration/manage-resources-containers/#meaning-of-cpu)。


## 创建命名空间

创建一个命名空间，以便本练习中创建的资源和集群的其余部分相隔离。

```shell
kubectl create namespace default-cpu-example
```

## 创建 LimitRange 和 Pod

以下为 {{< glossary_tooltip text="LimitRange" term_id="limitrange" >}} 的示例清单。
清单中声明了默认 CPU 请求和默认 CPU 限制。

{{< codenew file="admin/resource/cpu-defaults.yaml" >}}

在命名空间 default-cpu-example 中创建 LimitRange 对象：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-defaults.yaml --namespace=default-cpu-example
```

现在如果你在 default-cpu-example 命名空间中创建一个 Pod，
并且该 Pod 中所有容器都没有声明自己的 CPU 请求和 CPU 限制，
控制面会将 CPU 的默认请求值 0.5 和默认限制值 1 应用到 Pod 上。

以下为只包含一个容器的 Pod 的清单。该容器没有声明 CPU 请求和限制。

{{< codenew file="admin/resource/cpu-defaults-pod.yaml" >}}

创建 Pod。

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-defaults-pod.yaml --namespace=default-cpu-example
```

查看该 Pod 的声明：

```shell
kubectl get pod default-cpu-demo --output=yaml --namespace=default-cpu-example
```

输出显示该 Pod 的唯一的容器有 500m `cpu` 的 CPU 请求和 1 `cpu` 的 CPU 限制。
这些是 LimitRange 声明的默认值。

```shell
containers:
- image: nginx
  imagePullPolicy: Always
  name: default-cpu-demo-ctr
  resources:
    limits:
      cpu: "1"
    requests:
      cpu: 500m
```

## 你只声明容器的限制，而不声明请求会怎么样？

以下为只包含一个容器的 Pod 的清单。该容器声明了 CPU 限制，而没有声明 CPU 请求。

{{< codenew file="admin/resource/cpu-defaults-pod-2.yaml" >}}

创建 Pod

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-defaults-pod-2.yaml --namespace=default-cpu-example
```

查看你所创建的 Pod 的[规约](/zh-cn/docs/concepts/overview/working-with-objects/#object-spec-and-status)：

```
kubectl get pod default-cpu-demo-2 --output=yaml --namespace=default-cpu-example
```

输出显示该容器的 CPU 请求和 CPU 限制设置相同。注意该容器没有被指定默认的 CPU 请求值 0.5 `cpu`：

```
resources:
  limits:
    cpu: "1"
  requests:
    cpu: "1"
```

## 你只声明容器的请求，而不声明它的限制会怎么样？

这里给出了包含一个容器的 Pod 的示例清单。该容器声明了 CPU 请求，而没有声明 CPU 限制。

{{< codenew file="admin/resource/cpu-defaults-pod-3.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-defaults-pod-3.yaml --namespace=default-cpu-example
```

查看你所创建的 Pod 的规约：

```
kubectl get pod default-cpu-demo-3 --output=yaml --namespace=default-cpu-example
```

输出显示你所创建的 Pod 中，容器的 CPU 请求为 Pod 清单中声明的值。
然而同一容器的 CPU 限制被设置为 1 `cpu`，此值是该命名空间的默认 CPU 限制值。

```
resources:
  limits:
    cpu: "1"
  requests:
    cpu: 750m
```

## 默认 CPU 限制和请求的动机

如果你的命名空间设置了 CPU {{< glossary_tooltip text="资源配额" term_id="resource-quota" >}}，
为 CPU 限制设置一个默认值会很有帮助。
以下是 CPU 资源配额对命名空间的施加的两条限制：

* 命名空间中运行的每个 Pod 中的容器都必须有 CPU 限制。

* CPU 限制用来在 Pod 被调度到的节点上执行资源预留。

预留给命名空间中所有 Pod 使用的 CPU 总量不能超过规定的限制。

当你添加 LimitRange 时：

如果该命名空间中的任何 Pod 的容器未指定 CPU 限制，
控制面将默认 CPU 限制应用于该容器，
这样 Pod 可以在受到 CPU ResourceQuota 限制的命名空间中运行。

## 清理

删除你的命名空间：

```shell
kubectl delete namespace default-cpu-example
```

## {{% heading "whatsnext" %}}

### 集群管理员参考

* [为命名空间配置默认内存请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)
* [为命名空间配置内存限制的最小值和最大值](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/)
* [为命名空间配置 CPU 限制的最小值和最大值](/zh-cn/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/)
* [为命名空间配置内存和 CPU 配额](/zh-cn/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)
* [为命名空间配置 Pod 配额](/zh-cn/docs/tasks/administer-cluster/manage-resources/quota-pod-namespace/)
* [为 API 对象配置配额](/zh-cn/docs/tasks/administer-cluster/quota-api-object/)

### 应用开发者参考

* [为容器和 Pod 分配内存资源](/zh-cn/docs/tasks/configure-pod-container/assign-memory-resource/)
* [为容器和 Pod 分配 CPU 资源](/zh-cn/docs/tasks/configure-pod-container/assign-cpu-resource/)
* [为 Pod 配置服务质量](/zh-cn/docs/tasks/configure-pod-container/quality-service-pod/)
