---
layout: blog
title: "Kubernetes 1.27: StatefulSet 启动序号简化了迁移"
date: 2023-04-28
slug: statefulset-start-ordinal
---


**作者：** Peter Schuurman (Google)

**译者：** Xin Li (DaoCloud)

Kubernetes v1.26 为 [StatefulSet](/zh-cn/docs/concepts/workloads/controllers/statefulset/)
引入了一个新的 Alpha 级别特性，可以控制 Pod 副本的序号。
从 Kubernetes v1.27 开始，此特性进级到 Beta 阶段。序数可以从任意非负数开始，
这篇博文将讨论如何使用此功能。

## 背景

StatefulSet 序号为 Pod 副本提供顺序标识。当使用
[`OrderedReady` Pod 管理策略](/docs/tutorials/stateful-application/basic-stateful-set/#orderedready-pod-management)时，
Pod 是从序号索引 `0` 到 `N-1` 顺序创建的。

如今使用 Kubernetes 跨集群编排 StatefulSet 迁移具有挑战性。
虽然存在备份和恢复解决方案，但这些解决方案需要在迁移之前将应用程序的副本数缩为 0。
在当今这个完全互联的世界中，即使是计划内的应用停机可能也无法实现你的业务目标。

你可以使用[级联删除](/zh-cn/docs/tutorials/stateful-application/basic-stateful-set/#cascading-delete)或
[OnDelete 策略](/zh-cn/docs/tutorials/stateful-application/basic-stateful-set/#on-delete)来迁移单个 Pod，
但是这很容易出错并且管理起来很乏味。
当你的 Pod 出现故障或被逐出时，你将失去 StatefulSet 控制器的自我修复优势。

Kubernetes v1.26 使 StatefulSet 能够负责 {0..N-1} 范围内的一系列序数（序数 0、1、... 直到 N-1）。
有了它，你可以缩小源集群中的范围 {0..k-1}，并扩大目标集群中的互补范围 {k..N-1}，同时保证应用程序可用性。
这使你在编排跨集群迁移时保留**至多一个**语义（意味着最多有一个具有给定身份的
Pod 在 StatefulSet 中运行）和[滚动更新](/zh-cn/docs/tutorials/stateful-application/basic-stateful-set/#rolling-update）行为。

## 我为什么要使用此功能？

假设你在一个集群中运行 StatefulSet，并且需要将其迁移到另一个集群。你需要这样做的原因有很多：

 * **可扩展性**：你的 StatefulSet 对于你的集群而言规模过大，并且已经开始破坏集群中其他工作负载的服务质量。
 * **隔离性**：你在一个供多个用户访问的集群中运行 StatefulSet，而命名空间隔离是不够的。
 * **集群配置**：你想将 StatefulSet 迁移到另一个集群，以使用在当前集群上不存在的某些环境。
 * **控制平面升级**：你想将 StatefulSet 迁移到运行着较高版本控制平面，
   并且无法处承担就地升级控制平面所产生的风险或预留停机时间。

## 我该如何使用它？

在集群上启用 `StatefulSetStartOrdinal` 特性门控，并使用自定义的
`.spec.ordinals.start` 创建一个 StatefulSet。

## 试试看吧

在此演示中，我将使用新机制将 StatefulSet 从一个 Kubernetes 集群迁移到另一个。
[redis-cluster](https://github.com/bitnami/charts/tree/main/bitnami/redis-cluster)
Bitnami Helm chart 将用于安装 Redis。

所需工具：

 * [yq](https://github.com/mikefarah/yq)
 * [helm](https://helm.sh/docs/helm/helm_install/)

### 先决条件    {#demo-pre-requisites}

为此，我需要两个可以访问公共网络和存储的 Kubernetes 集群；
我已将集群命名为 `source` 和 `destination`。具体来说，我需要：

* 在两个集群上都启用 `StatefulSetStartOrdinal` 特性门控。
* `kubectl` 的客户端配置允许我以管理员身份访问这两个集群。
* 两个集群上都安装了相同的 `StorageClass`，并设置为两个集群的默认 `StorageClass`。
  这个 `StorageClass` 应该提供可从一个或两个集群访问的底层存储。
* 一种扁平的网络拓扑，允许 Pod 向任一集群中的 Pod 发送数据包和从中接收数据包。
  如果你在云提供商上创建集群，则此配置可能被称为私有云或私有网络。

1. 在两个集群上创建一个用于演示的命名空间：

   ```
   kubectl create ns kep-3335
   ```

2. 在 `source` 集群中部署一个有六个副本的 Redis 集群：

   ```
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm install redis --namespace kep-3335 \
     bitnami/redis-cluster \
     --set persistence.size=1Gi \
     --set cluster.nodes=6
   ```

3. 检查 `source` 集群中的副本状态：

   ```
   kubectl exec -it redis-redis-cluster-0 -- /bin/bash -c \
     "redis-cli -c -h redis-redis-cluster -a $(kubectl get secret redis-redis-cluster -o jsonpath="{.data.redis-password}" | base64 -d) CLUSTER NODES;"
   ```

   ```
   2ce30362c188aabc06f3eee5d92892d95b1da5c3 10.104.0.14:6379@16379 myself,master - 0 1669764411000 3 connected 10923-16383                                                                                                                                              
   7743661f60b6b17b5c71d083260419588b4f2451 10.104.0.16:6379@16379 slave 2ce30362c188aabc06f3eee5d92892d95b1da5c3 0 1669764410000 3 connected                                                                                             
   961f35e37c4eea507cfe12f96e3bfd694b9c21d4 10.104.0.18:6379@16379 slave a8765caed08f3e185cef22bd09edf409dc2bcc61 0 1669764411000 1 connected                                                                                                             
   7136e37d8864db983f334b85d2b094be47c830e5 10.104.0.15:6379@16379 slave 2cff613d763b22c180cd40668da8e452edef3fc8 0 1669764412595 2 connected                                                                                                                    
   a8765caed08f3e185cef22bd09edf409dc2bcc61 10.104.0.19:6379@16379 master - 0 1669764411592 1 connected 0-5460                                                                                                                                                   
   2cff613d763b22c180cd40668da8e452edef3fc8 10.104.0.17:6379@16379 master - 0 1669764410000 2 connected 5461-10922
   ```

4. 在 `destination` 集群中部署一个零副本的 Redis 集群：

   ```
   helm install redis --namespace kep-3335 \
     bitnami/redis-cluster \
     --set persistence.size=1Gi \
     --set cluster.nodes=0 \
     --set redis.extraEnvVars\[0\].name=REDIS_NODES,redis.extraEnvVars\[0\].value="redis-redis-cluster-headless.kep-3335.svc.cluster.local" \
     --set existingSecret=redis-redis-cluster
   ```

5. 将源集群中的 `redis-redis-cluster` StatefulSet 副本数缩小 1，
   以删除副本 `redis-redis-cluster-5`：

   ```
   kubectl patch sts redis-redis-cluster -p '{"spec": {"replicas": 5}}'
   ```

6. 将依赖从 `source` 集群迁移到 `destionation` 集群：
   以下命令将依赖资源从 `source` 复制到 `destionation`，其中与 `destionation`
   集群无关的详细信息已被删除（例如：`uid`、`resourceVersion`、`status`）。


   说明：如果使用配置了 `reclaimPolicy: Delete` 的 `StorageClass`，
        你应该在删除之前使用 `reclaimPolicy: Retain` 修补 `source` 中的 PV，
        以保留 `destination` 中使用的底层存储。
        有关详细信息，请参阅[更改 PersistentVolume](/zh-cn/docs/tasks/administer-cluster/change-pv-reclaim-policy/)
        的回收策略。
   
   ```
   kubectl get pvc redis-data-redis-redis-cluster-5 -o yaml | yq 'del(.metadata.uid, .metadata.resourceVersion, .metadata.annotations, .metadata.finalizers, .status)' > /tmp/pvc-redis-data-redis-redis-cluster-5.yaml
   kubectl get pv $(yq '.spec.volumeName' /tmp/pvc-redis-data-redis-redis-cluster-5.yaml) -o yaml | yq 'del(.metadata.uid, .metadata.resourceVersion, .metadata.annotations, .metadata.finalizers, .spec.claimRef, .status)' > /tmp/pv-redis-data-redis-redis-cluster-5.yaml
   kubectl get secret redis-redis-cluster -o yaml | yq 'del(.metadata.uid, .metadata.resourceVersion)' > /tmp/secret-redis-redis-cluster.yaml
   ```


   **`destination` 集群中的步骤**

   说明：对于 PV/PVC，此过程仅在你的 PV 使用的底层存储系统支持复制到 `destination`
        集群时才有效。可能不支持与特定节点或拓扑关联的存储。此外，某些存储系统可能会在 PV
        对象之外存储有关卷的附加元数据，并且可能需要更专门的序列来导入卷。
   
   ```
   kubectl create -f /tmp/pv-redis-data-redis-redis-cluster-5.yaml
   kubectl create -f /tmp/pvc-redis-data-redis-redis-cluster-5.yaml
   kubectl create -f /tmp/secret-redis-redis-cluster.yaml
   ```

7. 将 `destination` 集群中的 `redis-redis-cluster` StatefulSet 扩容 1，起始序号为 5：

   ```
   kubectl patch sts redis-redis-cluster -p '{"spec": {"ordinals": {"start": 5}, "replicas": 1}}'
   ```

8. 检查 `destination` 集群中的副本状态：

   ```
   kubectl exec -it redis-redis-cluster-5 -- /bin/bash -c \
     "redis-cli -c -h redis-redis-cluster -a $(kubectl get secret redis-redis-cluster -o jsonpath="{.data.redis-password}" | base64 -d) CLUSTER NODES;"
   ```

   我应该看到新副本（标记为 `myself`）已加入 Redis 集群（IP
   地址与 `source` 集群中的副本归属于不同的 CIDR 块）。

   ```
   2cff613d763b22c180cd40668da8e452edef3fc8 10.104.0.17:6379@16379 master - 0 1669766684000 2 connected 5461-10922
   7136e37d8864db983f334b85d2b094be47c830e5 10.108.0.22:6379@16379 myself,slave 2cff613d763b22c180cd40668da8e452edef3fc8 0 1669766685609 2 connected
   2ce30362c188aabc06f3eee5d92892d95b1da5c3 10.104.0.14:6379@16379 master - 0 1669766684000 3 connected 10923-16383
   961f35e37c4eea507cfe12f96e3bfd694b9c21d4 10.104.0.18:6379@16379 slave a8765caed08f3e185cef22bd09edf409dc2bcc61 0 1669766683600 1 connected
   a8765caed08f3e185cef22bd09edf409dc2bcc61 10.104.0.19:6379@16379 master - 0 1669766685000 1 connected 0-5460
   7743661f60b6b17b5c71d083260419588b4f2451 10.104.0.16:6379@16379 slave 2ce30362c188aabc06f3eee5d92892d95b1da5c3 0 1669766686613 3 connected
   ```

9. 对剩余的副本重复 #5 到 #7 的步骤，直到 `source` 集群中的 Redis StatefulSet 副本缩放为 0，
   并且 `destination` 集群中的 Redis StatefulSet 健康，总共有 6 个副本。

## 接下来？

此特性为跨集群拆分 StatefulSet 提供了一项基本支撑技术，但没有规定 StatefulSet 的迁移机制。
迁移需要对 StatefulSet 副本的协调，以及对存储和网络层的编排。这取决于使用 StatefulSet
安装的应用程序的存储和网络连接要求。此外，许多 StatefulSet 由
[operator](/zh-cn/docs/concepts/extend-kubernetes/operator/) 管理，这也增加了额外的迁移复杂性。

如果你有兴趣构建增强功能以简化这些过程，请参与
[SIG Multicluster](https://github.com/kubernetes/community/blob/master/sig-multicluster)
做出贡献！


