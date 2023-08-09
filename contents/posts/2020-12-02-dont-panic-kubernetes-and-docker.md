---
layout: blog
title: "别慌: Kubernetes 和 Docker"
date: 2020-12-02
slug: dont-panic-kubernetes-and-docker
evergreen: true
---

**作者：** Jorge Castro, Duffie Cooley, Kat Cosgrove, Justin Garrison, Noah Kantrowitz, Bob Killen, Rey Lejano, Dan “POP” Papandrea, Jeffrey Sica, Davanum “Dims” Srinivas

**更新**：Kubernetes 通过 `dockershim` 对 Docker 的支持现已移除。
有关更多信息，请阅读[移除 FAQ](/zh-cn/dockershim)。
你还可以通过专门的 [GitHub issue](https://github.com/kubernetes/kubernetes/issues/106917) 讨论弃用。

Kubernetes 从版本 v1.20 之后，[弃用 Docker](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.20.md#deprecation)
这个容器运行时。

**不必慌张，这件事并没有听起来那么吓人。**

弃用 Docker 这个底层运行时，转而支持符合为 Kubernetes 创建的容器运行接口
[Container Runtime Interface (CRI)](https://kubernetes.io/blog/2016/12/container-runtime-interface-cri-in-kubernetes/)
的运行时。
Docker 构建的镜像，将在你的集群的所有运行时中继续工作，一如既往。

如果你是 Kubernetes 的终端用户，这对你不会有太大影响。
这事并不意味着 Docker 已死、也不意味着你不能或不该继续把 Docker 用作开发工具。
Docker 仍然是构建容器的利器，使用命令 `docker build` 构建的镜像在 Kubernetes 集群中仍然可以运行。

如果你正在使用 GKE、EKS、或 AKS 这类托管 Kubernetes 服务，
你需要在 Kubernetes 后续版本移除对 Docker 支持之前，
确认工作节点使用了被支持的容器运行时。
如果你的节点被定制过，你可能需要根据你自己的环境和运行时需求更新它们。
请与你的服务供应商协作，确保做出适当的升级测试和计划。

如果你正在运营你自己的集群，那还应该做些工作，以避免集群中断。
在 v1.20 版中，你仅会得到一个 Docker 的弃用警告。
当对 Docker 运行时的支持在 Kubernetes 某个后续发行版（<del>目前的计划是 2021 年晚些时候的 1.22 版</del>）中被移除时，
你需要切换到 containerd 或 CRI-O 等兼容的容器运行时。
只要确保你选择的运行时支持你当前使用的 Docker 守护进程配置（例如 logging）。

## 那为什么会有这样的困惑，为什么每个人要害怕呢？{#so-why-the-confusion-and-what-is-everyone-freaking-out-about}

我们在这里讨论的是两套不同的环境，这就是造成困惑的根源。
在你的 Kubernetes 集群中，有一个叫做容器运行时的东西，它负责拉取并运行容器镜像。
Docker 对于运行时来说是一个流行的选择（其他常见的选择包括 containerd 和 CRI-O），
但 Docker 并非设计用来嵌入到 Kubernetes，这就是问题所在。

你看，我们称之为 “Docker” 的物件实际上并不是一个物件——它是一个完整的技术堆栈，
它其中一个叫做 “containerd” 的部件本身，才是一个高级容器运行时。
Docker 既酷炫又实用，因为它提供了很多用户体验增强功能，而这简化了我们做开发工作时的操作，
Kubernetes 用不到这些增强的用户体验，毕竟它并非人类。

因为这个用户友好的抽象层，Kubernetes 集群不得不引入一个叫做 Dockershim 的工具来访问它真正需要的 containerd。
这不是一件好事，因为这引入了额外的运维工作量，而且还可能出错。
实际上正在发生的事情就是：Dockershim 将在不早于 v1.23 版中从 kubelet 中被移除，也就取消对 Docker 容器运行时的支持。
你心里可能会想，如果 containerd 已经包含在 Docker 堆栈中，为什么 Kubernetes 需要 Dockershim。

Docker 不兼容 CRI，
[容器运行时接口](https://kubernetes.io/blog/2016/12/container-runtime-interface-cri-in-kubernetes/)。
如果支持，我们就不需要这个 shim 了，也就没问题了。
但这也不是世界末日，你也不需要恐慌——你唯一要做的就是把你的容器运行时从 Docker 切换到其他受支持的容器运行时。

要注意一点：如果你依赖底层的 Docker 套接字(`/var/run/docker.sock`)，作为你集群中工作流的一部分，
切换到不同的运行时会导致你无法使用它。
这种模式经常被称之为嵌套 Docker（Docker in Docker）。
对于这种特殊的场景，有很多选项，比如：
[kaniko](https://github.com/GoogleContainerTools/kaniko)、
[img](https://github.com/genuinetools/img)、和
[buildah](https://github.com/containers/buildah)。

## 那么，这一改变对开发人员意味着什么？我们还要写 Dockerfile 吗？还能用 Docker 构建镜像吗？{#what-does-this-change-mean-for-developers}

此次改变带来了一个不同的环境，这不同于我们常用的 Docker 交互方式。
你在开发环境中用的 Docker 和你 Kubernetes 集群中的 Docker 运行时无关。
我们知道这听起来让人困惑。
对于开发人员，Docker 从所有角度来看仍然有用，就跟这次改变之前一样。
Docker 构建的镜像并不是 Docker 特有的镜像——它是一个
OCI（[开放容器标准](https://opencontainers.org/)）镜像。
任一 OCI 兼容的镜像，不管它是用什么工具构建的，在 Kubernetes 的角度来看都是一样的。
[containerd](https://containerd.io/) 和
[CRI-O](https://cri-o.io/)
两者都知道怎么拉取并运行这些镜像。
这就是我们制定容器标准的原因。

所以，改变已经发生。
它确实带来了一些问题，但这不是一个灾难，总的说来，这还是一件好事。
根据你操作 Kubernetes 的方式的不同，这可能对你不构成任何问题，或者也只是意味着一点点的工作量。
从一个长远的角度看，它使得事情更简单。
如果你还在困惑，也没问题——这里还有很多事情；
Kubernetes 有很多变化中的功能，没有人是100%的专家。
我们鼓励你提出任何问题，无论水平高低、问题难易。
我们的目标是确保所有人都能在即将到来的改变中获得足够的了解。
我们希望这已经回答了你的大部分问题，并缓解了一些焦虑！❤️

还在寻求更多答案吗？请参考我们附带的
[移除 Dockershim 的常见问题](/zh-cn/blog/2020/12/02/dockershim-faq/) _(2022年2月更新)_。
