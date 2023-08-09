---
reviewers:
- robscott
title: 拓扑感知路由
content_type: concept
weight: 100
description: >-
  **拓扑感知路由**提供了一种机制帮助保持网络流量处于流量发起的区域内。
  在集群中 Pod 之间优先使用相同区域的流量有助于提高可靠性、性能（网络延迟和吞吐量）或降低成本。
---


{{< feature-state for_k8s_version="v1.23" state="beta" >}}

{{< note >}}
在 Kubernetes 1.27 之前，此特性称为**拓扑感知提示（Topology Aware Hint）**。
{{</ note >}}

**拓扑感知路由（Toplogy Aware Routing）** 调整路由行为，以优先保持流量在其发起区域内。
在某些情况下，这有助于降低成本或提高网络性能。


## 动机   {#motivation}

Kubernetes 集群越来越多地部署在多区域环境中。
**拓扑感知路由** 提供了一种机制帮助流量保留在其发起所在的区域内。
计算 {{<glossary_tooltip term_id="Service">}} 的端点时，
EndpointSlice 控制器考虑每个端点的物理拓扑（地区和区域），并填充提示字段以将其分配到区域。
诸如 {{<glossary_tooltip term_id="kube-proxy" text="kube-proxy">}}
等集群组件可以使用这些提示，影响流量的路由方式（优先考虑物理拓扑上更近的端点）。

## 启用拓扑感知路由   {#enabling-topology-aware-routing}

{{< note >}}
在 Kubernetes 1.27 之前，此行为是通过 `service.kubernetes.io/topology-aware-hints` 注解来控制的。
{{</ note >}}

你可以通过将 `service.kubernetes.io/topology-mode` 注解设置为 `Auto` 来启用 Service 的拓扑感知路由。
当每个区域中有足够的端点可用时，系统将为 EndpointSlices 填充拓扑提示，把每个端点分配给特定区域，
从而使流量被路由到更接近其来源的位置。

## 何时效果最佳   {#when-it-works-best}

此特性在以下场景中的工作效果最佳：

### 1. 入站流量均匀分布   {#incoming-traffic-is-evently-distributed}

如果大部分流量源自同一个区域，则该流量可能会使分配到该区域的端点子集过载。
当预计入站流量源自同一区域时，不建议使用此特性。

### 2. 服务在每个区域具有至少 3 个端点 {#three-or-more-endpoints-per-zone}

在一个三区域的集群中，这意味着有至少 9 个端点。如果每个区域的端点少于 3 个，
则 EndpointSlice 控制器很大概率（约 50％）无法平均分配端点，而是回退到默认的集群范围的路由方法。

## 工作原理 {#how-it-works}

“自动”启发式算法会尝试按比例分配一定数量的端点到每个区域。
请注意，这种启发方式对具有大量端点的 Service 效果最佳。

### EndpointSlice 控制器 {#implementation-control-plane}

当启用此启发方式时，EndpointSlice 控制器负责在各个 EndpointSlice 上设置提示信息。
控制器按比例给每个区域分配一定比例数量的端点。
这个比例基于在该区域中运行的节点的[可分配](/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable)
CPU 核心数。例如，如果一个区域有 2 个 CPU 核心，而另一个区域只有 1 个 CPU 核心，
那么控制器将给那个有 2 CPU 的区域分配两倍数量的端点。

以下示例展示了提供提示信息后 EndpointSlice 的样子：

```yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: example-hints
  labels:
    kubernetes.io/service-name: example-svc
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 80
endpoints:
  - addresses:
      - "10.1.2.3"
    conditions:
      ready: true
    hostname: pod-1
    zone: zone-a
    hints:
      forZones:
        - name: "zone-a"
```

### kube-proxy {#implementation-kube-proxy}

kube-proxy 组件依据 EndpointSlice 控制器设置的提示，过滤由它负责路由的端点。
在大多数场合，这意味着 kube-proxy 可以把流量路由到同一个区域的端点。
有时，控制器在另一不同的区域中分配端点，以确保在多个区域之间更平均地分配端点。
这会导致部分流量被路由到其他区域。

