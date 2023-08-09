---
layout: blog
title: "Kubernetes 1.27：为 NodePort Service 分配端口时避免冲突"
date: 2023-05-11
slug: nodeport-dynamic-and-static-allocation
---

**作者:** Xu Zhenglun (Alibaba)

**译者:** [Michael Yao](https://github.com/windsonsea) (DaoCloud)

在 Kubernetes 中，对于以一组 Pod 运行的应用，Service 可以为其提供统一的流量端点。
客户端可以使用 Service 提供的虚拟 IP 地址（或 **VIP**）进行访问，
Kubernetes 为访问不同的后端 Pod 的流量提供负载均衡能力，
但 ClusterIP 类型的 Service 仅限于供集群内的节点来访问，
而来自集群外的流量无法被路由。解决这个难题的一种方式是使用 `type: NodePort` Service，
这种服务会在集群所有节点上为特定端口建立映射关系，从而将来自集群外的流量重定向到集群内。

## Kubernetes 如何为 Services 分配节点端口？

当 `type: NodePort` Service 被创建时，其所对应的端口将以下述两种方式之一分配：

- **动态分配**：如果 Service 类型是 `NodePort` 且你没有为 Service 显式设置 `nodePort` 值，
  Kubernetes 控制面将在创建时自动为其分配一个未使用的端口。

- **静态分配**：除了上述动态自动分配，你还可以显式指定 nodeport 端口范围配置内的某端口。

你手动分配的 `nodePort` 值在整个集群范围内一定不能重复。
如果尝试在创建 `type: NodePort` Service 时显式指定已分配的节点端口，将产生错误。

## 为什么需要保留 NodePort Service 的端口？

有时你可能想要 NodePort Service 运行在众所周知的端口上，
便于集群内外的其他组件和用户可以使用这些端口。

在某些复杂的集群部署场景中在同一网络上混合了 Kubernetes 节点和其他服务器，
可能有必要使用某些预定义的端口进行通信。尤为特别的是，某些基础组件无法使用用来支撑
`type: LoadBalancer` Service 的 VIP，因为针对集群实现的虚拟 IP 地址映射也依赖这些基础组件。

现在假设你需要在 Kubernetes 上将一个 Minio 对象存储服务暴露给运行在 Kubernetes 集群外的客户端，
协商后的端口是 `30009`，我们需要创建以下 Service：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: minio
spec:
  ports:
  - name: api
    nodePort: 30009
    port: 9000
    protocol: TCP
    targetPort: 9000
  selector:
    app: minio
  type: NodePort
```

然而如前文所述，如果 `minio` Service 所需的端口 (30009) 未被预留，
且另一个 `type: NodePort`（或者也包括 `type: LoadBalancer`）Service
在 `minio` Service 之前或与之同时被创建、动态分配，TCP 端口 30009 可能被分配给了这个 Service；
如果出现这种情况，`minio` Service 的创建将由于节点端口冲突而失败。

## 如何才能避免 NodePort Service 端口冲突？

Kubernetes 1.24 引入了针对 `type: ClusterIP` Service 的变更，将集群 IP 地址的 CIDR
范围划分为使用不同分配策略的两块来[减少冲突的风险](/zh-cn/docs/reference/networking/virtual-ips/#avoiding-collisions)。
在 Kubernetes 1.27 中，作为一个 Alpha 特性，你可以为 `type: NodePort` Service 采用类似的策略。
你可以启用新的[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
`ServiceNodePortStaticSubrange`。开启此门控将允许你为
`type: NodePort` Service 使用不同的端口分配策略，减少冲突的风险。

`NodePort` 的端口范围将基于公式 `min(max(16, 节点端口数 / 32), 128)` 进行划分。
这个公式的结果将是一个介于 16 到 128 的数字，随着节点端口范围变大，步进值也会变大。
此公式的结果决定了静态端口范围的大小。当端口范围小于 16 时，静态端口范围的大小将被设为 0，
这意味着所有端口都将被动态分配。

动态端口分配默认使用数值较高的一段，一旦用完，它将使用较低范围。
这将允许用户在冲突风险较低的较低端口段上使用静态分配。

## 示例

### 默认范围：30000-32767

| 范围属性                | 值                                                                                              |
| ----------------------- | ----------------------------------------------------------------------------------------------- |
| service-node-port-range | 30000-32767                                                                                     |
| 分段偏移量              | &ensp; `min(max(16, 2768/32), 128)` <br>= `min(max(16, 86), 128)` <br>= `min(86, 128)` <br>= 86 |
| 起始静态段              | 30000                                                                                           |
| 结束静态段              | 30085                                                                                           |
| 起始动态段              | 30086                                                                                           |
| 结束动态段              | 32767                                                                                           |

{{< mermaid >}}
pie showData
    title 30000-32767
    "Static" : 86
    "Dynamic" : 2682
{{< /mermaid >}}

### 超小范围：30000-30015

| 范围属性                 | 值          |
| ----------------------- | ----------- |
| service-node-port-range | 30000-30015 |
| 分段偏移量               | 0           |
| 起始静态段               | -           |
| 结束静态段               | -           |
| 起始动态段               | 30000       |
| 动态动态段               | 30015       |

{{< mermaid >}}
pie showData
    title 30000-30015
    "Static" : 0
    "Dynamic" : 16
{{< /mermaid >}}

### 小（下边界）范围：30000-30127

| 范围属性                | 值                                                                                            |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| service-node-port-range | 30000-30127                                                                                   |
| 分段偏移量              | &ensp; `min(max(16, 128/32), 128)` <br>= `min(max(16, 4), 128)` <br>= `min(16, 128)` <br>= 16 |
| 起始静态段              | 30000                                                                                         |
| 结束静态段              | 30015                                                                                         |
| 起始动态段              | 30016                                                                                         |
| 结束动态段              | 30127                                                                                         |

{{< mermaid >}}
pie showData
    title 30000-30127
    "Static" : 16
    "Dynamic" : 112
{{< /mermaid >}}

### 大（上边界）范围：30000-34095

| 范围属性                | 值                                                                                                 |
| -----------------------| -------------------------------------------------------------------------------------------------- |
| service-node-port-range | 30000-34095                                                                                        |
| 分段偏移量              | &ensp; `min(max(16, 4096/32), 128)` <br>= `min(max(16, 128), 128)` <br>= `min(128, 128)` <br>= 128 |
| 起始静态段              | 30000                                                                                              |
| 结束静态段              | 30127                                                                                              |
| 起始动态段              | 30128                                                                                              |
| 结束动态段              | 34095                                                                                              |

{{< mermaid >}}
pie showData
    title 30000-34095
    "Static" : 128
    "Dynamic" : 3968
{{< /mermaid >}}

### 超大范围：30000-38191

| 范围属性                | 值                                                                                                 |
| ---------------------- | -------------------------------------------------------------------------------------------------- |
| service-node-port-range | 30000-38191                                                                                        |
| 分段偏移量             | &ensp; `min(max(16, 8192/32), 128)` <br>= `min(max(16, 256), 128)` <br>= `min(256, 128)` <br>= 128 |
| 起始静态段              | 30000                                                                                              |
| 结束静态段              | 30127                                                                                              |
| 起始动态段              | 30128                                                                                              |
| 结束动态段              | 38191                                                                                              |

{{< mermaid >}}
pie showData
    title 30000-38191
    "Static" : 128
    "Dynamic" : 8064
{{< /mermaid >}}
