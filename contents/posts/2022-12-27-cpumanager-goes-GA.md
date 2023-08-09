---
layout: blog
title: 'Kubernetes v1.26：CPUManager 正式发布'
date: 2022-12-27
slug: cpumanager-ga
---

**作者：** Francesco Romani (Red Hat)

**译者：** Michael Yao (DaoCloud)

CPU 管理器是 kubelet 的一部分；kubelet 是 Kubernetes 的节点代理，能够让用户给容器分配独占 CPU。
CPU 管理器自从 Kubernetes v1.10 [进阶至 Beta](/blog/2018/07/24/feature-highlight-cpu-manager/)，
已证明了它本身的可靠性，能够充分胜任将独占 CPU 分配给容器，因此采用率稳步增长，
使其成为性能关键型和低延迟场景的基本组件。随着时间的推移，大多数变更均与错误修复或内部重构有关，
以下列出了几个值得关注、用户可见的变更：

- [支持显式保留 CPU](https://github.com/Kubernetes/Kubernetes/pull/83592)：
  之前已经可以请求为系统资源（包括 kubelet 本身）保留给定数量的 CPU，这些 CPU 将不会被用于独占 CPU 分配。
  现在还可以显式选择保留哪些 CPU，而不是让 kubelet 自动拣选 CPU。
- 使用 kubelet 本地
  [PodResources API](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources)
  [向容器报告独占分配的 CPU](https://github.com/Kubernetes/Kubernetes/pull/97415)，就像已为设备所做的一样。
- [优化系统资源的使用](https://github.com/Kubernetes/Kubernetes/pull/101771)，消除不必要的 sysfs 变更。

CPU 管理器达到了“能胜任”的水平，因此在 Kubernetes v1.26 中，它进阶至正式发布（GA）状态。

## CPU 管理器的自定义选项   {#cpu-managed-customization}

CPU 管理器支持两种操作模式，使用其**策略**进行配置。
使用 `none` 策略，CPU 管理器将 CPU 分配给容器，除了 Pod 规约中设置的（可选）配额外，没有任何特定限制。
使用 `static` 策略，假设 Pod 属于 Guaranteed QoS 类，并且该 Pod 中的每个容器都请求一个整数核数的 vCPU，
则 CPU 管理器将独占分配 CPU。独占分配意味着（无论是来自同一个 Pod 还是来自不同的 Pod）其他容器都不会被调度到该 CPU 上。

这种简单的操作模型很好地服务了用户群体，但随着 CPU 管理器越来越成熟，
用户开始关注更复杂的使用场景以及如何更好地支持这些使用场景。

社区没有添加更多策略，而是意识到几乎所有新颖的用例都是 `static` CPU 管理器策略所赋予的一些行为变化。
因此，决定添加[调整静态策略行为的选项](https://github.com/Kubernetes/enhancements/tree/master/keps/sig-node/2625-cpumanager-policies-thread-placement #proposed-change）。
这些选项都达到了不同程度的成熟度，类似于其他的所有 Kubernetes 特性，
为了能够被接受，每个新选项在禁用时都能提供向后兼容的行为，并能在需要进行交互时记录彼此如何交互。

这使得 Kubernetes 项目能够将 CPU 管理器核心组件和核心 CPU 分配算法进阶至 GA，同时也开启了该领域新的实验时代。
在 Kubernetes v1.26 中，CPU
管理器支持[三个不同的策略选项](/zh-cn/docs/tasks/administer-cluster/cpu-management-policies#static-policy-options)：

`full-pcpus-only`
: 将 CPU 管理器核心分配算法限制为仅支持完整的物理核心，从而减少允许共享核心的硬件技术带来的嘈杂邻居问题。

`distribute-cpus-across-numa`
: 驱动 CPU 管理器跨 NUMA 节点均匀分配 CPU，以应对需要多个 NUMA 节点来满足分配的情况。

`align-by-socket`
: 更改 CPU 管理器将 CPU 分配给容器的方式：考虑 CPU 按插槽而不是 NUMA 节点边界对齐。

## 后续发展   {#further-development}

在主要 CPU 管理器特性进阶后，每个现有的策略选项将遵循其进阶过程，独立于 CPU 管理器和其他选项。
添加新选项的空间虽然存在，但随着对更高灵活性的需求不断增长，CPU 管理器及其策略选项当前所提供的灵活性也有不足。

社区中正在讨论如何将 CPU 管理器和当前属于 kubelet 可执行文件的其他资源管理器拆分为可插拔的独立 kubelet 插件。
如果你对这项努力感兴趣，请加入 SIG Node 交流频道（Slack、邮件列表、每周会议）进行讨论。

## 进一步阅读  {#further-reading}

请查阅[控制节点上的 CPU 管理策略](/zh-cn/docs/tasks/administer-cluster/cpu-management-policies/)任务页面以了解有关
CPU 管理器的更多信息及其如何适配其他节点级别资源管理器。

## 参与其中  {#getting-involved}

此特性由 [SIG Node](https://github.com/Kubernetes/community/blob/master/sig-node/README.md) 社区驱动。
请加入我们与社区建立联系，就上述特性和更多内容分享你的想法和反馈。我们期待你的回音！
