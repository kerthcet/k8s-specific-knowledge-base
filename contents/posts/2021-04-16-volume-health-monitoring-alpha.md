---
layout: blog
title: "卷健康监控的 Alpha 更新"
date: 2021-04-16
slug: volume-health-monitoring-alpha-update
---

**作者：** Xing Yang (VMware)

最初在 1.19 中引入的 CSI 卷健康监控功能在 1.21 版本中进行了大规模更新。

## 为什么要向 Kubernetes 添加卷健康监控？

如果没有卷健康监控，在 PVC 被 Pod 配置和使用后，Kubernetes 将不知道存储系统的底层卷的状态。
在 Kubernetes 中配置卷后，底层存储系统可能会发生很多事情。
例如，卷可能在 Kubernetes 之外被意外删除、卷所在的磁盘可能发生故障、容量不足、磁盘可能被降级而影响其性能等等。
即使卷被挂载到 Pod 上并被应用程序使用，以后也可能会出现诸如读/写 I/O 错误、文件系统损坏、在 Kubernetes 之外被意外卸载卷等问题。
当发生这样的事情时，调试和检测根本原因是非常困难的。

卷健康监控对 Kubernetes 用户非常有益。
它可以与 CSI 驱动程序通信以检索到底层存储系统检测到的错误。
用户可以收到报告上来的 PVC 事件继而采取行动。
例如，如果卷容量不足，他们可以请求卷扩展以获得更多空间。

## 什么是卷健康监控？

CSI 卷健康监控允许 CSI 驱动程序检测来自底层存储系统的异常卷状况，并将其作为 PVC 或 Pod 上的事件报送。

监控卷和使用卷健康信息报送事件的 Kubernetes 组件包括：

* Kubelet 除了收集现有的卷统计信息外，还将观察该节点上 PVC 的卷健康状况。
  如果 PVC 的健康状况异常，则会在使用 PVC 的 Pod 对象上报送事件。
  如果多个 Pod 使用相同的 PVC，则将在使用该 PVC 的所有 Pod 上报送事件。 
