---
title: 服务（Service）
id: service
date: 2018-04-12
full_link: /zh-cn/docs/concepts/services-networking/service/
short_description: >
  将运行在一组 Pods 上的应用程序公开为网络服务的抽象方法。

aka:
tags:
- fundamental
- core-object
---



将运行在一个或一组 {{< glossary_tooltip text="Pod" term_id="pod" >}} 上的网络应用程序公开为网络服务的方法。


服务所针对的 Pod 集（通常）由{{< glossary_tooltip text="选择算符" term_id="selector" >}}确定。
如果有 Pod 被添加或被删除，则与选择算符匹配的 Pod 集合将发生变化。
服务确保可以将网络流量定向到该工作负载的当前 Pod 集合。


Kubernetes Service 要么使用 IP 网络（IPv4、IPv6 或两者），要么引用位于域名系统 (DNS) 中的外部名称。

Service 的抽象可以实现其他机制，如 Ingress 和 Gateway。
