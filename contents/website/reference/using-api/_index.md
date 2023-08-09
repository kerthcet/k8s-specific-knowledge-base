---
title: API 概述
content_type: concept
weight: 20
no_list: true
card:
  name: reference
  weight: 50
  title: API 概述
---



本文提供了 Kubernetes API 的参考信息。

REST API 是 Kubernetes 的基本结构。
所有操作和组件之间的通信及外部用户命令都是调用 API 服务器处理的 REST API。
因此，Kubernetes 平台视一切皆为 API 对象，
且它们在 [API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/) 中有相应的定义。

[Kubernetes API 参考](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/)
列出了 Kubernetes {{< param "version" >}} 版本的 API。

如需了解一般背景信息，请查阅 [Kubernetes API](/zh-cn/docs/concepts/overview/kubernetes-api/)。
[Kubernetes API 控制访问](/zh-cn/docs/concepts/security/controlling-access/)描述了客户端如何向
Kubernetes API 服务器进行身份认证以及他们的请求如何被鉴权。

## API 版本控制 {#api-reference}

JSON 和 Protobuf 序列化模式遵循相同的模式更改原则。
以下描述涵盖了这两种格式。

API 版本控制和软件版本控制是间接相关的。
[API 和发布版本控制提案](https://git.k8s.io/sig-release/release-engineering/versioning.md)描述了
API 版本控制和软件版本控制间的关系。

不同的 API 版本代表着不同的稳定性和支持级别。
你可以在 [API 变更文档](https://git.k8s.io/community/contributors/devel/sig-architecture/api_changes.md#alpha-beta-and-stable-versions)
中查看到更多的不同级别的判定标准。

下面是每个级别的摘要：

- Alpha：
  - 版本名称包含 `alpha`（例如：`v1alpha1`）。
  - 内置的 Alpha API 版本默认被禁用且必须在 `kube-apiserver` 配置中显式启用才能使用。
  - 软件可能会有 Bug。启用某个特性可能会暴露出 Bug。
  - 对某个 Alpha API 特性的支持可能会随时被删除，恕不另行通知。
  - API 可能在以后的软件版本中以不兼容的方式更改，恕不另行通知。
  - 由于缺陷风险增加和缺乏长期支持，建议该软件仅用于短期测试集群。

- Beta：
  - 版本名称包含 `beta`（例如：`v2beta3`）。
  - 内置的 Beta API 版本默认被禁用且必须在 `kube-apiserver` 配置中显式启用才能使用
    （例外情况是 Kubernetes 1.22 之前引入的 Beta 版本的 API，这些 API 默认被启用）。
  - 内置 Beta API 版本从引入到弃用的最长生命周期为 9 个月或 3 个次要版本（以较长者为准），
    从弃用到移除的最长生命周期为 9 个月或 3 个次要版本（以较长者为准）。
  - 软件被很好的测试过。启用某个特性被认为是安全的。
  - 尽管一些特性会发生细节上的变化，但它们将会被长期支持。

  - 在随后的 Beta 版或 Stable 版中，对象的模式和（或）语义可能以不兼容的方式改变。
    当这种情况发生时，将提供迁移说明。
    适配后续的 Beta 或 Stable API 版本可能需要编辑或重新创建 API 对象，这可能并不简单。
    对于依赖此功能的应用程序，可能需要停机迁移。
  - 该版本的软件不建议生产使用。
    后续发布版本可能会有不兼容的变动。
    一旦 Beta API 版本被弃用且不再提供服务，
    则使用 Beta API 版本的用户需要转为使用后续的 Beta 或 Stable API 版本。

  {{< note >}}
  请尝试 Beta 版时特性时并提供反馈。
  特性完成 Beta 阶段测试后，就可能不会有太多的变更了。
  {{< /note >}}

- Stable：
  - 版本名称如 `vX`，其中 `X` 为整数。
  - 特性的 Stable 版本会出现在后续很多版本的发布软件中。
    Stable API 版本仍然适用于 Kubernetes 主要版本范围内的所有后续发布，
    并且 Kubernetes 的主要版本当前没有移除 Stable API 的修订计划。

## API 组 {#api-groups}

[API 组](https://git.k8s.io/design-proposals-archive/api-machinery/api-group.md)能够简化对
Kubernetes API 的扩展。API 组信息出现在 REST 路径中，也出现在序列化对象的 `apiVersion` 字段中。

以下是 Kubernetes 中的几个组：
*  **核心（core）**（也被称为 **legacy**）组的 REST 路径为 `/api/v1`。
   核心组并不作为 `apiVersion` 字段的一部分，例如， `apiVersion: v1`。
*  指定的组位于 REST 路径 `/apis/$GROUP_NAME/$VERSION`，
   并且使用 `apiVersion: $GROUP_NAME/$VERSION` （例如，`apiVersion: batch/v1`）。
   你可以在 [Kubernetes API 参考文档](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#-strong-api-groups-strong-)
   中查看全部的 API 组。

## 启用或禁用 API 组   {#enabling-or-disabling}

资源和 API 组是在默认情况下被启用的。
你可以通过在 API 服务器上设置 `--runtime-config` 参数来启用或禁用它们。
`--runtime-config` 参数接受逗号分隔的 `<key>[=<value>]` 对，
来描述 API 服务器的运行时配置。如果省略了 `=<value>` 部分，那么视其指定为 `=true`。
例如：

- 禁用 `batch/v1`，对应参数设置 `--runtime-config=batch/v1=false`
- 启用 `batch/v2alpha1`，对应参数设置 `--runtime-config=batch/v2alpha1`
- 要启用特定版本的 API，如 `storage.k8s.io/v1beta1/csistoragecapacities`，可以设置
  `--runtime-config=storage.k8s.io/v1beta1/csistoragecapacities`

{{< note >}}
启用或禁用组或资源时，
你需要重启 API 服务器和控制器管理器来使 `--runtime-config` 生效。
{{< /note >}}

## 持久化 {#persistence}

Kubernetes 通过 API 资源来将序列化的状态写到 {{< glossary_tooltip term_id="etcd" >}} 中存储。

## {{% heading "whatsnext" %}}

- 进一步了解 [API 惯例](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#api-conventions)
- 阅读[聚合器](https://git.k8s.io/design-proposals-archive/api-machinery/aggregated-api-servers.md)
