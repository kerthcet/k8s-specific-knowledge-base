---
title: 配置 Pod 的服务质量
content_type: task
weight: 60
---



本页介绍怎样配置 Pod 以让其归属于特定的
{{< glossary_tooltip text="服务质量类（Quality of Service class，QoS class）" term_id="qos-class" >}}.
Kubernetes 在 Node 资源不足时使用 QoS 类来就驱逐 Pod 作出决定。

Kubernetes 创建 Pod 时，会将如下 QoS 类之一设置到 Pod 上：

* [Guaranteed](/zh-cn/docs/concepts/workloads/pods/pod-qos/#guaranteed)
* [Burstable](/zh-cn/docs/concepts/workloads/pods/pod-qos/#burstable)
* [BestEffort](/zh-cn/docs/concepts/workloads/pods/pod-qos/#besteffort)

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

你还需要能够创建和删除名字空间。


## 创建名字空间  {#create-a-namespace}

创建一个名字空间，以便将本练习所创建的资源与集群的其余资源相隔离。

```shell
kubectl create namespace qos-example
```

## 创建一个 QoS 类为 Guaranteed 的 Pod  {#create-a-pod-that-gets-assigned-a-qos-class-of-guaranteed}

对于 QoS 类为 `Guaranteed` 的 Pod：

* Pod 中的每个容器都必须指定内存限制和内存请求。
* 对于 Pod 中的每个容器，内存限制必须等于内存请求。
* Pod 中的每个容器都必须指定 CPU 限制和 CPU 请求。
* 对于 Pod 中的每个容器，CPU 限制必须等于 CPU 请求。


这些限制同样适用于初始化容器和应用程序容器。
[临时容器（Ephemeral Container）](/zh-cn/docs/concepts/workloads/pods/ephemeral-containers/)
无法定义资源，因此不受这些约束限制。

下面是包含一个 Container 的 Pod 清单。该 Container 设置了内存请求和内存限制，值都是 200 MiB。
该 Container 设置了 CPU 请求和 CPU 限制，值都是 700 milliCPU：

{{< codenew file="pods/qos/qos-pod.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/qos/qos-pod.yaml --namespace=qos-example
```

查看 Pod 详情：

```shell
kubectl get pod qos-demo --namespace=qos-example --output=yaml
```

结果表明 Kubernetes 为 Pod 配置的 QoS 类为 `Guaranteed`。
结果也确认了 Pod 容器设置了与内存限制匹配的内存请求，设置了与 CPU 限制匹配的 CPU 请求。

```yaml
spec:
  containers:
    ...
    resources:
      limits:
        cpu: 700m
        memory: 200Mi
      requests:
        cpu: 700m
        memory: 200Mi
    ...
status:
  qosClass: Guaranteed
```

{{< note >}}
如果某 Container 指定了自己的内存限制，但没有指定内存请求，Kubernetes
会自动为它指定与内存限制相等的内存请求。同样，如果容器指定了自己的 CPU 限制，
但没有指定 CPU 请求，Kubernetes 会自动为它指定与 CPU 限制相等的 CPU 请求。
{{< /note >}}

#### 清理 {#clean-up-guaranteed}

删除 Pod：

```shell
kubectl delete pod qos-demo --namespace=qos-example
```

## 创建一个 QoS 类为 Burstable 的 Pod  {#create-a-pod-that-gets-assigned-a-qos-class-of-burstable}

如果满足下面条件，Kubernetes 将会指定 Pod 的 QoS 类为 `Burstable`：

* Pod 不符合 `Guaranteed` QoS 类的标准。
* Pod 中至少一个 Container 具有内存或 CPU 的请求或限制。

下面是包含一个 Container 的 Pod 清单。该 Container 设置的内存限制为 200 MiB，
内存请求为 100 MiB。

{{< codenew file="pods/qos/qos-pod-2.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/qos/qos-pod-2.yaml --namespace=qos-example
```

查看 Pod 详情：

```shell
kubectl get pod qos-demo-2 --namespace=qos-example --output=yaml
```

结果表明 Kubernetes 为 Pod 配置的 QoS 类为 `Burstable`。

```yaml
spec:
  containers:
  - image: nginx
    imagePullPolicy: Always
    name: qos-demo-2-ctr
    resources:
      limits:
        memory: 200Mi
      requests:
        memory: 100Mi
  ...
status:
  qosClass: Burstable
```

#### 清理  {#clean-up-burstable}

删除 Pod：

```shell
kubectl delete pod qos-demo-2 --namespace=qos-example
```

## 创建一个 QoS 类为 BestEffort 的 Pod  {#create-a-pod-that-gets-assigned-a-qos-class-of-besteffort}

对于 QoS 类为 `BestEffort` 的 Pod，Pod 中的 Container 必须没有设置内存和 CPU 限制或请求。

下面是包含一个 Container 的 Pod 清单。该 Container 没有设置内存和 CPU 限制或请求。

{{< codenew file="pods/qos/qos-pod-3.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/qos/qos-pod-3.yaml --namespace=qos-example
```

查看 Pod 详情：

```shell
kubectl get pod qos-demo-3 --namespace=qos-example --output=yaml
```

结果表明 Kubernetes 为 Pod 配置的 QoS 类为 `BestEffort`。

```yaml
spec:
  containers:
    ...
    resources: {}
  ...
status:
  qosClass: BestEffort
```

#### 清理   {#clean-up-besteffort}

删除 Pod：

```shell
kubectl delete pod qos-demo-3 --namespace=qos-example
```

## 创建包含两个容器的 Pod  {#create-a-pod-that-has-two-containers}

下面是包含两个 Container 的 Pod 清单。一个 Container 指定内存请求为 200 MiB。
另外一个 Container 没有指定任何请求或限制。

{{< codenew file="pods/qos/qos-pod-4.yaml" >}}

注意此 Pod 满足 `Burstable` QoS 类的标准。也就是说它不满足 `Guaranteed` QoS 类标准，
因为它的 Container 之一设有内存请求。

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/qos/qos-pod-4.yaml --namespace=qos-example
```

查看 Pod 详情：

```shell
kubectl get pod qos-demo-4 --namespace=qos-example --output=yaml
```

结果表明 Kubernetes 为 Pod 配置的 QoS 类为 `Burstable`：

```yaml
spec:
  containers:
    ...
    name: qos-demo-4-ctr-1
    resources:
      requests:
        memory: 200Mi
    ...
    name: qos-demo-4-ctr-2
    resources: {}
    ...
status:
  qosClass: Burstable
```

## 检视 Pod 的 QoS 类  {#retrieve-the-qos-class-for-a-pod}

你也可以只查看你所需要的字段，而不是查看所有字段：

```bash
kubectl --namespace=qos-example get pod qos-demo-4 -o jsonpath='{ .status.qosClass}{"\n"}'
```

```none
Burstable
```

## 环境清理  {#clean-up}

删除名字空间：

```shell
kubectl delete namespace qos-example
```

## {{% heading "whatsnext" %}}

### 应用开发者参考

* [为 Pod 和容器分配内存资源](/zh-cn/docs/tasks/configure-pod-container/assign-memory-resource/)
* [为 Pod 和容器分配 CPU 资源](/zh-cn/docs/tasks/configure-pod-container/assign-cpu-resource/)

### 集群管理员参考

* [为名字空间配置默认的内存请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)
* [为名字空间配置默认的 CPU 请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/)
* [为名字空间配置最小和最大内存限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/)
* [为名字空间配置最小和最大 CPU 限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/)
* [为名字空间配置内存和 CPU 配额](/zh-cn/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)
* [为名字空间配置 Pod 配额](/zh-cn/docs/tasks/administer-cluster/manage-resources/quota-pod-namespace/)
* [为 API 对象配置配额](/zh-cn/docs/tasks/administer-cluster/quota-api-object/)
* [控制节点上的拓扑管理策略](/zh-cn/docs/tasks/administer-cluster/topology-manager/)
