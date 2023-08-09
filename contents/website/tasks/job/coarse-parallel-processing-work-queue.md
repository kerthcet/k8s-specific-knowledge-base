---
title: 使用工作队列进行粗粒度并行处理
min-kubernetes-server-version: v1.8
content_type: task
weight: 20
---



本例中，我们会运行包含多个并行工作进程的 Kubernetes Job。

本例中，每个 Pod 一旦被创建，会立即从任务队列中取走一个工作单元并完成它，然后将工作单元从队列中删除后再退出。

下面是本次示例的主要步骤：

1. **启动一个消息队列服务**。
   本例中，我们使用 RabbitMQ，你也可以用其他的消息队列服务。
   在实际工作环境中，你可以创建一次消息队列服务然后在多个任务中重复使用。

1. **创建一个队列，放上消息数据**。
   每个消息表示一个要执行的任务。本例中，每个消息是一个整数值。
   我们将基于这个整数值执行很长的计算操作。

1. **启动一个在队列中执行这些任务的 Job**。
   该 Job 启动多个 Pod。每个 Pod 从消息队列中取走一个任务，处理任务，然后退出。

## {{% heading "prerequisites" %}}



要熟悉 Job 基本用法（非并行的），请参考
[Job](/zh-cn/docs/concepts/workloads/controllers/job/)。

{{< include "task-tutorial-prereqs.md" >}} 


## 启动消息队列服务   {#starting-a-message-queue-service}

本例使用了 RabbitMQ，但你可以更改该示例，使用其他 AMQP 类型的消息服务。

在实际工作中，在集群中一次性部署某个消息队列服务，之后在很多 Job 中复用，包括需要长期运行的服务。

按下面的方法启动 RabbitMQ：

```shell
kubectl create -f https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.3/examples/celery-rabbitmq/rabbitmq-service.yaml
```
```
service "rabbitmq-service" created
```

```shell
kubectl create -f https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.3/examples/celery-rabbitmq/rabbitmq-controller.yaml
```

```
replicationcontroller "rabbitmq-controller" created
```

