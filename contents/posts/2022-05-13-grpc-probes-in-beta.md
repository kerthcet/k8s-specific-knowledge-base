---
layout: blog
title: "Kubernetes 1.24：gRPC 容器探针功能进入 Beta 阶段"
date: 2022-05-13
slug: grpc-probes-now-in-beta
---

**作者**：Sergey Kanzhelev (Google)

**译者**：Xiaoyang Zhang（Huawei）

在 Kubernetes 1.24 中，gRPC 探针（probe）功能进入了 beta 阶段，默认情况下可用。
现在，你可以为 gRPC 应用程序配置启动、活跃和就绪探测，而无需公开任何 HTTP 端点，
也不需要可执行文件。Kubernetes 可以通过 gRPC 直接连接到你的工作负载并查询其状态。

## 一些历史

让管理你的工作负载的系统检查应用程序是否健康、启动是否正常，以及应用程序是否认为自己可以接收流量，是很有用的。
在添加 gRPC 探针支持之前，Kubernetes 已经允许你通过从容器镜像内部运行可执行文件、发出 HTTP
请求或检查 TCP 连接是否成功来检查健康状况。

对于大多数应用程序来说，这些检查就足够了。如果你的应用程序提供了用于运行状况（或准备就绪）检查的
gRPC 端点，则很容易重新调整 `exec` 探针的用途，将其用于 gRPC 运行状况检查。
在博文[在 Kubernetes 上对 gRPC 服务器进行健康检查](/zh-cn/blog/2018/10/01/health-checking-grpc-servers-on-kubernetes/)中，
Ahmet Alp Balkan 描述了如何做到这一点 —— 这种机制至今仍在工作。

