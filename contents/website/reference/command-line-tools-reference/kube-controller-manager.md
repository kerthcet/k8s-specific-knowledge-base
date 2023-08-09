---
title: kube-controller-manager
content_type: tool-reference
weight: 30
---

## {{% heading "synopsis" %}}

Kubernetes 控制器管理器是一个守护进程，内嵌随 Kubernetes 一起发布的核心控制回路。
在机器人和自动化的应用中，控制回路是一个永不休止的循环，用于调节系统状态。
在 Kubernetes 中，每个控制器是一个控制回路，通过 API 服务器监视集群的共享状态，
并尝试进行更改以将当前状态转为期望状态。
目前，Kubernetes 自带的控制器例子包括副本控制器、节点控制器、命名空间控制器和服务账号控制器等。

```
kube-controller-manager [flags]
```

## {{% heading "options" %}}

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--allocate-node-cidrs</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
基于云驱动来为 Pod 分配和设置子网掩码。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<p>
从度量值标签到准许值列表的映射。键名的格式为&lt;MetricName&gt;,&lt;LabelName&gt;。
准许值的格式为&lt;allowed_value&gt;,&lt;allowed_value&gt;...。
例如，<code>metric1,label1='v1,v2,v3', metric1,label2='v1,v2,v3',
metric2,label='v1,v2,v3'</code>。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
协调器（reconciler）在相邻两次对存储卷进行挂载和解除挂载操作之间的等待时间。
此时长必须长于 1 秒钟。此值设置为大于默认值时，可能导致存储卷无法与 Pod 匹配。
</td>
</tr>

<tr>
<td colspan="2">--authentication-kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
此标志值为一个 kubeconfig 文件的路径名。该文件中包含与某 Kubernetes “核心”
服务器相关的信息，并支持足够的权限以创建 tokenreviews.authentication.k8s.io。
此选项是可选的。如果设置为空值，则所有令牌请求都会被认作匿名请求，
Kubernetes 也不再在集群中查找客户端的 CA 证书信息。
</td>
</tr>

<tr>
<td colspan="2">--authentication-skip-lookup</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
此值为 false 时，通过 authentication-kubeconfig
参数所指定的文件会被用来检索集群中缺失的身份认证配置信息。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对 Webhook 令牌认证设施返回结果的缓存时长。
</td>
</tr>

<tr>
<td colspan="2">--authentication-tolerate-lookup-failure</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
此值为 true 时，即使无法从集群中检索到缺失的身份认证配置信息也无大碍。
需要注意的是，这样设置可能导致所有请求都被视作匿名请求。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
鉴权过程中会忽略的一个 HTTP 路径列表。
换言之，控制器管理器会对列表中路径的访问进行授权，并且无须征得
Kubernetes “核心” 服务器同意。
</td>
</tr>

<tr>
<td colspan="2">--authorization-kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 Kubernetes “核心” 服务器信息的 kubeconfig 文件路径，
所包含信息具有创建 subjectaccessreviews.authorization.k8s.io 的足够权限。
此参数是可选的。如果配置为空字符串，未被鉴权模块所忽略的请求都会被禁止。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对 Webhook 形式鉴权组件所返回的“已授权（Authorized）”响应的缓存时长。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对 Webhook 形式鉴权组件所返回的“未授权（Unauthorized）”响应的缓存时长。
</td>
</tr>

<tr>
<td colspan="2">--azure-container-registry-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
指向包含 Azure 容器仓库配置信息的文件的路径名。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
针对 <code>--secure-port</code> 端口上请求执行监听操作的 IP 地址。
所对应的网络接口必须从集群中其它位置可访问（含命令行及 Web 客户端）。
如果此值为空或者设定为非特定地址（<code>0.0.0.0</code> 或 <code>::</code>），
意味着所有网络接口都在监听范围。
</td>
</tr>

<tr>
<td colspan="2">--cert-dir string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
TLS 证书所在的目录。如果提供了 <code>--tls-cert-file</code> 和
<code>--tls-private-key-file</code>，此标志会被忽略。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
要使用的 CIDR 分配器类型。
</td>
</tr>

