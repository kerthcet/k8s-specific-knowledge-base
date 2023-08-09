---
api_metadata:
  apiVersion: "coordination.k8s.io/v1"
  import: "k8s.io/api/coordination/v1"
  kind: "Lease"
content_type: "api_reference"
description: "Lease 定义了租约的概念。"
title: "Lease"
weight: 5
---

`apiVersion: coordination.k8s.io/v1`

`import "k8s.io/api/coordination/v1"`

## Lease {#Lease}

Lease 定义了租约的概念。

<hr>

- **apiVersion**: coordination.k8s.io/v1

- **kind**: Lease

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../cluster-resources/lease-v1#LeaseSpec" >}}">LeaseSpec</a>)

  spec 包含 Lease 的规约。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

## LeaseSpec {#LeaseSpec}

LeaseSpec 是一个 Lease 的规约。

<hr>

- **acquireTime** (MicroTime)

  acquireTime 是当前租约被获取的时间。
  
  <a name="MicroTime"></a>
  **MicroTime 是微秒级精确时间的版本。**

- **holderIdentity** (string)

  holderIdentity 包含当前租约持有人的身份。

- **leaseDurationSeconds** (int32)

  leaseDurationSeconds 是租约候选人需要等待强制获取租约的持续时间。这是相对于上次观察到的 renewTime 的度量。

- **leaseTransitions** (int32)

  leaseTransitions 是租约持有人之间的转换次数。

- **renewTime** (MicroTime)

  renewTime 是当前租约持有人上次更新租约的时间。

  <a name="MicroTime"></a>
  **MicroTime 是具有微秒级精度的时间版本。**

## LeaseList {#LeaseList}

LeaseList 是 Lease 对象的列表。

<hr>

- **apiVersion**: coordination.k8s.io/v1

- **kind**: LeaseList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../cluster-resources/lease-v1#Lease" >}}">Lease</a>), required

  items 是架构对象的列表。

## 操作   {#operations}

<hr>

### `get` 读取指定的 Lease

#### HTTP 请求

GET /apis/coordination.k8s.io/v1/namespaces/{namespace}/leases/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  Lease 名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/lease-v1#Lease" >}}">Lease</a>): OK

401: Unauthorized

### `list` 列出或监视 Lease 类对象

#### HTTP 请求

GET /apis/coordination.k8s.io/v1/namespaces/{namespace}/leases

#### 参数

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

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

200 (<a href="{{< ref "../cluster-resources/lease-v1#LeaseList" >}}">LeaseList</a>): OK

401: Unauthorized

### `list` 列出或监视 Lease 类对象

#### HTTP 请求

GET /apis/coordination.k8s.io/v1/leases

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

200 (<a href="{{< ref "../cluster-resources/lease-v1#LeaseList" >}}">LeaseList</a>): OK

401: Unauthorized

### `create` 创建 Lease

#### HTTP 请求

POST /apis/coordination.k8s.io/v1/namespaces/{namespace}/leases

#### 参数

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../cluster-resources/lease-v1#Lease" >}}">Lease</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/lease-v1#Lease" >}}">Lease</a>): OK

201 (<a href="{{< ref "../cluster-resources/lease-v1#Lease" >}}">Lease</a>): Created

202 (<a href="{{< ref "../cluster-resources/lease-v1#Lease" >}}">Lease</a>): Accepted

401: Unauthorized

### `update` 替换指定的 Lease

#### HTTP 请求

PUT /apis/coordination.k8s.io/v1/namespaces/{namespace}/leases/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  Lease 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../cluster-resources/lease-v1#Lease" >}}">Lease</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/lease-v1#Lease" >}}">Lease</a>): OK

201 (<a href="{{< ref "../cluster-resources/lease-v1#Lease" >}}">Lease</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 Lease

#### HTTP 请求

PATCH /apis/coordination.k8s.io/v1/namespaces/{namespace}/leases/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  Lease 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/lease-v1#Lease" >}}">Lease</a>): OK

201 (<a href="{{< ref "../cluster-resources/lease-v1#Lease" >}}">Lease</a>): Created

401: Unauthorized

### `delete` 删除一个 Lease

#### HTTP 请求

DELETE /apis/coordination.k8s.io/v1/namespaces/{namespace}/leases/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  Lease 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 Lease 收款

#### HTTP 请求

DELETE /apis/coordination.k8s.io/v1/namespaces/{namespace}/leases

#### 参数

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **continue** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **gracePeriodSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **labelSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

- **resourceVersion** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
