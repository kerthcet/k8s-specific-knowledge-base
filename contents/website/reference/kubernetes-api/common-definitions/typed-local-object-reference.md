---
api_metadata:
  apiVersion: ""
  import: "k8s.io/api/core/v1"
  kind: "TypedLocalObjectReference"
content_type: "api_reference"
description: "TypedLocalObjectReference 包含足够的信息，可以让你在同一个名称空间中定位指定类型的引用对象。"
title: "TypedLocalObjectReference"
weight: 13
auto_generated: true
---




`import "k8s.io/api/core/v1"`


TypedLocalObjectReference 包含足够的信息，可以让你在同一个名称空间中定位特定类型的引用对象。

<hr>

- **kind** (string)，必需

  Kind 是被引用的资源的类型

- **name** (string)，必需

  Name 是被引用的资源的名称

- **apiGroup** (string)

  APIGroup 是被引用资源的组。如果不指定 APIGroup，则指定的 Kind 必须在核心 API 组中。对于任何其它第三方类型，都需要 APIGroup。





