---
api_metadata:
  apiVersion: "events.k8s.io/v1"
  import: "k8s.io/api/events/v1"
  kind: "Event"
content_type: "api_reference"
description: "Event 是集群中某个事件的报告。"
title: "Event"
weight: 3
---


`apiVersion: events.k8s.io/v1`

`import "k8s.io/api/events/v1"`

## Event {#Event}
Event 是集群中某个事件的报告。它一般表示系统的某些状态变化。
Event 的保留时间有限，触发器和消息可能会随着时间的推移而演变。
事件消费者不应假定给定原因的事件的时间所反映的是一致的下层触发因素，或具有该原因的事件的持续存在。
Events 应被视为通知性质的、尽最大努力而提供的补充数据。

<hr>

- **apiVersion**: events.k8s.io/v1

- **kind**: Event

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata


- **eventTime** (MicroTime)，必需

  evenTime 是该事件首次被观察到的时间。它是必需的。

  <a name="MicroTime"></a>

  
  **MicroTime 是微秒级精度的 Time 版本**

- **action** (string)

  action 是针对相关对象所采取的或已失败的动作。字段值是机器可读的。对于新的 Event，此字段不能为空，
  且最多为 128 个字符。

- **deprecatedCount** (int32)

  deprecatedCount 是确保与 core.v1 Event 类型向后兼容的已弃用字段。

- **deprecatedFirstTimestamp** (Time)

  deprecatedFirstTimestamp 是确保与 core.v1 Event 类型向后兼容的已弃用字段。

  <a name="Time"></a>
  
  **Time 是对 time.Time 的封装。Time 支持对 YAML 和 JSON 进行正确封包。为 time 包的许多函数方法提供了封装器。**

- **deprecatedLastTimestamp** (Time)

  deprecatedLastTimestamp 是确保与 core.v1 Event 类型向后兼容的已弃用字段。

  <a name="Time"></a>

  **Time 是对 time.Time 的封装。Time 支持对 YAML 和 JSON 进行正确封包。为 time 包的许多函数方法提供了封装器。**

- **deprecatedSource** (EventSource)

  deprecatedSource 是确保与 core.v1 Event 类型向后兼容的已弃用字段。

  <a name="EventSource"></a>
  

  **EventSource 包含事件信息。**

  - **deprecatedSource.component** (string)


    生成事件的组件。

  - **deprecatedSource.host** (string)


    产生事件的节点名称。

- **note** (string)

  node 是对该操作状态的可读描述。注释的最大长度是 1kB，但是库应该准备好处理最多 64kB 的值。

- **reason** (string)

  reason 是采取行动的原因。它是人类可读的。对于新的 Event，此字段不能为空，且最多为128个字符。

