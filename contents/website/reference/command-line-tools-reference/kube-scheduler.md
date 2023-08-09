---
title: kube-scheduler
content_type: tool-reference
weight: 30
---


## {{% heading "synopsis" %}}

Kubernetes 调度器是一个控制面进程，负责将 Pods 指派到节点上。
调度器基于约束和可用资源为调度队列中每个 Pod 确定其可合法放置的节点。
调度器之后对所有合法的节点进行排序，将 Pod 绑定到一个合适的节点。
在同一个集群中可以使用多个不同的调度器；kube-scheduler 是其参考实现。
参阅[调度](/zh-cn/docs/concepts/scheduling-eviction/)以获得关于调度和
kube-scheduler 组件的更多信息。

```
kube-scheduler [flags]
```

## {{% heading "options" %}}


<table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>


<tr>
<td colspan="2">--allow-metric-labels stringToString&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
这个键值映射表设置度量标签所允许设置的值。
其中键的格式是 &lt;MetricName&gt;,&lt;LabelName&gt;。
值的格式是 &lt;allowed_value&gt;,&lt;allowed_value&gt;。
例如：metric1,label1='v1,v2,v3', metric1,label2='v1,v2,v3' metric2,label1='v1,v2,v3'。
</td>
</tr>

<tr>
<td colspan="2">--authentication-kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
指向具有足够权限以创建 <code>tokenaccessreviews.authentication.k8s.io</code> 的
Kubernetes 核心服务器的 kubeconfig 文件。
这是可选的。如果为空，则所有令牌请求均被视为匿名请求，并且不会在集群中查找任何客户端 CA。
</td>
</tr>

<tr>
<td colspan="2">--authentication-skip-lookup</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如果为 false，则 authentication-kubeconfig 将用于从集群中查找缺少的身份验证配置。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
缓存来自 Webhook 令牌身份验证器的响应的持续时间。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如果为 true，则无法从集群中查找缺少的身份验证配置是致命的。
请注意，这可能导致身份验证将所有请求视为匿名。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在授权过程中跳过的 HTTP 路径列表，即在不联系 “core” kubernetes 服务器的情况下被授权的 HTTP 路径。
</td>
</tr>

<tr>
<td colspan="2">--authorization-kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
指向具有足够权限以创建 subjectaccessreviews.authorization.k8s.io 的
Kubernetes 核心服务器的 kubeconfig 文件。这是可选的。
如果为空，则所有未被鉴权机制略过的请求都会被禁止。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
缓存来自 Webhook 授权者的 “authorized” 响应的持续时间。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
缓存来自 Webhook 授权者的 “unauthorized” 响应的持续时间。
</td>
</tr>

<tr>
<td colspan="2">--azure-container-registry-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 Azure 容器仓库配置信息的文件的路径。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
监听 --secure-port 端口的 IP 地址。
集群的其余部分以及 CLI/ Web 客户端必须可以访问关联的接口。
如果为空，将使用所有接口（0.0.0.0 表示使用所有 IPv4 接口，“::” 表示使用所有 IPv6 接口）。
如果为空或未指定地址 (0.0.0.0 或 ::)，所有接口将被使用。
</td>
</tr>

<tr>
<td colspan="2">--cert-dir string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
TLS 证书所在的目录。如果提供了--tls-cert-file 和 --tls private-key-file，
则将忽略此参数。
</td>
</tr>

<tr>
<td colspan="2">--client-ca-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如果已设置，由 client-ca-file 中的证书机构签名的客户端证书的任何请求都将使用
与客户端证书的 CommonName 对应的身份进行身份验证。
</td>
</tr>

<tr>
<td colspan="2">--config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
配置文件的路径。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
已弃用: 如果启用了性能分析，则启用锁竞争分析。
如果 --config 指定了一个配置文件，那么这个参数将被忽略。
</td>
</tr>

<tr>
<td colspan="2">--disabled-metrics strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
这个标志提供了一个规避不良指标的选项。你必须提供完整的指标名称才能禁用它。
免责声明：禁用指标的优先级比显示隐藏的指标更高。
</td>
</tr>


<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
一组 key=value 对，描述了 alpha/experimental 特性门控开关。选项包括：<br/>
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
WindowsHostNetwork=true|false (ALPHA - 默认值为 true)
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kube-scheduler 帮助命令
</td>
</tr>

