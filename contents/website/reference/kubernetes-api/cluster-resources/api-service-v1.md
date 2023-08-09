---
api_metadata:
  apiVersion: "apiregistration.k8s.io/v1"
  import: "k8s.io/kube-aggregator/pkg/apis/apiregistration/v1"
  kind: "APIService"
content_type: "api_reference"
description: "APIService 是用来表示一个特定的 GroupVersion 的服务器"
title: "APIService"
weight: 4
---


`apiVersion: apiregistration.k8s.io/v1`

`import "k8s.io/kube-aggregator/pkg/apis/apiregistration/v1"`


## APIService {#APIService}

APIService 是用来表示一个特定的 GroupVersion 的服务器。名称必须为 "version.group"。

<hr>

- **apiVersion**: apiregistration.k8s.io/v1

- **kind**: APIService

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)
  标准的对象元数据。更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../cluster-resources/api-service-v1#APIServiceSpec" >}}">APIServiceSpec</a>)
  spec 包含用于定位和与服务器通信的信息

- **status** (<a href="{{< ref "../cluster-resources/api-service-v1#APIServiceStatus" >}}">APIServiceStatus</a>)
  status 包含某 API 服务器的派生信息


## APIServiceSpec {#APIServiceSpec}
APIServiceSpec 包含用于定位和与服务器通信的信息。仅支持 HTTPS 协议，但是你可以禁用证书验证。

<hr>

  groupPriorityMininum 是这个组至少应该具有的优先级。优先级高表示客户端优先选择该组。
  请注意，该组的其他版本可能会指定更高的 groupPriorityMininum 值，使得整个组获得更高的优先级。
  主排序基于 groupPriorityMinimum 值，从高到低排序（20 在 10 之前）。
  次要排序基于对象名称的字母顺序（v1.bar 在 v1.foo 之前）。
  我们建议这样配置：`*.k8s.io`（扩展除外）值设置为 18000，PaaS（OpenShift、Deis）建议值为 2000 左右。

  versionPriority 控制该 API 版本在其组中的排序，必须大于零。主排序基于 versionPriority，
  从高到低排序（20 在 10 之前）。因为在同一个组里，这个数字可以很小，可能是几十。
  在版本优先级相等的情况下，版本字符串将被用来计算组内的顺序。如果版本字符串是与 Kubernetes 的版本号形式类似，
  则它将排序在 Kubernetes 形式版本字符串之前。Kubernetes 的版本号字符串按字典顺序排列。
  Kubernetes 版本号以 “v” 字符开头，后面是一个数字（主版本），然后是可选字符串 “alpha” 或 “beta” 和另一个数字（次要版本）。
  它们首先按 GA > beta > alpha 排序（其中 GA 是没有 beta 或 alpha 等后缀的版本），然后比较主要版本，
  最后是比较次要版本。版本排序列表示例：v10、v2、v1、v11beta2、v10beta3、v3beta1、v12alpha1、v11alpha2、foo1、foo10。

- **caBundle** ([]byte)
  **原子性：将在合并期间被替换**

  caBundle 是一个 PEM 编码的 CA 包，用于验证 API 服务器的服务证书。如果未指定，
  则使用 API 服务器上的系统根证书。

- **group** (string)
  group 是此服务器主机的 API 组名称。

- **insecureSkipTLSVerify** (boolean)
  insecureSkipTLSVerify 代表在与此服务器通信时禁用 TLS 证书验证。强烈建议不要这样做。你应该使用 caBundle。  

- **service** (ServiceReference)
  service 是对该 API 服务器的服务的引用。它只能在端口 443 上通信。如果 service 是 nil，
  则意味着 API groupversion 的处理是在当前服务器上本地处理的。服务调用被直接委托给正常的处理程序链来完成。

  <a name="ServiceReference"></a>
  **ServiceReference 保存对 Service.legacy.k8s.io 的一个引用。**

  - **service.name** (string)
    name 是服务的名称
  
  - **service.namespace** (string)
    namespace 是服务的命名空间
  
  - **service.port** (int32)
    如果指定，则为托管 Webhook 的服务上的端口。为实现向后兼容，默认端口号为 443。
    `port` 应该是一个有效的端口号（1-65535，包含）。

- **version** (string)
  version 是此服务器的 API 版本。例如：“v1”。

## APIServiceStatus {#APIServiceStatus}

APIServiceStatus 包含有关 API 服务器的派生信息

<hr>

- **conditions** ([]APIServiceCondition)
  **补丁策略：基于键 `type` 合并**

  **Map：合并时将保留 type 键的唯一值**

  APIService 的当前服务状态。

  <a name="APIServiceCondition"></a>
  **APIServiceCondition 描述 APIService 在特定点的状态** 

    status 表示状况（Condition）的状态，取值为 True、False 或 Unknown 之一。
  
    type 是状况的类型。

  - **conditions.lastTransitionTime** (Time)
    上一次发生状况状态转换的时间。
  
    <a name="Time"></a>
    Time 是对 time.Time 的封装。Time 支持对 YAML 和 JSON 进行正确封包。为 time 包的许多函数方法提供了封装器。
  
  - **conditions.message** (string)
    指示上次转换的详细可读信息。  
  
  - **conditions.reason** (string)
    表述状况上次转换原因的、驼峰格式命名的、唯一的一个词。
  

## APIServiceList {#APIServiceList}
APIServiceList 是 APIService 对象的列表。

<hr>

- **apiVersion**: apiregistration.k8s.io/v1

- **kind**: APIServiceList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)
  标准的列表元数据。更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

  items 是 APIService 的列表


