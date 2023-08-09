---
api_metadata:
  apiVersion: "v1"
  import: "k8s.io/api/core/v1"
  kind: "PersistentVolume"
content_type: "api_reference"
description: "PersistentVolume (PV) 是管理员制备的一个存储资源。"
title: "PersistentVolume"
weight: 5
---

`apiVersion: v1`

`import "k8s.io/api/core/v1"`

## PersistentVolume {#PersistentVolume}

PersistentVolume (PV) 是管理员制备的一个存储资源。它类似于一个节点。更多信息：
https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes

<hr>

- **apiVersion**: v1

- **kind**: PersistentVolume


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolumeSpec" >}}">PersistentVolumeSpec</a>)

  spec 定义了集群所拥有的持久卷的规约。由管理员进行制备。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#persistent-volumes

- **status** (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolumeStatus" >}}">PersistentVolumeStatus</a>)

  status 表示持久卷的当前信息/状态。该值由系统填充，只读。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#persistent-volumes

## PersistentVolumeSpec {#PersistentVolumeSpec}
PersistentVolumeSpec 是持久卷的规约。

<hr>

- **accessModes** ([]string)

  accessModes 包含可以挂载卷的所有方式。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#access-modes

- **capacity** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

  capacity 描述持久卷的资源和容量。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#capacity


