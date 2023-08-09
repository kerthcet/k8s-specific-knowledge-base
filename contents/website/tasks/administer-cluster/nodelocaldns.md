---
title: 在 Kubernetes 集群中使用 NodeLocal DNSCache
content_type: task
weight: 390
---


{{< feature-state for_k8s_version="v1.18" state="stable" >}}

本页概述了 Kubernetes 中的 NodeLocal DNSCache 功能。

## {{% heading "prerequisites" %}}

 {{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


## 引言   {#introduction}

NodeLocal DNSCache 通过在集群节点上作为 DaemonSet 运行 DNS 缓存代理来提高集群 DNS 性能。
在当今的体系结构中，运行在 'ClusterFirst' DNS 模式下的 Pod 可以连接到 kube-dns `serviceIP` 进行 DNS 查询。
通过 kube-proxy 添加的 iptables 规则将其转换为 kube-dns/CoreDNS 端点。
借助这种新架构，Pod 将可以访问在同一节点上运行的 DNS 缓存代理，从而避免 iptables DNAT 规则和连接跟踪。
本地缓存代理将查询 kube-dns 服务以获取集群主机名的缓存缺失（默认为 "`cluster.local`" 后缀）。

## 动机   {#motivation}

* 使用当前的 DNS 体系结构，如果没有本地 kube-dns/CoreDNS 实例，则具有最高 DNS QPS
  的 Pod 可能必须延伸到另一个节点。
  在这种场景下，拥有本地缓存将有助于改善延迟。

* 跳过 iptables DNAT 和连接跟踪将有助于减少
  [conntrack 竞争](https://github.com/kubernetes/kubernetes/issues/56903)并避免
  UDP DNS 条目填满 conntrack 表。

* 从本地缓存代理到 kube-dns 服务的连接可以升级为 TCP。
  TCP conntrack 条目将在连接关闭时被删除，相反 UDP 条目必须超时
  （[默认](https://www.kernel.org/doc/Documentation/networking/nf_conntrack-sysctl.txt)
  `nf_conntrack_udp_timeout` 是 30 秒）。

* 将 DNS 查询从 UDP 升级到 TCP 将减少由于被丢弃的 UDP 包和 DNS 超时而带来的尾部等待时间；
  这类延时通常长达 30 秒（3 次重试 + 10 秒超时）。
  由于 nodelocal 缓存监听 UDP DNS 查询，应用不需要变更。

* 在节点级别对 DNS 请求的度量和可见性。

* 可以重新启用负缓存，从而减少对 kube-dns 服务的查询数量。

## 架构图   {#architecture-diagram}

启用 NodeLocal DNSCache 之后，DNS 查询所遵循的路径如下：

{{< figure src="/images/docs/nodelocaldns.svg" alt="NodeLocal DNSCache 流" title="Nodelocal DNSCache 流" caption="此图显示了 NodeLocal DNSCache 如何处理 DNS 查询。" class="diagram-medium" >}}

## 配置   {#configuration}

{{< note >}}
NodeLocal DNSCache 的本地侦听 IP 地址可以是任何地址，只要该地址不和你的集群里现有的 IP 地址发生冲突。
推荐使用本地范围内的地址，例如，IPv4 链路本地区段 '169.254.0.0/16' 内的地址，
或者 IPv6 唯一本地地址区段 'fd00::/8' 内的地址。
{{< /note >}}

可以使用以下步骤启动此功能：

* 根据示例 [`nodelocaldns.yaml`](https://github.com/kubernetes/kubernetes/blob/master/cluster/addons/dns/nodelocaldns/nodelocaldns.yaml)
  准备一个清单，把它保存为 `nodelocaldns.yaml`。

* 如果使用 IPv6，在使用 'IP:Port' 格式的时候需要把 CoreDNS 配置文件里的所有 IPv6 地址用方括号包起来。
  如果你使用上述的示例清单，
  需要把[配置行 L70](https://github.com/kubernetes/kubernetes/blob/b2ecd1b3a3192fbbe2b9e348e095326f51dc43dd/cluster/addons/dns/nodelocaldns/nodelocaldns.yaml#L70)
  修改为： "`health [__PILLAR__LOCAL__DNS__]:8080`"。

* 把清单里的变量更改为正确的值：

  ```shell
  kubedns=`kubectl get svc kube-dns -n kube-system -o jsonpath={.spec.clusterIP}`
  domain=<cluster-domain>
  localdns=<node-local-address>
  ```

  `<cluster-domain>` 的默认值是 "`cluster.local`"。`<node-local-address>` 是
  NodeLocal DNSCache 选择的本地侦听 IP 地址。

  * 如果 kube-proxy 运行在 IPTABLES 模式：

    ``` bash
    sed -i "s/__PILLAR__LOCAL__DNS__/$localdns/g; s/__PILLAR__DNS__DOMAIN__/$domain/g; s/__PILLAR__DNS__SERVER__/$kubedns/g" nodelocaldns.yaml
    ```

    node-local-dns Pod 会设置 `__PILLAR__CLUSTER__DNS__` 和 `__PILLAR__UPSTREAM__SERVERS__`。
    在此模式下, node-local-dns Pod 会同时侦听 kube-dns 服务的 IP 地址和
    `<node-local-address>` 的地址，以便 Pod 可以使用其中任何一个 IP 地址来查询 DNS 记录。

  * 如果 kube-proxy 运行在 IPVS 模式：

    ``` bash
    sed -i "s/__PILLAR__LOCAL__DNS__/$localdns/g; s/__PILLAR__DNS__DOMAIN__/$domain/g; s/,__PILLAR__DNS__SERVER__//g; s/__PILLAR__CLUSTER__DNS__/$kubedns/g" nodelocaldns.yaml
    ```

    在此模式下，node-local-dns Pod 只会侦听 `<node-local-address>` 的地址。
    node-local-dns 接口不能绑定 kube-dns 的集群 IP 地址，因为 IPVS 负载均衡使用的接口已经占用了该地址。
    node-local-dns Pod 会设置 `__PILLAR__UPSTREAM__SERVERS__`。

* 运行 `kubectl create -f nodelocaldns.yaml`

* 如果 kube-proxy 运行在 IPVS 模式，需要修改 kubelet 的 `--cluster-dns` 参数
  NodeLocal DNSCache 正在侦听的 `<node-local-address>` 地址。
  否则，不需要修改 `--cluster-dns` 参数，因为 NodeLocal DNSCache 会同时侦听
  kube-dns 服务的 IP 地址和 `<node-local-address>` 的地址。

启用后，`node-local-dns` Pod 将在每个集群节点上的 `kube-system` 名字空间中运行。
此 Pod 在缓存模式下运行 [CoreDNS](https://github.com/coredns/coredns)，
因此每个节点都可以使用不同插件公开的所有 CoreDNS 指标。

如果要禁用该功能，你可以使用 `kubectl delete -f <manifest>` 来删除 DaemonSet。
你还应该回滚你对 kubelet 配置所做的所有改动。

## StubDomains 和上游服务器配置   {#stubdomains-and-upstream-server-configuration}

`node-local-dns` Pod 能够自动读取 `kube-system` 名字空间中 `kube-dns` ConfigMap
中保存的 StubDomains 和上游服务器信息。ConfigMap
中的内容需要遵从[此示例](/zh-cn/docs/tasks/administer-cluster/dns-custom-nameservers/#example-1)中所给的格式。
`node-local-dns` ConfigMap 也可被直接修改，使用 Corefile 格式设置 stubDomain 配置。
某些云厂商可能不允许直接修改 `node-local-dns` ConfigMap 的内容。
在这种情况下，可以更新 `kube-dns` ConfigMap。

## 设置内存限制   {#setting-memory-limits}

`node-local-dns` Pod 使用内存来保存缓存项并处理查询。
由于它们并不监视 Kubernetes 对象变化，集群规模或者 Service/EndpointSlices
的数量都不会直接影响内存用量。内存用量会受到 DNS 查询模式的影响。
根据 [CoreDNS 文档](https://github.com/coredns/deployment/blob/master/kubernetes/Scaling_CoreDNS.md),

> The default cache size is 10000 entries, which uses about 30 MB when completely filled.
> （默认的缓存大小是 10000 个表项，当完全填充时会使用约 30 MB 内存）

这一数值是（缓存完全被填充时）每个服务器块的内存用量。
通过设置小一点的缓存大小可以降低内存用量。

并发查询的数量会影响内存需求，因为用来处理查询请求而创建的 Go 协程都需要一定量的内存。
你可以在 forward 插件中使用 `max_concurrent` 选项设置并发查询数量上限。

如果一个 `node-local-dns` Pod 尝试使用的内存超出可提供的内存量
（因为系统资源总量的，或者所配置的[资源约束](/zh-cn/docs/concepts/configuration/manage-resources-containers/)）的原因，
操作系统可能会关闭这一 Pod 的容器。
发生这种情况时，被终止的（"OOMKilled"）容器不会清理其启动期间所添加的定制包过滤规则。
该 `node-local-dns` 容器应该会被重启（因其作为 DaemonSet 的一部分被管理），
但因上述原因可能每次容器失败时都会导致 DNS 有一小段时间不可用：
the packet filtering rules direct DNS queries to a local Pod that is unhealthy
（包过滤器规则将 DNS 查询转发到本地某个不健康的 Pod）。

通过不带限制地运行 `node-local-dns` Pod 并度量其内存用量峰值，你可以为其确定一个合适的内存限制值。
你也可以安装并使用一个运行在 “Recommender Mode（建议者模式）” 的
[VerticalPodAutoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler)，
并查看该组件输出的建议信息。

