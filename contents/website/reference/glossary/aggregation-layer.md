---
title: 聚合层（Aggregation Layer）
id: aggregation-layer
date: 2018-10-08
full_link: /zh-cn/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/
short_description: >
  聚合层允许你在自己的集群上安装额外的 Kubernetes 风格的 API。

aka: 
tags:
- architecture
- extension
- operation
---

聚合层允许你在自己的集群上安装额外的 Kubernetes 风格的 API。


当你配置了 {{< glossary_tooltip text="Kubernetes API 服务器" term_id="kube-apiserver" >}} 来 [支持额外的 API](/zh-cn/docs/tasks/extend-kubernetes/configure-aggregation-layer/)，
你就可以在 Kubernetes API 中增加 `APIService` 对象来"申领（Claim）"一个 URL 路径。 
