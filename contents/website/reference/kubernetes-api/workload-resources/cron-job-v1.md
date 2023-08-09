---
api_metadata:
  apiVersion: "batch/v1"
  import: "k8s.io/api/batch/v1"
  kind: "CronJob"
content_type: "api_reference"
description: "CronJob 代表单个定时作业 (Cron Job) 的配置。"
title: "CronJob"
weight: 10
---


`apiVersion: batch/v1`

`import "k8s.io/api/batch/v1"`

## CronJob {#CronJob}

CronJob 代表单个定时作业（Cron Job) 的配置。

<hr>

- **apiVersion**: batch/v1

- **kind**: CronJob

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../workload-resources/cron-job-v1#CronJobSpec" >}}">CronJobSpec</a>)

  定时作业的预期行为的规约，包括排期表（Schedule）。更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

- **status** (<a href="{{< ref "../workload-resources/cron-job-v1#CronJobStatus" >}}">CronJobStatus</a>)

  定时作业的当前状态。更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

## CronJobSpec {#CronJobSpec}


CronJobSpec 描述了作业的执行方式和实际将运行的时间。

<hr>


- **jobTemplate** (JobTemplateSpec), 必需

  指定执行 CronJob 时将创建的作业。


  <a name="JobTemplateSpec"></a>
  **JobTemplateSpec 描述了从模板创建作业时应具有的数据**


  - **jobTemplate.metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

    从此模板创建的作业的标准对象元数据。更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
  

  - **jobTemplate.spec** (<a href="{{< ref "../workload-resources/job-v1#JobSpec" >}}">JobSpec</a>)

    对作业的预期行为的规约。更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
  

- **schedule** (string), 必需

  Cron 格式的排期表，请参阅 https://zh.wikipedia.org/wiki/Cron。
  

- **timeZone** (string)

  给定时间表的时区名称，请参阅 https://en.wikipedia.org/wiki/List_of_tz_database_time_zones。
  如果未指定，这将默认为 kube-controller-manager 进程的时区。
  有效时区名称和时区偏移量的设置由 API 服务器在 CronJob 验证期间从系统范围的时区数据库进行加载，
  在执行期间由控制器管理器从系统范围的时区数据库进行加载。
  如果找不到系统范围的时区数据库，则转而使用该数据库的捆绑版本。
  如果时区名称在 CronJob 的生命周期内或由于主机配置更改而变得无效，该控制器将停止创建新的 Job，
  并将创建一个原因为 UnknownTimeZone 的系统事件。更多信息，请请参阅
  https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/cron-jobs/#time-zones。


- **concurrencyPolicy** (string)

  指定如何处理作业的并发执行。 有效值为：

  - "Allow" (默认)：允许 CronJobs 并发运行；
  - "Forbid"：禁止并发运行，如果上一次运行尚未完成则跳过下一次运行；
  - "Replace"：取消当前正在运行的作业并将其替换为新作业。


- **startingDeadlineSeconds** (int64)

  可选字段。当作业因为某种原因错过预定时间时，设定作业的启动截止时间（秒）。错过排期的作业将被视为失败的作业。


- **suspend** (boolean)

  这个标志告诉控制器暂停后续的执行，它不适用于已经开始的执行。默认为 false。


- **successfulJobsHistoryLimit** (int32)

  要保留的成功完成作业数。值必须是非负整数。默认值为 3。


- **failedJobsHistoryLimit** (int32)

  要保留的以失败状态结束的作业个数。值必须是非负整数。默认值为 1。

## CronJobStatus {#CronJobStatus}

CronJobStatus 表示某个定时作业的当前状态。

<hr>

- **active** ([]<a href="{{< ref "../common-definitions/object-reference#ObjectReference" >}}">ObjectReference</a>)

  **Atomic: 将在合并过程中被替换**

  指向当前正在运行的作业的指针列表。

- **lastScheduleTime** (Time)

  上次成功调度作业的时间信息。

  <a name="Time"></a>
  **Time 是对 time.Time 的封装，它支持对 YAML 和 JSON 的正确编排。为 time 包提供的许多工厂方法模式提供了包装器。**

- **lastSuccessfulTime** (Time)

  上次成功完成作业的时间信息。

  <a name="Time"></a>
  **Time 是对 time.Time 的封装，它支持对 YAML 和 JSON 的正确编排。为 time 包提供的许多工厂方法模式提供了包装器。**

## CronJobList {#CronJobList}

CronJobList 是定时作业的集合。

<hr>

- **apiVersion**: batch/v1

- **kind**: CronJobList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准列表元数据。更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>), required

  items 是 CronJob 的列表。

## 操作 {#Operations}

<hr>

### `get` 查看指定的 CronJob

#### HTTP 请求

GET /apis/batch/v1/namespaces/{namespace}/cronjobs/{name}

#### 参数


- **name** (**路径参数**): string, 必需

  CronJob 的名称

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): OK

401: Unauthorized


### `get` 查看指定 CronJob 的状态

#### HTTP 请求

GET /apis/batch/v1/namespaces/{namespace}/cronjobs/{name}/status

#### 参数


- **name** (**路径参数**): string, 必需

  CronJob 的名称

- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): OK

