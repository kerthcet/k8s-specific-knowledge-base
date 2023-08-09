---
title: 使用 CronJob 运行自动化任务
min-kubernetes-server-version: v1.21
content_type: task
weight: 10
---


本页演示如何使用 Kubernetes {{< glossary_tooltip text="CronJob" term_id="cronjob" >}}
对象运行自动化任务。

## {{% heading "prerequisites" %}}

* {{< include "task-tutorial-prereqs.md" >}}


## 创建 CronJob {#creating-a-cron-job}

CronJob 需要一个配置文件。
以下是针对一个 CronJob 的清单，该 CronJob 每分钟运行一个简单的演示任务：

{{< codenew file="application/job/cronjob.yaml" >}}

执行以下命令以运行此 CronJob 示例：

```shell
kubectl create -f https://k8s.io/examples/application/job/cronjob.yaml
```

输出类似于：

```
cronjob.batch/hello created
```

创建好 CronJob 后，使用下面的命令来获取其状态：

```shell
kubectl get cronjob hello
```

输出类似于：

```
NAME    SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
hello   */1 * * * *   False     0        <none>          10s
```
就像你从命令返回结果看到的那样，CronJob 还没有调度或执行任何任务。大约需要一分钟任务才能创建好。

```shell
kubectl get jobs --watch
```

输出类似于：

```
NAME               COMPLETIONS   DURATION   AGE
hello-4111706356   0/1                      0s
hello-4111706356   0/1           0s         0s
hello-4111706356   1/1           5s         5s
```

现在你已经看到了一个运行中的任务被 “hello” CronJob 调度。
你可以停止监视这个任务，然后再次查看 CronJob 就能看到它调度任务：

```shell
kubectl get cronjob hello
```

输出类似于：

```
NAME    SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
hello   */1 * * * *   False     0        50s             75s
```

你应该能看到 `hello` CronJob 在 `LAST SCHEDULE` 声明的时间点成功地调度了一次任务。
目前有 0 个活跃的任务，这意味着任务执行完毕或者执行失败。

现在，找到最后一次调度任务创建的 Pod 并查看一个 Pod 的标准输出。

{{< note >}}
Job 名称与 Pod 名称不同。
{{< /note >}}

```shell
# 在你的系统上将 "hello-4111706356" 替换为 Job 名称
pods=$(kubectl get pods --selector=job-name=hello-4111706356 --output=jsonpath={.items..metadata.name})
```

查看 Pod 日志：

```shell
kubectl logs $pods
```
输出类似于：

```
Fri Feb 22 11:02:09 UTC 2019
Hello from the Kubernetes cluster
```


## 删除 CronJob {#deleting-a-cronjob}

当你不再需要 CronJob 时，可以用 `kubectl delete cronjob <cronjob name>` 删掉它：

```shell
kubectl delete cronjob hello
```

删除 CronJob 会清除它创建的所有任务和 Pod，并阻止它创建额外的任务。
你可以查阅[垃圾收集](/zh-cn/docs/concepts/architecture/garbage-collection/)。
