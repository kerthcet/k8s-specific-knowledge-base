---
title: 虚拟 IP 和服务代理
content_type: reference
weight: 50
---


Kubernetes {{< glossary_tooltip text="集群" term_id="cluster" >}}中的每个
{{< glossary_tooltip text="节点" term_id="node" >}}会运行一个
[kube-proxy](/zh-cn/docs/reference/command-line-tools-reference/kube-proxy/)
（除非你已经部署了自己的替换组件来替代 `kube-proxy`）。

`kube-proxy` 组件负责除 `type` 为
[`ExternalName`](/zh-cn/docs/concepts/services-networking/service/#externalname)
以外的{{< glossary_tooltip term_id="service" text="服务">}}，实现**虚拟 IP** 机制。

一个时不时出现的问题是，为什么 Kubernetes 依赖代理将入站流量转发到后端。
其他方案呢？例如，是否可以配置具有多个 A 值（或 IPv6 的 AAAA）的 DNS 记录，
使用轮询域名解析？

使用代理转发方式实现 Service 的原因有以下几个：

* DNS 的实现不遵守记录的 TTL 约定的历史由来已久，在记录过期后可能仍有结果缓存。
* 有些应用只做一次 DNS 查询，然后永久缓存结果。
* 即使应用程序和库进行了适当的重新解析，TTL 取值较低或为零的 DNS 记录可能会给 DNS 带来很大的压力，
  从而变得难以管理。

在下文中，你可以了解到 kube-proxy 各种实现方式的工作原理。
总的来说，你应该注意到，在运行 `kube-proxy` 时，
可能会修改内核级别的规则（例如，可能会创建 iptables 规则），
在某些情况下，这些规则直到重启才会被清理。
因此，运行 kube-proxy 这件事应该只由了解在计算机上使用低级别、特权网络代理服务会带来的后果的管理员执行。
尽管 `kube-proxy` 可执行文件支持 `cleanup` 功能，但这个功能并不是官方特性，因此只能根据具体情况使用。

<a id="example"></a>
本文中的一些细节会引用这样一个例子：
运行了 3 个 {{< glossary_tooltip text="Pod" term_id="pod" >}}
副本的无状态图像处理后端工作负载。
这些副本是可互换的；前端不需要关心它们调用了哪个后端副本。
即使组成这一组后端程序的 Pod 实际上可能会发生变化，
前端客户端不应该也没必要知道，而且也不需要跟踪这一组后端的状态。


## 代理模式 {#proxy-modes}

kube-proxy 会根据不同配置以不同的模式启动。

在 Linux 节点上，kube-proxy 的可用模式是：

[`iptables`](#proxy-mode-iptables)
: kube-proxy 在 Linux 上使用 iptables 配置数据包转发规则的一种模式。

[`ipvs`](#proxy-mode-ipvs)
: kube-proxy 使用 ipvs 配置数据包转发规则的一种模式。

Windows 上的 kube-proxy 只有一种模式可用：

[`kernelspace`](#proxy-mode-kernelspace)
: kube-proxy 在 Windows 内核中配置数据包转发规则的一种模式。

### `iptables` 代理模式 {#proxy-mode-iptables}

**此代理模式仅适用于 Linux 节点。**

在这种模式下，kube-proxy 监视 Kubernetes
{{< glossary_tooltip text="控制平面" term_id="control-plane" >}}，获知对 Service 和 EndpointSlice
{{< glossary_tooltip text="对象" term_id="object" >}}的添加和删除操作。
对于每个 Service，kube-proxy 会添加 iptables 规则，这些规则捕获流向 Service 的 `clusterIP` 和 `port` 的流量，
并将这些流量重定向到 Service 后端集合中的其中之一。
对于每个端点，它会添加指向一个特定后端 Pod 的 iptables 规则。

默认情况下，iptables 模式下的 kube-proxy 会随机选择一个后端。

使用 iptables 处理流量的系统开销较低，因为流量由 Linux netfilter 处理，
无需在用户空间和内核空间之间切换。这种方案也更为可靠。

如果 kube-proxy 以 iptables 模式运行，并且它选择的第一个 Pod 没有响应，
那么连接会失败。这与用户空间模式不同：
在后者这种情况下，kube-proxy 会检测到与第一个 Pod 的连接失败，
并会自动用不同的后端 Pod 重试。

你可以使用 Pod [就绪探针](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#container-probes)来验证后端 Pod 是否健康。
这样可以避免 kube-proxy 将流量发送到已知失败的 Pod 上。

{{< figure src="/images/docs/services-iptables-overview.svg" title="iptables 模式下 Service 的虚拟 IP 机制" class="diagram-medium" >}}

#### 示例 {#packet-processing-iptables}

例如，考虑本页中[前面](#example)描述的图像处理应用程序。
当创建后端 Service 时，Kubernetes 控制平面会分配一个虚拟 IP 地址，例如 10.0.0.1。
对于这个例子而言，假设 Service 端口是 1234。
集群中的所有 kube-proxy 实例都会观察到新 Service 的创建。

当节点上的 kube-proxy 观察到新 Service 时，它会添加一系列 iptables 规则，
这些规则从虚拟 IP 地址重定向到更多 iptables 规则，每个 Service 都定义了这些规则。
每个 Service 规则链接到每个后端端点的更多规则，
并且每个端点规则将流量重定向（使用目标 NAT）到后端。

当客户端连接到 Service 的虚拟 IP 地址时，iptables 规则会生效。
会选择一个后端（基于会话亲和性或随机选择），并将数据包重定向到后端，无需重写客户端 IP 地址。

当流量通过节点端口或负载均衡器进入时，也会执行相同的基本流程，
只是在这些情况下，客户端 IP 地址会被更改。

#### 优化 iptables 模式性能  {#optimizing-iptables-mode-performance}

在大型集群（有数万个 Pod 和 Service）中，当 Service（或其 EndpointSlices）发生变化时
iptables 模式的 kube-proxy 在更新内核中的规则时可能要用较长时间。
你可以通过（`kube-proxy --config <path>` 指定的）kube-proxy
[配置文件](/zh-cn/docs/reference/config-api/kube-proxy-config.v1alpha1/)的
[`iptables` 节](/zh-cn/docs/reference/config-api/kube-proxy-config.v1alpha1/#kubeproxy-config-k8s-io-v1alpha1-KubeProxyIPTablesConfiguration)中的选项来调整
kube-proxy 的同步行为：

```yaml
...
iptables:
  minSyncPeriod: 1s
  syncPeriod: 30s
...
```

##### 对 `iptables` 模式的性能优化 {#minimize-iptables-restore}

{{< feature-state for_k8s_version="v1.27" state="beta" >}}

在 Kubernetes {{< skew currentVersion >}} 中，kube-proxy 默认采用最小方式进行 `iptables-restore` 操作，
仅在 Service 或 EndpointSlice 实际发生变化的地方进行更新。这是一个性能优化。
最初的实现在每次同步时都会更新所有服务的所有规则；这有时会导致大型集群出现性能问题（更新延迟）。

如果你运行的不是 Kubernetes {{< skew currentVersion >}} 版本的 kube-proxy，
请检查你实际运行的版本的行为和相关建议。

如果你之前覆盖了 `minSyncPeriod`，你应该尝试删除该覆盖并让 kube-proxy 使用默认值（`1s`）或至少比升级前使用的值小。
你可以通过禁用 `MinimizeIPTablesRestore`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)来选择执行旧的行为
（你应该不需要）。

##### `minSyncPeriod`

`minSyncPeriod` 参数设置尝试同步 iptables 规则与内核之间的最短时长。
如果是 `0s`，那么每次有任一 Service 或 Endpoint 发生变更时，kube-proxy 都会立即同步这些规则。
这种方式在较小的集群中可以工作得很好，但如果在很短的时间内很多东西发生变更时，它会导致大量冗余工作。
例如，如果你有一个由 {{< glossary_tooltip text="Deployment" term_id="deployment" >}}
支持的 Service，共有 100 个 Pod，你删除了这个 Deployment，
且设置了 `minSyncPeriod: 0s`，kube-proxy 最终会从 iptables 规则中逐个删除 Service 的 Endpoint，
总共更新 100 次。使用较大的 `minSyncPeriod` 值时，多个 Pod 删除事件将被聚合在一起，
因此 kube-proxy 最终可能会进行例如 5 次更新，每次移除 20 个端点，
这样在 CPU 利用率方面更有效率，能够更快地同步所有变更。

`minSyncPeriod` 的值越大，可以聚合的工作越多，
但缺点是每个独立的变更可能最终要等待整个 `minSyncPeriod` 周期后才能被处理，
这意味着 iptables 规则要用更多时间才能与当前的 API 服务器状态同步。

默认值 `1s` 适用于大多数集群，
在大型集群中，可能需要将其设置为更大的值。
（特别是，如果 kube-proxy 的 `sync_proxy_rules_duration_seconds` 指标表明平均时间远大于 1 秒，
那么提高 `minSyncPeriod` 可能会使更新更有效率。）

##### `syncPeriod`

`syncPeriod` 参数控制与单次 Service 和 EndpointSlice 的变更没有直接关系的少数同步操作。
特别是，它控制 kube-proxy 在外部组件已干涉 kube-proxy 的 iptables 规则时通知的速度。
在大型集群中，kube-proxy 也仅在每隔 `syncPeriod` 时长执行某些清理操作，以避免不必要的工作。

在大多数情况下，提高 `syncPeriod` 预计不会对性能产生太大影响，
但在过去，有时将其设置为非常大的值（例如 `1h`）很有用。
现在不再推荐这种做法，因为它对功能的破坏可能会超过对性能的改进。

### IPVS 代理模式 {#proxy-mode-ipvs}

**此代理模式仅适用于 Linux 节点。**

在 `ipvs` 模式下，kube-proxy 监视 Kubernetes Service 和 EndpointSlice，
然后调用 `netlink` 接口创建 IPVS 规则，
并定期与 Kubernetes Service 和 EndpointSlice 同步 IPVS 规则。
该控制回路确保 IPVS 状态与期望的状态保持一致。
访问 Service 时，IPVS 会将流量导向到某一个后端 Pod。

IPVS 代理模式基于 netfilter 回调函数，类似于 iptables 模式，
但它使用哈希表作为底层数据结构，在内核空间中生效。
这意味着 IPVS 模式下的 kube-proxy 比 iptables 模式下的 kube-proxy
重定向流量的延迟更低，同步代理规则时性能也更好。
与其他代理模式相比，IPVS 模式还支持更高的网络流量吞吐量。

IPVS 为将流量均衡到后端 Pod 提供了更多选择：

* `rr`：轮询
* `lc`：最少连接（打开连接数最少）
* `dh`：目标地址哈希
* `sh`：源地址哈希
* `sed`：最短预期延迟
* `nq`：最少队列

{{< note >}}
要在 IPVS 模式下运行 kube-proxy，必须在启动 kube-proxy 之前确保节点上的 IPVS 可用。

当 kube-proxy 以 IPVS 代理模式启动时，它会验证 IPVS 内核模块是否可用。
如果未检测到 IPVS 内核模块，则 kube-proxy 会退回到 iptables 代理模式运行。
{{< /note >}}

{{< figure src="/images/docs/services-ipvs-overview.svg" title="IPVS 模式下 Service 的虚拟 IP 地址机制" class="diagram-medium" >}}

### `kernelspace` 代理模式   {#proxy-mode-kernelspace}

**此代理模式仅适用于 Windows 节点。**

kube-proxy 在 Windows **虚拟过滤平台** (VFP)（Windows vSwitch 的扩展）中配置数据包过滤规则。
这些规则处理节点级虚拟网络中的封装数据包，并重写数据包，使目标 IP 地址（和第 2 层信息）正确，
以便将数据包路由到正确的目的地。Windows VFP 类似于 Linux `nftables` 或 `iptables` 等工具。
Windows VFP 是最初为支持虚拟机网络而实现的 **Hyper-V Switch** 的扩展。

当节点上的 Pod 将流量发送到某虚拟 IP 地址，且 kube-proxy 选择不同节点上的 Pod
作为负载均衡目标时，`kernelspace` 代理模式会重写该数据包以将其发送到对应目标后端 Pod。
Windows 主机网络服务（HSN）会配置数据包重写规则，确保返回流量看起来来自虚拟 IP 地址，
而不是特定的后端 Pod。

#### `kernelspace` 模式的 Direct Server Return（DSR）    {#windows-direct-server-return}

{{< feature-state for_k8s_version="v1.14" state="alpha" >}}

作为基本操作的替代方案，托管服务后端 Pod 的节点可以直接应用数据包重写，
而不用将此工作交给运行客户端 Pod 的节点来执行。这称为**Direct Server Return（DSR）**。

要使用这种技术，你必须使用 `--enable-dsr` 命令行参数运行 kube-proxy **并**启用
`WinDSR` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)。

即使两个 Pod 在同一节点上运行，Direct Server Return（DSR）也可优化 Pod 的返回流量。

## 会话亲和性    {#session-affinity}

在这些代理模型中，绑定到 Service IP:Port 的流量被代理到合适的后端，
客户端不需要知道任何关于 Kubernetes、Service 或 Pod 的信息。

如果要确保来自特定客户端的连接每次都传递给同一个 Pod，
你可以通过设置 Service 的 `.spec.sessionAffinity` 为 `ClientIP`
来设置基于客户端 IP 地址的会话亲和性（默认为 `None`）。

### 会话粘性超时     {#session-stickiness-timeout}

你还可以通过设置 Service 的 `.spec.sessionAffinityConfig.clientIP.timeoutSeconds`
来设置最大会话粘性时间（默认值为 10800，即 3 小时）。

{{< note >}}
在 Windows 上不支持为 Service 设置最大会话粘性时间。
{{< /note >}}

## 将 IP 地址分配给 Service  {#ip-address-assignment-to-services}

与实际路由到固定目标的 Pod IP 地址不同，Service IP 实际上不是由单个主机回答的。
相反，kube-proxy 使用数据包处理逻辑（例如 Linux 的 iptables）
来定义**虚拟** IP 地址，这些地址会按需被透明重定向。

当客户端连接到 VIP 时，其流量会自动传输到适当的端点。
实际上，Service 的环境变量和 DNS 是根据 Service 的虚拟 IP 地址（和端口）填充的。

### 避免冲突      {#avoiding-collisions}

Kubernetes 的主要哲学之一是，
你不应需要在完全不是你的问题的情况下面对可能导致你的操作失败的情形。
对于 Service 资源的设计，也就是如果你选择的端口号可能与其他人的选择冲突，
就不应该让你自己选择 IP 地址。这是一种失败隔离。

为了允许你为 Service 选择 IP 地址，我们必须确保没有任何两个 Service 会发生冲突。
Kubernetes 通过从为 {{< glossary_tooltip text="API 服务器" term_id="kube-apiserver" >}}
配置的 `service-cluster-ip-range` CIDR 范围内为每个 Service 分配自己的 IP 地址来实现这一点。

#### IP 地址分配追踪

为了确保每个 Service 都获得唯一的 IP，内部分配器在创建每个 Service
之前更新 {{< glossary_tooltip term_id="etcd" >}} 中的全局分配映射，这种更新操作具有原子性。
映射对象必须存在于数据库中，这样 Service 才能获得 IP 地址分配，
否则创建将失败，并显示无法分配 IP 地址。

在控制平面中，后台控制器负责创建该映射（从使用内存锁定的旧版本的 Kubernetes 迁移时需要这一映射）。
Kubernetes 还使用控制器来检查无效的分配（例如，因管理员干预而导致无效分配）
以及清理已分配但没有 Service 使用的 IP 地址。

{{< feature-state for_k8s_version="v1.27" state="alpha" >}}
如果你启用 `MultiCIDRServiceAllocator` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gate/)
和 [`networking.k8s.io/v1alpha1` API 组](/zh-cn/docs/tasks/administer-cluster/enable-disable-api/)，
控制平面将用一个新的分配器替换现有的 etcd 分配器，使用 IPAddress 对象而不是内部的全局分配映射。
与每个 Service 关联的 ClusterIP 地址将有一个对应的 IPAddress 对象。

后台控制器也被一个新的控制器取代，来处理新的 IPAddress 对象和从旧的分配器模型的迁移。

新分配器的主要好处之一是它取消了对 `service-cluster-ip-range` 的大小限制，对 IPv4 没有大小限制，
对于 IPv6 用户可以使用等于或大于 /64 的掩码（以前是 /108）。

用户现在能够检查分配给他们的 Service 的 IP 地址，Kubernetes 扩展，
如 [Gateway](https://gateway-api.sigs.k8s.io/) API
可以使用这个新的 IPAddress 对象类别来增强 Kubernetes 的网络能力，解除内置 Service API 的限制。

```shell
kubectl get services
```
```
NAME         TYPE        CLUSTER-IP        EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   2001:db8:1:2::1   <none>        443/TCP   3d1h
```

```shell
kubectl get ipaddresses
```
```
NAME              PARENTREF
2001:db8:1:2::1   services/default/kubernetes
2001:db8:1:2::a   services/kube-system/kube-dns
```

#### Service 虚拟 IP 地址的地址段 {#service-ip-static-sub-range}

{{< feature-state for_k8s_version="v1.26" state="stable" >}}

Kubernetes 根据配置的 `service-cluster-ip-range` 的大小使用公式
`min(max(16, cidrSize / 16), 256)` 将 `ClusterIP` 范围分为两段。
该公式可以解释为：介于 16 和 256 之间，并在上下界之间存在渐进阶梯函数的分配。

Kubernetes 优先通过从高段中选择来为 Service 分配动态 IP 地址，
这意味着如果要将特定 IP 地址分配给 `type: ClusterIP` Service，
则应手动从**低**段中分配 IP 地址。
该方法降低了分配导致冲突的风险。

如果你禁用 `ServiceIPStaticSubrange`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)，
则 Kubernetes 用于手动分配和动态分配的 IP 共享单个地址池，这适用于 `type: ClusterIP` 的 Service。

## 流量策略 {#traffic-policies}

你可以设置 `.spec.internalTrafficPolicy` 和 `.spec.externalTrafficPolicy`
字段来控制 Kubernetes 如何将流量路由到健康（“就绪”）的后端。

### 内部流量策略 {#internal-traffic-policy}

{{< feature-state for_k8s_version="v1.26" state="stable" >}}

你可以设置 `.spec.internalTrafficPolicy` 字段来控制来自内部源的流量如何被路由。
有效值为 `Cluster` 和 `Local`。
将字段设置为 `Cluster` 会将内部流量路由到所有准备就绪的端点，
将字段设置为 `Local` 仅会将流量路由到本地节点准备就绪的端点。
如果流量策略为 `Local` 但没有本地节点端点，那么 kube-proxy 会丢弃该流量。

### 外部流量策略 {#external-traffic-policy}

你可以设置 `.spec.externalTrafficPolicy` 字段来控制从外部源路由的流量。
有效值为 `Cluster` 和 `Local`。
将字段设置为 `Cluster` 会将外部流量路由到所有准备就绪的端点，
将字段设置为 `Local` 仅会将流量路由到本地节点上准备就绪的端点。
如果流量策略为 `Local` 并且没有本地节点端点，
那么 kube-proxy 不会转发与相关 Service 相关的任何流量。

### 流向正终止的端点的流量  {#traffic-to-terminating-endpoints}

{{< feature-state for_k8s_version="v1.26" state="beta" >}}

如果为 kube-proxy 启用了 `ProxyTerminatingEndpoints`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)且流量策略为 `Local`，
则节点的 kube-proxy 将使用更复杂的算法为 Service 选择端点。
启用此特性时，kube-proxy 会检查节点是否具有本地端点以及是否所有本地端点都标记为正在终止过程中。
如果有本地端点并且**所有**本地端点都被标记为处于终止过程中，
则 kube-proxy 会将转发流量到这些正在终止过程中的端点。
否则，kube-proxy 会始终选择将流量转发到并未处于终止过程中的端点。

这种对处于终止过程中的端点的转发行为使得 `NodePort` 和 `LoadBalancer` Service
能有条不紊地腾空设置了 `externalTrafficPolicy: Local` 时的连接。

当一个 Deployment 被滚动更新时，处于负载均衡器后端的节点可能会将该 Deployment 的 N 个副本缩减到
0 个副本。在某些情况下，外部负载均衡器可能在两次执行健康检查探针之间将流量发送到具有 0 个副本的节点。
将流量路由到处于终止过程中的端点可确保正在缩减 Pod 的节点能够正常接收流量，
并逐渐降低指向那些处于终止过程中的 Pod 的流量。
到 Pod 完成终止时，外部负载均衡器应该已经发现节点的健康检查失败并从后端池中完全移除该节点。

## {{% heading "whatsnext" %}}

要了解有关 Service 的更多信息，
请阅读[使用 Service 连接应用](/zh-cn/docs/tutorials/services/connect-applications-service/)。

也可以：

* 阅读 [Service](/zh-cn/docs/concepts/services-networking/service/) 了解其概念
* 阅读 [Ingress](/zh-cn/docs/concepts/services-networking/ingress/) 了解其概念
* 阅读 [API 参考](/zh-cn/docs/reference/kubernetes-api/service-resources/service-v1/)进一步了解 Service API
