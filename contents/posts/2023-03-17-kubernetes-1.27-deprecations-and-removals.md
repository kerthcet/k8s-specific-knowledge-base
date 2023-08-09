---
layout: blog
title: "Kubernetes 在 v1.27 中移除的特性和主要变更"
date: 2023-03-17T14:00:00+0000
slug: upcoming-changes-in-kubernetes-v1-27
---

**作者**：Harshita Sao

**译者**：Michael Yao (DaoCloud)

随着 Kubernetes 发展和成熟，为了此项目的整体健康，某些特性可能会被弃用、移除或替换为优化过的特性。
基于目前在 v1.27 发布流程中获得的信息，本文将列举并描述一些计划在 Kubernetes v1.27 发布中的变更，
发布工作目前仍在进行中，可能会引入更多变更。

## k8s.gcr.io 重定向到 registry.k8s.io 相关说明   {#note-about-redirect}

Kubernetes 项目为了托管其容器镜像，使用社区拥有的一个名为 registry.k8s.io. 的镜像仓库。
**从 3 月 20 日起，所有来自过期 [k8s.gcr.io](https://cloud.google.com/container-registry/)
仓库的流量将被重定向到 [registry.k8s.io](https://github.com/kubernetes/registry.k8s.io)**。
已弃用的 k8s.gcr.io 仓库最终将被淘汰。

### 这次变更意味着什么？   {#what-does-this-change-mean}

- 如果你是一个子项目的 Maintainer，你必须更新自己的清单和 Helm Chart 来使用新的仓库。
- Kubernetes v1.27 版本不会发布到旧的仓库。
- 从 4 月份起，针对 v1.24、v1.25 和 v1.26 的补丁版本将不再发布到旧的仓库。

我们曾发布了一篇[博文](/blog/2023/03/10/image-registry-redirect/)，
讲述了此次变更有关的所有信息，以及影响到你时应该采取的措施。

## Kubernetes API 移除和弃用流程 {#k8s-api-deprecation-process}

Kubernetes 项目对特性有一个[文档完备的弃用策略](/zh-cn/docs/reference/using-api/deprecation-policy/)。
该策略规定，只有当较新的、稳定的相同 API 可用时，原有的稳定 API 才可以被弃用，
每个稳定级别的 API 都有一个最短的生命周期。弃用的 API 指的是已标记为将在后续发行某个
Kubernetes 版本时移除的 API；移除之前该 API 将继续发挥作用（从弃用起至少一年时间），
但使用时会显示一条警告。被移除的 API 将在当前版本中不再可用，此时你必须迁移以使用替换的 API。

- 正式发布（GA）或稳定的 API 版本可能被标记为已弃用，但只有在 Kubernetes 大版本更新时才会被移除。
- 测试版（Beta）或预发布 API 版本在弃用后必须在后续 3 个版本中继续支持。
- Alpha 或实验性 API 版本可以在任何版本中被移除，不另行通知。

无论一个 API 是因为某特性从 Beta 进阶至稳定阶段而被移除，还是因为该 API 根本没有成功，
所有移除均遵从上述弃用策略。无论何时移除一个 API，文档中都会列出迁移选项。

## 针对 Kubernetes v1.27 移除的 API 和其他变更   {#api-removals-and-other-changes-in-1.27}

### 从 `CSIStorageCapacity` 移除 `storage.k8s.io/v1beta1`

[CSIStorageCapacity](/zh-cn/docs/reference/kubernetes-api/config-and-storage-resources/csi-storage-capacity-v1/)
API 支持通过 CSIStorageCapacity 对象来暴露当前可用的存储容量，并增强在后续绑定时使用 CSI 卷的 Pod 的调度。
CSIStorageCapacity 的 `storage.k8s.io/v1beta1` API 版本在 v1.24 中已被弃用，将在 v1.27 中被移除。

迁移清单和 API 客户端以使用自 v1.24 起可用的 `storage.k8s.io/v1` API 版本。
所有现有的已持久保存的对象都可以通过这个新的 API 进行访问。

更多信息可以参阅
[Storage Capacity Constraints for Pod Scheduling KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/1472-storage-capacity-tracking)。

Kubernetes v1.27 没有移除任何其他 API；但还有其他若干特性将被移除。请继续阅读下文。

### 对弃用的 seccomp 注解的支持

在 Kubernetes v1.19 中，
[seccomp](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/135-seccomp)
（安全计算模式）支持进阶至正式发布 (GA)。
此特性通过限制 Pod（应用到所有容器）或单个容器可执行的系统调用可以提高工作负载安全性。

对 Alpha 状态的 seccomp 注解 `seccomp.security.alpha.kubernetes.io/pod` 和
`container.seccomp.security.alpha.kubernetes.io` 的支持自 v1.19 起被弃用，
现在已完全移除。当创建具有 seccomp 注解的 Pod 时 seccomp 字段将不再被自动填充。
Pod 应转为使用相应的 Pod 或容器 `securityContext.seccompProfile` 字段。

### 移除针对卷扩展的若干特性门控

针对[卷扩展](https://github.com/kubernetes/enhancements/issues/284)
GA 特性的以下特性门控将被移除，且不得再在 `--feature-gates` 标志中引用：

`ExpandCSIVolumes`
: 启用 CSI 卷的扩展。

`ExpandInUsePersistentVolumes`
: 启用扩展正使用的 PVC。

`ExpandPersistentVolumes`
: 启用持久卷的扩展。

### 移除 `--master-service-namespace` 命令行参数

kube-apiserver 接受一个已弃用的命令行参数 `--master-service-namespace`，
该参数指定在何处创建名为 `kubernetes` 的 Service 来表示 API 服务器。
Kubernetes v1.27 将移除自 v1.26 版本已被弃用的该参数。

### 移除 `ControllerManagerLeaderMigration` 特性门控

[Leader Migration](https://github.com/kubernetes/enhancements/issues/2436)
提供了一种机制，让 HA 集群在升级多副本的控制平面时通过在 `kube-controller-manager` 和
`cloud-controller-manager` 这两个组件之间共享的资源锁，安全地迁移“特定于云平台”的控制器。

`ControllerManagerLeaderMigration` 特性自 v1.24 正式发布，被无条件启用，
在 v1.27 版本中此特性门控选项将被移除。
如果你显式设置此特性门控，你将需要从命令行参数或配置文件中将其移除。

### 移除 `--enable-taint-manager` 命令行参数

kube-controller-manager 命令行参数 `--enable-taint-manager` 已被弃用，
将在 Kubernetes v1.27 中被移除。
该参数支持的特性[基于污点的驱逐](/zh-cn/docs/concepts/scheduling-eviction/taint-and-toleration/#taint-based-evictions)已被默认启用，
且在标志被移除时也将继续被隐式启用。

### 移除 `--pod-eviction-timeout` 命令行参数

弃用的命令行参数 `--pod-eviction-timeout` 将被从 kube-controller-manager 中移除。

### 移除 `CSI Migration` 特性门控

[CSI migration](https://github.com/kubernetes/enhancements/issues/625)
程序允许从树内卷插件移动到树外 CSI 驱动程序。
CSI 迁移自 Kubernetes v1.16 起正式发布，关联的 `CSIMigration` 特性门控将在 v1.27 中被移除。

### 移除 `CSIInlineVolume` 特性门控

[CSI Ephemeral Volume](https://github.com/kubernetes/kubernetes/pull/111258)
特性允许在 Pod 规约中直接指定 CSI 卷作为临时使用场景。这些 CSI 卷可用于使用挂载的卷直接在
Pod 内注入任意状态，例如配置、Secret、身份、变量或类似信息。
此特性在 v1.25 中进阶至正式发布。因此，此特性门控 `CSIInlineVolume` 将在 v1.27 版本中移除。

### 移除 `EphemeralContainers` 特性门控

[临时容器](/zh-cn/docs/concepts/workloads/pods/ephemeral-containers/)在 v1.25 中进阶至正式发布。
这些是具有临时持续周期的容器，在现有 Pod 的命名空间内执行。
临时容器通常由用户发起，以观察其他 Pod 和容器的状态进行故障排查和调试。
对于 Kubernetes v1.27，对临时容器的 API 支持被无条件启用；`EphemeralContainers` 特性门控将被移除。

### 移除 `LocalStorageCapacityIsolation` 特性门控

[Local Ephemeral Storage Capacity Isolation](https://github.com/kubernetes/kubernetes/pull/111513)
特性在 v1.25 中进阶至正式发布。此特性支持 `emptyDir` 卷这类 Pod 之间本地临时存储的容量隔离，
因此可以硬性限制 Pod 对共享资源的消耗。如果本地临时存储的消耗超过了配置的限制，kubelet 将驱逐 Pod。
特性门控 `LocalStorageCapacityIsolation` 将在 v1.27 版本中被移除。

### 移除 `NetworkPolicyEndPort` 特性门控

Kubernetes v1.25 版本将 NetworkPolicy 中的 `endPort` 进阶至正式发布。
支持 `endPort` 字段的 NetworkPolicy 提供程序可用于指定一系列端口以应用 NetworkPolicy。
以前每个 NetworkPolicy 只能针对一个端口。因此，此特性门控 `NetworkPolicyEndPort` 将在此版本中被移除。

请注意，`endPort` 字段必须得到 NetworkPolicy 提供程序的支持。
如果你的提供程序不支持 `endPort`，并且此字段在 NetworkPolicy 中指定，
则将创建仅涵盖端口字段（单个端口）的 NetworkPolicy。

### 移除 `StatefulSetMinReadySeconds` 特性门控

对于作为 StatefulSet 一部分的 Pod，只有当 Pod 至少在
[`minReadySeconds`](/zh-cn/docs/concepts/workloads/controllers/statefulset/#minimum-ready-seconds)
中指定的持续期内可用（并通过检查）时，Kubernetes 才会将此 Pod 标记为只读。
该特性在 Kubernetes v1.25 中正式发布，`StatefulSetMinReadySeconds`
特性门控将锁定为 true，并在 v1.27 版本中被移除。

### 移除 `IdentifyPodOS` 特性门控

你可以为 Pod 指定操作系统，此项特性支持自 v1.25 版本进入稳定。
`IdentifyPodOS` 特性门控将在 Kubernetes v1.27 中被移除。

### 移除 `DaemonSetUpdateSurge` 特性门控

Kubernetes v1.25 版本还稳定了对 DaemonSet Pod 的浪涌支持，
其实现是为了最大限度地减少部署期间 DaemonSet 的停机时间。
`DaemonSetUpdateSurge` 特性门控将在 Kubernetes v1.27 中被移除。

### 移除 `--container-runtime` 命令行参数

kubelet 接受一个已弃用的命令行参数 `--container-runtime`，
并且在移除 dockershim 代码后，唯一有效的值将是 `remote`。
Kubernetes v1.27 将移除该参数，该参数自 v1.24 版本以来已被弃用。

## 前瞻   {#looking-ahead}

Kubernetes 1.29 计划[移除的 API 官方列表](/zh-cn/docs/reference/using-api/deprecation-guide/#v1-29)包括：

- FlowSchema 和 PriorityLevelConfiguration 的 `flowcontrol.apiserver.k8s.io/v1beta2`
  API 版本将不再在 v1.29 中提供。

## 了解更多   {#want-to-know-more}

Kubernetes 发行说明中宣告了弃用信息。你可以在以下版本的发行说明中看到待弃用的公告：

- [Kubernetes v1.23](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.23.md#deprecation)

- [Kubernetes v1.24](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.24.md#deprecation)

- [Kubernetes v1.25](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.25.md#deprecation)

- [Kubernetes v1.26](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.26.md#deprecation)

我们将在
[Kubernetes v1.27](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.27.md#deprecation)
的 CHANGELOG 中正式宣布该版本的弃用信息。

有关弃用和移除流程信息，请查阅正式的
[Kubernetes 弃用策略](/zh-cn/docs/reference/using-api/deprecation-policy/#deprecating-parts-of-the-api)文档。
