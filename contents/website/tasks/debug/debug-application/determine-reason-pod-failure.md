---
title: 确定 Pod 失败的原因
content_type: task
weight: 30
---


本文介绍如何编写和读取容器的终止消息。

终止消息为容器提供了一种方法，可以将有关致命事件的信息写入某个位置，
在该位置可以通过仪表板和监控软件等工具轻松检索和显示致命事件。
在大多数情况下，你放入终止消息中的信息也应该写入
[常规 Kubernetes 日志](/zh-cn/docs/concepts/cluster-administration/logging/)。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}


## 读写终止消息   {#writing-and-reading-a-termination-message}

在本练习中，你将创建运行一个容器的 Pod。
配置文件指定在容器启动时要运行的命令。

{{< codenew file="debug/termination.yaml" >}}

1. 基于 YAML 配置文件创建 Pod：

   ```shell
   kubectl apply -f https://k8s.io/examples/debug/termination.yaml   
   ```

   YAML 文件中，在 `command` 和 `args` 字段，你可以看到容器休眠 10 秒然后将 "Sleep expired"
   写入 `/dev/termination-log` 文件。
   容器写完 "Sleep expired" 消息后就终止了。

2. 显示 Pod 的信息：

   ```shell
   kubectl get pod termination-demo
   ```

   重复前面的命令直到 Pod 不再运行。

3. 显示 Pod 的详细信息：

   ```shell
   kubectl get pod termination-demo --output=yaml
   ```

   输出结果包含 "Sleep expired" 消息：

   ```yaml
   apiVersion: v1
   kind: Pod
   ...
       lastState:
         terminated:
           containerID: ...
           exitCode: 0
           finishedAt: ...
           message: |
             Sleep expired
           ...
   ```

4. 使用 Go 模板过滤输出结果，使其只含有终止消息：

   ```shell
   kubectl get pod termination-demo -o go-template="{{range .status.containerStatuses}}{{.lastState.terminated.message}}{{end}}"
   ```

   如果你正在运行多容器 Pod，则可以使用 Go 模板来包含容器的名称。这样，你可以发现哪些容器出现故障：

   ```shell
   kubectl get pod multi-container-pod -o go-template='{{range .status.containerStatuses}}{{printf "%s:\n%s\n\n" .name .lastState.terminated.message}}{{end}}'
   ```

## 定制终止消息   {#customizing-the-termination-message}

Kubernetes 从容器的 `terminationMessagePath` 字段中指定的终止消息文件中检索终止消息，
默认值为 `/dev/termination-log`。
通过定制这个字段，你可以告诉 Kubernetes 使用不同的文件。
Kubernetes 使用指定文件中的内容在成功和失败时填充容器的状态消息。

终止消息旨在简要说明最终状态，例如断言失败消息。
kubelet 会截断长度超过 4096 字节的消息。

所有容器的总消息长度限制为 12KiB，将会在每个容器之间平均分配。
例如，如果有 12 个容器（`initContainers` 或 `containers`），
每个容器都有 1024 字节的可用终止消息空间。

默认的终止消息路径是 `/dev/termination-log`。
Pod 启动后不能设置终止消息路径。

在下例中，容器将终止消息写入 `/tmp/my-log` 给 Kubernetes 来检索：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: msg-path-demo
spec:
  containers:
  - name: msg-path-demo-container
    image: debian
    terminationMessagePath: "/tmp/my-log"
```

此外，用户可以设置容器的 `terminationMessagePolicy` 字段，以便进一步自定义。
此字段默认为 "`File`"，这意味着仅从终止消息文件中检索终止消息。
通过将 `terminationMessagePolicy` 设置为 "`FallbackToLogsOnError`"，你就可以告诉 Kubernetes，在容器因错误退出时，如果终止消息文件为空，则使用容器日志输出的最后一块作为终止消息。
日志输出限制为 2048 字节或 80 行，以较小者为准。

## {{% heading "whatsnext" %}}


* 参考 [Container](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#container-v1-core)
  资源的 `terminationMessagePath` 字段。
* 了解[检索日志](/zh-cn/docs/concepts/cluster-administration/logging/)。
* 了解 [Go 模板](https://pkg.go.dev/text/template)。

