---
title: ReplicaSet
feature:
  title: 自我修复
  anchor: ReplicationController 如何工作
  description: >
    重新启动失败的容器，在节点死亡时替换并重新调度容器，
    杀死不响应用户定义的健康检查的容器，
    并且在它们准备好服务之前不会将它们公布给客户端。
content_type: concept
weight: 20
---



ReplicaSet 的目的是维护一组在任何时候都处于运行状态的 Pod 副本的稳定集合。
因此，它通常用来保证给定数量的、完全相同的 Pod 的可用性。

## ReplicaSet 的工作原理 {#how-a-replicaset-works}

ReplicaSet 是通过一组字段来定义的，包括一个用来识别可获得的 Pod
的集合的选择算符、一个用来标明应该维护的副本个数的数值、一个用来指定应该创建新 Pod
以满足副本个数条件时要使用的 Pod 模板等等。
每个 ReplicaSet 都通过根据需要创建和删除 Pod 以使得副本个数达到期望值，
进而实现其存在价值。当 ReplicaSet 需要创建新的 Pod 时，会使用所提供的 Pod 模板。

ReplicaSet 通过 Pod 上的
[metadata.ownerReferences](/zh-cn/docs/concepts/architecture/garbage-collection/#owners-and-dependents)
字段连接到附属 Pod，该字段给出当前对象的属主资源。
ReplicaSet 所获得的 Pod 都在其 ownerReferences 字段中包含了属主 ReplicaSet
的标识信息。正是通过这一连接，ReplicaSet 知道它所维护的 Pod 集合的状态，
并据此计划其操作行为。

ReplicaSet 使用其选择算符来辨识要获得的 Pod 集合。如果某个 Pod 没有
OwnerReference 或者其 OwnerReference 不是一个{{< glossary_tooltip text="控制器" term_id="controller" >}}，
且其匹配到某 ReplicaSet 的选择算符，则该 Pod 立即被此 ReplicaSet 获得。

## 何时使用 ReplicaSet    {#when-to-use-a-replicaset}

ReplicaSet 确保任何时间都有指定数量的 Pod 副本在运行。
然而，Deployment 是一个更高级的概念，它管理 ReplicaSet，并向 Pod
提供声明式的更新以及许多其他有用的功能。
因此，我们建议使用 Deployment 而不是直接使用 ReplicaSet，
除非你需要自定义更新业务流程或根本不需要更新。

这实际上意味着，你可能永远不需要操作 ReplicaSet 对象：而是使用
Deployment，并在 spec 部分定义你的应用。

## 示例    {#example}

{{< codenew file="controllers/frontend.yaml" >}}

将此清单保存到 `frontend.yaml` 中，并将其提交到 Kubernetes 集群，
就能创建 yaml 文件所定义的 ReplicaSet 及其管理的 Pod。

```shell
kubectl apply -f https://kubernetes.io/examples/controllers/frontend.yaml
```

你可以看到当前被部署的 ReplicaSet：

```shell
kubectl get rs
```

并看到你所创建的前端：

```
NAME       DESIRED   CURRENT   READY   AGE
frontend   3         3         3       6s
```

你也可以查看 ReplicaSet 的状态：

```shell
kubectl describe rs/frontend
```

你会看到类似如下的输出：

```
Name:         frontend
Namespace:    default
Selector:     tier=frontend
Labels:       app=guestbook
              tier=frontend
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"apps/v1","kind":"ReplicaSet","metadata":{"annotations":{},"labels":{"app":"guestbook","tier":"frontend"},"name":"frontend",...
Replicas:     3 current / 3 desired
Pods Status:  3 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  tier=frontend
  Containers:
   php-redis:
    Image:        gcr.io/google_samples/gb-frontend:v3
    Port:         <none>
    Host Port:    <none>
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age   From                   Message
  ----    ------            ----  ----                   -------
  Normal  SuccessfulCreate  117s  replicaset-controller  Created pod: frontend-wtsmm
  Normal  SuccessfulCreate  116s  replicaset-controller  Created pod: frontend-b2zdv
  Normal  SuccessfulCreate  116s  replicaset-controller  Created pod: frontend-vcmts
```

最后可以查看启动了的 Pod 集合：

```shell
kubectl get pods
```

你会看到类似如下的 Pod 信息：

```
NAME             READY   STATUS    RESTARTS   AGE
frontend-b2zdv   1/1     Running   0          6m36s
frontend-vcmts   1/1     Running   0          6m36s
frontend-wtsmm   1/1     Running   0          6m36s
```

你也可以查看 Pod 的属主引用被设置为前端的 ReplicaSet。
要实现这点，可取回运行中的某个 Pod 的 YAML：

```shell
kubectl get pods frontend-b2zdv -o yaml
```

输出将类似这样，frontend ReplicaSet 的信息被设置在 metadata 的
`ownerReferences` 字段中：

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2020-02-12T07:06:16Z"
  generateName: frontend-
  labels:
    tier: frontend
  name: frontend-b2zdv
  namespace: default
  ownerReferences:
  - apiVersion: apps/v1
    blockOwnerDeletion: true
    controller: true
    kind: ReplicaSet
    name: frontend
    uid: f391f6db-bb9b-4c09-ae74-6a1f77f3d5cf
...
```

## 非模板 Pod 的获得    {#non-template-pod-acquisitions}

尽管你完全可以直接创建裸的 Pod，强烈建议你确保这些裸的 Pod 并不包含可能与你的某个
ReplicaSet 的选择算符相匹配的标签。原因在于 ReplicaSet 并不仅限于拥有在其模板中设置的
Pod，它还可以像前面小节中所描述的那样获得其他 Pod。

以前面的 frontend ReplicaSet 为例，并在以下清单中指定这些 Pod：

{{< codenew file="pods/pod-rs.yaml" >}}

由于这些 Pod 没有控制器（Controller，或其他对象）作为其属主引用，
并且其标签与 frontend ReplicaSet 的选择算符匹配，它们会立即被该 ReplicaSet 获取。

假定你在 frontend ReplicaSet 已经被部署之后创建 Pod，并且你已经在 ReplicaSet
中设置了其初始的 Pod 副本数以满足其副本计数需要：

```shell
kubectl apply -f https://kubernetes.io/examples/pods/pod-rs.yaml
```

新的 Pod 会被该 ReplicaSet 获取，并立即被 ReplicaSet 终止，
因为它们的存在会使得 ReplicaSet 中 Pod 个数超出其期望值。

取回 Pod：


```shell
kubectl get pods
```

输出显示新的 Pod 或者已经被终止，或者处于终止过程中：

```
NAME             READY   STATUS        RESTARTS   AGE
frontend-b2zdv   1/1     Running       0          10m
frontend-vcmts   1/1     Running       0          10m
frontend-wtsmm   1/1     Running       0          10m
pod1             0/1     Terminating   0          1s
pod2             0/1     Terminating   0          1s
```

如果你先行创建 Pod：

```shell
kubectl apply -f https://kubernetes.io/examples/pods/pod-rs.yaml
```

之后再创建 ReplicaSet：

```shell
kubectl apply -f https://kubernetes.io/examples/controllers/frontend.yaml
```

你会看到 ReplicaSet 已经获得了该 Pod，并仅根据其规约创建新的 Pod，
直到新的 Pod 和原来的 Pod 的总数达到其预期个数。
这时取回 Pod 列表：

```shell
kubectl get pods
```

将会生成下面的输出：

```
NAME             READY   STATUS    RESTARTS   AGE
frontend-hmmj2   1/1     Running   0          9s
pod1             1/1     Running   0          36s
pod2             1/1     Running   0          36s
```

采用这种方式，一个 ReplicaSet 中可以包含异质的 Pod 集合。

## 编写 ReplicaSet 的清单    {#writing-a-replicaset-manifest}

与所有其他 Kubernetes API 对象一样，ReplicaSet 也需要 `apiVersion`、`kind`、和 `metadata` 字段。
对于 ReplicaSet 而言，其 `kind` 始终是 ReplicaSet。

当控制平面为 ReplicaSet 创建新的 Pod 时，ReplicaSet
的 `.metadata.name` 是命名这些 Pod 的部分基础。ReplicaSet 的名称必须是一个合法的
[DNS 子域](/zh-cn/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names)值，
但这可能对 Pod 的主机名产生意外的结果。为获得最佳兼容性，名称应遵循更严格的
[DNS 标签](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-label-names)规则。

ReplicaSet 也需要
[`.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)
部分。

