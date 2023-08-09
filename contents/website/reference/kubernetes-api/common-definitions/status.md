---
api_metadata:
  apiVersion: ""
  import: "k8s.io/apimachinery/pkg/apis/meta/v1"
  kind: "Status"
content_type: "api_reference"
description: "状态（Status）是不返回其他对象的调用的返回值。"
title: "Status"
weight: 12
auto_generated: true
---





`import "k8s.io/apimachinery/pkg/apis/meta/v1"`


状态（Status）是不返回其他对象的调用的返回值。

<hr>

- **apiVersion** (string)


  APIVersion 定义对象表示的版本化模式。
  服务器应将已识别的模式转换为最新的内部值，并可能拒绝无法识别的值。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources

- **code** (int32)

  此状态的建议 HTTP 返回代码，如果未设置，则为 0。

- **details** (StatusDetails)

  与原因（Reason）相关的扩展数据。每个原因都可以定义自己的扩展细节。
  此字段是可选的，并且不保证返回的数据符合任何模式，除非由原因类型定义。

  <a name="StatusDetails"></a>
  *StatusDetails 是一组附加属性，可以由服务器设置以提供有关响应的附加信息。*
  *状态对象的原因字段定义将设置哪些属性。*
  *客户端必须忽略与每个属性的定义类型不匹配的字段，并且应该假定任何属性可能为空、无效或未定义。*

  - **details.causes** ([]StatusCause)

    Causes 数组包含与 StatusReason 故障相关的更多详细信息。
    并非所有 StatusReasons 都可以提供详细的原因。

    <a name="StatusCause"></a>
    *StatusCause 提供有关 api.Status 失败的更多信息，包括遇到多个错误的情况。*

    - **details.causes.field** (string)

      导致此错误的资源字段，由其 JSON 序列化命名。
      可能包括嵌套属性的点和后缀表示法。数组是从零开始索引的。
      由于字段有多个错误，字段可能会在一系列原因中出现多次。可选。

      示例：
        - “name”：当前资源上的字段 “name”
        - “items[0].name”：“items” 中第一个数组条目上的字段 “name”

    - **details.causes.message** (string)

      对错误原因的可读描述。该字段可以按原样呈现给读者。

    - **details.causes.reason** (string)

      错误原因的机器可读描述。如果此值为空，则没有可用信息。

  - **details.group** (string)

    与状态 StatusReason 关联的资源的组属性。

  - **details.kind** (string)

    与状态 StatusReason 关联的资源的种类属性。
    在某些操作上可能与请求的资源种类不同。
    更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

  - **details.name** (string)

    与状态 StatusReason 关联的资源的名称属性（当有一个可以描述的名称时）。

  - **details.retryAfterSeconds** (int32)

    如果指定，则应重试操作前的时间（以秒为单位）。
    一些错误可能表明客户端必须采取替代操作——对于这些错误，此字段可能指示在采取替代操作之前等待多长时间。

  - **details.uid** (string)

    资源的 UID（当有单个可以描述的资源时）。
    更多信息： https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names#uids

- **kind** (string)

  Kind 是一个字符串值，表示此对象表示的 REST 资源。
  服务器可以从客户端提交请求的端点推断出这一点。
  无法更新。驼峰式规则。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **message** (string)

  此操作状态的人类可读描述。

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准列表元数据。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds


- **reason** (string)

  机器可读的说明，说明此操作为何处于“失败”状态。
  如果此值为空，则没有可用信息。
  Reason 澄清了 HTTP 状态代码，但不会覆盖它。

- **status** (string)

  操作状态。“Success”或“Failure” 之一。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
