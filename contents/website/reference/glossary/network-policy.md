---
title: 网络策略
id: network-policy
date: 2018-04-12
full_link: /zh-cn/docs/concepts/services-networking/network-policies/
short_description: >
  网络策略是一种规范，规定了允许 Pod 组之间、Pod 与其他网络端点之间以怎样的方式进行通信。

aka: 
tags:
- networking
- architecture
- extension
---


网络策略是一种规范，规定了允许 Pod 组之间、Pod 与其他网络端点之间以怎样的方式进行通信。



网络策略帮助你声明式地配置允许哪些 Pod 之间、哪些命名空间之间允许进行通信，
并具体配置了哪些端口号来执行各个策略。`NetworkPolicy` 资源使用标签来选择 Pod，
并定义了所选 Pod 可以接受什么样的流量。网络策略由网络提供商提供的并被 Kubernetes 支持的网络插件实现。
请注意，当没有控制器实现网络资源时，创建网络资源将不会生效。
