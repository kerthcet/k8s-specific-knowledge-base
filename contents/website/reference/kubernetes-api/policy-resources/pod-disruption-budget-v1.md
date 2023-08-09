---
api_metadata:
  apiVersion: "policy/v1"
  import: "k8s.io/api/policy/v1"
  kind: "PodDisruptionBudget"
content_type: "api_reference"
description: "PodDisruptionBudget 是一个对象，用于定义可能对一组 Pod 造成的最大干扰。"
title: "PodDisruptionBudget"
weight: 4
---


`apiVersion: policy/v1`

`import "k8s.io/api/policy/v1"`

## PodDisruptionBudget {#PodDisruptionBudget}

PodDisruptionBudget 是一个对象，用于定义可能对一组 Pod 造成的最大干扰。

<hr>

- **apiVersion**: policy/v1

- **kind**: PodDisruptionBudget

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata。

- **spec** (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudgetSpec" >}}">PodDisruptionBudgetSpec</a>)

  PodDisruptionBudget 预期行为的规约。


- **status** (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudgetStatus" >}}">PodDisruptionBudgetStatus</a>)

  此 PodDisruptionBudget 的最近观测状态。

## PodDisruptionBudgetSpec {#PodDisruptionBudgetSpec}

PodDisruptionBudgetSpec 是对 PodDisruptionBudget 的描述。

<hr>


- **maxUnavailable** (IntOrString)

  如果 “selector” 所选中的 Pod 中最多有 “maxUnavailable” Pod 在驱逐后不可用（即去掉被驱逐的 Pod 之后），则允许驱逐。
  例如，可以通过将此字段设置为 0 来阻止所有自愿驱逐。此字段是与 “minAvailable” 互斥的设置。

  <a name="IntOrString"></a>
  IntOrString 是一种可以包含 int32 或字符串数值的类型。在 JSON 或 YAML 编组和解组时，
  会生成或使用内部类型。例如，此类型允许你定义一个可以接受名称或数字的 JSON 字段。


- **minAvailable** (IntOrString)

  如果 “selector” 所选中的 Pod 中，至少 “minAvailable” 个 Pod 在驱逐后仍然可用（即去掉被驱逐的 Pod 之后），则允许驱逐。
  因此，你可以通过将此字段设置为 “100%” 来禁止所有自愿驱逐。

  <a name="IntOrString"></a>
  IntOrString 是一种可以包含 int32 或字符串数值的类型。在 JSON 或 YAML 编组和解组时，
  会生成或使用内部类型。例如，此类型允许你定义一个可以接受名称或数字的 JSON 字段。


- **selector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)

  标签查询，用来选择其驱逐由干扰预算来管理的 Pod 集合。
  选择算符为 null 时将不会匹配任何 Pod，而空 ({}) 选择算符将选中名字空间内的所有 Pod。

- **unhealthyPodEvictionPolicy** (string)

  unhealthyPodEvictionPolicy 定义不健康的 Pod 应被考虑驱逐时的标准。
  当前的实现将健康的 Pod 视为具有 status.conditions 项且 type="Ready"、status="True" 的 Pod。

  有效的策略是 IfHealthyBudget 和 AlwaysAllow。
  如果没有策略被指定，则使用与 IfHealthyBudget 策略对应的默认行为。

  IfHealthyBudget 策略意味着正在运行（status.phase="Running"）但还不健康的 Pod
  只有在被守护的应用未受干扰（status.currentHealthy 至少等于 status.desiredHealthy）
  时才能被驱逐。健康的 Pod 将受到 PDB 的驱逐。

  AlwaysAllow 策略意味着无论是否满足 PDB 中的条件，所有正在运行（status.phase="Running"）但还不健康的
  Pod 都被视为受干扰且可以被驱逐。这意味着受干扰应用的透视运行 Pod 可能没有机会变得健康。
  健康的 Pod 将受到 PDB 的驱逐。

  将来可能会添加其他策略。如果客户端在该字段遇到未识别的策略，则做出驱逐决定的客户端应禁止驱逐不健康的 Pod。

  该字段是 Alpha 级别的。当特性门控 PDBUnhealthyPodEvictionPolicy 被启用（默认禁用）时，驱逐 API 使用此字段。