<tr>
<td colspan="2">--http2-max-streams-per-connection int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
服务器为客户端提供的 HTTP/2 连接最大限制。零表示使用 Golang 的默认值。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
已弃用: 与 kubernetes API 通信时使用的突发请求个数限值。
如果 --config 指定了一个配置文件，那么这个参数将被忽略。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
已弃用: 发送到 API 服务器的请求的内容类型。
如果 --config 指定了一个配置文件，那么这个参数将被忽略。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
已弃用: 与 kubernetes apiserver 通信时要使用的 QPS
如果 --config 指定了一个配置文件，那么这个参数将被忽略。
</td>
</tr>

<tr>
<td colspan="2">--kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
已弃用: 包含鉴权和主节点位置信息的 kubeconfig 文件的路径。
如果 --config 指定了一个配置文件，那么这个参数将被忽略。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在执行主循环之前，开始领导者选举并选出领导者。
使用多副本来实现高可用性时，可启用此标志。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
非领导者候选人在观察到领导者更新后将等待直到试图获得领导但未更新的领导者职位的等待时间。
这实际上是领导者在被另一位候选人替代之前可以停止的最大持续时间。
该情况仅在启用了领导者选举的情况下才适用。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
领导者尝试在停止领导之前更新领导职位的间隔时间。该时间必须小于租赁期限。
仅在启用了领导者选举的情况下才适用。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在领导者选举期间用于锁定的资源对象的类型。支持的选项有 `leases`、`endpointleases` 和 `configmapsleases`。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在领导者选举期间用于锁定的资源对象的名称。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在领导者选举期间用于锁定的资源对象的命名空间。
</td>
</tr>

<tr>
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
客户应在尝试获取和更新领导之间等待的时间。仅在启用了领导者选举的情况下才适用。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
已弃用: 定义锁对象的名称。将被删除以便使用 <code>--leader-elect-resource-name</code>。
如果 --config 指定了一个配置文件，那么这个参数将被忽略。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
已弃用: 定义锁对象的命名空间。将被删除以便使用 <code>leader-elect-resource-namespace</code>。
如果 --config 指定了一个配置文件，那么这个参数将被忽略。
</td>
</tr>


<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
两次日志刷新之间的最大秒数。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置日志格式。可选格式：“text”。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
日志记录到标准错误输出而不是文件。
</td>
</tr>

<tr>
<td colspan="2">--master string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
Kubernetes API 服务器的地址（覆盖 kubeconfig 中的任何值）。
</td>
</tr>

<tr>
<td colspan="2">--permit-address-sharing</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如果为 true，在绑定端口时将使用 SO_REUSEADDR。
这将允许同时绑定诸如 0.0.0.0 这类通配符 IP和特定 IP，
并且它避免等待内核释放处于 TIME_WAIT 状态的套接字。
默认值：false
</td>
</tr>

<tr>
<td colspan="2">--permit-port-sharing</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如果此标志为 true，在绑定端口时会使用 SO_REUSEPORT，从而允许不止一个
实例绑定到同一地址和端口。
默认值：false
</td>
</tr>

<tr>

</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
已弃用：Pod 可以在 unschedulablePods 中停留的最长时间。
如果 Pod 在 unschedulablePods 中停留的时间超过此值，则该 pod 将被从
unschedulablePods 移动到 backoffQ 或 activeQ。
此标志已弃用，将在 1.2 中删除。

</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
已弃用: 通过 Web 界面主机启用配置文件：<code>host:port/debug/pprof/</code>。
如果 --config 指定了一个配置文件，这个参数将被忽略。
</td>
</tr>

<tr>
<td colspan="2">--requestheader-allowed-names stringSlice</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
客户端证书通用名称列表，允许在 <code>--requestheader-username-headers</code>
指定的头部中提供用户名。如果为空，则允许任何由
<code>--requestheader-client-ca-file</code> 中证书机构验证的客户端证书。
</td>
</tr>

<tr>
<td colspan="2">--requestheader-client-ca-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在信任 <code>--requestheader-username-headers</code> 指定的头部中的用户名之前
用于验证传入请求上的客户端证书的根证书包。
警告：通常不应假定传入请求已经完成鉴权。
</td>
</tr>

