---
title: 已弃用 API 的迁移指南
weight: 45
content_type: reference
---


随着 Kubernetes API 的演化，API 会周期性地被重组或升级。
当 API 演化时，老的 API 会被弃用并被最终删除。
本页面包含你在将已弃用 API 版本迁移到新的更稳定的 API 版本时需要了解的知识。


## 各发行版本中移除的 API  {#removed-apis-by-release}

### v1.29

**v1.29** 发行版本将停止提供以下已弃用的 API 版本：

#### 流控制资源 {#flowcontrol-resources-v129}

**flowcontrol.apiserver.k8s.io/v1beta2** API 版本的 FlowSchema
和 PriorityLevelConfiguration 将不会在 v1.29 中提供。

* 迁移清单和 API 客户端使用 **flowcontrol.apiserver.k8s.io/v1beta3** API 版本，
  此 API 从 v1.26 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* **flowcontrol.apiserver.k8s.io/v1beta3** 中需要额外注意的变更：
  * PriorityLevelConfiguration 的 `spec.limited.assuredConcurrencyShares`
    字段已被更名为 `spec.limited.nominalConcurrencyShares`

### v1.27

**v1.27** 发行版本中将去除以下已弃用的 API 版本：

#### CSIStorageCapacity {#csistoragecapacity-v127}

**storage.k8s.io/v1beta1** API 版本的 CSIStorageCapacity 将不会在 v1.27 提供。

* 自 v1.24 版本起，迁移清单和 API 客户端使用 **storage.k8s.io/v1** API 版本
* 所有现有的持久化对象都可以通过新的 API 访问
* 没有需要额外注意的变更

### v1.26

**v1.26** 发行版本中将去除以下已弃用的 API 版本：

#### 流控制资源     {#flowcontrol-resources-v126}

从 v1.26 版本开始不再提供 **flowcontrol.apiserver.k8s.io/v1beta1** API 版本的
FlowSchema 和 PriorityLevelConfiguration。

* 迁移清单和 API 客户端使用 **flowcontrol.apiserver.k8s.io/v1beta3** API 版本，
  此 API 从 v1.26 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 没有需要额外注意的变更

#### HorizontalPodAutoscaler {#horizontalpodautoscaler-v126}

从 v1.26 版本开始不再提供 **autoscaling/v2beta2** API 版本的
HorizontalPodAutoscaler。

* 迁移清单和 API 客户端使用 **autoscaling/v2** API 版本，
  此 API 从 v1.23 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；

### v1.25

**v1.25** 发行版本将停止提供以下已废弃 API 版本：

#### CronJob {#cronjob-v125}

从 v1.25 版本开始不再提供 **batch/v1beta1** API 版本的 CronJob。

* 迁移清单和 API 客户端使用 **batch/v1** API 版本，此 API 从 v1.21 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 没有需要额外注意的变更。

#### EndpointSlice {#endpointslice-v125}

从 v1.25 版本开始不再提供 **discovery.k8s.io/v1beta1** API 版本的 EndpointSlice。

* 迁移清单和 API 客户端使用 **discovery.k8s.io/v1** API 版本，此 API 从 v1.21 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* **discovery.k8s.io/v1** 中值得注意的变更有：
  * 使用每个 Endpoint 的 `nodeName` 字段而不是已被弃用的
    `topology["kubernetes.io/hostname"]` 字段；
  * 使用每个 Endpoint 的 `zone` 字段而不是已被弃用的
    `topology["kubernetes.io/zone"]` 字段；
  * `topology` 字段被替换为 `deprecatedTopology`，并且在 v1 版本中不可写入。

#### Event {#event-v125}

从 v1.25 版本开始不再提供 **events.k8s.io/v1beta1** API 版本的 Event。

* 迁移清单和 API 客户端使用 **events.k8s.io/v1** API 版本，此 API 从 v1.19 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；

