---
title: 卷快照类
content_type: concept
weight: 61 # 置于卷快照章节后
---


本文档描述了 Kubernetes 中 VolumeSnapshotClass 的概念。建议熟悉
[卷快照（Volume Snapshots）](/zh-cn/docs/concepts/storage/volume-snapshots/)和
[存储类（Storage Class）](/zh-cn/docs/concepts/storage/storage-classes)。



## 介绍 {#introduction}

就像 StorageClass 为管理员提供了一种在配置卷时描述存储“类”的方法，
VolumeSnapshotClass 提供了一种在配置卷快照时描述存储“类”的方法。

## VolumeSnapshotClass 资源  {#the-volumesnapshortclass-resource}

每个 VolumeSnapshotClass 都包含 `driver`、`deletionPolicy` 和 `parameters` 字段，
在需要动态配置属于该类的 VolumeSnapshot 时使用。

VolumeSnapshotClass 对象的名称很重要，是用户可以请求特定类的方式。
管理员在首次创建 VolumeSnapshotClass 对象时设置类的名称和其他参数，
对象一旦创建就无法更新。

{{< note >}}
CRD 的安装是 Kubernetes 发行版的责任。 如果不存在所需的 CRD，则 VolumeSnapshotClass 的创建将失败。
{{< /note >}}

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: csi-hostpath-snapclass
driver: hostpath.csi.k8s.io
deletionPolicy: Delete
parameters:
```

管理员可以为未请求任何特定类绑定的 VolumeSnapshots 指定默认的 VolumeSnapshotClass，
方法是设置注解 `snapshot.storage.kubernetes.io/is-default-class: "true"`：

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: csi-hostpath-snapclass
  annotations:
    snapshot.storage.kubernetes.io/is-default-class: "true"
driver: hostpath.csi.k8s.io
deletionPolicy: Delete
parameters:
```

### 驱动程序 {#driver}

卷快照类有一个驱动程序，用于确定配置 VolumeSnapshot 的 CSI 卷插件。
此字段必须指定。

### 删除策略 {#deletion-policy}

卷快照类具有 `deletionPolicy` 属性。用户可以配置当所绑定的 VolumeSnapshot
对象将被删除时，如何处理 VolumeSnapshotContent 对象。
卷快照类的这个策略可以是 `Retain` 或者 `Delete`。这个策略字段必须指定。

如果删除策略是 `Delete`，那么底层的存储快照会和 VolumeSnapshotContent 对象
一起删除。如果删除策略是 `Retain`，那么底层快照和 VolumeSnapshotContent
对象都会被保留。

## 参数 {#parameters}

卷快照类具有描述属于该卷快照类的卷快照的参数，可根据 `driver` 接受不同的参数。
