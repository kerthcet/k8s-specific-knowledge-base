---
title: Operator 模式
id: operator-pattern
date: 2019-05-21
full_link: /zh-cn/docs/concepts/extend-kubernetes/operator/
short_description: >
  一种用于管理自定义资源的专用控制器

aka:
tags:
- architecture
---

[operator 模式](/zh-cn/docs/concepts/extend-kubernetes/operator/) 是一种系统设计， 
将 {{< glossary_tooltip term_id="controller" >}} 关联到一个或多个自定义资源。

除了使用作为 Kubernetes 自身一部分的内置控制器之外，你还可以通过
将控制器添加到集群中来扩展 Kubernetes。

如果正在运行的应用程序能够充当控制器并通过 API 访问的方式来执行任务操控
那些在控制平面中定义的自定义资源，这就是一个 operator 模式的示例。

