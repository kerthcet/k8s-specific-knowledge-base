---
title: " Kubernetes 社区每周聚会笔记- 2015年5月1日 "
date: 2015-05-11
slug: weekly-kubernetes-community-hangout
---

每个星期，Kubernetes 贡献者社区几乎都会在谷歌 Hangouts 上聚会。我们希望任何对此感兴趣的人都能了解这个论坛的讨论内容。


* 简单的滚动更新 - Brendan

    * 滚动更新 = RCs和Pods很好的例子。

    * ...pause… (Brendan 需要 Kelsey 的演示恢复技巧)

    * 滚动更新具有恢复功能:取消更新并重新启动，更新从停止的地方继续。

    * 新控制器获取旧控制器的名称，因此外观是纯粹的更新。

    * 还可以在 update 中命名版本(最后不会重命名)。


* Rocket 演示 - CoreOS 的伙计们

    * Rocket 和 docker 之间的主要区别: Rocket 是无守护进程和以 pod 为中心。。

    * Rocket 具有原生的 AppContainer 格式，但也支持 docker 镜像格式。

    * 可以在同一个 pod 中运行 AppContainer 和 docker 容器。

    * 变更接近于合并。


* 演示 service accounts 和 secrets 被添加到 pod - Jordan

    * 问题：很难获得与API通信的令牌。

    * 新的API对象："ServiceAccount"

    * ServiceAccount 是命名空间，控制器确保命名空间中至少存在一个个默认 service account。

    * 键入 "ServiceAccountToken"，控制器确保至少有一个默认令牌。

    * 演示

    *     * 可以使用 ServiceAccountToken 创建新的 service account。控制器将为它创建令牌。

    * 可以创建一个带有 service account 的 pod, pod 将在 /var/run/secrets/kubernetes.io/…


* Kubelet 在容器中运行 - Paul

    * Kubelet 成功地运行了带有 secret 的 pod。

