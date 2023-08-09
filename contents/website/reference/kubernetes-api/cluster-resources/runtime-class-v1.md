---
api_metadata:
  apiVersion: "node.k8s.io/v1"
  import: "k8s.io/api/node/v1"
  kind: "RuntimeClass"
content_type: "api_reference"
description: "RuntimeClass 定义集群中支持的容器运行时类。"
title: "RuntimeClass"
weight: 6
---
`apiVersion: node.k8s.io/v1`

`import "k8s.io/api/node/v1"`

## RuntimeClass {#RuntimeClass}
RuntimeClass 定义集群中支持的容器运行时类。
RuntimeClass 用于确定哪个容器运行时用于运行某 Pod 中的所有容器。
RuntimeClass 由用户或集群制备程序手动定义，并在 PodSpec 中引用。
Kubelet 负责在运行 Pod 之前解析 RuntimeClassName 引用。
有关更多详细信息，请参阅
https://kubernetes.io/zh-cn/docs/concepts/containers/runtime-class/

<hr>

- **apiVersion**: node.k8s.io/v1

- **kind**: RuntimeClass

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **handler** (string)，必需

  handler 指定底层运行时和配置，在 CRI 实现过程中将使用这些运行时和配置来处理这个类的 Pod。
  可能的值特定于节点和 CRI 配置。
  假定所有 handler 可用于每个节点上，且同一名称的 handler 在所有节点上是等效的。
  例如，一个名为 “runc” 的 handler 可能指定 runc OCI 运行时将（使用原生 Linux 容器）
  用于运行 Pod 中的容器。该 handler 必须采用小写，遵从 DNS Label (RFC 1123) 要求，且是不可变更的。

- **overhead** (Overhead)

  overhead 表示运行给定 RuntimeClass 的 Pod 时所关联的资源开销。有关更多详细信息，请参阅
  https://kubernetes.io/zh-cn/docs/concepts/scheduling-eviction/pod-overhead/

  <a name="Overhead"></a>
  **Overhead 结构表示运行一个 Pod 所关联的资源开销。**
  
  
  - **overhead.podFixed** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

    podFixed 表示与运行一个 Pod 所关联的资源开销。

- **scheduling** (Scheduling)

  scheduling 包含调度约束，这些约束用来确保以这个 RuntimeClass 运行的 Pod 被调度到支持此运行时类的节点。
  如果 scheduling 设为空，则假定所有节点支持此 RuntimeClass。

  <a name="Scheduling"></a>
  **Scheduling 指定支持 RuntimeClass 的节点的调度约束。**

  
  - **scheduling.nodeSelector** (map[string]string)

    nodeSelector 列出支持此 RuntimeClass 的节点上必须存在的标签。
    使用此 RuntimeClass 的 Pod 只能调度到与这个选择算符匹配的节点上。
    RuntimeClass nodeSelector 与 Pod 现有的 nodeSelector 合并。
    任何冲突均会使得该 Pod 在准入时被拒绝。
  
  
  - **scheduling.tolerations** ([]Toleration)

    **原子性：将在合并期间被替换**
    
    tolerations 在准入期间追加到以此 RuntimeClass 运行的 Pod（不包括重复项）上，
    本质上是求取 Pod 和 RuntimeClass 所容忍的节点并集。

    <a name="Toleration"></a>
    **附加此容忍度的 Pod 将容忍用匹配运算符 `operator` 运算后与三元组
    `<key,value,effect>` 匹配的任何污点。**

    
    - **scheduling.tolerations.key** (string)

      key 是容忍度所应用到的污点键。空意味着匹配所有污点键。
      如果键为空，则运算符必须为 Exists；这个组合意味着匹配所有值和所有键。

    - **scheduling.tolerations.operator** (string)

      operator 表示一个键与值的关系。有效的运算符为 Exists 和 Equal。默认为 Equal。
      Exists 等价于将值设置为通配符的情况，因此一个 Pod 可以容忍特定类别的所有污点。
    
    
    - **scheduling.tolerations.value** (string)

      value 是容忍度匹配到的污点值。如果运算符为 Exists，则值应为空，否则就是一个普通字符串。

    - **scheduling.tolerations.effect** (string)

      effect 表示匹配度污点效果。空意味着匹配所有污点效果。
      当指定值时，允许的值为 NoSchedule、PreferNoSchedule 或 NoExecute。
      
    - **scheduling.tolerations.tolerationSeconds** (int64)

      tolerationSeconds 表示容忍度容忍污点的时间段（必须是 NoExecute 的效果，否则忽略此字段）。
      默认情况下，不设置此字段，这意味着永远容忍污点（不驱逐）。零和负值将被系统视为 0（立即驱逐）。

## RuntimeClassList {#RuntimeClassList}
RuntimeClassList 是 RuntimeClass 对象的列表。

<hr>

- **apiVersion**: node.k8s.io/v1

- **kind**: RuntimeClassList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>)，必需

  items 是 schema 对象的列表。

## 操作 {#Operations}
<hr>

### `get` 读取指定的 RuntimeClass
#### HTTP 请求
GET /apis/node.k8s.io/v1/runtimeclasses/{name}

##### 参数
- **name** (**路径参数**): string，必需

  RuntimeClass 的名称

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): OK

401: Unauthorized

### `list` 列出或监视 RuntimeClass 类别的对象
#### HTTP 请求
GET /apis/node.k8s.io/v1/runtimeclasses

##### 参数
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
200 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClassList" >}}">RuntimeClassList</a>): OK

401: Unauthorized

### `create` 创建 RuntimeClass
#### HTTP 请求
POST /apis/node.k8s.io/v1/runtimeclasses
##### 参数
- **body**: <a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): OK

201 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): Created

202 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): Accepted

401: Unauthorized

### `update` 替换指定的 RuntimeClass
#### HTTP 请求
PUT /apis/node.k8s.io/v1/runtimeclasses/{name}

##### 参数
- **name** (**路径参数**): string，必需

  RuntimeClass 的名称

- **body**: <a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): OK

201 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 RuntimeClass
#### HTTP 请求
PATCH /apis/node.k8s.io/v1/runtimeclasses/{name}

##### 参数
- **name** (**路径参数**): string，必需

  RuntimeClass 的名称

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
200 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): OK

201 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): Created

401: Unauthorized

### `delete` 删除 RuntimeClass
#### HTTP 请求
DELETE /apis/node.k8s.io/v1/runtimeclasses/{name}

##### 参数
- **name** (**路径参数**): string，必需

  RuntimeClass 的名称

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

### `deletecollection` 删除 RuntimeClass 的集合
#### HTTP 请求
DELETE /apis/node.k8s.io/v1/runtimeclasses

##### 参数
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
