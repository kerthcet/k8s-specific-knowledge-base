---
title: 应用程序容器（App Container）
id: app-container
date: 2019-02-12
full_link:
short_description: >
  用于运行部分工作负载的容器。与 Init 容器比较而言。

aka:
tags:
- workload
---

应用程序容器是在 {{< glossary_tooltip text="Pod" term_id="pod" >}}
中的{{< glossary_tooltip text="容器" term_id="container" >}}（或 app 容器），
在 {{< glossary_tooltip text="Init 容器" term_id="init-container" >}}启动完毕后才开始启动。


Init 容器使你可以分离对于{{< glossary_tooltip text="工作负载" term_id="workload" >}}整体而言很重要的初始化细节，
并且一旦应用容器启动，它不需要继续运行。
如果 Pod 没有配置 Init 容器，则该 Pod 中的所有容器都是应用程序容器。
