---
title: 干扰（Disruption）
id: disruption
date: 2019-09-10
full_link: /zh-cn/docs/concepts/workloads/pods/disruptions/
short_description: >
   导致 Pod 服务停止的事件。
aka:
tags:
- fundamental
---

干扰（Disruption）是指导致一个或者多个 {{< glossary_tooltip term_id="pod" text="Pod" >}} 服务停止的事件。
干扰会影响依赖于受影响的 Pod 的资源，例如 {{< glossary_tooltip term_id="deployment" >}}。


如果你作为一个集群操作人员，销毁了一个从属于某个应用的 Pod，
Kubernetes 视之为**自愿干扰（Voluntary Disruption）**。
如果由于节点故障或者影响更大区域故障的断电导致 Pod 离线，
Kubernetes 视之为**非愿干扰（Involuntary Disruption）**。

更多信息请查阅[干扰](/zh-cn/docs/concepts/workloads/pods/disruptions/)。