<tr>
<td colspan="2">--client-ca-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如果设置了此标志，对于所有能够提供客户端证书的请求，若该证书由
<code>--client-ca-file</code> 中所给机构之一签署，
则该请求会被成功认证为客户端证书中 CommonName 所标识的实体。
</td>
</tr>

<tr>
<td colspan="2">--cloud-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
云驱动程序配置文件的路径。空字符串表示没有配置文件。
</td>
</tr>

<tr>
<td colspan="2">--cloud-provider string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
云服务的提供者。空字符串表示没有对应的提供者（驱动）。
</td>
</tr>

<tr>
<td colspan="2">--cluster-cidr string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
集群中 Pod 的 CIDR 范围。要求 <code>--allocate-node-cidrs</code> 标志为 true。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
集群实例的前缀。
</td>
</tr>

<tr>
<td colspan="2">--cluster-signing-cert-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 PEM 编码格式的 X509 CA 证书的文件名。该证书用来发放集群范围的证书。
如果设置了此标志，则不能指定更具体的 <code>--cluster-signing-*</code> 标志。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
所签名证书的有效期限。每个 CSR 可以通过设置 <code>spec.expirationSeconds</code> 来请求更短的证书。
</td>
</tr>

<tr>
<td colspan="2">--cluster-signing-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 PEM 编码的 RSA 或 ECDSA 私钥的文件名。该私钥用来对集群范围证书签名。
若指定了此选项，则不可再设置 <code>--cluster-signing-*</code> 参数。
</td>
</tr>

<tr>
<td colspan="2">--cluster-signing-kube-apiserver-client-cert-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 PEM 编码的 X509 CA 证书的文件名，
该证书用于为 kubernetes.io/kube-apiserver-client 签署者颁发证书。
如果指定，则不得设置 <code>--cluster-signing-{cert,key}-file</code>。
</td>
</tr>

<tr>
<td colspan="2">--cluster-signing-kube-apiserver-client-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 PEM 编码的 RSA 或 ECDSA 私钥的文件名，
该私钥用于为 kubernetes.io/kube-apiserver-client 签署者签名证书。
如果指定，则不得设置 <code>--cluster-signing-{cert,key}-file</code>。
</td>
</tr>

<tr>
<td colspan="2">--cluster-signing-kubelet-client-cert-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 PEM 编码的 X509 CA 证书的文件名，
该证书用于为 kubernetes.io/kube-apiserver-client-kubelet 签署者颁发证书。
如果指定，则不得设置 <code>--cluster-signing-{cert,key}-file</code>。
</td>
</tr>

<tr>
<td colspan="2">--cluster-signing-kubelet-client-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 PEM 编码的 RSA 或 ECDSA 私钥的文件名，
该私钥用于为 kubernetes.io/kube-apiserver-client-kubelet 签署者签名证书。
如果指定，则不得设置 <code>--cluster-signing-{cert,key}-file</code>。
</td>
</tr>

<tr>
<td colspan="2">--cluster-signing-kubelet-serving-cert-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 PEM 编码的 X509 CA 证书的文件名，
该证书用于为 kubernetes.io/kubelet-serving 签署者颁发证书。
如果指定，则不得设置 </code>--cluster-signing-{cert,key}-file</code>。
</td>
</tr>

<tr>
<td colspan="2">--cluster-signing-kubelet-serving-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 PEM 编码的 RSA或ECDSA 私钥的文件名，
该私钥用于对 kubernetes.io/kubelet-serving 签署者的证书进行签名。
如果指定，则不得设置 <code>--cluster-signing-{cert,key}-file</code>。
</td>
</tr>

<tr>
<td colspan="2">--cluster-signing-legacy-unknown-cert-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 PEM 编码的 X509 CA 证书的文件名，
用于为 kubernetes.io/legacy-unknown 签署者颁发证书。
如果指定，则不得设置 <code>--cluster-signing-{cert,key}-file</code>。
</td>
</tr>

