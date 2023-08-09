---
title: kube-proxy
content_type: tool-reference
weight: 30
---


## {{% heading "synopsis" %}}

Kubernetes 网络代理在每个节点上运行。网络代理反映了每个节点上 Kubernetes API
中定义的服务，并且可以执行简单的 TCP、UDP 和 SCTP 流转发，或者在一组后端进行
循环 TCP、UDP 和 SCTP 转发。
当前可通过 Docker-links-compatible 环境变量找到服务集群 IP 和端口，
这些环境变量指定了服务代理打开的端口。
有一个可选的插件，可以为这些集群 IP 提供集群 DNS。
用户必须使用 apiserver API 创建服务才能配置代理。

```
kube-proxy [flags]
```

## {{% heading "options" %}}


   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--add_dir_header</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果为 true，将文件目录添加到日志消息的头部
</p>
</td>
</tr>

<tr>
<td colspan="2">--alsologtostderr</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
设置为 true 表示将日志输出到文件的同时输出到 stderr（当 <code>--logtostderr=true</code> 时不生效）
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
代理服务器的 IP 地址（所有 IPv4 接口设置为 “0.0.0.0”，所有 IPv6 接口设置为 “::”）。
如果配置文件由 <code>--config</code> 指定，则忽略此参数。
</p></td>
</tr>

<tr>
<td colspan="2">--bind-address-hard-fail</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果为 true，kube-proxy 会将无法绑定端口的失败操作视为致命错误并退出。
</p></td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
逗号分隔的文件列表，用于检查 boot-id。使用第一个存在的文件。
</p></td>
</tr>

<tr>
<td colspan="2">--cleanup</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果为 true，清理 iptables 和 ipvs 规则并退出。
</p>
</td>
</tr>

<tr>
<td colspan="2">--cluster-cidr string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
集群中 Pod 的 CIDR 范围。配置后，将从该范围之外发送到服务集群 IP
的流量被伪装，从 Pod 发送到外部 LoadBalancer IP
的流量将被重定向到相应的集群 IP。
对于双协议栈集群，接受一个逗号分隔的列表，
每个 IP 协议族（IPv4 和 IPv6）至少包含一个 CIDR。
如果配置文件由 <code>--config</code> 指定，则忽略此参数。
</p>
</td>
</tr>

<tr>
<td colspan="2">--config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
配置文件的路径。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
来自 apiserver 的配置的刷新频率。必须大于 0。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
每个 CPU 核跟踪的最大 NAT 连接数（0 表示保留当前限制并忽略 conntrack-min 设置）。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
无论 <code>conntrack-max-per-core</code> 多少，要分配的 conntrack
条目的最小数量（将 <code>conntrack-max-per-core</code> 设置为 0 即可
保持当前的限制）。
</p>
</td>
</tr>

<tr>
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
处于 <code>CLOSE_WAIT</code> 状态的 TCP 连接的 NAT 超时。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
已建立的 TCP 连接的空闲超时（0 保持当前设置）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--detect-local-mode LocalMode</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
用于检测本地流量的模式。
如果配置文件由 <code>--config</code> 指定，则忽略此参数。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
一组 key=value 对，用来描述测试性/试验性功能的特性门控。可选项有：<br/>
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
WindowsHostNetwork=true|false (ALPHA - 默认值为 true)<br/>
如果配置文件由 <code>--config</code> 指定，则忽略此参数。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
服务健康状态检查的 IP 地址和端口（设置为 '0.0.0.0:10256' 表示使用所有
IPv4 接口，设置为 '[::]:10256' 表示使用所有 IPv6 接口）；
设置为空则禁用。
如果配置文件由 <code>--config</code> 指定，则忽略此参数。
</p>
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
kube-proxy 操作的帮助命令。
</p>
</td>
</tr>

<tr>
<td colspan="2">--hostname-override string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果非空，将使用此字符串而不是实际的主机名作为标识。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td>
</td>
<td style="line-height: 130%; word-wrap: break-word;">
<p>
如果设为 false，Kube-proxy 将禁用允许通过本地主机访问 NodePort 服务的传统行为，
这仅适用于 iptables 模式和 ipv4。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
在使用纯 iptables 代理时，用来设置 fwmark 空间的 bit，标记需要
SNAT 的数据包。必须在 [0,31] 范围内。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
iptables 规则可以随着端点和服务的更改而刷新的最小间隔（例如 '5s'、'1m'、'2h22m'）。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
刷新 iptables 规则的最大间隔（例如 '5s'、'1m'、'2h22m'）。必须大于 0。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-exclude-cidrs strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
逗号分隔的 CIDR 列表，ipvs 代理在清理 IPVS 规则时不会此列表中的地址范围。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-min-sync-period duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
ipvs 规则可以随着端点和服务的更改而刷新的最小间隔（例如 '5s'、'1m'、'2h22m'）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-scheduler string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
代理模式为 ipvs 时所选的 ipvs 调度器类型。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-strict-arp</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
通过将 <code>arp_ignore</code> 设置为 1 并将 <code>arp_announce</code>
设置为 2 启用严格的 ARP。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
刷新 ipvs 规则的最大间隔（例如 '5s'、'1m'、'2h22m'）。必须大于 0。
</p>
</td>
</tr>


<tr>
<td colspan="2">--ipvs-tcp-timeout duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
空闲 IPVS TCP 连接的超时时间，0 保持连接（例如 '5s'、'1m'、'2h22m'）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-tcpfin-timeout duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
收到 FIN 数据包后，IPVS TCP 连接的超时，0 保持当前设置不变。（例如 '5s'、'1m'、'2h22m'）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-udp-timeout duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
IPVS UDP 数据包的超时，0 保持当前设置不变。（例如 '5s'、'1m'、'2h22m'）。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
与 kubernetes apiserver 通信的突发数量。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
发送到 apiserver 的请求的内容类型。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
与 kubernetes apiserver 交互时使用的 QPS。
</p>
</td>
</tr>

