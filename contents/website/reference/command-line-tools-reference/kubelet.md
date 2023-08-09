---
title: kubelet
content_type: tool-reference
weight: 20
---

## {{% heading "synopsis" %}}


kubelet 是在每个节点上运行的主要 “节点代理”。它可以使用以下方式之一向 API 服务器注册：
- 主机名（hostname）；
- 覆盖主机名的参数；
- 特定于某云驱动的逻辑。

kubelet 是基于 PodSpec 来工作的。每个 PodSpec 是一个描述 Pod 的 YAML 或 JSON 对象。
kubelet 接受通过各种机制（主要是通过 apiserver）提供的一组 PodSpec，并确保这些
PodSpec 中描述的容器处于运行状态且运行状况良好。
kubelet 不管理不是由 Kubernetes 创建的容器。

除了来自 API 服务器的 PodSpec 之外，还可以通过以下两种方式将容器清单（manifest）提供给 kubelet。

- 文件（File）：利用命令行参数传递路径。kubelet 周期性地监视此路径下的文件是否有更新。
  监视周期默认为 20s，且可通过参数进行配置。

- HTTP 端点（HTTP endpoint）：利用命令行参数指定 HTTP 端点。
  此端点的监视周期默认为 20 秒，也可以使用参数进行配置。

```
kubelet [flags]
```

## {{% heading "options" %}}

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubelet 用来提供服务的 IP 地址（设置为 <code>0.0.0.0</code> 或 <code>::</code> 表示监听所有接口和 IP 协议族）。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--allowed-unsafe-sysctls strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用逗号分隔的字符串序列设置允许使用的非安全的 sysctls 或 sysctl 模式（以 <code>&ast;</code> 结尾）。
使用此参数时风险自担。（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置为 true 表示 kubelet 服务器可以接受匿名请求。未被任何认证组件拒绝的请求将被视为匿名请求。
匿名请求的用户名为 <code>system:anonymous</code>，用户组为 <code>system:unauthenticated</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--authentication-token-webhook</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
使用 <code>TokenReview</code> API 对持有者令牌进行身份认证。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对 Webhook 令牌认证组件所返回的响应的缓存时间。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubelet 服务器的鉴权模式。可选值包括：AlwaysAllow、Webhook。
Webhook 模式使用 SubjectAccessReview API 鉴权。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对 Webhook 认证组件所返回的 “Authorized（已授权）” 应答的缓存时间。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对 Webhook 认证组件所返回的 “Unauthorized（未授权）” 应答的缓存时间。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--azure-container-registry-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 Azure 容器镜像库配置信息的文件的路径。
</td>
</tr>

<tr>
<td colspan="2">--bootstrap-kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
某 kubeconfig 文件的路径，该文件将用于获取 kubelet 的客户端证书。
如果 <code>--kubeconfig</code> 所指定的文件不存在，则使用引导所用 kubeconfig
从 API 服务器请求客户端证书。成功后，将引用生成的客户端证书和密钥的 kubeconfig
写入 --kubeconfig 所指定的路径。客户端证书和密钥文件将存储在 <code>--cert-dir</code>
所指的目录。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
TLS 证书所在的目录。如果设置了 <code>--tls-cert-file</code> 和 <code>--tls-private-key-file</code>，
则此标志将被忽略。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubelet 用来操作本机 cgroup 时使用的驱动程序。支持的选项包括 <code>cgroupfs</code>
和 <code>systemd</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可选的选项，为 Pod 设置根 cgroup。容器运行时会尽可能使用此配置。
默认值 <code>""</code> 意味着将使用容器运行时的默认设置。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
启用创建 QoS cgroup 层次结构。此值为 true 时 kubelet 为 QoS 和 Pod 创建顶级的 cgroup。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--client-ca-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如果设置了此参数，则使用对应文件中机构之一检查请求中所携带的客户端证书。
若客户端证书通过身份认证，则其对应身份为其证书中所设置的 <code>CommonName</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--cloud-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
云驱动配置文件的路径。空字符串表示没有配置文件。
已弃用：将在 1.24 或更高版本中移除，以便于从 kubelet 中去除云驱动代码。
</td>
</tr>

<tr>
<td colspan="2">--cloud-provider string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
云服务的提供者。设置为空字符串表示在没有云驱动的情况下运行。
如果设置了此标志，则云驱动负责确定节点的名称（参考云提供商文档以确定是否以及如何使用主机名）。
已弃用：将在 1.24 或更高版本中移除，以便于从 kubelet 中去除云驱动代码。
</td>
</tr>

