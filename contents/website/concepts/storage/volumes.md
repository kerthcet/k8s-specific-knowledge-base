---
title: 卷
content_type: concept
weight: 10
---



容器中的文件在磁盘上是临时存放的，这给在容器中运行较重要的应用带来一些问题。
当容器崩溃或停止时会出现一个问题。此时容器状态未保存，
因此在容器生命周期内创建或修改的所有文件都将丢失。
在崩溃期间，kubelet 会以干净的状态重新启动容器。
当多个容器在一个 Pod 中运行并且需要共享文件时，会出现另一个问题。
跨所有容器设置和访问共享文件系统具有一定的挑战性。

Kubernetes {{< glossary_tooltip text="卷（Volume）" term_id="volume" >}}
这一抽象概念能够解决这两个问题。

阅读本文前建议你熟悉一下 [Pod](/zh-cn/docs/concepts/workloads/pods)。


## 背景  {#background}

Kubernetes 支持很多类型的卷。
{{< glossary_tooltip term_id="pod" text="Pod" >}} 可以同时使用任意数目的卷类型。
[临时卷](/zh-cn/docs/concepts/storage/ephemeral-volumes/)类型的生命周期与 Pod 相同，
但[持久卷](/zh-cn/docs/concepts/storage/persistent-volumes/)可以比 Pod 的存活期长。
当 Pod 不再存在时，Kubernetes 也会销毁临时卷；不过 Kubernetes 不会销毁持久卷。
对于给定 Pod 中任何类型的卷，在容器重启期间数据都不会丢失。

卷的核心是一个目录，其中可能存有数据，Pod 中的容器可以访问该目录中的数据。
所采用的特定的卷类型将决定该目录如何形成的、使用何种介质保存数据以及目录中存放的内容。

使用卷时, 在 `.spec.volumes` 字段中设置为 Pod 提供的卷，并在
`.spec.containers[*].volumeMounts` 字段中声明卷在容器中的挂载位置。
容器中的进程看到的文件系统视图是由它们的{{< glossary_tooltip text="容器镜像" term_id="image" >}}
的初始内容以及挂载在容器中的卷（如果定义了的话）所组成的。
其中根文件系统同容器镜像的内容相吻合。
任何在该文件系统下的写入操作，如果被允许的话，都会影响接下来容器中进程访问文件系统时所看到的内容。