* 一个[外部卷健康监视控制器](https://github.com/kubernetes-csi/external-health-monitor)监视 PVC 的卷健康并报告 PVC 上的事件。

请注意，在 Kubernetes 1.19 版本中首次引入此功能时，节点侧卷健康监控逻辑是一个外部代理。
在 Kubernetes 1.21 中，节点侧卷健康监控逻辑从外部代理移至 Kubelet，以避免 CSI 函数重复调用。
随着 1.21 中的这一变化，为 Kubelet 中的卷健康监控逻辑引入了一个新的 alpha [特性门](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/) `CSIVolumeHealth`。 

目前，卷健康监控功能仅供参考，因为它只报送 PVC 或 Pod 上的异常卷健康事件。
用户将需要检查这些事件并手动修复问题。
此功能可作为 Kubernetes 未来以编程方式检测和解决卷健康问题的基石。

## 如何在 Kubernetes 集群上使用卷健康？

要使用卷健康功能，首先确保你使用的 CSI 驱动程序支持此功能。
请参阅此 [CSI 驱动程序文档](https://kubernetes-csi.github.io/docs/drivers.html)以了解哪些 CSI 驱动程序支持此功能。

要从节点侧启用卷健康监控，需要启用 alpha 特性门 `CSIVolumeHealth`。

如果 CSI 驱动程序支持控制器端的卷健康监控功能，则有关异常卷条件的事件将记录在 PVC 上。

如果 CSI 驱动程序支持控制器端的卷健康监控功能，
当部署外部健康监控控制器时 `enable-node-watcher` 标志设置为 true，用户还可以获得有关节点故障的事件。
当检测到节点故障事件时，会在 PVC 上报送一个事件，指示使用该 PVC 的 Pod 在故障节点上。

如果 CSI 驱动程序支持节点端的卷健康监控功能，则有关异常卷条件的事件将使用 PVC 记录在 Pod 上。

## 作为存储供应商，如何向 CSI 驱动程序添加对卷健康的支持？

卷健康监控包括两个部分：
* 外部卷健康监控控制器从控制器端监控卷健康。
* Kubelet 从节点端监控卷的健康状况。

有关详细信息，请参阅 [CSI 规约](https://github.com/container-storage-interface/spec/blob/master/spec.md)
和 [Kubernetes-CSI 驱动开发者指南](https://kubernetes-csi.github.io/docs/volume-health-monitor.html)。

[CSI 主机路径驱动程序](https://github.com/kubernetes-csi/csi-driver-host-path)中有一个卷健康的示例实现。

### 控制器端卷健康监控

要了解如何部署外部卷健康监控控制器，
请参阅 CSI 文档中的 [CSI external-health-monitor-controller](https://kubernetes-csi.github.io/docs/external-health-monitor-controller.html)。

如果检测到异常卷条件，
外部健康监视器控制器调用 `ListVolumes` 或者 `ControllerGetVolume` CSI RPC 并报送 VolumeConditionAbnormal 事件以及 PVC 上的消息。
只有具有 `LIST_VOLUMES` 和 `VOLUME_CONDITION` 控制器能力、
或者具有 `GET_VOLUME` 和 `VOLUME_CONDITION` 能力的 CSI 驱动程序才支持外部控制器中的卷健康监控。

要从控制器端实现卷健康功能，CSI 驱动程序**必须**添加对新控制器功能的支持。

如果 CSI 驱动程序支持 `LIST_VOLUMES` 和 `VOLUME_CONDITION` 控制器功能，它**必须**实现控制器 RPC `ListVolumes` 并在响应中报送卷状况。

如果 CSI 驱动程序支持 `GET_VOLUME` 和 `VOLUME_CONDITION` 控制器功能，它**必须**实现控制器 PRC `ControllerGetVolume` 并在响应中报送卷状况。

如果 CSI 驱动程序支持 `LIST_VOLUMES`、`GET_VOLUME` 和 `VOLUME_CONDITION` 控制器功能，则外部健康监视控制器将仅调用 `ListVolumes` CSI RPC。

### 节点侧卷健康监控

如果检测到异常的卷条件，
Kubelet 会调用 `NodeGetVolumeStats` CSI RPC 并报送 VolumeConditionAbnormal 事件以及 Pod 上的信息。
只有具有 `VOLUME_CONDITION` 节点功能的 CSI 驱动程序才支持 Kubelet 中的卷健康监控。

要从节点端实现卷健康功能，CSI 驱动程序**必须**添加对新节点功能的支持。

如果 CSI 驱动程序支持 `VOLUME_CONDITION` 节点能力，它**必须**在节点 RPC `NodeGetVoumeStats` 中报送卷状况。

## 下一步是什么？

根据反馈和采纳情况，Kubernetes 团队计划在 1.22 或 1.23 中将 CSI 卷健康实施推向 beta。

我们还在探索如何在 Kubernetes 中使用卷健康信息进行编程检测和自动协调。

## 如何了解更多？

要了解卷健康监控的设计细节，请阅读[卷健康监控](https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/1432-volume-health-monitor)增强提案。

卷健康检测控制器源代码位于：
[https://github.com/kubernetes-csi/external-health-monitor](https://github.com/kubernetes-csi/external-health-monitor)。

[容器存储接口文档](https://kubernetes-csi.github.io/docs/)中还有关于卷健康检查的更多详细信息。

## 如何参与？

[Kubernetes Slack 频道 #csi](https://kubernetes.slack.com/messages/csi)
和任何[标准 SIG Storage 通信频道](https://github.com/kubernetes/community/blob/master/sig-storage/README.md#contact)都是联系 SIG Storage 和 CSI 团队的绝佳媒介。

我们非常感谢在 1.21 中帮助发布此功能的贡献者。
我们要感谢 Yuquan Ren ([NickrenREN](https://github.com/nickrenren)) 在外部健康监控仓库中实现了初始卷健康监控控制器和代理，
感谢 Ran Xu ([fengzixu](https://github.com/fengzixu)) 在 1.21 中将卷健康监控逻辑从外部代理转移到 Kubelet，
我们特别感谢以下人员的深刻评论：
David Ashpole ([dashpole](https://github.com/dashpole))、
Michelle Au ([msau42](https://github.com/msau42))、
David Eads ([deads2k](https://github.com/deads2k))、
Elana Hashman ([ehashman](https://github.com/ehashman))、
Seth Jennings ([sjenning](https://github.com/sjenning)) 和 Jiawei Wang ([Jiawei0227](https://github.com/Jiawei0227))

那些有兴趣参与 CSI 或 Kubernetes 存储系统任何部分的设计和开发的人，
请加入 [Kubernetes Storage 特殊兴趣小组](https://github.com/kubernetes/community/tree/master/sig-storage)（SIG）。
我们正在迅速发展，并且欢迎新的贡献者。
