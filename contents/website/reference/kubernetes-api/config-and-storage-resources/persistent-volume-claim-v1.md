---
api_metadata:
  apiVersion: "v1"
  import: "k8s.io/api/core/v1"
  kind: "PersistentVolumeClaim"
content_type: "api_reference"
description: "PersistentVolumeClaim 是用户针对一个持久卷的请求和申领。"
title: "PersistentVolumeClaim"
weight: 4
---

`apiVersion: v1`

`import "k8s.io/api/core/v1"`

## PersistentVolumeClaim {#PersistentVolumeClaim}

PersistentVolumeClaim 是用户针对一个持久卷的请求和申领。

<hr>

- **apiVersion**: v1

- **kind**: PersistentVolumeClaim

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaimSpec" >}}">PersistentVolumeClaimSpec</a>)

  spec 定义 Pod 作者所请求的卷的预期特征。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#persistentvolumeclaims

- **status** (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaimStatus" >}}">PersistentVolumeClaimStatus</a>)

  status 表示一个持久卷申领的当前信息/状态。只读。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#persistentvolumeclaims

## PersistentVolumeClaimSpec {#PersistentVolumeClaimSpec}
PersistentVolumeClaimSpec 描述存储设备的常用参数，并支持通过 source 来设置特定于提供商的属性。

<hr>

- **accessModes** ([]string)

  accessModes 包含卷应具备的预期访问模式。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#access-modes-1

- **selector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)

  selector 是在绑定时对卷进行选择所执行的标签查询。

- **resources** (ResourceRequirements)

  resources 表示卷应拥有的最小资源。
  如果启用了 RecoverVolumeExpansionFailure 功能特性，则允许用户指定这些资源要求，
  此值必须低于之前的值，但必须高于申领的状态字段中记录的容量。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#resources

  <a name="ResourceRequirements"></a>
  **ResourceRequirements 描述计算资源要求。**

  - **resources.claims** ([]ResourceClaim)

    **集合：键 name 的唯一值将在合并期间被保留**

    claims 列出了此容器使用的、在 spec.resourceClaims 中定义的资源的名称。

    这是一个 Alpha 字段，需要启用 DynamicResourceAllocation 特性门控。

    此字段是不可变的。

    <a name="ResourceClaim"></a>
    **ResourceClaim 引用 PodSpec.ResourceClaims 中的一个条目。**

    - **resources.claims.name** (string)，必需

      对于使用此字段的 Pod，name 必须与 pod.spec.resourceClaims 中的一个条目的名称匹配。

  - **resources.limits** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

    limits 描述允许的最大计算资源量。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/

  - **resources.requests** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

    requests 描述所需的最小计算资源量。
    如果针对容器省略 requests，则在显式指定的情况下默认为 limits，否则为具体实现所定义的值。请求不能超过限制。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/

- **volumeName** (string)

  volumeName 是对此申领所对应的 PersistentVolume 的绑定引用。

- **storageClassName** (string)

  storageClassName 是此申领所要求的 StorageClass 名称。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#class-1

- **volumeMode** (string)

  volumeMode 定义申领需要哪种类别的卷。当申领规约中未包含此字段时，意味着取值为 Filesystem。

### Beta 级别

