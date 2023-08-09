---
api_metadata:
  apiVersion: "scheduling.k8s.io/v1"
  import: "k8s.io/api/scheduling/v1"
  kind: "PriorityClass"
content_type: "api_reference"
description: "PriorityClass 定义了从优先级类名到优先级数值的映射。"
title: "PriorityClass"
weight: 13
auto_generated: false
---



`apiVersion: scheduling.k8s.io/v1`

`import "k8s.io/api/scheduling/v1"`

## PriorityClass {#PriorityClass}

PriorityClass 定义了从优先级类名到优先级数值的映射。
该值可以是任何有效的整数。

<hr>

- **apiVersion**: scheduling.k8s.io/v1

- **kind**: PriorityClass

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准对象的元数据。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **value** （int32），必需

  value 表示此优先级的整数值。这是 Pod 在其 Pod 规约中有此类名称时收到的实际优先级。

- **description** (string)

  description 是一个任意字符串，通常提供有关何时应使用此优先级的指南。

- **globalDefault** (boolean)

  globalDefault 指定是否应将此 PriorityClass 视为没有任何优先级类的 Pod 的默认优先级。
  只有一个 PriorityClass 可以标记为 `globalDefault`。
  但是，如果存在多个 PriorityClasses 且其 `globalDefault` 字段设置为 true，
  则将使用此类全局默认 PriorityClasses 的最小值作为默认优先级。
  
- **preemptionPolicy** (string)

  PreemptionPolicy 是抢占优先级较低的 Pod 的策略。
  可选值：Never、PreemptLowerPriority。
  如果未设置，则默认为 PreemptLowerPriority。

## PriorityClassList {#PriorityClassList}

PriorityClassList 是优先级类的集合。

<hr>

- **apiVersion**: scheduling.k8s.io/v1

- **kind**: PriorityClassList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准列表元数据。更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../workload-resources/priority-class-v1#PriorityClass" >}}">PriorityClass</a>)，必需

  items 是 PriorityClasses 的列表

## 操作 {#Operations}

<hr>

### `get` 读取特定的 PriorityClass

#### HTTP 请求

GET /apis/scheduling.k8s.io/v1/priorityclasses/{name}

#### 参数

- **name** （**路径参数**）: string，必需

  PriorityClass 名称

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/priority-class-v1#PriorityClass" >}}">PriorityClass</a>): OK

401: Unauthorized

### `list` 列出或观察 PriorityClass类的对象

#### HTTP 请求

GET /apis/scheduling.k8s.io/v1/priorityclasses

#### 参数

- **allowWatchBookmarks** （**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** （**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** （**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** （**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/priority-class-v1#PriorityClassList" >}}">PriorityClassList</a>): OK

401: Unauthorized

### `create` 创建一个 PriorityClass

#### HTTP 请求

POST /apis/scheduling.k8s.io/v1/priorityclasses

#### 参数

- **body**: <a href="{{< ref "../workload-resources/priority-class-v1#PriorityClass" >}}">PriorityClass</a>，必需
  
- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/priority-class-v1#PriorityClass" >}}">PriorityClass</a>): OK

201 (<a href="{{< ref "../workload-resources/priority-class-v1#PriorityClass" >}}">PriorityClass</a>): Created

202 (<a href="{{< ref "../workload-resources/priority-class-v1#PriorityClass" >}}">PriorityClass</a>): Accepted

401: Unauthorized

### `update` 替换指定的 PriorityClass

#### HTTP 请求

PUT /apis/scheduling.k8s.io/v1/priorityclasses/{name}

#### 参数

- **name** （**路径参数**）: string，必需

  PriorityClass 名称

- **body**: <a href="{{< ref "../workload-resources/priority-class-v1#PriorityClass" >}}">PriorityClass</a>，必需
 
- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200 (<a href="{{< ref "../workload-resources/priority-class-v1#PriorityClass" >}}">PriorityClass</a>): OK

201 (<a href="{{< ref "../workload-resources/priority-class-v1#PriorityClass" >}}">PriorityClass</a>): Created

401: Unauthorized


### `patch` 部分更新特定的 PriorityClass

#### HTTP 请求

PATCH /apis/scheduling.k8s.io/v1/priorityclasses/{name}

#### 参数

- **name** （**路径参数**）: string，必需

  PriorityClass 名称

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** （**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/priority-class-v1#PriorityClass" >}}">PriorityClass</a>): OK

201 (<a href="{{< ref "../workload-resources/priority-class-v1#PriorityClass" >}}">PriorityClass</a>): Created

401: Unauthorized

### `delete` 删除一个 PriorityClass

#### HTTP 请求

DELETE /apis/scheduling.k8s.io/v1/priorityclasses/{name}

#### 参数

- **name** （**路径参数**）: string，必需

  PriorityClass 名称。

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** （**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 PriorityClass 集合

#### HTTP 请求

DELETE /apis/scheduling.k8s.io/v1/priorityclasses

#### 参数

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **continue** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **gracePeriodSeconds** （**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **labelSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** （**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

- **resourceVersion** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** （**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
