---
title: 工作负载（Workload）
id: workloads
date: 2019-02-13
full_link: /zh-cn/docs/concepts/workloads/
short_description: >
   工作负载是在 Kubernetes 上运行的应用程序。

aka: 
tags:
- fundamental
---

   工作负载是在 Kubernetes 上运行的应用程序。


代表不同类型或部分工作负载的各种核心对象包括 DaemonSet、Deployment、Job、ReplicaSet 和 StatefulSet。

例如，具有 Web 服务器和数据库的工作负载可能在一个
{{< glossary_tooltip term_id="StatefulSet" >}} 中运行数据库，
而 Web 服务器运行在 {{< glossary_tooltip term_id="Deployment" >}}。