<tr>
<td colspan="2">--cluster-signing-legacy-unknown-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 PEM 编码的 RSA 或 ECDSA 私钥的文件名，
用于为 kubernetes.io/legacy-unknown 签署者签名证书。
如果指定，则不得设置 <code>--cluster-signing-{cert,key}-file</code>。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可以并发同步的 Deployment 对象个数。数值越大意味着对 Deployment 的响应越及时，
同时也意味着更大的 CPU（和网络带宽）压力。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可以并发执行的 Endpoints 同步操作个数。数值越大意味着更快的 Endpoints 更新操作，
同时也意味着更大的 CPU （和网络）压力。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可以并发执行的 EphemeralVolume 同步操作个数。数值越大意味着更快的 EphemeralVolume 更新操作，
同时也意味着更大的 CPU （和网络）压力。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可以并发同步的垃圾收集工作线程个数。
</td>
</tr>

<tr>
<td>
</td>
<td style="line-height: 130%; word-wrap: break-word;">
<p>
允许并发执行的、对水平 Pod 自动扩缩器对象进行同步的数量。
更大的数字 = 响应更快的水平 Pod 自动缩放器对象处理，但需要更高的 CPU（和网络）负载。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可以并发同步的 Namespace 对象个数。较大的数值意味着更快的名字空间终结操作，
不过也意味着更多的 CPU （和网络）占用。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
可以并发同步的副本控制器对象个数。较大的数值意味着更快的副本管理操作，
不过也意味着更多的 CPU （和网络）占用。
</p></td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可以并发同步的 ReplicaSet 个数。数值越大意味着副本管理的响应速度越快，
同时也意味着更多的 CPU （和网络）占用。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可以并发同步的 ResourceQuota 对象个数。数值越大，配额管理的响应速度越快，
不过对 CPU （和网络）的占用也越高。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可以并发执行的服务端点同步操作个数。数值越大，端点片段（Endpoint Slice）
的更新速度越快，不过对 CPU （和网络）的占用也越高。默认值为 5。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可以并发同步的 Service 对象个数。数值越大，服务管理的响应速度越快，
不过对 CPU （和网络）的占用也越高。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可以并发同步的服务账号令牌对象个数。数值越大，令牌生成的速度越快，
不过对 CPU （和网络）的占用也越高。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可以并发同步的 StatefulSet 对象个数。数值越大，StatefulSet 管理的响应速度越快，
不过对 CPU （和网络）的占用也越高。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可以并发同步的 TTL-after-finished 控制器线程个数。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
决定是否由 <code>--allocate-node-cidrs</code> 所分配的 CIDR 要通过云驱动程序来配置。
</td>
</tr>

<tr>
<td colspan="2">--contention-profiling</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在启用了性能分析（profiling）时，也启用锁竞争情况分析。
</td>
</tr>

<tr>
<td colspan="2">--controller-start-interval duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在两次启动控制器管理器之间的时间间隔。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
要启用的控制器列表。<code>*</code> 表示启用所有默认启用的控制器；
<code>foo</code> 启用名为 foo 的控制器；
<code>-foo</code> 表示禁用名为 foo 的控制器。<br/>
控制器的全集：attachdetach、bootstrapsigner、cloud-node-lifecycle、clusterrole-aggregation、cronjob、csrapproving、csrcleaner、csrsigning、daemonset、deployment、disruption、endpoint、endpointslice、endpointslicemirroring、ephemeral-volume、garbagecollector、horizontalpodautoscaling、job、namespace、nodeipam、nodelifecycle、persistentvolume-binder、persistentvolume-expander、podgc、pv-protection、pvc-protection、replicaset、replicationcontroller、resourcequota、root-ca-cert-publisher、route、service、serviceaccount、serviceaccount-token、statefulset、tokencleaner、ttl、ttl-after-finished<br/>
默认禁用的控制器有：bootstrapsigner 和 tokencleaner。</td>
</tr>

<tr>
<td colspan="2">--disable-attach-detach-reconcile-sync</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
禁用卷挂接/解挂调节器的同步。禁用此同步可能导致卷存储与 Pod 之间出现错位。
请小心使用。
</td>
</tr>

<tr>
<td colspan="2">--disabled-metrics strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
此标志提供对行为异常的度量值的防控措施。你必须提供度量值的完全限定名称才能将其禁用。
<B>声明</B>：禁用度量值的操作比显示隐藏度量值的操作优先级高。
</p></td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在环境允许的情况下启用动态卷制备。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
启用通用垃圾收集器。必须与 kube-apiserver 中对应的标志一致。
</td>
</tr>

