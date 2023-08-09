---
title: Job
content_type: concept
feature:
  title: 批量执行
  description: >
    除了服务之外，Kubernetes 还可以管理你的批处理和 CI 工作负载，在期望时替换掉失效的容器。
weight: 50
---


Job 会创建一个或者多个 Pod，并将继续重试 Pod 的执行，直到指定数量的 Pod 成功终止。
随着 Pod 成功结束，Job 跟踪记录成功完成的 Pod 个数。
当数量达到指定的成功个数阈值时，任务（即 Job）结束。
删除 Job 的操作会清除所创建的全部 Pod。
挂起 Job 的操作会删除 Job 的所有活跃 Pod，直到 Job 被再次恢复执行。

一种简单的使用场景下，你会创建一个 Job 对象以便以一种可靠的方式运行某 Pod 直到完成。
当第一个 Pod 失败或者被删除（比如因为节点硬件失效或者重启）时，Job
对象会启动一个新的 Pod。

你也可以使用 Job 以并行的方式运行多个 Pod。

如果你想按某种排期表（Schedule）运行 Job（单个任务或多个并行任务），请参阅
[CronJob](/zh-cn/docs/concepts/workloads/controllers/cron-jobs/)。


## 运行示例 Job     {#running-an-example-job}

下面是一个 Job 配置示例。它负责计算 π 到小数点后 2000 位，并将结果打印出来。
此计算大约需要 10 秒钟完成。

{{< codenew file="controllers/job.yaml" >}}

你可以使用下面的命令来运行此示例：

```shell
kubectl apply -f https://kubernetes.io/examples/controllers/job.yaml
```

输出类似于：

```
job.batch/pi created
```

使用 `kubectl` 来检查 Job 的状态：

{{< tabs name="Check status of Job" >}}
{{< tab name="kubectl describe job pi" codelang="bash" >}}
Name:           pi
Namespace:      default
Selector:       batch.kubernetes.io/controller-uid=c9948307-e56d-4b5d-8302-ae2d7b7da67c
Labels:         batch.kubernetes.io/controller-uid=c9948307-e56d-4b5d-8302-ae2d7b7da67c
                batch.kubernetes.io/job-name=pi
                ...
Annotations:    batch.kubernetes.io/job-tracking: ""
Parallelism:    1
Completions:    1
Start Time:     Mon, 02 Dec 2019 15:20:11 +0200
Completed At:   Mon, 02 Dec 2019 15:21:16 +0200
Duration:       65s
Pods Statuses:  0 Running / 1 Succeeded / 0 Failed
Pod Template:
  Labels:  batch.kubernetes.io/controller-uid=c9948307-e56d-4b5d-8302-ae2d7b7da67c
           batch.kubernetes.io/job-name=pi
  Containers:
   pi:
    Image:      perl:5.34.0
    Port:       <none>
    Host Port:  <none>
    Command:
      perl
      -Mbignum=bpi
      -wle
      print bpi(2000)
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age   From            Message
  ----    ------            ----  ----            -------
  Normal  SuccessfulCreate  21s   job-controller  Created pod: pi-xf9p4
  Normal  Completed         18s   job-controller  Job completed
{{< /tab >}}
{{< tab name="kubectl get job pi -o yaml" codelang="bash" >}}
apiVersion: batch/v1
kind: Job
metadata:
  annotations: batch.kubernetes.io/job-tracking: ""
             ...  
  creationTimestamp: "2022-11-10T17:53:53Z"
  generation: 1
  labels:
    batch.kubernetes.io/controller-uid: 863452e6-270d-420e-9b94-53a54146c223
    batch.kubernetes.io/job-name: pi
  name: pi
  namespace: default
  resourceVersion: "4751"
  uid: 204fb678-040b-497f-9266-35ffa8716d14
spec:
  backoffLimit: 4
  completionMode: NonIndexed
  completions: 1
  parallelism: 1
  selector:
    matchLabels:
      batch.kubernetes.io/controller-uid: 863452e6-270d-420e-9b94-53a54146c223
  suspend: false
  template:
    metadata:
      creationTimestamp: null
      labels:
        batch.kubernetes.io/controller-uid: 863452e6-270d-420e-9b94-53a54146c223
        batch.kubernetes.io/job-name: pi
    spec:
      containers:
      - command:
        - perl
        - -Mbignum=bpi
        - -wle
        - print bpi(2000)
        image: perl:5.34.0
        imagePullPolicy: IfNotPresent
        name: pi
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Never
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
  active: 1
  ready: 0
  startTime: "2022-11-10T17:53:57Z"
  uncountedTerminatedPods: {}
{{< /tab >}}
{{< /tabs >}}

要查看 Job 对应的已完成的 Pod，可以执行 `kubectl get pods`。

要以机器可读的方式列举隶属于某 Job 的全部 Pod，你可以使用类似下面这条命令：

```shell
pods=$(kubectl get pods --selector=batch.kubernetes.io/job-name=pi --output=jsonpath='{.items[*].metadata.name}')
echo $pods
```

输出类似于：

```
pi-5rwd7
```

这里，选择算符与 Job 的选择算符相同。`--output=jsonpath` 选项给出了一个表达式，
用来从返回的列表中提取每个 Pod 的 name 字段。

查看其中一个 Pod 的标准输出：

```shell
kubectl logs $pods
```

另外一种查看 Job 日志的方法：

```shell
kubectl logs jobs/pi
```

输出类似于：

