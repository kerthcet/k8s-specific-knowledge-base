---
title: StatefulSet
content_type: concept
weight: 30
---


StatefulSet 是用来管理有状态应用的工作负载 API 对象。

{{< glossary_definition term_id="statefulset" length="all" >}}


## 使用 StatefulSet   {#using-statefulsets}

StatefulSet 对于需要满足以下一个或多个需求的应用程序很有价值：

* 稳定的、唯一的网络标识符。
* 稳定的、持久的存储。
* 有序的、优雅的部署和扩缩。
* 有序的、自动的滚动更新。

在上面描述中，“稳定的”意味着 Pod 调度或重调度的整个过程是有持久性的。
如果应用程序不需要任何稳定的标识符或有序的部署、删除或扩缩，
则应该使用由一组无状态的副本控制器提供的工作负载来部署应用程序，比如
[Deployment](/zh-cn/docs/concepts/workloads/controllers/deployment/) 或者
[ReplicaSet](/zh-cn/docs/concepts/workloads/controllers/replicaset/)
可能更适用于你的无状态应用部署需要。

## 限制  {#limitations}

* 给定 Pod 的存储必须由
  [PersistentVolume Provisioner](https://github.com/kubernetes/examples/tree/master/staging/persistent-volume-provisioning/README.md)
  基于所请求的 `storage class` 来制备，或者由管理员预先制备。
* 删除或者扩缩 StatefulSet 并**不会**删除它关联的存储卷。
  这样做是为了保证数据安全，它通常比自动清除 StatefulSet 所有相关的资源更有价值。
* StatefulSet 当前需要[无头服务](/zh-cn/docs/concepts/services-networking/service/#headless-services)来负责 Pod
  的网络标识。你需要负责创建此服务。
* 当删除一个 StatefulSet 时，该 StatefulSet 不提供任何终止 Pod 的保证。
  为了实现 StatefulSet 中的 Pod 可以有序且体面地终止，可以在删除之前将 StatefulSet
  缩容到 0。
* 在默认 [Pod 管理策略](#pod-management-policies)(`OrderedReady`) 时使用[滚动更新](#rolling-updates)，
  可能进入需要[人工干预](#forced-rollback)才能修复的损坏状态。

## 组件  {#components}

下面的示例演示了 StatefulSet 的组件。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx # 必须匹配 .spec.template.metadata.labels
  serviceName: "nginx"
  replicas: 3 # 默认值是 1
  minReadySeconds: 10 # 默认值是 0
  template:
    metadata:
      labels:
        app: nginx # 必须匹配 .spec.selector.matchLabels
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: nginx
        image: registry.k8s.io/nginx-slim:0.8
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "my-storage-class"
      resources:
        requests:
          storage: 1Gi
```

上述例子中：

* 名为 `nginx` 的 Headless Service 用来控制网络域名。
* 名为 `web` 的 StatefulSet 有一个 Spec，它表明将在独立的 3 个 Pod 副本中启动 nginx 容器。
* `volumeClaimTemplates` 将通过 PersistentVolume 制备程序所准备的
  [PersistentVolumes](/zh-cn/docs/concepts/storage/persistent-volumes/) 来提供稳定的存储。

StatefulSet 的命名需要遵循
[DNS 标签](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-label-names)规范。

### Pod 选择算符     {#pod-selector}

你必须设置 StatefulSet 的 `.spec.selector` 字段，使之匹配其在
`.spec.template.metadata.labels` 中设置的标签。
未指定匹配的 Pod 选择算符将在创建 StatefulSet 期间导致验证错误。

### 卷申领模板  {#volume-claim-templates}

你可以设置 `.spec.volumeClaimTemplates`，
它可以使用 PersistentVolume 制备程序所准备的
[PersistentVolumes](/zh-cn/docs/concepts/storage/persistent-volumes/) 来提供稳定的存储。

### 最短就绪秒数 {#minimum-ready-seconds}

{{< feature-state for_k8s_version="v1.25" state="stable" >}}

`.spec.minReadySeconds` 是一个可选字段。
它指定新创建的 Pod 应该在没有任何容器崩溃的情况下运行并准备就绪，才能被认为是可用的。
这用于在使用[滚动更新](#rolling-updates)策略时检查滚动的进度。
该字段默认为 0（Pod 准备就绪后将被视为可用）。
要了解有关何时认为 Pod 准备就绪的更多信息，
请参阅[容器探针](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#container-probes)。

## Pod 标识   {#pod-identity}

StatefulSet Pod 具有唯一的标识，该标识包括顺序标识、稳定的网络标识和稳定的存储。
该标识和 Pod 是绑定的，与该 Pod 调度到哪个节点上无关。

### 有序索引   {#ordinal-index}

对于具有 N 个[副本](#replicas)的 StatefulSet，该 StatefulSet 中的每个 Pod 将被分配一个整数序号，
该序号在此 StatefulSet 上是唯一的。默认情况下，这些 Pod 将被从 0 到 N-1 的序号。

### 起始序号   {#start-ordinal}

{{< feature-state for_k8s_version="v1.27" state="beta" >}}

`.spec.ordinals` 是一个可选的字段，允许你配置分配给每个 Pod 的整数序号。
该字段默认为 nil 值。你必须启用 `StatefulSetStartOrdinal`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)才能使用此字段。
一旦启用，你就可以配置以下选项：

* `.spec.ordinals.start`：如果 `.spec.ordinals.start` 字段被设置，则 Pod 将被分配从
  `.spec.ordinals.start` 到 `.spec.ordinals.start + .spec.replicas - 1` 的序号。

### 稳定的网络 ID   {#stable-network-id}

StatefulSet 中的每个 Pod 根据 StatefulSet 的名称和 Pod 的序号派生出它的主机名。
组合主机名的格式为`$(StatefulSet 名称)-$(序号)`。
上例将会创建三个名称分别为 `web-0、web-1、web-2` 的 Pod。
StatefulSet 可以使用[无头服务](/zh-cn/docs/concepts/services-networking/service/#headless-services)控制它的
Pod 的网络域。管理域的这个服务的格式为：
`$(服务名称).$(名字空间).svc.cluster.local`，其中 `cluster.local` 是集群域。
一旦每个 Pod 创建成功，就会得到一个匹配的 DNS 子域，格式为：
`$(pod 名称).$(所属服务的 DNS 域名)`，其中所属服务由 StatefulSet 的 `serviceName` 域来设定。

取决于集群域内部 DNS 的配置，有可能无法查询一个刚刚启动的 Pod 的 DNS 命名。
当集群内其他客户端在 Pod 创建完成前发出 Pod 主机名查询时，就会发生这种情况。
负缓存 (在 DNS 中较为常见) 意味着之前失败的查询结果会被记录和重用至少若干秒钟，
即使 Pod 已经正常运行了也是如此。

如果需要在 Pod 被创建之后及时发现它们，可使用以下选项：

- 直接查询 Kubernetes API（比如，利用 watch 机制）而不是依赖于 DNS 查询
- 缩短 Kubernetes DNS 驱动的缓存时长（通常这意味着修改 CoreDNS 的 ConfigMap，目前缓存时长为 30 秒）

正如[限制](#limitations)中所述，
你需要负责创建[无头服务](/zh-cn/docs/concepts/services-networking/service/#headless-services)以便为 Pod 提供网络标识。

下面给出一些选择集群域、服务名、StatefulSet 名、及其怎样影响 StatefulSet 的 Pod 上的 DNS 名称的示例：

集群域名       | 服务（名字空间/名字）| StatefulSet（名字空间/名字） | StatefulSet 域名 | Pod DNS | Pod 主机名   |
-------------- | -------------------- | ---------------------------- | ---------------- | ------- | ------------ |
 cluster.local | default/nginx     | default/web       | nginx.default.svc.cluster.local | web-{0..N-1}.nginx.default.svc.cluster.local | web-{0..N-1} |
 cluster.local | foo/nginx         | foo/web           | nginx.foo.svc.cluster.local     | web-{0..N-1}.nginx.foo.svc.cluster.local     | web-{0..N-1} |
 kube.local    | foo/nginx         | foo/web           | nginx.foo.svc.kube.local        | web-{0..N-1}.nginx.foo.svc.kube.local        | web-{0..N-1} |

{{< note >}}
集群域会被设置为 `cluster.local`，除非有[其他配置](/zh-cn/docs/concepts/services-networking/dns-pod-service/)。
{{< /note >}}

### 稳定的存储  {#stable-storage}

对于 StatefulSet 中定义的每个 VolumeClaimTemplate，每个 Pod 接收到一个 PersistentVolumeClaim。
在上面的 nginx 示例中，每个 Pod 将会得到基于 StorageClass `my-storage-class` 制备的
1 Gib 的 PersistentVolume。
如果没有声明 StorageClass，就会使用默认的 StorageClass。
当一个 Pod 被调度（重新调度）到节点上时，它的 `volumeMounts` 会挂载与其
PersistentVolumeClaims 相关联的 PersistentVolume。
请注意，当 Pod 或者 StatefulSet 被删除时，与 PersistentVolumeClaims 相关联的
PersistentVolume 并不会被删除。要删除它必须通过手动方式来完成。

### Pod 名称标签   {#pod-name-label}

当 StatefulSet {{<glossary_tooltip text="控制器" term_id="controller">}}创建 Pod 时，
它会添加一个标签 `statefulset.kubernetes.io/pod-name`，该标签值设置为 Pod 名称。
这个标签允许你给 StatefulSet 中的特定 Pod 绑定一个 Service。

## 部署和扩缩保证   {#deployment-and-scaling-guarantees}

* 对于包含 N 个 副本的 StatefulSet，当部署 Pod 时，它们是依次创建的，顺序为 `0..N-1`。
* 当删除 Pod 时，它们是逆序终止的，顺序为 `N-1..0`。
* 在将扩缩操作应用到 Pod 之前，它前面的所有 Pod 必须是 Running 和 Ready 状态。
* 在一个 Pod 终止之前，所有的继任者必须完全关闭。

StatefulSet 不应将 `pod.Spec.TerminationGracePeriodSeconds` 设置为 0。
这种做法是不安全的，要强烈阻止。
更多的解释请参考[强制删除 StatefulSet Pod](/zh-cn/docs/tasks/run-application/force-delete-stateful-set-pod/)。

在上面的 nginx 示例被创建后，会按照 web-0、web-1、web-2 的顺序部署三个 Pod。
在 web-0 进入 [Running 和 Ready](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/)
状态前不会部署 web-1。在 web-1 进入 Running 和 Ready 状态前不会部署 web-2。
如果 web-1 已经处于 Running 和 Ready 状态，而 web-2 尚未部署，在此期间发生了
web-0 运行失败，那么 web-2 将不会被部署，要等到 web-0 部署完成并进入 Running 和
Ready 状态后，才会部署 web-2。

如果用户想将示例中的 StatefulSet 扩缩为 `replicas=1`，首先被终止的是 web-2。
在 web-2 没有被完全停止和删除前，web-1 不会被终止。
当 web-2 已被终止和删除、web-1 尚未被终止，如果在此期间发生 web-0 运行失败，
那么就不会终止 web-1，必须等到 web-0 进入 Running 和 Ready 状态后才会终止 web-1。

### Pod 管理策略 {#pod-management-policies}

StatefulSet 允许你放宽其排序保证，
同时通过它的 `.spec.podManagementPolicy` 域保持其唯一性和身份保证。

#### OrderedReady Pod 管理   {#orderedready-pod-management}

`OrderedReady` Pod 管理是 StatefulSet 的默认设置。
它实现了[上面](#deployment-and-scaling-guarantees)描述的功能。

#### 并行 Pod 管理   {#parallel-pod-management}

`Parallel` Pod 管理让 StatefulSet 控制器并行的启动或终止所有的 Pod，
启动或者终止其他 Pod 前，无需等待 Pod 进入 Running 和 Ready 或者完全停止状态。
这个选项只会影响扩缩操作的行为，更新则不会被影响。

## 更新策略  {#update-strategies}

StatefulSet 的 `.spec.updateStrategy` 字段让你可以配置和禁用掉自动滚动更新 Pod
的容器、标签、资源请求或限制、以及注解。有两个允许的值：

`OnDelete`
: 当 StatefulSet 的 `.spec.updateStrategy.type` 设置为 `OnDelete` 时，
  它的控制器将不会自动更新 StatefulSet 中的 Pod。
  用户必须手动删除 Pod 以便让控制器创建新的 Pod，以此来对 StatefulSet 的
  `.spec.template` 的变动作出反应。

`RollingUpdate`
: `RollingUpdate` 更新策略对 StatefulSet 中的 Pod 执行自动的滚动更新。这是默认的更新策略。

## 滚动更新 {#rolling-updates}

当 StatefulSet 的 `.spec.updateStrategy.type` 被设置为 `RollingUpdate` 时，
StatefulSet 控制器会删除和重建 StatefulSet 中的每个 Pod。
它将按照与 Pod 终止相同的顺序（从最大序号到最小序号）进行，每次更新一个 Pod。

Kubernetes 控制平面会等到被更新的 Pod 进入 Running 和 Ready 状态，然后再更新其前身。
如果你设置了 `.spec.minReadySeconds`（查看[最短就绪秒数](#minimum-ready-seconds)），
控制平面在 Pod 就绪后会额外等待一定的时间再执行下一步。

### 分区滚动更新   {#partitions}

通过声明 `.spec.updateStrategy.rollingUpdate.partition` 的方式，`RollingUpdate`
更新策略可以实现分区。
如果声明了一个分区，当 StatefulSet 的 `.spec.template` 被更新时，
所有序号大于等于该分区序号的 Pod 都会被更新。
所有序号小于该分区序号的 Pod 都不会被更新，并且，即使它们被删除也会依据之前的版本进行重建。
如果 StatefulSet 的 `.spec.updateStrategy.rollingUpdate.partition` 大于它的
`.spec.replicas`，则对它的 `.spec.template` 的更新将不会传递到它的 Pod。
在大多数情况下，你不需要使用分区，但如果你希望进行阶段更新、执行金丝雀或执行分阶段上线，则这些分区会非常有用。

### 最大不可用 Pod   {#maximum-unavailable-pods}

{{< feature-state for_k8s_version="v1.24" state="alpha" >}}

你可以通过指定 `.spec.updateStrategy.rollingUpdate.maxUnavailable`
字段来控制更新期间不可用的 Pod 的最大数量。
该值可以是绝对值（例如，“5”）或者是期望 Pod 个数的百分比（例如，`10%`）。
绝对值是根据百分比值四舍五入计算的。
该字段不能为 0。默认设置为 1。

该字段适用于 `0` 到 `replicas - 1` 范围内的所有 Pod。
如果在 `0` 到 `replicas - 1` 范围内存在不可用 Pod，这类 Pod 将被计入 `maxUnavailable` 值。

{{< note >}}
`maxUnavailable` 字段处于 Alpha 阶段，仅当 API 服务器启用了 `MaxUnavailableStatefulSet`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)时才起作用。
{{< /note >}}

### 强制回滚 {#forced-rollback}

在默认 [Pod 管理策略](#pod-management-policies)(`OrderedReady`) 下使用[滚动更新](#rolling-updates)，
可能进入需要人工干预才能修复的损坏状态。

如果更新后 Pod 模板配置进入无法运行或就绪的状态（例如，
由于错误的二进制文件或应用程序级配置错误），StatefulSet 将停止回滚并等待。

在这种状态下，仅将 Pod 模板还原为正确的配置是不够的。
由于[已知问题](https://github.com/kubernetes/kubernetes/issues/67250)，StatefulSet
将继续等待损坏状态的 Pod 准备就绪（永远不会发生），然后再尝试将其恢复为正常工作配置。

恢复模板后，还必须删除 StatefulSet 尝试使用错误的配置来运行的 Pod。这样，
StatefulSet 才会开始使用被还原的模板来重新创建 Pod。

## PersistentVolumeClaim 保留  {#persistentvolumeclaim-retention}

{{< feature-state for_k8s_version="v1.27" state="beta" >}}

在 StatefulSet 的生命周期中，可选字段
`.spec.persistentVolumeClaimRetentionPolicy` 控制是否删除以及如何删除 PVC。
使用该字段，你必须在 API 服务器和控制器管理器启用 `StatefulSetAutoDeletePVC`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)。
启用后，你可以为每个 StatefulSet 配置两个策略：

`whenDeleted`
: 配置删除 StatefulSet 时应用的卷保留行为。

`whenScaled`
: 配置当 StatefulSet 的副本数减少时应用的卷保留行为；例如，缩小集合时。

对于你可以配置的每个策略，你可以将值设置为 `Delete` 或 `Retain`。

`Delete`
: 对于受策略影响的每个 Pod，基于 StatefulSet 的 `volumeClaimTemplate` 字段创建的 PVC 都会被删除。
  使用 `whenDeleted` 策略，所有来自 `volumeClaimTemplate` 的 PVC 在其 Pod 被删除后都会被删除。
  使用 `whenScaled` 策略，只有与被缩减的 Pod 副本对应的 PVC 在其 Pod 被删除后才会被删除。

`Retain`（默认）
: 来自 `volumeClaimTemplate` 的 PVC 在 Pod 被删除时不受影响。这是此新功能之前的行为。

请记住，这些策略**仅**适用于由于 StatefulSet 被删除或被缩小而被删除的 Pod。
例如，如果与 StatefulSet 关联的 Pod 由于节点故障而失败，
并且控制平面创建了替换 Pod，则 StatefulSet 保留现有的 PVC。
现有卷不受影响，集群会将其附加到新 Pod 即将启动的节点上。

策略的默认值为 `Retain`，与此新功能之前的 StatefulSet 行为相匹配。

这是一个示例策略。

```yaml
apiVersion: apps/v1
kind: StatefulSet
...
spec:
  persistentVolumeClaimRetentionPolicy:
    whenDeleted: Retain
    whenScaled: Delete
...
```

StatefulSet {{<glossary_tooltip text="控制器" term_id="controller">}}为其 PVC
添加了[属主引用](/zh-cn/docs/concepts/overview/working-with-objects/owners-dependents/#owner-references-in-object-specifications)，
这些 PVC 在 Pod 终止后被{{<glossary_tooltip text="垃圾回收器" term_id="garbage-collection">}}删除。
这使 Pod 能够在删除 PVC 之前（以及在删除后备 PV 和卷之前，取决于保留策略）干净地卸载所有卷。
当你设置 `whenDeleted` 删除策略，对 StatefulSet 实例的属主引用放置在与该 StatefulSet 关联的所有 PVC 上。

`whenScaled` 策略必须仅在 Pod 缩减时删除 PVC，而不是在 Pod 因其他原因被删除时删除。
执行协调操作时，StatefulSet 控制器将其所需的副本数与集群上实际存在的 Pod 进行比较。
对于 StatefulSet 中的所有 Pod 而言，如果其 ID 大于副本数，则将被废弃并标记为需要删除。
如果 `whenScaled` 策略是 `Delete`，则在删除 Pod 之前，
首先将已销毁的 Pod 设置为与 StatefulSet 模板对应的 PVC 的属主。
这会导致 PVC 仅在已废弃的 Pod 终止后被垃圾收集。

这意味着如果控制器崩溃并重新启动，在其属主引用更新到适合策略的 Pod 之前，不会删除任何 Pod。
如果在控制器关闭时强制删除了已废弃的 Pod，则属主引用可能已被设置，也可能未被设置，具体取决于控制器何时崩溃。
更新属主引用可能需要几个协调循环，因此一些已废弃的 Pod 可能已经被设置了属主引用，而其他可能没有。
出于这个原因，我们建议等待控制器恢复，控制器将在终止 Pod 之前验证属主引用。
如果这不可行，则操作员应验证 PVC 上的属主引用，以确保在强制删除 Pod 时删除预期的对象。

### 副本数 {#replicas}

`.spec.replicas` 是一个可选字段，用于指定所需 Pod 的数量。它的默认值为 1。

如果你手动扩缩已部署的负载，例如通过 `kubectl scale statefulset statefulset --replicas=X`，
然后根据清单更新 StatefulSet（例如：通过运行 `kubectl apply -f statefulset.yaml`），
那么应用该清单的操作会覆盖你之前所做的手动扩缩。

如果 [HorizontalPodAutoscaler](/zh-cn/docs/tasks/run-application/horizontal-pod-autoscale/)
（或任何类似的水平扩缩 API）正在管理 StatefulSet 的扩缩，
请不要设置 `.spec.replicas`。
相反，允许 Kubernetes 控制平面自动管理 `.spec.replicas` 字段。

## {{% heading "whatsnext" %}}

* 了解 [Pod](/zh-cn/docs/concepts/workloads/pods)。
* 了解如何使用 StatefulSet
  * 跟随示例[部署有状态应用](/zh-cn/docs/tutorials/stateful-application/basic-stateful-set/)。
  * 跟随示例[使用 StatefulSet 部署 Cassandra](/zh-cn/docs/tutorials/stateful-application/cassandra/)。
  * 跟随示例[运行多副本的有状态应用程序](/zh-cn/docs/tasks/run-application/run-replicated-stateful-application/)。
  * 了解如何[扩缩 StatefulSet](/zh-cn/docs/tasks/run-application/scale-stateful-set/)。
  * 了解[删除 StatefulSet](/zh-cn/docs/tasks/run-application/delete-stateful-set/)涉及到的操作。
  * 了解如何[配置 Pod 以使用卷进行存储](/zh-cn/docs/tasks/configure-pod-container/configure-volume-storage/)。
  * 了解如何[配置 Pod 以使用 PersistentVolume 作为存储](/zh-cn/docs/tasks/configure-pod-container/configure-persistent-volume-storage/)。
* `StatefulSet` 是 Kubernetes REST API 中的顶级资源。阅读 {{< api-reference page="workload-resources/stateful-set-v1" >}}
   对象定义理解关于该资源的 API。
* 阅读 [Pod 干扰预算（Disruption Budget）](/zh-cn/docs/concepts/workloads/pods/disruptions/)，了解如何在干扰下运行高度可用的应用。

