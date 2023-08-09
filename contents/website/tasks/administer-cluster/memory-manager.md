---
title: 使用 NUMA 感知的内存管理器
content_type: task
min-kubernetes-server-version: v1.21
weight: 410
---



{{< feature-state state="beta" for_k8s_version="v1.22" >}}

Kubernetes 内存管理器（Memory Manager）为 `Guaranteed`
{{< glossary_tooltip text="QoS 类" term_id="qos-class" >}}
的 Pods 提供可保证的内存（及大页面）分配能力。

内存管理器使用提示生成协议来为 Pod 生成最合适的 NUMA 亲和性配置。
内存管理器将这类亲和性提示输入给中央管理器（即 Topology Manager）。
基于所给的提示和 Topology Manager（拓扑管理器）的策略设置，Pod
或者会被某节点接受，或者被该节点拒绝。

此外，内存管理器还确保 Pod 所请求的内存是从尽量少的 NUMA 节点分配而来。

内存管理器仅能用于 Linux 主机。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

为了使得内存资源与 Pod 规约中所请求的其他资源对齐：

- CPU 管理器应该被启用，并且在节点（Node）上要配置合适的 CPU 管理器策略，
  参见[控制 CPU 管理策略](/zh-cn/docs/tasks/administer-cluster/cpu-management-policies/)；
- 拓扑管理器要被启用，并且要在节点上配置合适的拓扑管理器策略，参见
  [控制拓扑管理器策略](/zh-cn/docs/tasks/administer-cluster/topology-manager/)。