<tr>
<td colspan="2">--cluster-dns strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
DNS 服务器的 IP 地址，以逗号分隔。此标志值用于 Pod 中设置了 “<code>dnsPolicy=ClusterFirst</code>”
时为容器提供 DNS 服务。<br/><B>注意:</B>：列表中出现的所有 DNS 服务器必须包含相同的记录组，
否则集群中的名称解析可能无法正常工作。至于名称解析过程中会牵涉到哪些 DNS 服务器，
这一点无法保证。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--cluster-domain string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
集群的域名。如果设置了此值，kubelet 除了将主机的搜索域配置到所有容器之外，还会为其
配置所搜这里指定的域名。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubelet 将从此标志所指的文件中加载其初始配置。此路径可以是绝对路径，也可以是相对路径。
相对路径按 kubelet 的当前工作目录起计。省略此参数时 kubelet 会使用内置的默认配置值。
命令行参数会覆盖此文件中的配置。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
【警告：Beta 特性】设置容器的日志文件个数上限。此值必须大于等于 2。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
【警告：Beta 特性】设置容器日志文件在轮换生成新文件时之前的最大值（例如，<code>10Mi</code>）。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
要使用的容器运行时。目前支持 <code>docker<code>、</code>remote</code>。
（已弃用：将会在 1.27 版本中移除，因为合法值只有 “remote”）
</td>
</tr>

<tr>
<td colspan="2">--container-runtime-endpoint string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
远程运行时服务的端点。目前支持 Linux 系统上的 UNIX 套接字和
Windows 系统上的 npipe 和 TCP 端点。例如：
<code>unix:///path/to/runtime.sock</code>、
<code>npipe:////./pipe/runtime</code>。
</td>
</tr>

