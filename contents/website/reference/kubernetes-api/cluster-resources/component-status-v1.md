---
api_metadata:
  apiVersion: "v1"
  import: "k8s.io/api/core/v1"
  kind: "ComponentStatus"
content_type: "api_reference"
description: "ComponentStatus（和 ComponentStatusList）保存集群检验信息。"
title: "ComponentStatus"
weight: 10
---

`apiVersion: v1`

`import "k8s.io/api/core/v1"`

## ComponentStatus {#ComponentStatus}
ComponentStatus（和 ComponentStatusList）保存集群检验信息。
已废弃：该 API 在 v1.19 及更高版本中废弃。

<hr>

- **apiVersion**: v1

- **kind**: ComponentStatus

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **conditions** ([]ComponentCondition)

  **补丁策略：基于键 `type` 合并**
  
  观测到的组件状况的列表。

  <a name="ComponentCondition"></a>
  **组件状况相关信息。**

  - **conditions.status** (string)，必需

    组件状况的状态。“Healthy” 的有效值为：“True”、“False” 或 “Unknown”。

  - **conditions.type** (string)，必需

    组件状况的类型。有效值：“Healthy”

  - **conditions.error** (string)

    组件状况的错误码。例如，一个健康检查错误码。

  - **conditions.message** (string)

    组件状况相关消息。例如，有关健康检查的信息。

## ComponentStatusList {#ComponentStatusList}
作为 ComponentStatus 对象列表，所有组件状况的状态。
已废弃：该 API 在 v1.19 及更高版本中废弃。
<hr>

- **apiVersion**: v1

- **kind**: ComponentStatusList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **items** ([]<a href="{{< ref "../cluster-resources/component-status-v1#ComponentStatus" >}}">ComponentStatus</a>)，必需

  ComponentStatus 对象的列表。

## 操作 {#Operations}
<hr>

### `get` 读取指定的 ComponentStatus
#### HTTP 请求
GET /api/v1/componentstatuses/{name}

#### 参数
- **name** (**路径参数**): string，必需

  ComponentStatus 的名称

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../cluster-resources/component-status-v1#ComponentStatus" >}}">ComponentStatus</a>): OK

401: Unauthorized

### `list` 列出 ComponentStatus 类别的对象
#### HTTP 请求
GET /api/v1/componentstatuses

#### 参数
- **allowWatchBookmarks** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应
200 (<a href="{{< ref "../cluster-resources/component-status-v1#ComponentStatusList" >}}">ComponentStatusList</a>): OK

401: Unauthorized
