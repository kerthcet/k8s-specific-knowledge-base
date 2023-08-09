---
title: 为 Pod 和容器管理资源
content_type: concept
weight: 40
feature:
  title: 自动装箱
  description: >
    根据资源需求和其他限制自动放置容器，同时避免影响可用性。
    将关键性的和尽力而为性质的工作负载进行混合放置，以提高资源利用率并节省更多资源。
---


当你定义 {{< glossary_tooltip text="Pod" term_id="pod" >}} 时可以选择性地为每个
{{< glossary_tooltip text="容器" term_id="container" >}}设定所需要的资源数量。
最常见的可设定资源是 CPU 和内存（RAM）大小；此外还有其他类型的资源。

当你为 Pod 中的 Container 指定了资源 **request（请求）**时，
{{< glossary_tooltip text="kube-scheduler" term_id="kube-scheduler" >}}
就利用该信息决定将 Pod 调度到哪个节点上。
当你为 Container 指定了资源 **limit（限制）**时，{{< glossary_tooltip text="kubelet" term_id="kubelet" >}}
就可以确保运行的容器不会使用超出所设限制的资源。
kubelet 还会为容器预留所 **request（请求）**数量的系统资源，供其使用。


## 请求和限制  {#requests-and-limits}

如果 Pod 运行所在的节点具有足够的可用资源，容器可能（且可以）使用超出对应资源
`request` 属性所设置的资源量。不过，容器不可以使用超出其资源 `limit`
属性所设置的资源量。

例如，如果你将容器的 `memory` 的请求量设置为 256 MiB，而该容器所处的 Pod
被调度到一个具有 8 GiB 内存的节点上，并且该节点上没有其他 Pod
运行，那么该容器就可以尝试使用更多的内存。