<tr>
<td colspan="2">--contention-profiling</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
当启用了性能分析时，启用锁竞争分析。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
为设置了 CPU 限制的容器启用 CPU CFS 配额保障。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置 CPU CFS 配额周期 <code>cpu.cfs_period_us</code>。默认使用 Linux 内核所设置的默认值。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
要使用的 CPU 管理器策略。可选值包括：<code>none</code> 和 <code>static</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--cpu-manager-policy-options string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
一组用于微调 CPU 管理器策略行为的 key=value 选项。如果未提供，保留默认行为。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
【警告：Alpha 特性】设置 CPU 管理器的调和时间。例如：<code>10s</code> 或者 <code>1m</code>。
如果未设置，默认使用节点状态更新频率。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
启用 Attach/Detach 控制器来挂接和摘除调度到该节点的卷，同时禁用 kubelet 执行挂接和摘除操作。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
启用服务器上用于日志收集和在本地运行容器和命令的端点。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
启用 kubelet 服务器。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用逗号分隔的列表，包含由 kubelet 强制执行的节点可分配资源级别。
可选配置为：<code>none</code>、<code>pods</code>、<code>system-reserved</code> 和 <code>kube-reserved</code>。
在设置 <code>system-reserved</code> 和 <code>kube-reserved</code> 这两个值时，同时要求设置
<code>--system-reserved-cgroup</code> 和 <code>--kube-reserved-cgroup</code> 这两个参数。
如果设置为 <code>none</code>，则不需要设置其他参数。
<a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/">参考相关文档</a>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
事件记录的个数的突发峰值上限，在遵从 <code>--event-qps</code> 阈值约束的前提下
临时允许事件记录达到此数目。该数字必须大于等于 0。如果为 0，则使用默认突发值（100）。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
QPS 用于限制事件创建的速率。该数字必须大于等于 0。如果为 0，则使用默认 QPS 值（50）。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
触发 Pod 驱逐操作的一组硬性门限（例如：<code>memory.available&lt;1Gi</code>
（内存可用值小于 1G）设置。在 Linux 节点上，默认值还包括
<code>nodefs.inodesFree<5%</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--eviction-max-pod-grace-period int32</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
响应满足软性驱逐阈值（Soft Eviction Threshold）而终止 Pod 时使用的最长宽限期（以秒为单位）。
如果设置为负数，则遵循 Pod 的指定值。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--eviction-minimum-reclaim string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
当某资源压力过大时，kubelet 将执行 Pod 驱逐操作。
此参数设置软性驱逐操作需要回收的资源的最小数量（例如：<code>imagefs.available=2Gi</code>）。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubelet 在驱逐压力状况解除之前的最长等待时间。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--eviction-soft string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置一组驱逐阈值（例如：<code>memory.available&lt;1.5Gi</code>）。
如果在相应的宽限期内达到该阈值，则会触发 Pod 驱逐操作。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--eviction-soft-grace-period string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置一组驱逐宽限期（例如，<code>memory.available=1m30s</code>），对应于触发软性 Pod
驱逐操作之前软性驱逐阈值所需持续的时间长短。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--exit-on-lock-contention</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置为 true 表示当发生锁文件竞争时 kubelet 可以退出。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置为 <code>true</code> 表示在计算节点可分配资源数量时忽略硬性逐出阈值设置。
参考<a href="https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/">
相关文档</a>。
已弃用：将在 1.24 或更高版本中移除。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
[实验性特性] 卷挂载器（mounter）的可执行文件的路径。设置为空表示使用默认挂载器 <code>mount</code>。
已弃用：将在 1.24 或更高版本移除以支持 CSI。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置为 true 表示如果主机启用了交换分区，kubelet 将直接失败。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--feature-gates &lt;一个由 “key=true/false” 组成的对偶&gt;</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用于 alpha 实验性特性的特性开关组，每个开关以 key=value 形式表示。当前可用开关包括：</br>
APIListChunking=true|false (BETA - 默认值为 true)<br/>
APIPriorityAndFairness=true|false (BETA - 默认值为 true)<br/>
APIResponseCompression=true|false (BETA - 默认值为 true)<br/>
APISelfSubjectReview=true|false (BETA - 默认值为 true)<br/>
APIServerIdentity=true|false (BETA - 默认值为 true)<br/>
APIServerTracing=true|false (BETA - 默认值为 true)<br/>
AdmissionWebhookMatchConditions=true|false (ALPHA - 默认值为 false)<br/>
AggregatedDiscoveryEndpoint=true|false (BETA - 默认值为 true)<br/>
AllAlpha=true|false (ALPHA - 默认值为 false)<br/>
AllBeta=true|false (BETA - 默认值为 false)<br/>
AnyVolumeDataSource=true|false (BETA - 默认值为 true)<br/>
AppArmor=true|false (BETA - 默认值为 true)<br/>
CPUManagerPolicyAlphaOptions=true|false (ALPHA - 默认值为 false)<br/>
CPUManagerPolicyBetaOptions=true|false (BETA - 默认值为 true)<br/>
CPUManagerPolicyOptions=true|false (BETA - 默认值为 true)<br/>
CSIMigrationPortworx=true|false (BETA - 默认值为 false)<br/>
CSIMigrationRBD=true|false (ALPHA - 默认值为 false)<br/>
CSINodeExpandSecret=true|false (BETA - 默认值为 true)<br/>
CSIVolumeHealth=true|false (ALPHA - 默认值为 false)<br/>
CloudControllerManagerWebhook=true|false (ALPHA - 默认值为 false)<br/>
CloudDualStackNodeIPs=true|false (ALPHA - 默认值为 false)<br/>
ClusterTrustBundle=true|false (ALPHA - 默认值为 false)<br/>
ComponentSLIs=true|false (BETA - 默认值为 true)<br/>
ContainerCheckpoint=true|false (ALPHA - 默认值为 false)<br/>
ContextualLogging=true|false (ALPHA - 默认值为 false)<br/>
CrossNamespaceVolumeDataSource=true|false (ALPHA - 默认值为 false)<br/>
CustomCPUCFSQuotaPeriod=true|false (ALPHA - 默认值为 false)<br/>
CustomResourceValidationExpressions=true|false (BETA - 默认值为 true)<br/>
DisableCloudProviders=true|false (ALPHA - 默认值为 false)<br/>
DisableKubeletCloudCredentialProviders=true|false (ALPHA - 默认值为 false)<br/>
DynamicResourceAllocation=true|false (ALPHA - 默认值为 false)<br/>
ElasticIndexedJob=true|false (BETA - 默认值为 true)<br/>
EventedPLEG=true|false (BETA - 默认值为 false)<br/>
ExpandedDNSConfig=true|false (BETA - 默认值为 true)<br/>
ExperimentalHostUserNamespaceDefaulting=true|false (BETA - 默认值为 false)<br/>
GracefulNodeShutdown=true|false (BETA - 默认值为 true)<br/>
GracefulNodeShutdownBasedOnPodPriority=true|false (BETA - 默认值为 true)<br/>
HPAContainerMetrics=true|false (BETA - 默认值为 true)<br/>
HPAScaleToZero=true|false (ALPHA - 默认值为 false)<br/>
HonorPVReclaimPolicy=true|false (ALPHA - 默认值为 false)<br/>
IPTablesOwnershipCleanup=true|false (BETA - 默认值为 true)<br/>
InPlacePodVerticalScaling=true|false (ALPHA - 默认值为 false)<br/>
InTreePluginAWSUnregister=true|false (ALPHA - 默认值为 false)<br/>
InTreePluginAzureDiskUnregister=true|false (ALPHA - 默认值为 false)<br/>
InTreePluginAzureFileUnregister=true|false (ALPHA - 默认值为 false)<br/>
InTreePluginGCEUnregister=true|false (ALPHA - 默认值为 false)<br/>
InTreePluginOpenStackUnregister=true|false (ALPHA - 默认值为 false)<br/>
InTreePluginPortworxUnregister=true|false (ALPHA - 默认值为 false)<br/>
InTreePluginRBDUnregister=true|false (ALPHA - 默认值为 false)<br/>
InTreePluginvSphereUnregister=true|false (ALPHA - 默认值为 false)<br/>
JobPodFailurePolicy=true|false (BETA - 默认值为 true)<br/>
JobReadyPods=true|false (BETA - 默认值为 true)<br/>
KMSv2=true|false (BETA - 默认值为 true)<br/>
KubeletInUserNamespace=true|false (ALPHA - 默认值为 false)<br/>
KubeletPodResources=true|false (BETA - 默认值为 true)<br/>
KubeletPodResourcesDynamicResources=true|false (ALPHA - 默认值为 false)<br/>
KubeletPodResourcesGet=true|false (ALPHA - 默认值为 false)<br/>
KubeletPodResourcesGetAllocatable=true|false (BETA - 默认值为 true)<br/>
KubeletTracing=true|false (BETA - 默认值为 true)<br/>
LegacyServiceAccountTokenTracking=true|false (BETA - 默认值为 true)<br/>
LocalStorageCapacityIsolationFSQuotaMonitoring=true|false (ALPHA - 默认值为 false)<br/>
LogarithmicScaleDown=true|false (BETA - 默认值为 true)<br/>
LoggingAlphaOptions=true|false (ALPHA - 默认值为 false)<br/>
LoggingBetaOptions=true|false (BETA - 默认值为 true)<br/>
MatchLabelKeysInPodTopologySpread=true|false (BETA - 默认值为 true)<br/>
MaxUnavailableStatefulSet=true|false (ALPHA - 默认值为 false)<br/>
MemoryManager=true|false (BETA - 默认值为 true)<br/>
MemoryQoS=true|false (ALPHA - 默认值为 false)<br/>
MinDomainsInPodTopologySpread=true|false (BETA - 默认值为 true)<br/>
MinimizeIPTablesRestore=true|false (BETA - 默认值为 true)<br/>
MultiCIDRRangeAllocator=true|false (ALPHA - 默认值为 false)<br/>
MultiCIDRServiceAllocator=true|false (ALPHA - 默认值为 false)<br/>
NetworkPolicyStatus=true|false (ALPHA - 默认值为 false)<br/>
NewVolumeManagerReconstruction=true|false (BETA - 默认值为 true)<br/>
NodeInclusionPolicyInPodTopologySpread=true|false (BETA - 默认值为 true)<br/>
NodeLogQuery=true|false (ALPHA - 默认值为 false)<br/>
NodeOutOfServiceVolumeDetach=true|false (BETA - 默认值为 true)<br/>
NodeSwap=true|false (ALPHA - 默认值为 false)<br/>
OpenAPIEnums=true|false (BETA - 默认值为 true)<br/>
PDBUnhealthyPodEvictionPolicy=true|false (BETA - 默认值为 true)<br/>
PodAndContainerStatsFromCRI=true|false (ALPHA - 默认值为 false)<br/>
PodDeletionCost=true|false (BETA - 默认值为 true)<br/>
PodDisruptionConditions=true|false (BETA - 默认值为 true)<br/>
PodHasNetworkCondition=true|false (ALPHA - 默认值为 false)<br/>
PodSchedulingReadiness=true|false (BETA - 默认值为 true)<br/>
ProbeTerminationGracePeriod=true|false (BETA - 默认值为 true)<br/>
ProcMountType=true|false (ALPHA - 默认值为 false)<br/>
ProxyTerminatingEndpoints=true|false (BETA - 默认值为 true)<br/>
QOSReserved=true|false (ALPHA - 默认值为 false)<br/>
ReadWriteOncePod=true|false (BETA - 默认值为 true)<br/>
RecoverVolumeExpansionFailure=true|false (ALPHA - 默认值为 false)<br/>
RemainingItemCount=true|false (BETA - 默认值为 true)<br/>
RetroactiveDefaultStorageClass=true|false (BETA - 默认值为 true)<br/>
RotateKubeletServerCertificate=true|false (BETA - 默认值为 true)<br/>
SELinuxMountReadWriteOncePod=true|false (BETA - 默认值为 true)<br/>
SecurityContextDeny=true|false (ALPHA - 默认值为 false)<br/>
ServiceNodePortStaticSubrange=true|false (ALPHA - 默认值为 false)<br/>
SizeMemoryBackedVolumes=true|false (BETA - 默认值为 true)<br/>
StableLoadBalancerNodeSet=true|false (BETA - 默认值为 true)<br/>
StatefulSetAutoDeletePVC=true|false (BETA - 默认值为 true)<br/>
StatefulSetStartOrdinal=true|false (BETA - 默认值为 true)<br/>
StorageVersionAPI=true|false (ALPHA - 默认值为 false)<br/>
StorageVersionHash=true|false (BETA - 默认值为 true)<br/>
TopologyAwareHints=true|false (BETA - 默认值为 true)<br/>
TopologyManagerPolicyAlphaOptions=true|false (ALPHA - 默认值为 false)<br/>
TopologyManagerPolicyBetaOptions=true|false (BETA - 默认值为 false)<br/>
TopologyManagerPolicyOptions=true|false (ALPHA - 默认值为 false)<br/>
UserNamespacesStatelessPodsSupport=true|false (ALPHA - 默认值为 false)<br/>
ValidatingAdmissionPolicy=true|false (ALPHA - 默认值为 false)<br/>
VolumeCapacityPriority=true|false (ALPHA - 默认值为 false)<br/>
WatchList=true|false (ALPHA - 默认值为 false)<br/>
WinDSR=true|false (ALPHA - 默认值为 false)<br/>
WinOverlay=true|false (BETA - 默认值为 true)<br/>
WindowsHostNetwork=true|false (ALPHA - 默认值为 true)</p>
已弃用: 应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file">进一步了解</a>）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
检查配置文件中新数据的时间间隔。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置 kubelet 执行发夹模式（hairpin）网络地址转译的方式。
该模式允许后端端点对其自身服务的访问能够再次经由负载均衡转发回自身。
可选项包括 <code>promiscuous-bridge</code>、<code>hairpin-veth</code> 和 <code>none</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
healthz 服务器提供服务所使用的 IP 地址（设置为 <code>0.0.0.0</code> 或 <code>::</code> 表示监听所有接口和 IP 协议族。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
本地 healthz 端点使用的端口（设置为 0 表示禁用）。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubelet 操作的帮助命令
</td>
</tr>

