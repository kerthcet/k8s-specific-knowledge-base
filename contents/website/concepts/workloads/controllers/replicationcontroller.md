---
title: ReplicationController
content_type: concept
weight: 90
---



{{< note >}}
现在推荐使用配置 [`ReplicaSet`](/zh-cn/docs/concepts/workloads/controllers/replicaset/) 的
[`Deployment`](/zh-cn/docs/concepts/workloads/controllers/deployment/) 来建立副本管理机制。
{{< /note >}}

**ReplicationController** 确保在任何时候都有特定数量的 Pod 副本处于运行状态。
换句话说，ReplicationController 确保一个 Pod 或一组同类的 Pod 总是可用的。


## ReplicationController 如何工作   {#how-a-replicationcontroller-works}

当 Pod 数量过多时，ReplicationController 会终止多余的 Pod。当 Pod 数量太少时，ReplicationController 将会启动新的 Pod。
与手动创建的 Pod 不同，由 ReplicationController 创建的 Pod 在失败、被删除或被终止时会被自动替换。
例如，在中断性维护（如内核升级）之后，你的 Pod 会在节点上重新创建。
因此，即使你的应用程序只需要一个 Pod，你也应该使用 ReplicationController 创建 Pod。
ReplicationController 类似于进程管理器，但是 ReplicationController 不是监控单个节点上的单个进程，而是监控跨多个节点的多个 Pod。

在讨论中，ReplicationController 通常缩写为 "rc"，并作为 kubectl 命令的快捷方式。

一个简单的示例是创建一个 ReplicationController 对象来可靠地无限期地运行 Pod 的一个实例。
更复杂的用例是运行一个多副本服务（如 web 服务器）的若干相同副本。

## 运行一个示例 ReplicationController   {#running-an-example-replicationcontroller}

这个示例 ReplicationController 配置运行 nginx Web 服务器的三个副本。

{{< codenew file="controllers/replication.yaml" >}}

通过下载示例文件并运行以下命令来运行示例任务:

```shell
kubectl apply -f https://k8s.io/examples/controllers/replication.yaml
```

输出类似于：

```
replicationcontroller/nginx created
```

使用以下命令检查 ReplicationController 的状态:

```shell
kubectl describe replicationcontrollers/nginx
```

输出类似于：

```
Name:        nginx
Namespace:   default
Selector:    app=nginx
Labels:      app=nginx
Annotations:    <none>
Replicas:    3 current / 3 desired
Pods Status: 0 Running / 3 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:       app=nginx
  Containers:
   nginx:
    Image:              nginx
    Port:               80/TCP
    Environment:        <none>
    Mounts:             <none>
  Volumes:              <none>
Events:
  FirstSeen       LastSeen     Count    From                        SubobjectPath    Type      Reason              Message
  ---------       --------     -----    ----                        -------------    ----      ------              -------
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-qrm3m
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-3ntk0
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-4ok8v
```

在这里，创建了三个 Pod，但没有一个 Pod 正在运行，这可能是因为正在拉取镜像。
稍后，相同的命令可能会显示：

```
Pods Status:    3 Running / 0 Waiting / 0 Succeeded / 0 Failed
```

要以机器可读的形式列出属于 ReplicationController 的所有 Pod，可以使用如下命令：

```shell
pods=$(kubectl get pods --selector=app=nginx --output=jsonpath={.items..metadata.name})
echo $pods
```

输出类似于：

```
nginx-3ntk0 nginx-4ok8v nginx-qrm3m
```

这里，选择算符与 ReplicationController 的选择算符相同（参见 `kubectl describe` 输出），并以不同的形式出现在 `replication.yaml` 中。
`--output=jsonpath` 选项指定了一个表达式，仅从返回列表中的每个 Pod 中获取名称。

## 编写一个 ReplicationController 清单   {#writing-a-replicationcontroller-manifest}

与所有其它 Kubernetes 配置一样，ReplicationController 需要 `apiVersion`、`kind` 和 `metadata` 字段。

当控制平面为 ReplicationController 创建新的 Pod 时，ReplicationController
的 `.metadata.name` 是命名这些 Pod 的部分基础。ReplicationController 的名称必须是一个合法的
[DNS 子域](/zh-cn/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names)值，
但这可能对 Pod 的主机名产生意外的结果。为获得最佳兼容性，名称应遵循更严格的
[DNS 标签](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-label-names)规则。

