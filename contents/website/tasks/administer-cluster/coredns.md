---
title: 使用 CoreDNS 进行服务发现
min-kubernetes-server-version: v1.9
content_type: task
weight: 380
---



此页面介绍了 CoreDNS 升级过程以及如何安装 CoreDNS 而不是 kube-dns。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


## 关于 CoreDNS

[CoreDNS](https://coredns.io) 是一个灵活可扩展的 DNS 服务器，可以作为 Kubernetes 集群 DNS。
与 Kubernetes 一样，CoreDNS 项目由 {{< glossary_tooltip text="CNCF" term_id="cncf" >}} 托管。

通过替换现有集群部署中的 kube-dns，或者使用 kubeadm 等工具来为你部署和升级集群，
可以在你的集群中使用 CoreDNS 而非 kube-dns。

## 安装 CoreDNS

有关手动部署或替换 kube-dns，请参阅
[CoreDNS GitHub 项目](https://github.com/coredns/deployment/tree/master/kubernetes)。

## 迁移到 CoreDNS

### 使用 kubeadm 升级现有集群

在 Kubernetes 1.21 版本中，kubeadm 移除了对将 `kube-dns` 作为 DNS 应用的支持。
对于 `kubeadm` v{{< skew currentVersion >}}，所支持的唯一的集群 DNS 应用是 CoreDNS。

当你使用 `kubeadm` 升级使用 `kube-dns` 的集群时，你还可以执行到 CoreDNS 的迁移。
在这种场景中，`kubeadm` 将基于 `kube-dns` ConfigMap 生成 CoreDNS 配置（"Corefile"），
保存存根域和上游名称服务器的配置。

## 升级 CoreDNS 

你可以在 [CoreDNS version in Kubernetes](https://github.com/coredns/deployment/blob/master/kubernetes/CoreDNS-k8s_version.md)
页面查看 kubeadm 为不同版本 Kubernetes 所安装的 CoreDNS 版本。

如果你只想升级 CoreDNS 或使用自己的定制镜像，也可以手动升级 CoreDNS。
参看[指南和演练](https://github.com/coredns/deployment/blob/master/kubernetes/Upgrading_CoreDNS.md)
文档了解如何平滑升级。
在升级你的集群过程中，请确保现有 CoreDNS 的配置（"Corefile"）被保留下来。

如果使用 `kubeadm` 工具来升级集群，则 `kubeadm` 可以自动处理保留现有 CoreDNS
配置这一事项。

## CoreDNS 调优

当资源利用方面有问题时，优化 CoreDNS 的配置可能是有用的。
有关详细信息，请参阅有关[扩缩 CoreDNS 的文档](https://github.com/coredns/deployment/blob/master/kubernetes/Scaling_CoreDNS.md)。

## {{% heading "whatsnext" %}}

你可以通过修改 CoreDNS 的配置（"Corefile"）来配置 [CoreDNS](https://coredns.io)，
以支持比 kube-dns 更多的用例。
请参考 `kubernetes` CoreDNS 插件的[文档](https://coredns.io/plugins/kubernetes/)
或者 CoreDNS 博客上的博文
[Custom DNS Entries for Kubernetes](https://coredns.io/2017/05/08/custom-dns-entries-for-kubernetes/)，
以了解更多信息。

