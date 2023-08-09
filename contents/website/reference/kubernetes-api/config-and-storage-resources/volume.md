---
api_metadata:
  apiVersion: ""
  import: "k8s.io/api/core/v1"
  kind: "Volume"
content_type: "api_reference"
description: "Volume 表示 Pod 中一个有名字的卷，可以由 Pod 中的任意容器进行访问。"
title: "Volume"
weight: 3
---

`import "k8s.io/api/core/v1"`

## Volume {#Volume}
Volume 表示 Pod 中一个有名字的卷，可以由 Pod 中的任意容器进行访问。

<hr>

- **name** (string)，必需

  卷的名称。必须是 DNS_LABEL 且在 Pod 内是唯一的。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/#names

### 暴露的持久卷 {#exposed-persistent-volumes}

- **persistentVolumeClaim** (PersistentVolumeClaimVolumeSource)

  persistentVolumeClaimVolumeSource 表示对同一名字空间中 PersistentVolumeClaim 的引用。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#persistentvolumeclaims

  <a name="PersistentVolumeClaimVolumeSource"></a>
  **PersistentVolumeClaimVolumeSource 引用同一名字空间中用户的 PVC。
  此卷找到绑定的 PV 并为 Pod 挂载这个 PV 卷。
  PersistentVolumeClaimVolumeSource 本质上是其他人（或系统）拥有的另一类卷的包装类。**


  - **persistentVolumeClaim.claimName** (string)，必需

    claimName 是与使用此卷的 Pod 位于同一名字空间中的 PersistentVolumeClaim 的名称。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes#persistentvolumeclaims

  - **persistentVolumeClaim.readOnly** (boolean)

    readOnly 将在卷挂载中强制设置 readOnly 属性。默认为 false。

### 投射 {#projections}