有关使用配置文件的常规信息，
参考[对象管理](/zh-cn/docs/concepts/overview/working-with-objects/object-management/)。

ReplicationController 也需要一个 [`.spec` 部分](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)。

### Pod 模板  {#pod-template}

`.spec.template` 是 `.spec` 的唯一必需字段。

`.spec.template` 是一个 [Pod 模板](/zh-cn/docs/concepts/workloads/pods/#pod-templates)。
它的模式与 {{< glossary_tooltip text="Pod" term_id="pod" >}} 完全相同，只是它是嵌套的，没有 `apiVersion` 或 `kind` 属性。

除了 Pod 所需的字段外，ReplicationController 中的 Pod 模板必须指定适当的标签和适当的重新启动策略。
对于标签，请确保不与其他控制器重叠。参考 [Pod 选择算符](#pod-selector)。

只允许 [`.spec.template.spec.restartPolicy`](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy)
等于 `Always`，如果没有指定，这是默认值。

对于本地容器重启，ReplicationController 委托给节点上的代理，
例如 [Kubelet](/zh-cn/docs/reference/command-line-tools-reference/kubelet/)。

### ReplicationController 上的标签   {#labels-on-the-replicacontroller}

ReplicationController 本身可以有标签 （`.metadata.labels`）。
通常，你可以将这些设置为 `.spec.template.metadata.labels`；
如果没有指定 `.metadata.labels` 那么它默认为 `.spec.template.metadata.labels`。
但是，Kubernetes 允许它们是不同的，`.metadata.labels` 不会影响 ReplicationController 的行为。

### Pod 选择算符 {#pod-selector}

`.spec.selector` 字段是一个[标签选择算符](/zh-cn/docs/concepts/overview/working-with-objects/labels/#label-selectors)。
ReplicationController 管理标签与选择算符匹配的所有 Pod。
它不区分它创建或删除的 Pod 和其他人或进程创建或删除的 Pod。
这允许在不影响正在运行的 Pod 的情况下替换 ReplicationController。

如果指定了 `.spec.template.metadata.labels`，它必须和 `.spec.selector` 相同，否则它将被 API 拒绝。
如果没有指定 `.spec.selector`，它将默认为 `.spec.template.metadata.labels`。

另外，通常不应直接使用另一个 ReplicationController 或另一个控制器（例如 Job）
来创建其标签与该选择算符匹配的任何 Pod。如果这样做，ReplicationController 会认为它创建了这些 Pod。
Kubernetes 并没有阻止你这样做。

如果你的确创建了多个控制器并且其选择算符之间存在重叠，那么你将不得不自己管理删除操作（参考[后文](#working-with-replicationcontrollers)）。

### 多个副本   {#multiple-replicas}

你可以通过设置 `.spec.replicas` 来指定应该同时运行多少个 Pod。
在任何时候，处于运行状态的 Pod 个数都可能高于或者低于设定值。例如，副本个数刚刚被增加或减少时，
或者一个 Pod 处于优雅终止过程中而其替代副本已经提前开始创建时。

如果你没有指定 `.spec.replicas`，那么它默认是 1。

## 使用 ReplicationController {#working-with-replicationcontrollers}

### 删除一个 ReplicationController 以及它的 Pod   {#deleteing-a-replicationcontroller-and-its-pods}

要删除一个 ReplicationController 以及它的 Pod，使用
[`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete)。
kubectl 将 ReplicationController 缩容为 0 并等待以便在删除 ReplicationController 本身之前删除每个 Pod。
如果这个 kubectl 命令被中断，可以重新启动它。

当使用 REST API 或[客户端库](/zh-cn/docs/reference/using-api/client-libraries)时，你需要明确地执行这些步骤（缩容副本为 0、
等待 Pod 删除，之后删除 ReplicationController 资源）。

### 只删除 ReplicationController   {#deleting-only-a-replicationcontroller}

你可以删除一个 ReplicationController 而不影响它的任何 Pod。

使用 kubectl，为 [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete) 指定 `--cascade=orphan` 选项。

当使用 REST API 或[客户端库](/zh-cn/docs/reference/using-api/client-libraries)时，只需删除 ReplicationController 对象。

一旦原始对象被删除，你可以创建一个新的 ReplicationController 来替换它。
只要新的和旧的 `.spec.selector` 相同，那么新的控制器将领养旧的 Pod。
但是，它不会做出任何努力使现有的 Pod 匹配新的、不同的 Pod 模板。
如果希望以受控方式更新 Pod 以使用新的 spec，请执行[滚动更新](#rolling-updates)操作。

### 从 ReplicationController 中隔离 Pod   {#isolating-pods-from-a-replicationcontroller}

通过更改 Pod 的标签，可以从 ReplicationController 的目标中删除 Pod。
此技术可用于从服务中删除 Pod 以进行调试、数据恢复等。以这种方式删除的 Pod
将被自动替换（假设复制副本的数量也没有更改）。

## 常见的使用模式   {#common-usage-patterns}

### 重新调度   {#rescheduling}

如上所述，无论你想要继续运行 1 个 Pod 还是 1000 个 Pod，一个 ReplicationController 都将确保存在指定数量的 Pod，即使在节点故障或 Pod 终止(例如，由于另一个控制代理的操作)的情况下也是如此。
### 扩缩容   {#scaling}

通过设置 `replicas` 字段，ReplicationController 可以允许扩容或缩容副本的数量。
你可以手动或通过自动扩缩控制代理来控制 ReplicationController 执行此操作。

### 滚动更新 {#rolling-updates}

ReplicationController 的设计目的是通过逐个替换 Pod 以方便滚动更新服务。

如 [#1353](https://issue.k8s.io/1353) PR 中所述，建议的方法是使用 1 个副本创建一个新的 ReplicationController，
逐个扩容新的（+1）和缩容旧的（-1）控制器，然后在旧的控制器达到 0 个副本后将其删除。
这一方法能够实现可控的 Pod 集合更新，即使存在意外失效的状况。

理想情况下，滚动更新控制器将考虑应用程序的就绪情况，并确保在任何给定时间都有足够数量的 Pod 有效地提供服务。

这两个 ReplicationController 将需要创建至少具有一个不同标签的 Pod，比如 Pod 主要容器的镜像标签，因为通常是镜像更新触发滚动更新。

### 多个版本跟踪   {#multiple-release-tracks}

除了在滚动更新过程中运行应用程序的多个版本之外，通常还会使用多个版本跟踪来长时间，
甚至持续运行多个版本。这些跟踪将根据标签加以区分。

例如，一个服务可能把具有 `tier in (frontend), environment in (prod)` 的所有 Pod 作为目标。
现在假设你有 10 个副本的 Pod 组成了这个层。但是你希望能够 `canary` （`金丝雀`）发布这个组件的新版本。
你可以为大部分副本设置一个 ReplicationController，其中 `replicas` 设置为 9，
标签为 `tier=frontend, environment=prod, track=stable` 而为 `canary`
设置另一个 ReplicationController，其中 `replicas` 设置为 1，
标签为 `tier=frontend, environment=prod, track=canary`。
现在这个服务覆盖了 `canary` 和非 `canary` Pod。但你可以单独处理
ReplicationController，以测试、监控结果等。

### 和服务一起使用 ReplicationController   {#using-replicationcontrollers-with-services}

多个 ReplicationController 可以位于一个服务的后面，例如，一部分流量流向旧版本，
一部分流量流向新版本。

一个 ReplicationController 永远不会自行终止，但它不会像服务那样长时间存活。
服务可以由多个 ReplicationController 控制的 Pod 组成，并且在服务的生命周期内
（例如，为了执行 Pod 更新而运行服务），可以创建和销毁许多 ReplicationController。
服务本身和它们的客户端都应该忽略负责维护服务 Pod 的 ReplicationController 的存在。

## 编写多副本的应用   {#writing-programs-for-replication}

由 ReplicationController 创建的 Pod 是可替换的，语义上是相同的，
尽管随着时间的推移，它们的配置可能会变得异构。
这显然适合于多副本的无状态服务器，但是 ReplicationController 也可以用于维护主选、
分片和工作池应用程序的可用性。
这样的应用程序应该使用动态的工作分配机制，例如
[RabbitMQ 工作队列](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)，
而不是静态的或者一次性定制每个 Pod 的配置，这被认为是一种反模式。
执行的任何 Pod 定制，例如资源的垂直自动调整大小（例如，CPU 或内存），
都应该由另一个在线控制器进程执行，这与 ReplicationController 本身没什么不同。

## ReplicationController 的职责   {#responsibilities-of-the-replicationcontroller}

ReplicationController 仅确保所需的 Pod 数量与其标签选择算符匹配，并且是可操作的。
目前，它的计数中只排除终止的 Pod。
未来，可能会考虑系统提供的[就绪状态](https://issue.k8s.io/620)和其他信息，
我们可能会对替换策略添加更多控制，
我们计划发出事件，这些事件可以被外部客户端用来实现任意复杂的替换和/或缩减策略。

ReplicationController 永远被限制在这个狭隘的职责范围内。
它本身既不执行就绪态探测，也不执行活跃性探测。
它不负责执行自动扩缩，而是由外部自动扩缩器控制（如
[#492](https://issue.k8s.io/492) 中所述），后者负责更改其 `replicas` 字段值。
我们不会向 ReplicationController 添加调度策略（例如，
[spreading](https://issue.k8s.io/367#issuecomment-48428019)）。
它也不应该验证所控制的 Pod 是否与当前指定的模板匹配，因为这会阻碍自动调整大小和其他自动化过程。
类似地，完成期限、整理依赖关系、配置扩展和其他特性也属于其他地方。
我们甚至计划考虑批量创建 Pod 的机制（查阅 [#170](https://issue.k8s.io/170)）。

ReplicationController 旨在成为可组合的构建基元。
我们希望在它和其他补充原语的基础上构建更高级别的 API 或者工具，以便于将来的用户使用。
kubectl 目前支持的 "macro" 操作（运行、扩缩、滚动更新）就是这方面的概念示例。
例如，我们可以想象类似于 [Asgard](https://netflixtechblog.com/asgard-web-based-cloud-management-and-deployment-2c9fc4e4d3a1)
的东西管理 ReplicationController、自动定标器、服务、调度策略、金丝雀发布等。

## API 对象   {#api-object}

在 Kubernetes REST API 中 Replication controller 是顶级资源。
更多关于 API 对象的详细信息可以在
[ReplicationController API 对象](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#replicationcontroller-v1-core)找到。

## ReplicationController 的替代方案   {#alternatives-to-replicationcontroller}

### ReplicaSet

[`ReplicaSet`](/zh-cn/docs/concepts/workloads/controllers/replicaset/) 是下一代 ReplicationController，
支持新的[基于集合的标签选择算符](/zh-cn/docs/concepts/overview/working-with-objects/labels/#set-based-requirement)。
它主要被 [`Deployment`](/zh-cn/docs/concepts/workloads/controllers/deployment/)
用来作为一种编排 Pod 创建、删除及更新的机制。
请注意，我们推荐使用 Deployment 而不是直接使用 ReplicaSet，除非你需要自定义更新编排或根本不需要更新。

### Deployment （推荐）

[`Deployment`](/zh-cn/docs/concepts/workloads/controllers/deployment/) 是一种更高级别的 API 对象，用于更新其底层 ReplicaSet 及其 Pod。
如果你想要这种滚动更新功能，那么推荐使用 Deployment，因为它们是声明式的、服务端的，并且具有其它特性。

### 裸 Pod

与用户直接创建 Pod 的情况不同，ReplicationController 能够替换因某些原因被删除或被终止的 Pod，
例如在节点故障或中断节点维护的情况下，例如内核升级。
因此，我们建议你使用 ReplicationController，即使你的应用程序只需要一个 Pod。
可以将其看作类似于进程管理器，它只管理跨多个节点的多个 Pod，而不是单个节点上的单个进程。
ReplicationController 将本地容器重启委托给节点上的某个代理（例如 Kubelet)。

### Job

对于预期会自行终止的 Pod (即批处理任务)，使用
[`Job`](/zh-cn/docs/concepts/workloads/controllers/job/) 而不是 ReplicationController。

### DaemonSet

对于提供机器级功能（例如机器监控或机器日志记录）的 Pod，
使用 [`DaemonSet`](/zh-cn/docs/concepts/workloads/controllers/daemonset/) 而不是
ReplicationController。
这些 Pod 的生命期与机器的生命期绑定：它们需要在其他 Pod 启动之前在机器上运行，
并且在机器准备重新启动或者关闭时安全地终止。

## {{% heading "whatsnext" %}}

- 了解 [Pod](/zh-cn/docs/concepts/workloads/pods)。
- 了解 [Depolyment](/zh-cn/docs/concepts/workloads/controllers/deployment/)，ReplicationController 的替代品。
- `ReplicationController` 是 Kubernetes REST API 的一部分，阅读 {{< api-reference page="workload-resources/replication-controller-v1" >}}
  对象定义以了解 replication controllers 的 API。

