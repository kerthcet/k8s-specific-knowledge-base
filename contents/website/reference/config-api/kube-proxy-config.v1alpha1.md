---
title: kube-proxy 配置 (v1alpha1)
content_type: tool-reference
package: kubeproxy.config.k8s.io/v1alpha1
---


## 资源类型    {#resource-types}

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

## `KubeProxyConfiguration`     {#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration}

KubeProxyConfiguration 包含用来配置 Kubernetes 代理服务器的所有配置信息。

<table class="table">
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubeproxy.config.k8s.io/v1alpha1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>KubeProxyConfiguration</code></td></tr>
  
<code>map[string]bool</code>
</td>
<td>
   <p><code>featureGates</code> 字段是一个功能特性名称到布尔值的映射表，
   用来启用或者禁用测试性质的功能特性。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>bindAddress</code> 字段是代理服务器提供服务时所用 IP 地址（设置为 0.0.0.0
时意味着在所有网络接口上提供服务）。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>healthzBindAddress</code> 字段是健康状态检查服务器提供服务时所使用的 IP 地址和端口，
   默认设置为 '0.0.0.0:10256'。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>metricsBindAddress</code> 字段是指标服务器提供服务时所使用的 IP 地址和端口，
   默认设置为 '127.0.0.1:10249'（设置为 0.0.0.0 意味着在所有接口上提供服务）。</p>
</td>
</tr>
<code>bool</code>
</td>
<td>
   <p><code>bindAddressHardFail</code> 字段设置为 true 时，
   kube-proxy 将无法绑定到某端口这类问题视为致命错误并直接退出。</p>
</td>
</tr>
<code>bool</code>
</td>
<td>
   <p><code>enableProfiling</code> 字段通过 '/debug/pprof' 处理程序在 Web 界面上启用性能分析。
   性能分析处理程序将由指标服务器执行。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>clusterCIDR</code> 字段是集群中 Pod 所使用的 CIDR 范围。
   这一地址范围用于对来自集群外的请求流量进行桥接。
   如果未设置，则 kube-proxy 不会对非集群内部的流量做桥接。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>hostnameOverride</code> 字段非空时，
   所给的字符串（而不是实际的主机名）将被用作 kube-proxy 的标识。</p>
</td>
</tr>
<a href="#ClientConnectionConfiguration"><code>ClientConnectionConfiguration</code></a>
</td>
<td>
   <p><code>clientConnection</code> 字段给出代理服务器与 API
   服务器通信时要使用的 kubeconfig 文件和客户端链接设置。</p>
</td>
</tr>
<a href="#kubeproxy-config-k8s-io-v1alpha1-KubeProxyIPTablesConfiguration"><code>KubeProxyIPTablesConfiguration</code></a>
</td>
<td>
   <p><code>iptables</code> 字段字段包含与 iptables 相关的配置选项。</p>
</td>
</tr>
<a href="#kubeproxy-config-k8s-io-v1alpha1-KubeProxyIPVSConfiguration"><code>KubeProxyIPVSConfiguration</code></a>
</td>
<td>
   <p><code>ipvs</code> 字段中包含与 ipvs 相关的配置选项。</p>
</td>
</tr>
<code>int32</code>
</td>
<td>
   <p><code>oomScoreAdj</code> 字段是为 kube-proxy 进程所设置的 oom-score-adj 值。
   此设置值必须介于 [-1000, 1000] 范围内。</p>
</td>
</tr>
<a href="#kubeproxy-config-k8s-io-v1alpha1-ProxyMode"><code>ProxyMode</code></a>
</td>
<td>
   <p><code>mode</code> 字段用来设置将使用的代理模式。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>portRange</code> 字段是主机端口的范围，形式为 ‘beginPort-endPort’（包含边界），
   用来设置代理服务所使用的端口。如果未指定（即 ‘0-0’），则代理服务会随机选择端口号。</p>
</td>
</tr>
<a href="#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConntrackConfiguration"><code>KubeProxyConntrackConfiguration</code></a>
</td>
<td>
   <p><code>conntrack</code> 字段包含与 conntrack 相关的配置选项。</p>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>configSyncPeriod</code> 字段是从 API 服务器刷新配置的频率。此值必须大于 0。</p>
