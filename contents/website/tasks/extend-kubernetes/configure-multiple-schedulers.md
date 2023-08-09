---
title: 配置多个调度器
content_type: task
weight: 20
---


Kubernetes 自带了一个默认调度器，其详细描述请查阅
[这里](/zh-cn/docs/reference/command-line-tools-reference/kube-scheduler/)。
如果默认调度器不适合你的需求，你可以实现自己的调度器。
而且，你甚至可以和默认调度器一起同时运行多个调度器，并告诉 Kubernetes 为每个
Pod 使用哪个调度器。
让我们通过一个例子讲述如何在 Kubernetes 中运行多个调度器。

关于实现调度器的具体细节描述超出了本文范围。
请参考 kube-scheduler 的实现，规范示例代码位于
[pkg/scheduler](https://github.com/kubernetes/kubernetes/tree/master/pkg/scheduler)。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


## 打包调度器

将调度器可执行文件打包到容器镜像中。出于示例目的，可以使用默认调度器
（kube-scheduler）作为第二个调度器。
克隆 [GitHub 上 Kubernetes 源代码](https://github.com/kubernetes/kubernetes)，
并编译构建源代码。

```shell
git clone https://github.com/kubernetes/kubernetes.git
cd kubernetes
make
```

创建一个包含 kube-scheduler 二进制文件的容器镜像。用于构建镜像的 `Dockerfile` 内容如下：

```docker
FROM busybox
ADD ./_output/local/bin/linux/amd64/kube-scheduler /usr/local/bin/kube-scheduler
```

将文件保存为 `Dockerfile`，构建镜像并将其推送到镜像仓库。
此示例将镜像推送到 [Google 容器镜像仓库（GCR）](https://cloud.google.com/container-registry/)。
有关详细信息，请阅读 GCR [文档](https://cloud.google.com/container-registry/docs/)。

```shell
docker build -t gcr.io/my-gcp-project/my-kube-scheduler:1.0 .
gcloud docker -- push gcr.io/my-gcp-project/my-kube-scheduler:1.0
```

## 为调度器定义 Kubernetes Deployment

现在将调度器放在容器镜像中，为它创建一个 Pod 配置，并在 Kubernetes 集群中
运行它。但是与其在集群中直接创建一个 Pod，不如使用
[Deployment](/zh-cn/docs/concepts/workloads/controllers/deployment/)。
Deployment 管理一个 [ReplicaSet](/zh-cn/docs/concepts/workloads/controllers/replicaset/)，
ReplicaSet 再管理 Pod，从而使调度器能够免受一些故障的影响。
以下是 Deployment 配置，将其保存为 `my-scheduler.yaml`：

{{< codenew file="admin/sched/my-scheduler.yaml" >}}

在以上的清单中，你使用 [KubeSchedulerConfiguration](/zh-cn/docs/reference/scheduling/config/) 
来自定义调度器实现的行为。当使用 `--config` 选项进行初始化时，该配置被传递到 `kube-scheduler`。
`my-scheduler-config` ConfigMap 存储配置数据。
`my-scheduler` Deployment 的 Pod 将 `my-scheduler-config` ConfigMap 挂载为一个卷。

在前面提到的调度器配置中，你的调度器通过 [KubeSchedulerProfile](/docs/reference/config-api/kube-scheduler-config.v1beta3/#kubescheduler-config-k8s-io-v1beta3-KubeSchedulerProfile) 进行实现。
{{< note >}}
要确定一个调度器是否可以调度特定的 Pod，PodTemplate 或 Pod 清单中的 `spec.schedulerName` 
字段必须匹配 `KubeSchedulerProfile` 中的 `schedulerName` 字段。
所有运行在集群中的调度器必须拥有唯一的名称。
{{< /note >}}

还要注意，我们创建了一个专用服务账号 `my-scheduler` 并将集群角色 `system:kube-scheduler`
绑定到它，以便它可以获得与 `kube-scheduler` 相同的权限。

请参阅 [kube-scheduler 文档](/docs/reference/command-line-tools-reference/kube-scheduler/)
获取其他命令行参数以及 [Scheduler 配置参考](/docs/reference/config-api/kube-scheduler-config.v1beta3/)
获取自定义 `kube-scheduler` 配置的详细说明。

## 在集群中运行第二个调度器

为了在 Kubernetes 集群中运行我们的第二个调度器，在 Kubernetes 集群中创建上面配置中指定的 Deployment：

```shell
kubectl create -f my-scheduler.yaml
```

验证调度器 Pod 正在运行：

```shell
kubectl get pods --namespace=kube-system
```

输出类似于：

```
NAME                                           READY     STATUS    RESTARTS   AGE
....
my-scheduler-lnf4s-4744f                       1/1       Running   0          2m
...
```

此列表中，除了默认的 `kube-scheduler` Pod 之外，你应该还能看到处于 “Running” 状态的
`my-scheduler` Pod。


### 启用领导者选举

要在启用了 leader 选举的情况下运行多调度器，你必须执行以下操作：

更新你的 YAML 文件中的 `my-scheduler-config` ConfigMap 里的 KubeSchedulerConfiguration 相关字段如下：

* `leaderElection.leaderElect` to `true`
* `leaderElection.resourceNamespace` to `<lock-object-namespace>`
* `leaderElection.resourceName` to `<lock-object-name>`

{{< note >}}
控制平面会为你创建锁对象，但是命名空间必须已经存在。
你可以使用 `kube-system` 命名空间。
{{< /note >}}

如果在集群上启用了 RBAC，则必须更新 `system：kube-scheduler` 集群角色。
将调度器名称添加到应用了 `endpoints` 和 `leases` 资源的规则的 resourceNames 中，如以下示例所示：

```shell
kubectl edit clusterrole system:kube-scheduler
```

{{< codenew file="admin/sched/clusterrole.yaml" >}}

## 为 Pod 指定调度器

现在第二个调度器正在运行，创建一些 Pod，并指定它们由默认调度器或部署的调度器进行调度。
为了使用特定的调度器调度给定的 Pod，在那个 Pod 的 spec 中指定调度器的名称。让我们看看三个例子。

- Pod spec 没有任何调度器名称

  {{< codenew file="admin/sched/pod1.yaml" >}}

  如果未提供调度器名称，则会使用 default-scheduler 自动调度 pod。

  将此文件另存为 `pod1.yaml`，并将其提交给 Kubernetes 集群。

  ```shell
  kubectl create -f pod1.yaml
  ```

- Pod spec 设置为 `default-scheduler`

  {{< codenew file="admin/sched/pod2.yaml" >}}

  通过将调度器名称作为 `spec.schedulerName` 参数的值来指定调度器。
  在这种情况下，我们提供默认调度器的名称，即 `default-scheduler`。

  将此文件另存为 `pod2.yaml`，并将其提交给 Kubernetes 集群。

  ```shell
  kubectl create -f pod2.yaml
  ```

- Pod spec 设置为 `my-scheduler`

  {{< codenew file="admin/sched/pod3.yaml" >}}

  在这种情况下，我们指定此 Pod 使用我们部署的 `my-scheduler` 来调度。
  请注意，`spec.schedulerName` 参数的值应该与调度器提供的 `KubeSchedulerProfile` 中的 `schedulerName` 字段相匹配。

  将此文件另存为 `pod3.yaml`，并将其提交给 Kubernetes 集群。

  ```shell
  kubectl create -f pod3.yaml
  ```

  确认所有三个 pod 都在运行。

  ```shell
  kubectl get pods
  ```


### 验证是否使用所需的调度器调度了 pod

为了更容易地完成这些示例，我们没有验证 Pod 实际上是使用所需的调度程序调度的。
我们可以通过更改 Pod 的顺序和上面的部署配置提交来验证这一点。
如果我们在提交调度器部署配置之前将所有 Pod 配置提交给 Kubernetes 集群，
我们将看到注解了 `annotation-second-scheduler` 的 Pod 始终处于 “Pending” 状态，
而其他两个 Pod 被调度。
一旦我们提交调度器部署配置并且我们的新调度器开始运行，注解了
`annotation-second-scheduler` 的 pod 就能被调度。
或者，可以查看事件日志中的 “Scheduled” 条目，以验证是否由所需的调度器调度了 Pod。

```shell
kubectl get events
```

你也可以使用[自定义调度器配置](/zh-cn/docs/reference/scheduling/config/#multiple-profiles)
或自定义容器镜像，用于集群的主调度器，方法是在相关控制平面节点上修改其静态 pod 清单。

