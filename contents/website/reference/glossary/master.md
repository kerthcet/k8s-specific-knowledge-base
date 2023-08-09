---
title: Master
id: master
date: 2020-04-16
short_description: >
  遗留术语，作为运行控制平面的节点的同义词使用。

aka:
tags:
- fundamental
---
 遗留术语，作为运行 {{< glossary_tooltip text="控制平面" term_id="control-plane" >}} 的 {{< glossary_tooltip text="节点" term_id="node" >}} 的同义词使用。



该术语仍被一些配置工具使用，如 {{< glossary_tooltip text="kubeadm" term_id="kubeadm" >}} 以及托管的服务，为 {{< glossary_tooltip text="节点（nodes）" term_id="node" >}} 添加 `kubernetes.io/role` 的 {{< glossary_tooltip text="标签（label）" term_id="label" >}}，以及管理控制平面 Pod 的调度。