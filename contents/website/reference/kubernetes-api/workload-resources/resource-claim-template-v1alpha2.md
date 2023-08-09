---
api_metadata:
  apiVersion: "resource.k8s.io/v1alpha2"
  import: "k8s.io/api/resource/v1alpha2"
  kind: "ResourceClaimTemplate"
content_type: "api_reference"
description: "ResourceClaimTemplate 用于生成 ResourceClaim 对象。"
title: "ResourceClaimTemplate v1alpha2"
weight: 16
---

`apiVersion: resource.k8s.io/v1alpha2`

`import "k8s.io/api/resource/v1alpha2"`

## ResourceClaimTemplate {#ResourceClaimTemplate}

ResourceClaimTemplate 用于生成 ResourceClaim 对象。

<hr>

- **apiVersion**: resource.k8s.io/v1alpha2

- **kind**: ResourceClaimTemplate

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。

- **spec** (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplateSpec" >}}">ResourceClaimTemplateSpec</a>), 必需

  描述要生成的 ResourceClaim。

  该字段是不可变的。当需要时，控制平面将为 Pod 创建一个 ResourceClaim，然后不再对其进行更新。

## ResourceClaimTemplateSpec {#ResourceClaimTemplateSpec}

ResourceClaimTemplateSpec 包含针对 ResourceClaim 的元数据和字段。

<hr>

*spec** (<a href="{{< ref "#ResourceClaimTemplateSpec" >}}">ResourceClaimSpec</a>), 必需

  ResourceClaim 的规约。整个内容将不加修改地复制到从模板创建的 ResourceClaim 中。
  与 ResourceClaim 中相同的字段在此处也是有效的。

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  ObjectMeta 可以包含创建 PVC 时将要复制到其中的标签和注解。
  不允许设置其他字段，并且即便设置了也会在验证期间被拒绝。

## ResourceClaimTemplateList {#ResourceClaimTemplateList}

ResourceClaimTemplateList 是申领模板的集合。

<hr>

- **apiVersion**: resource.k8s.io/v1alpha2

- **kind**: ResourceClaimTemplateList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据。

- **items** ([]<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>), 必需

  items 是资源申领模板的列表。

## 操作 {#Operations}

<hr>

### `get` 读取指定的 ResourceClaimTemplate

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaimtemplates/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  name of the ResourceClaimTemplate

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>): OK

401: Unauthorized

### `list` 列出或监视 ResourceClaimTemplate 类别的对象

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaimtemplates

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

200 (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplateList" >}}">ResourceClaimTemplateList</a>): OK

401: Unauthorized

### `list` 列出或监视 ResourceClaimTemplate 类别的对象

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/resourceclaimtemplates

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

200 (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplateList" >}}">ResourceClaimTemplateList</a>): OK

401: Unauthorized

### `create` 创建 ResourceClaimTemplate

#### HTTP 请求

POST /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaimtemplates

#### 参数

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>): Created

202 (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>): Accepted

401: Unauthorized

### `update` 替换指定的 ResourceClaimTemplate

#### HTTP 请求

PUT /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaimtemplates/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  name of the ResourceClaimTemplate

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 ResourceClaimTemplate

#### HTTP 请求

PATCH /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaimtemplates/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  name of the ResourceClaimTemplate

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

200 (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>): Created

401: Unauthorized

### `delete` 删除 ResourceClaimTemplate

#### HTTP 请求

DELETE /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaimtemplates/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  name of the ResourceClaimTemplate

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

200 (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>): OK

202 (<a href="{{< ref "../workload-resources/resource-claim-template-v1alpha2#ResourceClaimTemplate" >}}">ResourceClaimTemplate</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 ResourceClaimTemplate 的集合

#### HTTP 请求

DELETE /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaimtemplates

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
