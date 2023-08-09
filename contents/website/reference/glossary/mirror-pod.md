---
title: 镜像 Pod（Mirror Pod）
id: 静态-pod
date: 2019-08-06
short_description: >
  API 服务器中的一个对象，用于跟踪 kubelet 上的静态 pod。

aka:
tags:
- 基本的
---

镜像 Pod（Mirror Pod）是被 kubelet 用来代表{{< glossary_tooltip text="静态 Pod" term_id="static-pod" >}} 的
{{< glossary_tooltip text="pod" term_id="pod" >}} 对象。


当 kubelet 在其配置中发现一个静态容器时，
它会自动地尝试在 Kubernetes API 服务器上为它创建 Pod 对象。
这意味着 pod 在 API 服务器上将是可见的，但不能在其上进行控制。

（例如，删除镜像 Pod 也不会阻止 kubelet 守护进程继续运行它）。