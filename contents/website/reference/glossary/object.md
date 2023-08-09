---
title: 对象（Object）
id: object
date: 2020-10-12
full_link: /zh-cn/docs/concepts/overview/working-with-objects/#kubernetes-objects
short_description: >
   Kubernetes 系统中的实体，代表了集群的部分状态。
aka: 
tags:
- fundamental
---

Kubernetes 系统中的实体。Kubernetes API 用这些实体表示集群的状态。

Kubernetes 对象通常是一个“目标记录”-一旦你创建了一个对象，Kubernetes 
{{< glossary_tooltip text="控制平面（Control Plane）" term_id="control-plane" >}} 
不断工作，以确保它代表的项目确实存在。
创建一个对象相当于告知 Kubernetes 系统：你期望这部分集群负载看起来像什么；这也就是你集群的期望状态。