2018 年 8 月 21 日所[创建](https://github.com/grpc-ecosystem/grpc-health-probe/commit/2df4478982e95c9a57d5fe3f555667f4365c025d)的一种常用工具可以启用此功能，
工具于 [2018 年 9 月 19 日](https://github.com/grpc-ecosystem/grpc-health-probe/releases/tag/v0.1.0-alpha.1)首次发布。

这种 gRPC 应用健康检查的方法非常受欢迎。使用 GitHub 上的基本搜索，发现了带有 `grpc_health_probe`
的 [3,626 个 Dockerfile 文件](https://github.com/search?l=Dockerfile&q=grpc_health_probe&type=code)和
[6,621 个 yaml 文件](https://github.com/search?l=YAML&q=grpc_health_probe&type=Code)（在撰写本文时）。
这很好地表明了该工具的受欢迎程度，以及对其本地支持的需求。

Kubernetes v1.23 引入了一个 alpha 质量的实现，原生支持使用 gRPC 查询工作负载状态。
因为这是一个 alpha 特性，所以在 1.23 版中默认是禁用的。

## 使用该功能

我们用与其他探针类似的方式构建了 gRPC 健康检查，相信如果你熟悉 Kubernetes 中的其他探针类型，
它会[很容易使用](/zh-cn/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-grpc-liveness-probe)。
与涉及 `grpc_health_probe` 可执行文件的解决办法相比，原生支持的健康探针有许多好处。

有了原生 gRPC 支持，你不需要在镜像中下载和携带 `10MB` 的额外可执行文件。
Exec 探针通常比 gRPC 调用慢，因为它们需要实例化一个新进程来运行可执行文件。
当 Pod 在最大资源下运行并且在实例化新进程时遇到困难时，它还使得对边界情况的检查变得不那么智能。

不过有一些限制。由于为探针配置客户端证书很难，因此不支持依赖客户端身份验证的服务。
内置探针也不检查服务器证书，并忽略相关问题。

内置检查也不能配置为忽略某些类型的错误（`grpc_health_probe` 针对不同的错误返回不同的退出代码），
并且不能“串接”以在单个探测中对多个服务运行健康检查。

但是所有这些限制对于 gRPC 来说都是相当标准的，并且有简单的解决方法。

## 自己试试

### 集群级设置

你现在可以尝试这个功能。要尝试原生 gRPC 探针，你可以自己启动一个启用了
`GRPCContainerProbe` 特性门控的 Kubernetes 集群，可用的[工具](/zh-cn/docs/tasks/tools/)有很多。

由于特性门控 `GRPCContainerProbe` 在 1.24 版本中是默认启用的，因此许多供应商支持此功能开箱即用。
因此，你可以在自己选择的平台上创建 1.24 版本集群。一些供应商允许在 1.23 版本集群上启用 alpha 特性。

例如，在编写本文时，你可以在 GKE 上运行测试集群来进行快速测试。
其他供应商可能也有类似的功能，尤其是当你在 Kubernetes 1.24 版本发布很久后才阅读这篇博客时。

在 GKE 上使用以下命令（注意，版本是 `1.23`，并且指定了 `enable-kubernetes-alpha`）。

```shell
gcloud container clusters create test-grpc \
    --enable-kubernetes-alpha \
    --no-enable-autorepair \
    --no-enable-autoupgrade \
    --release-channel=rapid \
    --cluster-version=1.23
```

你还需要配置 kubectl 来访问集群：

```shell
gcloud container clusters get-credentials test-grpc
```

### 试用该功能

让我们创建 Pod 来测试 gRPC 探针是如何工作的。对于这个测试，我们将使用 `agnhost` 镜像。
这是一个 k8s 维护的镜像，可用于各种工作负载测试。例如，它有一个有用的
[grpc-health-checking](https://github.com/kubernetes/kubernetes/blob/b2c5bd2a278288b5ef19e25bf7413ecb872577a4/test/images/agnhost/README.md#grpc-health-checking)
模块，该模块暴露了两个端口：一个是提供健康检查服务的端口，另一个是对 `make-serving` 和
`make-not-serving` 命令做出反应的 http 端口。

下面是一个 Pod 定义示例。它启用 `grpc-health-checking` 模块，暴露 5000 和 8080 端口，并配置 gRPC 就绪探针：

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: test-grpc
spec:
  containers:
    - name: agnhost
      # 镜像自发布以来已更改（以前使用的仓库为 "k8s.gcr.io"）
      image: registry.k8s.io/e2e-test-images/agnhost:2.35
      command: ["/agnhost", "grpc-health-checking"]
      ports:
        - containerPort: 5000
        - containerPort: 8080
      readinessProbe:
        grpc:
          port: 5000
```

如果清单文件名为 `test.yaml`，你可以用以下命令创建 Pod，并检查它的状态。如输出片段所示，Pod 将处于就绪状态。

```shell
kubectl apply -f test.yaml
kubectl describe test-grpc
```

输出将包含如下内容：

```
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
```

现在让我们将健康检查端点状态更改为 `NOT_SERVING`。为了调用 Pod 的 http 端口，让我们创建一个端口转发：

```shell
kubectl port-forward test-grpc 8080:8080
```

你可以用 `curl` 来调用这个命令。

```shell
curl http://localhost:8080/make-not-serving
```

几秒钟后，端口状态将切换到未就绪。

```shell
kubectl describe pod test-grpc
```

现在的输出将显示：

```
Conditions:
  Type              Status
  Initialized       True
  Ready             False
  ContainersReady   False
  PodScheduled      True

...

  Warning  Unhealthy  2s (x6 over 42s)  kubelet            Readiness probe failed: service unhealthy (responded with "NOT_SERVING")
```

一旦切换回来，Pod 将在大约一秒钟后恢复到就绪状态：

```bash
curl http://localhost:8080/make-serving
kubectl describe test-grpc
```

输出表明 Pod 恢复为 `Ready`：

```
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
```

Kubernetes 上这种新的内置 gRPC 健康探测，使得通过 gRPC 实现健康检查比依赖使用额外的 `exec`
探测的旧方法更容易。请阅读官方
[文档](/zh-cn/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-grpc-liveness-probe)
了解更多信息并在该功能正式发布（GA）之前提供反馈。

## 总结

Kubernetes 是一个流行的工作负载编排平台，我们根据反馈和需求添加功能。
像 gRPC 探针支持这样的特性是一个小的改进，它将使许多应用程序开发人员的生活更容易，应用程序更有弹性。
在该功能 GA（正式发布）之前，现在就试试，并给出反馈。
