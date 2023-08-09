---
title: 调试 Init 容器
content_type: task
weight: 40
---



此页显示如何核查与 Init 容器执行相关的问题。
下面的示例命令行将 Pod 称为 `<pod-name>`，而 Init 容器称为 `<init-container-1>` 和
`<init-container-2>`。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


* 你应该熟悉 [Init 容器](/zh-cn/docs/concepts/workloads/pods/init-containers/)的基础知识。
* 你应该已经[配置好一个 Init 容器](/zh-cn/docs/tasks/configure-pod-container/configure-pod-initialization/#creating-a-pod-that-has-an-init-container/)。



## 检查 Init 容器的状态

显示你的 Pod 的状态：

```shell
kubectl get pod <pod-name>
```


例如，状态 `Init:1/2` 表明两个 Init 容器中的一个已经成功完成：

```
NAME         READY     STATUS     RESTARTS   AGE
<pod-name>   0/1       Init:1/2   0          7s
```

更多状态值及其含义请参考[理解 Pod 的状态](#understanding-pod-status)。

## 获取 Init 容器详情   {#getting-details-about-init-containers}

查看 Init 容器运行的更多详情：

```shell
kubectl describe pod <pod-name>
```

例如，对于包含两个 Init 容器的 Pod 可能显示如下信息：

```
Init Containers:
  <init-container-1>:
    Container ID:    ...
    ...
    State:           Terminated
      Reason:        Completed
      Exit Code:     0
      Started:       ...
      Finished:      ...
    Ready:           True
    Restart Count:   0
    ...
  <init-container-2>:
    Container ID:    ...
    ...
    State:           Waiting
      Reason:        CrashLoopBackOff
    Last State:      Terminated
      Reason:        Error
      Exit Code:     1
      Started:       ...
      Finished:      ...
    Ready:           False
    Restart Count:   3
    ...
```

你还可以通过编程方式读取 Pod Spec 上的 `status.initContainerStatuses` 字段，了解 Init 容器的状态：

```shell
kubectl get pod nginx --template '{{.status.initContainerStatuses}}'
```

此命令将返回与原始 JSON 中相同的信息.

## 通过 Init 容器访问日志   {#accessing-logs-from-init-containers}

与 Pod 名称一起传递 Init 容器名称，以访问容器的日志。

```shell
kubectl logs <pod-name> -c <init-container-2>
```

运行 Shell 脚本的 Init 容器在执行 Shell 脚本时输出命令本身。
例如，你可以在 Bash 中通过在脚本的开头运行 `set -x` 来实现。


## 理解 Pod 的状态   {#understanding-pod-status}

以 `Init:` 开头的 Pod 状态汇总了 Init 容器执行的状态。
下表介绍调试 Init 容器时可能看到的一些状态值示例。


状态   | 含义
------ | -------
`Init:N/M` | Pod 包含 `M` 个 Init 容器，其中 `N` 个已经运行完成。
`Init:Error` | Init 容器已执行失败。
`Init:CrashLoopBackOff` | Init 容器执行总是失败。
`Pending` | Pod 还没有开始执行 Init 容器。
`PodInitializing` or `Running` | Pod 已经完成执行 Init 容器。

