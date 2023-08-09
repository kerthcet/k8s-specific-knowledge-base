---
layout: blog
title: "Kubernetes 1.27：介绍用于磁盘卷组快照的新 API"
date: 2023-05-08
slug: kubernetes-1-27-volume-group-snapshot-alpha
---

**Author:** Xing Yang (VMware)

**译者**: [顾欣](https://github.com/asa3311) 

磁盘卷组快照在 Kubernetes v1.27 中作为 Alpha 特性被引入。
此特性引入了一个 Kubernetes API，允许用户对多个卷进行快照，以保证在发生故障时数据的一致性。
它使用标签选择器来将多个 `PersistentVolumeClaims` （持久卷申领）分组以进行快照。
这个新特性仅支持 CSI 卷驱动器。


## 磁盘卷组快照概述

一些存储系统提供了创建多个卷的崩溃一致性快照的能力。
卷组快照表示在同一时间点从多个卷中生成的“副本”。
卷组快照可以用来重新填充新的卷（预先填充快照数据）或者将现有卷恢复到以前的状态（由快照代表）。

## 为什么要在 Kubernetes 中添加卷组快照？

Kubernetes 的卷插件系统已经提供了一个强大的抽象层，
可以自动化块存储和文件存储的制备、挂接、挂载、调整大小和快照等操作。

所有这些特性的出发点是 Kubernetes 对工作负载可移植性的目标：
Kubernetes 致力于在分布式应用和底层集群之间创建一个抽象层，
使应用可以对承载它们的集群的特殊属性无感，应用部署不需要特定于某集群的知识。

Kubernetes 已经提供了一个 [VolumeSnapshot](/zh-cn/docs/concepts/storage/volume-snapshots/) API，
这个 API 提供对持久性卷进行快照的能力，可用于防止数据丢失或数据损坏。然而，
还有一些其他的快照功能并未被 VolumeSnapshot API 所覆盖。

一些存储系统支持一致性的卷组快照，允许在同一时间点在多个卷上生成快照，以实现写入顺序的一致性。
这对于包含多个卷的应用非常有用。例如，应用可能在一个卷中存储数据，在另一个卷中存储日志。
如果数据卷和日志卷的快照在不同的时间点进行，应用将不会保持一致，
当灾难发生时从这些快照中恢复，应用将无法正常工作。

确实，你可以首先使应用静默，然后依次为构成应用的每个卷中生成一个独立的快照，
等所有的快照都已逐个生成后，再取消应用的静止状态。这样你就可以得到应用一致性的快照。

然而，有时可能无法使应用静默，或者使应用静默的代价过高，因此你希望较少地进行这个操作。
相较于生成一致性的卷组快照，依次生成单个快照可能需要更长的时间。
由于这些原因，有些用户可能不希望经常使应用静默。例如，
用户可能希望每周进行一次需要应用静默的备份，而在每晚进行不需应用静默但带有卷组一致性支持的备份，
这种一致性支持将确保组中所有卷的崩溃一致性。

## Kubernetes 卷组快照 API

Kubernetes 卷组快照引入了
[三个新的 API 对象](https://github.com/kubernetes-csi/external-snapshotter/blob/master/client/apis/volumegroupsnapshot/v1alpha1/types.go)
用于管理快照：

`VolumeGroupSnapshot`：由 Kubernetes 用户（或由你的自动化系统）创建，
以请求为多个持久卷申领创建卷组快照。它包含了关于卷组快照操作的信息，
如卷组快照的生成时间戳以及是否可直接使用。
此对象的创建和删除代表了创建或删除集群资源（一个卷组快照）的意愿。

`VolumeGroupSnapshotContent`：由快照控制器动态生成的 VolumeGroupSnapshot 所创建。
它包含了关于卷组快照的信息，包括卷组快照 ID。此对象代表了集群上制备的一个资源（一个卷组快照）。 
VolumeGroupSnapshotContent 对象与其创建时所对应的 VolumeGroupSnapshot 之间存在一对一的映射。

`VolumeGroupSnapshotClass`：由集群管理员创建，用来描述如何创建卷组快照，
包括驱动程序信息、删除策略等。

这三种 API 类型被定义为自定义资源（CRD）。
这些 CRD 必须在 Kubernetes 集群中安装，以便 CSI 驱动程序支持卷组快照。

## 如何使用 Kubernetes 卷组快照

卷组快照是在 [external-snapshotter](https://github.com/kubernetes-csi/external-snapshotter)
仓库中实现的。实现卷组快照意味着添加或更改几个组件：

* 添加了新的 CustomResourceDefinition 用于 VolumeGroupSnapshot 和两个辅助性 API。
* 向通用快照控制器中添加卷组快照控制器的逻辑。
* 向通用快照验证 webhook 中添加卷组快照验证 webhook 的逻辑。
* 添加逻辑以便在快照 sidecar 控制器中进行 CSI 调用。

每个集群只部署一次卷快照控制器、CRD 和验证 webhook，
而 sidecar 则与每个 CSI 驱动程序一起打包。

因此，将卷快照控制器、CRD 和验证 webhook 作为集群插件部署是合理的。
我强烈建议 Kubernetes 发行版的厂商将卷快照控制器、
CRD 和验证 webhook 打包并作为他们的 Kubernetes 集群管理过程的一部分（独立于所有 CSI 驱动）。

### 使用 Kubernetes 创建新的卷组快照

一旦定义了一个 VolumeGroupSnapshotClass 对象，并且你有想要一起生成快照的卷，
就可以通过创建一个 VolumeGroupSnapshot 对象来请求一个新的卷组快照。

卷组快照的源指定了底层的卷组快照是应该动态创建，
还是应该使用预先存在的 VolumeGroupSnapshotContent。

预先存在的 VolumeGroupSnapshotContent 由集群管理员创建。
其中包含了在存储系统上实际卷组快照的细节，这些卷组快照可供集群用户使用。

在卷组快照源中，必须设置以下成员之一。

* `selector` - 针对要一起生成快照的 PersistentVolumeClaims 的标签查询。
  该 labelSelector 将用于匹配添加到 PVC 上的标签。
* `volumeGroupSnapshotContentName` - 指定一个现有的 VolumeGroupSnapshotContent 
  对象的名称，该对象代表着一个已存在的卷组快照。 

在以下示例中，有两个 PVC。

```console
NAME        STATUS    VOLUME                                     CAPACITY   ACCESSMODES   AGE
pvc-0       Bound     pvc-a42d7ea2-e3df-11ed-b5ea-0242ac120002   1Gi        RWO           48s
pvc-1       Bound     pvc-a42d81b8-e3df-11ed-b5ea-0242ac120002   1Gi        RWO           48s
```

标记 PVC。

```console
% kubectl label pvc pvc-0 group=myGroup
persistentvolumeclaim/pvc-0 labeled

% kubectl label pvc pvc-1 group=myGroup
persistentvolumeclaim/pvc-1 labeled
```

对于动态制备，必须设置一个选择算符，以便快照控制器可以找到带有匹配标签的 PVC，一起进行快照。

```yaml
apiVersion: groupsnapshot.storage.k8s.io/v1alpha1
kind: VolumeGroupSnapshot
metadata:
  name: new-group-snapshot-demo
  namespace: demo-namespace
spec:
  volumeGroupSnapshotClassName: csi-groupSnapclass
  source:
    selector:
      matchLabels:
        group: myGroup
```

在 VolumeGroupSnapshot 的规约中，用户可以指定 VolumeGroupSnapshotClass，
其中包含应使用哪个 CSI 驱动程序来创建卷组快照的信息。

作为创建卷组快照的一部分，将创建两个单独的卷快照。

```console
snapshot-62abb5db7204ac6e4c1198629fec533f2a5d9d60ea1a25f594de0bf8866c7947-2023-04-26-2.20.4
snapshot-2026811eb9f0787466171fe189c805a22cdb61a326235cd067dc3a1ac0104900-2023-04-26-2.20.4
```

### 如何在 Kubernetes 中使用卷组快照进行恢复

在恢复时，用户可以请求某 VolumeGroupSnapshot 的一部分，即某个 VolumeSnapshot 对象，
创建一个新的 PersistentVolumeClaim。这将触发新卷的制备过程，
并使用指定快照中的数据进行预填充。用户应该重复此步骤，直到为卷组快照的所有部分创建了所有卷。

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc0-restore
  namespace: demo-namespace
spec:
  storageClassName: csi-hostpath-sc
  dataSource:
    name: snapshot-62abb5db7204ac6e4c1198629fec533f2a5d9d60ea1a25f594de0bf8866c7947-2023-04-26-2.20.4
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

## 作为一个存储供应商，我应该如何为我的 CSI 驱动程序添加对卷组快照的支持？

要实现卷组快照功能，CSI 驱动**必须**：

* 实现一个新的组控制器服务。
* 实现组控制器的 RPC：`CreateVolumeGroupSnapshot`，`DeleteVolumeGroupSnapshot` 和 `GetVolumeGroupSnapshot`。
* 添加组控制器的特性 `CREATE_DELETE_GET_VOLUME_GROUP_SNAPSHOT`。

更多详情请参阅 
[CSI规范](https://github.com/container-storage-interface/spec/blob/master/spec.md) 
和 [Kubernetes-CSI驱动程序开发指南](https://kubernetes-csi.github.io/docs/)。

对于 CSI 卷驱动程序，它提供了一种建议采用的机制来部署容器化的 CSI 驱动程序以简化流程。

作为所推荐的部署过程的一部分，Kubernetes 团队提供了许多 sidecar（辅助）容器，
包括已经更新以支持卷组快照的 
[external-snapshotter](https://kubernetes-csi.github.io/docs/external-snapshotter.html) 
sidecar 容器。

external-snapshotter 会监听 Kubernetes API 服务器上的 `VolumeGroupSnapshotContent` 对象，
并对 CSI 端点触发 `CreateVolumeGroupSnapshot` 和 `DeleteVolumeGroupSnapshot` 操作。

## 有哪些限制？

Kubernetes 的卷组快照的 Alpha 版本具有以下限制：

* 不支持将现有的 PVC 还原到由快照表示的较早状态（仅支持从快照创建新的卷）。
* 除了存储系统提供的保证（例如崩溃一致性）之外，不提供应用一致性保证。
  请参阅此[文档](https://github.com/kubernetes/community/blob/master/wg-data-protection/data-protection-workflows-white-paper.md#quiesce-and-unquiesce-hooks)，
  了解有关应用一致性的更多讨论。

## 下一步是什么？

根据反馈和采用情况，Kubernetes 团队计划在 1.28 或 1.29 版本中将 CSI 卷组快照实现推进到 Beta 阶段。
我们有兴趣支持的一些功能包括卷复制、复制组、卷位置选择、应用静默、变更块跟踪等等。

## 如何获取更多信息？

- 有关卷组快照功能的[设计规约](https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/3476-volume-group-snapshot)。
- 卷组快照 API 和控制器的[代码仓库](https://github.com/kubernetes-csi/external-snapshotter)。
- CSI 关于卷组快照功能的[文档](https://kubernetes-csi.github.io/docs/)。

## 如何参与其中？

这个项目，就像 Kubernetes 的所有项目一样，是许多不同背景的贡献者共同努力的结果。
我代表 SIG Storage，
向在过去几个季度中积极参与项目并帮助项目达到 Alpha 版本的贡献者们表示衷心的感谢：

* Alex Meade ([ameade](https://github.com/ameade))
* Ben Swartzlander ([bswartz](https://github.com/bswartz))
* Humble Devassy Chirammal ([humblec](https://github.com/humblec))
* James Defelice ([jdef](https://github.com/jdef))
* Jan Šafránek ([jsafrane](https://github.com/jsafrane))
* Jing Xu ([jingxu97](https://github.com/jingxu97))
* Michelle Au ([msau42](https://github.com/msau42))
* Niels de Vos ([nixpanic](https://github.com/nixpanic))
* Rakshith R ([Rakshith-R](https://github.com/Rakshith-R))
* Raunak Shah ([RaunakShah](https://github.com/RaunakShah))
* Saad Ali ([saad-ali](https://github.com/saad-ali))
* Thomas Watson ([rbo54](https://github.com/rbo54))
* Xing Yang ([xing-yang](https://github.com/xing-yang))
* Yati Padia ([yati1998](https://github.com/yati1998))

我们还要感谢其他为该项目做出贡献的人，
包括帮助审核 [KEP](https://github.com/kubernetes/enhancements/pull/1551)和 
[CSI 规约 PR](https://github.com/container-storage-interface/spec/pull/519)的其他人员。

对于那些对参与 CSI 设计和开发或 Kubernetes 存储系统感兴趣的人，
欢迎加入 [Kubernetes存储特别兴趣小组](https://github.com/kubernetes/community/tree/master/sig-storage)（SIG）。
我们随时欢迎新的贡献者。

我们还定期举行[数据保护工作组会议](https://docs.google.com/document/d/15tLCV3csvjHbKb16DVk-mfUmFry_Rlwo-2uG6KNGsfw/edit#)。
欢迎新的与会者加入我们的讨论。
