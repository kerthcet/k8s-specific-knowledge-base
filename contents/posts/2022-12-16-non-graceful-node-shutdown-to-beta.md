---
layout: blog
title: "Kubernetes 1.26: 节点非体面关闭进入 Beta 阶段"
date: 2022-12-16T10:00:00-08:00
slug: kubernetes-1-26-non-graceful-node-shutdown-beta
---


**作者：** Xing Yang (VMware), Ashutosh Kumar (VMware)

**译者：** Xin Li (DaoCloud)

Kubernetes v1.24 [引入](https://kubernetes.io/blog/2022/05/20/kubernetes-1-24-non-graceful-node-shutdown-alpha/)
了用于处理[节点非体面关闭](/zh-cn/docs/concepts/architecture/nodes/#non-graceful-node-shutdown)改进的
Alpha 质量实现。

## 什么是 Kubernetes 中的节点关闭

在 Kubernetes 集群中，节点可能会关闭。这可能在计划内发生，也可能意外发生。
你可能计划进行安全补丁或内核升级并需要重新启动节点，或者它可能由于 VM 实例抢占而关闭。
节点也可能由于硬件故障或软件问题而关闭。

要触发节点关闭，你可以在 shell 中运行 `shutdown` 或 `poweroff` 命令，或者按下按钮关闭机器电源。

下面分别介绍什么是节点体面关闭，什么是节点非体面关闭。

## 什么是节点**体面**关闭？

kubelet 对[节点体面关闭](/zh-cn/docs/concepts/architecture/nodes/#graceful-node-shutdown)
的处理在于允许 kubelet 检测节点关闭事件，正确终止该节点上的 Pod，并在实际关闭之前释放资源。
[关键 Pod](/zh-cn/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/#marking-pod-as-critical)
在所有常规 Pod 终止后终止，以确保应用程序的基本功能可以尽可能长时间地继续工作。

## 什么是节点**非体面**关闭？

仅当 kubelet 的**节点关闭管理器**可以检测到即将到来的节点关闭操作时，节点关闭才可能是体面的。
但是，在某些情况下，kubelet 不能检测到节点关闭操作。
这可能是因为 `shutdown` 命令没有触发 Linux 上 kubelet 使用的 [Inhibitor Locks](https://www.freedesktop.org/wiki/Software/systemd/inhibit)
机制，或者是因为用户的失误导致。
例如，如果该节点的 `shutdownGracePeriod` 和 `shutdownGracePeriodCriticalPods` 详细信息配置不正确。

当一个节点关闭（或崩溃），并且 kubelet 节点关闭管理器**没有**检测到该关闭时，
就出现了非体面的节点关闭。节点非体面关闭对于有状态应用程序而言是一个问题。
如果节点以非正常方式关闭且节点上存在属于某 StatefulSet 的 Pod，
则该 Pod 将被无限期地阻滞在 `Terminating` 状态，并且控制平面无法在健康节点上为该 StatefulSet 创建替代 Pod。
你可以手动删除失败的 Pod，但这对于集群自愈来说并不是理想状态。
同样，作为 Deployment 的一部分创建的 ReplicaSet 中的 Pod 也将滞留在 `Terminating` 状态，
对于绑定到正在被关闭的节点上的其他 Pod，也将无限期地处于 `Terminating` 状态。
如果你设置了水平缩放限制，即使那些处于终止过程中的 Pod 也会被计入该限制，
因此如果你的工作负载已经达到最大缩放比例，则它可能难以自我修复。
（顺便说一句：如果非体面关闭的节点重新启动，kubelet 确实会删除旧的 Pod，并且控制平面可以进行替换。）


## Beta 阶段带来的新功能
在 Kubernetes v1.26 中，非体面节点关闭特性是 Beta 版，默认被启用。
`NodeOutOfServiceVolumeDetach` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)在
`kube-controller-manager` 中从可选启用变成默认启用。如果需要，
你仍然可以选择禁用此特性（也请提交一个 issue 来解释问题）。

在检测方面，kub​​e-controller-manager 报告了两个新指标。

`force_delete_pods_total`：被强制删除的 Pod 数（在 Pod 垃圾收集控制器重启时重置）

`force_delete_pod_errors_total`：尝试强制删除 Pod 时遇到的错误数（也会在 Pod 垃圾收集控制器重启时重置）

## 它是如何工作的？

在节点关闭的情况下，如果正常关闭不起作用或节点由于硬件故障或操作系统损坏而处于不可恢复状态，
你可以在 Node 上手动添加 `out-of-service` 污点。
例如，污点可以是 `node.kubernetes.io/out-of-service=nodeshutdown:NoExecute` 或
`node.kubernetes.io/out-of-service=nodeshutdown:NoSchedule`。
如果 Pod 上没有与之匹配的容忍规则，则此污点会触发节点上的 Pod 被强制删除。
附加到关闭中的节点的持久卷将被分离，新的 Pod 将在不同的运行节点上成功创建。

```
kubectl taint nodes <node-name> node.kubernetes.io/out-of-service=nodeshutdown:NoExecute
```

**注意**：在应用 out-of-service 污点之前，你必须验证节点是否已经处于关闭或断电状态（而不是在重新启动中），
要么是因为用户有意关闭它，要么是由于硬件故障或操作系统问题等导致节点关闭。

与 out-of-service 节点有关联的所有工作负载的 Pod 都被移动到新的运行节点，
并且所关闭的节点已恢复之后，你应该删除受影响节点上的污点。

## 接下来

根据反馈和采用情况，Kubernetes 团队计划在 1.27 或 1.28 中将非体面节点关闭实现推向正式发布（GA）状态。

此功能需要用户手动向节点添加污点以触发工作负载的故障转移并在节点恢复后删除污点。

如果有一种编程方式可以确定节点确实关闭并且节点和存储之间没有 IO，
则集群操作员可以通过自动应用 `out-of-service` 污点来自动执行此过程。

在工作负载成功转移到另一个正在运行的节点并且曾关闭的节点已恢复后，集群操作员可以自动删除污点。

将来，我们计划寻找方法来自动检测来隔离已关闭或处于不可恢复状态的节点，
并将其工作负载故障转移到另一个节点。

## 如何学习更多？

要了解更多信息，请阅读 Kubernetes 文档中的[非体面节点关闭](/zh-cn/docs/concepts/architecture/nodes/#non-graceful-node-shutdown)。

## 如何参与

我们非常感谢所有帮助设计、实施和审查此功能的贡献者：

* Michelle Au ([msau42](https://github.com/msau42)) 
* Derek Carr ([derekwaynecarr](https://github.com/derekwaynecarr))
* Danielle Endocrimes ([endocrimes](https://github.com/endocrimes)) 
* Tim Hockin  ([thockin](https://github.com/thockin))
* Ashutosh Kumar ([sonasingh46](https://github.com/sonasingh46)) 
* Hemant Kumar ([gnufied](https://github.com/gnufied))
* Yuiko Mouri([YuikoTakada](https://github.com/YuikoTakada))
* Mrunal Patel ([mrunalp](https://github.com/mrunalp))
* David Porter ([bobbypage](https://github.com/bobbypage))
* Yassine Tijani ([yastij](https://github.com/yastij)) 
* Jing Xu ([jingxu97](https://github.com/jingxu97))
* Xing Yang ([xing-yang](https://github.com/xing-yang))

一路上有很多人帮助审阅了设计和实现。我们要感谢为这项工作做出贡献的所有人，包括在过去几年中审查
[KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/2268-non-graceful-shutdown)
和实现的大约 30 人。

此功能是 SIG Storage 和 SIG Node 之间的协作。对于那些有兴趣参与 Kubernetes
存储系统任何部分的设计和开发的人，请加入 Kubernetes 存储特别兴趣小组 (SIG)。
对于那些有兴趣参与支持 Pod 和主机资源之间受控交互的组件的设计和开发，请加入 Kubernetes Node SIG。

