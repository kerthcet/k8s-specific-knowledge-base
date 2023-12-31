---
layout: blog
title: "Kubernetes 1.27：kubectl apply 裁剪更安全、更高效"
date: 2023-05-09
slug: introducing-kubectl-applyset-pruning
---

**作者:** Katrina Verey（独立个人）和 Justin Santa Barbara (Google)

**译者:** [Michael Yao](https://github.com/windsonsea) (DaoCloud)

通过 `kubectl apply` 命令执行声明式配置管理是创建或修改 Kubernetes 资源的黄金标准方法。
但这种方法也带来了一个挑战，那就是删除不再需要的资源。
在 Kubernetes 1.5 版本中，引入了 `--prune` 标志来解决此问题，
允许 `kubectl apply` 自动清理从当前配置中删除的先前应用的资源。

然而，现有的 `--prune` 实现存在设计缺陷，会降低性能并导致意外行为。
主要问题源于先前的 `apply` 操作未对已应用的集合进行显式编码，有必要进行易错的动态发现。
对象泄漏、意外过度选择资源以及与自定义资源的有限兼容性是这种实现的一些明显缺点。
此外，其与客户端 apply 的耦合阻碍了用户升级到更优秀的服务器端 apply 方式。

`kubectl` 的 1.27 版本引入了 Alpha 版本的重构裁剪实现，解决了这些问题。
这个基于 **ApplySet** 概念的新实现承诺能够提供更好的性能和更好的安全性。

**ApplySet** 是一个与集群上的**父**对象相关联的资源组，通过标准化的标签和注解进行标识和配置。
附加的标准化元数据允许准确标识集群内的 ApplySet **成员**对象，简化了裁剪等操作。

为了充分利用基于 ApplySet 的裁剪，设置 `KUBECTL_APPLYSET=true` 环境变量，
并在 `kubectl apply` 调用中包括标志 `--prune` 和 `--applyset`：

```shell
KUBECTL_APPLYSET=true kubectl apply -f <目录> --prune --applyset=<name>
```

默认情况下，ApplySet 使用 Secret 作为父对象。
但是，你也可以通过格式 `--applyset=configmaps/<name>` 来使用 ConfigMap。
如果所需的 Secret 或 ConfigMap 对象尚不存在，则 `kubectl` 将为你创建它。
此外，可以启用自定义资源以用作 ApplySet 父对象。

ApplySet 实现基于新的底层规约，可以通过提高其互操作性来支持更高层次的生态系统工具。
这种规约的轻量性使得这些工具可以继续使用现有的对象分组系统，
同时选用 ApplySet 的元数据约定以防被其他工具（例如 `kubectl`）意外更改。

基于 ApplySet 的裁剪提供了一种方法，保证有效解决之前 `kubectl` 中 `--prune` 实现的缺陷，
还可以帮助优化 Kubernetes 资源管理。请使用这个新特性并与社区分享你的经验。
ApplySet 正处于积极开发中，你的反馈至关重要！

### 更多资源

- 想了解如何使用基于 ApplySet 的裁剪，请阅读 Kubernetes 文档中的
  [使用配置文件以声明方式管理 Kubernetes 对象](/zh-cn/docs/tasks/manage-kubernetes-objects/declarative-config/)。
- 如需更深入地了解此特性的技术设计或了解如何用你自己工具实现 ApplySet 规范，
  请参阅 [KEP-3659](https://git.k8s.io/enhancements/keps/sig-cli/3659-kubectl-apply-prune/README.md):
  **ApplySet: `kubectl apply --prune` 重新设计和进阶策略**。

### 如何参与

如果你想参与 ApplySet 的开发，可以联系 [SIG CLI](https://git.k8s.io/community/sig-cli) 的开发人员。
如需提供有关此特性的反馈，请在 `kubernetes/kubectl`
代码库上[提交 bug](https://github.com/kubernetes/kubectl/issues/new?assignees=knverey,justinsb&labels=kind%2Fbug&template=bug-report.md)
或[提出增强请求](https://github.com/kubernetes/kubectl/issues/new?assignees=knverey,justinsb&labels=kind%2Fbug&template=enhancement.md)。
