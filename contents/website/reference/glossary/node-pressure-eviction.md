---
title: 节点压力驱逐
id: node-pressure-eviction
date: 2021-05-13
full_link: /zh-cn/docs/concepts/scheduling-eviction/node-pressure-eviction/
short_description: >
  节点压力驱逐是 kubelet 主动使 Pod 失败以回收节点上的资源的过程。
aka:
- kubelet eviction
tags:
- operation
---

节点压力驱逐是 {{<glossary_tooltip term_id="kubelet" text="kubelet">}} 主动终止 Pod 以回收节点上资源的过程。


kubelet 监控集群节点上的 CPU、内存、磁盘空间和文件系统 inode 等资源。
当这些资源中的一个或多个达到特定消耗水平时，
kubelet 可以主动使节点上的一个或多个 Pod 失效，以回收资源并防止饥饿。

节点压力驱逐不用于 [API 发起的驱逐](/zh-cn/docs/concepts/scheduling-eviction/api-eviction/)。
