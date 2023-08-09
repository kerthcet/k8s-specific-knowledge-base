---
title: Windows 存储
content_type: concept
weight: 110
---

此页面提供特定于 Windows 操作系统的存储概述。

## 持久存储 {#storage}
Windows 有一个分层文件系统驱动程序用来挂载容器层和创建基于 NTFS 的文件系统拷贝。
容器中的所有文件路径仅在该容器的上下文中解析。

* 使用 Docker 时，卷挂载只能是容器中的目录，而不能是单个文件。此限制不适用于 containerd。
* 卷挂载不能将文件或目录映射回宿主文件系统。
* 不支持只读文件系统，因为 Windows 注册表和 SAM 数据库始终需要写访问权限。不过，Windows 支持只读的卷。
* 不支持卷的用户掩码和访问许可，因为宿主与容器之间并不共享 SAM，二者之间不存在映射关系。
  所有访问许可都是在容器上下文中解析的。

因此，Windows 节点不支持以下存储功能：

* 卷子路径挂载：只能在 Windows 容器上挂载整个卷
* Secret 的子路径挂载
* 宿主挂载映射
* 只读的根文件系统（映射的卷仍然支持 `readOnly`）
* 块设备映射
* 内存作为存储介质（例如 `emptyDir.medium` 设置为 `Memory`）
* 类似 UID/GID、各用户不同的 Linux 文件系统访问许可等文件系统特性
* 使用 [DefaultMode 设置 Secret 权限](/zh-cn/docs/concepts/configuration/secret/#secret-files-permissions)
  （因为该特性依赖 UID/GID）
* 基于 NFS 的存储和卷支持
* 扩展已挂载卷（resizefs）

使用 Kubernetes {{< glossary_tooltip text="卷" term_id="volume" >}}，
对数据持久性和 Pod 卷共享有需求的复杂应用也可以部署到 Kubernetes 上。
管理与特定存储后端或协议相关的持久卷时，相关的操作包括：对卷的制备（Provisioning）、
去配（De-provisioning）和调整大小，将卷挂接到 Kubernetes 节点或从节点上解除挂接，
将卷挂载到需要持久数据的 Pod 中的某容器上或从容器上卸载。

卷管理组件作为 Kubernetes 卷[插件](/zh-cn/docs/concepts/storage/volumes/#volume-types)发布。
Windows 支持以下类型的 Kubernetes 卷插件：

* [`FlexVolume plugins`](/zh-cn/docs/concepts/storage/volumes/#flexvolume)
  * 请注意自 1.23 版本起，FlexVolume 已被弃用
* [`CSI Plugins`](/zh-cn/docs/concepts/storage/volumes/#csi)

##### 树内（In-Tree）卷插件  {#in-tree-volume-plugins}

以下树内（In-Tree）插件支持 Windows 节点上的持久存储：

* [`awsElasticBlockStore`](/zh-cn/docs/concepts/storage/volumes/#awselasticblockstore)
* [`azureDisk`](/zh-cn/docs/concepts/storage/volumes/#azuredisk)
* [`azureFile`](/zh-cn/docs/concepts/storage/volumes/#azurefile)
* [`gcePersistentDisk`](/zh-cn/docs/concepts/storage/volumes/#gcepersistentdisk)
* [`vsphereVolume`](/zh-cn/docs/concepts/storage/volumes/#vspherevolume)