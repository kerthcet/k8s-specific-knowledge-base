---
title: Pod
id: pod
date: 2018-04-12
full_link: /zh-cn/docs/concepts/workloads/pods/
short_description: >
  Pod 表示你的集群上一组正在运行的容器。

aka: 
tags:
- core-object
- fundamental
---


Pod 是 Kubernetes 的原子对象。
Pod 表示你的集群上一组正在运行的{{< glossary_tooltip text="容器（Container）" term_id="container" >}}。



通常创建 Pod 是为了运行单个主容器。
Pod 还可以运行可选的边车（sidecar）容器，以添加诸如日志记录之类的补充特性。
通常用 {{< glossary_tooltip term_id="deployment" >}} 来管理 Pod。
