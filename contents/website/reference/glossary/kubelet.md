---
title: Kubelet
id: kubelet
date: 2018-04-12
full_link: /docs/reference/generated/kubelet
short_description: >
  一个在集群中每个节点上运行的代理。它保证容器都运行在 Pod 中。

aka:
tags:
- fundamental
---

`kubelet` 会在集群中每个{{< glossary_tooltip text="节点（node）" term_id="node" >}}上运行。
它保证{{< glossary_tooltip text="容器（containers）" term_id="container" >}}都运行在
{{< glossary_tooltip text="Pod" term_id="pod" >}} 中。


kubelet 接收一组通过各类机制提供给它的 PodSpecs，
确保这些 PodSpecs 中描述的容器处于运行状态且健康。
kubelet 不会管理不是由 Kubernetes 创建的容器。