* **events.k8s.io/v1** 中值得注意的变更有：
  * `type` 字段只能设置为 `Normal` 和 `Warning` 之一；
  * `involvedObject` 字段被更名为 `regarding`；
  * `action`、`reason`、`reportingController` 和 `reportingInstance` 字段
    在创建新的 **events.k8s.io/v1** 版本 Event 时都是必需的字段；
  * 使用 `eventTime` 而不是已被弃用的 `firstTimestamp` 字段
    （该字段已被更名为 `deprecatedFirstTimestamp`，且不允许出现在新的 **events.k8s.io/v1** Event 对象中）；
  * 使用 `series.lastObservedTime` 而不是已被弃用的 `lastTimestamp` 字段
    （该字段已被更名为 `deprecatedLastTimestamp`，且不允许出现在新的 **events.k8s.io/v1** Event 对象中）；
  * 使用 `series.count` 而不是已被弃用的 `count` 字段
    （该字段已被更名为 `deprecatedCount`，且不允许出现在新的 **events.k8s.io/v1** Event 对象中）；
  * 使用 `reportingController` 而不是已被弃用的 `source.component` 字段
    （该字段已被更名为 `deprecatedSource.component`，且不允许出现在新的 **events.k8s.io/v1** Event 对象中）；
  * 使用 `reportingInstance` 而不是已被弃用的 `source.host` 字段
    （该字段已被更名为 `deprecatedSource.host`，且不允许出现在新的 **events.k8s.io/v1** Event 对象中）。

#### HorizontalPodAutoscaler {#horizontalpodautoscaler-v125}

从 v1.25 版本开始不再提供 **autoscaling/v2beta1** API 版本的
HorizontalPodAutoscaler。

* 迁移清单和 API 客户端使用 **autoscaling/v2** API 版本，此 API 从 v1.23 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问。

#### PodDisruptionBudget {#poddisruptionbudget-v125}

从 v1.25 版本开始不再提供 **policy/v1beta1** API 版本的 PodDisruptionBudget。

* 迁移清单和 API 客户端使用 **policy/v1** API 版本，此 API 从 v1.21 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* **policy/v1** 中需要额外注意的变更有：
  * 在 `policy/v1` 版本的 PodDisruptionBudget 中将 `spec.selector`
    设置为空（`{}`）时会选择名字空间中的所有 Pod（在 `policy/v1beta1`
    版本中，空的 `spec.selector` 不会选择任何 Pod）。如果 `spec.selector`
    未设置，则在两个 API 版本下都不会选择任何 Pod。

#### PodSecurityPolicy {#psp-v125}

从 v1.25 版本开始不再提供 **policy/v1beta1** API 版本中的 PodSecurityPolicy，
并且 PodSecurityPolicy 准入控制器也会被删除。

迁移到 [Pod 安全准入](/zh-cn/docs/concepts/security/pod-security-admission/)或[第三方准入 Webhook](/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/)。
有关迁移指南，请参阅[从 PodSecurityPolicy 迁移到内置 PodSecurity 准入控制器](/zh-cn/docs/tasks/configure-pod-container/migrate-from-psp/)。
有关弃用的更多信息，请参阅 [PodSecurityPolicy 弃用：过去、现在和未来](/zh-cn/blog/2021/04/06/podsecuritypolicy-deprecation-past-present-and-future/)。

#### RuntimeClass {#runtimeclass-v125}

从 v1.25 版本开始不再提供 **node.k8s.io/v1beta1** API 版本中的 RuntimeClass。

* 迁移清单和 API 客户端使用 **node.k8s.io/v1** API 版本，此 API 从 v1.20 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 没有需要额外注意的变更。

### v1.22

**v1.22** 发行版本停止提供以下已废弃 API 版本：

#### Webhook 资源   {#webhook-resources-v122}

**admissionregistration.k8s.io/v1beta1** API 版本的 MutatingWebhookConfiguration
和 ValidatingWebhookConfiguration 不在 v1.22 版本中继续提供。

* 迁移清单和 API 客户端使用 **admissionregistration.k8s.io/v1** API 版本，
  此 API 从 v1.16 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；

* 值得注意的变更：
  * `webhooks[*].failurePolicy` 在 v1 版本中默认值从 `Ignore` 改为 `Fail`
  * `webhooks[*].matchPolicy` 在 v1 版本中默认值从 `Exact` 改为 `Equivalent`
  * `webhooks[*].timeoutSeconds` 在 v1 版本中默认值从 `30s` 改为 `10s`
  * `webhooks[*].sideEffects` 的默认值被删除，并且该字段变为必须指定；
    在 v1 版本中可选的值只能是 `None` 和 `NoneOnDryRun` 之一
  * `webhooks[*].admissionReviewVersions` 的默认值被删除，在 v1
    版本中此字段变为必须指定（AdmissionReview 的被支持版本包括 `v1` 和 `v1beta1`）
  * `webhooks[*].name` 必须在通过 `admissionregistration.k8s.io/v1`
    创建的对象列表中唯一