```
3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989380952572010654858632788659361533818279682303019520353018529689957736225994138912497217752834791315155748572424541506959508295331168617278558890750983817546374649393192550604009277016711390098488240128583616035637076601047101819429555961989467678374494482553797747268471040475346462080466842590694912933136770289891521047521620569660240580381501935112533824300355876402474964732639141992726042699227967823547816360093417216412199245863150302861829745557067498385054945885869269956909272107975093029553211653449872027559602364806654991198818347977535663698074265425278625518184175746728909777727938000816470600161452491921732172147723501414419735685481613611573525521334757418494684385233239073941433345477624168625189835694855620992192221842725502542568876717904946016534668049886272327917860857843838279679766814541009538837863609506800642251252051173929848960841284886269456042419652850222106611863067442786220391949450471237137869609563643719172874677646575739624138908658326459958133904780275901
```

## 编写 Job 规约    {#writing-a-job-spec}

与 Kubernetes 中其他资源的配置类似，Job 也需要 `apiVersion`、`kind` 和 `metadata` 字段。

当控制面为 Job 创建新的 Pod 时，Job 的 `.metadata.name` 是命名这些 Pod 的基础组成部分。
Job 的名字必须是合法的 [DNS 子域名](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)值，
但这可能对 Pod 主机名产生意料之外的结果。为了获得最佳兼容性，此名字应遵循更严格的
[DNS 标签](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-label-names)规则。
即使该名字被要求遵循 DNS 子域名规则，也不得超过 63 个字符。

Job 配置还需要一个 [`.spec` 节](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)。

### Job 标签

Job 标签将为 `job-name` 和 `controller-uid` 加上 `batch.kubernetes.io/` 前缀。
### Pod 模板    {#pod-template}

Job 的 `.spec` 中只有 `.spec.template` 是必需的字段。