- **configMap** (ConfigMapVolumeSource)

  configMap 表示应填充此卷的 configMap。

  <a name="ConfigMapVolumeSource"></a>
  **将 ConfigMap 适配到一个卷中。目标 ConfigMap 的 data 字段的内容将以文件的形式呈现在一个卷中，
  使用 data 字段中的键名作为文件名，除非 items 元素中已经填充了由键名到路径的特定映射。
  ConfigMap 卷支持所有权管理和 SELinux 重新打标签。**

  - **configMap.name** (string)

    被引用资源的名称。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/#names

  - **configMap.optional** (boolean)

    optional 指定是否所引用的 ConfigMap 或其键必须已经被定义。


  - **configMap.defaultMode** (int32)

    defaultMode 是可选的：默认情况下，模式位用于为已创建的文件设置权限。
    必须是 0000 到 0777 之间的八进制值或 0 到 511 之间的十进制值。
    YAML 既接受八进制值也接受十进制值，JSON 针对模式位需要十进制值。此字段默认为 0644。
    路径内的目录不受此设置的影响。这可能与影响文件模式的其他选项（如 fsGroup）有冲突，且结果可以是其他模式位也被设置。

  - **configMap.items** ([]<a href="{{< ref "../config-and-storage-resources/volume#KeyToPath" >}}">KeyToPath</a>)

    如果未指定 items，则所引用的 ConfigMap 的 data 字段中的每个键值对将作为一个文件被投射到卷中，
    这个文件的名称是键名，而文件的内容是键的取值。
    如果指定 items，则所列出的键将被投射到指定的路径中，且不会显示未列出的键。
    如果指定的键不在 ConfigMap 中，则卷设置将出错，除非对应的键被标记为可选。
    路径必须是相对路径，不能包含 “..” 路径，也不能以 “..” 开头。

- **secret** (SecretVolumeSource)

  secret 表示用来填充此卷的 Secret。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#secret

  <a name="SecretVolumeSource"></a>
  **将 Secret 适配到一个卷中。
  目标 Secret 的 data 字段的内容将以文件的形式呈现在一个卷中，使用 data 字段中的键名作为文件名。
  Secret 卷支持所有权管理和 SELinux 重新打标签。**


  - **secret.secretName** (string)

    secretName 是要使用的、位于 Pod 的名字空间中的 Secret 名称。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#secret

  - **secret.optional** (boolean)

    optional 字段指定是否 Secret 或其键必须已经定义。


  - **secret.defaultMode** (int32)

    defaultMode 是可选的：默认情况下，模式位用于为已创建的文件设置权限。
    必须是 0000 到 0777 之间的八进制值或 0 到 511 之间的十进制值。
    YAML 既接受八进制值也接受十进制值，JSON 针对模式位需要十进制值。此字段默认为 0644。
    路径内的目录不受此设置的影响。
    这可能与影响文件模式的其他选项（如 fsGroup）有冲突，且结果可以是其他模式位也被设置。

  - **secret.items** ([]<a href="{{< ref "../config-and-storage-resources/volume#KeyToPath" >}}">KeyToPath</a>)

    如果未指定 items，则所引用的 Secret 的 data 字段中的每个键值对将作为一个文件被投射到卷中，
    这个文件的名称是键名，而文件的内容是键的取值。
    如果指定 items，则所列出的键将被投射到指定的路径中，且不会显示未列出的键。
    如果指定的键不在 Secret 中，则卷设置将出错，除非对应的键被标记为可选。
    路径必须是相对路径，不能包含 “..” 路径，也不能以 “..” 开头。

- **downwardAPI** (DownwardAPIVolumeSource)

  downwardAPI 表示有关 Pod 的 Downward API，用来填充此卷。

  <a name="DownwardAPIVolumeSource"></a>
  **DownwardAPIVolumeSource 表示包含 Downward API 信息的一个卷。Downward API 卷支持所有权管理和 SELinux 重新打标签。**


  - **downwardAPI.defaultMode** (int32)

    可选：默认情况下，模式位用于已创建的文件。
    必须是可选的：默认情况下，模式位用于为已创建的文件设置权限。
    必须是 0000 到 0777 之间的八进制值或 0 到 511 之间的十进制值。
    YAML 既接受八进制值也接受十进制值，JSON 针对模式位需要十进制值。此字段默认为 0644。
    路径内的目录不受此设置的影响。这可能与影响文件模式的其他选项（如 fsGroup）有冲突，且结果可以是其他模式位也被设置。

  - **downwardAPI.items** ([]<a href="{{< ref "../config-and-storage-resources/volume#DownwardAPIVolumeFile" >}}">DownwardAPIVolumeFile</a>)

    items 是 Downward API 卷文件的列表。

- **projected** (ProjectedVolumeSource)

  这是供 Secret、ConfigMap 和 Downward API 等所有资源使用的投射项。

  <a name="ProjectedVolumeSource"></a>
  **表示一个投射的卷源。**

  - **projected.defaultMode** (int32)

    defaultMode 是默认情况下用于为已创建的文件设置权限的模式位。
    必须是 0000 到 0777 之间的八进制值或 0 到 511 之间的十进制值。
    YAML 既接受八进制值也接受十进制值，JSON 针对模式位需要十进制值。
    路径内的目录不受此设置的影响。
    这可能与影响文件模式的其他选项（如 fsGroup）有冲突，且结果可以是其他模式位也被设置。


  - **projected.sources** ([]VolumeProjection)

    sources 是卷投射的列表。

    <a name="VolumeProjection"></a>
    **这里的投射项目可能与其他受支持的卷类型一起进行投射。**

    - **projected.sources.configMap** (ConfigMapProjection)

      与要投射的 ConfigMap 数据有关的 ConfigMap 信息。

      <a name="ConfigMapProjection"></a>
      **将 ConfigMap 适配到一个投射的卷中。
      目标 ConfigMap 的 Data 字段的内容将以文件的形式呈现在一个被投射的卷中，
      使用 data 字段中的键名作为文件名，除非 items 元素中已经填充了由键名到路径的特定映射。
      请注意，这等同于没有默认模式的 ConfigMap 卷源。**


      - **projected.sources.configMap.name** (string)

        被引用资源的名称。更多信息：
        https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/#names

      - **projected.sources.configMap.optional** (boolean)

        optional 指定是否所引用的 ConfigMap 或其键必须已经被定义。


      - **projected.sources.configMap.items** ([]<a href="{{< ref "../config-and-storage-resources/volume#KeyToPath" >}}">KeyToPath</a>)

        如果未指定 items，则所引用的 ConfigMap 的 data 字段中的每个键值对将作为一个文件被投射到卷中，
        这个文件的名称是键名，而文件的内容是键的取值。
        如果指定 items，则所列出的键将被投射到指定的路径中，且不会显示未列出的键。
        如果指定的键不在 ConfigMap 中，则卷设置将出错，除非对应的键被标记为可选。
        路径必须是相对路径，不能包含 “..” 路径，也不能以 “..” 开头。


    - **projected.sources.downwardAPI** (DownwardAPIProjection)

      与要投射的 downward API 数据有关的 downward API 信息。

      <a name="DownwardAPIProjection"></a>
      **表示投射到投射卷的 Downward API 信息。请注意，这等同于没有默认模式的 downwardAPI 卷源。**

      - **projected.sources.downwardAPI.items** ([]<a href="{{< ref "../config-and-storage-resources/volume#DownwardAPIVolumeFile" >}}">DownwardAPIVolumeFile</a>)

        items 是 DownwardAPIVolume 文件的列表。


    - **projected.sources.secret** (SecretProjection)

      与要投射的 Secret 数据有关的 Secret 信息。

      <a name="SecretProjection"></a>
      **将 Secret 适配到一个投射卷中。
      目标 Secret 的 data 字段的内容将以文件的形式呈现在一个投射卷中，使用 data 字段中的键名作为文件名。
      请注意，这等同于没有默认模式的 Secret 卷源。**

      - **projected.sources.secret.name** (string)

        被引用资源的名称。更多信息：
        https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/#names


      - **projected.sources.secret.optional** (boolean)

        optional 字段指定是否 Secret 或其键必须已经定义。

      - **projected.sources.secret.items** ([]<a href="{{< ref "../config-and-storage-resources/volume#KeyToPath" >}}">KeyToPath</a>)

        如果未指定 items，则所引用的 Secret 的 data 字段中的每个键值对将作为一个文件被投射到卷中，
        这个文件的名称是键名，而文件的内容是键的取值。
        如果指定 items，则所列出的键将被投射到指定的路径中，且不会显示未列出的键。
        如果指定的键不在 Secret 中，则卷设置将出错，除非对应的键被标记为可选。
        路径必须是相对路径，不能包含 “..” 路径，也不能以 “..” 开头。


    - **projected.sources.serviceAccountToken** (ServiceAccountTokenProjection)

      serviceAccountToken 是与要投射的服务账号令牌数据有关的信息。

      <a name="ServiceAccountTokenProjection"></a>
      **ServiceAccountTokenProjection 表示一个投射的服务账号令牌卷。
      这种投射可用于将服务账号令牌插入到 Pod 运行时文件系统，供访问 API（Kubernetes API Server 或其他）使用。**

      - **projected.sources.serviceAccountToken.path** (string)，必需

        path 是相对于令牌投射目标文件的挂载点的路径。


      - **projected.sources.serviceAccountToken.audience** (string)

        audience 是令牌的目标受众。
        令牌的接收方必须用令牌受众中指定的一个标识符来标识自己，否则应拒绝此令牌。
        受众默认为 apiserver 的标识符。

      - **projected.sources.serviceAccountToken.expirationSeconds** (int64)

        expirationSeconds 是所请求的服务账号令牌的有效期。
        当令牌即将到期时，kubelet 卷插件将主动轮换服务账号令牌。
        如果令牌超过其生存时间的 80% 或令牌超过 24 小时，kubelet 将开始尝试轮换令牌。
        默认为 1 小时且必须至少为 10 分钟。

### 本地/临时目录 {#local-temporary-directory}

- **emptyDir** (EmptyDirVolumeSource)

  emptyDir 表示与 Pod 生命周期相同的临时目录。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#emptydir

  <a name="EmptyDirVolumeSource"></a>
  **表示供 Pod 使用的一个空目录。空目录卷支持所有权管理和 SELinux 重新打标签。**

  - **emptyDir.medium** (string)

    medium 表示此目录应使用哪种类别的存储介质。默认为 ""，这意味着使用节点的默认介质。
    必须是空字符串（默认值）或 Memory。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#emptydir


  - **emptyDir.sizeLimit** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

    sizeLimit 是这个 EmptyDir 卷所需的本地存储总量。这个大小限制也适用于内存介质。
    EmptyDir 的内存介质最大使用量将是此处指定的 sizeLimit 与 Pod 中所有容器内存限制总和这两个值之间的最小值。
    默认为 nil，这意味着限制未被定义。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes/#emptydir

- **hostPath** (HostPathVolumeSource)

  hostPath 表示主机上预先存在的文件或目录，它们将被直接暴露给容器。
  这种卷通常用于系统代理或允许查看主机的其他特权操作。大多数容器**不需要**这种卷。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#hostpath

  <a name="HostPathVolumeSource"></a>
  **表示映射到 Pod 中的主机路径。主机路径卷不支持所有权管理或 SELinux 重新打标签。**


  - **hostPath.path** (string)，必需

    目录在主机上的路径。如果该路径是一个符号链接，则它将沿着链接指向真实路径。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#hostpath

  - **hostPath.type** (string)

    HostPath 卷的类型。默认为 ""。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#hostpath

### 持久卷 {#persistent-volumes}

- **awsElasticBlockStore** (AWSElasticBlockStoreVolumeSource)

  awsElasticBlockStore 表示挂接到 kubelet 的主机随后暴露给 Pod 的一个 AWS Disk 资源。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#awselasticblockstore

  <a name="AWSElasticBlockStoreVolumeSource"></a>
  **表示 AWS 上的 Persistent Disk 资源。挂载到一个容器之前 AWS EBS 磁盘必须存在。
  该磁盘还必须与 kubelet 位于相同的 AWS 区域中。AWS EBS 磁盘只能以读/写一次进行挂载。
  AWS EBS 卷支持所有权管理和 SELinux 重新打标签。**


  - **awsElasticBlockStore.volumeID** (string)，必需

    volumeID 是 AWS（Amazon EBS 卷）中持久磁盘资源的唯一 ID。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#awselasticblockstore

  - **awsElasticBlockStore.fsType** (string)

    fsType 是你要挂载的卷的文件系统类型。提示：确保主机操作系统支持此文件系统类型。
    例如：“ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为 “ext4”。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#awselasticblockstore


  - **awsElasticBlockStore.partition** (int32)

    partition 是你要挂载的卷中的分区。如果省略，则默认为按卷名称进行挂载。例如：对于卷 /dev/sda1，
    将分区指定为 “1”。类似地，/dev/sda 的卷分区为 “0”（或可以将属性留空）。

  - **awsElasticBlockStore.readOnly** (boolean)

    readOnly 值为 true 将使得卷挂载被强制设置为 readOnly。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#awselasticblockstore

- **azureDisk** (AzureDiskVolumeSource)

  azureDisk 表示挂载到主机上并绑定挂载到 Pod 上的 Azure 数据盘。

  <a name="AzureDiskVolumeSource"></a>
  **azureDisk 表示挂载到主机上并绑定挂载到 Pod 上的 Azure 数据盘。**


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

    readOnly 默认为 false（读/写）。此处的 readOnly 将强制设置卷挂载中的 readOnly 属性。

- **azureFile** (AzureFileVolumeSource)

  azureDisk 表示挂载到主机上并绑定挂载到 Pod 上的 Azure File Service。

  <a name="AzureFileVolumeSource"></a>
  **azureFile 表示挂载到主机上并绑定挂载到 Pod 上的 Azure File Service。**


  - **azureFile.secretName** (string)，必需

    secretName 是包含 Azure 存储账号名称和主键的 Secret 的名称。

  - **azureFile.shareName** (string)，必需

    shareName 是 Azure 共享名称。

  - **azureFile.readOnly** (boolean)

    readOnly 默认为 false（读/写）。此处的 readOnly 将强制设置卷挂载中的 readOnly 属性。

- **cephfs** (CephFSVolumeSource)

  cephfs 表示在主机上挂载的 Ceph FS，该文件系统挂载与 Pod 的生命周期相同。

  <a name="CephFSVolumeSource"></a>
  **表示在 Pod 的生命周期内持续的 Ceph Filesystem 挂载。cephfs 卷不支持所有权管理或 SELinux 重新打标签。**

  - **cephfs.monitors** ([]string)，必需

    monitors 是必需的。monitors 是 Ceph 监测的集合。更多信息：
    https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it


  - **cephfs.path** (string)

    path 是可选的。用作挂载的根，而不是挂载完整的 Ceph 树，默认为 “/”。

  - **cephfs.readOnly** (boolean)

    readOnly 是可选的。默认为 false（读/写）。
    此处的 readOnly 将强制设置卷挂载中的 readOnly 属性。更多信息：
    https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it


  - **cephfs.secretFile** (string)

    secretFile 是可选的。secretFile 是 User 对应的密钥环的路径，默认为 /etc/ceph/user.secret。更多信息：
    https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it

  - **cephfs.secretRef** (<a href="{{< ref "../common-definitions/local-object-reference#LocalObjectReference" >}}">LocalObjectReference</a>)

    secretRef 是可选的。secretRef 是针对用户的身份认证 Secret 的引用，默认为空。更多信息：
    https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it

  - **cephfs.user** (string)

    user 是可选的。user 是 rados 用户名，默认为 admin。更多信息：
    https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it

- **cinder** (CinderVolumeSource)

  cinder 表示 kubelet 主机上挂接和挂载的 Cinder 卷。更多信息：
  https://examples.k8s.io/mysql-cinder-pd/README.md

  <a name="CinderVolumeSource"></a>
  **表示 Openstack 中的一个 Cinder 卷资源。挂载到一个容器之前 Cinder 卷必须已经存在。
  该卷还必须与 kubelet 位于相同的地区中。cinder 卷支持所有权管理和 SELinux 重新打标签。**

  - **cinder.volumeID** (string)，必需

    volumeID 用于标识 Cinder 中的卷。更多信息：
    https://examples.k8s.io/mysql-cinder-pd/README.md


  - **cinder.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。例如：“ext4”、“xfs”、“ntfs”。
    如果未指定，则隐式推断为“ext4”。更多信息：
    https://examples.k8s.io/mysql-cinder-pd/README.md

  - **cinder.readOnly** (boolean)

    readOnly 默认为 false（读/写）。此处的 readOnly 将强制设置卷挂载中的 readOnly 属性。
    更多信息： https://examples.k8s.io/mysql-cinder-pd/README.md

  - **cinder.secretRef** (<a href="{{< ref "../common-definitions/local-object-reference#LocalObjectReference" >}}">LocalObjectReference</a>)

    secretRef 是可选的。指向 Secret 对象，内含的参数用于连接到 OpenStack。

- **csi** (CSIVolumeSource)

  csi 表示由某个外部容器存储接口（Container Storage Interface，CSI）驱动处理的临时存储（Beta 特性）。

  <a name="CSIVolumeSource"></a>
  **表示要挂载的卷的源位置，由外部 CSI 驱动进行管理。**

  - **csi.driver** (string)，必需

    driver 是处理此卷的 CSI 驱动的名称。咨询你的管理员以获取在集群中注册的正确名称。

  - **csi.fsType** (string)

    要挂载的 fsType。例如 “ext4”、“xfs”、“ntfs”。
    如果未提供，则将空值传递给关联的 CSI 驱动，以便决定要应用的默认文件系统。


  - **csi.nodePublishSecretRef** (<a href="{{< ref "../common-definitions/local-object-reference#LocalObjectReference" >}}">LocalObjectReference</a>)

    nodePublishSecretRef 是对包含敏感信息的 Secret 对象的引用，
    该 Secret 对象将被传递到 CSI 驱动以完成 CSI NodePublishVolume 和 NodeUnpublishVolume 调用。
    此字段是可选的，如果不需要 Secret，则此字段可以为空。
    如果 Secret 对象包含多个 Secret，则所有 Secret 引用将被传递。

  - **csi.readOnly** (boolean)

    readOnly 指定供卷使用的只读配置。默认为 false（读/写）。

  - **csi.volumeAttributes** (map[string]string)

    volumeAttributes 存储传递给 CSI 驱动且特定于驱动的属性。查阅你的驱动文档，了解支持的值。

- **ephemeral** (EphemeralVolumeSource)

  ephemeral 表示由一个集群存储驱动处理的卷。此卷的生命周期与定义该卷的 Pod 相关联。
  Pod 启动前创建此卷，Pod 移除时删除此卷。


  使用此字段的情形包括：
  a) 仅在 Pod 运行时才需要此卷，
  b) 需要从快照恢复或容量跟踪等正常卷的功能特性，
  c) 通过存储类指定存储驱动，以及
  d) 存储驱动支持通过 PersistentVolumeClaim 进行动态卷制备
  （有关此卷类型和 PersistentVolumeClaim 之间连接的更多信息，请参考 EphemeralVolumeSource）。


  对于持续时间超过单个 Pod 生命周期的卷，使用 PersistentVolumeClaim 或某种特定于供应商的 API。

  如果打算以这种方式使用 CSI 驱动，则将 CSI 用于轻量级本地临时卷。更多的相关信息，请参考驱动文档。

  一个 Pod 可以同时使用临时卷和持久卷这两种类别的卷。


  <a name="EphemeralVolumeSource"></a>
  **表示由一个正常存储驱动处理的临时卷。**

  - **ephemeral.volumeClaimTemplate** (PersistentVolumeClaimTemplate)

    将用于创建独立的 PVC 以制备卷。
    嵌入了 EphemeralVolumeSource 的 Pod 将是 PVC 的所有者，即 PVC 将与 Pod 一起删除。
    PVC 的名称将是 `<pod 名称>-<卷名称>`，其中 `<卷名称>` 是来自 `PodSpec.Volumes` 数组条目的名称。
    如果串联的名称对于 PVC 无效（例如太长），则 Pod 验证将拒绝该 Pod。


    如果具有此名称的现有 PVC 不属于此 Pod，则这一 PVC 将 **不会** 被用于此 Pod，以避免错误地使用不相关的卷。
    如果出现这种情况，Pod 的启动操作会被阻塞直到不相关的 PVC 被移除。
    如果 Pod 准备使用这样一个预先创建的 PVC，那么一旦此 Pod 出现，就必须更新 PVC，
    将其属主引用指向该 Pod。通常没有必要这样做，但这对手动重构损坏的集群时可能很有用。

    此字段是只读的，PVC 被创建后 Kubernetes 不会对其进行任何更改。


    必需，不能为 nil。

    <a name="PersistentVolumeClaimTemplate"></a>
    **PersistentVolumeClaimTemplate 用于作为 EphemeralVolumeSource 的一部分生成 PersistentVolumeClaim 对象。**


    - **ephemeral.volumeClaimTemplate.spec** (<a href="{{< ref "../config-and-storage-resources/persistent-volume-claim-v1#PersistentVolumeClaimSpec" >}}">PersistentVolumeClaimSpec</a>)，必需

      PersistentVolumeClaim 的规约。整个规约的内容将被原封不动地复制到从此模板创建的 PVC 中。
      与 PersistentVolumeClaim 相同的字段在此处也有效。

    - **ephemeral.volumeClaimTemplate.metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

      可能包含一些标签和注解，在创建 PVC 时，这些数据会被复制到 PVC 中。
      在验证期间，其他字段都不允许设置，即便设置也会在验证阶段被拒绝。

- **fc** (FCVolumeSource)

  fc 表示挂接到 kubelet 的主机随后暴露给 Pod 的一个 Fibre Channel 资源。

  <a name="FCVolumeSource"></a>
  **表示 Fibre Channel 卷。Fibre Channel 卷只能以读/写一次进行挂载。
  Fibre Channel 卷支持所有权管理和 SELinux 重新打标签。**


  - **fc.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。
    例如 “ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为 “ext4”。

  - **fc.lun** (int32)

    lun 是可选的：FC 目标 lun 编号。


  - **fc.readOnly** (boolean)

    readOnly 是可选的。默认为 false（读/写）。此处的 readOnly 将强制设置卷挂载中的 readOnly 属性。

  - **fc.targetWWNs** ([]string)

    targetWWNs 是可选的。FC 目标全球名称（WWN）。

  - **fc.wwids** ([]string)

    wwids 是可选的。FC 卷全球识别号（wwids）。
    必须设置 wwids 或 targetWWNs 及 lun 的组合，但不能同时设置两者。

- **flexVolume** (FlexVolumeSource)

  flexVolume 表示使用基于 exec 的插件制备/挂接的通用卷资源。

  <a name="FlexVolumeSource"></a>
  **flexVolume 表示使用基于 exec 的插件制备/挂接的通用卷资源。**

  - **flexVolume.driver** (string)，必需

    driver 是供此卷使用的驱动的名称。

  - **flexVolume.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。例如 “ext4”、“xfs”、“ntfs”。
    默认的文件系统取决于 flexVolume 脚本。


  - **flexVolume.options** (map[string]string)

    options 是可选的。此字段包含额外的命令选项（如果有）。

  - **flexVolume.readOnly** (boolean)

    readOnly 是可选的。默认为 false（读/写）。此处的 readOnly 将强制设置卷挂载中的 readOnly 属性。

  - **flexVolume.secretRef** (<a href="{{< ref "../common-definitions/local-object-reference#LocalObjectReference" >}}">LocalObjectReference</a>)

    secretRef 是可选的。secretRef 是对包含敏感信息的 Secret 对象的引用，该 Secret 会被传递到插件脚本。
    如果未指定 Secret 对象，则此字段可以为空。如果 Secret 对象包含多个 Secret，则所有 Secret 被传递到插件脚本。

- **flocker** (FlockerVolumeSource)

  flocker 表示挂接到一个 kubelet 主机的 Flocker 卷。Flocker 卷依赖于正在运行的 Flocker 控制服务。

  <a name="FlockerVolumeSource"></a>
  **表示 Flocker 代理挂载的 Flocker 卷。应设置一个且仅设置 datasetName 和 datasetUUID 中的一个。
  Flocker 卷不支持所有权管理或 SELinux 重新打标签。**

  - **flocker.datasetName** (string)

    datasetName 是存储为元数据的数据集的名称。Flocker 数据集的名称应视为已弃用。

  - **flocker.datasetUUID** (string)

    datasetUUID 是数据集的 UUID。这是 Flocker 数据集的唯一标识符。

- **gcePersistentDisk** (GCEPersistentDiskVolumeSource)

  gcePersistentDisk 表示挂接到 kubelet 的主机随后暴露给 Pod 的一个 GCE Disk 资源。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#gcepersistentdisk

  <a name="GCEPersistentDiskVolumeSource"></a>
  **表示 Google Compute Engine 中的 Persistent Disk 资源。
  挂载到一个容器之前 GCE PD 必须已经存在。该磁盘还必须与 kubelet 位于相同的 GCE 项目和区域中。
  GCE PD 只能挂载为读/写一次或只读多次。GCE PD 支持所有权管理和 SELinux 重新打标签。**


  - **gcePersistentDisk.pdName** (string)，必需

    pdName 是 GCE 中 PD 资源的唯一名称。用于标识 GCE 中的磁盘。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#gcepersistentdisk

  - **gcePersistentDisk.fsType** (string)

    fsType 是你要挂载的卷的文件系统类型。提示：确保主机操作系统支持此文件系统类型。
    例如：“ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为“ext4”。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#gcepersistentdisk


  - **gcePersistentDisk.partition** (int32)

    partition 是你要挂载的卷中的分区。如果省略，则默认为按卷名称进行挂载。
    例如：对于卷 /dev/sda1，将分区指定为 “1”。类似地，/dev/sda 的卷分区为 “0”（或可以将属性留空）。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#gcepersistentdisk

  - **gcePersistentDisk.readOnly** (boolean)

    此处的 readOnly 将强制设置卷挂载中的 readOnly 属性。默认为 false。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#gcepersistentdisk


- **glusterfs** （GlusterfsVolumeSource）

  glusterfs 表示关联到主机并暴露给 Pod 的 Glusterfs 卷。由管理员配置。更多信息：
  https://examples.k8s.io/volumes/glusterfs/README.md

  <a name="GlusterfsVolumeSource"></a>

  **表示在 Pod 生命周期内一直存在的 Glusterfs 挂载卷。Glusterfs 卷不支持属主管理或 SELinux 重标记。**
  

  - **glusterfs.endpoints** (string)，必需

    endpoints 是详细给出 Glusterfs 拓扑结构的端点的名称。更多信息：
    https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod

  - **glusterfs.path** (string)，必需

    path 是 Glusterfs 卷的路径。更多信息：
    https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod

  - **glusterfs.readOnly** (boolean)

    此处的 readOnly 将强制以只读权限挂载 Glusterfs 卷。
    默认为 false。更多信息：
    https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod

- **iscsi** (ISCSIVolumeSource)

  iscsi 表示挂接到 kubelet 的主机随后暴露给 Pod 的一个 ISCSI Disk 资源。更多信息：
  https://examples.k8s.io/volumes/iscsi/README.md

  <a name="ISCSIVolumeSource"></a>
  **表示一个 ISCSI 磁盘。ISCSI 卷只能以读/写一次进行挂载。ISCSI 卷支持所有权管理和 SELinux 重新打标签。**


  - **iscsi.iqn** (string)，必需

    iqn 是目标 iSCSI 限定名称。

  - **iscsi.lun** (int32)，必需

    lun 表示 iSCSI 目标逻辑单元号。

  - **iscsi.targetPortal** (string)，必需

    targetPortal 是 iSCSI 目标门户。
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

    此处的 readOnly 将强制设置卷挂载中的 readOnly 属性。默认为 false。

  - **iscsi.secretRef** (<a href="{{< ref "../common-definitions/local-object-reference#LocalObjectReference" >}}">LocalObjectReference</a>)

    secretRef 是 iSCSI 目标和发起程序身份认证所用的 CHAP Secret。

- **nfs** (NFSVolumeSource)

  nfs 表示在主机上挂载的 NFS，其生命周期与 Pod 相同。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/volumes#nfs

  <a name="NFSVolumeSource"></a>
  **表示 Pod 的生命周期内一直存在的 NFS 挂载。NFS 卷不支持所有权管理或 SELinux 重新打标签。**

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

    fSType 表示要挂载的文件系统类型。必须是主机操作系统支持的文件系统类型。例如 “ext4”、“xfs”。
    如果未指定，则隐式推断为 “ext4”。

  - **portworxVolume.readOnly** (boolean)

    readOnly 默认为 false（读/写）。此处的 readOnly 将强制设置卷挂载中的 readOnly 属性。

- **quobyte** (QuobyteVolumeSource)

  quobyte 表示在共享 Pod 生命周期的主机上挂载的 Quobyte。

  <a name="QuobyteVolumeSource"></a>
  **表示在 Pod 的生命周期内持续的 Quobyte 挂载。Quobyte 卷不支持所有权管理或 SELinux 重新打标签。**


  - **quobyte.registry** (string)，必需

    registry 表示将一个或多个 Quobyte Registry 服务指定为 host:port 对的字符串形式
    （多个条目用英文逗号分隔），用作卷的中央注册表。

  - **quobyte.volume** (string)，必需

    volume 是按名称引用已创建的 Quobyte 卷的字符串。

  - **quobyte.group** (string)

    group 是将卷访问映射到的组。默认为无组。


  - **quobyte.readOnly** (boolean)

    此处 readOnly 将强制使用只读权限挂载 Quobyte 卷。默认为 false。

  - **quobyte.tenant** (string)

    tenant 拥有 Backend Used 中给定的 Quobyte 卷，随动态制备的 Quobyte 卷一起使用，值由插件设置。

  - **quobyte.user** (string)

    user 是将卷访问映射到的用户。默认为 serivceaccount 用户。


- **rbd** (RBDVolumeSource)

  rbd 表示在共享 Pod 生命周期的主机上挂载的 Rados Block Device。更多信息：
  https://examples.k8s.io/volumes/rbd/README.md

  <a name="RBDVolumeSource"></a>
  **表示在 Pod 的生命周期内持续的 Rados Block Device 挂载。RBD 卷支持所有权管理和 SELinux 重新打标签。**

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

    keyring 是 RBDUser 密钥环的路径。默认为 /etc/ceph/keyring。更多信息：
    https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it

  - **rbd.pool** (string)

    pool 是 rados 池名称。默认为 rbd。更多信息：
    https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it

  - **rbd.readOnly** (boolean)

    此处的 readOnly 将强制设置卷挂载中的 readOnly 属性。默认为 false。更多信息：
    https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it


  - **rbd.secretRef** (<a href="{{< ref "../common-definitions/local-object-reference#LocalObjectReference" >}}">LocalObjectReference</a>)

    secretRef 是 RBDUser 的身份认证 Secret 的名称。如果提供，则重载 keyring。默认为 nil。更多信息：
    https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it

  - **rbd.user** (string)

    user 是 rados 用户名。默认为 admin。更多信息：
    https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it

- **scaleIO** (ScaleIOVolumeSource)

  scaleIO 表示 Kubernetes 节点上挂接和挂载的 ScaleIO 持久卷。

  <a name="ScaleIOVolumeSource"></a>
  **ScaleIOVolumeSource 表示一个 ScaleIO 持久卷。**

  - **scaleIO.gateway** (string)，必需

    gateway 是 ScaleIO API 网关的主机地址。


  - **scaleIO.secretRef** (<a href="{{< ref "../common-definitions/local-object-reference#LocalObjectReference" >}}">LocalObjectReference</a>)，必需

    secretRef 引用到 ScaleIO 用户的 Secret 和其他敏感信息。如果未提供此项，则 Login 操作将失败。

  - **scaleIO.system** (string)，必需

    system 是存储系统的名称，与 ScaleIO 中的配置相同。

  - **scaleIO.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。例如 “ext4”、“xfs”、“ntfs”。默认为 “xfs”。


  - **scaleIO.protectionDomain** (string)

    protectionDomain 是 ScaleIO 保护域（ScaleIO Protection Domain）的名称，用于已配置的存储。

  - **scaleIO.readOnly** (boolean)

    readOnly 默认为 false（读/写）。此处的 readOnly 将强制设置卷挂载中的 readOnly 属性。

  - **scaleIO.sslEnabled** (boolean)

    sslEnabled 标志启用/禁用与网关的 SSL 通信，默认为 false。


  - **scaleIO.storageMode** (string)

    storageMode 指示卷所用的存储应是 ThickProvisioned 或 ThinProvisioned。默认为 ThinProvisioned。

  - **scaleIO.storagePool** (string)

    storagePool 是与保护域关联的 ScaleIO Storage Pool。

  - **scaleIO.volumeName** (string)

    volumeName 是在与此卷源关联的 ScaleIO 系统中已创建的卷的名称。

- **storageos** (StorageOSVolumeSource)

  storageOS 表示 Kubernetes 节点上挂接和挂载的 StorageOS 卷。

  <a name="StorageOSVolumeSource"></a>
  **表示 StorageOS 持久卷资源。**

  - **storageos.fsType** (string)

    fsType 是要挂载的文件系统类型。必须是主机操作系统所支持的文件系统类型之一。
    例如 “ext4”、“xfs”、“ntfs”。如果未指定，则隐式推断为 “ext4”。


  - **storageos.readOnly** (boolean)

    readOnly 默认为 false（读/写）。此处的 readOnly 将强制设置卷挂载中的 readOnly 属性。

  - **storageos.secretRef** (<a href="{{< ref "../common-definitions/local-object-reference#LocalObjectReference" >}}">LocalObjectReference</a>)

    secretRef 指定用于获取 StorageOS API 凭据的 Secret。如果未指定，则将尝试使用默认值。


  - **storageos.volumeName** (string)

    volumeName 是 StorageOS 卷的人类可读名称。这些卷名称在一个名字空间内是唯一的。

  - **storageos.volumeNamespace** (string)

    volumeNamespace 指定 StorageOS 内卷的作用域。如果未指定名字空间，则将使用 Pod 的名字空间。
    这个设置使得 Kubernetes 的名字作用域可以在 StorageOS 内进行映射，实现更紧密的集成。
    将 volumeName 设为任何名称以重载默认的行为。如果你未在 StorageOS 内使用名字空间，则设为“default”。
    将创建 StorageOS 内预先不存在的名字空间。

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

### 已弃用 {#deprecated}

- **gitRepo** (GitRepoVolumeSource)

  gitRepo 表示特定修订版本的 git 仓库。（注意：GitRepo 已被弃用。）如果与为某容器提速 Git 仓库，
  可以先将 emptyDir 挂载到 InitContainer 上，由后者使用 git 克隆仓库，然后将 emptyDir 挂载到 Pod 的容器中。

  <a name="GitRepoVolumeSource"></a>
  **表示用 Git 仓库的内容进行填充的一个卷。Git 仓库卷不支持所有权管理。Git 仓库卷支持 SELinux 重新打标签。
  （注意：GitRepo 已被弃用。）如果与为某容器提速 Git 仓库，
  可以先将 emptyDir 挂载到 InitContainer 上，由后者使用 git 克隆仓库，然后将 emptyDir 挂载到 Pod 的容器中。**


  - **gitRepo.repository** (string)，必需

    repository 是仓库的 URL。

  - **gitRepo.directory** (string)

    directory 是目标目录的名称。不得包含 “..” 或以 “..” 开头。如果提供了 “.”，则卷目录将是 Git 仓库。
    否则，如果指定，卷将用给定名称的子目录中存放 Git 仓库。

  - **gitRepo.revision** (string)

    revision 是指定修订版本的提交哈希值。

## DownwardAPIVolumeFile {#DownwardAPIVolumeFile}
DownwardAPIVolumeFile 表示创建包含 Pod 字段的文件的信息。

<hr>

- **path** (string)，必需

  必需。path 是要创建的文件的相对路径名称。不得使用绝对路径，也不得包含 “..” 路径。
  必须用 UTF-8 进行编码。相对路径的第一项不得用 “..” 开头。

- **fieldRef** (<a href="{{< ref "../common-definitions/object-field-selector#ObjectFieldSelector" >}}">ObjectFieldSelector</a>)

  必需。选择 Pod 的字段：仅支持注解、标签、名称和名字空间。

- **mode** (int32)

  可选：模式位用于设置文件的权限，必须是 0000 到 0777 之间的八进制值或 0 到 511 之间的十进制值。
  YAML 既接受八进制值也接受十进制值，JSON 针对模式位需要十进制值。
  如果未指定，则将使用卷 defaultMode。
  这可能与影响文件模式的其他选项（如 fsGroup）有冲突，且结果可以是其他模式位也被设置。

- **resourceFieldRef** (<a href="{{< ref "../common-definitions/resource-field-selector#ResourceFieldSelector" >}}">ResourceFieldSelector</a>)

  选择容器的资源：目前仅支持资源限制与请求（limits.cpu、limits.memory、requests.cpu 和 requests.memory）。

## KeyToPath {#KeyToPath}

将一个字符串键映射到卷中的一个路径。

<hr>

- **key** (string)，必需

  key 是要投射的键。

- **path** (string)，必需

  path 是将键映射到的文件的相对路径。不能是绝对路径。不能包含路径元素 “..”。不能以字符串 “..” 开头。

- **mode** (int32)

  mode 是可选的：模式位用于为文件设置权限。必须是 0000 到 0777 之间的八进制值或 0 到 511 之间的十进制值。
  YAML 既接受八进制值也接受十进制值，JSON 针对模式位需要十进制值。
  如果未指定，则将使用卷 defaultMode。
  这可能与影响文件模式的其他选项（如 fsGroup）有冲突，且结果可以是其他模式位也被设置。