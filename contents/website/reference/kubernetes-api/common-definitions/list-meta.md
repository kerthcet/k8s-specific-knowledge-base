---
api_metadata:
  apiVersion: ""
  import: "k8s.io/apimachinery/pkg/apis/meta/v1"
  kind: "ListMeta"
content_type: "api_reference"
description: "ListMeta 描述了合成资源必须具有的元数据，包括列表和各种状态对象。"
title: "ListMeta"
weight: 3
auto_generated: true
---



`import "k8s.io/apimachinery/pkg/apis/meta/v1"`

`ListMeta` 描述了合成资源必须具有的元数据，包括列表和各种状态对象。
一个资源仅能有 `{ObjectMeta, ListMeta}` 中的一个。

<hr>


- **continue** (string)

  如果用户对返回的条目数量设置了限制，则 `continue` 可能被设置，表示服务器有更多可用的数据。
  该值是不透明的，可用于向提供此列表服务的端点发出另一个请求，以检索下一组可用的对象。
  如果服务器配置已更改或时间已过去几分钟，则可能无法继续提供一致的列表。
  除非你在错误消息中收到此令牌（token），否则使用此 `continue` 值时返回的 `resourceVersion` 
  字段应该和第一个响应中的值是相同的。


- **remainingItemCount** (int64)

  `remainingItemCount` 是列表中未包含在此列表响应中的后续项目的数量。
  如果列表请求包含标签或字段选择器，则剩余项目的数量是未知的，并且在序列化期间该字段将保持未设置和省略。
  如果列表是完整的（因为它没有分块或者这是最后一个块），那么就没有剩余的项目，并且在序列化过程中该字段将保持未设置和省略。
  早于 v1.15 的服务器不设置此字段。`remainingItemCount` 的预期用途是*估计*集合的大小。
  客户端不应依赖于设置准确的 `remainingItemCount`。


- **resourceVersion** (string)

  标识该对象的服务器内部版本的字符串，客户端可以用该字段来确定对象何时被更改。
  该值对客户端是不透明的，并且应该原样传回给服务器。该值由系统填充，只读。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#concurrency-control-and-consistency 。


- **selfLink** (string)
  
  selfLink 表示此对象的 URL，由系统填充，只读。
  
  已弃用：selfLink 是一个遗留的只读字段，不再由系统填充。





