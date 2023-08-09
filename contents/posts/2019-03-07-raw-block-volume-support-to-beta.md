---
layout: blog
title: Raw Block Volume 支持进入 Beta
date: 2019-03-07
slug: raw-block-volume-support-to-beta
---

**作者：**
Ben Swartzlander (NetApp), Saad Ali (Google)

Kubernetes v1.13 中对原生数据块卷（Raw Block Volume）的支持进入 Beta 阶段。此功能允许将持久卷作为块设备而不是作为已挂载的文件系统暴露在容器内部。

## 什么是块设备？

块设备允许对固定大小的块中的数据进行随机访问。硬盘驱动器、SSD 和 CD-ROM 驱动器都是块设备的例子。

通常，持久性性存储是在通过在块设备（例如磁盘或 SSD）之上构造文件系统（例如 ext4）的分层方式实现的。这样应用程序就可以读写文件而不是操作数据块进。操作系统负责使用指定的文件系统将文件读写转换为对底层设备的数据块读写。

值得注意的是，整个磁盘都是块设备，磁盘分区也是如此，存储区域网络（SAN）设备中的 LUN 也是一样的。

## 为什么要将 raw block volume 添加到 kubernetes？

有些特殊的应用程序需要直接访问块设备，原因例如，文件系统层会引入不必要的开销。最常见的情况是数据库，通常会直接在底层存储上组织数据。原生的块设备（Raw Block Devices）还通常由能自己实现某种存储服务的软件（软件定义的存储系统）使用。

从程序员的角度来看，块设备是一个非常大的字节数组，具有某种最小读写粒度，通常为 512 个字节，大部分情况为 4K 或更大。

随着在 Kubernetes 中运行数据库软件和存储基础架构软件变得越来越普遍，在 Kubernetes 中支持原生块设备的需求变得越来越重要。

## 哪些卷插件支持 raw block？

在发布此博客时，以下 in-tree 卷类型支持原生块设备：

- AWS EBS
- Azure Disk
- Cinder
- Fibre Channel
- GCE PD
- iSCSI
- Local volumes
- RBD (Ceph)
- Vsphere

Out-of-tree [CSI 卷驱动程序](https://kubernetes.io/blog/2019/01/15/container-storage-interface-ga/) 可能也支持原生数据块卷。Kubernetes CSI 对原生数据块卷的支持目前为 alpha 阶段。参考 [这篇](https://kubernetes-csi.github.io/docs/raw-block.html) 文档。

## Kubernetes raw block volume 的 API

原生数据块卷与普通存储卷有很多共同点。两者都通过创建与 `PersistentVolume` 对象绑定的 `PersistentVolumeClaim` 对象发起请求，并通过将它们加入到 `PodSpec` 的 volumes 数组中来连接到 Kubernetes 中的 Pod。

但是有两个重要的区别。首先，要请求原生数据块设备的 `PersistentVolumeClaim` 必须在 `PersistentVolumeClaimSpec` 中设置 `volumeMode = "Block"`。`volumeMode` 为空时与传统设置方式中的指定 `volumeMode = "Filesystem"` 是一样的。`PersistentVolumes` 在其 `PersistentVolumeSpec` 中也有一个 `volumeMode` 字段，`"Block"` 类型的 PVC 只能绑定到 `"Block"` 类型的 PV 上，而`"Filesystem"` 类型的 PVC 只能绑定到 `"Filesystem"` PV 上。

其次，在 Pod 中使用原生数据块卷时，必须在 `PodSpec` 的 Container 部分指定一个 `VolumeDevice`，而不是 `VolumeMount`。`VolumeDevices` 具备 `devicePaths` 而不是 `mountPaths`，在容器中，应用程序将看到位于该路径的设备，而不是挂载了的文件系统。

应用程序打开、读取和写入容器内的设备节点，就像它们在非容器化或虚拟环境中与系统上的任何块设备交互一样。

## 创建一个新的原生块设备 PVC

首先，请确保与您选择的存储类关联的驱动支持原生块设备。然后创建 PVC。

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteMany
  volumeMode: Block
  storageClassName: my-sc
  resources:
    requests:
    storage: 1Gi
```

## 使用原生块 PVC

在 Pod 定义中使用 PVC 时，需要选择块设备的设备路径，而不是文件系统的安装路径。

```
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: busybox
      command:
        - sleep
        - “3600”
      volumeDevices:
        - devicePath: /dev/block
          name: my-volume
      imagePullPolicy: IfNotPresent
  volumes:
    - name: my-volume
      persistentVolumeClaim:
        claimName: my-pvc
```

## 作为存储供应商，我如何在 CSI 插件中添加对原生块设备的支持？

CSI 插件的原生块支持仍然是 alpha 版本，但是现在可以改进了。[CSI 规范](https://github.com/container-storage-interface/spec/blob/master/spec.md) 详细说明了如何处理具有 `BlockVolume` 能力而不是 `MountVolume` 能力的卷的请求。CSI 插件可以支持两种类型的卷，也可以支持其中一种或另一种。更多详细信息，请查看 [这个文档](https://kubernetes-csi.github.io/docs/raw-block.html)。


## 问题/陷阱

由于块设备实质上还是设备，因此可以从容器内部对其进行底层操作，而文件系统的卷则无法执行这些操作。例如，实际上是块设备的 SCSI 磁盘支持使用 Linux ioctl 向设备发送 SCSI 命令。

默认情况下，Linux 不允许容器将 SCSI 命令从容器内部发送到磁盘。为此，必须向容器安全层级认证 `SYS_RAWIO` 功能实现这种行为。请参阅 [这篇](/docs/tasks/configure-pod-container/security-context/#set-capabilities-for-a-container) 文档。

另外，尽管 Kubernetes 保证可以将块设备交付到容器中，但不能保证它实际上是 SCSI 磁盘或任何其他类型的磁盘。用户必须确保所需的磁盘类型与 Pod 一起使用，或只部署可以处理各种块设备类型的应用程序。

## 如何学习更多？

在此处查看有关 snapshot 功能的其他文档：[Raw Block Volume 支持](/docs/concepts/storage/persistent-volumes/#raw-block-volume-support)

如何参与进来？

加入 Kubernetes 存储 SIG 和 CSI 社区，帮助我们添加更多出色的功能并改进现有功能，就像 raw block 存储一样！

https://github.com/kubernetes/community/tree/master/sig-storage
https://github.com/container-storage-interface/community/blob/master/README.md

特别感谢所有为 Kubernetes 增加 block volume 支持的贡献者，包括：

- Ben Swartzlander (https://github.com/bswartz)
- Brad Childs (https://github.com/childsb)
- Erin Boyd (https://github.com/erinboyd)
- Masaki Kimura (https://github.com/mkimuram)
- Matthew Wong (https://github.com/wongma7)
- Michelle Au (https://github.com/msau42)
- Mitsuhiro Tanino (https://github.com/mtanino)
- Saad Ali (https://github.com/saad-ali)
