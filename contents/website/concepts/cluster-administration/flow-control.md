---
title: API 优先级和公平性
content_type: concept
min-kubernetes-server-version: v1.18
weight: 110
---


{{< feature-state state="beta"  for_k8s_version="v1.20" >}}

对于集群管理员来说，控制 Kubernetes API 服务器在过载情况下的行为是一项关键任务。
{{< glossary_tooltip term_id="kube-apiserver" text="kube-apiserver" >}}
有一些控件（例如：命令行标志 `--max-requests-inflight` 和 `--max-mutating-requests-inflight`），
可以限制将要接受的未处理的请求，从而防止过量请求入站，潜在导致 API 服务器崩溃。
但是这些标志不足以保证在高流量期间，最重要的请求仍能被服务器接受。

API 优先级和公平性（APF）是一种替代方案，可提升上述最大并发限制。
APF 以更细粒度的方式对请求进行分类和隔离。
它还引入了空间有限的排队机制，因此在非常短暂的突发情况下，API 服务器不会拒绝任何请求。
通过使用公平排队技术从队列中分发请求，这样，
一个行为不佳的{{< glossary_tooltip text="控制器" term_id="controller" >}}就不会饿死其他控制器
（即使优先级相同）。

本功能特性在设计上期望其能与标准控制器一起工作得很好；
这类控制器使用通知组件（Informers）获得信息并对 API 请求的失效作出反应，
在处理失效时能够执行指数型回退。其他客户端也以类似方式工作。

{{< caution >}}
属于 “长时间运行” 类型的某些请求（例如远程命令执行或日志拖尾）不受 API 优先级和公平性过滤器的约束。
如果未启用 APF 特性，即便设置 `--max-requests-inflight` 标志，该类请求也不受约束。
APF 适用于 **watch** 请求。当 APF 被禁用时，**watch** 请求不受 `--max-requests-inflight` 限制。
{{< /caution >}}


## 启用/禁用 API 优先级和公平性    {#enabling-api-priority-and-fairness}

API 优先级与公平性（APF）特性由特性门控控制，默认情况下启用。
有关特性门控的一般性描述以及如何启用和禁用特性门控，
请参见[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)。
APF 的特性门控称为 `APIPriorityAndFairness`。
此特性也与某个 {{< glossary_tooltip term_id="api-group" text="API 组" >}}相关：
(a) `v1alpha1` 和 `v1beta1` 版本，默认被禁用；
(b) `v1beta2` 和 `v1beta3` 版本，默认被启用。
你可以在启动 `kube-apiserver` 时，添加以下命令行标志来禁用此功能门控及 API Beta 组：

```shell
kube-apiserver \
--feature-gates=APIPriorityAndFairness=false \
--runtime-config=flowcontrol.apiserver.k8s.io/v1beta2=false,flowcontrol.apiserver.k8s.io/v1beta3=false \
  # ...其他配置不变
```

或者，你也可以通过
`--runtime-config=flowcontrol.apiserver.k8s.io/v1alpha1=true,flowcontrol.apiserver.k8s.io/v1beta1=true`
启用 API 组的 v1alpha1 和 v1beta1 版本。

命令行标志 `--enable-priority-fairness=false` 将彻底禁用 APF 特性，
即使其他标志启用它也是无效。

## 概念    {#concepts}

APF 特性包含几个不同的功能。
传入的请求通过 **FlowSchema** 按照其属性分类，并分配优先级。
每个优先级维护自定义的并发限制，加强了隔离度，这样不同优先级的请求，就不会相互饿死。
在同一个优先级内，公平排队算法可以防止来自不同 **流（Flow）** 的请求相互饿死。
该算法将请求排队，通过排队机制，防止在平均负载较低时，通信量突增而导致请求失败。

### 优先级    {#priority-levels}

如果未启用 APF，API 服务器中的整体并发量将受到 `kube-apiserver` 的参数
`--max-requests-inflight` 和 `--max-mutating-requests-inflight` 的限制。
启用 APF 后，将对这些参数定义的并发限制进行求和，然后将总和分配到一组可配置的 **优先级** 中。
每个传入的请求都会分配一个优先级；每个优先级都有各自的限制，设定特定限制允许分发的并发请求数。

例如，默认配置包括针对领导者选举请求、内置控制器请求和 Pod 请求都单独设置优先级。
这表示即使异常的 Pod 向 API 服务器发送大量请求，也无法阻止领导者选举或内置控制器的操作执行成功。

优先级的并发限制会被定期调整，允许利用率较低的优先级将并发度临时借给利用率很高的优先级。
这些限制基于一个优先级可以借出多少个并发度以及可以借用多少个并发度的额定限制和界限，
所有这些均源自下述配置对象。

