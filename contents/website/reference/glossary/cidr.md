---
title: CIDR
id: cidr
date: 2019-11-12
full_link: 
short_description: >
  CIDR 是一种描述 IP 地址块的符号，被广泛使用于各种网络配置中。

aka:
tags:
- networking
---

CIDR（无类域间路由，Classless Inter-Domain Routing）是一种描述
IP 地址块的符号，被广泛使用于各种网络配置中。


在 Kubernetes 的上下文中，每个{{< glossary_tooltip text="节点" term_id="node" >}}
以 CIDR 形式（含起始地址和子网掩码）获得一个 IP 地址段，
从而能够为每个 {{< glossary_tooltip text="Pod" term_id="pod" >}} 分配一个独一无二的 IP 地址。
虽然其概念最初源自 IPv4，CIDR 已经被扩展为涵盖 IPv6。
