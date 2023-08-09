---
api_metadata:
  apiVersion: "apps/v1"
  import: "k8s.io/api/apps/v1"
  kind: "ReplicaSet"
content_type: "api_reference"
description: "ReplicaSet 确保在任何给定的时刻都在运行指定数量的 Pod 副本。"
title: "ReplicaSet"
weight: 4
---

`apiVersion: apps/v1`

`import "k8s.io/api/apps/v1"`

## ReplicaSet {#ReplicaSet}

ReplicaSet 确保在任何给定的时刻都在运行指定数量的 Pod 副本。

<hr>

- **apiVersion**: apps/v1

- **kind**: ReplicaSet

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)
  
  如果 ReplicaSet 的标签为空，则这些标签默认为与 ReplicaSet 管理的 Pod 相同。
  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSetSpec" >}}">ReplicaSetSpec</a>)
  
  spec 定义 ReplicaSet 预期行为的规约。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

- **status** (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSetStatus" >}}">ReplicaSetStatus</a>)
  
  status 是最近观测到的 ReplicaSet 状态。此数据可能在某个时间窗之后过期。
  该值由系统填充，只读。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

## ReplicaSetSpec {#ReplicaSetSpec}

ReplicaSetSpec 是 ReplicaSet 的规约。

<hr>

- **selector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)，必需
  
  selector 是针对 Pod 的标签查询，应与副本计数匹配。标签的主键和取值必须匹配，
  以便由这个 ReplicaSet 进行控制。它必须与 Pod 模板的标签匹配。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/labels/#label-selectors

- **template** (<a href="{{< ref "../workload-resources/pod-template-v1#PodTemplateSpec" >}}">PodTemplateSpec</a>)
  
  template 是描述 Pod 的一个对象，将在检测到副本不足时创建此对象。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/replicationcontroller#pod-template

- **replicas** (int32)
  
  replicas 是预期副本的数量。这是一个指针，用于辨别显式零和未指定的值。默认为 1。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/replicationcontroller/#what-is-a-replicationcontroller

- **minReadySeconds** (int32)
  
  新建的 Pod 在没有任何容器崩溃的情况下就绪并被系统视为可用的最短秒数。
  默认为 0（Pod 就绪后即被视为可用）。

## ReplicaSetStatus {#ReplicaSetStatus}

ReplicaSetStatus 表示 ReplicaSet 的当前状态。

<hr>

- **replicas** (int32)，必需
  
  replicas 是最近观测到的副本数量。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/replicationcontroller/#what-is-a-replicationcontroller

- **availableReplicas** (int32)
  
  此副本集可用副本（至少 minReadySeconds 才能就绪）的数量。

- **readyReplicas** (int32)
  
  readyReplicas 是此 ReplicaSet 在就绪状况下处理的目标 Pod 数量。

- **fullyLabeledReplicas** (int32)
  
  标签与 ReplicaSet 的 Pod 模板标签匹配的 Pod 数量。

- **conditions** ([]ReplicaSetCondition)
  
  **补丁策略：按照键 `type` 合并**
  
  表示副本集当前状态的最新可用观测值。
  
  <a name="ReplicaSetCondition"></a> 
  **ReplicaSetCondition 描述某个点的副本集状态。**
  

  - **conditions.status** (string)，必需
    
    状况的状态，取值为 True、False 或 Unknown 之一。
  
  - **conditions.type** (string)，必需
    
    副本集状况的类型。
  

  - **conditions.lastTransitionTime** (Time)
    
    状况上次从一个状态转换为另一个状态的时间。
    
    <a name="Time"></a>
    **Time 是对 time.Time 的封装。Time 支持对 YAML 和 JSON 进行正确封包。
    为 time 包的许多函数方法提供了封装器。**
  

  - **conditions.message** (string)
    
    这是一条人类可读的消息，指示有关上次转换的详细信息。
  
  - **conditions.reason** (string)
    
    状况上次转换的原因。

- **observedGeneration** (int64)
  
  observedGeneration 反映了最近观测到的 ReplicaSet 生成情况。

## ReplicaSetList {#ReplicaSetList}

ReplicaSetList 是多个 ReplicaSet 的集合。

<hr>

- **apiVersion**: apps/v1

- **kind**: ReplicaSetList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)
  
  标准的列表元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **items** ([]<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>)，必需
  
  ReplicaSet 的列表。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/replicationcontroller

## 操作 {#Operations}

<hr>

### `get` 读取指定的 ReplicaSet

#### HTTP 请求

GET /apis/apps/v1/namespaces/{namespace}/replicasets/{name}

#### 参数

- **name** (**路径参数**): string，必需
  
  ReplicaSet 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): OK

401: Unauthorized

### `get` 读取指定的 ReplicaSet 的状态

#### HTTP 请求

GET /apis/apps/v1/namespaces/{namespace}/replicasets/{name}/status

#### 参数

- **name** (**路径参数**): string，必需
  
  ReplicaSet 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): OK

401: Unauthorized

### `list` 列出或监视 ReplicaSet 类别的对象

#### HTTP 请求

GET /apis/apps/v1/namespaces/{namespace}/replicasets

#### 参数

- **namespace** (**路径参数**): string，必需
  
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

200 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSetList" >}}">ReplicaSetList</a>): OK

401: Unauthorized

### `list` 列出或监视 ReplicaSet 类别的对象

#### HTTP 请求

GET /apis/apps/v1/replicasets

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

200 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSetList" >}}">ReplicaSetList</a>): OK

401: Unauthorized

### `create` 创建 ReplicaSet

#### HTTP 请求

POST /apis/apps/v1/namespaces/{namespace}/replicasets

#### 参数

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>，必需

- **dryRun** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): OK

201 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): Created

202 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): Accepted

401: Unauthorized

### `update` 替换指定的 ReplicaSet

#### HTTP 请求

PUT /apis/apps/v1/namespaces/{namespace}/replicasets/{name}

#### 参数

- **name** (**路径参数**): string，必需
  
  ReplicaSet 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>，必需

- **dryRun** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): OK

201 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): Created

401: Unauthorized

### `update` 替换指定的 ReplicaSet 的状态

#### HTTP 请求

PUT /apis/apps/v1/namespaces/{namespace}/replicasets/{name}/status

#### 参数

- **name** (**路径参数**): string，必需
  
  ReplicaSet 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>，必需

- **dryRun** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): OK

201 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 ReplicaSet

#### HTTP 请求

PATCH /apis/apps/v1/namespaces/{namespace}/replicasets/{name}

#### 参数

- **name** (**路径参数**): string，必需
  
  ReplicaSet 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

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

200 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): OK

201 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 ReplicaSet 的状态

#### HTTP 请求

PATCH /apis/apps/v1/namespaces/{namespace}/replicasets/{name}/status

#### 参数

- **name** (**路径参数**): string，必需
  
  ReplicaSet 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

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

200 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): OK

201 (<a href="{{< ref "../workload-resources/replica-set-v1#ReplicaSet" >}}">ReplicaSet</a>): Created

401: Unauthorized

### `delete` 删除 ReplicaSet

#### HTTP 请求

DELETE /apis/apps/v1/namespaces/{namespace}/replicasets/{name}

#### 参数

- **name** (**路径参数**): string，必需
  
  ReplicaSet 的名称

- **namespace** (**路径参数**): string，必需
  
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

### `deletecollection` 删除 ReplicaSet 的集合

#### HTTP 请求

DELETE /apis/apps/v1/namespaces/{namespace}/replicasets

#### 参数

- **namespace** (**路径参数**): string，必需
  
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
