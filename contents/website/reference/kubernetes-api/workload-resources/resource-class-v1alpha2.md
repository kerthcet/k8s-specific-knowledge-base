---
api_metadata:
  apiVersion: "resource.k8s.io/v1alpha2"
  import: "k8s.io/api/resource/v1alpha2"
  kind: "ResourceClass"
content_type: "api_reference"
description: "ResourceClass 由管理员用于影响资源被分配的方式。"
title: "ResourceClass v1alpha2"
weight: 17
---

`apiVersion: resource.k8s.io/v1alpha2`

`import "k8s.io/api/resource/v1alpha2"`

## ResourceClass {#ResourceClass}

ResourceClass 由管理员用于影响资源被分配的方式。

这是一个 Alpha 级别的资源类型，需要启用 DynamicResourceAllocation 特性门控。

<hr>

- **apiVersion**: resource.k8s.io/v1alpha2

- **kind**: ResourceClass

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。

- **driverName** (string)，必需

  driverName 定义动态资源驱动的名称，该驱动用于分配使用此类的 ResourceClaim。

  资源驱动具有唯一的名称，以正向的域名顺序（acme.example.com）给出。

- **parametersRef** (ResourceClassParametersReference)

  parametersRef 引用任意一个独立的对象，其中可以包含驱动在分配使用此类的资源时所用的参数。
  动态资源驱动可以区分存储在此处的参数和存储在 ResourceClaimSpec 中的参数。

  <a name="ResourceClassParametersReference"></a>
  **ResourceClassParametersReference 包含了足够的信息，让你可以定位针对 ResourceClass 的参数。**


  - **parametersRef.kind** (string)，必需

    kind 是所引用资源的类别。这个值与参数对象元数据中的值相同。

  - **parametersRef.name** (string)，必需

    name 是所引用资源的名称。


  - **parametersRef.apiGroup** (string)

    apiGroup 是所引用资源的组。对于核心 API 而言此值为空。这与创建资源时所用的 apiVersion 中的组匹配。

  - **parametersRef.namespace** (string)

    包含被引用的资源的名字空间。对于集群作用域的资源必须为空，对于名字空间作用域的资源必须不为空。

- **suitableNodes** (NodeSelector)

  当 Pod 使用还未分配的 ResourceClaim 时，调度程序在尝试查找适合 Pod 的节点时，
  将仅考虑与选择算符匹配的节点。

  设置此字段是可选的，如果设置为 null，则所有节点都是候选者。

  <a name="NodeSelector"></a>
  **节点选择算符表示针对一组节点执行一个或多个标签查询的结果的并集；
  也就是说，它表示由节点选择算符条件表示的选择算符的逻辑或计算结果。**


  - **suitableNodes.nodeSelectorTerms** ([]NodeSelectorTerm)，必需

    必需。节点选择算符条件的列表。这些条件会按逻辑或的关系来计算。

    <a name="NodeSelectorTerm"></a>
    **Null 或空的节点选择算符条件不会与任何对象匹配。这些条件会按逻辑与的关系来计算。
    TopologySelectorTerm 类别实现了 NodeSelectorTerm 的子集。**


    - **suitableNodes.nodeSelectorTerms.matchExpressions** ([]<a href="{{< ref "../common-definitions/node-selector-requirement#NodeSelectorRequirement" >}}">NodeSelectorRequirement</a>)

      基于节点标签所设置的节点选择算符要求的列表。

    - **suitableNodes.nodeSelectorTerms.matchFields** ([]<a href="{{< ref "../common-definitions/node-selector-requirement#NodeSelectorRequirement" >}}">NodeSelectorRequirement</a>)

      基于节点字段所设置的节点选择算符要求的列表。

## ResourceClassList {#ResourceClassList}

ResourceClassList 是资源类的集合。

<hr>

- **apiVersion**: resource.k8s.io/v1alpha2

- **kind**: ResourceClassList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据。

- **items** ([]<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>)，必需

  items 是资源类的列表。

## 操作 {#Operations}

<hr>

### `get` 读取指定的 ResourceClass

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/resourceclasses/{name}

#### 参数

- **name**（**路径参数**）：string，必需

  ResourceClass 的名称。

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): OK

401: Unauthorized

### `list` 列出或监视 ResourceClass 类别的对象

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/resourceclasses

#### 参数

- **allowWatchBookmarks**（**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents**（**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch**（**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClassList" >}}">ResourceClassList</a>): OK

401: Unauthorized

### `create` 创建 ResourceClass

#### HTTP 请求

POST /apis/resource.k8s.io/v1alpha2/resourceclasses

#### 参数

- **body**: <a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): Created

202 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): Accepted

401: Unauthorized

### `update` 替换指定的 ResourceClass

#### HTTP 请求

PUT /apis/resource.k8s.io/v1alpha2/resourceclasses/{name}

#### 参数

- **name**（**路径参数**）：string，必需

  ResourceClass 的名称。

- **body**: <a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 ResourceClass

#### HTTP 请求

PATCH /apis/resource.k8s.io/v1alpha2/resourceclasses/{name}

#### 参数

- **name**（**路径参数**）：string，必需

  ResourceClass 的名称。

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force**（**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): Created

401: Unauthorized

### `delete` 删除 ResourceClass

#### HTTP 请求

DELETE /apis/resource.k8s.io/v1alpha2/resourceclasses/{name}

#### 参数

- **name**（**路径参数**）：string，必需

  ResourceClass 的名称。

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): OK

202 (<a href="{{< ref "../workload-resources/resource-class-v1alpha2#ResourceClass" >}}">ResourceClass</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 ResourceClass 的集合

#### HTTP 请求

DELETE /apis/resource.k8s.io/v1alpha2/resourceclasses

#### 参数

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **continue**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldSelector**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **gracePeriodSeconds**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **labelSelector**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

- **resourceVersion**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents**（**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
