---
title: 持久卷
feature:
  title: 存储编排
  description: >
    自动挂载所选存储系统，包括本地存储、诸如 <a href="https://aws.amazon.com/products/storage/">AWS</a>
    或 <a href="https://cloud.google.com/storage/">GCP</a>
    之类公有云提供商所提供的存储或者诸如 NFS、iSCSI、Ceph、Cinder 这类网络存储系统。
content_type: concept
weight: 20
---


本文描述 Kubernetes 中的**持久卷（Persistent Volume）** 。
建议先熟悉[卷（Volume）](/zh-cn/docs/concepts/storage/volumes/)的概念。


## 介绍  {#introduction}

存储的管理是一个与计算实例的管理完全不同的问题。
PersistentVolume 子系统为用户和管理员提供了一组 API，
将存储如何制备的细节从其如何被使用中抽象出来。
为了实现这点，我们引入了两个新的 API 资源：PersistentVolume 和
PersistentVolumeClaim。

**持久卷（PersistentVolume，PV）** 是集群中的一块存储，可以由管理员事先制备，
或者使用[存储类（Storage Class）](/zh-cn/docs/concepts/storage/storage-classes/)来动态制备。
持久卷是集群资源，就像节点也是集群资源一样。PV 持久卷和普通的 Volume 一样，
也是使用卷插件来实现的，只是它们拥有独立于任何使用 PV 的 Pod 的生命周期。
此 API 对象中记述了存储的实现细节，无论其背后是 NFS、iSCSI 还是特定于云平台的存储系统。

