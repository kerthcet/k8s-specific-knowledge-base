---
title: Kubernetes 系统组件指标
content_type: concept
weight: 70
---



通过系统组件指标可以更好地了解系统组个内部发生的情况。系统组件指标对于构建仪表板和告警特别有用。

Kubernetes 组件以 [Prometheus 格式](https://prometheus.io/docs/instrumenting/exposition_formats/)
生成度量值。
这种格式是结构化的纯文本，旨在使人和机器都可以阅读。


## Kubernetes 中组件的指标  {#metrics-in-kubernetes}

在大多数情况下，可以通过 HTTP 访问组件的 `/metrics` 端点来获取组件的度量值。
对于那些默认情况下不暴露端点的组件，可以使用 `--bind-address` 标志启用。

这些组件的示例：

* {{< glossary_tooltip term_id="kube-controller-manager" text="kube-controller-manager" >}}
* {{< glossary_tooltip term_id="kube-proxy" text="kube-proxy" >}}
* {{< glossary_tooltip term_id="kube-apiserver" text="kube-apiserver" >}}
* {{< glossary_tooltip term_id="kube-scheduler" text="kube-scheduler" >}}
* {{< glossary_tooltip term_id="kubelet" text="kubelet" >}}

在生产环境中，你可能需要配置 [Prometheus 服务器](https://prometheus.io/) 或
某些其他指标搜集器以定期收集这些指标，并使它们在某种时间序列数据库中可用。

请注意，{{< glossary_tooltip term_id="kubelet" text="kubelet" >}} 还会在 `/metrics/cadvisor`，
`/metrics/resource` 和 `/metrics/probes` 端点中公开度量值。这些度量值的生命周期各不相同。

如果你的集群使用了 {{< glossary_tooltip term_id="rbac" text="RBAC" >}}，
则读取指标需要通过基于用户、组或 ServiceAccount 的鉴权，要求具有允许访问
`/metrics` 的 ClusterRole。
例如：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: prometheus
rules:
  - nonResourceURLs:
      - "/metrics"
    verbs:
      - get
```

## 指标生命周期  {#metric-lifecycle}

Alpha 指标 →  稳定的指标 →  弃用的指标 →  隐藏的指标 → 删除的指标

Alpha 指标没有稳定性保证。这些指标可以随时被修改或者删除。

稳定的指标可以保证不会改变。这意味着：

* 稳定的、不包含已弃用（deprecated）签名的指标不会被删除（或重命名）
* 稳定的指标的类型不会被更改

已弃用的指标最终将被删除，不过仍然可用。
这类指标包含注解，标明其被废弃的版本。

例如：

* 被弃用之前：

  ```
  # HELP some_counter this counts things
  # TYPE some_counter counter
  some_counter 0
  ```

* 被弃用之后：

  ```
  # HELP some_counter (Deprecated since 1.15.0) this counts things
  # TYPE some_counter counter
  some_counter 0
  ```

隐藏的指标不会再被发布以供抓取，但仍然可用。
要使用隐藏指标，请参阅[显式隐藏指标](#show-hidden-metrics)节。

删除的指标不再被发布，亦无法使用。

## 显示隐藏指标   {#show-hidden-metrics}

如上所述，管理员可以通过设置可执行文件的命令行参数来启用隐藏指标，
如果管理员错过了上一版本中已经弃用的指标的迁移，则可以把这个用作管理员的逃生门。

`show-hidden-metrics-for-version` 标志接受版本号作为取值，版本号给出
你希望显示该发行版本中已弃用的指标。
版本表示为 x.y，其中 x 是主要版本，y 是次要版本。补丁程序版本不是必须的，
即使指标可能会在补丁程序发行版中弃用，原因是指标弃用策略规定仅针对次要版本。

该参数只能使用前一个次要版本。如果管理员将先前版本设置为 `show-hidden-metrics-for-version`，
则先前版本中隐藏的度量值会再度生成。不允许使用过旧的版本，因为那样会违反指标弃用策略。

以指标 `A` 为例，此处假设 `A` 在 1.n 中已弃用。根据指标弃用策略，我们可以得出以下结论：

* 在版本 `1.n` 中，这个指标已经弃用，且默认情况下可以生成。
* 在版本 `1.n+1` 中，这个指标默认隐藏，可以通过命令行参数 `show-hidden-metrics-for-version=1.n` 来再度生成。
* 在版本 `1.n+2` 中，这个指标就将被从代码中移除，不会再有任何逃生窗口。

如果你要从版本 `1.12` 升级到 `1.13`，但仍依赖于 `1.12` 中弃用的指标 `A`，则应通过命令行设置隐藏指标：
`--show-hidden-metrics=1.12`，并记住在升级到 `1.14` 版本之前删除此指标依赖项。

## 禁用加速器指标  {#disable-accelerator-metrics}

kubelet 通过 cAdvisor 收集加速器指标。为了收集这些指标，对于 NVIDIA GPU 之类的加速器，
kubelet 在驱动程序上保持打开状态。这意味着为了执行基础结构更改（例如更新驱动程序），
集群管理员需要停止 kubelet 代理。

现在，收集加速器指标的责任属于供应商，而不是 kubelet。供应商必须提供一个收集指标的容器，
并将其公开给指标服务（例如 Prometheus）。

[`DisableAcceleratorUsageMetrics` 特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
禁止由 kubelet 收集的指标。
关于[何时会在默认情况下启用此功能也有一定规划](https://github.com/kubernetes/enhancements/tree/411e51027db842355bd489691af897afc1a41a5e/keps/sig-node/1867-disable-accelerator-usage-metrics#graduation-criteria)。

## 组件指标  {#component-metrics}

### kube-controller-manager 指标  {#kube-controller-manager-metrics}

控制器管理器指标可提供有关控制器管理器性能和运行状况的重要洞察。
这些指标包括通用的 Go 语言运行时指标（例如 go_routine 数量）和控制器特定的度量指标，
例如可用于评估集群运行状况的 etcd 请求延迟或云提供商（AWS、GCE、OpenStack）的 API 延迟等。

从 Kubernetes 1.7 版本开始，详细的云提供商指标可用于 GCE、AWS、Vsphere 和 OpenStack 的存储操作。
这些指标可用于监控持久卷操作的运行状况。

比如，对于 GCE，这些指标称为：

```
cloudprovider_gce_api_request_duration_seconds { request = "instance_list"}
cloudprovider_gce_api_request_duration_seconds { request = "disk_insert"}
cloudprovider_gce_api_request_duration_seconds { request = "disk_delete"}
cloudprovider_gce_api_request_duration_seconds { request = "attach_disk"}
cloudprovider_gce_api_request_duration_seconds { request = "detach_disk"}
cloudprovider_gce_api_request_duration_seconds { request = "list_disk"}
```

### kube-scheduler 指标   {#kube-scheduler-metrics}

{{< feature-state for_k8s_version="v1.21" state="beta" >}}

调度器会暴露一些可选的指标，报告所有运行中 Pods 所请求的资源和期望的约束值。
这些指标可用来构造容量规划监控面板、访问调度约束的当前或历史数据、
快速发现因为缺少资源而无法被调度的负载，或者将 Pod 的实际资源用量
与其请求值进行比较。

kube-scheduler 组件能够辩识各个 Pod 所配置的资源
[请求和约束](/zh-cn/docs/concepts/configuration/manage-resources-containers/)。
在 Pod 的资源请求值或者约束值非零时，kube-scheduler 会以度量值时间序列的形式
生成报告。该时间序列值包含以下标签：
- 名字空间
- Pod 名称
- Pod 调度所处节点，或者当 Pod 未被调度时用空字符串表示
- 优先级
- 为 Pod 所指派的调度器
- 资源的名称（例如，`cpu`）
- 资源的单位，如果知道的话（例如，`cores`）

一旦 Pod 进入完成状态（其 `restartPolicy` 为 `Never` 或 `OnFailure`，且
其处于 `Succeeded` 或 `Failed` Pod 阶段，或者已经被删除且所有容器都具有
终止状态），该时间序列停止报告，因为调度器现在可以调度其它 Pod 来执行。
这两个指标称作 `kube_pod_resource_request` 和 `kube_pod_resource_limit`。

指标暴露在 HTTP 端点 `/metrics/resources`，与调度器上的 `/metrics` 端点
一样要求相同的访问授权。你必须使用
`--show-hidden-metrics-for-version=1.20` 标志才能暴露那些稳定性为 Alpha
的指标。

## 禁用指标 {#disabling-metrics}

你可以通过命令行标志 `--disabled-metrics` 来关闭某指标。
在例如某指标会带来性能问题的情况下，这一操作可能是有用的。
标志的参数值是一组被禁止的指标（例如：`--disabled-metrics=metric1,metric2`）。

## 指标顺序性保证    {#metric-cardinality-enforcement}

在 Alpha 阶段，标志只能接受一组映射值作为可以使用的指标标签。
每个映射值的格式为`<指标名称>,<标签名称>=<可用标签列表>`，其中
`<可用标签列表>` 是一个用逗号分隔的、可接受的标签名的列表。

最终的格式看起来会是这样：

```
--allow-label-value <指标名称>,<标签名称>='<可用值1>,<可用值2>...', <指标名称2>,<标签名称>='<可用值1>, <可用值2>...', ...
```

下面是一个例子：

```none
--allow-label-value number_count_metric,odd_number='1,3,5', number_count_metric,even_number='2,4,6', date_gauge_metric,weekend='Saturday,Sunday'
```

## {{% heading "whatsnext" %}}

* 阅读有关指标的 [Prometheus 文本格式](https://github.com/prometheus/docs/blob/master/content/docs/instrumenting/exposition_formats.md#text-based-format)
* 阅读有关 [Kubernetes 弃用策略](/zh-cn/docs/reference/using-api/deprecation-policy/#deprecating-a-feature-or-behavior)
