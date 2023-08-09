---
title: 租约
content_type: concept
weight: 30
---


分布式系统通常需要**租约（Lease）**；租约提供了一种机制来锁定共享资源并协调集合成员之间的活动。
在 Kubernetes 中，租约概念表示为 `coordination.k8s.io`
{{< glossary_tooltip text="API 组" term_id="api-group" >}}中的
[Lease](/zh-cn/docs/reference/kubernetes-api/cluster-resources/lease-v1/) 对象，
常用于类似节点心跳和组件级领导者选举等系统核心能力。


## 节点心跳  {#node-heart-beats}

Kubernetes 使用 Lease API 将 kubelet 节点心跳传递到 Kubernetes API 服务器。
对于每个 `Node`，在 `kube-node-lease` 名字空间中都有一个具有匹配名称的 `Lease` 对象。
在此基础上，每个 kubelet 心跳都是对该 `Lease` 对象的 **update** 请求，更新该 Lease 的 `spec.renewTime` 字段。
Kubernetes 控制平面使用此字段的时间戳来确定此 `Node` 的可用性。

更多细节请参阅 [Node Lease 对象](/zh-cn/docs/concepts/architecture/nodes/#heartbeats)。

## 领导者选举  {#leader-election}

Kubernetes 也使用 Lease 确保在任何给定时间某个组件只有一个实例在运行。
这在高可用配置中由 `kube-controller-manager` 和 `kube-scheduler` 等控制平面组件进行使用，
这些组件只应有一个实例激活运行，而其他实例待机。

## API 服务器身份   {#api-server-identity}

{{< feature-state for_k8s_version="v1.26" state="beta" >}}

从 Kubernetes v1.26 开始，每个 `kube-apiserver` 都使用 Lease API 将其身份发布到系统中的其他位置。
虽然它本身并不是特别有用，但为客户端提供了一种机制来发现有多少个 `kube-apiserver` 实例正在操作
Kubernetes 控制平面。kube-apiserver 租约的存在使得未来可以在各个 kube-apiserver 之间协调新的能力。

你可以检查 `kube-system` 名字空间中名为 `kube-apiserver-<sha256-hash>` 的 Lease 对象来查看每个
kube-apiserver 拥有的租约。你还可以使用标签选择算符 `k8s.io/component=kube-apiserver`：

```shell
kubectl -n kube-system get lease -l k8s.io/component=kube-apiserver
```

```
NAME                                        HOLDER                                                                           AGE
kube-apiserver-c4vwjftbvpc5os2vvzle4qg27a   kube-apiserver-c4vwjftbvpc5os2vvzle4qg27a_9cbf54e5-1136-44bd-8f9a-1dcd15c346b4   5m33s
kube-apiserver-dz2dqprdpsgnm756t5rnov7yka   kube-apiserver-dz2dqprdpsgnm756t5rnov7yka_84f2a85d-37c1-4b14-b6b9-603e62e4896f   4m23s
kube-apiserver-fyloo45sdenffw2ugwaz3likua   kube-apiserver-fyloo45sdenffw2ugwaz3likua_c5ffa286-8a9a-45d4-91e7-61118ed58d2e   4m43s
```

租约名称中使用的 SHA256 哈希基于 API 服务器所看到的操作系统主机名生成。
每个 kube-apiserver 都应该被配置为使用集群中唯一的主机名。
使用相同主机名的 kube-apiserver 新实例将使用新的持有者身份接管现有 Lease，而不是实例化新的 Lease 对象。
你可以通过检查 `kubernetes.io/hostname` 标签的值来查看 kube-apisever 所使用的主机名：

```shell
kubectl -n kube-system get lease kube-apiserver-c4vwjftbvpc5os2vvzle4qg27a -o yaml
```

```yaml
apiVersion: coordination.k8s.io/v1
kind: Lease
metadata:
  creationTimestamp: "2022-11-30T15:37:15Z"
  labels:
    k8s.io/component: kube-apiserver
    kubernetes.io/hostname: kind-control-plane
  name: kube-apiserver-c4vwjftbvpc5os2vvzle4qg27a
  namespace: kube-system
  resourceVersion: "18171"
  uid: d6c68901-4ec5-4385-b1ef-2d783738da6c
spec:
  holderIdentity: kube-apiserver-c4vwjftbvpc5os2vvzle4qg27a_9cbf54e5-1136-44bd-8f9a-1dcd15c346b4
  leaseDurationSeconds: 3600
  renewTime: "2022-11-30T18:04:27.912073Z"
```

kube-apiserver 中不再存续的已到期租约将在到期 1 小时后被新的 kube-apiserver 作为垃圾收集。

你可以通过禁用 `APIServerIdentity`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)来禁用 API 服务器身份租约。

## 工作负载    {#custom-workload}

你自己的工作负载可以定义自己使用的 Lease。例如，
你可以运行自定义的{{< glossary_tooltip term_id="controller" text="控制器" >}}，
让主要成员或领导者成员在其中执行其对等方未执行的操作。
你定义一个 Lease，以便控制器副本可以使用 Kubernetes API 进行协调以选择或选举一个领导者。
如果你使用 Lease，良好的做法是为明显关联到产品或组件的 Lease 定义一个名称。
例如，如果你有一个名为 Example Foo 的组件，可以使用名为 `example-foo` 的 Lease。

如果集群操作员或其他终端用户可以部署一个组件的多个实例，
则选择名称前缀并挑选一种机制（例如 Deployment 名称的哈希）以避免 Lease 的名称冲突。

你可以使用另一种方式来达到相同的效果：不同的软件产品不相互冲突。
