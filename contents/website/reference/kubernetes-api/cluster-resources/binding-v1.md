---
api_metadata:
  apiVersion: "v1"
  import: "k8s.io/api/core/v1"
  kind: "Binding"
content_type: "api_reference"
description: "Binding 将一个对象与另一个对象联系起来; 例如，一个 Pod 被调度程序绑定到一个节点。"
title: "Binding"
weight: 9
auto_generated: true
---

`apiVersion: v1`

`import "k8s.io/api/core/v1"`


## Binding {#Binding}
Binding 将一个对象与另一个对象联系起来; 例如，一个 Pod 被调度程序绑定到一个节点。
已在 1.7 版本弃用，请使用 Pod 的 binding 子资源。
<hr>

- **apiVersion**: v1


- **kind**: Binding


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)
  标准对象的元数据， 更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata


- **target** (<a href="{{< ref "../common-definitions/object-reference#ObjectReference" >}}">ObjectReference</a>)， 必需

  要绑定到标准对象的目标对象。
## 操作   {#operations}

<hr>

### `create` 创建一个 Binding

#### HTTP 请求

POST /api/v1/namespaces/{namespace}/bindings

#### 参数

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../cluster-resources/binding-v1#Binding" >}}">Binding</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>



- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/binding-v1#Binding" >}}">Binding</a>): OK

201 (<a href="{{< ref "../cluster-resources/binding-v1#Binding" >}}">Binding</a>): Created

202 (<a href="{{< ref "../cluster-resources/binding-v1#Binding" >}}">Binding</a>): Accepted

401: Unauthorized

### `create` 创建 Pod 的绑定

#### HTTP 请求

POST /api/v1/namespaces/{namespace}/pods/{name}/binding
#### 参数

- **name** (**路径参数**): string, 必需

  Binding 的名称

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../cluster-resources/binding-v1#Binding" >}}">Binding</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/binding-v1#Binding" >}}">Binding</a>): OK

201 (<a href="{{< ref "../cluster-resources/binding-v1#Binding" >}}">Binding</a>): Created

202 (<a href="{{< ref "../cluster-resources/binding-v1#Binding" >}}">Binding</a>): Accepted

401: Unauthorized
