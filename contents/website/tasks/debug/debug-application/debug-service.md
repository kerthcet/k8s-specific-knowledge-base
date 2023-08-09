---
content_type: task
title: 调试 Service
weight: 20
---



对于新安装的 Kubernetes，经常出现的问题是 Service 无法正常运行。你已经通过
Deployment（或其他工作负载控制器）运行了 Pod，并创建 Service ，
但是当你尝试访问它时，没有任何响应。此文档有望对你有所帮助并找出问题所在。


## 在 Pod 中运行命令

对于这里的许多步骤，你可能希望知道运行在集群中的 Pod 看起来是什么样的。
最简单的方法是运行一个交互式的 busybox Pod：

```none
kubectl run -it --rm --restart=Never busybox --image=gcr.io/google-containers/busybox sh
```

{{< note >}}
如果没有看到命令提示符，请按回车。
{{< /note >}}

如果你已经有了你想使用的正在运行的 Pod，则可以运行以下命令去进入：

```shell
kubectl exec <POD-NAME> -c <CONTAINER-NAME> -- <COMMAND>
```

## 设置  {#setup}

为了完成本次实践的任务，我们先运行几个 Pod。
由于你可能正在调试自己的 Service，所以，你可以使用自己的信息进行替换，
或者你也可以跟着教程并开始下面的步骤来获得第二个数据点。

```shell
kubectl create deployment hostnames --image=registry.k8s.io/serve_hostname
```

```none
deployment.apps/hostnames created
```

`kubectl` 命令将打印创建或变更的资源的类型和名称，它们可以在后续命令中使用。
让我们将这个 deployment 的副本数扩至 3。

```shell
kubectl scale deployment hostnames --replicas=3
```

```none
deployment.apps/hostnames scaled
```

请注意这与你使用以下 YAML 方式启动 Deployment 类似：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: hostnames
  name: hostnames
spec:
  selector:
    matchLabels:
      app: hostnames
  replicas: 3
  template:
    metadata:
      labels:
        app: hostnames
    spec:
      containers:
      - name: hostnames
        image: registry.k8s.io/serve_hostname
```

"app" 标签是 `kubectl create deployment` 根据 Deployment 名称自动设置的。

确认你的 Pod 是运行状态:

```shell
kubectl get pods -l app=hostnames
```

```none
NAME                        READY     STATUS    RESTARTS   AGE
hostnames-632524106-bbpiw   1/1       Running   0          2m
hostnames-632524106-ly40y   1/1       Running   0          2m
hostnames-632524106-tlaok   1/1       Running   0          2m
```

你还可以确认你的 Pod 是否正在提供服务。你可以获取 Pod IP 地址列表并直接对其进行测试。

```shell
kubectl get pods -l app=hostnames \
    -o go-template='{{range .items}}{{.status.podIP}}{{"\n"}}{{end}}'
```

```none
10.244.0.5
10.244.0.6
10.244.0.7
```

用于本教程的示例容器通过 HTTP 在端口 9376 上提供其自己的主机名，
但是如果要调试自己的应用程序，则需要使用你的 Pod 正在侦听的端口号。

在 Pod 内运行：

```shell
for ep in 10.244.0.5:9376 10.244.0.6:9376 10.244.0.7:9376; do
    wget -qO- $ep
done
```

输出类似这样：

```
hostnames-632524106-bbpiw
hostnames-632524106-ly40y
hostnames-632524106-tlaok
```

如果此时你没有收到期望的响应，则你的 Pod 状态可能不健康，或者可能没有在你认为正确的端口上进行监听。
你可能会发现 `kubectl logs` 命令对于查看正在发生的事情很有用，
或者你可能需要通过`kubectl exec` 直接进入 Pod 中并从那里进行调试。

假设到目前为止一切都已按计划进行，那么你可以开始调查为何你的 Service 无法正常工作。

## Service 是否存在？   {#does-the-service-exist}

细心的读者会注意到我们实际上尚未创建 Service —— 这是有意而为之。
这一步有时会被遗忘，这是首先要检查的步骤。

那么，如果我尝试访问不存在的 Service 会怎样？ 
假设你有另一个 Pod 通过名称匹配到 Service，你将得到类似结果：

```shell
wget -O- hostnames
```

```none
Resolving hostnames (hostnames)... failed: Name or service not known.
wget: unable to resolve host address 'hostnames'
```

首先要检查的是该 Service 是否真实存在：

```shell
kubectl get svc hostnames
```

```none
No resources found.
Error from server (NotFound): services "hostnames" not found
```

让我们创建 Service。 和以前一样，在这次实践中 —— 你可以在此处使用自己的 Service 的内容。

```shell
kubectl expose deployment hostnames --port=80 --target-port=9376
```

```none
service/hostnames exposed
```

重新运行查询命令：

```shell
kubectl get svc hostnames
```

```none
NAME        TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
hostnames   ClusterIP   10.0.1.175   <none>        80/TCP    5s
```

现在你知道了 Service 确实存在。

同前，此步骤效果与通过 YAML 方式启动 Service 一样：

```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    app: hostnames
  name: hostnames
