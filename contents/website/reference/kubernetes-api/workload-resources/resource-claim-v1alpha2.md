---
api_metadata:
  apiVersion: "resource.k8s.io/v1alpha2"
  import: "k8s.io/api/resource/v1alpha2"
  kind: "ResourceClaim"
content_type: "api_reference"
description: "ResourceClaim 描述资源使用者需要哪些资源。"
title: "ResourceClaim v1alpha2"
weight: 15
---

`apiVersion: resource.k8s.io/v1alpha2`

`import "k8s.io/api/resource/v1alpha2"`

## ResourceClaim {#ResourceClaim}

ResourceClaim 描述资源使用者需要哪些资源。它的状态跟踪资源是否已被分配以及产生的属性是什么。

这是一个 Alpha 级别的资源类型，需要启用 DynamicResourceAllocation 特性门控。

<hr>

- **apiVersion**: resource.k8s.io/v1alpha2

- **kind**: ResourceClaim

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。

- **spec** (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaimSpec" >}}">ResourceClaimSpec</a>)，必需

  spec 描述了需要被分配的资源所需的属性。它只能在创建 ResourceClaim 时设置一次。

- **status** (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaimStatus" >}}">ResourceClaimStatus</a>)

  status 描述资源是否可用以及具有哪些属性。

## ResourceClaimSpec {#ResourceClaimSpec}

ResourceClaimSpec 定义资源如何被分配。

<hr>

- **resourceClassName** (string)，必需

  resourceClassName 通过部署驱动时创建的 ResourceClass 名称来引用驱动和附加参数。

- **allocationMode** (string)

  分配可以立即开始或在 Pod 想要使用资源时开始。"WaitForFirstConsumer" 是默认值。

- **parametersRef** (ResourceClaimParametersReference)

  parametersRef 引用一个单独的对象，包含驱动为申领分配资源时将使用的任意参数。

  此对象必须与 ResourceClaim 在同一个名字空间中。

  <a name="ResourceClaimParametersReference"></a>
  **ResourceClaimParametersReference 包含足够信息，便于你定位 ResourceClaim 的参数。
  该对象必须与 ResourceClaim 在相同的名字空间中。**


  - **parametersRef.kind** (string)，必需

    kind 是所引用资源的类别。这个值与参数对象元数据中的值相同，例如 "ConfigMap"。

  - **parametersRef.name** (string)，必需

    name 是所引用资源的名称。

  - **parametersRef.apiGroup** (string)

    apiGroup 是所引用资源的组。对于核心 API 而言此值为空。
    字段值与创建资源时所用的 apiVersion 中的组匹配。

## ResourceClaimStatus {#ResourceClaimStatus}

ResourceClaimStatus 跟踪资源是否已被分配以及产生的属性是什么。

<hr>

