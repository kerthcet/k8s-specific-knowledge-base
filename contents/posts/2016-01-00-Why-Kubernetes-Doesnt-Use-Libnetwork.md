---
title: " 为什么 Kubernetes 不用 libnetwork "
date: 2016-01-14
slug: why-kubernetes-doesnt-use-libnetwork
---



在 1.0 版本发布之前，Kubernetes 已经有了一个非常基础的网络插件形式-大约在引入 Docker’s [libnetwork](https://github.com/docker/libnetwork) 和 Container Network Model ([CNM](https://github.com/docker/libnetwork/blob/master/docs/design.md)) 的时候。与 libnetwork 不同，Kubernetes 插件系统仍然保留它的 'alpha' 名称。现在 Docker 的网络插件支持已经发布并得到支持，我们发现一个明显的问题是 Kubernetes 尚未采用它。毕竟，供应商几乎肯定会为 Docker 编写插件-我们最好还是用相同的驱动程序，对吧？


在进一步说明之前，重要的是记住 Kubernetes 是一个支持多种容器运行时的系统， Docker 只是其中之一。配置网络只是每一个运行时的一个方面，所以当人们问起“ Kubernetes 会支持CNM吗？”，他们真正的意思是“ Kubernetes 会支持 Docker 运行时的 CNM 驱动吗？”如果我们能够跨运行时实现通用的网络支持会很棒，但这不是一个明确的目标。


实际上， Kubernetes 还没有为 Docker 运行时采用 CNM/libnetwork 。事实上，我们一直在研究 CoreOS 提出的替代 Container Network Interface ([CNI](https://github.com/appc/cni/blob/master/SPEC.md)) 模型以及 App Container ([appc](https://github.com/appc)) 规范的一部分。为什么我们要这么做？有很多技术和非技术的原因。


首先，Docker 的网络驱动程序设计中存在一些基本假设，这些假设会给我们带来问题。


Docker 有一个“本地”和“全局”驱动程序的概念。本地驱动程序（例如 "bridge" ）以机器为中心，不进行任何跨节点协调。全局驱动程序（例如 "overlay" ）依赖于 [libkv](https://github.com/docker/libkv) （一个键值存储抽象库）来协调跨机器。这个键值存储是另一个插件接口，并且是非常低级的（键和值，没有其他含义）。 要在 Kubernetes 集群中运行类似 Docker's overlay 驱动程序，我们要么需要集群管理员来运行 [consul](https://github.com/hashicorp/consul), [etcd](https://github.com/coreos/etcd) 或 [zookeeper](https://zookeeper.apache.org/) 的整个不同实例 (see [multi-host networking](https://docs.docker.com/engine/userguide/networking/get-started-overlay/)) 否则我们必须提供我们自己的 libkv 实现，那被 Kubernetes 支持。


后者听起来很有吸引力，并且我们尝试实现它，但 libkv 接口是非常低级的，并且架构在内部定义为 Docker 。我们必须直接暴露我们的底层键值存储，或者提供键值语义（在我们的结构化API之上，它本身是在键值系统上实现的）。对于性能，可伸缩性和安全性原因，这些都不是很有吸引力。最终结果是，当使用 Docker 网络的目标是简化事情时，整个系统将显得更加复杂。


对于愿意并且能够运行必需的基础架构以满足 Docker 全局驱动程序并自己配置 Docker 的用户， Docker 网络应该“正常工作。” Kubernetes 不会妨碍这样的设置，无论项目的方向如何，该选项都应该可用。但是对于默认安装，实际的结论是这对用户来说是一个不应有的负担，因此我们不能使用 Docker 的全局驱动程序（包括 "overlay" ），这消除了使用 Docker 插件的很多价值。


Docker 的网络模型做出了许多对 Kubernetes 无效的假设。在 docker 1.8 和 1.9 版本中，它包含一个从根本上有缺陷的“发现”实现，导致容器中的 `/etc/hosts` 文件损坏 ([docker #17190](https://github.com/docker/docker/issues/17190)) - 并且这不容易被关闭。在 1.10 版本中，Docker 计划 [捆绑一个新的DNS服务器](https://github.com/docker/docker/issues/17195)，目前还不清楚是否可以关闭它。容器级命名不是 Kubernetes 的正确抽象 - 我们已经有了自己的服务命名，发现和绑定概念，并且我们已经有了自己的 DNS 模式和服务器（基于完善的 [SkyDNS](https://github.com/skynetservices/skydns) ）。捆绑的解决方案不足以满足我们的需求，但不能禁用。


与本地/全局拆分正交， Docker 具有进程内和进程外（ "remote" ）插件。我们调查了是否可以绕过 libnetwork （从而跳过上面的问题）并直接驱动 Docker remote 插件。不幸的是，这意味着我们无法使用任何 Docker 进程中的插件，特别是 "bridge" 和 "overlay"，这再次消除了 libnetwork 的大部分功能。


另一方面， CNI 在哲学上与 Kubernetes 更加一致。它比 CNM 简单得多，不需要守护进程，并且至少有合理的跨平台（ CoreOS 的 [rkt](https://coreos.com/rkt/docs/) 容器运行时支持它）。跨平台意味着有机会启用跨运行时（例如 Docker ， Rocket ， Hyper ）运行相同的网络配置。 它遵循 UNIX 的理念，即做好一件事。


此外，包装 CNI 插件并生成更加个性化的 CNI 插件是微不足道的 - 它可以通过简单的 shell 脚本完成。 CNM 在这方面要复杂得多。这使得 CNI 对于快速开发和迭代是有吸引力的选择。早期的原型已经证明，可以将 kubelet 中几乎 100％ 的当前硬编码网络逻辑弹出到插件中。


我们调查了为 Docker [编写 "bridge" CNM驱动程序](https://groups.google.com/g/kubernetes-sig-network/c/5MWRPxsURUw) 并运行 CNI 驱动程序。事实证明这非常复杂。首先， CNM 和 CNI 模型非常不同，因此没有一种“方法”协调一致。 我们仍然有上面讨论的全球与本地和键值问题。假设这个驱动程序会声明自己是本地的，我们必须从 Kubernetes 获取有关逻辑网络的信息。


不幸的是， Docker 驱动程序很难映射到像 Kubernetes 这样的其他控制平面。具体来说，驱动程序不会被告知连接容器的网络名称 - 只是 Docker 内部分配的 ID 。这使得驱动程序很难映射回另一个系统中存在的任何网络概念。


这个问题和其他问题已由网络供应商提出给 Docker 开发人员，并且通常关闭为“按预期工作”，([libnetwork #139](https://github.com/docker/libnetwork/issues/139), [libnetwork #486](https://github.com/docker/libnetwork/issues/486), [libnetwork #514](https://github.com/docker/libnetwork/pull/514), [libnetwork #865](https://github.com/docker/libnetwork/issues/865), [docker #18864](https://github.com/docker/docker/issues/18864))，即使它们使非 Docker 第三方系统更难以与之集成。在整个调查过程中， Docker 明确表示他们对偏离当前路线或委托控制的想法不太欢迎。这对我们来说非常令人担忧，因为 Kubernetes 补充了 Docker 并增加了很多功能，但它存在于 Docker 之外。


出于所有这些原因，我们选择投资 CNI 作为 Kubernetes 插件模型。这会有一些不幸的副作用。它们中的大多数都相对较小（例如， `docker inspect` 不会显示 IP 地址），特别是由 `docker run` 启动的容器可能无法与 Kubernetes 启动的容器通信，如果网络集成商想要与 Kubernetes 完全集成，则必须提供 CNI 驱动程序。但另一方面， Kubernetes 将变得更简单，更灵活，早期引入的许多丑陋的（例如配置 Docker 使用我们的网桥）将会消失。


当我们沿着这条道路前进时，我们会保持开放，以便更好地整合和简化。如果您对我们如何做到这一点有所想法，我们真的希望听到它们 - 在 [slack](http://slack.k8s.io/) 或者 [network SIG mailing-list](https://groups.google.com/g/kubernetes-sig-network) 找到我们。

Tim Hockin, Software Engineer, Google
