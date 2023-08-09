---
title: Pod 优先级和抢占
content_type: concept
weight: 90
---



{{< feature-state for_k8s_version="v1.14" state="stable" >}}

[Pod](/zh-cn/docs/concepts/workloads/pods/) 可以有**优先级**。
优先级表示一个 Pod 相对于其他 Pod 的重要性。
如果一个 Pod 无法被调度，调度程序会尝试抢占（驱逐）较低优先级的 Pod，
以使悬决 Pod 可以被调度。


{{< warning >}}
在一个并非所有用户都是可信的集群中，恶意用户可能以最高优先级创建 Pod，
导致其他 Pod 被驱逐或者无法被调度。
管理员可以使用 ResourceQuota 来阻止用户创建高优先级的 Pod。
参见[默认限制优先级消费](/zh-cn/docs/concepts/policy/resource-quotas/#limit-priority-class-consumption-by-default)。

{{< /warning >}}

## 如何使用优先级和抢占 {#how-to-use-priority-and-preemption}

要使用优先级和抢占：

1.  新增一个或多个 [PriorityClass](#priorityclass)。

1.  创建 Pod，并将其 [`priorityClassName`](#pod-priority) 设置为新增的 PriorityClass。
    当然你不需要直接创建 Pod；通常，你将会添加 `priorityClassName` 到集合对象（如 Deployment）
    的 Pod 模板中。

继续阅读以获取有关这些步骤的更多信息。

{{< note >}}
Kubernetes 已经提供了 2 个 PriorityClass：
`system-cluster-critical` 和 `system-node-critical`。
这些是常见的类，用于[确保始终优先调度关键组件](/zh-cn/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/)。
{{< /note >}}

## PriorityClass {#priorityclass}

PriorityClass 是一个无命名空间对象，它定义了从优先级类名称到优先级整数值的映射。
名称在 PriorityClass 对象元数据的 `name` 字段中指定。
值在必填的 `value` 字段中指定。值越大，优先级越高。
PriorityClass 对象的名称必须是有效的
[DNS 子域名](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)，
并且它不能以 `system-` 为前缀。

PriorityClass 对象可以设置任何小于或等于 10 亿的 32 位整数值。
这意味着 PriorityClass 对象的值范围是从 -2,147,483,648 到 1,000,000,000（含）。
保留更大的数字，用于表示关键系统 Pod 的内置 PriorityClass。
集群管理员应该为这类映射分别创建独立的 PriorityClass 对象。

PriorityClass 还有两个可选字段：`globalDefault` 和 `description`。
`globalDefault` 字段表示这个 PriorityClass 的值应该用于没有 `priorityClassName` 的 Pod。
系统中只能存在一个 `globalDefault` 设置为 true 的 PriorityClass。
如果不存在设置了 `globalDefault` 的 PriorityClass，
则没有 `priorityClassName` 的 Pod 的优先级为零。

`description` 字段是一个任意字符串。
它用来告诉集群用户何时应该使用此 PriorityClass。

### 关于 PodPriority 和现有集群的注意事项 {#notes-about-podpriority-and-existing-clusters}

- 如果你升级一个已经存在的但尚未使用此特性的集群，该集群中已经存在的 Pod 的优先级等效于零。

- 添加一个将 `globalDefault` 设置为 `true` 的 PriorityClass 不会改变现有 Pod 的优先级。
  此类 PriorityClass 的值仅用于添加 PriorityClass 后创建的 Pod。

- 如果你删除了某个 PriorityClass 对象，则使用被删除的 PriorityClass 名称的现有 Pod 保持不变，
  但是你不能再创建使用已删除的 PriorityClass 名称的 Pod。

### PriorityClass 示例 {#example-priorityclass}

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "此优先级类应仅用于 XYZ 服务 Pod。"
```

## 非抢占式 PriorityClass {#non-preempting-priority-class}

{{< feature-state for_k8s_version="v1.24" state="stable" >}}

配置了 `preemptionPolicy: Never` 的 Pod 将被放置在调度队列中较低优先级 Pod 之前，
但它们不能抢占其他 Pod。等待调度的非抢占式 Pod 将留在调度队列中，直到有足够的可用资源，
它才可以被调度。非抢占式 Pod，像其他 Pod 一样，受调度程序回退的影响。
这意味着如果调度程序尝试这些 Pod 并且无法调度它们，它们将以更低的频率被重试，
从而允许其他优先级较低的 Pod 排在它们之前。

非抢占式 Pod 仍可能被其他高优先级 Pod 抢占。

`preemptionPolicy` 默认为 `PreemptLowerPriority`，
这将允许该 PriorityClass 的 Pod 抢占较低优先级的 Pod（现有默认行为也是如此）。
如果 `preemptionPolicy` 设置为 `Never`，则该 PriorityClass 中的 Pod 将是非抢占式的。

数据科学工作负载是一个示例用例。用户可以提交他们希望优先于其他工作负载的作业，
但不希望因为抢占运行中的 Pod 而导致现有工作被丢弃。
设置为 `preemptionPolicy: Never` 的高优先级作业将在其他排队的 Pod 之前被调度，
只要足够的集群资源“自然地”变得可用。

### 非抢占式 PriorityClass 示例   {#example-non-preempting-priorityclass}

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority-nonpreempting
value: 1000000
preemptionPolicy: Never
globalDefault: false
description: "This priority class will not cause other pods to be preempted."
```

## Pod 优先级 {#pod-priority}

在你拥有一个或多个 PriorityClass 对象之后，
你可以创建在其规约中指定这些 PriorityClass 名称之一的 Pod。
优先级准入控制器使用 `priorityClassName` 字段并填充优先级的整数值。
如果未找到所指定的优先级类，则拒绝 Pod。

以下 YAML 是 Pod 配置的示例，它使用在前面的示例中创建的 PriorityClass。
优先级准入控制器检查 Pod 规约并将其优先级解析为 1000000。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: test
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  priorityClassName: high-priority
```

### Pod 优先级对调度顺序的影响 {#effect-of-pod-priority-on-scheduling-order}

当启用 Pod 优先级时，调度程序会按优先级对悬决 Pod 进行排序，
并且每个悬决的 Pod 会被放置在调度队列中其他优先级较低的悬决 Pod 之前。
因此，如果满足调度要求，较高优先级的 Pod 可能会比具有较低优先级的 Pod 更早调度。
如果无法调度此类 Pod，调度程序将继续并尝试调度其他较低优先级的 Pod。

## 抢占    {#preemption}

Pod 被创建后会进入队列等待调度。
调度器从队列中挑选一个 Pod 并尝试将它调度到某个节点上。
如果没有找到满足 Pod 的所指定的所有要求的节点，则触发对悬决 Pod 的抢占逻辑。
让我们将悬决 Pod 称为 P。抢占逻辑试图找到一个节点，
在该节点中删除一个或多个优先级低于 P 的 Pod，则可以将 P 调度到该节点上。
如果找到这样的节点，一个或多个优先级较低的 Pod 会被从节点中驱逐。
被驱逐的 Pod 消失后，P 可以被调度到该节点上。

### 用户暴露的信息 {#user-exposed-information}

当 Pod P 抢占节点 N 上的一个或多个 Pod 时，
Pod P 状态的 `nominatedNodeName` 字段被设置为节点 N 的名称。
该字段帮助调度程序跟踪为 Pod P 保留的资源，并为用户提供有关其集群中抢占的信息。

请注意，Pod P 不一定会调度到“被提名的节点（Nominated Node）”。
调度程序总是在迭代任何其他节点之前尝试“指定节点”。
在 Pod 因抢占而牺牲时，它们将获得体面终止期。
如果调度程序正在等待牺牲者 Pod 终止时另一个节点变得可用，
则调度程序可以使用另一个节点来调度 Pod P。
因此，Pod 规约中的 `nominatedNodeName` 和 `nodeName` 并不总是相同。
此外，如果调度程序抢占节点 N 上的 Pod，但随后比 Pod P 更高优先级的 Pod 到达，
则调度程序可能会将节点 N 分配给新的更高优先级的 Pod。
在这种情况下，调度程序会清除 Pod P 的 `nominatedNodeName`。
通过这样做，调度程序使 Pod P 有资格抢占另一个节点上的 Pod。

### 抢占的限制 {#limitations-of-preemption}

#### 被抢占牺牲者的体面终止

当 Pod 被抢占时，牺牲者会得到他们的
[体面终止期](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)。
它们可以在体面终止期内完成工作并退出。如果它们不这样做就会被杀死。
这个体面终止期在调度程序抢占 Pod 的时间点和待处理的 Pod (P)
可以在节点 (N) 上调度的时间点之间划分出了一个时间跨度。
同时，调度器会继续调度其他待处理的 Pod。当牺牲者退出或被终止时，
调度程序会尝试在待处理队列中调度 Pod。
因此，调度器抢占牺牲者的时间点与 Pod P 被调度的时间点之间通常存在时间间隔。
为了最小化这个差距，可以将低优先级 Pod 的体面终止时间设置为零或一个小数字。

#### 支持 PodDisruptionBudget，但不保证

[PodDisruptionBudget](/zh-cn/docs/concepts/workloads/pods/disruptions/)
(PDB) 允许多副本应用程序的所有者限制因自愿性质的干扰而同时终止的 Pod 数量。
Kubernetes 在抢占 Pod 时支持 PDB，但对 PDB 的支持是基于尽力而为原则的。
调度器会尝试寻找不会因被抢占而违反 PDB 的牺牲者，但如果没有找到这样的牺牲者，
抢占仍然会发生，并且即使违反了 PDB 约束也会删除优先级较低的 Pod。

#### 与低优先级 Pod 之间的 Pod 间亲和性

只有当这个问题的答案是肯定的时，才考虑在一个节点上执行抢占操作：
“如果从此节点上删除优先级低于悬决 Pod 的所有 Pod，悬决 Pod 是否可以在该节点上调度？”

{{< note >}}
抢占并不一定会删除所有较低优先级的 Pod。
如果悬决 Pod 可以通过删除少于所有较低优先级的 Pod 来调度，
那么只有一部分较低优先级的 Pod 会被删除。
即便如此，上述问题的答案必须是肯定的。
如果答案是否定的，则不考虑在该节点上执行抢占。
{{< /note >}}

如果悬决 Pod 与节点上的一个或多个较低优先级 Pod 具有 Pod 间{{< glossary_tooltip text="亲和性" term_id="affinity" >}}，
则在没有这些较低优先级 Pod 的情况下，无法满足 Pod 间亲和性规则。
在这种情况下，调度程序不会抢占节点上的任何 Pod。
相反，它寻找另一个节点。调度程序可能会找到合适的节点，
也可能不会。无法保证悬决 Pod 可以被调度。

我们针对此问题推荐的解决方案是仅针对同等或更高优先级的 Pod 设置 Pod 间亲和性。

#### 跨节点抢占

假设正在考虑在一个节点 N 上执行抢占，以便可以在 N 上调度待处理的 Pod P。
只有当另一个节点上的 Pod 被抢占时，P 才可能在 N 上变得可行。
下面是一个例子：

* 调度器正在考虑将 Pod P 调度到节点 N 上。
* Pod Q 正在与节点 N 位于同一区域的另一个节点上运行。
* Pod P 与 Pod Q 具有 Zone 维度的反亲和（`topologyKey:topology.kubernetes.io/zone`）设置。
* Pod P 与 Zone 中的其他 Pod 之间没有其他反亲和性设置。
* 为了在节点 N 上调度 Pod P，可以抢占 Pod Q，但调度器不会进行跨节点抢占。
  因此，Pod P 将被视为在节点 N 上不可调度。

如果将 Pod Q 从所在节点中移除，则不会违反 Pod 间反亲和性约束，
并且 Pod P 可能会被调度到节点 N 上。

如果有足够的需求，并且如果我们找到性能合理的算法，
我们可能会考虑在未来版本中添加跨节点抢占。

## 故障排除 {#troubleshooting}

Pod 优先级和抢占可能会产生不必要的副作用。以下是一些潜在问题的示例以及处理这些问题的方法。

### Pod 被不必要地抢占

抢占在资源压力较大时从集群中删除现有 Pod，为更高优先级的悬决 Pod 腾出空间。
如果你错误地为某些 Pod 设置了高优先级，这些无意的高优先级 Pod 可能会导致集群中出现抢占行为。
Pod 优先级是通过设置 Pod 规约中的 `priorityClassName` 字段来指定的。
优先级的整数值然后被解析并填充到 `podSpec` 的 `priority` 字段。

为了解决这个问题，你可以将这些 Pod 的 `priorityClassName` 更改为使用较低优先级的类，
或者将该字段留空。默认情况下，空的 `priorityClassName` 解析为零。

当 Pod 被抢占时，集群会为被抢占的 Pod 记录事件。只有当集群没有足够的资源用于 Pod 时，
才会发生抢占。在这种情况下，只有当悬决 Pod（抢占者）的优先级高于受害 Pod 时才会发生抢占。
当没有悬决 Pod，或者悬决 Pod 的优先级等于或低于牺牲者时，不得发生抢占。
如果在这种情况下发生抢占，请提出问题。

### 有 Pod 被抢占，但抢占者并没有被调度

当 Pod 被抢占时，它们会收到请求的体面终止期，默认为 30 秒。
如果受害 Pod 在此期限内没有终止，它们将被强制终止。
一旦所有牺牲者都离开，就可以调度抢占者 Pod。

在抢占者 Pod 等待牺牲者离开的同时，可能某个适合同一个节点的更高优先级的 Pod 被创建。
在这种情况下，调度器将调度优先级更高的 Pod 而不是抢占者。

这是预期的行为：具有较高优先级的 Pod 应该取代具有较低优先级的 Pod。

### 优先级较高的 Pod 在优先级较低的 Pod 之前被抢占

调度程序尝试查找可以运行悬决 Pod 的节点。如果没有找到这样的节点，
调度程序会尝试从任意节点中删除优先级较低的 Pod，以便为悬决 Pod 腾出空间。
如果具有低优先级 Pod 的节点无法运行悬决 Pod，
调度器可能会选择另一个具有更高优先级 Pod 的节点（与其他节点上的 Pod 相比）进行抢占。
牺牲者的优先级必须仍然低于抢占者 Pod。

当有多个节点可供执行抢占操作时，调度器会尝试选择具有一组优先级最低的 Pod 的节点。
但是，如果此类 Pod 具有 PodDisruptionBudget，当它们被抢占时，
则会违反 PodDisruptionBudget，那么调度程序可能会选择另一个具有更高优先级 Pod 的节点。

当存在多个节点抢占且上述场景均不适用时，调度器会选择优先级最低的节点。

## Pod 优先级和服务质量之间的相互作用 {#interactions-of-pod-priority-and-qos}

Pod 优先级和 {{<glossary_tooltip text="QoS 类" term_id="qos-class" >}}
是两个正交特征，交互很少，并且对基于 QoS 类设置 Pod 的优先级没有默认限制。
调度器的抢占逻辑在选择抢占目标时不考虑 QoS。
抢占会考虑 Pod 优先级并尝试选择一组优先级最低的目标。
仅当移除优先级最低的 Pod 不足以让调度程序调度抢占式 Pod，
或者最低优先级的 Pod 受 PodDisruptionBudget 保护时，才会考虑优先级较高的 Pod。

kubelet 使用优先级来确定
[节点压力驱逐](/zh-cn/docs/concepts/scheduling-eviction/node-pressure-eviction/) Pod 的顺序。
你可以使用 QoS 类来估计 Pod 最有可能被驱逐的顺序。kubelet 根据以下因素对 Pod 进行驱逐排名：

1. 对紧俏资源的使用是否超过请求值
1. Pod 优先级
1. 相对于请求的资源使用量

有关更多详细信息，请参阅
[kubelet 驱逐时 Pod 的选择](/zh-cn/docs/concepts/scheduling-eviction/node-pressure-eviction/#pod-selection-for-kubelet-eviction)。

当某 Pod 的资源用量未超过其请求时，kubelet 节点压力驱逐不会驱逐该 Pod。
如果优先级较低的 Pod 的资源使用量没有超过其请求，则不会被驱逐。
另一个优先级较高且资源使用量超过其请求的 Pod 可能会被驱逐。

## {{% heading "whatsnext" %}}

* 阅读有关将 ResourceQuota 与 PriorityClass 结合使用的信息：
  [默认限制优先级消费](/zh-cn/docs/concepts/policy/resource-quotas/#limit-priority-class-consumption-by-default)
* 了解 [Pod 干扰](/zh-cn/docs/concepts/workloads/pods/disruptions/)
* 了解 [API 发起的驱逐](/zh-cn/docs/concepts/scheduling-eviction/api-eviction/)
* 了解[节点压力驱逐](/zh-cn/docs/concepts/scheduling-eviction/node-pressure-eviction/)
