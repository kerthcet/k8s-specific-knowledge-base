---
title: 容器生命周期钩子（Container Lifecycle Hooks）
id: container-lifecycle-hooks
date: 2018-10-08
full_link: /zh-cn/docs/concepts/containers/container-lifecycle-hooks/
short_description: >
  生命周期钩子暴露容器管理生命周期中的事件，允许用户在事件发生时运行代码。

aka: 
tags:
- extension
---

  生命周期钩子（Lifecycle Hooks）暴露{{< glossary_tooltip text="容器" term_id="container" >}}管理生命周期中的事件，允许用户在事件发生时运行代码。


针对容器暴露了两个钩子：
PostStart 在容器创建之后立即执行，
PreStop 在容器停止之前立即阻塞并被调用。
