---
title: 通过名字空间共享集群
content_type: task
weight: 340
---

本页展示如何查看、使用和删除{{< glossary_tooltip text="名字空间" term_id="namespace" >}}。
本页同时展示如何使用 Kubernetes 名字空间来划分集群。

## {{% heading "prerequisites" %}}

* 你已拥有一个[配置好的 Kubernetes 集群](/zh-cn/docs/setup/)。
* 你已对 Kubernetes 的 {{< glossary_tooltip text="Pod" term_id="pod" >}}、
  {{< glossary_tooltip term_id="service" text="Service" >}} 和
  {{< glossary_tooltip text="Deployment" term_id="deployment" >}} 有基本理解。


## 查看名字空间

列出集群中现有的名字空间：

```shell
kubectl get namespaces
```
```console
NAME          STATUS    AGE
default       Active    11d
kube-system   Active    11d
kube-public   Active    11d
```

初始状态下，Kubernetes 具有三个名字空间：

* `default` 无名字空间对象的默认名字空间
* `kube-system` 由 Kubernetes 系统创建的对象的名字空间
* `kube-public` 自动创建且被所有用户可读的名字空间（包括未经身份认证的）。
  此名字空间通常在某些资源在整个集群中可见且可公开读取时被集群使用。
  此名字空间的公共方面只是一个约定，而不是一个必要条件。

你还可以通过下列命令获取特定名字空间的摘要：

```shell
kubectl get namespaces <name>
```

或用下面的命令获取详细信息：

```shell
kubectl describe namespaces <name>
```

```console
Name:           default
Labels:         <none>
Annotations:    <none>
Status:         Active

No resource quota.

Resource Limits
 Type       Resource    Min Max Default
 ----               --------    --- --- ---
 Container          cpu         -   -   100m
```

请注意，这些详情同时显示了资源配额（如果存在）以及资源限制区间。

资源配额跟踪并聚合 **Namespace** 中资源的使用情况，
并允许集群运营者定义 **Namespace** 可能消耗的 **Hard** 资源使用限制。

限制区间定义了单个实体在一个 **Namespace** 中可使用的最小/最大资源量约束。