## PodDisruptionBudgetStatus {#PodDisruptionBudgetStatus}

PodDisruptionBudgetStatus 表示有关此 PodDisruptionBudget 状态的信息。状态可能会反映系统的实际状态。

<hr>


- **currentHealthy** (int32), 必需

  当前健康 Pod 的数量。


- **desiredHealthy** (int32), 必需

  健康 Pod 的最小期望值。


- **disruptionsAllowed** (int32), 必需

  当前允许的 Pod 干扰计数。


- **expectedPods** (int32), 必需

  此干扰预算计入的 Pod 总数

- **conditions** ([]Condition)


  **补丁策略：根据 `type` 键执行合并操作**

  **Map：键 type 的唯一值将在合并期间被保留**

  conditions 包含 PDB 的状况。干扰控制器会设置 DisruptionAllowed 状况。
  以下是 reason 字段的已知值（将来可能会添加其他原因）：

  - SyncFailed：控制器遇到错误并且无法计算允许的干扰计数。因此不允许任何干扰，且状况的状态将变为 False。
  - InsufficientPods：Pod 的数量只能小于或等于 PodDisruptionBudget 要求的数量。
    不允许任何干扰，且状况的状态将是 False。
  - SufficientPods：Pod 个数超出 PodDisruptionBudget 所要求的阈值。
    此状况为 True 时，基于 disruptsAllowed 属性确定所允许的干扰数目。


  <a name="Condition"></a>
  Condition 包含此 API 资源当前状态的一个方面的详细信息。


  - **conditions.lastTransitionTime** (Time), 必需

    lastTransitionTime 是状况最近一次从一种状态转换到另一种状态的时间。
    这种变化通常出现在下层状况发生变化的时候。如果无法了解下层状况变化，使用 API 字段更改的时间也是可以接受的。

    <a name="Time"></a>
    Time 是 time.Time 的包装器，它支持对 YAML 和 JSON 的正确编组。
    time 包的许多工厂方法提供了包装器。


  - **conditions.message** (string), 必需

    message 是一条人类可读的消息，指示有关转换的详细信息。它可能是一个空字符串。


  - **conditions.reason** (string), 必需

    reason 包含一个程序标识符，指示状况最后一次转换的原因。
    特定状况类型的生产者可以定义该字段的预期值和含义，以及这些值是否可被视为有保证的 API。
    该值应该是 CamelCase 字符串。此字段不能为空。


  - **conditions.status** (string), 必需

    状况的状态为 True、False、Unknown 之一。


  - **conditions.type** (string), 必需

    CamelCase 或 foo.example.com/CamelCase 形式的状况类型。


  - **conditions.observedGeneration** (int64)

    observedGeneration 表示设置状况时所基于的 .metadata.generation。
    例如，如果 .metadata.generation 当前为 12，但 .status.conditions[x].observedGeneration 为 9，
    则状况相对于实例的当前状态已过期。


- **disruptedPods** (map[string]Time)

  disruptedPods 包含有关 Pod 的一些信息，这些 Pod 的驱逐操作已由 API 服务器上的 eviction 子资源处理程序处理,
  但尚未被 PodDisruptionBudget 控制器观察到。
  从 API 服务器处理驱逐请求到 PDB 控制器看到该 Pod 已标记为删除（或超时后），Pod 将记录在此映射中。
  映射中的键名是 Pod 的名称，键值是 API 服务器处理驱逐请求的时间。
  如果删除没有发生并且 Pod 仍然存在，PodDisruptionBudget 控制器将在一段时间后自动将 Pod 从列表中删除。
  如果一切顺利，此映射大部分时间应该是空的。映射中的存在大量条目可能表明 Pod 删除存在问题。

  <a name="Time"></a>
  Time 是 time.Time 的包装器，它支持对 YAML 和 JSON 的正确编组。
  time 包的许多工厂方法提供了包装器。


- **observedGeneration** (int64)

  更新此 PDB 状态时观察到的最新一代。
  DisruptionsAllowed 和其他状态信息仅在 observedGeneration 等于 PDB 的对象的代数时才有效。

## PodDisruptionBudgetList {#PodDisruptionBudgetList}


PodDisruptionBudgetList 是 PodDisruptionBudget 的集合。

<hr>

- **apiVersion**: policy/v1

- **kind**: PodDisruptionBudgetList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的对象元数据。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata。


- **items** ([]<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>), 必需

  items 是 PodDisruptionBudgets 的列表。


## 操作 {#Operations}

<hr>


### `get` 读取指定的 PodDisruptionBudget

#### HTTP 请求

GET /apis/policy/v1/namespaces/{namespace}/poddisruptionbudgets/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  PodDisruptionBudget 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): OK

401: Unauthorized

### `get` 读取指定 PodDisruptionBudget 的状态

#### HTTP 请求

GET /apis/policy/v1/namespaces/{namespace}/poddisruptionbudgets/{name}/status

#### 参数

- **name** (**路径参数**): string, 必需

  PodDisruptionBudget 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

响应

200 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): OK

401: Unauthorized

### `list` 列出或监视 PodDisruptionBudget 类型的对象

#### HTTP 请求

GET /apis/policy/v1/namespaces/{namespace}/poddisruptionbudgets

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

200 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudgetList" >}}">PodDisruptionBudgetList</a>): OK

401: Unauthorized

### `list` 列出或监视 PodDisruptionBudget 类型的对象

#### HTTP 请求

GET /apis/policy/v1/poddisruptionbudgets

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

200 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudgetList" >}}">PodDisruptionBudgetList</a>): OK

401: Unauthorized

### `create` 创建一个 PodDisruptionBudget
#### HTTP 请求

POST /apis/policy/v1/namespaces/{namespace}/poddisruptionbudgets

#### 参数

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>,
  必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): OK

201 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): Created

202 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): Accepted

401: Unauthorized

### `update` 替换指定的 PodDisruptionBudget

#### HTTP 请求

PUT /apis/policy/v1/namespaces/{namespace}/poddisruptionbudgets/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  PodDisruptionBudget 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>,
  必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

#### 响应

200 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): OK

201 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): Created

401: Unauthorized

### `update` 替换指定 PodDisruptionBudget 的状态

#### HTTP 请求

PUT /apis/policy/v1/namespaces/{namespace}/poddisruptionbudgets/{name}/status

#### 参数

- **name** (**路径参数**): string, 必需

  PodDisruptionBudget 的名称。

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>,
  必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


#### 响应

200 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): OK

201 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 PodDisruptionBudget

#### HTTP 请求

PATCH /apis/policy/v1/namespaces/{namespace}/poddisruptionbudgets/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  PodDisruptionBudget 的名称

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

200 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): OK

201 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): Created

401: Unauthorized

### `patch` 部分更新指定 PodDisruptionBudget 的状态

#### HTTP 请求

PATCH /apis/policy/v1/namespaces/{namespace}/poddisruptionbudgets/{name}/status

#### 参数

- **name** (**路径参数**): string, 必需

  PodDisruptionBudget 的名称。

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

200 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): OK

201 (<a href="{{< ref "../policy-resources/pod-disruption-budget-v1#PodDisruptionBudget" >}}">PodDisruptionBudget</a>): Created

401: Unauthorized

### `delete` 删除 PodDisruptionBudget

#### HTTP 请求

DELETE /apis/policy/v1/namespaces/{namespace}/poddisruptionbudgets/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  PodDisruptionBudget 的名称。

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

### `deletecollection` 删除 PodDisruptionBudget 的集合

#### HTTP Request

DELETE /apis/policy/v1/namespaces/{namespace}/poddisruptionbudgets

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