<tr>
<td colspan="2">--enable-hostpath-provisioner</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在没有云驱动程序的情况下，启用 HostPath 持久卷的制备。
此参数便于对卷供应功能进行开发和测试。HostPath 卷的制备并非受支持的功能特性，
在多节点的集群中也无法工作，因此除了开发和测试环境中不应使用 HostPath 卷的制备。
</td>
</tr>

<tr>
<td colspan="2">--enable-leader-migration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
此标志决定是否启用控制器领导者迁移。
</p></td>
</tr>

<tr>
<td colspan="2">--endpoint-updates-batch-period duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
端点（Endpoint）批量更新周期时长。对 Pod 变更的处理会被延迟，
以便将其与即将到来的更新操作合并，从而减少端点更新操作次数。
较大的数值意味着端点更新的迟滞时间会增长，也意味着所生成的端点版本个数会变少。
</td>
</tr>

<tr>
<td colspan="2">--endpointslice-updates-batch-period duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
端点片段（Endpoint Slice）批量更新周期时长。对 Pod 变更的处理会被延迟，
以便将其与即将到来的更新操作合并，从而减少端点更新操作次数。
较大的数值意味着端点更新的迟滞时间会增长，也意味着所生成的端点版本个数会变少。
</td>
</tr>

<tr>
<td colspan="2">--external-cloud-volume-plugin string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
当云驱动程序设置为 external 时要使用的插件名称。此字符串可以为空。
只能在云驱动程序为 external 时设置。
目前用来保证节点控制器和卷控制器能够在三种云驱动上正常工作。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td>
<td style="line-height: 130%; word-wrap: break-word;">
<p>
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
WindowsHostNetwork=true|false (ALPHA - 默认值为 true)
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
FlexVolume 插件要搜索第三方卷插件的目录路径全名。
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kube-controller-manager 的帮助信息。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
Pod 启动之后可以忽略 CPU 采样值的时长。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
自动扩缩程序的回溯时长。
自动扩缩程序不会基于在给定的时长内所建议的规模对负载执行缩容操作。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
Pod 启动之后，在此值所给定的时长内，就绪状态的变化都不会作为初始的就绪状态。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
水平 Pod 扩缩器对 Pod 数目执行同步操作的周期。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
此值为目标值与实际值的比值与 1.0 的差值。只有超过此标志所设的阈值时，
HPA 才会考虑执行缩放操作。
</td>
</tr>

<tr>
<td colspan="2">--http2-max-streams-per-connection int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
服务器为客户端所设置的 HTTP/2 连接中流式连接个数上限。
此值为 0 表示采用 Go 语言库所设置的默认值。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
与 Kubernetes API 服务器通信时突发峰值请求个数上限。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
向 API 服务器发送请求时使用的内容类型（Content-Type）。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
与 API 服务器通信时每秒请求数（QPS）限制。
</td>
</tr>

<tr>
<td colspan="2">--kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
指向 kubeconfig 文件的路径。该文件中包含主控节点位置以及鉴权凭据信息。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
节点控制器在执行 Pod 驱逐操作逻辑时，
基于此标志所设置的节点个数阈值来判断所在集群是否为大规模集群。
当集群规模小于等于此规模时，
<code>--secondary-node-eviction-rate</code> 会被隐式重设为 0。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在执行主循环之前，启动领导选举（Leader Election）客户端，并尝试获得领导者身份。
在运行多副本组件时启用此标志有助于提高可用性。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对于未获得领导者身份的节点，
在探测到领导者身份需要更迭时需要等待此标志所设置的时长，
才能尝试去获得曾经是领导者但尚未续约的席位。本质上，
这个时长也是现有领导者节点在被其他候选节点替代之前可以停止的最长时长。
只有集群启用了领导者选举机制时，此标志才起作用。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
当前执行领导者角色的节点在被停止履行领导职责之前可多次尝试续约领导者身份；
此标志给出相邻两次尝试之间的间歇时长。
此值必须小于租期时长（Lease Duration）。
仅在集群启用了领导者选举时有效。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在领导者选举期间用于锁定的资源对象的类型。 支持的选项为
<code>leases</code>、<code>endpointsleases</code> 和 <code>configmapsleases</code>。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在领导者选举期间，用来执行锁操作的资源对象名称。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在领导者选举期间，用来执行锁操作的资源对象的名字空间。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
尝试获得领导者身份时，客户端在相邻两次尝试之间要等待的时长。
此标志仅在启用了领导者选举的集群中起作用。
</td>
</tr>