<tr>
<td colspan="2">--hostname-override string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如果为非空，将使用此字符串而不是实际的主机名作为节点标识。如果设置了
<code>--cloud-provider</code>，则云驱动将确定节点的名称
（请查阅云服务商文档以确定是否以及如何使用主机名）。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
HTTP 服务以获取新数据的时间间隔。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--image-credential-provider-bin-dir string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
指向凭据提供组件可执行文件所在目录的路径。
</td>
</tr>

<tr>
<td colspan="2">--image-credential-provider-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
指向凭据提供插件配置文件所在目录的路径。
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
镜像垃圾回收上限。磁盘使用空间达到该百分比时，镜像垃圾回收将持续工作。
值必须在 [0，100] 范围内。要禁用镜像垃圾回收，请设置为 100。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
镜像垃圾回收下限。磁盘使用空间在达到该百分比之前，镜像垃圾回收操作不会运行。
值必须在 [0，100] 范围内，并且不得大于 <code>--image-gc-high-threshold</code>的值。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--image-service-endpoint string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
[实验性特性] 远程镜像服务的端点。若未设定则默认情况下使用 <code>--container-runtime-endpoint</code>
的值。目前支持的类型包括在 Linux 系统上的 UNIX 套接字端点和 Windows 系统上的 npipe 和 TCP 端点。
例如：<code>unix:///var/run/dockershim.sock</code>、<code>npipe:////./pipe/dockershim</code>。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
标记数据包将被丢弃的 fwmark 位设置。必须在 [0，31] 范围内。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
标记数据包将进行 SNAT 的 fwmark 空间位设置。必须在 [0，31] 范围内。
请将此参数与 <code>kube-proxy</code> 中的相应参数匹配。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--keep-terminated-pod-volumes</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置为 true 表示 Pod 终止后仍然保留之前挂载过的卷，常用于调试与卷有关的问题。
已弃用：将未来版本中移除。
</td>
</tr>