如果你将某容器的 `memory` 限制设置为 4 GiB，kubelet
（和{{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}）就会确保该限制生效。
容器运行时会禁止容器使用超出所设置资源限制的资源。
例如：当容器中进程尝试使用超出所允许内存量的资源时，系统内核会将尝试申请内存的进程终止，
并引发内存不足（OOM）错误。

限制可以以被动方式来实现（系统会在发现违例时进行干预），或者通过强制生效的方式实现
（系统会避免容器用量超出限制）。不同的容器运行时采用不同方式来实现相同的限制。

{{< note >}}
如果你为某个资源指定了限制，但不指定请求，
并且没有应用准入时机制为该资源设置默认请求，
然后 Kubernetes 复制你所指定的限制值，将其用作资源的请求值。
{{< /note >}}

## 资源类型  {#resource-types}

**CPU** 和 **内存** 都是 **资源类型**。每种资源类型具有其基本单位。
CPU 表达的是计算处理能力，其单位是 [Kubernetes CPU](#meaning-of-cpu)。
内存的单位是字节。
对于 Linux 负载，则可以指定巨页（Huge Page）资源。
巨页是 Linux 特有的功能，节点内核在其中分配的内存块比默认页大小大得多。

例如，在默认页面大小为 4KiB 的系统上，你可以指定限制 `hugepages-2Mi: 80Mi`。
如果容器尝试分配 40 个 2MiB 大小的巨页（总共 80 MiB ），则分配请求会失败。

{{< note >}}
你不能过量使用 `hugepages- *` 资源。
这与 `memory` 和 `cpu` 资源不同。
{{< /note >}}

CPU 和内存统称为 **计算资源**，或简称为 **资源**。
计算资源的数量是可测量的，可以被请求、被分配、被消耗。
它们与 [API 资源](/zh-cn/docs/concepts/overview/kubernetes-api/)不同。
API 资源（如 Pod 和 [Service](/zh-cn/docs/concepts/services-networking/service/)）是可通过
Kubernetes API 服务器读取和修改的对象。

## Pod 和 容器的资源请求和限制  {#resource-requests-and-limits-of-pod-and-container}

针对每个容器，你都可以指定其资源限制和请求，包括如下选项：

* `spec.containers[].resources.limits.cpu`
* `spec.containers[].resources.limits.memory`
* `spec.containers[].resources.limits.hugepages-<size>`
* `spec.containers[].resources.requests.cpu`
* `spec.containers[].resources.requests.memory`
* `spec.containers[].resources.requests.hugepages-<size>`

尽管你只能逐个容器地指定请求和限制值，考虑 Pod 的总体资源请求和限制也是有用的。
对特定资源而言，**Pod 的资源请求/限制** 是 Pod 中各容器对该类型资源的请求/限制的总和。

## Kubernetes 中的资源单位  {#resource-units-in-kubernetes}

### CPU 资源单位    {#meaning-of-cpu}

CPU 资源的限制和请求以 “cpu” 为单位。
在 Kubernetes 中，一个 CPU 等于 **1 个物理 CPU 核** 或者 **1 个虚拟核**，
取决于节点是一台物理主机还是运行在某物理主机上的虚拟机。

你也可以表达带小数 CPU 的请求。
当你定义一个容器，将其 `spec.containers[].resources.requests.cpu` 设置为 0.5 时，
你所请求的 CPU 是你请求 `1.0` CPU 时的一半。
对于 CPU 资源单位，[数量](/zh-cn/docs/reference/kubernetes-api/common-definitions/quantity/)
表达式 `0.1` 等价于表达式 `100m`，可以看作 “100 millicpu”。
有些人说成是“一百毫核”，其实说的是同样的事情。

CPU 资源总是设置为资源的绝对数量而非相对数量值。
例如，无论容器运行在单核、双核或者 48-核的机器上，`500m` CPU 表示的是大约相同的计算能力。

{{< note >}}
Kubernetes 不允许设置精度小于 `1m` 的 CPU 资源。
因此，当 CPU 单位小于 `1` 或 `1000m` 时，使用毫核的形式是有用的；
例如 `5m` 而不是 `0.005`。
{{< /note >}}

## 内存资源单位      {#meaning-of-memory}

`memory` 的限制和请求以字节为单位。
你可以使用普通的整数，或者带有以下
[数量](/zh-cn/docs/reference/kubernetes-api/common-definitions/quantity/)后缀
的定点数字来表示内存：E、P、T、G、M、k。
你也可以使用对应的 2 的幂数：Ei、Pi、Ti、Gi、Mi、Ki。
例如，以下表达式所代表的是大致相同的值：

```shell
128974848、129e6、129M、128974848000m、123Mi
```

请注意后缀的大小写。如果你请求 `400m` 临时存储，实际上所请求的是 0.4 字节。
如果有人这样设定资源请求或限制，可能他的实际想法是申请 400Mi 字节（`400Mi`）
或者 400M 字节。

## 容器资源示例     {#example-1}

以下 Pod 有两个容器。每个容器的请求为 0.25 CPU 和 64MiB（2<sup>26</sup> 字节）内存，
每个容器的资源限制为 0.5 CPU 和 128MiB 内存。
你可以认为该 Pod 的资源请求为 0.5 CPU 和 128 MiB 内存，资源限制为 1 CPU 和 256MiB 内存。

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: frontend
spec:
  containers:
  - name: app
    image: images.my-company.example/app:v4
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
  - name: log-aggregator
    image: images.my-company.example/log-aggregator:v6
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

## 带资源请求的 Pod 如何调度  {#how-pods-with-resource-limits-are-run}

当你创建一个 Pod 时，Kubernetes 调度程序将为 Pod 选择一个节点。
每个节点对每种资源类型都有一个容量上限：可为 Pod 提供的 CPU 和内存量。
调度程序确保对于每种资源类型，所调度的容器的资源请求的总和小于节点的容量。
请注意，尽管节点上的实际内存或 CPU 资源使用量非常低，如果容量检查失败，
调度程序仍会拒绝在该节点上放置 Pod。
当稍后节点上资源用量增加，例如到达请求率的每日峰值区间时，节点上也不会出现资源不足的问题。

## Kubernetes 应用资源请求与限制的方式 {#how-pods-with-resource-limits-are-run}

当 kubelet 将容器作为 Pod 的一部分启动时，它会将容器的 CPU 和内存请求与限制信息传递给容器运行时。

在 Linux 系统上，容器运行时通常会配置内核
{{< glossary_tooltip text="CGroups" term_id="cgroup" >}}，负责应用并实施所定义的请求。

- CPU 限制定义的是容器可使用的 CPU 时间的硬性上限。
  在每个调度周期（时间片）期间，Linux 内核检查是否已经超出该限制；
  内核会在允许该 cgroup 恢复执行之前会等待。
- CPU 请求值定义的是一个权重值。如果若干不同的容器（CGroups）需要在一个共享的系统上竞争运行，
  CPU 请求值大的负载会获得比请求值小的负载更多的 CPU 时间。
- 内存请求值主要用于（Kubernetes）Pod 调度期间。在一个启用了 CGroup v2 的节点上，
  容器运行时可能会使用内存请求值作为设置 `memory.min` 和 `memory.low` 的提示值。
- 内存限制定义的是 cgroup 的内存限制。如果容器尝试分配的内存量超出限制，
  则 Linux 内核的内存不足处理子系统会被激活，并停止尝试分配内存的容器中的某个进程。
  如果该进程在容器中 PID 为 1，而容器被标记为可重新启动，则 Kubernetes
  会重新启动该容器。
- Pod 或容器的内存限制也适用于通过内存供应的卷，例如 `emptyDir` 卷。
  kubelet 会跟踪 `tmpfs` 形式的 emptyDir 卷用量，将其作为容器的内存用量，
  而不是临时存储用量。

如果某容器内存用量超过其内存请求值并且所在节点内存不足时，容器所处的 Pod
可能被{{< glossary_tooltip text="逐出" term_id="eviction" >}}。

每个容器可能被允许也可能不被允许使用超过其 CPU 限制的处理时间。
但是，容器运行时不会由于 CPU 使用率过高而杀死 Pod 或容器。

要确定某容器是否会由于资源限制而无法调度或被杀死，请参阅[疑难解答](#troubleshooting)节。

### 监控计算和内存资源用量  {#monitoring-compute-memory-resource-usage}

kubelet 会将 Pod 的资源使用情况作为 Pod
[`status`](/zh-cn/docs/concepts/overview/working-with-objects/#object-spec-and-status)
的一部分来报告的。

如果为集群配置了可选的[监控工具](/zh-cn/docs/tasks/debug/debug-cluster/resource-usage-monitoring/)，
则可以直接从[指标 API](/zh-cn/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/#metrics-api)
或者监控工具获得 Pod 的资源使用情况。

## 本地临时存储   {#local-ephemeral-storage}

{{< feature-state for_k8s_version="v1.25" state="stable" >}}

节点通常还可以具有本地的临时性存储，由本地挂接的可写入设备或者有时也用 RAM
来提供支持。
“临时（Ephemeral）”意味着对所存储的数据不提供长期可用性的保证。

Pods 通常可以使用临时性本地存储来实现缓冲区、保存日志等功能。
kubelet 可以为使用本地临时存储的 Pods 提供这种存储空间，允许后者使用
[`emptyDir`](/zh-cn/docs/concepts/storage/volumes/#emptydir)
类型的{{< glossary_tooltip term_id="volume" text="卷" >}}将其挂载到容器中。

kubelet 也使用此类存储来保存[节点层面的容器日志](/zh-cn/docs/concepts/cluster-administration/logging/#logging-at-the-node-level)、
容器镜像文件以及运行中容器的可写入层。

{{< caution >}}
如果节点失效，存储在临时性存储中的数据会丢失。
你的应用不能对本地临时性存储的性能 SLA（例如磁盘 IOPS）作任何假定。
{{< /caution >}}

{{< note >}}
为了使临时性存储的资源配额生效，需要完成以下两个步骤：

* 管理员在命名空间中设置临时性存储的资源配额。
* 用户需要在 Pod spec 中指定临时性存储资源的限制。

如果用户在 Pod spec 中未指定临时性存储资源的限制，
则临时性存储的资源配额不会生效。
{{< /note >}}

Kubernetes 允许你跟踪、预留和限制 Pod
可消耗的临时性本地存储数量。

### 本地临时性存储的配置  {##configurations-for-local-ephemeral-storage}

Kubernetes 有两种方式支持节点上配置本地临时性存储：

{{< tabs name="local_storage_configurations" >}}
{{% tab name="单一文件系统" %}}
采用这种配置时，你会把所有类型的临时性本地数据（包括 `emptyDir`
卷、可写入容器层、容器镜像、日志等）放到同一个文件系统中。
作为最有效的 kubelet 配置方式，这意味着该文件系统是专门提供给 Kubernetes
（kubelet）来保存数据的。

kubelet 也会生成[节点层面的容器日志](/zh-cn/docs/concepts/cluster-administration/logging/#logging-at-the-node-level)，
并按临时性本地存储的方式对待之。

kubelet 会将日志写入到所配置的日志目录（默认为 `/var/log`）下的文件中；
还会针对其他本地存储的数据使用同一个基础目录（默认为 `/var/lib/kubelet`）。

通常，`/var/lib/kubelet` 和 `/var/log` 都是在系统的根文件系统中。kubelet
的设计也考虑到这一点。

你的集群节点当然可以包含其他的、并非用于 Kubernetes 的很多文件系统。
{{% /tab %}}


{{% tab name="双文件系统" %}}

你使用节点上的某个文件系统来保存运行 Pods 时产生的临时性数据：日志和
`emptyDir` 卷等。你可以使用这个文件系统来保存其他数据（例如：与 Kubernetes
无关的其他系统日志）；这个文件系统还可以是根文件系统。

kubelet 也将[节点层面的容器日志](/zh-cn/docs/concepts/cluster-administration/logging/#logging-at-the-node-level)
写入到第一个文件系统中，并按临时性本地存储的方式对待之。

同时你使用另一个由不同逻辑存储设备支持的文件系统。在这种配置下，你会告诉
kubelet 将容器镜像层和可写层保存到这第二个文件系统上的某个目录中。

第一个文件系统中不包含任何镜像层和可写层数据。

当然，你的集群节点上还可以有很多其他与 Kubernetes 没有关联的文件系统。
{{% /tab %}}
{{< /tabs >}}

kubelet 能够度量其本地存储的用量。
实现度量机制的前提是你已使用本地临时存储所支持的配置之一对节点进行配置。

如果你的节点配置不同于以上预期，kubelet 就无法对临时性本地存储实施资源限制。

{{< note >}}
kubelet 会将 `tmpfs` emptyDir 卷的用量当作容器内存用量，而不是本地临时性存储来统计。
{{< /note >}}

{{< note >}}
kubelet 将仅跟踪临时存储的根文件系统。
挂载一个单独磁盘到 `/var/lib/kubelet` 或 `/var/lib/containers` 的操作系统布局将不会正确地报告临时存储。
{{< /note >}}

### 为本地临时性存储设置请求和限制  {#setting-requests-and-limits-for-local-ephemeral-storage}

你可以指定 `ephemeral-storage` 来管理本地临时性存储。
Pod 中的每个容器可以设置以下属性：

* `spec.containers[].resources.limits.ephemeral-storage`
* `spec.containers[].resources.requests.ephemeral-storage`

`ephemeral-storage` 的请求和限制是按量纲计量的。
你可以使用一般整数或者定点数字加上下面的后缀来表达存储量：E、P、T、G、M、k。
你也可以使用对应的 2 的幂级数来表达：Ei、Pi、Ti、Gi、Mi、Ki。
例如，下面的表达式所表达的大致是同一个值：

- `128974848`
- `129e6`
- `129M`
- `123Mi`

请注意后缀的大小写。如果你请求 `400m` 临时存储，实际上所请求的是 0.4 字节。
如果有人这样设定资源请求或限制，可能他的实际想法是申请 400Mi 字节（`400Mi`）
或者 400M 字节。


在下面的例子中，Pod 包含两个容器。每个容器请求 2 GiB 大小的本地临时性存储。
每个容器都设置了 4 GiB 作为其本地临时性存储的限制。
因此，整个 Pod 的本地临时性存储请求是 4 GiB，且其本地临时性存储的限制为 8 GiB。
该限制值中有 500Mi 可供 `emptyDir` 卷使用。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: frontend
spec:
  containers:
  - name: app
    image: images.my-company.example/app:v4
    resources:
      requests:
        ephemeral-storage: "2Gi"
      limits:
        ephemeral-storage: "4Gi"
    volumeMounts:
    - name: ephemeral
      mountPath: "/tmp"
  - name: log-aggregator
    image: images.my-company.example/log-aggregator:v6
    resources:
      requests:
        ephemeral-storage: "2Gi"
      limits:
        ephemeral-storage: "4Gi"
    volumeMounts:
    - name: ephemeral
      mountPath: "/tmp"
  volumes:
    - name: ephemeral
      emptyDir:
        sizeLimit: 500Mi
```


### 带临时性存储的 Pods 的调度行为  {#how-pods-with-ephemeral-storage-requests-are-scheduled}

当你创建一个 Pod 时，Kubernetes 调度器会为 Pod 选择一个节点来运行之。
每个节点都有一个本地临时性存储的上限，是其可提供给 Pod 使用的总量。
欲了解更多信息，
可参考[节点可分配资源](/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable)节。

调度器会确保所调度的容器的资源请求总和不会超出节点的资源容量。

### 临时性存储消耗的管理 {#resource-emphemeralstorage-consumption}

如果 kubelet 将本地临时性存储作为资源来管理，则 kubelet 会度量以下各处的存储用量：

- `emptyDir` 卷，除了 **tmpfs** `emptyDir` 卷
- 保存节点层面日志的目录
- 可写入的容器镜像层

如果某 Pod 的临时存储用量超出了你所允许的范围，kubelet
会向其发出逐出（eviction）信号，触发该 Pod 被逐出所在节点。

就容器层面的隔离而言，如果某容器的可写入镜像层和日志用量超出其存储限制，
kubelet 也会将所在的 Pod 标记为逐出候选。

就 Pod 层面的隔离而言，kubelet 会将 Pod 中所有容器的限制相加，得到 Pod
存储限制的总值。如果所有容器的本地临时性存储用量总和加上 Pod 的 `emptyDir`
卷的用量超出 Pod 存储限制，kubelet 也会将该 Pod 标记为逐出候选。

{{< caution >}}
如果 kubelet 没有度量本地临时性存储的用量，即使 Pod
的本地存储用量超出其限制也不会被逐出。

不过，如果用于可写入容器镜像层、节点层面日志或者 `emptyDir` 卷的文件系统中可用空间太少，
节点会为自身设置本地存储不足的{{< glossary_tooltip text="污点" term_id="taint" >}}标签。
这一污点会触发对那些无法容忍该污点的 Pod 的逐出操作。

关于临时性本地存储的配置信息，请参考[这里](#configurations-for-local-ephemeral-storage)
{{< /caution >}}

kubelet 支持使用不同方式来度量 Pod 的存储用量：

{{< tabs name="resource-emphemeralstorage-measurement" >}}
{{% tab name="周期性扫描" %}}

kubelet 按预定周期执行扫描操作，检查 `emptyDir` 卷、容器日志目录以及可写入容器镜像层。

这一扫描会度量存储空间用量。

{{< note >}}
在这种模式下，kubelet 并不检查已删除文件所对应的、仍处于打开状态的文件描述符。

如果你（或者容器）在 `emptyDir` 卷中创建了一个文件，
写入一些内容之后再次打开该文件并执行了删除操作，所删除文件对应的 inode 仍然存在，
直到你关闭该文件为止。kubelet 不会将该文件所占用的空间视为已使用空间。
{{< /note >}}

{{% /tab %}}

{{% tab name="文件系统项目配额" %}}

{{< feature-state for_k8s_version="v1.15" state="alpha" >}}

项目配额（Project Quota）是一个操作系统层的功能特性，用来管理文件系统中的存储用量。
在 Kubernetes 中，你可以启用项目配额以监视存储用量。
你需要确保节点上为 `emptyDir` 提供存储的文件系统支持项目配额。
例如，XFS 和 ext4fs 文件系统都支持项目配额。

{{< note >}}
项目配额可以帮你监视存储用量，但无法强制执行限制。
{{< /note >}}

Kubernetes 所使用的项目 ID 始于 `1048576`。
所使用的 IDs 会注册在 `/etc/projects` 和 `/etc/projid` 文件中。
如果该范围中的项目 ID 已经在系统中被用于其他目的，则已占用的项目 ID
也必须注册到 `/etc/projects` 和 `/etc/projid` 中，这样 Kubernetes
才不会使用它们。

配额方式与目录扫描方式相比速度更快，结果更精确。当某个目录被分配给某个项目时，
该目录下所创建的所有文件都属于该项目，内核只需要跟踪该项目中的文件所使用的存储块个数。
如果某文件被创建后又被删除，但对应文件描述符仍处于打开状态，
该文件会继续耗用存储空间。配额跟踪技术能够精确第记录对应存储空间的状态，
而目录扫描方式会忽略被删除文件所占用的空间。


如果你希望使用项目配额，你需要：

* 在 [kubelet 配置](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/)中使用
  `featureGates` 字段或者使用 `--feature-gates` 命令行参数启用
  `LocalStorageCapacityIsolationFSQuotaMonitoring=true` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)。

* 确保根文件系统（或者可选的运行时文件系统）启用了项目配额。所有 XFS
  文件系统都支持项目配额。
  对 extf 文件系统而言，你需要在文件系统尚未被挂载时启用项目配额跟踪特性：

  ```bash
  # 对 ext4 而言，在 /dev/block-device 尚未被挂载时执行下面操作
  sudo tune2fs -O project -Q prjquota /dev/block-device
  ```

* 确保根文件系统（或者可选的运行时文件系统）在挂载时项目配额特性是被启用了的。
  对于 XFS 和 ext4fs 而言，对应的挂载选项称作 `prjquota`。

{{% /tab %}}
{{< /tabs >}}

## 扩展资源（Extended Resources）   {#extended-resources}

扩展资源是 `kubernetes.io` 域名之外的标准资源名称。
它们使得集群管理员能够颁布非 Kubernetes 内置资源，而用户可以使用他们。

使用扩展资源需要两个步骤。首先，集群管理员必须颁布扩展资源。
其次，用户必须在 Pod 中请求扩展资源。

### 管理扩展资源   {#managing-extended-resources}

#### 节点级扩展资源     {#node-level-extended-resources}

节点级扩展资源绑定到节点。

##### 设备插件管理的资源   {#device-plugin-managed-resources}

有关如何颁布在各节点上由设备插件所管理的资源，
请参阅[设备插件](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)。

##### 其他资源   {#other-resources}

为了颁布新的节点级扩展资源，集群操作员可以向 API 服务器提交 `PATCH` HTTP 请求，
以在集群中节点的 `status.capacity` 中为其配置可用数量。
完成此操作后，节点的 `status.capacity` 字段中将包含新资源。
kubelet 会异步地对 `status.allocatable` 字段执行自动更新操作，使之包含新资源。

由于调度器在评估 Pod 是否适合在某节点上执行时会使用节点的 `status.allocatable` 值，
调度器只会考虑异步更新之后的新值。
在更新节点容量使之包含新资源之后和请求该资源的第一个 Pod 被调度到该节点之间，
可能会有短暂的延迟。

**示例：**

这是一个示例，显示了如何使用 `curl` 构造 HTTP 请求，公告主节点为 `k8s-master`
的节点 `k8s-node-1` 上存在五个 `example.com/foo` 资源。

```shell
curl --header "Content-Type: application/json-patch+json" \
--request PATCH \
--data '[{"op": "add", "path": "/status/capacity/example.com~1foo", "value": "5"}]' \
http://k8s-master:8080/api/v1/nodes/k8s-node-1/status
```

{{< note >}}
在前面的请求中，`~1` 是在 patch 路径中对字符 `/` 的编码。
JSON-Patch 中的操作路径的值被视为 JSON-Pointer 类型。
有关更多详细信息，请参见
[IETF RFC 6901 第 3 节](https://tools.ietf.org/html/rfc6901#section-3)。
{{< /note >}}

#### 集群层面的扩展资源   {#cluster-level-extended-resources}

集群层面的扩展资源并不绑定到具体节点。
它们通常由调度器扩展程序（Scheduler Extenders）管理，这些程序处理资源消耗和资源配额。

你可以在[调度器配置](/zh-cn/docs/reference/config-api/kube-scheduler-config.v1beta3/)
中指定由调度器扩展程序处理的扩展资源。

**示例：**

下面的调度器策略配置标明集群层扩展资源 "example.com/foo" 由调度器扩展程序处理。

- 仅当 Pod 请求 "example.com/foo" 时，调度器才会将 Pod 发送到调度器扩展程序。
- `ignoredByScheduler` 字段指定调度器不要在其 `PodFitsResources` 断言中检查
  "example.com/foo" 资源。

```json
{
  "kind": "Policy",
  "apiVersion": "v1",
  "extenders": [
    {
      "urlPrefix": "<extender-endpoint>",
      "bindVerb": "bind",
      "managedResources": [
        {
          "name": "example.com/foo",
          "ignoredByScheduler": true
        }
      ]
    }
  ]
}
```

### 使用扩展资源  {#consuming-extended-resources}

就像 CPU 和内存一样，用户可以在 Pod 的规约中使用扩展资源。
调度器负责资源的核算，确保同时分配给 Pod 的资源总量不会超过可用数量。

API 服务器将扩展资源的数量限制为整数。
**有效** 数量的示例是 `3`、`3000m` 和 `3Ki`。
**无效** 数量的示例是 `0.5` 和 `1500m`。

{{< note >}}
扩展资源取代了非透明整数资源（Opaque Integer Resources，OIR）。
用户可以使用 `kubernetes.io`（保留）以外的任何域名前缀。
{{< /note >}}

要在 Pod 中使用扩展资源，请在容器规约的 `spec.containers[].resources.limits`
映射中包含资源名称作为键。

{{< note >}}
扩展资源不能过量使用，因此如果容器规约中同时存在请求和限制，则它们的取值必须相同。
{{< /note >}}

仅当所有资源请求（包括 CPU、内存和任何扩展资源）都被满足时，Pod 才能被调度。
在资源请求无法满足时，Pod 会保持在 `PENDING` 状态。

**示例：**

下面的 Pod 请求 2 个 CPU 和 1 个 "example.com/foo"（扩展资源）。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: my-container
    image: myimage
    resources:
      requests:
        cpu: 2
        example.com/foo: 1
      limits:
        example.com/foo: 1
```

## PID 限制   {#pid-limiting}

进程 ID（PID）限制允许对 kubelet 进行配置，以限制给定 Pod 可以消耗的 PID 数量。
有关信息，请参见 [PID 限制](/zh-cn/docs/concepts/policy/pid-limiting/)。

## 疑难解答  {#troubleshooting}

### 我的 Pod 处于悬决状态且事件信息显示 `FailedScheduling`  {#my-pods-are-pending-with-event-message-failedscheduling}

如果调度器找不到该 Pod 可以匹配的任何节点，则该 Pod 将保持未被调度状态，
直到找到一个可以被调度到的位置。每当调度器找不到 Pod 可以调度的地方时，
会产生一个 [Event](/zh-cn/docs/reference/kubernetes-api/cluster-resources/event-v1/)。
你可以使用 `kubectl` 来查看 Pod 的事件；例如：

```shell
kubectl describe pod frontend | grep -A 9999999999 Events
```

```
Events:
  Type     Reason            Age   From               Message
  ----     ------            ----  ----               -------
  Warning  FailedScheduling  23s   default-scheduler  0/42 nodes available: insufficient cpu
```

在上述示例中，由于节点上的 CPU 资源不足，名为 “frontend” 的 Pod 无法被调度。
由于内存不足（PodExceedsFreeMemory）而导致失败时，也有类似的错误消息。
一般来说，如果 Pod 处于悬决状态且有这种类型的消息时，你可以尝试如下几件事情：

- 向集群添加更多节点。
- 终止不需要的 Pod，为悬决的 Pod 腾出空间。
- 检查 Pod 所需的资源是否超出所有节点的资源容量。例如，如果所有节点的容量都是`cpu：1`，
  那么一个请求为 `cpu: 1.1` 的 Pod 永远不会被调度。
- 检查节点上的污点设置。如果集群中节点上存在污点，而新的 Pod 不能容忍污点，
  调度器只会考虑将 Pod 调度到不带有该污点的节点上。

你可以使用 `kubectl describe nodes` 命令检查节点容量和已分配的资源数量。 例如：

```shell
kubectl describe nodes e2e-test-node-pool-4lw4
```

```
Name:            e2e-test-node-pool-4lw4
[ ... 这里忽略了若干行以便阅读 ...]
Capacity:
 cpu:                               2
 memory:                            7679792Ki
 pods:                              110
Allocatable:
 cpu:                               1800m
 memory:                            7474992Ki
 pods:                              110
[ ... 这里忽略了若干行以便阅读 ...]
Non-terminated Pods:        (5 in total)
  Namespace    Name                                  CPU Requests  CPU Limits  Memory Requests  Memory Limits
  ---------    ----                                  ------------  ----------  ---------------  -------------
  kube-system  fluentd-gcp-v1.38-28bv1               100m (5%)     0 (0%)      200Mi (2%)       200Mi (2%)
  kube-system  kube-dns-3297075139-61lj3             260m (13%)    0 (0%)      100Mi (1%)       170Mi (2%)
  kube-system  kube-proxy-e2e-test-...               100m (5%)     0 (0%)      0 (0%)           0 (0%)
  kube-system  monitoring-influxdb-grafana-v4-z1m12  200m (10%)    200m (10%)  600Mi (8%)       600Mi (8%)
  kube-system  node-problem-detector-v0.1-fj7m3      20m (1%)      200m (10%)  20Mi (0%)        100Mi (1%)
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  CPU Requests    CPU Limits    Memory Requests    Memory Limits
  ------------    ----------    ---------------    -------------
  680m (34%)      400m (20%)    920Mi (11%)        1070Mi (13%)
```

在上面的输出中，你可以看到如果 Pod 请求超过 1.120 CPU 或者 6.23Gi 内存，节点将无法满足。

通过查看 "Pods" 部分，你将看到哪些 Pod 占用了节点上的资源。

Pods 可用的资源量低于节点的资源总量，因为系统守护进程也会使用一部分可用资源。
在 Kubernetes API 中，每个 Node 都有一个 `.status.allocatable` 字段
（详情参见 [NodeStatus](/zh-cn/docs/reference/kubernetes-api/cluster-resources/node-v1/#NodeStatus)）。

字段 `.status.allocatable` 描述节点上可以用于 Pod 的资源总量（例如：15 个虚拟
CPU、7538 MiB 内存）。关于 Kubernetes 中节点可分配资源的信息，
可参阅[为系统守护进程预留计算资源](/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/)。

你可以配置[资源配额](/zh-cn/docs/concepts/policy/resource-quotas/)功能特性以限制每个名字空间可以使用的资源总量。
当某名字空间中存在 ResourceQuota 时，Kubernetes 会在该名字空间中的对象强制实施配额。
例如，如果你为不同的团队分配名字空间，你可以为这些名字空间添加 ResourceQuota。
设置资源配额有助于防止一个团队占用太多资源，以至于这种占用会影响其他团队。

你还需要考虑为这些名字空间设置授权访问：
为名字空间提供 **全部** 的写权限时，具有合适权限的人可能删除所有资源，
包括所配置的 ResourceQuota。


### 我的容器被终止了  {#my-container-is-terminated}

你的容器可能因为资源紧张而被终止。要查看容器是否因为遇到资源限制而被杀死，
请针对相关的 Pod 执行 `kubectl describe pod`：

```shell
kubectl describe pod simmemleak-hra99
```

输出类似于：

```
Name:                           simmemleak-hra99
Namespace:                      default
Image(s):                       saadali/simmemleak
Node:                           kubernetes-node-tf0f/10.240.216.66
Labels:                         name=simmemleak
Status:                         Running
Reason:
Message:
IP:                             10.244.2.75
Containers:
  simmemleak:
    Image:  saadali/simmemleak:latest
    Limits:
      cpu:          100m
      memory:       50Mi
    State:          Running
      Started:      Tue, 07 Jul 2019 12:54:41 -0700
    Last State:     Terminated
      Reason:       OOMKilled
      Exit Code:    137
      Started:      Fri, 07 Jul 2019 12:54:30 -0700
      Finished:     Fri, 07 Jul 2019 12:54:33 -0700
    Ready:          False
    Restart Count:  5
Conditions:
  Type      Status
  Ready     False
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  42s   default-scheduler  Successfully assigned simmemleak-hra99 to kubernetes-node-tf0f
  Normal  Pulled     41s   kubelet            Container image "saadali/simmemleak:latest" already present on machine
  Normal  Created    41s   kubelet            Created container simmemleak
  Normal  Started    40s   kubelet            Started container simmemleak
  Normal  Killing    32s   kubelet            Killing container with id ead3fb35-5cf5-44ed-9ae1-488115be66c6: Need to kill Pod
```

在上面的例子中，`Restart Count: 5` 意味着 Pod 中的 `simmemleak`
容器被终止并且（到目前为止）重启了五次。
原因 `OOMKilled` 显示容器尝试使用超出其限制的内存量。

你接下来要做的或许是检查应用代码，看看是否存在内存泄露。
如果你发现应用的行为与你所预期的相同，则可以考虑为该容器设置一个更高的内存限制
（也可能需要设置请求值）。

## {{% heading "whatsnext" %}}

* 获取[分配内存资源给容器和 Pod](/zh-cn/docs/tasks/configure-pod-container/assign-memory-resource/) 的实践经验
* 获取[分配 CPU 资源给容器和 Pod](/zh-cn/docs/tasks/configure-pod-container/assign-cpu-resource/) 的实践经验
* 阅读 API 参考如何定义[容器](/zh-cn/docs/reference/kubernetes-api/workload-resources/pod-v1/#Container)
  及其[资源请求](/zh-cn/docs/reference/kubernetes-api/workload-resources/pod-v1/#resources)。
* 阅读 XFS 中[项目配额](https://www.linux.org/docs/man8/xfs_quota.html)的文档
* 进一步阅读 [kube-scheduler 配置参考 (v1beta3)](/zh-cn/docs/reference/config-api/kube-scheduler-config.v1beta3/)
* 进一步阅读 [Pod 的服务质量等级](/zh-cn/docs/concepts/workloads/pods/pod-qos/)
