---
title: 卷快照
content_type: concept
weight: 60
---


在 Kubernetes 中，**卷快照** 是一个存储系统上卷的快照，本文假设你已经熟悉了 Kubernetes
的[持久卷](/zh-cn/docs/concepts/storage/persistent-volumes/)。


## 介绍 {#introduction}

与 `PersistentVolume` 和 `PersistentVolumeClaim` 这两个 API 资源用于给用户和管理员制备卷类似，
`VolumeSnapshotContent` 和 `VolumeSnapshot` 这两个 API 资源用于给用户和管理员创建卷快照。

`VolumeSnapshotContent` 是从一个卷获取的一种快照，该卷由管理员在集群中进行制备。
就像持久卷（PersistentVolume）是集群的资源一样，它也是集群中的资源。

`VolumeSnapshot` 是用户对于卷的快照的请求。它类似于持久卷声明（PersistentVolumeClaim）。

`VolumeSnapshotClass` 允许指定属于 `VolumeSnapshot` 的不同属性。在从存储系统的相同卷上获取的快照之间，
这些属性可能有所不同，因此不能通过使用与 `PersistentVolumeClaim` 相同的 `StorageClass` 来表示。

卷快照能力为 Kubernetes 用户提供了一种标准的方式来在指定时间点复制卷的内容，并且不需要创建全新的卷。
例如，这一功能使得数据库管理员能够在执行编辑或删除之类的修改之前对数据库执行备份。

当使用该功能时，用户需要注意以下几点：

- API 对象 `VolumeSnapshot`，`VolumeSnapshotContent` 和 `VolumeSnapshotClass`
  是 {{< glossary_tooltip term_id="CustomResourceDefinition" text="CRD" >}}，
  不属于核心 API。
- `VolumeSnapshot` 支持仅可用于 CSI 驱动。
- 作为 `VolumeSnapshot` 部署过程的一部分，Kubernetes 团队提供了一个部署于控制平面的快照控制器，
  并且提供了一个叫做 `csi-snapshotter` 的边车（Sidecar）辅助容器，和 CSI 驱动程序一起部署。
  快照控制器监视 `VolumeSnapshot` 和 `VolumeSnapshotContent` 对象，
  并且负责创建和删除 `VolumeSnapshotContent` 对象。
  边车 csi-snapshotter 监视 `VolumeSnapshotContent` 对象，
  并且触发针对 CSI 端点的 `CreateSnapshot` 和 `DeleteSnapshot` 的操作。
- 还有一个验证性质的 Webhook 服务器，可以对快照对象进行更严格的验证。
  Kubernetes 发行版应将其与快照控制器和 CRD（而非 CSI 驱动程序）一起安装。
  此服务器应该安装在所有启用了快照功能的 Kubernetes 集群中。