<tr>
<td colspan="2">--leader-migration-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
控制器领导者迁移所用的配置文件路径。
此值为空意味着使用控制器管理器的默认配置。
配置文件应该是 <code>controllermanager.config.k8s.io</code> 组、
<code>v1alpha1</code> 版本的 <code>LeaderMigrationConfiguration</code> 结构。
</p></td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
将内存中日志数据清除到日志文件中时，相邻两次清除操作之间最大间隔秒数。
</td>
</tr>

<tr>
</tr>

<tr>
<td>
</td>
<td style="line-height: 130%; word-wrap: break-word;">
<p>
设置日志格式。允许的格式：&quot;text&quot;。
</p>
</td>
</tr>

<tr>
<td colspan="2">--master string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
Kubernetes API 服务器的地址。此值会覆盖 kubeconfig 文件中所给的地址。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
每个 EndpointSlice 中可以添加的端点个数上限。每个片段中端点个数越多，
得到的片段个数越少，但是片段的规模会变得更大。默认值为 100。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
自省程序的重新同步时隔下限。实际时隔长度会在 <code>min-resync-period</code> 和
<code>2 * min-resync-period</code> 之间。
</td>
</tr>

<tr>
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
EndpointSliceMirroring 控制器将同时执行的服务端点同步操作数。
较大的数量 = 更快的端点切片更新，但 CPU（和网络）负载更多。 默认为 5。
</td>
</tr>

<tr>
<td colspan="2">--mirroring-endpointslice-updates-batch-period duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
EndpointSlice 的长度更新了 EndpointSliceMirroring 控制器的批处理周期。
EndpointSlice 更改的处理将延迟此持续时间，
以使它们与潜在的即将进行的更新结合在一起，并减少 EndpointSlice 更新的总数。 
较大的数量 = 较高的端点编程延迟，但是生成的端点修订版本数量较少
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
EndpointSliceMirroring 控制器将添加到 EndpointSlice 的最大端点数。
每个分片的端点越多，端点分片越少，但资源越大。默认为 100。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对名字空间对象进行同步的周期。
</td>
</tr>

<tr>
<td colspan="2">--node-cidr-mask-size int32</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
集群中节点 CIDR 的掩码长度。对 IPv4 而言默认为 24；对 IPv6 而言默认为 64。
</td>
</tr>

<tr>
<td colspan="2">--node-cidr-mask-size-ipv4 int32</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在双堆栈（同时支持 IPv4 和 IPv6）的集群中，节点 IPV4 CIDR 掩码长度。默认为 24。
</td>
</tr>

<tr>
<td colspan="2">--node-cidr-mask-size-ipv6 int32</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在双堆栈（同时支持 IPv4 和 IPv6）的集群中，节点 IPv6 CIDR 掩码长度。默认为 64。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
当某区域健康时，在节点故障的情况下每秒删除 Pods 的节点数。
请参阅 <code>--unhealthy-zone-threshold</code>
以了解“健康”的判定标准。
这里的区域（zone）在集群并不跨多个区域时指的是整个集群。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在将一个 Node 标记为不健康之前允许其无响应的时长上限。
必须比 kubelet 的 nodeStatusUpdateFrequency 大 N 倍；
这里 N 指的是 kubelet 发送节点状态的重试次数。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
节点控制器对节点状态进行同步的重复周期。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在节点启动期间，节点可以处于无响应状态；
但超出此标志所设置的时长仍然无响应则该节点被标记为不健康。
</td>
</tr>

<tr>
<td colspan="2">--permit-address-sharing</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
如果此标志为 true，则在绑定端口时使用 <code>SO_REUSEADDR</code>。
这就意味着可以同时绑定到 <code>0.0.0.0</code> 和特定的 IP 地址，
并且避免等待内核释放处于 <code>TIME_WAITE</code> 状态的套接字。[默认值=false]。
</p></td>
</tr>


