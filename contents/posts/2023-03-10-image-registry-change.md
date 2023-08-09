---
layout: blog
title: "k8s.gcr.io 重定向到 registry.k8s.io - 用户须知"
date: 2023-03-10T17:00:00.000Z
slug: image-registry-redirect
---

**作者**：Bob Killen (Google)、Davanum Srinivas (AWS)、Chris Short (AWS)、Frederico Muñoz (SAS
Institute)、Tim Bannister (The Scale Factory)、Ricky Sadowski (AWS)、Grace Nguyen (Expo)、Mahamed
Ali (Rackspace Technology)、Mars Toktonaliev（独立个人）、Laura Santamaria (Dell)、Kat Cosgrove
(Dell)

**译者**：Michael Yao (DaoCloud)

3 月 20 日星期一，k8s.gcr.io
仓库[被重定向到了社区拥有的仓库](https://kubernetes.io/blog/2022/11/28/registry-k8s-io-faster-cheaper-ga/)：
**registry.k8s.io** 。

## 长话短说：本次变更须知   {#you-need-to-know}

- 3 月 20 日星期一，来自 k8s.gcr.io 旧仓库的流量被重定向到了 registry.k8s.io，
  最终目标是逐步淘汰 k8s.gcr.io。
- 如果你在受限的环境中运行，且你为 k8s.gcr.io 限定采用了严格的域名或 IP 地址访问策略，
  那么 k8s.gcr.io 开始重定向到新仓库之后镜像拉取操作将不起作用。
- 少量非标准的客户端不会处理镜像仓库的 HTTP 重定向，将需要直接指向 registry.k8s.io。
- 本次重定向只是一个协助用户进行切换的权宜之计。弃用的 k8s.gcr.io 仓库将在某个时间点被淘汰。
  **请尽快更新你的清单，尽快指向 registry.k8s.io。**
- 如果你托管自己的镜像仓库，你可以将需要的镜像拷贝到自己的仓库，这样也能减少到社区所拥有仓库的流量压力。

如果你认为自己可能受到了影响，或如果你想知道本次变更的更多相关信息，请继续阅读下文。

## 若我受到影响该怎样检查？   {#how-can-i-check}

若要测试到 registry.k8s.io 的连通性，测试是否能够从 registry.k8s.io 拉取镜像，
可以在你所选的命名空间中执行类似以下的命令：

```shell
kubectl run hello-world -ti --rm --image=registry.k8s.io/busybox:latest --restart=Never -- date
```

当你执行上一条命令时，若一切工作正常，预期的输出如下：

```none
$ kubectl run hello-world -ti --rm --image=registry.k8s.io/busybox:latest --restart=Never -- date
Fri Feb 31 07:07:07 UTC 2023
pod "hello-world" deleted
```

## 若我受到影响会看到哪种错误？   {#what-kind-of-errors}

出现的错误可能取决于你正使用的容器运行时类别以及你被路由到的端点，
通常会出现 `ErrImagePull`、`ImagePullBackOff` 这类错误，
也可能容器创建失败时伴随着警告 `FailedCreatePodSandBox`。

以下举例的错误消息显示了由于未知的证书使得代理后的部署拉取失败：

```none
FailedCreatePodSandBox: Failed to create pod sandbox: rpc error: code = Unknown desc = Error response from daemon: Head “https://us-west1-docker.pkg.dev/v2/k8s-artifacts-prod/images/pause/manifests/3.8”: x509: certificate signed by unknown authority
```

## 哪些镜像会受影响？    {#what-images-be-impacted}

k8s.gcr.io 上的 **所有** 镜像都会受到本次变更的影响。
k8s.gcr.io 除了 Kubernetes 各个版本外还托管了许多镜像。
大量 Kubernetes 子项目也在其上托管了自己的镜像。
例如 `dns/k8s-dns-node-cache`、`ingress-nginx/controller` 和
`node-problem-detector/node-problem-detector` 这些镜像。

## 我受影响了。我该怎么办？   {#what-should-i-do}

若受影响的用户在受限的环境中运行，最好的办法是将必需的镜像拷贝到私有仓库，或在自己的仓库中配置一个直通缓存。
在仓库之间拷贝镜像可使用若干工具：
[crane](https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_copy.md)
就是其中一种工具，通过使用 `crane copy SRC DST` 可以将镜像拷贝到私有仓库。还有一些供应商特定的工具，例如 Google 的
[gcrane](https://cloud.google.com/container-registry/docs/migrate-external-containers#copy)，
这个工具实现了类似的功能，但针对其平台自身做了一些精简。

## 我怎样才能找到哪些镜像正使用旧仓库，如何修复？    {#how-can-i-find-and-fix}

**方案 1**：
试试[上一篇博文](https://kubernetes.io/blog/2023/02/06/k8s-gcr-io-freeze-announcement/#what-s-next)中所述的一条
kubectl 命令：

```shell
kubectl get pods --all-namespaces -o jsonpath="{.items[*].spec.containers[*].image}" |\
tr -s '[[:space:]]' '\n' |\
sort |\
uniq -c
```

**方案 2**：`kubectl` [krew](https://krew.sigs.k8s.io/) 的一个插件已被开发完成，名为
[`community-images`](https://github.com/kubernetes-sigs/community-images#kubectl-community-images)，
它能够使用 k8s.gcr.io 端点扫描和报告所有正使用 k8s.gcr.io 的镜像。

如果你安装了 krew，你可以运行以下命令进行安装：

```shell
kubectl krew install community-images
```

并用以下命令生成一个报告：

```shell
kubectl community-images
```

对于安装和示例输出的其他方法，可以查阅代码仓库：
[kubernetes-sigs/community-images](https://github.com/kubernetes-sigs/community-images)。

**方案 3**：如果你不能直接访问集群，或如果你管理了许多集群，最好的方式是在清单（manifest）和
Chart 中搜索 **"k8s.gcr.io"**。

**方案 4**：如果你想预防基于 k8s.gcr.io 的镜像在你的集群中运行，可以在
[AWS EKS 最佳实践代码仓库](https://github.com/aws/aws-eks-best-practices/tree/master/policies/k8s-registry-deprecation)中找到针对
[Gatekeeper](https://open-policy-agent.github.io/gatekeeper-library/website/)
和 [Kyverno](https://kyverno.io/) 的示例策略，这些策略可以阻止镜像被拉取。
你可以在任何 Kubernetes 集群中使用这些第三方策略。

**方案 5**：作为 **最后一个** 备选方案，
你可以使用[修改性质的准入 Webhook](/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/#what-are-admission-webhooks)
来动态更改镜像地址。在更新你的清单之前这只应视为一个权宜之计。你可以在
[k8s-gcr-quickfix](https://github.com/abstractinfrastructure/k8s-gcr-quickfix)
中找到（第三方）可变性质的 Webhook 和 Kyverno 策略。

## 为什么 Kubernetes 要换到一个全新的镜像仓库？   {#why-did-k8s-change-registry}

k8s.gcr.io 托管在一个 [Google Container Registry (GCR)](https://cloud.google.com/container-registry)
自定义的域中，这是专为 Kubernetes 项目搭建的域。自 Kubernetes 项目启动以来，
这个仓库一直运作良好，我们感谢 Google 提供这些资源，然而如今还有其他云提供商和供应商希望托管这些镜像，
以便为他们自己云平台上的用户提供更好的体验。除了去年 Google
[捐赠 300 万美金的续延承诺](https://www.cncf.io/google-cloud-recommits-3m-to-kubernetes/)来支持本项目的基础设施外，
Amazon Web Services (AWS) 也在[底特律召开的 Kubecon NA 2022 上发言](https://youtu.be/PPdimejomWo?t=236)公布了相当的捐赠金额。
AWS 能为用户提供更好的体验（距离用户更近的服务器 = 更快的下载速度），同时还能减轻 GCR 的出站带宽和成本。

有关此次变更的更多详情，请查阅
[registry.k8s.io：更快、成本更低且正式发布 (GA)](/blog/2022/11/28/registry-k8s-io-faster-cheaper-ga/)。

## 为什么要设置重定向？   {#why-is-a-redirect}

本项目在[去年发布 1.25 时切换至 registry.k8s.io](/blog/2022/11/28/registry-k8s-io-faster-cheaper-ga/)；
然而，大多数镜像拉取流量仍被重定向到旧端点 k8s.gcr.io。
从项目角度看，这对我们来说是不可持续的，因为这样既没有完全利用其他供应商捐赠给本项目的资源，
也由于流量服务成本而使我们面临资金耗尽的危险。

重定向将使本项目能够利用这些新资源的优势，从而显著降低我们的出站带宽成本。
我们预计此次更改只会影响一小部分用户，他们可能在受限环境中运行 Kubernetes，
或使用了老旧到无法处理重定向行为的客户端。

## k8s.gcr.io 将会怎样？   {#what-will-happen-to-k8s-gcr-io}

除了重定向之外，k8s.gcr.io 将被冻结，
[且在 2023 年 4 月 3 日之后将不会随着新的镜像而更新](/zh-cn/blog/2023/02/06/k8s-gcr-io-freeze-announcement/)。
`k8s.gcr.io` 将不再获取任何新的版本、补丁或安全更新。
这个旧仓库将继续保持可用，以帮助人们迁移，但在以后将会被彻底淘汰。

## 我仍有疑问，我该去哪儿询问？   {#what-should-i-go}

有关 registry.k8s.io 及其为何开发这个新仓库的更多信息，请参见
[registry.k8s.io：更快、成本更低且正式发布](/blog/2022/11/28/registry-k8s-io-faster-cheaper-ga/)。

如果你想了解镜像冻结以及最后一版可用镜像的更多信息，请参见博文：
[k8s.gcr.io 镜像仓库将从 2023 年 4 月 3 日起被冻结](/zh-cn/blog/2023/02/06/k8s-gcr-io-freeze-announcement/)。

有关 registry.k8s.io
架构及其[请求处理决策树](https://github.com/kubernetes/registry.k8s.io/blob/8408d0501a88b3d2531ff54b14eeb0e3c900a4f3/cmd/archeio/docs/request-handling.md)的信息，
请查阅 [kubernetes/registry.k8s.io 代码仓库](https://github.com/kubernetes/registry.k8s.io)。

若你认为自己在使用新仓库和重定向时遇到 bug，请在
[kubernetes/registry.k8s.io 代码仓库](https://github.com/kubernetes/registry.k8s.io/issues/new/choose)中提出 Issue。
**请先检查是否有人提出了类似的 Issue，再行创建新 Issue。**