spec:
  selector:
    app: hostnames
  ports:
  - name: default
    protocol: TCP
    port: 80
    targetPort: 9376
```

为了突出配置范围的完整性，你在此处创建的 Service 使用的端口号与 Pods 不同。
对于许多真实的 Service，这些值可以是相同的。

## 是否存在影响目标 Pod 的网络策略入站规则？

如果你部署了任何可能影响到 `hostnames-*` Pod 的传入流量的网络策略入站规则，
则需要对其进行检查。

详细信息，请参阅[网络策略](/zh-cn/docs/concepts/services-networking/network-policies/)。

## Service 是否可通过 DNS 名字访问？  {#does-the-service-work-by-dns-name}

通常客户端通过 DNS 名称来匹配到 Service。

从相同命名空间下的 Pod 中运行以下命令：

```shell
nslookup hostnames
```

```none
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      hostnames
Address 1: 10.0.1.175 hostnames.default.svc.cluster.local
```

如果失败，那么你的 Pod 和 Service 可能位于不同的命名空间中，
请尝试使用限定命名空间的名称（同样在 Pod 内运行）：

```shell
nslookup hostnames.default
```

```none
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      hostnames.default
Address 1: 10.0.1.175 hostnames.default.svc.cluster.local
```

如果成功，那么需要调整你的应用，使用跨命名空间的名称去访问它，
或者在相同的命名空间中运行应用和 Service。如果仍然失败，请尝试一个完全限定的名称：

```shell
nslookup hostnames.default.svc.cluster.local
```

```none
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      hostnames.default.svc.cluster.local
Address 1: 10.0.1.175 hostnames.default.svc.cluster.local
```

注意这里的后缀："default.svc.cluster.local"。"default" 是我们正在操作的命名空间。
"svc" 表示这是一个 Service。"cluster.local" 是你的集群域，在你自己的集群中可能会有所不同。

你也可以在集群中的节点上尝试此操作：

{{< note >}}
10.0.0.10 是集群的 DNS 服务 IP，你的可能有所不同。
{{< /note >}}

```shell
nslookup hostnames.default.svc.cluster.local 10.0.0.10
```

```none
Server:         10.0.0.10
Address:        10.0.0.10#53

Name:   hostnames.default.svc.cluster.local
Address: 10.0.1.175
```

如果你能够使用完全限定的名称查找，但不能使用相对名称，则需要检查你 Pod 中的
`/etc/resolv.conf` 文件是否正确。在 Pod 中运行以下命令：

```shell
cat /etc/resolv.conf
```

你应该可以看到类似这样的输出：

```
nameserver 10.0.0.10
search default.svc.cluster.local svc.cluster.local cluster.local example.com
options ndots:5
```

`nameserver` 行必须指示你的集群的 DNS Service，
它是通过 `--cluster-dns` 标志传递到 kubelet 的。

`search` 行必须包含一个适当的后缀，以便查找 Service 名称。
在本例中，它查找本地命名空间（`default.svc.cluster.local`）中的服务和所有命名空间
（`svc.cluster.local`）中的服务，最后在集群（`cluster.local`）中查找服务的名称。
根据你自己的安装情况，可能会有额外的记录（最多 6 条）。
集群后缀是通过 `--cluster-domain` 标志传递给 `kubelet` 的。 
本文中，我们假定后缀是 “cluster.local”。
你的集群配置可能不同，这种情况下，你应该在上面的所有命令中更改它。

`options` 行必须设置足够高的 `ndots`，以便 DNS 客户端库考虑搜索路径。
在默认情况下，Kubernetes 将这个值设置为 5，这个值足够高，足以覆盖它生成的所有 DNS 名称。

### 是否存在 Service 能通过 DNS 名称访问？{#does-any-service-exist-in-dns}

如果上面的方式仍然失败，DNS 查找不到你需要的 Service ，你可以后退一步，
看看还有什么其它东西没有正常工作。
Kubernetes 主 Service 应该一直是工作的。在 Pod 中运行如下命令：

```shell
nslookup kubernetes.default
```
```none
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      kubernetes.default
Address 1: 10.0.0.1 kubernetes.default.svc.cluster.local
```

如果失败，你可能需要转到本文的 [kube-proxy](#is-the-kube-proxy-working) 节，
或者甚至回到文档的顶部重新开始，但不是调试你自己的 Service ，而是调试 DNS Service。

### Service 能够通过 IP 访问么？   {#does-the-service-work-by-ip}

假设你已经确认 DNS 工作正常，那么接下来要测试的是你的 Service 能否通过它的 IP 正常访问。
从集群中的一个 Pod，尝试访问 Service 的 IP（从上面的 `kubectl get` 命令获取）。

```shell
for i in $(seq 1 3); do 
    wget -qO- 10.0.1.175:80
