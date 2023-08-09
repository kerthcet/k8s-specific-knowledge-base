---
title: "容器"
weight: 40
description: 打包应用及其运行依赖环境的技术。
content_type: concept
---

每个运行的容器都是可重复的；
包含依赖环境在内的标准，意味着无论你在哪里运行它都会得到相同的行为。

容器将应用程序从底层的主机设施中解耦。
这使得在不同的云或 OS 环境中部署更加容易。

Kubernetes 集群中的每个{{< glossary_tooltip text="节点" term_id="node" >}}都会运行容器，
这些容器构成分配给该节点的 [Pod](/zh-cn/docs/concepts/workloads/pods/)。
单个 Pod 中的容器会在共同调度下，于同一位置运行在相同的节点上。


## 容器镜像 {#container-images}
[容器镜像](/zh-cn/docs/concepts/containers/images/)是一个随时可以运行的软件包，
包含运行应用程序所需的一切：代码和它需要的所有运行时、应用程序和系统库，以及一些基本设置的默认值。

容器旨在设计成无状态且[不可变的](https://glossary.cncf.io/immutable-infrastructure/)：
你不应更改已经运行的容器的代码。如果有一个容器化的应用程序需要修改，
正确的流程是：先构建包含更改的新镜像，再基于新构建的镜像重新运行容器。

## 容器运行时  {#container-runtimes}

{{< glossary_definition term_id="container-runtime" length="all" >}}

通常，你可以允许集群为一个 Pod 选择其默认的容器运行时。如果你需要在集群中使用多个容器运行时，
你可以为一个 Pod 指定 [RuntimeClass](/zh-cn/docs/concepts/containers/runtime-class/)，
以确保 Kubernetes 会使用特定的容器运行时来运行这些容器。

你还可以通过 RuntimeClass，使用相同的容器运行时，但使用不同设定的配置来运行不同的 Pod。