401: Unauthorized

### `list` 查看或监视 CronJob 类别的对象

#### HTTP 请求

GET /apis/batch/v1/namespaces/{namespace}/cronjobs

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

200 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJobList" >}}">CronJobList</a>): OK

401: Unauthorized

### `list` 查看或监视 CronJob 类型的对象

#### HTTP 请求

GET /apis/batch/v1/cronjobs

#### 参数


- **allowWatchBookmarks** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>


- **continue** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>


- **fieldSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


- **labelSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>


- **limit** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


- **resourceVersion** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>


- **timeoutSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>


- **watch** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>


#### 响应

200 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJobList" >}}">CronJobList</a>): OK

401: Unauthorized


### `create` 创建一个 CronJob

#### HTTP 请求

POST /apis/batch/v1/namespaces/{namespace}/cronjobs

#### 参数


- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>, 必需


- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): OK

201 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): Created

202 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): Accepted

401: Unauthorized


### `update` 替换指定的 CronJob

#### HTTP 请求

PUT /apis/batch/v1/namespaces/{namespace}/cronjobs/{name}

#### 参数


- **name** (**路径参数**): string, 必需

  CronJob 的名称


- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): OK

201 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): Created

401: Unauthorized


### `update` 替换指定 CronJob 的状态

#### HTTP 请求

PUT /apis/batch/v1/namespaces/{namespace}/cronjobs/{name}/status

#### 参数


- **name** (**路径参数**): string, 必需

  CronJob 的名称


- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>, 必需


- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): OK

201 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): Created

401: Unauthorized


### `patch` 部分更新指定的 CronJob

#### HTTP 请求

PATCH /apis/batch/v1/namespaces/{namespace}/cronjobs/{name}

#### 参数


- **name** (**路径参数**): string, 必需

  CronJob 的名称


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

200 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): OK

201 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): Created

401: Unauthorized


### `patch` 部分更新指定 CronJob 的状态

#### HTTP 请求

PATCH /apis/batch/v1/namespaces/{namespace}/cronjobs/{name}/status

#### 参数


- **name** (**路径参数**): string, 必需

  CronJob 的名称


- **namespace** (**路径参数**): string, 必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, 必需


- **dryRun** (**参数参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (**参数参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **fieldValidation** (**参数参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


- **force** (**参数参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>


- **pretty** (**参数参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): OK

201 (<a href="{{< ref "../workload-resources/cron-job-v1#CronJob" >}}">CronJob</a>): Created

401: Unauthorized


### `delete` 删除一个 CronJob

#### HTTP 请求

DELETE /apis/batch/v1/namespaces/{namespace}/cronjobs/{name}

#### 参数


- **name** (**路径参数**): string, 必需

  CronJob 的名称


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


### `deletecollection` 删除一组 CronJob

#### HTTP 请求

DELETE /apis/batch/v1/namespaces/{namespace}/cronjobs

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