done
```

输出应该类似这样：

```
hostnames-632524106-bbpiw
hostnames-632524106-ly40y
hostnames-632524106-tlaok
```

如果 Service 状态是正常的，你应该得到正确的响应。
如果没有，有很多可能出错的地方，请继续阅读。

## Service 的配置是否正确？   {#is-the-service-defined-correctly}

这听起来可能很愚蠢，但你应该两次甚至三次检查你的 Service 配置是否正确，并且与你的 Pod 匹配。
查看你的 Service 配置并验证它：

```shell
kubectl get service hostnames -o json
```

```json
{
    "kind": "Service",
    "apiVersion": "v1",
    "metadata": {
        "name": "hostnames",
        "namespace": "default",
        "uid": "428c8b6c-24bc-11e5-936d-42010af0a9bc",
        "resourceVersion": "347189",
        "creationTimestamp": "2015-07-07T15:24:29Z",
        "labels": {
            "app": "hostnames"
        }
    },
    "spec": {
        "ports": [
            {
                "name": "default",
                "protocol": "TCP",
                "port": 80,
                "targetPort": 9376,
                "nodePort": 0
            }
        ],
        "selector": {
            "app": "hostnames"
        },
        "clusterIP": "10.0.1.175",
        "type": "ClusterIP",
        "sessionAffinity": "None"
    },
    "status": {
        "loadBalancer": {}
    }
}
```

* 你想要访问的 Service 端口是否在 `spec.ports[]` 中列出？
* `targetPort` 对你的 Pod 来说正确吗（许多 Pod 使用与 Service 不同的端口）？
* 如果你想使用数值型端口，那么它的类型是一个数值（9376）还是字符串 “9376”？
* 如果你想使用名称型端口，那么你的 Pod 是否暴露了一个同名端口？
* 端口的 `protocol` 和 Pod 的是否对应？

## Service 有 Endpoints 吗？  {#does-the-service-have-any-endpoints}

如果你已经走到了这一步，你已经确认你的 Service 被正确定义，并能通过 DNS 解析。
现在，让我们检查一下，你运行的 Pod 确实是被 Service 选中的。

早些时候，我们已经看到 Pod 是运行状态。我们可以再检查一下：

```shell
kubectl get pods -l app=hostnames
```

```none
NAME                        READY     STATUS    RESTARTS   AGE
hostnames-632524106-bbpiw   1/1       Running   0          1h
hostnames-632524106-ly40y   1/1       Running   0          1h
hostnames-632524106-tlaok   1/1       Running   0          1h
```

`-l app=hostnames` 参数是在 Service 上配置的标签选择器。

“AGE” 列表明这些 Pod 已经启动一个小时了，这意味着它们运行良好，而未崩溃。

"RESTARTS" 列表明 Pod 没有经常崩溃或重启。经常性崩溃可能导致间歇性连接问题。
如果重启次数过大，通过[调试 Pod](/zh-cn/docs/tasks/debug/debug-application/debug-pods)
了解相关技术。

在 Kubernetes 系统中有一个控制回路，它评估每个 Service 的选择算符，并将结果保存到
Endpoints 对象中。

```shell
kubectl get endpoints hostnames
```

```
NAME        ENDPOINTS
hostnames   10.244.0.5:9376,10.244.0.6:9376,10.244.0.7:9376
```

这证实 Endpoints 控制器已经为你的 Service 找到了正确的 Pods。
如果 `ENDPOINTS` 列的值为 `<none>`，则应检查 Service 的 `spec.selector` 字段，
以及你实际想选择的 Pod 的 `metadata.labels` 的值。
常见的错误是输入错误或其他错误，例如 Service 想选择 `app=hostnames`，但是
Deployment 指定的是 `run=hostnames`。在 1.18之前的版本中 `kubectl run`
也可以被用来创建 Deployment。

## Pod 工作正常吗？   {#are-the-pods-working}

至此，你知道你的 Service 已存在，并且已匹配到你的Pod。在本实验的开始，你已经检查了 Pod 本身。
让我们再次检查 Pod 是否确实在工作 - 你可以绕过 Service 机制并直接转到 Pod，
如上面的 Endpoints 所示。

{{< note >}}
这些命令使用的是 Pod 端口（9376），而不是 Service 端口（80）。
{{< /note >}}

在 Pod 中运行：

```shell
for ep in 10.244.0.5:9376 10.244.0.6:9376 10.244.0.7:9376; do
    wget -qO- $ep
