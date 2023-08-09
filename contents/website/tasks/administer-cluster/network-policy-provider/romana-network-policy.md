---
title: 使用 Romana 提供 NetworkPolicy
content_type: task
weight: 50
---



本页展示如何使用 Romana 作为 NetworkPolicy。

## {{% heading "prerequisites" %}}

完成 [kubeadm 入门指南](/zh-cn/docs/reference/setup-tools/kubeadm/)中的 1、2、3 步。

## 使用 kubeadm 安装 Romana

按照[容器化安装指南](https://github.com/romana/romana/tree/master/containerize)，
使用 kubeadm 安装。

## 应用网络策略

使用以下的一种方式应用网络策略：

* [Romana 网络策略](https://github.com/romana/romana/wiki/Romana-policies)
  * [Romana 网络策略例子](https://github.com/romana/core/blob/master/doc/policy.md)
* NetworkPolicy API

## {{% heading "whatsnext" %}}

Romana 安装完成后，你可以按照
[声明网络策略](/zh-cn/docs/tasks/administer-cluster/declare-network-policy/)
去尝试使用 Kubernetes NetworkPolicy。