### 请求占用的席位  {#seats-occupied-by-a-request}

上述并发管理的描述是基线情况。各个请求具有不同的持续时间，
但在与一个优先级的并发限制进行比较时，这些请求在任何给定时刻都以同等方式进行计数。
在这个基线场景中，每个请求占用一个并发单位。
我们用 “席位（Seat）” 一词来表示一个并发单位，其灵感来自火车或飞机上每位乘客占用一个固定座位的供应方式。

但有些请求所占用的席位不止一个。有些请求是服务器预估将返回大量对象的 **list** 请求。
我们发现这类请求会给服务器带来异常沉重的负担。
出于这个原因，服务器估算将返回的对象数量，并认为请求所占用的席位数与估算得到的数量成正比。

### watch 请求的执行时间调整  {#execution-time-tweak-for-watch-requests}

APF 管理 **watch** 请求，但这需要考量基线行为之外的一些情况。
第一个关注点是如何判定 **watch** 请求的席位占用时长。
取决于请求参数不同，对 **watch** 请求的响应可能以针对所有预先存在的对象 **create** 通知开头，也可能不这样。
一旦最初的突发通知（如果有）结束，APF 将认为 **watch** 请求已经用完其席位。

每当向服务器通知创建/更新/删除一个对象时，正常通知都会以并发突发的方式发送到所有相关的 **watch** 响应流。
为此，APF 认为每个写入请求都会在实际写入完成后花费一些额外的时间来占用席位。
服务器估算要发送的通知数量，并调整写入请求的席位数以及包含这些额外工作后的席位占用时间。

### 排队    {#queuing}

即使在同一优先级内，也可能存在大量不同的流量源。
在过载情况下，防止一个请求流饿死其他流是非常有价值的
（尤其是在一个较为常见的场景中，一个有故障的客户端会疯狂地向 kube-apiserver 发送请求，
理想情况下，这个有故障的客户端不应对其他客户端产生太大的影响）。
公平排队算法在处理具有相同优先级的请求时，实现了上述场景。
每个请求都被分配到某个 **流（Flow）** 中，该 **流** 由对应的 FlowSchema 的名字加上一个
**流区分项（Flow Distinguisher）** 来标识。
这里的流区分项可以是发出请求的用户、目标资源的名字空间或什么都不是。
系统尝试为不同流中具有相同优先级的请求赋予近似相等的权重。
要启用对不同实例的不同处理方式，多实例的控制器要分别用不同的用户名来执行身份认证。

将请求划分到流中之后，APF 功能将请求分配到队列中。
分配时使用一种称为{{< glossary_tooltip term_id="shuffle-sharding" text="混洗分片（Shuffle-Sharding）" >}}的技术。
该技术可以相对有效地利用队列隔离低强度流与高强度流。

排队算法的细节可针对每个优先等级进行调整，并允许管理员在内存占用、
公平性（当总流量超标时，各个独立的流将都会取得进展）、
突发流量的容忍度以及排队引发的额外延迟之间进行权衡。

### 豁免请求    {#exempt-requests}

某些特别重要的请求不受制于此特性施加的任何限制。
这些豁免可防止不当的流控配置完全禁用 API 服务器。

## 资源    {#resources}

