---
title: 特定于节点的卷数限制
content_type: concept
weight: 90
---



此页面描述了各个云供应商可关联至一个节点的最大卷数。

谷歌、亚马逊和微软等云供应商通常对可以关联到节点的卷数量进行限制。
Kubernetes 需要尊重这些限制。 否则，在节点上调度的 Pod 可能会卡住去等待卷的关联。


## Kubernetes 的默认限制

The Kubernetes 调度器对关联于一个节点的卷数有默认限制：
<table>
  <tr><th>云服务</th><th>每节点最大卷数</th></tr>
  <tr><td><a href="https://aws.amazon.com/ebs/">Amazon Elastic Block Store (EBS)</a></td><td>39</td></tr>
  <tr><td><a href="https://cloud.google.com/persistent-disk/">Google Persistent Disk</a></td><td>16</td></tr>
  <tr><td><a href="https://azure.microsoft.com/en-us/services/storage/main-disks/">Microsoft Azure Disk Storage</a></td><td>16</td></tr>
</table>

## 自定义限制

你可以通过设置 `KUBE_MAX_PD_VOLS` 环境变量的值来设置这些限制，然后再启动调度器。
CSI 驱动程序可能具有不同的过程，关于如何自定义其限制请参阅相关文档。

如果设置的限制高于默认限制，请谨慎使用。请参阅云提供商的文档以确保节点可支持你设置的限制。

此限制应用于整个集群，所以它会影响所有节点。

## 动态卷限制

{{< feature-state state="stable" for_k8s_version="v1.17" >}}

以下卷类型支持动态卷限制。

- Amazon EBS
- Google Persistent Disk
- Azure Disk
- CSI

对于由内建插件管理的卷，Kubernetes 会自动确定节点类型并确保节点上可关联的卷数目合规。 例如：

* 在
<a href="https://cloud.google.com/compute/">Google Compute Engine</a>环境中,
[根据节点类型](https://cloud.google.com/compute/docs/disks/#pdnumberlimits)最多可以将127个卷关联到节点。

* 对于 M5、C5、R5、T3 和 Z1D 类型实例的 Amazon EBS 磁盘，Kubernetes 仅允许 25 个卷关联到节点。
对于 ec2 上的其他实例类型
<a href="https://aws.amazon.com/ec2/">Amazon Elastic Compute Cloud (EC2)</a>,
Kubernetes 允许 39 个卷关联至节点。

* 在 Azure 环境中, 根据节点类型，最多 64 个磁盘可以关联至一个节点。
更多详细信息，请参阅[Azure 虚拟机的数量大小](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes)。

* 如果 CSI 存储驱动程序（使用 `NodeGetInfo` ）为节点通告卷数上限，则 {{< glossary_tooltip text="kube-scheduler" term_id="kube-scheduler" >}} 将遵守该限制值。
参考 [CSI 规范](https://github.com/container-storage-interface/spec/blob/master/spec.md#nodegetinfo) 获取更多详细信息。

* 对于由已迁移到 CSI 驱动程序的树内插件管理的卷，最大卷数将是 CSI 驱动程序报告的卷数。


