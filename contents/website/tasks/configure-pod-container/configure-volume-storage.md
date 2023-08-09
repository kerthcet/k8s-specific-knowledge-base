---
title: 配置 Pod 以使用卷进行存储
content_type: task
weight: 80
---

此页面展示了如何配置 Pod 以使用卷进行存储。

只要容器存在，容器的文件系统就会存在，因此当一个容器终止并重新启动，对该容器的文件系统改动将丢失。
对于独立于容器的持久化存储，你可以使用[卷](/zh-cn/docs/concepts/storage/volumes/)。
这对于有状态应用程序尤为重要，例如键值存储（如 Redis）和数据库。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


## 为 Pod 配置卷   {#configure-a-volume-for-a-pod}

在本练习中，你将创建一个运行 Pod，该 Pod 仅运行一个容器并拥有一个类型为
[emptyDir](/zh-cn/docs/concepts/storage/volumes/#emptydir) 的卷，
在整个 Pod 生命周期中一直存在，即使 Pod 中的容器被终止和重启。以下是 Pod 的配置：

{{< codenew file="pods/storage/redis.yaml" >}}

1. 创建 Pod:

   ```shell
   kubectl apply -f https://k8s.io/examples/pods/storage/redis.yaml
   ```

2. 验证 Pod 中的容器是否正在运行，然后留意 Pod 的更改：

   ```shell
   kubectl get pod redis --watch
   ```


   输出如下：

   ```console
   NAME      READY     STATUS    RESTARTS   AGE
   redis     1/1       Running   0          13s
   ```

3. 在另一个终端，用 Shell 连接正在运行的容器：

   ```shell
   kubectl exec -it redis -- /bin/bash
   ```

4. 在你的 Shell 中，切换到 `/data/redis` 目录下，然后创建一个文件：

   ```shell
   root@redis:/data# cd /data/redis/
   root@redis:/data/redis# echo Hello > test-file
   ```

5. 在你的 Shell 中，列出正在运行的进程：

   ```shell
   root@redis:/data/redis# apt-get update
   root@redis:/data/redis# apt-get install procps
   root@redis:/data/redis# ps aux
   ```


   输出类似于：

   ```console
   USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
   redis        1  0.1  0.1  33308  3828 ?        Ssl  00:46   0:00 redis-server *:6379
   root        12  0.0  0.0  20228  3020 ?        Ss   00:47   0:00 /bin/bash
   root        15  0.0  0.0  17500  2072 ?        R+   00:48   0:00 ps aux
   ```

6. 在你的 Shell 中，结束 Redis 进程：

   ```shell
   root@redis:/data/redis# kill <pid>
   ```


   其中 `<pid>` 是 Redis 进程的 ID (PID)。

7. 在你原先终端中，留意 Redis Pod 的更改。最终你将会看到和下面类似的输出：

   ```console
   NAME      READY     STATUS     RESTARTS   AGE
   redis     1/1       Running    0          13s
   redis     0/1       Completed  0         6m
   redis     1/1       Running    1         6m
   ```

此时，容器已经终止并重新启动。这是因为 Redis Pod 的
[restartPolicy](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core)
为 `Always`。

1. 用 Shell 进入重新启动的容器中：

   ```shell
   kubectl exec -it redis -- /bin/bash
   ```

2. 在你的 Shell 中，进入到 `/data/redis` 目录下，并确认 `test-file` 文件是否仍然存在。

   ```shell
   root@redis:/data/redis# cd /data/redis/
   root@redis:/data/redis# ls
   test-file
   ```

3. 删除为此练习所创建的 Pod：

   ```shell
   kubectl delete pod redis
   ```

## {{% heading "whatsnext" %}}

- 参阅 [Volume](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#volume-v1-core)。
- 参阅 [Pod](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#pod-v1-core)。
- 除了 `emptyDir` 提供的本地磁盘存储外，Kubernetes 还支持许多不同的网络附加存储解决方案，
  包括 GCE 上的 PD 和 EC2 上的 EBS，它们是关键数据的首选，并将处理节点上的一些细节，
  例如安装和卸载设备。了解更多详情请参阅[卷](/zh-cn/docs/concepts/storage/volumes/)。

