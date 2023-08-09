---
layout: blog
title: "Kubernetes 1.24：卷扩充现在成为稳定功能"
date: 2022-05-05
slug: volume-expansion-ga
---


**作者：** Hemant Kumar (Red Hat)

卷扩充在 Kubernetes 1.8 作为 Alpha 功能引入，
在 Kubernetes 1.11 进入了 Beta 阶段。
在 Kubernetes 1.24 中，我们很高兴地宣布卷扩充正式发布（GA）。

此功能允许 Kubernetes 用户简单地编辑其 `PersistentVolumeClaim` 对象，
并在 PVC Spec 中指定新的大小，Kubernetes 将使用存储后端自动扩充卷，
同时也会扩充 Pod 使用的底层文件系统，使得无需任何停机时间成为可能。
### 如何使用卷扩充

通过编辑 PVC 的 `spec` 字段，指定不同的（和更大的）存储请求，
可以触发 PersistentVolume 的扩充。
例如，给定以下 PVC：

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi # 在此处指定新的大小
```
你可以指定新的值来替代旧的 `1Gi` 大小来请求扩充下层 PersistentVolume。
一旦你更改了请求的大小，可以查看 PVC 的 `status.conditions` 字段，
确认卷大小的调整是否已完成。

当 Kubernetes 开始扩充卷时，它会给 PVC 添加 `Resizing` 状况。
一旦扩充结束，这个状况会被移除。通过监控与 PVC 关联的事件，
还可以获得更多关于扩充操作进度的信息：

```bash
kubectl describe pvc <pvc>
```
### 存储驱动支持

然而，并不是每种卷类型都默认支持扩充。
某些卷类型（如树内 hostpath 卷）不支持扩充。
对于 CSI 卷，
CSI 驱动必须在控制器或节点服务（如果合适，二者兼备）
中具有 `EXPAND_VOLUME` 能力。
请参阅 CSI 驱动的文档，了解其是否支持卷扩充。

有关支持卷扩充的树内（intree）卷类型，
请参阅卷扩充文档：[扩充 PVC 申领](/zh-cn/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims)。

通常，为了对可扩充的卷提供某种程度的控制，
只有在存储类将 `allowVolumeExpansion` 参数设置为 `true` 时，
动态供应的 PVC 才是可扩充的。

Kubernetes 集群管理员必须编辑相应的 StorageClass 对象，
并将 `allowVolumeExpansion` 字段设置为 `true`。例如：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp2-default
provisioner: kubernetes.io/aws-ebs
parameters:
  secretNamespace: ""
  secretName: ""
allowVolumeExpansion: true
```
### 在线扩充与离线扩充比较

默认情况下，Kubernetes 会在用户请求调整大小后立即尝试扩充卷。
如果一个或多个 Pod 正在使用该卷，
Kubernetes 会尝试通过在线调整大小来扩充该卷；
因此，卷扩充通常不需要应用停机。
节点上的文件系统也可以在线扩充，因此不需要关闭任何正在使用 PVC 的 Pod。

如果要扩充的 PersistentVolume 未被使用，Kubernetes 会用离线方式调整卷大小
（而且，由于该卷未使用，所以也不会造成工作负载中断）。
但在某些情况下，如果底层存储驱动只能支持离线扩充，
则 PVC 用户必须先停止 Pod，才能让扩充成功。
请参阅存储提供商的文档，了解其支持哪种模式的卷扩充。

当卷扩充作为 Alpha 功能引入时，
Kubernetes 仅支持在节点上进行离线的文件系统扩充，
因此需要用户重新启动 Pod，才能完成文件系统的大小调整。
今天，用户的行为已经被改变，无论底层 PersistentVolume 是在线还是离线，
Kubernetes 都会尽最大努力满足任何调整大小的请求。
如果你的存储提供商支持在线扩充，则无需重启 Pod 即可完成卷扩充。
## 下一步

尽管卷扩充在最近的 v1.24 发行版中成为了稳定版本，
但 SIG Storage 团队仍然在努力让 Kubernetes 用户扩充其持久性存储变得更简单。
Kubernetes 1.23 引入了卷扩充失败后触发恢复机制的功能特性，
允许用户在大小调整失败后尝试自助修复。
更多详细信息，请参阅[处理扩充卷过程中的失败](/zh-cn/docs/concepts/storage/persistent-volumes/#recovering-from-failure-when-expanding-volumes)。
Kubernetes 贡献者社区也在讨论有状态（StatefulSet）驱动的存储扩充的潜力。
这个提议的功能特性将允许用户通过直接编辑 StatefulSet 对象，
触发为 StatefulSet 提供存储的所有底层 PV 的扩充。
更多详细信息，请参阅[通过 StatefulSet 支持卷扩充](https://github.com/kubernetes/enhancements/issues/661)的改善提议。