卷挂载在镜像中的[指定路径](#using-subpath)下。
Pod 配置中的每个容器必须独立指定各个卷的挂载位置。

卷不能挂载到其他卷之上（不过存在一种[使用 subPath](#using-subpath) 的相关机制），也不能与其他卷有硬链接。

## 卷类型  {#volume-types}

Kubernetes 支持下列类型的卷：

### awsElasticBlockStore （已弃用）   {#awselasticblockstore}

{{< feature-state for_k8s_version="v1.17" state="deprecated" >}}

`awsElasticBlockStore` 卷将 Amazon Web 服务（AWS）[EBS 卷](https://aws.amazon.com/ebs/)挂载到你的
Pod 中。`emptyDir` 在 Pod 被删除时也会一起被删除，但 EBS 卷的内容在删除
Pod 时会被保留，卷只是被卸载掉了。
这意味着 EBS 卷可以预先填充数据，并且该数据可以在 Pod 之间共享。

{{< note >}}
你在使用 EBS 卷之前必须使用 `aws ec2 create-volume` 命令或者 AWS API 创建该卷。
{{< /note >}}

使用 `awsElasticBlockStore` 卷时有一些限制：

* Pod 运行所在的节点必须是 AWS EC2 实例。
* 这些实例需要与 EBS 卷在相同的地域（Region）和可用区（Availability-Zone）。
* EBS 卷只支持被挂载到单个 EC2 实例上。

#### 创建 AWS EBS 卷

在将 EBS 卷用到 Pod 上之前，你首先要创建它。

```shell
aws ec2 create-volume --availability-zone=eu-west-1a --size=10 --volume-type=gp2
```

确保该区域与你的集群所在的区域相匹配。还要检查卷的大小和 EBS 卷类型都适合你的用途。

#### AWS EBS 配置示例

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-ebs
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /test-ebs
      name: test-volume
  volumes:
  - name: test-volume
    # 此 AWS EBS 卷必须已经存在
    awsElasticBlockStore:
      volumeID: "<volume id>"
      fsType: ext4
```
如果 EBS 卷是分区的，你可以提供可选的字段 `partition: "<partition number>"` 来指定要挂载到哪个分区上。

#### AWS EBS CSI 卷迁移

{{< feature-state for_k8s_version="v1.25" state="stable" >}}

启用 `awsElasticBlockStore` 的 `CSIMigration` 特性后，所有插件操作将从现有的树内插件重定向到
`ebs.csi.aws.com` 容器存储接口（CSI）驱动程序。
为了使用此特性，必须在集群中安装
[AWS EBS CSI 驱动](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)。

#### AWS EBS CSI 迁移结束

{{< feature-state for_k8s_version="v1.17" state="alpha" >}}

要禁止控制器管理器和 kubelet 加载 `awsElasticBlockStore` 存储插件，
请将 `InTreePluginAWSUnregister` 标志设置为 `true`。

### azureDisk （已弃用）   {#azuredisk}

{{< feature-state for_k8s_version="v1.19" state="deprecated" >}}

`azureDisk` 卷类型用来在 Pod 上挂载 Microsoft Azure
[数据盘（Data Disk）](https://azure.microsoft.com/en-us/documentation/articles/virtual-machines-linux-about-disks-vhds/) 。
若需了解更多详情，请参考 [`azureDisk` 卷插件](https://github.com/kubernetes/examples/tree/master/staging/volumes/azure_disk/README.md)。

#### azureDisk 的 CSI 迁移  {#azuredisk-csi-migration}

{{< feature-state for_k8s_version="v1.24" state="stable" >}}

启用 `azureDisk` 的 `CSIMigration` 特性后，所有插件操作从现有的树内插件重定向到
`disk.csi.azure.com` 容器存储接口（CSI）驱动程序。
为了使用此特性，必须在集群中安装
[Azure 磁盘 CSI 驱动程序](https://github.com/kubernetes-sigs/azuredisk-csi-driver)。

#### azureDisk CSI 迁移完成

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

要禁止控制器管理器和 kubelet 加载 `azureDisk` 存储插件，
请将 `InTreePluginAzureDiskUnregister` 标志设置为 `true`。

### azureFile （已弃用）    {#azurefile}

{{< feature-state for_k8s_version="v1.21" state="deprecated" >}}

`azureFile` 卷类型用来在 Pod 上挂载 Microsoft Azure 文件卷（File Volume）（SMB 2.1 和 3.0）。
更多详情请参考 [`azureFile` 卷插件](https://github.com/kubernetes/examples/tree/master/staging/volumes/azure_file/README.md)。

#### azureFile CSI 迁移  {#azurefile-csi-migration}

{{< feature-state for_k8s_version="v1.26" state="stable" >}}

启用 `azureFile` 的 `CSIMigration` 特性后，所有插件操作将从现有的树内插件重定向到
`file.csi.azure.com` 容器存储接口（CSI）驱动程序。要使用此特性，必须在集群中安装
[Azure 文件 CSI 驱动程序](https://github.com/kubernetes-sigs/azurefile-csi-driver)，
并且 `CSIMigrationAzureFile`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
必须被启用。

Azure 文件 CSI 驱动尚不支持为同一卷设置不同的 fsgroup。
如果 `CSIMigrationAzureFile` 特性被启用，用不同的 fsgroup 来使用同一卷也是不被支持的。

#### azureFile CSI 迁移完成

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

要禁止控制器管理器和 kubelet 加载 `azureFile` 存储插件，
请将 `InTreePluginAzureFileUnregister` 标志设置为 `true`。

### cephfs {#cephfs}

`cephfs` 卷允许你将现存的 CephFS 卷挂载到 Pod 中。
不像 `emptyDir` 那样会在 Pod 被删除的同时也会被删除，`cephfs`
卷的内容在 Pod 被删除时会被保留，只是卷被卸载了。
这意味着 `cephfs` 卷可以被预先填充数据，且这些数据可以在
Pod 之间共享。同一 `cephfs` 卷可同时被多个写者挂载。

{{< note >}}
在使用 Ceph 卷之前，你的 Ceph 服务器必须已经运行并将要使用的 share 导出（exported）。
{{< /note >}}

更多信息请参考 [CephFS 示例](https://github.com/kubernetes/examples/tree/master/volumes/cephfs/)。

### cinder （已弃用）   {#cinder}

{{< feature-state for_k8s_version="v1.18" state="deprecated" >}}

{{< note >}}
Kubernetes 必须配置了 OpenStack Cloud Provider。
{{< /note >}}

`cinder` 卷类型用于将 OpenStack Cinder 卷挂载到 Pod 中。

#### Cinder 卷示例配置  {#cinder-volume-example-configuration}

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-cinder
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-cinder-container
    volumeMounts:
    - mountPath: /test-cinder
      name: test-volume
  volumes:
  - name: test-volume
    # 此 OpenStack 卷必须已经存在
    cinder:
      volumeID: "<volume id>"
      fsType: ext4
```

#### OpenStack CSI 迁移

{{< feature-state for_k8s_version="v1.24" state="stable" >}}

自 Kubernetes 1.21 版本起，Cinder 的 `CSIMigration` 特性是默认被启用的。
此特性会将插件的所有操作从现有的树内插件重定向到
`cinder.csi.openstack.org` 容器存储接口（CSI）驱动程序。
为了使用此特性，必须在集群中安装
[OpenStack Cinder CSI 驱动程序](https://github.com/kubernetes/cloud-provider-openstack/blob/master/docs/cinder-csi-plugin/using-cinder-csi-plugin.md)，
你可以通过设置 `CSIMigrationOpenStack`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
为 `false` 来禁止 Cinder CSI 迁移。

要禁止控制器管理器和 kubelet 加载树内 Cinder 插件，你可以启用
`InTreePluginOpenStackUnregister` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)。

### configMap

[`configMap`](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/)
卷提供了向 Pod 注入配置数据的方法。
ConfigMap 对象中存储的数据可以被 `configMap` 类型的卷引用，然后被 Pod 中运行的容器化应用使用。

引用 configMap 对象时，你可以在卷中通过它的名称来引用。
你可以自定义 ConfigMap 中特定条目所要使用的路径。
下面的配置显示了如何将名为 `log-config` 的 ConfigMap 挂载到名为 `configmap-pod`
的 Pod 中：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-pod
spec:
  containers:
    - name: test
      image: busybox:1.28
      volumeMounts:
        - name: config-vol
          mountPath: /etc/config
  volumes:
    - name: config-vol
      configMap:
        name: log-config
        items:
          - key: log_level
            path: log_level
```

`log-config` ConfigMap 以卷的形式挂载，并且存储在 `log_level`
条目中的所有内容都被挂载到 Pod 的 `/etc/config/log_level` 路径下。
请注意，这个路径来源于卷的 `mountPath` 和 `log_level` 键对应的 `path`。

{{< note >}}
* 在使用 [ConfigMap](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/) 之前你首先要创建它。
* ConfigMap 总是以 `readOnly` 的模式挂载。
* 容器以 [`subPath`](#using-subpath) 卷挂载方式使用 ConfigMap 时，将无法接收 ConfigMap 的更新。
* 文本数据挂载成文件时采用 UTF-8 字符编码。如果使用其他字符编码形式，可使用
  `binaryData` 字段。
{{< /note >}}

### downwardAPI {#downwardapi}

`downwardAPI` 卷用于为应用提供 {{< glossary_tooltip term_id="downward-api" text="downward API" >}} 数据。
在这类卷中，所公开的数据以纯文本格式的只读文件形式存在。

{{< note >}}
容器以 [subPath](#using-subpath) 卷挂载方式使用 downward API 时，在字段值更改时将不能接收到它的更新。
{{< /note >}}

更多详细信息请参考[通过文件将 Pod 信息呈现给容器](/zh-cn/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/)。

### emptyDir {#emptydir}

当 Pod 分派到某个节点上时，`emptyDir` 卷会被创建，并且在 Pod 在该节点上运行期间，卷一直存在。
就像其名称表示的那样，卷最初是空的。
尽管 Pod 中的容器挂载 `emptyDir` 卷的路径可能相同也可能不同，这些容器都可以读写
`emptyDir` 卷中相同的文件。
当 Pod 因为某些原因被从节点上删除时，`emptyDir` 卷中的数据也会被永久删除。

{{< note >}}
容器崩溃并**不**会导致 Pod 被从节点上移除，因此容器崩溃期间 `emptyDir` 卷中的数据是安全的。
{{< /note >}}

`emptyDir` 的一些用途：

* 缓存空间，例如基于磁盘的归并排序。
* 为耗时较长的计算任务提供检查点，以便任务能方便地从崩溃前状态恢复执行。
* 在 Web 服务器容器服务数据时，保存内容管理器容器获取的文件。

`emptyDir.medium` 字段用来控制 `emptyDir` 卷的存储位置。
默认情况下，`emptyDir` 卷存储在该节点所使用的介质上；
此处的介质可以是磁盘、SSD 或网络存储，这取决于你的环境。
你可以将 `emptyDir.medium` 字段设置为 `"Memory"`，
以告诉 Kubernetes 为你挂载 tmpfs（基于 RAM 的文件系统）。
虽然 tmpfs 速度非常快，但是要注意它与磁盘不同：tmpfs 在节点重启时会被清除，
并且你所写入的所有文件都会计入容器的内存消耗，受容器内存限制约束。

你可以通过为默认介质指定大小限制，来限制 `emptyDir` 卷的存储容量。
此存储是从[节点临时存储](/zh-cn/docs/concepts/configuration/manage-resources-containers/#setting-requests-and-limits-for-local-ephemeral-storage)中分配的。
如果来自其他来源（如日志文件或镜像分层数据）的数据占满了存储，`emptyDir`
可能会在达到此限制之前发生存储容量不足的问题。

{{< note >}}
当启用 `SizeMemoryBackedVolumes` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)时，
你可以为基于内存提供的卷指定大小。
如果未指定大小，则基于内存的卷的大小为 Linux 主机上内存的 50%。
{{< /note>}}

#### emptyDir 配置示例

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir:
      sizeLimit: 500Mi
```

### fc (光纤通道) {#fc}

`fc` 卷类型允许将现有的光纤通道块存储卷挂载到 Pod 中。
可以使用卷配置中的参数 `targetWWNs` 来指定单个或多个目标 WWN（World Wide Names）。
如果指定了多个 WWN，targetWWNs 期望这些 WWN 来自多路径连接。

{{< note >}}
你必须配置 FC SAN Zoning，以便预先向目标 WWN 分配和屏蔽这些 LUN（卷），这样
Kubernetes 主机才可以访问它们。
{{< /note >}}

更多详情请参考 [FC 示例](https://github.com/kubernetes/examples/tree/master/staging/volumes/fibre_channel)。

### gcePersistentDisk（已弃用） {#gcepersistentdisk}

{{< feature-state for_k8s_version="v1.17" state="deprecated" >}}

`gcePersistentDisk` 卷能将谷歌计算引擎 (GCE) [持久盘（PD）](http://cloud.google.com/compute/docs/disks)
挂载到你的 Pod 中。
不像 `emptyDir` 那样会在 Pod 被删除的同时也会被删除，持久盘卷的内容在删除 Pod
时会被保留，卷只是被卸载了。
这意味着持久盘卷可以被预先填充数据，并且这些数据可以在 Pod 之间共享。

{{< note >}}
在使用 PD 前，你必须使用 `gcloud` 或者 GCE API 或 UI 创建它。
{{< /note >}}

使用 `gcePersistentDisk` 时有一些限制：

* 运行 Pod 的节点必须是 GCE VM
* 这些 VM 必须和持久盘位于相同的 GCE 项目和区域（zone）

GCE PD 的一个特点是它们可以同时被多个消费者以只读方式挂载。
这意味着你可以用数据集预先填充 PD，然后根据需要并行地在尽可能多的 Pod 中提供该数据集。
不幸的是，PD 只能由单个使用者以读写模式挂载，即不允许同时写入。

在由 ReplicationController 所管理的 Pod 上使用 GCE PD 将会失败，除非 PD
是只读模式或者副本的数量是 0 或 1。

#### 创建 GCE 持久盘（PD）   {#gce-create-persistent-disk}

在 Pod 中使用 GCE 持久盘之前，你首先要创建它。

```shell
gcloud compute disks create --size=500GB --zone=us-central1-a my-data-disk
```

#### GCE 持久盘配置示例 {#gce-pd-configuration-example}

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /test-pd
      name: test-volume
  volumes:
  - name: test-volume
    # 此 GCE PD 必须已经存在
    gcePersistentDisk:
      pdName: my-data-disk
      fsType: ext4
```
#### 区域持久盘   {#regional-persistent-disks}

[区域持久盘](https://cloud.google.com/compute/docs/disks/#repds)特性允许你创建能在同一区域的两个可用区中使用的持久盘。
要使用这个特性，必须以持久卷（PersistentVolume）的方式提供卷；直接从
Pod 引用这种卷是不可以的。

#### 手动供应基于区域 PD 的 PersistentVolume {#manually-provisioning-regional-pd-pv}

使用[为 GCE PD 定义的存储类](/zh-cn/docs/concepts/storage/storage-classes/#gce-pd)
可以实现动态供应。在创建 PersistentVolume 之前，你首先要创建 PD。

```shell
gcloud compute disks create --size=500GB my-data-disk
  --region us-central1
  --replica-zones us-central1-a,us-central1-b
```

#### 区域持久盘配置示例

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-volume
spec:
  capacity:
    storage: 400Gi
  accessModes:
  - ReadWriteOnce
  gcePersistentDisk:
    pdName: my-data-disk
    fsType: ext4
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        # failure-domain.beta.kubernetes.io/zone 应在 1.21 之前使用
        - key: topology.kubernetes.io/zone
          operator: In
          values:
          - us-central1-a
          - us-central1-b
```

#### GCE CSI 迁移  {#gce-csi-migration}

{{< feature-state for_k8s_version="v1.25" state="stable" >}}

启用 GCE PD 的 `CSIMigration` 特性后，所有插件操作将从现有的树内插件重定向到
`pd.csi.storage.gke.io` 容器存储接口（CSI）驱动程序。
为了使用此特性，必须在集群中上安装
[GCE PD CSI 驱动程序](https://github.com/kubernetes-sigs/gcp-compute-persistent-disk-csi-driver)。

#### GCE CSI 迁移完成

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

要禁止控制器管理器和 kubelet 加载 `gcePersistentDisk` 存储插件，请将
`InTreePluginGCEUnregister` 标志设置为 `true`。


### gitRepo (已弃用)    {#gitrepo}

{{< warning >}}
`gitRepo` 卷类型已经被废弃。如果需要在容器中提供 git 仓库，请将一个
[EmptyDir](#emptydir) 卷挂载到 InitContainer 中，使用 git
命令完成仓库的克隆操作，然后将 [EmptyDir](#emptydir) 卷挂载到 Pod 的容器中。
{{< /warning >}}

`gitRepo` 卷是一个卷插件的例子。
该查卷挂载一个空目录，并将一个 Git 代码仓库克隆到这个目录中供 Pod 使用。

下面给出一个 `gitRepo` 卷的示例：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: server
spec:
  containers:
  - image: nginx
    name: nginx
    volumeMounts:
    - mountPath: /mypath
      name: git-volume
  volumes:
  - name: git-volume
    gitRepo:
      repository: "git@somewhere:me/my-git-repository.git"
      revision: "22f1d8406d464b0c0874075539c1f2e96c253775"
```

### glusterfs（已移除）   {#glusterfs}


Kubernetes {{< skew currentVersion >}} 不包含 `glusterfs` 卷类型。

GlusterFS 树内存储驱动程序在 Kubernetes v1.25 版本中被弃用，然后在 v1.26 版本中被完全移除。
 
### hostPath {#hostpath}

{{< warning >}}
HostPath 卷存在许多安全风险，最佳做法是尽可能避免使用 HostPath。
当必须使用 HostPath 卷时，它的范围应仅限于所需的文件或目录，并以只读方式挂载。

如果通过 AdmissionPolicy 限制 HostPath 对特定目录的访问，则必须要求
`volumeMounts` 使用 `readOnly` 挂载以使策略生效。
{{< /warning >}}

`hostPath` 卷能将主机节点文件系统上的文件或目录挂载到你的 Pod 中。
虽然这不是大多数 Pod 需要的，但是它为一些应用程序提供了强大的逃生舱。

例如，`hostPath` 的一些用法有：

* 运行一个需要访问 Docker 内部机制的容器；可使用 `hostPath` 挂载 `/var/lib/docker` 路径。
* 在容器中运行 cAdvisor 时，以 `hostPath` 方式挂载 `/sys`。
* 允许 Pod 指定给定的 `hostPath` 在运行 Pod 之前是否应该存在，是否应该创建以及应该以什么方式存在。

除了必需的 `path` 属性之外，你可以选择性地为 `hostPath` 卷指定 `type`。

支持的 `type` 值如下：

| 取值  | 行为     |
|:------|:---------|
| | 空字符串（默认）用于向后兼容，这意味着在安装 hostPath 卷之前不会执行任何检查。 |
| `DirectoryOrCreate` | 如果在给定路径上什么都不存在，那么将根据需要创建空目录，权限设置为 0755，具有与 kubelet 相同的组和属主信息。 |
| `Directory` | 在给定路径上必须存在的目录。|
| `FileOrCreate` | 如果在给定路径上什么都不存在，那么将在那里根据需要创建空文件，权限设置为 0644，具有与 kubelet 相同的组和所有权。|
| `File` | 在给定路径上必须存在的文件。|
| `Socket` | 在给定路径上必须存在的 UNIX 套接字。|
| `CharDevice` | 在给定路径上必须存在的字符设备。|
| `BlockDevice` | 在给定路径上必须存在的块设备。|

当使用这种类型的卷时要小心，因为：

* HostPath 卷可能会暴露特权系统凭据（例如 Kubelet）或特权
  API（例如容器运行时套接字），可用于容器逃逸或攻击集群的其他部分。
* 具有相同配置（例如基于同一 PodTemplate 创建）的多个 Pod
  会由于节点上文件的不同而在不同节点上有不同的行为。
* 下层主机上创建的文件或目录只能由 root 用户写入。
  你需要在[特权容器](/zh-cn/docs/tasks/configure-pod-container/security-context/)中以
  root 身份运行进程，或者修改主机上的文件权限以便容器能够写入 `hostPath` 卷。

#### hostPath 配置示例

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /test-pd
      name: test-volume
  volumes:
  - name: test-volume
    hostPath:
      # 宿主上目录位置
      path: /data
      # 此字段为可选
      type: Directory
```

{{< caution >}}
`FileOrCreate` 模式不会负责创建文件的父目录。
如果欲挂载的文件的父目录不存在，Pod 启动会失败。
为了确保这种模式能够工作，可以尝试把文件和它对应的目录分开挂载，如
[`FileOrCreate` 配置](#hostpath-fileorcreate-example) 所示。
{{< /caution >}}

#### hostPath FileOrCreate 配置示例  {#hostpath-fileorcreate-example}

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-webserver
spec:
  containers:
  - name: test-webserver
    image: registry.k8s.io/test-webserver:latest
    volumeMounts:
    - mountPath: /var/local/aaa
      name: mydir
    - mountPath: /var/local/aaa/1.txt
      name: myfile
  volumes:
  - name: mydir
    hostPath:
      # 确保文件所在目录成功创建。
      path: /var/local/aaa
      type: DirectoryOrCreate
  - name: myfile
    hostPath:
      path: /var/local/aaa/1.txt
      type: FileOrCreate
```

### iscsi

`iscsi` 卷能将 iSCSI (基于 IP 的 SCSI) 卷挂载到你的 Pod 中。
不像 `emptyDir` 那样会在删除 Pod 的同时也会被删除，`iscsi`
卷的内容在删除 Pod 时会被保留，卷只是被卸载。
这意味着 `iscsi` 卷可以被预先填充数据，并且这些数据可以在 Pod 之间共享。

{{< note >}}
在使用 iSCSI 卷之前，你必须拥有自己的 iSCSI 服务器，并在上面创建卷。
{{< /note >}}

iSCSI 的一个特点是它可以同时被多个用户以只读方式挂载。
这意味着你可以用数据集预先填充卷，然后根据需要在尽可能多的 Pod 上使用它。
不幸的是，iSCSI 卷只能由单个使用者以读写模式挂载。不允许同时写入。

更多详情请参考 [iSCSI 示例](https://github.com/kubernetes/examples/tree/master/volumes/iscsi)。

### local

`local` 卷所代表的是某个被挂载的本地存储设备，例如磁盘、分区或者目录。

`local` 卷只能用作静态创建的持久卷。不支持动态配置。

与 `hostPath` 卷相比，`local` 卷能够以持久和可移植的方式使用，而无需手动将 Pod
调度到节点。系统通过查看 PersistentVolume 的节点亲和性配置，就能了解卷的节点约束。

然而，`local` 卷仍然取决于底层节点的可用性，并不适合所有应用程序。
如果节点变得不健康，那么 `local` 卷也将变得不可被 Pod 访问。使用它的 Pod 将不能运行。
使用 `local` 卷的应用程序必须能够容忍这种可用性的降低，以及因底层磁盘的耐用性特征而带来的潜在的数据丢失风险。

下面是一个使用 `local` 卷和 `nodeAffinity` 的持久卷示例：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: example-pv
spec:
  capacity:
    storage: 100Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete
  storageClassName: local-storage
  local:
    path: /mnt/disks/ssd1
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - example-node
```

使用 `local` 卷时，你需要设置 PersistentVolume 对象的 `nodeAffinity` 字段。
Kubernetes 调度器使用 PersistentVolume 的 `nodeAffinity` 信息来将使用 `local`
卷的 Pod 调度到正确的节点。

PersistentVolume 对象的 `volumeMode` 字段可被设置为 "Block"
（而不是默认值 "Filesystem"），以将 `local` 卷作为原始块设备暴露出来。

使用 `local` 卷时，建议创建一个 StorageClass 并将其 `volumeBindingMode` 设置为
`WaitForFirstConsumer`。要了解更多详细信息，请参考
[local StorageClass 示例](/zh-cn/docs/concepts/storage/storage-classes/#local)。
延迟卷绑定的操作可以确保 Kubernetes 在为 PersistentVolumeClaim 作出绑定决策时，会评估
Pod 可能具有的其他节点约束，例如：如节点资源需求、节点选择器、Pod 亲和性和 Pod 反亲和性。

你可以在 Kubernetes 之外单独运行静态驱动以改进对 local 卷的生命周期管理。
请注意，此驱动尚不支持动态配置。
有关如何运行外部 `local` 卷驱动，请参考
[local 卷驱动用户指南](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner)。

{{< note >}}
如果不使用外部静态驱动来管理卷的生命周期，用户需要手动清理和删除 local 类型的持久卷。
{{< /note >}}

### nfs

`nfs` 卷能将 NFS (网络文件系统) 挂载到你的 Pod 中。
不像 `emptyDir` 那样会在删除 Pod 的同时也会被删除，`nfs` 卷的内容在删除 Pod
时会被保存，卷只是被卸载。
这意味着 `nfs` 卷可以被预先填充数据，并且这些数据可以在 Pod 之间共享。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /my-nfs-data
      name: test-volume
  volumes:
  - name: test-volume
    nfs:
      server: my-nfs-server.example.com
      path: /my-nfs-volume
      readOnly: true
```

{{< note >}}
在使用 NFS 卷之前，你必须运行自己的 NFS 服务器并将目标 share 导出备用。

还需要注意，不能在 Pod spec 中指定 NFS 挂载可选项。
可以选择设置服务端的挂载可选项，或者使用
[/etc/nfsmount.conf](https://man7.org/linux/man-pages/man5/nfsmount.conf.5.html)。
此外，还可以通过允许设置挂载可选项的持久卷挂载 NFS 卷。
{{< /note >}}

如需了解用持久卷挂载 NFS 卷的示例，请参考 [NFS 示例](https://github.com/kubernetes/examples/tree/master/staging/volumes/nfs)。

### persistentVolumeClaim {#persistentvolumeclaim}

`persistentVolumeClaim` 卷用来将[持久卷](/zh-cn/docs/concepts/storage/persistent-volumes/)（PersistentVolume）挂载到 Pod 中。
持久卷申领（PersistentVolumeClaim）是用户在不知道特定云环境细节的情况下“申领”持久存储（例如
GCE PersistentDisk 或者 iSCSI 卷）的一种方法。

更多详情请参考[持久卷](/zh-cn/docs/concepts/storage/persistent-volumes/)。

### portworxVolume（已弃用） {#portworxvolume}

{{< feature-state for_k8s_version="v1.25" state="deprecated" >}}

`portworxVolume` 是一个可伸缩的块存储层，能够以超融合（hyperconverged）的方式与 Kubernetes 一起运行。
[Portworx](https://portworx.com/use-case/kubernetes-storage/)
支持对服务器上存储的指纹处理、基于存储能力进行分层以及跨多个服务器整合存储容量。
Portworx 可以以 in-guest 方式在虚拟机中运行，也可以在裸金属 Linux 节点上运行。

`portworxVolume` 类型的卷可以通过 Kubernetes 动态创建，也可以预先配备并在 Pod 内引用。
下面是一个引用预先配备的 Portworx 卷的示例 Pod：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-portworx-volume-pod
spec:
  containers:
  - image: registry.k8s.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /mnt
      name: pxvol
  volumes:
  - name: pxvol
    # 此 Portworx 卷必须已经存在
    portworxVolume:
      volumeID: "pxvol"
      fsType: "<fs-type>"
```

{{< note >}}
在 Pod 中使用 portworxVolume 之前，你要确保有一个名为 `pxvol` 的 PortworxVolume 存在。
{{< /note >}}

更多详情可以参考 [Portworx 卷](https://github.com/kubernetes/examples/tree/master/staging/volumes/portworx/README.md)。

#### Portworx CSI 迁移

{{< feature-state for_k8s_version="v1.25" state="beta" >}}

已针对 Portworx 添加 `CSIMigration` 特性，但在 Kubernetes 1.23 中默认禁用，因为它处于 Alpha 状态。
自 v1.25 以来它已进入 Beta 阶段，但默认仍关闭。
它将所有插件操作不再指向树内插件（In-Tree Plugin），转而指向
`pxd.portworx.com` 容器存储接口（Container Storage Interface，CSI）驱动。
[Portworx CSI 驱动程序](https://docs.portworx.com/portworx-install-with-kubernetes/storage-operations/csi/)必须安装在集群上。
要启用此特性，需在 kube-controller-manager 和 kubelet 中设置 `CSIMigrationPortworx=true`。

### projected （投射）   {#projected}

投射卷能将若干现有的卷来源映射到同一目录上。更多详情请参考[投射卷](/zh-cn/docs/concepts/storage/projected-volumes/)。

### rbd

`rbd` 卷允许将 [Rados 块设备](https://docs.ceph.com/en/latest/rbd/)卷挂载到你的 Pod 中。
不像 `emptyDir` 那样会在删除 Pod 的同时也会被删除，`rbd` 卷的内容在删除 Pod 时会被保存，卷只是被卸载。
这意味着 `rbd` 卷可以被预先填充数据，并且这些数据可以在 Pod 之间共享。

{{< note >}}
在使用 RBD 之前，你必须安装运行 Ceph。
{{< /note >}}

RBD 的一个特性是它可以同时被多个用户以只读方式挂载。
这意味着你可以用数据集预先填充卷，然后根据需要在尽可能多的 Pod 中并行地使用卷。
不幸的是，RBD 卷只能由单个使用者以读写模式安装。不允许同时写入。

更多详情请参考
[RBD 示例](https://github.com/kubernetes/examples/tree/master/volumes/rbd)。

#### RBD CSI 迁移 {#rbd-csi-migration}

{{< feature-state for_k8s_version="v1.23" state="alpha" >}}

启用 RBD 的 `CSIMigration` 特性后，所有插件操作从现有的树内插件重定向到
`rbd.csi.ceph.com` {{<glossary_tooltip text="CSI" term_id="csi" >}} 驱动程序。
要使用该特性，必须在集群内安装
[Ceph CSI 驱动](https://github.com/ceph/ceph-csi)，并启用 `csiMigrationRBD`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)。
（请注意，`csiMigrationRBD` 标志已在 v1.24 版本中移除且替换为 `CSIMigrationRBD`。）

{{< note >}}
作为一位管理存储的 Kubernetes 集群操作者，在尝试迁移到 RBD CSI 驱动前，你必须完成下列先决事项：

* 你必须在集群中安装 v3.5.0 或更高版本的 Ceph CSI 驱动（`rbd.csi.ceph.com`）。
* 因为 `clusterID` 是 CSI 驱动程序必需的参数，而树内存储类又将 `monitors`
  作为一个必需的参数，所以 Kubernetes 存储管理者需要根据 `monitors`
  的哈希值（例：`#echo -n '<monitors_string>' | md5sum`）来创建
  `clusterID`，并保持该 `monitors` 存在于该 `clusterID` 的配置中。
* 同时，如果树内存储类的 `adminId` 的值不是 `admin`，那么其 `adminSecretName`
  就需要被修改成 `adminId` 参数的 base64 编码值。
{{< /note >}}

### secret

`secret` 卷用来给 Pod 传递敏感信息，例如密码。你可以将 Secret 存储在 Kubernetes
API 服务器上，然后以文件的形式挂载到 Pod 中，无需直接与 Kubernetes 耦合。
`secret` 卷由 tmpfs（基于 RAM 的文件系统）提供存储，因此它们永远不会被写入非易失性（持久化的）存储器。

{{< note >}}
* 使用前你必须在 Kubernetes API 中创建 Secret。
* Secret 总是以 `readOnly` 的模式挂载。
* 容器以 [`subPath`](#using-subpath) 卷挂载方式使用 Secret 时，将无法接收 Secret 的更新。
{{< /note >}}

更多详情请参考[配置 Secrets](/zh-cn/docs/concepts/configuration/secret/)。

### vsphereVolume（已弃用） {#vspherevolume}

{{< note >}}
建议你改用 vSphere CSI 树外驱动程序。
{{< /note >}}

`vsphereVolume` 用来将 vSphere VMDK 卷挂载到你的 Pod 中。
在卸载卷时，卷的内容会被保留。
vSphereVolume 卷类型支持 VMFS 和 VSAN 数据仓库。

进一步信息可参考
[vSphere 卷](https://github.com/kubernetes/examples/tree/master/staging/volumes/vsphere)。

#### vSphere CSI 迁移  {#vsphere-csi-migration}

{{< feature-state for_k8s_version="v1.26" state="stable" >}}


在 Kubernetes {{< skew currentVersion >}} 中，对树内 `vsphereVolume`
类的所有操作都会被重定向至 `csi.vsphere.vmware.com` {{< glossary_tooltip text="CSI" term_id="csi" >}} 驱动程序。

[vSphere CSI 驱动](https://github.com/kubernetes-sigs/vsphere-csi-driver)必须安装到集群上。
你可以在 VMware 的文档页面[迁移树内 vSphere 卷插件到 vSphere 容器存储插件](https://docs.vmware.com/en/VMware-vSphere-Container-Storage-Plug-in/2.0/vmware-vsphere-csp-getting-started/GUID-968D421F-D464-4E22-8127-6CB9FF54423F.html)
中找到有关如何迁移树内 `vsphereVolume` 的其他建议。
如果未安装 vSphere CSI 驱动程序，则无法对由树内 `vsphereVolume` 类型创建的 PV 执行卷操作。

你必须运行 vSphere 7.0u2 或更高版本才能迁移到 vSphere CSI 驱动程序。

如果你正在运行 Kubernetes v{{< skew currentVersion >}}，请查阅该 Kubernetes 版本的文档。

{{< note >}}
vSphere CSI 驱动不支持内置 `vsphereVolume` 的以下 StorageClass 参数：

* `diskformat`
* `hostfailurestotolerate`
* `forceprovisioning`
* `cachereservation`
* `diskstripes`
* `objectspacereservation`
* `iopslimit`

使用这些参数创建的现有卷将被迁移到 vSphere CSI 驱动，不过使用 vSphere
CSI 驱动所创建的新卷都不会理会这些参数。

{{< /note >}}

#### vSphere CSI 迁移完成   {#vsphere-csi-migration-complete}

{{< feature-state for_k8s_version="v1.19" state="beta" >}}

为了避免控制器管理器和 kubelet 加载 `vsphereVolume` 插件，你需要将
`InTreePluginvSphereUnregister` 特性设置为 `true`。你还必须在所有工作节点上安装
`csi.vsphere.vmware.com` {{< glossary_tooltip text="CSI" term_id="csi" >}} 驱动。

## 使用 subPath  {#using-subpath}

有时，在单个 Pod 中共享卷以供多方使用是很有用的。
`volumeMounts.subPath` 属性可用于指定所引用的卷内的子路径，而不是其根路径。

下面例子展示了如何配置某包含 LAMP 堆栈（Linux Apache MySQL PHP）的 Pod 使用同一共享卷。
此示例中的 `subPath` 配置不建议在生产环境中使用。
PHP 应用的代码和相关数据映射到卷的 `html` 文件夹，MySQL 数据库存储在卷的 `mysql` 文件夹中：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-lamp-site
spec:
    containers:
    - name: mysql
      image: mysql
      env:
      - name: MYSQL_ROOT_PASSWORD
        value: "rootpasswd"
      volumeMounts:
      - mountPath: /var/lib/mysql
        name: site-data
        subPath: mysql
    - name: php
      image: php:7.0-apache
      volumeMounts:
      - mountPath: /var/www/html
        name: site-data
        subPath: html
    volumes:
    - name: site-data
      persistentVolumeClaim:
        claimName: my-lamp-site-data
```

### 使用带有扩展环境变量的 subPath  {#using-subpath-expanded-environment}

{{< feature-state for_k8s_version="v1.17" state="stable" >}}

使用 `subPathExpr` 字段可以基于 downward API 环境变量来构造 `subPath` 目录名。
`subPath` 和 `subPathExpr` 属性是互斥的。

在这个示例中，`Pod` 使用 `subPathExpr` 来 `hostPath` 卷 `/var/log/pods` 中创建目录 `pod1`。
`hostPath` 卷采用来自 `downwardAPI` 的 Pod 名称生成目录名。
宿主目录 `/var/log/pods/pod1` 被挂载到容器的 `/logs` 中。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod1
spec:
  containers:
  - name: container1
    env:
    - name: POD_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    image: busybox:1.28
    command: [ "sh", "-c", "while [ true ]; do echo 'Hello'; sleep 10; done | tee -a /logs/hello.txt" ]
    volumeMounts:
    - name: workdir1
      mountPath: /logs
      # 包裹变量名的是小括号，而不是大括号
      subPathExpr: $(POD_NAME)
  restartPolicy: Never
  volumes:
  - name: workdir1
    hostPath:
      path: /var/log/pods
```

## 资源   {#resources}

`emptyDir` 卷的存储介质（例如磁盘、SSD 等）是由保存 kubelet
数据的根目录（通常是 `/var/lib/kubelet`）的文件系统的介质确定。
Kubernetes 对 `emptyDir` 卷或者 `hostPath` 卷可以消耗的空间没有限制，容器之间或 Pod 之间也没有隔离。

要了解如何使用资源规约来请求空间，
可参考[如何管理资源](/zh-cn/docs/concepts/configuration/manage-resources-containers/)。

## 树外（Out-of-Tree）卷插件    {#out-of-tree-volume-plugins}

Out-of-Tree 卷插件包括{{< glossary_tooltip text="容器存储接口（CSI）" term_id="csi" >}}和
FlexVolume（已弃用）。它们使存储供应商能够创建自定义存储插件，而无需将插件源码添加到
Kubernetes 代码仓库。

以前，所有卷插件（如上面列出的卷类型）都是“树内（In-Tree）”的。
“树内”插件是与 Kubernetes 的核心组件一同构建、链接、编译和交付的。
这意味着向 Kubernetes 添加新的存储系统（卷插件）需要将代码合并到 Kubernetes 核心代码库中。

CSI 和 FlexVolume 都允许独立于 Kubernetes 代码库开发卷插件，并作为扩展部署（安装）在 Kubernetes 集群上。

对于希望创建树外（Out-Of-Tree）卷插件的存储供应商，请参考
[卷插件常见问题](https://github.com/kubernetes/community/blob/master/sig-storage/volume-plugin-faq.md)。

### CSI

[容器存储接口](https://github.com/container-storage-interface/spec/blob/master/spec.md) (CSI)
为容器编排系统（如 Kubernetes）定义标准接口，以将任意存储系统暴露给它们的容器工作负载。

更多详情请阅读 [CSI 设计方案](https://git.k8s.io/design-proposals-archive/storage/container-storage-interface.md)。

{{< note >}}
Kubernetes v1.13 废弃了对 CSI 规范版本 0.2 和 0.3 的支持，并将在以后的版本中删除。
{{< /note >}}

{{< note >}}
CSI 驱动可能并非兼容所有的 Kubernetes 版本。
请查看特定 CSI 驱动的文档，以了解各个 Kubernetes 版本所支持的部署步骤以及兼容性列表。
{{< /note >}}

一旦在 Kubernetes 集群上部署了 CSI 兼容卷驱动程序，用户就可以使用
`csi` 卷类型来挂接、挂载 CSI 驱动所提供的卷。

`csi` 卷可以在 Pod 中以三种方式使用：

* 通过 PersistentVolumeClaim(#persistentvolumeclaim) 对象引用
* 使用[一般性的临时卷](/zh-cn/docs/concepts/storage/ephemeral-volumes/#generic-ephemeral-volumes)
* 使用 [CSI 临时卷](/zh-cn/docs/concepts/storage/ephemeral-volumes/#csi-ephemeral-volumes)，
  前提是驱动支持这种用法

存储管理员可以使用以下字段来配置 CSI 持久卷：

* `driver`：指定要使用的卷驱动名称的字符串值。
  这个值必须与 CSI 驱动程序在 `GetPluginInfoResponse` 中返回的值相对应；该接口定义在
  [CSI 规范](https://github.com/container-storage-interface/spec/blob/master/spec.md#getplugininfo)中。
  Kubernetes 使用所给的值来标识要调用的 CSI 驱动程序；CSI
  驱动程序也使用该值来辨识哪些 PV 对象属于该 CSI 驱动程序。

* `volumeHandle`：唯一标识卷的字符串值。
  该值必须与 CSI 驱动在 `CreateVolumeResponse` 的 `volume_id` 字段中返回的值相对应；接口定义在
  [CSI 规范](https://github.com/container-storage-interface/spec/blob/master/spec.md#createvolume) 中。
  在所有对 CSI 卷驱动程序的调用中，引用该 CSI 卷时都使用此值作为 `volume_id` 参数。

* `readOnly`：一个可选的布尔值，指示通过 `ControllerPublished` 关联该卷时是否设置该卷为只读。默认值是 false。
  该值通过 `ControllerPublishVolumeRequest` 中的 `readonly` 字段传递给 CSI 驱动。

* `fsType`：如果 PV 的 `VolumeMode` 为 `Filesystem`，那么此字段指定挂载卷时应该使用的文件系统。
  如果卷尚未格式化，并且支持格式化，此值将用于格式化卷。
  此值可以通过 `ControllerPublishVolumeRequest`、`NodeStageVolumeRequest` 和
  `NodePublishVolumeRequest` 的 `VolumeCapability` 字段传递给 CSI 驱动。

* `volumeAttributes`：一个字符串到字符串的映射表，用来设置卷的静态属性。
  该映射必须与 CSI 驱动程序返回的 `CreateVolumeResponse` 中的 `volume.attributes`
  字段的映射相对应；
  [CSI 规范](https://github.com/container-storage-interface/spec/blob/master/spec.md#createvolume)中有相应的定义。
  该映射通过`ControllerPublishVolumeRequest`、`NodeStageVolumeRequest`、和
  `NodePublishVolumeRequest` 中的 `volume_context` 字段传递给 CSI 驱动。

* `controllerPublishSecretRef`：对包含敏感信息的 Secret 对象的引用；
  该敏感信息会被传递给 CSI 驱动来完成 CSI `ControllerPublishVolume` 和
  `ControllerUnpublishVolume` 调用。
  此字段是可选的；在不需要 Secret 时可以是空的。
  如果 Secret 包含多个 Secret 条目，则所有的 Secret 条目都会被传递。

* `nodeExpandSecretRef`：对包含敏感信息的 Secret 对象的引用，
  该信息会传递给 CSI 驱动以完成 CSI `NodeExpandVolume` 调用。
  此字段是可选的，如果不需要 Secret，则可能是空的。
  如果 Secret 包含多个 Secret 条目，则传递所有 Secret 条目。
  当你为节点初始化的卷扩展配置 Secret 数据时，kubelet 会通过 `NodeExpandVolume()`
  调用将该数据传递给 CSI 驱动。为了使用 `nodeExpandSecretRef` 字段，
  你的集群应运行 Kubernetes 1.25 或更高版本，
  如果你所运行的 Kubernetes 是 1.25 或 1.26，你必须为每个 kube-apiserver
  和每个节点上的 kubelet 启用名为 `CSINodeExpandSecret`
  的[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)。
  在 Kubernetes 1.27 版本中，此特性已默认启用，无需显式启用特性门控。
  在节点初始化的存储大小调整操作期间，你还必须使用支持或需要 Secret 数据的 CSI 驱动。

* `nodePublishSecretRef`：对包含敏感信息的 Secret 对象的引用。
  该信息传递给 CSI 驱动来完成 CSI `NodePublishVolume` 调用。
  此字段是可选的，如果不需要 Secret，则可能是空的。
  如果 Secret 对象包含多个 Secret 条目，则传递所有 Secret 条目。

* `nodeStageSecretRef`：对包含敏感信息的 Secret 对象的引用，
  该信息会传递给 CSI 驱动以完成 CSI `NodeStageVolume` 调用。
  此字段是可选的，如果不需要 Secret，则可能是空的。
  如果 Secret 包含多个 Secret 条目，则传递所有 Secret 条目。

#### CSI 原始块卷支持    {#csi-raw-block-volume-support}

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

具有外部 CSI 驱动程序的供应商能够在 Kubernetes 工作负载中实现原始块卷支持。

你可以和以前一样，
安装自己的[带有原始块卷支持的 PV/PVC](/zh-cn/docs/concepts/storage/persistent-volumes/#raw-block-volume-support)，
采用 CSI 对此过程没有影响。

#### CSI 临时卷   {#csi-ephemeral-volumes}

{{< feature-state for_k8s_version="v1.25" state="stable" >}}

你可以直接在 Pod 规约中配置 CSI 卷。采用这种方式配置的卷都是临时卷，
无法在 Pod 重新启动后继续存在。
进一步的信息可参阅[临时卷](/zh-cn/docs/concepts/storage/ephemeral-volumes/#csi-ephemeral-volumes)。

有关如何开发 CSI 驱动的更多信息，请参考 [kubernetes-csi 文档](https://kubernetes-csi.github.io/docs/)。

#### Windows CSI 代理  {#windows-csi-proxy}

{{< feature-state for_k8s_version="v1.22" state="stable" >}}

CSI 节点插件需要执行多种特权操作，例如扫描磁盘设备和挂载文件系统等。
这些操作在每个宿主操作系统上都是不同的。对于 Linux 工作节点而言，容器化的 CSI
节点插件通常部署为特权容器。对于 Windows 工作节点而言，容器化 CSI
节点插件的特权操作是通过 [csi-proxy](https://github.com/kubernetes-csi/csi-proxy)
来支持的。csi-proxy 是一个由社区管理的、独立的可执行二进制文件，
需要被预安装到每个 Windows 节点上。

要了解更多的细节，可以参考你要部署的 CSI 插件的部署指南。

#### 从树内插件迁移到 CSI 驱动程序  {#migrating-to-csi-drivers-from-in-tree-plugins}

{{< feature-state for_k8s_version="v1.25" state="stable" >}}

`CSIMigration` 特性针对现有树内插件的操作会被定向到相应的 CSI 插件（应已安装和配置）。
因此，操作员在过渡到取代树内插件的 CSI 驱动时，无需对现有存储类、PV 或 PVC（指树内插件）进行任何配置更改。

所支持的操作和特性包括：配备（Provisioning）/删除、挂接（Attach）/解挂（Detach）、
挂载（Mount）/卸载（Unmount）和调整卷大小。

上面的[卷类型](#volume-types)节列出了支持 `CSIMigration` 并已实现相应 CSI
驱动程序的树内插件。

下面是支持 Windows 节点上持久性存储的树内插件：

* [`awsElasticBlockStore`](#awselasticblockstore)
* [`azureDisk`](#azuredisk)
* [`azureFile`](#azurefile)
* [`gcePersistentDisk`](#gcepersistentdisk)
* [`vsphereVolume`](#vspherevolume)

### flexVolume（已弃用）   {#flexvolume}

{{< feature-state for_k8s_version="v1.23" state="deprecated" >}}

FlexVolume 是一个使用基于 exec 的模型来与驱动程序对接的树外插件接口。
用户必须在每个节点上的预定义卷插件路径中安装 FlexVolume
驱动程序可执行文件，在某些情况下，控制平面节点中也要安装。

Pod 通过 `flexvolume` 树内插件与 FlexVolume 驱动程序交互。
更多详情请参考 FlexVolume
[README](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-storage/flexvolume.md#readme) 文档。

下面的 FlexVolume [插件](https://github.com/Microsoft/K8s-Storage-Plugins/tree/master/flexvolume/windows)
以 PowerShell 脚本的形式部署在宿主系统上，支持 Windows 节点：

* [SMB](https://github.com/microsoft/K8s-Storage-Plugins/tree/master/flexvolume/windows/plugins/microsoft.com~smb.cmd)
* [iSCSI](https://github.com/microsoft/K8s-Storage-Plugins/tree/master/flexvolume/windows/plugins/microsoft.com~iscsi.cmd)

{{< note >}}
FlexVolume 已被弃用。推荐使用树外 CSI 驱动来将外部存储整合进 Kubernetes。

FlexVolume 驱动的维护者应开发一个 CSI 驱动并帮助用户从 FlexVolume 驱动迁移到 CSI。
FlexVolume 用户应迁移工作负载以使用对等的 CSI 驱动。
{{< /note >}}

## 挂载卷的传播   {#mount-propagation}

挂载卷的传播能力允许将容器安装的卷共享到同一 Pod 中的其他容器，甚至共享到同一节点上的其他 Pod。

卷的挂载传播特性由 `Container.volumeMounts` 中的 `mountPropagation` 字段控制。
它的值包括：


* `None` - 此卷挂载将不会感知到主机后续在此卷或其任何子目录上执行的挂载变化。
   类似的，容器所创建的卷挂载在主机上是不可见的。这是默认模式。

   该模式等同于 [`mount(8)`](https://man7.org/linux/man-pages/man8/mount.8.html)中描述的
   `rprivate` 挂载传播选项。

   然而，当 `rprivate` 传播选项不适用时，CRI 运行时可以转为选择 `rslave` 挂载传播选项
   （即 `HostToContainer`）。当挂载源包含 Docker 守护进程的根目录（`/var/lib/docker`）时，
   cri-dockerd (Docker) 已知可以选择 `rslave` 挂载传播选项。
   。

* `HostToContainer` - 此卷挂载将会感知到主机后续针对此卷或其任何子目录的挂载操作。

  换句话说，如果主机在此挂载卷中挂载任何内容，容器将能看到它被挂载在那里。

  类似的，配置了 `Bidirectional` 挂载传播选项的 Pod 如果在同一卷上挂载了内容，挂载传播设置为
  `HostToContainer` 的容器都将能看到这一变化。

  该模式等同于 [`mount(8)`](https://man7.org/linux/man-pages/man8/mount.8.html)中描述的
  `rslave` 挂载传播选项。

* `Bidirectional` - 这种卷挂载和 `HostToContainer` 挂载表现相同。
  另外，容器创建的卷挂载将被传播回至主机和使用同一卷的所有 Pod 的所有容器。

  该模式等同于 [`mount(8)`](https://man7.org/linux/man-pages/man8/mount.8.html)中描述的
  `rshared` 挂载传播选项。

  {{< warning >}}
  `Bidirectional` 形式的挂载传播可能比较危险。
  它可以破坏主机操作系统，因此它只被允许在特权容器中使用。
  强烈建议你熟悉 Linux 内核行为。
  此外，由 Pod 中的容器创建的任何卷挂载必须在终止时由容器销毁（卸载）。
  {{< /warning >}}

### 配置  {#configuration}

在某些部署环境中，挂载传播正常工作前，必须在 Docker 中正确配置挂载共享（mount share），如下所示。

编辑你的 Docker `systemd` 服务文件，按下面的方法设置 `MountFlags`：

```shell
MountFlags=shared
```

或者，如果存在 `MountFlags=slave` 就删除掉。然后重启 Docker 守护进程：

```shell
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## {{% heading "whatsnext" %}}

参考[使用持久卷部署 WordPress 和 MySQL](/zh-cn/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/) 示例。