</td>
</tr>
<code>[]string</code>
</td>
<td>
   <p><code>nodePortAddresses</code> 字段是 kube-proxy 进程的
   <code>--nodeport-addresses</code> 命令行参数设置。
   此值必须是合法的 IP 段。所给的 IP 段会作为参数来选择 NodePort 类型服务所使用的接口。
   如果有人希望将本地主机（Localhost）上的服务暴露给本地访问，
   同时暴露在某些其他网络接口上以实现某种目标，可以使用 IP 段的列表。
   如果此值被设置为 &quot;127.0.0.0/8&quot;，则 kube-proxy 将仅为 NodePort
   服务选择本地回路（loopback）接口。
   如果此值被设置为非零的 IP 段，则 kube-proxy 会对 IP 作过滤，仅使用适用于当前节点的 IP 地址。
   空的字符串列表意味着选择所有网络接口。</p>
</td>
</tr>
<a href="#kubeproxy-config-k8s-io-v1alpha1-KubeProxyWinkernelConfiguration"><code>KubeProxyWinkernelConfiguration</code></a>
</td>
<td>
   <p><code>winkernel</code> 字段包含与 winkernel 相关的配置选项。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>showHiddenMetricsForVersion</code> 字段给出的是一个 Kubernetes 版本号字符串，
   用来设置你希望显示隐藏指标的版本。</p>
</td>
</tr>
<a href="#kubeproxy-config-k8s-io-v1alpha1-LocalMode"><code>LocalMode</code></a>
</td>
<td>
   <p><code>detectLocalMode</code> 字段用来确定检测本地流量的方式，默认为 LocalModeClusterCIDR。</p>
</td>
</tr>
<a href="#kubeproxy-config-k8s-io-v1alpha1-DetectLocalConfiguration"><code>DetectLocalConfiguration</code></a>
</td>
<td>
   <p><code>detectLocal</code> 字段包含与 DetectLocalMode 相关的可选配置设置。</p>
</td>
</tr>
</tbody>
</table>

## `DetectLocalConfiguration`     {#kubeproxy-config-k8s-io-v1alpha1-DetectLocalConfiguration}

**出现在：**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

DetectLocalConfiguration 包含与 DetectLocalMode 选项相关的可选设置。

<table class="table">
<tbody>

<code>string</code>
</td>
<td>
   <p><code>bridgeInterface</code> 字段是一个表示单个桥接接口名称的字符串参数。
   Kube-proxy 将来自这个给定桥接接口的流量视为本地流量。
   如果 DetectLocalMode 设置为 LocalModeBridgeInterface，则应设置该参数。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>interfaceNamePrefix</code> 字段是一个表示单个接口前缀名称的字符串参数。
   Kube-proxy 将来自一个或多个与给定前缀匹配的接口流量视为本地流量。
   如果 DetectLocalMode 设置为 LocalModeInterfaceNamePrefix，则应设置该参数。</p>
</td>
</tr>
</tbody>
</table>

## `KubeProxyConntrackConfiguration`     {#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConntrackConfiguration}
    
**出现在：**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

KubeProxyConntrackConfiguration 包含为 Kubernetes 代理服务器提供的 conntrack 设置。

<table class="table">
<tbody>
  
<code>int32</code>
</td>
<td>
   <p><code>maxPerCore</code> 字段是每个 CPU 核所跟踪的 NAT 链接个数上限
   （0 意味着保留当前上限限制并忽略 min 字段设置值）。</p>
</td>
</tr>
<code>int32</code>
</td>
<td>
   <p><code>min</code> 字段给出要分配的链接跟踪记录个数下限。
   设置此值时会忽略 maxPerCore 的值（将 maxPerCore 设置为 0 时不会调整上限值）。</p>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>tcpEstablishedTimeout</code> 字段给出空闲 TCP 连接的保留时间（例如，'2s'）。
   此值必须大于 0。</p>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>tcpCloseWaitTimeout</code> 字段用来设置空闲的、处于 CLOSE_WAIT 状态的 conntrack 条目
   保留在 conntrack 表中的时间长度（例如，'60s'）。
   此设置值必须大于 0。</p>
</td>
</tr>
</tbody>
</table>

## `KubeProxyIPTablesConfiguration`     {#kubeproxy-config-k8s-io-v1alpha1-KubeProxyIPTablesConfiguration}
    
**出现在：**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

KubeProxyIPTablesConfiguration 包含用于 Kubernetes 代理服务器的、与 iptables 相关的配置细节。

<table class="table">
<tbody>

<code>int32</code>
</td>
<td>
   <p><code>masqueradeBit</code> 字段是 iptables fwmark 空间中的具体一位，
   用来在纯 iptables 代理模式下设置 SNAT。此值必须介于 [0, 31]（含边界值）。</p>
