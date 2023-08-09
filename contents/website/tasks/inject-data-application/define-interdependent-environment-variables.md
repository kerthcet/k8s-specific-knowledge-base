---
title: 定义相互依赖的环境变量
content_type: task
weight: 20
---


本页展示了如何为 Kubernetes Pod 中的容器定义相互依赖的环境变量。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}


## 为容器定义相互依赖的环境变量   {#define-an-environment-dependent-variable-for-a-container}

当创建一个 Pod 时，你可以为运行在 Pod 中的容器设置相互依赖的环境变量。
若要设置相互依赖的环境变量，你可以在配置清单文件的 `env` 的 `value` 中使用 $(VAR_NAME)。

在本练习中，你会创建一个单容器的 Pod。
此 Pod 的配置文件定义了一个已定义常用用法的相互依赖的环境变量。
下面是此 Pod 的配置清单：

{{< codenew file="pods/inject/dependent-envars.yaml" >}}

1. 依据清单创建 Pod：

   ```shell
   kubectl apply -f https://k8s.io/examples/pods/inject/dependent-envars.yaml
   ```
   ```
   pod/dependent-envars-demo created
   ```

2. 列出运行的 Pod：

   ```shell
   kubectl get pods dependent-envars-demo
   ```
   ```
   NAME                      READY     STATUS    RESTARTS   AGE
   dependent-envars-demo     1/1       Running   0          9s
   ```

3. 检查 Pod 中运行容器的日志：

   ```shell
   kubectl logs pod/dependent-envars-demo
   ```
   ```

   UNCHANGED_REFERENCE=$(PROTOCOL)://172.17.0.1:80
   SERVICE_ADDRESS=https://172.17.0.1:80
   ESCAPED_REFERENCE=$(PROTOCOL)://172.17.0.1:80
   ```

如上所示，你已经定义了 `SERVICE_ADDRESS` 的正确依赖引用，
`UNCHANGED_REFERENCE` 的错误依赖引用，
并跳过了 `ESCAPED_REFERENCE` 的依赖引用。

如果环境变量被引用时已事先定义，则引用可以正确解析，
比如 `SERVICE_ADDRESS` 的例子。

请注意，`env` 列表中的顺序很重要。如果某环境变量定义出现在列表的尾部，
则在解析列表前部环境变量时不会视其为“已被定义”。
这就是为什么 `UNCHANGED_REFERENCE` 在上面的示例中解析 `$(PROTOCOL)` 失败的原因。

当环境变量未定义或仅包含部分变量时，未定义的变量会被当做普通字符串对待，
比如 `UNCHANGED_REFERENCE` 的例子。
注意，解析不正确的环境变量通常不会阻止容器启动。

`$(VAR_NAME)` 这样的语法可以用两个 `$` 转义，即：`$$(VAR_NAME)`。
无论引用的变量是否定义，转义的引用永远不会展开。
这一点可以从上面 `ESCAPED_REFERENCE` 的例子得到印证。

## {{% heading "whatsnext" %}}

* 进一步了解[环境变量](/zh-cn/docs/tasks/inject-data-application/environment-variable-expose-pod-information/)。
* 参阅 [EnvVarSource](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#envvarsource-v1-core)。