- **claimRef** (<a href="{{< ref "../common-definitions/object-reference#ObjectReference" >}}">ObjectReference</a>)

  claimRef 是 PersistentVolume 和 PersistentVolumeClaim 之间双向绑定的一部分。
  预期在绑定时为非空。claim.VolumeName 是在 PV 和 PVC 间绑定关系的正式确认。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#binding

- **mountOptions** ([]string)

  mountOptions 是挂载选项的列表，例如 ["ro", "soft"]。
  针对此字段无合法性检查——如果某选项无效，则只是挂载会失败。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes/#mount-options


- **nodeAffinity** (VolumeNodeAffinity)

  nodeAffinity 定义可以从哪些节点访问此卷的约束限制。此字段会影响调度使用此卷的 Pod。

  <a name="VolumeNodeAffinity"></a>
  **VolumeNodeAffinity 定义可以从哪些节点访问此卷的约束限制。**

  - **nodeAffinity.required** (NodeSelector)

    required 指定必须满足的硬性节点约束。

    <a name="NodeSelector"></a>
    **节点选择器表示在一组节点上一个或多个标签查询结果的并集；
    也就是说，它表示由节点选择器条件表示的选择器的逻辑或计算结果。**

    - **nodeAffinity.required.nodeSelectorTerms** ([]NodeSelectorTerm)，必需

      必需。节点选择器条件的列表。这些条件是逻辑或的计算结果。

      <a name="NodeSelectorTerm"></a>
      **一个 null 或空的节点选择器条件不会与任何对象匹配。这些条件会按逻辑与的关系来计算。
      TopologySelectorTerm 类别实现了 NodeSelectorTerm 的子集。**

      - **nodeAffinity.required.nodeSelectorTerms.matchExpressions** ([]<a href="{{< ref "../common-definitions/node-selector-requirement#NodeSelectorRequirement" >}}">NodeSelectorRequirement</a>)

        基于节点标签所设置的节点选择器要求的列表。

      - **nodeAffinity.required.nodeSelectorTerms.matchFields** ([]<a href="{{< ref "../common-definitions/node-selector-requirement#NodeSelectorRequirement" >}}">NodeSelectorRequirement</a>)

        基于节点字段所设置的节点选择器要求的列表。


- **persistentVolumeReclaimPolicy** (string)

  persistentVolumeReclaimPolicy 定义当从持久卷声明释放持久卷时会发生什么。
  有效的选项为 Retain（手动创建 PersistentVolumes 所用的默认值）、
  Delete（动态制备 PersistentVolumes 所用的默认值）和 Recycle（已弃用）。
  Recycle 选项必须被 PersistentVolume 下层的卷插件所支持才行。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#reclaiming


- **storageClassName** (string)

  storageClassName 是这个持久卷所属于的 StorageClass 的名称。
  空值意味着此卷不属于任何 StorageClass。

- **volumeMode** (string)

  volumeMode 定义一个卷是带着已格式化的文件系统来使用还是保持在原始块状态来使用。
  当 spec 中未包含此字段时，意味着取值为 Filesystem。

### Local

- **hostPath** (HostPathVolumeSource)

  hostPath 表示主机上的目录，由开发或测试人员进行制备。hostPath 仅对单节点开发和测试有用！
  不会以任何方式支持主机存储（On-host storage），并且**不能用于**多节点集群中。
  更多信息： https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#hostpath

  <a name="HostPathVolumeSource"></a>
  **表示映射到 Pod 中的主机路径。主机路径卷不支持所有权管理或 SELinux 重新打标签。**

  - **hostPath.path** (string)，必需

    目录在主机上的路径。如果该路径是一个符号链接，则它将沿着链接指向真实路径。
    更多信息： https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#hostpath

  - **hostPath.type** (string)

    HostPath 卷的类型。默认为 ""。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#hostpath


- **local** (LocalVolumeSource)

  local 表示具有节点亲和性的直连式存储。

  <a name="LocalVolumeSource"></a>
  **local 表示具有节点亲和性的直连式存储（Beta 特性）。**

  - **local.path** (string)，必需

    指向节点上卷的完整路径。它可以是一个目录或块设备（磁盘、分区...）。

  - **local.fsType** (string)

    fsType 是要挂载的文件系统类型。它仅适用于 path 是一个块设备的情况。
    必须是主机操作系统所支持的文件系统类型之一。例如 “ext4”、“xfs”、“ntfs”。
    在未指定的情况下，默认值是自动选择一个文件系统。

### 持久卷 {#persistent-volumes}

- **awsElasticBlockStore** (AWSElasticBlockStoreVolumeSource)

  awsElasticBlockStore 表示挂接到 kubelet 的主机随后暴露给 Pod 的一个 AWS Disk 资源。
  更多信息： https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#awselasticblockstore

  <a name="AWSElasticBlockStoreVolumeSource"></a>
  **表示 AWS 上的 Persistent Disk 资源。挂载到一个容器之前 AWS EBS 磁盘必须存在。
  该磁盘还必须与 kubelet 位于相同的 AWS 区域中。AWS EBS 磁盘只能以读/写一次进行挂载。
  AWS EBS 卷支持所有权管理和 SELinux 重新打标签。**


  - **awsElasticBlockStore.volumeID** (string)，必需

    volumeID 是 AWS（Amazon EBS 卷）中持久磁盘资源的唯一 ID。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#awselasticblockstore

  - **awsElasticBlockStore.fsType** (string)

    fsType 是你要挂载的卷的文件系统类型。提示：确保主机操作系统支持此文件系统类型。
    例如：“ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为“ext4”。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#awselasticblockstore

  - **awsElasticBlockStore.partition** (int32)

    partition 是你要挂载的卷中的分区。如果省略，则默认为按卷名称进行挂载。
    例如：对于卷 /dev/sda1，将分区指定为 “1”。
    类似地，/dev/sda 的卷分区为 “0”（或可以将属性留空）。

  - **awsElasticBlockStore.readOnly** (boolean)

    readOnly 值为 true 将在 VolumeMounts 中强制设置 readOnly。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#awselasticblockstore


- **azureDisk** (AzureDiskVolumeSource)

  azureDisk 表示主机上挂载的 Azure Data Disk 并绑定挂载到 Pod 上。

  <a name="AzureDiskVolumeSource"></a>
  **azureDisk 表示主机上挂载的 Azure Data Disk 并绑定挂载到 Pod 上。**


  - **azureDisk.diskName** (string)，必需

    diskName 是 Blob 存储中数据盘的名称。

  - **azureDisk.diskURI** (string)，必需

    diskURI 是 Blob 存储中数据盘的 URI。

  - **azureDisk.cachingMode** (string)

    cachingMode 是主机缓存（Host Caching）模式：None、Read Only、Read Write。

  - **azureDisk.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。
    例如 “ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为 “ext4”。

  - **azureDisk.kind** (string)

    kind 预期值包括：
    - Shared：每个存储帐户多个 Blob 磁盘；
    - Dedicated：每个存储帐户单个 Blob 磁盘；
    - Managed：azure 托管的数据盘（仅托管的可用性集合中）。
    默认为 Shared。

  - **azureDisk.readOnly** (boolean)

    readOnly 默认为 false（读/写）。此处 readOnly 将在 VolumeMounts 中强制设置 readOnly。


- **azureFile** (AzureFilePersistentVolumeSource)

  azureDisk 表示主机上挂载的 Azure File Service 并绑定挂载到 Pod 上。

  <a name="AzureFilePersistentVolumeSource"></a>
  **azureFile 表示主机上挂载的 Azure File Service 并绑定挂载到 Pod 上。**

  - **azureFile.secretName** (string)，必需

    secretName 是包含 Azure 存储账号名称和主键的 Secret 的名称。

  - **azureFile.shareName** (string)，必需

    shareName 是 azure Share Name。

  - **azureFile.readOnly** (boolean)

    readOnly 默认为 false（读/写）。此处 readOnly 将在 VolumeMounts 中强制设置 readOnly。

  - **azureFile.secretNamespace** (string)

    secretNamespace 是包含 Azure 存储账号名称和主键的 Secret 的名字空间，默认与 Pod 相同。


- **cephfs** (CephFSPersistentVolumeSource)

  cephfs 表示在主机上挂载的 Ceph FS，该文件系统挂载与 Pod 的生命周期相同。

  <a name="CephFSPersistentVolumeSource"></a>
  **表示在 Pod 的生命周期内持续的 Ceph Filesystem 挂载。cephfs 卷不支持所有权管理或 SELinux 重新打标签。**


  - **cephfs.monitors** ([]string)，必需

    monitors 是必需的。monitors 是 Ceph 监测的集合。更多信息：
    https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it

  - **cephfs.path** (string)

    path 是可选的。用作挂载的根，而不是完整的 Ceph 树，默认为 /。

  - **cephfs.readOnly** (boolean)

    readOnly 是可选的。默认为 false（读/写）。此处 readOnly 将在 VolumeMounts 中强制设置 readOnly。
    更多信息： https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it

  - **cephfs.secretFile** (string)

    secretFile 是可选的。secretFile 是 user 对应的密钥环的路径，默认为 /etc/ceph/user.secret。
    更多信息： https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it


  - **cephfs.secretRef** (SecretReference)

    secretRef 是可选的。secretRef 是针对用户到身份认证 Secret 的引用，默认为空。更多信息：
    https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it

    <a name="SecretReference"></a>
    **SecretReference 表示对某 Secret 的引用，其中包含足够的信息来访问任何名字空间中的 Secret。**

    - **cephfs.secretRef.name** (string)

      name 在名字空间内是唯一的，以引用一个 Secret 资源。

    - **cephfs.secretRef.namespace** (string)

      namespace 指定一个名字空间，Secret 名称在该名字空间中必须唯一。

  - **cephfs.user** (string)

    user 是可选的。user 是 rados 用户名，默认为 admin。更多信息：
    https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it


- **cinder** (CinderPersistentVolumeSource)

  cinder 表示 kubelet 主机上挂接和挂载的 Cinder 卷。更多信息：
  https://examples.k8s.io/mysql-cinder-pd/README.md

  <a name="CinderPersistentVolumeSource"></a>
  **表示 OpenStack 中的一个 Cinder 卷资源。挂载到一个容器之前 Cinder 卷必须已经存在。
  该卷还必须与 kubelet 位于相同的地区中。cinder 卷支持所有权管理和 SELinux 重新打标签。**


  - **cinder.volumeID** (string)，必需

    volumeID 用于标识 Cinder 中的卷。更多信息：
    https://examples.k8s.io/mysql-cinder-pd/README.md

  - **cinder.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统支持的文件系统类型。
    例如：“ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为 “ext4”。更多信息：
    https://examples.k8s.io/mysql-cinder-pd/README.md

  - **cinder.readOnly** (boolean)

    readOnly 是可选的。默认为 false（读/写）。
    此处 readOnly 将在 VolumeMounts 中强制设置 readOnly。更多信息：
    https://examples.k8s.io/mysql-cinder-pd/README.md


  - **cinder.secretRef** (SecretReference)

    secretRef 是可选的。指向 Secret 对象，内含的参数用于连接到 OpenStack。

    <a name="SecretReference"></a>
    **SecretReference 表示对某 Secret 的引用，其中包含足够的信息来访问任何名字空间中的 Secret。**

    - **cinder.secretRef.name** (string)

      name 在名字空间内是唯一的，以引用一个 Secret 资源。

    - **cinder.secretRef.namespace** (string)

      namespace 指定一个名字空间，Secret 名称在该名字空间中必须唯一。


- **csi** (CSIPersistentVolumeSource)

  csi 表示由一个外部 CSI 驱动处理的存储（Beta 特性）。

  <a name="CSIPersistentVolumeSource"></a>
  **表示由一个外部 CSI 卷驱动管理的存储（Beta 特性）。**

  - **csi.driver** (string)，必需

    driver 是此卷所使用的驱动的名称。必需。

  - **csi.volumeHandle** (string)，必需

    volumeHandle 是 CSI 卷插件的 CreateVolume 所返回的唯一卷名称，用于在所有后续调用中引用此卷。必需。


  - **csi.controllerExpandSecretRef** (SecretReference)

    controllerExpandSecretRef 是对包含敏感信息的 Secret 对象的引用，
    该 Secret 会被传递到 CSI 驱动以完成 CSI ControllerExpandVolume 调用。
    此字段是可选的，且如果不需要 Secret，则此字段可以为空。
    如果 Secret 对象包含多个 Secret，则所有 Secret 被传递。

    <a name="SecretReference"></a>
    **SecretReference 表示对某 Secret 的引用，其中包含足够的信息来访问任何名字空间中的 Secret。**

    - **csi.controllerExpandSecretRef.name** (string)

      name 在名字空间内是唯一的，以引用一个 Secret 资源。

    - **csi.controllerExpandSecretRef.namespace** (string)

      namespace 指定一个名字空间，Secret 名称在该名字空间中必须唯一。


  - **csi.controllerPublishSecretRef** (SecretReference)

    controllerPublishSecretRef 是对包含敏感信息的 Secret 对象的引用，
    该 Secret 会被传递到 CSI 驱动以完成 CSI ControllerPublishVolume 和 ControllerUnpublishVolume 调用。
    此字段是可选的，且如果不需要 Secret，则此字段可以为空。
    如果 Secret 对象包含多个 Secret，则所有 Secret 被传递。

    <a name="SecretReference"></a>
    **SecretReference 表示对某 Secret 的引用，其中包含足够的信息来访问任何名字空间中的 Secret。**

    - **csi.controllerPublishSecretRef.name** (string)

      name 在名字空间内是唯一的，以引用一个 Secret 资源。

    - **csi.controllerPublishSecretRef.namespace** (string)

      namespace 指定一个名字空间，Secret 名称在该名字空间中必须唯一。


  - **csi.fsType** (string)

    要挂载的 fsType。必须是主机操作系统所支持的文件系统类型之一。例如 “ext4”、“xfs”、“ntfs”。

  - **csi.nodeExpandSecretRef** (SecretReference)

    nodeExpandSecretRef 是对包含敏感信息的 Secret 对象的引用，
    从而传递到 CSI 驱动以完成 CSI NodeExpandVolume 和 NodeUnpublishVolume 调用。
    这是一个 Beta 字段，通过 CSINodeExpandSecret 特性门控默认启用。
    此字段是可选的，且如果不需要 Secret，则此字段可以为空。
    如果 Secret 对象包含多个 Secret，则所有 Secret 被传递。

    <a name="SecretReference"></a>
    **SecretReference 表示对某 Secret 的引用，其中包含足够的信息来访问任何名字空间中的 Secret。**

    - **csi.nodeExpandSecretRef.name** (string)

      name 在名字空间内是唯一的，以引用一个 Secret 资源。

    - **csi.nodeExpandSecretRef.namespace** (string)

      namespace 指定一个名字空间，Secret 名称在该名字空间中必须唯一。


  - **csi.nodePublishSecretRef** (SecretReference)

    nodePublishSecretRef 是对包含敏感信息的 Secret 对象的引用，
    以传递到 CSI 驱动以完成 CSI NodePublishVolume 和 NodeUnpublishVolume 调用。
    此字段是可选的，且如果不需要 Secret，则此字段可以为空。
    如果 Secret 对象包含多个 Secret，则所有 Secret 被传递。

    **SecretReference 表示对某 Secret 的引用，其中包含足够的信息来访问任何名字空间中的 Secret。**

    - **csi.nodePublishSecretRef.name** (string)

      name 在名字空间内是唯一的，以引用一个 Secret 资源。

    - **csi.nodePublishSecretRef.namespace** (string)

      namespace 定义了 Secret 名称必须唯一的空间。


  - **csi.nodeStageSecretRef** (SecretReference)

    nodeStageSecretRef 是对包含敏感信息的 Secret 对象的引用，
    从而传递到 CSI 驱动以完成 CSI NodeStageVolume、NodeStageVolume 和 NodeUnstageVolume 调用。
    此字段是可选的，且如果不需要 Secret，则此字段可以为空。
    如果 Secret 对象包含多个 Secret，则所有 Secret 被传递。

    <a name="SecretReference"></a>
    **SecretReference 表示对某 Secret 的引用，其中包含足够的信息来访问任何名字空间中的 Secret。**

    - **csi.nodeStageSecretRef.name** (string)

      name 在名字空间内是唯一的，以引用一个 Secret 资源。

    - **csi.nodeStageSecretRef.namespace** (string)

      namespace 指定一个名字空间，Secret 名称在该名字空间中必须唯一。


  - **csi.readOnly** (boolean)

    传递到 ControllerPublishVolumeRequest 的 readOnly 值。默认为 false（读/写）。

  - **csi.volumeAttributes** (map[string]string)

    要发布的卷的 volumeAttributes。


- **fc** (FCVolumeSource)

  fc 表示挂接到 kubelet 的主机并随后暴露给 Pod 的一个光纤通道（FC）资源。

  <a name="FCVolumeSource"></a>
  **表示光纤通道卷。光纤通道卷只能以读/写一次进行挂载。光纤通道卷支持所有权管理和 SELinux 重新打标签。**


  - **fc.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。
    例如 “ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为 “ext4”。

  - **fc.lun** (int32)

    lun 是可选的。FC 目标 lun 编号。

  - **fc.readOnly** (boolean)

    readOnly 是可选的。默认为 false（读/写）。
    此处 readOnly 将在 VolumeMounts 中强制设置 readOnly。

  - **fc.targetWWNs** ([]string)

    targetWWNs 是可选的。FC 目标全球名称（WWN）。

  - **fc.wwids** ([]string)

    wwids 是可选的。FC 卷全球识别号（wwids）。
    必须设置 wwids 或 targetWWNs 及 lun 的组合，但不能同时设置两者。


- **flexVolume** (FlexPersistentVolumeSource)

  flexVolume 表示使用基于 exec 的插件制备/挂接的通用卷资源。

  <a name="FlexPersistentVolumeSource"></a>
  **FlexPersistentVolumeSource 表示使用基于 exec 的插件制备/挂接的通用持久卷资源。**


  - **flexVolume.driver** (string)，必需

    driver 是此卷所使用的驱动的名称。

  - **flexVolume.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。
    例如 “ext4”、“xfs”、“ntfs”。默认的文件系统取决于 flexVolume 脚本。

  - **flexVolume.options** (map[string]string)

    options 是可选的。此字段包含额外的命令选项（如果有）。

  - **flexVolume.readOnly** (boolean)

    readOnly 是可选的。默认为 false（读/写）。
    此处 readOnly 将在 VolumeMounts 中强制设置 readOnly。


  - **flexVolume.secretRef** (SecretReference)

    secretRef 是可选的。secretRef 是对包含敏感信息的 Secret 对象的引用，从而传递到插件脚本。
    如果未指定 Secret 对象，则此字段可以为空。如果 Secret 对象包含多个 Secret，则所有 Secret 被传递到插件脚本。

    <a name="SecretReference"></a>
    **SecretReference 表示对某 Secret 的引用，其中包含足够的信息来访问任何名字空间中的 Secret。**

    - **flexVolume.secretRef.name** (string)

      name 在名字空间内是唯一的，以引用一个 Secret 资源。

    - **flexVolume.secretRef.namespace** (string)

      namespace 指定一个名字空间，Secret 名称在该名字空间中必须唯一。


- **flocker** (FlockerVolumeSource)

  flocker 表示挂接到 kubelet 的主机并暴露给 Pod 供其使用的 Flocker 卷。
  这取决于所运行的 Flocker 控制服务。

  <a name="FlockerVolumeSource"></a>
  **表示 Flocker 代理挂载的 Flocker 卷。应设置且仅设置 datasetName 和 datasetUUID 中的一个。
  Flocker 卷不支持所有权管理或 SELinux 重新打标签。**

  - **flocker.datasetName** (string)

    datasetName 是存储为元数据的数据集的名称。针对 Flocker 有关数据集的名称应视为已弃用。

  - **flocker.datasetUUID** (string)

    datasetUUID 是数据集的 UUID。这是 Flocker 数据集的唯一标识符。


- **gcePersistentDisk** (GCEPersistentDiskVolumeSource)

  gcePersistentDisk 表示挂接到 kubelet 的主机随后暴露给 Pod 的一个 GCE Disk 资源。
  由管理员进行制备。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#gcepersistentdisk

  <a name="GCEPersistentDiskVolumeSource"></a>

  **表示 Google 计算引擎中的 Persistent Disk 资源。挂载到一个容器之前 GCE PD 必须存在。
  该磁盘还必须与 kubelet 位于相同的 GCE 项目和区域中。GCE PD 只能挂载为读/写一次或只读多次。
  GCE PD 支持所有权管理和 SELinux 重新打标签。**


  - **gcePersistentDisk.pdName** (string)，必需

    pdName 是 GCE 中 PD 资源的唯一名称。用于标识 GCE 中的磁盘。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#gcepersistentdisk

  - **gcePersistentDisk.fsType** (string)

    fsType 是你要挂载的卷的文件系统类型。提示：确保主机操作系统支持此文件系统类型。
    例如：“ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为 “ext4”。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#gcepersistentdisk

  - **gcePersistentDisk.partition** (int32)

    partition 是你要挂载的卷中的分区。如果省略，则默认为按卷名称进行挂载。
    例如：对于卷 /dev/sda1，将分区指定为 “1”。类似地，/dev/sda 的卷分区为 “0”（或可以将属性留空）。
    更多信息： https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#gcepersistentdisk

  - **gcePersistentDisk.readOnly** (boolean)

    此处 readOnly 将在 VolumeMounts 中强制设置 readOnly。默认为 false。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#gcepersistentdisk


- **glusterfs** （GlusterfsPersistentVolumeSource）

  glusterfs 表示关联到主机并暴露给 Pod 的 Glusterfs 卷。由管理员配置。
  更多信息：https://examples.k8s.io/volumes/glusterfs/README.md

  <a name="GlusterfsPersistentVolumeSource"></a>
  **表示在 Pod 生命周期内一直存在的 Glusterfs 挂载卷。Glusterfs 卷不支持属主管理或 SELinux 重标记。**


  - **glusterfs.endpoints** (string)，必需

    endpoints 是详细给出 Glusterfs 拓扑结构的端点的名称。
    更多信息: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod

  - **glusterfs.path** (string)，必需

    path 是 Glusterfs 卷的路径。
    更多信息: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod

  - **glusterfs.endpointsNamespace** (string)

    endpointsNamespace 是 Glusterfs 端点所在的命名空间。
    如果 endpointNamespace 为空，则默认值与所绑定的 PVC 的命名空间相同。
    更多信息: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod

  - **glusterfs.readOnly** (boolean)

    此处的 readOnly 将强制以只读权限挂载 Glusterfs 卷。
    默认为 false。
    更多信息: https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod


- **iscsi** (ISCSIPersistentVolumeSource)

  iscsi 表示挂接到 kubelet 的主机随后暴露给 Pod 的一个 ISCSI Disk 资源。由管理员进行制备。

  <a name="ISCSIPersistentVolumeSource"></a>
  **ISCSIPersistentVolumeSource 表示一个 ISCSI 磁盘。ISCSI 卷只能以读/写一次进行挂载。ISCSI 卷支持所有权管理和 SELinux 重新打标签。**


  - **iscsi.iqn** (string)，必需

    iqn 是目标 iSCSI 限定名称（Target iSCSI Qualified Name）。

  - **iscsi.lun** (int32)，必需

    lun 是 iSCSI 目标逻辑单元号（iSCSI Target Lun）。

  - **iscsi.targetPortal** (string)，必需

    targetPortal 是 iSCSI 目标门户（iSCSI Target Portal）。
    如果不是默认端口（通常是 TCP 端口 860 和 3260），则 Portal 为 IP 或 ip_addr:port。


  - **iscsi.chapAuthDiscovery** (boolean)

    chapAuthDiscovery 定义是否支持 iSCSI Discovery CHAP 身份认证。

  - **iscsi.chapAuthSession** (boolean)

    chapAuthSession 定义是否支持 iSCSI Session CHAP 身份认证。

  - **iscsi.fsType** (string)

    fsType 是你要挂载的卷的文件系统类型。提示：确保主机操作系统支持此文件系统类型。
    例如：“ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为 “ext4”。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#iscsi


  - **iscsi.initiatorName** (string)

    initiatorName 是自定义的 iSCSI 发起程序名称（iSCSI Initiator Name）。
    如果同时用 iscsiInterface 指定 initiatorName，将为连接创建新的 iSCSI 接口 \<目标门户>:\<卷名称>。

  - **iscsi.iscsiInterface** (string)

    iscsiInterface 是使用 iSCSI 传输的接口名称。默认为 “default”（tcp）。

  - **iscsi.portals** ([]string)

    portals 是 iSCSI 目标门户列表（iSCSI Target Portal List）。
    如果不是默认端口（通常是 TCP 端口 860 和 3260），则 Portal 为 IP 或 ip_addr:port。

  - **iscsi.readOnly** (boolean)

    此处 readOnly 将在 VolumeMounts 中强制设置 readOnly。默认为 false。


  - **iscsi.secretRef** (SecretReference)

    secretRef 是 iSCSI 目标和发起程序身份认证所用的 CHAP Secret。

    <a name="SecretReference"></a>
    **SecretReference 表示对某 Secret 的引用，其中包含足够的信息来访问任何名字空间中的 Secret。**

    - **iscsi.secretRef.name** (string)

      name 在名字空间内是唯一的，以引用一个 Secret 资源。

    - **iscsi.secretRef.namespace** (string)

      namespace 指定一个名字空间，Secret 名称在该名字空间中必须唯一。


- **nfs** (NFSVolumeSource)

  nfs 表示主机上挂载的 NFS。由管理员进行制备。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#nfs

  <a name="NFSVolumeSource"></a>
  **表示 Pod 的生命周期内持续的 NFS 挂载。NFS 卷不支持所有权管理或 SELinux 重新打标签。**

  - **nfs.path** (string)，必需

    path 是由 NFS 服务器导出的路径。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#nfs

  - **nfs.server** (string)，必需

    server 是 NFS 服务器的主机名或 IP 地址。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#nfs

  - **nfs.readOnly** (boolean)

    此处 readOnly 将强制使用只读权限挂载 NFS 导出。默认为 false。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#nfs


- **photonPersistentDisk** (PhotonPersistentDiskVolumeSource)

  photonPersistentDisk 表示 kubelet 主机上挂接和挂载的 PhotonController 持久磁盘。

  <a name="PhotonPersistentDiskVolumeSource"></a>
  **表示 Photon Controller 持久磁盘资源。**

  - **photonPersistentDisk.pdID** (string)，必需

    pdID 是标识 Photon Controller 持久磁盘的 ID。

  - **photonPersistentDisk.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。
    例如 “ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为 “ext4”。


- **portworxVolume** (PortworxVolumeSource)

  portworxVolume 表示 kubelet 主机上挂接和挂载的 portworx 卷。

  <a name="PortworxVolumeSource"></a>
  **PortworxVolumeSource 表示 Portworx 卷资源。**

  - **portworxVolume.volumeID** (string)，必需

    volumeID 唯一标识 Portworx 卷。

  - **portworxVolume.fsType** (string)

    fSType 表示要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。
    例如 “ext4”、“xfs”。如果未指定，则隐式推断为 “ext4”。

  - **portworxVolume.readOnly** (boolean)

    readOnly 默认为 false（读/写）。此处 readOnly 将在 VolumeMounts 中强制设置 readOnly。


- **quobyte** (QuobyteVolumeSource)

  quobyte 表示在共享 Pod 生命周期的主机上挂载的 Quobyte。

  <a name="QuobyteVolumeSource"></a>
  **表示在 Pod 的生命周期内持续的 Quobyte 挂载。Quobyte 卷不支持所有权管理或 SELinux 重新打标签。**

  - **quobyte.registry** (string)，必需

    registry 表示将一个或多个 Quobyte Registry 服务指定为 host:port
    对的字符串形式（多个条目用英文逗号分隔），用作卷的中央注册表。

  - **quobyte.volume** (string)，必需

    volume 是一个字符串，通过名称引用已创建的 Quobyte 卷。


  - **quobyte.group** (string)

    group 是将卷访问映射到的组。默认为无组。

  - **quobyte.readOnly** (boolean)

    此处 readOnly 将强制使用只读权限挂载 Quobyte 卷。默认为 false。

  - **quobyte.tenant** (string)

    后台中拥有给定 Quobyte 卷的租户。用于动态制备的 Quobyte 卷，其值由插件设置。

  - **quobyte.user** (string)

    user 是将卷访问映射到的用户。默认为 serivceaccount 用户。


- **rbd** (RBDPersistentVolumeSource)

  rbd 表示主机上挂载的 Rados 块设备，其生命周期与 Pod 生命周期相同。更多信息：
  https://examples.k8s.io/volumes/rbd/README.md

  <a name="RBDPersistentVolumeSource"></a>
  **表示在 Pod 的生命周期内一直存在的 Rados 块设备挂载。RBD 卷支持所有权管理和 SELinux 重新打标签。**

  - **rbd.image** (string)，必需

    image 是 rados 镜像名称。更多信息：
    https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it

  - **rbd.monitors** ([]string)，必需

    monitors 是 Ceph 监测的集合。更多信息：
    https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it


  - **rbd.fsType** (string)

    fsType 是你要挂载的卷的文件系统类型。提示：确保主机操作系统支持此文件系统类型。
    例如：“ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为 “ext4”。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#rbd

  - **rbd.keyring** (string)

    keyring 是给定用户的密钥环的路径。默认为 /etc/ceph/keyring。更多信息：
    https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it

  - **rbd.pool** (string)

    pool 是 rados 池名称。默认为 rbd。更多信息：
    https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it

  - **rbd.readOnly** (boolean)

    此处 readOnly 将在 VolumeMounts 中强制设置 readOnly。默认为 false。更多信息：
    https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it


  - **rbd.secretRef** (SecretReference)

    secretRef 是针对 RBDUser 的身份认证 Secret 的名称。如果提供，则重载 keyring。默认为 nil。
    更多信息： https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it

    <a name="SecretReference"></a>
    **SecretReference 表示对某 Secret 的引用，其中包含足够的信息来访问任何名字空间中的 Secret。**

    - **rbd.secretRef.name** (string)

      name 在名字空间内是唯一的，以引用一个 Secret 资源。

    - **rbd.secretRef.namespace** (string)

      namespace 指定一个名字空间，Secret 名称在该名字空间中必须唯一。

  - **rbd.user** (string)

    user 是 rados 用户名。默认为 admin。更多信息：
    https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it


- **scaleIO** (ScaleIOPersistentVolumeSource)

  scaleIO 表示 Kubernetes 节点上挂接和挂载的 ScaleIO 持久卷。

  <a name="ScaleIOPersistentVolumeSource"></a>
  **ScaleIOPersistentVolumeSource 表示一个 ScaleIO 持久卷。**

  - **scaleIO.gateway** (string)，必需

    gateway 是 ScaleIO API 网关的主机地址。


  - **scaleIO.secretRef** (SecretReference)，必需

    secretRef 引用包含 ScaleIO 用户和其他敏感信息的 Secret。如果未提供此项，则 Login 操作将失败。

    <a name="SecretReference"></a>
    **SecretReference 表示对某 Secret 的引用，其中包含足够的信息来访问任何名字空间中的 Secret。**

    - **scaleIO.secretRef.name** (string)

      name 在名字空间内是唯一的，以引用一个 Secret 资源。

    - **scaleIO.secretRef.namespace** (string)

      namespace 指定一个名字空间，Secret 名称在该名字空间中必须唯一。


  - **scaleIO.system** (string)，必需

    system 是 ScaleIO 中所配置的存储系统的名称。

  - **scaleIO.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。
    例如 “ext4”、“xfs”、“ntfs”。默认为 “xfs”。

  - **scaleIO.protectionDomain** (string)

    protectionDomain 是 ScaleIO 保护域（ScaleIO Protection Domain）的名称，用于已配置的存储。

  - **scaleIO.readOnly** (boolean)

    readOnly 默认为 false（读/写）。此处 readOnly 将在 VolumeMounts 中强制设置 readOnly。


  - **scaleIO.sslEnabled** (boolean)

    sslEnabled 是启用/禁用与网关（Gateway）进行 SSL 通信的标志，默认为 false。

  - **scaleIO.storageMode** (string)

    storageMode 指示卷所用的存储应是 ThickProvisioned 或 ThinProvisioned。
    默认为 ThinProvisioned。

  - **scaleIO.storagePool** (string)

    storagePool 是与保护域关联的 ScaleIO Storage Pool。

  - **scaleIO.volumeName** (string)

    volumeName 是在与此卷源关联的 ScaleIO 系统中已创建的卷的名称。


- **storageos** (StorageOSPersistentVolumeSource)

  storageOS 表示一个 StorageOS 卷，该卷被挂接到 kubelet 的主机并挂载到 Pod 中。更多信息：
  https://examples.k8s.io/volumes/storageos/README.md

  <a name="StorageOSPersistentVolumeSource"></a>
  **表示 StorageOS 持久卷资源。**

  - **storageos.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。
    例如 “ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为 “ext4”。

  - **storageos.readOnly** (boolean)

    readOnly 默认为 false（读/写）。此处 readOnly 将在 VolumeMounts 中强制设置 readOnly。


  - **storageos.secretRef** (<a href="{{< ref "../common-definitions/object-reference#ObjectReference" >}}">ObjectReference</a>)

    secretRef 指定用于获取 StorageOS API 凭据的 Secret。如果未指定，则将尝试使用默认值。

  - **storageos.volumeName** (string)

    volumeName 是 StorageOS 卷的人类可读名称。这些卷名称在一个名字空间内是唯一的。

  - **storageos.volumeNamespace** (string)

    volumeNamespace 指定 StorageOS 内卷的作用域。如果未指定名字空间，则将使用 Pod 的名字空间。
    这一字段的存在允许 Kubernetes 中名称作用域与 StorageOS 进行映射，实现更紧密的集成。
    将 volumeName 设为任何名称均可以重载默认的行为。
    如果你未在 StorageOS 内使用名字空间，则设为 “default”。
    StorageOS 内预先不存在的名字空间会被创建。


- **vsphereVolume** (VsphereVirtualDiskVolumeSource)

  vsphereVolume 表示 kubelet 主机上挂接和挂载的 vSphere 卷。

  <a name="VsphereVirtualDiskVolumeSource"></a>
  **表示 vSphere 卷资源。**

  - **vsphereVolume.volumePath** (string)，必需

    volumePath 是标识 vSphere 卷 vmdk 的路径。

  - **vsphereVolume.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。
    例如 “ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为 “ext4”。

  - **vsphereVolume.storagePolicyID** (string)

    storagePolicyID 是与 StoragePolicyName 关联的基于存储策略的管理（SPBM）配置文件 ID。

  - **vsphereVolume.storagePolicyName** (string)

    storagePolicyName 是基于存储策略的管理（SPBM）配置文件名称。

## PersistentVolumeStatus {#PersistentVolumeStatus}

PersistentVolumeStatus 是持久卷的当前状态。

<hr>


- **message** (string)

  message 是一条人类可读的消息，指明有关卷为何处于此状态的详细信息。

- **phase** (string)

  phase 表示一个卷是否可用，是否绑定到一个 PVC 或是否由某个 PVC 释放。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#phase

- **reason** (string)

  reason 是一个描述任何故障的简短 CamelCase 字符串，用于机器解析并在 CLI 中整齐地显示。

## PersistentVolumeList {#PersistentVolumeList}
PersistentVolumeList 是 PersistentVolume 各项的列表。

<hr>

- **apiVersion**: v1

- **kind**: PersistentVolumeList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **items** ([]<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>)，必需

  items 是持久卷的列表。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes

## 操作 {#Operations}

<hr>

### `get` 读取指定的 PersistentVolume
#### HTTP 请求
GET /api/v1/persistentvolumes/{name}

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolume 的名称

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): OK

401: Unauthorized

### `get` 读取指定的 PersistentVolume 的状态
#### HTTP 请求
GET /api/v1/persistentvolumes/{name}/status

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolume 的名称

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): OK

401: Unauthorized

### `list` 列出或观测类别为 PersistentVolume 的对象
#### HTTP 请求
GET /api/v1/persistentvolumes

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
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolumeList" >}}">PersistentVolumeList</a>): OK

401: Unauthorized

### `create` 创建 PersistentVolume
#### HTTP 请求
POST /api/v1/persistentvolumes

#### 参数
- **body**: <a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>，必需
- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): Created

202 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): Accepted

401: Unauthorized

### `update` 替换指定的 PersistentVolume
#### HTTP 请求
PUT /api/v1/persistentvolumes/{name}

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolume 的名称

- **body**: <a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): Created

401: Unauthorized

### `update` 替换指定的 PersistentVolume 的状态
#### HTTP 请求
PUT /api/v1/persistentvolumes/{name}/status

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolume 的名称

- **body**: <a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 PersistentVolume
#### HTTP 请求
PATCH /api/v1/persistentvolumes/{name}

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolume 的名称

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
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 PersistentVolume 的状态
#### HTTP 请求
PATCH /api/v1/persistentvolumes/{name}/status

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolume 的名称

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
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): Created

401: Unauthorized

### `delete` 删除 PersistentVolume
#### HTTP 请求
DELETE /api/v1/persistentvolumes/{name}

#### 参数
- **name** (**路径参数**): string，必需

  PersistentVolume 的名称

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
200 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): OK

202 (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolume" >}}">PersistentVolume</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 PersistentVolume 的集合
#### HTTP 请求
DELETE /api/v1/persistentvolumes

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
