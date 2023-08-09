---
title: 特性门控（Feature gate）
id: feature-gate
date: 2023-01-12
full_link: /zh-cn/docs/reference/command-line-tools-reference/feature-gates/
short_description: >
  一种控制是否启用某特定 Kubernetes 特性的方法。

aka: 
tags:
- fundamental
- operation
---

特性门控是一组键（非透明的字符串值），你可以用它来控制在你的集群中启用哪些 Kubernetes 特性。


你可以在每个 Kubernetes 组件中使用 `--feature-gates` 命令行标志来开启或关闭这些特性。
每个 Kubernetes 组件都可以让你开启或关闭一组与该组件相关的特性门控。
Kubernetes 文档列出了当前所有的[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)及其控制的内容。
