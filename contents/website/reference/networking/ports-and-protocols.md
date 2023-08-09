---
title: 端口和协议
content_type: reference
weight: 50
---


当你在一个有严格网络边界的环境里运行 Kubernetes，例如拥有物理网络防火墙或者拥有公有云中虚拟网络的自有数据中心，
了解 Kubernetes 组件使用了哪些端口和协议是非常有用的。

## 控制面  {#control-plane}

| 协议     | 方向      | 端口范围     | 目的                     | 使用者                     |
|----------|-----------|------------|-------------------------|---------------------------|
| TCP      | 入站       | 6443       | Kubernetes API server   | 所有                       |
| TCP      | 入站       | 2379-2380  | etcd server client API  | kube-apiserver, etcd      |
| TCP      | 入站       | 10250      | Kubelet API             | 自身, 控制面                |
| TCP      | 入站       | 10259      | kube-scheduler          | 自身                       |
| TCP      | 入站       | 10257      | kube-controller-manager | 自身                       |

尽管 etcd 的端口也列举在控制面的部分，但你也可以在外部自己托管 etcd 集群或者自定义端口。

## 工作节点  {#node}

| 协议     | 方向      | 端口范围     | 目的                     | 使用者                  |
|----------|-----------|-------------|-----------------------|-------------------------|
| TCP      | 入站       | 10250       | Kubelet API           | 自身, 控制面             |
| TCP      | 入站       | 30000-32767 | NodePort Services†    | 所有                    |

† [NodePort Services](/zh-cn/docs/concepts/services-networking/service/)的默认端口范围。

所有默认端口都可以重新配置。当使用自定义的端口时，你需要打开这些端口来代替这里提到的默认端口。

一个常见的例子是 API 服务器的端口有时会配置为 443。或者你也可以使用默认端口，
把 API 服务器放到一个监听 443 端口的负载均衡器后面，并且路由所有请求到 API 服务器的默认端口。