- **regarding** (<a href="{{< ref "../common-definitions/object-reference#ObjectReference" >}}">ObjectReference</a>)

  关于包含此 Event 所涉及的对象。在大多数情况下，所指的是报告事件的控制器所实现的一个 Object。
  例如 ReplicaSetController 实现了 ReplicaSet，这个事件被触发是因为控制器对 ReplicaSet 对象做了一些变化。

- **related** (<a href="{{< ref "../common-definitions/object-reference#ObjectReference" >}}">ObjectReference</a>)

  related 是用于更复杂操作的、可选的、从属性的对象。例如，当 regarding 对象触发 related 对象的创建或删除时。

- **reportingController** (string)

  reportingController 是触发该事件的控制器的名称,例如 `kubernetes.io/kubelet`。对于新的　Event，此字段不能为空。

- **reportingInstance** (string)

  reportingInstance 为控制器实例的 ID,例如 `kubelet-xyzf`。对于新的 Event，此字段不能为空，且最多为 128 个字符。 

- **series** (EventSeries)

  series 是该事件代表的事件系列的数据，如果是单事件，则为 nil。

  <a name="EventSeries"></a>

  EventSeries 包含一系列事件的信息，即一段时间内持续发生的事情。
  EventSeries 的更新频率由事件报告者决定。
  默认事件报告程序在 "k8s.io/client-go/tools/events/event_broadcaster.go" 
  展示在发生心跳时该结构如何被更新，可以指导定制的报告者实现。


  - **series.count** (int32)，必需

    
    count 是到最后一次心跳时间为止在该系列中出现的次数。


  - **series.lastObservedTime** (MicroTime)，必需

    lastObservedTime 是在最后一次心跳时间之前看到最后一个 Event 的时间。

    <a name="MicroTime"></a>


    **MicroTime 是微秒级精度的 Time 版本。**

- **type** (string)

  type 是该事件的类型（Normal、Warning），未来可能会添加新的类型。字段值是机器可读的。
  对于新的 Event，此字段不能为空。

## EventList {#EventList}

EventList 是一个 Event 对象列表。

<hr>

- **apiVersion**: events.k8s.io/v1

- **kind**: EventList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

   标准的列表元数据。更多信息: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../cluster-resources/event-v1#Event" >}}">Event</a>)，必需

  items 是模式（Schema）对象的列表。

## 操作 {#操作}

<hr>

### `get` 读取特定 Event

#### HTTP 请求

GET /apis/events.k8s.io/v1/namespaces/{namespace}/events/{name}

#### 参数

- **name** (**路径参数**)：string，必需

  Event 名称

- **namespace** (**路径参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**路径参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/event-v1#Event" >}}">Event</a>): OK

401: Unauthorized

### `list` 列出或观察事件类型对象

#### HTTP 请求

GET /apis/events.k8s.io/v1/namespaces/{namespace}/events

#### 参数

- **namespace** (**路径参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **allowWatchBookmarks** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**)： boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/event-v1#EventList" >}}">EventList</a>): OK

401: Unauthorized

### `list` 列出或观察事件类型对象

#### HTTP 请求

GET /apis/events.k8s.io/v1/events

#### 参数

- **allowWatchBookmarks** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**)： boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/event-v1#EventList" >}}">EventList</a>): OK

401: Unauthorized

### `create` 创建一个 Event

#### HTTP 请求

POST /apis/events.k8s.io/v1/namespaces/{namespace}/events

#### 参数

- **namespace** (**查询参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../cluster-resources/event-v1#Event" >}}">Event</a>，必需

- **dryRun** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/event-v1#Event" >}}">Event</a>): OK

201 (<a href="{{< ref "../cluster-resources/event-v1#Event" >}}">Event</a>): Created

202 (<a href="{{< ref "../cluster-resources/event-v1#Event" >}}">Event</a>): Accepted

401: Unauthorized

### `update` 替换指定 Event

#### HTTP 请求

PUT /apis/events.k8s.io/v1/namespaces/{namespace}/events/{name}
#### 参数

- **name** (**路径参数**)：string，必需

  Event 名称

- **namespace** (**路径参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**：<a href="{{< ref "../cluster-resources/event-v1#Event" >}}">Event</a>，必需
  
- **dryRun** (**查询参数**)：必需

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/event-v1#Event" >}}">Event</a>): OK

201 (<a href="{{< ref "../cluster-resources/event-v1#Event" >}}">Event</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 Event

#### HTTP 请求

PATCH /apis/events.k8s.io/v1/namespaces/{namespace}/events/{name}

#### 参数

- **name** (**路径参数**)：string，必需

  Event 名称

- **namespace** (**路径参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

  
- **dryRun** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/event-v1#Event" >}}">Event</a>): OK

201 (<a href="{{< ref "../cluster-resources/event-v1#Event" >}}">Event</a>): Created

401: Unauthorized

### `delete` 删除 Event

#### HTTP 请求

DELETE /apis/events.k8s.io/v1/namespaces/{namespace}/events/{name}

#### 参数

- **name** (**路径参数**)：string，必需

  Event 名称

- **namespace** (**路径参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 Event 集合

#### HTTP 请求

DELETE /apis/events.k8s.io/v1/namespaces/{namespace}/events

#### 参数

- **namespace** (*in path*)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **continue** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **dryRun** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldSelector** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **gracePeriodSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **labelSelector** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

- **resourceVersion** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (*查询参数*)：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**)： boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized

