---
api_metadata:
apiVersion: "batch/v1"
import: "k8s.io/api/batch/v1"
kind: "Job"
content_type: "api_reference"
description: "Job 表示单个任务的配置。"
title: "Job"
weight: 9
---

`apiVersion: batch/v1`

`import "k8s.io/api/batch/v1"`

## Job {#Job}

Job 表示单个任务的配置。

<hr>

- **apiVersion**: batch/v1

- **kind**: Job

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../workload-resources/job-v1#JobSpec" >}}">JobSpec</a>)

  任务的预期行为的规约。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

- **status** (<a href="{{< ref "../workload-resources/job-v1#JobStatus" >}}">JobStatus</a>)

  任务的当前状态。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

## JobSpec {#JobSpec}

JobSpec 描述了任务执行的情况。

<hr>

### Replicas

- **template** (<a href="{{< ref "../workload-resources/pod-template-v1#PodTemplateSpec" >}}">PodTemplateSpec</a>), 必需

  描述执行任务时将创建的 Pod。template.spec.restartPolicy 可以取的值只能是
  "Never" 或 "OnFailure"。更多信息：
  https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/

- **parallelism** (int32)

  指定任务应在任何给定时刻预期运行的 Pod 个数上限。
  当(.spec.completions - .status.successful) \< .spec.parallelism 时，
  即当剩余的工作小于最大并行度时，在稳定状态下运行的 Pod 的实际数量将小于此数量。
  更多信息：
  https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/

### Lifecycle

- **completions** (int32)

  指定任务应该运行并预期成功完成的 Pod 个数。设置为空意味着任何 Pod 的成功都标识着所有 Pod 的成功，
  并允许 parallelism 设置为任何正值。设置为 1 意味着并行性被限制为 1，并且该 Pod 的成功标志着任务的成功。更多信息：
  https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/

- **completionMode** (string)

  completionMode 指定如何跟踪 Pod 完成情况。它可以是 `NonIndexed`（默认）或者 `Indexed`。

  `NonIndexed` 表示当有 `.spec.completions` 个成功完成的 Pod 时，认为 Job 完成。每个 Pod 完成都是彼此同源的。


  `Indexed` 意味着 Job 的各个 Pod 会获得对应的完成索引值，从 0 到（`.spec.completions - 1`），可在注解
  "batch.kubernetes.io/job-completion-index" 中找到。当每个索引都对应有一个成功完成的 Pod 时，
  该任务被认为是完成的。
  当值为 `Indexed` 时，必须指定 `.spec.completions` 并且 `.spec.parallelism` 必须小于或等于 10^5。
  此外，Pod 名称采用 `$(job-name)-$(index)-$(random-string)` 的形式，Pod 主机名采用
  `$(job-name)-$(index)` 的形式。


  将来可能添加更多的完成模式。如果 Job 控制器发现它无法识别的模式
  （这种情况在升级期间由于版本偏差可能发生），则控制器会跳过 Job 的更新。

- **backoffLimit** (int32)

  指定标记此任务失败之前的重试次数。默认值为 6。

- **activeDeadlineSeconds** (int64)

  系统尝试终止任务之前任务可以持续活跃的持续时间（秒），时间长度是相对于 startTime 的；
  字段值必须为正整数。如果任务被挂起（在创建期间或因更新而挂起），
  则当任务再次恢复时，此计时器会被停止并重置。

- **ttlSecondsAfterFinished** (int32)

  ttlSecondsAfterFinished 限制已完成执行（完成或失败）的任务的生命周期。如果设置了这个字段，
  在 Job 完成 ttlSecondsAfterFinished 秒之后，就可以被自动删除。
  当 Job 被删除时，它的生命周期保证（例如终结器）会被考察。
  如果未设置此字段，则任务不会被自动删除。如果此字段设置为零，则任务在完成后即可立即删除。

- **suspend** (boolean)

  suspend 指定 Job 控制器是否应该创建 Pod。如果创建 Job 时将 suspend 设置为 true，则 Job 控制器不会创建任何 Pod。
  如果 Job 在创建后被挂起（即标志从 false 变为 true），则 Job 控制器将删除与该 Job 关联的所有活动 Pod。
  用户必须设计他们的工作负载来优雅地处理这个问题。暂停 Job 将重置 Job 的 startTime 字段，
  也会重置 ActiveDeadlineSeconds 计时器。默认为 false。

### Selector

- **selector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)

  对应与 Pod 计数匹配的 Pod 的标签查询。通常，系统会为你设置此字段。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/labels/#label-selectors

- **manualSelector** (boolean)

  manualSelector 控制 Pod 标签和 Pod 选择器的生成。除非你确定你在做什么，否则不要设置 `manualSelector`。
  当此字段为 false 或未设置时，系统会选择此 Pod 唯一的标签并将这些标签附加到 Pod 模板。
  当此字段为 true 时，用户负责选择唯一标签并指定选择器。
  未能选择唯一标签可能会导致此任务和其他任务无法正常运行。但是，你可能会在使用旧的 `extensions/v1beta1` API
  创建的任务中看到 `manualSelector=true`。更多信息：
  https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/#specifying-your-own-pod-selector

### Alpha 级别   {#alpha-level}

- **podFailurePolicy** (PodFailurePolicy)

  指定处理失效 Pod 的策略。特别是，它允许指定采取关联操作需要满足的一组操作和状况。
  如果为空，则应用默认行为：由该任务的 .status.failed 字段表示的失效 Pod 的计数器将递增，
  并针对 backoffLimit 进行检查。此字段不能与 restartPolicy=OnFailure 结合使用。


  此字段是 Alpha 级别。要使用此字段，你必须启用 `JobPodFailurePolicy` 特性门控（默认被禁用）。

  <a name="PodFailurePolicy"></a>
  **PodFailurePolicy 描述失效的 Pod 如何影响 backoffLimit。**


  - **podFailurePolicy.rules** ([]PodFailurePolicyRule)，必需

    **原子: 将在合并期间被替换**
    
    Pod 失效策略规则的列表。这些规则按顺序进行评估。一旦某规则匹配 Pod 失效，则其余规将被忽略。
    当没有规则匹配 Pod 失效时，将应用默认的处理方式：
    Pod 失效的计数器递增并针对 backoffLimit 进行检查。最多允许 20 个。


    <a name="PodFailurePolicyRule"></a>
    **PodFailurePolicyRule 描述当满足要求时如何处理一个 Pod 失效。
    在每个规则中可以使用 onExitCodes 和 onPodConditions 之一，但不能同时使用二者。**


    - **podFailurePolicy.rules.action** (string)，必需

      指定当要求满足时对 Pod 失效采取的操作。可能的值是：

      - FailJob：表示 Pod 的任务被标记为 Failed 且所有正在运行的 Pod 都被终止。


      - Ignore：表示 .backoffLimit 的计数器没有递增，并创建了一个替代 Pod。

      - Count：表示以默认方式处理该 Pod，计数器朝着 .backoffLimit 的方向递增。

      后续会考虑增加其他值。客户端应通过跳过此规则对未知的操作做出反应。


    - **podFailurePolicy.rules.onPodConditions** ([]PodFailurePolicyOnPodConditionsPattern)，必需

      **原子: 将在合并期间被替换**


      表示对 Pod 状况的要求。该要求表示为 Pod 状况模式的一个列表。
      如果至少一个模式与实际的 Pod 状况匹配，则满足此要求。最多允许 20 个。

      <a name="PodFailurePolicyOnPodConditionsPattern"></a>
      **PodFailurePolicyOnPodConditionsPattern 描述与实际 Pod 状况类型匹配的模式。**


      - **podFailurePolicy.rules.onPodConditions.status** (string)，必需

        指定必需的 Pod 状况状态。要匹配一个 Pod 状况，指定的状态必须等于该 Pod 状况状态。默认为 True。

      - **podFailurePolicy.rules.onPodConditions.type** (string)，必需

        指定必需的 Pod 状况类型。要匹配一个 Pod 状况，指定的类型必须等于该 Pod 状况类型。


    - **podFailurePolicy.rules.onExitCodes** (PodFailurePolicyOnExitCodesRequirement)

      表示容器退出码有关的要求。

      <a name="PodFailurePolicyOnExitCodesRequirement"></a>
      **PodFailurePolicyOnExitCodesRequirement 描述根据容器退出码处理失效 Pod 的要求。
      特别是，它为每个应用容器和 Init 容器状态查找在 Pod 状态中分别用 .status.containerStatuses 和
      .status.initContainerStatuses 字段表示的 .state.terminated.exitCode。
      成功完成的容器（退出码 0）被排除在此要求检查之外。**


      - **podFailurePolicy.rules.onExitCodes.operator** (string)，必需

        表示容器退出码和指定值之间的关系。成功完成的容器（退出码 0）被排除在此要求检查之外。可能的值为：
        
        - In：如果至少一个容器退出码（如果有多个容器不受 'containerName' 字段限制，则可能是多个退出码）
          在一组指定值中，则满足要求。

        - NotIn：如果至少一个容器退出码（如果有多个容器不受 'containerName' 字段限制，则可能是多个退出码）
          不在一组指定值中，则满足要求。

        后续会考虑增加其他值。客户端应通过假设不满足要求来对未知操作符做出反应。


      - **podFailurePolicy.rules.onExitCodes.values** ([]int32)，必需

        **集合：合并期间保留唯一值**
        
        指定值集。每个返回的容器退出码（在多个容器的情况下可能是多个）将根据该操作符有关的这个值集进行检查。
        值的列表必须有序且不得包含重复项。值 '0' 不能用于 In 操作符。至少需要 1 个。最多允许 255 个。


      - **podFailurePolicy.rules.onExitCodes.containerName** (string)

        将退出码的检查限制为具有指定名称的容器。当为 null 时，该规则适用于所有容器。
        当被指定时，它应与 Pod 模板中的容器名称或 initContainer 名称之一匹配。

## JobStatus {#JobStatus}

JobStatus 表示 Job 的当前状态。

<hr>

- **startTime** (Time)

  表示任务控制器开始处理任务的时间。在挂起状态下创建 Job 时，直到第一次恢复时才会设置此字段。
  每次从暂停中恢复任务时都会重置此字段。它表示为 RFC3339 格式的 UTC 时间。

  <a name="Time"></a>
  **Time 是 time.Time 的包装器，支持正确编码为 YAML 和 JSON。time 包提供的许多工厂方法都提供了包装器。**

- **completionTime** (Time)

  表示任务完成的时间。不能保证对多个独立操作按发生的先后顺序设置。此字段表示为 RFC3339 格式的 UTC 时间。
  仅当任务成功完成时才设置完成时间。

  <a name="Time"></a>
  **Time 是 time.Time 的包装器，支持正确编码为 YAML 和 JSON。time 包提供的许多工厂方法都提供了包装器。**

- **active** (int32)

  待处理和正在运行的 Pod 的数量。

- **failed** (int32)

  进入 Failed 阶段的 Pod 数量。

- **succeeded** (int32)

  进入 Succeeded 阶段的 Pod 数量。
- **completedIndexes** (string)

  completedIndexes 以文本格式保存 `.spec.completionMode` 设置为 `"Indexed"` 的 Pod 已完成的索引。
  索引用十进制整数表示，用逗号分隔。数字是按递增的顺序排列的。三个或更多的连续数字被压缩，
  用系列的第一个和最后一个元素表示，用连字符分开。例如，如果完成的索引是 1、3、4、5 和 7，则表示为 "1、3-5、7"。

- **conditions** ([]JobCondition)

  **补丁策略：根据 `type` 键合并**

  **原子: 将在合并期间被替换**

  对象当前状态的最新可用观察结果。当任务失败时，其中一个状况的类型为 “Failed”，状态为 true。
  当任务被暂停时，其中一个状况的类型为 “Suspended”，状态为true；当任务被恢复时，该状况的状态将变为 false。
  任务完成时，其中一个状况的类型为 "Complete"，状态为 true。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/jobs-run-to-completion/

  <a name="JobCondition"></a>
  **JobCondition 描述任务的当前状况。**


  - **conditions.status** (string), 必需

    状况的状态：True、False、Unknown 之一。

  - **conditions.type** (string), 必需

    任务状况的类型：Completed 或 Failed。

  - **conditions.lastProbeTime** (Time)

    最后一次探测的时间。

    
    <a name="Time"></a>
    **Time 是对 time.Time 的封装，支持正确编码为 YAML 和 JSON。我们为 time 包提供的许多工厂方法提供了封装器。**


  - **conditions.lastTransitionTime** (Time)

    上一次从一种状况转换到另一种状况的时间。


    <a name="Time"></a>
    **Time 是 time.Time 的包装器，支持正确编码为 YAML 和 JSON。time 包提供的许多工厂方法都提供了包装器。**


  - **conditions.message** (string)

    表示上次转换信息的人类可读消息。

  - **conditions.reason** (string)

    状况最后一次转换的（简要）原因

- **uncountedTerminatedPods** (UncountedTerminatedPods)

  UncountedTerminatedPods 保存已终止但尚未被任务控制器纳入状态计数器中的 Pod 的 UID 的集合。

  任务控制器所创建 Pod 带有终结器。当 Pod 终止（成功或失败）时，控制器将执行三个步骤以在任务状态中对其进行说明：

  1. 将 Pod UID 添加到此字段的列表中。
  2. 去掉 Pod 中的终结器。
  3. 从数组中删除 Pod UID，同时为相应的计数器加一。

  使用此字段可能无法跟踪旧任务，在这种情况下，该字段保持为空。

  <a name="UncountedTerminatedPods"></a>
  **UncountedTerminatedPods 持有已经终止的 Pod 的 UID，但还没有被计入工作状态计数器中。**


  - **uncountedTerminatedPods.failed** ([]string)

    **集合：合并期间保留唯一值**

    failed 字段包含已失败 Pod 的 UID。


  - **uncountedTerminatedPods.succeeded** ([]string)

    **集合：合并期间保留唯一值**

    succeeded 包含已成功的 Pod 的 UID。

### Beta 级别   {#beta-level}

- **ready** (int32)

  状况为 Ready 的 Pod 数量。

  此字段为 Beta 级别。当特性门控 JobReadyPods 启用（默认启用）时，任务控制器会填充该字段。

## JobList {#JobList}

JobList 是 Job 的集合。

<hr>

- **apiVersion**: batch/v1

- **kind**: JobList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准列表元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>), required

  items 是 Job 对象的列表。

