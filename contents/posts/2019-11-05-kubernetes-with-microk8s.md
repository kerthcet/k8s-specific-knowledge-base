---
layout: blog
title: '使用 Microk8s 在 Linux 上本地运行 Kubernetes'
date: 2019-11-26
slug: running-kubernetes-locally-on-linux-with-microk8s
---

**作者**: [Ihor Dvoretskyi](https://twitter.com/idvoretskyi)，开发支持者，云原生计算基金会；[Carmine Rimi](https://twitter.com/carminerimi)
本文是关于 Linux 上的本地部署选项[系列](https://twitter.com/idvoretskyi)的第二篇，涵盖了 [MicroK8s](https://microk8s.io/)。Microk8s 是本地部署 Kubernetes 集群的 'click-and-run' 方案，最初由 Ubuntu 的发布者 Canonical 开发。
虽然 Minikube 通常为 Kubernetes 集群创建一个本地虚拟机（VM），但是 MicroK8s 不需要 VM。它使用[snap](https://snapcraft.io/) 包，这是一种应用程序打包和隔离技术。
这种差异有其优点和缺点。在这里，我们将讨论一些有趣的区别，并且基于 VM 的方法和非 VM 方法的好处。第一个因素是跨平台的移植性。虽然 Minikube VM 可以跨操作系统移植——它不仅支持 Linux，还支持 Windows、macOS、甚至 FreeBSD，但 Microk8s 需要 Linux，而且只在[那些支持 snaps](https://snapcraft.io/docs/installing-snapd) 的发行版上。支持大多数流行的 Linux 发行版。
另一个考虑到的因素是资源消耗。虽然 VM 设备为您提供了更好的可移植性，但它确实意味着您将消耗更多资源来运行 VM，这主要是因为 VM 提供了一个完整的操作系统，并且运行在管理程序之上。当 VM 处于休眠时你将消耗更多的磁盘空间。当它运行时，你将会消耗更多的 RAM 和 CPU。因为 Microk8s 不需要创建虚拟机，你将会有更多的资源去运行你的工作负载和其他设备。考虑到所占用的空间更小，MicroK8s 是物联网设备的理想选择-你甚至可以在 Paspberry Pi 和设备上使用它！
最后，项目似乎遵循了不同的发布节奏和策略。Microk8s 和 snaps 通常提供[渠道](https://snapcraft.io/docs/channels)允许你使用测试版和发布 KUbernetes 新版本的候选版本，同样也提供先前稳定版本。Microk8s 通常几乎立刻发布 Kubernetes 上游的稳定版本。
但是等等，还有更多！Minikube 和 Microk8s 都是作为单节点集群启动的。本质上来说，它们允许你用单个工作节点创建 Kubernetes 集群。这种情况即将改变 - MicroK8s 早期的 alpha 版本包括集群。有了这个能力，你可以创建正如你希望多的工作节点的 KUbernetes 集群。对于创建集群来说，这是一个没有主见的选项 - 开发者在节点之间创建网络连接和集成了其他所需要的基础设施，比如一个外部的负载均衡。总的来说，MicroK8s 提供了一种快速简易的方法，使得少量的计算机和虚拟机变成一个多节点的 Kubernetes 集群。以后我们将撰写更多这种体系结构的文章。
## 免责声明 

这不是 MicroK8s 官方介绍文档。你可以在它的官方[网页](https://microk8s.io/docs/)查询运行和使用 MicroK8s 的详情信息，其中覆盖了不同的用例，操作系统，环境等。相反，这篇文章的意图是提供在 Linux 上运行 MicroK8s 清晰易懂的指南。
## 前提条件 

一个[支持 snaps](https://snapcraft.io/docs/installing-snapd) 的 Linux 发行版是被需要的。这篇指南，我们将会用支持 snaps 且即开即用的 Ubuntu 18.04 LTS。如果你对运行在 Windows 或者 Mac 上的 MicroK8s 感兴趣，你应该检查[多通道](https://multipass.run)，安装一个快速的 Ubuntu VM，作为在你的系统上运行虚拟机 Ubuntu 的官方方式。
## MicroK8s 安装

简洁的 MicroK8s 安装：
```shell
sudo snap install microk8s --classic
```

<center>{{<figure width="600" src="/images/blog/2019-11-05-kubernetes-with-microk8s/001-install.png">}}</center>
以上的命令将会在几秒内安装一个本地单节点的 Kubernetes 集群。一旦命令执行结束，你的 Kubernetes 集群将会启动并运行。
```shell
sudo microk8s.status
```

<center>{{<figure width="600" src="/images/blog/2019-11-05-kubernetes-with-microk8s/002-status.png">}}</center>

## 使用 microk8s
使用 MicrosK8s 就像和安装它一样便捷。MicroK8s 本身包括一个 `kubectl` 库，该库可以通过执行 `microk8s.kubectl` 命令去访问。例如：
```shell
microk8s.kubectl get nodes
```

<center>{{<figure width="600" src="/images/blog/2019-11-05-kubernetes-with-microk8s/003-nodes.png">}}</center>

当使用前缀 `microk8s.kubectl` 时，允许在没有影响的情况下并行地安装另一个系统级的 kubectl，你可以便捷地使用 `snap alias` 命令摆脱它：
```shell
sudo snap alias microk8s.kubectl kubectl
```
<center>{{<figure width="600" src="/images/blog/2019-11-05-kubernetes-with-microk8s/004-alias.png">}}</center>

这将允许你以后便捷地使用 `kubectl`，你可以用 `snap unalias`命令恢复这个改变。
```shell
kubectl get nodes
```

<center>{{<figure width="600" src="/images/blog/2019-11-05-kubernetes-with-microk8s/005-nodes.png">}}</center>

## MicroK8s 插件
使用 MicroK8s 其中最大的好处之一事实上是也支持各种各样的插件和扩展。更重要的是它们是开箱即用的，用户仅仅需要启动它们。通过运行 `microk8s.status` 命令检查出扩展的完整列表。
```
sudo microk8s.status
```
截至到写这篇文章为止，MicroK8s 已支持以下插件：

<center>{{<figure width="600" src="/images/blog/2019-11-05-kubernetes-with-microk8s/006-status.png">}}</center>

社区创建和贡献了越来越多的插件，经常检查他们是十分有帮助的。
## 发布渠道
```shell
sudo snap info microk8s
```

<center>{{<figure width="600" src="/images/blog/2019-11-05-kubernetes-with-microk8s/010-releases.png">}}</center>

## 安装简单的应用 

在这篇指南中我将会用 NGINX 作为一个示例应用程序（[官方 Docker Hub 镜像](https://hub.docker.com/_/nginx)）。

```shell
kubectl create deployment nginx --image=nginx
```
为了检查安装，让我们运行以下命令：
```shell
kubectl get deployments
```

```shell
kubectl get pods
```

<center>{{<figure width="600" src="/images/blog/2019-11-05-kubernetes-with-microk8s/007-deployments.png">}}</center>

我们也可以检索出 Kubernetes 集群中所有可用对象的完整输出。
```shell
kubectl get all --all-namespaces
```

<center>{{<figure width="600" src="/images/blog/2019-11-05-kubernetes-with-microk8s/008-all.png">}}</center>

## 卸载 MircroK8s

卸载您的 microk8s 集群与卸载 Snap 同样便捷。
```shell
sudo snap remove microk8s
```

<center>{{<figure width="600" src="/images/blog/2019-11-05-kubernetes-with-microk8s/009-remove.png">}}</center>

## 截屏视频
[![asciicast](https://asciinema.org/a/263394.svg)](https://asciinema.org/a/263394)


