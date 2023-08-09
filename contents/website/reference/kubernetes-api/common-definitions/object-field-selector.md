---
api_metadata:
  apiVersion: ""
  import: "k8s.io/api/core/v1"
  kind: "ObjectFieldSelector"
content_type: "api_reference"
description: "ObjectFieldSelector 选择对象的 APIVersioned 字段。"
title: "ObjectFieldSelector"
weight: 6
auto_generated: true
---




`import "k8s.io/api/core/v1"`

ObjectFieldSelector 选择对象的 APIVersioned 字段。
<hr>


- **fieldPath** (string)，必需的

  在指定 API 版本中要选择的字段的路径。

- **apiVersion** (string)

  `fieldPath` 写入时所使用的模式版本，默认为 "v1"。


