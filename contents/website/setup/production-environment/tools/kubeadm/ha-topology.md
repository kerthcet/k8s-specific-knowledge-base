---
title: 高可用拓扑选项
content_type: concept
weight: 50
---


本页面介绍了配置高可用（HA）Kubernetes 集群拓扑的两个选项。

你可以设置 HA 集群：

- 使用堆叠（stacked）控制平面节点，其中 etcd 节点与控制平面节点共存
- 使用外部 etcd 节点，其中 etcd 在与控制平面不同的节点上运行

在设置 HA 集群之前，你应该仔细考虑每种拓扑的优缺点。

{{< note >}}
kubeadm 静态引导 etcd 集群。
阅读 etcd [集群指南](https://github.com/etcd-io/etcd/blob/release-3.4/Documentation/op-guide/clustering.md#static)以获得更多详细信息。
{{< /note >}}


## 堆叠（Stacked）etcd 拓扑    {#stacked-etcd-topology}

堆叠（Stacked）HA 集群是一种这样的[拓扑](https://zh.wikipedia.org/wiki/%E7%BD%91%E7%BB%9C%E6%8B%93%E6%89%91)，
其中 etcd 分布式数据存储集群堆叠在 kubeadm 管理的控制平面节点上，作为控制平面的一个组件运行。

每个控制平面节点运行 `kube-apiserver`、`kube-scheduler` 和 `kube-controller-manager` 实例。
`kube-apiserver` 使用负载均衡器暴露给工作节点。

每个控制平面节点创建一个本地 etcd 成员（member），这个 etcd 成员只与该节点的 `kube-apiserver` 通信。
这同样适用于本地 `kube-controller-manager` 和 `kube-scheduler` 实例。

这种拓扑将控制平面和 etcd 成员耦合在同一节点上。相对使用外部 etcd 集群，
设置起来更简单，而且更易于副本管理。

然而，堆叠集群存在耦合失败的风险。如果一个节点发生故障，则 etcd 成员和控制平面实例都将丢失，
并且冗余会受到影响。你可以通过添加更多控制平面节点来降低此风险。

因此，你应该为 HA 集群运行至少三个堆叠的控制平面节点。

这是 kubeadm 中的默认拓扑。当使用 `kubeadm init` 和 `kubeadm join --control-plane` 时，
在控制平面节点上会自动创建本地 etcd 成员。

![堆叠的 etcd 拓扑](/zh-cn/docs/images/kubeadm-ha-topology-stacked-etcd.svg)

## 外部 etcd 拓扑    {#external-etcd-topology}

具有外部 etcd 的 HA 集群是一种这样的[拓扑](https://zh.wikipedia.org/wiki/%E7%BD%91%E7%BB%9C%E6%8B%93%E6%89%91)，
其中 etcd 分布式数据存储集群在独立于控制平面节点的其他节点上运行。

就像堆叠的 etcd 拓扑一样，外部 etcd 拓扑中的每个控制平面节点都会运行
`kube-apiserver`、`kube-scheduler` 和 `kube-controller-manager` 实例。
同样，`kube-apiserver` 使用负载均衡器暴露给工作节点。但是 etcd 成员在不同的主机上运行，
每个 etcd 主机与每个控制平面节点的 `kube-apiserver` 通信。

这种拓扑结构解耦了控制平面和 etcd 成员。因此它提供了一种 HA 设置，
其中失去控制平面实例或者 etcd 成员的影响较小，并且不会像堆叠的 HA 拓扑那样影响集群冗余。

但此拓扑需要两倍于堆叠 HA 拓扑的主机数量。
具有此拓扑的 HA 集群至少需要三个用于控制平面节点的主机和三个用于 etcd 节点的主机。

![外部 etcd 拓扑](/zh-cn/docs/images/kubeadm-ha-topology-external-etcd.svg)

## {{% heading "whatsnext" %}}

- [使用 kubeadm 设置高可用集群](/zh-cn/docs/setup/production-environment/tools/kubeadm/high-availability/)
