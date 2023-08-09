---
api_metadata:
  apiVersion: "apps/v1"
  import: "k8s.io/api/apps/v1"
  kind: "Deployment"
content_type: "api_reference"
description: "Deployment 使得 Pod 和 ReplicaSet 能够进行声明式更新。"
title: "Deployment"
weight: 5
---

`apiVersion: apps/v1`

`import "k8s.io/api/apps/v1"`

## Deployment {#Deployment}

Deployment 使得 Pod 和 ReplicaSet 能够进行声明式更新。

<hr>

- **apiVersion**: apps/v1

- **kind**: Deployment

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)
  
  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../workload-resources/deployment-v1#DeploymentSpec" >}}">DeploymentSpec</a>)
  
  Deployment 预期行为的规约。

- **status** (<a href="{{< ref "../workload-resources/deployment-v1#DeploymentStatus" >}}">DeploymentStatus</a>)
  
  最近观测到的 Deployment 状态。

## DeploymentSpec {#DeploymentSpec}

DeploymentSpec 定义 Deployment 预期行为的规约。

<hr>

- **selector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)，必需
  
  供 Pod 所用的标签选择算符。通过此字段选择现有 ReplicaSet 的 Pod 集合，
  被选中的 ReplicaSet 将受到这个 Deployment 的影响。此字段必须与 Pod 模板的标签匹配。

- **template** (<a href="{{< ref "../workload-resources/pod-template-v1#PodTemplateSpec" >}}">PodTemplateSpec</a>)，必需
  
  template 描述将要创建的 Pod。`template.spec.restartPolicy`
  唯一被允许的值是 `Always`。

- **replicas** (int32)
  
  预期 Pod 的数量。这是一个指针，用于辨别显式零和未指定的值。默认为 1。

- **minReadySeconds** (int32)
  
  新建的 Pod 在没有任何容器崩溃的情况下就绪并被系统视为可用的最短秒数。
  默认为 0（Pod 就绪后即被视为可用）。

- **strategy** (DeploymentStrategy)
  
  **补丁策略：retainKeys**
  
  将现有 Pod 替换为新 Pod 时所用的部署策略。
  
  <a name="DeploymentStrategy"></a>
  **DeploymentStrategy 描述如何将现有 Pod 替换为新 Pod。**
  

  - **strategy.type** (string)
    
    部署的类型。取值可以是 “Recreate” 或 “RollingUpdate”。默认为 RollingUpdate。
  
  - **strategy.rollingUpdate** (RollingUpdateDeployment)
    
    滚动更新这些配置参数。仅当 type = RollingUpdate 时才出现。
    
    <a name="RollingUpdateDeployment"></a>
    **控制滚动更新预期行为的规约。**
    

    - **strategy.rollingUpdate.maxSurge** (IntOrString)
      
      超出预期的 Pod 数量之后可以调度的最大 Pod 数量。该值可以是一个绝对数（例如：
      5）或一个预期 Pod 的百分比（例如：10%）。如果 MaxUnavailable 为 0，则此字段不能为 0。
      通过向上取整计算得出一个百分比绝对数。默认为 25%。例如：当此值设为 30% 时，
      如果滚动更新启动，则可以立即对 ReplicaSet 扩容，从而使得新旧 Pod 总数不超过预期 Pod 数量的 130%。
      一旦旧 Pod 被杀死，则可以再次对新的 ReplicaSet 扩容，
      确保更新期间任何时间运行的 Pod 总数最多为预期 Pod 数量的 130%。
      
      <a name="IntOrString"></a>
      **IntOrString 是可以保存 int32 或字符串的一个类型。
      当用于 JSON 或 YAML 编组和取消编组时，它会产生或消费内部类型。
      例如，这允许你拥有一个可以接受名称或数值的 JSON 字段。**
    

    - **strategy.rollingUpdate.maxUnavailable** (IntOrString)
      
      更新期间可能不可用的最大 Pod 数量。该值可以是一个绝对数（例如：
      5）或一个预期 Pod 的百分比（例如：10%）。通过向下取整计算得出一个百分比绝对数。
      如果 MaxSurge 为 0，则此字段不能为 0。默认为 25%。
      例如：当此字段设为 30%，则在滚动更新启动时 ReplicaSet 可以立即缩容为预期 Pod 数量的 70%。
      一旦新的 Pod 就绪，ReplicaSet 可以再次缩容，接下来对新的 ReplicaSet 扩容，
      确保更新期间任何时间可用的 Pod 总数至少是预期 Pod 数量的 70%。
      
      <a name="IntOrString"></a>
      **IntOrString 是可以保存 int32 或字符串的一个类型。
      当用于 JSON 或 YAML 编组和取消编组时，它会产生或消费内部类型。
      例如，这允许你拥有一个可以接受名称或数值的 JSON 字段。**

- **revisionHistoryLimit** (int32)
  
  保留允许回滚的旧 ReplicaSet 的数量。这是一个指针，用于辨别显式零和未指定的值。默认为 10。

- **progressDeadlineSeconds** (int32)
  
  Deployment 在被视为失败之前取得进展的最大秒数。Deployment 控制器将继续处理失败的部署，
  原因为 ProgressDeadlineExceeded 的状况将被显示在 Deployment 状态中。
  请注意，在 Deployment 暂停期间将不会估算进度。默认为 600s。

- **paused** (boolean)
  
  指示部署被暂停。

## DeploymentStatus {#DeploymentStatus}

DeploymentStatus 是最近观测到的 Deployment 状态。

<hr>

- **replicas** (int32)
  
  此部署所针对的（其标签与选择算符匹配）未终止 Pod 的总数。

- **availableReplicas** (int32)
  
  此部署针对的可用（至少 minReadySeconds 才能就绪）的 Pod 总数。

- **readyReplicas** (int32)
  
  readyReplicas 是此 Deployment 在就绪状况下处理的目标 Pod 数量。

- **unavailableReplicas** (int32)
  
  此部署针对的不可用 Pod 总数。这是 Deployment 具有 100% 可用容量时仍然必需的 Pod 总数。
  它们可能是正在运行但还不可用的 Pod，也可能是尚未创建的 Pod。

- **updatedReplicas** (int32)
  
  此 Deployment 所针对的未终止 Pod 的总数，这些 Pod 采用了预期的模板规约。

- **collisionCount** (int32)
  
  供 Deployment 所用的哈希冲突计数。
  Deployment 控制器在需要为最新的 ReplicaSet 创建名称时将此字段用作冲突预防机制。

- **conditions** ([]DeploymentCondition)
  
  **补丁策略：按照键 `type` 合并**
  
  表示 Deployment 当前状态的最新可用观测值。
  
  <a name="DeploymentCondition"></a>
  **DeploymentCondition 描述某个点的部署状态。**
  

  - **conditions.status** (string)，必需
    
    状况的状态，取值为 True、False 或 Unknown 之一。
  
  - **conditions.type** (string)，必需
    
    Deployment 状况的类型。
  

  - **conditions.lastTransitionTime** (Time)
    
    状况上次从一个状态转换为另一个状态的时间。
    
    <a name="Time"></a>
    **Time 是对 time.Time 的封装。Time 支持对 YAML 和 JSON 进行正确封包。
    为 time 包的许多函数方法提供了封装器。**
  

  - **conditions.lastUpdateTime** (Time)
    
    上次更新此状况的时间。
    
    <a name="Time"></a> 
    **Time 是对 time.Time 的封装。Time 支持对 YAML 和 JSON 进行正确封包。
    为 time 包的许多函数方法提供了封装器。**
  

  - **conditions.message** (string)
    
    这是一条人类可读的消息，指示有关上次转换的详细信息。
  
  - **conditions.reason** (string)
    
    状况上次转换的原因。

- **observedGeneration** (int64)
  
  Deployment 控制器观测到的代数（Generation）。

## DeploymentList {#DeploymentList}

DeploymentList 是 Deployment 的列表。

<hr>

- **apiVersion**: apps/v1

- **kind**: DeploymentList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)
  
  标准的列表元数据。