- **dataSource** (<a href="{{< ref "../common-definitions/typed-local-object-reference#TypedLocalObjectReference" >}}">TypedLocalObjectReference</a>)

  dataSource 字段可用于二选一：

  - 现有的 VolumeSnapshot 对象（snapshot.storage.k8s.io/VolumeSnapshot）

  - 现有的 PVC (PersistentVolumeClaim)

  如果制备器或外部控制器可以支持指定的数据源，则它将根据指定数据源的内容创建新的卷。
  当 AnyVolumeDataSource 特性门控被启用时，dataSource 内容将被复制到 dataSourceRef，
  当 dataSourceRef.namespace 未被指定时，dataSourceRef 内容将被复制到 dataSource。
  如果名字空间被指定，则 dataSourceRef 不会被复制到 dataSource。

- **dataSourceRef** (TypedObjectReference)

  dataSourceRef 指定一个对象，当需要非空卷时，可以使用它来为卷填充数据。
  此字段值可以是来自非空 API 组（非核心对象）的任意对象，或一个 PersistentVolumeClaim 对象。
  如果设置了此字段，则仅当所指定对象的类型与所安装的某些卷填充器或动态制备器匹配时，卷绑定才会成功。
  此字段将替换 dataSource 字段的功能，因此如果两个字段非空，其取值必须相同。
  为了向后兼容，当未在 dataSourceRef 中指定名字空间时，
  如果（dataSource 和 dataSourceRef）其中一个字段为空且另一个字段非空，则两个字段将被自动设为相同的值。
  在 dataSourceRef 中指定名字空间时，dataSource 未被设置为相同的值且必须为空。
  dataSource 和 dataSourceRef 之间有三个重要的区别：

  * dataSource 仅允许两个特定类型的对象，而 dataSourceRef 允许任何非核心对象以及 PersistentVolumeClaim 对象。
  * dataSource 忽略不允许的值（这类值会被丢弃），而 dataSourceRef 保留所有值并在指定不允许的值时产生错误。
  * dataSource 仅允许本地对象，而 dataSourceRef 允许任意名字空间中的对象。

  (Beta) 使用此字段需要启用 AnyVolumeDataSource 特性门控。
  (Alpha) 使用 dataSourceRef 的名字空间字段需要启用 CrossNamespaceVolumeDataSource 特性门控。

  <a name="TypedObjectReference"></a>
  **

  - **dataSourceRef.kind** (string)，必需

    kind 是正被引用的资源的类型。

  - **dataSourceRef.name** (string)，必需

    name 是正被引用的资源的名称。

  - **dataSourceRef.apiGroup** (string)

    apiGroup 是正被引用的资源的组。如果 apiGroup 未被指定，则指定的 kind 必须在核心 API 组中。
    对于任何第三方类型，apiGroup 是必需的。

  - **dataSourceRef.namespace** (string)

    namespace 是正被引用的资源的名字空间。请注意，当指定一个名字空间时，
    在引用的名字空间中 gateway.networking.k8s.io/ReferenceGrant 对象是必需的，
    以允许该名字空间的所有者接受引用。有关详细信息，请参阅 ReferenceGrant 文档。
    (Alpha) 此字段需要启用 CrossNamespaceVolumeDataSource 特性门控。

## PersistentVolumeClaimStatus {#PersistentVolumeClaimStatus}
PersistentVolumeClaimStatus 是持久卷申领的当前状态。

<hr>

- **accessModes** ([]string)

  accessModes 包含支持 PVC 的卷所具有的实际访问模式。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#access-modes-1

- **allocatedResources** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

  allocatedResources 跟踪分配给 PVC 的容量。
  当出现卷扩充操作请求时，此字段可能大于实际的容量。
  就存储配额而言，将使用 allocatedResources 和 PVC.spec.resources 二者中的更大值。
  如果未设置 allocatedResources，则 PVC.spec.resources 单独用于配额计算。
  如果减小一个卷扩充容量请求，则仅当没有正在进行的扩充操作且实际卷容量等于或小于请求的容量时，
  才会减小 allocatedResources。
  这是一个 Alpha 字段，需要启用 RecoverVolumeExpansionFailure 功能特性。

- **capacity** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

  capacity 表示底层卷的实际资源。

- **conditions** ([]PersistentVolumeClaimCondition)

  **补丁策略：按照键 `type` 合并**

  conditions 是持久卷声明的当前的状况。
  如果正在调整底层持久卷的大小，则状况将被设为 “ResizeStarted”。

  <a name="PersistentVolumeClaimCondition"></a>
  **PersistentVolumeClaimCondition 包含有关 PVC 状态的详细信息。**

  - **conditions.status** (string)，必需
  
  - **conditions.type** (string)，必需
  
  - **conditions.lastProbeTime** (Time)
    
    lastProbeTime 是我们探测 PVC 状况的时间。
    
    <a name="Time"></a> 
    **Time 是 time.Time 的包装类，支持正确地序列化为 YAML 和 JSON。
    为 time 包提供的许多工厂方法提供了包装类。**

  - **conditions.lastTransitionTime** (Time)

    lastTransitionTime 是状况从一个状态转换为另一个状态的时间。

    <a name="Time"></a> 
    **Time 是 time.Time 的包装类，支持正确地序列化为 YAML 和 JSON。
    为 time 包提供的许多工厂方法提供了包装类。**
  
  - **conditions.message** (string)

    message 是人类可读的消息，指示有关上一次转换的详细信息。
  
  - **conditions.reason** (string)

    reason 是唯一的，它应该是一个机器可理解的简短字符串，指明上次状况转换的原因。
    如果它报告 “ResizeStarted”，则意味着正在调整底层持久卷的大小。

- **phase** (string)

  phase 表示 PersistentVolumeClaim 的当前阶段。

- **resizeStatus** (string)

  resizeStatus 存储大小调整操作的状态。默认不设置 resizeStatus，但在扩充完成时，
  resizeStatus 将由大小调整控制器或 kubelet 设为空。
  这是一个 Alpha 字段，需要启用 RecoverVolumeExpansionFailure 功能特性。

## PersistentVolumeClaimList {#PersistentVolumeClaimList}
PersistentVolumeClaimList 是 PersistentVolumeClaim 各项的列表。

<hr>

- **apiVersion**: v1

- **kind**: PersistentVolumeClaimList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **items** ([]<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>)，必需

  items 是持久卷申领的列表。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#persistentvolumeclaims

## 操作 {#Operations}
<hr>

### `get` 读取指定的 PersistentVolumeClaim
#### HTTP 请求
GET /api/v1/namespaces/{namespace}/persistentvolumeclaims/{name}

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolumeClaim 的名称

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): OK