<tr>
<td colspan="2">--requestheader-extra-headers-prefix strings&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
要检查请求头部前缀列表。建议使用 <code>X-Remote-Extra-</code>。
</td>
</tr>

<tr>
<td colspan="2">--requestheader-group-headers strings&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用于检查组的请求头部列表。建议使用 <code>X-Remote-Group</code>。
</td>
</tr>

<tr>
<td colspan="2">--requestheader-username-headers strings&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用于检查用户名的请求头部列表。<code>X-Remote-User</code> 很常用。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
通过身份验证和授权为 HTTPS 服务的端口。如果为 0，则根本不提供 HTTPS。
</td>
</tr>

<tr>
<td colspan="2">--show-hidden-metrics-for-version string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
你希望显式隐藏指标的老版本号。只有较早的此版本号有意义，其它值都是不允许的。
格式为 &lt;主版本&gt;.&lt;此版本&gt;，例如：'1.16'。
此格式的目的是确保你有机会注意到是否下一个发行版本中隐藏了一些额外的指标，
而不是当某些指标在该版本之后被彻底移除时感到震惊。
</td>
</tr>


<tr>
<td colspan="2">--tls-cert-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含默认的 HTTPS x509 证书的文件。（如果有 CA 证书，在服务器证书之后并置）。
如果启用了 HTTPS 服务，并且未提供 <code>--tls-cert-file</code> 和
<code>--tls-private-key-file</code>，则会为公共地址生成一个自签名证书和密钥，
并将其保存到 <code>--cert-dir</code> 指定的目录中。
</td>
</tr>

<tr>
<td colspan="2">--tls-cipher-suites strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
服务器的密码套件列表，以逗号分隔。如果省略，将使用默认的 Go 密码套件。
优先考虑的值：
TLS_AES_128_GCM_SHA256, TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256, TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA, TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305, TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256, TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305, TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256, TLS_RSA_WITH_3DES_EDE_CBC_SHA, TLS_RSA_WITH_AES_128_CBC_SHA, TLS_RSA_WITH_AES_128_GCM_SHA256, TLS_RSA_WITH_AES_256_CBC_SHA, TLS_RSA_WITH_AES_256_GCM_SHA384.<br/>
不安全的值：
TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_ECDSA_WITH_RC4_128_SHA, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_RSA_WITH_RC4_128_SHA, TLS_RSA_WITH_AES_128_CBC_SHA256, TLS_RSA_WITH_RC4_128_SHA.
</td>
</tr>

<tr>
<td colspan="2">--tls-min-version string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
支持的最低 TLS 版本。可能的值：VersionTLS10, VersionTLS11, VersionTLS12, VersionTLS13
</td>
</tr>

<tr>
<td colspan="2">--tls-private-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含与 --tls-cert-file 匹配的默认 x509 私钥的文件。
</td>
</tr>

<tr>
<td colspan="2">--tls-sni-cert-key string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
一对 x509 证书和私钥文件路径，也可以包含由全限定域名构成的域名模式列表作为后缀，
并可能带有前缀的通配符段。域名匹配还允许是 IP 地址，
但是只有当 apiserver 对客户端请求的 IP 地址可见时，才能使用 IP。
如果未提供域名匹配模式，则提取证书名称。
非通配符匹配优先于通配符匹配，显式域名匹配优先于提取而来的名称。
若有多个密钥/证书对，可多次使用 <code>--tls-sni-cert-key</code>。
例如: "example.crt,example.key" 或者 "foo.crt,foo.key:*.foo.com,foo.com"。
</td>
</tr>

<tr>
<td colspan="2">-v, --v int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置日志级别详细程度的数字
</td>
</tr>

<tr>
<td colspan="2">--version version[=true]</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
打印版本信息并退出。
</td>
</tr>

<tr>
<td colspan="2">--vmodule pattern=N,...</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
以逗号分隔的 “pattern=N” 设置列表，用于文件过滤的日志记录（仅适用于文本日志格式）。
</td>
</tr>

<tr>
<td colspan="2">--write-config-to string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如果设置此参数，将配置值写入此文件并退出。
</td>
</tr>

</tbody>
</table>