</td>
</tr>
<code>bool</code>
</td>
<td>
   <p><code>masqueradeAll</code> 字段用来通知 kube-proxy
   在使用纯 iptables 代理模式时对所有流量执行 SNAT 操作。</p>
</td>
</tr>
<code>bool</code>
</td>
<td>
   <p>localhostNodePorts 告知 kube-proxy 允许通过 localhost 访问服务 NodePorts（仅 iptables 模式）</p>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>syncPeriod</code> 字段给出 iptables
   规则的刷新周期（例如，'5s'、'1m'、'2h22m'）。此值必须大于 0。</p>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>minSyncPeriod</code> 字段给出 iptables
   规则被刷新的最小周期（例如，'5s'、'1m'、'2h22m'）。</p>
</td>
</tr>
</tbody>
</table>

## `KubeProxyIPVSConfiguration`     {#kubeproxy-config-k8s-io-v1alpha1-KubeProxyIPVSConfiguration}
    
**出现在：**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

KubeProxyIPVSConfiguration 包含用于 Kubernetes 代理服务器的、与 ipvs 相关的配置细节。

<table class="table">
<tbody>
 
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>syncPeriod</code> 字段给出 ipvs 规则的刷新周期（例如，'5s'、'1m'、'2h22m'）。
   此值必须大于 0。</p>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>minSyncPeriod</code> 字段给出 ipvs 规则被刷新的最小周期（例如，'5s'、'1m'、'2h22m'）。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p>IPVS 调度器。</p>
</td>
</tr>
<code>[]string</code>
</td>
<td>
   <p><code>excludeCIDRs</code> 字段取值为一个 CIDR 列表，ipvs 代理程序在清理 IPVS 服务时不应触碰这些 IP 地址。</p>
</td>
</tr>
<code>bool</code>
</td>
<td>
   <p><code>strictARP</code> 字段用来配置 arp_ignore 和 arp_announce，以避免（错误地）响应来自 kube-ipvs0 接口的
   ARP 查询请求。</p>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>tcpTimeout</code> 字段是用于设置空闲 IPVS TCP 会话的超时值。
   默认值为 0，意味着使用系统上当前的超时值设置。</p>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>tcpFinTimeout</code> 字段用来设置 IPVS TCP 会话在收到 FIN 之后的超时值。
   默认值为 0，意味着使用系统上当前的超时值设置。</p>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>udpTimeout</code> 字段用来设置 IPVS UDP 包的超时值。
   默认值为 0，意味着使用系统上当前的超时值设置。</p>
</td>
</tr>
</tbody>
</table>

## `KubeProxyWinkernelConfiguration`     {#kubeproxy-config-k8s-io-v1alpha1-KubeProxyWinkernelConfiguration}
    
**出现在：**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

KubeProxyWinkernelConfiguration 包含 Kubernetes 代理服务器的 Windows/HNS 设置。

<table class="table">
<tbody>

<code>string</code>
</td>
<td>
   <p><code>networkName</code> 字段是 kube-proxy 用来创建端点和策略的网络名称。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>sourceVip</code> 字段是执行负载均衡时进行 NAT 转换所使用的源端 VIP 端点 IP 地址。</p>
</td>
</tr>
<code>bool</code>
</td>
<td>
   <p><code>enableDSR</code> 字段通知 kube-proxy 是否使用 DSR 来创建 HNS 策略。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>rootHnsEndpointName</code>
   字段是附加到用于根网络命名空间二层桥接的 hnsendpoint 的名称。</p>
</td>
</tr>
<code>bool</code>
</td>
<td>
   <p><code>forwardHealthCheckVip</code>
   字段为 Windows 上的健康检查端口转发服务 VIP。</p>
</td>
</tr>
</tbody>
</table>

## `LocalMode`     {#kubeproxy-config-k8s-io-v1alpha1-LocalMode}

（<code>string</code> 类型的别名）

**出现在：**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

LocalMode 代表的是对节点上本地流量进行检测的模式。

## `ProxyMode`     {#kubeproxy-config-k8s-io-v1alpha1-ProxyMode}


（<code>string</code> 类型的别名）

**出现在：**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)

<p>ProxyMode 表示的是 Kubernetes 代理服务器所使用的模式。</p>

<p>目前 Linux 平台上有两种可用的代理模式：'iptables' 和 'ipvs'。
在 Windows 平台上可用的一种代理模式是：'kernelspace'。</p>

