---
title: 审计
content_type: concept
---


Kubernetes **审计（Auditing）** 功能提供了与安全相关的、按时间顺序排列的记录集，
记录每个用户、使用 Kubernetes API 的应用以及控制面自身引发的活动。

审计功能使得集群管理员能够回答以下问题：

 - 发生了什么？
 - 什么时候发生的？
 - 谁触发的？
 - 活动发生在哪个（些）对象上？
 - 在哪观察到的？
 - 它从哪触发的？
 - 活动的后续处理行为是什么？


审计记录最初产生于
[kube-apiserver](/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver/)
内部。每个请求在不同执行阶段都会生成审计事件；这些审计事件会根据特定策略被预处理并写入后端。
策略确定要记录的内容和用来存储记录的后端，当前的后端支持日志文件和 webhook。

每个请求都可被记录其相关的**阶段（stage）**。已定义的阶段有：

- `RequestReceived` - 此阶段对应审计处理器接收到请求后，
  并且在委托给其余处理器之前生成的事件。
- `ResponseStarted` - 在响应消息的头部发送后，响应消息体发送前生成的事件。
  只有长时间运行的请求（例如 watch）才会生成这个阶段。
- `ResponseComplete` - 当响应消息体完成并且没有更多数据需要传输的时候。
- `Panic` - 当 panic 发生时生成。

