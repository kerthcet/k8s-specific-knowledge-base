---
layout: blog
title: 'Kubernetes 1.14 稳定性改进中的进程ID限制'
date: 2019-04-15
slug: process-id-limiting-for-stability-improvements-in-kubernetes-1.14
---

**作者: Derek Carr**

你是否见过有人拿走了比属于他们那一份更多的饼干？ 一个人走过来，抓起半打新鲜烤制的大块巧克力饼干然后匆匆离去，就像饼干怪兽大喊 “Om nom nom nom”。

在一些罕见的工作负载中，Kubernetes 集群内部也发生了类似的情况。每个 Pod 和 Node 都有有限数量的可能的进程 ID（PID），供所有应用程序共享。尽管很少有进程或 Pod 能够进入并获取所有 PID，但由于这种行为，一些用户会遇到资源匮乏的情况。 因此，在 Kubernetes 1.14 中，我们引入了一项增强功能，以降低单个  Pod 垄断所有可用 PID 的风险。


## 你能预留一些 PIDs 吗？

在这里，我们谈论的是某些容器的贪婪性。 在理想情况之外，失控进程有时会发生，特别是在测试集群中。 因此，在这些集群中会发生一些混乱的非生产环境准备就绪的事情。

在这种情况下，可能会在节点内部发生类似于 fork 炸弹耗尽 PID 的攻击。随着资源的缓慢腐蚀，被一些不断产生子进程的僵尸般的进程所接管，其他正常的工作负载会因为这些像气球般不断膨胀的浪费的处理能力而开始受到冲击。这可能导致同一 Pod 上的其他进程缺少所需的 PID。这也可能导致有趣的副作用，因为节点可能会发生故障，并且该Pod的副本将安排到新的机器上，至此，该过程将在整个集群中重复进行。

## 解决问题

因此，在 Kubernetes 1.14 中，我们添加了一个特性，允许通过配置 kubelet，限制给定 Pod 可以消耗的 PID 数量。如果该机器支持 32768 个 PIDs 和 100 个 Pod，则可以为每个 Pod 提供 300 个 PIDs 的预算，以防止 PIDs 完全耗尽。如果管理员想要像 CPU 或内存那样过度使用 PIDs，那么他们也可以配置超额使用，但是这样会有一些额外风险。不管怎样，没有一个Pod能搞坏整个机器。这通常会防止简单的分叉函数炸弹接管你的集群。

此更改允许管理员保护一个 Pod 不受另一个 Pod 的影响，但不能确保计算机上的所有 Pod 都能保护节点和节点代理本身不受影响。因此，我们在这个版本中以 Alpha 的形式引入了这个一个特性，它提供了 PIDs 在节点代理（ kubelet、runtime 等）与 Pod 上的最终用户工作负载的分离。管理员可以预定特定数量的 pid（类似于今天如何预定 CPU 或内存），并确保它们不会被该计算机上的 pod 消耗。一旦从 Alpha 进入到 Beta，然后在将来的 Kubernetes 版本中稳定下来，我们就可以使用这个特性防止 Linux 资源耗尽。

开始使用 [Kubernetes 1.14](https://github.com/Kubernetes/Kubernetes/releases/tag/v1.14.0)。
##参与其中

如果您对此特性有反馈或有兴趣参与其设计与开发，请加入[节点特别兴趣小组](https://github.com/kubernetes/community/tree/master/sig Node)。

###关于作者：
Derek Carr 是 Red Hat 高级首席软件工程师。他也是 Kubernetes 的贡献者和 Kubernetes 社区指导委员会的成员。