从 v1.22 开始，内存管理器通过[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
`MemoryManager` 默认启用。

在 v1.22 之前，`kubelet` 必须在启动时设置如下标志：

`--feature-gates=MemoryManager=true`

这样内存管理器特性才会被启用。

## 内存管理器如何运作？

内存管理器目前为 Guaranteed QoS 类中的 Pod 提供可保证的内存（和大页面）分配能力。
若要立即将内存管理器启用，可参照[内存管理器配置](#memory-manager-configuration)节中的指南，
之后按[将 Pod 放入 Guaranteed QoS 类](#placing-a-pod-in-the-guaranteed-qos-class)
节中所展示的，准备并部署一个 `Guaranteed` Pod。

内存管理器是一个提示驱动组件（Hint Provider），负责为拓扑管理器提供拓扑提示，
后者根据这些拓扑提示对所请求的资源执行对齐操作。
内存管理器也会为 Pods 应用 `cgroups` 设置（即 `cpuset.mems`）。
与 Pod 准入和部署流程相关的完整流程图在[Memory Manager KEP: Design Overview][4]，
下面也有说明。

![Pod 准入与部署流程中的内存管理器](/images/docs/memory-manager-diagram.svg)

在这个过程中，内存管理器会更新其内部存储于[节点映射和内存映射][2]中的计数器，
从而管理有保障的内存分配。

内存管理器在启动和运行期间按下述逻辑更新节点映射（Node Map）。

### 启动  {#startup}

当节点管理员应用 `--reserved-memory` [预留内存标志](#reserved-memory-flag)时执行此逻辑。
这时，节点映射会被更新以反映内存的预留，如
[Memory Manager KEP: Memory Maps at start-up (with examples)][5]
所说明。

当配置了 `Static` 策略时，管理员必须提供 `--reserved-memory` 标志设置。

### 运行时  {#runtime} 

参考文献 [Memory Manager KEP: Memory Maps at runtime (with examples)][6]
中说明了成功的 Pod 部署是如何影响节点映射的，该文档也解释了可能发生的内存不足
（Out-of-memory，OOM）情况是如何进一步被 Kubernetes 或操作系统处理的。

在内存管理器运作的语境中，一个重要的话题是对 NUMA 分组的管理。
每当 Pod 的内存请求超出单个 NUMA 节点容量时，内存管理器会尝试创建一个包含多个
NUMA 节点的分组，从而扩展内存容量。解决这个问题的详细描述在文档
[Memory Manager KEP: How to enable the guaranteed memory allocation over many NUMA nodes?][3]
中。同时，关于 NUMA 分组是如何管理的，你还可以参考文档
[Memory Manager KEP: Simulation - how the Memory Manager works? (by examples)][1]。

## 内存管理器配置   {#memory-manager-configuration}

其他管理器也要预先配置。接下来，内存管理器特性需要被启用，
并且采用 `Static` 策略（[静态策略](#policy-static)）运行。
作为可选操作，可以预留一定数量的内存给系统或者 kubelet 进程以增强节点的稳定性
（[预留内存标志](#reserved-memory-flag)）。

### 策略    {#policies}

内存管理器支持两种策略。你可以通过 `kubelet` 标志 `--memory-manager-policy`
来选择一种策略：

* `None` （默认）
* `Static`

#### None 策略    {#policy-none}

这是默认的策略，并且不会以任何方式影响内存分配。该策略的行为好像内存管理器不存在一样。

`None` 策略返回默认的拓扑提示信息。这种特殊的提示会表明拓扑驱动组件（Hint Provider）
（在这里是内存管理器）对任何资源都没有与 NUMA 亲和性关联的偏好。

#### Static 策略    {#policy-static}

对 `Guaranteed` Pod 而言，`Static` 内存管理器策略会返回拓扑提示信息，
该信息与内存分配有保障的 NUMA 节点集合有关，并且内存管理器还通过更新内部的[节点映射][2]
对象来完成内存预留。

对 `BestEffort` 或 `Burstable` Pod 而言，因为不存在对有保障的内存资源的请求，
`Static` 内存管理器策略会返回默认的拓扑提示，并且不会通过内部的[节点映射][2]对象来预留内存。

### 预留内存标志    {#reserved-memory-flag}

[节点可分配](/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/)机制通常被节点管理员用来为
kubelet 或操作系统进程预留 K8S 节点上的系统资源，目的是提高节点稳定性。
有一组专用的标志可用于这个目的，为节点设置总的预留内存量。
此预配置的值接下来会被用来计算节点上对 Pods “可分配的”内存。

Kubernetes 调度器在优化 Pod 调度过程时，会考虑“可分配的”内存。
前面提到的标志包括 `--kube-reserved`、`--system-reserved` 和 `--eviction-threshold`。
这些标志值的综合计作预留内存的总量。

为内存管理器而新增加的 `--reserved-memory` 标志可以（让节点管理员）将总的预留内存进行划分，
并完成跨 NUMA 节点的预留操作。

标志设置的值是一个按 NUMA 节点的不同内存类型所给的内存预留的值的列表，用逗号分开。
可以使用分号作为分隔符来指定跨多个 NUMA 节点的内存预留。
只有在内存管理器特性被启用的语境下，这个参数才有意义。
内存管理器不会使用这些预留的内存来为容器负载分配内存。

例如，如果你有一个可用内存为 `10Gi` 的 NUMA 节点 "NUMA0"，而参数 `--reserved-memory`
被设置成要在 "NUMA0" 上预留 `1Gi` 的内存，那么内存管理器会假定节点上只有 `9Gi`
内存可用于容器负载。

你也可以忽略此参数，不过这样做时，你要清楚，所有 NUMA
节点上预留内存的数量要等于[节点可分配特性](/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/)
所设定的内存量。如果至少有一个节点可分配参数值为非零，你就需要至少为一个 NUMA
节点设置 `--reserved-memory`。实际上，`eviction-hard` 阈值默认为 `100Mi`，
所以当使用 `Static` 策略时，`--reserved-memory` 是必须设置的。

此外，应尽量避免如下配置：

1. 重复的配置，即同一 NUMA 节点或内存类型被设置不同的取值；
1. 为某种内存类型设置约束值为零；
1. 使用物理硬件上不存在的 NUMA 节点 ID；
1. 使用名字不是 `memory` 或 `hugepages-<size>` 的内存类型名称
   （特定的 `<size>` 的大页面也必须存在）。

语法：

`--reserved-memory N:memory-type1=value1,memory-type2=value2,...`

* `N`（整数）- NUMA 节点索引，例如，`0`
* `memory-type`（字符串）- 代表内存类型：
  * `memory` - 常规内存；
  * `hugepages-2Mi` 或 `hugepages-1Gi` - 大页面
* `value`（字符串） - 预留内存的量，例如 `1Gi`

用法示例：

`--reserved-memory 0:memory=1Gi,hugepages-1Gi=2Gi`

或者

`--reserved-memory 0:memory=1Gi --reserved-memory 1:memory=2Gi`


`--reserved-memory '0:memory=1Gi;1:memory=2Gi'`

当你为 `--reserved-memory` 标志指定取值时，必须要遵从之前通过节点可分配特性标志所设置的值。
换言之，对每种内存类型而言都要遵从下面的规则：

`sum(reserved-memory(i)) = kube-reserved + system-reserved + eviction-threshold` 

其中，`i` 是 NUMA 节点的索引。

如果你不遵守上面的公式，内存管理器会在启动时输出错误信息。

换言之，上面的例子我们一共要预留 `3Gi` 的常规内存（`type=memory`），即：

`sum(reserved-memory(i)) = reserved-memory(0) + reserved-memory(1) = 1Gi + 2Gi = 3Gi`

下面的例子中给出与节点可分配配置相关的 kubelet 命令行参数：

* `--kube-reserved=cpu=500m,memory=50Mi`
* `--system-reserved=cpu=123m,memory=333Mi`
* `--eviction-hard=memory.available<500Mi`

{{< note >}}
默认的硬性驱逐阈值是 100MiB，**不是**零。
请记得在使用 `--reserved-memory` 设置要预留的内存量时，加上这个硬性驱逐阈值。
否则 kubelet 不会启动内存管理器，而会输出一个错误信息。
{{< /note >}}

下面是一个正确配置的示例：

```shell
--feature-gates=MemoryManager=true
--kube-reserved=cpu=4,memory=4Gi
--system-reserved=cpu=1,memory=1Gi
--memory-manager-policy=Static
--reserved-memory '0:memory=3Gi;1:memory=2148Mi'
```

我们对上面的配置做一个检查：

1. `kube-reserved + system-reserved + eviction-hard(default) = reserved-memory(0) + reserved-memory(1)`
1. `4GiB + 1GiB + 100MiB = 3GiB + 2148MiB`
1. `5120MiB + 100MiB = 3072MiB + 2148MiB`
1. `5220MiB = 5220MiB` （这是对的）

## 将 Pod 放入 Guaranteed QoS 类  {#placing-a-pod-in-the-guaranteed-qos-class} 

若所选择的策略不是 `None`，则内存管理器会辨识处于 `Guaranteed` QoS 类中的 Pod。
内存管理器为每个 `Guaranteed` Pod 向拓扑管理器提供拓扑提示信息。
对于不在 `Guaranteed` QoS 类中的其他 Pod，内存管理器向拓扑管理器提供默认的拓扑提示信息。

下面的来自 Pod 清单的片段将 Pod 加入到 `Guaranteed` QoS 类中。

当 Pod 的 CPU `requests` 等于 `limits` 且为整数值时，Pod 将运行在 `Guaranteed` QoS 类中。

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "2"
        example.com/device: "1"
      requests:
        memory: "200Mi"
        cpu: "2"
        example.com/device: "1"
```

此外，共享 CPU 的 Pods 在 `requests` 等于 `limits` 值时也运行在 `Guaranteed` QoS 类中。

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "300m"
        example.com/device: "1"
      requests:
        memory: "200Mi"
        cpu: "300m"
        example.com/device: "1"
```

要注意的是，只有 CPU 和内存请求都被设置时，Pod 才会进入 Guaranteed QoS 类。

## 故障排查   {#troubleshooting}

下面的方法可用来排查为什么 Pod 无法被调度或者被节点拒绝：

- Pod 状态 - 可表明拓扑亲和性错误
- 系统日志 - 包含用来调试的有价值的信息，例如，关于所生成的提示信息
- 状态文件 - 其中包含内存管理器内部状态的转储（包含[节点映射和内存映射][2]）
- 从 v1.22 开始，[设备插件资源 API](#device-plugin-resource-api) 
  可以用来检索关于为容器预留的内存的信息

### Pod 状态 （TopologyAffinityError）   {#TopologyAffinityError}

这类错误通常在以下情形出现：

* 节点缺少足够的资源来满足 Pod 请求
* Pod 的请求因为特定的拓扑管理器策略限制而被拒绝

错误信息会出现在 Pod 的状态中：

```shell
kubectl get pods
```

```none
NAME         READY   STATUS                  RESTARTS   AGE
guaranteed   0/1     TopologyAffinityError   0          113s
```

使用 `kubectl describe pod <id>` 或 `kubectl get events` 可以获得详细的错误信息。

```none
Warning  TopologyAffinityError  10m   kubelet, dell8  Resources cannot be allocated with Topology locality
```

### 系统日志     {#system-logs}

针对特定的 Pod 搜索系统日志。

内存管理器为 Pod 所生成的提示信息可以在日志中找到。
此外，日志中应该也存在 CPU 管理器所生成的提示信息。

拓扑管理器将这些提示信息进行合并，计算得到唯一的最合适的提示数据。
此最佳提示数据也应该出现在日志中。

最佳提示表明要在哪里分配所有的资源。拓扑管理器会用当前的策略来测试此数据，
并基于得出的结论或者接纳 Pod 到节点，或者将其拒绝。

此外，你可以搜索日志查找与内存管理器相关的其他条目，例如 `cgroups` 和
`cpuset.mems` 的更新信息等。

### 检查节点上内存管理器状态

我们首先部署一个 `Guaranteed` Pod 示例，其规约如下所示：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: guaranteed
spec:
  containers:
  - name: guaranteed
    image: consumer
    imagePullPolicy: Never
    resources:
      limits:
        cpu: "2"
        memory: 150Gi
      requests:
        cpu: "2"
        memory: 150Gi
    command: ["sleep","infinity"]
```

接下来，我们登录到 Pod 运行所在的节点，检查位于
`/var/lib/kubelet/memory_manager_state` 的状态文件：

```json
{
   "policyName":"Static",
   "machineState":{
      "0":{
         "numberOfAssignments":1,
         "memoryMap":{
            "hugepages-1Gi":{
               "total":0,
               "systemReserved":0,
               "allocatable":0,
               "reserved":0,
               "free":0
            },
            "memory":{
               "total":134987354112,
               "systemReserved":3221225472,
               "allocatable":131766128640,
               "reserved":131766128640,
               "free":0
            }
         },
         "nodes":[
            0,
            1
         ]
      },
      "1":{
         "numberOfAssignments":1,
         "memoryMap":{
            "hugepages-1Gi":{
               "total":0,
               "systemReserved":0,
               "allocatable":0,
               "reserved":0,
               "free":0
            },
            "memory":{
               "total":135286722560,
               "systemReserved":2252341248,
               "allocatable":133034381312,
               "reserved":29295144960,
               "free":103739236352
            }
         },
         "nodes":[
            0,
            1
         ]
      }
   },
   "entries":{
      "fa9bdd38-6df9-4cf9-aa67-8c4814da37a8":{
         "guaranteed":[
            {
               "numaAffinity":[
                  0,
                  1
               ],
               "type":"memory",
               "size":161061273600
            }
         ]
      }
   },
   "checksum":4142013182
}
```

从这个状态文件，可以推断 Pod 被同时绑定到两个 NUMA 节点，即：

```json
"numaAffinity":[
   0,
   1
],
```

术语绑定（pinned）意味着 Pod 的内存使用被（通过 `cgroups` 配置）限制到这些 NUMA 节点。

这也直接意味着内存管理器已经创建了一个 NUMA 分组，由这两个 NUMA 节点组成，
即索引值分别为 `0` 和 `1` 的 NUMA 节点。

注意 NUMA 分组的管理是有一个相对复杂的管理器处理的，
相关逻辑的进一步细节可在内存管理器的 KEP 中[示例1][1]和[跨 NUMA 节点][3]节找到。

为了分析 NUMA 组中可用的内存资源，必须对分组内 NUMA 节点对应的条目进行汇总。

例如，NUMA 分组中空闲的“常规”内存的总量可以通过将分组内所有 NUMA
节点上空闲内存加和来计算，即将 NUMA 节点 `0` 和 NUMA 节点 `1`  的 `"memory"` 节
（分别是 `"free":0` 和 `"free": 103739236352`）相加，得到此分组中空闲的“常规”
内存总量为 `0 + 103739236352` 字节。

`"systemReserved": 3221225472` 这一行表明节点的管理员使用 `--reserved-memory` 为 NUMA
节点 `0` 上运行的 kubelet 和系统进程预留了 `3221225472` 字节 （即 `3Gi`）。

### 设备插件资源 API     {#device-plugin-resource-api}

kubelet 提供了一个 `PodResourceLister` gRPC 服务来启用对资源和相关元数据的检测。
通过使用它的
[List gRPC 端点](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#grpc-endpoint-list)，
可以获得每个容器的预留内存信息，该信息位于 protobuf 协议的 `ContainerMemory` 消息中。
只能针对 Guaranteed QoS 类中的 Pod 来检索此信息。

## {{% heading "whatsnext" %}}

- [Memory Manager KEP: Design Overview][4]
- [Memory Manager KEP: Memory Maps at start-up (with examples)][5]
- [Memory Manager KEP: Memory Maps at runtime (with examples)][6]
- [Memory Manager KEP: Simulation - how the Memory Manager works? (by examples)][1]
- [Memory Manager KEP: The Concept of Node Map and Memory Maps][2]
- [Memory Manager KEP: How to enable the guaranteed memory allocation over many NUMA nodes?][3]

[1]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1769-memory-manager#simulation---how-the-memory-manager-works-by-examples
[2]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1769-memory-manager#the-concept-of-node-map-and-memory-maps
[3]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1769-memory-manager#how-to-enable-the-guaranteed-memory-allocation-over-many-numa-nodes
[4]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1769-memory-manager#design-overview
[5]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1769-memory-manager#memory-maps-at-start-up-with-examples
[6]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1769-memory-manager#memory-maps-at-runtime-with-examples