{{< note >}}
[审计事件配置](/zh-cn/docs/reference/config-api/apiserver-audit.v1/#audit-k8s-io-v1-Event)
的配置与 [Event](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#event-v1-core)
API 对象不同。
{{< /note >}}

审计日志记录功能会增加 API server 的内存消耗，因为需要为每个请求存储审计所需的某些上下文。
内存消耗取决于审计日志记录的配置。

## 审计策略  {#audit-policy}

审计策略定义了关于应记录哪些事件以及应包含哪些数据的规则。
审计策略对象结构定义在
[`audit.k8s.io` API 组](/zh-cn/docs/reference/config-api/apiserver-audit.v1/#audit-k8s-io-v1-Policy)。
处理事件时，将按顺序与规则列表进行比较。第一个匹配规则设置事件的**审计级别（Audit Level）**。
已定义的审计级别有：

- `None` - 符合这条规则的日志将不会记录。
- `Metadata` - 记录请求的元数据（请求的用户、时间戳、资源、动词等等），
  但是不记录请求或者响应的消息体。
- `Request` - 记录事件的元数据和请求的消息体，但是不记录响应的消息体。
  这不适用于非资源类型的请求。
- `RequestResponse` - 记录事件的元数据，请求和响应的消息体。这不适用于非资源类型的请求。

你可以使用 `--audit-policy-file` 标志将包含策略的文件传递给 `kube-apiserver`。
如果不设置该标志，则不记录事件。
注意 `rules` 字段**必须**在审计策略文件中提供。没有（0）规则的策略将被视为非法配置。

以下是一个审计策略文件的示例：

{{< codenew file="audit/audit-policy.yaml" >}}

你可以使用最低限度的审计策略文件在 `Metadata` 级别记录所有请求：

```yaml
# 在 Metadata 级别为所有请求生成日志
apiVersion: audit.k8s.io/v1beta1
kind: Policy
rules:
- level: Metadata
```

如果你在打磨自己的审计配置文件，你可以使用为 Google Container-Optimized OS
设计的审计配置作为出发点。你可以参考
[configure-helper.sh](https://github.com/kubernetes/kubernetes/blob/master/cluster/gce/gci/configure-helper.sh)
脚本，该脚本能够生成审计策略文件。你可以直接在脚本中看到审计策略的绝大部份内容。

你也可以参考 [`Policy` 配置参考](/zh-cn/docs/reference/config-api/apiserver-audit.v1/#audit-k8s-io-v1-Policy)
以获取有关已定义字段的详细信息。

## 审计后端   {#audit-backends}

审计后端实现将审计事件导出到外部存储。`kube-apiserver` 默认提供两个后端：

- Log 后端，将事件写入到文件系统
- Webhook 后端，将事件发送到外部 HTTP API

在这所有情况下，审计事件均遵循 Kubernetes API 在
[`audit.k8s.io` API 组](/zh-cn/docs/reference/config-api/apiserver-audit.v1/#audit-k8s-io-v1-Event)
中定义的结构。

{{< note >}}
对于 patch 请求，请求的消息体需要是设定 patch 操作的 JSON 所构成的一个串，
而不是一个完整的 Kubernetes API 对象的 JSON 串。
例如，以下的示例是一个合法的 patch 请求消息体，该请求对应
`/apis/batch/v1/namespaces/some-namespace/jobs/some-job-name`：

```json
[
  {
    "op": "replace",
    "path": "/spec/parallelism",
    "value": 0
  },
  {
    "op": "remove",
    "path": "/spec/template/spec/containers/0/terminationMessagePolicy"
  }
]
```
{{< /note >}}

### Log 后端   {#log-backend}

Log 后端将审计事件写入 [JSONlines](https://jsonlines.org/) 格式的文件。
你可以使用以下 `kube-apiserver` 标志配置 Log 审计后端：

- `--audit-log-path` 指定用来写入审计事件的日志文件路径。不指定此标志会禁用日志后端。`-` 意味着标准化
- `--audit-log-maxage` 定义保留旧审计日志文件的最大天数
- `--audit-log-maxbackup` 定义要保留的审计日志文件的最大数量
- `--audit-log-maxsize` 定义审计日志文件轮转之前的最大大小（兆字节）

如果你的集群控制面以 Pod 的形式运行 kube-apiserver，记得要通过 `hostPath`
卷来访问策略文件和日志文件所在的目录，这样审计记录才会持久保存下来。例如：

```yaml
  - --audit-policy-file=/etc/kubernetes/audit-policy.yaml
  - --audit-log-path=/var/log/kubernetes/audit/audit.log
```

接下来挂载数据卷：

```yaml
...
volumeMounts:
  - mountPath: /etc/kubernetes/audit-policy.yaml
    name: audit
    readOnly: true
  - mountPath: /var/log/kubernetes/audit/
    name: audit-log
    readOnly: false
```

最后配置 `hostPath`：

```yaml
...
volumes:
- name: audit
  hostPath:
    path: /etc/kubernetes/audit-policy.yaml
    type: File

- name: audit-log
  hostPath:
    path: /var/log/kubernetes/audit/
    type: DirectoryOrCreate
```

### Webhook 后端   {#webhook-backend}

Webhook 后端将审计事件发送到远程 Web API，该远程 API 应该暴露与 `kube-apiserver`
形式相同的 API，包括其身份认证机制。你可以使用如下 kube-apiserver 标志来配置
Webhook 审计后端：

- `--audit-webhook-config-file` 设置 Webhook 配置文件的路径。Webhook 配置文件实际上是一个
  [kubeconfig 文件](/zh-cn/docs/concepts/configuration/organize-cluster-access-kubeconfig/)。
- `--audit-webhook-initial-backoff` 指定在第一次失败后重发请求等待的时间。随后的请求将以指数退避重试。

Webhook 配置文件使用 kubeconfig 格式指定服务的远程地址和用于连接它的凭据。

## 事件批处理  {#batching}

日志和 Webhook 后端都支持批处理。以 Webhook 为例，以下是可用参数列表。要获取日志
后端的同样参数，请在参数名称中将 `webhook` 替换为 `log`。
默认情况下，在 `webhook` 中批处理是被启用的，在 `log` 中批处理是被禁用的。
同样，默认情况下，在 `webhook` 中启用带宽限制，在 `log` 中禁用带宽限制。

- `--audit-webhook-mode` 定义缓存策略，可选值如下：
  - `batch` - 以批处理缓存事件和异步的过程。这是默认值。
  - `blocking` - 在 API 服务器处理每个单独事件时，阻塞其响应。
  - `blocking-strict` - 与 `blocking` 相同，不过当审计日志在 RequestReceived
    阶段失败时，整个 API 服务请求会失效。

以下参数仅用于 `batch` 模式：

- `--audit-webhook-batch-buffer-size` 定义 batch 之前要缓存的事件数。
  如果传入事件的速率溢出缓存区，则会丢弃事件。
- `--audit-webhook-batch-max-size` 定义一个 batch 中的最大事件数。
- `--audit-webhook-batch-max-wait` 无条件 batch 队列中的事件前等待的最大事件。
- `--audit-webhook-batch-throttle-qps` 每秒生成的最大批次数。
- `--audit-webhook-batch-throttle-burst` 在达到允许的 QPS 前，同一时刻允许存在的最大 batch 生成数。

## 参数调整   {#parameter-tuning}

需要设置参数以适应 API 服务器上的负载。

例如，如果 kube-apiserver 每秒收到 100 个请求，并且每个请求仅在 `ResponseStarted`
和 `ResponseComplete` 阶段进行审计，则应该考虑每秒生成约 200 个审计事件。
假设批处理中最多有 100 个事件，则应将限制级别设置为每秒至少 2 个查询。
假设后端最多需要 5 秒钟来写入事件，你应该设置缓冲区大小以容纳最多 5 秒的事件，
即 10 个 batch，即 1000 个事件。

但是，在大多数情况下，默认参数应该足够了，你不必手动设置它们。
你可以查看 kube-apiserver 公开的以下 Prometheus 指标，并在日志中监控审计子系统的状态。

- `apiserver_audit_event_total` 包含所有暴露的审计事件数量的指标。
- `apiserver_audit_error_total` 在暴露时由于发生错误而被丢弃的事件的数量。

### 日志条目截断   {#truncate}

日志后端和 Webhook 后端都支持限制所输出的事件大小。
例如，下面是可以为日志后端配置的标志列表：

- `audit-log-truncate-enabled`：是否弃用事件和批次的截断处理。
- `audit-log-truncate-max-batch-size`：向下层后端发送的各批次的最大字节数。
- `audit-log-truncate-max-event-size`：向下层后端发送的审计事件的最大字节数。

默认情况下，截断操作在 `webhook` 和 `log` 后端都是被禁用的，集群管理员需要设置
`audit-log-truncate-enabled` 或 `audit-webhook-truncate-enabled` 标志来启用此操作。

## {{% heading "whatsnext" %}}

* 进一步了解 [Mutating webhook 审计注解](/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/#mutating-webhook-auditing-annotations)。
* 通过阅读审计配置参考，进一步了解
  [`Event`](/docs/reference/config-api/apiserver-audit.v1/#audit-k8s-io-v1-Event)
  和 [`Policy`](/docs/reference/config-api/apiserver-audit.v1/#audit-k8s-io-v1-Policy) 资源的信息。