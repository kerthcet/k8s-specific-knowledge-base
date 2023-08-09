---
title: 节点压力驱逐
content_type: concept
weight: 100
---

{{<glossary_definition term_id="node-pressure-eviction" length="short">}}</br>

{{<glossary_tooltip term_id="kubelet" text="kubelet">}}
监控集群节点的内存、磁盘空间和文件系统的 inode 等资源。
当这些资源中的一个或者多个达到特定的消耗水平，
kubelet 可以主动地使节点上一个或者多个 Pod 失效，以回收资源防止饥饿。

在节点压力驱逐期间，kubelet 将所选 Pod 的 `PodPhase` 设置为 `Failed`。这将终止 Pod。

节点压力驱逐不同于 [API 发起的驱逐](/zh-cn/docs/concepts/scheduling-eviction/api-eviction/)。

kubelet 并不理会你配置的 `PodDisruptionBudget` 或者是 Pod 的 `terminationGracePeriodSeconds`。
如果你使用了[软驱逐条件](#soft-eviction-thresholds)，kubelet 会考虑你所配置的
`eviction-max-pod-grace-period`。
如果你使用了[硬驱逐条件](#hard-eviction-thresholds)，它使用 `0s` 宽限期来终止 Pod。

如果 Pod 是由替换失败 Pod 的{{< glossary_tooltip text="工作负载" term_id="workload" >}}资源
（例如 {{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}}
或者 {{< glossary_tooltip text="Deployment" term_id="deployment" >}}）管理，
则控制平面或 `kube-controller-manager` 会创建新的 Pod 来代替被驱逐的 Pod。

{{<note>}}
kubelet 在终止最终用户 Pod 之前会尝试[回收节点级资源](#reclaim-node-resources)。
例如，它会在磁盘资源不足时删除未使用的容器镜像。
{{</note>}}

kubelet 使用各种参数来做出驱逐决定，如下所示：

- 驱逐信号
- 驱逐条件
- 监控间隔

### 驱逐信号 {#eviction-signals}

驱逐信号是特定资源在特定时间点的当前状态。
kubelet 使用驱逐信号，通过将信号与驱逐条件进行比较来做出驱逐决定，
驱逐条件是节点上应该可用资源的最小量。

kubelet 使用以下驱逐信号：

| 驱逐信号              | 描述                                                                                   |
|----------------------|---------------------------------------------------------------------------------------|
| `memory.available`   | `memory.available` := `node.status.capacity[memory]` - `node.stats.memory.workingSet` |
| `nodefs.available`   | `nodefs.available` := `node.stats.fs.available`                                       |
| `nodefs.inodesFree`  | `nodefs.inodesFree` := `node.stats.fs.inodesFree`                                     |
| `imagefs.available`  | `imagefs.available` := `node.stats.runtime.imagefs.available`                         |
| `imagefs.inodesFree` | `imagefs.inodesFree` := `node.stats.runtime.imagefs.inodesFree`                       |
| `pid.available`      | `pid.available` := `node.stats.rlimit.maxpid` - `node.stats.rlimit.curproc`           |

在上表中，`描述`列显示了 kubelet 如何获取信号的值。每个信号支持百分比值或者是字面值。
kubelet 计算相对于与信号有关的总量的百分比值。

`memory.available` 的值来自 cgroupfs，而不是像 `free -m` 这样的工具。
这很重要，因为 `free -m` 在容器中不起作用，如果用户使用
[节点可分配资源](/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable)
这一功能特性，资源不足的判定是基于 cgroup 层次结构中的用户 Pod 所处的局部及 cgroup 根节点作出的。
这个[脚本](/zh-cn/examples/admin/resource/memory-available.sh)
重现了 kubelet 为计算 `memory.available` 而执行的相同步骤。
kubelet 在其计算中排除了 inactive_file（即非活动 LRU 列表上基于文件来虚拟的内存的字节数），
因为它假定在压力下内存是可回收的。

kubelet 支持以下文件系统分区：

1. `nodefs`：节点的主要文件系统，用于本地磁盘卷、emptyDir、日志存储等。
   例如，`nodefs` 包含 `/var/lib/kubelet/`。
1. `imagefs`：可选文件系统，供容器运行时存储容器镜像和容器可写层。

kubelet 会自动发现这些文件系统并忽略其他文件系统。kubelet 不支持其他配置。

一些 kubelet 垃圾收集功能已被弃用，以鼓励使用驱逐机制。

| 现有标志 | 新的标志 | 原因 |
| ------------- | -------- | --------- |
| `--image-gc-high-threshold` | `--eviction-hard` 或 `--eviction-soft` | 现有的驱逐信号可以触发镜像垃圾收集 |
| `--image-gc-low-threshold` | `--eviction-minimum-reclaim` | 驱逐回收具有相同的行为 |
| `--maximum-dead-containers` | - | 一旦旧的日志存储在容器的上下文之外就会被弃用 |
| `--maximum-dead-containers-per-container` | - | 一旦旧的日志存储在容器的上下文之外就会被弃用 |
| `--minimum-container-ttl-duration` | - | 一旦旧的日志存储在容器的上下文之外就会被弃用 |

### 驱逐条件 {#eviction-thresholds}

你可以为 kubelet 指定自定义驱逐条件，以便在作出驱逐决定时使用。

驱逐条件的形式为 `[eviction-signal][operator][quantity]`，其中：

* `eviction-signal` 是要使用的[驱逐信号](#eviction-signals)。
* `operator` 是你想要的[关系运算符](https://en.wikipedia.org/wiki/Relational_operator#Standard_relational_operators)，
  比如 `<`（小于）。
* `quantity` 是驱逐条件数量，例如 `1Gi`。
  `quantity` 的值必须与 Kubernetes 使用的数量表示相匹配。
  你可以使用文字值或百分比（`%`）。

例如，如果一个节点的总内存为 10Gi 并且你希望在可用内存低于 1Gi 时触发驱逐，
则可以将驱逐条件定义为 `memory.available<10%` 或 `memory.available< 1G`。
你不能同时使用二者。

你可以配置软和硬驱逐条件。

#### 软驱逐条件 {#soft-eviction-thresholds}

软驱逐条件将驱逐条件与管理员所必须指定的宽限期配对。
在超过宽限期之前，kubelet 不会驱逐 Pod。
如果没有指定的宽限期，kubelet 会在启动时返回错误。

你可以既指定软驱逐条件宽限期，又指定 Pod 终止宽限期的上限，给 kubelet 在驱逐期间使用。
如果你指定了宽限期的上限并且 Pod 满足软驱逐阈条件，则 kubelet 将使用两个宽限期中的较小者。
如果你没有指定宽限期上限，kubelet 会立即杀死被驱逐的 Pod，不允许其体面终止。

你可以使用以下标志来配置软驱逐条件：

* `eviction-soft`：一组驱逐条件，如 `memory.available<1.5Gi`，
  如果驱逐条件持续时长超过指定的宽限期，可以触发 Pod 驱逐。
* `eviction-soft-grace-period`：一组驱逐宽限期，
  如 `memory.available=1m30s`，定义软驱逐条件在触发 Pod 驱逐之前必须保持多长时间。
* `eviction-max-pod-grace-period`：在满足软驱逐条件而终止 Pod 时使用的最大允许宽限期（以秒为单位）。

#### 硬驱逐条件 {#hard-eviction-thresholds}

硬驱逐条件没有宽限期。当达到硬驱逐条件时，
kubelet 会立即杀死 pod，而不会正常终止以回收紧缺的资源。

你可以使用 `eviction-hard` 标志来配置一组硬驱逐条件，
例如 `memory.available<1Gi`。

kubelet 具有以下默认硬驱逐条件：

* `memory.available<100Mi`
* `nodefs.available<10%`
* `imagefs.available<15%`
* `nodefs.inodesFree<5%`（Linux 节点）

只有在没有更改任何参数的情况下，硬驱逐阈值才会被设置成这些默认值。
如果你更改了任何参数的值，则其他参数的取值不会继承其默认值设置，而将被设置为零。
为了提供自定义值，你应该分别设置所有阈值。

### 驱逐监测间隔

kubelet 根据其配置的 `housekeeping-interval`（默认为 `10s`）评估驱逐条件。

### 节点条件 {#node-conditions}

kubelet 报告节点状况以反映节点处于压力之下，因为满足硬或软驱逐条件，与配置的宽限期无关。

kubelet 根据下表将驱逐信号映射为节点状况：

| 节点条件 | 驱逐信号 | 描述 |
|---------|--------|------|
| `MemoryPressure` | `memory.available` | 节点上的可用内存已满足驱逐条件 |
| `DiskPressure`   | `nodefs.available`、`nodefs.inodesFree`、`imagefs.available` 或 `imagefs.inodesFree` | 节点的根文件系统或镜像文件系统上的可用磁盘空间和 inode 已满足驱逐条件 |
| `PIDPressure`    | `pid.available` | (Linux) 节点上的可用进程标识符已低于驱逐条件 |

kubelet 根据配置的 `--node-status-update-frequency` 更新节点条件，默认为 `10s`。

#### 节点条件振荡

在某些情况下，节点在软驱逐条件上下振荡，而没有保持定义的宽限期。
这会导致报告的节点条件在 `true` 和 `false` 之间不断切换，从而导致错误的驱逐决策。

为了防止振荡，你可以使用 `eviction-pressure-transition-period` 标志，
该标志控制 kubelet 在将节点条件转换为不同状态之前必须等待的时间。
过渡期的默认值为 `5m`。

### 回收节点级资源 {#reclaim-node-resources}

kubelet 在驱逐最终用户 Pod 之前会先尝试回收节点级资源。

当报告 `DiskPressure` 节点状况时，kubelet 会根据节点上的文件系统回收节点级资源。

#### 有 `imagefs`

如果节点有一个专用的 `imagefs` 文件系统供容器运行时使用，kubelet 会执行以下操作：

- 如果 `nodefs` 文件系统满足驱逐条件，kubelet 垃圾收集死亡 Pod 和容器。
- 如果 `imagefs` 文件系统满足驱逐条件，kubelet 将删除所有未使用的镜像。

#### 没有 `imagefs`

如果节点只有一个满足驱逐条件的 `nodefs` 文件系统，
kubelet 按以下顺序释放磁盘空间：

1. 对死亡的 Pod 和容器进行垃圾收集
1. 删除未使用的镜像

### kubelet 驱逐时 Pod 的选择

如果 kubelet 回收节点级资源的尝试没有使驱逐信号低于条件，
则 kubelet 开始驱逐最终用户 Pod。

kubelet 使用以下参数来确定 Pod 驱逐顺序：

1. Pod 的资源使用是否超过其请求
1. [Pod 优先级](/zh-cn/docs/concepts/scheduling-eviction/pod-priority-preemption/)
1. Pod 相对于请求的资源使用情况

因此，kubelet 按以下顺序排列和驱逐 Pod：

1. 首先考虑资源使用量超过其请求的 `BestEffort` 或 `Burstable` Pod。
   这些 Pod 会根据它们的优先级以及它们的资源使用级别超过其请求的程度被逐出。
1. 资源使用量少于请求量的 `Guaranteed` Pod 和 `Burstable` Pod 根据其优先级被最后驱逐。

{{<note>}}
kubelet 不使用 Pod 的 QoS 类来确定驱逐顺序。
在回收内存等资源时，你可以使用 QoS 类来估计最可能的 Pod 驱逐顺序。
QoS 不适用于临时存储（EphemeralStorage）请求，
因此如果节点在 `DiskPressure` 下，则上述场景将不适用。
{{</note>}}

仅当 `Guaranteed` Pod 中所有容器都被指定了请求和限制并且二者相等时，才保证 Pod 不被驱逐。
这些 Pod 永远不会因为另一个 Pod 的资源消耗而被驱逐。
如果系统守护进程（例如 `kubelet` 和 `journald`）
消耗的资源比通过 `system-reserved` 或 `kube-reserved` 分配保留的资源多，
并且该节点只有 `Guaranteed` 或 `Burstable` Pod 使用的资源少于其上剩余的请求，
那么 kubelet 必须选择驱逐这些 Pod 中的一个以保持节点稳定性并减少资源匮乏对其他 Pod 的影响。
在这种情况下，它会选择首先驱逐最低优先级的 Pod。

当 kubelet 因 inode 或 PID 不足而驱逐 Pod 时，
它使用优先级来确定驱逐顺序，因为 inode 和 PID 没有请求。

kubelet 根据节点是否具有专用的 `imagefs` 文件系统对 Pod 进行不同的排序：


#### 有 `imagefs`

如果 `nodefs` 触发驱逐，
kubelet 会根据 `nodefs` 使用情况（`本地卷 + 所有容器的日志`）对 Pod 进行排序。

如果 `imagefs` 触发驱逐，kubelet 会根据所有容器的可写层使用情况对 Pod 进行排序。

#### 没有 `imagefs`

如果 `nodefs` 触发驱逐，
kubelet 会根据磁盘总用量（`本地卷 + 日志和所有容器的可写层`）对 Pod 进行排序。


### 最小驱逐回收 {#minimum-eviction-reclaim}

在某些情况下，驱逐 Pod 只会回收少量的紧俏资源。
这可能导致 kubelet 反复达到配置的驱逐条件并触发多次驱逐。

你可以使用 `--eviction-minimum-reclaim` 标志或
[kubelet 配置文件](/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/)
为每个资源配置最小回收量。
当 kubelet 注意到某个资源耗尽时，它会继续回收该资源，直到回收到你所指定的数量为止。

例如，以下配置设置最小回收量：

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
evictionHard:
  memory.available: "500Mi"
  nodefs.available: "1Gi"
  imagefs.available: "100Gi"
evictionMinimumReclaim:
  memory.available: "0Mi"
  nodefs.available: "500Mi"
  imagefs.available: "2Gi"
```

在这个例子中，如果 `nodefs.available` 信号满足驱逐条件，
kubelet 会回收资源，直到信号达到 `1Gi` 的条件，
然后继续回收至少 `500Mi` 直到信号达到 `1.5Gi`。

类似地，kubelet 会回收 `imagefs` 资源，直到 `imagefs.available` 信号达到 `102Gi`。

对于所有资源，默认的 `eviction-minimum-reclaim` 为 `0`。

### 节点内存不足行为

如果节点在 kubelet 能够回收内存之前遇到内存不足（OOM）事件，
则节点依赖 [oom_killer](https://lwn.net/Articles/391222/) 来响应。

kubelet 根据 Pod 的服务质量（QoS）为每个容器设置一个 `oom_score_adj` 值。

| 服务质量            | oom_score_adj                                                                     |
|--------------------|-----------------------------------------------------------------------------------|
| `Guaranteed`       | -997                                                                              |
| `BestEffort`       | 1000                                                                              |
| `Burstable`        | min(max(2, 1000 - (1000 * memoryRequestBytes) / machineMemoryCapacityBytes), 999) |

{{<note>}}
kubelet 还将具有 `system-node-critical`
{{<glossary_tooltip text="优先级" term_id="pod-priority">}}
的 Pod 中的容器 `oom_score_adj` 值设为 `-997`。
{{</note>}}

如果 kubelet 在节点遇到 OOM 之前无法回收内存，
则 `oom_killer` 根据它在节点上使用的内存百分比计算 `oom_score`，
然后加上 `oom_score_adj` 得到每个容器有效的 `oom_score`。
然后它会杀死得分最高的容器。

这意味着低 QoS Pod 中相对于其调度请求消耗内存较多的容器，将首先被杀死。

与 Pod 驱逐不同，如果容器被 OOM 杀死，
`kubelet` 可以根据其 `RestartPolicy` 重新启动它。

### 最佳实践 {#node-pressure-eviction-good-practices}

以下部分描述了驱逐配置的最佳实践。

#### 可调度的资源和驱逐策略

当你为 kubelet 配置驱逐策略时，
你应该确保调度程序不会在 Pod 触发驱逐时对其进行调度，因为这类 Pod 会立即引起内存压力。

考虑以下场景：

* 节点内存容量：`10Gi`
* 操作员希望为系统守护进程（内核、`kubelet` 等）保留 10% 的内存容量
* 操作员希望在节点内存利用率达到 95% 以上时驱逐 Pod，以减少系统 OOM 的概率。

为此，kubelet 启动设置如下：

```
--eviction-hard=memory.available<500Mi
--system-reserved=memory=1.5Gi
```

在此配置中，`--system-reserved` 标志为系统预留了 `1.5Gi` 的内存，
即 `总内存的 10% + 驱逐条件量`。

如果 Pod 使用的内存超过其请求值或者系统使用的内存超过 `1Gi`，
则节点可以达到驱逐条件，这使得 `memory.available` 信号低于 `500Mi` 并触发条件。

### DaemonSet

Pod 优先级是做出驱逐决定的主要因素。
如果你不希望 kubelet 驱逐属于 `DaemonSet` 的 Pod，
请在 Pod 规约中为这些 Pod 提供足够高的 `priorityClass`。
你还可以使用优先级较低的 `priorityClass` 或默认配置，
仅在有足够资源时才运行 `DaemonSet` Pod。

### 已知问题

以下部分描述了与资源不足处理相关的已知问题。

#### kubelet 可能不会立即观察到内存压力

默认情况下，kubelet 轮询 `cAdvisor` 以定期收集内存使用情况统计信息。
如果该轮询时间窗口内内存使用量迅速增加，kubelet 可能无法足够快地观察到 `MemoryPressure`，
但是 `OOMKiller` 仍将被调用。

你可以使用 `--kernel-memcg-notification`
标志在 kubelet 上启用 `memcg` 通知 API，以便在超过条件时立即收到通知。

如果你不是追求极端利用率，而是要采取合理的过量使用措施，
则解决此问题的可行方法是使用 `--kube-reserved` 和 `--system-reserved` 标志为系统分配内存。

#### active_file 内存未被视为可用内存

在 Linux 上，内核跟踪活动 LRU 列表上的基于文件所虚拟的内存字节数作为 `active_file` 统计信息。
kubelet 将 `active_file` 内存区域视为不可回收。
对于大量使用块设备形式的本地存储（包括临时本地存储）的工作负载，
文件和块数据的内核级缓存意味着许多最近访问的缓存页面可能被计为 `active_file`。
如果这些内核块缓冲区中在活动 LRU 列表上有足够多，
kubelet 很容易将其视为资源用量过量并为节点设置内存压力污点，从而触发 Pod 驱逐。

更多细节请参见 [https://github.com/kubernetes/kubernetes/issues/43916](https://github.com/kubernetes/kubernetes/issues/43916)。

你可以通过为可能执行 I/O 密集型活动的容器设置相同的内存限制和内存请求来应对该行为。
你将需要估计或测量该容器的最佳内存限制值。

## {{% heading "whatsnext" %}}

* 了解 [API 发起的驱逐](/zh-cn/docs/concepts/scheduling-eviction/api-eviction/)
* 了解 [Pod 优先级和抢占](/zh-cn/docs/concepts/scheduling-eviction/pod-priority-preemption/)
* 了解 [PodDisruptionBudgets](/zh-cn/docs/tasks/run-application/configure-pdb/)
* 了解[服务质量](/zh-cn/docs/tasks/configure-pod-container/quality-service-pod/)（QoS）
* 查看[驱逐 API](/docs/reference/generated/kubernetes-api/{{<param "version">}}/#create-eviction-pod-v1-core)