## 操作 {#Operations}

<hr>

### `get` 读取指定的 Job

#### HTTP 请求

GET /apis/batch/v1/namespaces/{namespace}/jobs/{name}

#### 参数

- **name** (**路径参数**)：string，必需

  Job 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

401: Unauthorized

### `get` 读取指定任务的状态

#### HTTP 请求

GET /apis/batch/v1/namespaces/{namespace}/jobs/{name}/status

#### 参数

- **name** (**路径参数**): string, 必需

  Job 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

401: Unauthorized

### `list` 列举或监测 Job 类别的对象

#### HTTP 请求

GET /apis/batch/v1/namespaces/{namespace}/jobs

#### 参数

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **allowWatchBookmarks** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/job-v1#JobList" >}}">JobList</a>): OK

401: Unauthorized

### `list` 列举或监测 Job 类别的对象

#### HTTP 请求

GET /apis/batch/v1/jobs

#### 参数

- **allowWatchBookmarks** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/job-v1#JobList" >}}">JobList</a>): OK

401: Unauthorized

### `create` 创建一个 Job

#### HTTP 请求

POST /apis/batch/v1/namespaces/{namespace}/jobs

#### 参数

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

201 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): Created

202 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): Accepted

401: Unauthorized

### `update` 替换指定的 Job

#### HTTP 请求

PUT /apis/batch/v1/namespaces/{namespace}/jobs/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  Job 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

201 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): Created

401: Unauthorized

### `update` 替换指定 Job 的状态

#### HTTP 请求

PUT /apis/batch/v1/namespaces/{namespace}/jobs/{name}/status

#### 参数

- **name** (**路径参数**): string, 必需

  Job 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

201 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 Job

#### HTTP 请求

PATCH /apis/batch/v1/namespaces/{namespace}/jobs/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  Job 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

201 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): Created

401: Unauthorized

### `patch` 部分更新指定 Job 的状态

#### HTTP 请求

PATCH /apis/batch/v1/namespaces/{namespace}/jobs/{name}/status

#### 参数

- **name** (**路径参数**): string, 必需

  Job 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

201 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): Created

401: Unauthorized

### `delete` 删除一个 Job

#### HTTP 请求

DELETE /apis/batch/v1/namespaces/{namespace}/jobs/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  Job 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 Job 的集合

#### HTTP 请求

DELETE /apis/batch/v1/namespaces/{namespace}/jobs

#### 参数

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **continue** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **gracePeriodSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **labelSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

- **resourceVersion** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
