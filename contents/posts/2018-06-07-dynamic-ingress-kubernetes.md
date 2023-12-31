---
title: 'Kubernetes 的动态 Ingress'
date: 2018-06-07
layout: blog
Author: Richard Li (Datawire)
slug: dynamic-ingress-in-kubernetes
---


Kubernetes 可以轻松部署由许多微服务组成的应用程序，但这种架构的关键挑战之一是动态地将流量路由到这些服务中的每一个。
一种方法是使用 [Ambassador](https://www.getambassador.io)，
一个基于 [Envoy Proxy](https://www.envoyproxy.io) 构建的 Kubernetes 原生开源 API 网关。
Ambassador 专为动态环境而设计，这类环境中的服务可能被频繁添加或删除。

Ambassador 使用 Kubernetes 注解进行配置。
注解用于配置从给定 Kubernetes 服务到特定 URL 的具体映射关系。
每个映射中可以包括多个注解，用于配置路由。
注解的例子有速率限制、协议、跨源请求共享（CORS）、流量影射和路由规则等。


## 一个简单的 Ambassador 示例

Ambassador 通常作为 Kubernetes Deployment 来安装，也可以作为 Helm Chart 使用。
配置 Ambassador 时，请使用 Ambassador 注解创建 Kubernetes 服务。
下面是一个例子，用来配置 Ambassador，将针对 /httpbin/ 的请求路由到公共的 httpbin.org 服务：

```
apiVersion: v1
kind: Service
metadata:
  name: httpbin
  annotations:
    getambassador.io/config: |
      ---
      apiVersion: ambassador/v0
      kind:  Mapping
      name:  httpbin_mapping
      prefix: /httpbin/
      service: httpbin.org:80
      host_rewrite: httpbin.org
spec:
  type: ClusterIP
  ports:
    - port: 80
```


例子中创建了一个 Mapping 对象，其 prefix 设置为 /httpbin/，service 名称为 httpbin.org。
其中的 host_rewrite 注解指定 HTTP 的 host 头部字段应设置为 httpbin.org。


## Kubeflow

[Kubeflow](https://github.com/kubeflow/kubeflow) 提供了一种简单的方法，用于在 Kubernetes 上轻松部署机器学习基础设施。
Kubeflow 团队需要一个代理，为 Kubeflow 中所使用的各种服务提供集中化的认证和路由能力；Kubeflow 中许多服务本质上都是生命期很短的。

<center><i>Kubeflow architecture, pre-Ambassador</center></i>


## 服务配置

有了 Ambassador，Kubeflow 可以使用分布式模型进行配置。
Ambassador 不使用集中的配置文件，而是允许每个服务通过 Kubernetes 注解在 Ambassador 中配置其路由。
下面是一个简化的配置示例：

```
---
apiVersion: ambassador/v0
kind:  Mapping
name: tfserving-mapping-test-post
prefix: /models/test/
rewrite: /model/test/:predict
method: POST
service: test.kubeflow:8000
```


示例中，“test” 服务使用 Ambassador 注解来为服务动态配置路由。
所配置的路由仅在 HTTP 方法是 POST 时触发；注解中同时还给出了一条重写规则。


## Kubeflow 和 Ambassador

通过 Ambassador，Kubeflow 可以使用 Kubernetes 注解轻松管理路由。
Kubeflow 配置同一个 Ingress 对象，将流量定向到 Ambassador，然后根据需要创建具有 Ambassador 注解的服务，以将流量定向到特定后端。
例如，在部署 TensorFlow 服务时，Kubeflow 会创建 Kubernetes 服务并为其添加注解，
以便用户能够在 `https://<ingress主机>/models/<模型名称>/` 处访问到模型本身。
Kubeflow 还可以使用 Envoy Proxy 来进行实际的 L7 路由。
通过 Ambassador，Kubeflow 能够更充分地利用 URL 重写和基于方法的路由等额外的路由配置能力。

如果您对在 Kubeflow 中使用 Ambassador 感兴趣，标准的 Kubeflow 安装会自动安装和配置 Ambassador。

如果您有兴趣将 Ambassador 用作 API 网关或 Kubernetes 的 Ingress 解决方案，
请参阅 [Ambassador 入门指南](https://www.getambassador.io/user-guide/getting-started)。

