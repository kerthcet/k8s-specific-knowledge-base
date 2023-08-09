---
layout: blog
title: "Kubernetes 的 iptables 链不是 API"
date: 2022-09-07
slug: iptables-chains-not-api
---


**作者：** Dan Winship (Red Hat)

**译者：** Xin Li (DaoCloud)

一些 Kubernetes 组件（例如 kubelet 和 kube-proxy）在执行操作时，会创建特定的 iptables 链和规则。
这些链从未被计划使其成为任何 Kubernetes API/ABI 保证的一部分，
但一些外部组件仍然使用其中的一些链（特别是使用 `KUBE-MARK-MASQ` 将数据包标记为需要伪装）。

作为 v1.25 版本的一部分，SIG Network 明确声明：
Kubernetes 创建的 iptables 链仅供 Kubernetes 内部使用（有一个例外），
第三方组件不应假定 Kubernetes 会创建任何特定的 iptables 链，
或者这些链将包含任何特定的规则（即使它们确实存在）。

然后，在未来的版本中，作为 [KEP-3178] 的一部分，我们将开始逐步淘汰 Kubernetes
本身不再需要的某些链。Kubernetes 自身之外且使用了 `KUBE-MARK-MASQ`、`KUBE-MARK-DROP`
或 Kubernetes 所生成的其它 iptables 链的组件应当开始迁移。

[KEP-3178]: https://github.com/kubernetes/enhancements/issues/3178

## 背景   {#background}

除了各种为 Service 创建的 iptables 链之外，kube-proxy 还创建了某些通用 iptables 链，
用作服务代理的一部分。 过去，kubelet 还使用 iptables
来实现一些功能（例如为 Pod 设置 `hostPort` 映射），因此它也冗余地创建了一些重复的链。

然而，随着 1.24 版本 Kubernetes 中 [dockershim 的移除]，
kubelet 现在不再为某种目的使用任何 iptables 规则；
过去使用 iptables 来完成的事情现在总是由容器运行时或网络插件负责，
现在 kubelet 没有理由创建任何 iptables 规则。

同时，虽然 iptables 仍然是 Linux 上默认的 kube-proxy 后端，
但它不会永远是默认选项，因为相关的命令行工具和内核 API 基本上已被弃用，
并且不再得到改进。（RHEL 9 [记录警告] 如果你使用 iptables API，即使是通过 `iptables-nft`。）

尽管在 Kubernetes 1.25，iptables kube-proxy 仍然很流行，
并且 kubelet 继续创建它过去创建的 iptables 规则（尽管不再**使用**它们），
第三方软件不能假设核心 Kubernetes 组件将来会继续创建这些规则。

[移除 dockershim]: https://kubernetes.io/zh-cn/blog/2022/02/17/dockershim-faq/
[记录警告]: https://access.redhat.com/solutions/6739041

## 即将发生的变化

从现在开始的几个版本中，kubelet 将不再在 `nat` 表中创建以下 iptables 链：

  - `KUBE-MARK-DROP`
  - `KUBE-MARK-MASQ`
  - `KUBE-POSTROUTING`

此外，`filter` 表中的 `KUBE-FIREWALL` 链将不再具有当前与
`KUBE-MARK-DROP` 关联的功能（并且它最终可能会完全消失）。

此更改将通过 `IPTablesOwnershipCleanup` 特性门控逐步实施。
你可以手动在 Kubernetes 1.25 中开启此特性进行测试。
目前的计划是将其在 Kubernetes 1.27 中默认启用，
尽管这可能会延迟到以后的版本。（不会在 Kubernetes 1.27 版本之前调整。）

## 如果你使用 Kubernetes 的 iptables 链怎么办

（尽管下面的讨论侧重于仍然基于 iptables 的短期修复，
但你可能也应该开始考虑最终迁移到 nftables 或其他 API。）

### 如果你使用 `KUBE-MARK-MASQ` 链...  {#use-case-kube-mark-drop}

如果你正在使用 `KUBE-MARK-MASQ` 链来伪装数据包，
你有两个选择：（1）重写你的规则以直接使用 `-j MASQUERADE`，
（2）创建你自己的替代链，完成“为伪装而设标记”的任务。

kube-proxy 使用 `KUBE-MARK-MASQ` 的原因是因为在很多情况下它需要在数据包上同时调用 
`-j DNAT` 和 `-j MASQUERADE`，但不可能同时在 iptables 中调用这两种方法；
`DNAT` 必须从 `PREROUTING`（或 `OUTPUT`）链中调用（因为它可能会改变数据包将被路由到的位置）而
`MASQUERADE` 必须从 `POSTROUTING` 中调用（因为它伪装的源 IP 地址取决于最终的路由）。

