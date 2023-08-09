---
layout: blog
title: "Kubernetes 1.27：持久卷的单个 Pod 访问模式升级到 Beta"
date: 2023-04-20
slug: read-write-once-pod-access-mode-beta
---

**作者**：Chris Henzie (Google)

**译者**：顾欣 (ICBC)

随着 Kubernetes v1.27 的发布，ReadWriteOncePod 功能已经升级为 Beta 版。
在这篇博客文章中，我们将更详细地介绍这个功能，作用以及在 Beta 版本中的发展。

## 什么是 ReadWriteOncePod  {#what-is-readwriteoncepod}

ReadWriteOncePod 是 Kubernetes 在 v1.22 中引入的一种新的访问模式，
适用于 [PersistentVolume](/zh-cn/docs/concepts/storage/persistent-volumes/#persistent-volumes)(PVs)
和 [PersistentVolumeClaim](/zh-cn/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)(PVCs)。
此访问模式使你能够将存储卷访问限制在集群中的单个 Pod 上，确保一次只有一个 Pod 可以写入存储卷。
这可能对需要单一写入者访问存储的有状态工作负载特别有用。

要了解有关访问模式和 ReadWriteOncePod 如何工作的更多背景信息，
请阅读 2021 年介绍 PersistentVolume 的单个 Pod 访问模式的文章中的[什么是访问模式和为什么它们如此重要？](/blog/2021/09/13/read-write-once-pod-access-mode-alpha/#what-are-access-modes-and-why-are-they-important)。

## ReadWriteOncePod 的 Beta 版中变化  {#changes-in-the-readwriteoncepod-beta}

ReadWriteOncePod Beta 版为使用 ReadWriteOncePod PVC 的 Pod 添加[调度器抢占](/zh-cn/docs/concepts/scheduling-eviction/pod-priority-preemption/)。

调度器抢占允许更高优先级的 Pod 抢占较低优先级的 Pod，以便它们可以在同一节点上运行。
在此版本中，如果更高优先级的 Pod 需要相同的 PVC，使用 ReadWriteOncePod PVCs 的 Pod 也可以被抢占。

## 如何开始使用 ReadWriteOncePod？  {#how-can-i-start-using-readwriteoncepod}

随着 ReadWriteOncePod 现已升级为 Beta 版，在 v1.27 及更高版本的集群中将默认启用该功能。

请注意，ReadWriteOncePod [仅支持 CSI 卷](/zh-cn/docs/concepts/storage/persistent-volumes/#access-modes)。
在使用此功能之前，你需要将以下 [CSI Sidecars](https://kubernetes-csi.github.io/docs/sidecar-containers.html)更新至以下版本或更高版本：

- [csi-provisioner:v3.0.0+](https://github.com/kubernetes-csi/external-provisioner/releases/tag/v3.0.0)
- [csi-attacher:v3.3.0+](https://github.com/kubernetes-csi/external-attacher/releases/tag/v3.3.0)
- [csi-resizer:v1.3.0+](https://github.com/kubernetes-csi/external-resizer/releases/tag/v1.3.0)

要开始使用 ReadWriteOncePod，请创建具有 ReadWriteOncePod 访问模式的 PVC：

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: single-writer-only
spec:
  accessModes:
  - ReadWriteOncePod #仅允许一个容器访问且独占写入权限。
  resources:
    requests:
      storage: 1Gi
```

如果你的存储插件支持[动态制备](/zh-cn/docs/concepts/storage/dynamic-provisioning/)，
新创建的持久卷将应用 ReadWriteOncePod 访问模式。

阅读[迁移现有持久卷](/blog/2021/09/13/read-write-once-pod-access-mode-alpha/#migrating-existing-persistentvolumes)
以了解如何迁移现有卷以使用 ReadWriteOncePod。

## 如何了解更多信息？ {#how-can-i-learn-more}

请查看 [Alpha 版博客](/blog/2021/09/13/read-write-once-pod-access-mode-alpha)和
[KEP-2485](https://github.com/kubernetes/enhancements/blob/master/keps/sig-storage/2485-read-write-once-pod-pv-access-mode/README.md)
以了解关于 ReadWriteOncePod 访问模式的更多详细信息以及对 CSI 规约作更改的动机。

## 如何参与？ {#how-do-i-get-involved}

[Kubernetes #csi Slack](https://kubernetes.slack.com/messages/csi)频道以及任何常规的
[SIG 存储沟通渠道](https://github.com/kubernetes/community/blob/master/sig-storage/README.md#contact)
都是联系 SIG 存储和 CSI 团队的最佳途径。

特别感谢以下人士的仔细的审查和反馈，帮助完成了这个功能：

* Abdullah Gharaibeh (ahg-g)
* Aldo Culquicondor (alculquicondor)
* Antonio Ojea (aojea)
* David Eads (deads2k)
* Jan Šafránek (jsafrane)
* Joe Betz (jpbetz)
* Kante Yin (kerthcet)
* Michelle Au (msau42)
* Tim Bannister (sftim)
* Xing Yang (xing-yang)

如果您有兴趣参与 CSI 或 Kubernetes 存储系统的任何部分的设计和开发，
请加入 [Kubernetes 存储特别兴趣小组](https://github.com/kubernetes/community/tree/master/sig-storage)(SIG)。
我们正在迅速发展，始终欢迎新的贡献者。