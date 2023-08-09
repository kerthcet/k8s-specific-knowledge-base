---
title: 运行一个有状态的应用程序
content_type: tutorial
weight: 30
---


本页展示如何使用 {{< glossary_tooltip term_id="statefulset" >}}
控制器运行一个有状态的应用程序。此例是多副本的 MySQL 数据库。
示例应用的拓扑结构有一个主服务器和多个副本，使用异步的基于行（Row-Based）
的数据复制。

{{< note >}}
**这一配置不适合生产环境。**
MySQL 设置都使用的是不安全的默认值，这是因为我们想把重点放在 Kubernetes
中运行有状态应用程序的一般模式上。
{{< /note >}}

## {{% heading "prerequisites" %}}

- {{< include "task-tutorial-prereqs.md" >}}
- {{< include "default-storage-class-prereqs.md" >}}
- 本教程假定你熟悉
  [PersistentVolumes](/zh-cn/docs/concepts/storage/persistent-volumes/)
  与 [StatefulSet](/zh-cn/docs/concepts/workloads/controllers/statefulset/)，
  以及其他核心概念，例如 [Pod](/zh-cn/docs/concepts/workloads/pods/)、
  [服务](/zh-cn/docs/concepts/services-networking/service/)与
  [ConfigMap](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/)。
- 熟悉 MySQL 会有所帮助，但是本教程旨在介绍对其他系统应该有用的常规模式。
- 你正在使用默认命名空间或不包含任何冲突对象的另一个命名空间。

## {{% heading "objectives" %}}

- 使用 StatefulSet 部署多副本 MySQL 拓扑架构。
- 发送 MySQL 客户端请求。
- 观察对宕机的抵抗力。
- 扩缩 StatefulSet 的规模。


## 部署 MySQL  {#deploy-mysql}

MySQL 示例部署包含一个 ConfigMap、两个 Service 与一个 StatefulSet。

### 创建一个 ConfigMap   {#configmap}

使用以下的 YAML 配置文件创建 ConfigMap ：

{{< codenew file="application/mysql/mysql-configmap.yaml" >}}

```shell
kubectl apply -f https://k8s.io/examples/application/mysql/mysql-configmap.yaml
```

这个 ConfigMap 提供 `my.cnf` 覆盖设置，使你可以独立控制 MySQL 主服务器和副本服务器的配置。
在这里，你希望主服务器能够将复制日志提供给副本服务器，
并且希望副本服务器拒绝任何不是通过复制进行的写操作。

ConfigMap 本身没有什么特别之处，因而也不会出现不同部分应用于不同的 Pod 的情况。
每个 Pod 都会在初始化时基于 StatefulSet 控制器提供的信息决定要查看的部分。

### 创建 Service  {#services}

使用以下 YAML 配置文件创建服务：

{{< codenew file="application/mysql/mysql-services.yaml" >}}

```shell
kubectl apply -f https://k8s.io/examples/application/mysql/mysql-services.yaml
```

这个无头 Service 给 StatefulSet {{< glossary_tooltip text="控制器" term_id="controller" >}}
为集合中每个 Pod 创建的 DNS 条目提供了一个宿主。
因为无头服务名为 `mysql`，所以可以通过在同一 Kubernetes 集群和命名空间中的任何其他 Pod
内解析 `<Pod 名称>.mysql` 来访问 Pod。

客户端 Service 称为 `mysql-read`，是一种常规 Service，具有其自己的集群 IP。
该集群 IP 在报告就绪的所有 MySQL Pod 之间分配连接。
可能的端点集合包括 MySQL 主节点和所有副本节点。

请注意，只有读查询才能使用负载平衡的客户端 Service。
因为只有一个 MySQL 主服务器，所以客户端应直接连接到 MySQL 主服务器 Pod
（通过其在无头 Service 中的 DNS 条目）以执行写入操作。

### 创建 StatefulSet {#statefulset}

最后，使用以下 YAML 配置文件创建 StatefulSet：

{{< codenew file="application/mysql/mysql-statefulset.yaml" >}}

