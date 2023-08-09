---
title: Kubernetes 对象
content_type: concept
weight: 10
description: >
  Kubernetes 对象是 Kubernetes 系统中的持久性实体。
  Kubernetes 使用这些实体表示你的集群状态。
  了解 Kubernetes 对象模型以及如何使用这些对象。
simple_list: true
card:
  name: concepts
  weight: 40
---


本页说明了在 Kubernetes API 中是如何表示 Kubernetes 对象的，
以及如何使用 `.yaml` 格式的文件表示 Kubernetes 对象。


## 理解 Kubernetes 对象    {#kubernetes-objects}

在 Kubernetes 系统中，**Kubernetes 对象**是持久化的实体。
Kubernetes 使用这些实体去表示整个集群的状态。
具体而言，它们描述了如下信息：

* 哪些容器化应用正在运行（以及在哪些节点上运行）
* 可以被应用使用的资源
* 关于应用运行时行为的策略，比如重启策略、升级策略以及容错策略

Kubernetes 对象是一种“意向表达（Record of Intent）”。一旦创建该对象，
Kubernetes 系统将不断工作以确保该对象存在。通过创建对象，你本质上是在告知
Kubernetes 系统，你想要的集群工作负载状态看起来应是什么样子的，
这就是 Kubernetes 集群所谓的**期望状态（Desired State）**。

操作 Kubernetes 对象 —— 无论是创建、修改或者删除 —— 需要使用
[Kubernetes API](/zh-cn/docs/concepts/overview/kubernetes-api)。
比如，当使用 `kubectl` 命令行接口（CLI）时，CLI 会调用必要的 Kubernetes API；
也可以在程序中使用[客户端库](/zh-cn/docs/reference/using-api/client-libraries/)，
来直接调用 Kubernetes API。

### 对象规约（Spec）与状态（Status）    {#object-spec-and-status}

几乎每个 Kubernetes 对象包含两个嵌套的对象字段，它们负责管理对象的配置：
对象 **`spec`（规约）** 和对象 **`status`（状态）**。
对于具有 `spec` 的对象，你必须在创建对象时设置其内容，描述你希望对象所具有的特征：
**期望状态（Desired State）**。

`status` 描述了对象的**当前状态（Current State）**，它是由 Kubernetes
系统和组件设置并更新的。在任何时刻，Kubernetes
{{< glossary_tooltip text="控制平面" term_id="control-plane" >}}
都一直在积极地管理着对象的实际状态，以使之达成期望状态。

例如，Kubernetes 中的 Deployment 对象能够表示运行在集群中的应用。
当创建 Deployment 时，你可能会设置 Deployment 的 `spec`，指定该应用要有 3 个副本运行。
Kubernetes 系统读取 Deployment 的 `spec`，
并启动我们所期望的应用的 3 个实例 —— 更新状态以与规约相匹配。
如果这些实例中有的失败了（一种状态变更），Kubernetes 系统会通过执行修正操作来响应
`spec` 和 `status` 间的不一致 —— 意味着它会启动一个新的实例来替换。

关于对象 spec、status 和 metadata 的更多信息，可参阅
[Kubernetes API 约定](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md)。

### 描述 Kubernetes 对象    {#describing-a-kubernetes-object}

创建 Kubernetes 对象时，必须提供对象的 `spec`，用来描述该对象的期望状态，
以及关于对象的一些基本信息（例如名称）。
当使用 Kubernetes API 创建对象时（直接创建或经由 `kubectl` 创建），
API 请求必须在请求主体中包含 JSON 格式的信息。
**大多数情况下，你需要提供 `.yaml` 文件为 kubectl 提供这些信息**。
`kubectl` 在发起 API 请求时，将这些信息转换成 JSON 格式。

这里有一个 `.yaml` 示例文件，展示了 Kubernetes Deployment 的必需字段和对象 `spec`：

{{< codenew file="application/deployment.yaml" >}}

