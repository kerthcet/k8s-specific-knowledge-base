---
api_metadata:
  apiVersion: "flowcontrol.apiserver.k8s.io/v1beta3"
  import: "k8s.io/api/flowcontrol/v1beta3"
  kind: "PriorityLevelConfiguration"
content_type: "api_reference"
description: "PriorityLevelConfiguration 表示一个优先级的配置。"
title: "PriorityLevelConfiguration v1beta3"
weight: 8
---

`apiVersion: flowcontrol.apiserver.k8s.io/v1beta3`

`import "k8s.io/api/flowcontrol/v1beta3"`

## PriorityLevelConfiguration {#PriorityLevelConfiguration}

PriorityLevelConfiguration 表示一个优先级的配置。

<hr>

- **apiVersion**: flowcontrol.apiserver.k8s.io/v1beta3

- **kind**: PriorityLevelConfiguration

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)
  
  `metadata` 是标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfigurationSpec" >}}">PriorityLevelConfigurationSpec</a>)
  
  `spec` 是 “request-priority” 预期行为的规约。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

- **status** (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfigurationStatus" >}}">PriorityLevelConfigurationStatus</a>)
  
  `status` 是 “请求优先级” 的当前状况。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

## PriorityLevelConfigurationSpec {#PriorityLevelConfigurationSpec}

PriorityLevelConfigurationSpec 指定一个优先级的配置。

<hr>

- **type** (string)，必需
  
  `type` 指示此优先级是否遵从有关请求执行的限制。
  取值为 `"Exempt"` 意味着此优先级的请求不遵从某个限制（且因此从不排队）且不会减损其他优先级可用的容量。
  取值为 `"Limited"` 意味着 (a) 此优先级的请求遵从这些限制且
  (b) 服务器某些受限的容量仅可用于此优先级。必需。

- **limited** (LimitedPriorityLevelConfiguration)
  
  `limited` 指定如何为某个受限的优先级处理请求。
  当且仅当 `type` 是 `"Limited"` 时，此字段必须为非空。
  
  <a name="LimitedPriorityLevelConfiguration"></a>
  LimitedPriorityLevelConfiguration 指定如何处理需要被限制的请求。它解决两个问题：
  * 如何限制此优先级的请求？
  * 应如何处理超出此限制的请求？
  
  
  - **limited.borrowingLimitPercent** (int32)
   
    `borrowingLimitPercent` 配置如果存在，则可用来限制此优先级级别可以从其他优先级级别中租借多少资源。
    该限制被称为该级别的 BorrowingConcurrencyLimit（BorrowingCL），它限制了该级别可以同时租借的资源总数。
    该字段保存了该限制与该级别标称并发限制之比。当此字段非空时，必须为正整数，并按以下方式计算限制值：

    BorrowingCL(i) = round(NominalCL(i) * borrowingLimitPercent(i) / 100.0)

    该字段值可以大于100，表示该优先级可以大于自己标称并发限制（NominalCL）。当此字段为 `nil` 时，表示无限制。
  
  
  - **limited.lendablePercent** (int32)

    `lendablePercent` 规定了 NominalCL 可被其他优先级级别租借资源数百分比。
    此字段的值必须在 0 到 100 之间，包括 0 和 100，默认为 0。
    其他级别可以从该级别借用的资源数被称为此级别的 LendableConcurrencyLimit（LendableCL），定义如下。

    LendableCL(i) = round( NominalCL(i) * lendablePercent(i)/100.0 )
  

  - **limited.limitResponse** (LimitResponse)
    
    `limitResponse` 指示如何处理当前无法立即执行的请求。
    
    <a name="LimitResponse"></a>
    **LimitResponse 定义如何处理当前无法立即执行的请求。**
    

    - **limited.limitResponse.type** (string)，必需
      
      `type` 是 “Queue” 或 “Reject”。此字段必须设置。
      “Queue” 意味着在到达时无法被执行的请求可以被放到队列中，直到它们被执行或者队列长度超出限制为止。
      “Reject” 意味着到达时无法执行的请求将被拒绝。
    

    - **limited.limitResponse.queuing** (QueuingConfiguration)
      
      `queuing` 包含排队所用的配置参数。只有 `type` 是 `"Queue"` 时，此字段才可以为非空。
      
      <a name="QueuingConfiguration"></a>
      **QueuingConfiguration 保存排队所用的配置参数。**
      

      - **limited.limitResponse.queuing.handSize** (int32)
        
        `handSize` 是一个小的正数，用于配置如何将请求随机分片到队列中。
        当以该优先级将请求排队时，将对请求的流标识符（字符串对）进行哈希计算，
        该哈希值用于打乱队列队列的列表，并处理此处指定的一批请求。
        请求被放入这一批次中最短的队列中。
        `handSize` 不得大于 `queues`，并且应该明显更小（以便几个大的流量不会使大多数队列饱和）。
        有关设置此字段的更多详细指导，请参阅面向用户的文档。此字段的默认值为 8。
      

      - **limited.limitResponse.queuing.queueLengthLimit** (int32)
        
        `queueLengthLimit` 是任意时刻允许在此优先级的给定队列中等待的请求数上限；
        额外的请求将被拒绝。
        此值必须是正数。如果未指定，则默认为 50。
      
      - **limited.limitResponse.queuing.queues** (int32)
        
        `queues` 是这个优先级的队列数。此队列在每个 API 服务器上独立存在。此值必须是正数。
        将其设置为 1 相当于禁止了混洗分片操作，进而使得对相关流模式的区分方法不再有意义。
        此字段的默认值为 64。


  - **limited.nominalConcurrencyShares** (int32)

    `nominalConcurrencyShares`（NCS）用于计算该优先级级别的标称并发限制（NominalCL）。
     NCS 表示可以在此优先级级别同时运行的席位数量上限，包括来自本优先级级别的请求，
     以及从此优先级级别租借席位的其他级别的请求。
     服务器的并发度限制（ServerCL）根据 NCS 值按比例分别给各 Limited 优先级级别：

     NominalCL(i)  = ceil( ServerCL * NCS(i) / sum_ncs ) sum_ncs = sum[limited priority level k] NCS(k)

     较大的数字意味着更大的标称并发限制（NominalCL），但是这将牺牲其他 Limited 优先级级别的资源。该字段的默认值为 30。

