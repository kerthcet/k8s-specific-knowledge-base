---
title: Deployment
id: deployment
date: 2018-04-12
full_link: /zh-cn/docs/concepts/workloads/controllers/deployment/
short_description: >
  管理集群上的多副本应用。
aka: 
tags:
- fundamental
- core-object
- workload
---

管理多副本应用的一种 API 对象，通常通过运行没有本地状态的 Pod 来完成工作。


每个副本表现为一个 {{<glossary_tooltip term_id="pod" >}}，
Pod 分布在集群中的{{<glossary_tooltip text="节点" term_id="node" >}}上。
对于确实需要本地状态的工作负载，请考虑使用 {{<glossary_tooltip term_id="StatefulSet" >}}。