相较于上面使用 `.yaml` 文件来创建 Deployment，另一种类似的方式是使用 `kubectl` 命令行接口（CLI）中的
[`kubectl apply`](/docs/reference/generated/kubectl/kubectl-commands#apply) 命令，
将 `.yaml` 文件作为参数。下面是一个示例：

```shell
kubectl apply -f https://k8s.io/examples/application/deployment.yaml
```

输出类似下面这样：

```
deployment.apps/nginx-deployment created
```

### 必需字段    {#required-fields}

在想要创建的 Kubernetes 对象所对应的 `.yaml` 文件中，需要配置的字段如下：

* `apiVersion` - 创建该对象所使用的 Kubernetes API 的版本
* `kind` - 想要创建的对象的类别
* `metadata` - 帮助唯一标识对象的一些数据，包括一个 `name` 字符串、`UID` 和可选的 `namespace`
* `spec` - 你所期望的该对象的状态

对每个 Kubernetes 对象而言，其 `spec` 之精确格式都是不同的，包含了特定于该对象的嵌套字段。
[Kubernetes API 参考](/zh-cn/docs/reference/kubernetes-api/)可以帮助你找到想要使用
Kubernetes 创建的所有对象的规约格式。

例如，参阅 Pod API 参考文档中
[`spec` 字段](/zh-cn/docs/reference/kubernetes-api/workload-resources/pod-v1/#PodSpec)。
对于每个 Pod，其 `.spec` 字段设置了 Pod 及其期望状态（例如 Pod 中每个容器的容器镜像名称）。
另一个对象规约的例子是 StatefulSet API 中的
[`spec` 字段](/zh-cn/docs/reference/kubernetes-api/workload-resources/stateful-set-v1/#StatefulSetSpec)。
对于 StatefulSet 而言，其 `.spec` 字段设置了 StatefulSet 及其期望状态。
在 StatefulSet 的 `.spec` 内，有一个为 Pod 对象提供的[模板](/zh-cn/docs/concepts/workloads/pods/#pod-templates)。
该模板描述了 StatefulSet 控制器为了满足 StatefulSet 规约而要创建的 Pod。
不同类型的对象可以有不同的 `.status` 信息。API 参考页面给出了 `.status` 字段的详细结构，
以及针对不同类型 API 对象的具体内容。

## 服务器端字段验证   {#server-side-field-validation}

从 Kubernetes v1.25 开始，API
服务器提供了服务器端[字段验证](/zh-cn/docs/reference/using-api/api-concepts/#field-validation)，
可以检测对象中未被识别或重复的字段。它在服务器端提供了 `kubectl --validate` 的所有功能。

`kubectl` 工具使用 `--validate` 标志来设置字段验证级别。它接受值
`ignore`、`warn` 和 `strict`，同时还接受值 `true`（等同于 `strict`）和
`false`（等同于 `ignore`）。`kubectl` 的默认验证设置为 `--validate=true`。

`Strict`
: 严格的字段验证，验证失败时会报错

`Warn`
: 执行字段验证，但错误会以警告形式提供而不是拒绝请求

`Ignore`
: 不执行服务器端字段验证

当 `kubectl` 无法连接到支持字段验证的 API 服务器时，它将回退为使用客户端验证。
Kubernetes 1.27 及更高版本始终提供字段验证；较早的 Kubernetes 版本可能没有此功能。
如果你的集群版本低于 v1.27，可以查阅适用于你的 Kubernetes 版本的文档。

## {{% heading "whatsnext" %}}

如果你刚开始学习 Kubernetes，可以进一步阅读以下信息：

* 最重要的 Kubernetes 基本对象 [Pod](/zh-cn/docs/concepts/workloads/pods/)。
* [Deployment](/zh-cn/docs/concepts/workloads/controllers/deployment/) 对象。
* Kubernetes 中的[控制器](/zh-cn/docs/concepts/architecture/controller/)。
* [kubectl](/zh-cn/docs/reference/kubectl/) 和
  [kubectl 命令](/docs/reference/generated/kubectl/kubectl-commands)。

从总体上了解 Kubernetes API，可以查阅：

* [Kubernetes API 概述](/zh-cn/docs/reference/using-api/)

若要更深入地了解 Kubernetes 对象，可以阅读本节的其他页面：