流控 API 涉及两种资源。
[PriorityLevelConfiguration](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#prioritylevelconfiguration-v1beta2-flowcontrol-apiserver-k8s-io)
定义可用的优先级和可处理的并发预算量，还可以微调排队行为。
[FlowSchema](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#flowschema-v1beta2-flowcontrol-apiserver-k8s-io)
用于对每个入站请求进行分类，并与一个 PriorityLevelConfiguration 相匹配。
此外同一 API 组还有一个 `v1alpha1` 版本，其中包含语法和语义都相同的资源类别。

### PriorityLevelConfiguration

一个 PriorityLevelConfiguration 表示单个优先级。每个 PriorityLevelConfiguration
对未完成的请求数有各自的限制，对排队中的请求数也有限制。

PriorityLevelConfiguration 的额定并发限制不是指定请求绝对数量，而是以“额定并发份额”的形式指定。
API 服务器的总并发量限制通过这些份额按例分配到现有 PriorityLevelConfiguration 中，
为每个级别按照数量赋予其额定限制。
集群管理员可以更改 `--max-requests-inflight` （或 `--max-mutating-requests-inflight`）的值，
再重新启动 `kube-apiserver` 来增加或减小服务器的总流量，
然后所有的 PriorityLevelConfiguration 将看到其最大并发增加（或减少）了相同的比例。

{{< caution >}}
在 `v1beta3` 之前的版本中，相关的 PriorityLevelConfiguration
字段被命名为“保证并发份额”而不是“额定并发份额”。此外在 Kubernetes v1.25
及更早的版本中，不存在定期的调整：所实施的始终是额定/保证的限制，不存在调整。
{{< /caution >}}

一个优先级可以借出的并发数界限以及可以借用的并发数界限在
PriorityLevelConfiguration 表现该优先级的额定限制。
这些界限值乘以额定限制/100.0 并取整，被解析为绝对席位数量。
某优先级的动态调整并发限制范围被约束在
(a) 其额定限制的下限值减去其可借出的席位和
(b) 其额定限制的上限值加上它可以借用的席位之间。
在每次调整时，通过每个优先级推导得出动态限制，具体过程为回收最近出现需求的所有借出的席位，
然后在刚刚描述的界限内共同公平地响应有关这些优先级最近的席位需求。

{{< caution >}}
启用 APF 特性时，服务器的总并发限制被设置为 `--max-requests-inflight` 及
`--max-mutating-requests-inflight` 之和。变更性和非变更性请求之间不再有任何不同；
如果你想针对某给定资源分别进行处理，请制作单独的 FlowSchema，分别匹配变更性和非变更性的动作。
{{< /caution >}}

当入站请求的数量大于分配的 PriorityLevelConfiguration 中允许的并发级别时，
`type` 字段将确定对额外请求的处理方式。
`Reject` 类型，表示多余的流量将立即被 HTTP 429（请求过多）错误所拒绝。
`Queue` 类型，表示对超过阈值的请求进行排队，将使用阈值分片和公平排队技术来平衡请求流之间的进度。

公平排队算法支持通过排队配置对优先级微调。
可以在[增强建议](https://github.com/kubernetes/enhancements/tree/master/keps/sig-api-machinery/1040-priority-and-fairness)中阅读算法的详细信息，
但总之：

* `queues` 递增能减少不同流之间的冲突概率，但代价是增加了内存使用量。
  值为 1 时，会禁用公平排队逻辑，但仍允许请求排队。

* `queueLengthLimit` 递增可以在不丢弃任何请求的情况下支撑更大的突发流量，
  但代价是增加了等待时间和内存使用量。

* 修改 `handSize` 允许你调整过载情况下不同流之间的冲突概率以及单个流可用的整体并发性。

  {{< note >}}
  较大的 `handSize` 使两个单独的流程发生碰撞的可能性较小（因此，一个流可以饿死另一个流），
  但是更有可能的是少数流可以控制 apiserver。
  较大的 `handSize` 还可能增加单个高并发流的延迟量。
  单个流中可能排队的请求的最大数量为 `handSize * queueLengthLimit`。
  {{< /note >}}

下表显示了有趣的随机分片配置集合，每行显示给定的老鼠（低强度流）
被不同数量的大象挤压（高强度流）的概率。
表来源请参阅： https://play.golang.org/p/Gi0PLgVHiUg

{{< table caption = "混分切片配置示例" >}}
随机分片 | 队列数 | 1 个大象 | 4 个大象 | 16 个大象
|----------|-----------|------------|----------------|--------------------|
| 12 | 32 | 4.428838398950118e-09 | 0.11431348830099144 | 0.9935089607656024 |
| 10 | 32 | 1.550093439632541e-08 | 0.0626479840223545 | 0.9753101519027554 |
| 10 | 64 | 6.601827268370426e-12 | 0.00045571320990370776 | 0.49999929150089345 |
| 9 | 64 | 3.6310049976037345e-11 | 0.00045501212304112273 | 0.4282314876454858 |
| 8 | 64 | 2.25929199850899e-10 | 0.0004886697053040446 | 0.35935114681123076 |
| 8 | 128 | 6.994461389026097e-13 | 3.4055790161620863e-06 | 0.02746173137155063 |
| 7 | 128 | 1.0579122850901972e-11 | 6.960839379258192e-06 | 0.02406157386340147 |
| 7 | 256 | 7.597695465552631e-14 | 6.728547142019406e-08 | 0.0006709661542533682 |
| 6 | 256 | 2.7134626662687968e-12 | 2.9516464018476436e-07 | 0.0008895654642000348 |
| 6 | 512 | 4.116062922897309e-14 | 4.982983350480894e-09 | 2.26025764343413e-05 |
| 6 | 1024 | 6.337324016514285e-16 | 8.09060164312957e-11 | 4.517408062903668e-07 |
{{< /table >}}

### FlowSchema

FlowSchema 匹配一些入站请求，并将它们分配给优先级。
每个入站请求都会对 FlowSchema 测试是否匹配，
首先从 `matchingPrecedence` 数值最低的匹配开始，
然后依次进行，直到首个匹配出现。

{{< caution >}}
对一个请求来说，只有首个匹配的 FlowSchema  才有意义。
如果一个入站请求与多个 FlowSchema 匹配，则将基于逻辑上最高优先级 `matchingPrecedence` 的请求进行筛选。
如果一个请求匹配多个 FlowSchema 且 `matchingPrecedence` 的值相同，则按 `name` 的字典序选择最小，
但是最好不要依赖它，而是确保不存在两个 FlowSchema 具有相同的 `matchingPrecedence` 值。
{{< /caution >}}

当给定的请求与某个 FlowSchema 的 `rules` 的其中一条匹配，那么就认为该请求与该 FlowSchema 匹配。
判断规则与该请求是否匹配，**不仅**要求该条规则的 `subjects` 字段至少存在一个与该请求相匹配，
**而且**要求该条规则的 `resourceRules` 或 `nonResourceRules`
（取决于传入请求是针对资源 URL 还是非资源 URL）字段至少存在一个与该请求相匹配。

对于 `subjects` 中的 `name` 字段和资源和非资源规则的
`verbs`、`apiGroups`、`resources`、`namespaces` 和 `nonResourceURLs` 字段，
可以指定通配符 `*` 来匹配任意值，从而有效地忽略该字段。

FlowSchema 的 `distinguisherMethod.type` 字段决定了如何把与该模式匹配的请求分散到各个流中。
可能是 `ByUser`，在这种情况下，一个请求用户将无法饿死其他容量的用户；
或者是 `ByNamespace`，在这种情况下，一个名字空间中的资源请求将无法饿死其它名字空间的资源请求；
或者为空（或者可以完全省略 `distinguisherMethod`），
在这种情况下，与此 FlowSchema 匹配的请求将被视为单个流的一部分。
资源和你的特定环境决定了如何选择正确一个 FlowSchema。

## 默认值    {#defaults}

每个 kube-apiserver 会维护两种类型的 APF 配置对象：强制的（Mandatory）和建议的（Suggested）。

### 强制的配置对象   {#mandatory-configuration-objects}

有四种强制的配置对象对应内置的守护行为。这里的行为是服务器在还未创建对象之前就具备的行为，
而当这些对象存在时，其规约反映了这类行为。四种强制的对象如下：

* 强制的 `exempt` 优先级用于完全不受流控限制的请求：它们总是立刻被分发。
  强制的 `exempt` FlowSchema 把 `system:masters` 组的所有请求都归入该优先级。
  如果合适，你可以定义新的 FlowSchema，将其他请求定向到该优先级。

* 强制的 `catch-all` 优先级与强制的 `catch-all` FlowSchema 结合使用，
  以确保每个请求都分类。一般而言，你不应该依赖于 `catch-all` 的配置，
  而应适当地创建自己的 `catch-all` FlowSchema 和 PriorityLevelConfiguration
  （或使用默认安装的 `global-default` 配置）。
  因为这一优先级不是正常场景下要使用的，`catch-all` 优先级的并发度份额很小，
  并且不会对请求进行排队。

### 建议的配置对象   {#suggested-configuration-objects}

建议的 FlowSchema 和 PriorityLevelConfiguration 包含合理的默认配置。
你可以修改这些对象或者根据需要创建新的配置对象。如果你的集群可能承受较重负载，
那么你就要考虑哪种配置最合适。

建议的配置把请求分为六个优先级：

* `node-high` 优先级用于来自节点的健康状态更新。

* `system` 优先级用于 `system:nodes` 组（即 kubelet）的与健康状态更新无关的请求；
  kubelet 必须能连上 API 服务器，以便工作负载能够调度到其上。

* `leader-election` 优先级用于内置控制器的领导选举的请求
  （特别是来自 `kube-system` 名字空间中 `system:kube-controller-manager` 和
  `system:kube-scheduler` 用户和服务账号，针对 `endpoints`、`configmaps` 或 `leases` 的请求）。
  将这些请求与其他流量相隔离非常重要，因为领导者选举失败会导致控制器发生故障并重新启动，
  这反过来会导致新启动的控制器在同步信息时，流量开销更大。

* `workload-high` 优先级用于内置控制器的其他请求。
* `workload-low` 优先级用于来自所有其他服务帐户的请求，通常包括来自 Pod
  中运行的控制器的所有请求。
* `global-default` 优先级可处理所有其他流量，例如：非特权用户运行的交互式
  `kubectl` 命令。

建议的 FlowSchema 用来将请求导向上述的优先级内，这里不再一一列举。

### 强制的与建议的配置对象的维护   {#maintenance-of-the-mandatory-and-suggested-configuration-objects}

每个 `kube-apiserver` 都独立地维护其强制的与建议的配置对象，
这一维护操作既是服务器的初始行为，也是其周期性操作的一部分。
因此，当存在不同版本的服务器时，如果各个服务器对于配置对象中的合适内容有不同意见，
就可能出现抖动。

每个 `kube-apiserver` 都会对强制的与建议的配置对象执行初始的维护操作，
之后（每分钟）对这些对象执行周期性的维护。

对于强制的配置对象，维护操作包括确保对象存在并且包含合适的规约（如果存在的话）。
服务器会拒绝创建或更新与其守护行为不一致的规约。

对建议的配置对象的维护操作被设计为允许其规约被重载。删除操作是不允许的，
维护操作期间会重建这类配置对象。如果你不需要某个建议的配置对象，
你需要将它放在一边，并让其规约所产生的影响最小化。
对建议的配置对象而言，其维护方面的设计也支持在上线新的 `kube-apiserver`
时完成自动的迁移动作，即便可能因为当前的服务器集合存在不同的版本而可能造成抖动仍是如此。

对建议的配置对象的维护操作包括基于服务器建议的规约创建对象
（如果对象不存在的话）。反之，如果对象已经存在，维护操作的行为取决于是否
`kube-apiserver` 或者用户在控制对象。如果 `kube-apiserver` 在控制对象，
则服务器确保对象的规约与服务器所给的建议匹配，如果用户在控制对象，
对象的规约保持不变。

关于谁在控制对象这个问题，首先要看对象上的 `apf.kubernetes.io/autoupdate-spec`
注解。如果对象上存在这个注解，并且其取值为`true`，则 kube-apiserver
在控制该对象。如果存在这个注解，并且其取值为`false`，则用户在控制对象。
如果这两个条件都不满足，则需要进一步查看对象的 `metadata.generation`。
如果该值为 1，则 kube-apiserver 控制对象，否则用户控制对象。
这些规则是在 1.22 发行版中引入的，而对 `metadata.generation`
的考量是为了便于从之前较简单的行为迁移过来。希望控制建议的配置对象的用户应该将对象的
`apf.kubernetes.io/autoupdate-spec` 注解设置为 `false`。

对强制的或建议的配置对象的维护操作也包括确保对象上存在 `apf.kubernetes.io/autoupdate-spec`
这一注解，并且其取值准确地反映了是否 kube-apiserver 在控制着对象。

维护操作还包括删除那些既非强制又非建议的配置，同时注解配置为
`apf.kubernetes.io/autoupdate-spec=true` 的对象。

## 健康检查并发豁免    {#health-check-concurrency-exemption}

推荐配置没有为本地 kubelet 对 kube-apiserver 执行健康检查的请求进行任何特殊处理
——它们倾向于使用安全端口，但不提供凭据。
在推荐配置中，这些请求将分配 `global-default` FlowSchema 和 `global-default` 优先级，
这样其他流量可以排除健康检查。

如果添加以下 FlowSchema，健康检查请求不受速率限制。

{{< caution >}}
进行此更改后，任何敌对方都可以发送与此 FlowSchema 匹配的任意数量的健康检查请求。
如果你有 Web 流量过滤器或类似的外部安全机制保护集群的 API 服务器免受常规网络流量的侵扰，
则可以配置规则，阻止所有来自集群外部的健康检查请求。
{{< /caution >}}

{{< codenew file="priority-and-fairness/health-for-strangers.yaml" >}}

## 问题诊断    {#diagnostics}

启用了 APF 的 API 服务器，它每个 HTTP 响应都有两个额外的 HTTP 头：
`X-Kubernetes-PF-FlowSchema-UID` 和 `X-Kubernetes-PF-PriorityLevel-UID`，
注意与请求匹配的 FlowSchema 和已分配的优先级。
如果请求用户没有查看这些对象的权限，则这些 HTTP 头中将不包含 API 对象的名称，
因此在调试时，你可以使用类似如下的命令：

```shell
kubectl get flowschemas -o custom-columns="uid:{metadata.uid},name:{metadata.name}"
kubectl get prioritylevelconfigurations -o custom-columns="uid:{metadata.uid},name:{metadata.name}"
```

来获取 UID 到 FlowSchema 的名称和 UID 到 PriorityLevelConfiguration 的名称的映射。

## 可观察性    {#observability}

### 指标    {#metrics}

{{< note >}}
在 Kubernetes v1.20 之前的版本中，标签 `flow_schema` 和 `priority_level`
的名称有时被写作 `flowSchema` 和 `priorityLevel`，即存在不一致的情况。
如果你在运行 Kubernetes v1.19 或者更早版本，你需要参考你所使用的集群版本对应的文档。
{{< /note >}}

当你开启了 APF 后，kube-apiserver 会暴露额外指标。
监视这些指标有助于判断你的配置是否不当地限制了重要流量，
或者发现可能会损害系统健康的，行为不良的工作负载。

* `apiserver_flowcontrol_rejected_requests_total` 是一个计数器向量，
  记录被拒绝的请求数量（自服务器启动以来累计值），
  由标签 `flow_chema`（表示与请求匹配的 FlowSchema）、`priority_level`
  （表示分配给请该求的优先级）和 `reason` 来区分。
  `reason` 标签将是以下值之一：

  * `queue-full`，表明已经有太多请求排队
  * `concurrency-limit`，表示将 PriorityLevelConfiguration 配置为
    `Reject` 而不是 `Queue`，或者
  * `time-out`，表示在其排队时间超期的请求仍在队列中。
  * `cancelled`，表示该请求未被清除锁定，已从队列中移除。

* `apiserver_flowcontrol_dispatched_requests_total` 是一个计数器向量，
  记录开始执行的请求数量（自服务器启动以来的累积值），
  由 `flow_schema` 和 `priority_level` 来区分。


* `apiserver_current_inqueue_requests` 是一个表向量，
  记录最近排队请求数量的高水位线，
  由标签 `request_kind` 分组，标签的值为 `mutating` 或 `readOnly`。
  这些高水位线表示在最近一秒钟内看到的最大数字。
  它们补充说明了老的表向量 `apiserver_current_inflight_requests`
  （该量保存了最后一个窗口中，正在处理的请求数量的高水位线）。

* `apiserver_flowcontrol_read_vs_write_current_requests` 是一个直方图向量，
  在每个纳秒结束时记录请求数量的观察值，由标签 `phase`（取值为 `waiting` 及 `executing`）
  和 `request_kind`（取值为 `mutating` 及 `readOnly`）区分。
  每个观察到的值是一个介于 0 和 1 之间的比值，计算方式为请求数除以该请求数的对应限制
  （等待的队列长度限制和执行所用的并发限制）。

* `apiserver_flowcontrol_current_inqueue_requests` 是一个表向量，
  记录包含排队中的（未执行）请求的瞬时数量，
  由 `priority_level` 和 `flow_schema` 区分。

* `apiserver_flowcontrol_current_executing_requests` 是一个表向量，
  记录包含执行中（不在队列中等待）请求的瞬时数量，
  由 `priority_level` 和 `flow_schema` 进一步区分。

* `apiserver_flowcontrol_request_concurrency_in_use` 是一个规范向量，
  包含占用座位的瞬时数量，由 `priority_level` 和 `flow_schema` 进一步区分。

* `apiserver_flowcontrol_priority_level_request_utilization` 是一个直方图向量，
  在每个纳秒结束时记录请求数量的观察值，
  由标签 `phase`（取值为 `waiting` 及 `executing`）和 `priority_level` 区分。
  每个观察到的值是一个介于 0 和 1 之间的比值，计算方式为请求数除以该请求数的对应限制
  （等待的队列长度限制和执行所用的并发限制）。

* `apiserver_flowcontrol_priority_level_seat_utilization` 是一个直方图向量，
  在每个纳秒结束时记录某个优先级并发度限制利用率的观察值，由标签 `priority_level` 区分。
  此利用率是一个分数：（占用的席位数）/（并发限制）。
  此指标考虑了除 WATCH 之外的所有请求的所有执行阶段（包括写入结束时的正常延迟和额外延迟，
  以覆盖相应的通知操作）；对于 WATCH 请求，只考虑传递预先存在对象通知的初始阶段。
  该向量中的每个直方图也带有 `phase: executing`（等待阶段没有席位限制）的标签。

* `apiserver_flowcontrol_request_queue_length_after_enqueue` 是一个直方图向量，
  记录请求队列的长度，由 `priority_level` 和 `flow_schema` 进一步区分。
  每个排队中的请求都会为其直方图贡献一个样本，并在添加请求后立即上报队列的长度。
  请注意，这样产生的统计数据与无偏调查不同。

  {{< note >}}
  直方图中的离群值在这里表示单个流（即，一个用户或一个名字空间的请求，
  具体取决于配置）正在疯狂地向 API 服务器发请求，并受到限制。
  相反，如果一个优先级的直方图显示该优先级的所有队列都比其他优先级的队列长，
  则增加 PriorityLevelConfiguration 的并发份额是比较合适的。
  {{< /note >}}

* `apiserver_flowcontrol_request_concurrency_limit` 与
  `apiserver_flowcontrol_nominal_limit_seats` 相同。在优先级之间引入并发度借用之前，
  此字段始终等于 `apiserver_flowcontrol_current_limit_seats`
  （它过去不作为一个独立的指标存在）。

* `apiserver_flowcontrol_nominal_limit_seats` 是一个表向量，包含每个优先级的额定并发度限制，
  指标值根据 API 服务器的总并发度限制和各优先级所配置的额定并发度份额计算得出。

* `apiserver_flowcontrol_lower_limit_seats` 是一个表向量，包含每个优先级的动态并发度限制的下限。

* `apiserver_flowcontrol_upper_limit_seats` 是一个表向量，包含每个优先级的动态并发度限制的上限。

* `apiserver_flowcontrol_demand_seats` 是一个直方图向量，
  统计每纳秒结束时每个优先级的（席位需求）/（额定并发限制）比率的观察值。
  某优先级的席位需求是针对排队的请求和初始执行阶段的请求，在请求的初始和最终执行阶段占用的最大席位数之和。

* `apiserver_flowcontrol_demand_seats_high_watermark` 是一个表向量，
  为每个优先级包含了上一个并发度借用调整期间所观察到的最大席位需求。

* `apiserver_flowcontrol_demand_seats_average` 是一个表向量，
  为每个优先级包含了上一个并发度借用调整期间所观察到的时间加权平均席位需求。

* `apiserver_flowcontrol_demand_seats_stdev` 是一个表向量，
  为每个优先级包含了上一个并发度借用调整期间所观察到的席位需求的时间加权总标准偏差。

* `apiserver_flowcontrol_demand_seats_smoothed` 是一个表向量，
  为每个优先级包含了上一个并发度调整期间确定的平滑包络席位需求。

* `apiserver_flowcontrol_target_seats` 是一个表向量，
  包含每个优先级触发借用分配问题的并发度目标值。

* `apiserver_flowcontrol_seat_fair_frac` 是一个表向量，
  包含了上一个借用调整期间确定的公平分配比例。

* `apiserver_flowcontrol_current_limit_seats` 是一个表向量，
  包含每个优先级的上一次调整期间得出的动态并发限制。

* `apiserver_flowcontrol_request_wait_duration_seconds` 是一个直方图向量，
  记录请求排队的时间，
  由标签 `flow_schema`、`priority_level` 和 `execute` 进一步区分。
  标签 `execute` 表示请求是否开始执行。

  {{< note >}}
  由于每个 FlowSchema 总会给请求分配 PriorityLevelConfiguration，
  因此你可以为一个优先级添加所有 FlowSchema 的直方图，以获取分配给该优先级的请求的有效直方图。
  {{< /note >}}

* `apiserver_flowcontrol_request_execution_seconds` 是一个直方图向量，
  记录请求实际执行需要花费的时间，
  由标签 `flow_schema` 和 `priority_level` 进一步区分。

* `apiserver_flowcontrol_watch_count_samples` 是一个直方图向量，
  记录给定写的相关活动 WATCH 请求数量，
  由标签 `flow_schema` 和 `priority_level` 进一步区分。

* `apiserver_flowcontrol_work_estimated_seats` 是一个直方图向量，
  记录与估计席位（最初阶段和最后阶段的最多人数）相关联的请求数量，
  由标签 `flow_schema` 和 `priority_level` 进一步区分。

* `apiserver_flowcontrol_request_dispatch_no_accommodation_total`
  是一个事件数量的计数器，这些事件在原则上可能导致请求被分派，
  但由于并发度不足而没有被分派，
  由标签 `flow_schema` 和 `priority_level` 进一步区分。

### 调试端点    {#debug-endpoints}

启用 APF 特性后，kube-apiserver 会在其 HTTP/HTTPS 端口提供以下路径：

- `/debug/api_priority_and_fairness/dump_priority_levels` ——
  所有优先级及其当前状态的列表。你可以这样获取：

  ```shell
  kubectl get --raw /debug/api_priority_and_fairness/dump_priority_levels
  ```

  输出类似于：

  ```none
  PriorityLevelName, ActiveQueues, IsIdle, IsQuiescing, WaitingRequests, ExecutingRequests, DispatchedRequests, RejectedRequests, TimedoutRequests, CancelledRequests
  catch-all,         0,            true,   false,       0,               0,                 1,                  0,                0,                0
  exempt,            <none>,       <none>, <none>,      <none>,          <none>,            <none>,             <none>,           <none>,           <none>
  global-default,    0,            true,   false,       0,               0,                 46,                 0,                0,                0
  leader-election,   0,            true,   false,       0,               0,                 4,                  0,                0,                0
  node-high,         0,            true,   false,       0,               0,                 34,                 0,                0,                0
  system,            0,            true,   false,       0,               0,                 48,                 0,                0,                0
  workload-high,     0,            true,   false,       0,               0,                 500,                0,                0,                0
  workload-low,      0,            true,   false,       0,               0,                 0,                  0,                0,                0
  ```

- `/debug/api_priority_and_fairness/dump_queues` —— 所有队列及其当前状态的列表。
  你可以这样获取：

  ```shell
  kubectl get --raw /debug/api_priority_and_fairness/dump_queues
  ```

  输出类似于：

  ```none
  PriorityLevelName, Index,  PendingRequests, ExecutingRequests, VirtualStart,
  workload-high,     0,      0,               0,                 0.0000,
  workload-high,     1,      0,               0,                 0.0000,
  workload-high,     2,      0,               0,                 0.0000,
  ...
  leader-election,   14,     0,               0,                 0.0000,
  leader-election,   15,     0,               0,                 0.0000,
  ```

- `/debug/api_priority_and_fairness/dump_requests` —— 当前正在队列中等待的所有请求的列表。
  你可以这样获取：

  ```shell
  kubectl get --raw /debug/api_priority_and_fairness/dump_requests
  ```

  输出类似于：

  ```none
  PriorityLevelName, FlowSchemaName, QueueIndex, RequestIndexInQueue, FlowDistingsher,       ArriveTime,
  exempt,            <none>,         <none>,     <none>,              <none>,                <none>,
  system,            system-nodes,   12,         0,                   system:node:127.0.0.1, 2020-07-23T15:26:57.179170694Z,
  ```

  针对每个优先级别，输出中还包含一条虚拟记录，对应豁免限制。

  你可以使用以下命令获得更详细的清单：

  ```shell
  kubectl get --raw '/debug/api_priority_and_fairness/dump_requests?includeRequestDetails=1'
  ```

  输出类似于：

  ```none
  PriorityLevelName, FlowSchemaName, QueueIndex, RequestIndexInQueue, FlowDistingsher,       ArriveTime,                     UserName,              Verb,   APIPath,                                                     Namespace, Name,   APIVersion, Resource, SubResource,
  system,            system-nodes,   12,         0,                   system:node:127.0.0.1, 2020-07-23T15:31:03.583823404Z, system:node:127.0.0.1, create, /api/v1/namespaces/scaletest/configmaps,
  system,            system-nodes,   12,         1,                   system:node:127.0.0.1, 2020-07-23T15:31:03.594555947Z, system:node:127.0.0.1, create, /api/v1/namespaces/scaletest/configmaps,
  ```

### 调试日志生成行为  {#debug-logging}

在 `-v=3` 或更详细的情况下，服务器会为每个请求输出一行 httplog，它包括以下属性。

- `apf_fs`：请求被分类到的 FlowSchema 的名称。
- `apf_pl`：该 FlowSchema 的优先级名称。
- `apf_iseats`：为请求执行的初始（正常）阶段确定的席位数量。
- `apf_fseats`：为请求的最后执行阶段（考虑关联的 WATCH 通知）确定的席位数量。
- `apf_additionalLatency`：请求执行最后阶段的持续时间。

在更高级别的精细度下，将有日志行揭示 APF 如何处理请求的详细信息，主要用于调试目的。

### 响应头  {#response-headers}

APF 将以下两个头添加到每个 HTTP 响应消息中。

- `X-Kubernetes-PF-FlowSchema-UID` 保存相应请求被分类到的 FlowSchema 对象的 UID。
- `X-Kubernetes-PF-PriorityLevel-UID` 保存与该 FlowSchema 关联的 PriorityLevelConfiguration 对象的 UID。

## {{% heading "whatsnext" %}}

有关 API 优先级和公平性的设计细节的背景信息，
请参阅[增强提案](https://github.com/kubernetes/enhancements/tree/master/keps/sig-api-machinery/1040-priority-and-fairness)。
你可以通过 [SIG API Machinery](https://github.com/kubernetes/community/tree/master/sig-api-machinery/)
或特性的 [Slack 频道](https://kubernetes.slack.com/messages/api-priority-and-fairness/)提出建议和特性请求。
