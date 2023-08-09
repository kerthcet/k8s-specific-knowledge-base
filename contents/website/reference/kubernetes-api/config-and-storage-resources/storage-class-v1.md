---
api_metadata:
  apiVersion: "storage.k8s.io/v1"
  import: "k8s.io/api/storage/v1"
  kind: "StorageClass"
content_type: "api_reference"
description: "StorageClass 为可以动态制备 PersistentVolume 的存储类描述参数。"
title: "StorageClass"
weight: 6
---

`apiVersion: storage.k8s.io/v1`

`import "k8s.io/api/storage/v1"`

## StorageClass {#StorageClass}
StorageClass 为可以动态制备 PersistentVolume 的存储类描述参数。

StorageClass 是不受名字空间作用域限制的；按照 etcd 设定的存储类的名称位于 ObjectMeta.Name 中。

<hr>

- **apiVersion**: storage.k8s.io/v1

- **kind**: StorageClass

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **provisioner** (string)，必需

  provisioner 表示制备器的类别。

- **allowVolumeExpansion** (boolean)

  allowVolumeExpansion 显示存储类是否允许卷扩充。

- **allowedTopologies** ([]TopologySelectorTerm)

  **原子性：将在合并期间被替换**
  
  allowedTopologies 限制可以动态制备卷的节点拓扑。每个卷插件定义其自己支持的拓扑规约。
  空的 TopologySelectorTerm 列表意味着没有拓扑限制。
  只有启用 VolumeScheduling 功能特性的服务器才能使用此字段。
  
  <a name="TopologySelectorTerm"></a> 
  **拓扑选择器条件表示标签查询的结果。
  一个 null 或空的拓扑选择器条件不会匹配任何对象。各个条件的要求按逻辑与的关系来计算。
  此选择器作为 NodeSelectorTerm 所提供功能的子集。此功能为 Alpha 特性，将来可能会变更。**

  - **allowedTopologies.matchLabelExpressions** ([]TopologySelectorLabelRequirement)

    按标签设置的拓扑选择器要求的列表。
    
    <a name="TopologySelectorLabelRequirement"></a> 
    **拓扑选择器要求是与给定标签匹配的一个选择器。此功能为 Alpha 特性，将来可能会变更。**
    
    - **allowedTopologies.matchLabelExpressions.key** (string)，必需

      选择器所针对的标签键。
    
    - **allowedTopologies.matchLabelExpressions.values** ([]string)，必需

      字符串数组。一个值必须与要选择的标签匹配。values 中的每个条目按逻辑或的关系来计算。

- **mountOptions** ([]string)

  mountOptions 控制此存储类动态制备的 PersistentVolume 的挂载配置。
  （例如 ["ro", "soft"]）。
  系统对选项作检查——如果有一个选项无效，则这些 PV 的挂载将失败。

- **parameters** (map[string]string)

  parameters 包含应创建此存储类卷的制备器的参数。

- **reclaimPolicy** (string)

  reclaimPolicy 控制此存储类动态制备的 PersistentVolume 的 reclaimPolicy。默认为 Delete。

- **volumeBindingMode** (string)

  volumeBindingMode 指示应该如何制备和绑定 PersistentVolumeClaim。
  未设置时，将使用 VolumeBindingImmediate。
  只有启用 VolumeScheduling 功能特性的服务器才能使用此字段。

## StorageClassList {#StorageClassList}
StorageClassList 是存储类的集合。

<hr>

- **apiVersion**: storage.k8s.io/v1

- **kind**: StorageClassList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>)，必需

  items 是 StorageClass 的列表。

## 操作 {#Operations}

<hr>

### `get` 读取指定的 StorageClass
#### HTTP 请求
GET /apis/storage.k8s.io/v1/storageclasses/{name}

#### 参数
- **name** (**路径参数**): string，必需

  StorageClass 的名称

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>): OK

401: Unauthorized

### `list` 列出或观测类别为 StorageClass 的对象
#### HTTP 请求
GET /apis/storage.k8s.io/v1/storageclasses

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
200 (<a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClassList" >}}">StorageClassList</a>): OK

401: Unauthorized

### `create` 创建 StorageClass
#### HTTP 请求
POST /apis/storage.k8s.io/v1/storageclasses

#### 参数
- **body**: <a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>): Created

202 (<a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>): Accepted

401: Unauthorized

### `update` 替换指定的 StorageClass
#### HTTP 请求
PUT /apis/storage.k8s.io/v1/storageclasses/{name}

#### 参数
- **name** (**路径参数**): string，必需

  StorageClass 的名称

- **body**: <a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 StorageClass
#### HTTP 请求
PATCH /apis/storage.k8s.io/v1/storageclasses/{name}

#### 参数
- **name** (**路径参数**): string，必需

  StorageClass 的名称

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
200 (<a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>): Created

401: Unauthorized

### `delete` 删除 StorageClass
#### HTTP 请求
DELETE /apis/storage.k8s.io/v1/storageclasses/{name}

#### 参数
- **name** (**路径参数**): string，必需

  StorageClass 的名称

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
200 (<a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>): OK

202 (<a href="{{< ref "../config-and-storage-resources/storage-class-v1#StorageClass" >}}">StorageClass</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 StorageClass 的集合
#### HTTP 请求
DELETE /apis/storage.k8s.io/v1/storageclasses

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
