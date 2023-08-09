---
title: Operator 模式
content_type: concept
weight: 30
---



Operator 是 Kubernetes 的扩展软件，
它利用[定制资源](/zh-cn/docs/concepts/extend-kubernetes/api-extension/custom-resources/)管理应用及其组件。
Operator 遵循 Kubernetes 的理念，特别是在[控制器](/zh-cn/docs/concepts/architecture/controller)方面。


## 初衷 {#motivation}

**Operator 模式** 旨在记述（正在管理一个或一组服务的）运维人员的关键目标。
这些运维人员负责一些特定的应用和 Service，他们需要清楚地知道系统应该如何运行、如何部署以及出现问题时如何处理。

在 Kubernetes 上运行工作负载的人们都喜欢通过自动化来处理重复的任务。
Operator 模式会封装你编写的（Kubernetes 本身提供功能以外的）任务自动化代码。

## Kubernetes 上的 Operator {#operators-in-kubernetes}

Kubernetes 为自动化而生。无需任何修改，你即可以从 Kubernetes 核心中获得许多内置的自动化功能。
你可以使用 Kubernetes 自动化部署和运行工作负载，**甚至** 可以自动化 Kubernetes 自身。

Kubernetes 的 {{< glossary_tooltip text="Operator 模式" term_id="operator-pattern" >}}概念允许你在不修改
Kubernetes 自身代码的情况下，
通过为一个或多个自定义资源关联{{< glossary_tooltip text="控制器" term_id="controller" >}}来扩展集群的能力。
Operator 是 Kubernetes API 的客户端，
充当[自定义资源](/zh-cn/docs/concepts/extend-kubernetes/api-extension/custom-resources/)的控制器。

## Operator 示例 {#example}

使用 Operator 可以自动化的事情包括：

* 按需部署应用
* 获取/还原应用状态的备份
* 处理应用代码的升级以及相关改动。例如数据库 Schema 或额外的配置设置
* 发布一个 Service，要求不支持 Kubernetes API 的应用也能发现它
* 模拟整个或部分集群中的故障以测试其稳定性
* 在没有内部成员选举程序的情况下，为分布式应用选择首领角色


想要更详细的了解 Operator？下面是一个示例：

1. 有一个名为 SampleDB 的自定义资源，你可以将其配置到集群中。
2. 一个包含 Operator 控制器部分的 Deployment，用来确保 Pod 处于运行状态。
3. Operator 代码的容器镜像。
4. 控制器代码，负责查询控制平面以找出已配置的 SampleDB 资源。
5. Operator 的核心是告诉 API 服务器，如何使现实与代码里配置的资源匹配。
   * 如果添加新的 SampleDB，Operator 将设置 PersistentVolumeClaims 以提供持久化的数据库存储，
     设置 StatefulSet 以运行 SampleDB，并设置 Job 来处理初始配置。
   * 如果你删除它，Operator 将建立快照，然后确保 StatefulSet 和 Volume 已被删除。
6. Operator 也可以管理常规数据库的备份。对于每个 SampleDB 资源，Operator
   会确定何时创建（可以连接到数据库并进行备份的）Pod。这些 Pod 将依赖于
   ConfigMap 和/或具有数据库连接详细信息和凭据的 Secret。
7. 由于 Operator 旨在为其管理的资源提供强大的自动化功能，因此它还需要一些额外的支持性代码。
   在这个示例中，代码将检查数据库是否正运行在旧版本上，
   如果是，则创建 Job 对象为你升级数据库。

## 部署 Operator {#deploying-operators}

部署 Operator 最常见的方法是将自定义资源及其关联的控制器添加到你的集群中。
跟运行容器化应用一样，控制器通常会运行在{{< glossary_tooltip text="控制平面" term_id="control-plane" >}}之外。
例如，你可以在集群中将控制器作为 Deployment 运行。

## 使用 Operator {#using-operators}

部署 Operator 后，你可以对 Operator 所使用的资源执行添加、修改或删除操作。
按照上面的示例，你将为 Operator 本身建立一个 Deployment，然后：

```shell
kubectl get SampleDB                   # 查找所配置的数据库

kubectl edit SampleDB/example-database # 手动修改某些配置
```

可以了！Operator 会负责应用所作的更改并保持现有服务处于良好的状态。

## 编写你自己的 Operator {#writing-operator}


如果生态系统中没可以实现你目标的 Operator，你可以自己编写代码。

你还可以使用任何支持
[Kubernetes API 客户端](/zh-cn/docs/reference/using-api/client-libraries/)的语言或运行时来实现
Operator（即控制器）。

以下是一些库和工具，你可用于编写自己的云原生 Operator。

{{% thirdparty-content %}}


* [Charmed Operator Framework](https://juju.is/)
* [Java Operator SDK](https://github.com/java-operator-sdk/java-operator-sdk)
* [Kopf](https://github.com/nolar/kopf) (Kubernetes Operator Pythonic Framework)
* [kube-rs](https://kube.rs/) (Rust)
* [kubebuilder](https://book.kubebuilder.io/)
* [KubeOps](https://buehler.github.io/dotnet-operator-sdk/) (.NET operator SDK)
* [KUDO](https://kudo.dev/)（Kubernetes 通用声明式 Operator）
* [Mast](https://docs.ansi.services/mast/user_guide/operator/)
* [Metacontroller](https://metacontroller.github.io/metacontroller/intro.html)，可与 Webhook 结合使用，以实现自己的功能。
* [Operator Framework](https://operatorframework.io)
* [shell-operator](https://github.com/flant/shell-operator)

## {{% heading "whatsnext" %}}


* 阅读 {{< glossary_tooltip text="CNCF" term_id="cncf" >}} [Operator 白皮书](https://github.com/cncf/tag-app-delivery/blob/eece8f7307f2970f46f100f51932db106db46968/operator-wg/whitepaper/Operator-WhitePaper_v1-0.md)。
* 详细了解[定制资源](/zh-cn/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
* 在 [OperatorHub.io](https://operatorhub.io/) 上找到现成的、适合你的 Operator
* [发布](https://operatorhub.io/)你的 Operator，让别人也可以使用
* 阅读 [CoreOS 原始文章](https://web.archive.org/web/20170129131616/https://coreos.com/blog/introducing-operators.html)，它介绍了 Operator 模式（这是一个存档版本的原始文章）。
* 阅读这篇来自谷歌云的关于构建 Operator
  最佳实践的[文章](https://cloud.google.com/blog/products/containers-kubernetes/best-practices-for-building-kubernetes-operators-and-stateful-apps)
