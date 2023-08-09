---
layout: blog
title: '更新 NGINX-Ingress 以使用稳定的 Ingress API'
date: 2021-07-26
slug: update-with-ingress-nginx
---

**作者：** James Strong, Ricardo Katz

对于所有 Kubernetes API，一旦它们被正式发布（GA），就有一个创建、维护和最终弃用它们的过程。
networking.k8s.io API 组也不例外。
即将发布的 Kubernetes 1.22 版本将移除几个与网络相关的已弃用 API：

- [IngressClass](/zh-cn/docs/concepts/services-networking/ingress/#ingress-class) 的 `networking.k8s.io/v1beta1` API 版本
- [Ingress](/zh-cn/docs/concepts/services-networking/ingress/) 的所有 Beta 版本: `extensions/v1beta1` 和 `networking.k8s.io/v1beta1`

在 v1.22 Kubernetes 集群上，你能够通过稳定版本（v1）的 API 访问 Ingress 和 IngressClass 对象，
但无法通过其 Beta API 访问。 
自 [2017](https://github.com/kubernetes/kubernetes/issues/43214)、
[2019](https://kubernetes.io/blog/2019/07/18/api-deprecations-in-1-16/) 
以来一直讨论关于 Kubernetes 1.16 弃用 API 的更改，
最近的讨论是在 KEP-1453：[Ingress API 毕业到 GA](https://github.com/kubernetes/enhancements/tree/master/keps/sig-network/1453-ingress-api#122)。

在社区会议中，网络特别兴趣小组决定继续支持带有 0.47.0 版本 Ingress-NGINX 的早于 1.22 版本的 Kubernetes。
在 Kubernetes 1.22 发布后，对 Ingress-NGINX 的支持将持续六个月。
团队会根据需要解决 Ingress-NGINX 的额外错误修复和 CVE 问题。

Ingress-NGINX 将拥有独立的分支和发布版本来支持这个模型，与 Kubernetes 项目流程相一致。
Ingress-NGINX 项目的未来版本将跟踪和支持最新版本的 Kubernetes。

{{< table caption="Kubernetes 各版本支持的 Ingress NGINX 版本" >}}
Kubernetes 版本  | Ingress-NGINX 版本 | 公告
:-------------------|:----------------------|:------------
v1.22              | v1.0.0-alpha.2     | 新特性，以及错误修复。
v1.21              | v0.47.x        | 仅修复安全问题或系统崩溃的错误。没有宣布终止支持日期。
v1.20              | v0.47.x        | 仅修复安全问题或系统崩溃的错误。没有宣布终止支持日期。
v1.19              | v0.47.x        | 仅修复安全问题或系统崩溃的错误。仅在 Kubernetes v1.22.0 发布后的 6 个月内提供修复支持。
{{< /table >}}    

由于 Kubernetes 1.22 中的更新，**v0.47.0** 将无法与 Kubernetes 1.22 一起使用。 

## 你需要做什么

团队目前正在升级 Ingress-NGINX 以支持向 v1 的迁移，
你可以在[此处](https://github.com/kubernetes/ingress-nginx/pull/7156)跟踪进度。
在对 Ingress v1 的支持完成之前，
我们不会对功能进行改进。

同时，团队会确保没有兼容性问题：

* 更新到最新的 Ingress-NGINX 版本，
  目前是 [v0.47.0](https://github.com/kubernetes/ingress-nginx/releases/tag/controller-v0.47.0)。 
* Kubernetes 1.22 发布后，请确保使用的是支持 Ingress 和 IngressClass 稳定 API 的最新版本的 Ingress-NGINX。
* 使用集群版本 >= 1.19 测试 Ingress-NGINX 版本 v1.0.0-alpha.2，并将任何问题报告给项目 GitHub 页面。

欢迎社区对此工作的反馈和支持。
Ingress-NGINX 子项目定期举行社区会议，
我们会讨论这个问题以及项目面临的其他问题。
有关子项目的更多信息，请参阅 [SIG Network](https://github.com/kubernetes/community/tree/master/sig-network)。
