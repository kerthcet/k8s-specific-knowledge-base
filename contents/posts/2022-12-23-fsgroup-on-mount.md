---
layout: blog
title: "Kubernetes 1.26: 支持在挂载时将 Pod fsGroup 传递给 CSI 驱动程序"
date: 2022-12-23
slug: kubernetes-12-06-fsgroup-on-mount
---


**作者：** Fabio Bertinatto (Red Hat), Hemant Kumar (Red Hat)

**译者：** Xin Li (DaoCloud)

将 `fsGroup` 委托给 CSI 驱动程序管理首先在 Kubernetes 1.22 中作为 Alpha 特性引入，
并在 Kubernetes 1.25 中进阶至 Beta 状态。
对于 Kubernetes 1.26，我们很高兴地宣布此特性已进阶至正式发布（GA）状态。

在此版本中，如果你在 Pod（Linux）
的[安全上下文](/zh-cn/docs/tasks/configure-pod-container/security-context/#set-the-security-context-for-a-pod)中指定一个 `fsGroup`，
则该 Pod 容器中的所有进程都是该附加组的一部分。

在以前的 Kubernetes 版本中，kubelet **总是**根据 Pod 的
`.spec.securityContext.fsGroupChangePolicy` 字段中指定的策略，
将 `fsGroup` 属主关系和权限的更改应用于卷中的文件。

从 Kubernetes 1.26 开始，CSI 驱动程序可以选择在卷挂载期间应用 `fsGroup` 设置，
这使 kubelet 无需更改这些卷中文件和目录的权限。

## 它是如何工作的？

支持此功能的 CSI 驱动程序应通告其 `VOLUME_MOUNT_GROUP` 节点能力。

kubelet 识别此信息后，在 Pod 启动期间将 fsGroup 信息传递给 CSI 驱动程序。
这个过程是通过 [`NodeStageVolumeRequest`](https://github.com/container-storage-interface/spec/blob/v1.7.0/spec.md#nodestagevolume)
和 [`NodePublishVolumeRequest`](https://github.com/container-storage-interface/spec/blob/v1.7.0/spec.md#nodepublishvolume)
CSI 调用完成的。

因此，CSI 驱动程序应使用**挂载选项**将 `fsGroup` 应用到卷中的文件上。
例如，[Azure File CSIDriver](https://github.com/kubernetes-sigs/azurefile-csi-driver)
利用 `gid` 挂载选项将 `fsGroup` 信息映射到卷中的所有文件。

应该注意的是，在上面的示例中，kubelet 避免直接将权限更改应用于该卷文件中的文件和目录。
此外，有两个策略定义不再有效：CSIDriver 对象的 `.spec.fsGroupPolicy` 和
Pod 的 `.spec.securityContext.fsGroupChangePolicy` 都不再起作用。

有关此功能内部工作原理的更多详细信息，请查看 CSI
开发人员文档中的[增强建议](https://github.com/kubernetes/enhancements/blob/master/keps/sig-storage/2317-fsgroup-on-mount/)和
[CSI 驱动程序 `fsGroup` 支持](https://kubernetes-csi.github.io/docs/support-fsgroup.html)。

## 这一特性为何重要？

如果没有此功能，则无法在某些存储环境中将 fsGroup 信息应用于文件。

例如，Azure 文件不支持 POSIX 风格的文件所有权和权限概念，CSI 驱动程序只能在卷级别设置文件权限。

## 我该如何使用它？

此功能应该对用户基本透明。如果你维护应支持此功能的 CSI 驱动程序，
请阅读 [CSI 驱动程序 `fsGroup` 支持](https://kubernetes-csi.github.io/docs/support-fsgroup.html)
以获取有关如何在你的 CSI 驱动程序中支持此功能的更多信息。

不支持此功能的现有 CSI 驱动程序将继续照常工作：他们不会从 kubelet 收到任何
`fsGroup` 信息。除此之外，kubelet 将根据 CSIDriver 的
`.spec.fsGroupPolicy` 和相关 Pod 的 `.spec.securityContext.fsGroupChangePolicy`
中指定的策略，继续对这些卷中文件的属主关系和权限进行更改。