我们仅用到
[celery-rabbitmq 示例](https://github.com/kubernetes/kubernetes/tree/release-1.3/examples/celery-rabbitmq)中描述的部分功能。

## 测试消息队列服务   {#testing-the-message-queue-service}

现在，我们可以试着访问消息队列。我们将会创建一个临时的可交互的 Pod，
在它上面安装一些工具，然后用队列做实验。

首先创建一个临时的可交互的 Pod：

```shell
# 创建一个临时的可交互的 Pod
kubectl run -i --tty temp --image ubuntu:18.04
```
```
Waiting for pod default/temp-loe07 to be running, status is Pending, pod ready: false
... [ previous line repeats several times .. hit return when it stops ] ...
```

请注意你的 Pod 名称和命令提示符将会不同。

接下来安装 `amqp-tools`，这样我们就能用消息队列了。

```shell
# 安装一些工具
root@temp-loe07:/# apt-get update
.... [ lots of output ] ....
root@temp-loe07:/# apt-get install -y curl ca-certificates amqp-tools python dnsutils
.... [ lots of output ] ....
```

后续，我们将制作一个包含这些包的 Docker 镜像。

接着，我们将要验证可以发现 RabbitMQ 服务：

```
# 请注意 rabbitmq-service 拥有一个由 Kubernetes 提供的 DNS 名称：

root@temp-loe07:/# nslookup rabbitmq-service
Server:        10.0.0.10
Address:    10.0.0.10#53

Name:    rabbitmq-service.default.svc.cluster.local
Address: 10.0.147.152

# 你的 IP 地址会不同
```

如果 Kube-DNS 没有正确安装，上一步可能会出错。
你也可以在环境变量中找到服务 IP。

```
# env | grep RABBIT | grep HOST
RABBITMQ_SERVICE_SERVICE_HOST=10.0.147.152

# 你的 IP 地址会有所不同
```

接着我们将要确认可以创建队列，并能发布消息和消费消息。


```shell
# 下一行，rabbitmq-service 是访问 rabbitmq-service 的主机名。5672是 rabbitmq 的标准端口。

root@temp-loe07:/# export BROKER_URL=amqp://guest:guest@rabbitmq-service:5672

# 如果上一步中你不能解析 "rabbitmq-service"，可以用下面的命令替换：
# root@temp-loe07:/# BROKER_URL=amqp://guest:guest@$RABBITMQ_SERVICE_SERVICE_HOST:5672

# 现在创建队列：

root@temp-loe07:/# /usr/bin/amqp-declare-queue --url=$BROKER_URL -q foo -d foo

# 向它推送一条消息:

root@temp-loe07:/# /usr/bin/amqp-publish --url=$BROKER_URL -r foo -p -b Hello

# 然后取回它.

root@temp-loe07:/# /usr/bin/amqp-consume --url=$BROKER_URL -q foo -c 1 cat && echo
Hello
root@temp-loe07:/#
```


最后一个命令中，`amqp-consume` 工具从队列中取走了一个消息，并把该消息传递给了随机命令的标准输出。
在这种情况下，`cat` 会打印它从标准输入中读取的字符，echo 会添加回车符以便示例可读。

## 为队列增加任务  {#filling-the-queue-with-tasks}

现在让我们给队列增加一些任务。在我们的示例中，任务是多个待打印的字符串。

实践中，消息的内容可以是：

- 待处理的文件名
- 程序额外的参数
- 数据库表的关键字范围
- 模拟任务的配置参数
- 待渲染的场景的帧序列号


本例中，如果有大量的数据需要被 Job 的所有 Pod 读取，典型的做法是把它们放在一个共享文件系统中，
如 NFS（Network File System 网络文件系统），并以只读的方式挂载到所有 Pod，或者 Pod 中的程序从类似 HDFS
（Hadoop Distributed File System 分布式文件系统）的集群文件系统中读取。

例如，我们创建队列并使用 amqp 命令行工具向队列中填充消息。实践中，你可以写个程序来利用 amqp 客户端库来填充这些队列。

```shell
/usr/bin/amqp-declare-queue --url=$BROKER_URL -q job1  -d job1
for f in apple banana cherry date fig grape lemon melon
do
  /usr/bin/amqp-publish --url=$BROKER_URL -r job1 -p -b $f
done
```

这样，我们给队列中填充了 8 个消息。

## 创建镜像   {#create-an-image}

现在我们可以创建一个做为 Job 来运行的镜像。

我们将用 `amqp-consume` 实用程序从队列中读取消息并运行实际的程序。
这里给出一个非常简单的示例程序：

{{< codenew language="python" file="application/job/rabbitmq/worker.py" >}}

赋予脚本执行权限:

```shell
chmod +x worker.py
```



现在，编译镜像。如果你在用源代码树，那么切换到目录 `examples/job/work-queue-1`。
否则的话，创建一个临时目录，切换到这个目录。下载
[Dockerfile](/examples/application/job/rabbitmq/Dockerfile) 和
[worker.py](/examples/application/job/rabbitmq/worker.py)。
无论哪种情况，都可以用下面的命令编译镜像：

```shell
docker build -t job-wq-1 .
```

对于 [Docker Hub](https://hub.docker.com/), 给你的应用镜像打上标签，
标签为你的用户名，然后用下面的命令推送到 Hub。用你的 Hub 用户名替换 `<username>`。 

```shell
docker tag job-wq-1 <username>/job-wq-1
docker push <username>/job-wq-1
```

如果你在用[谷歌容器仓库](https://cloud.google.com/tools/container-registry/)，
用你的项目 ID 作为标签打到你的应用镜像上，然后推送到 GCR。
用你的项目 ID 替换 `<project>`。

```shell
docker tag job-wq-1 gcr.io/<project>/job-wq-1
gcloud docker -- push gcr.io/<project>/job-wq-1
```

## 定义 Job   {#defining-a-job}

这里给出一个 Job 定义 YAML 文件。你将需要拷贝一份 Job 并编辑该镜像以匹配你使用的名称，保存为 `./job.yaml`。

{{< codenew file="application/job/rabbitmq/job.yaml" >}}

本例中，每个 Pod 使用队列中的一个消息然后退出。
这样，Job 的完成计数就代表了完成的工作项的数量。
本例中我们设置 `.spec.completions: 8`，因为我们放了 8 项内容在队列中。

## 运行 Job   {#running-the-job}

现在我们运行 Job：

```shell
kubectl apply -f ./job.yaml
```

你可以等待 Job 在某个超时时间后成功：

```shell
# 状况名称的检查不区分大小写
kubectl wait --for=condition=complete --timeout=300s job/job-wq-1
```

接下来查看 Job：

```shell
kubectl describe jobs/job-wq-1
```
```
Name:             job-wq-1
Namespace:        default
Selector:         controller-uid=41d75705-92df-11e7-b85e-fa163ee3c11f
Labels:           controller-uid=41d75705-92df-11e7-b85e-fa163ee3c11f
                  job-name=job-wq-1
Annotations:      <none>
Parallelism:      2
Completions:      8
Start Time:       Wed, 06 Sep 2017 16:42:02 +0800
Pods Statuses:    0 Running / 8 Succeeded / 0 Failed
Pod Template:
  Labels:       controller-uid=41d75705-92df-11e7-b85e-fa163ee3c11f
                job-name=job-wq-1
  Containers:
   c:
    Image:      gcr.io/causal-jigsaw-637/job-wq-1
    Port:
    Environment:
      BROKER_URL:       amqp://guest:guest@rabbitmq-service:5672
      QUEUE:            job1
    Mounts:             <none>
  Volumes:              <none>
Events:
  FirstSeen  LastSeen   Count    From    SubobjectPath    Type      Reason              Message
  ─────────  ────────   ─────    ────    ─────────────    ──────    ──────              ───────
  27s        27s        1        {job }                   Normal    SuccessfulCreate    Created pod: job-wq-1-hcobb
  27s        27s        1        {job }                   Normal    SuccessfulCreate    Created pod: job-wq-1-weytj
  27s        27s        1        {job }                   Normal    SuccessfulCreate    Created pod: job-wq-1-qaam5
  27s        27s        1        {job }                   Normal    SuccessfulCreate    Created pod: job-wq-1-b67sr
  26s        26s        1        {job }                   Normal    SuccessfulCreate    Created pod: job-wq-1-xe5hj
  15s        15s        1        {job }                   Normal    SuccessfulCreate    Created pod: job-wq-1-w2zqe
  14s        14s        1        {job }                   Normal    SuccessfulCreate    Created pod: job-wq-1-d6ppa
  14s        14s        1        {job }                   Normal    SuccessfulCreate    Created pod: job-wq-1-p17e0
```

该 Job 的所有 Pod 都已成功。耶！


## 替代方案   {#alternatives}

本文所讲述的处理方法的好处是你不需要修改你的 "worker" 程序使其知道工作队列的存在。

本文所描述的方法需要你运行一个消息队列服务。如果不方便运行消息队列服务，
你也许会考虑另外一种[任务模式](/zh-cn/docs/concepts/workloads/controllers/job/#job-patterns)。

本文所述的方法为每个工作项创建了一个 Pod。
如果你的工作项仅需数秒钟，为每个工作项创建 Pod 会增加很多的常规消耗。
可以考虑另外的方案请参考[示例](/zh-cn/docs/tasks/job/fine-parallel-processing-work-queue/)，
这种方案可以实现每个 Pod 执行多个工作项。

示例中，我们使用 `amqp-consume` 从消息队列读取消息并执行我们真正的程序。
这样的好处是你不需要修改你的程序使其知道队列的存在。
要了解怎样使用客户端库和工作队列通信，
请参考[不同的示例](/zh-cn/docs/tasks/job/fine-parallel-processing-work-queue/)。

## 友情提醒   {#caveats}

如果设置的完成数量小于队列中的消息数量，会导致一部分消息项不会被执行。

如果设置的完成数量大于队列中的消息数量，当队列中所有的消息都处理完成后，
Job 也会显示为未完成。Job 将创建 Pod 并阻塞等待消息输入。

当发生下面两种情况时，即使队列中所有的消息都处理完了，Job 也不会显示为完成状态：
* 在 amqp-consume 命令拿到消息和容器成功退出之间的时间段内，执行杀死容器操作；
* 在 kubelet 向 api-server 传回 Pod 成功运行之前，发生节点崩溃。

