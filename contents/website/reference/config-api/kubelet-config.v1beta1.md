---
title: Kubelet 配置 (v1beta1)
content_type: tool-reference
package: kubelet.config.k8s.io/v1beta1
---


## 资源类型

- [CredentialProviderConfig](#kubelet-config-k8s-io-v1beta1-CredentialProviderConfig)
- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)
- [SerializedNodeConfigSource](#kubelet-config-k8s-io-v1beta1-SerializedNodeConfigSource)

## `CredentialProviderConfig`     {#kubelet-config-k8s-io-v1beta1-CredentialProviderConfig}

CredentialProviderConfig 包含有关每个 exec 凭据提供者的配置信息。
Kubelet 从磁盘上读取这些配置信息，并根据 CredentialProvider 类型启用各个提供者。

<table class="table">
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubelet.config.k8s.io/v1beta1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>CredentialProviderConfig</code></td></tr>
    
  
<a href="#kubelet-config-k8s-io-v1beta1-CredentialProvider"><code>[]CredentialProvider</code></a>
</td>
<td>
   <p>
   <code>providers</code> 是一组凭据提供者插件，这些插件会被 kubelet 启用。
   多个提供者可以匹配到同一镜像上，这时，来自所有提供者的凭据信息都会返回给 kubelet。
   如果针对同一镜像调用了多个提供者，则结果会被组合起来。如果提供者返回的认证主键有重复，
   列表中先出现的提供者所返回的值将被使用。
   </p>
</td>
</tr>
</tbody>
</table>

## `KubeletConfiguration`     {#kubelet-config-k8s-io-v1beta1-KubeletConfiguration}

KubeletConfiguration 中包含 Kubelet 的配置。

<table class="table">
<tbody>

<tr><td><code>apiVersion</code><br/>string</td><td><code>kubelet.config.k8s.io/v1beta1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>KubeletConfiguration</code></td></tr>
<tr><td><code>enableServer</code> <B>[必需]</B><br/>
<code>bool</code>
</td>
<td>
  <p><code>enableServer</code> 会启用 kubelet 的安全服务器。</p>
  <p>注意：kubelet 的不安全端口由 <code>readOnlyPort</code> 选项控制。</p>
  <p>默认值：<code>true</code></p>
</td>
</tr>

<tr><td><code>staticPodPath</code><br/>
<code>string</code>
</td>
<td>
  <p><code>staticPodPath</code> 是指向要运行的本地（静态）Pod 的目录，
或者指向某个静态 Pod 文件的路径。</p>
  <p>默认值：&quot;&quot;</p>
</td>
</tr>

<tr><td><code>syncFrequency</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
  <p><code>syncFrequency</code> 是对运行中的容器和配置进行同步的最长周期。</p>
  <p>默认值：&quot;1m&quot;</p>
</td>
</tr>

<tr><td><code>fileCheckFrequency</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
  <p><code>fileCheckFrequency</code> 是对配置文件中新数据进行检查的时间间隔值。</p>
  <p>默认值：&quot;20s&quot;</p>
</td>
</tr>

<tr><td><code>httpCheckFrequency</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
  <p><code>httpCheckFrequency</code> 是对 HTTP 服务器上新数据进行检查的时间间隔值。</p>
  <p>默认值：&quot;20s&quot;</p>
</td>
</tr>

<tr><td><code>staticPodURL</code><br/>
<code>string</code>
</td>
<td>
  <p><code>staticPodURL</code> 是访问要运行的静态 Pod 的 URL 地址。
  <p>默认值：&quot;&quot;</p>
</td>
</tr>

<tr><td><code>staticPodURLHeader</code><br/>
<code>map[string][]string</code>
</td>
<td>
   <p><code>staticPodURLHeader</code>是一个由字符串组成的映射表，其中包含的 HTTP
头部信息用于访问<code>podURL</code>。</p>
  <p>默认值：nil</p>
</td>
</tr>

<tr><td><code>address</code><br/>
<code>string</code>
</td>
<td>
   <p><code>address</code> 是 kubelet 提供服务所用的 IP 地址（设置为 0.0.0.0
使用所有网络接口提供服务）。</p>
  <p>默认值：&quot;0.0.0.0&quot;</p>
</td>
</tr>

<tr><td><code>port</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>port</code> 是 kubelet 用来提供服务所使用的端口号。
这一端口号必须介于 1 到 65535 之间，包含 1 和 65535。</p>
  <p>默认值：10250</p>
</td>
</tr>

<tr><td><code>readOnlyPort</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>readOnlyPort</code> 是 kubelet 用来提供服务所使用的只读端口号。
此端口上的服务不支持身份认证或鉴权。这一端口号必须介于 1 到 65535 之间，
包含 1 和 65535。将此字段设置为 0 会禁用只读服务。</p>
   <p>默认值：0（禁用）</p>
</td>
</tr>

<tr><td><code>tlsCertFile</code><br/>
<code>string</code>
</td>
<td>
  <p><code>tlsCertFile</code>是包含 HTTPS 所需要的 x509 证书的文件
（如果有 CA 证书，会串接到服务器证书之后）。如果<code>tlsCertFile</code>
和<code>tlsPrivateKeyFile</code>都没有设置，则系统会为节点的公开地址生成自签名的证书和私钥，
并将其保存到 kubelet <code>--cert-dir</code>参数所指定的目录下。</p>
  <p>默认值：&quot;&quot;</p>
</td>
</tr>

<tr><td><code>tlsPrivateKeyFile</code><br/>
<code>string</code>
</td>
<td>
   <p><code>tlsPrivateKeyFile</code>是一个包含与<code>tlsCertFile</code>
证书匹配的 X509 私钥的文件。</p>
  <p>默认值：&quot;&quot;</p>
</td>
</tr>

<tr><td><code>tlsCipherSuites</code><br/>
<code>[]string</code>
</td>
<td>
   <p><code>tlsCipherSuites</code>是一个字符串列表，其中包含服务器所接受的加密包名称。
列表中的每个值来自于<code>tls</code>包中定义的常数（https://golang.org/pkg/crypto/tls/#pkg-constants）。</p>
  <p>默认值：nil</p>
</td>
</tr>

<tr><td><code>tlsMinVersion</code><br/>
<code>string</code>
</td>
<td>
   <p><code>tlsMinVersion</code>给出所支持的最小 TLS 版本。
字段取值来自于<code>tls</code>包中的常数定义（https://golang.org/pkg/crypto/tls/#pkg-constants）。</p>
  <p>默认值：&quot;&quot;</p>
</td>
</tr>

<tr><td><code>rotateCertificates</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>rotateCertificates</code>用来启用客户端证书轮换。kubelet 会调用
<code>certificates.k8s.io</code> API 来请求新的证书。需要有一个批复人批准证书签名请求。</p>
  <p>默认值：false</code>
</td>
</tr>

<tr><td><code>serverTLSBootstrap</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>serverTLSBootstrap</code>用来启用服务器证书引导。系统不再使用自签名的服务证书，
kubelet 会调用<code>certificates.k8s.io</code> API 来请求证书。
需要有一个批复人来批准证书签名请求（CSR）。
设置此字段时，<code>RotateKubeletServerCertificate</code>特性必须被启用。</p>
  <p>默认值：false</p>
</td>
</tr>

<tr><td><code>authentication</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletAuthentication"><code>KubeletAuthentication</code></a>
</td>
<td>
   <p><code>authorization</code>设置发送给 kubelet 服务器的请求是如何进行身份认证的。</p>
   <p>默认值：</p>
<p><code><pre>
anonymous:
  enabled: false
webhook:
  enabled: true
cacheTTL: &quot;2m&quot;
</pre></code></p>
</td>
</tr>

<tr><td><code>authorization</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletAuthorization"><code>KubeletAuthorization</code></a>
</td>
<td>
   <p><code>authorization</code>设置发送给 kubelet 服务器的请求是如何进行鉴权的。</p>
  <p>默认值：</p>
  <pre><code>
  mode: Webhook
  webhook:
    cacheAuthorizedTTL: &quot;5m&quot;
    cacheUnauthorizedTTL: &quot;30s&quot;
  </code></pre>
</td>
</tr>

<tr><td><code>registryPullQPS</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>registryPullQPS</code>是每秒钟可以执行的镜像仓库拉取操作限值。
此值必须不能为负数。将其设置为 0 表示没有限值。</p>
  <p>默认值：5</code>
</td>
</tr>

<tr><td><code>registryBurst</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>registryBurst</code>是突发性镜像拉取的上限值，允许镜像拉取临时上升到所指定数量，
不过仍然不超过<code>registryPullQPS</code>所设置的约束。此值必须是非负值。
只有<code>registryPullQPS</code>参数值大于 0 时才会使用此设置。</p>
  <p>默认值：10</p>
</td>
</tr>

<tr><td><code>eventRecordQPS</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>eventRecordQPS</code>设置每秒钟可创建的事件个数上限。如果此值为 0，
则表示没有限制。此值不能设置为负数。</p>
  <p>默认值：50</p>
</td>
</tr>

<tr><td><code>eventBurst</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>eventBurst</code>是突发性事件创建的上限值，允许事件创建临时上升到所指定数量，
不过仍然不超过<code>eventRecordQPS</code>所设置的约束。此值必须是非负值，
且只有<code>eventRecordQPS</code> &gt; 0 时才会使用此设置。</p>
  <p>默认值：100</p>
</td>
</tr>

<tr><td><code>enableDebuggingHandlers</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>enableDebuggingHandlers</code>启用服务器上用来访问日志、
在本地运行容器和命令的端点，包括<code>exec</code>、<code>attach</code>、
<code>logs</code>和<code>portforward</code>等功能。</p>
  <p>默认值：true</p>
</td>
</tr>

<tr><td><code>enableContentionProfiling</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>enableContentionProfiling</code>用于启用阻塞性能分析，
仅用于<code>enableDebuggingHandlers</code>为<code>true</code>的场合。</p>
  <p>默认值：false</code>
</td>
</tr>

<tr><td><code>healthzPort</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>healthzPort</code>是本地主机上提供<code>healthz</code>端点的端口
（设置值为 0 时表示禁止）。合法值介于 1 和 65535 之间。</p>
  <p>默认值：10248</p>
</td>
</tr>

<tr><td><code>healthzBindAddress</code><br/>
<code>string</code>
</td>
<td>
   <p><code>healthzBindAddress<code>是<code>healthz</code>服务器用来提供服务的 IP 地址。</p>
  <p>默认值：&quot;127.0.0.1&quot;</p>
</td>
</tr>

<tr><td><code>oomScoreAdj</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>oomScoreAdj</code> 是为 kubelet 进程设置的<code>oom-score-adj</code>值。
所设置的取值要在 [-1000, 1000] 范围之内。</p>
   <p>默认值：-999</p>
</td>
</tr>

<tr><td><code>clusterDomain</code><br/>
<code>string</code>
</td>
<td>
   <p><code>clusterDomain</code>是集群的 DNS 域名。如果设置了此字段，kubelet
会配置所有容器，使之在搜索主机的搜索域的同时也搜索这里指定的 DNS 域。</p>
   <p>默认值：&quot;&quot;</p>
</td>
</tr>

<tr><td><code>clusterDNS</code><br/>
<code>[]string</code>
</td>
<td>
  <p><code>clusterDNS</code>是集群 DNS 服务器的 IP 地址的列表。
如果设置了，kubelet 将会配置所有容器使用这里的 IP 地址而不是宿主系统上的 DNS
服务器来完成 DNS 解析。
  <p>默认值：nil</p>
</td>
</tr>

<tr><td><code>streamingConnectionIdleTimeout</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>streamingConnectionIdleTimeout</code>设置流式连接在被自动关闭之前可以空闲的最长时间。</p>
   <p>默认值：&quot;4h&quot;</p>
</td>
</tr>

<tr><td><code>nodeStatusUpdateFrequency</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>nodeStatusUpdateFrequency</code>是 kubelet 计算节点状态的频率。
如果未启用节点租约特性，这一字段设置的也是 kubelet 向控制面投递节点状态的频率。</p>
   <p>注意：如果节点租约特性未被启用，更改此参数设置时要非常小心，
所设置的参数值必须与节点控制器的<code>nodeMonitorGracePeriod</code>协同。</p>
   <p>默认值：&quot;10s&quot;</p>
</td>
</tr>

<tr><td><code>nodeStatusReportFrequency</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>nodeStatusReportFrequency</code>是节点状态未发生变化时，kubelet
向控制面更新节点状态的频率。如果节点状态发生变化，则 kubelet 会忽略这一频率设置，
立即更新节点状态。</p>
   <p>此字段仅当启用了节点租约特性时才被使用。<code>nodeStatusReportFrequency</code>
的默认值是&quot;5m&quot;。不过，如果<code>nodeStatusUpdateFrequency</code>
被显式设置了，则<code>nodeStatusReportFrequency</code>的默认值会等于
<code>nodeStatusUpdateFrequency</code>值，这是为了实现向后兼容。</p>
   <p>默认值：&quot;5m&quot;</p>
</td>
</tr>

<tr><td><code>nodeLeaseDurationSeconds</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>nodeLeaseDurationSeconds</code>是 kubelet 会在其对应的 Lease 对象上设置的时长值。
<code>NodeLease</code>让 kubelet 来在<code>kube-node-lease</code>名字空间中创建
按节点名称命名的租约并定期执行续约操作，并通过这种机制来了解节点健康状况。</p>
   <p>如果租约过期，则节点可被视作不健康。根据 KEP-0009 约定，目前的租约每 10 秒钟续约一次。
在将来，租约的续约时间间隔可能会根据租约的时长来设置。</p>
   <p>此字段的取值必须大于零。</p>
  <p>默认值：40</p>
</td>
</tr>

<tr><td><code>imageMinimumGCAge</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>imageMinimumGCAge</code>是对未使用镜像进行垃圾搜集之前允许其存在的时长。</p>
   <p>默认值：&quot;2m&quot;</p>
</td>
</tr>

<tr><td><code>imageGCHighThresholdPercent</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>imageGCHighThresholdPercent</code>所给的是镜像的磁盘用量百分数，
一旦镜像用量超过此阈值，则镜像垃圾收集会一直运行。百分比是用这里的值除以 100
得到的，所以此字段取值必须介于 0 和 100 之间，包括 0 和 100。如果设置了此字段，
则取值必须大于<code>imageGCLowThresholdPercent</code>取值。</p>
   <p>默认值：85</p>
</td>
</tr>

<tr><td><code>imageGCLowThresholdPercent</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>imageGCLowThresholdPercent</code>所给的是镜像的磁盘用量百分数，
镜像用量低于此阈值时不会执行镜像垃圾收集操作。垃圾收集操作也将此作为最低磁盘用量边界。
百分比是用这里的值除以 100 得到的，所以此字段取值必须介于 0 和 100 之间，包括 0 和 100。
如果设置了此字段，则取值必须小于<code>imageGCHighThresholdPercent</code>取值。</p>
   <p>默认值：80</p>
</td>
</tr>

<tr><td><code>volumeStatsAggPeriod</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>volumeStatsAggPeriod</code>是计算和缓存所有 Pod 磁盘用量的频率。</p>
   <p>默认值：&quot;1m&quot;</p>
</td>
</tr>

<tr><td><code>kubeletCgroups</code><br/>
<code>string</code>
</td>
<td>
   <p><code>kubeletCgroups</code>是用来隔离 kubelet 的控制组（CGroup）的绝对名称。</p>
   <p>默认值：&quot;&quot;</p>
</td>
</tr>

<tr><td><code>systemCgroups</code><br/>
<code>string</code>
</td>
<td>
   <p><code>systemCgroups</code>是用来放置那些未被容器化的、非内核的进程的控制组
（CGroup）的绝对名称。设置为空字符串表示没有这类容器。回滚此字段设置需要重启节点。
当此字段非空时，必须设置<code>cgroupRoot</code>字段。</p>
   <p>默认值：&quot;&quot;</p>
</td>
</tr>

<tr><td><code>cgroupRoot</code><br/>
<code>string</code>
</td>
<td>
   <p><code>cgroupRoot</code>是用来运行 Pod 的控制组（CGroup）。
容器运行时会尽可能处理此字段的设置值。</p>
</td>
</tr>

<tr><td><code>cgroupsPerQOS</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>cgroupsPerQOS</code>用来启用基于 QoS 的控制组（CGroup）层次结构：
顶层的控制组用于不同 QoS 类，所有<code>Burstable</code>和<code>BestEffort</code> Pod
都会被放置到对应的顶级 QoS 控制组下。</p>
   <p>默认值：true</p>
</td>
</tr>

<tr><td><code>cgroupDriver</code><br/>
<code>string</code>
</td>
<td>
   <p><code>cgroupDriver</code>是 kubelet 用来操控宿主系统上控制组（CGroup）
的驱动程序（cgroupfs 或 systemd）。</p>
   <p>默认值：&quot;cgroupfs&quot;</p>
</td>
</tr>

<tr><td><code>cpuManagerPolicy</code><br/>
<code>string</code>
</td>
<td>
   <p><code>cpuManagerPolicy</code>是要使用的策略名称。需要启用<code>CPUManager</code>
特性门控。</p>
   <p>默认值：&quot;none&quot;</p>
</td>
</tr>

<tr><td><code>cpuManagerPolicyOptions</code><br/>
<code>map[string]string</code>
</td>
<td>
   <p><code>cpuManagerPolicyOptions</code>是一组<code>key=value</code>键值映射，
容许通过额外的选项来精细调整 CPU 管理器策略的行为。需要<code>CPUManager</code>和
<code>CPUManagerPolicyOptions</code>两个特性门控都被启用。</p>
   <p>默认值：nil</p>
</td>
</tr>

<tr><td><code>cpuManagerReconcilePeriod</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>cpuManagerReconcilePeriod</code>是 CPU 管理器的协调周期时长。默认值：&quot;10s&quot;</p>
</td>
</tr>

<tr><td><code>memoryManagerPolicy</code><br/>
<code>string</code>
</td>
<td>
   <p><code>memoryManagerPolicy</code>是内存管理器要使用的策略的名称。
要求启用<code>MemoryManager</code>特性门控。</p>
   <p>默认值：&quot;none&quot;</p>
</td>
</tr>

<tr><td><code>topologyManagerPolicy</code><br/>
<code>string</code>
</td>
<td>
   <p><code>topologyManagerPolicy</code>是要使用的拓扑管理器策略名称。合法值包括：</p> 
   <ul>
    <li><code>restricted</code>：kubelet 仅接受在所请求资源上实现最佳 NUMA 对齐的 Pod。</li>
    <li><code>best-effort</code>：kubelet 会优选在 CPU 和设备资源上实现 NUMA 对齐的 Pod。</li>
    <li><code>none</code>：kubelet 不了解 Pod CPU 和设备资源 NUMA 对齐需求。</li>
    <li><code>single-numa-node</code>：kubelet 仅允许在 CPU 和设备资源上对齐到同一 NUMA 节点的 Pod。</li>
   </ul>
   <p>默认值：&quot;none&quot;</p>
</td>
</tr>

<tr><td><code>topologyManagerScope</code><br/>
<code>string</code>
</td>
<td>
   <p><code>topologyManagerScope</code>代表的是拓扑提示生成的范围，
拓扑提示信息由提示提供者生成，提供给拓扑管理器。合法值包括：</p>
   <ul>
    <li><code>container</code>：拓扑策略是按每个容器来实施的。</li>
    <li><code>pod</code>：拓扑策略是按每个 Pod 来实施的。</li>
   </ul>
   <p>默认值：&quot;container&quot;</p>
</td>
</tr>

<tr><td><code>topologyManagerPolicyOptions</code><br/>
<code>map[string]string</code>
</td>
<td>
   <p>TopologyManagerPolicyOptions 是一组 key=value 键值映射，容许设置额外的选项来微调拓扑管理器策略的行为。需要同时启用 &quot;TopologyManager&quot; 和 &quot;TopologyManagerPolicyOptions&quot; 特性门控。
默认值：nil</p>
</td>
</tr>

<tr><td><code>qosReserved</code><br/>
<code>map[string]string</code>
</td>
<td>
   <p><code>qosReserved</code>是一组从资源名称到百分比值的映射，用来为<code>Guaranteed</code>
QoS 类型的负载预留供其独占使用的资源百分比。目前支持的资源为：&quot;memory&quot;。
需要启用<code>QOSReserved</code>特性门控。</p>
   <p>默认值：nil</p>
</td>
</tr>

<tr><td><code>runtimeRequestTimeout</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>runtimeRequestTimeout</code>用来设置除长期运行的请求（<code>pull</code>、
<code>logs</code>、<code>exec</code>和<code>attach</code>）之外所有运行时请求的超时时长。</p>
   <p>默认值：&quot;2m&quot;</p>
</td>
</tr>

<tr><td><code>hairpinMode</code><br/>
<code>string</code>
</td>
<td>
   <p><code>hairpinMode</code>设置 kubelet 如何为发夹模式数据包配置容器网桥。
设置此字段可以让 Service 中的端点在尝试访问自身 Service 时将服务请求路由的自身。
可选值有：</p>
   <ul>
    <li>&quot;promiscuous-bridge&quot;：将容器网桥设置为混杂模式。</li>
    <li>&quot;hairpin-veth&quot;：在容器的 veth 接口上设置发夹模式标记。</li>
    <li>&quot;none&quot;：什么也不做。</li>
   </ul>
   <p>一般而言，用户必须设置<code>--hairpin-mode=hairpin-veth</code>才能实现发夹模式的网络地址转译
（NAT），因为混杂模式的网桥要求存在一个名为<code>cbr0</code>的容器网桥。</p>
   <p>默认值：&quot;promiscuous-bridge&quot;</p>
</td>
</tr>

<tr><td><code>maxPods</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>maxPods</code>是此 kubelet 上课运行的 Pod 个数上限。此值必须为非负整数。</p>
   <p>默认值：110</p>
</td>
</tr>

<tr><td><code>podCIDR</code><br/>
<code>string</code>
</td>
<td>
   <p><code>podCIDR</code>是用来设置 Pod IP 地址的 CIDR 值，仅用于独立部署模式。
运行于集群模式时，这一数值会从控制面获得。</p>
   <p>默认值：&quot;&quot;</p>
</td>
</tr>

<tr><td><code>podPidsLimit</code><br/>
<code>int64</code>
</td>
<td>
   <p><code>podPidsLimit</code>是每个 Pod 中可使用的 PID 个数上限。</p>
   <p>默认值：-1</p>
</td>
</tr>

<tr><td><code>resolvConf</code><br/>
<code>string</code>
</td>
<td>
   <p><code>resolvConf</code>是一个域名解析配置文件，用作容器 DNS 解析配置的基础。</p>
   <p>如果此值设置为空字符串，则会覆盖 DNS 解析的默认配置，
本质上相当于禁用了 DNS 查询。</p>
   <p>默认值：&quot;/etc/resolv.conf&quot;</p>
</td>
</tr>

<tr><td><code>runOnce</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>runOnce</code>字段被设置时，kubelet 会咨询 API 服务器一次并获得 Pod 列表，
运行在静态 Pod 文件中指定的 Pod 及这里所获得的 Pod，然后退出。</p>
   <p>默认值：false</p>
</td>
</tr>

<tr><td><code>cpuCFSQuota</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>cpuCFSQuota</code>允许为设置了 CPU 限制的容器实施 CPU CFS 配额约束。</p>
   <p>默认值：true</p>
</td>
</tr>

<tr><td><code>cpuCFSQuotaPeriod</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>cpuCFSQuotaPeriod</code>设置 CPU CFS 配额周期值，<code>cpu.cfs_period_us</code>。
此值需要介于 1 毫秒和 1 秒之间，包含 1 毫秒和 1 秒。
此功能要求启用 <code>CustomCPUCFSQuotaPeriod</code> 特性门控被启用。</p>
   <p>默认值：&quot;100ms&quot;</p>
</td>
</tr>

<tr><td><code>nodeStatusMaxImages</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>nodeStatusMaxImages</code>限制<code>Node.status.images</code>中报告的镜像数量。
此值必须大于 -2。</p>
   <p>注意：如果设置为 -1，则不会对镜像数量做限制；如果设置为 0，则不会返回任何镜像。</p>
   <p>默认值：50</p>
</td>
</tr>

<tr><td><code>maxOpenFiles</code><br/>
<code>int64</code>
</td>
<td>
   <p><code>maxOpenFiles</code>是 kubelet 进程可以打开的文件个数。此值必须不能为负数。</p>
   <p>默认值：1000000</p>
</td>
</tr>

<tr><td><code>contentType</code><br/>
<code>string</code>
</td>
<td>
   <p><code>contentType</code>是向 API 服务器发送请求时使用的内容类型。</p>
   <p>默认值：&quot;application/vnd.kubernetes.protobuf&quot;</p>
</td>
</tr>

<tr><td><code>kubeAPIQPS</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>kubeAPIQPS</code>设置与 Kubernetes API 服务器通信时要使用的 QPS（每秒查询数）。</p>
   <p>默认值：50</p>
</td>
</tr>

<tr><td><code>kubeAPIBurst</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>kubeAPIBurst</code>设置与 Kubernetes API 服务器通信时突发的流量级别。
此字段取值不可以是负数。</p>
   <p>默认值：100</p>
</td>
</tr>

<tr><td><code>serializeImagePulls</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>serializeImagePulls</code>被启用时会通知 kubelet 每次仅拉取一个镜像。
我们建议<em>不要</em>在所运行的 docker 守护进程版本低于 1.9、使用 aufs
存储后端的节点上更改默认值。详细信息可参见 Issue #10959。</p>
   <p>默认值：true</p>
</td>
</tr>

<tr><td><code>maxParallelImagePulls</code><br/>
<code>int32</code>
</td>
<td>
   <p>maxParallelImagePulls 设置并行拉取镜像的最大数量。
如果 serializeImagePulls 为 true，则无法设置此字段。
把它设置为 nil 意味着没有限制。</p>
   <p>默认值：true</p>
</td>
</tr>
<tr><td><code>evictionHard</code><br/>
<code>map[string]string</code>
</td>
<td>
   <p><code>evictionHard</code>是一个映射，是从信号名称到定义硬性驱逐阈值的映射。
例如：<code>{&quot;memory.available&quot;: &quot;300Mi&quot;}</code>。
如果希望显式地禁用，可以在任意资源上将其阈值设置为 0% 或 100%。</p>
   <p>默认值：</p>
   <code><pre>
   memory.available:  &quot;100Mi&quot;
   nodefs.available:  &quot;10%&quot;
   nodefs.inodesFree: &quot;5%&quot;
   imagefs.available: &quot;15%&quot;
  </pre></code>
</td>
</tr>

<tr><td><code>evictionSoft</code><br/>
<code>map[string]string</code>
</td>
<td>
   <p><code>evictionSoft</code>是一个映射，是从信号名称到定义软性驱逐阈值的映射。
例如：<code>{&quot;memory.available&quot;: &quot;300Mi&quot;}</code>。</p>
   <p>默认值：nil</p>
</td>
</tr>

<tr><td><code>evictionSoftGracePeriod</code><br/>
<code>map[string]string</code>
</td>
<td>
   <p><code>evictionSoftGracePeriod</code>是一个映射，是从信号名称到每个软性驱逐信号的宽限期限。
例如：<code>{&quot;memory.available&quot;: &quot;30s&quot;}</code>。</p>
   <p>默认值：nil</p>
</td>
</tr>

<tr><td><code>evictionPressureTransitionPeriod</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>evictionPressureTransitionPeriod</code>设置 kubelet
离开驱逐压力状况之前必须要等待的时长。</p>
   <p>默认值：&quot;5m&quot;</p>
</td>
</tr>

<tr><td><code>evictionMaxPodGracePeriod</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>evictionMaxPodGracePeriod</code>是指达到软性逐出阈值而引起 Pod 终止时，
可以赋予的宽限期限最大值（按秒计）。这个值本质上限制了软性逐出事件发生时，
Pod 可以获得的<code>terminationGracePeriodSeconds</code>。</p>
   <p>注意：由于 Issue #64530 的原因，系统中存在一个缺陷，即此处所设置的值会在软性逐出时覆盖
Pod 的宽限期设置，从而有可能增加 Pod 上原本设置的宽限期限时长。
这个缺陷会在未来版本中修复。</p>
   <p>默认值：0</p>
</td>
</tr>

<tr><td><code>evictionMinimumReclaim</code><br/>
<code>map[string]string</code>
</td>
<td>
   <p><code>evictionMinimumReclaim</code>是一个映射，定义信号名称与最小回收量数值之间的关系。
最小回收量指的是资源压力较大而执行 Pod 驱逐操作时，kubelet 对给定资源的最小回收量。
例如：<code>{&quot;imagefs.available&quot;: &quot;2Gi&quot;}</code>。</p>
   <p>默认值：nil</p>
</td>
</tr>

<tr><td><code>podsPerCore</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>podsPerCore</code>设置的是每个核上 Pod 个数上限。此值不能超过<code>maxPods</code>。
所设值必须是非负整数。如果设置为 0，则意味着对 Pod 个数没有限制。</p>
   <p>默认值：0</p>
</td>
</tr>

<tr><td><code>enableControllerAttachDetach</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>enableControllerAttachDetach</code>用来允许 Attach/Detach
控制器管理调度到本节点的卷的挂接（attachment）和解除挂接（detachement），
并且禁止 kubelet 执行任何 attach/detach 操作。</p>
   <p>注意：kubelet 不支持挂接 CSI 卷和解除挂接，
因此对于该用例，此选项必须为 true。</p>
   <p>默认值：true</p>
</td>
</tr>

<tr><td><code>protectKernelDefaults</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>protectKernelDefaults</code>设置为<code>true</code>时，会令 kubelet
在发现内核参数与预期不符时出错退出。若此字段设置为<code>false</code>，则 kubelet
会尝试更改内核参数以满足其预期。</p>
   <p>默认值：false</p>
</td>
</tr>

<tr><td><code>makeIPTablesUtilChains</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>makeIPTablesUtilChains</code>设置为<code>true</code>时，相当于允许 kubelet
确保一组 iptables 规则存在于宿主机上。这些规则会为不同的组件（例如 kube-proxy）
提供工具性质的规则。它们是基于<code>iptablesMasqueradeBit</code>和<code>iptablesDropBit</code>
来创建的。</p>
   <p>默认值：true</p>
</td>
</tr>

<tr><td><code>iptablesMasqueradeBit</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>iptablesMasqueradeBit</code>是 iptables fwmark 空间中用来为 SNAT
作标记的位。此值必须介于<code>[0, 31]</code>区间，必须与其他标记位不同。</p>
   <p>警告：请确保此值设置与 kube-proxy 中对应的参数设置取值相同。</p>
   <p>默认值：14</p>
</td>
</tr>

<tr><td><code>iptablesDropBit</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>iptablesDropBit</code>是 iptables fwmark 空间中用来标记丢弃包的数据位。
此值必须介于<code>[0, 31]</code>区间，必须与其他标记位不同。</p>
   <p>默认值：15</p>
</td>
</tr>

<tr><td><code>featureGates</code><br/>
<code>map[string]bool</code>
</td>
<td>
   <p><code>featureGates</code>是一个从功能特性名称到布尔值的映射，用来启用或禁用实验性的功能。
此字段可逐条更改文件 &quot;k8s.io/kubernetes/pkg/features/kube_features.go&quot;
中所给的内置默认值。</p>
   <p>默认值：nil</p>
</td>
</tr>

<tr><td><code>failSwapOn</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>failSwapOn</code>通知 kubelet 在节点上启用交换分区时拒绝启动。</p>
   <p>默认值：true</p>
</td>
</tr>

<tr><td><code>memorySwap</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-MemorySwapConfiguration"><code>MemorySwapConfiguration</code></a>
</td>
<td>
   <p><code>memorySwap</code>配置容器负载可用的交换内存。</p>
</td>
</tr>

<tr><td><code>containerLogMaxSize</code><br/>
<code>string</code>
</td>
<td>
   <p><code>containerLogMaxSize</code>是定义容器日志文件被轮转之前可以到达的最大尺寸。
例如：&quot;5Mi&quot; 或 &quot;256Ki&quot;。</p>
   <p>默认值：&quot;10Mi&quot;</p>
</td>
</tr>

<tr><td><code>containerLogMaxFiles</code><br/>
<code>int32</code>
</td>
<td>
   <p><code>containerLogMaxFiles</code>设置每个容器可以存在的日志文件个数上限。</p>
   <p>默认值：&quot;5&quot;</p>
</td>
</tr>

<tr><td><code>configMapAndSecretChangeDetectionStrategy</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-ResourceChangeDetectionStrategy"><code>ResourceChangeDetectionStrategy</code></a>
</td>
<td>
   <p><code>configMapAndSecretChangeDetectionStrategy</code>是 ConfigMap 和 Secret
管理器的运行模式。合法值包括：</p>
   <ul>
    <li><code>Get</code>：kubelet 从 API 服务器直接取回必要的对象；</li>
    <li><code>Cache</code>：kubelet 使用 TTL 缓存来管理来自 API 服务器的对象；</li>
    <li><code>Watch</code>：kubelet 使用 watch 操作来观察所关心的对象的变更。</li>
    </ul>
   <p>默认值：&quot;Watch&quot;</p>
</td>
</tr>

<tr><td><code>systemReserved</code><br/>
<code>map[string]string</code>
</td>
<td>
   <p><code>systemReserved</code>是一组<code>资源名称=资源数量</code>对，
用来描述为非 Kubernetes 组件预留的资源（例如：'cpu=200m,memory=150G'）。</p>
   <p>目前仅支持 CPU 和内存。更多细节可参见
   https://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/ 。</p>
   <p>默认值：Nil</p>
</td>
</tr>

<tr><td><code>kubeReserved</code><br/>
<code>map[string]string</code>
</td>
<td>
   <p><code>kubeReserved</code>是一组<code>资源名称=资源数量</code>对，
用来描述为 Kubernetes 系统组件预留的资源（例如：'cpu=200m,memory=150G'）。
目前支持 CPU、内存和根文件系统的本地存储。
更多细节可参见 https://kubernetes.io/zh/docs/concepts/configuration/manage-resources-containers/。</p>
   <p>默认值：Nil</p>
</td>
</tr>

<tr><td><code>reservedSystemCPUs</code> <B>[必需]</B><br/>
<code>string</code>
</td>
<td>
   <p><code>reservedSystemCPUs</code>选项设置为宿主级系统线程和 Kubernetes
相关线程所预留的 CPU 列表。此字段提供的是一种“静态”的 CPU 列表，而不是像
<code>systemReserved</code>和<code>kubeReserved</code>所提供的“动态”列表。
此选项不支持<code>systemReservedCgroup</code>或<code>kubeReservedCgroup</code>。</p>
</td>
</tr>

<tr><td><code>showHiddenMetricsForVersion</code><br/>
<code>string</code>
</td>
<td>
   <p><code>showHiddenMetricsForVersion<code>是你希望显示隐藏度量值的上一版本。
只有上一个次版本是有意义的，其他值都是不允许的。
字段值的格式为<code>&lt;major&gt;.&lt;minor&gt;</code>，例如：<code>1.16</code>。
此格式的目的是为了确保在下一个版本中有新的度量值被隐藏时，你有机会注意到这类变化，
而不是当这些度量值在其后的版本中彻底去除时来不及应对。</p>
   <p>默认值：&quot;&quot;</p>
</td>
</tr>

<tr><td><code>systemReservedCgroup</code><br/>
<code>string</code>
</td>
<td>
   <p><code>systemReservedCgroup</code>帮助 kubelet 识别用来为 OS 系统级守护进程实施
<code>systemReserved</code>计算资源预留时使用的顶级控制组（CGroup）。
参考 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable">Node Allocatable</a>
以了解详细信息。</p>
   <p>默认值：&quot;&quot;</p>
</td>
</tr>


<tr><td><code>kubeReservedCgroup</code><br/>
<code>string</code>
</td>
<td>
   <p><code>kubeReservedCgroup</code> 帮助 kubelet 识别用来为 Kubernetes 节点系统级守护进程实施
<code>kubeReserved</code>计算资源预留时使用的顶级控制组（CGroup）。
参阅 <a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable">Node Allocatable</a>
了解进一步的信息。</p>
   <p>默认值：&quot;&quot;</p>
</td>
</tr>

<tr><td><code>enforceNodeAllocatable</code><br/>
<code>[]string</code>
</td>
<td>
   <p>此标志设置 kubelet 需要执行的各类节点可分配资源策略。此字段接受一组选项列表。
可接受的选项有<code>none</code>、<code>pods</code>、<code>system-reserved</code>和
<code>kube-reserved</code>。</p>
   <p>如果设置了<code>none</code>，则字段值中不可以包含其他选项。</p>
   <p>如果列表中包含<code>system-reserved</code>，则必须设置<code>systemReservedCgroup</code>。</p>
   <p>如果列表中包含<code>kube-reserved</code>，则必须设置<code>kubeReservedCgroup</code>。</p>
   <p>这个字段只有在<code>cgroupsPerQOS</code>被设置为<code>true</code>才被支持。</p>
   <p>参阅<a href="https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable">Node Allocatable</a>
了解进一步的信息。</p>
   <p>默认值：[&quot;pods&quot;]</p>
</td>
</tr>

<tr><td><code>allowedUnsafeSysctls</code><br/>
<code>[]string</code>
</td>
<td>
   <p>用逗号分隔的白名单列表，其中包含不安全的 sysctl 或 sysctl 模式（以<code>&#42;</code>结尾）。
</p>
   <p>不安全的 sysctl 组有 <code>kernel.shm&#42;</code>、<code>kernel.msg&#42;</code>、
<code>kernel.sem</code>、<code>fs.mqueue.&#42;</code> 和<code>net.&#42;</code>。</p>
   <p>例如：&quot;<code>kernel.msg&#42;,net.ipv4.route.min\_pmtu</code>&quot;</p>
   <p>默认值：[]</p>
</td>
</tr>

<tr><td><code>volumePluginDir</code><br/>
<code>string</code>
</td>
<td>
   <p><code>volumePluginDir</code>是用来搜索其他第三方卷插件的目录的路径。</p>
   <p>默认值：&quot;/usr/libexec/kubernetes/kubelet-plugins/volume/exec/&quot;</p>
</td>
</tr>

<tr><td><code>providerID</code><br/>
<code>string</code>
</td>
<td>
   <p><code>providerID</code>字段被设置时，指定的是一个外部提供者（即云驱动）实例的唯一 ID，
该提供者可用来唯一性地标识特定节点。</p>
   <p>默认值：&quot;&quot;</p>
</td>
</tr>

<tr><td><code>kernelMemcgNotification</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>kernelMemcgNotification</code>字段如果被设置了，会告知 kubelet 集成内核的
memcg 通知机制来确定是否超出内存逐出阈值，而不是使用轮询机制来判定。</p>
   <p>默认值：false</p>
</td>
</tr>

<tr><td><code>logging</code> <B>[必需]</B><br/>
<a href="#LoggingConfiguration"><code>LoggingConfiguration</code></a>
</td>
<td>
   <p><code>logging</code>设置日志机制选项。更多的详细信息科参阅
<a href="https://github.com/kubernetes/component-base/blob/master/logs/options.go">日志选项</a>。</p>
   <p>默认值：</p>
   <code><pre>Format: text</pre></code>
</td>
</tr>

<tr><td><code>enableSystemLogHandler</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>enableSystemLogHandler</code>用来启用通过 Web 接口 host:port/logs/
访问系统日志的能力。</p>
   <p>默认值：true</p>
</td>
</tr>

<tr><td><code>enableSystemLogQuery</code><br/>
<code>bool</code>
</td>
<td>
   <p>enableSystemLogQuery 启用在 /logs 端点上的节点日志查询功能。
此外，还必须启用 enableSystemLogHandler 才能使此功能起作用。</p>
   <p>默认值：false</p>
</td>
</tr>
<tr><td><code>shutdownGracePeriod</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>shutdownGracePeriod</code>设置节点关闭期间，节点自身需要延迟以及为
Pod 提供的宽限期限的总时长。</p>
   <p>默认值：&quot;0s&quot;</p>
</td>
</tr>

<tr><td><code>shutdownGracePeriodCriticalPods</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>shutdownGracePeriodCriticalPods</code>设置节点关闭期间用来终止关键性
Pod 的时长。此时长要短于<code>shutdownGracePeriod</code>。
例如，如果<code>shutdownGracePeriod=30s</code>，<code>shutdownGracePeriodCriticalPods=10s<code>，
在节点关闭期间，前 20 秒钟被预留用来体面终止普通 Pod，后 10 秒钟用来终止关键 Pod。</p>
   <p>默认值：&quot;0s&quot;</p>
</td>
</tr>

<tr><td><code>shutdownGracePeriodByPodPriority</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-ShutdownGracePeriodByPodPriority"><code>[]ShutdownGracePeriodByPodPriority</code></a>
</td>
<td>
   <p><code>shutdownGracePeriodByPodPriority</code>设置基于 Pod
相关的优先级类值而确定的体面关闭时间。当 kubelet 收到关闭请求的时候，kubelet
会针对节点上运行的所有 Pod 发起关闭操作，这些关闭操作会根据 Pod 的优先级确定其宽限期限，
之后 kubelet 等待所有 Pod 退出。</p>
   <p>数组中的每个表项代表的是节点关闭时 Pod 的体面终止时间；这里的 Pod
的优先级类介于列表中当前优先级类值和下一个表项的优先级类值之间。</p>
   <p>例如，要赋予关键 Pod 10 秒钟时间来关闭，赋予优先级&gt;=10000 Pod 20 秒钟时间来关闭，
赋予其余的 Pod 30 秒钟来关闭。</p>
   <p>shutdownGracePeriodByPodPriority:</p>
   <ul>
   <li>priority: 2000000000
   shutdownGracePeriodSeconds: 10</li>
   <li>priority: 10000
   shutdownGracePeriodSeconds: 20</li>
   <li>priority: 0
   shutdownGracePeriodSeconds: 30</li>
   </ul>
   <p>在退出之前，kubelet 要等待的时间上限为节点上所有优先级类的
<code>shutdownGracePeriodSeconds</code>的最大值。
当所有 Pod 都退出或者到达其宽限期限时，kubelet 会释放关闭防护锁。
此功能要求<code>GracefulNodeShutdown</code>特性门控被启用。</p>
   <p>当<code>shutdownGracePeriod</code>或<code>shutdownGracePeriodCriticalPods</code>
被设置时，此配置字段必须为空。</p>
   <p>默认值：nil</p>
</td>
</tr>

<tr><td><code>reservedMemory</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-MemoryReservation"><code>[]MemoryReservation</code></a>
</td>
<td>
   <p><code>reservedMemory</code>给出一个逗号分隔的列表，为 NUMA 节点预留内存。</p>
   <p>此参数仅在内存管理器功能特性语境下有意义。内存管理器不会为容器负载分配预留内存。
例如，如果你的 NUMA0 节点内存为 10Gi，<code>reservedMemory</code>设置为在 NUMA0
上预留 1Gi 内存，内存管理器会认为其上只有 9Gi 内存可供分配。</p>
   <p>你可以设置不同数量的 NUMA 节点和内存类型。你也可以完全忽略这个字段，不过你要清楚，
所有 NUMA 节点上预留内存的总量要等于通过
<a href="https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable">node allocatable</a>
设置的内存量。</p>
   <p>如果至少有一个节点可分配参数设置值非零，则你需要设置至少一个 NUMA 节点。</p>
   <p>此外，避免如下设置：</p>
   <ol>
   <li>在配置值中存在重复项，NUMA 节点和内存类型相同，但配置值不同，这是不允许的。</li>
   <li>为任何内存类型设置限制值为零。</li>
   <li>NUMA 节点 ID 在宿主系统上不存在。/li>
   <li>除<code>memory</code>和<code>hugepages-&lt;size&gt;</code>之外的内存类型。</li>
   </ol>
   <p>默认值：nil</p>
</td>
</tr>

<tr><td><code>enableProfilingHandler</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>enableProfilingHandler</code>启用通过 host:port/debug/pprof/ 接口来执行性能分析。</p>
   <p>默认值：true</p>
</td>
</tr>

<tr><td><code>enableDebugFlagsHandler</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>enableDebugFlagsHandler</code>启用通过 host:port/debug/flags/v Web
接口上的标志设置。</p>
   <p>默认值：true</p>
</td>
</tr>

<tr><td><code>seccompDefault</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>seccompDefault</code>字段允许针对所有负载将<code>RuntimeDefault</code>
设置为默认的 seccomp 配置。这一设置要求对应的<code>SeccompDefault</code>特性门控被启用。</p>
   <p>默认值：false</p>
</td>
</tr>

<tr><td><code>memoryThrottlingFactor</code><br/>
<code>float64</code>
</td>
<td>
   <p>当设置 cgroupv2 <code>memory.high</code>以实施<code>MemoryQoS</code>特性时，
<code>memoryThrottlingFactor</code>用来作为内存限制或节点可分配内存的系数。</p>
   <p>减小此系数会为容器控制组设置较低的 high 限制值，从而增大回收压力；反之，
增大此系数会降低回收压力。更多细节参见 https://kep.k8s.io/2570。</p>
   <p>默认值：0.8</p>
</td>
</tr>

<tr><td><code>registerWithTaints</code><br/>
<a href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#taint-v1-core"><code>[]core/v1.Taint</code></a>
</td>
<td>
   <p><code>registerWithTaints</code>是一个由污点组成的数组，包含 kubelet
注册自身时要向节点对象添加的污点。只有<code>registerNode</code>为<code>true</code>
时才会起作用，并且仅在节点的最初注册时起作用。</p>
   <p>默认值：nil</p>
</td>
</tr>

<tr><td><code>registerNode</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>registerNode</code>启用向 API 服务器的自动注册。</p>
   <p>默认值：true</p>
</td>
</tr>
<tr><td><code>tracing</code><br/>
<a href="#TracingConfiguration"><code>TracingConfiguration</code></a>
</td>
<td>
   <p>tracing 为 OpenTelemetry 追踪客户端设置版本化的配置信息。
参阅 https://kep.k8s.io/2832 了解更多细节。</p>
</td>
</tr>
<tr><td><code>localStorageCapacityIsolation</code><br/>
<code>bool</code>
</td>
<td>
   <p>localStorageCapacityIsolation 启用本地临时存储隔离特性。默认设置为 true。
此特性允许用户为容器的临时存储设置请求/限制，并以类似的方式管理 cpu 和 memory 的请求/限制。
此特性还允许为 emptyDir 卷设置 sizeLimit，如果卷所用的磁盘超过此限制将触发 Pod 驱逐。
此特性取决于准确测定根文件系统磁盘用量的能力。对于 kind rootless 这类系统，
如果不支持此能力，则 LocalStorageCapacityIsolation 特性应被禁用。
一旦禁用，用户不应该为容器的临时存储设置请求/限制，也不应该为 emptyDir 设置 sizeLimit。
默认值：true</p>
</td>
</tr>
<tr><td><code>containerRuntimeEndpoint</code> <B>[必需]</B><br/>
<code>string</code>
</td>
<td>
   <p>containerRuntimeEndpoint 是容器运行时的端点。
Linux 支持 UNIX 域套接字，而 Windows 支持命名管道和 TCP 端点。
示例：'unix://path/to/runtime.sock', 'npipe:////./pipe/runtime'。</p>
</td>
</tr>
<tr><td><code>imageServiceEndpoint</code><br/>
<code>string</code>
</td>
<td>
   <p>imageServiceEndpoint 是容器镜像服务的端点。
Linux 支持 UNIX 域套接字，而 Windows 支持命名管道和 TCP 端点。
示例：'unix:///path/to/runtime.sock'、'npipe:////./pipe/runtime'。
如果未指定，则使用 containerRuntimeEndpoint 中的值。</p>
</td>
</tr>
</tbody>
</table>

## `SerializedNodeConfigSource`     {#kubelet-config-k8s-io-v1beta1-SerializedNodeConfigSource}

SerializedNodeConfigSource 允许对 `v1.NodeConfigSource` 执行序列化操作。
这一类型供 kubelet 内部使用，以便跟踪动态配置的检查点。
此资源存在于 kubeletconfig API 组是因为它被当做是对 kubelet 的一种版本化输入。

<table class="table">
<tbody>

<tr><td><code>apiVersion</code><br/>string</td><td><code>kubelet.config.k8s.io/v1beta1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>SerializedNodeConfigSource</code></td></tr>

<tr><td><code>source</code><br/>
<a href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#nodeconfigsource-v1-core"><code>core/v1.NodeConfigSource</code></a>
</td>
<td>
   <p><code>source</code>是我们执行序列化的数据源。</p>
</td>
</tr>

</tbody>
</table>

## `CredentialProvider`     {#kubelet-config-k8s-io-v1beta1-CredentialProvider}

**出现在：**

- [CredentialProviderConfig](#kubelet-config-k8s-io-v1beta1-CredentialProviderConfig)

CredentialProvider 代表的是要被 kubelet 调用的一个 exec 插件。
这一插件只会在所拉取的镜像与该插件所处理的镜像匹配时才会被调用（参见 <code>matchImages</code>）。

<table class="table">
<tbody>

<code>string</code>
</td>
<td>
   <p>
   <code>name</code> 是凭据提供者的名称（必需）。此名称必须与 kubelet
   所看到的提供者可执行文件的名称匹配。可执行文件必须位于 kubelet 的 
   <code>bin</code> 目录（通过 <code>--image-credential-provider-bin-dir</code> 设置）下。
   </p>
</td>
</tr>
<code>[]string</code>
</td>
<td>
<p><code>matchImages</code> 是一个必须设置的字符串列表，用来匹配镜像以便确定是否要调用此提供者。
如果字符串之一与 kubelet 所请求的镜像匹配，则此插件会被调用并给予提供凭证的机会。
镜像应该包含镜像库域名和 URL 路径。</p>
<p><code>matchImages</code> 中的每个条目都是一个模式字符串，其中可以包含端口号和路径。
域名部分可以包含统配符，但端口或路径部分不可以。通配符可以用作子域名，例如
<code>&ast;.k8s.io</code> 或 <code>k8s.&ast;.io</code>，以及顶级域名，如 <code>k8s.&ast;</code>。</p>
<p>对类似 <code>app&ast;.k8s.io</code> 这类部分子域名的匹配也是支持的。
每个通配符只能用来匹配一个子域名段，所以 <code>&ast;.io</code> 不会匹配 <code>&ast;.k8s.io</code>。</p>
<p>镜像与 <code>matchImages</code> 之间存在匹配时，以下条件都要满足：</p>
<ul>
  <li>二者均包含相同个数的域名部分，并且每个域名部分都对应匹配；</li>
  <li><code>matchImages</code> 条目中的 URL 路径部分必须是目标镜像的 URL 路径的前缀；</li>
  <li>如果 <code>matchImages</code> 条目中包含端口号，则端口号也必须与镜像端口号匹配。</li>
</ul>
<p><code>matchImages</code> 的一些示例如下：</p>
<ul>
<li>123456789.dkr.ecr.us-east-1.amazonaws.com</li>
<li>&ast;.azurecr.io</li>
<li>gcr.io</li>
<li>&ast;.&ast;.registry.io</li>
<li>registry.io:8080/path</li>
</ul>
</td>
</tr>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p>
   <code>defaultCacheDuration</code> 是插件在内存中缓存凭据的默认时长，
   在插件响应中没有给出缓存时长时，使用这里设置的值。此字段是必需的。
   </p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p>
   要求 exec 插件 CredentialProviderRequest 请求的输入版本。
   所返回的 CredentialProviderResponse 必须使用与输入相同的编码版本。当前支持的值有：
   </p>
<ul>
<li>credentialprovider.kubelet.k8s.io/v1beta1</li>
</ul>
</td>
</tr>
<tr><td><code>args</code><br/>
<code>[]string</code>
</td>
<td>
   <p>在执行插件可执行文件时要传递给命令的参数。</p>
</td>
</tr>
<tr><td><code>env</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-ExecEnvVar"><code>[]ExecEnvVar</code></a>
</td>
<td>
   <p>
   <code>env</code> 定义要提供给插件进程的额外的环境变量。
   这些环境变量会与主机上的其他环境变量以及 client-go 所使用的环境变量组合起来，
   一起传递给插件。
   </p>
</td>
</tr>
</tbody>
</table>

## `ExecEnvVar`     {#kubelet-config-k8s-io-v1beta1-ExecEnvVar}

**出现在：**

- [CredentialProvider](#kubelet-config-k8s-io-v1beta1-CredentialProvider)

ExecEnvVar 用来在执行基于 exec 的凭据插件时设置环境变量。

<table class="table">
<tbody>

<code>string</code>
</td>
<td>
   <span class="text-muted">
   无描述
   </span>
</td>
</tr>
<code>string</code>
</td>
<td>
   <span class="text-muted">
   无描述
   </span>
</td>
</tr>
</tbody>
</table>


## `KubeletAnonymousAuthentication`     {#kubelet-config-k8s-io-v1beta1-KubeletAnonymousAuthentication}

**出现在：**

- [KubeletAuthentication](#kubelet-config-k8s-io-v1beta1-KubeletAuthentication)

<table class="table">
<tbody>

<tr><td><code>enabled</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>enabled</code>允许匿名用户向 kubelet 服务器发送请求。
未被其他身份认证方法拒绝的请求都会被当做匿名请求。
匿名请求对应的用户名为<code>system:anonymous</code>，对应的用户组名为
<code>system:unauthenticated</code>。</p>
</td>
</tr>
</tbody>
</table>

## `KubeletAuthentication`     {#kubelet-config-k8s-io-v1beta1-KubeletAuthentication}

**出现在：**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)

<table class="table">
<tbody>

<tr><td><code>x509</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletX509Authentication"><code>KubeletX509Authentication</code></a>
</td>
<td>
   <p><code>x509</code>包含与 x509 客户端证书认证相关的配置。</p>
</td>
</tr>

<tr><td><code>webhook</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletWebhookAuthentication"><code>KubeletWebhookAuthentication</code></a>
</td>
<td>
   <p><code>webhook</code>包含与 Webhook 持有者令牌认证相关的配置。</p>
</td>
</tr>

<tr><td><code>anonymous</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletAnonymousAuthentication"><code>KubeletAnonymousAuthentication</code></a>
</td>
<td>
   <p><code>anonymous</code>包含与匿名身份认证相关的配置信息。</p>
</td>
</tr>
</tbody>
</table>

## `KubeletAuthorization`     {#kubelet-config-k8s-io-v1beta1-KubeletAuthorization}

**出现在：**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)

<table class="table">
<tbody>

<tr><td><code>mode</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletAuthorizationMode"><code>KubeletAuthorizationMode</code></a>
</td>
<td>
   <p><code>mode>是应用到 kubelet 服务器所接收到的请求上的鉴权模式。合法值包括
<code>AlwaysAllow</code>和<code>Webhook</code>。
Webhook 模式使用 <code>SubjectAccessReview</code> API 来确定鉴权。</p>
</td>
</tr>

<tr><td><code>webhook</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletWebhookAuthorization"><code>KubeletWebhookAuthorization</code></a>
</td>
<td>
   <p><code>webhook</code>包含与 Webhook 鉴权相关的配置信息。</p>
</td>
</tr>
</tbody>
</table>

## `KubeletAuthorizationMode`     {#kubelet-config-k8s-io-v1beta1-KubeletAuthorizationMode}

（`string` 类型的别名）

**出现在：**

- [KubeletAuthorization](#kubelet-config-k8s-io-v1beta1-KubeletAuthorization)

## `KubeletWebhookAuthentication`     {#kubelet-config-k8s-io-v1beta1-KubeletWebhookAuthentication}

**出现在：**

- [KubeletAuthentication](#kubelet-config-k8s-io-v1beta1-KubeletAuthentication)

<table class="table">
<tbody>

<tr><td><code>enabled</code><br/>
<code>bool</code>
</td>
<td>
   <p><code>enabled</code>允许使用<code>tokenreviews.authentication.k8s.io</code>
API 来提供持有者令牌身份认证。</p>
</td>
</tr>

<tr><td><code>cacheTTL</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>cacheTTL</code>启用对身份认证结果的缓存。</p>
</td>
</tr>
</tbody>
</table>

## `KubeletWebhookAuthorization`     {#kubelet-config-k8s-io-v1beta1-KubeletWebhookAuthorization}

**出现在：**

- [KubeletAuthorization](#kubelet-config-k8s-io-v1beta1-KubeletAuthorization)

<table class="table">
<tbody>

<tr><td><code>cacheAuthorizedTTL</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>cacheAuthorizedTTL</code>设置来自 Webhook 鉴权组件的 'authorized'
响应的缓存时长。</p>
</td>
</tr>
<tr><td><code>cacheUnauthorizedTTL</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p><code>cacheUnauthorizedTTL</code>设置来自 Webhook 鉴权组件的 'unauthorized'
响应的缓存时长。</p>
</td>
</tr>
</tbody>
</table>

## `KubeletX509Authentication`     {#kubelet-config-k8s-io-v1beta1-KubeletX509Authentication}

**出现在：**

- [KubeletAuthentication](#kubelet-config-k8s-io-v1beta1-KubeletAuthentication)

<table class="table">
<tbody>

<tr><td><code>clientCAFile</code><br/>
<code>string</code>
</td>
<td>
   <p><code>clientCAFile</code>是一个指向 PEM 编发的证书包的路径。
如果设置了此字段，则能够提供由此证书包中机构之一所签名的客户端证书的请求会被成功认证，
并且其用户名对应于客户端证书的<code>CommonName</code>、组名对应于客户端证书的
<code>Organization</code>。</p>
</td>
</tr>
</tbody>
</table>

## `MemoryReservation`     {#kubelet-config-k8s-io-v1beta1-MemoryReservation}

**出现在：**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)

MemoryReservation 为每个 NUMA 节点设置不同类型的内存预留。

<table class="table">
<tbody>

<tr><td><code>numaNode</code> <B>[必需]</B><br/>
<code>int32</code>
</td>
<td>
   <p>NUMA 节点</p>
</td>
</tr>

<tr><td><code>limits</code> <B>[必需]</B><br/>
<a href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#resourcelist-v1-core"><code>core/v1.ResourceList</code></a>
</td>
<td>
   <p>资源列表</p>
</td>
</tr>
</tbody>
</table>

## `MemorySwapConfiguration`     {#kubelet-config-k8s-io-v1beta1-MemorySwapConfiguration}

**出现在：**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)

<table class="table">
<tbody>

<tr><td><code>swapBehavior</code><br/>
<code>string</code>
</td>
<td>
   <p><code>swapBehavior</code>配置容器负载可以使用的交换内存。可以是
   <ul>
    <li>&quot;&quot;、&quot;LimitedSwap&quot;：工作负载的内存和交换分区总用量不能超过 Pod 的内存限制；</li>
    <li>&quot;UnlimitedSwap&quot;：工作负载可以无限制地使用交换分区，上限是可分配的约束。</li>
   </ul>
</td>
</tr>
</tbody>
</table>

## `ResourceChangeDetectionStrategy`     {#kubelet-config-k8s-io-v1beta1-ResourceChangeDetectionStrategy}

（`string` 类型的别名）

**出现在：**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)

ResourceChangeDetectionStrategy 给出的是内部管理器（ConfigMap、Secret）
用来发现对象变化的模式。

## `ShutdownGracePeriodByPodPriority`     {#kubelet-config-k8s-io-v1beta1-ShutdownGracePeriodByPodPriority}

**出现在：**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)

ShutdownGracePeriodByPodPriority 基于 Pod 关联的优先级类数值来为其设置关闭宽限时间。

<table class="table">
<tbody>

<tr><td><code>priority</code> <B>[必需]</B><br/>
<code>int32</code>
</td>
<td>
   <p><code>priority</code>是与关闭宽限期限相关联的优先级值。</p>
</td>
</tr>

<tr><td><code>shutdownGracePeriodSeconds</code> <B>[必需]</B><br/>
<code>int64</code>
</td>
<td>
   <p><code>shutdownGracePeriodSeconds</code>是按秒数给出的关闭宽限期限。
</td>
</tr>
</tbody>
</table>

## `FormatOptions`     {#FormatOptions}

**出现在：**

- [LoggingConfiguration](#LoggingConfiguration)

<p>
FormatOptions 包含为不同日志格式提供的选项。
</p>

<table class="table">
<tbody>

<tr><td><code>json</code> <B>[必需]</B><br/>
<a href="#JSONOptions"><code>JSONOptions</code></a>
</td>
<td>
   <p>[Alpha] JSON 包含记录 &quot;json&quot; 格式日志的选项。
只有 LoggingAlphaOptions 特性门控被启用时才可用。</p>
</td>
</tr>
</tbody>
</table>

## `JSONOptions`     {#JSONOptions}

**出现在：**

- [FormatOptions](#FormatOptions)

<p>
JSONOptions 包含为 &quot;json&quot; 日志格式提供的选项。
</p>

<table class="table">
<tbody>
<tr><td><code>splitStream</code> <B>[必需]</B><br/>
<code>bool</code>
</td>
<td>
   <p>
   [Alpha] <code>splitStream</code> 将错误信息重定向到标准错误输出（stderr），
而将提示信息重定向到标准输出（stdout），并为二者提供缓存。
默认设置是将二者都写出到标准输出，并且不提供缓存。
只有 LoggingAlphaOptions 特性门控被启用时才可用。
   </p>
</td>
</tr>

<tr><td><code>infoBufferSize</code> <B>[必需]</B><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/api/resource#QuantityValue"><code>k8s.io/apimachinery/pkg/api/resource.QuantityValue</code></a>
</td>
<td>
   <p>
   [Alpha] <code>infoBufferSize</code> 在分离数据流时用来设置提示数据流的大小。
默认值为 0，相当于禁止缓存。只有 LoggingAlphaOptions 特性门控被启用时才可用。
   </p>
</td>
</tr>
</tbody>
</table>

## `LogFormatFactory`     {#LogFormatFactory}

<p>LogFormatFactory 提供了对某些附加的、非默认的日志格式的支持。</p>

## `LoggingConfiguration`     {#LoggingConfiguration}

**出现在：**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)

LoggingConfiguration 包含日志选项。

<table class="table">
<tbody>

<tr><td><code>format</code> <B>[必需]</B><br/>
<code>string</code>
</td>
<td>
  <p>
  <code>format<code> 设置日志消息的结构。默认的格式取值为 <code>text</code>。
  </p>
</td>
</tr>

<tr><td><code>flushFrequency</code> <B>[必需]</B><br/>
<a href="https://pkg.go.dev/time#Duration"><code>time.Duration</code></a>
</td>
<td>
  <p>
   对日志进行清洗的最大间隔纳秒数（例如，1s = 1000000000）。
   如果所选的日志后端在写入日志消息时不提供缓存，则此配置会被忽略。
  </p>
</td>
</tr>

<tr><td><code>verbosity</code> <B>[必需]</B><br/>
<a href="#VerbosityLevel"><code>VerbosityLevel</code></a>
</td>
<td>
  <p>
  <code>verbosity</code> 用来确定日志消息记录的详细程度阈值。默认值为 0，
意味着仅记录最重要的消息。数值越大，额外的消息越多。出错消息总是会被记录下来。
  </p>
</td>
</tr>

<tr><td><code>vmodule</code> <B>[必需]</B><br/>
<a href="#VModuleConfiguration"><code>VModuleConfiguration</code></a>
</td>
<td>
  <p>
  <code>vmodule</code> 会在单个文件层面重载 verbosity 阈值的设置。
这一选项仅支持 &quot;text&quot; 日志格式。
  </p>
</td>
</tr>

<tr><td><code>options</code> <B>[必需]</B><br/>
<a href="#FormatOptions"><code>FormatOptions</code></a>
</td>
<td>
  <p>
  [Alpha] <code>options</code> 中包含特定于不同日志格式的附加参数。
只有针对所选格式的选项会被使用，但是合法性检查时会查看所有参数。
只有 LoggingAlphaOptions 特性门控被启用时才可用。
  </p>
</td>
</tr>
</tbody>
</table>

## `TracingConfiguration`     {#TracingConfiguration}

**出现在：**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)

<p>TracingConfiguration 为 OpenTelemetry 追踪客户端提供版本化的配置信息。</p>


<table class="table">
<thead><tr><th width="30%">字段</th><th>描述</th></tr></thead>
<tbody>
    
  
<tr><td><code>endpoint</code><br/>
<code>string</code>
</td>
<td>
   <p>采集器的 endpoint，此组件将向其报告追踪链路。
此连接不安全，目前不支持 TLS。推荐不设置，endpoint 是 otlp grpc 默认值，localhost:4317。</p>
</td>
</tr>
<tr><td><code>samplingRatePerMillion</code><br/>
<code>int32</code>
</td>
<td>
   <p>samplingRatePerMillion 是每百万 span 要采集的样本数。推荐不设置。
如果不设置，则采样器优先使用其父级 span 的采样率，否则不采样。</p>
</td>
</tr>
</tbody>
</table>

## `VModuleConfiguration`     {#VModuleConfiguration}

（`[]k8s.io/component-base/logs/api/v1.VModuleItem` 的别名）

**出现在：**

- [LoggingConfiguration](#LoggingConfiguration)

VModuleConfiguration 是一个集合，其中包含一个个文件名（或文件名模式）
及其对应的详细程度阈值。

## `VerbosityLevel`     {#VerbosityLevel}
    
（`uint32` 的别名）

**出现在：**

- [LoggingConfiguration](#LoggingConfiguration)

<p>VerbosityLevel 表示 klog 或 logr 的详细程度（verbosity）阈值。</p>

