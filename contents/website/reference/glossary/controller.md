---
title: 控制器（Controller）
id: controller
date: 2018-04-12
full_link: /zh-cn/docs/concepts/architecture/controller/
short_description: >
  控制器通过 API 服务器监控集群的公共状态，并致力于将当前状态转变为期望的状态。

aka: 
tags:
- architecture
- fundamental
---
																			  
在 Kubernetes 中，控制器通过监控{{< glossary_tooltip text="集群" term_id="cluster" >}}
的公共状态，并致力于将当前状态转变为期望的状态。

												  
控制器（{{< glossary_tooltip text="控制平面" term_id="control-plane" >}}的一部分）
通过 {{< glossary_tooltip text="API 服务器" term_id="kube-apiserver" >}}监控你的集群中的公共状态。

其中一些控制器是运行在控制平面内部的，对 Kubernetes 来说，他们提供核心控制操作。
比如：部署控制器（deployment controller）、守护控制器（daemonset controller）、
命名空间控制器（namespace controller）、持久化数据卷控制器（persistent volume controller）（等）
都是运行在 {{< glossary_tooltip text="kube-controller-manager" term_id="kube-controller-manager" >}} 中的。