<tr>
<td colspan="2">--kernel-memcg-notification</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
若启用，则 kubelet 将与内核中的 memcg 通知机制集成，不再使用轮询的方式来判定
是否 Pod 达到内存驱逐阈值。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
每秒发送到 API 服务器 的突发请求数量上限。
该数字必须大于或等于 0。如果为 0，则使用默认的突发值（100）。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
发送到 apiserver 的请求的内容类型。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
与 apiserver 通信的每秒查询个数（QPS）。
此值必须 &gt;= 0。如果为 0，则使用默认 QPS（50）。
不包含事件和节点心跳 API，它们的速率限制是由一组不同的标志所控制。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubernetes 系统预留的资源配置，以一组 <code>&lt;资源名称&gt;=&lt;资源数量&gt;</code> 格式表示。
（例如：<code>cpu=200m,memory=500Mi,ephemeral-storage=1Gi,pid='100'</code>）。
当前支持 <code>cpu</code>、<code>memory</code> 和用于根文件系统的 <code>ephemeral-storage</code>。
请参阅<a href="https://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/">这里</a>获取更多信息。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
给出某个顶层 cgroup 绝对名称，该 cgroup 用于管理通过标志 <code>--kube-reserved</code>
为 kubernetes 组件所预留的计算资源。例如：<code>"/kube-reserved"</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubeconfig 配置文件的路径，指定如何连接到 API 服务器。
提供 <code>--kubeconfig</code> 将启用 API 服务器模式，而省略 <code>--kubeconfig</code> 将启用独立模式。
</td>
</tr>

<tr>
<td colspan="2">--kubelet-cgroups string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用于创建和运行 kubelet 的 cgroup 的绝对名称。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--local-storage-capacity-isolation&gt;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: <code>true</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如果此值为 true，将启用本地临时存储隔离。
否则，本地存储隔离功能特性将被禁用。
（已弃用：这个参数应该通过 Kubelet 的 <code>--config</code> 标志指定的配置文件来设置。
有关详细信息，请参阅 https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/）。
</td>
</tr>

