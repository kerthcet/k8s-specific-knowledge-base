---
layout: blog
title: "Kubernetes 1.27: 原地调整 Pod 资源 (alpha)"
date: 2023-05-12
slug: in-place-pod-resize-alpha
---

**作者:** Vinay Kulkarni (Kubescaler Labs)

**译者**：[Paco Xu](https://github.com/pacoxu) (Daocloud)

如果你部署的 Pod 设置了 CPU 或内存资源，你就可能已经注意到更改资源值会导致 Pod 重新启动。
以前，这对于运行的负载来说是一个破坏性的操作。

在 Kubernetes v1.27 中，我们添加了一个新的 alpha 特性，允许用户调整分配给 Pod 的
CPU 和内存资源大小，而无需重新启动容器。 首先，API 层面现在允许修改 Pod 容器中的
`resources` 字段下的 `cpu` 和 `memory` 资源。资源修改只需 patch 正在运行的 pod
规约即可。

这也意味着 Pod 定义中的 `resource` 字段不能再被视为 Pod 实际资源的指标。监控程序必须
查看 Pod 状态中的新字段来获取实际资源状况。Kubernetes 通过 CRI（Container Runtime
Interface，容器运行时接口）API 调用运行时（例如 containerd）来查询实际的 CPU 和内存
的请求和限制。容器运行时的响应会反映在 Pod 的状态中。

此外，Pod 中还添加了对应于资源调整的新字段 `restartPolicy`。这个字段使用户可以控制在资
源调整时容器的行为。

## 1.27 版本有什么新内容?

除了在 Pod 规范中添加调整策略之外，还在 Pod 状态中的 `containerStatuses` 中添加了一个名为
`allocatedResources` 的新字段。该字段反映了分配给 Pod 容器的节点资源。

此外，容器状态中还添加了一个名为 `resources` 的新字段。该字段反映的是如同容器运行时所报告的、
针对正运行的容器配置的实际资源 requests 和 limits。

最后，Pod 状态中添加了新字段 `resize`。`resize` 字段显示上次请求待处理的调整状态。
此字段可以具有以下值：

- Proposed：此值表示请求调整已被确认，并且请求已被验证和记录。
- InProgress：此值表示节点已接受调整请求，并正在将其应用于 Pod 的容器。
- Deferred：此值意味着在此时无法批准请求的调整，节点将继续重试。 当其他 Pod 退出并释放节点资源时，调整可能会被真正实施。
- Infeasible：此值是一种信号，表示节点无法承接所请求的调整值。 如果所请求的调整超过节点可分配给 Pod 的最大资源，则可能会发生这种情况。

## 何时使用此功能？

以下是此功能可能有价值的一些示例：

- 正在运行的 Pod 资源限制或者请求过多或过少。
- 一些过度预配资源的 Pod 调度到某个节点，会导致资源利用率较低的集群上因为
  CPU 或内存不足而无法调度 Pod。
- 驱逐某些需要较多资源的有状态 Pod 是一项成本较高或破坏性的操作。
  这种场景下，缩小节点中的其他优先级较低的 Pod 的资源，或者移走这些 Pod 的成本更低。

## 如何使用这个功能

在 v1.27 中使用此功能，必须启用 `InPlacePodVerticalScaling` 特性门控。
可以如下所示启动一个启用了此特性的本地集群：

```
root@vbuild:~/go/src/k8s.io/kubernetes# FEATURE_GATES=InPlacePodVerticalScaling=true ./hack/local-up-cluster.sh
go version go1.20.2 linux/arm64
+++ [0320 13:52:02] Building go targets for linux/arm64
    k8s.io/kubernetes/cmd/kubectl (static)
    k8s.io/kubernetes/cmd/kube-apiserver (static)
    k8s.io/kubernetes/cmd/kube-controller-manager (static)
    k8s.io/kubernetes/cmd/cloud-controller-manager (non-static)
    k8s.io/kubernetes/cmd/kubelet (non-static)
...
...
Logs:
  /tmp/etcd.log
  /tmp/kube-apiserver.log
  /tmp/kube-controller-manager.log

  /tmp/kube-proxy.log
  /tmp/kube-scheduler.log
  /tmp/kubelet.log

To start using your cluster, you can open up another terminal/tab and run:

  export KUBECONFIG=/var/run/kubernetes/admin.kubeconfig
  cluster/kubectl.sh

# Alternatively, you can write to the default kubeconfig:

  export KUBERNETES_PROVIDER=local

  cluster/kubectl.sh config set-cluster local --server=https://localhost:6443 --certificate-authority=/var/run/kubernetes/server-ca.crt
  cluster/kubectl.sh config set-credentials myself --client-key=/var/run/kubernetes/client-admin.key --client-certificate=/var/run/kubernetes/client-admin.crt
  cluster/kubectl.sh config set-context local --cluster=local --user=myself
  cluster/kubectl.sh config use-context local
  cluster/kubectl.sh

```

一旦本地集群启动并运行，Kubernetes 用户就可以调度带有资源配置的 pod，并通过 kubectl 调整 pod
的资源。 以下演示视频演示了如何使用此功能的示例。

{{< youtube id="1m2FOuB6Bh0" title="原地调整 Pod CPU 或内存资源">}}

## 示例用例

### 云端开发环境

在这种场景下，开发人员或开发团队在本地编写代码，但在和生产环境资源配置相同的 Kubernetes pod 中的
构建和测试代码。当开发人员编写代码时，此类 Pod 需要最少的资源，但在构建代码或运行一系列测试时需要
更多的 CPU 和内存。 这个用例可以利用原地调整 pod 资源的功能（在 eBPF 的一点帮助下）快速调整 pod
资源的大小，并避免内核 OOM（内存不足）Killer 终止其进程。

[KubeCon North America 2022 会议演讲](https://www.youtube.com/watch?v=jjfa1cVJLwc)中详细介绍了上述用例。

### Java进程初始化CPU要求

某些 Java 应用程序在初始化期间 CPU 资源使用量可能比正常进程操作期间所需的 CPU 资源多很多。
如果此类应用程序指定适合正常操作的 CPU 请求和限制，会导致程序启动时间很长。这样的 pod
可以在创建 pod 时请求更高的 CPU 值。在应用程序完成初始化后，降低资源配置仍然可以正常运行。

## 已知问题

该功能在 v1.27 中仍然是 [alpha 阶段](/docs/reference/command-line-tools-reference/feature-gates/#feature-stages).
以下是用户可能会遇到的一些已知问题：

- containerd v1.6.9 以下的版本不具备此功能的所需的 CRI 支持，无法完成端到端的闭环。
尝试调整 Pod 大小将显示为卡在 `InProgress` 状态，并且 Pod 状态中的 `resources`
字段永远不会更新，即使新资源配置可能已经在正在运行的容器上生效了。
- Pod 资源调整可能会遇到与其他 Pod 更新的冲突，导致 pod 资源调整操作被推迟。
- 可能需要一段时间才能在 Pod 的状态中反映出调整后的容器资源。
- 此特性与静态 CPU 管理策略不兼容。

## 致谢

此功能是 Kubernetes 社区高度协作努力的结果。这里是对在这个功能实现过程中，贡献了很多帮助的一部分人的一点点致意。

- [@thockin](https://github.com/thockin) 如此细致的 API 设计和严密的代码审核。
- [@derekwaynecarr](https://github.com/derekwaynecarr) 设计简化和 API & Node 代码审核。
- [@dchen1107](https://github.com/dchen1107) 介绍了 Borg 的大量知识，帮助我们避免落入潜在的陷阱。
- [@ruiwen-zhao](https://github.com/ruiwen-zhao) 增加 containerd 支持，使得 E2E 能够闭环。
- [@wangchen615](https://github.com/wangchen615) 实现完整的 E2E 测试并推进调度问题修复。
- [@bobbypage](https://github.com/bobbypage) 提供宝贵的帮助，让 CI 准备就绪并快速排查问题，尤其是在我休假时。
- [@Random-Liu](https://github.com/Random-Liu) kubelet 代码审查以及定位竞态条件问题。
- [@Huang-Wei](https://github.com/Huang-Wei), [@ahg-g](https://github.com/ahg-g), [@alculquicondor](https://github.com/alculquicondor) 帮助完成调度部分的修改。
- [@mikebrow](https://github.com/mikebrow) [@marosset](https://github.com/marosset) 帮助我在 v1.25 代码审查并最终合并 CRI 部分的修改。
- [@endocrimes](https://github.com/endocrimes), [@ehashman](https://github.com/ehashman) 帮助确保经常被忽视的测试处于良好状态。
- [@mrunalp](https://github.com/mrunalp) cgroupv2 部分的代码审查并保证了 v1 和 v2 的清晰处理。
- [@liggitt](https://github.com/liggitt), [@gjkim42](https://github.com/gjkim42) 在合并代码后，帮助追踪遗漏的重要问题的根因。
- [@SergeyKanzhelev](https://github.com/SergeyKanzhelev) 在冲刺阶段支持和解决各种问题。
- [@pdgetrf](https://github.com/pdgetrf) 完成了第一个原型。
- [@dashpole](https://github.com/dashpole) 让我快速了解 Kubernetes 的做事方式。
- [@bsalamat](https://github.com/bsalamat), [@kgolab](https://github.com/kgolab) 在早期阶段提供非常周到的见解和建议。
- [@sftim](https://github.com/sftim), [@tengqm](https://github.com/tengqm) 确保文档易于理解。
- [@dims](https://github.com/dims) 无所不在并帮助在关键时刻进行合并。
- 发布团队确保了项目保持健康。

非常感谢我非常支持的管理层 [Xiaoning Ding 博士](https://www.linkedin.com/in/xiaoningding/) 和
[Ying Xiong 博士](https://www.linkedin.com/in/ying-xiong-59a2482/)，感谢他们的耐心和鼓励。

## 参考

### 应用程序开发者参考

- [调整分配给容器的 CPU 和内存资源](/zh-cn/docs/tasks/configure-pod-container/resize-container-resources/)
- [为容器和 Pod 分配内存资源](/zh-cn/docs/tasks/configure-pod-container/assign-memory-resource/)
- [为容器和 Pod 分配 CPU 资源](/zh-cn/docs/tasks/configure-pod-container/assign-cpu-resource/)

### 集群管理员参考

- [为命名空间配置默认的内存请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)
- [为命名空间配置默认的 CPU 请求和限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/)
