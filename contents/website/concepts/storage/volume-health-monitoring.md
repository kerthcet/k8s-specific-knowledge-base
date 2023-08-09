---
title: 卷健康监测
content_type: concept
weight: 100
---


{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

{{< glossary_tooltip text="CSI" term_id="csi" >}} 卷健康监测支持 CSI 驱动从底层的存储系统着手，
探测异常的卷状态，并以事件的形式上报到 {{< glossary_tooltip text="PVCs" term_id="persistent-volume-claim" >}}
或 {{< glossary_tooltip text="Pods" term_id="pod" >}}.


## 卷健康监测 {#volume-health-monitoring}

Kubernetes _卷健康监测_ 是 Kubernetes 容器存储接口（CSI）实现的一部分。
卷健康监测特性由两个组件实现：外部健康监测控制器和 {{< glossary_tooltip term_id="kubelet" text="kubelet" >}}。

如果 CSI 驱动器通过控制器的方式支持卷健康监测特性，那么只要在 CSI 卷上监测到异常卷状态，就会在
{{< glossary_tooltip text="PersistentVolumeClaim" term_id="persistent-volume-claim" >}} (PVC)
中上报一个事件。

外部健康监测{{< glossary_tooltip text="控制器" term_id="controller" >}}也会监测节点失效事件。
如果要启动节点失效监测功能，你可以设置标志 `enable-node-watcher` 为 `true`。
当外部健康监测器检测到节点失效事件，控制器会报送一个事件，该事件会在 PVC 上继续上报，
以表明使用此 PVC 的 Pod 正位于一个失效的节点上。

如果 CSI 驱动程序支持节点测的卷健康检测，那当在 CSI 卷上检测到异常卷时，
会在使用该 PVC 的每个 Pod 上触发一个事件。
此外，卷运行状况信息作为 Kubelet VolumeStats 指标公开。
添加了一个新的指标 kubelet_volume_stats_health_status_abnormal。
该指标包括两个标签：`namespace` 和 `persistentvolumeclaim`。
计数为 1 或 0。1 表示卷不正常，0 表示卷正常。更多信息请访问[KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/1432-volume-health-monitor#kubelet-metrics-changes)。

{{< note >}}
你需要启用 `CSIVolumeHealth`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)，
才能在节点上使用此特性。
{{< /note >}}

## {{% heading "whatsnext" %}}

参阅 [CSI 驱动程序文档](https://kubernetes-csi.github.io/docs/drivers.html)，
可以找出有哪些 CSI 驱动程序实现了此特性。
