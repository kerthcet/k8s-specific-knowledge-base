---
title: 为命名空间配置内存和 CPU 配额
content_type: task
weight: 50
description: >-
  为命名空间定义总的 CPU 和内存资源限制。
---



本文介绍如何为{{< glossary_tooltip text="命名空间" term_id="namespace" >}}下运行的所有
Pod 设置总的内存和 CPU 配额。你可以通过使用 [ResourceQuota](/zh-cn/docs/reference/kubernetes-api/policy-resources/resource-quota-v1/)
对象设置配额.

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

在你的集群里你必须要有创建命名空间的权限。

集群中每个节点至少有 1 GiB 的内存。


## 创建命名空间

创建一个命名空间，以便本练习中创建的资源和集群的其余部分相隔离。

```shell
kubectl create namespace quota-mem-cpu-example
```

## 创建 ResourceQuota

下面是 ResourceQuota 的示例清单：

{{< codenew file="admin/resource/quota-mem-cpu.yaml" >}}

创建 ResourceQuota：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/quota-mem-cpu.yaml --namespace=quota-mem-cpu-example
```

查看 ResourceQuota 详情：

```shell
kubectl get resourcequota mem-cpu-demo --namespace=quota-mem-cpu-example --output=yaml
```

ResourceQuota 在 quota-mem-cpu-example 命名空间中设置了如下要求：

* 在该命名空间中的每个 Pod 的所有容器都必须要有内存请求和限制，以及 CPU 请求和限制。
* 在该命名空间中所有 Pod 的内存请求总和不能超过 1 GiB。
* 在该命名空间中所有 Pod 的内存限制总和不能超过 2 GiB。
* 在该命名空间中所有 Pod 的 CPU 请求总和不能超过 1 cpu。
* 在该命名空间中所有 Pod 的 CPU 限制总和不能超过 2 cpu。

请阅读 [CPU 的含义](/zh-cn/docs/concepts/configuration/manage-resources-containers/#meaning-of-cpu)
理解 "1 CPU" 在 Kubernetes 中的含义。
## 创建 Pod

以下是 Pod 的示例清单：

{{< codenew file="admin/resource/quota-mem-cpu-pod.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/quota-mem-cpu-pod.yaml --namespace=quota-mem-cpu-example
```

确认 Pod 正在运行，并且其容器处于健康状态：

```shell
kubectl get pod quota-mem-cpu-demo --namespace=quota-mem-cpu-example
```

再查看 ResourceQuota 的详情：

```shell
kubectl get resourcequota mem-cpu-demo --namespace=quota-mem-cpu-example --output=yaml
```

输出结果显示了配额以及有多少配额已经被使用。你可以看到 Pod 的内存和 CPU 请求值及限制值没有超过配额。

```
status:
  hard:
    limits.cpu: "2"
    limits.memory: 2Gi
    requests.cpu: "1"
    requests.memory: 1Gi
  used:
    limits.cpu: 800m
    limits.memory: 800Mi
    requests.cpu: 400m
    requests.memory: 600Mi
```

如果有 `jq` 工具的话，你可以通过（使用 [JSONPath](/zh-cn/docs/reference/kubectl/jsonpath/)）
直接查询 `used` 字段的值，并且输出整齐的 JSON 格式。

```shell
kubectl get resourcequota mem-cpu-demo --namespace=quota-mem-cpu-example -o jsonpath='{ .status.used }' | jq .
```

## 尝试创建第二个 Pod

以下为第二个 Pod 的清单：

{{< codenew file="admin/resource/quota-mem-cpu-pod-2.yaml" >}}


在清单中，你可以看到 Pod 的内存请求为 700 MiB。
请注意新的内存请求与已经使用的内存请求之和超过了内存请求的配额：
600 MiB + 700 MiB > 1 GiB。

尝试创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/quota-mem-cpu-pod-2.yaml --namespace=quota-mem-cpu-example
```

第二个 Pod 不能被创建成功。输出结果显示创建第二个 Pod 会导致内存请求总量超过内存请求配额。

```
Error from server (Forbidden): error when creating "examples/admin/resource/quota-mem-cpu-pod-2.yaml":
pods "quota-mem-cpu-demo-2" is forbidden: exceeded quota: mem-cpu-demo,
requested: requests.memory=700Mi,used: requests.memory=600Mi, limited: requests.memory=1Gi
```

## 讨论

如你在本练习中所见，你可以用 ResourceQuota 限制命名空间中所有 Pod 的内存请求总量。
同样你也可以限制内存限制总量、CPU 请求总量、CPU 限制总量。

除了可以管理命名空间资源使用的总和，如果你想限制单个 Pod，或者限制这些 Pod 中的容器资源，
可以使用 [LimitRange](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/)
实现这类的功能。

## 清理

删除你的命名空间：

```shell
kubectl delete namespace quota-mem-cpu-example
```

## {{% heading "whatsnext" %}}

### 集群管理员参考

* [为命名空间配置默认内存请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)
* [为命名空间配置默认 CPU 请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/)
* [为命名空间配置内存限制的最小值和最大值](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/)
* [为命名空间配置 CPU 限制的最小值和最大值](/zh-cn/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/)
* [为命名空间配置 Pod 配额](/zh-cn/docs/tasks/administer-cluster/manage-resources/quota-pod-namespace/)
* [为 API 对象配置配额](/zh-cn/docs/tasks/administer-cluster/quota-api-object/)

### 应用开发者参考

* [为容器和 Pod 分配内存资源](/zh-cn/docs/tasks/configure-pod-container/assign-memory-resource/)
* [为容器和 Pod 分配 CPU 资源](/zh-cn/docs/tasks/configure-pod-container/assign-cpu-resource/)
* [为 Pod 配置服务质量](/zh-cn/docs/tasks/configure-pod-container/quality-service-pod/)

