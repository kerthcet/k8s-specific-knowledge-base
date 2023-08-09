---
title: 端点（Endpoints）
id: endpoints
date: 2020-04-23
full_link: 
short_description: >
  端点负责记录与服务（Service）的选择器相匹配的 Pod 的 IP 地址。

aka:
tags:
- networking
---

端点负责记录与服务的{{< glossary_tooltip text="选择器" term_id="selector" >}}相匹配的 Pod 的 IP 地址。


端点可以手动配置到{{< glossary_tooltip text="服务（Service）" term_id="service" >}}上，而不必指定选择器标识。

{{< glossary_tooltip text="EndpointSlice" term_id="endpoint-slice" >}} 提供了一种可伸缩、可扩展的替代方案。