<tr>
<td colspan="2">--lock-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
【警告：Alpha 特性】kubelet 用作锁文件的文件路径。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
两次日志刷新之间的最大秒数（默认值为 5s）。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
[Alpha 特性]在具有拆分输出流的 JSON 格式中，可以将信息消息缓冲一段时间以提高性能。
零字节的默认值禁用缓冲。大小可以指定为字节数（512）、1000 的倍数（1K）、1024 的倍数（2Ki） 或这些（3M、4G、5Mi、6Gi）的幂。
启用 <code>LoggingAlphaOptions</code> 特性门控来使用此功能。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--log-json-split-stream</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
[Alpha 特性]以 JSON 格式，将错误消息写入 stderr，将 info 消息写入 stdout。
启用 <code>LoggingAlphaOptions</code> 特性门控来使用此功能。
默认是将单个流写入标准输出。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置日志格式。允许的格式：<code>text</code>、<code>json</code>（由 <code>LoggingBetaOptions</code> 控制）。
（已弃用：此参数应通过 Kubelet 的 <code>--config</code> 标志指定的配置文件设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置为 true 表示 kubelet 将确保 <code>iptables</code> 规则在主机上存在。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--manifest-url string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用于访问要运行的其他 Pod 规范的 URL。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--manifest-url-header string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
取值为由 HTTP 头部组成的逗号分隔列表，在访问 <code>--manifest-url</code> 所给出的 URL 时使用。
名称相同的多个头部将按所列的顺序添加。该参数可以多次使用。例如：
<code>--manifest-url-header 'a:hello,b:again,c:world' --manifest-url-header 'b:beautiful'</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubelet 向 Pod 注入 Kubernetes 主控服务信息时使用的命名空间。
已弃用：此标志将在未来的版本中删除。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubelet 进程可以打开的最大文件数量。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
此 kubelet 能运行的 Pod 最大数量。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置全局可保留的已停止容器实例个数上限。
每个实例会占用一些磁盘空间。要禁用，可设置为负数。
已弃用：改用 <code>--eviction-hard</code> 或 <code>--eviction-soft</code>。
此标志将在未来的版本中删除。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
每个已停止容器可以保留的的最大实例数量。每个容器占用一些磁盘空间。
已弃用：改用 <code>--eviction-hard</code> 或 <code>--eviction-soft</code>。
此标志将在未来的版本中删除。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
内存管理器策略使用。可选值：<code>'None'</code>、<code>'Static'</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--minimum-container-ttl-duration duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
已结束的容器在被垃圾回收清理之前的最少存活时间。
例如：<code>'300ms'</code>、<code>'10s'</code> 或者 <code>'2h45m'</code>。
已弃用：请改用 <code>--eviction-hard</code> 或者 <code>--eviction-soft</code>。
此标志将在未来的版本中删除。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
已结束的容器在被垃圾回收清理之前的最少存活时间。
例如：<code>'300ms'</code>、<code>'10s'</code> 或者 <code>'2h45m'</code>。
已弃用：这个参数应该通过 Kubelet 的 <code>--config</code> 标志指定的配置文件来设置。
（<a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--node-ip string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
节点的 IP 地址（或逗号分隔的双栈 IP 地址）。
如果未设置，kubelet 将使用节点的默认 IPv4 地址（如果有）或默认 IPv6 地址（如果它没有 IPv4 地址）。
你可以传值 <code>'::'</code> 使其偏向于默认的 IPv6 地址而不是默认的 IPv4 地址。
</td>
</tr>

<tr>
<td colspan="2">--node-labels &lt;key=value pairs&gt;</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
【警告：Alpha 特性】kubelet 在集群中注册本节点时设置的标签。标签以
<code>key=value</code> 的格式表示，多个标签以逗号分隔。名字空间 <code>kubernetes.io</code>
中的标签必须以 <code>kubelet.kubernetes.io</code> 或 <code>node.kubernetes.io</code> 为前缀，
或者在以下明确允许范围内：
<code>beta.kubernetes.io/arch</code>, <code>beta.kubernetes.io/instance-type</code>,
<code>beta.kubernetes.io/os</code>, <code>failure-domain.beta.kubernetes.io/region</code>,
<code>failure-domain.beta.kubernetes.io/zone</code>, <code>kubernetes.io/arch</code>,
<code>kubernetes.io/hostname</code>, <code>kubernetes.io/os</code>,
<code>node.kubernetes.io/instance-type</code>, <code>topology.kubernetes.io/region</code>,
<code>topology.kubernetes.io/zone</code>。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在 <code>node.status.images</code> 中可以报告的最大镜像数量。如果指定为 -1，则不设上限。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
指定 kubelet 向主控节点汇报节点状态的时间间隔。注意：更改此常量时请务必谨慎，
它必须与节点控制器中的 <code>nodeMonitorGracePeriod</code> 一起使用。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubelet 进程的 oom-score-adj 参数值。有效范围为 <code>[-1000，1000]</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--pod-cidr string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用于给 Pod 分配 IP 地址的 CIDR 地址池，仅在独立运行模式下使用。
在集群模式下，CIDR 设置是从主服务器获取的。对于 IPv6，分配的 IP 的最大数量为 65536。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--pod-infra-container-image string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
默认值: <code>registry.k8s.io/pause:3.9
</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
所指定的镜像不会被镜像垃圾收集器删除。
CRI 实现有自己的配置来设置此镜像。
（已弃用：将在 1.27 中删除，镜像垃圾收集器将从 CRI 获取沙箱镜像信息。）
</td>
</tr>

