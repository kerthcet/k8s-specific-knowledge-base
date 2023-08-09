---
title: 控制节点上的 CPU 管理策略
content_type: task
min-kubernetes-server-version: v1.26
weight: 140
---


{{< feature-state for_k8s_version="v1.26" state="stable" >}}

按照设计，Kubernetes 对 Pod 执行相关的很多方面进行了抽象，使得用户不必关心。
然而，为了正常运行，有些工作负载要求在延迟和/或性能方面有更强的保证。
为此，kubelet 提供方法来实现更复杂的负载放置策略，同时保持抽象，避免显式的放置指令。

有关资源管理的详细信息，
请参阅 [Pod 和容器的资源管理](/zh-cn/docs/concepts/configuration/manage-resources-containers)文档。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

如果你正在运行一个旧版本的 Kubernetes，请参阅与该版本对应的文档。


## CPU 管理策略   {#cpu-management-policies}

默认情况下，kubelet 使用 [CFS 配额](https://en.wikipedia.org/wiki/Completely_Fair_Scheduler)
来执行 Pod 的 CPU 约束。
当节点上运行了很多 CPU 密集的 Pod 时，工作负载可能会迁移到不同的 CPU 核，
这取决于调度时 Pod 是否被扼制，以及哪些 CPU 核是可用的。
许多工作负载对这种迁移不敏感，因此无需任何干预即可正常工作。

然而，有些工作负载的性能明显地受到 CPU 缓存亲和性以及调度延迟的影响。
对此，kubelet 提供了可选的 CPU 管理策略，来确定节点上的一些分配偏好。

### 配置   {#configuration}

CPU 管理策略通过 kubelet 参数 `--cpu-manager-policy`
或 [KubeletConfiguration](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/)
中的 `cpuManagerPolicy` 字段来指定。
支持两种策略：

* [`none`](#none-policy)：默认策略。
* [`static`](#static-policy)：允许为节点上具有某些资源特征的 Pod 赋予增强的 CPU 亲和性和独占性。

CPU 管理器定期通过 CRI 写入资源更新，以保证内存中 CPU 分配与 cgroupfs 一致。
同步频率通过新增的 Kubelet 配置参数 `--cpu-manager-reconcile-period` 来设置。
如果不指定，默认与 `--node-status-update-frequency` 的周期相同。

Static 策略的行为可以使用 `--cpu-manager-policy-options` 参数来微调。
该参数采用一个逗号分隔的 `key=value` 策略选项列表。
如果你禁用 `CPUManagerPolicyOptions`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)，
则你不能微调 CPU 管理器策略。这种情况下，CPU 管理器仅使用其默认设置运行。

除了顶级的 `CPUManagerPolicyOptions` 特性门控，
策略选项分为两组：Alpha 质量（默认隐藏）和 Beta 质量（默认可见）。
这些组分别由 `CPUManagerPolicyAlphaOptions` 和 `CPUManagerPolicyBetaOptions` 特性门控来管控。
不同于 Kubernetes 标准，这里是由这些特性门控来管控选项组，因为为每个单独选项都添加一个特性门控过于繁琐。

### 更改 CPU 管理器策略   {#changing-the-cpu-manager-policy}

由于 CPU 管理器策略只能在 kubelet 生成新 Pod 时应用，所以简单地从 "none" 更改为 "static"
将不会对现有的 Pod 起作用。
因此，为了正确更改节点上的 CPU 管理器策略，请执行以下步骤：

1. [腾空](/zh-cn/docs/tasks/administer-cluster/safely-drain-node)节点。
2. 停止 kubelet。
3. 删除旧的 CPU 管理器状态文件。该文件的路径默认为 `/var/lib/kubelet/cpu_manager_state`。
   这将清除 CPUManager 维护的状态，以便新策略设置的 cpu-sets 不会与之冲突。
4. 编辑 kubelet 配置以将 CPU 管理器策略更改为所需的值。
5. 启动 kubelet。

对需要更改其 CPU 管理器策略的每个节点重复此过程。
跳过此过程将导致 kubelet crashlooping 并出现以下错误：

```
could not restore state from checkpoint: configured policy "static" differs from state checkpoint policy "none", please drain this node and delete the CPU manager checkpoint file "/var/lib/kubelet/cpu_manager_state" before restarting Kubelet
```

### none 策略   {#none-policy}

`none` 策略显式地启用现有的默认 CPU 亲和方案，不提供操作系统调度器默认行为之外的亲和性策略。
通过 CFS 配额来实现 [Guaranteed Pods](/zh-cn/docs/tasks/configure-pod-container/quality-service-pod/)
和 [Burstable Pods](/zh-cn/docs/tasks/configure-pod-container/quality-service-pod/)
的 CPU 使用限制。

### static 策略   {#static-policy}

`static` 策略针对具有整数型 CPU `requests` 的 `Guaranteed` Pod，
它允许该类 Pod 中的容器访问节点上的独占 CPU 资源。这种独占性是使用
[cpuset cgroup 控制器](https://www.kernel.org/doc/Documentation/cgroup-v1/cpusets.txt)来实现的。

{{< note >}}
诸如容器运行时和 kubelet 本身的系统服务可以继续在这些独占 CPU 上运行。独占性仅针对其他 Pod。
{{< /note >}}

{{< note >}}
CPU 管理器不支持运行时下线和上线 CPU。此外，如果节点上的在线 CPU 集合发生变化，
则必须驱逐节点上的 Pod，并通过删除 kubelet 根目录中的状态文件 `cpu_manager_state`
来手动重置 CPU 管理器。
{{< /note >}}

此策略管理一个 CPU 共享池，该共享池最初包含节点上所有的 CPU 资源。
可独占性 CPU 资源数量等于节点的 CPU 总量减去通过 kubelet `--kube-reserved` 或 `--system-reserved`
参数保留的 CPU 资源。
从 1.17 版本开始，可以通过 kubelet `--reserved-cpus` 参数显式地指定 CPU 预留列表。
由 `--reserved-cpus` 指定的显式 CPU 列表优先于由 `--kube-reserved` 和 `--system-reserved`
指定的 CPU 预留。
通过这些参数预留的 CPU 是以整数方式，按物理核心 ID 升序从初始共享池获取的。
共享池是 `BestEffort` 和 `Burstable` Pod 运行的 CPU 集合。
`Guaranteed` Pod 中的容器，如果声明了非整数值的 CPU `requests`，也将运行在共享池的 CPU 上。
只有 `Guaranteed` Pod 中，指定了整数型 CPU `requests` 的容器，才会被分配独占 CPU 资源。

{{< note >}}
当启用 static 策略时，要求使用 `--kube-reserved` 和/或 `--system-reserved` 或
`--reserved-cpus` 来保证预留的 CPU 值大于零。
这是因为零预留 CPU 值可能使得共享池变空。
{{< /note >}}

当 `Guaranteed` Pod 调度到节点上时，如果其容器符合静态分配要求，
相应的 CPU 会被从共享池中移除，并放置到容器的 cpuset 中。
因为这些容器所使用的 CPU 受到调度域本身的限制，所以不需要使用 CFS 配额来进行 CPU 的绑定。
换言之，容器 cpuset  中的 CPU 数量与 Pod 规约中指定的整数型 CPU `limit` 相等。
这种静态分配增强了 CPU 亲和性，减少了 CPU 密集的工作负载在节流时引起的上下文切换。

考虑以下 Pod 规格的容器：

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
```

该 Pod 属于 `BestEffort` QoS 类型，因为其未指定 `requests` 或 `limits` 值。
所以该容器运行在共享 CPU 池中。

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
      requests:
        memory: "100Mi"
```

该 Pod 属于 `Burstable` QoS 类型，因为其资源 `requests` 不等于 `limits`，且未指定 `cpu` 数量。
所以该容器运行在共享 CPU 池中。

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "2"
      requests:
        memory: "100Mi"
        cpu: "1"
```

该 Pod 属于 `Burstable` QoS 类型，因为其资源 `requests` 不等于 `limits`。
所以该容器运行在共享 CPU 池中。

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "2"
      requests:
        memory: "200Mi"
        cpu: "2"
```

该 Pod 属于 `Guaranteed` QoS 类型，因为其 `requests` 值与 `limits`相等。
同时，容器对 CPU 资源的限制值是一个大于或等于 1 的整数值。
所以，该 `nginx` 容器被赋予 2 个独占 CPU。

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "1.5"
      requests:
        memory: "200Mi"
        cpu: "1.5"
```

该 Pod 属于 `Guaranteed` QoS 类型，因为其 `requests` 值与 `limits`相等。
但是容器对 CPU 资源的限制值是一个小数。所以该容器运行在共享 CPU 池中。

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "2"
```

该 Pod 属于 `Guaranteed` QoS 类型，因其指定了 `limits` 值，同时当未显式指定时，
`requests` 值被设置为与 `limits` 值相等。
同时，容器对 CPU 资源的限制值是一个大于或等于 1 的整数值。
所以，该 `nginx` 容器被赋予 2 个独占 CPU。

#### Static 策略选项

你可以使用以下特性门控根据成熟度级别打开或关闭选项组：
* `CPUManagerPolicyBetaOptions` 默认启用。禁用以隐藏 beta 级选项。
* `CPUManagerPolicyAlphaOptions` 默认禁用。启用以显示 alpha 级选项。
你仍然必须使用 `CPUManagerPolicyOptions` kubelet 选项启用每个选项。

静态 `CPUManager` 策略存在以下策略选项：
* `full-pcpus-only`（Beta，默认可见）（1.22 或更高版本）
* `distribute-cpus-across-numa`（alpha，默认隐藏）（1.23 或更高版本）
* `align-by-socket`（Alpha，默认隐藏）（1.25 或更高版本）

如果使用 `full-pcpus-only` 策略选项，static 策略总是会分配完整的物理核心。
默认情况下，如果不使用该选项，static 策略会使用拓扑感知最适合的分配方法来分配 CPU。
在启用了 SMT 的系统上，此策略所分配是与硬件线程对应的、独立的虚拟核。
这会导致不同的容器共享相同的物理核心，
该行为进而会导致[吵闹的邻居问题](https://en.wikipedia.org/wiki/Cloud_computing_issues#Performance_interference_and_noisy_neighbors)。
启用该选项之后，只有当一个 Pod 里所有容器的 CPU 请求都能够分配到完整的物理核心时，
kubelet 才会接受该 Pod。
如果 Pod 没有被准入，它会被置于 Failed 状态，错误消息是 `SMTAlignmentError`。

如果使用 `distribute-cpus-across-numa` 策略选项，
在需要多个 NUMA 节点来满足分配的情况下，
static 策略会在 NUMA 节点上平均分配 CPU。
默认情况下，`CPUManager` 会将 CPU 分配到一个 NUMA 节点上，直到它被填满，
剩余的 CPU 会简单地溢出到下一个 NUMA 节点。
这会导致依赖于同步屏障（以及类似的同步原语）的并行代码出现不期望的瓶颈，
因为此类代码的运行速度往往取决于最慢的工作线程
（由于至少一个 NUMA 节点存在可用 CPU 较少的情况，因此速度变慢）。
通过在 NUMA 节点上平均分配 CPU，
应用程序开发人员可以更轻松地确保没有某个工作线程单独受到 NUMA 影响，
从而提高这些类型应用程序的整体性能。

如果指定了 `align-by-socket` 策略选项，那么在决定如何分配 CPU 给容器时，CPU 将被视为在 CPU 的插槽边界对齐。
默认情况下，`CPUManager` 在 NUMA 边界对齐 CPU 分配，如果需要从多个 NUMA 节点提取出 CPU 以满足分配，将可能会导致系统性能下降。
尽管 `align-by-socket` 策略试图确保从 NUMA 节点的**最小**数量分配所有 CPU，但不能保证这些 NUMA 节点将位于同一个 CPU 的插槽上。
通过指示 `CPUManager` 在 CPU 的插槽边界而不是 NUMA 边界显式对齐 CPU，我们能够避免此类问题。
注意，此策略选项不兼容 `TopologyManager` 与 `single-numa-node` 策略，并且不适用于 CPU 的插槽数量大于 NUMA 节点数量的硬件。

可以通过将 `full-pcpus-only=true` 添加到 CPUManager 策略选项来启用 `full-pcpus-only` 选项。
同样地，可以通过将 `distribute-cpus-across-numa=true` 添加到 CPUManager 策略选项来启用 `distribute-cpus-across-numa` 选项。
当两者都设置时，它们是“累加的”，因为 CPU 将分布在 NUMA 节点的 full-pcpus 块中，而不是单个核心。
可以通过将 `align-by-socket=true` 添加到 `CPUManager` 策略选项来启用 `align-by-socket` 策略选项。
同样，也能够将 `distribute-cpus-across-numa=true` 添加到 `full-pcpus-only`
和 `distribute-cpus-across-numa` 策略选项中。