401: Unauthorized

### `get` 读取指定的 PersistentVolumeClaim 的状态
#### HTTP 请求

GET /api/v1/namespaces/{namespace}/persistentvolumeclaims/{name}/status

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolumeClaim 的名称

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): OK

401: Unauthorized

### `list` 列出或观测类别为 PersistentVolumeClaim 的对象
#### HTTP 请求
GET /api/v1/namespaces/{namespace}/persistentvolumeclaims

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
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaimList" >}}">PersistentVolumeClaimList</a>): OK

401: Unauthorized

### `list` 列出或观测类别为 PersistentVolumeClaim 的对象
#### HTTP 请求
GET /api/v1/persistentvolumeclaims

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
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaimList" >}}">PersistentVolumeClaimList</a>): OK

401: Unauthorized

### `create` 创建 PersistentVolumeClaim
#### HTTP 请求
POST /api/v1/namespaces/{namespace}/persistentvolumeclaims

#### 参数
- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): Created

202 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): Accepted

401: Unauthorized

### `update` 替换指定的 PersistentVolumeClaim
#### HTTP 请求
PUT /api/v1/namespaces/{namespace}/persistentvolumeclaims/{name}

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolumeClaim 的名称

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): Created

401: Unauthorized

### `update` 替换指定的 PersistentVolumeClaim 的状态
#### HTTP 请求
PUT /api/v1/namespaces/{namespace}/persistentvolumeclaims/{name}/status

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolumeClaim 的名称

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 PersistentVolumeClaim
#### HTTP 请求
PATCH /api/v1/namespaces/{namespace}/persistentvolumeclaims/{name}

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolumeClaim 的名称

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
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 PersistentVolumeClaim 的状态
#### HTTP 请求
PATCH /api/v1/namespaces/{namespace}/persistentvolumeclaims/{name}/status

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolumeClaim 的名称

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
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): Created

401: Unauthorized

### `delete` 删除 PersistentVolumeClaim
#### HTTP 请求
DELETE /api/v1/namespaces/{namespace}/persistentvolumeclaims/{name}

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolumeClaim 的名称

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
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): OK

202 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaim" >}}">PersistentVolumeClaim</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 PersistentVolumeClaim 的集合
#### HTTP 请求
DELETE /api/v1/namespaces/{namespace}/persistentvolumeclaims

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
