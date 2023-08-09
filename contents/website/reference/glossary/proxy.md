---
title: 代理（Proxy）
id: proxy
date: 2019-09-10
short_description: >
  充当客户端和服务器之间的中介的应用程序

aka:
tags:
- networking
---
在计算机领域，代理指的是充当远程服务中介的服务器。



客户端与代理进行交互；代理将客户端的数据复制到实际服务器；实际服务器回复代理；代理将实际服务器的回复发送给客户端。

[kube-proxy](/zh-cn/docs/reference/command-line-tools-reference/kube-proxy/) 是集群中每个节点上运行的网络代理，实现了部分 Kubernetes {{< glossary_tooltip term_id="service">}} 概念。

你可以将 kube-proxy 作为普通的用户态代理服务运行。
如果你的操作系统支持，则可以在混合模式下运行 kube-proxy；该模式使用较少的系统资源即可达到相同的总体效果。