- **allocation** (AllocationResult)

  一旦某资源或资源集已被成功分配，资源驱动就会设置 allocation 的值。
  如果此项未被设置，则表示资源尚未被分配。

  <a name="AllocationResult"></a>
  **AllocationResult 包含已分配资源的属性。**


  - **allocation.availableOnNodes** (NodeSelector)

    在资源驱动完成资源分配之后，将设置此字段以通知调度器可以将使用了 ResourceClaim 的 Pod 调度到哪里。

    设置此字段是可选的。如果字段值为空，表示资源可以在任何地方访问。

    <a name="NodeSelector"></a>
    **节点选择算符表示对一组节点执行一个或多个标签查询的结果的并集；
    也就是说，它表示由节点选择算符条件表示的选择算符的逻辑或计算结果。**


    - **allocation.availableOnNodes.nodeSelectorTerms** ([]NodeSelectorTerm)，必需

      必需。节点选择算符条件的列表。这些条件以逻辑或进行计算。

      <a name="NodeSelectorTerm"></a>
      **一个 null 或空的节点选择算符条件不会与任何对象匹配。条件中的要求会按逻辑与的关系来计算。
      TopologySelectorTerm 类别实现了 NodeSelectorTerm 的子集。**

      - **allocation.availableOnNodes.nodeSelectorTerms.matchExpressions** ([]<a href="{{< ref "../common-definitions/node-selector-requirement#NodeSelectorRequirement" >}}">NodeSelectorRequirement</a>)


        基于节点标签所设置的节点选择算符要求的列表。

      - **allocation.availableOnNodes.nodeSelectorTerms.matchFields** ([]<a href="{{< ref "../common-definitions/node-selector-requirement#NodeSelectorRequirement" >}}">NodeSelectorRequirement</a>)


        基于节点字段所设置的节点选择算符要求的列表。

  - **allocation.resourceHandles** ([]ResourceHandle)


    **原子性：将在合并期间被替换**

    resourceHandles 包含应在申领的整个生命期中保持的、与某资源分配所关联的状态。
    每个 resourceHandle 包含应向特定 kubelet 插件传递的数据，
    一旦资源落到某具体节点上，这些数据就会被传递给该插件。
    此数据将在成功分配后由驱动返回，并对 Kubernetes 不透明。
    必要时驱动文档可能会向用户阐述如何解读这些数据。


    设置此字段是可选的。它最大可以有 32 个条目。如果为 null（或为空），
    则假定此分配将由某个确定的 kubelet 插件处理，
    不会附加 resourceHandle 数据。所调用的 kubelet 插件的名称将与嵌入此
    AllocationResult 的 ResourceClaimStatus 中设置的 driverName 匹配。

    <a name="ResourceHandle"></a>
    **resourceHandle 保存不透明的资源数据，以供特定的 kubelet 插件处理。**


    - **allocation.resourceHandles.data** (string)

      data 包含与此 resourceHandle 关联的不透明数据。
      data 由资源驱动中的控制器组件设置，该驱动的名字与嵌入此 resourceHandle 的
      ResourceClaimStatus 中设置的 driverName 相同。
      data 在分配时进行设置，供 kubelet 插件处理；所指的插件的名称与此 resourceHandle
      所设置的 driverName 相同。

      该字段的最大值为 16KiB。此值在未来可能会增加，但不会减少。

    - **allocation.resourceHandles.driverName** (string)


      driverName 指定资源驱动的名称；一旦 resourceHandle 落到某具体节点，
      就应调用该驱动对应的 kubelet 插件来处理此数据。
      字段值可能与嵌入此 resourceHandle 的 ResourceClaimStatus 中设置的 driverName 不同。

  - **allocation.shareable** (boolean)


    shareable 确定资源是否同时支持多个使用者。

- **deallocationRequested** (boolean)
  
  deallocationRequested 表示某 ResourceClaim 将被取消分配。

  出现请求后，驱动必须释放此申领，重置此字段并清除 allocation 字段。

  在 deallocationRequested 被设置时，不能将新的使用者添加到 reservedFor。

- **driverName** (string)

  driverName 是在确定了分配之后，从 ResourceClass 复制而来的驱动名称。

- **reservedFor** ([]ResourceClaimConsumerReference)

  **Map：合并期间根据键 uid 保留不重复的值**

  reservedFor 标明目前哪些实体允许使用申领。如果引用未为某个 Pod 预留的 ResourceClaim，则该 Pod 将不会启动。


  最多可以有 32 个这样的预留。这一限制可能会在未来放宽，但不会减少。

  <a name="ResourceClaimConsumerReference"></a>
  **ResourceClaimConsumerReference 包含足够的信息以便定位 ResourceClaim 的使用者。
  用户必须是与 ResourceClaim 在同一名字空间中的资源。**

  
  - **reservedFor.name** (string)，必需

    name 是所引用资源的名称。

  - **reservedFor.resource** (string)，必需

    resource 是所引用资源的类别，例如 "pods"。

  - **reservedFor.uid** (string)，必需

    uid 用于唯一标识资源的某实例。

  - **reservedFor.apiGroup** (string)

    apiGroup 是所引用资源的组。对于核心 API 而言此值为空。
    字段值与创建资源时所用的 apiVersion 中的组匹配。

## ResourceClaimList {#ResourceClaimList}

ResourceClaimList 是申领的集合。

<hr>

- **apiVersion**: resource.k8s.io/v1alpha2

- **kind**: ResourceClaimList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据。

- **items** ([]<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>)，必需

  items 是资源申领的列表。

## 操作 {#Operations}

<hr>

### `get` 读取指定的 ResourceClaim

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}

#### 参数

- **name**（**路径参数**）：string，必需

  ResourceClaim 的名称。

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

401: Unauthorized

### `get` 读取指定 ResourceClaim 的状态

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}/status

#### 参数

- **name**（**路径参数**）：string，必需

  ResourceClaim 的名称。

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

401: Unauthorized

### `list` 列出或监视 ResourceClaim 类别的对象

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims

#### 参数

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

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

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaimList" >}}">ResourceClaimList</a>): OK

401: Unauthorized

### `list` 列出或监视 ResourceClaim 类别的对象

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/resourceclaims

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

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaimList" >}}">ResourceClaimList</a>): OK

401: Unauthorized

### `create` 创建 ResourceClaim

#### HTTP 请求

POST /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims

#### 参数

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): Created

202 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): Accepted

401: Unauthorized

### `update` 替换指定的 ResourceClaim

#### HTTP 请求

PUT /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}

#### 参数

- **name**（**路径参数**）：string，必需

  ResourceClaim 的名称。

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): Created

401: Unauthorized

### `update` 替换指定 ResourceClaim 的状态

#### HTTP 请求

PUT /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}/status

#### 参数

- **name**（**路径参数**）：string，必需

  ResourceClaim 的名称。

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 ResourceClaim

#### HTTP 请求

PATCH /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}

#### 参数

- **name**（**路径参数**）：string，必需

  ResourceClaim 的名称。

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

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

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): Created

401: Unauthorized

### `patch` 部分更新指定 ResourceClaim 的状态

#### HTTP 请求

PATCH /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}/status

#### 参数

- **name**（**路径参数**）：string，必需

  ResourceClaim 的名称。

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

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

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

201 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): Created

401: Unauthorized

### `delete` 删除 ResourceClaim

#### HTTP 请求

DELETE /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims/{name}

#### 参数

- **name**（**路径参数**）：string，必需

  ResourceClaim 的名称。

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

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

200 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): OK

202 (<a href="{{< ref "../workload-resources/resource-claim-v1alpha2#ResourceClaim" >}}">ResourceClaim</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 ResourceClaim 的集合

#### HTTP 请求

DELETE /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/resourceclaims

#### 参数

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

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
