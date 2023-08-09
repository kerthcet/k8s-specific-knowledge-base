---
title: 服务内部流量策略
content_type: concept
weight: 120
description: >-
   如果集群中的两个 Pod 想要通信，并且两个 Pod 实际上都在同一节点运行，
   **服务内部流量策略** 可以将网络流量限制在该节点内。
   通过集群网络避免流量往返有助于提高可靠性、增强性能（网络延迟和吞吐量）或降低成本。
---


{{< feature-state for_k8s_version="v1.26" state="stable" >}}

**服务内部流量策略**开启了内部流量限制，将内部流量只路由到发起方所处节点内的服务端点。
这里的”内部“流量指当前集群中的 Pod 所发起的流量。
这种机制有助于节省开销，提升效率。


## 使用服务内部流量策略 {#using-service-internal-traffic-policy}

你可以通过将 {{< glossary_tooltip text="Service" term_id="service" >}} 的
`.spec.internalTrafficPolicy` 项设置为 `Local`，
来为它指定一个内部专用的流量策略。
此设置就相当于告诉 kube-proxy 对于集群内部流量只能使用节点本地的服务端口。

{{< note >}}
如果某节点上的 Pod 均不提供指定 Service 的服务端点，
即使该 Service 在其他节点上有可用的服务端点，
Service 的行为看起来也像是它只有 0 个服务端点（只针对此节点上的 Pod）。
{{< /note >}}

以下示例展示了把 Service 的 `.spec.internalTrafficPolicy` 项设为 `Local` 时，
Service 的样子：


```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
  internalTrafficPolicy: Local
```

## 工作原理 {#how-it-works}

kube-proxy 基于 `spec.internalTrafficPolicy` 的设置来过滤路由的目标服务端点。
当它的值设为 `Local` 时，只会选择节点本地的服务端点。
当它的值设为 `Cluster` 或缺省时，Kubernetes 会选择所有的服务端点。

## {{% heading "whatsnext" %}}

* 请阅读[拓扑感知提示](/zh-cn/docs/concepts/services-networking/topology-aware-hints)
* 请阅读 [Service 的外部流量策略](/zh-cn/docs/tasks/access-application-cluster/create-external-load-balancer/#preserving-the-client-source-ip)
* 遵循[使用 Service 连接到应用](/zh-cn/docs/tutorials/services/connect-applications-service/)教程