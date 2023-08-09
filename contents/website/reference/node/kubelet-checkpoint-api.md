---
content_type: "reference"
title: Kubelet Checkpoint API
weight: 10
---

{{< feature-state for_k8s_version="v1.25" state="alpha" >}}

为容器生成检查点这个功能可以为一个正在运行的容器创建有状态的拷贝。
一旦容器有一个有状态的拷贝，你就可以将其移动到其他计算机进行调试或类似用途。

如果你将通过检查点操作生成的容器数据移动到能够恢复该容器的一台计算机，
所恢复的容器将从之前检查点操作执行的时间点继续运行。
你也可以检视所保存的数据，前提是你拥有这类操作的合适工具。

创建容器的检查点可能会产生安全隐患。
通常，一个检查点包含执行检查点操作时容器中所有进程的所有内存页。
这意味着以前存在于内存中的一切内容现在都在本地磁盘上获得。
这里的内容包括一切私密数据和可能用于加密的密钥。
底层 CRI 实现（该节点上的容器运行时）应创建只有 `root` 用户可以访问的检查点存档。
另外重要的是记住：如果检查点存档被转移到另一个系统，该检查点存档的所有者将可以读取所有内存页。

## 操作 {#operations}

### `post` 对指定的容器执行检查点操作    {#post-checkpoint}

告知 kubelet 对指定 Pod 中的特定容器执行检查点操作。

查阅 [Kubelet 身份验证/鉴权参考](/zh-cn/docs/reference/access-authn-authz/kubelet-authn-authz)了解如何控制对
kubelet 检查点接口的访问。

Kubelet 将对底层 {{<glossary_tooltip term_id="cri" text="CRI">}} 实现请求执行检查点操作。
在该检查点请求中，Kubelet 将检查点存档的名称设置为 `checkpoint-<pod 全称>-<容器名称>-<时间戳>.tar`，
还会请求将该检查点存档存储到其根目录（由 `--root-dir` 定义）下的 `checkpoints` 子目录中。
这个目录默认为 `/var/lib/kubelet/checkpoints`。

检查点存档的格式为 **tar**，可以使用 [`tar`](https://pubs.opengroup.org/onlinepubs/7908799/xcu/tar.html)
的一种实现来读取。存档文件的内容取决于底层 CRI 实现（该节点的容器运行时）。

#### HTTP 请求 {#post-checkpoint-request}

POST /checkpoint/{namespace}/{pod}/{container}

#### 参数 {#post-checkpoint-params}

- **namespace** (**路径参数**)：string，必需

  {{< glossary_tooltip term_id="namespace" >}}

- **pod** (**路径参数**)：string，必需

  {{< glossary_tooltip term_id="pod" >}}

- **container** (**路径参数**)：string，必需

  {{< glossary_tooltip term_id="container" >}}

- **timeout** (**查询参数**)：integer


  等待检查点创建完成的超时时间（单位为秒）。
  如果超时值为零或未设定，将使用默认的 {{<glossary_tooltip term_id="cri" text="CRI">}} 超时时间值。
  生成检查点所需的时长直接取决于容器所用的内存。容器使用的内存越多，创建相应检查点所需的时间越长。

#### 响应 {#post-checkpoint-response}

200: OK

401: Unauthorized

404: Not Found（如果 `ContainerCheckpoint` 特性门控被禁用）

404: Not Found（如果指定的 `namespace`、`pod` 或 `container` 无法被找到）

500: Internal Server Error（如果执行检查点操作期间 CRI 实现遇到一个错误（参阅错误消息了解更多细节））

500: Internal Server Error（如果 CRI 实现未实现检查点 CRI API（参阅错误消息了解更多细节））

{{< comment >}}
TODO：一旦 CRI 实现具有检查点/恢复能力，就会添加有关返回码的更多信息。
      这个 TODO 在发布之前无法被修复，因为 CRI 实现需要先合并对 Kubernetes 的变更，
      才能实现新的 ContainerCheckpoint CRI API 调用。我们需要等到 1.25 发布后才能修复此问题。
{{< /comment >}}
