---
title: " Kubernetes 社区每周聚会笔记- 2015年4月24日 "
date: 2015-04-30
slug: weekly-kubernetes-community-hangout_29
---


每个星期，Kubernetes 贡献者社区几乎都会在谷歌 Hangouts 上聚会。我们希望任何对此感兴趣的人都能了解这个论坛的讨论内容。

日程安排：

* Flocker 和 Kubernetes 集成演示

笔记：

* flocker 和 kubernetes 集成演示
* * Flocker Q/A

    * 迁移后文件是否仍存在于node1上？

    * Brendan: 有没有计划把它做成一本书？我们不需要 powerstrip？

        * Luke:  需要找出感兴趣的来决定我们是否想让它成为 kube 中的一个一流的持久性磁盘提供商。

        * Brendan: 删除对 powerstrip 的需求会使其易于使用。完全去做。

        * Tim: 将它添加到 kubernetes 应该不超过45分钟:)


    * Derek: 持久卷和请求相比呢?

        * Luke: 除了基于 ZFS 的新后端之外，差别不大。使工作负载真正可移植。

        * Tim: 与基于网络的卷非常不同。有趣的是，它是唯一允许升级媒体的产品。

        * Brendan: 请求，它如何查找重复请求？Cassandra 希望在底层复制数据。向上和向下扩缩是有效的。根据负载动态地创建存储。它的步骤不仅仅是快照——通过编程使用预分配创建副本。

        * Tim: 帮助自动配置。


    * Brian: flocker 是否需要其他组件？

        * Kai: Flocker 控制服务与主服务器位于同一位置。(dia 在博客上)。Powerstrip + Powerstrip Flocker。对在 etcd 中持久化状态非常有趣。它保存关于每个卷的元数据。

        * Brendan: 在未来，flocker 可以是一个插件，我们将负责持久性。发布 v1.0。

        * Brian: 有兴趣为 flocker 等服务添加通用插件。

        * Luke: 当扩展到单个节点上的许多容器时，Zfs 会变得非常有价值。


    * Alex: flocker 服务可以作为 pod 运行吗？

        * Kai: 是的，唯一的要求是 flocker 控制服务应该能够与 zfs 代理对话。需要在主机上安装 zfs 代理，并且需要访问 zfs 二进制文件。

        * Brendan: 从理论上讲，所有 zfs 位都可以与设备一起放入容器中。

        * Luke: 是的，仍然在处理跨容器安装问题。

        * Tim: pmorie 正在通过它使 kubelet 在容器中工作。可能重复使用。

    * Kai: Cinder 支持即将到来。几天之后。
* Bob: 向 GKE 推送 kube 的过程是怎样的？需要更多的可见度。


