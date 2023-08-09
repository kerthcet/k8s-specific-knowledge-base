---
title: 通过环境变量将 Pod 信息呈现给容器
content_type: task
weight: 30
---

此页面展示 Pod 如何使用 **downward API** 通过环境变量把自身的信息呈现给 Pod 中运行的容器。
你可以使用环境变量来呈现 Pod 的字段、容器字段或两者。

在 Kubernetes 中有两种方式可以将 Pod 和容器字段呈现给运行中的容器：

* 如本任务所述的**环境变量**
* [卷文件](/zh-cn/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/)

这两种呈现 Pod 和容器字段的方式统称为 downward API。

Service 是 Kubernetes 管理的容器化应用之间的主要通信模式，因此在运行时能发现这些 Service 是很有帮助的。

在[这里](/zh-cn/docs/tutorials/services/connect-applications-service/#accessing-the-service)
阅读更多关于访问 Service 的信息。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}


## 用 Pod 字段作为环境变量的值   {#use-pod-fields-as-values-for-env-var}

在这部分练习中，你将创建一个包含一个容器的 Pod。并将 Pod 级别的字段作为环境变量投射到正在运行的容器中。

{{< codenew file="pods/inject/dapi-envars-pod.yaml" >}}

这个清单中，你可以看到五个环境变量。`env` 字段定义了一组环境变量。
数组中第一个元素指定 `MY_NODE_NAME` 这个环境变量从 Pod 的 `spec.nodeName` 字段获取变量值。
同样，其它环境变量也是从 Pod 的字段获取它们的变量值。

{{< note >}}
本示例中的字段是 Pod 字段，不是 Pod 中 Container 的字段。
{{< /note >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/inject/dapi-envars-pod.yaml
```

验证 Pod 中的容器运行正常：

```shell
# 如果新创建的 Pod 还是处于不健康状态，请重新运行此命令几次。
kubectl get pods
```

查看容器日志：

```shell
kubectl logs dapi-envars-fieldref
```

输出信息显示了所选择的环境变量的值：

```
minikube
dapi-envars-fieldref
default
172.17.0.4
default
```

要了解为什么这些值出现在日志中，请查看配置文件中的 `command` 和 `args` 字段。
当容器启动时，它将五个环境变量的值写入标准输出。每十秒重复执行一次。

接下来，进入 Pod 中运行的容器，打开一个 Shell：

```shell
kubectl exec -it dapi-envars-fieldref -- sh
```

在 Shell 中，查看环境变量：

```shell
# 在容器内的 `shell` 中运行
printenv
```

输出信息显示环境变量已经设置为 Pod 字段的值。

```
MY_POD_SERVICE_ACCOUNT=default
...
MY_POD_NAMESPACE=default
MY_POD_IP=172.17.0.4
...
MY_NODE_NAME=minikube
...
MY_POD_NAME=dapi-envars-fieldref
```

## 使用容器字段作为环境变量的值    {#use-container-fields-as-value-for-env-var}

前面的练习中，你将 Pod 级别的字段作为环境变量的值。
接下来这个练习中，你将传递属于 Pod 定义的字段，但这些字段取自特定容器而不是整个 Pod。

这里是只包含一个容器的 Pod 的清单：

{{< codenew file="pods/inject/dapi-envars-container.yaml" >}}

这个清单中，你可以看到四个环境变量。`env` 字段定义了一组环境变量。
数组中第一个元素指定 `MY_CPU_REQUEST` 这个环境变量从容器的 `requests.cpu`
字段获取变量值。同样，其它的环境变量也是从特定于这个容器的字段中获取它们的变量值。

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/inject/dapi-envars-container.yaml
```

验证 Pod 中的容器运行正常：

```shell
# 如果新创建的 Pod 还是处于不健康状态，请重新运行此命令几次。
kubectl get pods
```

查看容器日志：

```shell
kubectl logs dapi-envars-resourcefieldref
```

输出信息显示了所选择的环境变量的值：

```
1
1
33554432
67108864
```

## {{% heading "whatsnext" %}}

* 阅读[给容器定义环境变量](/zh-cn/docs/tasks/inject-data-application/define-environment-variable-container/)
* 阅读 Pod 的 [`spec`](/zh-cn/docs/reference/kubernetes-api/workload-resources/pod-v1/#PodSpec)
  API 包括容器（Pod 的一部分）的定义。
* 阅读可以使用 downward API 呈现的[可用字段](/zh-cn/docs/concepts/workloads/pods/downward-api/#available-fields)列表。

在旧版 API 参考中阅读有关 Pod、容器和环境变量的信息：

* [PodSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core)
* [Container](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#container-v1-core)
* [EnvVar](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#envvar-v1-core)
* [EnvVarSource](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#envvarsource-v1-core)
* [ObjectFieldSelector](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#objectfieldselector-v1-core)
* [ResourceFieldSelector](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#resourcefieldselector-v1-core)

