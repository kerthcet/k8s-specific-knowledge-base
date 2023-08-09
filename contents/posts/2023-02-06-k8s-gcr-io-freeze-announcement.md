---
layout: blog
title: "k8s.gcr.io 镜像仓库将从 2023 年 4 月 3 日起被冻结"
date: 2023-02-06
slug: k8s-gcr-io-freeze-announcement
---

**作者**：Mahamed Ali (Rackspace Technology)

**译者**：Michael Yao (Daocloud)

Kubernetes 项目运行一个名为 `registry.k8s.io`、由社区管理的镜像仓库来托管其容器镜像。
2023 年 4 月 3 日，旧仓库 `k8s.gcr.io` 将被冻结，Kubernetes 及其相关子项目的镜像将不再推送到这个旧仓库。

`registry.k8s.io` 这个仓库代替了旧仓库，这个新仓库已正式发布七个月。
我们也发布了一篇[博文](/blog/2022/11/28/registry-k8s-io-faster-cheaper-ga/)阐述新仓库给社区和
Kubernetes 项目带来的好处。这篇博客再次宣布后续版本的 Kubernetes 将不可用于旧仓库。这个时刻已经到来。

这次变更对贡献者意味着：

- 如果你是某子项目的 Maintainer，你将需要更新清单 (manifest) 和 Helm Chart 才能使用新仓库。

这次变更对终端用户意味着：

- Kubernetes 1.27 版本将不会发布到旧仓库。
- 1.24、1.25 和 1.26 版本的补丁从 4 月份起将不再发布到旧仓库。请阅读以下时间线，了解旧仓库最终补丁版本的详情。
- 从 1.25 开始，默认的镜像仓库已设置为 `registry.k8s.io`。`kubeadm` 和 `kubelet`
  中的这个镜像仓库地址是可覆盖的，但设置为 `k8s.gcr.io` 将在 4 月份之后的新版本中失败，
  因为旧仓库将没有这些版本了。
- 如果你想提高集群的可靠性，不想再依赖社区管理的镜像仓库，或你正在外部流量受限的网络中运行 Kubernetes，
  你应该考虑托管本地镜像仓库的镜像。一些云供应商可能会为此提供托管解决方案。

## 变更时间线   {#timeline-of-changes}

- `k8s.gcr.io` 将于 2023 年 4 月 3 日被冻结
- 1.27 预计于 2023 年 4 月 12 日发布
- `k8s.gcr.io` 上的最后一个 1.23 版本将是 1.23.18（1.23 在仓库冻结前进入不再支持阶段）
- `k8s.gcr.io` 上的最后一个 1.24 版本将是 1.24.12
- `k8s.gcr.io` 上的最后一个 1.25 版本将是 1.25.8
- `k8s.gcr.io` 上的最后一个 1.26 版本将是 1.26.3

## 下一步   {#whats-next}

请确保你的集群未依赖旧的镜像仓库。例如，你可以运行以下命令列出 Pod 使用的镜像：

```shell
kubectl get pods --all-namespaces -o jsonpath="{.items[*].spec.containers[*].image}" |\
tr -s '[[:space:]]' '\n' |\
sort |\
uniq -c
```

旧的镜像仓库可能存在其他依赖项。请确保你检查了所有潜在的依赖项，以保持集群健康和最新。

## 致谢   {#acknowledgments}

__改变是艰难的__，但只有镜像服务平台演进才能确保 Kubernetes 项目可持续的未来。
我们努力为 Kubernetes 的每个使用者提供更好的服务。从社区各个角落汇聚而来的众多贡献者长期努力工作，
确保我们能够做出尽可能最好的决策、履行计划并尽最大努力传达这些计划。

衷心感谢：

- 来自 SIG K8s Infra 的 Aaron Crickenberger、Arnaud Meukam、Benjamin Elder、Caleb
  Woodbine、Davanum Srinivas、Mahamed Ali 和 Tim Hockin
- 来自 SIG Node 的 Brian McQueen 和 Sergey Kanzhelev
- 来自 SIG Cluster Lifecycle 的 Lubomir Ivanov
- 来自 SIG Release 的 Adolfo García Veytia、Jeremy Rickard、Sascha Grunert 和 Stephen Augustus
- 来自 SIG Contribex 的 Bob Killen 和 Kaslin Fields
- 来自 Security Response Committee（安全响应委员会）的 Tim Allclair

此外非常感谢负责联络各个云提供商合作伙伴的朋友们：来自 Amazon 的 Jay Pipes 和来自 Google 的 Jon Johnson Jr.
