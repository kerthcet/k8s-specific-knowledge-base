---
title: 使用源 IP
content_type: tutorial
min-kubernetes-server-version: v1.5
weight: 10
---


运行在 Kubernetes 集群中的应用程序通过 Service 抽象发现彼此并相互通信，它们也用 Service 与外部世界通信。
本文解释了发送到不同类型 Service 的数据包的源 IP 会发生什么情况，以及如何根据需要切换此行为。

## {{% heading "prerequisites" %}}

## 术语表  {#terminology}

本文使用了下列术语：

{{< comment >}}
如果本地化此部分，请链接到目标本地化的等效 Wikipedia 页面。
{{< /comment >}}

[NAT](https://zh.wikipedia.org/wiki/%E7%BD%91%E7%BB%9C%E5%9C%B0%E5%9D%80%E8%BD%AC%E6%8D%A2)
: 网络地址转换

[Source NAT](https://en.wikipedia.org/wiki/Network_address_translation#SNAT)
: 替换数据包上的源 IP；在本页面中，这通常意味着替换为节点的 IP 地址

[Destination NAT](https://en.wikipedia.org/wiki/Network_address_translation#DNAT)
: 替换数据包上的目标 IP；在本页面中，这通常意味着替换为 {{<glossary_tooltip text="Pod" term_id="pod" >}} 的 IP 地址

[VIP](/zh-cn/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies)
: 一个虚拟 IP 地址，例如分配给 Kubernetes 中每个 {{<glossary_tooltip text="Service" term_id="service" >}} 的 IP 地址

[Kube-proxy](/zh-cn/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies)
: 一个网络守护程序，在每个节点上协调 Service VIP 管理

## 先决条件  {#prerequisites}

{{< include "task-tutorial-prereqs.md" >}}

示例使用一个小型 nginx Web 服务器，服务器通过 HTTP 标头返回它接收到的请求的源 IP。
你可以按如下方式创建它：

```shell
kubectl create deployment source-ip-app --image=registry.k8s.io/echoserver:1.4
```
输出为：

```
deployment.apps/source-ip-app created
```

## {{% heading "objectives" %}}

* 通过多种类型的 Service 暴露一个简单应用
* 了解每种 Service 类型如何处理源 IP NAT
* 了解保留源 IP 所涉及的权衡


## `Type=ClusterIP` 类型 Service 的源 IP  {#source-ip-for-services-with-type-clusterip}

如果你在 [iptables 模式](/zh-cn/docs/reference/networking/virtual-ips/#proxy-mode-iptables)（默认）下运行
kube-proxy，则从集群内发送到 ClusterIP 的数据包永远不会进行源 NAT。
你可以通过在运行 kube-proxy 的节点上获取 `http://localhost:10249/proxyMode` 来查询 kube-proxy 模式。

```console
kubectl get nodes
```
输出类似于：

```
NAME                           STATUS     ROLES    AGE     VERSION
kubernetes-node-6jst   Ready      <none>   2h      v1.13.0
kubernetes-node-cx31   Ready      <none>   2h      v1.13.0
kubernetes-node-jj1t   Ready      <none>   2h      v1.13.0
```

在其中一个节点上获取代理模式（kube-proxy 监听 10249 端口）：

```shell
# 在要查询的节点上的 Shell 中运行
curl http://localhost:10249/proxyMode
```
输出为：

```
iptables
```

你可以通过在源 IP 应用程序上创建 Service 来测试源 IP 保留：

```shell
kubectl expose deployment source-ip-app --name=clusterip --port=80 --target-port=8080
```
输出为：

```
service/clusterip exposed
```

```shell
kubectl get svc clusterip
```
输出类似于：

```
NAME         TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
clusterip    ClusterIP   10.0.170.92   <none>        80/TCP    51s
```

并从同一集群中的 Pod 中访问 `ClusterIP`：

```shell
kubectl run busybox -it --image=busybox:1.28 --restart=Never --rm
```
输出类似于：

```
Waiting for pod default/busybox to be running, status is Pending, pod ready: false
If you don't see a command prompt, try pressing enter.
```
然后，你可以在该 Pod 中运行命令：

```shell
# 从 “kubectl run” 的终端中运行
ip addr
```
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
3: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1460 qdisc noqueue
    link/ether 0a:58:0a:f4:03:08 brd ff:ff:ff:ff:ff:ff
    inet 10.244.3.8/24 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::188a:84ff:feb0:26a5/64 scope link
       valid_lft forever preferred_lft forever
```

然后使用 `wget` 查询本地 Web 服务器：

```shell
# 将 “10.0.170.92” 替换为 Service 中名为 “clusterip” 的 IPv4 地址
wget -qO - 10.0.170.92
```

```
CLIENT VALUES:
client_address=10.244.3.8
command=GET
...
```

不管客户端 Pod 和服务器 Pod 位于同一节点还是不同节点，`client_address` 始终是客户端 Pod 的 IP 地址。

## `Type=NodePort` 类型 Service 的源 IP  {#source-ip-for-services-with-type-nodeport}

默认情况下，发送到 [`Type=NodePort`](/zh-cn/docs/concepts/services-networking/service/#type-nodeport)
的 Service 的数据包会经过源 NAT 处理。你可以通过创建一个 `NodePort` 的 Service 来测试这点：

```shell
kubectl expose deployment source-ip-app --name=nodeport --port=80 --target-port=8080 --type=NodePort
```
输出为：

```
service/nodeport exposed
```

```shell
NODEPORT=$(kubectl get -o jsonpath="{.spec.ports[0].nodePort}" services nodeport)
NODES=$(kubectl get nodes -o jsonpath='{ $.items[*].status.addresses[?(@.type=="InternalIP")].address }')
```

如果你在云供应商上运行，你可能需要为上面报告的 `nodes:nodeport` 打开防火墙规则。
现在你可以尝试通过上面分配的节点端口从集群外部访问 Service。

```shell
for node in $NODES; do curl -s $node:$NODEPORT | grep -i client_address; done
```
输出类似于：

```
client_address=10.180.1.1
client_address=10.240.0.5
client_address=10.240.0.3
```

请注意，这些并不是正确的客户端 IP，它们是集群的内部 IP。这是所发生的事情：

* 客户端发送数据包到 `node2:nodePort`
* `node2` 使用它自己的 IP 地址替换数据包的源 IP 地址（SNAT）
* `node2` 将数据包上的目标 IP 替换为 Pod IP
* 数据包被路由到 node1，然后到端点
* Pod 的回复被路由回 node2
* Pod 的回复被发送回给客户端

用图表示：
{{< figure src="/zh-cn/docs/images/tutor-service-nodePort-fig01.svg" alt="图 1：源 IP NodePort" class="diagram-large" caption="如图。使用 SNAT 的源 IP（Type=NodePort）" link="https://mermaid.live/edit#pako:eNqNkV9rwyAUxb-K3LysYEqS_WFYKAzat9GHdW9zDxKvi9RoMIZtlH732ZjSbE970cu5v3s86hFqJxEYfHjRNeT5ZcUtIbXRaMNN2hZ5vrYRqt52cSXV-4iMSuwkZiYtyX739EqWaahMQ-V1qPxDVLNOvkYrO6fj2dupWMR2iiT6foOKdEZoS5Q2hmVSStoH7w7IMqXUVOefWoaG3XVftHbGeZYVRbH6ZXJ47CeL2-qhxvt_ucTe1SUlpuMN6CX12XeGpLdJiaMMFFr0rdAyvvfxjHEIDbbIgcVSohKDCRy4PUV06KQIuJU6OA9MCdMjBTEEt_-2NbDgB7xAGy3i97VJPP0ABRmcqg" >}}

为避免这种情况，Kubernetes 有一个特性可以[保留客户端源 IP](/zh-cn/docs/tasks/access-application-cluster/create-external-load-balancer/#preserving-the-client-source-ip)。
如果将 `service.spec.externalTrafficPolicy` 设置为 `Local`，
kube-proxy 只会将代理请求代理到本地端点，而不会将流量转发到其他节点。
这种方法保留了原始源 IP 地址。如果没有本地端点，则发送到该节点的数据包将被丢弃，
因此你可以在任何数据包处理规则中依赖正确的源 IP，你可能会应用一个数据包使其通过该端点。

设置 `service.spec.externalTrafficPolicy` 字段如下：

```shell
kubectl patch svc nodeport -p '{"spec":{"externalTrafficPolicy":"Local"}}'
```
输出为：

```
service/nodeport patched
```

现在，重新运行测试：

```shell
for node in $NODES; do curl --connect-timeout 1 -s $node:$NODEPORT | grep -i client_address; done
```
输出类似于：
```
client_address=198.51.100.79
```

请注意，你只从运行端点 Pod 的节点得到了回复，这个回复有**正确的**客户端 IP。

这是发生的事情：

* 客户端将数据包发送到没有任何端点的 `node2:nodePort`
* 数据包被丢弃
* 客户端发送数据包到**必有**端点的 `node1:nodePort`
* node1 使用正确的源 IP 地址将数据包路由到端点

用图表示：
{{< figure src="/zh-cn/docs/images/tutor-service-nodePort-fig02.svg" alt="图 2：源 IP NodePort" class="diagram-large" caption="如图。源 IP（Type=NodePort）保存客户端源 IP 地址" link="" >}}

## `Type=LoadBalancer` 类型 Service 的源 IP  {#source-ip-for-services-with-type-loadbalancer}

默认情况下，发送到 [`Type=LoadBalancer`](/zh-cn/docs/concepts/services-networking/service/#loadbalancer)
的 Service 的数据包经过源 NAT处理，因为所有处于 `Ready` 状态的可调度 Kubernetes
节点对于负载均衡的流量都是符合条件的。
因此，如果数据包到达一个没有端点的节点，系统会将其代理到一个**带有**端点的节点，用该节点的 IP 替换数据包上的源 IP（如上一节所述）。

你可以通过负载均衡器上暴露 source-ip-app 进行测试：

```shell
kubectl expose deployment source-ip-app --name=loadbalancer --port=80 --target-port=8080 --type=LoadBalancer
```
输出为：
```
service/loadbalancer exposed
```

打印 Service 的 IP 地址：
```console
kubectl get svc loadbalancer
```
输出类似于：
```
NAME           TYPE           CLUSTER-IP    EXTERNAL-IP       PORT(S)   AGE
loadbalancer   LoadBalancer   10.0.65.118   203.0.113.140     80/TCP    5m
```

接下来，发送请求到 Service 的 的外部 IP（External-IP）：
```shell
curl 203.0.113.140
```
输出类似于：
```
CLIENT VALUES:
client_address=10.240.0.5
...
```

然而，如果你在 Google Kubernetes Engine/GCE 上运行，
将相同的 `service.spec.externalTrafficPolicy` 字段设置为 `Local`，
故意导致健康检查失败，从而强制没有端点的节点把自己从负载均衡流量的可选节点列表中删除。

用图表示：

![具有 externalTrafficPolicy 的源 IP](/zh-cn/docs/images/sourceip-externaltrafficpolicy.svg)

你可以通过设置注解进行测试：

```shell
kubectl patch svc loadbalancer -p '{"spec":{"externalTrafficPolicy":"Local"}}'
```

你应该能够立即看到 Kubernetes 分配的 `service.spec.healthCheckNodePort` 字段：

```shell
kubectl get svc loadbalancer -o yaml | grep -i healthCheckNodePort
```
输出类似于：
```yaml
  healthCheckNodePort: 32122
```

`service.spec.healthCheckNodePort` 字段指向每个在 `/healthz`
路径上提供健康检查的节点的端口。你可以这样测试：

```shell
kubectl get pod -o wide -l app=source-ip-app
```
输出类似于：
```
NAME                            READY     STATUS    RESTARTS   AGE       IP             NODE
source-ip-app-826191075-qehz4   1/1       Running   0          20h       10.180.1.136   kubernetes-node-6jst
```

使用 `curl` 获取各个节点上的 `/healthz` 端点：
```shell
# 在你选择的节点上本地运行
curl localhost:32122/healthz
```
```
1 Service Endpoints found
```

在不同的节点上，你可能会得到不同的结果：
```shell
# 在你选择的节点上本地运行
curl localhost:32122/healthz
```
```
No Service Endpoints Found
```

在{{<glossary_tooltip text="控制平面" term_id="control-plane" >}}上运行的控制器负责分配云负载均衡器。
同一个控制器还在每个节点上分配指向此端口/路径的 HTTP 健康检查。
等待大约 10 秒，让 2 个没有端点的节点健康检查失败，然后使用 `curl` 查询负载均衡器的 IPv4 地址：

```shell
curl 203.0.113.140
```
输出类似于：
```
CLIENT VALUES:
client_address=198.51.100.79
...
```

## 跨平台支持  {#cross-platform-support}

只有部分云提供商为 `Type=LoadBalancer` 的 Service 提供保存源 IP 的支持。
你正在运行的云提供商可能会以几种不同的方式满足对负载均衡器的请求：

1. 使用终止客户端连接并打开到你的节点/端点的新连接的代理。
   在这种情况下，源 IP 将始终是云 LB 的源 IP，而不是客户端的源 IP。

2. 使用数据包转发器，这样客户端发送到负载均衡器 VIP
   的请求最终会到达具有客户端源 IP 的节点，而不是中间代理。

第一类负载均衡器必须使用负载均衡器和后端之间商定的协议来传达真实的客户端 IP，
例如 HTTP [转发](https://tools.ietf.org/html/rfc7239#section-5.2)或
[X-FORWARDED-FOR](https://zh.wikipedia.org/wiki/X-Forwarded-For)
标头，或[代理协议](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)。
第二类负载均衡器可以通过创建指向存储在 Service 上的 `service.spec.healthCheckNodePort`
字段中的端口的 HTTP 健康检查来利用上述功能。

## {{% heading "cleanup" %}}

删除 Service：

```shell
kubectl delete svc -l app=source-ip-app
```

删除 Deployment、ReplicaSet 和 Pod：

```shell
kubectl delete deployment source-ip-app
```

## {{% heading "whatsnext" %}}

* 详细了解[通过 Service 连接应用程序](/zh-cn/docs/tutorials/services/connect-applications-service/)
* 阅读如何[创建外部负载均衡器](/zh-cn/docs/tasks/access-application-cluster/create-external-load-balancer/)
