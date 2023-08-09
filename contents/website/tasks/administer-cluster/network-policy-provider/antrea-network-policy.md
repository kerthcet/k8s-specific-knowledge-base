---
title: 使用 Antrea 提供 NetworkPolicy
content_type: task
weight: 10
---

本页展示了如何在 kubernetes 中安装和使用 Antrea CNI 插件。
要了解 Antrea 项目的背景，请阅读 [Antrea 介绍](https://antrea.io/docs/)。

## {{% heading "prerequisites" %}}

你需要拥有一个 kuernetes 集群。
遵循 [kubeadm 入门指南](/zh-cn/docs/reference/setup-tools/kubeadm/)自行创建一个。


## 使用 kubeadm 部署 Antrea
遵循[入门](https://github.com/vmware-tanzu/antrea/blob/main/docs/getting-started.md)指南
为 kubeadm 部署 Antrea 。

## {{% heading "whatsnext" %}}

一旦你的集群已经运行，你可以遵循 
[声明网络策略](/zh-cn/docs/tasks/administer-cluster/declare-network-policy/)
来尝试 Kubernetes NetworkPolicy。