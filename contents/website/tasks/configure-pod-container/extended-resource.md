---
title: 为容器分派扩展资源 
content_type: task
weight: 70
---



{{< feature-state state="stable" >}}

本文介绍如何为容器指定扩展资源。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

在你开始此练习前，请先练习
[为节点广播扩展资源](/zh-cn/docs/tasks/administer-cluster/extended-resource-node/)。
在那个练习中将配置你的一个节点来广播 dongle 资源。


## 给 Pod 分派扩展资源

要请求扩展资源，需要在你的容器清单中包括 `resources:requests` 字段。
扩展资源可以使用任何完全限定名称，只是不能使用 `*.kubernetes.io/`。
有效的扩展资源名的格式为 `example.com/foo`，其中 `example.com` 应被替换为
你的组织的域名，而 `foo` 则是描述性的资源名称。

下面是包含一个容器的 Pod 配置文件：

{{< codenew file="pods/resource/extended-resource-pod.yaml" >}}

在配置文件中，你可以看到容器请求了 3 个 dongles。

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/resource/extended-resource-pod.yaml
```

检查 Pod 是否运行正常：

```shell
kubectl get pod extended-resource-demo
```

描述 Pod:

```shell
kubectl describe pod extended-resource-demo
```

输出结果显示 dongle 请求如下：

```yaml
Limits:
  example.com/dongle: 3
Requests:
  example.com/dongle: 3
```

## 尝试创建第二个 Pod

下面是包含一个容器的 Pod 配置文件，容器请求了 2 个 dongles。

{{< codenew file="pods/resource/extended-resource-pod-2.yaml" >}}

Kubernetes 将不能满足 2 个 dongles 的请求，因为第一个 Pod 已经使用了 4 个可用 dongles 中的 3 个。

尝试创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/resource/extended-resource-pod-2.yaml
```

描述 Pod：

```shell
kubectl describe pod extended-resource-demo-2
```

输出结果表明 Pod 不能被调度，因为没有一个节点上存在两个可用的 dongles。

```
Conditions:
  Type    Status
  PodScheduled  False
...
Events:
  ...
  ... Warning   FailedScheduling  pod (extended-resource-demo-2) failed to fit in any node
fit failure summary on nodes : Insufficient example.com/dongle (1)
```

查看 Pod 的状态：

```shell
kubectl get pod extended-resource-demo-2
```

输出结果表明 Pod 虽然被创建了，但没有被调度到节点上正常运行。Pod 的状态为 Pending：

```yaml
NAME                       READY     STATUS    RESTARTS   AGE
extended-resource-demo-2   0/1       Pending   0          6m
```

## 清理

删除本练习中创建的 Pod：

```shell
kubectl delete pod extended-resource-demo
kubectl delete pod extended-resource-demo-2
```

## {{% heading "whatsnext" %}}

## 应用开发者参考

* [为容器和 Pod 分配内存资源](/zh-cn/docs/tasks/configure-pod-container/assign-memory-resource/)
* [为容器和 Pod 分配 CPU 资源](/zh-cn/docs/tasks/configure-pod-container/assign-cpu-resource/)

### 集群管理员参考

* [为节点广播扩展资源](/zh-cn/docs/tasks/administer-cluster/extended-resource-node/)

