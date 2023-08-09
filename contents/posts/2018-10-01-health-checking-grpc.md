---
layout: blog
title:  '在 Kubernetes 上对 gRPC 服务器进行健康检查'
date: 2018-10-01
slug: health-checking-grpc-servers-on-kubernetes
---

**作者**： [Ahmet Alp Balkan](https://twitter.com/ahmetb) (Google)

**更新（2021 年 12 月）：** “Kubernetes 从 v1.23 开始具有内置 gRPC 健康探测。
了解更多信息，请参阅[配置存活探针、就绪探针和启动探针](/zh-cn/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-grpc-liveness-probe)。
本文最初是为有关实现相同任务的外部工具所写。”

[gRPC](https://grpc.io) 将成为本地云微服务间进行通信的通用语言。如果您现在将 gRPC 应用程序部署到 Kubernetes，您可能会想要了解配置健康检查的最佳方法。在本文中，我们将介绍 [grpc-health-probe](https://github.com/grpc-ecosystem/grpc-health-probe/)，这是 Kubernetes 原生的健康检查 gRPC 应用程序的方法。

如果您不熟悉，Kubernetes的 [健康检查](/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/)（存活探针和就绪探针）可以使您的应用程序在睡眠时保持可用状态。当检测到没有回应的 Pod 时，会将其标记为不健康，并使这些 Pod 重新启动或重新安排。

Kubernetes 原本 [不支持](https://github.com/kubernetes/kubernetes/issues/21493) gRPC 健康检查。gRPC 的开发人员在 Kubernetes 中部署时可以采用以下三种方法：

[![当前在 kubernetes 上进行 gRPC 健康检查的选项](/images/blog/2019-09-30-health-checking-grpc/options.png)](/images/blog/2019-09-30-health-checking-grpc/options.png)


1.  **httpGet prob：** 不能与 gRPC 一起使用。您需要重构您的应用程序，必须同时支持 gRPC 和 HTTP/1.1 协议（在不同的端口号上）。
2.  **tcpSocket probe：** 打开 gRPC 服务器的 Socket 是没有意义的，因为它无法读取响应主体。
3.  **exec probe：** 将定期调用容器生态系统中的程序。对于 gRPC，这意味着您要自己实现健康 RPC，然后使用容器编写并交付客户端工具。

我们可以做得更好吗？这是肯定的。

## 介绍 “grpc-health-probe”

为了使上述 "exec probe" 方法标准化，我们需要：

- 可以在任何 gRPC 服务器中轻松实现的 **标准** 健康检查 "协议" 。
- 一种 **标准** 健康检查 "工具" ，可以轻松查询健康协议。

幸运的是，gRPC 具有 [标准的健康检查协议](https://github.com/grpc/grpc/blob/v1.15.0/doc/health-checking.md)。可以用任何语言轻松调用它。几乎所有实现 gRPC 的语言都附带了生成的代码和用于设置健康状态的实用程序。

如果您在 gRPC 应用程序中 [实现](https://github.com/grpc/grpc/blob/v1.15.0/src/proto/grpc/health/v1/health.proto) 此健康检查协议，那么可以使用标准或通用工具调用 `Check()` 方法来确定服务器状态。

接下来您需要的是 "标准工具" [**grpc-health-probe**](https://github.com/grpc-ecosystem/grpc-health-probe/)。

<a href='/images/blog/2019-09-30-health-checking-grpc/grpc_health_probe.png'>
    <img width="768"  title='grpc-health-probe on kubernetes'
        src='/images/blog/2019-09-30-health-checking-grpc/grpc_health_probe.png'/>
</a>

使用此工具，您可以在所有 gRPC 应用程序中使用相同的健康检查配置。这种方法有以下要求：

1.  用您喜欢的语言找到 gRPC 的 "健康" 模块并开始使用它（例如 [Go 库](https://godoc.org/github.com/grpc/grpc-go/health)）。
2.  将二进制文件 [grpc_health_probe](https://github.com/grpc-ecosystem/grpc-health-probe/) 送到容器中。
3.  [配置](https://github.com/grpc-ecosystem/grpc-health-probe/tree/1329d682b4232c102600b5e7886df8ffdcaf9e26#example-grpc-health-checking-on-kubernetes) Kubernetes 的 "exec" 检查模块来调用容器中的 "grpc_health_probe" 工具。

在这种情况下，执行 "grpc_health_probe" 将通过 `localhost` 调用您的 gRPC 服务器，因为它们位于同一个容器中。

## 下一步工作

**grpc-health-probe** 项目仍处于初期阶段，需要您的反馈。它支持多种功能，例如与 TLS 服务器通信和配置延时连接/RPC。

如果您最近要在 Kubernetes 上运行 gRPC 服务器，请尝试使用 gRPC Health Protocol，并在您的 Deployment 中尝试 grpc-health-probe，然后 [进行反馈](https://github.com/grpc-ecosystem/grpc-health-probe/)。

## 更多内容

- 协议： [GRPC Health Checking Protocol](https://github.com/grpc/grpc/blob/v1.15.0/doc/health-checking.md) ([health.proto](https://github.com/grpc/grpc/blob/v1.15.0/src/proto/grpc/health/v1/health.proto))
- 文档： [Kubernetes 存活和就绪探针](/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/)
- 文章： [升级版 Kubernetes 健康检查模式](https://ahmet.im/blog/advanced-kubernetes-health-checks/)