<tr>
<td colspan="2">--pod-manifest-path string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置包含要运行的静态 Pod 的文件的路径，或单个静态 Pod 文件的路径。以点（<code>.</code>）
开头的文件将被忽略。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置每个 Pod 中的最大进程数目。如果为 -1，则 kubelet 使用节点可分配的 PID 容量作为默认值。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--pods-per-core int32</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubelet 在每个处理器核上可运行的 Pod 数量。此 kubelet 上的 Pod 总数不能超过
<code>--max-pods</code> 标志值。因此，如果此计算结果导致在 kubelet
上允许更多数量的 Pod，则使用 <code>--max-pods</code> 值。值为 0 表示不作限制。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubelet 服务监听的本机端口号。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--protect-kernel-defaults</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置 kubelet 的默认内核调整行为。如果已设置该参数，当任何内核可调参数与
kubelet 默认值不同时，kubelet 都会出错。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--provider-id string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置主机数据库（即，云驱动）中用来标识节点的唯一标识。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--qos-reserved string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
【警告：Alpha 特性】设置在指定的 QoS 级别预留的 Pod 资源请求，以一组
<code>"资源名称=百分比"</code> 的形式进行设置，例如 <code>memory=50%</code>。
当前仅支持内存（memory）。要求启用 <code>QOSReserved</code> 特性门控。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubelet 可以在没有身份验证/鉴权的情况下提供只读服务的端口（设置为 0 表示禁用）。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
向 API 服务器注册节点，如果未提供 <code>--kubeconfig</code>，此标志无关紧要，
因为 Kubelet 没有 API 服务器可注册。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
注册本节点为可调度的节点。当 <code>--register-node</code>标志为 false 时此设置无效。
已弃用：此参数将在未来的版本中删除。
</td>
</tr>

<tr>
<td colspan="2">--register-with-taints string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置本节点的污点标记，格式为 <code>&lt;key&gt;=&lt;value&gt;:&lt;effect&gt;</code>，
以逗号分隔。当 <code>--register-node</code> 为 false 时此标志无效。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置突发性镜像拉取的个数上限，在不超过 <code>--registration-qps</code> 设置值的前提下
暂时允许此参数所给的镜像拉取个数。仅在 <code>--registry-qps</code> 大于 0 时使用。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如此值大于 0，可用来限制镜像仓库的 QPS 上限。设置为 0，表示不受限制。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--reserved-cpus string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用逗号分隔的一组 CPU 或 CPU 范围列表，给出为系统和 Kubernetes 保留使用的 CPU。
此列表所给出的设置优先于通过 <code>--system-reserved</code> 和
<code>--kube-reskube-reserved</code> 所保留的 CPU 个数配置。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--reserved-memory string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
以逗号分隔的 NUMA 节点内存预留列表。（例如 <code>--reserved-memory 0:memory=1Gi,hugepages-1M=2Gi --reserved-memory 1:memory=2Gi</code>）。
每种内存类型的总和应该等于<code>--kube-reserved</code>、<code>--system-reserved</code>和<code>--eviction-threshold</之和 代码>。
<a href="https://kubernetes.io/docs/tasks/administer-cluster/memory-manager/#reserved-memory-flag">了解更多详细信息。</a>
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
名字解析服务的配置文件名，用作容器 DNS 解析配置的基础。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置用于管理 kubelet 文件的根目录（例如挂载卷的相关文件等）。
</td>
</tr>

