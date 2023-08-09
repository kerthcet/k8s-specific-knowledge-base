---
api_metadata:
  apiVersion: "storage.k8s.io/v1"
  import: "k8s.io/api/storage/v1"
  kind: "VolumeAttachment"
content_type: "api_reference"
description: "VolumeAttachment 抓取将指定卷挂接到指定节点或从指定节点解除挂接指定卷的意图。"
title: "VolumeAttachment"
weight: 7
---

`apiVersion: storage.k8s.io/v1`

`import "k8s.io/api/storage/v1"`

## VolumeAttachment {#VolumeAttachment}
VolumeAttachment 抓取将指定卷挂接到指定节点或从指定节点解除挂接指定卷的意图。

VolumeAttachment 对象未划分命名空间。

<hr>

- **apiVersion**: storage.k8s.io/v1

- **kind**: VolumeAttachment

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachmentSpec" >}}">VolumeAttachmentSpec</a>)，必需

  spec 表示期望的挂接/解除挂接卷行为的规约。由 Kubernetes 系统填充。

- **status** (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachmentStatus" >}}">VolumeAttachmentStatus</a>)

  status 表示 VolumeAttachment 请求的状态。由完成挂接或解除挂接操作的实体（即外部挂接器）进行填充。

## VolumeAttachmentSpec {#VolumeAttachmentSpec}
VolumeAttachmentSpec 是 VolumeAttachment 请求的规约。

<hr>

- **attacher** (string)，必需

  attacher 表示必须处理此请求的卷驱动的名称。这是由 GetPluginName() 返回的名称。

- **nodeName** (string)，必需

  nodeName 表示卷应挂接到的节点。

- **source** (VolumeAttachmentSource)，必需

  source 表示应挂接的卷。

  <a name="VolumeAttachmentSource"></a>
  **VolumeAttachmentSource 表示应挂接的卷。现在只能通过外部挂接器挂接 PersistenVolume，
  将来我们可能还允许 Pod 中的内联卷。只能设置一个成员。**

  - **source.inlineVolumeSpec** (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolumeSpec" >}}">PersistentVolumeSpec</a>)

    inlineVolumeSpec 包含挂接由 Pod 的内联 VolumeSource 定义的持久卷时所有必需的信息。
    仅为 CSIMigation 功能填充此字段。
    它包含从 Pod 的内联 VolumeSource 转换为 PersistentVolumeSpec 的字段。
    此字段处于 Beta 阶段，且只有启用 CSIMigration 功能的服务器才能使用此字段。

  - **source.persistentVolumeName** (string)

    persistentVolumeName 是要挂接的持久卷的名称。

## VolumeAttachmentStatus {#VolumeAttachmentStatus}
VolumeAttachmentStatus 是 VolumeAttachment 请求的状态。

<hr>

- **attached** (boolean)，必需

  attached 表示卷被成功挂接。此字段只能由完成挂接操作的实体（例如外部挂接器）进行设置。

- **attachError** (VolumeError)

  attachError 表示挂接操作期间遇到的最后一个错误，如果有。
  此字段只能由完成挂接操作的实体（例如外部挂接器）进行设置。

  <a name="VolumeError"></a>
  **VolumeError 抓取卷操作期间遇到的一个错误。**

  - **attachError.message** (string)

    message 表示挂接或解除挂接操作期间遇到的错误。
    此字符串可以放入日志，因此它不应包含敏感信息。

  - **attachError.time** (Time)

    遇到错误的时间。

    <a name="Time"></a>
    **time 是 time.Time 的包装类，支持正确地序列化为 YAML 和 JSON。
    为 time 包提供的许多工厂方法提供了包装类。**

- **attachmentMetadata** (map[string]string)

  成功挂接时，attachmentMetadata 字段将由挂接操作返回的任何信息进行填充，
  这些信息必须传递到后续的 WaitForAttach 或 Mount 调用中。
  此字段只能由完成挂接操作的实体（例如外部挂接器）进行设置。

- **detachError** (VolumeError)

  detachError 表示解除挂接操作期间遇到的最后一个错误，如果有。
  此字段只能由完成解除挂接操作的实体（例如外部挂接器）进行设置。

  <a name="VolumeError"></a>
  **VolumeError 抓取卷操作期间遇到的一个错误。**

  - **detachError.message** (string)

    message 表示挂接或解除挂接操作期间遇到的错误。
    此字符串可以放入日志，因此它不应包含敏感信息。

  - **detachError.time** (Time)

    time 表示遇到错误的时间。

    <a name="Time"></a>
    **time 是 time.Time 的包装类，支持正确地序列化为 YAML 和 JSON。
    为 time 包提供的许多工厂方法提供了包装类。**

## VolumeAttachmentList {#VolumeAttachmentList}
VolumeAttachmentList 是 VolumeAttachment 对象的集合。

<hr>

- **apiVersion**: storage.k8s.io/v1

- **kind**: VolumeAttachmentList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>)，必需

  items 是 VolumeAttachment 的列表。

## 操作 {#Operations}

<hr>

### `get` 读取指定的 VolumeAttachment

#### HTTP 请求

GET /apis/storage.k8s.io/v1/volumeattachments/{name}

#### 参数

- **name** (**路径参数**): string，必需

  VolumeAttachment 的名称

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

401: Unauthorized

### `get` 读取指定的 VolumeAttachment 的状态

#### HTTP 请求

GET /apis/storage.k8s.io/v1/volumeattachments/{name}/status

#### 参数

- **name** (**路径参数**): string，必需

  VolumeAttachment 的名称

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

401: Unauthorized

### `list` 列出或观测类别为 VolumeAttachment 的对象

#### HTTP 请求

GET /apis/storage.k8s.io/v1/volumeattachments

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

200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachmentList" >}}">VolumeAttachmentList</a>): OK

401: Unauthorized

### `create` 创建 VolumeAttachment

#### HTTP 请求

POST /apis/storage.k8s.io/v1/volumeattachments

#### 参数

- **body**: <a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Created

202 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Accepted

401: Unauthorized

### `update` 替换指定的 VolumeAttachment

#### HTTP 请求

PUT /apis/storage.k8s.io/v1/volumeattachments/{name}

#### 参数

- **name** (**路径参数**): string，必需

  VolumeAttachment 的名称

- **body**: <a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Created

401: Unauthorized

### `update` 替换指定的 VolumeAttachment 的状态

#### HTTP 请求

PUT /apis/storage.k8s.io/v1/volumeattachments/{name}/status

#### 参数

- **name** (**路径参数**): string，必需

  VolumeAttachment 的名称

- **body**: <a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 VolumeAttachment

#### HTTP 请求

PATCH /apis/storage.k8s.io/v1/volumeattachments/{name}

#### 参数

- **name** (**路径参数**): string，必需

  VolumeAttachment 的名称

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

200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 VolumeAttachment 的状态

#### HTTP 请求

PATCH /apis/storage.k8s.io/v1/volumeattachments/{name}/status

#### 参数

- **name** (**路径参数**): string，必需

  VolumeAttachment 的名称

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

200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Created

401: Unauthorized

### `delete` 删除 VolumeAttachment

#### HTTP 请求

DELETE /apis/storage.k8s.io/v1/volumeattachments/{name}

#### 参数

- **name** (**路径参数**): string，必需

  VolumeAttachment 的名称

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

200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

202 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 VolumeAttachment 的集合

#### HTTP 请求

DELETE /apis/storage.k8s.io/v1/volumeattachments

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
