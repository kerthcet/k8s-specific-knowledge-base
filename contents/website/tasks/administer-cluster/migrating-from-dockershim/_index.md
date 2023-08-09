---
title: 从 dockershim 迁移
weight: 20
content_type: task
no_list: true
---


本节提供从 dockershim 迁移到其他容器运行时的必备知识。

自从 Kubernetes 1.20 宣布
[弃用 dockershim](/zh-cn/blog/2020/12/08/kubernetes-1-20-release-announcement/#dockershim-deprecation)，
各类疑问随之而来：这对各类工作负载和 Kubernetes 部署会产生什么影响。
我们的[弃用 Dockershim 常见问题](/blog/2022/02/17/dockershim-faq/)可以帮助你更好地理解这个问题。

Dockershim 在 Kubernetes v1.24 版本已经被移除。
如果你集群内是通过 dockershim 使用 Docker Engine 作为容器运行时，并希望 Kubernetes 升级到 v1.24，
建议你迁移到其他容器运行时或使用其他方法以获得 Docker 引擎支持。

请参阅[容器运行时](/zh-cn/docs/setup/production-environment/container-runtimes/)
一节以了解可用的备选项。

带 dockershim 的 Kubernetes 版本 (1.23) 已不再支持，
v1.24 [很快](/zh-cn/releases/#release-v1-24)也将不再支持。

当在迁移过程中遇到麻烦，请[上报问题](https://github.com/kubernetes/kubernetes/issues)。
那么问题就可以及时修复，你的集群也可以进入移除 dockershim 前的就绪状态。
在 v1.24 支持结束后，如果出现影响集群的严重问题，
你需要联系你的 Kubernetes 供应商以获得支持或一次升级多个版本。

你的集群中可以有不止一种类型的节点，尽管这不是常见的情况。

下面这些任务可以帮助你完成迁移：

* [检查移除 Dockershim 是否影响到你](/zh-cn/docs/tasks/administer-cluster/migrating-from-dockershim/check-if-dockershim-removal-affects-you/)
* [将 Docker Engine 节点从 dockershim 迁移到 cri-dockerd](/zh-cn/docs/tasks/administer-cluster/migrating-from-dockershim/migrate-dockershim-dockerd/)
* [从 dockershim 迁移遥测和安全代理](/zh-cn/docs/tasks/administer-cluster/migrating-from-dockershim/migrating-telemetry-and-security-agents/)

## {{% heading "whatsnext" %}}

* 查看[容器运行时](/zh-cn/docs/setup/production-environment/container-runtimes/)了解可选的容器运行时。
* 如果你发现与 dockershim 迁移相关的缺陷或其他技术问题，
  可以在 Kubernetes 项目[报告问题](https://github.com/kubernetes/kubernetes/issues/new/choose)。