<tr>
<td colspan="2">--kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
包含鉴权信息的 kubeconfig 文件的路径（主控节点位置由 master 标志设置）。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
当日志命中 file:N，触发一次堆栈追踪
</p></td>
</tr>

<tr>
<td colspan="2">--log_dir string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果非空，则在此目录中写入日志文件（当 <code>--logtostderr=true</code> 时不生效）
</p></td>
</tr>

<tr>
<td colspan="2">--log_file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果非空，使用此日志文件（当 <code>--logtostderr=true</code> 时不生效）
</p></td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
定义日志文件可以增长到的最大大小（当 <code>--logtostderr=true</code> 时不生效）。
单位是兆字节。如果值为 0，则最大文件大小不受限制。
</p></td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
日志输出到 stderr 而不是文件。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
用来检查 Machine-ID 的文件列表，用逗号分隔。
使用找到的第一个文件。
</p></td>
</tr>

<tr>
<td colspan="2">--masquerade-all</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果使用纯 iptables 代理，则对通过服务集群 IP 发送的所有流量
进行 SNAT（通常不需要）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--master string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
Kubernetes API 服务器的地址（覆盖 kubeconfig 中的相关值）。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
metrics 服务器要使用的 IP 地址和端口
（设置为 '0.0.0.0:10249' 则使用所有 IPv4 接口，设置为 '[::]:10249' 则使用所有 IPv6 接口）
设置为空则禁用。
如果配置文件由 <code>--config</code> 指定，则忽略此参数。
</p>
</td>
</tr>

<tr>
<td colspan="2">--nodeport-addresses strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
一个字符串值，指定用于 NodePort 服务的地址。
值可以是有效的 IP 块（例如 1.2.3.0/24, 1.2.3.4/32）。
默认的空字符串切片（[]）表示使用所有本地地址。
如果配置文件由 <code>--config</code> 指定，则忽略此参数。
</p>
</td>
</tr>

<tr>
<td colspan="2">--one_output</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果为 true，则仅将日志写入其本身的严重性级别
（而不是写入每个较低的严重性级别；当 <code>--logtostderr=true</code> 时不生效）。
</p></td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
kube-proxy 进程中的 oom-score-adj 值，必须在 [-1000,1000] 范围内。
如果配置文件由 <code>--config</code> 指定，则忽略此参数。
</p>
</td>
</tr>

<tr>
<td colspan="2">--pod-bridge-interface string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
集群中的一个桥接接口名称。
Kube-proxy 将来自与该值匹配的桥接接口的流量视为本地流量。
如果 DetectLocalMode 设置为 BridgeInterface，则应设置该参数。
</td>
</tr>

<tr>
<td colspan="2">--pod-interface-name-prefix string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
集群中的一个接口前缀。
Kube-proxy 将来自与给定前缀匹配的接口的流量视为本地流量。
如果 DetectLocalMode 设置为 InterfaceNamePrefix，则应设置该参数。
</td>
</tr>

<tr>
<td colspan="2">--profiling</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果为 true，则通过 Web 接口 <code>/debug/pprof</code> 启用性能分析。
如果配置文件由 <code>--config</code> 指定，则忽略此参数。
</p>
</td>
</tr>

<tr>
<td colspan="2">--proxy-mode ProxyMode</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
使用哪种代理模式：在 Linux 上可以是 'iptables'（默认）或 'ipvs'。
在 Windows 上唯一支持的值是 'kernelspace'。
如果配置文件由 <code>--config</code> 指定，则忽略此参数。
</p>
</td>
</tr>

<tr>
<td colspan="2">--proxy-port-range port-range</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
可以用来代理服务流量的主机端口范围（包括'起始端口-结束端口'、
'单个端口'、'起始端口+偏移'几种形式）。
如果未指定或者设置为 0（或 0-0），则随机选择端口。
</p>
</td>
</tr>

<tr>
<td colspan="2">--show-hidden-metrics-for-version string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
要显示隐藏指标的先前版本。
仅先前的次要版本有意义，不允许其他值。
格式为 &lt;major&gt;.&lt;minor&gt;，例如 '1.16'。
这种格式的目的是确保你有机会注意到下一个发行版是否隐藏了其他指标，
而不是在之后将其永久删除时感到惊讶。
如果配置文件由 <code>--config</code> 指定，则忽略此参数。
</p>
</td>
</tr>

<tr>
<td colspan="2">--skip_headers</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果为 true，则避免在日志消息中使用头部前缀
</p></td>
</tr>

<tr>
<td colspan="2">--skip_log_headers</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果为 true，则在打开日志文件时避免使用头部（当 <code>--logtostderr=true</code> 时不生效）
</p></td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
当写入到文件或 stderr 时设置严重程度达到或超过此阈值的日志输出到 stderr
（当 <code>--logtostderr=true</code> 或 <code>--alsologtostderr=false</code> 时不生效）。
</p></td>
</tr>

<tr>
<td colspan="2">-v, --v int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
设置日志级别详细程度的数值。
</p></td>
</tr>

<tr>
<td colspan="2">--version version[=true]</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
打印版本信息并退出。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
以逗号分割的 pattern=N 设置的列表，用于文件过滤日志
</p></td>
</tr>

<tr>
<td colspan="2">--write-config-to string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果设置，将默认配置信息写入此文件并退出。
</p>
</td>
</tr>

</tbody>
</table>

