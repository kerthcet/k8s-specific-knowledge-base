---
title: 云提供商（Cloud Provider）
id: cloud-provider
date: 2018-04-12
short_description: >
  一个提供云计算平台的组织。

aka:
- 云服务提供商（Cloud Service Provider）
tags:
- community
---

 一个提供云计算平台的商业机构或其他组织。


云提供商（Cloud provider），有时也称作云服务提供商（CSPs）提供云计算平台或服务。

很多云提供商提供托管的基础设施（也称作基础设施即服务或 IaaS）。
针对托管的基础设施，云提供商负责服务器、存储和网络，而用户（你）
负责管理其上运行的各层软件，例如运行一个 Kubernetes 集群。

你也会看到 Kubernetes 被作为托管服务提供；有时也称作平台即服务或 PaaS。
针对托管的 Kubernetes，你的云提供商负责 Kubernetes 的控制平面以及
 {{< glossary_tooltip term_id="node" text="节点" >}} 及他们所依赖的基础设施：
网络、存储以及其他一些诸如负载均衡器之类的元素。
