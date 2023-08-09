---
api_metadata:
  apiVersion: "apps/v1"
  import: "k8s.io/api/apps/v1"
  kind: "ControllerRevision"
content_type: "api_reference"
description: "ControllerRevision 实现了状态数据的不可变快照。"
title: "ControllerRevision"
weight: 7
---


`apiVersion: apps/v1`

`import "k8s.io/api/apps/v1"`

## ControllerRevision {#ControllerRevision}

ControllerRevision 实现了状态数据的不可变快照。
客户端负责序列化和反序列化对象，包含对象内部状态。
成功创建 ControllerRevision 后，将无法对其进行更新。
API 服务器将无法成功验证所有尝试改变 data 字段的请求。
但是，可以删除 ControllerRevisions。
请注意，由于 DaemonSet 和 StatefulSet 控制器都使用它来进行更新和回滚，所以这个对象是 Beta 版。
但是，它可能会在未来版本中更改名称和表示形式，客户不应依赖其稳定性。
它主要供控制器内部使用。

<hr>

- **apiVersion**: apps/v1

- **kind**: ControllerRevision

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **revision** (int64)，必需

  revision 表示 data 表示的状态的修订。

- **data** (RawExtension)

  data 是状态的序列化表示。
  

  <a name="RawExtension"></a>
  **RawExtension 用于以外部版本来保存扩展数据。**
  

  要使用它，请生成一个字段，在外部、版本化结构中以 RawExtension 作为其类型，在内部结构中以 Object 作为其类型。
  你还需要注册你的各个插件类型。
  
  
  // 内部包：

    ```go
    type MyAPIObject struct {  
      runtime.TypeMeta `json:",inline"`   
      MyPlugin runtime.Object `json:"myPlugin"`  
    } 

    type PluginA struct {  
      AOption string `json:"aOption"`  
    }
    ```
  

  // 外部包：

    ```go
    type MyAPIObject struct {  
      runtime.TypeMeta `json:",inline"`  
      MyPlugin runtime.RawExtension `json:"myPlugin"`    
    } 

    type PluginA struct {  
      AOption string `json:"aOption"`  
    }
    ```
  

  // 在网络上，JSON 看起来像这样：

    ```json
    {  
      "kind":"MyAPIObject",  
      "apiVersion":"v1",  
      "myPlugin": {  
        "kind":"PluginA",  
        "aOption":"foo",  
      },  
    }
    ```
  
  
  那么会发生什么？
  解码首先使用 json 或 yaml 将序列化数据解组到你的外部 MyAPIObject 中。
  这会导致原始 JSON 被存储下来，但不会被解包。
  下一步是复制（使用 pkg/conversion）到内部结构中。
  runtime 包的 DefaultScheme 安装了转换函数，它将解析存储在 RawExtension 中的 JSON，
  将其转换为正确的对象类型，并将其存储在 Object 中。
  （TODO：如果对象是未知类型，将创建并存储一个 `runtime.Unknown`对象。）

## ControllerRevisionList {#ControllerRevisionList}

ControllerRevisionList 是一个包含 ControllerRevision 对象列表的资源。

<hr>

- **apiVersion**: apps/v1

- **kind**: ControllerRevisionList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevision" >}}">ControllerRevision</a>)，必需

  items 是 ControllerRevisions 的列表

## 操作 {#Operations}

<hr>

### `get` 读取特定的 ControllerRevision

#### HTTP 请求

GET /apis/apps/v1/namespaces/{namespace}/controllerrevisions/{name}

#### 参数

- **name** （**路径参数**）：string，必需

  ControllerRevision 的名称

- **namespace** （**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevision" >}}">ControllerRevision</a>): OK

401: Unauthorized

### `list` 列出或监视 ControllerRevision 类别的对象

#### HTTP 请求

GET /apis/apps/v1/namespaces/{namespace}/controllerrevisions

#### 参数

- **namespace** （**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **allowWatchBookmarks** （**查询参数**）： boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (**查询参数**)): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** （**查询参数**）： integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** （**查询参数**）： boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevisionList" >}}">ControllerRevisionList</a>): OK

401: Unauthorized

### `list` 列出或监视 ControllerRevision 类别的对象

#### HTTP 请求

GET /apis/apps/v1/controllerrevisions

#### 参数

- **allowWatchBookmarks** （**查询参数**）： boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** （**查询参数**）： integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** （**查询参数**）： integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** （**查询参数**）： boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevisionList" >}}">ControllerRevisionList</a>): OK

401: Unauthorized

### `create` 创建一个 ControllerRevision

#### HTTP 请求

POST /apis/apps/v1/namespaces/{namespace}/controllerrevisions

#### 参数

- **namespace** （**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevision" >}}">ControllerRevision</a>，必需

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevision" >}}">ControllerRevision</a>): OK

201 (<a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevision" >}}">ControllerRevision</a>): Created

202 (<a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevision" >}}">ControllerRevision</a>): Accepted

401: Unauthorized

### `update` 替换特定的 ControllerRevision

#### HTTP 参数

PUT /apis/apps/v1/namespaces/{namespace}/controllerrevisions/{name}

#### 参数

- **name** （**路径参数**）：string，必需

  ControllerRevision 的名称

- **namespace** （**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevision" >}}">ControllerRevision</a>，必需

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200 (<a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevision" >}}">ControllerRevision</a>): OK

201 (<a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevision" >}}">ControllerRevision</a>): Created

401: Unauthorized

### `patch` 部分更新特定的 ControllerRevision

#### HTTP 请求

PATCH /apis/apps/v1/namespaces/{namespace}/controllerrevisions/{name}

#### 参数

- **name** （**路径参数**）：string，必需

  ControllerRevision 的名称

- **namespace** （**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** （**查询参数**）： boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevision" >}}">ControllerRevision</a>): OK

201 (<a href="{{< ref "../workload-resources/controller-revision-v1#ControllerRevision" >}}">ControllerRevision</a>): Created

401: Unauthorized

### `delete` 删除一个 ControllerRevision

#### HTTP 请求

DELETE /apis/apps/v1/namespaces/{namespace}/controllerrevisions/{name}

#### 参数

- **name** （**路径参数**）：string，必需

  ControllerRevision 的名称

- **namespace** （**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** （**查询参数**）： integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 ControllerRevision 集合

#### HTTP 请求

DELETE /apis/apps/v1/namespaces/{namespace}/controllerrevisions

#### 参数

- **namespace** （**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **continue** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **gracePeriodSeconds** （**查询参数**）： integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **labelSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** （**查询参数**）： integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

- **resourceVersion** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** （**查询参数**）： integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized

