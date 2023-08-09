---
api_metadata:
  apiVersion: "resource.k8s.io/v1alpha2"
  import: "k8s.io/api/resource/v1alpha2"
  kind: "PodSchedulingContext"
content_type: "api_reference"
description: "PodSchedulingContext 对象包含使用 \"WaitForFirstConsumer\" 分配模式的 ResourceClaims 来调度 Pod 所需的信息。"
title: "PodSchedulingContext v1alpha2"
weight: 14
---

`apiVersion: resource.k8s.io/v1alpha2`

`import "k8s.io/api/resource/v1alpha2"`

## PodSchedulingContext {#PodSchedulingContext}

PodSchedulingContext 对象包含调度某些 Pod 所需要的额外信息，这些 Pod 使用了
“WaitForFirstConsumer” 分配模式的 ResourceClaim。

本功能特性是 Alpha 级别的特性，需要启用 DynamicResourceAllocation 特性门控。

<hr>

- **apiVersion**: resource.k8s.io/v1alpha2

- **kind**: PodSchedulingContext

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。

- **spec** (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContextSpec" >}}">PodSchedulingContextSpec</a>)，必需

  spec 描述了 Pod 需要在哪里找到资源。

- **status** (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContextStatus" >}}">PodSchedulingContextStatus</a>)

  status 描述了 Pod 的资源可以在哪里分配。

## PodSchedulingContextSpec {#PodSchedulingContextSpec}

PodSchedulingContextSpec 描述了 Pod 所需要的资源在哪里。

<hr>

- **potentialNodes** ([]string)

  **集合：合并期间保留唯一值**

  potentialNodes 列出可以运行 Pod 的节点。

  该字段的大小限制为 128。对于许多集群来说，这已经足够大了。
  较大的集群可能需要更多的尝试去找到一个适合所有待定资源的节点。
  这个限制值可能会在以后提高，但不会降低。

- **selectedNode** (string)

  selectedNode 是一个节点，由 Pod 引用的 ResourceClaim 将在此节点上尝试，
  且尝试的分配模式是 “WaitForFirstConsumer”。

## PodSchedulingContextStatus {#PodSchedulingContextStatus}

PodSchedulingContextStatus 描述 Pod 的资源可以从哪里分配。

<hr>

- **resourceClaims** ([]ResourceClaimSchedulingStatus)

  **映射：键 `name` 的唯一值将在合并过程中保留**

  resourceClaims 描述了每个 pod.spec.resourceClaim 条目的资源可用性，
  其中对应的 ResourceClaim 使用 “WaitForFirstConsumer” 分配模式。

  <a name="ResourceClaimSchedulingStatus"></a>
  **ResourceClaimSchedulingStatus 包含关于一个采用 “WaitForFirstConsumer”
  分配模式的特定 ResourceClaim 的信息。**

  - **resourceClaims.name** (string)


    name 与 pod.spec.resourceClaims[*].name 字段匹配。

  - **resourceClaims.unsuitableNodes** ([]string)

    
    **集合：合并期间保留唯一值**

    unsuitableNodes 列出 ResourceClaim 无法被分配的节点。

    该字段的大小限制为 128，与 PodSchedulingSpec.PotentialNodes 相同。
    这可能会在以后增加，但不会减少。

## PodSchedulingContextList {#PodSchedulingContextList}

PodSchedulingContextList 是 Pod 调度对象的集合。

<hr>

- **apiVersion**: resource.k8s.io/v1alpha2

- **kind**: PodSchedulingContextList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据。

- **items** ([]<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>)，必需

  items 是 PodSchedulingContext 对象的列表。

## 操作 {#Operations}

<hr>

### `get` 读取指定的 PodSchedulingContext

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/podschedulingcontexts/{name}

#### 参数

- **name**（**路径参数**）：string，必需

  PodSchedulingContext 的名称。

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): OK

401: Unauthorized

### `get` 读取指定 PodSchedulingContext 的状态

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/podschedulingcontexts/{name}/status

#### 参数

- **name**（**路径参数**）：string，必需

  PodSchedulingContext 的名称。

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): OK

401: Unauthorized

### `list` 列出或监视 PodSchedulingContext 类别的对象

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/podschedulingcontexts

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

200 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContextList" >}}">PodSchedulingContextList</a>): OK

401: Unauthorized

### `list` 列出或监视 PodSchedulingContext 类别的对象

#### HTTP 请求

GET /apis/resource.k8s.io/v1alpha2/podschedulingcontexts

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

200 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContextList" >}}">PodSchedulingContextList</a>): OK

401: Unauthorized

### `create` 创建 PodSchedulingContext

#### HTTP 请求

POST /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/podschedulingcontexts

#### 参数

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): OK

201 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): Created

202 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): Accepted

401: Unauthorized

### `update` 替换指定的 PodSchedulingContext

#### HTTP 请求

PUT /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/podschedulingcontexts/{name}

#### 参数

- **name**（**路径参数**）：string，必需

  PodSchedulingContext 的名称。

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): OK

201 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): Created

401: Unauthorized

### `update` 替换指定 PodSchedulingContext 的状态

#### HTTP 请求

PUT /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/podschedulingcontexts/{name}/status

#### 参数

- **name**（**路径参数**）：string，必需

  PodSchedulingContext 的名称。

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): OK

201 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 PodSchedulingContext

#### HTTP 请求

PATCH /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/podschedulingcontexts/{name}

#### 参数

- **name**（**路径参数**）：string，必需

  PodSchedulingContext 的名称。

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

200 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): OK

201 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): Created

401: Unauthorized

### `patch` 部分更新指定 PodSchedulingContext 的状态

#### HTTP 请求

PATCH /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/podschedulingcontexts/{name}/status

#### 参数

- **name**（**路径参数**）：string，必需

  PodSchedulingContext 的名称。

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

200 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): OK

201 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): Created

401: Unauthorized

### `delete` 删除 PodSchedulingContext

#### HTTP 请求

DELETE /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/podschedulingcontexts/{name}

#### 参数

- **name**（**路径参数**）：string，必需

  PodSchedulingContext 的名称。

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

200 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): OK

202 (<a href="{{< ref "../workload-resources/pod-scheduling-context-v1alpha2#PodSchedulingContext" >}}">PodSchedulingContext</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 PodSchedulingContext 的集合

#### HTTP 请求

DELETE /apis/resource.k8s.io/v1alpha2/namespaces/{namespace}/podschedulingcontexts

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