## PriorityLevelConfigurationStatus {#PriorityLevelConfigurationStatus}

PriorityLevelConfigurationStatus 表示 “请求优先级” 的当前状况。

<hr>

- **conditions** ([]PriorityLevelConfigurationCondition)
  
  **Map：合并期间保留根据键 type 保留其唯一值**
  
  `conditions` 是 “请求优先级” 的当前状况。
  
  <a name="PriorityLevelConfigurationCondition"></a>
  **PriorityLevelConfigurationCondition 定义优先级的状况。**
  

  - **conditions.lastTransitionTime** (Time)
    
    `lastTransitionTime` 是状况上次从一个状态转换为另一个状态的时间。
    
    <a name="Time"></a>
    **Time 是对 time.Time 的封装。Time 支持对 YAML 和 JSON 进行正确封包。
    为 time 包的许多函数方法提供了封装器。**
  

  - **conditions.message** (string)
    
    `message` 是人类可读的消息，指示有关上次转换的详细信息。
  
  - **conditions.reason** (string)
    
    `reason` 是状况上次转换原因的、驼峰格式命名的、唯一的一个词。
  

  - **conditions.status** (string)
    
    `status` 表示状况的状态，取值为 True、False 或 Unknown 之一。必需。
  
  - **conditions.type** (string)
    
    `type` 表示状况的类型，必需。

## PriorityLevelConfigurationList {#PriorityLevelConfigurationList}

PriorityLevelConfigurationList 是 PriorityLevelConfiguration 对象的列表。

<hr>

- **apiVersion**: flowcontrol.apiserver.k8s.io/v1beta3

- **kind**: PriorityLevelConfigurationList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)
  
  `metadata` 是标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>)，必需
  
  `items` 是请求优先级设置的列表。

## 操作 {#Operations}

<hr>

### `get` 读取指定的 PriorityLevelConfiguration

#### HTTP 请求

GET /apis/flowcontrol.apiserver.k8s.io/v1beta3/prioritylevelconfigurations/{name}

#### 参数

- **name** (**路径参数**): string，必需
  
  PriorityLevelConfiguration 的名称

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

401: Unauthorized

### `get` 读取指定的 PriorityLevelConfiguration 的状态

#### HTTP 请求

GET /apis/flowcontrol.apiserver.k8s.io/v1beta3/prioritylevelconfigurations/{name}/status

#### 参数

- **name** (**路径参数**): string，必需
  
  PriorityLevelConfiguration 的名称

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

401: Unauthorized

### `list` 列出或监视 PriorityLevelConfiguration 类别的对象

#### HTTP 请求

GET /apis/flowcontrol.apiserver.k8s.io/v1beta3/prioritylevelconfigurations

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

200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfigurationList" >}}">PriorityLevelConfigurationList</a>): OK

401: Unauthorized

### `create` 创建 PriorityLevelConfiguration

#### HTTP 请求

POST /apis/flowcontrol.apiserver.k8s.io/v1beta3/prioritylevelconfigurations

#### 参数

- **body**: <a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>，必需

- **dryRun** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

201 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): Created

202 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): Accepted

401: Unauthorized

### `update` 替换指定的 PriorityLevelConfiguration

#### HTTP 请求

PUT /apis/flowcontrol.apiserver.k8s.io/v1beta3/prioritylevelconfigurations/{name}

#### 参数

- **name** (**路径参数**): string，必需
  
  PriorityLevelConfiguration 的名称

- **body**: <a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>，必需

- **dryRun** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

201 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): Created

401: Unauthorized

### `update` 替换指定的 PriorityLevelConfiguration 的状态

#### HTTP 请求

PUT /apis/flowcontrol.apiserver.k8s.io/v1beta3/prioritylevelconfigurations/{name}/status

#### 参数

- **name** (**路径参数**): string，必需
  
  PriorityLevelConfiguration 的名称

- **body**: <a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>，必需

- **dryRun** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

201 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 PriorityLevelConfiguration

#### HTTP 请求

PATCH /apis/flowcontrol.apiserver.k8s.io/v1beta3/prioritylevelconfigurations/{name}

#### 参数

- **name** (**路径参数**): string，必需
  
  PriorityLevelConfiguration 的名称

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

200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

201 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 PriorityLevelConfiguration 的状态

#### HTTP 请求

PATCH /apis/flowcontrol.apiserver.k8s.io/v1beta3/prioritylevelconfigurations/{name}/status

#### 参数

- **name** (**路径参数**): string，必需
  
  PriorityLevelConfiguration 的名称

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

200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

201 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta3#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): Created

401: Unauthorized

### `delete` 删除 PriorityLevelConfiguration

#### HTTP 请求

DELETE /apis/flowcontrol.apiserver.k8s.io/v1beta3/prioritylevelconfigurations/{name}

#### 参数

- **name** (**路径参数**): string，必需
  
  PriorityLevelConfiguration 的名称

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

### `deletecollection` 删除 PriorityLevelConfiguration 的集合

#### HTTP 请求

DELETE /apis/flowcontrol.apiserver.k8s.io/v1beta3/prioritylevelconfigurations

#### 参数

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
