---
layout: blog
title: "聚焦 SIG Storage"
slug: sig-storage-spotlight
date: 2022-08-22
---

**作者**：Frederico Muñoz (SAS)

自 Kubernetes 诞生之初，持久数据以及如何解决有状态应用程序的需求一直是一个重要的话题。
对无状态部署的支持是很自然的、从一开始就存在的，并引起了人们的关注，变得众所周知。
从早期开始，我们也致力于更好地支持有状态应用程序，每个版本都增加了可以在 Kubernetes 上运行的范围。

消息队列、数据库、集群文件系统：这些是具有不同存储要求的解决方案的一些示例，
如今这些解决方案越来越多地部署在 Kubernetes 中。
处理来自许多不同供应商的临时和持久存储（本地或远程、文件或块），同时考虑如何提供用户期望的所需弹性和数据一致性，
所有这些都在 SIG Storage 的整体负责范围之内。

在这次 SIG Storage 采访报道中，[Frederico Muñoz](https://twitter.com/fredericomunoz)
（SAS 的云和架构负责人）与 VMware 技术负责人兼 SIG Storage 联合主席
[Xing Yang](https://twitter.com/2000xyang)，讨论了 SIG 的组织方式、当前的挑战是什么以及如何进行参与和贡献。

## 关于 SIG Storage

**Frederico (FSM)**：你好，感谢你给我这个机会了解更多关于 SIG Storage 的情况。
你能否介绍一下你自己、你的角色以及你是如何参与 SIG Storage 的。

**Xing Yang (XY)**：我是 VMware 的技术主管，从事云原生存储方面的工作。我也是 SIG Storage 的联合主席。
我从 2017 年底开始参与 K8s SIG Storage，开始为
[VolumeSnapshot](https://kubernetes.io/zh-cn/docs/concepts/storage/volume-snapshots/) 项目做贡献。
那时，VolumeSnapshot 项目仍处于实验性的 pre-alpha 阶段。它需要贡献者。所以我自愿提供帮助。
然后我与其他社区成员合作，在 2018 年的 K8s 1.12 版本中将 VolumeSnapshot 带入 Alpha，
2019 年在 K8s 1.17 版本中带入 Beta，并最终在 2020 年在 1.20 版本中带入 GA。

**FSM**：仅仅阅读 [SIG Storage 章程](https://github.com/kubernetes/community/blob/master/sig-storage/charter.md)
就可以看出，SIG Storage 涵盖了很多领域，你能描述一下 SIG 的组织方式吗？

**XY**：在 SIG Storage 中，有两位联合主席和两位技术主管。来自 Google 的 Saad Ali 和我是联合主席。
来自 Google 的 Michelle Au 和来自 Red Hat 的 Jan Šafránek 是技术主管。

我们每两周召开一次会议，讨论我们正在为每个特定版本开发的功能，获取状态，确保每个功能都有开发人员和审阅人员在处理它，
并提醒人们发布截止日期等。有关 SIG 的更多信息，请查阅[社区页面](https://github.com/kubernetes/community/tree/master/sig-storage)。
人们还可以将需要关注的 PR、需要讨论的设计提案和其他议题添加到会议议程文档中。
我们将在项目跟踪完成后对其进行审查。

我们还举行其他的定期会议，如 CSI 实施会议，Object Bucket API 设计会议，以及在需要时针对特定议题的一次性会议。
还有一个由 SIG Storage 和 SIG Apps 赞助的
[K8s 数据保护工作组](https://github.com/kubernetes/community/blob/master/wg-data-protection/README.md)。
SIG Storage 拥有或共同拥有数据保护工作组正在讨论的功能特性。

## 存储和 Kubernetes

**FSM**：存储是很多模块的基础组件，尤其是 Kubernetes：你认为 Kubernetes 在存储管理方面的具体挑战是什么?

**XY**：在 Kubernetes 中，卷操作涉及多个组件。例如，创建一个使用 PVC 的 Pod 涉及多个组件。
有 Attach Detach Controller 和 external-attacher 负责将 PVC 连接到 Pod。
还有 Kubelet 可以将 PVC 挂载到 Pod 上。当然，CSI 驱动程序也参与其中。
在多个组件之间进行协调时，有时可能会出现竞争状况。

另一个挑战是关于核心与 [Custom Resource Definitions](https://kubernetes.io/zh-cn/docs/concepts/extend-kubernetes/api-extension/custom-resources/)（CRD），
这并不是特定于存储的。CRD 是一种扩展 Kubernetes 功能的好方法，同时又不会向 Kubernetes 核心本身添加太多代码。
然而，这也意味着运行 Kubernetes 集群时需要许多外部组件。

在 SIG Storage 方面，一个最好的例子是卷快照。卷快照 API 被定义为 CRD。
API 定义和控制器是 out-of-tree。有一个通用的快照控制器和一个快照验证 Webhook
应该部署在控制平面上，类似于 kube-controller-manager 的部署方式。
虽然 Volume Snapshot 是一个 CRD，但它是 SIG Storage 的核心特性。
建议 K8s 集群发行版部署卷快照 CRD、快照控制器和快照验证 Webhook，然而，大多数时候我们没有看到发行版部署它们。
因此，这对存储供应商来说就成了一个问题：现在部署这些非驱动程序特定的通用组件成为他们的责任。
如果客户需要使用多个存储系统，且部署多个 CSI 驱动，可能会导致冲突。

**FSM**：不仅要考虑单个存储系统的复杂性，还要考虑它们在 Kubernetes 中如何一起使用？

**XY**：是的，有许多不同的存储系统可以为 Kubernetes 中的容器提供存储。它们的工作方式不同。找到适合所有人的解决方案是具有挑战性的。

**FSM**：Kubernetes 中的存储还涉及与外部解决方案的交互，可能比 Kubernetes 的其他部分更多。
这种与供应商和外部供应商的互动是否具有挑战性？它是否以任何方式随着时间而演变？

**XY**：是的，这绝对是具有挑战性的。最初 Kubernetes 存储具有 in-tree 卷插件接口。
多家存储供应商实现了 in-tree 接口，并在 Kubernetes 核心代码库中拥有卷插件。这引起了很多问题。
如果卷插件中存在错误，它会影响整个 Kubernetes 代码库。所有卷插件必须与 Kubernetes 一起发布。
如果存储供应商需要修复其插件中的错误或希望与他们自己的产品版本保持一致，这是不灵活的。

**FSM**：这就是 CSI 加入的原因？

**XY**：没错，接下来就是[容器存储接口](https://kubernetes-csi.github.io/docs/)（CSI）。
这是一个试图设计通用存储接口的行业标准，以便存储供应商可以编写一个插件并让它在一系列容器编排系统（CO）中工作。
现在 Kubernetes 是主要的 CO，但是在 CSI 刚开始的时候，除了 Kubernetes 之外，还有 Docker、Mesos、Cloud Foundry。
CSI 驱动程序是 out-of-tree 的，因此可以按照自己的节奏进行错误修复和发布。

与 in-tree 卷插件相比，CSI 绝对是一个很大的改进。CSI 的 Kubernetes
实现[自 1.13 版本以来](https://kubernetes.io/blog/2019/01/15/container-storage-interface-ga/)就达到 GA。
它已经发展了很长时间。SIG Storage 一直致力于将 in-tree 卷插件迁移到 out-of-tree 的 CSI 驱动，已经有几个版本了。

**FSM**：将驱动程序从 Kubernetes 主仓移到 CSI 中是一项重要的改进。

**XY**： CSI 接口是对 in-tree 卷插件接口的改进，但是仍然存在挑战。有很多存储系统。
目前在 [CSI 驱动程序文档中列出了 100 多个 CSI 驱动程序](https://kubernetes-csi.github.io/docs/drivers.html)。
这些存储系统也非常多样化。因此，很难设计一个适用于所有人的通用 API。
我们在 CSI 驱动层面引入了功能，但当同一驱动配置的卷具有不同的行为时，我们也会面临挑战。
前几天我们刚刚开会讨论每种卷 CSI 驱动程序功能。
当同一个驱动程序同时支持块卷和文件卷时，我们在区分某些 CSI 驱动程序功能时遇到了问题。
我们将召开后续会议来讨论这个问题。

## 持续的挑战

**FSM**：具体来说，对于 [1.25 版本](https://github.com/kubernetes/sig-release/tree/master/releases/release-1.25)
们可以看到管道中有一些与存储相关的 [KEPs](https://bit.ly/k8s125-enhancements)。
你是否认为这个版本对 SIG 特别重要？

**XY**：我不会说一个版本比其他版本更重要。在任何给定的版本中，我们都在做一些非常重要的事情。

**FSM**：确实如此，但你是否想指出 1.25 版本的特定特性和亮点呢？

**XY**：好的。对于 1.25 版本，我想强调以下几点：

* [CSI 迁移](https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/625-csi-migration)
  是一项持续的工作，SIG Storage 已经工作了几个版本了。目标是将 in-tree 卷插件移动到 out-of-tree 的
  CSI 驱动程序，并最终删除 in-tree 卷插件。在 1.25 版本中，有 7 个 KEP 与 CSI 迁移有关。
  有一个核心 KEP 用于通用的 CSI 迁移功能。它的目标是在 1.25 版本中达到 GA。
  GCE PD 和 AWS EBS 的 CSI 迁移以 GA 为目标。vSphere 的 CSI 迁移的目标是在默认情况下启用特性门控，
  在 1.25 版本中达到 Beta。Ceph RBD 和 PortWorx 的目标是达到 Beta，默认关闭特性门控。
  Ceph FS 的目标是达到 Alpha。

* 我要强调的第二个是 [COSI，容器对象存储接口](https://github.com/kubernetes-sigs/container-object-storage-interface-spec)。
  这是 SIG Storage 下的一个子项目。COSI 提出对象存储 Kubernetes API 来支持 Kubernetes 工作负载的对象存储操作的编排。
  它还为对象存储提供商引入了 gRPC 接口，以编写驱动程序来配置存储桶。COSI 团队已经在这个项目上工作两年多了。
  COSI 功能的目标是 1.25 版本中达到 Alpha。KEP 刚刚合入。COSI 团队正在根据更新后的 KEP 更新实现。

* 我要提到的另一个功能是 [CSI 临时卷](https://github.com/kubernetes/enhancements/issues/596)支持。
  此功能允许在临时用例的 Pod 规约中直接指定 CSI 卷。它们可用于使用已安装的卷直接在 Pod 内注入任意状态，
  例如配置、Secrets、身份、变量或类似信息。这最初是在 1.15 版本中作为一个 Alpha 功能引入的，现在它的目标是在 1.25 版本中达到 GA。

**FSM**：如果你必须单独列出一些内容，那么 SIG 正在研究的最紧迫的领域是什么?

**XY**：CSI 迁移绝对是 SIG 投入大量精力的领域之一，并且现在已经进行了多个版本。它还涉及来自多个云提供商和存储供应商的工作。

## 社区参与

**FSM**：Kubernetes 是一个社区驱动的项目。对任何希望参与 SIG Storage 工作的人有什么建议吗？他们应该从哪里开始？

**XY**：查看 [SIG Storage 社区页面](https://github.com/kubernetes/community/tree/master/sig-storage)，
它有很多关于如何开始的信息。[SIG 年度报告](https://github.com/kubernetes/community/blob/master/sig-storage/annual-report-2021.md)告诉你我们每年做了什么。
查看贡献指南。它有一些演示的链接，可以帮助你熟悉 Kubernetes 存储概念。

参加我们[在星期四举行的双周会议](https://github.com/kubernetes/community/tree/master/sig-storage#meetings)。
了解 SIG 的运作方式以及我们为每个版本所做的工作。找到你感兴趣的项目并提供贡献。
正如我之前提到的，我通过参与 Volume Snapshot 项目开始了 SIG Storage。

**FSM**：你有什么要补充的结束语吗？

**XY**：SIG Storage 总是欢迎新的贡献者。
我们需要贡献者来帮助构建新功能、修复错误、进行代码审查、编写测试、监控测试网格的健康状况以及改进文档等。

**FSM**：非常感谢你抽出宝贵时间让我们深入了解 SIG Storage！