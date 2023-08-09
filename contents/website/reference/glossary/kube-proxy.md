---
title: kube-proxy
id: kube-proxy
date: 2018-04-12
full_link: /zh-cn/docs/reference/command-line-tools-reference/kube-proxy/
short_description: >
  `kube-proxy` 是集群中每个节点上运行的网络代理。

aka:
tags:
- fundamental
- networking
---
[kube-proxy](/zh-cn/docs/reference/command-line-tools-reference/kube-proxy/)
是集群中每个{{< glossary_tooltip text="节点（node）" term_id="node" >}}上所运行的网络代理，
实现 Kubernetes {{< glossary_tooltip term_id="service">}} 概念的一部分。


kube-proxy 维护节点上的一些网络规则，
这些网络规则会允许从集群内部或外部的网络会话与 Pod 进行网络通信。

如果操作系统提供了可用的数据包过滤层，则 kube-proxy 会通过它来实现网络规则。
否则，kube-proxy 仅做流量转发。