## Operations {#Operations}

<hr>

### `get` 读取指定的 APIService

#### HTTP 请求

GET /apis/apiregistration.k8s.io/v1/apiservices/{name}

#### 参数

- **name** （**路径参数**）：string，必需

  APIService 名称

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): OK

401: Unauthorized

### `get` 读取指定 APIService 的状态

#### HTTP 请求

GET /apis/apiregistration.k8s.io/v1/apiservices/{name}/status

#### 参数

- **name** （**路径参数**）：string，必需

  APIService 名称

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): OK

401: Unauthorized

### `list` 列出或观察 APIService 类的对象

#### HTTP 请求

GET /apis/apiregistration.k8s.io/v1/apiservices

#### 参数

- **allowWatchBookmarks** （**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>


  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>


  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>


  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>


  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>


  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>


  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/api-service-v1#APIServiceList" >}}">APIServiceList</a>): OK

401: Unauthorized

### `create` 创建一个 APIService

#### HTTP 请求

POST /apis/apiregistration.k8s.io/v1/apiservices

#### 参数



  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): OK

201 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): Created

202 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): Accepted

401: Unauthorized

### `update` 替换指定的 APIService

#### HTTP 请求

PUT /apis/apiregistration.k8s.io/v1/apiservices/{name}

#### 参数

  APIService 名称



  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): OK

201 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): Created

401: Unauthorized

### `update` 替换指定 APIService 的 status

#### HTTP 请求

PUT /apis/apiregistration.k8s.io/v1/apiservices/{name}/status

#### 参数
- **name**（**路径参数**）：string， 必需

  APIService 名称



  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): OK

201 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 APIService

#### HTTP 请求

PATCH /apis/apiregistration.k8s.io/v1/apiservices/{name}

#### 参数

- **name**（**路径参数**）：string， 必需

  APIService 名称



  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): OK

201 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): Created

401: Unauthorized

### `patch` 部分更新指定 APIService 的 status

#### HTTP 请求

PATCH /apis/apiregistration.k8s.io/v1/apiservices/{name}/status

#### 参数

- **name**（**路径参数**）：string， 必需

  APIService 名称



  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): OK

201 (<a href="{{< ref "../cluster-resources/api-service-v1#APIService" >}}">APIService</a>): Created

401: Unauthorized

### `delete` 删除一个 APIService

#### HTTP 请求

DELETE /apis/apiregistration.k8s.io/v1/apiservices/{name}

#### 参数

- **name**（**路径参数**）：string， 必需

  APIService 名称

- **body**：<a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>


  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 APIService 集合

#### HTTP 请求

DELETE /apis/apiregistration.k8s.io/v1/apiservices

#### 参数

- **body**：<a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>


  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>


  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>


  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>


  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>


  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>


  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>


  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>


  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
