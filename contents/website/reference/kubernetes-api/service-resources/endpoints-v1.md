---
api_metadata:
  apiVersion: "v1"
  import: "k8s.io/api/core/v1"
  kind: "Endpoints"
content_type: "api_reference"
description: "Endpoints 是实现实际服务的端点的集合。"
title: "Endpoints"
weight: 2
---

`apiVersion: v1`

`import "k8s.io/api/core/v1"`

## Endpoints {#Endpoints}

Endpoints 是实现实际服务的端点的集合。举例:

	 Name: "mysvc",
	 Subsets: [
	   {
	     Addresses: [{"ip": "10.10.1.1"}, {"ip": "10.10.2.2"}],
	     Ports: [{"name": "a", "port": 8675}, {"name": "b", "port": 309}]
	   },
	   {
	     Addresses: [{"ip": "10.10.3.3"}],
	     Ports: [{"name": "a", "port": 93}, {"name": "b", "port": 76}]
	   },
	]

<hr>

- **apiVersion**: v1

- **kind**: Endpoints

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **subsets** ([]EndpointSubset)

  所有端点的集合是所有 subsets 的并集。不同地址会根据其 IP 地址被放入不同子集。
  对于具有多个端口的单个地址，如果其中一些端口已就绪，而另一些端口未就绪（因为它们来自不同的容器），
  将导致地址显示在不同端口的不同子集中。
  任何地址都不可以同时出现在 addresses 和 notReadyAddress 中的相同子集内。

  <a name="EndpointSubset"></a>
  **EndpointSubset 是一组具有公共端口集的地址。扩展的端点集是 addresses 和 ports 的笛卡尔乘积。例如假设：**

  	{
  	  Addresses: [{"ip": "10.10.1.1"}, {"ip": "10.10.2.2"}],
  	  Ports:     [{"name": "a", "port": 8675}, {"name": "b", "port": 309}]
  	}

  则最终的端点集可以看作:


  	a: [ 10.10.1.1:8675, 10.10.2.2:8675 ],
  	b: [ 10.10.1.1:309, 10.10.2.2:309 ]*


  - **subsets.addresses** ([]EndpointAddress)
  

    提供标记为就绪的相关端口的 IP 地址。
    这些端点应该被认为是负载均衡器和客户端可以安全使用的。


    <a name="EndpointAddress"></a>
    **EndpointAddress 是描述单个 IP 地址的元组。**


    - **subsets.addresses.ip** (string), 必需

      端点的 IP。不可以是本地回路（127.0.0.0/8 或 ::1）、
      链路本地（169.254.0.0/16 或 fe80::/10）或链路本地多播（224.0.0.0/24
      或 ff02::/16)）地址。

    - **subsets.addresses.hostname** (string)
      

      端点主机名称。

    - **subsets.addresses.nodeName** (string)
      

      可选：承载此端点的节点。此字段可用于确定一个节点的本地端点。

    - **subsets.addresses.targetRef** (<a href="{{< ref "../common-definitions/object-reference#ObjectReference" >}}">ObjectReference</a>)


      对提供端点的对象的引用。
            
  - **subsets.notReadyAddresses** ([]EndpointAddress)


    提供相关端口但由于尚未完成启动、最近未通过就绪态检查或最近未通过活跃性检查而被标记为当前未就绪的 IP 地址。
    <a name="EndpointAddress"></a>
    **EndpointAddress 是描述单个 IP 地址的元组。**


    - **subsets.notReadyAddresses.ip** (string), 必需

      端点的 IP。不可以是本地环路（127.0.0.0/8 或 ::1）、
      链路本地（169.254.0.0/16 或 fe80::/10）或链路本地多播（224.0.0.0/24
      或 ff02::/16）地址。

    - **subsets.notReadyAddresses.hostname** (string)


      端点主机名称。

    - **subsets.notReadyAddresses.nodeName** (string)
    

      可选：承载此端点的节点。此字段可用于确定节点的本地端点。

    - **subsets.notReadyAddresses.targetRef** (<a href="{{< ref "../common-definitions/object-reference#ObjectReference" >}}">ObjectReference</a>)


      对提供端点的对象的引用。

  - **subsets.ports** ([]EndpointPort)


    相关 IP 地址上可用的端口号。
    

    <a name="EndpointPort"></a>
    **EndpointPort 是描述单个端口的元组。**


    - **subsets.ports.port** (int32), 必需

      端点的端口号。

    - **subsets.ports.protocol** (string)


      此端口的 IP 协议。必须是 UDP、TCP 或 SCTP。默认值为 TCP。
      
    - **subsets.ports.name** (string)
    

      端口的名称。此字段必须与相应 ServicePort 中的 `name` 字段匹配。必须是 DNS_LABEL。
      仅当定义了一个端口时才可选。

    - **subsets.ports.appProtocol** (string)
      

      端口的应用程序协议。这被用作实现的提示，为他们理解的协议提供更丰富的行为。
      此字段遵循标准的 Kubernetes 标签语法。有效值为：

      
      * 未加前缀的名称保留给 IANA 标准服务名称（遵循 RFC-6335 和 https://www.iana.org/assignments/service-names)。
      
      * Kubernetes 定义的前缀名称
        * 'kubernetes.io/h2c' - HTTP/2 明文，如 https://www.rfc-editor.org/rfc/rfc7540 中所述
    
      * 其他协议应使用实现定义的前缀名称，如 mycompany.com/my-custom-protocol。

## EndpointsList {#EndpointsList}

EndpointsList 是端点列表。

<hr>

- **apiVersion**: v1

- **kind**: EndpointsList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **items** ([]<a href="{{< ref "../service-resources/endpoints-v1#Endpoints" >}}">Endpoints</a>), 必需

  端点列表。 

## 操作 {#Operations}

<hr>

### `get` 读取指定的 Endpoints

#### HTTP 请求

GET /api/v1/namespaces/{namespace}/endpoints/{name}

#### 参数

- **name** (**路径参数**)：string，必需

  Endpoints 的名称。

- **namespace** (**路径参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/endpoints-v1#Endpoints" >}}">Endpoints</a>): OK

401: Unauthorized

### `list` 列出或监测 Endpoints 类型的对象

#### HTTP 请求

GET /api/v1/namespaces/{namespace}/endpoints

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

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../service-resources/endpoints-v1#EndpointsList" >}}">EndpointsList</a>): OK

401: Unauthorized

### `list` 列出或监测 Endpoints 类型的对象

#### HTTP 请求

GET /api/v1/endpoints

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

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../service-resources/endpoints-v1#EndpointsList" >}}">EndpointsList</a>): OK

401: Unauthorized

### `create` 创建 Endpoints

#### HTTP 请求

POST /api/v1/namespaces/{namespace}/endpoints

#### 参数

- **namespace** (**路径参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../service-resources/endpoints-v1#Endpoints" >}}">Endpoints</a>, 必需

- **dryRun** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/endpoints-v1#Endpoints" >}}">Endpoints</a>): OK

201 (<a href="{{< ref "../service-resources/endpoints-v1#Endpoints" >}}">Endpoints</a>): Created

202 (<a href="{{< ref "../service-resources/endpoints-v1#Endpoints" >}}">Endpoints</a>): Accepted

401: Unauthorized

### `update` 替换指定的 Endpoints

#### HTTP 请求

PUT /api/v1/namespaces/{namespace}/endpoints/{name}

#### 参数

- **name** (**路径参数**)：string，必需
 
  Endpoints 名称

- **namespace** (**路径参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../service-resources/endpoints-v1#Endpoints" >}}">Endpoints</a>, required

- **dryRun** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/endpoints-v1#Endpoints" >}}">Endpoints</a>): OK

201 (<a href="{{< ref "../service-resources/endpoints-v1#Endpoints" >}}">Endpoints</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 Endpoints

#### HTTP 请求

PATCH /api/v1/namespaces/{namespace}/endpoints/{name}

#### 参数

- **name** (**路径参数**)：string，必需

  Endpoints 名称

- **namespace** (**路径参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, 必需
  
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

200 (<a href="{{< ref "../service-resources/endpoints-v1#Endpoints" >}}">Endpoints</a>): OK

201 (<a href="{{< ref "../service-resources/endpoints-v1#Endpoints" >}}">Endpoints</a>): Created

401: Unauthorized

### `delete` 删除 Endpoints

#### HTTP 请求

DELETE /api/v1/namespaces/{namespace}/endpoints/{name}

#### 参数

- **name** (**路径参数**)：string，必需

  Endpoints 名称

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

### `deletecollection` 删除 Endpoints 组

#### HTTP 请求

DELETE /api/v1/namespaces/{namespace}/endpoints

#### 参数

- **namespace** (**路径参数**)：string，必需

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

- **resourceVersionMatch** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
