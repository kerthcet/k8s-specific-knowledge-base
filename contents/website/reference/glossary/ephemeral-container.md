---
title: 临时容器（Ephemeral Container）
id: ephemeral-container
date: 2019-08-26
full_link: /zh-cn/docs/concepts/workloads/pods/ephemeral-containers/
short_description: >
  你可以在 Pod 中临时运行的一种容器类型
aka:
tags:
- fundamental
---

你可以在 {{< glossary_tooltip term_id="pod" >}} 中临时运行的一种 {{< glossary_tooltip term_id="container" >}} 类型。


如果想要调查运行中有问题的 Pod，可以向该 Pod 添加一个临时容器（Ephemeral Container）并进行诊断。
临时容器没有资源或调度保证，因此不应该使用它们来运行工作负载本身的任何部分。

{{< glossary_tooltip text="静态 Pod" term_id="static-pod" >}} 不支持临时容器。