#### CustomResourceDefinition {#customresourcedefinition-v122}

**apiextensions.k8s.io/v1beta1** API 版本的 CustomResourceDefinition
不在 v1.22 版本中继续提供。

* 迁移清单和 API 客户端使用 **apiextensions/v1** API 版本，此 API 从 v1.16 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 值得注意的变更：
  * `spec.scope` 的默认值不再是 `Namespaced`，该字段必须显式指定
  * `spec.version` 在 v1 版本中被删除；应改用 `spec.versions`
  * `spec.validation` 在 v1 版本中被删除；应改用 `spec.versions[*].schema`
  * `spec.subresources` 在 v1 版本中被删除；应改用 `spec.versions[*].subresources`
  * `spec.additionalPrinterColumns` 在 v1 版本中被删除；应改用
    `spec.versions[*].additionalPrinterColumns`
  * `spec.conversion.webhookClientConfig` 在 v1 版本中被移动到
    `spec.conversion.webhook.clientConfig` 中


  * `spec.conversion.conversionReviewVersions` 在 v1 版本中被移动到
    `spec.conversion.webhook.conversionReviewVersions`
  * `spec.versions[*].schema.openAPIV3Schema` 在创建 v1 版本的
    CustomResourceDefinition 对象时变成必需字段，并且其取值必须是一个
    [结构化的 Schema](/zh-cn/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#specifying-a-structural-schema)
  * `spec.preserveUnknownFields: true` 在创建 v1 版本的 CustomResourceDefinition
    对象时不允许指定；该配置必须在 Schema 定义中使用
    `x-kubernetes-preserve-unknown-fields: true` 来设置
  * 在 v1 版本中，`additionalPrinterColumns` 的条目中的 `JSONPath` 字段被更名为
    `jsonPath`（补丁 [#66531](https://github.com/kubernetes/kubernetes/issues/66531)）

#### APIService {#apiservice-v122}

**apiregistration/v1beta1** API 版本的 APIService 不在 v1.22 版本中继续提供。

* 迁移清单和 API 客户端使用 **apiregistration.k8s.io/v1** API 版本，此 API 从
  v1.10 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 没有需要额外注意的变更。

#### TokenReview {#tokenreview-v122}

**authentication.k8s.io/v1beta1** API 版本的 TokenReview 不在 v1.22 版本中继续提供。

* 迁移清单和 API 客户端使用 **authentication.k8s.io/v1** API 版本，此 API 从
  v1.6 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 没有需要额外注意的变更。

#### SubjectAccessReview resources {#subjectaccessreview-resources-v122}

**authorization.k8s.io/v1beta1** API 版本的 LocalSubjectAccessReview、
SelfSubjectAccessReview、SubjectAccessReview、SelfSubjectRulesReview 不在 v1.22 版本中继续提供。

* 迁移清单和 API 客户端使用 **authorization.k8s.io/v1** API 版本，此 API 从
  v1.6 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 需要额外注意的变更：
  * `spec.group` 在 v1 版本中被更名为 `spec.groups`
    （补丁 [#32709](https://github.com/kubernetes/kubernetes/issues/32709)）

#### CertificateSigningRequest {#certificatesigningrequest-v122}

**certificates.k8s.io/v1beta1** API 版本的 CertificateSigningRequest 不在
v1.22 版本中继续提供。

* 迁移清单和 API 客户端使用 **certificates.k8s.io/v1** API 版本，此 API 从
  v1.19 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；

* `certificates.k8s.io/v1` 中需要额外注意的变更：
  * 对于请求证书的 API 客户端而言：
    * `spec.signerName` 现在变成必需字段（参阅
      [已知的 Kubernetes 签署者](/zh-cn/docs/reference/access-authn-authz/certificate-signing-requests/#kubernetes-signers)），
      并且通过 `certificates.k8s.io/v1` API 不可以创建签署者为
      `kubernetes.io/legacy-unknown` 的请求
    * `spec.usages` 现在变成必需字段，其中不可以包含重复的字符串值，
      并且只能包含已知的用法字符串
  * 对于要批准或者签署证书的 API 客户端而言：
    * `status.conditions` 中不可以包含重复的类型
    * `status.conditions[*].status` 字段现在变为必需字段
    * `status.certificate` 必须是 PEM 编码的，而且其中只能包含 `CERTIFICATE`
      数据块

#### Lease {#lease-v122}

**coordination.k8s.io/v1beta1** API 版本的 Lease 不在 v1.22 版本中继续提供。

* 迁移清单和 API 客户端使用 **coordination.k8s.io/v1** API 版本，此 API 从
  v1.14 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 没有需要额外注意的变更。

#### Ingress {#ingress-v122}

**extensions/v1beta1** 和 **networking.k8s.io/v1beta1** API 版本的 Ingress
不在 v1.22 版本中继续提供。

* 迁移清单和 API 客户端使用 **networking.k8s.io/v1** API 版本，此 API 从
  v1.19 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 值得注意的变更：
  * `spec.backend` 字段被更名为 `spec.defaultBackend`
  * 后端的 `serviceName` 字段被更名为 `service.name`
  * 数值表示的后端 `servicePort` 字段被更名为 `service.port.number`
  * 字符串表示的后端 `servicePort` 字段被更名为 `service.port.name`
  * 对所有要指定的路径，`pathType` 都成为必需字段。
    可选项为 `Prefix`、`Exact` 和 `ImplementationSpecific`。
    要匹配 `v1beta1` 版本中未定义路径类型时的行为，可使用 `ImplementationSpecific`

#### IngressClass {#ingressclass-v122}

**networking.k8s.io/v1beta1** API 版本的 IngressClass 不在 v1.22 版本中继续提供。

* 迁移清单和 API 客户端使用 **networking.k8s.io/v1** API 版本，此 API 从
  v1.19 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 没有需要额外注意的变更。

#### RBAC 资源   {#rbac-resources-v122}

**rbac.authorization.k8s.io/v1beta1** API 版本的 ClusterRole、ClusterRoleBinding、
Role 和 RoleBinding 不在 v1.22 版本中继续提供。

* 迁移清单和 API 客户端使用 **rbac.authorization.k8s.io/v1** API 版本，此 API 从
  v1.8 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 没有需要额外注意的变更。

#### PriorityClass {#priorityclass-v122}

**scheduling.k8s.io/v1beta1** API 版本的 PriorityClass 不在 v1.22 版本中继续提供。

* 迁移清单和 API 客户端使用 **scheduling.k8s.io/v1** API 版本，此 API 从
  v1.14 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 没有需要额外注意的变更。

#### 存储资源  {#storage-resources-v122}

**storage.k8s.io/v1beta1** API 版本的 CSIDriver、CSINode、StorageClass
和 VolumeAttachment 不在 v1.22 版本中继续提供。

* 迁移清单和 API 客户端使用 **storage.k8s.io/v1** API 版本
  * CSIDriver 从 v1.19 版本开始在 **storage.k8s.io/v1** 中提供；
  * CSINode 从 v1.17 版本开始在 **storage.k8s.io/v1** 中提供；
  * StorageClass 从 v1.6 版本开始在 **storage.k8s.io/v1** 中提供；
  * VolumeAttachment 从 v1.13 版本开始在 **storage.k8s.io/v1** 中提供；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 没有需要额外注意的变更。

### v1.16

**v1.16** 发行版本停止提供以下已废弃 API 版本：

#### NetworkPolicy {#networkpolicy-v116}

**extensions/v1beta1** API 版本的 NetworkPolicy 不在 v1.16 版本中继续提供。

* 迁移清单和 API 客户端使用 **networking.k8s.io/v1** API 版本，此 API 从
  v1.8 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问。

#### DaemonSet {#daemonset-v116}

**extensions/v1beta1** 和 **apps/v1beta2** API 版本的 DaemonSet 在
v1.16 版本中不再继续提供。

* 迁移清单和 API 客户端使用 **apps/v1** API 版本，此 API 从 v1.9 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 值得注意的变更：
  * `spec.templateGeneration` 字段被删除
  * `spec.selector` 现在变成必需字段，并且在对象创建之后不可变更；
    可以将现有模板的标签作为选择算符以实现无缝迁移。
  * `spec.updateStrategy.type` 的默认值变为 `RollingUpdate`
    （`extensions/v1beta1` API 版本中的默认值是 `OnDelete`）。

#### Deployment {#deployment-v116}

**extensions/v1beta1**、**apps/v1beta1** 和 **apps/v1beta2** API 版本的
Deployment 在 v1.16 版本中不再继续提供。

* 迁移清单和 API 客户端使用 **apps/v1** API 版本，此 API 从 v1.9 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 值得注意的变更：
  * `spec.rollbackTo` 字段被删除
  * `spec.selector` 字段现在变为必需字段，并且在 Deployment 创建之后不可变更；
    可以使用现有的模板的标签作为选择算符以实现无缝迁移。
  * `spec.progressDeadlineSeconds` 的默认值变为 `600` 秒
    （`extensions/v1beta1` 中的默认值是没有期限）
  * `spec.revisionHistoryLimit` 的默认值变为 `10`
    （`apps/v1beta1` API 版本中此字段默认值为 `2`，在`extensions/v1beta1` API
    版本中的默认行为是保留所有历史记录）。
  * `maxSurge` 和 `maxUnavailable` 的默认值变为 `25%`
    （在 `extensions/v1beta1` API 版本中，这些字段的默认值是 `1`）。

#### StatefulSet {#statefulset-v116}

**apps/v1beta1** 和 **apps/v1beta2** API 版本的 StatefulSet 在 v1.16 版本中不再继续提供。

* 迁移清单和 API 客户端使用 **apps/v1** API 版本，此 API 从 v1.9 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 值得注意的变更：
  * `spec.selector` 字段现在变为必需字段，并且在 StatefulSet 创建之后不可变更；
    可以使用现有的模板的标签作为选择算符以实现无缝迁移。
  * `spec.updateStrategy.type` 的默认值变为 `RollingUpdate`
    （`apps/v1beta1` API 版本中的默认值是 `OnDelete`）。

#### ReplicaSet {#replicaset-v116}

**extensions/v1beta1**、**apps/v1beta1** 和 **apps/v1beta2** API 版本的
ReplicaSet 在 v1.16 版本中不再继续提供。

* 迁移清单和 API 客户端使用 **apps/v1** API 版本，此 API 从 v1.9 版本开始可用；
* 所有的已保存的对象都可以通过新的 API 来访问；
* 值得注意的变更：
  * `spec.selector` 现在变成必需字段，并且在对象创建之后不可变更；
    可以将现有模板的标签作为选择算符以实现无缝迁移。

#### PodSecurityPolicy {#psp-v116}

**extensions/v1beta1** API 版本的 PodSecurityPolicy 在 v1.16 版本中不再继续提供。

* 迁移清单和 API 客户端使用 **policy/v1beta1** API 版本，此 API 从 v1.10 版本开始可用；
* 注意 **policy/v1beta1** API 版本的 PodSecurityPolicy 会在 v1.25 版本中移除。

## 需要做什么   {#what-to-do}

### 在禁用已启用 API 的情况下执行测试

你可以通过在启动 API 服务器时禁用特定的 API 版本来模拟即将发生的
API 移除，从而完成测试。在 API 服务器启动参数中添加如下标志：

`--runtime-config=<group>/<version>=false`

例如：

`--runtime-config=admissionregistration.k8s.io/v1beta1=false,apiextensions.k8s.io/v1beta1,...`

### 定位何处使用了已弃用的 API

使用 [client warnings, metrics, and audit information available in 1.19+](/blog/2020/09/03/warnings/#deprecation-warnings)
来定位在何处使用了已弃用的 API。

### 迁移到未被弃用的 API

* 更新自定义的集成组件和控制器，调用未被弃用的 API
* 更改 YAML 文件引用未被弃用的 API

你可以用 `kubectl-convert` 命令（在 v1.20 之前是 `kubectl convert`）
来自动转换现有对象：

`kubectl-convert -f <file> --output-version <group>/<version>`.

例如，要将较老的 Deployment 版本转换为 `apps/v1` 版本，你可以运行：

`kubectl-convert -f ./my-deployment.yaml --output-version apps/v1`

需要注意的是这种操作使用的默认值可能并不理想。
要进一步了解某个特定资源，可查阅 Kubernetes [API 参考](/zh-cn/docs/reference/kubernetes-api/)。