理论上，kube-proxy 可以有一组规则来匹配 `PREROUTING`/`OUTPUT`
中的数据包并调用 `-j DNAT`，然后有第二组规则来匹配 `POSTROUTING`
中的相同数据包并调用 `-j MASQUERADE`。
但是，为了提高效率，kube-proxy 只匹配了一次，在 `PREROUTING`/`OUTPUT` 期间调用 `-j DNAT`，
然后调用 `-j KUBE-MARK-MASQ` 在内核数据包标记属性上设置一个比特，作为对自身的提醒。
然后，在 `POSTROUTING` 期间，通过一条规则来匹配所有先前标记的数据包，并对它们调用 `-j MASQUERADE`。

如果你有**很多**规则需要像 kube-proxy 一样对同一个数据包同时执行 DNAT 和伪装操作，
那么你可能需要类似的安排。但在许多情况下，使用 `KUBE-MARK-MASQ` 的组件之所以这样做，
只是因为它们复制了 kube-proxy 的行为，而不理解 kube-proxy 为何这样做。
许多这些组件可以很容易地重写为仅使用单独的 DNAT 和伪装规则。
（在没有发生 DNAT 的情况下，使用 `KUBE-MARK-MASQ` 的意义就更小了；
只需将你的规则从 `PREROUTING` 移至 `POSTROUTING` 并直接调用 `-j MASQUERADE`。）

### 如果你使用 `KUBE-MARK-DROP`... {#use-case-kube-mark-drop}

`KUBE-MARK-DROP` 的基本原理与 `KUBE-MARK-MASQ` 类似：
kube-proxy 想要在 `nat` `KUBE-SERVICES` 链中做出丢包决定以及其他决定，
但你只能从 `filter` 表中调用 `-j DROP`。

通常，删除对 `KUBE-MARK-DROP` 的依赖的方法与删除对 `KUBE-MARK-MASQ` 的依赖的方法相同。
在 kube-proxy 的场景中，很容易将 `nat` 表中的 `KUBE-MARK-DROP`
的用法替换为直接调用 `filter` 表中的 `DROP`，因为 DNAT 规则和 DROP 规则之间没有复杂的交互关系，
因此 DROP 规则可以简单地从 `nat` 移动到 `filter`。
更复杂的场景中，可能需要在 `nat` 和 `filter` 表中“重新匹配”相同的数据包。

### 如果你使用 Kubelet 的 iptables 规则来确定 `iptables-legacy` 与 `iptables-nft`... {#use-case-iptables-mode}

对于从容器内部操纵主机网络命名空间 iptables 规则的组件而言，需要一些方法来确定主机是使用旧的
`iptables-legacy` 二进制文件还是新的 `iptables-nft` 二进制文件（与不同的内核 API 交互）下。

[`iptables-wrappers`] 模块为此类组件提供了一种自动检测系统 iptables 模式的方法，
但在过去，它通过假设 kubelet 将在任何容器启动之前创建“一堆” iptables
规则来实现这一点，因此它可以通过查看哪种模式定义了更多规则来猜测主机文件系统中的
iptables 二进制文件正在使用哪种模式。

在未来的版本中，kubelet 将不再创建许多 iptables 规则，
因此基于计算存在的规则数量的启发式方法可能会失败。

然而，从 1.24 开始，kubelet 总是在它使用的任何 iptables 子系统的
`mangle` 表中创建一个名为 `KUBE-IPTABLES-HINT` 的链。
组件现在可以查找这个特定的链，以了解 kubelet（以及系统的其余部分）正在使用哪个 iptables 子系统。

（此外，从 Kubernetes 1.17 开始，kubelet 在 `mangle` 表中创建了一个名为 `KUBE-KUBELET-CANARY` 的链。
虽然这条链在未来可能会消失，但它仍然会在旧版本中存在，因此在任何最新版本的 Kubernetes 中，
至少会包含 `KUBE-IPTABLES-HINT` 或 `KUBE-KUBELET-CANARY` 两条链的其中一个。）

`iptables-wrappers` 包[已经被更新]，以提供这个新的启发式逻辑，
所以如果你以前使用过它，你可以用它的更新版本重建你的容器镜像。

[`iptables-wrappers`]: https://github.com/kubernetes-sigs/iptables-wrappers/
[已经更新]: https://github.com/kubernetes-sigs/iptables-wrappers/pull/3

## 延伸阅读

[KEP-3178] 跟踪了清理 iptables 链所有权和弃用旧链的项目。

[KEP-3178]: https://github.com/kubernetes/enhancements/issues/3178