```shell
kubectl apply -f https://k8s.io/examples/application/mysql/mysql-statefulset.yaml
```

你可以通过运行以下命令查看启动进度：

```shell
kubectl get pods -l app=mysql --watch
```

一段时间后，你应该看到所有 3 个 Pod 进入 `Running` 状态：

```
NAME      READY     STATUS    RESTARTS   AGE
mysql-0   2/2       Running   0          2m
mysql-1   2/2       Running   0          1m
mysql-2   2/2       Running   0          1m
```

输入 **Ctrl+C** 结束监视操作。

{{< note >}}
如果你看不到任何进度，确保已启用[前提条件](#准备开始)中提到的动态
PersistentVolume 制备器。
{{< /note >}}

此清单使用多种技术来管理作为 StatefulSet 的一部分的有状态 Pod。
下一节重点介绍其中的一些技巧，以解释 StatefulSet 创建 Pod 时发生的状况。

## 了解有状态的 Pod 初始化   {#understanding-stateful-pod-init}

StatefulSet 控制器按序数索引顺序地每次启动一个 Pod。
它一直等到每个 Pod 报告就绪才再启动下一个 Pod。

此外，控制器为每个 Pod 分配一个唯一、稳定的名称，形如 `<statefulset 名称>-<序数索引>`，
其结果是 Pods 名为 `mysql-0`、`mysql-1` 和 `mysql-2`。

上述 StatefulSet 清单中的 Pod 模板利用这些属性来执行 MySQL 副本的有序启动。

### 生成配置   {#generating-config}

在启动 Pod 规约中的任何容器之前，Pod 首先按顺序运行所有的
[Init 容器](/zh-cn/docs/concepts/workloads/pods/init-containers/)。

第一个名为 `init-mysql` 的 Init 容器根据序号索引生成特殊的 MySQL 配置文件。

该脚本通过从 Pod 名称的末尾提取索引来确定自己的序号索引，而 Pod 名称由 `hostname` 命令返回。
然后将序数（带有数字偏移量以避免保留值）保存到 MySQL `conf.d` 目录中的文件 `server-id.cnf`。
这一操作将 StatefulSet 所提供的唯一、稳定的标识转换为 MySQL 服务器 ID，
而这些 ID 也是需要唯一性、稳定性保证的。

通过将内容复制到 `conf.d` 中，`init-mysql` 容器中的脚本也可以应用 ConfigMap 中的
`primary.cnf` 或 `replica.cnf`。
由于示例部署结构由单个 MySQL 主节点和任意数量的副本节点组成，
因此脚本仅将序数 `0` 指定为主节点，而将其他所有节点指定为副本节点。

与 StatefulSet
控制器的[部署顺序保证](/zh-cn/docs/concepts/workloads/controllers/statefulset/#deployment-and-scaling-guarantees)相结合，
可以确保 MySQL 主服务器在创建副本服务器之前已准备就绪，以便它们可以开始复制。

### 克隆现有数据   {#cloning-existing-data}

通常，当新 Pod 作为副本节点加入集合时，必须假定 MySQL 主节点可能已经有数据。
还必须假设复制日志可能不会一直追溯到时间的开始。

这些保守的假设是允许正在运行的 StatefulSet 随时间扩大和缩小而不是固定在其初始大小的关键。

第二个名为 `clone-mysql` 的 Init 容器，第一次在带有空 PersistentVolume 的副本 Pod
上启动时，会在从属 Pod 上执行克隆操作。
这意味着它将从另一个运行中的 Pod 复制所有现有数据，使此其本地状态足够一致，
从而可以开始从主服务器复制。

MySQL 本身不提供执行此操作的机制，因此本示例使用了一种流行的开源工具 Percona XtraBackup。
在克隆期间，源 MySQL 服务器性能可能会受到影响。
为了最大程度地减少对 MySQL 主服务器的影响，该脚本指示每个 Pod 从序号较低的 Pod 中克隆。
可以这样做的原因是 StatefulSet 控制器始终确保在启动 Pod `N+1` 之前 Pod `N` 已准备就绪。

### 开始复制   {#starting-replication}

Init 容器成功完成后，应用容器将运行。MySQL Pod 由运行实际 `mysqld` 服务的 `mysql`
容器和充当[辅助工具](/blog/2015/06/the-distributed-system-toolkit-patterns)的
xtrabackup 容器组成。

`xtrabackup` sidecar 容器查看克隆的数据文件，并确定是否有必要在副本服务器上初始化 MySQL 复制。
如果是这样，它将等待 `mysqld` 准备就绪，然后使用从 XtraBackup 克隆文件中提取的复制参数执行
`CHANGE MASTER TO` 和 `START SLAVE` 命令。

一旦副本服务器开始复制后，它会记住其 MySQL 主服务器，并且如果服务器重新启动或连接中断也会自动重新连接。
另外，因为副本服务器会以其稳定的 DNS 名称查找主服务器（`mysql-0.mysql`），
即使由于重新调度而获得新的 Pod IP，它们也会自动找到主服务器。

最后，开始复制后，`xtrabackup` 容器监听来自其他 Pod 的连接，处理其数据克隆请求。
如果 StatefulSet 扩大规模，或者下一个 Pod 失去其 PersistentVolumeClaim 并需要重新克隆，
则此服务器将无限期保持运行。

## 发送客户端请求   {#sending-client-traffic}

你可以通过运行带有 `mysql:5.7` 镜像的临时容器并运行 `mysql` 客户端二进制文件，
将测试查询发送到 MySQL 主服务器（主机名 `mysql-0.mysql`）。

```shell
kubectl run mysql-client --image=mysql:5.7 -i --rm --restart=Never --\
  mysql -h mysql-0.mysql <<EOF
CREATE DATABASE test;
CREATE TABLE test.messages (message VARCHAR(250));
INSERT INTO test.messages VALUES ('hello');
EOF
```

使用主机名 `mysql-read` 将测试查询发送到任何报告为就绪的服务器：

```shell
kubectl run mysql-client --image=mysql:5.7 -i -t --rm --restart=Never --\
  mysql -h mysql-read -e "SELECT * FROM test.messages"
```

你应该获得如下输出：

```
Waiting for pod default/mysql-client to be running, status is Pending, pod ready: false
+---------+
| message |
+---------+
| hello   |
+---------+
pod "mysql-client" deleted
```

为了演示 `mysql-read` 服务在服务器之间分配连接，你可以在循环中运行 `SELECT @@server_id`：

```shell
kubectl run mysql-client-loop --image=mysql:5.7 -i -t --rm --restart=Never --\
  bash -ic "while sleep 1; do mysql -h mysql-read -e 'SELECT @@server_id,NOW()'; done"
```

你应该看到报告的 `@@server_id` 发生随机变化，因为每次尝试连接时都可能选择了不同的端点：

```
+-------------+---------------------+
| @@server_id | NOW()               |
+-------------+---------------------+
|         100 | 2006-01-02 15:04:05 |
+-------------+---------------------+
+-------------+---------------------+
| @@server_id | NOW()               |
+-------------+---------------------+
|         102 | 2006-01-02 15:04:06 |
+-------------+---------------------+
+-------------+---------------------+
| @@server_id | NOW()               |
+-------------+---------------------+
|         101 | 2006-01-02 15:04:07 |
+-------------+---------------------+
```

要停止循环时可以按 **Ctrl+C** ，但是让它在另一个窗口中运行非常有用，
这样你就可以看到以下步骤的效果。

## 模拟 Pod 和 Node 失效   {#simulate-pod-and-node-downtime}

为了证明从副本节点缓存而不是单个服务器读取数据的可用性提高，请在使 Pod 退出 Ready
状态时，保持上述 `SELECT @@server_id` 循环一直运行。

### 破坏就绪态探测   {#break-readiness-probe}

`mysql` 容器的[就绪态探测](/zh-cn/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-readiness-probes)
运行命令 `mysql -h 127.0.0.1 -e 'SELECT 1'`，以确保服务器已启动并能够执行查询。

迫使就绪态探测失败的一种方法就是中止该命令：

```shell
kubectl exec mysql-2 -c mysql -- mv /usr/bin/mysql /usr/bin/mysql.off
```

此命令会进入 Pod `mysql-2` 的实际容器文件系统，重命名 `mysql` 命令，导致就绪态探测无法找到它。
几秒钟后， Pod 会报告其中一个容器未就绪。你可以通过运行以下命令进行检查：

```shell
kubectl get pod mysql-2
```

在 `READY` 列中查找 `1/2`：

```
NAME      READY     STATUS    RESTARTS   AGE
mysql-2   1/2       Running   0          3m
```

此时，你应该会看到 `SELECT @@server_id` 循环继续运行，尽管它不再报告 `102`。
回想一下，`init-mysql` 脚本将 `server-id` 定义为 `100 + $ordinal`，
因此服务器 ID `102` 对应于 Pod `mysql-2`。

现在修复 Pod，几秒钟后它应该重新出现在循环输出中：

```shell
kubectl exec mysql-2 -c mysql -- mv /usr/bin/mysql.off /usr/bin/mysql
```

### 删除 Pod   {#delete-pods}

如果删除了 Pod，则 StatefulSet 还会重新创建 Pod，类似于 ReplicaSet 对无状态 Pod 所做的操作。

```shell
kubectl delete pod mysql-2
```

StatefulSet 控制器注意到不再存在 `mysql-2` Pod，于是创建一个具有相同名称并链接到相同
PersistentVolumeClaim 的新 Pod。
你应该看到服务器 ID `102` 从循环输出中消失了一段时间，然后又自行出现。

### 腾空节点   {#drain-a-node}

如果你的 Kubernetes 集群具有多个节点，则可以通过发出以下
[drain](/docs/reference/generated/kubectl/kubectl-commands/#drain)
命令来模拟节点停机（就好像节点在被升级）。

首先确定 MySQL Pod 之一在哪个节点上：

```shell
kubectl get pod mysql-2 -o wide
```

节点名称应显示在最后一列中：

```
NAME      READY     STATUS    RESTARTS   AGE       IP            NODE
mysql-2   2/2       Running   0          15m       10.244.5.27   kubernetes-node-9l2t
```

接下来，通过运行以下命令腾空节点，该命令将其保护起来，以使新的 Pod 不能调度到该节点，
然后逐出所有现有的 Pod。将 `<节点名称>` 替换为在上一步中找到的节点名称。

{{< caution >}}
腾空一个 Node 可能影响到在该节点上运行的其他负载和应用。
只应在测试集群上执行下列步骤。
{{< /caution >}}


```shell
# 关于对其他负载的影响，参见前文建议
kubectl drain <节点名称> --force --delete-local-data --ignore-daemonsets
```

现在，你可以监视 Pod 被重新调度到其他节点上：

```shell
kubectl get pod mysql-2 -o wide --watch
```

它看起来应该像这样：

```
NAME      READY   STATUS          RESTARTS   AGE       IP            NODE
mysql-2   2/2     Terminating     0          15m       10.244.1.56   kubernetes-node-9l2t
[...]
mysql-2   0/2     Pending         0          0s        <none>        kubernetes-node-fjlm
mysql-2   0/2     Init:0/2        0          0s        <none>        kubernetes-node-fjlm
mysql-2   0/2     Init:1/2        0          20s       10.244.5.32   kubernetes-node-fjlm
mysql-2   0/2     PodInitializing 0          21s       10.244.5.32   kubernetes-node-fjlm
mysql-2   1/2     Running         0          22s       10.244.5.32   kubernetes-node-fjlm
mysql-2   2/2     Running         0          30s       10.244.5.32   kubernetes-node-fjlm
```

再次，你应该看到服务器 ID `102` 从 `SELECT @@server_id`
循环输出中消失一段时间，然后再次出现。

现在去掉节点保护（Uncordon），使其恢复为正常模式:

```shell
kubectl uncordon <节点名称>
```

## 扩展副本节点数量    {#scaling-number-of-replicas}

使用 MySQL 复制时，你可以通过添加副本节点来扩展读取查询的能力。
对于 StatefulSet，你可以使用单个命令实现此目的：

```shell
kubectl scale statefulset mysql --replicas=5
```

运行下面的命令，监视新的 Pod 启动：

```shell
kubectl get pods -l app=mysql --watch
```

一旦 Pod 启动，你应该看到服务器 ID `103` 和 `104` 开始出现在 `SELECT @@server_id`
循环输出中。

你还可以验证这些新服务器在存在之前已添加了数据：

```shell
kubectl run mysql-client --image=mysql:5.7 -i -t --rm --restart=Never --\
  mysql -h mysql-3.mysql -e "SELECT * FROM test.messages"
```

```
Waiting for pod default/mysql-client to be running, status is Pending, pod ready: false
+---------+
| message |
+---------+
| hello   |
+---------+
pod "mysql-client" deleted
```

向下缩容操作也是很平滑的：

```shell
kubectl scale statefulset mysql --replicas=3
```

{{< note >}}
扩容操作会自动创建新的 PersistentVolumeClaim，但是缩容时不会自动删除这些 PVC。
这使你可以选择保留那些已被初始化的 PVC，以加速再次扩容，或者在删除它们之前提取数据。
{{< /note >}}

你可以通过运行以下命令查看此效果：

```shell
kubectl get pvc -l app=mysql
```

这表明，尽管将 StatefulSet 缩小为 3，所有 5 个 PVC 仍然存在：

```
NAME           STATUS    VOLUME                                     CAPACITY   ACCESSMODES   AGE
data-mysql-0   Bound     pvc-8acbf5dc-b103-11e6-93fa-42010a800002   10Gi       RWO           20m
data-mysql-1   Bound     pvc-8ad39820-b103-11e6-93fa-42010a800002   10Gi       RWO           20m
data-mysql-2   Bound     pvc-8ad69a6d-b103-11e6-93fa-42010a800002   10Gi       RWO           20m
data-mysql-3   Bound     pvc-50043c45-b1c5-11e6-93fa-42010a800002   10Gi       RWO           2m
data-mysql-4   Bound     pvc-500a9957-b1c5-11e6-93fa-42010a800002   10Gi       RWO           2m
```

如果你不打算重复使用多余的 PVC，则可以删除它们：

```shell
kubectl delete pvc data-mysql-3
kubectl delete pvc data-mysql-4
```

## {{% heading "cleanup" %}}

1. 通过在终端上按 **Ctrl+C** 取消 `SELECT @@server_id` 循环，或从另一个终端运行以下命令：

   ```shell
   kubectl delete pod mysql-client-loop --now
   ```

2. 删除 StatefulSet。这也会开始终止 Pod。

   ```shell
   kubectl delete statefulset mysql
   ```

3. 验证 Pod 消失。它们可能需要一些时间才能完成终止。

   ```shell
   kubectl get pods -l app=mysql
   ```

   当上述命令返回如下内容时，你就知道 Pod 已终止：

   ```
   No resources found.
   ```

4. 删除 ConfigMap、Service 和 PersistentVolumeClaim。

   ```shell
   kubectl delete configmap,service,pvc -l app=mysql
   ```

5. 如果你手动制备 PersistentVolume，则还需要手动删除它们，并释放下层资源。
   如果你使用了动态制备器，当得知你删除 PersistentVolumeClaim 时，它将自动删除 PersistentVolume。
   一些动态制备器（例如用于 EBS 和 PD 的制备器）也会在删除 PersistentVolume 时释放下层资源。

## {{% heading "whatsnext" %}}

- 进一步了解[为 StatefulSet 扩缩容](/zh-cn/docs/tasks/run-application/scale-stateful-set/)；
- 进一步了解[调试 StatefulSet](/zh-cn/docs/tasks/debug/debug-application/debug-statefulset/)；
- 进一步了解[删除 StatefulSet](/zh-cn/docs/tasks/run-application/delete-stateful-set/)；
- 进一步了解[强制删除 StatefulSet Pod](/zh-cn/docs/tasks/run-application/force-delete-stateful-set-pod/)；
- 在 [Helm Charts 仓库](https://artifacthub.io/)中查找其他有状态的应用程序示例。
