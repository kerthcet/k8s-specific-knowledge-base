---
title: 副本控制器（ReplicationController）
id: replication-controller
date: 2018-04-12
full_link: 
short_description: >
  一种管理多副本应用的（已弃用）的 API 对象。

aka: 
tags:
- workload
- core-object
---


一种管理多副本应用的工作负载资源，能够确保特定个数的
{{< glossary_tooltip text="Pod" term_id="pod" >}}
实例处于运行状态。


控制平面确保即使某些 Pod 失效、被你手动删除或错误地启动了过多 Pod 时，
指定数量的 Pod 仍处于运行状态。

{{< note >}}
ReplicationController 已被弃用。请参见执行类似功能的
{{< glossary_tooltip text="Deployment" term_id="deployment" >}}。
{{< /note >}}
