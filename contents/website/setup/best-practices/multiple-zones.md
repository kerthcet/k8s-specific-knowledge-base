---
title: 运行于多可用区环境
weight: 10
content_type: concept
---


本页描述如何跨多个区（Zone）中运行集群。


## 背景

Kubernetes 从设计上允许同一个 Kubernetes 集群跨多个失效区来运行，
通常这些区位于某个称作 _区域（region）_ 逻辑分组中。
主要的云提供商都将区域定义为一组失效区的集合（也称作 _可用区（Availability Zones）_），
能够提供一组一致的功能特性：每个区域内，各个可用区提供相同的 API 和服务。

典型的云体系结构都会尝试降低某个区中的失效影响到其他区中服务的概率。

## 控制面行为   {#control-plane-behavior}

所有的[控制面组件](/zh-cn/docs/concepts/overview/components/#control-plane-components)
都支持以一组可相互替换的资源池的形式来运行，每个组件都有多个副本。

当你部署集群控制面时，应将控制面组件的副本跨多个失效区来部署。
如果可用性是一个很重要的指标，应该选择至少三个失效区，并将每个
控制面组件（API 服务器、调度器、etcd、控制器管理器）复制多个副本，
跨至少三个失效区来部署。如果你在运行云控制器管理器，则也应该将
该组件跨所选的三个失效区来部署。

{{< note >}}
Kubernetes 并不会为 API 服务器端点提供跨失效区的弹性。
你可以为集群 API 服务器使用多种技术来提升其可用性，包括使用
DNS 轮转、SRV 记录或者带健康检查的第三方负载均衡解决方案等等。
{{< /note >}}

## 节点行为   {#node-behavior}

Kubernetes 自动为负载资源（如{{< glossary_tooltip text="Deployment" term_id="deployment" >}}
或 {{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}})）
跨集群中不同节点来部署其 Pods。
这种分布逻辑有助于降低失效带来的影响。

节点启动时，每个节点上的 kubelet 会向 Kubernetes API 中代表该 kubelet 的 Node 对象
添加 {{< glossary_tooltip text="标签" term_id="label" >}}。
这些标签可能包含[区信息](/zh-cn/docs/reference/labels-annotations-taints/#topologykubernetesiozone)。

如果你的集群跨了多个可用区或者地理区域，你可以使用节点标签，结合
[Pod 拓扑分布约束](/zh-cn/docs/concepts/scheduling-eviction/topology-spread-constraints/)
来控制如何在你的集群中多个失效域之间分布 Pods。这里的失效域可以是
地理区域、可用区甚至是特定节点。
这些提示信息使得{{< glossary_tooltip text="调度器" term_id="kube-scheduler" >}}
能够更好地分布 Pods，以实现更好的可用性，降低因为某种失效给整个工作负载
带来的风险。

例如，你可以设置一种约束，确保某个 StatefulSet 中的三个副本都运行在
不同的可用区中，只要其他条件允许。你可以通过声明的方式来定义这种约束，
而不需要显式指定每个工作负载使用哪些可用区。

### 跨多个区分布节点 {#distributing-nodes-across-zones}

Kubernetes 的核心逻辑并不会帮你创建节点，你需要自行完成此操作，或者使用
类似 [Cluster API](https://cluster-api.sigs.k8s.io/) 这类工具来替你管理节点。

使用类似 Cluster API 这类工具，你可以跨多个失效域来定义一组用做你的集群
工作节点的机器，以及当整个区的服务出现中断时如何自动治愈集群的策略。

## 为 Pods 手动指定区

你可以应用[节点选择算符约束](/zh-cn/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector)
到你所创建的 Pods 上，或者为 Deployment、StatefulSet 或 Job 这类工作负载资源
中的 Pod 模板设置此类约束。

## 跨区的存储访问

当创建持久卷时，`PersistentVolumeLabel` 
[准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/)
会自动向那些链接到特定区的 PersistentVolume 添加区标签。
{{< glossary_tooltip text="调度器" term_id="kube-scheduler" >}}通过其
`NoVolumeZoneConflict` 断言确保申领给定 PersistentVolume 的 Pods 只会
被调度到该卷所在的可用区。

你可以为 PersistentVolumeClaim 指定{{< glossary_tooltip text="StorageClass" term_id="storage-class" >}}
以设置该类中的存储可以使用的失效域（区）。
要了解如何配置能够感知失效域或区的 StorageClass，请参阅
[可用的拓扑逻辑](/zh-cn/docs/concepts/storage/storage-classes/#allowed-topologies)。

## 网络  {#networking}

Kubernetes 自身不提供与可用区相关的联网配置。
你可以使用[网络插件](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
来配置集群的联网，该网络解决方案可能拥有一些与可用区相关的元素。
例如，如果你的云提供商支持 `type=LoadBalancer` 的 Service，则负载均衡器
可能仅会将请求流量发送到运行在负责处理给定连接的负载均衡器组件所在的区。
请查阅云提供商的文档了解详细信息。

对于自定义的或本地集群部署，也可以考虑这些因素
{{< glossary_tooltip text="Service" term_id="service" >}} 
{{< glossary_tooltip text="Ingress" term_id="ingress" >}} 的行为，
包括处理不同失效区的方法，在很大程度上取决于你的集群是如何搭建的。

## 失效恢复    {#fault-recovery}

在搭建集群时，你可能需要考虑当某区域中的所有失效区都同时掉线时，是否以及如何
恢复服务。例如，你是否要求在某个区中至少有一个节点能够运行 Pod？
请确保任何对集群很关键的修复工作都不要指望集群中至少有一个健康节点。
例如：当所有节点都不健康时，你可能需要运行某个修复性的 Job，
该 Job 要设置特定的{{< glossary_tooltip text="容忍度" term_id="toleration" >}}
以便修复操作能够至少将一个节点恢复为可用状态。

Kubernetes 对这类问题没有现成的解决方案；不过这也是要考虑的因素之一。

## {{% heading "whatsnext" %}}

要了解调度器如何在集群中放置 Pods 并遵从所配置的约束，可参阅
[调度与驱逐](/zh-cn/docs/concepts/scheduling-eviction/)。