- **items** ([]<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>)，必需
  
  items 是 Deployment 的列表。

## 操作 {#Operations}

<hr>

### `get` 读取指定的 Deployment

#### HTTP 请求

GET /apis/apps/v1/namespaces/{namespace}/deployments/{name}

#### 参数

- **name** (**路径参数**): string，必需
  
  Deployment 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): OK

401: Unauthorized

### `get` 读取指定的 Deployment 的状态

#### HTTP 请求

GET /apis/apps/v1/namespaces/{namespace}/deployments/{name}/status

#### 参数

- **name** (**路径参数**): string，必需
  
  Deployment 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): OK

401: Unauthorized

### `list` 列出或监视 Deployment 类别的对象

#### HTTP 请求

GET /apis/apps/v1/namespaces/{namespace}/deployments

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

200 (<a href="{{< ref "../workload-resources/deployment-v1#DeploymentList" >}}">DeploymentList</a>): OK

401: Unauthorized

### `list` 列出或监视 Deployment 类别的对象

#### HTTP 请求

GET /apis/apps/v1/deployments

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

200 (<a href="{{< ref "../workload-resources/deployment-v1#DeploymentList" >}}">DeploymentList</a>): OK

401: Unauthorized

### `create` 创建 Deployment

#### HTTP 请求

POST /apis/apps/v1/namespaces/{namespace}/deployments

#### 参数

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>，必需

- **dryRun** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): OK

201 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): Created

202 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): Accepted

401: Unauthorized

### `update` 替换指定的 Deployment

#### HTTP 请求

PUT /apis/apps/v1/namespaces/{namespace}/deployments/{name}

#### 参数

- **name** (**路径参数**): string，必需
  
  Deployment 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>，必需

- **dryRun** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): OK

201 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): Created

401: Unauthorized

### `update` 替换指定的 Deployment 的状态

#### HTTP 请求

PUT /apis/apps/v1/namespaces/{namespace}/deployments/{name}/status

#### 参数

- **name** (**路径参数**): string，必需
  
  Deployment 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>，必需

- **dryRun** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): OK

201 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 Deployment

#### HTTP 请求

PATCH /apis/apps/v1/namespaces/{namespace}/deployments/{name}

#### 参数

- **name** (**路径参数**): string，必需
  
  Deployment 的名称

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

200 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): OK

201 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 Deployment 的状态

#### HTTP 请求

PATCH /apis/apps/v1/namespaces/{namespace}/deployments/{name}/status

#### 参数

- **name** (**路径参数**): string，必需
  
  Deployment 的名称

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

200 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): OK

201 (<a href="{{< ref "../workload-resources/deployment-v1#Deployment" >}}">Deployment</a>): Created

401: Unauthorized

### `delete` 删除 Deployment

#### HTTP 请求

DELETE /apis/apps/v1/namespaces/{namespace}/deployments/{name}

#### 参数

- **name** (**路径参数**): string，必需
  
  Deployment 的名称

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

### `deletecollection` 删除 Deployment 的集合

#### HTTP 请求

DELETE /apis/apps/v1/namespaces/{namespace}/deployments

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
