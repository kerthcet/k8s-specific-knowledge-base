---
title: Pod 开销
content_type: concept
weight: 30
---



{{< feature-state for_k8s_version="v1.24" state="stable" >}}


在节点上运行 Pod 时，Pod 本身占用大量系统资源。这些是运行 Pod 内容器所需资源之外的资源。
在 Kubernetes 中，_POD 开销_ 是一种方法，用于计算 Pod 基础设施在容器请求和限制之上消耗的资源。




在 Kubernetes 中，Pod 的开销是根据与 Pod 的 [RuntimeClass](/zh-cn/docs/concepts/containers/runtime-class/)
相关联的开销在[准入](/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/#what-are-admission-webhooks)时设置的。


在调度 Pod 时，除了考虑容器资源请求的总和外，还要考虑 Pod 开销。
类似地，kubelet 将在确定 Pod cgroups 的大小和执行 Pod 驱逐排序时也会考虑 Pod 开销。

## 配置 Pod 开销 {#set-up}

你需要确保使用一个定义了 `overhead` 字段的 `RuntimeClass`。

## 使用示例

要使用 Pod 开销，你需要一个定义了 `overhead` 字段的 RuntimeClass。
作为例子，下面的 RuntimeClass 定义中包含一个虚拟化所用的容器运行时，
RuntimeClass 如下，其中每个 Pod 大约使用 120MiB 用来运行虚拟机和寄宿操作系统：

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: kata-fc
handler: kata-fc
overhead:
  podFixed:
    memory: "120Mi"
    cpu: "250m"
```

通过指定 `kata-fc` RuntimeClass 处理程序创建的工作负载会将内存和 CPU
开销计入资源配额计算、节点调度以及 Pod cgroup 尺寸确定。

假设我们运行下面给出的工作负载示例 test-pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  runtimeClassName: kata-fc
  containers:
  - name: busybox-ctr
    image: busybox:1.28
    stdin: true
    tty: true
    resources:
      limits:
        cpu: 500m
        memory: 100Mi
  - name: nginx-ctr
    image: nginx
    resources:
      limits:
        cpu: 1500m
        memory: 100Mi
```

在准入阶段 RuntimeClass [准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/)
更新工作负载的 PodSpec 以包含
RuntimeClass 中定义的 `overhead`。如果 PodSpec 中已定义该字段，该 Pod 将会被拒绝。
在这个例子中，由于只指定了 RuntimeClass 名称，所以准入控制器更新了 Pod，使之包含 `overhead`。

在 RuntimeClass 准入控制器进行修改后，你可以查看更新后的 Pod 开销值：
```bash
kubectl get pod test-pod -o jsonpath='{.spec.overhead}'
```

输出：
```
map[cpu:250m memory:120Mi]
```

如果定义了 [ResourceQuota](/zh-cn/docs/concepts/policy/resource-quotas/), 
则容器请求的总量以及 `overhead` 字段都将计算在内。

当 kube-scheduler 决定在哪一个节点调度运行新的 Pod 时，调度器会兼顾该 Pod 的
`overhead` 以及该 Pod 的容器请求总量。在这个示例中，调度器将资源请求和开销相加，
然后寻找具备 2.25 CPU 和 320 MiB 内存可用的节点。

一旦 Pod 被调度到了某个节点， 该节点上的 kubelet 将为该 Pod 新建一个 
{{< glossary_tooltip text="cgroup" term_id="cgroup" >}}。 底层容器运行时将在这个
Pod 中创建容器。

如果该资源对每一个容器都定义了一个限制（定义了限制值的 Guaranteed QoS 或者
Burstable QoS），kubelet 会为与该资源（CPU 的 `cpu.cfs_quota_us` 以及内存的
`memory.limit_in_bytes`）
相关的 Pod cgroup 设定一个上限。该上限基于 PodSpec 中定义的容器限制总量与 `overhead` 之和。

对于 CPU，如果 Pod 的 QoS 是 Guaranteed 或者 Burstable，kubelet 会基于容器请求总量与
PodSpec 中定义的 `overhead` 之和设置 `cpu.shares`。

请看这个例子，验证工作负载的容器请求：

```bash
kubectl get pod test-pod -o jsonpath='{.spec.containers[*].resources.limits}'
```

容器请求总计 2000m CPU 和 200MiB 内存：

```
map[cpu: 500m memory:100Mi] map[cpu:1500m memory:100Mi]
```

对照从节点观察到的情况来检查一下：

```bash
kubectl describe node | grep test-pod -B2
```

该输出显示请求了 2250m CPU 以及 320MiB 内存。请求包含了 Pod 开销在内：
```
  Namespace    Name       CPU Requests  CPU Limits   Memory Requests  Memory Limits  AGE
  ---------    ----       ------------  ----------   ---------------  -------------  ---
  default      test-pod   2250m (56%)   2250m (56%)  320Mi (1%)       320Mi (1%)     36m
```

## 验证 Pod cgroup 限制

在工作负载所运行的节点上检查 Pod 的内存 cgroups。在接下来的例子中，
将在该节点上使用具备 CRI 兼容的容器运行时命令行工具
[`crictl`](https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md)。
这是一个显示 Pod 开销行为的高级示例， 预计用户不需要直接在节点上检查 cgroups。
首先在特定的节点上确定该 Pod 的标识符：

```bash
# 在该 Pod 被调度到的节点上执行如下命令：
POD_ID="$(sudo crictl pods --name test-pod -q)"
```

可以依此判断该 Pod 的 cgroup 路径：

```bash
# 在该 Pod 被调度到的节点上执行如下命令：
sudo crictl inspectp -o=json $POD_ID | grep cgroupsPath
```

执行结果的 cgroup 路径中包含了该 Pod 的 `pause` 容器。Pod 级别的 cgroup 在即上一层目录。

```
  "cgroupsPath": "/kubepods/podd7f4b509-cf94-4951-9417-d1087c92a5b2/7ccf55aee35dd16aca4189c952d83487297f3cd760f1bbf09620e206e7d0c27a"
```

在这个例子中，该 Pod 的 cgroup 路径是 `kubepods/podd7f4b509-cf94-4951-9417-d1087c92a5b2`。
验证内存的 Pod 级别 cgroup 设置：

```bash
# 在该 Pod 被调度到的节点上执行这个命令。
# 另外，修改 cgroup 的名称以匹配为该 Pod 分配的 cgroup。
 cat /sys/fs/cgroup/memory/kubepods/podd7f4b509-cf94-4951-9417-d1087c92a5b2/memory.limit_in_bytes
```

和预期的一样，这一数值为 320 MiB。

```
335544320
```

### 可观察性

在 [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics) 中可以通过
`kube_pod_overhead_*` 指标来协助确定何时使用 Pod 开销，
以及协助观察以一个既定开销运行的工作负载的稳定性。
该特性在 kube-state-metrics 的 1.9 发行版本中不可用，不过预计将在后续版本中发布。
在此之前，用户需要从源代码构建 kube-state-metrics。

## {{% heading "whatsnext" %}}

* 学习更多关于 [RuntimeClass](/zh-cn/docs/concepts/containers/runtime-class/) 的信息
* 阅读 [PodOverhead 设计](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/688-pod-overhead)增强建议以获取更多上下文
