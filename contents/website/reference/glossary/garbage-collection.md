---
title: 垃圾收集（Garbage Collection）
id: garbage-collection
date: 2021-07-07
full_link: /zh-cn/docs/concepts/architecture/garbage-collection/
short_description: >
  Kubernetes 用于清理集群资源的各种机制的统称。

aka: 
tags:
- fundamental
- operation
---

垃圾收集（Garbage Collection）是 Kubernetes 用于清理集群资源的各种机制的统称。


Kubernetes 使用垃圾收集机制来清理资源，例如：
[未使用的容器和镜像](/zh-cn/docs/concepts/architecture/garbage-collection/#containers-images)、
[失败的 Pod](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#pod-garbage-collection)、
[目标资源拥有的对象](/zh-cn/docs/concepts/overview/working-with-objects/owners-dependents/)、
[已完成的 Job](/zh-cn/docs/concepts/workloads/controllers/ttlafterfinished/)、
过期或出错的资源。
