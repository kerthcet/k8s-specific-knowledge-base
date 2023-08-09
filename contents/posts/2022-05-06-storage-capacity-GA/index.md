---
layout: blog
title: "Kubernetes 1.24 版本中存储容量跟踪特性进入 GA 阶段"
date: 2022-05-06
slug: storage-capacity-ga
---

 **作者:** Patrick Ohly（Intel）

在 Kubernetes v1.24 版本中，[存储容量](/zh-cn/docs/concepts/storage/storage-capacity/)跟踪已经成为一项正式发布的功能。

## 已经解决的问题

如[上一篇关于此功能的博文](/blog/2021/04/14/local-storage-features-go-beta/)中所详细介绍的，
存储容量跟踪允许 CSI 驱动程序发布有关剩余容量的信息。当 Pod 仍然有需要配置的卷时，
kube-scheduler 使用该信息为 Pod 选择合适的节点。

如果没有这些信息，Pod 可能会被卡住，而不会被调度到合适节点，这是因为 kube-scheduler
只能盲目地选择节点。由于 CSI 驱动程序管理的下层存储系统没有足够的容量，
kube-scheduler 常常会选择一个无法为其配置卷的节点。

因为 CSI 驱动程序发布的这些存储容量信息在被使用的时候可能已经不是最新的信息了，
所以最终选择的节点无法正常工作的情况仍然可能会发生。
卷配置通过通知调度程序需要在其他节点上重试来恢复。

升级到 GA 版本后重新进行的[负载测试](https://github.com/kubernetes-csi/csi-driver-host-path/blob/master/docs/storage-capacity-tracking.md)证实，
集群中部署了存储容量跟踪功能的 Pod 可以使用所有的存储，而没有部署此功能的 Pod 就会被卡住。

## *尚未*解决的问题

如果尝试恢复一个制备失败的卷，存在一个已知的限制：
如果 Pod 使用两个卷并且只能制备其中一个，那么所有将来的调度决策都受到已经制备的卷的限制。
如果该卷是节点的本地卷，并且另一个卷无法被制备，则 Pod 会卡住。
此问题早在存储容量跟踪功能之前就存在，虽然苛刻的附加条件使这种情况不太可能发生，
但是无法完全避免，当然每个 Pod 仅使用一个卷的情况除外。

[KEP 草案](https://github.com/kubernetes/enhancements/pull/1703)中提出了一个解决此问题的想法：
已制备但尚未被使用的卷不能包含任何有价值的数据，因此可以在其他地方释放并且再次被制备。
SIG Storage 正在寻找对此感兴趣并且愿意继续从事此工作的开发人员。

另一个没有解决的问题是 Cluster Autoscaler 对包含卷的 Pod 的支持。
对于具有存储容量跟踪功能的 CSI 驱动程序，我们开发了一个原型并在此
[PR](https://github.com/kubernetes/autoscaler/pull/3887) 中进行了讨论。
此原型旨在与任意 CSI 驱动程序协同工作，但这种灵活性使其难以配置并减慢了扩展操作：
因为自动扩展程序无法模拟卷制备操作，它一次只能将集群扩展一个节点，这是此方案的不足之处。

因此，这个 PR 没有被合入，需要另一种不同的方法，在自动缩放器和 CSI 驱动程序之间实现更紧密的耦合。
为此，需要更好地了解哪些本地存储 CSI 驱动程序与集群自动缩放结合使用。如果这会引出新的 KEP，
那么用户将不得不在实践中尝试实现，然后才能迁移到 beta 版本或 GA 版本中。
如果你对此主题感兴趣，请联系 SIG Storage。

## 致谢

非常感谢为此功能做出贡献或提供反馈的 [SIG Scheduling](https://github.com/kubernetes/community/tree/master/sig-scheduling)、
[SIG Autoscaling](https://github.com/kubernetes/community/tree/master/sig-autoscaling) 
和 [SIG Storage](https://github.com/kubernetes/community/tree/master/sig-storage) 成员！
