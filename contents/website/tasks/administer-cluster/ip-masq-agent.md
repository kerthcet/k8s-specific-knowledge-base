---
title: IP Masquerade Agent 用户指南
content_type: task
weight: 230
---

此页面展示如何配置和启用 `ip-masq-agent`。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

## IP Masquerade Agent 用户指南   {#ip-masquerade-agent-user-guide}

`ip-masq-agent` 配置 iptables 规则以隐藏位于集群节点 IP 地址后面的 Pod 的 IP 地址。
这通常在将流量发送到集群的 Pod
[CIDR](https://zh.wikipedia.org/wiki/%E6%97%A0%E7%B1%BB%E5%88%AB%E5%9F%9F%E9%97%B4%E8%B7%AF%E7%94%B1)
范围之外的目的地时使用。

### 关键术语    {#key-terms}

* **NAT（网络地址转换）**：
  是一种通过修改 IP 地址头中的源和/或目标地址信息将一个 IP 地址重新映射
  到另一个 IP 地址的方法。通常由执行 IP 路由的设备执行。

* **伪装**：
  NAT 的一种形式，通常用于执行多对一地址转换，其中多个源 IP 地址被隐藏在
  单个地址后面，该地址通常是执行 IP 路由的设备。在 Kubernetes 中，
  这是节点的 IP 地址。

* **CIDR（无类别域间路由）**：
  基于可变长度子网掩码，允许指定任意长度的前缀。
  CIDR 引入了一种新的 IP 地址表示方法，现在通常称为 **CIDR 表示法**，
  其中地址或路由前缀后添加一个后缀，用来表示前缀的位数，例如 192.168.2.0/24。

* **本地链路**：
  本地链路是仅对网段或主机所连接的广播域内的通信有效的网络地址。
  IPv4 的本地链路地址在 CIDR 表示法的地址块 169.254.0.0/16 中定义。

ip-masq-agent 配置 iptables 规则，以便在将流量发送到集群节点的 IP 和集群 IP
范围之外的目标时处理伪装节点或 Pod 的 IP 地址。这本质上隐藏了集群节点 IP 地址后面的
Pod IP 地址。在某些环境中，去往"外部"地址的流量必须从已知的机器地址发出。
例如，在 Google Cloud 中，任何到互联网的流量都必须来自 VM 的 IP。
使用容器时，如 Google Kubernetes Engine，从 Pod IP 发出的流量将被拒绝出站。
为了避免这种情况，我们必须将 Pod IP 隐藏在 VM 自己的 IP 地址后面 - 通常称为"伪装"。
默认情况下，代理配置为将
[RFC 1918](https://tools.ietf.org/html/rfc1918)
指定的三个私有 IP 范围视为非伪装
[CIDR](https://zh.wikipedia.org/wiki/%E6%97%A0%E7%B1%BB%E5%88%AB%E5%9F%9F%E9%97%B4%E8%B7%AF%E7%94%B1)。
这些范围是 10.0.0.0/8、172.16.0.0/12 和 192.168.0.0/16。
默认情况下，代理还将链路本地地址（169.254.0.0/16）视为非伪装 CIDR。
代理程序配置为每隔 60 秒从 **/etc/config/ip-masq-agent** 重新加载其配置，
这也是可修改的。

![masq/non-masq example](/images/docs/ip-masq.png)

代理配置文件必须使用 YAML 或 JSON 语法编写，并且可能包含三个可选值：

* `nonMasqueradeCIDRs`：
  [CIDR](https://zh.wikipedia.org/wiki/%E6%97%A0%E7%B1%BB%E5%88%AB%E5%9F%9F%E9%97%B4%E8%B7%AF%E7%94%B1)
  表示法中的字符串列表，用于指定不需伪装的地址范围。

* `masqLinkLocal`：布尔值（true/false），表示是否为本地链路前缀 `169.254.0.0/16`
  的流量提供伪装。默认为 false。

* `resyncInterval`：代理从磁盘重新加载配置的重试时间间隔。
  例如 '30s'，其中 's' 是秒，'ms' 是毫秒。

10.0.0.0/8、172.16.0.0/12 和 192.168.0.0/16 范围内的流量不会被伪装。
任何其他流量（假设是互联网）将被伪装。
Pod 访问本地目的地的例子，可以是其节点的 IP 地址、另一节点的地址或集群的 IP 地址范围内的一个 IP 地址。
默认情况下，任何其他流量都将伪装。以下条目展示了 ip-masq-agent 的默认使用的规则：

```shell
iptables -t nat -L IP-MASQ-AGENT
```

```none
target     prot opt source               destination
RETURN     all  --  anywhere             169.254.0.0/16       /* ip-masq-agent: cluster-local traffic should not be subject to MASQUERADE */ ADDRTYPE match dst-type !LOCAL
RETURN     all  --  anywhere             10.0.0.0/8           /* ip-masq-agent: cluster-local traffic should not be subject to MASQUERADE */ ADDRTYPE match dst-type !LOCAL
RETURN     all  --  anywhere             172.16.0.0/12        /* ip-masq-agent: cluster-local traffic should not be subject to MASQUERADE */ ADDRTYPE match dst-type !LOCAL
RETURN     all  --  anywhere             192.168.0.0/16       /* ip-masq-agent: cluster-local traffic should not be subject to MASQUERADE */ ADDRTYPE match dst-type !LOCAL
MASQUERADE  all  --  anywhere             anywhere             /* ip-masq-agent: outbound traffic should be subject to MASQUERADE (this match must come after cluster-local CIDR matches) */ ADDRTYPE match dst-type !LOCAL
```

默认情况下，在 GCE/Google Kubernetes Engine 中，如果启用了网络策略，
或者你使用的集群 CIDR 不在 10.0.0.0/8 范围内，
则 `ip-masq-agent` 将在你的集群中运行。
如果你在其他环境中运行，可以将 `ip-masq-agent`
[DaemonSet](/zh-cn/docs/concepts/workloads/controllers/daemonset/)
添加到你的集群中。


## 创建 ip-masq-agent   {#create-ip-masq-agent}

通过运行以下 kubectl 指令创建 ip-masq-agent：

```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/ip-masq-agent/master/ip-masq-agent.yaml
```

你必须同时将适当的节点标签应用于集群中希望代理运行的任何节点。

```shell
kubectl label nodes my-node node.kubernetes.io/masq-agent-ds-ready=true
```

更多信息可以通过 ip-masq-agent 文档[这里](https://github.com/kubernetes-sigs/ip-masq-agent)找到。

在大多数情况下，默认的规则集应该足够；但是，如果你的集群不是这种情况，则可以创建并应用
[ConfigMap](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/)
来自定义受影响的 IP 范围。
例如，要允许 ip-masq-agent 仅作用于 10.0.0.0/8，你可以在一个名为 "config" 的文件中创建以下
[ConfigMap](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/)。

{{< note >}}
重要的是，该文件之所以被称为 config，是因为默认情况下，该文件将被用作
`ip-masq-agent` 查找的主键：

```yaml
nonMasqueradeCIDRs:
  - 10.0.0.0/8
resyncInterval: 60s
```
{{< /note >}}

运行以下命令将 ConfigMap 添加到你的集群：

```shell
kubectl create configmap ip-masq-agent --from-file=config --namespace=kube-system
```

这将更新位于 `/etc/config/ip-masq-agent` 的一个文件，该文件以 `resyncInterval`
为周期定期检查并应用于集群节点。
重新同步间隔到期后，你应该看到你的更改在 iptables 规则中体现：

```shell
iptables -t nat -L IP-MASQ-AGENT
```

```none
Chain IP-MASQ-AGENT (1 references)
target     prot opt source               destination
RETURN     all  --  anywhere             169.254.0.0/16       /* ip-masq-agent: cluster-local traffic should not be subject to MASQUERADE */ ADDRTYPE match dst-type !LOCAL
RETURN     all  --  anywhere             10.0.0.0/8           /* ip-masq-agent: cluster-local
MASQUERADE  all  --  anywhere             anywhere             /* ip-masq-agent: outbound traffic should be subject to MASQUERADE (this match must come after cluster-local CIDR matches) */ ADDRTYPE match dst-type !LOCAL
```

默认情况下，本地链路范围（169.254.0.0/16）也由 ip-masq agent 处理，
该代理设置适当的 iptables 规则。要使 ip-masq-agent 忽略本地链路，
可以在 ConfigMap 中将 `masqLinkLocal` 设置为 true。

```yaml
nonMasqueradeCIDRs:
  - 10.0.0.0/8
resyncInterval: 60s
masqLinkLocal: true
```