done
```

输出应该类似这样：

```
hostnames-632524106-bbpiw
hostnames-632524106-ly40y
hostnames-632524106-tlaok
```

你希望 Endpoint 列表中的每个 Pod 都返回自己的主机名。 
如果情况并非如此（或你自己的 Pod 的正确行为是什么），你应调查发生了什么事情。

## kube-proxy 正常工作吗？  {#is-the-kube-proxy-working}

如果你到达这里，则说明你的 Service 正在运行，拥有 Endpoints，Pod 真正在提供服务。
此时，整个 Service 代理机制是可疑的。让我们一步一步地确认它没问题。

Service 的默认实现（在大多数集群上应用的）是 kube-proxy。
这是一个在每个节点上运行的程序，负责配置用于提供 Service 抽象的机制之一。
如果你的集群不使用 kube-proxy，则以下各节将不适用，你将必须检查你正在使用的 Service 的实现方式。

### kube-proxy 正常运行吗？  {#is-kube-proxy working}

确认 `kube-proxy` 正在节点上运行。在节点上直接运行，你将会得到类似以下的输出：

```shell
ps auxw | grep kube-proxy
```

```none
root  4194  0.4  0.1 101864 17696 ?    Sl Jul04  25:43 /usr/local/bin/kube-proxy --master=https://kubernetes-master --kubeconfig=/var/lib/kube-proxy/kubeconfig --v=2
```

下一步，确认它并没有出现明显的失败，比如连接主节点失败。要做到这一点，你必须查看日志。
访问日志的方式取决于你节点的操作系统。
在某些操作系统上日志是一个文件，如 /var/log/messages kube-proxy.log，
而其他操作系统使用 `journalctl` 访问日志。你应该看到输出类似于：

```none
I1027 22:14:53.995134    5063 server.go:200] Running in resource-only container "/kube-proxy"
I1027 22:14:53.998163    5063 server.go:247] Using iptables Proxier.
I1027 22:14:54.038140    5063 proxier.go:352] Setting endpoints for "kube-system/kube-dns:dns-tcp" to [10.244.1.3:53]
I1027 22:14:54.038164    5063 proxier.go:352] Setting endpoints for "kube-system/kube-dns:dns" to [10.244.1.3:53]
I1027 22:14:54.038209    5063 proxier.go:352] Setting endpoints for "default/kubernetes:https" to [10.240.0.2:443]
I1027 22:14:54.038238    5063 proxier.go:429] Not syncing iptables until Services and Endpoints have been received from master
I1027 22:14:54.040048    5063 proxier.go:294] Adding new service "default/kubernetes:https" at 10.0.0.1:443/TCP
I1027 22:14:54.040154    5063 proxier.go:294] Adding new service "kube-system/kube-dns:dns" at 10.0.0.10:53/UDP
I1027 22:14:54.040223    5063 proxier.go:294] Adding new service "kube-system/kube-dns:dns-tcp" at 10.0.0.10:53/TCP
```

如果你看到有关无法连接主节点的错误消息，则应再次检查节点配置和安装步骤。

`kube-proxy` 无法正确运行的可能原因之一是找不到所需的 `conntrack` 二进制文件。
在一些 Linux 系统上，这也是可能发生的，这取决于你如何安装集群，
例如，你是手动开始一步步安装 Kubernetes。如果是这样的话，你需要手动安装
`conntrack` 包（例如，在 Ubuntu 上使用 `sudo apt install conntrack`），然后重试。

Kube-proxy 可以以若干模式之一运行。在上述日志中，`Using iptables Proxier`
行表示 kube-proxy 在 "iptables" 模式下运行。
最常见的另一种模式是 "ipvs"。

#### Iptables 模式   {#iptables-mode}

在 "iptables" 模式中, 你应该可以在节点上看到如下输出:

```shell
iptables-save | grep hostnames
```

```none
-A KUBE-SEP-57KPRZ3JQVENLNBR -s 10.244.3.6/32 -m comment --comment "default/hostnames:" -j MARK --set-xmark 0x00004000/0x00004000
-A KUBE-SEP-57KPRZ3JQVENLNBR -p tcp -m comment --comment "default/hostnames:" -m tcp -j DNAT --to-destination 10.244.3.6:9376
-A KUBE-SEP-WNBA2IHDGP2BOBGZ -s 10.244.1.7/32 -m comment --comment "default/hostnames:" -j MARK --set-xmark 0x00004000/0x00004000
-A KUBE-SEP-WNBA2IHDGP2BOBGZ -p tcp -m comment --comment "default/hostnames:" -m tcp -j DNAT --to-destination 10.244.1.7:9376
-A KUBE-SEP-X3P2623AGDH6CDF3 -s 10.244.2.3/32 -m comment --comment "default/hostnames:" -j MARK --set-xmark 0x00004000/0x00004000
-A KUBE-SEP-X3P2623AGDH6CDF3 -p tcp -m comment --comment "default/hostnames:" -m tcp -j DNAT --to-destination 10.244.2.3:9376
-A KUBE-SERVICES -d 10.0.1.175/32 -p tcp -m comment --comment "default/hostnames: cluster IP" -m tcp --dport 80 -j KUBE-SVC-NWV5X2332I4OT4T3
-A KUBE-SVC-NWV5X2332I4OT4T3 -m comment --comment "default/hostnames:" -m statistic --mode random --probability 0.33332999982 -j KUBE-SEP-WNBA2IHDGP2BOBGZ
-A KUBE-SVC-NWV5X2332I4OT4T3 -m comment --comment "default/hostnames:" -m statistic --mode random --probability 0.50000000000 -j KUBE-SEP-X3P2623AGDH6CDF3
-A KUBE-SVC-NWV5X2332I4OT4T3 -m comment --comment "default/hostnames:" -j KUBE-SEP-57KPRZ3JQVENLNBR
```

对于每个 Service 的每个端口，应有 1 条 `KUBE-SERVICES` 规则、一个 `KUBE-SVC-<hash>` 链。
对于每个 Pod 末端，在那个 `KUBE-SVC-<hash>` 链中应该有一些规则与之对应，还应该
有一个 `KUBE-SEP-<hash>` 链与之对应，其中包含为数不多的几条规则。
实际的规则数量可能会根据你实际的配置（包括 NodePort 和 LoadBalancer 服务）有所不同。

#### IPVS 模式   {#ipvs-mode}

在 "ipvs" 模式中, 你应该在节点下看到如下输出：

```shell
ipvsadm -ln
```

```none
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
...
TCP  10.0.1.175:80 rr
  -> 10.244.0.5:9376               Masq    1      0          0
  -> 10.244.0.6:9376               Masq    1      0          0
  -> 10.244.0.7:9376               Masq    1      0          0