参阅[准入控制：限制区间](https://git.k8s.io/design-proposals-archive/resource-management/admission_control_limit_range.md)。

名字空间可以处于下列两个阶段中的一个:

* `Active` 名字空间正在被使用中
* `Terminating` 名字空间正在被删除，且不能被用于新对象。

更多细节，参阅 API
参考中的[名字空间](/zh-cn/docs/reference/kubernetes-api/cluster-resources/namespace-v1/)。

## 创建名字空间

{{< note >}}
避免使用前缀 `kube-` 创建名字空间，因为它是为 Kubernetes 系统名字空间保留的。
{{< /note >}}

新建一个名为 `my-namespace.yaml` 的 YAML 文件，并写入下列内容：

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: <insert-namespace-name-here>
```

然后运行：

```shell
kubectl create -f ./my-namespace.yaml
```

或者，你可以使用下面的命令创建名字空间：

```shell
kubectl create namespace <insert-namespace-name-here>
```

请注意，名字空间的名称必须是一个合法的
[DNS 标签](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-label-names)。

可选字段 `finalizers` 允许观察者们在名字空间被删除时清除资源。
记住如果指定了一个不存在的终结器，名字空间仍会被创建，
但如果用户试图删除它，它将陷入 `Terminating` 状态。

更多有关 `finalizers` 的信息请查阅
[设计文档](https://git.k8s.io/design-proposals-archive/architecture/namespaces.md#finalizers)中名字空间部分。

## 删除名字空间

删除名字空间使用命令：

```shell
kubectl delete namespaces <insert-some-namespace-name>
```

{{< warning >}}
这会删除名字空间下的 **所有内容** ！
{{< /warning >}}

删除是异步的，所以有一段时间你会看到名字空间处于 `Terminating` 状态。

## 使用 Kubernetes 名字空间细分你的集群

默认情况下，Kubernetes 集群会在配置集群时实例化一个 default 名字空间，用以存放集群所使用的默认
Pod、Service 和 Deployment 集合。

假设你有一个新的集群，你可以通过执行以下操作来内省可用的名字空间：

```shell
kubectl get namespaces
```

```console
NAME      STATUS    AGE
default   Active    13m
```

### 创建新的名字空间

在本练习中，我们将创建两个额外的 Kubernetes 名字空间来保存我们的内容。

在某组织使用共享的 Kubernetes 集群进行开发和生产的场景中：

- 开发团队希望在集群中维护一个空间，以便他们可以查看用于构建和运行其应用程序的 Pod、Service
  和 Deployment 列表。在这个空间里，Kubernetes 资源被自由地加入或移除，
  对谁能够或不能修改资源的限制被放宽，以实现敏捷开发。
   
- 运维团队希望在集群中维护一个空间，以便他们可以强制实施一些严格的规程，
  对谁可以或不可以操作运行生产站点的 Pod、Service 和 Deployment 集合进行控制。
   
该组织可以遵循的一种模式是将 Kubernetes 集群划分为两个名字空间：`development` 和 `production`。
让我们创建两个新的名字空间来保存我们的工作。

使用 kubectl 创建 `development` 名字空间。

```shell
kubectl create -f https://k8s.io/examples/admin/namespace-dev.json
```

让我们使用 kubectl 创建 `production` 名字空间。

```shell
kubectl create -f https://k8s.io/examples/admin/namespace-prod.json
```

为了确保一切正常，列出集群中的所有名字空间。

```shell
kubectl get namespaces --show-labels
```

```console
NAME          STATUS    AGE       LABELS
default       Active    32m       <none>
development   Active    29s       name=development
production    Active    23s       name=production
```

### 在每个名字空间中创建 Pod

Kubernetes 名字空间为集群中的 Pod、Service 和 Deployment 提供了作用域。
与一个名字空间交互的用户不会看到另一个名字空间中的内容。
为了演示这一点，让我们在 `development` 名字空间中启动一个简单的 Deployment 和 Pod。

```shell
kubectl create deployment snowflake \
  --image=registry.k8s.io/serve_hostname \
  -n=development --replicas=2
```

我们创建了一个副本个数为 2 的 Deployment，运行名为 `snowflake` 的
Pod，其中包含一个负责提供主机名的基本容器。

```shell
kubectl get deployment -n=development
```
```console
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
snowflake    2/2     2            2           2m
```

```shell
kubectl get pods -l app=snowflake -n=development
```
```console
NAME                         READY     STATUS    RESTARTS   AGE
snowflake-3968820950-9dgr8   1/1       Running   0          2m
snowflake-3968820950-vgc4n   1/1       Running   0          2m
```

看起来还不错，开发人员能够做他们想做的事，而且他们不必担心会影响到
`production` 名字空间下面的内容。

让我们切换到 `production` 名字空间，
展示一下一个名字空间中的资源是如何对另一个名字空间隐藏的。
名字空间 `production` 应该是空的，下面的命令应该不会返回任何东西。

```shell
kubectl get deployment -n=production
kubectl get pods -n=production
```

生产环境下一般以养牛的方式运行负载，所以让我们创建一些 Cattle（牛）Pod。

```shell
kubectl create deployment cattle --image=registry.k8s.io/serve_hostname -n=production
kubectl scale deployment cattle --replicas=5 -n=production

kubectl get deployment -n=production
```

```console
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
cattle       5/5     5            5           10s
```

```shell
kubectl get pods -l app=cattle -n=production
```
```console
NAME                      READY     STATUS    RESTARTS   AGE
cattle-2263376956-41xy6   1/1       Running   0          34s
cattle-2263376956-kw466   1/1       Running   0          34s
cattle-2263376956-n4v97   1/1       Running   0          34s
cattle-2263376956-p5p3i   1/1       Running   0          34s
cattle-2263376956-sxpth   1/1       Running   0          34s
```

此时，应该很清楚地展示了用户在一个名字空间中创建的资源对另一个名字空间是隐藏的。

随着 Kubernetes 中的策略支持的发展，我们将扩展此场景，以展示如何为每个名字空间提供不同的授权规则。


## 理解使用名字空间的动机

单个集群应该能满足多个用户及用户组的需求（以下称为 “用户社区”）。

Kubernetes **名字空间** 帮助不同的项目、团队或客户去共享 Kubernetes 集群。

名字空间通过以下方式实现这点：

1. 为[名字](/zh-cn/docs/concepts/overview/working-with-objects/names/)设置作用域.
2. 为集群中的部分资源关联鉴权和策略的机制。

使用多个名字空间是可选的。

每个用户社区都希望能够与其他社区隔离开展工作。
每个用户社区都有自己的：

1. 资源（Pod、服务、副本控制器等等）
2. 策略（谁能或不能在他们的社区里执行操作）
3. 约束（该社区允许多少配额等等）

集群运营者可以为每个唯一用户社区创建名字空间。

名字空间为下列内容提供唯一的作用域：

1. 命名资源（避免基本的命名冲突）
2. 将管理权限委派给可信用户
3. 限制社区资源消耗的能力

用例包括:

1. 作为集群运营者, 我希望能在单个集群上支持多个用户社区。
2. 作为集群运营者，我希望将集群分区的权限委派给这些社区中的受信任用户。
3. 作为集群运营者，我希望能限定每个用户社区可使用的资源量，以限制对使用同一集群的其他用户社区的影响。
4. 作为集群用户，我希望与我的用户社区相关的资源进行交互，而与其他用户社区在该集群上执行的操作无关。

## 理解名字空间和 DNS

当你创建[服务](/zh-cn/docs/concepts/services-networking/service/)时，Kubernetes
会创建相应的 [DNS 条目](/zh-cn/docs/concepts/services-networking/dns-pod-service/)。
此条目的格式为 `<服务名称>.<名字空间名称>.svc.cluster.local`。
这意味着如果容器使用 `<服务名称>`，它将解析为名字空间本地的服务。
这对于在多个名字空间（如开发、暂存和生产）中使用相同的配置非常有用。
如果要跨名字空间访问，则需要使用完全限定的域名（FQDN）。

## {{% heading "whatsnext" %}}

* 进一步了解[设置名字空间偏好](/zh-cn/docs/concepts/overview/working-with-objects/namespaces/#setting-the-namespace-preference)
* 进一步了解[设置请求的名字空间](/zh-cn/docs/concepts/overview/working-with-objects/namespaces/#setting-the-namespace-for-a-request)
* 参阅[名字空间的设计文档](https://git.k8s.io/design-proposals-archive/architecture/namespaces.md)