**持久卷申领（PersistentVolumeClaim，PVC）** 表达的是用户对存储的请求。概念上与 Pod 类似。
Pod 会耗用节点资源，而 PVC 申领会耗用 PV 资源。Pod 可以请求特定数量的资源（CPU
和内存）；同样 PVC 申领也可以请求特定的大小和访问模式
（例如，可以要求 PV 卷能够以 ReadWriteOnce、ReadOnlyMany 或 ReadWriteMany
模式之一来挂载，参见[访问模式](#access-modes)）。

尽管 PersistentVolumeClaim 允许用户消耗抽象的存储资源，
常见的情况是针对不同的问题用户需要的是具有不同属性（如，性能）的 PersistentVolume 卷。
集群管理员需要能够提供不同性质的 PersistentVolume，
并且这些 PV 卷之间的差别不仅限于卷大小和访问模式，同时又不能将卷是如何实现的这些细节暴露给用户。
为了满足这类需求，就有了**存储类（StorageClass）** 资源。

参见[基于运行示例的详细演练](/zh-cn/docs/tasks/configure-pod-container/configure-persistent-volume-storage/)。

## 卷和申领的生命周期   {#lifecycle-of-a-volume-and-claim}

PV 卷是集群中的资源。PVC 申领是对这些资源的请求，也被用来执行对资源的申领检查。
PV 卷和 PVC 申领之间的互动遵循如下生命周期：

### 制备   {#provisioning}

PV 卷的制备有两种方式：静态制备或动态制备。

#### 静态制备  {#static}

集群管理员创建若干 PV 卷。这些卷对象带有真实存储的细节信息，
并且对集群用户可用（可见）。PV 卷对象存在于 Kubernetes  API 中，可供用户消费（使用）。

#### 动态制备     {#dynamic}

如果管理员所创建的所有静态 PV 卷都无法与用户的 PersistentVolumeClaim 匹配，
集群可以尝试为该 PVC 申领动态制备一个存储卷。
这一制备操作是基于 StorageClass 来实现的：PVC 申领必须请求某个
[存储类](/zh-cn/docs/concepts/storage/storage-classes/)，
同时集群管理员必须已经创建并配置了该类，这样动态制备卷的动作才会发生。
如果 PVC 申领指定存储类为 `""`，则相当于为自身禁止使用动态制备的卷。

为了基于存储类完成动态的存储制备，集群管理员需要在 API 服务器上启用 `DefaultStorageClass`
[准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#defaultstorageclass)。
举例而言，可以通过保证 `DefaultStorageClass` 出现在 API 服务器组件的
`--enable-admission-plugins` 标志值中实现这点；该标志的值可以是逗号分隔的有序列表。
关于 API 服务器标志的更多信息，可以参考
[kube-apiserver](/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver/)
文档。

### 绑定     {#binding}

用户创建一个带有特定存储容量和特定访问模式需求的 PersistentVolumeClaim 对象；
在动态制备场景下，这个 PVC 对象可能已经创建完毕。
控制平面中的控制回路监测新的 PVC 对象，寻找与之匹配的 PV 卷（如果可能的话），
并将二者绑定到一起。
如果为了新的 PVC 申领动态制备了 PV 卷，则控制回路总是将该 PV 卷绑定到这一 PVC 申领。
否则，用户总是能够获得他们所请求的资源，只是所获得的 PV 卷可能会超出所请求的配置。
一旦绑定关系建立，则 PersistentVolumeClaim 绑定就是排他性的，
无论该 PVC 申领是如何与 PV 卷建立的绑定关系。
PVC 申领与 PV 卷之间的绑定是一种一对一的映射，实现上使用 ClaimRef 来记述
PV 卷与 PVC 申领间的双向绑定关系。

如果找不到匹配的 PV 卷，PVC 申领会无限期地处于未绑定状态。
当与之匹配的 PV 卷可用时，PVC 申领会被绑定。
例如，即使某集群上制备了很多 50 Gi 大小的 PV 卷，也无法与请求
100 Gi 大小的存储的 PVC 匹配。当新的 100 Gi PV 卷被加入到集群时，
该 PVC 才有可能被绑定。

### 使用    {#using}

Pod 将 PVC 申领当做存储卷来使用。集群会检视 PVC 申领，找到所绑定的卷，
并为 Pod 挂载该卷。对于支持多种访问模式的卷，
用户要在 Pod 中以卷的形式使用申领时指定期望的访问模式。

一旦用户有了申领对象并且该申领已经被绑定，
则所绑定的 PV 卷在用户仍然需要它期间一直属于该用户。
用户通过在 Pod 的 `volumes` 块中包含 `persistentVolumeClaim`
节区来调度 Pod，访问所申领的 PV 卷。
相关细节可参阅[使用申领作为卷](#claims-as-volumes)。

### 保护使用中的存储对象   {#storage-object-in-use-protection}

保护使用中的存储对象（Storage Object in Use Protection）
这一功能特性的目的是确保仍被 Pod 使用的 PersistentVolumeClaim（PVC）
对象及其所绑定的 PersistentVolume（PV）对象在系统中不会被删除，因为这样做可能会引起数据丢失。

{{< note >}}
当使用某 PVC 的 Pod 对象仍然存在时，认为该 PVC 仍被此 Pod 使用。
{{< /note >}}

如果用户删除被某 Pod 使用的 PVC 对象，该 PVC 申领不会被立即移除。
PVC 对象的移除会被推迟，直至其不再被任何 Pod 使用。
此外，如果管理员删除已绑定到某 PVC 申领的 PV 卷，该 PV 卷也不会被立即移除。
PV 对象的移除也要推迟到该 PV 不再绑定到 PVC。

你可以看到当 PVC 的状态为 `Terminating` 且其 `Finalizers` 列表中包含
`kubernetes.io/pvc-protection` 时，PVC 对象是处于被保护状态的。

```shell
kubectl describe pvc hostpath
```
```
Name:          hostpath
Namespace:     default
StorageClass:  example-hostpath
Status:        Terminating
Volume:
Labels:        <none>
Annotations:   volume.beta.kubernetes.io/storage-class=example-hostpath
               volume.beta.kubernetes.io/storage-provisioner=example.com/hostpath
Finalizers:    [kubernetes.io/pvc-protection]
...
```

你也可以看到当 PV 对象的状态为 `Terminating` 且其 `Finalizers` 列表中包含
`kubernetes.io/pv-protection` 时，PV 对象是处于被保护状态的。

```shell
kubectl describe pv task-pv-volume
```
```
Name:            task-pv-volume
Labels:          type=local
Annotations:     <none>
Finalizers:      [kubernetes.io/pv-protection]
StorageClass:    standard
Status:          Terminating
Claim:
Reclaim Policy:  Delete
Access Modes:    RWO
Capacity:        1Gi
Message:
Source:
    Type:          HostPath (bare host directory volume)
    Path:          /tmp/data
    HostPathType:
Events:            <none>
```

### 回收（Reclaiming）   {#reclaiming}

当用户不再使用其存储卷时，他们可以从 API 中将 PVC 对象删除，
从而允许该资源被回收再利用。PersistentVolume 对象的回收策略告诉集群，
当其被从申领中释放时如何处理该数据卷。
目前，数据卷可以被 Retained（保留）、Recycled（回收）或 Deleted（删除）。

#### 保留（Retain）    {#retain}

回收策略 `Retain` 使得用户可以手动回收资源。当 PersistentVolumeClaim
对象被删除时，PersistentVolume 卷仍然存在，对应的数据卷被视为"已释放（released）"。
由于卷上仍然存在这前一申领人的数据，该卷还不能用于其他申领。
管理员可以通过下面的步骤来手动回收该卷：

1. 删除 PersistentVolume 对象。与之相关的、位于外部基础设施中的存储资产
   （例如 AWS EBS、GCE PD、Azure Disk 或 Cinder 卷）在 PV 删除之后仍然存在。
1. 根据情况，手动清除所关联的存储资产上的数据。
1. 手动删除所关联的存储资产。

如果你希望重用该存储资产，可以基于存储资产的定义创建新的 PersistentVolume 卷对象。

#### 删除（Delete）    {#delete}

对于支持 `Delete` 回收策略的卷插件，删除动作会将 PersistentVolume 对象从
Kubernetes 中移除，同时也会从外部基础设施（如 AWS EBS、GCE PD、Azure Disk 或
Cinder 卷）中移除所关联的存储资产。
动态制备的卷会继承[其 StorageClass 中设置的回收策略](#reclaim-policy)，
该策略默认为 `Delete`。管理员需要根据用户的期望来配置 StorageClass；
否则 PV 卷被创建之后必须要被编辑或者修补。
参阅[更改 PV 卷的回收策略](/zh-cn/docs/tasks/administer-cluster/change-pv-reclaim-policy/)。

#### 回收（Recycle）     {#recycle}

{{< warning >}}
回收策略 `Recycle` 已被废弃。取而代之的建议方案是使用动态制备。
{{< /warning >}}

如果下层的卷插件支持，回收策略 `Recycle` 会在卷上执行一些基本的擦除
（`rm -rf /thevolume/*`）操作，之后允许该卷用于新的 PVC 申领。

不过，管理员可以按[参考资料](/zh-cn/docs/reference/command-line-tools-reference/kube-controller-manager/)中所述，
使用 Kubernetes 控制器管理器命令行参数来配置一个定制的回收器（Recycler）
Pod 模板。此定制的回收器 Pod 模板必须包含一个 `volumes` 规约，如下例所示：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pv-recycler
  namespace: default
spec:
  restartPolicy: Never
  volumes:
  - name: vol
    hostPath:
      path: /any/path/it/will/be/replaced
  containers:
  - name: pv-recycler
    image: "registry.k8s.io/busybox"
    command: ["/bin/sh", "-c", "test -e /scrub && rm -rf /scrub/..?* /scrub/.[!.]* /scrub/*  && test -z \"$(ls -A /scrub)\" || exit 1"]
    volumeMounts:
    - name: vol
      mountPath: /scrub
```

定制回收器 Pod 模板中在 `volumes` 部分所指定的特定路径要替换为正被回收的卷的路径。

### PersistentVolume 删除保护 finalizer  {#persistentvolume-deletion-protection-finalizer}

{{< feature-state for_k8s_version="v1.23" state="alpha" >}}

可以在 PersistentVolume 上添加终结器（Finalizer），
以确保只有在删除对应的存储后才删除具有 `Delete` 回收策略的 PersistentVolume。

新引入的 `kubernetes.io/pv-controller` 和 `external-provisioner.volume.kubernetes.io/finalizer`
终结器仅会被添加到动态制备的卷上。

终结器 `kubernetes.io/pv-controller` 会被添加到树内插件卷上。
下面是一个例子：

```shell
kubectl describe pv pvc-74a498d6-3929-47e8-8c02-078c1ece4d78
```
```none
Name:            pvc-74a498d6-3929-47e8-8c02-078c1ece4d78
Labels:          <none>
Annotations:     kubernetes.io/createdby: vsphere-volume-dynamic-provisioner
                 pv.kubernetes.io/bound-by-controller: yes
                 pv.kubernetes.io/provisioned-by: kubernetes.io/vsphere-volume
Finalizers:      [kubernetes.io/pv-protection kubernetes.io/pv-controller]
StorageClass:    vcp-sc
Status:          Bound
Claim:           default/vcp-pvc-1
Reclaim Policy:  Delete
Access Modes:    RWO
VolumeMode:      Filesystem
Capacity:        1Gi
Node Affinity:   <none>
Message:         
Source:
    Type:               vSphereVolume (a Persistent Disk resource in vSphere)
    VolumePath:         [vsanDatastore] d49c4a62-166f-ce12-c464-020077ba5d46/kubernetes-dynamic-pvc-74a498d6-3929-47e8-8c02-078c1ece4d78.vmdk
    FSType:             ext4
    StoragePolicyName:  vSAN Default Storage Policy
Events:                 <none>
```

终结器 `external-provisioner.volume.kubernetes.io/finalizer` 会被添加到 CSI 卷上。下面是一个例子：

```none
Name:            pvc-2f0bab97-85a8-4552-8044-eb8be45cf48d
Labels:          <none>
Annotations:     pv.kubernetes.io/provisioned-by: csi.vsphere.vmware.com
Finalizers:      [kubernetes.io/pv-protection external-provisioner.volume.kubernetes.io/finalizer]
StorageClass:    fast
Status:          Bound
Claim:           demo-app/nginx-logs
Reclaim Policy:  Delete
Access Modes:    RWO
VolumeMode:      Filesystem
Capacity:        200Mi
Node Affinity:   <none>
Message:         
Source:
    Type:              CSI (a Container Storage Interface (CSI) volume source)
    Driver:            csi.vsphere.vmware.com
    FSType:            ext4
    VolumeHandle:      44830fa8-79b4-406b-8b58-621ba25353fd
    ReadOnly:          false
    VolumeAttributes:      storage.kubernetes.io/csiProvisionerIdentity=1648442357185-8081-csi.vsphere.vmware.com
                           type=vSphere CNS Block Volume
Events:                <none>
```

当为特定的树内卷插件启用了 `CSIMigration{provider}` 特性标志时，`kubernetes.io/pv-controller`
终结器将被替换为 `external-provisioner.volume.kubernetes.io/finalizer` 终结器。

### 预留 PersistentVolume  {#reserving-a-persistentvolume}

控制平面可以在集群中[将 PersistentVolumeClaims 绑定到匹配的 PersistentVolumes](#binding)。
但是，如果你希望 PVC 绑定到特定 PV，则需要预先绑定它们。

通过在 PersistentVolumeClaim 中指定 PersistentVolume，你可以声明该特定
PV 与 PVC 之间的绑定关系。如果该 PersistentVolume 存在且未被通过其
`claimRef` 字段预留给 PersistentVolumeClaim，则该 PersistentVolume
会和该 PersistentVolumeClaim 绑定到一起。

绑定操作不会考虑某些卷匹配条件是否满足，包括节点亲和性等等。
控制面仍然会检查[存储类](/zh-cn/docs/concepts/storage/storage-classes/)、
访问模式和所请求的存储尺寸都是合法的。

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: foo-pvc
  namespace: foo
spec:
  storageClassName: "" # 此处须显式设置空字符串，否则会被设置为默认的 StorageClass
  volumeName: foo-pv
  ...
```

此方法无法对 PersistentVolume 的绑定特权做出任何形式的保证。
如果有其他 PersistentVolumeClaim 可以使用你所指定的 PV，
则你应该首先预留该存储卷。你可以将 PV 的 `claimRef` 字段设置为相关的
PersistentVolumeClaim 以确保其他 PVC 不会绑定到该 PV 卷。

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: foo-pv
spec:
  storageClassName: ""
  claimRef:
    name: foo-pvc
    namespace: foo
  ...
```

如果你想要使用 `claimPolicy` 属性设置为 `Retain` 的 PersistentVolume 卷时，
包括你希望复用现有的 PV 卷时，这点是很有用的

### 扩充 PVC 申领   {#expanding-persistent-volumes-claims}

{{< feature-state for_k8s_version="v1.24" state="stable" >}}

现在，对扩充 PVC 申领的支持默认处于被启用状态。你可以扩充以下类型的卷：

* azureDisk
* azureFile
* awsElasticBlockStore
* cinder （已弃用）
* {{< glossary_tooltip text="csi" term_id="csi" >}}
* flexVolume （已弃用）
* gcePersistentDisk
* rbd
* portworxVolume

只有当 PVC 的存储类中将 `allowVolumeExpansion` 设置为 true 时，你才可以扩充该 PVC 申领。

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: example-vol-default
provisioner: vendor-name.example/magicstorage
parameters:
  resturl: "http://192.168.10.100:8080"
  restuser: ""
  secretNamespace: ""
  secretName: ""
allowVolumeExpansion: true
```

如果要为某 PVC 请求较大的存储卷，可以编辑 PVC 对象，设置一个更大的尺寸值。
这一编辑操作会触发为下层 PersistentVolume 提供存储的卷的扩充。
Kubernetes 不会创建新的 PV 卷来满足此申领的请求。
与之相反，现有的卷会被调整大小。

{{< warning >}}
直接编辑 PersistentVolume 的大小可以阻止该卷自动调整大小。
如果对 PersistentVolume 的容量进行编辑，然后又将其所对应的
PersistentVolumeClaim 的 `.spec` 进行编辑，使该 PersistentVolumeClaim
的大小匹配 PersistentVolume 的话，则不会发生存储大小的调整。
Kubernetes 控制平面将看到两个资源的所需状态匹配，
并认为其后备卷的大小已被手动增加，无需调整。
{{< /warning >}}

#### CSI 卷的扩充     {#csi-volume-expansion}

{{< feature-state for_k8s_version="v1.24" state="stable" >}}

对 CSI 卷的扩充能力默认是被启用的，不过扩充 CSI 卷要求 CSI
驱动支持卷扩充操作。可参阅特定 CSI 驱动的文档了解更多信息。

#### 重设包含文件系统的卷的大小 {#resizing-a-volume-containing-a-file-system}

只有卷中包含的文件系统是 XFS、Ext3 或者 Ext4 时，你才可以重设卷的大小。

当卷中包含文件系统时，只有在 Pod 使用 `ReadWrite` 模式来使用 PVC
申领的情况下才能重设其文件系统的大小。文件系统扩充的操作或者是在 Pod
启动期间完成，或者在下层文件系统支持在线扩充的前提下在 Pod 运行期间完成。

如果 FlexVolumes 的驱动将 `RequiresFSResize` 能力设置为 `true`，
则该 FlexVolume 卷（于 Kubernetes v1.23 弃用）可以在 Pod 重启期间调整大小。

#### 重设使用中 PVC 申领的大小    {#resizing-an-in-use-persistentvolumevlaim}

{{< feature-state for_k8s_version="v1.24" state="stable" >}}

在这种情况下，你不需要删除和重建正在使用某现有 PVC 的 Pod 或 Deployment。
所有使用中的 PVC 在其文件系统被扩充之后，立即可供其 Pod 使用。
此功能特性对于没有被 Pod 或 Deployment 使用的 PVC 而言没有效果。
你必须在执行扩展操作之前创建一个使用该 PVC 的 Pod。

与其他卷类型类似，FlexVolume 卷也可以在被 Pod 使用期间执行扩充操作。

{{< note >}}
FlexVolume 卷的重设大小只能在下层驱动支持重设大小的时候才可进行。
{{< /note >}}

{{< note >}}
扩充 EBS 卷的操作非常耗时。同时还存在另一个配额限制：
每 6 小时只能执行一次（尺寸）修改操作。
{{< /note >}}

#### 处理扩充卷过程中的失败      {#recovering-from-failure-when-expanding-volumes}

如果用户指定的新大小过大，底层存储系统无法满足，PVC 的扩展将不断重试，
直到用户或集群管理员采取一些措施。这种情况是不希望发生的，因此 Kubernetes
提供了以下从此类故障中恢复的方法。

{{< tabs name="recovery_methods" >}}
{{% tab name="集群管理员手动处理" %}}

如果扩充下层存储的操作失败，集群管理员可以手动地恢复 PVC
申领的状态并取消重设大小的请求。否则，在没有管理员干预的情况下，
控制器会反复重试重设大小的操作。

1. 将绑定到 PVC 申领的 PV 卷标记为 `Retain` 回收策略。
2. 删除 PVC 对象。由于 PV 的回收策略为 `Retain`，我们不会在重建 PVC 时丢失数据。
3. 删除 PV 规约中的 `claimRef` 项，这样新的 PVC 可以绑定到该卷。
   这一操作会使得 PV 卷变为 "可用（Available）"。
4. 使用小于 PV 卷大小的尺寸重建 PVC，设置 PVC 的 `volumeName` 字段为 PV 卷的名称。
   这一操作将把新的 PVC 对象绑定到现有的 PV 卷。
5. 不要忘记恢复 PV 卷上设置的回收策略。

{{% /tab %}}
{{% tab name="通过请求扩展为更小尺寸" %}}
{{% feature-state for_k8s_version="v1.23" state="alpha" %}}

{{< note >}}
Kubernetes 从 1.23 版本开始将允许用户恢复失败的 PVC 扩展这一能力作为
alpha 特性支持。`RecoverVolumeExpansionFailure` 必须被启用以允许使用此特性。
可参考[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
文档了解更多信息。
{{< /note >}}

如果集群中的特性门控 `RecoverVolumeExpansionFailure`
已启用，在 PVC 的扩展发生失败时，你可以使用比先前请求的值更小的尺寸来重试扩展。
要使用一个更小的尺寸尝试请求新的扩展，请编辑该 PVC 的 `.spec.resources`
并选择一个比你之前所尝试的值更小的值。
如果由于容量限制而无法成功扩展至更高的值，这将很有用。
如果发生了这种情况，或者你怀疑可能发生了这种情况，
你可以通过指定一个在底层存储制备容量限制内的尺寸来重试扩展。
你可以通过查看 `.status.resizeStatus` 以及 PVC 上的事件来监控调整大小操作的状态。

请注意，
尽管你可以指定比之前的请求更低的存储量，新值必须仍然高于 `.status.capacity`。
Kubernetes 不支持将 PVC 缩小到小于其当前的尺寸。

{{% /tab %}}
{{% /tabs %}}


## 持久卷的类型     {#types-of-persistent-volumes}

PV 持久卷是用插件的形式来实现的。Kubernetes 目前支持以下插件：

* [`cephfs`](/zh-cn/docs/concepts/storage/volumes/#cephfs) - CephFS volume
* [`csi`](/zh-cn/docs/concepts/storage/volumes/#csi) - 容器存储接口 (CSI)
* [`fc`](/zh-cn/docs/concepts/storage/volumes/#fc) - Fibre Channel (FC) 存储
* [`hostPath`](/zh-cn/docs/concepts/storage/volumes/#hostpath) - HostPath 卷
  （仅供单节点测试使用；不适用于多节点集群；请尝试使用 `local` 卷作为替代）
* [`iscsi`](/zh-cn/docs/concepts/storage/volumes/#iscsi) - iSCSI (SCSI over IP) 存储
* [`local`](/zh-cn/docs/concepts/storage/volumes/#local) - 节点上挂载的本地存储设备
* [`nfs`](/zh-cn/docs/concepts/storage/volumes/#nfs) - 网络文件系统 (NFS) 存储
* [`rbd`](/zh-cn/docs/concepts/storage/volumes/#rbd) - Rados 块设备 (RBD) 卷

以下的持久卷已被弃用。这意味着当前仍是支持的，但是 Kubernetes 将来的发行版会将其移除。

* [`awsElasticBlockStore`](/zh-cn/docs/concepts/storage/volumes/#awselasticblockstore) - AWS 弹性块存储（EBS）
  （于 v1.17 **弃用**）
* [`azureDisk`](/zh-cn/docs/concepts/storage/volumes/#azuredisk) - Azure Disk
  （于 v1.19 **弃用**）
* [`azureFile`](/zh-cn/docs/concepts/storage/volumes/#azurefile) - Azure File
  （于 v1.21 **弃用**）
* [`cinder`](/zh-cn/docs/concepts/storage/volumes/#cinder) - Cinder（OpenStack 块存储）（于 v1.18 **弃用**）
* [`flexVolume`](/zh-cn/docs/concepts/storage/volumes/#flexVolume) - FlexVolume （于 v1.23 **弃用**）
* [`gcePersistentDisk`](/zh-cn/docs/concepts/storage/volumes/#gcepersistentdisk) - GCE Persistent Disk
  （于 v1.17 **弃用**）
* [`portworxVolume`](/zh-cn/docs/concepts/storage/volumes/#portworxvolume) - Portworx 卷
  （于 v1.25 **弃用**）
* [`vsphereVolume`](/zh-cn/docs/concepts/storage/volumes/#vspherevolume) - vSphere VMDK 卷
  （于 v1.19 **弃用**）


旧版本的 Kubernetes 仍支持这些“树内（In-Tree）”持久卷类型：

* `photonPersistentDisk` - Photon 控制器持久化盘。（从 v1.15 版本开始将**不可用**）
* [`scaleIO`](/zh-cn/docs/concepts/storage/volumes/#scaleio) - ScaleIO 卷（v1.21 之后**不可用**）
* [`flocker`](/zh-cn/docs/concepts/storage/volumes/#flocker) - Flocker 存储
  （v1.25 之后**不可用**）
* [`quobyte`](/zh-cn/docs/concepts/storage/volumes/#quobyte) - Quobyte 卷
  （v1.25 之后**不可用**）
* [`storageos`](/zh-cn/docs/concepts/storage/volumes/#storageos) - StorageOS 卷
  （v1.25 之后**不可用**）

## 持久卷    {#persistent-volumes}

每个 PV 对象都包含 `spec` 部分和 `status` 部分，分别对应卷的规约和状态。
PersistentVolume 对象的名称必须是合法的
[DNS 子域名](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv0003
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: slow
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: /tmp
    server: 172.17.0.2
```

{{< note >}}
在集群中使用持久卷存储通常需要一些特定于具体卷类型的辅助程序。
在这个例子中，PersistentVolume 是 NFS 类型的，因此需要辅助程序 `/sbin/mount.nfs`
来支持挂载 NFS 文件系统。
{{< /note >}}

### 容量    {#capacity}

一般而言，每个 PV 卷都有确定的存储容量。
容量属性是使用 PV 对象的 `capacity` 属性来设置的。
参考词汇表中的[量纲（Quantity）](/zh-cn/docs/reference/glossary/?all=true#term-quantity)
词条，了解 `capacity` 字段可以接受的单位。

目前，存储大小是可以设置和请求的唯一资源。
未来可能会包含 IOPS、吞吐量等属性。

### 卷模式     {#volume-mode}

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

针对 PV 持久卷，Kubernetes
支持两种卷模式（`volumeModes`）：`Filesystem（文件系统）` 和 `Block（块）`。
`volumeMode` 是一个可选的 API 参数。
如果该参数被省略，默认的卷模式是 `Filesystem`。

`volumeMode` 属性设置为 `Filesystem` 的卷会被 Pod **挂载（Mount）** 到某个目录。
如果卷的存储来自某块设备而该设备目前为空，Kuberneretes 会在第一次挂载卷之前在设备上创建文件系统。

你可以将 `volumeMode` 设置为 `Block`，以便将卷作为原始块设备来使用。
这类卷以块设备的方式交给 Pod 使用，其上没有任何文件系统。
这种模式对于为 Pod 提供一种使用最快可能方式来访问卷而言很有帮助，
Pod 和卷之间不存在文件系统层。另外，Pod 中运行的应用必须知道如何处理原始块设备。
关于如何在 Pod 中使用 `volumeMode: Block` 的卷，
可参阅[原始块卷支持](#raw-block-volume-support)。

### 访问模式   {#access-modes}

PersistentVolume 卷可以用资源提供者所支持的任何方式挂载到宿主系统上。
如下表所示，提供者（驱动）的能力不同，每个 PV 卷的访问模式都会设置为对应卷所支持的模式值。
例如，NFS 可以支持多个读写客户，但是某个特定的 NFS PV 卷可能在服务器上以只读的方式导出。
每个 PV 卷都会获得自身的访问模式集合，描述的是特定 PV 卷的能力。

访问模式有：

`ReadWriteOnce`
: 卷可以被一个节点以读写方式挂载。
  ReadWriteOnce 访问模式也允许运行在同一节点上的多个 Pod 访问卷。

`ReadOnlyMany`
: 卷可以被多个节点以只读方式挂载。

`ReadWriteMany`
: 卷可以被多个节点以读写方式挂载。

`ReadWriteOncePod`
: {{< feature-state for_k8s_version="v1.27" state="beta" >}}
  卷可以被单个 Pod 以读写方式挂载。
  如果你想确保整个集群中只有一个 Pod 可以读取或写入该 PVC，
  请使用 ReadWriteOncePod 访问模式。这只支持 CSI 卷以及需要 Kubernetes 1.22 以上版本。

这篇博客文章 [Introducing Single Pod Access Mode for PersistentVolumes](/blog/2021/09/13/read-write-once-pod-access-mode-alpha/)
描述了更详细的内容。

在命令行接口（CLI）中，访问模式也使用以下缩写形式：

* RWO - ReadWriteOnce
* ROX - ReadOnlyMany
* RWX - ReadWriteMany
* RWOP - ReadWriteOncePod

{{< note >}}
Kubernetes 使用卷访问模式来匹配 PersistentVolumeClaim 和 PersistentVolume。
在某些场合下，卷访问模式也会限制 PersistentVolume 可以挂载的位置。
卷访问模式并**不会**在存储已经被挂载的情况下为其实施写保护。
即使访问模式设置为 ReadWriteOnce、ReadOnlyMany 或 ReadWriteMany，它们也不会对卷形成限制。
例如，即使某个卷创建时设置为 ReadOnlyMany，也无法保证该卷是只读的。
如果访问模式设置为 ReadWriteOncePod，则卷会被限制起来并且只能挂载到一个 Pod 上。
{{< /note >}}

> **重要提醒！** 每个卷同一时刻只能以一种访问模式挂载，即使该卷能够支持多种访问模式。
> 例如，一个 GCEPersistentDisk 卷可以被某节点以 ReadWriteOnce
> 模式挂载，或者被多个节点以 ReadOnlyMany 模式挂载，但不可以同时以两种模式挂载。


| 卷插件               | ReadWriteOnce          | ReadOnlyMany          | ReadWriteMany | ReadWriteOncePod       |
| :---                 | :---:                  | :---:                 | :---:         | -                      |
| AWSElasticBlockStore | &#x2713;               | -                     | -             | -                      |
| AzureFile            | &#x2713;               | &#x2713;              | &#x2713;      | -                      |
| AzureDisk            | &#x2713;               | -                     | -             | -                      |
| CephFS               | &#x2713;               | &#x2713;              | &#x2713;      | -                      |
| Cinder               | &#x2713;               | -                     | ([如果多次挂接卷可用](https://github.com/kubernetes/cloud-provider-openstack/blob/master/docs/cinder-csi-plugin/features.md#multi-attach-volumes))            | -                      |
| CSI                  | 取决于驱动              | 取决于驱动            | 取决于驱动      | 取决于驱动    |
| FC                   | &#x2713;               | &#x2713;              | -             | -                      |
| FlexVolume           | &#x2713;               | &#x2713;              | 取决于驱动   | -              |
| GCEPersistentDisk    | &#x2713;               | &#x2713;              | -             | -                      |
| Glusterfs            | &#x2713;               | &#x2713;              | &#x2713;      | -                      |
| HostPath             | &#x2713;               | -                     | -             | -                      |
| iSCSI                | &#x2713;               | &#x2713;              | -             | -                      |
| NFS                  | &#x2713;               | &#x2713;              | &#x2713;      | -                      |
| RBD                  | &#x2713;               | &#x2713;              | -             | -                      |
| VsphereVolume        | &#x2713;               | -                     | -（Pod 运行于同一节点上时可行） | - |
| PortworxVolume       | &#x2713;               | -                     | &#x2713;      | -                  | - |

### 类    {#class}

每个 PV 可以属于某个类（Class），通过将其 `storageClassName` 属性设置为某个
[StorageClass](/zh-cn/docs/concepts/storage/storage-classes/) 的名称来指定。
特定类的 PV 卷只能绑定到请求该类存储卷的 PVC 申领。
未设置 `storageClassName` 的 PV 卷没有类设定，只能绑定到那些没有指定特定存储类的 PVC 申领。

早前，Kubernetes 使用注解 `volume.beta.kubernetes.io/storage-class` 而不是
`storageClassName` 属性。这一注解目前仍然起作用，不过在将来的 Kubernetes
发布版本中该注解会被彻底废弃。

### 回收策略   {#reclaim-policy}

目前的回收策略有：

* Retain -- 手动回收
* Recycle -- 基本擦除 (`rm -rf /thevolume/*`)
* Delete -- 诸如 AWS EBS、GCE PD、Azure Disk 或 OpenStack Cinder 卷这类关联存储资产也被删除

目前，仅 NFS 和 HostPath 支持回收（Recycle）。
AWS EBS、GCE PD、Azure Disk 和 Cinder 卷都支持删除（Delete）。

### 挂载选项    {#mount-options}

Kubernetes 管理员可以指定持久卷被挂载到节点上时使用的附加挂载选项。

{{< note >}}
并非所有持久卷类型都支持挂载选项。
{{< /note >}}

以下卷类型支持挂载选项：

* `awsElasticBlockStore`
* `azureDisk`
* `azureFile`
* `cephfs`
* `cinder`（于 v1.18 **弃用**）
* `gcePersistentDisk`
* `iscsi`
* `nfs`
* `rbd`
* `vsphereVolume`

Kubernetes 不对挂载选项执行合法性检查。如果挂载选项是非法的，挂载就会失败。

早前，Kubernetes 使用注解 `volume.beta.kubernetes.io/mount-options` 而不是
`mountOptions` 属性。这一注解目前仍然起作用，不过在将来的 Kubernetes
发布版本中该注解会被彻底废弃。

### 节点亲和性   {#node-affinity}

{{< note >}}
对大多数类型的卷而言，你不需要设置节点亲和性字段。
[AWS EBS](/zh-cn/docs/concepts/storage/volumes/#awselasticblockstore)、
[GCE PD](/zh-cn/docs/concepts/storage/volumes/#gcepersistentdisk) 和
[Azure Disk](/zh-cn/docs/concepts/storage/volumes/#azuredisk) 卷类型都能自动设置相关字段。
你需要为 [local](/zh-cn/docs/concepts/storage/volumes/#local) 卷显式地设置此属性。
{{< /note >}}

每个 PV 卷可以通过设置节点亲和性来定义一些约束，进而限制从哪些节点上可以访问此卷。
使用这些卷的 Pod 只会被调度到节点亲和性规则所选择的节点上执行。
要设置节点亲和性，配置 PV 卷 `.spec` 中的 `nodeAffinity`。
[持久卷](/zh-cn/docs/reference/kubernetes-api/config-and-storage-resources/persistent-volume-v1/#PersistentVolumeSpec)
API 参考关于该字段的更多细节。

### 阶段   {#phase}

每个卷会处于以下阶段（Phase）之一：

* Available（可用）-- 卷是一个空闲资源，尚未绑定到任何申领；
* Bound（已绑定）-- 该卷已经绑定到某申领；
* Released（已释放）-- 所绑定的申领已被删除，但是资源尚未被集群回收；
* Failed（失败）-- 卷的自动回收操作失败。

命令行接口能够显示绑定到某 PV 卷的 PVC 对象。

## PersistentVolumeClaims

每个 PVC 对象都有 `spec` 和 `status` 部分，分别对应申领的规约和状态。
PersistentVolumeClaim 对象的名称必须是合法的
[DNS 子域名](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 8Gi
  storageClassName: slow
  selector:
    matchLabels:
      release: "stable"
    matchExpressions:
      - {key: environment, operator: In, values: [dev]}
```

### 访问模式 {#access-modes}

申领在请求具有特定访问模式的存储时，使用与卷相同的[访问模式约定](#access-modes)。

### 卷模式 {#volume-modes}

申领使用[与卷相同的约定](#volume-mode)来表明是将卷作为文件系统还是块设备来使用。

### 资源    {#resources}

申领和 Pod 一样，也可以请求特定数量的资源。在这个上下文中，请求的资源是存储。
卷和申领都使用相同的
[资源模型](https://git.k8s.io/design-proposals-archive/scheduling/resources.md)。

### 选择算符    {#selector}

申领可以设置[标签选择算符](/zh-cn/docs/concepts/overview/working-with-objects/labels/#label-selectors)
来进一步过滤卷集合。只有标签与选择算符相匹配的卷能够绑定到申领上。
选择算符包含两个字段：

* `matchLabels` - 卷必须包含带有此值的标签
* `matchExpressions` - 通过设定键（key）、值列表和操作符（operator）
  来构造的需求。合法的操作符有 In、NotIn、Exists 和 DoesNotExist。

来自 `matchLabels` 和 `matchExpressions` 的所有需求都按逻辑与的方式组合在一起。
这些需求都必须被满足才被视为匹配。

### 类      {#class}

申领可以通过为 `storageClassName` 属性设置
[StorageClass](/zh-cn/docs/concepts/storage/storage-classes/) 的名称来请求特定的存储类。
只有所请求的类的 PV 卷，即 `storageClassName` 值与 PVC 设置相同的 PV 卷，
才能绑定到 PVC 申领。

PVC 申领不必一定要请求某个类。如果 PVC 的 `storageClassName` 属性值设置为 `""`，
则被视为要请求的是没有设置存储类的 PV 卷，因此这一 PVC 申领只能绑定到未设置存储类的
PV 卷（未设置注解或者注解值为 `""` 的 PersistentVolume（PV）对象在系统中不会被删除，
因为这样做可能会引起数据丢失。未设置 `storageClassName` 的 PVC 与此大不相同，
也会被集群作不同处理。具体筛查方式取决于
[`DefaultStorageClass` 准入控制器插件](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#defaultstorageclass)
是否被启用。

* 如果准入控制器插件被启用，则管理员可以设置一个默认的 StorageClass。
  所有未设置 `storageClassName` 的 PVC 都只能绑定到隶属于默认存储类的 PV 卷。
  设置默认 StorageClass 的工作是通过将对应 StorageClass 对象的注解
  `storageclass.kubernetes.io/is-default-class` 赋值为 `true` 来完成的。
  如果管理员未设置默认存储类，集群对 PVC 创建的处理方式与未启用准入控制器插件时相同。
  如果设定的默认存储类不止一个，准入控制插件会禁止所有创建 PVC 操作。
* 如果准入控制器插件被关闭，则不存在默认 StorageClass 的说法。
  所有将 `storageClassName` 设为 `""` 的 PVC 只能被绑定到也将 `storageClassName` 设为 `""` 的 PV。
  不过，只要默认的 StorageClass 可用，就可以稍后更新缺少 `storageClassName` 的 PVC。
  如果这个 PVC 更新了，它将不再绑定到也将 `storageClassName` 设为 `""` 的 PV。

参阅[可追溯的默认 StorageClass 赋值](#retroactive-default-storageclass-assignment)了解更多详细信息。

取决于安装方法，默认的 StorageClass 可能在集群安装期间由插件管理器（Addon
Manager）部署到集群中。

当某 PVC 除了请求 StorageClass 之外还设置了 `selector`，则这两种需求会按逻辑与关系处理：
只有隶属于所请求类且带有所请求标签的 PV 才能绑定到 PVC。

{{< note >}}
目前，设置了非空 `selector` 的 PVC 对象无法让集群为其动态制备 PV 卷。
{{< /note >}}

早前，Kubernetes 使用注解 `volume.beta.kubernetes.io/storage-class` 而不是
`storageClassName` 属性。这一注解目前仍然起作用，不过在将来的 Kubernetes
发布版本中该注解会被彻底废弃。

#### 可追溯的默认 StorageClass 赋值 {#retroactive-default-storageclass-assignment}

{{< feature-state for_k8s_version="v1.26" state="beta" >}}

你可以创建 PersistentVolumeClaim，而无需为新 PVC 指定 `storageClassName`。
即使你的集群中不存在默认 StorageClass，你也可以这样做。
在这种情况下，新的 PVC 会按照你的定义进行创建，并且在默认值可用之前，该 PVC 的 `storageClassName` 保持不设置。

当一个默认的 StorageClass 变得可用时，控制平面会识别所有未设置 `storageClassName` 的现有 PVC。
对于 `storageClassName` 为空值或没有此主键的 PVC，
控制平面会更新这些 PVC 以设置其 `storageClassName` 与新的默认 StorageClass 匹配。
如果你有一个现有的 PVC，其中 `storageClassName` 是 `""`，
并且你配置了默认 StorageClass，则此 PVC 将不会得到更新。

为了保持绑定到 `storageClassName` 设为 `""` 的 PV（当存在默认 StorageClass 时），
你需要将关联 PVC 的 `storageClassName` 设置为 `""`。

此行为可帮助管理员更改默认 StorageClass，方法是先移除旧的 PVC，然后再创建或设置另一个 PVC。
这一时间窗口内因为没有指定默认值，会导致所创建的未设置 `storageClassName` 的 PVC 也没有默认值设置，
但由于默认 StorageClass 赋值是可追溯的，这种更改默认值的方式是安全的。

## 使用申领作为卷     {#claims-as-volumes}

Pod 将申领作为卷来使用，并藉此访问存储资源。
申领必须位于使用它的 Pod 所在的同一名字空间内。
集群在 Pod 的名字空间中查找申领，并使用它来获得申领所使用的 PV 卷。
之后，卷会被挂载到宿主上并挂载到 Pod 中。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: nginx
      volumeMounts:
      - mountPath: "/var/www/html"
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: myclaim
```

### 关于名字空间的说明    {#a-note-on-namespaces}

PersistentVolume 卷的绑定是排他性的。
由于 PersistentVolumeClaim 是名字空间作用域的对象，使用
"Many" 模式（`ROX`、`RWX`）来挂载申领的操作只能在同一名字空间内进行。

### 类型为 `hostpath` 的 PersistentVolume  {#persistentvolumes-typed-hostpath}

`hostPath` PersistentVolume 使用节点上的文件或目录来模拟网络附加（network-attached）存储。
相关细节可参阅 [`hostPath` 卷示例](/zh-cn/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolume)。

## 原始块卷支持   {#raw-block-volume-support}

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

以下卷插件支持原始块卷，包括其动态制备（如果支持的话）的卷：

* AWSElasticBlockStore
* AzureDisk
* CSI
* FC（光纤通道）
* GCEPersistentDisk
* iSCSI
* Local 卷
* OpenStack Cinder
* RBD（Ceph 块设备）
* VsphereVolume

### 使用原始块卷的持久卷      {#persistent-volume-using-a-raw-block-volume}

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: block-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  volumeMode: Block
  persistentVolumeReclaimPolicy: Retain
  fc:
    targetWWNs: ["50060e801049cfd1"]
    lun: 0
    readOnly: false
```

### 申请原始块卷的 PVC 申领      {#persistent-volume-claim-requesting-a-raw-block-volume}

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: block-pvc
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Block
  resources:
    requests:
      storage: 10Gi
```
### 在容器中添加原始块设备路径的 Pod 规约  {#pod-spec-adding-raw-block-device-path-in-container}

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-block-volume
spec:
  containers:
    - name: fc-container
      image: fedora:26
      command: ["/bin/sh", "-c"]
      args: [ "tail -f /dev/null" ]
      volumeDevices:
        - name: data
          devicePath: /dev/xvda
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: block-pvc
```

{{< note >}}
向 Pod 中添加原始块设备时，你要在容器内设置设备路径而不是挂载路径。
{{< /note >}}

### 绑定块卷     {#binding-block-volumes}

如果用户通过 PersistentVolumeClaim 规约的 `volumeMode` 字段来表明对原始块设备的请求，
绑定规则与之前版本中未在规约中考虑此模式的实现略有不同。
下面列举的表格是用户和管理员可以为请求原始块设备所作设置的组合。
此表格表明在不同的组合下卷是否会被绑定。

静态制备卷的卷绑定矩阵：

| PV volumeMode | PVC volumeMode  | Result           |
| --------------|:---------------:| ----------------:|
|   未指定      | 未指定          | 绑定             |
|   未指定      | Block           | 不绑定           |
|   未指定      | Filesystem      | 绑定             |
|   Block       | 未指定          | 不绑定           |
|   Block       | Block           | 绑定             |
|   Block       | Filesystem      | 不绑定           |
|   Filesystem  | Filesystem      | 绑定             |
|   Filesystem  | Block           | 不绑定           |
|   Filesystem  | 未指定          | 绑定             |

{{< note >}}
Alpha 发行版本中仅支持静态制备的卷。
管理员需要在处理原始块设备时小心处理这些值。
{{< /note >}}

## 对卷快照及从卷快照中恢复卷的支持 {#volume-snapshot-and-restore-volume-from-snapshot-support}

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

卷快照（Volume Snapshot）仅支持树外 CSI 卷插件。
有关细节可参阅[卷快照](/zh-cn/docs/concepts/storage/volume-snapshots/)文档。
树内卷插件被弃用。你可以查阅[卷插件 FAQ](https://git.k8s.io/community/sig-storage/volume-plugin-faq.md)
了解已弃用的卷插件。

### 基于卷快照创建 PVC 申领     {#create-persistent-volume-claim-from-volume-snapshot}

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: restore-pvc
spec:
  storageClassName: csi-hostpath-sc
  dataSource:
    name: new-snapshot-test
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

## 卷克隆     {#volume-cloning}

[卷克隆](/zh-cn/docs/concepts/storage/volume-pvc-datasource/)功能特性仅适用于 CSI 卷插件。

### 基于现有 PVC 创建新的 PVC 申领    {#create-persistent-volume-claim-from-an-existing-pvc}

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cloned-pvc
spec:
  storageClassName: my-csi-plugin
  dataSource:
    name: existing-src-pvc-name
    kind: PersistentVolumeClaim
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

## 卷填充器（Populator）与数据源      {#volume-populators-and-data-sources}

{{< feature-state for_k8s_version="v1.24" state="beta" >}}

Kubernetes 支持自定义的卷填充器。要使用自定义的卷填充器，你必须为
kube-apiserver 和 kube-controller-manager 启用 `AnyVolumeDataSource`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)。

卷填充器利用了 PVC 规约字段 `dataSourceRef`。
不像 `dataSource` 字段只能包含对另一个持久卷申领或卷快照的引用，
`dataSourceRef` 字段可以包含对同一命名空间中任何对象的引用（不包含除 PVC 以外的核心资源）。
对于启用了特性门控的集群，使用 `dataSourceRef` 比 `dataSource` 更好。

## 跨名字空间数据源   {#cross-namespace-data-sources}

{{< feature-state for_k8s_version="v1.26" state="alpha" >}}

Kubernetes 支持跨名字空间卷数据源。
要使用跨名字空间卷数据源，你必须为 kube-apiserver、kube-controller 管理器启用
`AnyVolumeDataSource` 和 `CrossNamespaceVolumeDataSource`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)。
此外，你必须为 csi-provisioner 启用 `CrossNamespaceVolumeDataSource` 特性门控。

启用 `CrossNamespaceVolumeDataSource` 特性门控允许你在 dataSourceRef 字段中指定名字空间。

{{< note >}}
当你为卷数据源指定名字空间时，Kubernetes 在接受此引用之前在另一个名字空间中检查 ReferenceGrant。
ReferenceGrant 是 `gateway.networking.k8s.io` 扩展 API 的一部分。更多细节请参见 Gateway API 文档中的
[ReferenceGrant](https://gateway-api.sigs.k8s.io/api-types/referencegrant/)。
这意味着你必须在使用此机制之前至少使用 Gateway API 的 ReferenceGrant 来扩展 Kubernetes 集群。
{{< /note >}}

## 数据源引用   {#data-source-references}

`dataSourceRef` 字段的行为与 `dataSource` 字段几乎相同。
如果其中一个字段被指定而另一个字段没有被指定，API 服务器将给两个字段相同的值。
这两个字段都不能在创建后改变，如果试图为这两个字段指定不同的值，将导致验证错误。
因此，这两个字段将总是有相同的内容。

在 `dataSourceRef` 字段和 `dataSource` 字段之间有两个用户应该注意的区别：

* `dataSource` 字段会忽略无效的值（如同是空值），
   而 `dataSourceRef` 字段永远不会忽略值，并且若填入一个无效的值，会导致错误。
   无效值指的是 PVC 之外的核心对象（没有 apiGroup 的对象）。
* `dataSourceRef` 字段可以包含不同类型的对象，而 `dataSource` 字段只允许 PVC 和卷快照。

当 `CrossNamespaceVolumeDataSource` 特性被启用时，存在其他区别：

* `dataSource` 字段仅允许本地对象，而 `dataSourceRef` 字段允许任何名字空间中的对象。
* 若指定了 namespace，则 `dataSource` 和 `dataSourceRef` 不会被同步。

用户始终应该在启用了此特性门控的集群上使用 `dataSourceRef`，
在没有启用该特性门控的集群上使用 `dataSource`。
在任何情况下都没有必要查看这两个字段。
这两个字段的值看似相同但是语义稍微不一样，是为了向后兼容。
特别是混用旧版本和新版本的控制器时，它们能够互通。

## 使用卷填充器   {#using-volume-populators}

卷填充器是能创建非空卷的{{< glossary_tooltip text="控制器" term_id="controller" >}}，
其卷的内容通过一个自定义资源决定。
用户通过使用 `dataSourceRef` 字段引用自定义资源来创建一个被填充的卷：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: populated-pvc
spec:
  dataSourceRef:
    name: example-name
    kind: ExampleDataSource
    apiGroup: example.storage.k8s.io
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

因为卷填充器是外部组件，如果没有安装所有正确的组件，试图创建一个使用卷填充器的 PVC 就会失败。
外部控制器应该在 PVC 上产生事件，以提供创建状态的反馈，包括在由于缺少某些组件而无法创建 PVC 的情况下发出警告。

你可以把 alpha 版本的[卷数据源验证器](https://github.com/kubernetes-csi/volume-data-source-validator)
控制器安装到你的集群中。
如果没有填充器处理该数据源的情况下，该控制器会在 PVC 上产生警告事件。
当一个合适的填充器被安装到 PVC 上时，该控制器的职责是上报与卷创建有关的事件，以及在该过程中发生的问题。

### 使用跨名字空间的卷数据源   {#using-a-cross-namespace-volume-data-source}

{{< feature-state for_k8s_version="v1.26" state="alpha" >}}

创建 ReferenceGrant 以允许名字空间属主接受引用。
你通过使用 `dataSourceRef` 字段指定跨名字空间卷数据源，定义填充的卷。
你必须在源名字空间中已经有一个有效的 ReferenceGrant：

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: ReferenceGrant
metadata:
  name: allow-ns1-pvc
  namespace: default
spec:
  from:
  - group: ""
    kind: PersistentVolumeClaim
    namespace: ns1
  to:
  - group: snapshot.storage.k8s.io
    kind: VolumeSnapshot
    name: new-snapshot-demo
```

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: foo-pvc
  namespace: ns1
spec:
  storageClassName: example
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  dataSourceRef:
    apiGroup: snapshot.storage.k8s.io
    kind: VolumeSnapshot
    name: new-snapshot-demo
    namespace: default
  volumeMode: Filesystem
```

## 编写可移植的配置   {#writing-portable-configuration}

如果你要编写配置模板和示例用来在很多集群上运行并且需要持久性存储，建议你使用以下模式：

- 将 PersistentVolumeClaim 对象包含到你的配置包（Bundle）中，和 Deployment
  以及 ConfigMap 等放在一起。
- 不要在配置中包含 PersistentVolume 对象，因为对配置进行实例化的用户很可能
  没有创建 PersistentVolume 的权限。

- 为用户提供在实例化模板时指定存储类名称的能力。
  - 仍按用户提供存储类名称，将该名称放到 `persistentVolumeClaim.storageClassName` 字段中。
    这样会使得 PVC 在集群被管理员启用了存储类支持时能够匹配到正确的存储类，
  - 如果用户未指定存储类名称，将 `persistentVolumeClaim.storageClassName` 留空（nil）。
    这样，集群会使用默认 `StorageClass` 为用户自动制备一个存储卷。
    很多集群环境都配置了默认的 `StorageClass`，或者管理员也可以自行创建默认的
    `StorageClass`。

- 在你的工具链中，监测经过一段时间后仍未被绑定的 PVC 对象，要让用户知道这些对象，
  因为这可能意味着集群不支持动态存储（因而用户必须先创建一个匹配的 PV），或者
  集群没有配置存储系统（因而用户无法配置需要 PVC 的工作负载配置）。

## {{% heading "whatsnext" %}}

* 进一步了解[创建持久卷](/zh-cn/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolume)。
* 进一步学习[创建 PVC 申领](/zh-cn/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolumeclaim)。
* 阅读[持久存储的设计文档](https://git.k8s.io/design-proposals-archive/storage/persistent-storage.md)。

### API 参考    {#reference}

阅读以下页面中描述的 API：

* [`PersistentVolume`](/zh-cn/docs/reference/kubernetes-api/config-and-storage-resources/persistent-volume-v1/)
* [`PersistentVolumeClaim`](/zh-cn/docs/reference/kubernetes-api/config-and-storage-resources/persistent-volume-claim-v1/)