<tr>
<td colspan="2">--permit-port-sharing</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如果为 true，则在绑定端口时将使用 <code>SO_REUSEPORT</code>，
这允许多个实例在同一地址和端口上进行绑定。[默认值=false]。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
通过位于 <code>host:port/debug/pprof/</code> 的 Web 接口启用性能分析。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
NFS 清洗 Pod 在清洗用过的卷时，根据此标志所设置的秒数，
为每清洗 1 GiB 数据增加对应超时时长，作为 activeDeadlineSeconds。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对于 HostPath 回收器 Pod，设置其 activeDeadlineSeconds 参数下限。
此参数仅用于开发和测试目的，不适合在多节点集群中使用。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
NFS 回收器 Pod 要使用的 activeDeadlineSeconds 参数下限。
</td>
</tr>

<tr>
<td colspan="2">--pv-recycler-pod-template-filepath-hostpath string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对 HostPath 持久卷进行回收利用时，用作模板的 Pod 定义文件所在路径。
此标志仅用于开发和测试目的，不适合多节点集群中使用。
</td>
</tr>

<tr>
<td colspan="2">--pv-recycler-pod-template-filepath-nfs string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对 NFS 卷执行回收利用时，用作模板的 Pod 定义文件所在路径。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
HostPath 清洗器 Pod 在清洗对应类型持久卷时，为每 GiB 数据增加此标志所设置的秒数，
作为其 activeDeadlineSeconds 参数。此标志仅用于开发和测试环境，不适合多节点集群环境。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
持久卷（PV）和持久卷申领（PVC）对象的同步周期。
</td>
</tr>

<tr>
<td colspan="2">--requestheader-allowed-names strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
标志值是客户端证书中的 Common Names 列表。其中所列的名称可以通过
<code>--requestheader-username-headers</code> 所设置的 HTTP 头部来提供用户名。
如果此标志值为空表，则被 <code>--requestheader-client-ca-file</code>
中机构所验证过的所有客户端证书都是允许的。
</td>
</tr>

<tr>
<td colspan="2">--requestheader-client-ca-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
根证书包文件名。在信任通过 <code>--requestheader-username-headers</code>
所指定的任何用户名之前，要使用这里的证书来检查请求中的客户证书。
警告：一般不要依赖对请求所作的鉴权结果。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
要插入的请求头部前缀。建议使用 <code>X-Remote-Exra-</code>。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用来检查用户组名的请求头部名称列表。建议使用 <code>X-Remote-Group</code>。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用来检查用户名的请求头部名称列表。建议使用 <code>X-Remote-User</code>。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对系统中配额用量信息进行同步的周期。
</td>
</tr>

<tr>
<td colspan="2">--root-ca-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
如果此标志非空，则在服务账号的令牌 Secret 中会包含此根证书机构。
所指定标志值必须是一个合法的 PEM 编码的 CA 证书包。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
对云驱动为节点所创建的路由信息进行调解的周期。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
当一个区域不健康造成节点失效时，每秒钟从此标志所给的节点上删除 Pod 的节点个数。
参见 <code>--unhealthy-zone-threshold</code> 以了解“健康与否”的判定标准。
在只有一个区域的集群中，区域指的是整个集群。如果集群规模小于
<code>--large-cluster-size-threshold</code> 所设置的节点个数时，
此值被隐式地重设为 0。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在此端口上提供 HTTPS 身份认证和鉴权操作。若此标志值为 0，则不提供 HTTPS 服务。
</td>
</tr>

<tr>
<td colspan="2">--service-account-private-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 PEM 编码的 RSA 或 ECDSA 私钥数据的文件名，这些私钥用来对服务账号令牌签名。
</td>
</tr>

<tr>
<td colspan="2">--service-cluster-ip-range string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
集群中 Service 对象的 CIDR 范围。要求 <code>--allocate-node-cidrs</code> 标志为 true。
</td>
</tr>

<tr>
<td colspan="2">--show-hidden-metrics-for-version string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
你希望展示隐藏度量值的上一个版本。只有上一个次版本号有意义，其他值都是不允许的。
字符串格式为 "&lt;major&gt;.&lt;minor&gt;"。例如："1.16"。
此格式的目的是确保你能够有机会注意到下一个版本隐藏了一些额外的度量值，
而不是在更新版本中某些度量值被彻底删除时措手不及。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
在已终止 Pod 垃圾收集器删除已终止 Pod 之前，可以保留的已终止 Pod 的个数上限。
若此值小于等于 0，则相当于禁止垃圾回收已终止的 Pod。
</td>
</tr>

