---
title: 容器环境
content_type: concept
weight: 20
---


本页描述了在容器环境里容器可用的资源。


## 容器环境  {#container-environment}

Kubernetes 的容器环境给容器提供了几个重要的资源：

* 文件系统，其中包含一个[镜像](/zh-cn/docs/concepts/containers/images/)
  和一个或多个的[卷](/zh-cn/docs/concepts/storage/volumes/)
* 容器自身的信息
* 集群中其他对象的信息

### 容器信息

一个容器的 **hostname** 是该容器运行所在的 Pod 的名称。通过 `hostname` 命令或者调用 libc 中的
[`gethostname`](https://man7.org/linux/man-pages/man2/gethostname.2.html) 函数可以获取该名称。

Pod 名称和命名空间可以通过
[下行 API](/zh-cn/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/)
转换为环境变量。

Pod 定义中的用户所定义的环境变量也可在容器中使用，就像在 container 镜像中静态指定的任何环境变量一样。

### 集群信息

创建容器时正在运行的所有服务都可用作该容器的环境变量。
这里的服务仅限于新容器的 Pod 所在的名字空间中的服务，以及 Kubernetes 控制面的服务。

对于名为 **foo** 的服务，当映射到名为 **bar** 的容器时，定义了以下变量：

```shell
FOO_SERVICE_HOST=<其上服务正运行的主机>
FOO_SERVICE_PORT=<其上服务正运行的端口>
```

服务具有专用的 IP 地址。如果启用了
[DNS 插件](https://releases.k8s.io/v{{< skew currentPatchVersion >}}/cluster/addons/dns/)，
可以在容器中通过 DNS 来访问服务。

## {{% heading "whatsnext" %}}

* 学习更多有关[容器生命周期回调](/zh-cn/docs/concepts/containers/container-lifecycle-hooks/)的知识。
* 动手[为容器的生命周期事件设置处理函数](/zh-cn/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/)。


