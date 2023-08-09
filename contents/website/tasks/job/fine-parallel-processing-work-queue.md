---
title: 使用工作队列进行精细的并行处理
content_type: task
min-kubernetes-server-version: v1.8
weight: 30
---


在这个例子中，我们会运行一个 Kubernetes Job，其中的 Pod 会运行多个并行工作进程。

在这个例子中，当每个 Pod 被创建时，它会从一个任务队列中获取一个工作单元，处理它，然后重复，直到到达队列的尾部。

下面是这个示例的步骤概述：


1. **启动存储服务用于保存工作队列。** 在这个例子中，我们使用 Redis 来存储工作项。
   在上一个例子中，我们使用了 RabbitMQ。
   在这个例子中，由于 AMQP 不能为客户端提供一个良好的方法来检测一个有限长度的工作队列是否为空，
   我们使用了 Redis 和一个自定义的工作队列客户端库。
   在实践中，你可能会设置一个类似于 Redis 的存储库，并将其同时用于多项任务或其他事务的工作队列。

2. **创建一个队列，然后向其中填充消息。** 每个消息表示一个将要被处理的工作任务。
   在这个例子中，消息是一个我们将用于进行长度计算的整数。

3. **启动一个 Job 对队列中的任务进行处理**。这个 Job 启动了若干个 Pod。
   每个 Pod 从消息队列中取出一个工作任务，处理它，然后重复，直到到达队列的尾部。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}


熟悉基本的、非并行的 [Job](/zh-cn/docs/concepts/workloads/controllers/job/)。


## 启动 Redis

