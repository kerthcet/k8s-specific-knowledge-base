---
layout: blog
title: "Kubernetes 的取证容器检查点"
date: 2022-12-05
slug: forensic-container-checkpointing-alpha
---

**作者:** [Adrian Reber](https://github.com/adrianreber) (Red Hat)

取证容器检查点（Forensic container checkpointing）基于 [CRIU][criu]（Checkpoint/Restore In Userspace ，用户空间的检查点/恢复），
并允许创建正在运行的容器的有状态副本，而容器不知道它正在被检查。容器的副本，可以在沙箱环境中被多次分析和恢复，而原始容器并不知道。
取证容器检查点是作为一个 alpha 特性在 Kubernetes v1.25 中引入的。

## 工作原理

在 CRIU 的帮助下，检查（checkpoint）和恢复容器成为可能。CRIU 集成在 runc、crun、CRI-O 和 containerd 中，
而在 Kubernetes 中实现的取证容器检查点使用这些现有的 CRIU 集成。

## 这一特性为何重要？

借助 CRIU 和相应的集成，可以获得磁盘上正在运行的容器的所有信息和状态，供以后进行取证分析。
取证分析对于在不阻止或影响可疑容器的情况下，对其进行检查可能很重要。如果容器确实受到攻击，攻击者可能会检测到检查容器的企图。
获取检查点并在沙箱环境中分析容器，提供了在原始容器和可能的攻击者不知道检查的情况下检查容器的可能性。

除了取证容器检查点用例，还可以在不丢失内部状态的情况下，将容器从一个节点迁移到另一个节点。
特别是对于初始化时间长的有状态容器，从检查点恢复，可能会节省重新启动后的时间，或者实现更快的启动时间。

## 如何使用容器检查点？

该功能在[特性门控][container-checkpoint-feature-gate]后面，因此在使用这个新功能之前，
请确保启用了 ContainerCheckpoint 特性门控。


运行时还必须支持容器检查点：

* containerd：相关支持目前正在讨论中。有关更多详细信息，请参见 [containerd pull request #6965][containerd-checkpoint-restore-pr]。
* CRI-O：v1.25 支持取证容器检查点。

## CRI-O 的使用示例

要将取证容器检查点与 CRI-O 结合使用，需要使用命令行选项--enable-criu-support=true 启动运行时。
Kubernetes 方面，你需要在启用 ContainerCheckpoint 特性门控的情况下运行你的集群。
由于检查点功能是由 CRIU 提供的，因此也有必要安装 CRIU。
通常 runc 或 crun 依赖于 CRIU，因此它是自动安装的。

值得一提的是，在编写本文时，检查点功能被认为是 CRI-O 和 Kubernetes 中的一个 alpha 级特性，其安全影响仍在评估之中。

一旦容器和 pod 开始运行，就可以创建一个检查点。[检查点][kubelet-checkpoint-api]目前只在 **kubelet** 级别暴露。
要检查一个容器，可以在运行该容器的节点上运行 curl，并触发一个检查点：

```shell
curl -X POST "https://localhost:10250/checkpoint/namespace/podId/container"
```

对于 **default** 命名空间中 **counters** Pod 中名为 **counter** 的容器，可通过以下方式访问 **kubelet** API 端点：

```shell
curl -X POST "https://localhost:10250/checkpoint/default/counters/counter"
```

为了完整起见，以下 `curl` 命令行选项对于让 `curl` 接受 **kubelet** 的自签名证书并授权使用
**kubelet** 检查点 API 是必要的：

```shell
--insecure --cert /var/run/kubernetes/client-admin.crt --key /var/run/kubernetes/client-admin.key
```

触发这个 **kubelet** API 将从 CRI-O 请求创建一个检查点，CRI-O 从你的低级运行时（例如 `runc`）请求一个检查点。
看到这个请求，`runc` 调用 `criu` 工具来执行实际的检查点操作。

检查点操作完成后，检查点应该位于
`/var/lib/kubelet/checkpoints/checkpoint-<pod-name>_<namespace-name>-<container-name>-<timestamp>.tar`

然后，你可以使用 tar 归档文件在其他地方恢复容器。

### 在 Kubernetes 外恢复检查点容器（使用 CRI-O）

使用检查点 tar 归档文件，可以在 Kubernetes 之外的 CRI-O 沙箱实例中恢复容器。
为了在恢复过程中获得更好的用户体验，建议你使用 CRI-O GitHub 的 **main** 分支中最新版本的 CRI-O。
如果你使用的是 CRI-O v1.25，你需要在启动容器之前手动创建 Kubernetes 会创建的某些目录。
在 Kubernetes 外恢复容器的第一步是使用 **crictl** 创建一个 pod 沙箱：

```shell
crictl runp pod-config.json
```

然后，你可以将之前的检查点容器恢复到新创建的 pod 沙箱中：

```shell
crictl create <POD_ID> container-config.json pod-config.json
```

你不需要在 container-config.json 的注册表中指定容器镜像，而是需要指定你之前创建的检查点归档文件的路径：

```json
{
  "metadata": {
      "name": "counter"
  },
  "image":{
      "image": "/var/lib/kubelet/checkpoints/<checkpoint-archive>.tar"
  }
}
```

接下来，运行 crictl start <CONTAINER_ID>来启动该容器，然后应该会运行先前检查点容器的副本。

### 在 Kubernetes 中恢复检查点容器

要在 Kubernetes 中直接恢复之前的检查点容器，需要将检查点归档文件转换成可以推送到注册中心的镜像。

转换本地检查点存档的一种方法包括在 [buildah][buildah] 的帮助下执行以下步骤：

```shell
newcontainer=$(buildah from scratch)
buildah add $newcontainer /var/lib/kubelet/checkpoints/checkpoint-<pod-name>_<namespace-name>-<container-name>-<timestamp>.tar /
buildah config --annotation=io.kubernetes.cri-o.annotations.checkpoint.name=<container-name> $newcontainer
buildah commit $newcontainer checkpoint-image:latest
buildah rm $newcontainer
```

生成的镜像未经标准化，只能与 CRI-O 结合使用。请将此镜像格式视为 pre-alpha 格式。
社区正在[讨论][image-spec-discussion]如何标准化这样的检查点镜像格式。
重要的是要记住，这种尚未标准化的镜像格式只有在 CRI-O 已经用`--enable-criu-support=true` 启动时才有效。
在 CRIU 支持下启动 CRI-O 的安全影响尚不清楚，因此应谨慎使用功能和镜像格式。

现在，你需要将该镜像推送到容器镜像注册中心。例如：

```shell
buildah push localhost/checkpoint-image:latest container-image-registry.example/user/checkpoint-image:latest
```

要恢复此检查点镜像（container-image-registry.example/user/checkpoint-image:latest），
该镜像需要在 Pod 的规约中列出。下面是一个清单示例：

```yaml
apiVersion: v1
kind: Pod
metadata:
  namePrefix: example-
spec:
  containers:
  - name: <container-name>
    image: container-image-registry.example/user/checkpoint-image:latest
  nodeName: <destination-node>
```

Kubernetes 将新的 Pod 调度到一个节点上。该节点上的 kubelet 指示容器运行时（本例中为 CRI-O）
基于指定为 `registry/user/checkpoint-image:latest` 的镜像创建并启动容器。
CRI-O 检测到 `registry/user/checkpoint-image:latest` 是对检查点数据的引用，而不是容器镜像。
然后，与创建和启动容器的通常步骤不同，CRI-O 获取检查点数据，并从指定的检查点恢复容器。

该 Pod 中的应用程序将继续运行，就像检查点未被获取一样；在该容器中，
应用程序的外观和行为，与正常启动且未从检查点恢复的任何其他容器相似。

通过这些步骤，可以用在不同节点上运行的新的等效 Pod，替换在一个节点上运行的 Pod，而不会丢失该 Pod中容器的状态。

## 如何参与？

你可以通过多种方式参与 SIG Node：

* Slack: [#sig-node][sig-node]
* [Mailing list][Mailing list]

## 延伸阅读

有关如何分析容器检查点的详细信息，请参阅后续文章[取证容器分析][forensic-container-analysis]。

[forensic-container-analysis]: /zh-cn/blog/2023/03/10/forensic-container-analysis/
[criu]: https://criu.org/
[containerd-checkpoint-restore-pr]: https://github.com/containerd/containerd/pull/6965
[container-checkpoint-feature-gate]: https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/
[image-spec-discussion]: <https://github.com/opencontainers/image-spec/issues/962>
[kubelet-checkpoint-api]: <https://kubernetes.io/docs/reference/node/kubelet-checkpoint-api/>
[buildah]: <https://buildah.io/>
[sig-node]: <https://kubernetes.slack.com/messages/sig-node>
[Mailing list]: <https://groups.google.com/forum/#!forum/kubernetes-sig-node>
