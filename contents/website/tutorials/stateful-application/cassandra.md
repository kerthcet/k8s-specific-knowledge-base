---
title: "示例：使用 StatefulSet 部署 Cassandra"
content_type: tutorial
weight: 30
---


本教程描述了如何在 Kubernetes 上运行 [Apache Cassandra](https://cassandra.apache.org/)。
数据库 Cassandra 需要永久性存储提供数据持久性（应用**状态**）。
在此示例中，自定义 Cassandra seed provider 使数据库在接入 Cassandra 集群时能够发现新的 Cassandra 实例。

使用**StatefulSet**可以更轻松地将有状态的应用程序部署到你的 Kubernetes 集群中。
有关本教程中使用的功能的更多信息，
请参阅 [StatefulSet](/zh-cn/docs/concepts/workloads/controllers/statefulset/)。

{{< note >}}
Cassandra 和 Kubernetes 都使用术语**节点**来表示集群的成员。
在本教程中，属于 StatefulSet 的 Pod 是 Cassandra 节点，并且是 Cassandra 集群的成员（称为 **ring**）。
当这些 Pod 在你的 Kubernetes 集群中运行时，Kubernetes 控制平面会将这些 Pod 调度到 Kubernetes 的
{{< glossary_tooltip text="节点" term_id="node" >}}上。

当 Cassandra 节点启动时，使用 **seed 列表**来引导发现 ring 中的其他节点。
本教程部署了一个自定义的 Cassandra seed provider，
使数据库可以发现 Kubernetes 集群中出现的新的 Cassandra Pod。
{{< /note >}}

## {{% heading "objectives" %}}

* 创建并验证 Cassandra 无头（headless）{{< glossary_tooltip text="Service" term_id="service" >}}。
* 使用 {{< glossary_tooltip term_id="StatefulSet" >}} 创建一个 Cassandra ring。
* 验证 StatefulSet。
* 修改 StatefulSet。
* 删除 StatefulSet 及其 {{< glossary_tooltip text="Pod" term_id="pod" >}}。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

要完成本教程，你应该已经熟悉 {{< glossary_tooltip text="Pod" term_id="pod" >}}、
{{< glossary_tooltip text="Service" term_id="service" >}} 和
{{< glossary_tooltip text="StatefulSet" term_id="StatefulSet" >}}。

### 额外的 Minikube 设置说明

{{< caution >}}
[Minikube](https://minikube.sigs.k8s.io/docs/) 默认需要 2048MB 内存和 2 个 CPU。
在本教程中，使用默认资源配置运行 Minikube 会出现资源不足的错误。为避免这些错误，请使用以下设置启动 Minikube：

```shell
minikube start --memory 5120 --cpus=4
```

{{< /caution >}}

## 为 Cassandra 创建无头（headless） Services {#creating-a-cassandra-headless-service}

在 Kubernetes 中，一个 {{< glossary_tooltip text="Service" term_id="service" >}}
描述了一组执行相同任务的 {{< glossary_tooltip text="Pod" term_id="pod" >}}。

以下 Service 用于在 Cassandra Pod 和集群中的客户端之间进行 DNS 查找：

{{< codenew file="application/cassandra/cassandra-service.yaml" >}}

创建一个 Service 来跟踪 `cassandra-service.yaml` 文件中的所有 Cassandra StatefulSet：

```shell
kubectl apply -f https://k8s.io/examples/application/cassandra/cassandra-service.yaml
```

### 验证(可选) {#validating}

获取 Cassandra Service。

```shell
kubectl get svc cassandra
```

响应是：

```
NAME        TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
cassandra   ClusterIP   None         <none>        9042/TCP   45s
```

如果没有看到名为 `cassandra` 的服务，则表示创建失败。
请阅读[调试服务](/zh-cn/docs/tasks/debug/debug-application/debug-service/)，以解决常见问题。

## 使用 StatefulSet 创建 Cassandra Ring

下面包含的 StatefulSet 清单创建了一个由三个 Pod 组成的 Cassandra ring。

{{< note >}}
本示例使用 Minikube 的默认配置程序。
请为正在使用的云更新以下 StatefulSet。
{{< /note >}}

{{< codenew file="application/cassandra/cassandra-statefulset.yaml" >}}

使用 `cassandra-statefulset.yaml` 文件创建 Cassandra StatefulSet：

```shell
# 如果你能未经修改地应用 cassandra-statefulset.yaml，请使用此命令
kubectl apply -f https://k8s.io/examples/application/cassandra/cassandra-statefulset.yaml
```

如果你为了适合你的集群需要修改 `cassandra-statefulset.yaml`，
下载 https://k8s.io/examples/application/cassandra/cassandra-statefulset.yaml，
然后应用修改后的清单。

```shell
# 如果使用本地的 cassandra-statefulset.yaml ，请使用此命令
kubectl apply -f cassandra-statefulset.yaml
```

## 验证 Cassandra StatefulSet

1. 获取 Cassandra StatefulSet:

   ```shell
   kubectl get statefulset cassandra
   ```
   
   响应应该与此类似：

   ```
   NAME        DESIRED   CURRENT   AGE
   cassandra   3         0         13s
   ```

   `StatefulSet` 资源会按顺序部署 Pod。

2. 获取 Pod 查看已排序的创建状态：
   
   ```shell
   kubectl get pods -l="app=cassandra"
   ```

   响应应该与此类似：

   ```
   NAME          READY     STATUS              RESTARTS   AGE
   cassandra-0   1/1       Running             0          1m
   cassandra-1   0/1       ContainerCreating   0          8s
   ```

   这三个 Pod 要花几分钟的时间才能部署。部署之后，相同的命令将返回类似于以下的输出：

   ```
   NAME          READY     STATUS    RESTARTS   AGE
   cassandra-0   1/1       Running   0          10m
   cassandra-1   1/1       Running   0          9m
   cassandra-2   1/1       Running   0          8m
   ```
3. 运行第一个 Pod 中的 Cassandra [nodetool](https://cwiki.apache.org/confluence/display/CASSANDRA2/NodeTool)，
   以显示 ring 的状态。

   ```shell
   kubectl exec -it cassandra-0 -- nodetool status
   ```

   响应应该与此类似：

   ```
   Datacenter: DC1-K8Demo
   ======================
   Status=Up/Down
   |/ State=Normal/Leaving/Joining/Moving
   --  Address     Load       Tokens       Owns (effective)  Host ID                               Rack
   UN  172.17.0.5  83.57 KiB  32           74.0%             e2dd09e6-d9d3-477e-96c5-45094c08db0f  Rack1-K8Demo
   UN  172.17.0.4  101.04 KiB  32           58.8%             f89d6835-3a42-4419-92b3-0e62cae1479c  Rack1-K8Demo
   UN  172.17.0.6  84.74 KiB  32           67.1%             a6a1e8c2-3dc5-4417-b1a0-26507af2aaad  Rack1-K8Demo
   ```

## 修改 Cassandra StatefulSet

使用 `kubectl edit` 修改 Cassandra StatefulSet 的大小。

1. 运行以下命令：

   ```shell
   kubectl edit statefulset cassandra
   ```

   此命令你的终端中打开一个编辑器。需要更改的是 `replicas` 字段。下面是 StatefulSet 文件的片段示例：

    ```yaml
    # 请编辑以下对象。以 '#' 开头的行将被忽略，
    # 且空文件将放弃编辑。如果保存此文件时发生错误，
    # 将重新打开并显示相关故障。
    apiVersion: apps/v1
    kind: StatefulSet
    metadata:
      creationTimestamp: 2016-08-13T18:40:58Z
      generation: 1
      labels:
      app: cassandra
      name: cassandra
      namespace: default
      resourceVersion: "323"
      uid: 7a219483-6185-11e6-a910-42010a8a0fc0
    spec:
      replicas: 3
    ```

2. 将副本数（replicas）更改为 4，然后保存清单。

   StatefulSet 现在可以扩展到运行 4 个 Pod。

3. 获取 Cassandra StatefulSet 验证更改：

   ```shell
   kubectl get statefulset cassandra
   ```

   响应应该与此类似：

   ```
   NAME        DESIRED   CURRENT   AGE
   cassandra   4         4         36m
   ```

## {{% heading "cleanup" %}}

删除或缩小 StatefulSet 不会删除与 StatefulSet 关联的卷。
这个设置是出于安全考虑，因为你的数据比自动清除所有相关的 StatefulSet 资源更有价值。

{{< warning >}}
根据存储类和回收策略，删除 **PersistentVolumeClaims** 可能导致关联的卷也被删除。
千万不要认为其容量声明被删除，你就能访问数据。
{{< /warning >}}

1. 运行以下命令（连在一起成为一个单独的命令）删除 Cassandra StatefulSet 中的所有内容：

   ```shell
   grace=$(kubectl get pod cassandra-0 -o=jsonpath='{.spec.terminationGracePeriodSeconds}') \
     && kubectl delete statefulset -l app=cassandra \
     && echo "Sleeping ${grace} seconds" 1>&2 \
     && sleep $grace \
     && kubectl delete persistentvolumeclaim -l app=cassandra
   ```

2. 运行以下命令，删除你为 Cassandra 设置的 Service：

   ```shell
   kubectl delete service -l app=cassandra
   ```

## Cassandra 容器环境变量

本教程中的 Pod 使用来自 Google [容器镜像库](https://cloud.google.com/container-registry/docs/)
的 [`gcr.io/google-samples/cassandra:v13`](https://github.com/kubernetes/examples/blob/master/cassandra/image/Dockerfile)
镜像。上面的 Docker 镜像基于 [debian-base](https://github.com/kubernetes/release/tree/master/images/build/debian-base)，
并且包含 OpenJDK 8。

该镜像包括来自 Apache Debian 存储库的标准 Cassandra 安装。
通过使用环境变量，你可以更改插入到 `cassandra.yaml` 中的值。

| 环境变量                 | 默认值           |
| ------------------------ |:---------------: |
| `CASSANDRA_CLUSTER_NAME` | `'Test Cluster'` |
| `CASSANDRA_NUM_TOKENS`   | `32`             |
| `CASSANDRA_RPC_ADDRESS`  | `0.0.0.0`        |

## {{% heading "whatsnext" %}}

* 了解如何[扩缩 StatefulSet](/docs/tasks/run-application/scale-stateful-set/)。
* 了解有关 [*KubernetesSeedProvider*](https://github.com/kubernetes/examples/blob/master/cassandra/java/src/main/java/io/k8s/cassandra/KubernetesSeedProvider.java) 的更多信息
* 查看更多自定义 [Seed Provider Configurations](https://git.k8s.io/examples/cassandra/java/README.md)