对于这个例子，为了简单起见，我们将启动一个单实例的 Redis。
了解如何部署一个可伸缩、高可用的 Redis 例子，请查看
[Redis 示例](https://github.com/kubernetes/examples/tree/master/guestbook)

你也可以直接下载如下文件：

- [`redis-pod.yaml`](/examples/application/job/redis/redis-pod.yaml)
- [`redis-service.yaml`](/examples/application/job/redis/redis-service.yaml)
- [`Dockerfile`](/examples/application/job/redis/Dockerfile)
- [`job.yaml`](/examples/application/job/redis/job.yaml)
- [`rediswq.py`](/examples/application/job/redis/rediswq.py)
- [`worker.py`](/examples/application/job/redis/worker.py)

## 使用任务填充队列

现在，让我们往队列里添加一些 “任务”。在这个例子中，我们的任务是一些将被打印出来的字符串。

启动一个临时的可交互的 Pod 用于运行 Redis 命令行界面。

```shell
kubectl run -i --tty temp --image redis --command "/bin/sh"
```

输出类似于：
```
Waiting for pod default/redis2-c7h78 to be running, status is Pending, pod ready: false
Hit enter for command prompt
```

现在按回车键，启动 Redis 命令行界面，然后创建一个存在若干个工作项的列表。

```shell
# redis-cli -h redis
redis:6379> rpush job2 "apple"
(integer) 1
redis:6379> rpush job2 "banana"
(integer) 2
redis:6379> rpush job2 "cherry"
(integer) 3
redis:6379> rpush job2 "date"
(integer) 4
redis:6379> rpush job2 "fig"
(integer) 5
redis:6379> rpush job2 "grape"
(integer) 6
redis:6379> rpush job2 "lemon"
(integer) 7
redis:6379> rpush job2 "melon"
(integer) 8
redis:6379> rpush job2 "orange"
(integer) 9
redis:6379> lrange job2 0 -1
1) "apple"
2) "banana"
3) "cherry"
4) "date"
5) "fig"
6) "grape"
7) "lemon"
8) "melon"
9) "orange"
```

因此，这个键为 `job2` 的列表就是我们的工作队列。

注意：如果你还没有正确地配置 Kube DNS，你可能需要将上面的第一步改为
`redis-cli -h $REDIS_SERVICE_HOST`。

## 创建镜像

现在我们已经准备好创建一个我们要运行的镜像。

我们会使用一个带有 Redis 客户端的 Python 工作程序从消息队列中读出消息。

这里提供了一个简单的 Redis 工作队列客户端库，名为 rediswq.py ([下载](/examples/application/job/redis/rediswq.py))。

Job 中每个 Pod 内的 “工作程序” 使用工作队列客户端库获取工作。具体如下：

{{< codenew language="python" file="application/job/redis/worker.py" >}}

你也可以下载 [`worker.py`](/examples/application/job/redis/worker.py)、
[`rediswq.py`](/examples/application/job/redis/rediswq.py) 和
[`Dockerfile`](/examples/application/job/redis/Dockerfile) 文件。然后构建镜像：

```shell
docker build -t job-wq-2 .
```

### Push 镜像

对于 [Docker Hub](https://hub.docker.com/)，请先用你的用户名给镜像打上标签，
然后使用下面的命令 push 你的镜像到仓库。请将 `<username>` 替换为你自己的 Hub 用户名。

```shell
docker tag job-wq-2 <username>/job-wq-2
docker push <username>/job-wq-2
```

你需要将镜像 push 到一个公共仓库或者
[配置集群访问你的私有仓库](/zh-cn/docs/concepts/containers/images/)。

如果你使用的是 [Google Container Registry](https://cloud.google.com/tools/container-registry/)，
请先用你的 project ID 给你的镜像打上标签，然后 push 到 GCR 。请将 `<project>` 替换为你自己的 project ID。

```shell
docker tag job-wq-2 gcr.io/<project>/job-wq-2
gcloud docker -- push gcr.io/<project>/job-wq-2
```

## 定义一个 Job

这是 Job 定义：

{{< codenew file="application/job/redis/job.yaml" >}}

请确保将 Job 模板中的 `gcr.io/myproject` 更改为你自己的路径。

在这个例子中，每个 Pod 处理了队列中的多个项目，直到队列中没有项目时便退出。
因为是由工作程序自行检测工作队列是否为空，并且 Job 控制器不知道工作队列的存在，
这依赖于工作程序在完成工作时发出信号。
工作程序以成功退出的形式发出信号表示工作队列已经为空。
所以，只要有任意一个工作程序成功退出，控制器就知道工作已经完成了，所有的 Pod 将很快会退出。
因此，我们将 Job 的完成计数（Completion Count）设置为 1。
尽管如此，Job 控制器还是会等待其它 Pod 完成。

## 运行 Job

现在运行这个 Job：

```shell
kubectl apply -f ./job.yaml
```

稍等片刻，然后检查这个 Job。

```shell
kubectl describe jobs/job-wq-2
```

```
Name:             job-wq-2
Namespace:        default
Selector:         controller-uid=b1c7e4e3-92e1-11e7-b85e-fa163ee3c11f
Labels:           controller-uid=b1c7e4e3-92e1-11e7-b85e-fa163ee3c11f
                  job-name=job-wq-2
Annotations:      <none>
Parallelism:      2
Completions:      <unset>
Start Time:       Mon, 11 Jan 2016 17:07:59 -0800
Pods Statuses:    1 Running / 0 Succeeded / 0 Failed
Pod Template:
  Labels:       controller-uid=b1c7e4e3-92e1-11e7-b85e-fa163ee3c11f
                job-name=job-wq-2
  Containers:
   c:
    Image:              gcr.io/exampleproject/job-wq-2
    Port:
    Environment:        <none>
    Mounts:             <none>
  Volumes:              <none>
Events:
  FirstSeen    LastSeen    Count    From            SubobjectPath    Type        Reason            Message
  ---------    --------    -----    ----            -------------    --------    ------            -------
  33s          33s         1        {job-controller }                Normal      SuccessfulCreate  Created pod: job-wq-2-lglf8
```

你可以等待 Job 成功，等待时长有超时限制：

```shell
# 状况名称的检查不区分大小写
kubectl wait --for=condition=complete --timeout=300s job/job-wq-2
```

```shell
kubectl logs pods/job-wq-2-7r7b2
```
```
Worker with sessionID: bbd72d0a-9e5c-4dd6-abf6-416cc267991f
Initial queue state: empty=False
Working on banana
Working on date
Working on lemon
```

你可以看到，其中的一个 Pod 处理了若干个工作单元。


## 替代方案

如果你不方便运行一个队列服务或者修改你的容器用于运行一个工作队列，你可以考虑其它的
[Job 模式](/zh-cn/docs/concepts/workloads/controllers/job/#job-patterns)。

如果你有持续的后台处理业务，那么可以考虑使用 `ReplicaSet` 来运行你的后台业务，
和运行一个类似 [https://github.com/resque/resque](https://github.com/resque/resque)
的后台处理库。
