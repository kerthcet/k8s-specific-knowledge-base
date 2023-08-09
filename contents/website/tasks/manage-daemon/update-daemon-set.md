---
title: 对 DaemonSet 执行滚动更新
content_type: task
weight: 10
---



本文介绍了如何对 DaemonSet 执行滚动更新。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}


## DaemonSet 更新策略    {#daemonset-update-strategy}

DaemonSet 有两种更新策略：


* `OnDelete`: 使用 `OnDelete` 更新策略时，在更新 DaemonSet 模板后，只有当你手动删除老的
  DaemonSet pods 之后，新的 DaemonSet Pod **才会**被自动创建。跟 Kubernetes 1.6 以前的版本类似。
* `RollingUpdate`: 这是默认的更新策略。使用 `RollingUpdate` 更新策略时，在更新 DaemonSet 模板后，
  老的 DaemonSet Pod 将被终止，并且将以受控方式自动创建新的 DaemonSet Pod。
  更新期间，最多只能有 DaemonSet 的一个 Pod 运行于每个节点上。

## 执行滚动更新    {#performing-a-rolling-update}

要启用 DaemonSet 的滚动更新功能，必须设置 `.spec.updateStrategy.type` 为 `RollingUpdate`。

你可能想设置
[`.spec.updateStrategy.rollingUpdate.maxUnavailable`](/zh-cn/docs/reference/kubernetes-api/workload-resources/daemon-set-v1/#DaemonSetSpec) (默认为 1)，
[`.spec.minReadySeconds`](/zh-cn/docs/reference/kubernetes-api/workload-resources/daemon-set-v1/#DaemonSetSpec) (默认为 0) 和
[`.spec.updateStrategy.rollingUpdate.maxSurge`](/zh-cn/docs/reference/kubernetes-api/workload-resources/daemon-set-v1/#DaemonSetSpec)
（默认为 0）。

### 创建带有 `RollingUpdate` 更新策略的 DaemonSet    {#creating-a-daemonset-with-rollingupdate-update-strategy}

下面的 YAML 包含一个 DaemonSet，其更新策略为 'RollingUpdate'：

{{< codenew file="controllers/fluentd-daemonset.yaml" >}}

检查了 DaemonSet 清单中更新策略的设置之后，创建 DaemonSet：

```shell
kubectl create -f https://k8s.io/examples/controllers/fluentd-daemonset.yaml
```

另一种方式是如果你希望使用 `kubectl apply` 来更新 DaemonSet 的话，
也可以使用 `kubectl apply` 来创建 DaemonSet：

```shell
kubectl apply -f https://k8s.io/examples/controllers/fluentd-daemonset.yaml
```

### 检查 DaemonSet 的滚动更新策略    {#checking-daemonset-rollingupdate-update-strategy}

首先，检查 DaemonSet 的更新策略，确保已经将其设置为 `RollingUpdate`:

```shell
kubectl get ds/fluentd-elasticsearch -o go-template='{{.spec.updateStrategy.type}}{{"\n"}}' -n kube-system
```

如果还没在系统中创建 DaemonSet，请使用以下命令检查 DaemonSet 的清单：

```shell
kubectl apply -f https://k8s.io/examples/controllers/fluentd-daemonset.yaml --dry-run=client -o go-template='{{.spec.updateStrategy.type}}{{"\n"}}'
```

两个命令的输出都应该为：

```
RollingUpdate
```

如果输出不是 `RollingUpdate`，请返回并相应地修改 DaemonSet 对象或者清单。

### 更新 DaemonSet 模板    {#updating-a-daemonset-template}

对 `RollingUpdate` DaemonSet 的 `.spec.template` 的任何更新都将触发滚动更新。
这可以通过几个不同的 `kubectl` 命令来完成。

{{< codenew file="controllers/fluentd-daemonset-update.yaml" >}}

#### 声明式命令    {#declarative-commands}

如果你使用[配置文件](/zh-cn/docs/tasks/manage-kubernetes-objects/declarative-config/)来更新
DaemonSet，请使用 `kubectl apply`：

```shell
kubectl apply -f https://k8s.io/examples/controllers/fluentd-daemonset-update.yaml
```

#### 指令式命令    {#imperative-commands}

如果你使用[指令式命令](/zh-cn/docs/tasks/manage-kubernetes-objects/imperative-command/)来更新
DaemonSets，请使用 `kubectl edit`：

```shell
kubectl edit ds/fluentd-elasticsearch -n kube-system
```

##### 只更新容器镜像    {#updating-only-the-container-image}

如果你只需要更新 DaemonSet 模板里的容器镜像，比如 `.spec.template.spec.containers[*].image`，
请使用 `kubectl set image`：

```shell
kubectl set image ds/fluentd-elasticsearch fluentd-elasticsearch=quay.io/fluentd_elasticsearch/fluentd:v2.6.0 -n kube-system
```

### 监视滚动更新状态    {#watching-the-rolling-update-status}

最后，观察 DaemonSet 最新滚动更新的进度：

```shell
kubectl rollout status ds/fluentd-elasticsearch -n kube-system
```

当滚动更新完成时，输出结果如下：

```shell
daemonset "fluentd-elasticsearch" successfully rolled out
```

## 故障排查    {#troubleshooting}

### DaemonSet 滚动更新卡住    {#daemonset-rolling-update-is-stuck}

有时，DaemonSet 滚动更新可能卡住，以下是一些可能的原因：

#### 一些节点可用资源耗尽    {#some-nodes-run-out-of-resources}

DaemonSet 滚动更新可能会卡住，其 Pod 至少在某个节点上无法调度运行。
当节点上[可用资源耗尽](/zh-cn/docs/concepts/scheduling-eviction/node-pressure-eviction/)时，
这是可能的。

发生这种情况时，通过对 `kubectl get nodes` 和下面命令行的输出作比较，
找出没有调度 DaemonSet Pod 的节点：

```shell
kubectl get pods -l name=fluentd-elasticsearch -o wide -n kube-system
```

一旦找到这些节点，从节点上删除一些非 DaemonSet Pod，为新的 DaemonSet Pod 腾出空间。

{{< note >}}
当所删除的 Pod 不受任何控制器管理，也不是多副本的 Pod时，上述操作将导致服务中断。
同时，上述操作也不会考虑
[PodDisruptionBudget](/zh-cn/docs/tasks/run-application/configure-pdb/)
所施加的约束。
{{< /note >}}

#### 不完整的滚动更新    {#broken-rollout}

如果最近的 DaemonSet 模板更新被破坏了，比如，容器处于崩溃循环状态或者容器镜像不存在
（通常由于拼写错误），就会发生 DaemonSet 滚动更新中断。

要解决此问题，需再次更新 DaemonSet 模板。新的滚动更新不会被以前的不健康的滚动更新阻止。

#### 时钟偏差    {#clock-skew}

如果在 DaemonSet 中指定了 `.spec.minReadySeconds`，主控节点和工作节点之间的时钟偏差会使
DaemonSet 无法检测到正确的滚动更新进度。

## 清理    {#clean-up}

从名字空间中删除 DaemonSet：

```shell
kubectl delete ds fluentd-elasticsearch -n kube-system
```

## {{% heading "whatsnext" %}}

* 查看[在 DaemonSet 上执行回滚](/zh-cn/docs/tasks/manage-daemon/rollback-daemon-set/)
* 查看[创建 DaemonSet 以收养现有 DaemonSet Pod](/zh-cn/docs/concepts/workloads/controllers/daemonset/)