<tr>
<td colspan="2">--tls-cert-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含 HTTPS 所用的默认 X509 证书的文件。如果有 CA 证书，会被串接在服务器证书之后。
若启用了 HTTPS 服务且 <code>--tls-cert-file</code> 和 <code>--tls-private-key-file</code>
标志未设置，
则为节点的公开地址生成自签名的证书和密钥，并保存到 <code>--cert-dir</code>
所给的目录中。
</td>
</tr>

<tr>
<td colspan="2">--tls-cipher-suites strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
供服务器使用的加密包的逗号分隔列表。若忽略此标志，则使用 Go 语言默认的加密包。<br/>
可选值包括：TLS_AES_128_GCM_SHA256、TLS_AES_256_GCM_SHA384、TLS_CHACHA20_POLY1305_SHA256、TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA、TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256、TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA、TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384、TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305、TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256、TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA、TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256、TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA、TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384、TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305、TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256、TLS_RSA_WITH_AES_128_CBC_SHA、TLS_RSA_WITH_AES_128_GCM_SHA256、TLS_RSA_WITH_AES_256_CBC_SHA、TLS_RSA_WITH_AES_256_GCM_SHA384。
<br/>不安全的值: TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256、TLS_ECDHE_ECDSA_WITH_RC4_128_SHA、TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA、TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256、TLS_ECDHE_RSA_WITH_RC4_128_SHA、TLS_RSA_WITH_3DES_EDE_CBC_SHA、TLS_RSA_WITH_AES_128_CBC_SHA256、TLS_RSA_WITH_RC4_128_SHA。
</td>
</tr>

<tr>
<td colspan="2">--tls-min-version string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
可支持的最低 TLS 版本。可选值包括：
“VersionTLS10”、“VersionTLS11”、“VersionTLS12”、“VersionTLS13”。
</td>
</tr>

<tr>
<td colspan="2">--tls-private-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
包含与 <code>--tls-cert-file</code> 对应的默认 X509 私钥的文件。
</td>
</tr>

<tr>
<td colspan="2">--tls-sni-cert-key string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
X509 证书和私钥文件路径的耦对。作为可选项，可以添加域名模式的列表，
其中每个域名模式都是可以带通配片段前缀的全限定域名（FQDN）。
域名模式也可以使用 IP 地址字符串，
不过只有 API 服务器在所给 IP 地址上对客户端可见时才可以使用 IP 地址。
在未提供域名模式时，从证书中提取域名。
如果有非通配方式的匹配，则优先于通配方式的匹配；显式的域名模式优先于提取的域名。
当存在多个密钥/证书耦对时，可以多次使用 <code>--tls-sni-cert-key</code> 标志。
例如：<code>example.crt,example.key</code> 或 <code>foo.crt,foo.key:\*.foo.com,foo.com</code>。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
仅当给定区域中处于非就绪状态的节点（最少 3 个）的占比高于此值时，
才将该区域视为不健康。
</td>
</tr>

<tr>
<td colspan="2">--use-service-account-credentials</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
当此标志为 true 时，为每个控制器单独使用服务账号凭据。
</td>
</tr>

<tr>
<td colspan="2">-v, --v int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
日志级别详细程度取值。
</td>
</tr>

<tr>
<td colspan="2">--version version[=true]</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
打印版本信息之后退出。
</td>
</tr>

<tr>
<td colspan="2">--vmodule pattern=N,...</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
由逗号分隔的列表，每一项都是 pattern=N 格式，用来执行根据文件过滤的日志行为（仅适用于 text 日志格式）。
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
此标志为 false 时，禁止本地回路 IP 地址和 <code>--volume-host-cidr-denylist</code>
中所指定的 CIDR 范围。
</td>
</tr>

<tr>
<td colspan="2">--volume-host-cidr-denylist strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用逗号分隔的一个 CIDR 范围列表，禁止使用这些地址上的卷插件。
</td>
</tr>

</tbody>
</table>

