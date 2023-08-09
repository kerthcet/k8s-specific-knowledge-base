---
title: 容器生命周期回调
content_type: concept
weight: 40
---


这个页面描述了 kubelet 管理的容器如何使用容器生命周期回调框架，
藉由其管理生命周期中的事件触发，运行指定代码。


## 概述

类似于许多具有生命周期回调组件的编程语言框架，例如 Angular、Kubernetes 为容器提供了生命周期回调。
回调使容器能够了解其管理生命周期中的事件，并在执行相应的生命周期回调时运行在处理程序中实现的代码。

## 容器回调 {#container-hooks}

有两个回调暴露给容器：

`PostStart`

这个回调在容器被创建之后立即被执行。
但是，不能保证回调会在容器入口点（ENTRYPOINT）之前执行。
没有参数传递给处理程序。

`PreStop`

在容器因 API 请求或者管理事件（诸如存活态探针、启动探针失败、资源抢占、资源竞争等）
而被终止之前，此回调会被调用。
如果容器已经处于已终止或者已完成状态，则对 preStop 回调的调用将失败。
在用来停止容器的 TERM 信号被发出之前，回调必须执行结束。
Pod 的终止宽限周期在 `PreStop` 回调被执行之前即开始计数，
所以无论回调函数的执行结果如何，容器最终都会在 Pod 的终止宽限期内被终止。
没有参数会被传递给处理程序。

有关终止行为的更详细描述，请参见
[终止 Pod](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)。

### 回调处理程序的实现

容器可以通过实现和注册该回调的处理程序来访问该回调。
针对容器，有两种类型的回调处理程序可供实现：


* Exec - 在容器的 cgroups 和名字空间中执行特定的命令（例如 `pre-stop.sh`）。
  命令所消耗的资源计入容器的资源消耗。
* HTTP - 对容器上的特定端点执行 HTTP 请求。

### 回调处理程序执行

当调用容器生命周期管理回调时，Kubernetes 管理系统根据回调动作执行其处理程序，
`httpGet` 和 `tcpSocket` 在 kubelet 进程执行，而 `exec` 则由容器内执行。

回调处理程序调用在包含容器的 Pod 上下文中是同步的。
这意味着对于 `PostStart` 回调，容器入口点和回调异步触发。
但是，如果回调运行或挂起的时间太长，则容器无法达到 `running` 状态。

`PreStop` 回调并不会与停止容器的信号处理程序异步执行；回调必须在可以发送信号之前完成执行。
如果 `PreStop` 回调在执行期间停滞不前，Pod 的阶段会变成 `Terminating`并且一直处于该状态，
直到其 `terminationGracePeriodSeconds` 耗尽为止，这时 Pod 会被杀死。
这一宽限期是针对 `PreStop` 回调的执行时间及容器正常停止时间的总和而言的。
例如，如果 `terminationGracePeriodSeconds` 是 60，回调函数花了 55 秒钟完成执行，
而容器在收到信号之后花了 10 秒钟来正常结束，那么容器会在其能够正常结束之前即被杀死，
因为 `terminationGracePeriodSeconds` 的值小于后面两件事情所花费的总时间（55+10）。

如果 `PostStart` 或 `PreStop` 回调失败，它会杀死容器。

用户应该使他们的回调处理程序尽可能的轻量级。
但也需要考虑长时间运行的命令也很有用的情况，比如在停止容器之前保存状态。

### 回调递送保证

回调的递送应该是**至少一次**，这意味着对于任何给定的事件，
例如 `PostStart` 或 `PreStop`，回调可以被调用多次。
如何正确处理被多次调用的情况，是回调实现所要考虑的问题。

通常情况下，只会进行单次递送。
例如，如果 HTTP 回调接收器宕机，无法接收流量，则不会尝试重新发送。
然而，偶尔也会发生重复递送的可能。
例如，如果 kubelet 在发送回调的过程中重新启动，回调可能会在 kubelet 恢复后重新发送。

### 调试回调处理程序

回调处理程序的日志不会在 Pod 事件中公开。
如果处理程序由于某种原因失败，它将播放一个事件。
对于 `PostStart`，这是 `FailedPostStartHook` 事件，对于 `PreStop`，这是 `FailedPreStopHook` 事件。
要自己生成失败的 `FailedPostStartHook` 事件，请修改
[lifecycle-events.yaml](https://raw.githubusercontent.com/kubernetes/website/main/content/en/examples/pods/lifecycle-events.yaml)
文件将 postStart 命令更改为 “badcommand” 并应用它。
以下是通过运行 `kubectl describe pod lifecycle-demo` 后你看到的一些结果事件的示例输出：

```
Events:
  Type     Reason               Age              From               Message
  ----     ------               ----             ----               -------
  Normal   Scheduled            7s               default-scheduler  Successfully assigned default/lifecycle-demo to ip-XXX-XXX-XX-XX.us-east-2...
  Normal   Pulled               6s               kubelet            Successfully pulled image "nginx" in 229.604315ms
  Normal   Pulling              4s (x2 over 6s)  kubelet            Pulling image "nginx"
  Normal   Created              4s (x2 over 5s)  kubelet            Created container lifecycle-demo-container
  Normal   Started              4s (x2 over 5s)  kubelet            Started container lifecycle-demo-container
  Warning  FailedPostStartHook  4s (x2 over 5s)  kubelet            Exec lifecycle hook ([badcommand]) for Container "lifecycle-demo-container" in Pod "lifecycle-demo_default(30229739-9651-4e5a-9a32-a8f1688862db)" failed - error: command 'badcommand' exited with 126: , message: "OCI runtime exec failed: exec failed: container_linux.go:380: starting container process caused: exec: \"badcommand\": executable file not found in $PATH: unknown\r\n"
  Normal   Killing              4s (x2 over 5s)  kubelet            FailedPostStartHook
  Normal   Pulled               4s               kubelet            Successfully pulled image "nginx" in 215.66395ms
  Warning  BackOff              2s (x2 over 3s)  kubelet            Back-off restarting failed container
```

## {{% heading "whatsnext" %}}


* 进一步了解[容器环境](/zh-cn/docs/concepts/containers/container-environment/)。
* 动手[为容器的生命周期事件设置处理函数](/zh-cn/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/)。

