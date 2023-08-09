---
layout: blog
title: "Kubernetes 1.23：树内存储向 CSI 卷迁移工作的进展更新"
date: 2021-12-10
slug: storage-in-tree-to-csi-migration-status-update
---

**作者**: Jiawei Wang（谷歌）

自 Kubernetes v1.14 引入容器存储接口（[Container Storage Interface, CSI](/blog/2019/01/15/container-storage-interface-ga/)）的工作达到 alpha 阶段后，自 v1.17 起，Kubernetes 树内存储插件（in-tree storage plugin）向 CSI 的迁移基础设施已步入 [beta 阶段](/blog/2019/12/09/kubernetes-1-17-feature-csi-migration-beta/)。

自那时起，Kubernetes 存储特别兴趣组（special interest groups, SIG）及其他 Kubernetes 特别兴趣组就在努力确保这一功能的稳定性和兼容性，为正式发布做准备。
本文旨在介绍该功能的最新开发进展，以及 Kubernetes v1.17 到 v1.23 之间的变化。此外，我还将介绍每个存储插件的 CSI 迁移功能达到正式发布阶段的未来路线图。

## 快速回顾：CSI 迁移功能是什么？为什么要迁移？  {#quick-recap-what-is-csi-migration-and-why-migrate}

容器存储接口旨在帮助 Kubernetes 取代其现有的树内存储驱动机制──特别是供应商的特定插件。自 v1.13 起，Kubernetes 对[容器存储接口](https://github.com/container-storage-interface/spec/blob/master/spec.md#README)的支持工作已达到[正式发布阶段](/blog/2019/01/15/container-storage-interface-ga/)。引入对 CSI 驱动的支持，将使得 Kubernetes 和存储后端技术之间的集成工作更易建立和维护。使用 CSI 驱动可以实现更好的可维护性（驱动作者可以决定自己的发布周期和支持生命周期）、减少出现漏洞的机会（得益于更少的树内代码，出现错误的风险会降低。另外，集群操作员可以只选择集群需要的存储驱动）。

随着更多的 CSI 驱动诞生并进入生产就绪阶段，Kubernetes 存储特别兴趣组希望所有 Kubernetes 用户都能从 CSI 模型中受益──然而，我们不应破坏与现有存储 API 类型的 API 兼容性。对此，我们给出的解决方案是 CSI 迁移：该功能实现将树内存储 API 翻译成等效的 CSI API，并把操作委托给一个替换的 CSI 驱动来完成。

CSI 迁移工作使存储后端现有的树内存储插件（如 `kubernetes.io/gce-pd` 或 `kubernetes.io/aws-ebs`）能够被相应的 [CSI 驱动](https://kubernetes-csi.github.io/docs/introduction.html) 所取代。如果 CSI 迁移功能正确发挥作用，Kubernetes 终端用户应该不会注意到有什么变化。现有的 `StorageClass`、`PersistentVolume` 和 `PersistentVolumeClaim` 对象应继续工作。当 Kubernetes 集群管理员更新集群以启用 CSI 迁移功能时，利用到 PVCs[^1]（由树内存储插件支持）的现有工作负载将继续像以前一样运作──不过在幕后，Kubernetes 将所有存储管理操作（以前面向树内存储驱动的）交给 CSI 驱动控制。

举个例子。假设你是 `kubernetes.io/gce-pd` 用户，在启用 CSI 迁移功能后，你仍然可以使用 `kubernetes.io/gce-pd` 来配置新卷、挂载现有的 GCE-PD 卷或删除现有卷。所有现有的 API/接口 仍将正常工作──只不过，底层功能调用都将通向 [GCE PD CSI 驱动](https://github.com/kubernetes-sigs/gcp-compute-persistent-disk-csi-driver)，而不是 Kubernetes 的树内存储功能。

这使得 Kubernetes 终端用户可以顺利过渡。另外，对于存储插件的开发者，我们可以减少他们维护树内存储插件的负担，并最终将这些插件从 Kubernetes 核心的二进制中移除。

## 改进与更新  {#what-has-been-changed-and-what-s-new}
在 Kubernetes v1.17 及更早的工作基础上，此后的发布有了以下一系列改变：

### 新的特性门控（feature gate）  {#new-feature-gates}
Kubernetes v1.21 弃用了 `CSIMigration{provider}Complete` 特性参数（feature flag），它们不再生效。取而代之的是名为 `InTreePlugin{vendor}Unregister` 的新特性参数，它们保留了 `CSIMigration{provider}Complete` 提供的所有功能。

`CSIMigration{provider}Complete` 是作为 CSI 迁移功能在所有节点上启用后的补充特性门控于之前引入的。这个参数可注销参数名称中 `{provider}` 部分所指定的树内存储插件。

当你启用该特性门控时，你的集群不再使用树内驱动代码，而是直接选择并使用相应的 CSI 驱动。同时，集群并不检查节点上 CSI 迁移功能是否启用，以及 CSI 驱动是否实际部署。

虽然这一特性门控是一个很好的帮手，但 Kubernetes 存储特别兴趣组（以及，我相信还有很多集群操作员）同样希望有一个特性门控可以让你即使在不启用 CSI 迁移功能时，也能禁用树内存储插件。例如，你可能希望在一个 GCE 集群上禁用 EBS 存储插件，因为 EBS 卷是其他供应商的云（AWS）所专有的。

为了使这成为可能，Kubernetes v1.21 引入了一个新的特性参数集合：`InTreePlugin{vendor}Unregister`。

`InTreePlugin{vendor}Unregister` 是一种特性门控，可以独立于 CSI 迁移功能来启用或禁用。当启用此种特性门控时，组件将不会把相应的树内存储插件注册到支持的列表中。如果集群操作员只启用了这种参数，终端用户将在使用该插件的 PVC[^1] 处遇到错误，提示其找不到插件。如果集群操作员不想支持过时的树内存储 API，只支持 CSI，那么他们可能希望启用这种特性门控而不考虑 CSI 迁移功能。


### 可观察性  {#observability}

Kubernetes v1.21 引入了跟踪 CSI 迁移功能的[指标](https://github.com/kubernetes/kubernetes/issues/98279)。你可以使用这些指标来观察你的集群是如何使用存储服务的，以及对该存储的访问使用的是传统的树内驱动还是基于 CSI 的替代。

| 组件 | 指标 | 注释 |
| ---- | ---- | ---- |
| Kube-Controller-Manager | storage_operation_duration_seconds | 一个新的标签 `migrated` 被添加到指标中，以表明该存储操作是否由 CSI 迁移功能操作（字符串值为 `true` 表示启用，`false` 表示未启用）。 |
| Kubelet | csi_operations_seconds | 新的指标提供的标签包括 `driver_name`、`method_name`、`grpc_status_code` 和 `migrated`。这些标签的含义与 `csi_sidecar_operations_seconds` 相同。 |
| CSI Sidecars(provisioner, attacher, resizer) | csi_sidecar_operations_seconds | 一个新的标签 `migrated` 被添加到指标中，以表明该存储操作是否由 CSI 迁移功能操作（字符串值为 `true` 表示启用，`false` 表示未启用）。 |

### 错误修复和功能改进  {#bug-fixes-and-feature-improvement}

籍由 beta 测试人员的帮助，我们修复了许多错误──如悬空附件、垃圾收集、拓扑标签错误等。

### 与 Kubernetes 云提供商特别兴趣组、集群生命周期特别兴趣组的合作  {#cloud-provider-cluster-lifecycle-collaboration}

Kubernetes 存储特别兴趣组与云提供商特别兴趣组和集群生命周期特别兴趣组，正为了 CSI 迁移功能上线而密切合作。

如果你采用托管 Kubernetes 服务，请询问你的供应商是否有什么工作需要完成。在许多情况下，供应商将管理迁移，你不需要做额外的工作。

如果你使用的是 Kubernetes 的发行版，请查看其官方文档，了解对该功能的支持情况。对于已进入正式发布阶段的 CSI 迁移功能，Kubernetes 存储特别兴趣组正与Kubernetes 集群生命周期特别兴趣组合作，以便在这些功能于 Kubernetes 中可用时，使迁移机制也进入到周边工具（如 kubeadm）中。

## 时间计划及当前状态  {#timeline-and-status}

各驱动的当前发布及目标发布如下表所示：

| 驱动 | Alpha | Beta（启用树内插件） | Beta（默认启用） | 正式发布 | 目标：移除“树内存储插件” |
| ---------------- | ----- | ------------------------- | -------------------- | ------------- | ------------------------------- |
| AWS EBS          | 1.14  | 1.17                      | 1.23                 | 1.24 (Target) | 1.26 (Target)                   |
| GCE PD           | 1.14  | 1.17                      | 1.23                 | 1.24 (Target) | 1.26 (Target)                   |
| OpenStack Cinder | 1.14  | 1.18                      | 1.21                 | 1.24 (Target) | 1.26 (Target)                   |
| Azure Disk       | 1.15  | 1.19                      | 1.23                 | 1.24 (Target) | 1.26 (Target)                   |
| Azure File       | 1.15  | 1.21                      | 1.24 (Target)        | 1.25 (Target) | 1.27 (Target)                   |
| vSphere          | 1.18  | 1.19                      | 1.24 (Target)        | 1.25 (Target) | 1.27 (Target)                   |
| Ceph RBD         | 1.23  |
| Portworx         | 1.23  |

以下存储驱动将不会支持 CSI 迁移功能。其中 ScaleIO 驱动已经被移除；其他驱动都被弃用，并将从 Kubernetes 核心中删除。

| 驱动 | 被弃用 | 代码移除 |
| ---- | ---- | ---- |
| ScaleIO   | 1.16 | 1.22          |
| Flocker   | 1.22 | 1.25 (Target) |
| Quobyte   | 1.22 | 1.25 (Target) |
| StorageOS | 1.22 | 1.25 (Target) |

## 下一步的计划  {#what-s-next}

随着更多的 CSI 驱动进入正式发布阶段，我们希望尽快将整个 CSI 迁移功能标记为正式发布状态。我们计划在 Kubernetes v1.26 和 v1.27 之前移除云提供商树内存储插件的代码。

## 作为用户，我应该做什么？  {#what-should-i-do-as-a-user}

请注意，Kubernetes 存储系统的所有新功能（如卷快照）将只被添加到 CSI 接口。因此，如果你正在启动一个新的集群、首次创建有状态的应用程序，或者需要这些新功能，我们建议你在本地使用 CSI 驱动（而不是树内卷插件 API）。遵循[最新的 CSI 驱动用户指南](https://kubernetes-csi.github.io/docs/drivers.html)并使用新的 CSI API。

然而，如果您选择沿用现有集群或继续使用传统卷 API 的规约，CSI 迁移功能将确保我们通过新 CSI 驱动继续支持这些部署。但是，如果您想利用快照等新功能，则需要进行手动迁移，将现有的树内持久卷重新导入为 CSI 持久卷。

## 我如何参与其中？  {#how-do-i-get-involved}
Kubernetes Slack 频道 [#csi-migration](https://kubernetes.slack.com/messages/csi-migration) 以及任何一个标准的 [SIG Storage 通信频道](https://github.com/kubernetes/community/blob/master/sig-storage/README.md#contact)都是与 Kubernetes 存储特别兴趣组和迁移工作组团队联系的绝佳媒介。

该项目，和其他所有 Kubernetes 项目一样，是许多来自不同背景的贡献者共同努力的结果。我们非常感谢在过去几个季度里挺身而出帮助推动项目发展的贡献者们：

* Michelle Au (msau42)
* Jan Šafránek (jsafrane)
* Hemant Kumar (gnufied)

特别感谢以下人士对 CSI 迁移功能的精辟评论、全面考虑和宝贵贡献：

* Andy Zhang (andyzhangz)
* Divyen Patel (divyenpatel)
* Deep Debroy (ddebroy)
* Humble Devassy Chirammal (humblec)
* Jing Xu (jingxu97)
* Jordan Liggitt (liggitt)
* Matthew Cary (mattcary)
* Matthew Wong (wongma7)
* Neha Arora (nearora-msft)
* Oksana Naumov (trierra)
* Saad Ali (saad-ali)
* Tim Bannister (sftim)
* Xing Yang (xing-yang)

有兴趣参与 CSI 或 Kubernetes 存储系统任何部分的设计和开发的人，请加入 [Kubernetes 存储特别兴趣组](https://github.com/kubernetes/community/tree/master/sig-storage)。我们正在迅速成长，并一直欢迎新的贡献者。


[^1]: 持久卷申领（PersistentVolumeClaim，PVC）