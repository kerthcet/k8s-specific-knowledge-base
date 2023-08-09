---
title: Kubernetes API 健康端点
content_type: concept
weight: 50
---

Kubernetes {{< glossary_tooltip term_id="kube-apiserver" text="API 服务器" >}} 提供 API 端点以指示 API 服务器的当前状态。
本文描述了这些 API 端点，并说明如何使用。


## API 健康端点  {#api-endpoints-for-health}

Kubernetes API 服务器提供 3 个 API 端点（`healthz`、`livez` 和 `readyz`）来表明 API 服务器的当前状态。
`healthz` 端点已被弃用（自 Kubernetes v1.16 起），你应该使用更为明确的 `livez` 和 `readyz` 端点。
`livez` 端点可与 `--livez-grace-period` [标志](/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver)一起使用，来指定启动持续时间。
为了正常关机，你可以使用 `/readyz` 端点并指定 `--shutdown-delay-duration` [标志](/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver)。
检查 API 服务器的 `healthz`/`livez`/`readyz` 端点的机器应依赖于 HTTP 状态代码。
状态码 `200` 表示 API 服务器是 `healthy`、`live` 还是 `ready`，具体取决于所调用的端点。
以下更详细的选项供操作人员使用，用来调试其集群或了解 API 服务器的状态。

以下示例将显示如何与运行状况 API 端点进行交互。

对于所有端点，都可以使用 `verbose` 参数来打印检查项以及检查状态。
这对于操作人员调试 API 服务器的当前状态很有用，这些不打算给机器使用：

```shell
curl -k https://localhost:6443/livez?verbose
```

或从具有身份验证的远程主机：

```shell
kubectl get --raw='/readyz?verbose'
```

输出将如下所示：

```
[+]ping ok
[+]log ok
[+]etcd ok
[+]poststarthook/start-kube-apiserver-admission-initializer ok
[+]poststarthook/generic-apiserver-start-informers ok
[+]poststarthook/start-apiextensions-informers ok
[+]poststarthook/start-apiextensions-controllers ok
[+]poststarthook/crd-informer-synced ok
[+]poststarthook/bootstrap-controller ok
[+]poststarthook/rbac/bootstrap-roles ok
[+]poststarthook/scheduling/bootstrap-system-priority-classes ok
[+]poststarthook/start-cluster-authentication-info-controller ok
[+]poststarthook/start-kube-aggregator-informers ok
[+]poststarthook/apiservice-registration-controller ok
[+]poststarthook/apiservice-status-available-controller ok
[+]poststarthook/kube-apiserver-autoregistration ok
[+]autoregister-completion ok
[+]poststarthook/apiservice-openapi-controller ok
healthz check passed
```

Kubernetes API 服务器也支持排除特定的检查项。
查询参数也可以像以下示例一样进行组合：

```shell
curl -k 'https://localhost:6443/readyz?verbose&exclude=etcd'
```

输出显示排除了 `etcd` 检查：

```
[+]ping ok
[+]log ok
[+]etcd excluded: ok
[+]poststarthook/start-kube-apiserver-admission-initializer ok
[+]poststarthook/generic-apiserver-start-informers ok
[+]poststarthook/start-apiextensions-informers ok
[+]poststarthook/start-apiextensions-controllers ok
[+]poststarthook/crd-informer-synced ok
[+]poststarthook/bootstrap-controller ok
[+]poststarthook/rbac/bootstrap-roles ok
[+]poststarthook/scheduling/bootstrap-system-priority-classes ok
[+]poststarthook/start-cluster-authentication-info-controller ok
[+]poststarthook/start-kube-aggregator-informers ok
[+]poststarthook/apiservice-registration-controller ok
[+]poststarthook/apiservice-status-available-controller ok
[+]poststarthook/kube-apiserver-autoregistration ok
[+]autoregister-completion ok
[+]poststarthook/apiservice-openapi-controller ok
[+]shutdown ok
healthz check passed
```

## 独立健康检查  {#individual-health-check}

{{< feature-state state="alpha" >}}

每个单独的健康检查都会公开一个 HTTP 端点，并且可以单独检查。
单个运行状况检查的模式为 `/livez/<healthcheck-name>`，其中 `livez` 和 `readyz` 表明你要检查的是 API 服务器是否存活或就绪。
`<healthcheck-name>` 的路径可以通过上面的 `verbose` 参数发现 ，并采用 `[+]` 和 `ok` 之间的路径。
这些单独的健康检查不应由机器使用，但对于操作人员调试系统而言，是有帮助的：

```shell
curl -k https://localhost:6443/livez/etcd
```