<tr>
<td colspan="2">--rotate-certificates</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置当客户端证书即将过期时 kubelet 自动从
<code>kube-apiserver</code> 请求新的证书进行轮换。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--rotate-server-certificates</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
【警告：Beta 特性】当 kubelet 的服务证书即将过期时自动从 kube-apiserver 请求新的证书进行轮换。
要求启用 <code>RotateKubeletServerCertificate</code> 特性门控，以及对提交的
<code>CertificateSigningRequest</code> 对象进行批复（Approve）操作。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--runonce</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置为 <code>true</code> 表示从本地清单或远程 URL 创建完 Pod 后立即退出 kubelet 进程。
与 <code>--enable-server</code> 标志互斥。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--runtime-cgroups string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置用于创建和运行容器运行时的 cgroup 的绝对名称。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置除了长时间运行的请求（包括 <code>pull</code>、<code>logs</code>、<code>exec</code>
和 <code>attach</code> 等操作）之外的其他运行时请求的超时时间。
到达超时时间时，请求会被取消，抛出一个错误并会等待重试。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--seccomp-default string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
【警告：Beta 特性】启用 <code>RuntimeDefault</code> 作为所有工作负载的默认 seccomp 配置文件。<code>SeccompDefault</code> 特性门控必须启用以允许此标志，默认情况下禁用。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
逐一拉取镜像。建议 *不要* 在 docker 守护进程版本低于 1.9 或启用了 Aufs 存储后端的节点上
更改默认值。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置流连接在自动关闭之前可以空闲的最长时间。0 表示没有超时限制。
例如：<code>5m</code>。
注意：与 kubelet 服务器的所有连接最长持续时间为 4 小时。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在运行中的容器与其配置之间执行同步操作的最长时间间隔。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--system-cgroups string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
此标志值为一个 cgroup 的绝对名称，用于所有尚未放置在根目录下某 cgroup 内的非内核进程。
空值表示不指定 cgroup。回滚该参数需要重启机器。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
系统预留的资源配置，以一组 <code>资源名称=资源数量</code> 的格式表示，
（例如：<code>cpu=200m,memory=500Mi,ephemeral-storage=1Gi,pid='100'</code>）。
目前仅支持 <code>cpu</code> 和 <code>memory</code> 的设置。
更多细节可参考
<a href="http://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/">相关文档</a>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
此标志给出一个顶层 cgroup 绝对名称，该 cgroup 用于管理非 kubernetes 组件，
这些组件的计算资源通过 <code>--system-reserved</code> 标志进行预留。
例如 <code>"/system-reserved"</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--tls-cert-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 x509 证书的文件路径，用于 HTTPS 认证。
如果有中间证书，则中间证书要串接在在服务器证书之后。
如果未提供 <code>--tls-cert-file</code> 和 <code>--tls-private-key-file</code>，
kubelet 会为公开地址生成自签名证书和密钥，并将其保存到通过
<code>--cert-dir</code> 指定的目录中。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--tls-cipher-suites string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
服务器端加密算法列表，以逗号分隔。如果不设置，则使用 Go 语言加密包的默认算法列表。<br/>
首选算法：
<code>TLS_AES_128_GCM_SHA256</code>, <code>TLS_AES_256_GCM_SHA384</code>, <code>TLS_CHACHA20_POLY1305_SHA256</code>, <code>TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA</code>, <code>TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256</code>, <code>TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA</code>, <code>TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384</code>, <code>TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305</code>, <code>TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256</code>, <code>TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA</code>, <code>TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256</code>, <code>TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA</code>, <code>TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384</code>, <code>TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305</code>, <code>TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256</code>, <code>TLS_RSA_WITH_AES_128_CBC_SHA</code>, <code>TLS_RSA_WITH_AES_128_GCM_SHA256</code>, <code>TLS_RSA_WITH_AES_256_CBC_SHA</code>, <code>TLS_RSA_WITH_AES_256_GCM_SHA384</code><br/>
不安全算法：
<code>TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256</code>, <code>TLS_ECDHE_ECDSA_WITH_RC4_128_SHA</code>, <code>TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA</code>, <code>TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256</code>, <code>TLS_ECDHE_RSA_WITH_RC4_128_SHA</code>, <code>TLS_RSA_WITH_3DES_EDE_CBC_SHA</code>, <code>TLS_RSA_WITH_AES_128_CBC_SHA256</code>, <code>TLS_RSA_WITH_RC4_128_SHA</code>.<br/>
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--tls-min-version string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置支持的最小 TLS 版本号，可选的版本号包括：<code>VersionTLS10</code>、
<code>VersionTLS11</code>、<code>VersionTLS12</code> 和 <code>VersionTLS13</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--tls-private-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含与 <code>--tls-cert-file</code> 对应的 x509 私钥文件路径。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>


<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
要使用的拓扑管理器策略，用于微调它们的行为。
可能的取值有：<code>'none'</code>、<code>'best-effort'</code>、<code>'restricted'</code>、<code>'single-numa-node'</code>。
（已弃用：此参数应通过 Kubelet 的 <code>--config</code>
标志指定的配置文件设置。请参阅
<a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">--topology-manager-policy-options string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置拓扑管理策略（Topology Manager policy）。可选值包括：<code>none</code>、
<code>best-effort</code>、<code>restricted</code> 和 <code>single-numa-node</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
拓扑提示信息使用范围。拓扑管理器从提示提供者（Hints Providers）处收集提示信息，
并将其应用到所定义的范围以确保 Pod 准入。
可选值包括：<code>container</code>（默认）、<code>pod</code>。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
<td colspan="2">-v, --v Level</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置 kubelet 日志级别详细程度的数值。
</td>
</tr>

<tr>
<td colspan="2">--version version[=true]</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
打印 kubelet 版本信息并退出。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
以逗号分隔的 <code>pattern=N</code> 设置列表，用于文件过滤的日志记录
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用来搜索第三方存储卷插件的目录。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
指定 kubelet 计算和缓存所有 Pod 和卷的磁盘用量总值的时间间隔。要禁用磁盘用量计算，
可设置为 0。
（已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
请参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/">kubelet-config-file</a> 了解更多信息。）
</td>
</tr>
</tbody>
</table>