...
```

对于每个 Service 的每个端口，还有 NodePort，External IP 和 LoadBalancer 类型服务
的 IP，kube-proxy 将创建一个虚拟服务器。
对于每个 Pod 末端，它将创建相应的真实服务器。
在此示例中，服务主机名（`10.0.1.175:80`）拥有 3 个末端（`10.244.0.5:9376`、
`10.244.0.6:9376` 和 `10.244.0.7:9376`）。

### kube-proxy 是否在执行代理操作?    {#is-kube-proxy-proxying}

假设你确实遇到上述情况之一，请重试从节点上通过 IP 访问你的 Service ：

```shell
curl 10.0.1.175:80
```

```none
hostnames-632524106-bbpiw
```

如果这步操作仍然失败，请查看 `kube-proxy` 日志中的特定行，如：

```none
Setting endpoints for default/hostnames:default to [10.244.0.5:9376 10.244.0.6:9376 10.244.0.7:9376]
```

如果你没有看到这些，请尝试将 `-v` 标志设置为 4 并重新启动 `kube-proxy`，然后再查看日志。

### 边缘案例: Pod 无法通过 Service IP 连接到它本身  {#a-pod-fails-to-reach-itself-via-the-service-ip}

这听起来似乎不太可能，但是确实可能发生，并且应该可以工作。

如果网络没有为“发夹模式（Hairpin）”流量生成正确配置，
通常当 `kube-proxy` 以 `iptables` 模式运行，并且 Pod 与桥接网络连接时，就会发生这种情况。
`kubelet` 提供了 `hairpin-mode`
[标志](/zh-cn/docs/reference/command-line-tools-reference/kubelet/)。
如果 Service 的末端尝试访问自己的 Service VIP，则该端点可以把流量负载均衡回来到它们自身。
`hairpin-mode` 标志必须被设置为 `hairpin-veth` 或者 `promiscuous-bridge`。

诊断此类问题的常见步骤如下：

* 确认 `hairpin-mode` 被设置为 `hairpin-veth` 或 `promiscuous-bridge`。
  你应该可以看到下面这样。本例中 `hairpin-mode` 被设置为 `promiscuous-bridge`。

  ```shell
  ps auxw | grep kubelet
  ```
  ```none
  root      3392  1.1  0.8 186804 65208 ?        Sl   00:51  11:11 /usr/local/bin/kubelet --enable-debugging-handlers=true --config=/etc/kubernetes/manifests --allow-privileged=True --v=4 --cluster-dns=10.0.0.10 --cluster-domain=cluster.local --configure-cbr0=true --cgroup-root=/ --system-cgroups=/system --hairpin-mode=promiscuous-bridge --runtime-cgroups=/docker-daemon --kubelet-cgroups=/kubelet --babysit-daemons=true --max-pods=110 --serialize-image-pulls=false --outofdisk-transition-frequency=0
  ```

* 确认有效的 `hairpin-mode`。要做到这一点，你必须查看 kubelet 日志。
  访问日志取决于节点的操作系统。在一些操作系统上，它是一个文件，如 /var/log/kubelet.log，
  而其他操作系统则使用 `journalctl` 访问日志。请注意，由于兼容性，
  有效的 `hairpin-mode` 可能不匹配 `--hairpin-mode` 标志。在 kubelet.log
  中检查是否有带有关键字 `hairpin` 的日志行。应该有日志行指示有效的
  `hairpin-mode`，就像下面这样。

  ```none
  I0629 00:51:43.648698    3252 kubelet.go:380] Hairpin mode set to "promiscuous-bridge"
  ```

* 如果有效的发夹模式是 `hairpin-veth`, 要保证 `Kubelet` 有操作节点上 `/sys` 的权限。
  如果一切正常，你将会看到如下输出:

  ```shell
  for intf in /sys/devices/virtual/net/cbr0/brif/*; do cat $intf/hairpin_mode; done
  ```
  ```none
  1
  1
  1
  1
  ```

* 如果有效的发卡模式是 `promiscuous-bridge`, 要保证 `Kubelet` 有操作节点上
  Linux 网桥的权限。如果 `cbr0` 桥正在被使用且被正确设置，你将会看到如下输出:

  ```shell
  ifconfig cbr0 |grep PROMISC
  ```
  ```none
  UP BROADCAST RUNNING PROMISC MULTICAST  MTU:1460  Metric:1
  ```

* 如果以上步骤都不能解决问题，请寻求帮助。

## 寻求帮助  {#seek-help}

如果你走到这一步，那么就真的是奇怪的事情发生了。你的 Service 正在运行，有 Endpoints 存在，
你的 Pods 也确实在提供服务。你的 DNS 正常，`iptables` 规则已经安装，`kube-proxy` 看起来也正常。
然而 Service 还是没有正常工作。这种情况下，请告诉我们，以便我们可以帮助调查！

通过 [Slack](https://slack.k8s.io/) 或者 [Forum](https://discuss.kubernetes.io) 或者
[GitHub](https://github.com/kubernetes/kubernetes) 联系我们。

## {{% heading "whatsnext" %}}

访问[故障排查概述文档](/zh-cn/docs/tasks/debug/)获取更多信息。

