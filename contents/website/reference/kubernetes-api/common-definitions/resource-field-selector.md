---
api_metadata:
  apiVersion: ""
  import: "k8s.io/api/core/v1"
  kind: "ResourceFieldSelector"
content_type: "api_reference"
description: "ResourceFieldSelector 表示容器资源（CPU，内存）及其输出格式。"
title: "ResourceFieldSelector"
weight: 11
auto_generated: true
---





`import "k8s.io/api/core/v1"`


ResourceFieldSelector 表示容器资源（CPU，内存）及其输出格式。

<hr>

- **resource** (string)，必选

  必选：选择的资源

- **containerName** (string)

  容器名称：对卷必选，对环境变量可选

- **divisor** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

  指定所曝光资源的输出格式，默认值为“1”



