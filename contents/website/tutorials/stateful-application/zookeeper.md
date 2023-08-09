---
title: 运行 ZooKeeper，一个分布式协调系统
content_type: tutorial
weight: 40
---


本教程展示了在 Kubernetes 上使用
[StatefulSet](/zh-cn/docs/concepts/workloads/controllers/statefulset/)、
[PodDisruptionBudget](/zh-cn/docs/concepts/workloads/pods/disruptions/#pod-disruption-budget) 和
[PodAntiAffinity](/zh-cn/docs/concepts/scheduling-eviction/assign-pod-node/#亲和与反亲和)
特性运行 [Apache Zookeeper](https://zookeeper.apache.org)。

## {{% heading "prerequisites" %}}

在开始本教程前，你应该熟悉以下 Kubernetes 概念。

- [Pods](/zh-cn/docs/concepts/workloads/pods/)
- [集群 DNS](/zh-cn/docs/concepts/services-networking/dns-pod-service/)
- [无头服务（Headless Service）](/zh-cn/docs/concepts/services-networking/service/#headless-services)
- [PersistentVolumes](/zh-cn/docs/concepts/storage/persistent-volumes/)
- [PersistentVolume 制备](https://github.com/kubernetes/examples/tree/master/staging/persistent-volume-provisioning/)
- [StatefulSet](/zh-cn/docs/concepts/workloads/controllers/statefulset/)
- [PodDisruptionBudget](/zh-cn/docs/concepts/workloads/pods/disruptions/#pod-disruption-budget)
- [PodAntiAffinity](/zh-cn/docs/concepts/scheduling-eviction/assign-pod-node/#亲和与反亲和)
- [kubectl CLI](/zh-cn/docs/reference/kubectl/kubectl/)

你需要一个至少包含四个节点的集群，每个节点至少 2 个 CPU 和 4 GiB 内存。
在本教程中你将会隔离（Cordon）和腾空（Drain ）集群的节点。
**这意味着集群节点上所有的 Pod 将会被终止并移除。这些节点也会暂时变为不可调度**。
在本教程中你应该使用一个独占的集群，或者保证你造成的干扰不会影响其它租户。

本教程假设你的集群已配置为动态制备 PersistentVolume。
如果你的集群没有配置成这样，在开始本教程前，你需要手动准备三个 20 GiB 的卷。

## {{% heading "objectives" %}}

在学习本教程后，你将熟悉下列内容。

* 如何使用 StatefulSet 部署一个 ZooKeeper ensemble。
* 如何一致地配置 ensemble。
* 如何在 ensemble 中分布 ZooKeeper 服务器的部署。
* 如何在计划维护中使用 PodDisruptionBudget 确保服务可用性。


### ZooKeeper   {#zookeeper-basics}

[Apache ZooKeeper](https://zookeeper.apache.org/doc/current/)
是一个分布式的开源协调服务，用于分布式系统。
ZooKeeper 允许你读取、写入数据和发现数据更新。
数据按层次结构组织在文件系统中，并复制到 ensemble（一个 ZooKeeper 服务器的集合） 
中所有的 ZooKeeper 服务器。对数据的所有操作都是原子的和顺序一致的。
ZooKeeper 通过
[Zab](https://pdfs.semanticscholar.org/b02c/6b00bd5dbdbd951fddb00b906c82fa80f0b3.pdf)
一致性协议在 ensemble 的所有服务器之间复制一个状态机来确保这个特性。

Ensemble 使用 Zab 协议选举一个领导者，在选举出领导者前不能写入数据。
一旦选举出了领导者，ensemble 使用 Zab 保证所有写入被复制到一个 quorum，
然后这些写入操作才会被确认并对客户端可用。
如果没有遵照加权 quorums，一个 quorum 表示包含当前领导者的 ensemble 的多数成员。
例如，如果 ensemble 有 3 个服务器，一个包含领导者的成员和另一个服务器就组成了一个
quorum。
如果 ensemble 不能达成一个 quorum，数据将不能被写入。

ZooKeeper 在内存中保存它们的整个状态机，但是每个改变都被写入一个在存储介质上的持久
WAL（Write Ahead Log）。
当一个服务器出现故障时，它能够通过回放 WAL 恢复之前的状态。
为了防止 WAL 无限制的增长，ZooKeeper 服务器会定期的将内存状态快照保存到存储介质。
这些快照能够直接加载到内存中，所有在这个快照之前的 WAL 条目都可以被安全的丢弃。

## 创建一个 ZooKeeper Ensemble

下面的清单包含一个[无头服务](/zh-cn/docs/concepts/services-networking/service/#headless-services)、
一个 [Service](/zh-cn/docs/concepts/services-networking/service/)、
一个 [PodDisruptionBudget](/zh-cn/docs/concepts/workloads/pods/disruptions/#specifying-a-poddisruptionbudget)
和一个 [StatefulSet](/zh-cn/docs/concepts/workloads/controllers/statefulset/)。

{{< codenew file="application/zookeeper/zookeeper.yaml" >}}

打开一个命令行终端，使用命令
[`kubectl apply`](/docs/reference/generated/kubectl/kubectl-commands/#apply)
创建这个清单。

```shell
kubectl apply -f https://k8s.io/examples/application/zookeeper/zookeeper.yaml
```

这个操作创建了 `zk-hs` 无头服务、`zk-cs` 服务、`zk-pdb` PodDisruptionBudget
和 `zk` StatefulSet。

```
service/zk-hs created
service/zk-cs created
poddisruptionbudget.policy/zk-pdb created
statefulset.apps/zk created
```

使用命令
[`kubectl get`](/docs/reference/generated/kubectl/kubectl-commands/#get)
查看 StatefulSet 控制器创建的几个 Pod。

```shell
kubectl get pods -w -l app=zk
```

一旦 `zk-2` Pod 变成 Running 和 Ready 状态，请使用 `CRTL-C` 结束 kubectl。

```
NAME      READY     STATUS    RESTARTS   AGE
zk-0      0/1       Pending   0          0s
zk-0      0/1       Pending   0         0s
zk-0      0/1       ContainerCreating   0         0s
zk-0      0/1       Running   0         19s
zk-0      1/1       Running   0         40s
zk-1      0/1       Pending   0         0s
zk-1      0/1       Pending   0         0s
zk-1      0/1       ContainerCreating   0         0s
zk-1      0/1       Running   0         18s
zk-1      1/1       Running   0         40s
zk-2      0/1       Pending   0         0s
zk-2      0/1       Pending   0         0s
zk-2      0/1       ContainerCreating   0         0s
zk-2      0/1       Running   0         19s
zk-2      1/1       Running   0         40s
```

StatefulSet 控制器创建 3 个 Pod，每个 Pod 包含一个
[ZooKeeper](https://archive.apache.org/dist/zookeeper/stable/) 服务容器。

### 促成 Leader 选举  {#facilitating-leader-election}

由于在匿名网络中没有用于选举 leader 的终止算法，Zab 要求显式的进行成员关系配置，
以执行 leader 选举。Ensemble 中的每个服务器都需要具有一个独一无二的标识符，
所有的服务器均需要知道标识符的全集，并且每个标识符都需要和一个网络地址相关联。

使用命令
[`kubectl exec`](/docs/reference/generated/kubectl/kubectl-commands/#exec)
获取 `zk` StatefulSet 中 Pod 的主机名。

```shell
for i in 0 1 2; do kubectl exec zk-$i -- hostname; done
```

StatefulSet 控制器基于每个 Pod 的序号索引为它们各自提供一个唯一的主机名。
主机名采用 `<statefulset 名称>-<序数索引>` 的形式。
由于 `zk` StatefulSet 的 `replicas` 字段设置为 3，这个集合的控制器将创建
3 个 Pod，主机名为：`zk-0`、`zk-1` 和 `zk-2`。

```
zk-0
zk-1
zk-2
```

ZooKeeper ensemble 中的服务器使用自然数作为唯一标识符，
每个服务器的标识符都保存在服务器的数据目录中一个名为 `myid` 的文件里。

检查每个服务器的 `myid` 文件的内容。

```shell
for i in 0 1 2; do echo "myid zk-$i";kubectl exec zk-$i -- cat /var/lib/zookeeper/data/myid; done
```

由于标识符为自然数并且序号索引是非负整数，你可以在序号上加 1 来生成一个标识符。

```
myid zk-0
1
myid zk-1
2
myid zk-2
3
```

获取 `zk` StatefulSet 中每个 Pod 的全限定域名（Fully Qualified Domain Name，FQDN）。

```shell
for i in 0 1 2; do kubectl exec zk-$i -- hostname -f; done
```

`zk-hs` Service 为所有 Pod 创建了一个域：`zk-hs.default.svc.cluster.local`。

```
zk-0.zk-hs.default.svc.cluster.local
zk-1.zk-hs.default.svc.cluster.local
zk-2.zk-hs.default.svc.cluster.local
```

[Kubernetes DNS](/zh-cn/docs/concepts/services-networking/dns-pod-service/)
中的 A 记录将 FQDN 解析成为 Pod 的 IP 地址。
如果 Kubernetes 重新调度这些 Pod，这个 A 记录将会使用这些 Pod 的新 IP 地址完成更新，
但 A 记录的名称不会改变。

ZooKeeper 在一个名为 `zoo.cfg` 的文件中保存它的应用配置。
使用 `kubectl exec` 在  `zk-0` Pod 中查看 `zoo.cfg` 文件的内容。

```shell
kubectl exec zk-0 -- cat /opt/zookeeper/conf/zoo.cfg
```

文件底部为 `server.1`、`server.2` 和 `server.3`，其中的 `1`、`2` 和 `3`
分别对应 ZooKeeper 服务器的 `myid` 文件中的标识符。
它们被设置为 `zk` StatefulSet 中的 Pods 的 FQDNs。

```
clientPort=2181
dataDir=/var/lib/zookeeper/data
dataLogDir=/var/lib/zookeeper/log
tickTime=2000
initLimit=10
syncLimit=2000
maxClientCnxns=60
minSessionTimeout= 4000
maxSessionTimeout= 40000
autopurge.snapRetainCount=3
autopurge.purgeInterval=0
server.1=zk-0.zk-hs.default.svc.cluster.local:2888:3888
server.2=zk-1.zk-hs.default.svc.cluster.local:2888:3888
server.3=zk-2.zk-hs.default.svc.cluster.local:2888:3888
```

### 达成共识   {#achieving-consensus}

一致性协议要求每个参与者的标识符唯一。
在 Zab 协议里任何两个参与者都不应该声明相同的唯一标识符。
对于让系统中的进程协商哪些进程已经提交了哪些数据而言，这是必须的。
如果有两个 Pod 使用相同的序号启动，这两个 ZooKeeper
服务器会将自己识别为相同的服务器。

```shell
kubectl get pods -w -l app=zk
```

```
NAME      READY     STATUS    RESTARTS   AGE
zk-0      0/1       Pending   0          0s
zk-0      0/1       Pending   0         0s
zk-0      0/1       ContainerCreating   0         0s
zk-0      0/1       Running   0         19s
zk-0      1/1       Running   0         40s
zk-1      0/1       Pending   0         0s
zk-1      0/1       Pending   0         0s
zk-1      0/1       ContainerCreating   0         0s
zk-1      0/1       Running   0         18s
zk-1      1/1       Running   0         40s
zk-2      0/1       Pending   0         0s
zk-2      0/1       Pending   0         0s
zk-2      0/1       ContainerCreating   0         0s
zk-2      0/1       Running   0         19s
zk-2      1/1       Running   0         40s
```

每个 Pod 的 A 记录仅在 Pod 变成 Ready 状态时被录入。
因此，ZooKeeper 服务器的 FQDN 只会解析到一个端点，
而那个端点将是申领其 `myid` 文件中所配置标识的唯一 ZooKeeper 服务器。

```
zk-0.zk-hs.default.svc.cluster.local
zk-1.zk-hs.default.svc.cluster.local
zk-2.zk-hs.default.svc.cluster.local
```


这保证了 ZooKeeper 的 `zoo.cfg` 文件中的 `servers` 属性代表了一个正确配置的 ensemble。

```
server.1=zk-0.zk-hs.default.svc.cluster.local:2888:3888
server.2=zk-1.zk-hs.default.svc.cluster.local:2888:3888
server.3=zk-2.zk-hs.default.svc.cluster.local:2888:3888
```

当服务器使用 Zab 协议尝试提交一个值的时候，它们会达成一致并成功提交这个值
（如果领导者选举成功并且至少有两个 Pod 处于 Running 和 Ready 状态），
或者将会失败（如果没有满足上述条件中的任意一条）。
当一个服务器承认另一个服务器的代写时不会有状态产生。

### Ensemble 健康检查

最基本的健康检查是向一个 ZooKeeper 服务器写入一些数据，然后从另一个服务器读取这些数据。

使用 `zkCli.sh` 脚本在 `zk-0` Pod 上写入 `world` 到路径 `/hello`。

```shell
kubectl exec zk-0 zkCli.sh create /hello world
```
```
WATCHER::

WatchedEvent state:SyncConnected type:None path:null
Created /hello
```

使用下面的命令从 `zk-1` Pod 获取数据。

```shell
kubectl exec zk-1 zkCli.sh get /hello
```

你在 `zk-0` 上创建的数据在 ensemble 中所有的服务器上都是可用的。

```
WATCHER::

WatchedEvent state:SyncConnected type:None path:null
world
cZxid = 0x100000002
ctime = Thu Dec 08 15:13:30 UTC 2016
mZxid = 0x100000002
mtime = Thu Dec 08 15:13:30 UTC 2016
pZxid = 0x100000002
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 5
numChildren = 0
```

### 提供持久存储

如同在 [ZooKeeper](#zookeeper-basics) 一节所提到的，
ZooKeeper 提交所有的条目到一个持久 WAL，并周期性的将内存快照写入存储介质。
对于使用一致性协议实现一个复制状态机的应用来说，
使用 WAL 提供持久化是一种常用的技术，对于普通的存储应用也是如此。

使用 [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands/#delete)
删除 `zk` StatefulSet。

```shell
kubectl delete statefulset zk
```

```
statefulset.apps "zk" deleted
```

观察 StatefulSet 中的 Pod 变为终止状态。

```shell
kubectl get pods -w -l app=zk
```

当 `zk-0` 完全终止时，使用 `CRTL-C` 结束 kubectl。

```
zk-2      1/1       Terminating   0         9m
zk-0      1/1       Terminating   0         11m
zk-1      1/1       Terminating   0         10m
zk-2      0/1       Terminating   0         9m
zk-2      0/1       Terminating   0         9m
zk-2      0/1       Terminating   0         9m
zk-1      0/1       Terminating   0         10m
zk-1      0/1       Terminating   0         10m
zk-1      0/1       Terminating   0         10m
zk-0      0/1       Terminating   0         11m
zk-0      0/1       Terminating   0         11m
zk-0      0/1       Terminating   0         11m
```

重新应用 `zookeeper.yaml` 中的清单。

```shell
kubectl apply -f https://k8s.io/examples/application/zookeeper/zookeeper.yaml
```

`zk` StatefulSet 将会被创建。由于清单中的其他 API 对象已经存在，所以它们不会被修改。

观察 StatefulSet 控制器重建 StatefulSet 的 Pod。

```shell
kubectl get pods -w -l app=zk
```

一旦 `zk-2` Pod 处于 Running 和 Ready 状态，使用 `CRTL-C` 停止 kubectl 命令。

```
NAME      READY     STATUS    RESTARTS   AGE
zk-0      0/1       Pending   0          0s
zk-0      0/1       Pending   0         0s
zk-0      0/1       ContainerCreating   0         0s
zk-0      0/1       Running   0         19s
zk-0      1/1       Running   0         40s
zk-1      0/1       Pending   0         0s
zk-1      0/1       Pending   0         0s
zk-1      0/1       ContainerCreating   0         0s
zk-1      0/1       Running   0         18s
zk-1      1/1       Running   0         40s
zk-2      0/1       Pending   0         0s
zk-2      0/1       Pending   0         0s
zk-2      0/1       ContainerCreating   0         0s
zk-2      0/1       Running   0         19s
zk-2      1/1       Running   0         40s
```

从 `zk-2` Pod 中获取你在[健康检查](#Ensemble-健康检查)中输入的值。

```shell
kubectl exec zk-2 zkCli.sh get /hello
```

尽管 `zk` StatefulSet 中所有的 Pod 都已经被终止并重建过，
ensemble 仍然使用原来的数值提供服务。

```
WATCHER::

WatchedEvent state:SyncConnected type:None path:null
world
cZxid = 0x100000002
ctime = Thu Dec 08 15:13:30 UTC 2016
mZxid = 0x100000002
mtime = Thu Dec 08 15:13:30 UTC 2016
pZxid = 0x100000002
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 5
numChildren = 0
```

`zk` StatefulSet 的 `spec` 中的 `volumeClaimTemplates`
字段标识了将要为每个 Pod 准备的 PersistentVolume。

```yaml
volumeClaimTemplates:
  - metadata:
      name: datadir
      annotations:
        volume.alpha.kubernetes.io/storage-class: anything
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 20Gi
```

`StatefulSet` 控制器为 `StatefulSet` 中的每个 Pod 生成一个 `PersistentVolumeClaim`。

获取 `StatefulSet` 的 `PersistentVolumeClaim`。

```shell
kubectl get pvc -l app=zk
```

当 `StatefulSet` 重新创建它的 Pod 时，Pod 的 PersistentVolume 会被重新挂载。

```
NAME           STATUS    VOLUME                                     CAPACITY   ACCESSMODES   AGE
datadir-zk-0   Bound     pvc-bed742cd-bcb1-11e6-994f-42010a800002   20Gi       RWO           1h
datadir-zk-1   Bound     pvc-bedd27d2-bcb1-11e6-994f-42010a800002   20Gi       RWO           1h
datadir-zk-2   Bound     pvc-bee0817e-bcb1-11e6-994f-42010a800002   20Gi       RWO           1h
```

StatefulSet 的容器 `template` 中的 `volumeMounts` 一节使得
PersistentVolume 被挂载到 ZooKeeper 服务器的数据目录。

```yaml
volumeMounts:
- name: datadir
  mountPath: /var/lib/zookeeper
```

当 `zk` `StatefulSet` 中的一个 Pod 被（重新）调度时，它总是拥有相同的 PersistentVolume，
挂载到 ZooKeeper 服务器的数据目录。
即使在 Pod 被重新调度时，所有对 ZooKeeper 服务器的 WAL 的写入和它们的全部快照都仍然是持久的。

## 确保一致性配置

如同在[促成领导者选举](#facilitating-leader-election)和[达成一致](#achieving-consensus)
小节中提到的，ZooKeeper ensemble 中的服务器需要一致性的配置来选举一个领导者并形成一个
quorum。它们还需要 Zab 协议的一致性配置来保证这个协议在网络中正确的工作。
在这次的示例中，我们通过直接将配置写入代码清单中来达到该目的。

获取 `zk` StatefulSet。

```shell
kubectl get sts zk -o yaml
```
```
    ...
    command:
      - sh
      - -c
      - "start-zookeeper \
        --servers=3 \
        --data_dir=/var/lib/zookeeper/data \
        --data_log_dir=/var/lib/zookeeper/data/log \
        --conf_dir=/opt/zookeeper/conf \
        --client_port=2181 \
        --election_port=3888 \
        --server_port=2888 \
        --tick_time=2000 \
        --init_limit=10 \
        --sync_limit=5 \
        --heap=512M \
        --max_client_cnxns=60 \
        --snap_retain_count=3 \
        --purge_interval=12 \
        --max_session_timeout=40000 \
        --min_session_timeout=4000 \
        --log_level=INFO"
...
```

用于启动 ZooKeeper 服务器的命令将这些配置作为命令行参数传给了 ensemble。
你也可以通过环境变量来传入这些配置。

### 配置日志   {#configuring-logging}

`zkGenConfig.sh` 脚本产生的一个文件控制了 ZooKeeper 的日志行为。
ZooKeeper 使用了 [Log4j](http://logging.apache.org/log4j/2.x/)
并默认使用基于文件大小和时间的滚动文件追加器作为日志配置。

从 `zk` StatefulSet 的一个 Pod 中获取日志配置。

```shell
kubectl exec zk-0 cat /usr/etc/zookeeper/log4j.properties
```

下面的日志配置会使 ZooKeeper 进程将其所有的日志写入标志输出文件流中。

```
zookeeper.root.logger=CONSOLE
zookeeper.console.threshold=INFO
log4j.rootLogger=${zookeeper.root.logger}
log4j.appender.CONSOLE=org.apache.log4j.ConsoleAppender
log4j.appender.CONSOLE.Threshold=${zookeeper.console.threshold}
log4j.appender.CONSOLE.layout=org.apache.log4j.PatternLayout
log4j.appender.CONSOLE.layout.ConversionPattern=%d{ISO8601} [myid:%X{myid}] - %-5p [%t:%C{1}@%L] - %m%n
```

这是在容器里安全记录日志的最简单的方法。
由于应用的日志被写入标准输出，Kubernetes 将会为你处理日志轮转。
Kubernetes 还实现了一个智能保存策略，
保证写入标准输出和标准错误流的应用日志不会耗尽本地存储介质。

使用命令 [`kubectl logs`](/docs/reference/generated/kubectl/kubectl-commands/#logs)
从一个 Pod 中取回最后 20 行日志。

```shell
kubectl logs zk-0 --tail 20
```

使用 `kubectl logs` 或者从 Kubernetes Dashboard 可以查看写入到标准输出和标准错误流中的应用日志。

```
2016-12-06 19:34:16,236 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxn@827] - Processing ruok command from /127.0.0.1:52740
2016-12-06 19:34:16,237 [myid:1] - INFO  [Thread-1136:NIOServerCnxn@1008] - Closed socket connection for client /127.0.0.1:52740 (no session established for client)
2016-12-06 19:34:26,155 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxnFactory@192] - Accepted socket connection from /127.0.0.1:52749
2016-12-06 19:34:26,155 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxn@827] - Processing ruok command from /127.0.0.1:52749
2016-12-06 19:34:26,156 [myid:1] - INFO  [Thread-1137:NIOServerCnxn@1008] - Closed socket connection for client /127.0.0.1:52749 (no session established for client)
2016-12-06 19:34:26,222 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxnFactory@192] - Accepted socket connection from /127.0.0.1:52750
2016-12-06 19:34:26,222 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxn@827] - Processing ruok command from /127.0.0.1:52750
2016-12-06 19:34:26,226 [myid:1] - INFO  [Thread-1138:NIOServerCnxn@1008] - Closed socket connection for client /127.0.0.1:52750 (no session established for client)
2016-12-06 19:34:36,151 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxnFactory@192] - Accepted socket connection from /127.0.0.1:52760
2016-12-06 19:34:36,152 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxn@827] - Processing ruok command from /127.0.0.1:52760
2016-12-06 19:34:36,152 [myid:1] - INFO  [Thread-1139:NIOServerCnxn@1008] - Closed socket connection for client /127.0.0.1:52760 (no session established for client)
2016-12-06 19:34:36,230 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxnFactory@192] - Accepted socket connection from /127.0.0.1:52761
2016-12-06 19:34:36,231 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxn@827] - Processing ruok command from /127.0.0.1:52761
2016-12-06 19:34:36,231 [myid:1] - INFO  [Thread-1140:NIOServerCnxn@1008] - Closed socket connection for client /127.0.0.1:52761 (no session established for client)
2016-12-06 19:34:46,149 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxnFactory@192] - Accepted socket connection from /127.0.0.1:52767
2016-12-06 19:34:46,149 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxn@827] - Processing ruok command from /127.0.0.1:52767
2016-12-06 19:34:46,149 [myid:1] - INFO  [Thread-1141:NIOServerCnxn@1008] - Closed socket connection for client /127.0.0.1:52767 (no session established for client)
2016-12-06 19:34:46,230 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxnFactory@192] - Accepted socket connection from /127.0.0.1:52768
2016-12-06 19:34:46,230 [myid:1] - INFO  [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxn@827] - Processing ruok command from /127.0.0.1:52768
2016-12-06 19:34:46,230 [myid:1] - INFO  [Thread-1142:NIOServerCnxn@1008] - Closed socket connection for client /127.0.0.1:52768 (no session established for client)
```

Kubernetes 支持与多种日志方案集成。
你可以选择一个最适合你的集群和应用的日志解决方案。
对于集群级别的日志输出与整合，可以考虑部署一个
[边车容器](/zh-cn/docs/concepts/cluster-administration/logging#sidecar-container-with-logging-agent)
来轮转和提供日志数据。

### 配置非特权用户

在容器中允许应用以特权用户运行这条最佳实践是值得商讨的。
如果你的组织要求应用以非特权用户运行，你可以使用
[SecurityContext](/zh-cn/docs/tasks/configure-pod-container/security-context/)
控制运行容器入口点所使用的用户。

`zk` StatefulSet 的 Pod 的 `template` 包含了一个 `SecurityContext`。

```yaml
securityContext:
  runAsUser: 1000
  fsGroup: 1000
```

在 Pod 的容器内部，UID 1000 对应用户 zookeeper，GID 1000 对应用户组 zookeeper。

从 `zk-0` Pod 获取 ZooKeeper 进程信息。

```shell
kubectl exec zk-0 -- ps -elf
```

由于 `securityContext` 对象的 `runAsUser` 字段被设置为 1000 而不是 root，
ZooKeeper 进程将以 zookeeper 用户运行。

```
F S UID        PID  PPID  C PRI  NI ADDR SZ WCHAN  STIME TTY          TIME CMD
4 S zookeep+     1     0  0  80   0 -  1127 -      20:46 ?        00:00:00 sh -c zkGenConfig.sh && zkServer.sh start-foreground
0 S zookeep+    27     1  0  80   0 - 1155556 -    20:46 ?        00:00:19 /usr/lib/jvm/java-8-openjdk-amd64/bin/java -Dzookeeper.log.dir=/var/log/zookeeper -Dzookeeper.root.logger=INFO,CONSOLE -cp /usr/bin/../build/classes:/usr/bin/../build/lib/*.jar:/usr/bin/../share/zookeeper/zookeeper-3.4.9.jar:/usr/bin/../share/zookeeper/slf4j-log4j12-1.6.1.jar:/usr/bin/../share/zookeeper/slf4j-api-1.6.1.jar:/usr/bin/../share/zookeeper/netty-3.10.5.Final.jar:/usr/bin/../share/zookeeper/log4j-1.2.16.jar:/usr/bin/../share/zookeeper/jline-0.9.94.jar:/usr/bin/../src/java/lib/*.jar:/usr/bin/../etc/zookeeper: -Xmx2G -Xms2G -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.local.only=false org.apache.zookeeper.server.quorum.QuorumPeerMain /usr/bin/../etc/zookeeper/zoo.cfg
```

默认情况下，当 Pod 的 PersistentVolume 被挂载到 ZooKeeper 服务器的数据目录时，
它只能被 root 用户访问。这个配置将阻止 ZooKeeper 进程写入它的 WAL 及保存快照。

在 `zk-0` Pod 上获取 ZooKeeper 数据目录的文件权限。

```shell
kubectl exec -ti zk-0 -- ls -ld /var/lib/zookeeper/data
```

由于 `securityContext` 对象的 `fsGroup` 字段设置为 1000，
Pod 的 PersistentVolume 的所有权属于 zookeeper 用户组，
因而 ZooKeeper 进程能够成功地读写数据。

```
drwxr-sr-x 3 zookeeper zookeeper 4096 Dec  5 20:45 /var/lib/zookeeper/data
```

## 管理 ZooKeeper 进程

[ZooKeeper 文档](https://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_supervision)
指出 “你将需要一个监管程序用于管理每个 ZooKeeper 服务进程（JVM）”。
在分布式系统中，使用一个看门狗（监管程序）来重启故障进程是一种常用的模式。

### 更新 Ensemble

`zk` `StatefulSet` 的更新策略被设置为了 `RollingUpdate`。

你可以使用 `kubectl patch` 更新分配给每个服务器的 `cpus` 的数量。

```shell
kubectl patch sts zk --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/resources/requests/cpu", "value":"0.3"}]'
```

```
statefulset.apps/zk patched
```

使用 `kubectl rollout status` 观测更新状态。

```shell
kubectl rollout status sts/zk
```

```
waiting for statefulset rolling update to complete 0 pods at revision zk-5db4499664...
Waiting for 1 pods to be ready...
Waiting for 1 pods to be ready...
waiting for statefulset rolling update to complete 1 pods at revision zk-5db4499664...
Waiting for 1 pods to be ready...
Waiting for 1 pods to be ready...
waiting for statefulset rolling update to complete 2 pods at revision zk-5db4499664...
Waiting for 1 pods to be ready...
Waiting for 1 pods to be ready...
statefulset rolling update complete 3 pods at revision zk-5db4499664...
```

这项操作会逆序地依次终止每一个 Pod，并用新的配置重新创建。
这样做确保了在滚动更新的过程中 quorum 依旧保持工作。

使用 `kubectl rollout history` 命令查看历史或先前的配置。

```shell
kubectl rollout history sts/zk
```

输出类似于：

```
statefulsets "zk"
REVISION
1
2
```

使用 `kubectl rollout undo` 命令撤销这次的改动。

```shell
kubectl rollout undo sts/zk
```

输出类似于：

```
statefulset.apps/zk rolled back
```

### 处理进程故障

[重启策略](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy)
控制 Kubernetes 如何处理一个 Pod 中容器入口点的进程故障。
对于 StatefulSet 中的 Pod 来说，Always 是唯一合适的 RestartPolicy，也是默认值。
你应该**绝不**覆盖有状态应用的默认策略。

检查 `zk-0` Pod 中运行的 ZooKeeper 服务器的进程树。

```shell
kubectl exec zk-0 -- ps -ef
```

作为容器入口点的命令的 PID 为 1，Zookeeper 进程是入口点的子进程，PID 为 27。

```
UID        PID  PPID  C STIME TTY          TIME CMD
zookeep+     1     0  0 15:03 ?        00:00:00 sh -c zkGenConfig.sh && zkServer.sh start-foreground
zookeep+    27     1  0 15:03 ?        00:00:03 /usr/lib/jvm/java-8-openjdk-amd64/bin/java -Dzookeeper.log.dir=/var/log/zookeeper -Dzookeeper.root.logger=INFO,CONSOLE -cp /usr/bin/../build/classes:/usr/bin/../build/lib/*.jar:/usr/bin/../share/zookeeper/zookeeper-3.4.9.jar:/usr/bin/../share/zookeeper/slf4j-log4j12-1.6.1.jar:/usr/bin/../share/zookeeper/slf4j-api-1.6.1.jar:/usr/bin/../share/zookeeper/netty-3.10.5.Final.jar:/usr/bin/../share/zookeeper/log4j-1.2.16.jar:/usr/bin/../share/zookeeper/jline-0.9.94.jar:/usr/bin/../src/java/lib/*.jar:/usr/bin/../etc/zookeeper: -Xmx2G -Xms2G -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.local.only=false org.apache.zookeeper.server.quorum.QuorumPeerMain /usr/bin/../etc/zookeeper/zoo.cfg
```

在一个终端观察 `zk` `StatefulSet` 中的 Pod。

```shell
kubectl get pod -w -l app=zk
```

在另一个终端杀掉 Pod `zk-0` 中的 ZooKeeper 进程。

```shell
 kubectl exec zk-0 -- pkill java
```

ZooKeeper 进程的终结导致了它父进程的终止。由于容器的 `RestartPolicy`
是 Always，所以父进程被重启。

```
NAME      READY     STATUS    RESTARTS   AGE
zk-0      1/1       Running   0          21m
zk-1      1/1       Running   0          20m
zk-2      1/1       Running   0          19m
NAME      READY     STATUS    RESTARTS   AGE
zk-0      0/1       Error     0          29m
zk-0      0/1       Running   1         29m
zk-0      1/1       Running   1         29m
```

如果你的应用使用一个脚本（例如 `zkServer.sh`）来启动一个实现了应用业务逻辑的进程，
这个脚本必须和子进程一起结束。这保证了当实现应用业务逻辑的进程故障时，
Kubernetes 会重启这个应用的容器。

### 存活性测试

你的应用配置为自动重启故障进程，但这对于保持一个分布式系统的健康来说是不够的。
许多场景下，一个系统进程可以是活动状态但不响应请求，或者是不健康状态。
你应该使用存活性探针来通知 Kubernetes 你的应用进程处于不健康状态，需要被重启。

`zk` `StatefulSet` 的 Pod 的 `template` 一节指定了一个存活探针。

```yaml
  livenessProbe:
    exec:
      command:
      - sh
      - -c
      - "zookeeper-ready 2181"
    initialDelaySeconds: 15
    timeoutSeconds: 5
```

这个探针调用一个简单的 Bash 脚本，使用 ZooKeeper 的四字缩写 `ruok`
来测试服务器的健康状态。

```
OK=$(echo ruok | nc 127.0.0.1 $1)
if [ "$OK" == "imok" ]; then
    exit 0
else
    exit 1
fi
```

在一个终端窗口中使用下面的命令观察 `zk` StatefulSet 中的 Pod。

```shell
kubectl get pod -w -l app=zk
```

在另一个窗口中，从 Pod `zk-0` 的文件系统中删除 `zookeeper-ready` 脚本。

```shell
kubectl exec zk-0 -- rm /opt/zookeeper/bin/zookeeper-ready
```

当 ZooKeeper 进程的存活探针探测失败时，Kubernetes 将会为你自动重启这个进程，
从而保证 ensemble 中不健康状态的进程都被重启。

```shell
kubectl get pod -w -l app=zk
```

```
NAME      READY     STATUS    RESTARTS   AGE
zk-0      1/1       Running   0          1h
zk-1      1/1       Running   0          1h
zk-2      1/1       Running   0          1h
NAME      READY     STATUS    RESTARTS   AGE
zk-0      0/1       Running   0          1h
zk-0      0/1       Running   1         1h
zk-0      1/1       Running   1         1h
```

### 就绪性测试

就绪不同于存活。如果一个进程是存活的，它是可调度和健康的。
如果一个进程是就绪的，它应该能够处理输入。存活是就绪的必要非充分条件。
在许多场景下，特别是初始化和终止过程中，一个进程可以是存活但没有就绪的。

如果你指定了一个就绪探针，Kubernetes 将保证在就绪检查通过之前，
你的应用不会接收到网络流量。

对于一个 ZooKeeper 服务器来说，存活即就绪。
因此 `zookeeper.yaml` 清单中的就绪探针和存活探针完全相同。

```yaml
  readinessProbe:
    exec:
      command:
      - sh
      - -c
      - "zookeeper-ready 2181"
    initialDelaySeconds: 15
    timeoutSeconds: 5
```

虽然存活探针和就绪探针是相同的，但同时指定它们两者仍然重要。
这保证了 ZooKeeper ensemble 中只有健康的服务器能接收网络流量。

## 容忍节点故障

ZooKeeper 需要一个 quorum 来提交数据变动。对于一个拥有 3 个服务器的 ensemble 来说，
必须有两个服务器是健康的，写入才能成功。
在基于 quorum 的系统里，成员被部署在多个故障域中以保证可用性。
为了防止由于某台机器断连引起服务中断，最佳实践是防止应用的多个实例在相同的机器上共存。

默认情况下，Kubernetes 可以把 `StatefulSet` 的 Pod 部署在相同节点上。
对于你创建的 3 个服务器的 ensemble 来说，
如果有两个服务器并存于相同的节点上并且该节点发生故障时，ZooKeeper 服务将中断，
直至至少其中一个 Pod 被重新调度。

你应该总是提供多余的容量以允许关键系统进程在节点故障时能够被重新调度。
如果你这样做了，服务故障就只会持续到 Kubernetes 调度器重新调度某个
ZooKeeper 服务器为止。
但是，如果希望你的服务在容忍节点故障时无停服时间，你应该设置 `podAntiAffinity`。

使用下面的命令获取 `zk` `StatefulSet` 中的 Pod 的节点。

```shell
for i in 0 1 2; do kubectl get pod zk-$i --template {{.spec.nodeName}}; echo ""; done
```

`zk` `StatefulSet` 中所有的 Pod 都被部署在不同的节点。

```
kubernetes-node-cxpk
kubernetes-node-a5aq
kubernetes-node-2g2d
```


这是因为 `zk` `StatefulSet` 中的 Pod 指定了 `PodAntiAffinity`。

```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
            - key: "app"
              operator: In
              values:
                - zk
        topologyKey: "kubernetes.io/hostname"
```

`requiredDuringSchedulingIgnoredDuringExecution` 告诉 Kubernetes 调度器，
在以 `topologyKey` 指定的域中，绝对不要把带有键为 `app`、值为 `zk` 的标签
的两个 Pod 调度到相同的节点。`topologyKey` `kubernetes.io/hostname` 表示
这个域是一个单独的节点。
使用不同的规则、标签和选择算符，你能够通过这种技术把你的 ensemble 分布
在不同的物理、网络和电力故障域之间。

## 节点维护期间保持应用可用

**在本节中你将会隔离（Cordon）和腾空（Drain）节点。
如果你是在一个共享的集群里使用本教程，请保证不会影响到其他租户。**

上一小节展示了如何在节点之间分散 Pod 以在计划外的节点故障时保证服务存活。
但是你也需要为计划内维护引起的临时节点故障做准备。

使用此命令获取你的集群中的节点。

```shell
kubectl get nodes
```


使用 [`kubectl cordon`](/docs/reference/generated/kubectl/kubectl-commands/#cordon)
隔离你的集群中除 4 个节点以外的所有节点。

```shell
kubectl cordon <node-name>
```

使用下面的命令获取 `zk-pdb` `PodDisruptionBudget`。

```shell
kubectl get pdb zk-pdb
```

`max-unavailable` 字段指示 Kubernetes 在任何时候，`zk` `StatefulSet`
至多有一个 Pod 是不可用的。

```
NAME      MIN-AVAILABLE   MAX-UNAVAILABLE   ALLOWED-DISRUPTIONS   AGE
zk-pdb    N/A             1                 1
```

在一个终端中，使用下面的命令观察 `zk` `StatefulSet` 中的 Pod。

```shell
kubectl get pods -w -l app=zk
```


在另一个终端中，使用下面的命令获取 Pod 当前调度的节点。

```shell
for i in 0 1 2; do kubectl get pod zk-$i --template {{.spec.nodeName}}; echo ""; done
```

```
kubernetes-node-pb41
kubernetes-node-ixsl
kubernetes-node-i4c4
```


使用 [`kubectl drain`](/docs/reference/generated/kubectl/kubectl-commands/#drain)
来隔离和腾空 `zk-0` Pod 调度所在的节点。

```shell
kubectl drain $(kubectl get pod zk-0 --template {{.spec.nodeName}}) --ignore-daemonsets --force --delete-emptydir-data
```

输出类似于：

```
node "kubernetes-node-pb41" cordoned

WARNING: Deleting pods not managed by ReplicationController, ReplicaSet, Job, or DaemonSet: fluentd-cloud-logging-kubernetes-node-pb41, kube-proxy-kubernetes-node-pb41; Ignoring DaemonSet-managed pods: node-problem-detector-v0.1-o5elz
pod "zk-0" deleted
node "kubernetes-node-pb41" drained
```

由于你的集群中有 4 个节点, `kubectl drain` 执行成功，`zk-0` 被调度到其它节点。

```
NAME      READY     STATUS    RESTARTS   AGE
zk-0      1/1       Running   2          1h
zk-1      1/1       Running   0          1h
zk-2      1/1       Running   0          1h
NAME      READY     STATUS        RESTARTS   AGE
zk-0      1/1       Terminating   2          2h
zk-0      0/1       Terminating   2         2h
zk-0      0/1       Terminating   2         2h
zk-0      0/1       Terminating   2         2h
zk-0      0/1       Pending   0         0s
zk-0      0/1       Pending   0         0s
zk-0      0/1       ContainerCreating   0         0s
zk-0      0/1       Running   0         51s
zk-0      1/1       Running   0         1m
```

在第一个终端中持续观察 `StatefulSet` 的 Pod 并腾空 `zk-1` 调度所在的节点。

```shell
kubectl drain $(kubectl get pod zk-1 --template {{.spec.nodeName}}) --ignore-daemonsets --force --delete-emptydir-data
```

输出类似于：

```
kubernetes-node-ixsl" cordoned
WARNING: Deleting pods not managed by ReplicationController, ReplicaSet, Job, or DaemonSet: fluentd-cloud-logging-kubernetes-node-ixsl, kube-proxy-kubernetes-node-ixsl; Ignoring DaemonSet-managed pods: node-problem-detector-v0.1-voc74
pod "zk-1" deleted
node "kubernetes-node-ixsl" drained
```

`zk-1` Pod 不能被调度，这是因为 `zk` `StatefulSet` 包含了一个防止 Pod
共存的 `PodAntiAffinity` 规则，而且只有两个节点可用于调度，
这个 Pod 将保持在 Pending 状态。

```shell
kubectl get pods -w -l app=zk
```

输出类似于：

```
NAME      READY     STATUS              RESTARTS   AGE
zk-0      1/1       Running             2          1h
zk-1      1/1       Running             0          1h
zk-2      1/1       Running             0          1h
NAME      READY     STATUS              RESTARTS   AGE
zk-0      1/1       Terminating         2          2h
zk-0      0/1       Terminating         2          2h
zk-0      0/1       Terminating         2          2h
zk-0      0/1       Terminating         2          2h
zk-0      0/1       Pending             0          0s
zk-0      0/1       Pending             0          0s
zk-0      0/1       ContainerCreating   0          0s
zk-0      0/1       Running             0          51s
zk-0      1/1       Running             0          1m
zk-1      1/1       Terminating         0          2h
zk-1      0/1       Terminating         0          2h
zk-1      0/1       Terminating         0          2h
zk-1      0/1       Terminating         0          2h
zk-1      0/1       Pending             0          0s
zk-1      0/1       Pending             0          0s
```

继续观察 StatefulSet 中的 Pod 并腾空 `zk-2` 调度所在的节点。

```shell
kubectl drain $(kubectl get pod zk-2 --template {{.spec.nodeName}}) --ignore-daemonsets --force --delete-emptydir-data
```

输出类似于：

```
node "kubernetes-node-i4c4" cordoned

WARNING: Deleting pods not managed by ReplicationController, ReplicaSet, Job, or DaemonSet: fluentd-cloud-logging-kubernetes-node-i4c4, kube-proxy-kubernetes-node-i4c4; Ignoring DaemonSet-managed pods: node-problem-detector-v0.1-dyrog
WARNING: Ignoring DaemonSet-managed pods: node-problem-detector-v0.1-dyrog; Deleting pods not managed by ReplicationController, ReplicaSet, Job, or DaemonSet: fluentd-cloud-logging-kubernetes-node-i4c4, kube-proxy-kubernetes-node-i4c4
There are pending pods when an error occurred: Cannot evict pod as it would violate the pod's disruption budget.
pod/zk-2
```

使用 `CTRL-C` 终止 kubectl。

你不能腾空第三个节点，因为驱逐 `zk-2` 将和 `zk-budget` 冲突。
然而这个节点仍然处于隔离状态（Cordoned）。

使用 `zkCli.sh` 从 `zk-0` 取回你的健康检查中输入的数值。

```shell
kubectl exec zk-0 zkCli.sh get /hello
```

由于遵守了 `PodDisruptionBudget`，服务仍然可用。

```
WatchedEvent state:SyncConnected type:None path:null
world
cZxid = 0x200000002
ctime = Wed Dec 07 00:08:59 UTC 2016
mZxid = 0x200000002
mtime = Wed Dec 07 00:08:59 UTC 2016
pZxid = 0x200000002
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 5
numChildren = 0
```

使用 [`kubectl uncordon`](/docs/reference/generated/kubectl/kubectl-commands/#uncordon)
来取消对第一个节点的隔离。

```shell
kubectl uncordon kubernetes-node-pb41
```

输出类似于：

```
node "kubernetes-node-pb41" uncordoned
```

`zk-1` 被重新调度到了这个节点。等待 `zk-1` 变为 Running 和 Ready 状态。

```shell
kubectl get pods -w -l app=zk
```

输出类似于：

```
NAME      READY     STATUS             RESTARTS  AGE
zk-0      1/1       Running            2         1h
zk-1      1/1       Running            0         1h
zk-2      1/1       Running            0         1h
NAME      READY     STATUS             RESTARTS  AGE
zk-0      1/1       Terminating        2         2h
zk-0      0/1       Terminating        2         2h
zk-0      0/1       Terminating        2         2h
zk-0      0/1       Terminating        2         2h
zk-0      0/1       Pending            0         0s
zk-0      0/1       Pending            0         0s
zk-0      0/1       ContainerCreating  0         0s
zk-0      0/1       Running            0         51s
zk-0      1/1       Running            0         1m
zk-1      1/1       Terminating        0         2h
zk-1      0/1       Terminating        0         2h
zk-1      0/1       Terminating        0         2h
zk-1      0/1       Terminating        0         2h
zk-1      0/1       Pending            0         0s
zk-1      0/1       Pending            0         0s
zk-1      0/1       Pending            0         12m
zk-1      0/1       ContainerCreating  0         12m
zk-1      0/1       Running            0         13m
zk-1      1/1       Running            0         13m
```

尝试腾空 `zk-2` 调度所在的节点。

```shell
kubectl drain $(kubectl get pod zk-2 --template {{.spec.nodeName}}) --ignore-daemonsets --force --delete-emptydir-data
```

输出类似于：

```
node "kubernetes-node-i4c4" already cordoned
WARNING: Deleting pods not managed by ReplicationController, ReplicaSet, Job, or DaemonSet: fluentd-cloud-logging-kubernetes-node-i4c4, kube-proxy-kubernetes-node-i4c4; Ignoring DaemonSet-managed pods: node-problem-detector-v0.1-dyrog
pod "heapster-v1.2.0-2604621511-wht1r" deleted
pod "zk-2" deleted
node "kubernetes-node-i4c4" drained
```

这次 `kubectl drain` 执行成功。

取消第二个节点的隔离，以允许 `zk-2` 被重新调度。

```shell
kubectl uncordon kubernetes-node-ixsl
```

输出类似于：

```
node "kubernetes-node-ixsl" uncordoned
```

你可以同时使用 `kubectl drain` 和 `PodDisruptionBudgets` 来保证你的服务在维护过程中仍然可用。
如果使用了腾空操作来隔离节点并在节点离线之前驱逐了 Pod，
那么设置了干扰预算的服务将会遵守该预算。
你应该总是为关键服务分配额外容量，这样它们的 Pod 就能够迅速的重新调度。

## {{% heading "cleanup" %}}

* 使用 `kubectl uncordon` 解除你集群中所有节点的隔离。
* 你需要删除在本教程中使用的 PersistentVolume 的持久存储介质。
  请遵循必须的步骤，基于你的环境、存储配置和制备方法，保证回收所有的存储。