<p>如果代理模式未被指定，将使用最佳可用的代理模式（目前在 Linux 上是 <code>iptables</code>，在 Windows 上是 <code>kernelspace</code>）。
如果不能使用选定的代理模式（由于缺少内核支持、缺少用户空间组件等），则 kube-proxy 将出错并退出。</p>

## `ClientConnectionConfiguration`     {#ClientConnectionConfiguration}
    
**出现在：**

- [KubeProxyConfiguration](#kubeproxy-config-k8s-io-v1alpha1-KubeProxyConfiguration)


- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerConfiguration)

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1beta3-KubeSchedulerConfiguration)

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1-KubeSchedulerConfiguration)

- [GenericControllerManagerConfiguration](#controllermanager-config-k8s-io-v1alpha1-GenericControllerManagerConfiguration)

ClientConnectionConfiguration 包含构造客户端所需要的细节信息。

<table class="table">
<tbody>

<code>string</code>
</td>
<td>
   <p><code>kubeconfig</code> 字段是指向一个 KubeConfig 文件的路径。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>acceptContentTypes</code> 字段定义客户端在连接到服务器时所发送的 Accept 头部字段。
   此设置值会覆盖默认配置 'application/json'。
   此字段会控制某特定客户端与指定服务器的所有链接。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>contentType</code> 字段是从此客户端向服务器发送数据时使用的内容类型（Content Type）。</p>
</td>
</tr>
<code>float32</code>
</td>
<td>
   <p><code>qps</code> 字段控制此连接上每秒钟可以发送的查询请求个数。</p>
</td>
</tr>
<code>int32</code>
</td>
<td>
   <p><code>burst</code> 字段允许客户端超出其速率限制时可以临时累积的额外查询个数。</p>
</td>
</tr>
</tbody>
</table>

## `DebuggingConfiguration`     {#DebuggingConfiguration}

**出现在：**

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerConfiguration)

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1beta3-KubeSchedulerConfiguration)

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1-KubeSchedulerConfiguration)

- [GenericControllerManagerConfiguration](#controllermanager-config-k8s-io-v1alpha1-GenericControllerManagerConfiguration)

DebuggingConfiguration 包含调试相关功能的配置。

<table class="table">
<tbody>

<tr><td><code>enableProfiling</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   <p><code>enableProfiling</code> 字段通过位于 <code>host:port/debug/pprof/</code>
   的 Web 接口启用性能分析。</p>
</td>
</tr>
<tr><td><code>enableContentionProfiling</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   <p><code>enableContentionProfiling</code> 字段在 <code>enableProfiling</code>
   为 true 时启用阻塞分析。</p>
</td>
</tr>
</tbody>
</table>


## `LeaderElectionConfiguration`     {#LeaderElectionConfiguration}

**出现在：**

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerConfiguration)

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1beta3-KubeSchedulerConfiguration)

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1-KubeSchedulerConfiguration)

- [GenericControllerManagerConfiguration](#controllermanager-config-k8s-io-v1alpha1-GenericControllerManagerConfiguration)

LeaderElectionConfiguration 为能够支持领导者选举的组件定义其领导者选举客户端的配置。

<table class="table">
<tbody>

<code>bool</code>
</td>
<td>
   <p>
   <code>leaderElect</code> 字段允许领导者选举客户端在进入主循环执行之前先获得领导者角色。
   运行多副本组件时启用此功能有助于提高可用性。
   </p>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p>
   <code>leaseDuration</code> 字段是非领导角色候选者在观察到需要领导席位更新时要等待的时间；
   只有经过所设置时长才可以尝试去获得一个仍处于领导状态但需要被刷新的席位。
   这里的设置值本质上意味着某个领导者在被另一个候选者替换掉之前可以停止运行的最长时长。
   只有当启用了领导者选举时此字段有意义。
   </p>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p>
   <code>renewDeadline</code> 字段设置的是当前领导者在停止扮演领导角色之前需要刷新领导状态的时间间隔。
   此值必须小于或等于租约期限的长度。只有到启用了领导者选举时此字段才有意义。
   </p>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p>
   <code>retryPeriod</code> 字段是客户端在连续两次尝试获得或者刷新领导状态之间需要等待的时长。
   只有当启用了领导者选举时此字段才有意义。
   </p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>resourceLock</code> 字段给出在领导者选举期间要作为锁来使用的资源对象类型。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>resourceName</code> 字段给出在领导者选举期间要作为锁来使用的资源对象名称。</p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p><code>resourceNamespace</code> 字段给出在领导者选举期间要作为锁来使用的资源对象所在名字空间。</p>
</td>
</tr>
</tbody>
</table>