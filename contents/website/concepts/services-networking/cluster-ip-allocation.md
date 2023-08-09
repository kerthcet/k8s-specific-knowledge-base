---
title: Service ClusterIP 分配
content_type: concept
weight: 120
---



在 Kubernetes 中，[Service](/zh-cn/docs/concepts/services-networking/service/) 是一种抽象的方式，
用于公开在一组 Pod 上运行的应用。
Service 可以具有集群作用域的虚拟 IP 地址（使用 `type: ClusterIP` 的 Service）。
客户端可以使用该虚拟 IP 地址进行连接，Kubernetes 通过不同的后台 Pod 对该 Service 的流量进行负载均衡。
## Service ClusterIP 是如何分配的？
当 Kubernetes 需要为 Service 分配虚拟 IP 地址时，该分配会通过以下两种方式之一进行：

**动态分配**
: 集群的控制面自动从所配置的 IP 范围内为 `type: ClusterIP` 选择一个空闲 IP 地址。

**静态分配**
: 根据为 Service 所配置的 IP 范围，选定并设置你的 IP 地址。

在整个集群中，每个 Service 的 `ClusterIP` 都必须是唯一的。
尝试使用已分配的 `ClusterIP` 创建 Service 将返回错误。

## 为什么需要预留 Service 的 ClusterIP ？

有时你可能希望 Services 在众所周知的 IP 上面运行，以便集群中的其他组件和用户可以使用它们。

最好的例子是集群的 DNS Service。作为一种非强制性的约定，一些 Kubernetes 安装程序
将 Service IP 范围中的第 10 个 IP 地址分配给 DNS 服务。假设将集群的 Service IP 范围配置为 
10.96.0.0/16，并且希望 DNS Service IP 为 10.96.0.10，则必须创建如下 Service：

```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    k8s-app: kube-dns
    kubernetes.io/cluster-service: "true"
    kubernetes.io/name: CoreDNS
  name: kube-dns
  namespace: kube-system
spec:
  clusterIP: 10.96.0.10
  ports:
  - name: dns
    port: 53
    protocol: UDP
    targetPort: 53
  - name: dns-tcp
    port: 53
    protocol: TCP
    targetPort: 53
  selector:
    k8s-app: kube-dns
  type: ClusterIP
```
但如前所述，IP 地址 10.96.0.10 尚未被保留。如果在 DNS 启动之前或同时采用动态分配机制创建其他 Service，
则它们有可能被分配此 IP，因此，你将无法创建 DNS Service，因为它会因冲突错误而失败。


## 如何避免 Service ClusterIP 冲突？{#avoid-ClusterIP-conflict}

Kubernetes 中用來将 ClusterIP 分配给 Service 的分配策略降低了冲突的风险。

`ClusterIP` 范围根据公式 `min(max(16, cidrSize / 16), 256)` 进行划分，
描述为不小于 16 且不大于 256，并在二者之间有一个渐进的步长。

默认情况下，动态 IP 分配使用地址较高的一段，一旦用完，它将使用较低范围。
这将允许用户在冲突风险较低的较低地址段上使用静态分配。

## 示例 {#allocation-examples}

### 示例 1 {#allocation-example-1}

此示例使用 IP 地址范围：10.96.0.0/24（CIDR 表示法）作为 Service 的 IP 地址。
范围大小：2<sup>8</sup> - 2 = 254  
带宽偏移量：`min(max(16, 256/16), 256)` = `min(16, 256)` = 16  
静态带宽起始地址：10.96.0.1  
静态带宽结束地址：10.96.0.16  
范围结束地址：10.96.0.254  

{{< mermaid >}}
pie showData
    title 10.96.0.0/24
    "静态分配" : 16
    "动态分配" : 238
{{< /mermaid >}}

### 示例 2 {#allocation-example-2}

此示例使用 IP 地址范围 10.96.0.0/20（CIDR 表示法）作为 Service 的 IP 地址。


范围大小：2<sup>12</sup> - 2 = 4094  
带宽偏移量：`min(max(16, 4096/16), 256)` = `min(256, 256)` = 256  
静态带宽起始地址：10.96.0.1  
静态带宽结束地址：10.96.1.0  
范围结束地址：10.96.15.254  

{{< mermaid >}}
pie showData
    title 10.96.0.0/20
    "静态分配" : 256
    "动态分配" : 3838
{{< /mermaid >}}

### 示例 3 {#allocation-example-3}

此示例使用 IP 地址范围 10.96.0.0/16（CIDR 表示法）作为 Service 的 IP 地址。

范围大小：2<sup>16</sup> - 2 = 65534  
带宽偏移量：`min(max(16, 65536/16), 256)` = `min(4096, 256)` = 256  
静态带宽起始地址：10.96.0.1  
静态带宽结束地址：10.96.1.0  
范围结束地址：10.96.255.254  

{{< mermaid >}}
pie showData
    title 10.96.0.0/16
    "静态分配" : 256
    "动态分配" : 65278
{{< /mermaid >}}

## {{% heading "whatsnext" %}}

* 阅读[服务外部流量策略](/zh-cn/docs/tasks/access-application-cluster/create-external-load-balancer/#preserving-the-client-source-ip)
* 阅读[应用程序与服务连接](/zh-cn/docs/tutorials/services/connect-applications-service/)
* 阅读[服务](/zh-cn/docs/concepts/services-networking/service/)

