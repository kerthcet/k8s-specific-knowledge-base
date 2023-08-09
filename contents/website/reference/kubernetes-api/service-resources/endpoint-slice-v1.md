---
api_metadata:
  apiVersion: "discovery.k8s.io/v1"
  import: "k8s.io/api/discovery/v1"
  kind: "EndpointSlice"
content_type: "api_reference"
description: "EndpointSlice 是实现某 Service 的端点的子集."
title: "EndpointSlice"
weight: 3
---


`apiVersion: discovery.k8s.io/v1`

`import "k8s.io/api/discovery/v1"`

## EndpointSlice {#EndpointSlice}

EndpointSlice 是实现某 Service 的端点的子集。一个 Service 可以有多个 EndpointSlice 对象与之对应，
必须将所有的 EndpointSlice 拼接起来才能形成一套完整的端点集合。Service 通过标签来选择 EndpointSlice。

<hr>

- **apiVersion**：discovery.k8s.io/v1

- **kind**：EndpointSlice

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。

  
  addressType 指定当前 EndpointSlice 携带的地址类型。一个 EndpointSlice 只能携带同一类型的地址。
  EndpointSlice 对象创建完成后不可以再更改 addressType 字段。
  目前支持的地址类型为：

  * IPv4：表示 IPv4 地址。
  * IPv6：表示 IPv6 地址。
  * FQDN：表示完全限定域名。


  **原子性：合并期间将被替换**

  endpoints 是当前 EndpointSlice 中一组唯一的端点。每个 EndpointSlice 最多可以包含 1000 个端点。

  <a name="Endpoint"></a>

  **端点是实现某 Service 的一个逻辑“后端”。**

    
    
    **集合：不重复的值在合并期间会被保留**

    
    本端点的地址。此字段的内容会根据对应的 EndpointSlice addressType 字段的值进行解释。
    消费者必须根据自身能力处理不同类型的地址。此字段必须至少包含 1 个地址，最多不超过 100 个地址。
    假定这些地址都是可替换的，而且客户端也可能选择只用第一个元素。参阅： https://issue.k8s.io/106267

  - **endpoints.conditions** (EndpointConditions)

    
    conditions 包含和本端点当前状态有关的信息。

    <a name="EndpointConditions"></a>

    
    **EndpointConditions 是端点的当前状况。**

    - **endpoints.conditions.ready** (boolean)  
      
      
      ready 说明此端点已经准备好根据相关的系统映射接收流量。nil 值表示状态未知。
      在大多数情况下，消费者应将这种未知状态视为就绪（ready）。
      考虑到兼容性，对于正在结束状态下的端点，永远不能将 ready 设置为“true”，
      除非正常的就绪行为被显式覆盖，例如当关联的服务设置了 publishNotReadyAddresses 标志时。

    - **endpoints.conditions.serving** (boolean)
      
      
      serving 和 ready 非常相似。唯一的不同在于,
      即便某端点的状态为 Terminating 也可以设置 serving。
      对于处在终止过程中的就绪端点，此状况应被设置为 “true”。
      如果设置为 nil，则消费者应该以 ready 值为准。

    - **endpoints.conditions.terminating** (boolean)
      
      
      terminating 说明当前端点正在终止过程中。nil 值表示状态未知。
      消费者应将这种未知状态视为端点并不处于终止过程中。

  - **endpoints.deprecatedTopology** (map[string]string)
    
    
    deprecatedTopology 包含 v1beta1 API 的拓扑信息部分。目前已经弃用了此字段，
    移除 v1beta1 API 时（不早于 Kubernetes v1.24）会一起移除此字段。
    此字段目前仍然可以存储值，但是不能通过 v1 API 写入数据。
    向此字段写入数据的任何尝试都会被忽略，并且不会通知用户。
    移除此字段后，可以在 zone 和 nodeName 字段中查看拓扑信息。

  - **endpoints.hints** (EndpointHints)

    
    hints 是关于应该如何使用某端点的提示信息。

    <a name="EndpointHints"></a>

    
    **EndpointHints 提供应该如何使用某端点的提示信息。**

    - **endpoints.hints.forZones** ([]ForZone)

      
      **原子性：合并期间将被替换**

      
      forZones 表示应该由哪个可用区调用此端点从才能激活拓扑感知路由。

      <a name="ForZone"></a>

      
      **ForZone 指示应该由哪些可用区调度此端点。**


        
        name 代表可用区的名称。

  - **endpoints.hostname** (string)

    
    此端点的主机名称。端点的使用者可以通过此字段区分各个端点（例如，通过 DNS 域名）。
    使用同一主机名称的多个端点应被视为可替换（例如，DNS 中的多个 A 记录）。
    必须为小写字母，并且需要通过 DNS Label (RFC 1123) 验证。

  - **endpoints.nodeName** (string)

    
    nodeName 是托管此端点的 Node 的名称，使用 nodeName 可以决定 Node 本地有哪些端点。

  - **endpoints.targetRef** (<a href="{{< ref "../common-definitions/object-reference#ObjectReference" >}}">ObjectReference</a>)

    
    targetRef 是对代表此端点的 Kubernetes 对象的引用。

  - **endpoints.zone** (string)

    
    zone 是此端点所在的可用区（Zone）的名称。

- **ports** ([]EndpointPort)

  
  **原子性：合并期间会被替代**
  
  
  ports 列出了当前 EndpointSlice 中各个端点所暴露的网络端口。每个端口的名称不得重复。
  当 ports 列表为空时，表示没有已经指定暴露哪些端口。如果端口值被定义为 nil，表示暴露“所有端口”。
  每个 EndpointSlice 最多可以包含 100 个端口。

  <a name="EndpointPort"></a>

  
  **EndpointPort 是 EndpointSlice 使用的端口。**

  - **ports.port** (int32)

    
    port 表示端点的端口号。如果未指定，就不限制端口，且必须根据消费者的具体环境进行解释。

  - **ports.protocol** (string)

    
    protocol 表示此端口的 IP 协议。必须为 UDP、TCP 或 SCTP。默认为 TCP。

  - **ports.name** (string)

    
    name 表示此端口的名称。EndpointSlice 中所有端口的名称都不得重复。
    如果 EndpointSlice 是基于 Kubernetes Service 创建的，
    那么此端口的名称和 Service.ports[].name 字段的值一致。默认为空字符串。
    名称必须是空字符串，或者必须通过 DNS_LABEL 验证：
    
    * 最多包含 63 个字符。
    * 必须包含英文小写字母或'-'。
    * 必须以字母开头并以字母结尾。

  - **ports.appProtocol** (string)


    此端口的应用层协议。字段值被用作提示，允许协议实现为其所理解的协议提供更丰富的行为。
    此字段遵循标准的 Kubernetes 标签句法。有效的取值是：

    * 不带前缀的协议名 - 是 IANA 标准服务的保留名称（参见 RFC-6335 和 https://www.iana.org/assignments/service-names）。

    * Kubernetes 定义的前缀名称：
      * 'kubernetes.io/h2c' - 使用明文的 HTTP/2 协议，详见 https://www.rfc-editor.org/rfc/rfc7540

    * 其他协议应该使用带前缀的名称，例如 mycompany.com/my-custom-protocol。

## EndpointSliceList {#EndpointSliceList}

EndpointSliceList 是 EndpointSlice 的列表。

<hr>

- **apiVersion**：discovery.k8s.io/v1

- **kind**：EndpointSliceList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据


  items 是 EndpointSlice 列表

## 操作 {#操作}

<hr>

### `get` 读取指定的 EndpointSlice

#### HTTP 请求

GET /apis/discovery.k8s.io/v1/namespaces/{namespace}/endpointslices/{name}

#### 参数

- **name** (**路径参数**)：string, 必需

  EndpointSlice 的名称

- **namespace** (**路径参数**)：string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/endpoint-slice-v1#EndpointSlice" >}}">EndpointSlice</a>)：OK

401：Unauthorized

### `list` 列举或监测 EndpointSlice 类别的对象

#### HTTP 请求

GET /apis/discovery.k8s.io/v1/namespaces/{namespace}/endpointslices

#### 参数

- **namespace** (**路径参数**)：string, 必需

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

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../service-resources/endpoint-slice-v1#EndpointSliceList" >}}">EndpointSliceList</a>): OK

401：Unauthorized

### `list` 列举或监测 EndpointSlice 类别的对象

#### HTTP 请求

GET /apis/discovery.k8s.io/v1/endpointslices

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

- **resourceVersionMatch** (*查询参数*)：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../service-resources/endpoint-slice-v1#EndpointSliceList" >}}">EndpointSliceList</a>)：OK

401：Unauthorized

### `create` 创建 EndpointSlice

#### HTTP 请求

POST /apis/discovery.k8s.io/v1/namespaces/{namespace}/endpointslices

#### 参数

- **namespace** (**路径参数**)：string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **dryRun** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/endpoint-slice-v1#EndpointSlice" >}}">EndpointSlice</a>)：OK

201 (<a href="{{< ref "../service-resources/endpoint-slice-v1#EndpointSlice" >}}">EndpointSlice</a>)：Created

202 (<a href="{{< ref "../service-resources/endpoint-slice-v1#EndpointSlice" >}}">EndpointSlice</a>)：Accepted

401：Unauthorized

### `update` 替换指定的 EndpointSlice

#### HTTP 请求

PUT /apis/discovery.k8s.io/v1/namespaces/{namespace}/endpointslices/{name}

#### 参数

- **name** (**路径参数**)：string, 必需

  EndpointSlice 的名称

- **namespace** (**路径参数**)：string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **dryRun** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**)：string-

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/endpoint-slice-v1#EndpointSlice" >}}">EndpointSlice</a>)：OK

201 (<a href="{{< ref "../service-resources/endpoint-slice-v1#EndpointSlice" >}}">EndpointSlice</a>)：Created

401：Unauthorized

### `patch` 部分更新指定的 EndpointSlice

#### HTTP 请求

PATCH /apis/discovery.k8s.io/v1/namespaces/{namespace}/endpointslices/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  EndpointSlice 的名称

- **namespace** (**路径参数**)：string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


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

200 (<a href="{{< ref "../service-resources/endpoint-slice-v1#EndpointSlice" >}}">EndpointSlice</a>)：OK

201 (<a href="{{< ref "../service-resources/endpoint-slice-v1#EndpointSlice" >}}">EndpointSlice</a>)：Created

401：Unauthorized

### `delete` 删除 EndpointSlice

#### HTTP 请求

DELETE /apis/discovery.k8s.io/v1/namespaces/{namespace}/endpointslices/{name}

#### 参数

- **name** (**路径参数**)：string, 必需

  EndpointSlice 的名称

- **namespace** (**路径参数**)：string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**：<a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>)：OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>)：Accepted

401：Unauthorized

### `deletecollection` 删除 EndpointSlice 的集合

#### HTTP 请求

DELETE /apis/discovery.k8s.io/v1/namespaces/{namespace}/endpointslices

#### 参数

- **namespace** (**路径参数**)：string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**：<a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

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

- **resourceVersionMatch** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>)：OK

401：Unauthorized