- CSI 驱动可能实现，也可能没有实现卷快照功能。CSI 驱动可能会使用 csi-snapshotter
  来提供对卷快照的支持。详见 [CSI 驱动程序文档](https://kubernetes-csi.github.io/docs/)
- Kubernetes 负责 CRD 和快照控制器的安装。

## 卷快照和卷快照内容的生命周期 {#lifecycle-of-a-volume-snapshot-and-volume-snapshot-content}

`VolumeSnapshotContents` 是集群中的资源。`VolumeSnapshots` 是对于这些资源的请求。
`VolumeSnapshotContents` 和 `VolumeSnapshots` 之间的交互遵循以下生命周期：

### 制备卷快照 {#provisioning-volume-snapshot}

快照可以通过两种方式进行制备：预制备或动态制备。

#### 预制备 {#static}

集群管理员创建多个 `VolumeSnapshotContents`。它们带有存储系统上实际卷快照的详细信息，可以供集群用户使用。
它们存在于 Kubernetes API 中，并且能够被使用。

#### 动态制备 {#dynamic}

可以从 `PersistentVolumeClaim` 中动态获取快照，而不用使用已经存在的快照。
在获取快照时，[卷快照类](/zh-cn/docs/concepts/storage/volume-snapshot-classes/)
指定要用的特定于存储提供程序的参数。

### 绑定 {#binding}

在预制备和动态制备场景下，快照控制器处理绑定 `VolumeSnapshot` 对象和其合适的 `VolumeSnapshotContent` 对象。
绑定关系是一对一的。

在预制备快照绑定场景下，`VolumeSnapshotContent` 对象创建之后，才会和 `VolumeSnapshot` 进行绑定。

### 快照源的持久性卷声明保护   {#persistent-volume-claim-as-snapshot-source-protection}

这种保护的目的是确保在从系统中获取快照时，不会将正在使用的
{{< glossary_tooltip text="PersistentVolumeClaim" term_id="persistent-volume-claim" >}}
API 对象从系统中删除（因为这可能会导致数据丢失）。

在为某 `PersistentVolumeClaim` 生成快照时，该 `PersistentVolumeClaim` 处于被使用状态。
如果删除一个正作为快照源使用的 `PersistentVolumeClaim` API 对象，该 `PersistentVolumeClaim` 对象不会立即被移除。
相反，移除 `PersistentVolumeClaim` 对象的动作会被推迟，直到快照状态变为 ReadyToUse 或快照操作被中止时再执行。

### 删除 {#delete}

删除 `VolumeSnapshot` 对象触发删除 `VolumeSnapshotContent` 操作，并且 `DeletionPolicy` 会紧跟着执行。
如果 `DeletionPolicy` 是 `Delete`，那么底层存储快照会和 `VolumeSnapshotContent` 一起被删除。
如果 `DeletionPolicy` 是 `Retain`，那么底层快照和 `VolumeSnapshotContent` 都会被保留。

## 卷快照 {#volume-snapshots}

每个 `VolumeSnapshot` 包含一个 spec 和一个 status。

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: new-snapshot-test
spec:
  volumeSnapshotClassName: csi-hostpath-snapclass
  source:
    persistentVolumeClaimName: pvc-test
```

`persistentVolumeClaimName` 是 `PersistentVolumeClaim` 数据源对快照的名称。
这个字段是动态制备快照中的必填字段。

卷快照可以通过指定 [VolumeSnapshotClass](/zh-cn/docs/concepts/storage/volume-snapshot-classes/)
使用 `volumeSnapshotClassName` 属性来请求特定类。如果没有设置，那么使用默认类（如果有）。

如下面例子所示，对于预制备的快照，需要给快照指定 `volumeSnapshotContentName` 作为来源。
对于预制备的快照 `source` 中的`volumeSnapshotContentName` 字段是必填的。

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: test-snapshot
spec:
  source:
    volumeSnapshotContentName: test-content
```

## 卷快照内容   {#volume-snapshot-contents}

每个 VolumeSnapshotContent 对象包含 spec 和 status。
在动态制备时，快照通用控制器创建 `VolumeSnapshotContent` 对象。下面是例子：

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotContent
metadata:
  name: snapcontent-72d9a349-aacd-42d2-a240-d775650d2455
spec:
  deletionPolicy: Delete
  driver: hostpath.csi.k8s.io
  source:
    volumeHandle: ee0cfb94-f8d4-11e9-b2d8-0242ac110002
  sourceVolumeMode: Filesystem
  volumeSnapshotClassName: csi-hostpath-snapclass
  volumeSnapshotRef:
    name: new-snapshot-test
    namespace: default
    uid: 72d9a349-aacd-42d2-a240-d775650d2455
```

`volumeHandle` 是存储后端创建卷的唯一标识符，在卷创建期间由 CSI 驱动程序返回。
动态设置快照需要此字段。它指出了快照的卷源。

对于预制备快照，你（作为集群管理员）要按如下命令来创建 `VolumeSnapshotContent` 对象。

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotContent
metadata:
  name: new-snapshot-content-test
spec:
  deletionPolicy: Delete
  driver: hostpath.csi.k8s.io
  source:
    snapshotHandle: 7bdd0de3-aaeb-11e8-9aae-0242ac110002
  sourceVolumeMode: Filesystem
  volumeSnapshotRef:
    name: new-snapshot-test
    namespace: default
```

`snapshotHandle` 是存储后端创建卷的唯一标识符。对于预制备的快照，这个字段是必需的。
它指定此 `VolumeSnapshotContent` 表示的存储系统上的 CSI 快照 ID。

`sourceVolumeMode` 是创建快照的卷的模式。`sourceVolumeMode` 字段的值可以是
`Filesystem` 或 `Block`。如果没有指定源卷模式，Kubernetes 会将快照视为未知的源卷模式。

`volumeSnapshotRef` 字段是对相应的 `VolumeSnapshot` 的引用。
请注意，当 `VolumeSnapshotContent` 被创建为预配置快照时。
`volumeSnapshotRef` 中引用的 `VolumeSnapshot` 可能还不存在。

## 转换快照的卷模式 {#convert-volume-mode}

如果在你的集群上安装的 `VolumeSnapshots` API 支持 `sourceVolumeMode`
字段，则该 API 可以防止未经授权的用户转换卷的模式。

要检查你的集群是否具有此特性的能力，可以运行如下命令：

```shell
kubectl get crd volumesnapshotcontent -o yaml
```

如果你希望允许用户从现有的 `VolumeSnapshot` 创建 `PersistentVolumeClaim`，
但是使用与源卷不同的卷模式，则需要添加注解
`snapshot.storage.kubernetes.io/allow-volume-mode-change: "true"`
到对应 `VolumeSnapshot` 的 `VolumeSnapshotContent` 中。

对于预制备的快照，`spec.sourceVolumeMode` 需要由集群管理员填充。

启用此特性的 `VolumeSnapshotContent` 资源示例如下所示：

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotContent
metadata:
  name: new-snapshot-content-test
  annotations:
    - snapshot.storage.kubernetes.io/allow-volume-mode-change: "true"
spec:
  deletionPolicy: Delete
  driver: hostpath.csi.k8s.io
  source:
    snapshotHandle: 7bdd0de3-aaeb-11e8-9aae-0242ac110002
  sourceVolumeMode: Filesystem
  volumeSnapshotRef:
    name: new-snapshot-test
    namespace: default
```

## 从快照制备卷 {#provisioning-volumes-from-snapshots}

你可以制备一个新卷，该卷预填充了快照中的数据，在 `PersistentVolumeClaim` 对象中使用 **dataSource** 字段。

更多详细信息，
请参阅[卷快照和从快照还原卷](/zh-cn/docs/concepts/storage/persistent-volumes/#volume-snapshot-and-restore-volume-from-snapshot-support)。
