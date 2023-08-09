---
title: 众所周知的标签、注解和污点
content_type: concept
weight: 40
no_list: true
---

Kubernetes 将所有标签和注解保留在 kubernetes.io 和 k8s.io 名字空间中。

本文档既可作为值的参考，也可作为分配值的协调点。


## API 对象上使用的标签、注解和污点   {#labels-annotations-and-taints-used-on-api-objects}

### app.kubernetes.io/component {#app-kubernetes-io-component}

例子：`app.kubernetes.io/component: "database"`

用于：所有对象（通常用于[工作负载资源](/zh-cn/docs/reference/kubernetes-api/workload-resources/)）。

架构中的组件。

[推荐标签](/zh-cn/docs/concepts/overview/working-with-objects/common-labels/#labels)之一。

### app.kubernetes.io/created-by（已弃用）  {#app-kubernetes-io-created-by}

示例：`app.kubernetes.io/created-by: "controller-manager"`

用于：所有对象（通常用于[工作负载资源](/zh-cn/docs/reference/kubernetes-api/workload-resources/)）。

创建此资源的控制器/用户。

{{< note >}}
从 v1.9 开始，这个标签被弃用。
{{< /note >}}

### app.kubernetes.io/instance {#app-kubernetes-io-instance}

示例：`app.kubernetes.io/instance: "mysql-abcxzy"`

用于：所有对象（通常用于[工作负载资源](/zh-cn/docs/reference/kubernetes-api/workload-resources/)）。

标识应用实例的唯一名称。要分配一个不唯一的名称，可使用 [app.kubernetes.io/name](#app-kubernetes-io-name)。

[推荐标签](/zh-cn/docs/concepts/overview/working-with-objects/common-labels/#labels)之一。

### app.kubernetes.io/managed-by {#app-kubernetes-io-manged-by}

示例：`app.kubernetes.io/managed-by: "helm"`

用于：所有对象（通常用于[工作负载资源](/zh-cn/docs/reference/kubernetes-api/workload-resources/)）。

用于管理应用操作的工具。

[推荐标签](/zh-cn/docs/concepts/overview/working-with-objects/common-labels/#labels)之一。

### app.kubernetes.io/name {#app-kubernetes-io-name}

示例：`app.kubernetes.io/name: "mysql"`

用于：所有对象（通常用于[工作负载资源](/zh-cn/docs/reference/kubernetes-api/workload-resources/)）。

应用的名称。

[推荐标签](/zh-cn/docs/concepts/overview/working-with-objects/common-labels/#labels)之一。

### app.kubernetes.io/part-of {#app-kubernetes-io-part-of}

示例：`app.kubernetes.io/part-of: "wordpress"`

用于：所有对象（通常用于[工作负载资源](/zh-cn/docs/reference/kubernetes-api/workload-resources/)）。

此应用所属的更高级别应用的名称。

[推荐标签](/zh-cn/docs/concepts/overview/working-with-objects/common-labels/#labels)之一。

### app.kubernetes.io/version {#app-kubernetes-io-version}

示例：`app.kubernetes.io/version: "5.7.21"`

用于：所有对象（通常用于[工作负载资源](/zh-cn/docs/reference/kubernetes-api/workload-resources/)）。

值的常见形式包括：

- [语义版本](https://semver.org/spec/v1.0.0.html)
- 针对源代码的 Git [修订哈希](https://git-scm.com/book/en/v2/Git-Tools-Revision-Selection#_single_revisions)。

[推荐标签](/zh-cn/docs/concepts/overview/working-with-objects/common-labels/#labels)之一。

### applyset.kubernetes.io/additional-namespaces (alpha) {#applyset-kubernetes-io-additional-namespaces}

示例：`applyset.kubernetes.io/additional-namespaces: "namespace1,namespace2"`

用于：作为 ApplySet 父对象使用的对象。

此注解处于 alpha 阶段。
对于 Kubernetes {{< skew currentVersion >}} 版本，如果定义它们的
{{< glossary_tooltip term_id="CustomResourceDefinition" text="CustomResourceDefinition" >}}
打了 `applyset.kubernetes.io/is-parent-type` 标签，
那么你可以在 Secret、ConfigMaps 或自定义资源上使用此注解。

规范的部分功能用来实现
[在 kubectl 中基于 ApplySet 的删除](/zh-cn/docs/tasks/manage-kubernetes-objects/declarative-config/#alternative-kubectl-apply-f-directory-prune)。
此注解应用于父对象，这些父对象用于跟踪 ApplySet 以将 ApplySet 的作用域扩展到父对象自己的命名空间(如果有的话)之外。
注解的值是以逗号分隔的命名空间的名字列表，不包含在其中找到对象的父命名空间。

### applyset.kubernetes.io/contains-group-resources (alpha) {#applyset-kubernetes-io-contains-group-resources}

示例：`applyset.kubernetes.io/contains-group-resources: "certificates.cert-manager.io,configmaps,deployments.apps,secrets,services"`

用于：作为 ApplySet 父对象使用的对象。

此注解处于 alpha 阶段。
对于 Kubernetes {{< skew currentVersion >}} 版本， 如果定义它们的
{{< glossary_tooltip term_id="CustomResourceDefinition" text="CustomResourceDefinition" >}}
打了 `applyset.kubernetes.io/is-parent-type` 标签，
那么你可以在 Secret、ConfigMaps 或自定义资源上使用此注解。

规范的部分功能用来实现
[在 kubectl 中基于 ApplySet 的删除](/zh-cn/docs/tasks/manage-kubernetes-objects/declarative-config/#alternative-kubectl-apply-f-directory-prune)。
此注解应用于父对象， 这些父对象用于跟踪 ApplySet 以优化 ApplySet 成员对象列表。
它在 AppySet 规范中是可选的，因为工具可以执行发现或使用不同的优化。
然而，对于 Kubernetes {{< skew currentVersion >}} 版本，它是 kubectl 必需的。
当存在时，注解的值必须是一个以逗号分隔的 group-kinds 列表，采用完全限定的名称格式，例如 `<resource>.<group>`。

### applyset.kubernetes.io/id (alpha) {#applyset-kubernetes-io-id}

示例：`applyset.kubernetes.io/id: "applyset-0eFHV8ySqp7XoShsGvyWFQD3s96yqwHmzc4e0HR1dsY-v1"`

用于：作为 ApplySet 父对象使用的对象。

此注解处于 alpha 阶段。
对于 Kubernetes {{< skew currentVersion >}} 版本， 如果定义它们的
{{< glossary_tooltip term_id="CustomResourceDefinition" text="CustomResourceDefinition" >}}
打了 `applyset.kubernetes.io/is-parent-type` 标签，那么你可以在 Secret、ConfigMaps 或自定义资源上使用此注解。

规范的部分功能用来实现
[在 kubectl 中基于 ApplySet 的删除](/zh-cn/docs/tasks/manage-kubernetes-objects/declarative-config/#alternative-kubectl-apply-f-directory-prune)。
此标签使对象成为 AppySet 父对象。
它的值是 ApplySet 的唯一 ID，该 ID 派生自父对象本身的标识。
该 ID **必须** 是所在对象的 group-kind-name-namespace 的 hash 的 base64 编码（使用 RFC4648 的 URL 安全编码），
格式为： `<base64(sha256(<name>.<namespace>.<kind>.<group>))>`。
此标签的值与对象 UID 之间没有关系。

### applyset.kubernetes.io/is-parent-type (alpha) {#applyset-kubernetes-io-is-parent-type}

示例：`applyset.kubernetes.io/is-parent-type: "true"`

用于：自定义资源 （CRD）

此注解处于 alpha 阶段。
规范的部分功能用来实现
[在 kubectl 中基于 ApplySet 的删除](/zh-cn/docs/tasks/manage-kubernetes-objects/declarative-config/#alternative-kubectl-apply-f-directory-prune)。
你可以在 {{< glossary_tooltip term_id="CustomResourceDefinition" text="CustomResourceDefinition" >}} (CRD) 上设置这个标签，
以将它定义的自定义资源类型(而不是 CRD 本身)标识为 ApplySet 的允许父类。
这个标签唯一允许的值是 `"true"`；如果你想将一个 CRD 标记为不是 ApplySet 的有效父级，请省略这个标签。

### applyset.kubernetes.io/part-of (alpha) {#applyset-kubernetes-io-part-of}

示例：`applyset.kubernetes.io/part-of: "applyset-0eFHV8ySqp7XoShsGvyWFQD3s96yqwHmzc4e0HR1dsY-v1"`

用于：所有对象。

此注解处于 alpha 阶段。
规范的部分功能用来实现
[在 kubectl 中基于 ApplySet 的删除](/zh-cn/docs/tasks/manage-kubernetes-objects/declarative-config/#alternative-kubectl-apply-f-directory-prune)。
此标签使对象成为 ApplySet 的成员。
标签的值 **必须** 与父对象上的 `applyset.kubernetes.io/id` 标签的值相匹配。

### applyset.kubernetes.io/tooling (alpha) {#applyset-kubernetes-io-tooling}

示例：`applyset.kubernetes.io/tooling: "kubectl/v{{< skew currentVersion >}}"`

用于：作为 ApplySet 父对象使用的对象。

此注解处于 alpha 阶段。
对于 Kubernetes {{< skew currentVersion >}} 版本， 如果定义它们的
{{< glossary_tooltip term_id="CustomResourceDefinition" text="CustomResourceDefinition" >}}
打了 `applyset.kubernetes.io/is-parent-type` 标签，那么你可以在 Secret、ConfigMaps 或自定义资源上使用此注解。

规范的部分功能用来实现
[在 kubectl 中基于 ApplySet 的删除](/zh-cn/docs/tasks/manage-kubernetes-objects/declarative-config/#alternative-kubectl-apply-f-directory-prune)。
此注解应用于父对象，这些父对象用于跟踪 ApplySet 以指示哪个工具管理 AppySet。
工具应该拒绝改变属于其他工具 ApplySets。
该值必须采用 `<toolname>/<semver>` 格式。

### cluster-autoscaler.kubernetes.io/safe-to-evict  {#cluster-autoscaler-safe-to-evict}

例子：`cluster-autoscaler.kubernetes.io/safe-to-evict: "true"`

用于：Pod

当这个注解设置为 `"true"` 时，即使其他规则通常会阻止驱逐操作，也会允许该集群自动扩缩器驱逐一个 Pod。
集群自动扩缩器从不驱逐将此注解显式设置为 `"false"` 的 Pod；你可以针对要保持运行的重要 Pod 设置此注解。
如果未设置此注解，则集群自动扩缩器将遵循其 Pod 级别的行为。


### config.kubernetes.io/local-config {#config-kubernetes-io-local-config}

例子：`config.kubernetes.io/local-config: "true"`

用于：所有对象

该注解用于清单中的对象，表示某对象是本地配置，不应提交到 Kubernetes API。
对于这个注解，当值为 "true" 时，表示该对象仅被客户端工具使用，不应提交到 API 服务器。
当值为 "false"，可以用来声明该对象应提交到 API 服务器，即使它是本地对象。

该注解是 Kubernetes 资源模型 (KRM) 函数规范的一部分，被 Kustomize 和其他类似的第三方工具使用。
例如，Kustomize 会从其最终构建输出中删除带有此注解的对象。


### internal.config.kubernetes.io/* (保留的前缀) {#internal.config.kubernetes.io-reserved-wildcard}

用于：所有对象

该前缀被保留，供遵从 Kubernetes 资源模型 (KRM) 函数规范的编排工具内部使用。
带有该前缀的注解仅在编排过程中使用，不会持久化到文件系统。
换句话说，编排工具应从本地文件系统读取文件时设置这些注解，并在将函数输出写回文件系统时删除它们。

除非特定注解另有说明，KRM 函数不得修改带有此前缀的注解。
这使得编排工具可以添加额外的内部注解，而不需要更改现有函数。


### internal.config.kubernetes.io/path {#internal-config-kubernetes-io-path}

例子：`internal.config.kubernetes.io/path: "relative/file/path.yaml"`

用于：所有对象

此注解记录了加载对象清单文件的（斜线分隔、与操作系统无关）相对路径。
该路径相对于文件系统上由编排工具确定的固定位置。

该注解是 Kubernetes 资源模型 (KRM) 函数规范的一部分，被 Kustomize 和其他类似的第三方工具使用。

KRM 函数**不应**在输入对象上修改此注解，除非它正在修改引用的文件。
KRM 函数**可以**在它所生成的对象上包含这个注解。


### internal.config.kubernetes.io/index {#internal-config-kubernetes-io-index}

例子：`internal.config.kubernetes.io/index: "2"`

用于：所有对象

该注解记录了包含对象的 YAML 文档在加载对象的清单文件中的零索引位置。
请注意，YAML 文档由三个破折号 (---) 分隔，每个文档可以包含一个对象。
如果未指定此注解，则该值为 0。

该注解是 Kubernetes 资源模型 (KRM) 函数规范的一部分，被 Kustomize 和其他类似的第三方工具使用。

KRM 函数**不应**在输入对象上修改此注解，除非它正在修改引用的文件。
KRM 函数**可以**在它所生成的对象上包含这个注解。


### kubernetes.io/arch {#kubernetes-io-arch}

例子：`kubernetes.io/arch: "amd64"`

用于：Node

Kubelet 使用 Go 定义的 `runtime.GOARCH` 填充它。如果你混合使用 ARM 和 X86 节点，这会很方便。


### kubernetes.io/os {#kubernetes-io-os}

例子：`kubernetes.io/os: "linux"`

用于：Node，Pod

对于节点，kubelet 会根据 Go 定义的 `runtime.GOOS` 填充这个值。
你可以很方便地在集群中混合使用操作系统（例如：混合使用 Linux 和 Windows 节点）。

你还可以在 Pod 上设置这个标签。
Kubernetes 允许你为此标签设置任何值；如果你使用此标签，
你应该将其设置为与该 Pod 实际使用的操作系统相对应的 Go `runtime.GOOS` 字符串。

当 Pod 的 kubernetes.io/os 标签值与节点上的标签值不匹配时，节点上的 kubelet 不会运行该 Pod。
但是，kube-scheduler 并未考虑这一点。
另外，如果你为 Pod 指定的操作系统与运行该 kubelet 的节点操作系统不相同，那么 kubelet 会拒绝运行该 Pod。
请查看 [Pod 操作系统](/zh-cn/docs/concepts/workloads/pods/#pod-os) 了解更多详情。

### kubernetes.io/metadata.name {#kubernetes-io-metadata-name}

例子：`kubernetes.io/metadata.name: "mynamespace"`

用于：Namespace

Kubernetes API 服务器（{{<glossary_tooltip text="控制平面" term_id="control-plane" >}} 的一部分）在所有 Namespace 上设置此标签。
标签值被设置 Namespace 的名称。你无法更改此标签的值。

如果你想使用标签{{<glossary_tooltip text="选择算符" term_id="selector" >}}定位特定 Namespace，这很有用。

### kubernetes.io/limit-ranger   {#kubernetes-io-limit-ranger}

例子：`kubernetes.io/limit-ranger: "LimitRanger plugin set: cpu, memory request for container nginx; cpu, memory limit for container nginx"`

用于：Pod

Kubernetes 默认不提供任何资源限制，这意味着除非你明确定义限制，否则你的容器将可以无限消耗 CPU 和内存。
你可以为 Pod 定义默认请求或默认限制。为此，你可以在相关命名空间中创建一个 LimitRange。
在你定义 LimitRange 后部署的 Pod 将受到这些限制。
注解 `kubernetes.io/limit-ranger` 记录了为 Pod 指定的资源默认值，以及成功应用这些默认值。
有关更多详细信息，请阅读 [LimitRanges](/zh-cn/docs/concepts/policy/limit-range)。

### addonmanager.kubernetes.io/mode

示例：`addonmanager.kubernetes.io/mode: "Reconcile"`

用于：所有对象。

要指定如何管理外接插件，你可以使用 `addonmanager.kubernetes.io/mode` 标签。
这个标签可以有三个标签之一：`Reconcile`，`EnsureExists`，或者 `Ignore`。

- `Reconcile`：插件资源将定期与预期状态协调。如果有任何差异，插件管理器将根据需要重新创建、重新配置或删除资源。如果没有指定标签， 此值是默认值。
- `EnsureExists`：插件资源将仅检查是否存在，但在创建后不会修改。当没有具有该名称的资源实例时，外接程序管理器将创建或重新创建资源。
- `Ignore`：插件资源将被忽略。此模式对于与外接插件管理器不兼容或由其他控制器管理的插件程序非常有用。

有关详细信息，请参见
[Addon-manager](https://github.com/kubernetes/kubernetes/blob/master/cluster/addons/addon-manager/README.md)

### beta.kubernetes.io/arch (已弃用) {#beta-kubernetes-io-arch}

此标签已被弃用。请改用 `kubernetes.io/arch`。

### beta.kubernetes.io/os (已弃用) {#beta-kubernetes-io-os}

此标签已被弃用。请改用 `kubernetes.io/os`。

### kube-aggregator.kubernetes.io/automanaged {#kube-aggregator-kubernetesio-automanaged}

例子：`kube-aggregator.kubernetes.io/automanaged: "onstart"`

用于：APIService

`kube-apiserver` 会在由 API 服务器自动创建的所有 APIService 对象上设置这个标签。
该标签标记了控制平面应如何管理该 APIService。你不应自行添加、修改或删除此标签。

{{< note >}}
当自动托管的 APIService 对象没有内置或自定义资源 API 对应于该 APIService 的 API 组/版本时，
它将被 kube-apiserver 删除。
{{< /note >}}

有两个可能的值：

- `onstart`：API 服务器应在启动时协调 APIService，但在其他时间不会进行协调。
- `true`：API 服务器应持续协调此 APIService。

### service.alpha.kubernetes.io/tolerate-unready-endpoints（已弃用）   {#service-alpha-kubernetes-io-tolerate-unready-endpoints-deprecated}

用于：StatefulSet

Service 上的这个注解表示 Endpoints 控制器是否应该继续为未准备好的 Pod 创建 Endpoints。
这些 Service 的 Endpoints 保留其 DNS 记录，并从 kubelet 启动 Pod 中的所有容器并将其标记为
**Running** 的那一刻起继续接收 Service 的流量，直到 kubelet 停止所有容器并从 API 服务器删除 Pod 为止。

### kubernetes.io/hostname {#kubernetesiohostname}

例子：`kubernetes.io/hostname: "ip-172-20-114-199.ec2.internal"`

用于：Node

Kubelet 使用主机名填充此标签。请注意，可以通过将 `--hostname-override` 标志传递给 `kubelet` 来替代“实际”主机名。

此标签也用作拓扑层次结构的一部分。有关详细信息，请参阅 [topology.kubernetes.io/zone](#topologykubernetesiozone)。

### kubernetes.io/change-cause {#change-cause}

例子：`kubernetes.io/change-cause: "kubectl edit --record deployment foo"`

用于：所有对象

此注解是对某些事物发生变更的原因的最佳猜测。

将 `--record` 添加到可能会更改对象的 `kubectl` 命令时会填充它。

### kubernetes.io/description {#description}

例子：`kubernetes.io/description: "Description of K8s object."`

用于：所有对象

此注解用于描述给定对象的特定行为。

### kubernetes.io/enforce-mountable-secrets {#enforce-mountable-secrets}

例子：`kubernetes.io/enforce-mountable-secrets: "true"`

用于：ServiceAccount

此注解的值必须为 **true** 才能生效。此注解表示作为此服务帐户运行的 Pod
只能引用在服务帐户的 `secrets` 字段中指定的 Secret API 对象。

### node.kubernetes.io/exclude-from-external-load-balancers   {#exclude-from-external-load-balancer}

例子：`node.kubernetes.io/exclude-from-external-load-balancers`

用于：Node

Kubernetes 自动在其创建的集群上启用 `ServiceNodeExclusion` 特性门控。
在一个集群上启用此特性门控后，你可以添加标签到特定的 Worker 节点，将这些节点从后端服务器列表排除在外。
以下命令可用于从后端集的后端服务器列表中排除一个 Worker 节点：

`kubectl label nodes <node-name> node.kubernetes.io/exclude-from-external-load-balancers=true`

### controller.kubernetes.io/pod-deletion-cost {#pod-deletion-cost}

例子：`controller.kubernetes.io/pod-deletion-cost: "10"`

用于：Pod

该注解用于设置
[Pod 删除成本](/zh-cn/docs/concepts/workloads/controllers/replicaset/#pod-deletion-cost)允许用户影响
ReplicaSet 缩减顺序。注解解析为 `int32` 类型。

### cluster-autoscaler.kubernetes.io/enable-ds-eviction {#enable-ds-eviction}

例子：`cluster-autoscaler.kubernetes.io/enable-ds-eviction: "true"`

用于：Pod

该注解控制 DaemonSet Pod 是否应由 ClusterAutoscaler 驱逐。
该注解需要在 DaemonSet 清单中的 DaemonSet Pod 上指定。
当该注解设为 `"true"` 时，即使其他规则通常会阻止驱逐，也将允许 ClusterAutoscaler 驱逐 DaemonSet Pod。
要取消允许 ClusterAutoscaler 驱逐 DaemonSet Pod，你可以为重要的 DaemonSet Pod 将该注解设为 `"false"`。
如果未设置该注解，则 Cluster Autoscaler 将遵循其整体行为（即根据其配置驱逐 DaemonSet）。

{{< note >}}
该注解仅影响 DaemonSet Pod。
{{< /note >}}

### kubernetes.io/ingress-bandwidth {#ingerss-bandwidth}

{{< note >}}
入站流量控制注解是一项实验性功能。
如果要启用流量控制支持，必须将 `bandwidth` 插件添加到 CNI 配置文件（默认为 `/etc/cni/net.d`）
并确保二进制文件包含在你的 CNI bin 目录中（默认为 `/opt/cni/bin`）。
{{< /note >}}

示例：`kubernetes.io/ingress-bandwidth: 10M`

用于：Pod

你可以对 Pod 应用服务质量流量控制并有效限制其可用带宽。
入站流量（到 Pod）通过控制排队的数据包来处理，以有效地处理数据。
要限制 Pod 的带宽，请编写对象定义 JSON 文件并使用 `kubernetes.io/ingress-bandwidth`
注解指定数据流量速度。用于指定入站的速率单位是每秒，
作为[量纲（Quantity）](/zh-cn/docs/reference/kubernetes-api/common-definitions/quantity/)。
例如，`10M` 表示每秒 10 兆比特。

### kubernetes.io/egress-bandwidth {#egress-bandwidth}

{{< note >}}
出站流量控制注解是一项实验性功能。
如果要启用流量控制支持，必须将 `bandwidth` 插件添加到 CNI 配置文件（默认为 `/etc/cni/net.d`）
并确保二进制文件包含在你的 CNI bin 目录中（默认为 `/opt/cni/bin`）。
{{< /note >}}

示例：`kubernetes.io/egress-bandwidth: 10M`

用于：Pod

出站流量（来自 pod）由策略控制，策略只是丢弃超过配置速率的数据包。
你为一个 Pod 所设置的限制不会影响其他 Pod 的带宽。
要限制 Pod 的带宽，请编写对象定义 JSON 文件并使用 `kubernetes.io/egress-bandwidth` 注解指定数据流量速度。
用于指定出站的速率单位是每秒比特数，
以[量纲（Quantity）](/zh-cn/docs/reference/kubernetes-api/common-definitions/quantity/)的形式给出。
例如，`10M` 表示每秒 10 兆比特。

### beta.kubernetes.io/instance-type (已弃用) {#beta-kubernetes-io-instance-type}

{{< note >}}
从 v1.17 开始，此标签已弃用，取而代之的是 [node.kubernetes.io/instance-type](#nodekubernetesioinstance-type)。
{{< /note >}}

### node.kubernetes.io/instance-type {#nodekubernetesioinstance-type}

例子：`node.kubernetes.io/instance-type: "m3.medium"`

用于：Node

Kubelet 使用 `cloudprovider` 定义的实例类型填充它。
仅当你使用 `cloudprovider` 时才会设置此项。如果你希望将某些工作负载定位到某些实例类型，则此设置非常方便，
但通常你希望依靠 Kubernetes 调度程序来执行基于资源的调度。
你应该基于属性而不是实例类型来调度（例如：需要 GPU，而不是需要 `g2.2xlarge`）。

### failure-domain.beta.kubernetes.io/region (已弃用) {#failure-domainbetakubernetesioregion}

请参阅 [topology.kubernetes.io/region](#topologykubernetesioregion)。

{{< note >}}
从 v1.17 开始，此标签已弃用，取而代之的是 [topology.kubernetes.io/region](#topologykubernetesioregion)。
{{</note>}}

### failure-domain.beta.kubernetes.io/zone (已弃用) {#failure-domainbetakubernetesiozone}

请参阅 [topology.kubernetes.io/zone](#topologykubernetesiozone)。

{{< note >}}
从 v1.17 开始，此标签已弃用，取而代之的是 [topology.kubernetes.io/zone](#topologykubernetesiozone)。
{{</note>}}

### pv.kubernetes.io/bind-completed {#pv-kubernetesiobind-completed}

例子：`pv.kubernetes.io/bind-completed: "yes"`

用于：PersistentVolumeClaim

当在 PersistentVolumeClaim (PVC) 上设置此注解时，表示 PVC 的生命周期已通过初始绑定设置。
当存在此注解时，该信息会改变控制平面解释 PVC 对象状态的方式。此注解的值对 Kubernetes 无关紧要。

### pv.kubernetes.io/bound-by-controller {#pv-kubernetesioboundby-controller}

例子：`pv.kubernetes.io/bound-by-controller: "yes"`

用于：PersistentVolume、PersistentVolumeClaim

如果此注解设置在 PersistentVolume 或 PersistentVolumeClaim 上，则表示存储绑定
（PersistentVolume → PersistentVolumeClaim，或 PersistentVolumeClaim → PersistentVolume）
已由{{< glossary_tooltip text="控制器" term_id="controller" >}}配置完毕。
如果未设置此注解，且存在存储绑定，则缺少该注解意味着绑定是手动完成的。此注解的值无关紧要。

### pv.kubernetes.io/provisioned-by {#pv-kubernetesiodynamically-provisioned}

例子：`pv.kubernetes.io/provisioned-by: "kubernetes.io/rbd"`

用于：PersistentVolume

此注解被添加到已由 Kubernetes 动态制备的 PersistentVolume (PV)。
它的值是创建卷的卷插件的名称。它同时服务于用户（显示 PV 的来源）和 Kubernetes（识别其决策中动态制备的 PV）。

### pv.kubernetes.io/migrated-to {#pv-kubernetesio-migratedto}

例子：`pv.kubernetes.io/migrated-to: pd.csi.storage.gke.io`

用于：PersistentVolume、PersistentVolumeClaim

它被添加到 PersistentVolume (PV) 和 PersistentVolumeClaim (PVC)，应该由其相应的 CSI
驱动程序通过 `CSIMigration` 特性门控动态制备/删除。设置此注解后，Kubernetes 组件将“停止”，
而 `external-provisioner` 将作用于对象。

### statefulset.kubernetes.io/pod-name {#statefulsetkubernetesiopod-name}

例子：`statefulset.kubernetes.io/pod-name: "mystatefulset-7"`

当 StatefulSet 控制器为 StatefulSet 创建 Pod 时，控制平面会在该 Pod 上设置此标签。标签的值是正在创建的 Pod 的名称。

有关详细信息，请参阅 StatefulSet 主题中的 [Pod 名称标签](/zh-cn/docs/concepts/workloads/controllers/statefulset/#pod-name-label)。

### scheduler.alpha.kubernetes.io/node-selector {#schedulerkubernetesnode-selector}

例子：`scheduler.alpha.kubernetes.io/node-selector: "name-of-node-selector"`

用于：Namespace

[PodNodeSelector](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#podnodeselector) 
使用此注解键为名字空间中的 Pod 设置节点选择算符。

### topology.kubernetes.io/region {#topologykubernetesioregion}

例子：`topology.kubernetes.io/region: "us-east-1"`

请参阅 [topology.kubernetes.io/zone](#topologykubernetesiozone)。

### topology.kubernetes.io/zone {#topologykubernetesiozone}

例子：`topology.kubernetes.io/zone: "us-east-1c"`

用于：Node、PersistentVolume

在 Node 上：`kubelet` 或外部 `cloud-controller-manager` 使用 `cloudprovider` 提供的信息填充它。
仅当你使用 `cloudprovider` 时才会设置此项。
但是，如果它在你的拓扑中有意义，你应该考虑在 Node 上设置它。

在 PersistentVolume 上：拓扑感知卷配置器将自动在 `PersistentVolume` 上设置 Node 亲和性约束。

一个 Zone 代表一个逻辑故障域。Kubernetes 集群通常跨越多个 Zone 以提高可用性。虽然 Zone 的确切定义留给基础设施实现，
但 Zone 的常见属性包括 Zone 内非常低的网络延迟、Zone 内的免费网络流量以及与其他 Zone 的故障独立性。
例如，一个 Zone 内的 Node 可能共享一个网络交换机，但不同 Zone 中的 Node 无法共享交换机。

一个 Region 代表一个更大的域，由一个或多个 Zone 组成。Kubernetes 集群跨多个 Region 并不常见，
虽然 Zone 或 Region 的确切定义留给基础设施实现，
但 Region 的共同属性包括它们之间的网络延迟比它们内部更高，它们之间的网络流量成本非零，
以及与其他 Zone 或 Region 的故障独立性。
例如，一个 Region 内的 Node 可能共享电力基础设施（例如 UPS 或发电机），但不同 Region 的 Node 通常不会共享电力基础设施。

Kubernetes 对 Zone 和 Region 的结构做了一些假设：

1. Zone 和 Region 是分层的：Zone 是 Region 的严格子集，没有 Zone 可以在两个 Region 中；

2. Zone 名称跨 Region 是唯一的；例如，Region “africa-east-1” 可能由 Zone “africa-east-1a”
   和 “africa-east-1b” 组成。

你可以大胆假设拓扑标签不会改变。尽管严格地讲标签是可变的，
但节点的用户可以假设给定节点只能通过销毁和重新创建才能完成 Zone 间移动。

Kubernetes 可以通过多种方式使用这些信息。例如，调度程序会自动尝试将 ReplicaSet 中的 Pod
分布在单 Zone 集群中的多个节点上（以便减少节点故障的影响，请参阅 [kubernetes.io/hostname](#kubernetesiohostname)）。
对于多 Zone 集群，这种分布行为也适用于 Zone（以减少 Zone 故障的影响）。
Zone 级别的 Pod 分布是通过 **SelectorSpreadPriority** 实现的。

**SelectorSpreadPriority** 是一个尽力而为的放置机制。如果集群中的 Zone 是异构的
（例如：节点数量不同、节点类型不同或 Pod 资源需求有别等），这种放置机制可能会让你的
Pod 无法实现跨 Zone 均匀分布。
如果需要，你可以使用同质 Zone（节点数量和类型均相同）来减少不均匀分布的可能性。

调度程序还将（通过 **VolumeZonePredicate** 条件）确保申领给定卷的 Pod 仅被放置在与该卷相同的 Zone 中。
卷不能跨 Zone 挂接。

你应该考虑手动添加标签（或添加对 `PersistentVolumeLabel` 的支持）。
基于 `PersistentVolumeLabel`，调度程序可以防止 Pod 挂载来自其他 Zone 的卷。
如果你的基础架构没有此限制，则不需要将 Zone 标签添加到卷上。

### volume.beta.kubernetes.io/storage-provisioner (已弃用) {#volume-beta-kubernetes-io-storage-provisioner}

例子：`volume.beta.kubernetes.io/storage-provisioner: "k8s.io/minikube-hostpath"`

用于：PersistentVolumeClaim

此注解已被弃用。

### volume.beta.kubernetes.io/storage-class（已弃用）   {#volume-beta-storage-class}

例子：`volume.beta.kubernetes.io/storage-class: "example-class"`

用于：PersistentVolume、PersistentVolumeClaim

此注解可以为 PersistentVolume (PV) 或 PersistentVolumeClaim (PVC) 指定
[StorageClass](/zh-cn/docs/concepts/storage/storage-classes/)。
当 `storageClassName` 属性和 `volume.beta.kubernetes.io/storage-class` 注解均被指定时，
注解 `volume.beta.kubernetes.io/storage-class` 将优先于 `storageClassName` 属性。

此注解已被弃用。作为替代方案，你应该为 PersistentVolumeClaim 或 PersistentVolume 设置
[`storageClassName` 字段](/zh-cn/docs/concepts/storage/persistent-volumes/#class)。

### volume.beta.kubernetes.io/mount-options（已弃用） {#mount-options}

例子：`volume.beta.kubernetes.io/mount-options: "ro,soft"`

用于：PersistentVolume

针对 PersistentVolume 挂载到一个节点上的情形，
Kubernetes 管理员可以指定更多的[挂载选项](/zh-cn/docs/concepts/storage/persistent-volumes/#mount-options)。

该注解已弃用。

### volume.kubernetes.io/storage-provisioner {#volume-kubernetes-io-storage-provisioner}

用于：PersistentVolumeClaim

此注解将被添加到根据需要动态制备的 PVC 上。

### volume.kubernetes.io/selected-node   {#selected-node}

用于：PersistentVolumeClaim

此注解被添加到调度程序所触发的 PVC 上，对应的 PVC 需要被动态制备。注解值是选定节点的名称。

### volumes.kubernetes.io/controller-managed-attach-detach   {#controller-managed-attach-detach}

用于：Node

如果节点已在其自身上设置了注解 `volumes.kubernetes.io/controller-managed-attach-detach`，
那么它的存储挂接和解除挂接的操作是交由运行在
{{< glossary_tooltip term_id="kube-controller-manager" text="kube-controller-manager" >}}
中的**卷挂接/解除挂接**{{< glossary_tooltip text="控制器" term_id="controller" >}}来管理的。

注解的值并不重要；如果节点上存在该注解，则由控制器管理存储挂接和解除挂接的操作。

### node.kubernetes.io/windows-build {#nodekubernetesiowindows-build}

例子：`node.kubernetes.io/windows-build: "10.0.17763"`

用于：Node

当 kubelet 在 Microsoft Windows 上运行时，它会自动标记其所在节点以记录所使用的 Windows Server 的版本。

标签的值采用 “MajorVersion.MinorVersion.BuildNumber” 格式。

### service.kubernetes.io/headless {#servicekubernetesioheadless}

例子：`service.kubernetes.io/headless: ""`

用于：Service

当拥有的 Service 是无头类型时，控制平面将此标签添加到 Endpoints 对象。

### kubernetes.io/service-name {#kubernetesioservice-name}

例子：`kubernetes.io/service-name: "my-website"`

用于：EndpointSlice

Kubernetes 使用这个标签将
[EndpointSlices](/zh-cn/docs/concepts/services-networking/endpoint-slices/)
与[服务](/zh-cn/docs/concepts/services-networking/service/)关联。

这个标签记录了 EndpointSlice 后备服务的{{< glossary_tooltip term_id="name" text="名称">}}。
所有 EndpointSlice 都应将此标签设置为其关联服务的名称。

### kubernetes.io/service-account.name {#service-account-name}

示例：`kubernetes.io/service-account.name: "sa-name"`

用于：Secret

这个注解记录了令牌（存储在 `kubernetes.io/service-account-token` 类型的 Secret 中）所代表的
ServiceAccount 的{{<glossary_tooltip term_id="name" text="名称">}}。

### kubernetes.io/service-account.uid {#service-account-uid}

示例：`kubernetes.io/service-account.uid: da68f9c6-9d26-11e7-b84e-002dc52800da`

用于：Secret

该注解记录了令牌（存储在 `kubernetes.io/service-account-token` 类型的 Secret 中）所代表的
ServiceAccount 的{{<glossary_tooltip term_id="uid" text="唯一 ID" >}}。

### kubernetes.io/legacy-token-last-used

例子：`kubernetes.io/legacy-token-last-used: 2022-10-24`

用于：Secret

控制面仅为 `kubernetes.io/service-account-token` 类型的 Secret 添加此标签。
该标签的值记录着控制面最近一次接到客户端使用服务帐户令牌进行身份验证请求的日期（ISO 8601
格式，UTC 时区）

如果上一次使用老的令牌的时间在集群获得此特性（添加于 Kubernetes v1.26）之前，则不会设置此标签。

### endpointslice.kubernetes.io/managed-by {#endpointslicekubernetesiomanaged-by}

例子：`endpointslice.kubernetes.io/managed-by: "controller"`

用于：EndpointSlice

用于标示管理 EndpointSlice 的控制器或实体。该标签旨在使不同的 EndpointSlice
对象能够由同一集群内的不同控制器或实体管理。

### endpointslice.kubernetes.io/skip-mirror {#endpointslicekubernetesioskip-mirror}

例子：`endpointslice.kubernetes.io/skip-mirror: "true"`

用于：Endpoints

可以在 Endpoints 资源上将此标签设置为 `"true"`，以指示 EndpointSliceMirroring
控制器不应使用 EndpointSlice 镜像此 Endpoints 资源。

### service.kubernetes.io/service-proxy-name {#servicekubernetesioservice-proxy-name}

例子：`service.kubernetes.io/service-proxy-name: "foo-bar"`

用于：Service

kube-proxy 自定义代理会使用这个标签，它将服务控制委托给自定义代理。

### experimental.windows.kubernetes.io/isolation-type (已弃用) {#experimental-windows-kubernetes-io-isolation-type}

例子：`experimental.windows.kubernetes.io/isolation-type: "hyperv"`

用于：Pod

注解用于运行具有 Hyper-V 隔离的 Windows 容器。要使用 Hyper-V 隔离功能并创建 Hyper-V
隔离容器，kubelet 启动时应该需要设置特性门控 HyperVContainer=true。

{{< note >}}
你只能在具有单个容器的 Pod 上设置此注解。
从 v1.20 开始，此注解已弃用。1.21 中删除了实验性 Hyper-V 支持。
{{</note>}}

### ingressclass.kubernetes.io/is-default-class {#ingressclass-kubernetes-io-is-default-class}

例子：`ingressclass.kubernetes.io/is-default-class: "true"`

用于：IngressClass

当单个 IngressClass 资源将此注解设置为 `"true"`时，新的未指定 Ingress 类的 Ingress
资源将被设置为此默认类。

### kubernetes.io/ingress.class (已弃用) {#kubernetes-io-ingress-class}

{{< note >}}
从 v1.18 开始，不推荐使用此注解以鼓励使用 `spec.ingressClassName`。
{{</note>}}

### storageclass.kubernetes.io/is-default-class {#storageclass-kubernetes-io-is-default-class}

例子：`ingressclass.kubernetes.io/is-default-class: "true"`

用于：StorageClass

当单个 StorageClass 资源将此注解设置为 `"true"` 时，新的未指定存储类的 PersistentVolumeClaim
资源将被设置为此默认类。

### alpha.kubernetes.io/provided-node-ip {#alpha-kubernetes-io-provided-node-ip}

例子：`alpha.kubernetes.io/provided-node-ip: "10.0.0.1"`

用于：Node

kubelet 可以在 Node 上设置此注解来表示其配置的 IPv4 地址。

如果 kubelet 被启动时 `--cloud-provider` 标志设置为任一云驱动（包括外部云驱动和传统树内云驱动）
kubelet 会在 Node 上设置此注解以表示从命令行标志（`--node-ip`）设置的 IP 地址。
云控制器管理器通过云驱动验证此 IP 是否有效。

### batch.kubernetes.io/job-completion-index {#batch-kubernetes-io-job-completion-index}

例子：`batch.kubernetes.io/job-completion-index: "3"`

用于：Pod

kube-controller-manager 中的 Job 控制器为使用 Indexed
[完成模式](/zh-cn/docs/concepts/workloads/controllers/job/#completion-mode)创建的 Pod
设置此注解。

### kubectl.kubernetes.io/default-container {#kubectl-kubernetes-io-default-container}

例子：`kubectl.kubernetes.io/default-container: "front-end-app"`

此注解的值是此 Pod 的默认容器名称。例如，未指定 `-c` 或 `--container` 标志时执行
`kubectl logs` 或 `kubectl exec` 命令将使用此默认容器。

### kubectl.kubernetes.io/default-logs-container（已弃用）   {#default-logs-container}

例子：`kubectl.kubernetes.io/default-logs-container: "front-end-app"`

此注解的值是针对此 Pod 的默认日志记录容器的名称。例如，不带 `-c` 或 `--container`
标志的 `kubectl logs` 将使用此默认容器。

{{< note >}}
此注解已被弃用。取而代之的是使用
[`kubectl.kubernetes.io/default-container`](#kubectl-kubernetes-io-default-container) 注解。
Kubernetes v1.25 及更高版本将忽略此注解。
{{< /note >}}

### endpoints.kubernetes.io/over-capacity {#endpoints-kubernetes-io-over-capacity}

例子：`endpoints.kubernetes.io/over-capacity:truncated`

用于：Endpoints

如果关联的 {{< glossary_tooltip term_id="service" >}} 有超过 1000 个后备端点，
则{{< glossary_tooltip text="控制平面" term_id="control-plane" >}}将此注解添加到
[Endpoints](/zh-cn/docs/concepts/services-networking/service/#endpoints) 对象。
此注解表示 Endpoints 对象已超出容量，并且已将 Endpoints 数截断为 1000。

如果后端端点的数量低于 1000，则控制平面将移除此注解。

### batch.kubernetes.io/job-tracking (已弃用) {#batch-kubernetes-io-job-tracking}

例子：`batch.kubernetes.io/job-tracking: ""`

用于：Job

Job 上存在此注解表明控制平面正在[使用 Finalizer 追踪 Job](/zh-cn/docs/concepts/workloads/controllers/job/#job-tracking-with-finalizers)。
控制平面使用此注解来安全地转换为使用 Finalizer 追踪 Job，而此特性正在开发中。
你 **不** 可以手动添加或删除此注解。

{{< note >}}
从 Kubernetes 1.26 开始，该注解被弃用。
Kubernetes 1.27 及以上版本将忽略此注解，并始终使用 Finalizer 追踪 Job。
{{< /note >}}

### job-name (deprecated) {#job-name}

示例：`job-name: "pi"`

用于：由 Jobs 控制的 Jobs 和 Pods

{{< note >}}
由 Kubernetes 1.27 开始，本标签被弃用。
Kubernetes 1.27 及更高版本忽略这个标签，改为具有 `job-name` 前缀的标签。
{{< /note >}}

### controller-uid (deprecated) {#controller-uid}

示例：`controller-uid: "$UID"`

用于：由 Jobs 控制的 Jobs 和 Pods

{{< note >}}
由 Kubernetes 1.27 开始，本标签被弃用。
Kubernetes 1.27 及更高版本忽略这个标签，改为具有 `controller-uid` 前缀的标签。
{{< /note >}}

### batch.kubernetes.io/job-name {#batchkubernetesio-job-name}

示例：`batch.kubernetes.io/job-name: "pi"`

用于：由 Jobs 控制的 Jobs 和 Pods

这个标签被用作一种用户友好的方式来获得与某个 Job 相对应的 Pods。
`job-name` 来自 Job 的 `name` 并且允许以一种简单的方式获得与 Job 对应的 Pods。

### batch.kubernetes.io/controller-uid {#batchkubernetesio-controller-uid}

示例：`batch.kubernetes.io/controller-uid: "$UID"`

用于：由 Jobs 控制的 Jobs 和 Pods

这个标签被用作一种编程方式来获得对应于某个 Job 的所有 Pods。
`controller-uid` 是在 `selector` 字段中设置的唯一标识符，
因此 Job 控制器可以获取所有对应的 Pods。

### scheduler.alpha.kubernetes.io/defaultTolerations {#scheduleralphakubernetesio-defaulttolerations}

例子：`scheduler.alpha.kubernetes.io/defaultTolerations: '[{"operator": "Equal", "value": "value1", "effect": "NoSchedule", "key": "dedicated-node"}]'`

用于：Namespace

此注解需要启用
[PodTolerationRestriction](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#podtolerationrestriction)
准入控制器。此注解键允许为某个命名空间分配容忍度，在这个命名空间中创建的所有新 Pod 都会被添加这些容忍度。

### scheduler.alpha.kubernetes.io/tolerationsWhitelist {#schedulerkubernetestolerations-whitelist}

示例：`scheduler.alpha.kubernetes.io/tolerationsWhitelist: '[{"operator": "Exists", "effect": "NoSchedule", "key": "dedicated-node"}]'`

用于：命名空间

此注解只有在启用（alpha）
[PodTolerationRestriction](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#podtolerationrestriction)
控制器时才生效。
注解值是一个 JSON 文档，它为它所注解的命名空间定义了一个允许容忍的列表。
当你创建一个 Pod 或修改其容忍度时，API 服务器将检查容忍度，以查看它们是否在允许列表中。
只有在检查成功的情况下，Pod 才被允操作。

### scheduler.alpha.kubernetes.io/preferAvoidPods（已弃用） {#scheduleralphakubernetesio-preferavoidpods}

用于：Node

此注解需要启用 [NodePreferAvoidPods 调度插件](/zh-cn/docs/reference/scheduling/config/#scheduling-plugins)。
该插件自 Kubernetes 1.22 起已被弃用。
请改用[污点和容忍度](/zh-cn/docs/concepts/scheduling-eviction/taint-and-toleration/)。

**下面列出的污点总是在 Node 上使用**

### node.kubernetes.io/not-ready {#node-kubernetes-io-not-ready}

例子：`node.kubernetes.io/not-ready: "NoExecute"`

Node 控制器通过监控 Node 的健康状况来检测 Node 是否准备就绪，并相应地添加或删除此污点。

### node.kubernetes.io/unreachable {#node-kubernetes-io-unreachable}

例子：`node.kubernetes.io/unreachable: "NoExecute"`

Node 控制器将此污点添加到对应[节点状况](/zh-cn/docs/concepts/architecture/nodes/#condition)`Ready`
为 `Unknown` 的 Node 上。

### node.kubernetes.io/unschedulable {#node-kubernetes-io-unschedulable}

例子：`node.kubernetes.io/unschedulable: "NoSchedule"`

在初始化 Node 期间，为避免竞争条件，此污点将被添加到 Node 上。

### node.kubernetes.io/memory-pressure {#node-kubernetes-io-memory-pressure}

例子：`node.kubernetes.io/memory-pressure: "NoSchedule"`

kubelet 根据在 Node 上观察到的 `memory.available` 和 `allocatableMemory.available` 检测内存压力。
然后将观察到的值与可以在 kubelet 上设置的相应阈值进行比较，以确定是否应添加/删除 Node 状况和污点。

### node.kubernetes.io/disk-pressure {#node-kubernetes-io-disk-pressure}

例子：`node.kubernetes.io/disk-pressure :"NoSchedule"`

kubelet 根据在 Node 上观察到的 `imagefs.available`、`imagefs.inodesFree`、`nodefs.available`
和 `nodefs.inodesFree`（仅限 Linux ）检测磁盘压力。
然后将观察到的值与可以在 kubelet 上设置的相应阈值进行比较，以确定是否应添加/删除 Node 状况和污点。

### node.kubernetes.io/network-unavailable {#node-kubernetes-io-network-unavailable}

例子：`node.kubernetes.io/network-unavailable: "NoSchedule"`

当使用的云驱动指示需要额外的网络配置时，此注解最初由 kubelet 设置。
只有云上的路由被正确地配置了，此污点才会被云驱动移除

### node.kubernetes.io/pid-pressure {#node-kubernetes-io-pid-pressure}

例子：`node.kubernetes.io/pid-pressure: "NoSchedule"`

kubelet 检查 `/proc/sys/kernel/pid_max` 大小的 D 值和 Kubernetes 在 Node 上消耗的 PID，
以获取可用 PID 数量，并将其作为 `pid.available` 指标值。
然后该指标与在 kubelet 上设置的相应阈值进行比较，以确定是否应该添加/删除 Node 状况和污点。

### node.kubernetes.io/out-of-service {#out-of-service}
例子：`node.kubernetes.io/out-of-service:NoExecute`

用户可以手动将污点添加到节点，将其标记为停止服务。
如果 `kube-controller-manager` 上启用了 `NodeOutOfServiceVolumeDetach`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)，
并且一个节点被这个污点标记为停止服务，如果节点上的 Pod 没有对应的容忍度，
这类 Pod 将被强制删除，并且，针对在节点上被终止 Pod 的卷分离操作将被立即执行。

{{< caution >}}
有关何时以及如何使用此污点的更多详细信息，请参阅[非正常节点关闭](/zh-cn/docs/concepts/architecture/nodes/#non-graceful-node-shutdown)。
{{< /caution >}}

### node.cloudprovider.kubernetes.io/uninitialized {#node-cloudprovider-kubernetes-io-shutdown}

例子：`node.cloudprovider.kubernetes.io/uninitialized: "NoSchedule"`

在使用“外部”云驱动启动 kubelet 时，在 Node 上设置此污点以将其标记为不可用，直到来自
cloud-controller-manager 的控制器初始化此 Node，然后移除污点。

### node.cloudprovider.kubernetes.io/shutdown {#node-cloudprovider-kubernetes-io-shutdown}

例子：`node.cloudprovider.kubernetes.io/shutdown: "NoSchedule"`

如果 Node 处于云驱动所指定的关闭状态，则 Node 会相应地被设置污点，对应的污点和效果为
`node.cloudprovider.kubernetes.io/shutdown` 和 `NoSchedule`。

### feature.node.kubernetes.io/*
用于：节点
示例：`feature.node.kubernetes.io/network-sriov.capable: "true"`

这些特性作为标签在运行 NFD 的节点上的 KubernetesNode 对象中公布。
所有内置的标签都使用 feature.node.kubernetes.io 标签命名空间，并且格式为
`feature.node.kubernetes.io/<feature-name>: <true>`。
NFD 有许多用于创建特定于供应商和应用程序的标签的扩展点。
有关详细信息，请参阅 [定制资源](https://kubernetes-sigs.github.io/node-feature-discovery/v0.12/usage/customization-guide).

### nfd.node.kubernetes.io/master.version

示例：`nfd.node.kubernetes.io/master.version: "v0.6.0"`

用于：节点

对于调度 NFD-[master](https://kubernetes-sigs.github.io/node-feature-discovery/stable/usage/nfd-master.html)的节点，
此注解记录 NFD-master 的版本。
它仅用于提供信息。

### nfd.node.kubernetes.io/worker.version

示例：`nfd.node.kubernetes.io/worker.version: "v0.4.0"`

用于：节点

这个注解记录 NFD-[worker](https://kubernetes-sigs.github.io/node-feature-discovery/stable/usage/nfd-worker.html)
的版本(如果在节点上运行了一个 NFD-worker 的话)。
它只用于提供信息。

<--
### nfd.node.kubernetes.io/feature-labels

Example: `nfd.node.kubernetes.io/feature-labels: "cpu-cpuid.ADX,cpu-cpuid.AESNI,cpu-hardware_multithreading,kernel-version.full"`

Used on: Nodes

This annotation records a comma-separated list of node feature labels managed by
[Node Feature Discovery](https://kubernetes-sigs.github.io/node-feature-discovery/) (NFD).
NFD uses this for an internal mechanism. You should not edit this annotation yourself.
-->
### nfd.node.kubernetes.io/feature-labels

示例：`nfd.node.kubernetes.io/feature-labels: "cpu-cpuid.ADX,cpu-cpuid.AESNI,cpu-hardware_multithreading,kernel-version.full"`

用于：节点

此注解记录由 [Node Feature Discovery](https://kubernetes-sigs.github.io/node-feature-discovery/) (NFD) 管理的以逗号分隔的节点特性标签列表。
NFD 将其用于内部机制。
你不应该自己编辑这个注释。

### nfd.node.kubernetes.io/extended-resources

示例：`nfd.node.kubernetes.io/extended-resources: "accelerator.acme.example/q500,example.com/coprocessor-fx5"`

用于：节点

此注解记录由 [Node Feature Discovery](https://kubernetes-sigs.github.io/node-feature-discovery/) (NFD)
管理的以逗号分隔的 [扩展资源](/zh-cn/docs/concepts/configuration/manage-resources-containers/#extended-resources) 列表。
NFD 将其用于内部机制。
你不应该自己编辑这个注释。

{{< note >}}
这些注释仅适用于运行 NFD 的节点。
要了解更多关于 NFD 及其组件的信息，请访问其官方文档
[文档](https://kubernetes-sigs.github.io/node-feature-discovery/stable/get-started/).
{{< /note >}}

### pod-security.kubernetes.io/enforce {#pod-security-kubernetes-io-enforce}

例子：`pod-security.kubernetes.io/enforce: "baseline"`

用于：Namespace

值**必须**是 `privileged`、`baseline` 或 `restricted` 之一，它们对应于
[Pod 安全标准](/zh-cn/docs/concepts/security/pod-security-standards) 级别。
特别地，`enforce` 标签 **禁止** 在带标签的 Namespace 中创建任何不符合指示级别要求的 Pod。

请请参阅[在名字空间级别实施 Pod 安全性](/zh-cn/docs/concepts/security/pod-security-admission)了解更多信息。

### pod-security.kubernetes.io/enforce-version {#pod-security-kubernetes-io-enforce-version}

例子：`pod-security.kubernetes.io/enforce-version: "{{< skew currentVersion >}}"`

用于：Namespace

值**必须**是 `latest` 或格式为 `v<MAJOR>.<MINOR>` 的有效 Kubernetes 版本。
此注解决定了在验证提交的 Pod 时要应用的
[Pod 安全标准](/zh-cn/docs/concepts/security/pod-security-standards)策略的版本。

请参阅[在名字空间级别实施 Pod 安全性](/zh-cn/docs/concepts/security/pod-security-admission)了解更多信息。

### pod-security.kubernetes.io/audit {#pod-security-kubernetes-io-audit}

例子：`pod-security.kubernetes.io/audit: "baseline"`

用于：Namespace

值**必须**是与 [Pod 安全标准](/zh-cn/docs/concepts/security/pod-security-standards) 级别相对应的
`privileged`、`baseline` 或 `restricted` 之一。
具体来说，`audit` 标签不会阻止在带标签的 Namespace 中创建不符合指示级别要求的 Pod，
但会向该 Pod 添加审计注解。

请参阅[在名字空间级别实施 Pod 安全性](/zh-cn/docs/concepts/security/pod-security-admission)了解更多信息。

### pod-security.kubernetes.io/audit-version {#pod-security-kubernetes-io-audit-version}

例子：`pod-security.kubernetes.io/audit-version: "{{< skew currentVersion >}}"`

用于：Namespace

值**必须**是 `latest` 或格式为 `v<MAJOR>.<MINOR>` 的有效 Kubernetes 版本。
此注解决定了在验证提交的 Pod 时要应用的
[Pod 安全标准](/zh-cn/docs/concepts/security/pod-security-standards)策略的版本。

请参阅[在名字空间级别实施 Pod 安全性](/zh-cn/docs/concepts/security/pod-security-admission)了解更多信息。

### pod-security.kubernetes.io/warn {#pod-security-kubernetes-io-warn}

例子：`pod-security.kubernetes.io/warn: "baseline"`

用于：Namespace

值**必须**是与 [Pod 安全标准](/zh-cn/docs/concepts/security/pod-security-standards)级别相对应的
`privileged`、`baseline` 或 `restricted` 之一。特别地，
`warn` 标签不会阻止在带标签的 Namespace 中创建不符合指示级别概述要求的 Pod，但会在这样做后向用户返回警告。
请注意，在创建或更新包含 Pod 模板的对象时也会显示警告，例如 Deployment、Jobs、StatefulSets 等。

请参阅[在名字空间级别实施 Pod 安全性](/zh-cn/docs/concepts/security/pod-security-admission)了解更多信息。

### pod-security.kubernetes.io/warn-version {#pod-security-kubernetes-io-warn-version}

例子：`pod-security.kubernetes.io/warn-version: "{{< skew currentVersion >}}"`

用于：Namespace

值**必须**是 `latest` 或格式为 `v<MAJOR>.<MINOR>` 的有效 Kubernetes 版本。
此注解决定了在验证提交的 Pod 时要应用的 [Pod 安全标准](/zh-cn/docs/concepts/security/pod-security-standards)策略的版本。
请注意，在创建或更新包含 Pod 模板的对象时也会显示警告，
例如 Deployment、Jobs、StatefulSets 等。

请参阅[在名字空间级别实施 Pod 安全性](/zh-cn/docs/concepts/security/pod-security-admission)了解更多信息。

### rbac.authorization.kubernetes.io/autoupdate

例子：`rbac.authorization.kubernetes.io/autoupdate: "false"`

用于：ClusterRole、ClusterRoleBinding、Role、RoleBinding

当在 kube-apiserver 创建的默认 RBAC 对象上将此注解设置为 `"true"` 时，
这些对象会在服务器启动时自动更新以添加缺少的权限和主体（额外的权限和主体留在原处）。
要防止自动更新特定的 Role 或 RoleBinding，请将此注解设置为 `"false"`。
如果你创建自己的 RBAC 对象并将此注解设置为 `"false"`，则 `kubectl auth reconcile`
（允许协调在{{< glossary_tooltip text="清单" term_id="manifest" >}}中给出的任意 RBAC 对象）
尊重此注解并且不会自动添加缺少的权限和主体。

### kubernetes.io/psp（已弃用） {#kubernetes-io-psp}

例如：`kubernetes.io/psp: restricted`

用于：Pod

这个注解只在你使用 [PodSecurityPolicies](/zh-cn/docs/concepts/security/pod-security-policy/) 时才有意义。
Kubernetes v{{< skew currentVersion >}} 不支持 PodSecurityPolicy API。

当 PodSecurityPolicy 准入控制器接受一个 Pod 时，会修改该 Pod，并给这个 Pod 添加此注解。
注解的值是用来对 Pod 进行验证检查的 PodSecurityPolicy 的名称。

### seccomp.security.alpha.kubernetes.io/pod (非功能性) {#seccomp-security-alpha-kubernetes-io-pod}

较早版本的 Kubernetes 允许你使用此注释 {{< glossary_tooltip text="annotation" term_id="annotation" >}}
配置 seccomp 行为。
请参考 [使用 seccomp 限制容器的系统调用](/zh-cn/docs/tutorials/security/seccomp/)
了解为 Pod 指定 seccomp 限制的受支持方法。

### container.seccomp.security.alpha.kubernetes.io/[NAME] (非功能性) {#container-seccomp-security-alpha-kubernetes-io}

较早版本的 Kubernetes 允许你使用此注释 {{< glossary_tooltip text="annotation" term_id="annotation" >}}
配置 seccomp 行为。
请参考 [使用 seccomp 限制容器的系统调用](/zh-cn/docs/tutorials/security/seccomp/)
了解为 Pod 指定 seccomp 限制的受支持方法。

### snapshot.storage.kubernetes.io/allow-volume-mode-change {#allow-volume-mode-change}
例子：`snapshot.storage.kubernetes.io/allow-volume-mode-change: "true"`

用于：VolumeSnapshotContent

值可以是 `true` 或者 `false`。取值决定了当从 VolumeSnapshot 创建
{{< glossary_tooltip text="PersistentVolumeClaim" term_id="persistent-volume-claim" >}}
时，用户是否可以修改源卷的模式。

更多信息请参阅[转换快照的卷模式](/zh-cn/docs/concepts/storage/volume-snapshots/#convert-volume-mode)和
[Kubernetes CSI 开发者文档](https://kubernetes-csi.github.io/docs/)。

### scheduler.alpha.kubernetes.io/critical-pod（已弃用）{#scheduler-alpha-kubernetes-io-critical-pod}

例子：`scheduler.alpha.kubernetes.io/critical-pod: ""`

用于：Pod

此注解让 Kubernetes 控制平面知晓某个 Pod 是一个关键的 Pod，这样 descheduler
将不会移除该 Pod。

{{< note >}}
从 v1.16 开始，此注解被移除，取而代之的是 [Pod 优先级](/zh-cn/docs/concepts/scheduling-eviction/pod-priority-preemption/)。
{{< /note >}}

## 用于审计的注解    {#annonations-used-for-audit}


- [`authorization.k8s.io/decision`](/zh-cn/docs/reference/labels-annotations-taints/audit-annotations/#authorization-k8s-io-decision)
- [`authorization.k8s.io/reason`](/zh-cn/docs/reference/labels-annotations-taints/audit-annotations/#authorization-k8s-io-reason)
- [`insecure-sha1.invalid-cert.kubernetes.io/$hostname`](/zh-cn/docs/reference/labels-annotations-taints/audit-annotations/#insecure-sha1-invalid-cert-kubernetes-io-hostname)
- [`missing-san.invalid-cert.kubernetes.io/$hostname`](/zh-cn/docs/reference/labels-annotations-taints/audit-annotations/#missing-san-invalid-cert-kubernetes-io-hostname)
- [`pod-security.kubernetes.io/audit-violations`](/zh-cn/docs/reference/labels-annotations-taints/audit-annotations/#pod-security-kubernetes-io-audit-violations)
- [`pod-security.kubernetes.io/enforce-policy`](/zh-cn/docs/reference/labels-annotations-taints/audit-annotations/#pod-security-kubernetes-io-enforce-policy)
- [`pod-security.kubernetes.io/exempt`](/zh-cn/docs/reference/labels-annotations-taints/audit-annotations/#pod-security-kubernetes-io-exempt)

在[审计注解](/zh-cn/docs/reference/labels-annotations-taints/audit-annotations/)页面上查看更多详细信息。

## kubeadm  {#kubeadm}

### kubeadm.alpha.kubernetes.io/cri-socket  {#cri-socket}

例子：`kubeadm.alpha.kubernetes.io/cri-socket: unix:///run/containerd/container.sock`

用于：Node

kubeadm 用来保存 `init`/`join` 时提供给 kubeadm 以后使用的 CRI 套接字信息的注解。
kubeadm 使用此信息为 Node 对象设置注解。
此注解仍然是 “alpha” 阶段，因为理论上这应该是 KubeletConfiguration 中的一个字段。

### kubeadm.kubernetes.io/etcd.advertise-client-urls  {#etcd-advertise-client-urls}

例子：`kubeadm.kubernetes.io/etcd.advertise-client-urls: https://172.17.0.18:2379`

用于：Pod

kubeadm 为本地管理的 etcd Pod 设置的注解，用来跟踪 etcd 客户端应连接到的 URL 列表。
这主要用于 etcd 集群健康检查目的。

### kubeadm.kubernetes.io/kube-apiserver.advertise-address.endpoint {#kube-apiserver-advertise-address-endpoint}

例子：`kubeadm.kubernetes.io/kube-apiserver.advertise-address.endpoint: https://172.17.0.18:6443`

用于：Pod

kubeadm 为本地管理的 kube-apiserver Pod 设置的注解，用以跟踪该 API 服务器实例的公开宣告地址/端口端点。

### kubeadm.kubernetes.io/component-config.hash {#component-config-hash}

例子：`kubeadm.kubernetes.io/component-config.hash: 2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae`

用于：ConfigMap

kubeadm 为它所管理的 ConfigMaps 设置的注解，用于配置组件。它包含一个哈希（SHA-256）值，
用于确定用户是否应用了不同于特定组件的 kubeadm 默认设置的设置。

### node-role.kubernetes.io/control-plane

用于： 节点

用来指示该节点用于运行 {{< glossary_tooltip text="control plane" term_id="control-plane" >}} 组件的标记标签。
Kubeadm 工具将此标签应用于其管理的控制平面节点。
其他集群管理工具通常也会设置此污点。

你可以使用此标签来标记控制平面节点，以便更容易地将 Pods 仅安排到这些节点上，或者避免在控制平面上运行 Pods。
如果设置了此标签，[EndpointSlice 控制器](/zh-cn/docs/concepts/services-networking/topology-aware-routing/#implementation-control-plane)
在计算拓扑感知提示时将忽略该节点。

### node-role.kubernetes.io/control-plane {#node-role-kubernetes-io-control-plane-taint}

用于：节点

Kubeadm 应用在控制平面节点上的污点, 用来限制启动 Pod，并且只允许特定 Pod 可调度到这些节点上。

示例：`node-role.kubernetes.io/control-plane:NoSchedule`

如果应用此污点，则控制平面节点只允许对其进行关键工作负载调度。可以在特定节点上使用以下命令手动删除此污染。
```shell
kubectl taint nodes <node-name> node-role.kubernetes.io/control-plane:NoSchedule-
```

kubeadm 应用在控制平面节点上的污点，仅允许在其上调度关键工作负载。

### node-role.kubernetes.io/master（已弃用） {#node-role-kubernetes-io-master-taint}

用于：Node

例子：`node-role.kubernetes.io/master:NoSchedule`

kubeadm 先前应用在控制平面节点上的污点，仅允许在其上调度关键工作负载。
替换为 [`node-role.kubernetes.io/control-plane`](#node-role-kubernetes-io-control-plane-taint)；
kubeadm 不再设置或使用这个废弃的污点。