## 保护措施 {#safeguards}

Kubernetes 控制平面和每个节点上的 kube-proxy 在使用拓扑感知提示信息前，会应用一些保护措施规则。
如果规则无法顺利通过，kube-proxy 将无视区域限制，从集群中的任意位置选择端点。

1. **端点数量不足：** 如果一个集群中，端点数量少于区域数量，控制器不创建任何提示。

2. **不可能实现均衡分配：** 在一些场合中，不可能实现端点在区域中的平衡分配。
   例如，假设 zone-a 比 zone-b 大两倍，但只有 2 个端点，
   那分配到 zone-a 的端点可能收到比 zone-b 多两倍的流量。
   如果控制器不能确保此“期望的过载”值低于每一个区域可接受的阈值，控制器将不添加提示信息。
   重要的是，这不是基于实时反馈。所以对于特定的端点仍有可能超载。

3. **一个或多个 Node 信息不足：** 如果任一节点没有设置标签 `topology.kubernetes.io/zone`，
   或没有上报可分配的 CPU 数据，控制平面将不会设置任何拓扑感知提示，
   进而 kube-proxy 也就不能根据区域来过滤端点。

4. **至少一个端点没有设置区域提示：** 当这种情况发生时，
   kube-proxy 会假设从拓扑感知提示到拓扑感知路由（或反方向）的迁移仍在进行中，
   在这种场合下过滤 Service 的端点是有风险的，所以 kube-proxy 回退到使用所有端点。

5. **提示中不存在某区域：** 如果 kube-proxy 无法找到提示中指向它当前所在的区域的端点，
   它将回退到使用来自所有区域的端点。当你向现有集群新增新的区域时，这种情况发生概率很高。

## 限制 {#constraints}

* 当 Service 的 `externalTrafficPolicy` 或 `internalTrafficPolicy` 设置值为 `Local` 时，
  系统将不使用拓扑感知提示信息。你可以在同一集群中的不同服务上使用这两个特性，但不能在同一个服务上这么做。

* 这种方法不适用于大部分流量来自于一部分区域的 Service。
  相反，这项技术的假设是入站流量与各区域中节点的服务能力成比例关系。

* EndpointSlice 控制器在计算各区域的比例时，会忽略未就绪的节点。
  在大部分节点未就绪的场景下，这样做会带来非预期的结果。

* EndpointSlice 控制器忽略设置了 `node-role.kubernetes.io/control-plane` 或
  `node-role.kubernetes.io/master` 标签的节点。如果工作负载也在这些节点上运行，也可能会产生问题。

* EndpointSlice 控制器在分派或计算各区域的比例时，并不会考虑
  {{< glossary_tooltip text="容忍度" term_id="toleration" >}}。
  如果 Service 背后的各 Pod 被限制只能运行在集群节点的一个子集上，计算比例时不会考虑这点。

* 这项技术和自动扩缩容机制之间可能存在冲突。例如，如果大量流量来源于同一个区域，
  那只有分配到该区域的端点才可用来处理流量。这会导致
  {{< glossary_tooltip text="Pod 自动水平扩缩容" term_id="horizontal-pod-autoscaler" >}}
  要么不能处理这种场景，要么会在别的区域添加 Pod。

## 自定义启发方式   {#custom-heuristics}

Kubernetes 的部署方式有很多种，没有一种按区域分配端点的启发式方法能够适用于所有场景。
此特性的一个关键目标是：如果内置的启发方式不能满足你的使用场景，则可以开发自定义的启发方式。
启用自定义启发方式的第一步包含在了 1.27 版本中。
这是一个限制性较强的实现，可能尚未涵盖一些重要的、可进一步探索的场景。

## {{% heading "whatsnext" %}}

* 参阅[使用 Service 连接到应用](/zh-cn/docs/tutorials/services/connect-applications-service/)教程