### Pod 模板    {#pod-template}

`.spec.template` 是一个 [Pod 模板](/zh-cn/docs/concepts/workloads/pods/#pod-templates)，
要求设置标签。在 `frontend.yaml` 示例中，我们指定了标签 `tier: frontend`。
注意不要将标签与其他控制器的选择算符重叠，否则那些控制器会尝试收养此 Pod。

对于模板的[重启策略](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy)
字段，`.spec.template.spec.restartPolicy`，唯一允许的取值是 `Always`，这也是默认值.

### Pod 选择算符   {#pod-selector}

`.spec.selector` 字段是一个[标签选择算符](/zh-cn/docs/concepts/overview/working-with-objects/labels/)。
如前文中[所讨论的](#how-a-replicaset-works)，这些是用来标识要被获取的 Pod
的标签。在签名的 `frontend.yaml` 示例中，选择算符为：

```yaml
matchLabels:
  tier: frontend
```

在 ReplicaSet 中，`.spec.template.metadata.labels` 的值必须与 `spec.selector`
值相匹配，否则该配置会被 API 拒绝。

{{< note >}}
对于设置了相同的 `.spec.selector`，但
`.spec.template.metadata.labels` 和 `.spec.template.spec` 字段不同的两个
ReplicaSet 而言，每个 ReplicaSet 都会忽略被另一个 ReplicaSet 所创建的 Pod。
{{< /note >}}

### Replicas

你可以通过设置 `.spec.replicas` 来指定要同时运行的 Pod 个数。
ReplicaSet 创建、删除 Pod 以与此值匹配。

如果你没有指定 `.spec.replicas`，那么默认值为 1。

## 使用 ReplicaSet    {#working-with-replicasets}

### 删除 ReplicaSet 和它的 Pod    {#deleting-a-replicaset-and-its-pods}

要删除 ReplicaSet 和它的所有 Pod，使用
[`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete) 命令。
默认情况下，[垃圾收集器](/zh-cn/docs/concepts/architecture/garbage-collection/)
自动删除所有依赖的 Pod。

当使用 REST API 或 `client-go` 库时，你必须在 `-d` 选项中将 `propagationPolicy`
设置为 `Background` 或 `Foreground`。例如：

```shell
kubectl proxy --port=8080
curl -X DELETE  'localhost:8080/apis/apps/v1/namespaces/default/replicasets/frontend' \
  -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
  -H "Content-Type: application/json"
```

### 只删除 ReplicaSet    {#deleting-just-a-replicaset}

你可以只删除 ReplicaSet 而不影响它的各个 Pod，方法是使用
[`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete)
命令并设置 `--cascade=orphan` 选项。

当使用 REST API 或 `client-go` 库时，你必须将 `propagationPolicy` 设置为 `Orphan`。
例如：

```shell
kubectl proxy --port=8080
curl -X DELETE  'localhost:8080/apis/apps/v1/namespaces/default/replicasets/frontend' \
  -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Orphan"}' \
  -H "Content-Type: application/json"
```

一旦删除了原来的 ReplicaSet，就可以创建一个新的来替换它。
由于新旧 ReplicaSet 的 `.spec.selector` 是相同的，新的 ReplicaSet 将接管老的 Pod。
但是，它不会努力使现有的 Pod 与新的、不同的 Pod 模板匹配。
若想要以可控的方式更新 Pod 的规约，可以使用
[Deployment](/zh-cn/docs/concepts/workloads/controllers/deployment/#creating-a-deployment)
资源，因为 ReplicaSet 并不直接支持滚动更新。

### 将 Pod 从 ReplicaSet 中隔离    {#isolating-pods-from-a-replicaset}

可以通过改变标签来从 ReplicaSet 中移除 Pod。
这种技术可以用来从服务中去除 Pod，以便进行排错、数据恢复等。
以这种方式移除的 Pod 将被自动替换（假设副本的数量没有改变）。

### 扩缩 ReplicaSet    {#scaling-a-replicaset}

通过更新 `.spec.replicas` 字段，ReplicaSet 可以被轻松地进行扩缩。ReplicaSet
控制器能确保匹配标签选择器的数量的 Pod 是可用的和可操作的。

在降低集合规模时，ReplicaSet 控制器通过对可用的所有 Pod 进行排序来优先选择要被删除的那些 Pod。
其一般性算法如下：

1. 首先选择剔除悬决（Pending，且不可调度）的各个 Pod
2. 如果设置了 `controller.kubernetes.io/pod-deletion-cost` 注解，则注解值较小的优先被裁减掉
3. 所处节点上副本个数较多的 Pod 优先于所处节点上副本较少者
4. 如果 Pod 的创建时间不同，最近创建的 Pod 优先于早前创建的 Pod 被裁减。
   （当 `LogarithmicScaleDown` 这一[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
   被启用时，创建时间是按整数幂级来分组的）。

如果以上比较结果都相同，则随机选择。

### Pod 删除开销   {#pod-deletion-cost}

{{< feature-state for_k8s_version="v1.22" state="beta" >}}

通过使用 [`controller.kubernetes.io/pod-deletion-cost`](/zh-cn/docs/reference/labels-annotations-taints/#pod-deletion-cost)
注解，用户可以对 ReplicaSet 缩容时要先删除哪些 Pod 设置偏好。

此注解要设置到 Pod 上，取值范围为 [-2147483647, 2147483647]。
所代表的是删除同一 ReplicaSet 中其他 Pod 相比较而言的开销。
删除开销较小的 Pod 比删除开销较高的 Pod 更容易被删除。

Pod 如果未设置此注解，则隐含的设置值为 0。负值也是可接受的。
如果注解值非法，API 服务器会拒绝对应的 Pod。

此功能特性处于 Beta 阶段，默认被启用。你可以通过为 kube-apiserver 和
kube-controller-manager 设置[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
`PodDeletionCost` 来禁用此功能。

{{< note >}}
- 此机制实施时仅是尽力而为，并不能对 Pod 的删除顺序作出任何保证；
- 用户应避免频繁更新注解值，例如根据某观测度量值来更新此注解值是应该避免的。
  这样做会在 API 服务器上产生大量的 Pod 更新操作。
{{< /note >}}

#### 使用场景示例    {#example-use-case}

同一应用的不同 Pod 可能其利用率是不同的。在对应用执行缩容操作时，
可能希望移除利用率较低的 Pod。为了避免频繁更新 Pod，应用应该在执行缩容操作之前更新一次
`controller.kubernetes.io/pod-deletion-cost` 注解值
（将注解值设置为一个与其 Pod 利用率对应的值）。
如果应用自身控制器缩容操作时（例如 Spark 部署的驱动 Pod），这种机制是可以起作用的。

### ReplicaSet 作为水平的 Pod 自动扩缩器目标    {#replicaset-as-a-horizontal-pod-autoscaler-target}

ReplicaSet 也可以作为[水平的 Pod 扩缩器 (HPA)](/zh-cn/docs/tasks/run-application/horizontal-pod-autoscale/)
的目标。也就是说，ReplicaSet 可以被 HPA 自动扩缩。
以下是 HPA 以我们在前一个示例中创建的副本集为目标的示例。

{{< codenew file="controllers/hpa-rs.yaml" >}}

将这个列表保存到 `hpa-rs.yaml` 并提交到 Kubernetes 集群，就能创建它所定义的
HPA，进而就能根据复制的 Pod 的 CPU 利用率对目标 ReplicaSet 进行自动扩缩。

```shell
kubectl apply -f https://k8s.io/examples/controllers/hpa-rs.yaml
```

或者，可以使用 `kubectl autoscale` 命令完成相同的操作（而且它更简单！）

```shell
kubectl autoscale rs frontend --max=10 --min=3 --cpu-percent=50
```

## ReplicaSet 的替代方案    {#alternatives-to-replicaset}

### Deployment（推荐）    {#deployment-recommended}

[`Deployment`](/zh-cn/docs/concepts/workloads/controllers/deployment/) 是一个可以拥有
ReplicaSet 并使用声明式方式在服务器端完成对 Pod 滚动更新的对象。
尽管 ReplicaSet 可以独立使用，目前它们的主要用途是提供给 Deployment 作为编排
Pod 创建、删除和更新的一种机制。当使用 Deployment 时，你不必关心如何管理它所创建的
ReplicaSet，Deployment 拥有并管理其 ReplicaSet。
因此，建议你在需要 ReplicaSet 时使用 Deployment。

### 裸 Pod    {#bare-pods}

与用户直接创建 Pod 的情况不同，ReplicaSet 会替换那些由于某些原因被删除或被终止的
Pod，例如在节点故障或破坏性的节点维护（如内核升级）的情况下。
因为这个原因，我们建议你使用 ReplicaSet，即使应用程序只需要一个 Pod。
想像一下，ReplicaSet 类似于进程监视器，只不过它在多个节点上监视多个 Pod，
而不是在单个节点上监视单个进程。
ReplicaSet 将本地容器重启的任务委托给了节点上的某个代理（例如，Kubelet）去完成。

### Job

使用[`Job`](/zh-cn/docs/concepts/workloads/controllers/job/) 代替 ReplicaSet，
可以用于那些期望自行终止的 Pod。

### DaemonSet

对于管理那些提供主机级别功能（如主机监控和主机日志）的容器，
就要用 [`DaemonSet`](/zh-cn/docs/concepts/workloads/controllers/daemonset/)
而不用 ReplicaSet。
这些 Pod 的寿命与主机寿命有关：这些 Pod 需要先于主机上的其他 Pod 运行，
并且在机器准备重新启动/关闭时安全地终止。

### ReplicationController

ReplicaSet 是 [ReplicationController](/zh-cn/docs/concepts/workloads/controllers/replicationcontroller/)
的后继者。二者目的相同且行为类似，只是 ReplicationController 不支持
[标签用户指南](/zh-cn/docs/concepts/overview/working-with-objects/labels/#label-selectors)
中讨论的基于集合的选择算符需求。
因此，相比于 ReplicationController，应优先考虑 ReplicaSet。

## {{% heading "whatsnext" %}}

* 了解 [Pod](/zh-cn/docs/concepts/workloads/pods)。
* 了解 [Deployment](/zh-cn/docs/concepts/workloads/controllers/deployment/)。
* [使用 Deployment 运行一个无状态应用](/zh-cn/docs/tasks/run-application/run-stateless-application-deployment/)，
  它依赖于 ReplicaSet。
* `ReplicaSet` 是 Kubernetes REST API 中的顶级资源。阅读
  {{< api-reference page="workload-resources/replica-set-v1" >}}
  对象定义理解关于该资源的 API。
* 阅读 [Pod 干扰预算（Disruption Budget）](/zh-cn/docs/concepts/workloads/pods/disruptions/)，
  了解如何在干扰下运行高度可用的应用。
