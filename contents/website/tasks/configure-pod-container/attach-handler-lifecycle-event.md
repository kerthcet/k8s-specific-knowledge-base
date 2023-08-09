---
title: 为容器的生命周期事件设置处理函数
content_type: task
weight: 180
---


这个页面将演示如何为容器的生命周期事件挂接处理函数。Kubernetes 支持 postStart 和 preStop 事件。
当一个容器启动后，Kubernetes 将立即发送 postStart 事件；在容器被终结之前，
Kubernetes 将发送一个 preStop 事件。容器可以为每个事件指定一个处理程序。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


## 定义 postStart 和 preStop 处理函数  {#define-poststart-and-prestop-handlers}

在本练习中，你将创建一个包含一个容器的 Pod，该容器为 postStart 和 preStop 事件提供对应的处理函数。

下面是对应 Pod 的配置文件：

{{< codenew file="pods/lifecycle-events.yaml" >}}

在上述配置文件中，你可以看到 postStart 命令在容器的 `/usr/share` 目录下写入文件 `message`。
命令 preStop 负责优雅地终止 nginx 服务。当因为失效而导致容器终止时，这一处理方式很有用。

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/lifecycle-events.yaml
```

验证 Pod 中的容器已经运行：

```shell
kubectl get pod lifecycle-demo
```

使用 shell 连接到你的 Pod 里的容器：

```shell
kubectl exec -it lifecycle-demo -- /bin/bash
```

在 shell 中，验证 `postStart` 处理函数创建了 `message` 文件：

```
root@lifecycle-demo:/# cat /usr/share/message
```

命令行输出的是 `postStart` 处理函数所写入的文本：

```
Hello from the postStart handler
```


## 讨论  {#discussion}

Kubernetes 在容器创建后立即发送 postStart 事件。
然而，postStart 处理函数的调用不保证早于容器的入口点（entrypoint）
的执行。postStart 处理函数与容器的代码是异步执行的，但 Kubernetes
的容器管理逻辑会一直阻塞等待 postStart 处理函数执行完毕。
只有 postStart 处理函数执行完毕，容器的状态才会变成
RUNNING。

Kubernetes 在容器结束前立即发送 preStop 事件。除非 Pod 宽限期限超时，
Kubernetes 的容器管理逻辑会一直阻塞等待 preStop 处理函数执行完毕。
更多细节请参阅 [Pod 的生命周期](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/)。

{{< note >}}
Kubernetes 只有在一个 Pod 或该 Pod 中的容器**结束（Terminated）** 的时候才会发送 preStop 事件，
这意味着在 Pod **完成（Completed）** 时
preStop 的事件处理逻辑不会被触发。有关这个限制，
请参阅[容器回调](/zh-cn/docs/concepts/containers/container-lifecycle-hooks/#container-hooks)了解详情。
{{< /note >}}

## {{% heading "whatsnext" %}}

* 进一步了解[容器生命周期回调](/zh-cn/docs/concepts/containers/container-lifecycle-hooks/)。
* 进一步了解 [Pod 的生命周期](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/)。

### 参考

* [Lifecycle](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#lifecycle-v1-core)
* [Container](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#container-v1-core)
* 参阅 [PodSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core) 中关于 `terminationGracePeriodSeconds` 的部分