字段 `.spec.template` 的值是一个 [Pod 模板](/zh-cn/docs/concepts/workloads/pods/#pod-templates)。
其定义规范与 {{< glossary_tooltip text="Pod" term_id="pod" >}}
完全相同，只是其中不再需要 `apiVersion` 或 `kind` 字段。

除了作为 Pod 所必需的字段之外，Job 中的 Pod 模板必须设置合适的标签
（参见 [Pod 选择算符](#pod-selector)）和合适的重启策略。

Job 中 Pod 的 [`RestartPolicy`](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy)
只能设置为 `Never` 或 `OnFailure` 之一。

### Pod 选择算符   {#pod-selector}

字段 `.spec.selector` 是可选的。在绝大多数场合，你都不需要为其赋值。
参阅[设置自己的 Pod 选择算符](#specifying-your-own-pod-selector).

### Job 的并行执行 {#parallel-jobs}

适合以 Job 形式来运行的任务主要有三种：

1. 非并行 Job：
   - 通常只启动一个 Pod，除非该 Pod 失败。
   - 当 Pod 成功终止时，立即视 Job 为完成状态。
1. 具有**确定完成计数**的并行 Job：
   - `.spec.completions` 字段设置为非 0 的正数值。
   - Job 用来代表整个任务，当成功的 Pod 个数达到 `.spec.completions` 时，Job 被视为完成。
   - 当使用 `.spec.completionMode="Indexed"` 时，每个 Pod 都会获得一个不同的
     索引值，介于 0 和 `.spec.completions-1` 之间。
1. 带**工作队列**的并行 Job：
   - 不设置 `spec.completions`，默认值为 `.spec.parallelism`。
   - 多个 Pod 之间必须相互协调，或者借助外部服务确定每个 Pod 要处理哪个工作条目。
     例如，任一 Pod 都可以从工作队列中取走最多 N 个工作条目。
   - 每个 Pod 都可以独立确定是否其它 Pod 都已完成，进而确定 Job 是否完成。
   - 当 Job 中**任何** Pod 成功终止，不再创建新 Pod。
   - 一旦至少 1 个 Pod 成功完成，并且所有 Pod 都已终止，即可宣告 Job 成功完成。
   - 一旦任何 Pod 成功退出，任何其它 Pod 都不应再对此任务执行任何操作或生成任何输出。
     所有 Pod 都应启动退出过程。

对于**非并行**的 Job，你可以不设置 `spec.completions` 和 `spec.parallelism`。
这两个属性都不设置时，均取默认值 1。

对于**确定完成计数**类型的 Job，你应该设置 `.spec.completions` 为所需要的完成个数。
你可以设置 `.spec.parallelism`，也可以不设置。其默认值为 1。

对于一个**工作队列** Job，你不可以设置 `.spec.completions`，但要将`.spec.parallelism`
设置为一个非负整数。

关于如何利用不同类型的 Job 的更多信息，请参见 [Job 模式](#job-patterns)一节。

#### 控制并行性   {#controlling-parallelism}

并行性请求（`.spec.parallelism`）可以设置为任何非负整数。
如果未设置，则默认为 1。
如果设置为 0，则 Job 相当于启动之后便被暂停，直到此值被增加。

实际并行性（在任意时刻运行状态的 Pod 个数）可能比并行性请求略大或略小，
原因如下：

- 对于**确定完成计数** Job，实际上并行执行的 Pod 个数不会超出剩余的完成数。
  如果 `.spec.parallelism` 值较高，会被忽略。
- 对于**工作队列** Job，有任何 Job 成功结束之后，不会有新的 Pod 启动。
  不过，剩下的 Pod 允许执行完毕。
- 如果 Job {{< glossary_tooltip text="控制器" term_id="controller" >}} 没有来得及作出响应，或者
- 如果 Job 控制器因为任何原因（例如，缺少 `ResourceQuota` 或者没有权限）无法创建 Pod。
  Pod 个数可能比请求的数目小。
- Job 控制器可能会因为之前同一 Job 中 Pod 失效次数过多而压制新 Pod 的创建。
- 当 Pod 处于体面终止进程中，需要一定时间才能停止。

### 完成模式   {#completion-mode}

{{< feature-state for_k8s_version="v1.24" state="stable" >}}

带有**确定完成计数**的 Job，即 `.spec.completions` 不为 null 的 Job，
都可以在其 `.spec.completionMode` 中设置完成模式：

- `NonIndexed`（默认值）：当成功完成的 Pod 个数达到 `.spec.completions` 所
  设值时认为 Job 已经完成。换言之，每个 Job 完成事件都是独立无关且同质的。
  要注意的是，当 `.spec.completions` 取值为 null 时，Job 被隐式处理为 `NonIndexed`。
- `Indexed`：Job 的 Pod 会获得对应的完成索引，取值为 0 到 `.spec.completions-1`。
  该索引可以通过三种方式获取：
  - Pod 注解 `batch.kubernetes.io/job-completion-index`。
  - 作为 Pod 主机名的一部分，遵循模式 `$(job-name)-$(index)`。
    当你同时使用带索引的 Job（Indexed Job）与 {{< glossary_tooltip term_id="Service" >}}，
    Job 中的 Pod 可以通过 DNS 使用确切的主机名互相寻址。
    有关如何配置的更多信息，请参阅[带 Pod 间通信的 Job](/zh-cn/docs/tasks/job/job-with-pod-to-pod-communication/)。
  - 对于容器化的任务，在环境变量 `JOB_COMPLETION_INDEX` 中。

  当每个索引都对应一个成功完成的 Pod 时，Job 被认为是已完成的。
  关于如何使用这种模式的更多信息，可参阅
  [用带索引的 Job 执行基于静态任务分配的并行处理](/zh-cn/docs/tasks/job/indexed-parallel-processing-static/)。

{{< note >}}
带同一索引值启动的 Pod 可能不止一个（由于节点故障、kubelet
重启或 Pod 驱逐等各种原因），尽管这种情况很少发生。
在这种情况下，只有第一个成功完成的 Pod 才会被记入完成计数中并更新作业的状态。
其他为同一索引值运行或完成的 Pod 一旦被检测到，将被 Job 控制器删除。
{{< /note >}}

## 处理 Pod 和容器失效    {#handling-pod-and-container-failures}

Pod 中的容器可能因为多种不同原因失效，例如因为其中的进程退出时返回值非零，
或者容器因为超出内存约束而被杀死等等。
如果发生这类事件，并且 `.spec.template.spec.restartPolicy = "OnFailure"`，
Pod 则继续留在当前节点，但容器会被重新运行。
因此，你的程序需要能够处理在本地被重启的情况，或者要设置
`.spec.template.spec.restartPolicy = "Never"`。
关于 `restartPolicy` 的更多信息，可参阅
[Pod 生命周期](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#example-states)。

整个 Pod 也可能会失败，且原因各不相同。
例如，当 Pod 启动时，节点失效（被升级、被重启、被删除等）或者其中的容器失败而
`.spec.template.spec.restartPolicy = "Never"`。
当 Pod 失败时，Job 控制器会启动一个新的 Pod。
这意味着，你的应用需要处理在一个新 Pod 中被重启的情况。
尤其是应用需要处理之前运行所产生的临时文件、锁、不完整的输出等问题。

默认情况下，每个 Pod 失效都被计入 `.spec.backoffLimit` 限制，
请参阅 [Pod 回退失效策略](#pod-backoff-failure-policy)。
但你可以通过设置 Job 的 [Pod 失效策略](#pod-failure-policy)自定义对 Pod 失效的处理方式。

注意，即使你将 `.spec.parallelism` 设置为 1，且将 `.spec.completions` 设置为
1，并且 `.spec.template.spec.restartPolicy` 设置为 "Never"，同一程序仍然有可能被启动两次。

如果你确实将 `.spec.parallelism` 和 `.spec.completions` 都设置为比 1 大的值，
那就有可能同时出现多个 Pod 运行的情况。
为此，你的 Pod 也必须能够处理并发性问题。

当[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
`PodDisruptionConditions` 和 `JobPodFailurePolicy` 都被启用且 `.spec.podFailurePolicy` 字段被设置时，
Job 控制器不会将终止过程中的 Pod（已设置 `.metadata.deletionTimestamp` 字段的 Pod）视为失效 Pod，
直到该 Pod 完全终止（其 `.status.phase` 为 `Failed` 或 `Succeeded`）。
但只要终止变得显而易见，Job 控制器就会创建一个替代的 Pod。一旦 Pod 终止，Job 控制器将把这个刚终止的
Pod 考虑在内，评估相关 Job 的 `.backoffLimit` 和 `.podFailurePolicy`。

如果不满足任一要求，即使 Pod 稍后以 `phase: "Succeeded"` 终止，Job 控制器也会将此即将终止的 Pod 计为立即失效。

### Pod 回退失效策略    {#pod-backoff-failure-policy}

在有些情形下，你可能希望 Job 在经历若干次重试之后直接进入失败状态，
因为这很可能意味着遇到了配置错误。
为了实现这点，可以将 `.spec.backoffLimit` 设置为视 Job 为失败之前的重试次数。
失效回退的限制值默认为 6。
与 Job 相关的失效的 Pod 会被 Job 控制器重建，回退重试时间将会按指数增长
（从 10 秒、20 秒到 40 秒）最多至 6 分钟。

计算重试次数有以下两种方法：
- 计算 `.status.phase = "Failed"` 的 Pod 数量。
- 当 Pod 的 `restartPolicy = "OnFailure"` 时，针对 `.status.phase` 等于 `Pending` 或
  `Running` 的 Pod，计算其中所有容器的重试次数。

如果两种方式其中一个的值达到 `.spec.backoffLimit`，则 Job 被判定为失败。

{{< note >}}
如果你的 Job 的 `restartPolicy` 被设置为 "OnFailure"，就要注意运行该 Job 的 Pod
会在 Job 到达失效回退次数上限时自动被终止。
这会使得调试 Job 中可执行文件的工作变得非常棘手。
我们建议在调试 Job 时将 `restartPolicy` 设置为 "Never"，
或者使用日志系统来确保失效 Job 的输出不会意外遗失。
{{< /note >}}

### Pod 失效策略 {#pod-failure-policy}

{{< feature-state for_k8s_version="v1.26" state="beta" >}}

{{< note >}}
只有你在集群中启用了
`JobPodFailurePolicy` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)，
你才能为某个 Job 配置 Pod 失效策略。
此外，建议启用 `PodDisruptionConditions` 特性门控以便在 Pod 失效策略中检测和处理 Pod 干扰状况
（参考：[Pod 干扰状况](/zh-cn/docs/concepts/workloads/pods/disruptions#pod-disruption-conditions)）。
这两个特性门控都是在 Kubernetes {{< skew currentVersion >}} 中提供的。
{{< /note >}}

Pod 失效策略使用 `.spec.podFailurePolicy` 字段来定义，
它能让你的集群根据容器的退出码和 Pod 状况来处理 Pod 失效事件。

在某些情况下，你可能希望更好地控制 Pod 失效的处理方式，
而不是仅限于 [Pod 回退失效策略](#pod-backoff-failure-policy)所提供的控制能力，
后者是基于 Job 的 `.spec.backoffLimit` 实现的。以下是一些使用场景：
* 通过避免不必要的 Pod 重启来优化工作负载的运行成本，
  你可以在某 Job 中一个 Pod 失效且其退出码表明存在软件错误时立即终止该 Job。
* 为了保证即使有干扰也能完成 Job，你可以忽略由干扰导致的 Pod 失效
  （例如{{< glossary_tooltip text="抢占" term_id="preemption" >}}、
  {{< glossary_tooltip text="通过 API 发起的驱逐" term_id="api-eviction" >}}
  或基于{{< glossary_tooltip text="污点" term_id="taint" >}}的驱逐），
  这样这些失效就不会被计入 `.spec.backoffLimit` 的重试限制中。

你可以在 `.spec.podFailurePolicy` 字段中配置 Pod 失效策略，以满足上述使用场景。
该策略可以根据容器退出码和 Pod 状况来处理 Pod 失效。

下面是一个定义了 `podFailurePolicy` 的 Job 的清单：

{{< codenew file="/controllers/job-pod-failure-policy-example.yaml" >}}

在上面的示例中，Pod 失效策略的第一条规则规定如果 `main` 容器失败并且退出码为 42，
Job 将被标记为失败。以下是 `main` 容器的具体规则：

- 退出码 0 代表容器成功
- 退出码 42 代表**整个 Job** 失败
- 所有其他退出码都代表容器失败，同时也代表着整个 Pod 失效。
  如果重启总次数低于 `backoffLimit` 定义的次数，则会重新启动 Pod，
  如果等于 `backoffLimit` 所设置的次数，则代表**整个 Job** 失效。

{{< note >}}
因为 Pod 模板中指定了 `restartPolicy: Never`，
所以 kubelet 将不会重启 Pod 中的 `main` 容器。
{{< /note >}}

Pod 失效策略的第二条规则，
指定对于状况为 `DisruptionTarget` 的失效 Pod 采取 `Ignore` 操作，
统计 `.spec.backoffLimit` 重试次数限制时不考虑 Pod 因干扰而发生的异常。

{{< note >}}
如果根据 Pod 失效策略或 Pod 回退失效策略判定 Pod 已经失效，
并且 Job 正在运行多个 Pod，Kubernetes 将终止该 Job 中仍处于 Pending 或 Running 的所有 Pod。
{{< /note >}}

下面是此 API 的一些要求和语义：
- 如果你想在 Job 中使用 `.spec.podFailurePolicy` 字段，
  你必须将 Job 的 Pod 模板中的 `.spec.restartPolicy` 设置为 `Never`。
- 在 `spec.podFailurePolicy.rules` 中设定的 Pod 失效策略规则将按序评估。
  一旦某个规则与 Pod 失效策略匹配，其余规则将被忽略。
  当没有规则匹配 Pod 失效策略时，将会采用默认的处理方式。
- 你可能希望在 `spec.podFailurePolicy.rules[*].containerName`
  中通过指定的名称将规则限制到特定容器。
  如果不设置，规则将适用于所有容器。
  如果指定了容器名称，它应该匹配 Pod 模板中的一个普通容器或一个初始容器（Init Container）。
- 你可以在 `spec.podFailurePolicy.rules[*].action` 指定当 Pod 失效策略发生匹配时要采取的操作。
  可能的值为：
  - `FailJob`：表示 Pod 的任务应标记为 Failed，并且所有正在运行的 Pod 应被终止。
  - `Ignore`：表示 `.spec.backoffLimit` 的计数器不应该增加，应该创建一个替换的 Pod。
  - `Count`：表示 Pod 应该以默认方式处理。`.spec.backoffLimit` 的计数器应该增加。

{{< note >}}
当你使用 `podFailurePolicy` 时，Job 控制器只匹配处于 `Failed` 阶段的 Pod。
具有删除时间戳但不处于终止阶段（`Failed` 或 `Succeeded`）的 Pod 被视为仍在终止中。
这意味着终止中的 Pod 会保留一个[跟踪 Finalizer](#job-tracking-with-finalizers)，
直到到达终止阶段。
从 Kubernetes 1.27 开始，kubelet 将删除的 Pod 转换到终止阶段
（参阅 [Pod 阶段](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase)）。
这确保已删除的 Pod 的 Finalizer 被 Job 控制器移除。
{{< /note >}}

## Job 终止与清理    {#job-termination-and-cleanup}

Job 完成时不会再创建新的 Pod，不过已有的 Pod [通常](#pod-backoff-failure-policy)也不会被删除。
保留这些 Pod 使得你可以查看已完成的 Pod 的日志输出，以便检查错误、警告或者其它诊断性输出。
Job 完成时 Job 对象也一样被保留下来，这样你就可以查看它的状态。
在查看了 Job 状态之后删除老的 Job 的操作留给了用户自己。
你可以使用 `kubectl` 来删除 Job（例如，`kubectl delete jobs/pi`
或者 `kubectl delete -f ./job.yaml`）。
当使用 `kubectl` 来删除 Job 时，该 Job 所创建的 Pod 也会被删除。

默认情况下，Job 会持续运行，除非某个 Pod 失败（`restartPolicy=Never`）
或者某个容器出错退出（`restartPolicy=OnFailure`）。
这时，Job 基于前述的 `spec.backoffLimit` 来决定是否以及如何重试。
一旦重试次数到达 `.spec.backoffLimit` 所设的上限，Job 会被标记为失败，
其中运行的 Pod 都会被终止。

终止 Job 的另一种方式是设置一个活跃期限。
你可以为 Job 的 `.spec.activeDeadlineSeconds` 设置一个秒数值。
该值适用于 Job 的整个生命期，无论 Job 创建了多少个 Pod。
一旦 Job 运行时间达到 `activeDeadlineSeconds` 秒，其所有运行中的 Pod 都会被终止，
并且 Job 的状态更新为 `type: Failed` 及 `reason: DeadlineExceeded`。

注意 Job 的 `.spec.activeDeadlineSeconds` 优先级高于其 `.spec.backoffLimit` 设置。
因此，如果一个 Job 正在重试一个或多个失效的 Pod，该 Job 一旦到达
`activeDeadlineSeconds` 所设的时限即不再部署额外的 Pod，
即使其重试次数还未达到 `backoffLimit` 所设的限制。

例如：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi-with-timeout
spec:
  backoffLimit: 5
  activeDeadlineSeconds: 100
  template:
    spec:
      containers:
      - name: pi
        image: perl:5.34.0
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
```
注意 Job 规约和 Job 中的
[Pod 模板规约](/zh-cn/docs/concepts/workloads/pods/init-containers/#detailed-behavior)
都有 `activeDeadlineSeconds` 字段。
请确保你在合适的层次设置正确的字段。

还要注意的是，`restartPolicy` 对应的是 Pod，而不是 Job 本身：
一旦 Job 状态变为 `type: Failed`，就不会再发生 Job 重启的动作。
换言之，由 `.spec.activeDeadlineSeconds` 和 `.spec.backoffLimit` 所触发的 Job
终结机制都会导致 Job 永久性的失败，而这类状态都需要手工干预才能解决。

## 自动清理完成的 Job   {#clean-up-finished-jobs-automatically}

完成的 Job 通常不需要留存在系统中。在系统中一直保留它们会给 API 服务器带来额外的压力。
如果 Job 由某种更高级别的控制器来管理，例如
[CronJob](/zh-cn/docs/concepts/workloads/controllers/cron-jobs/)，
则 Job 可以被 CronJob 基于特定的根据容量裁定的清理策略清理掉。

### 已完成 Job 的 TTL 机制  {#ttl-mechanisms-for-finished-jobs}

{{< feature-state for_k8s_version="v1.23" state="stable" >}}

自动清理已完成 Job （状态为 `Complete` 或 `Failed`）的另一种方式是使用由
[TTL 控制器](/zh-cn/docs/concepts/workloads/controllers/ttlafterfinished/)所提供的 TTL 机制。
通过设置 Job 的 `.spec.ttlSecondsAfterFinished` 字段，可以让该控制器清理掉已结束的资源。

TTL 控制器清理 Job 时，会级联式地删除 Job 对象。
换言之，它会删除所有依赖的对象，包括 Pod 及 Job 本身。
注意，当 Job 被删除时，系统会考虑其生命周期保障，例如其 Finalizers。

例如：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi-with-ttl
spec:
  ttlSecondsAfterFinished: 100
  template:
    spec:
      containers:
      - name: pi
        image: perl:5.34.0
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
```

Job `pi-with-ttl` 在结束 100 秒之后，可以成为被自动删除的对象。

如果该字段设置为 `0`，Job 在结束之后立即成为可被自动删除的对象。
如果该字段没有设置，Job 不会在结束之后被 TTL 控制器自动清除。

{{< note >}}
建议设置 `ttlSecondsAfterFinished` 字段，因为非托管任务
（是你直接创建的 Job，而不是通过其他工作负载 API（如 CronJob）间接创建的 Job）
的默认删除策略是 `orphanDependents`，这会导致非托管 Job 创建的 Pod 在该 Job 被完全删除后被保留。
即使{{< glossary_tooltip text="控制面" term_id="control-plane" >}}最终在 Pod 失效或完成后
对已删除 Job 中的这些 Pod 执行[垃圾收集](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#pod-garbage-collection)操作，
这些残留的 Pod 有时可能会导致集群性能下降，或者在最坏的情况下会导致集群因这种性能下降而离线。

你可以使用 [LimitRange](/zh-cn/docs/concepts/policy/limit-range/) 和
[ResourceQuota](/zh-cn/docs/concepts/policy/resource-quotas/)，
设定一个特定名字空间可以消耗的资源上限。
{{< /note >}}

## Job 模式  {#job-patterns}

Job 对象可以用来支持多个 Pod 的可靠的并发执行。
Job 对象不是设计用来支持相互通信的并行进程的，后者一般在科学计算中应用较多。
Job 的确能够支持对一组相互独立而又有所关联的**工作条目**的并行处理。
这类工作条目可能是要发送的电子邮件、要渲染的视频帧、要编解码的文件、NoSQL
数据库中要扫描的主键范围等等。

在一个复杂系统中，可能存在多个不同的工作条目集合。
这里我们仅考虑用户希望一起管理的工作条目集合之一：**批处理作业**。

并行计算的模式有好多种，每种都有自己的强项和弱点。这里要权衡的因素有：

- 每个工作条目对应一个 Job 或者所有工作条目对应同一 Job 对象。
  后者更适合处理大量工作条目的场景；
  前者会给用户带来一些额外的负担，而且需要系统管理大量的 Job 对象。
- 创建与工作条目相等的 Pod 或者令每个 Pod 可以处理多个工作条目。
  前者通常不需要对现有代码和容器做较大改动；
  后者则更适合工作条目数量较大的场合，原因同上。
- 有几种技术都会用到工作队列。这意味着需要运行一个队列服务，
  并修改现有程序或容器使之能够利用该工作队列。
  与之比较，其他方案在修改现有容器化应用以适应需求方面可能更容易一些。

下面是对这些权衡的汇总，第 2 到 4 列对应上面的权衡比较。
模式的名称对应了相关示例和更详细描述的链接。

| 模式  | 单个 Job 对象 | Pod 数少于工作条目数？ | 直接使用应用无需修改? |
| ----- |:-------------:|:-----------------------:|:---------------------:|
| [每工作条目一 Pod 的队列](/zh-cn/docs/tasks/job/coarse-parallel-processing-work-queue/) | ✓ | | 有时 |
| [Pod 数量可变的队列](/zh-cn/docs/tasks/job/fine-parallel-processing-work-queue/) | ✓ | ✓ |  |
| [静态任务分派的带索引的 Job](/zh-cn/docs/tasks/job/indexed-parallel-processing-static) | ✓ |  | ✓ |
| [Job 模板扩展](/zh-cn/docs/tasks/job/parallel-processing-expansion/)  |  |  | ✓ |
| [带 Pod 间通信的 Job](/zh-cn/docs/tasks/job/job-with-pod-to-pod-communication/)  | ✓ | 有时 | 有时 |

当你使用 `.spec.completions` 来设置完成数时，Job 控制器所创建的每个 Pod
使用完全相同的 [`spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)。
这意味着任务的所有 Pod 都有相同的命令行，都使用相同的镜像和数据卷，
甚至连环境变量都（几乎）相同。
这些模式是让每个 Pod 执行不同工作的几种不同形式。

下表显示的是每种模式下 `.spec.parallelism` 和 `.spec.completions` 所需要的设置。
其中，`W` 表示的是工作条目的个数。

| 模式  | `.spec.completions` |  `.spec.parallelism` |
| ----- |:-------------------:|:--------------------:|
| [每工作条目一 Pod 的队列](/zh-cn/docs/tasks/job/coarse-parallel-processing-work-queue/) | W | 任意值 |
| [Pod 个数可变的队列](/zh-cn/docs/tasks/job/fine-parallel-processing-work-queue/) | 1 | 任意值 |
| [静态任务分派的带索引的 Job](/zh-cn/docs/tasks/job/indexed-parallel-processing-static) | W |  | 任意值 |
| [Job 模板扩展](/zh-cn/docs/tasks/job/parallel-processing-expansion/) | 1 | 应该为 1 |
| [带 Pod 间通信的 Job](/zh-cn/docs/tasks/job/job-with-pod-to-pod-communication/) | W | W |

## 高级用法   {#advanced-usage}

### 挂起 Job   {#suspending-a-job}

{{< feature-state for_k8s_version="v1.24" state="stable" >}}

Job 被创建时，Job 控制器会马上开始执行 Pod 创建操作以满足 Job 的需求，
并持续执行此操作直到 Job 完成为止。
不过你可能想要暂时挂起 Job 执行，或启动处于挂起状态的 Job，
并拥有一个自定义控制器以后再决定什么时候开始。

要挂起一个 Job，你可以更新 `.spec.suspend` 字段为 true，
之后，当你希望恢复其执行时，将其更新为 false。
创建一个 `.spec.suspend` 被设置为 true 的 Job 本质上会将其创建为被挂起状态。

当 Job 被从挂起状态恢复执行时，其 `.status.startTime` 字段会被重置为当前的时间。
这意味着 `.spec.activeDeadlineSeconds` 计时器会在 Job 挂起时被停止，
并在 Job 恢复执行时复位。

当你挂起一个 Job 时，所有正在运行且状态不是 `Completed` 的 Pod
将被[终止](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)。
Pod 的体面终止期限会被考虑，不过 Pod 自身也必须在此期限之内处理完信号。
处理逻辑可能包括保存进度以便将来恢复，或者取消已经做出的变更等等。
Pod 以这种形式终止时，不会被记入 Job 的 `completions` 计数。

处于被挂起状态的 Job 的定义示例可能是这样子：

```shell
kubectl get job myjob -o yaml
```

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: myjob
spec:
  suspend: true
  parallelism: 1
  completions: 5
  template:
    spec:
      ...
```

你也可以使用命令行为 Job 打补丁来切换 Job 的挂起状态。

挂起一个活跃的 Job：

```shell
kubectl patch job/myjob --type=strategic --patch '{"spec":{"suspend":true}}'
```

恢复一个挂起的 Job：

```shell
kubectl patch job/myjob --type=strategic --patch '{"spec":{"suspend":false}}'
```

Job 的 `status` 可以用来确定 Job 是否被挂起，或者曾经被挂起。

```shell
kubectl get jobs/myjob -o yaml
```

```yaml
apiVersion: batch/v1
kind: Job
# .metadata 和 .spec 已省略
status:
  conditions:
  - lastProbeTime: "2021-02-05T13:14:33Z"
    lastTransitionTime: "2021-02-05T13:14:33Z"
    status: "True"
    type: Suspended
  startTime: "2021-02-05T13:13:48Z"
```

Job 的 "Suspended" 类型的状况在状态值为 "True" 时意味着 Job 正被挂起；
`lastTransitionTime` 字段可被用来确定 Job 被挂起的时长。
如果此状况字段的取值为 "False"，则 Job 之前被挂起且现在在运行。
如果 "Suspended" 状况在 `status` 字段中不存在，则意味着 Job 从未被停止执行。

当 Job 被挂起和恢复执行时，也会生成事件：

```shell
kubectl describe jobs/myjob
```

```
Name:           myjob
...
Events:
  Type    Reason            Age   From            Message
  ----    ------            ----  ----            -------
  Normal  SuccessfulCreate  12m   job-controller  Created pod: myjob-hlrpl
  Normal  SuccessfulDelete  11m   job-controller  Deleted pod: myjob-hlrpl
  Normal  Suspended         11m   job-controller  Job suspended
  Normal  SuccessfulCreate  3s    job-controller  Created pod: myjob-jvb44
  Normal  Resumed           3s    job-controller  Job resumed
```

最后四个事件，特别是 "Suspended" 和 "Resumed" 事件，都是因为 `.spec.suspend`
字段值被改来改去造成的。在这两个事件之间，我们看到没有 Pod 被创建，不过当
Job 被恢复执行时，Pod 创建操作立即被重启执行。

### 可变调度指令 {#mutable-scheduling-directives}

{{< feature-state for_k8s_version="v1.27" state="stable" >}}

{{< note >}}
为了使用此功能，你必须在 [API 服务器](/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver/)上启用
`JobMutableNodeSchedulingDirectives` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)。
默认情况下启用。
{{< /note >}}

在大多数情况下，并行作业会希望 Pod 在一定约束条件下运行，
比如所有的 Pod 都在同一个区域，或者所有的 Pod 都在 GPU 型号 x 或 y 上，而不是两者的混合。

[suspend](#suspending-a-job) 字段是实现这些语义的第一步。
suspend 允许自定义队列控制器，以决定工作何时开始；然而，一旦工作被取消暂停，
自定义队列控制器对 Job 中 Pod 的实际放置位置没有影响。

此特性允许在 Job 开始之前更新调度指令，从而为定制队列提供影响 Pod
放置的能力，同时将 Pod 与节点间的分配关系留给 kube-scheduler 决定。
这一特性仅适用于之前从未被暂停过的、已暂停的 Job。
控制器能够影响 Pod 放置，同时参考实际 pod-to-node 分配给 kube-scheduler。
这仅适用于从未暂停的 Job。

Job 的 Pod 模板中可以更新的字段是节点亲和性、节点选择器、容忍、标签、注解和
[调度门控](/zh-cn/docs/concepts/scheduling-eviction/pod-scheduling-readiness/)。

### 指定你自己的 Pod 选择算符 {#specifying-your-own-pod-selector}

通常，当你创建一个 Job 对象时，你不会设置 `.spec.selector`。
系统的默认值填充逻辑会在创建 Job 时添加此字段。
它会选择一个不会与任何其他 Job 重叠的选择算符设置。

不过，有些场合下，你可能需要重载这个自动设置的选择算符。
为了实现这点，你可以手动设置 Job 的 `spec.selector` 字段。

做这个操作时请务必小心。
如果你所设定的标签选择算符并不唯一针对 Job 对应的 Pod 集合，
甚或该算符还能匹配其他无关的 Pod，这些无关的 Job 的 Pod 可能会被删除。
或者当前 Job 会将另外一些 Pod 当作是完成自身工作的 Pod，
又或者两个 Job 之一或者二者同时都拒绝创建 Pod，无法运行至完成状态。
如果所设置的算符不具有唯一性，其他控制器（如 RC 副本控制器）及其所管理的 Pod
集合可能会变得行为不可预测。
Kubernetes 不会在你设置 `.spec.selector` 时尝试阻止你犯这类错误。

下面是一个示例场景，在这种场景下你可能会使用刚刚讲述的特性。

假定名为 `old` 的 Job 已经处于运行状态。
你希望已有的 Pod 继续运行，但你希望 Job 接下来要创建的其他 Pod
使用一个不同的 Pod 模板，甚至希望 Job 的名字也发生变化。
你无法更新现有的 Job，因为这些字段都是不可更新的。
因此，你会删除 `old` Job，但**允许该 Job 的 Pod 集合继续运行**。
这是通过 `kubectl delete jobs/old --cascade=orphan` 实现的。
在删除之前，我们先记下该 Job 所使用的选择算符。

```shell
kubectl get job old -o yaml
```

输出类似于：

```yaml
kind: Job
metadata:
  name: old
  ...
spec:
  selector:
    matchLabels:
      batch.kubernetes.io/controller-uid: a8f3d00d-c6d2-11e5-9f87-42010af00002
  ...
```

接下来你会创建名为 `new` 的新 Job，并显式地为其设置相同的选择算符。
由于现有 Pod 都具有标签
`batch.kubernetes.io/controller-uid=a8f3d00d-c6d2-11e5-9f87-42010af00002`，
它们也会被名为 `new` 的 Job 所控制。

你需要在新 Job 中设置 `manualSelector: true`，
因为你并未使用系统通常自动为你生成的选择算符。

```yaml
kind: Job
metadata:
  name: new
  ...
spec:
  manualSelector: true
  selector:
    matchLabels:
      batch.kubernetes.io/controller-uid: a8f3d00d-c6d2-11e5-9f87-42010af00002
  ...
```

新的 Job 自身会有一个不同于 `a8f3d00d-c6d2-11e5-9f87-42010af00002` 的唯一 ID。
设置 `manualSelector: true`
是在告诉系统你知道自己在干什么并要求系统允许这种不匹配的存在。

### 使用 Finalizer 追踪 Job   {#job-tracking-with-finalizers}

{{< feature-state for_k8s_version="v1.26" state="stable" >}}

{{< note >}}
如果 Job 是在特性门控 `JobTrackingWithFinalizers` 被禁用时创建的，即使你将控制面升级到 1.26，
控制面也不会使用 Finalizer 跟踪 Job。
{{< /note >}}

控制面会跟踪属于任何 Job 的 Pod，并通知是否有任何这样的 Pod 被从 API 服务器中移除。
为了实现这一点，Job 控制器创建的 Pod 带有 Finalizer `batch.kubernetes.io/job-tracking`。
控制器只有在 Pod 被记入 Job 状态后才会移除 Finalizer，允许 Pod 可以被其他控制器或用户移除。

在升级到 Kubernetes 1.26 之前或在启用特性门控 `JobTrackingWithFinalizers`
之前创建的 Job 被跟踪时不使用 Pod Finalizer。
Job {{< glossary_tooltip term_id="controller" text="控制器" >}}仅根据集群中存在的 Pod
更新 `succeeded` 和 `failed` Pod 的状态计数器。如果 Pod 被从集群中删除，控制面可能无法跟踪 Job 的进度。

你可以根据检查 Job 是否含有 `batch.kubernetes.io/job-tracking` 注解，
来确定控制面是否正在使用 Pod Finalizer 追踪 Job。
你**不**应该给 Job 手动添加或删除该注解。
取而代之的是你可以重新创建 Job 以确保使用 Pod Finalizer 跟踪这些 Job。

### 弹性索引 Job  {#elastic-indexed-job}

{{< feature-state for_k8s_version="v1.27" state="beta" >}}

你可以通过同时改变 `.spec.parallelism` 和 `.spec.completions` 来扩大或缩小带索引 Job，
从而满足 `.spec.parallelism == .spec.completions`。
当 [API 服务器](/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver/)
上的 `ElasticIndexedJob` 特性门控被禁用时，`.spec.completions` 是不可变的。
弹性索引 Job 的使用场景包括需要扩展索引 Job 的批处理工作负载，例如 MPI、Horovord、Ray
和 PyTorch 训练作业。

## 替代方案  {#alternatives}

### 裸 Pod  {#bare-pods}

当 Pod 运行所在的节点重启或者失败，Pod 会被终止并且不会被重启。
Job 会重新创建新的 Pod 来替代已终止的 Pod。
因为这个原因，我们建议你使用 Job 而不是独立的裸 Pod，
即使你的应用仅需要一个 Pod。

### 副本控制器    {#replication-controller}

Job 与[副本控制器](/zh-cn/docs/concepts/workloads/controllers/replicationcontroller/)是彼此互补的。
副本控制器管理的是那些不希望被终止的 Pod （例如，Web 服务器），
Job 管理的是那些希望被终止的 Pod（例如，批处理作业）。

正如在 [Pod 生命期](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/) 中讨论的，
`Job` 仅适合于 `restartPolicy` 设置为 `OnFailure` 或 `Never` 的 Pod。
注意：如果 `restartPolicy` 未设置，其默认值是 `Always`。

### 单个 Job 启动控制器 Pod    {#single-job-starts-controller-pod}

另一种模式是用唯一的 Job 来创建 Pod，而该 Pod 负责启动其他 Pod，
因此扮演了一种后启动 Pod 的控制器的角色。
这种模式的灵活性更高，但是有时候可能会把事情搞得很复杂，很难入门，
并且与 Kubernetes 的集成度很低。

这种模式的实例之一是用 Job 来启动一个运行脚本的 Pod，脚本负责启动 Spark
主控制器（参见 [Spark 示例](https://github.com/kubernetes/examples/tree/master/staging/spark/README.md)），
运行 Spark 驱动，之后完成清理工作。

这种方法的优点之一是整个过程得到了 Job 对象的完成保障，
同时维持了对创建哪些 Pod、如何向其分派工作的完全控制能力，

## {{% heading "whatsnext" %}}

* 了解 [Pod](/zh-cn/docs/concepts/workloads/pods)。
* 了解运行 Job 的不同的方式：
  * [使用工作队列进行粗粒度并行处理](/zh-cn/docs/tasks/job/coarse-parallel-processing-work-queue/)
  * [使用工作队列进行精细的并行处理](/zh-cn/docs/tasks/job/fine-parallel-processing-work-queue/)
  * [使用索引作业完成静态工作分配下的并行处理](/zh-cn/docs/tasks/job/indexed-parallel-processing-static/)
  * 基于一个模板运行多个 Job：[使用展开的方式进行并行处理](/zh-cn/docs/tasks/job/parallel-processing-expansion/)
* 跟随[自动清理完成的 Job](#clean-up-finished-jobs-automatically) 文中的链接，了解你的集群如何清理完成和失败的任务。
* `Job` 是 Kubernetes REST API 的一部分。阅读 {{< api-reference page="workload-resources/job-v1" >}}
  对象定义理解关于该资源的 API。
* 阅读 [`CronJob`](/zh-cn/docs/concepts/workloads/controllers/cron-jobs/)，
  它允许你定义一系列定期运行的 Job，类似于 UNIX 工具 `cron`。
* 根据循序渐进的[示例](/zh-cn/docs/tasks/job/pod-failure-policy/)，
  练习如何使用 `podFailurePolicy` 配置处理可重试和不可重试的 Pod 失效。
