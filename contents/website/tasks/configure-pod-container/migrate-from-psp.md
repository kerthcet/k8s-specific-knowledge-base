---
title: 从 PodSecurityPolicy 迁移到内置的 PodSecurity 准入控制器
content_type: task
min-kubernetes-server-version: v1.22
weight: 260
---



本页面描述从 PodSecurityPolicy 迁移到内置的 PodSecurity 准入控制器的过程。
这一迁移过程可以通过综合使用试运行、`audit` 和 `warn` 模式等来实现，
尽管在使用了变更式 PSP 时会变得有些困难。

## {{% heading "prerequisites" %}}

{{% version-check %}}

如果你目前运行的 Kubernetes 版本不是 {{< skew currentVersion >}}，
你可能要切换本页面以查阅你实际所运行的 Kubernetes 版本文档。

本页面假定你已经熟悉 [Pod 安全性准入](/zh-cn/docs/concepts/security/pod-security-admission/)的基本概念。


## 方法概览    {#overall-approach}

你可以采取多种策略来完成从 PodSecurityPolicy 到 Pod 安全性准入
（Pod Security Admission）的迁移。
下面是一种可能的迁移路径，其目标是尽可能降低生产环境不可用的风险，
以及安全性仍然不足的风险。

0. 确定 Pod 安全性准入是否对于你的使用场景而言比较合适。
1. 审查名字空间访问权限。
2. 简化、标准化 PodSecurityPolicy。
3. 更新名字空间：
   1. 确定合适的 Pod 安全性级别；
   2. 验证该 Pod 安全性级别可工作；
   3. 实施该 Pod 安全性级别；
   4. 绕过 PodSecurityPolicy。
4. 审阅名字空间创建过程。
5. 禁用 PodSecurityPolicy。

## 0. 确定是否 Pod 安全性准入适合你  {#is-psa-right-for-you}

Pod 安全性准入被设计用来直接满足最常见的安全性需求，并提供一组可用于多个集群的安全性级别。
不过，这一机制比 PodSecurityPolicy 的灵活度要低。
值得注意的是，PodSecurityPolicy 所支持的以下特性是 Pod 安全性准入所不支持的：

- **设置默认的安全性约束** - Pod 安全性准入是一个非变更性质的准入控制器，
  这就意味着它不会在对 Pod 进行合法性检查之前更改其配置。如果你之前依赖于 PSP 的这方面能力，
  你或者需要更改你的负载以满足 Pod 安全性约束，或者需要使用一个
  [变更性质的准入 Webhook](/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/)
  来执行相应的变更。进一步的细节可参见后文的[简化和标准化 PodSecurityPolicy](#simplify-psps)。
- **对策略定义的细粒度控制** - Pod 安全性准入仅支持
  [三种标准级别](/zh-cn/docs/concepts/security/pod-security-standards/)。
  如果你需要对特定的约束施加更多的控制，你就需要使用一个
  [验证性质的准入 Webhook](/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/)
  以实施这列策略。
- **粒度小于名字空间的策略** - PodSecurityPolicy 允许你为不同的服务账户或用户绑定不同策略，
  即使这些服务账户或用户隶属于同一个名字空间。这一方法有很多缺陷，不建议使用。
  不过如果你的确需要这种功能，你就需要使用第三方的 Webhook。
  唯一的例外是当你只需要完全针对某用户或者
  [RuntimeClasses](/zh-cn/docs/concepts/containers/runtime-class/) 赋予豁免规则时，
  Pod 安全性准入的确也为豁免规则暴露一些
  [静态配置](/zh-cn/docs/concepts/security/pod-security-admission/#exemptions)。

即便 Pod 安全性准入无法满足你的所有需求，该机制也是设计用作其他策略实施机制的
**补充**，因此可以和其他准入 Webhook 一起运行，进而提供一种有用的兜底机制。

## 1. 审查名字空间访问权限  {#review-namespace-permissions}

Pod 安全性准入是通过[名字空间上的标签](/zh-cn/docs/concepts/security/pod-security-admission/#pod-security-admission-labels-for-namespaces)
来控制的。这也就是说，任何能够更新（或通过 patch 部分更新或创建）
名字空间的人都可以更改该名字空间的 Pod 安全性级别，而这可能会被利用来绕过约束性更强的策略。
在继续执行迁移操作之前，请确保只有被信任的、有特权的用户具有这类名字空间访问权限。
不建议将这类强大的访问权限授予不应获得权限提升的用户，不过如果你必须这样做，
你需要使用一个[准入 Webhook](/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/)
来针对为 Namespace 对象设置 Pod 安全性级别设置额外的约束。

## 2. 简化、标准化 PodSecurityPolicy    {#simplify-psps}

在本节中，你会削减变更性质的 PodSecurityPolicy，去掉 Pod 安全性标准范畴之外的选项。
针对要修改的、已存在的 PodSecurityPolicy，你应该将这里所建议的更改写入到其离线副本中。
所克隆的 PSP 应该与原来的副本名字不同，并且按字母序要排到原副本之前
（例如，可以向 PSP 名字前加一个 `0`）。
先不要在 Kubernetes 中创建新的策略 -
这类操作会在后文的[推出更新的策略](#psp-update-rollout)部分讨论。

### 2.a. 去掉纯粹变更性质的字段    {#eliminating-mutaging-fields}

如果某个 PodSecurityPolicy 能够变更字段，你可能会在关掉 PodSecurityPolicy
时发现有些 Pod 无法满足 Pod 安全性级别。为避免这类状况，
你应该在执行切换操作之前去掉所有 PSP 的变更操作。
不幸的是，PSP 没有对变更性和验证性字段做清晰的区分，所以这一迁移操作也不够简单直接。

你可以先去掉那些纯粹变更性质的字段，留下验证策略中的其他内容。
这些字段（也列举于[将 PodSecurityPolicy 映射到 Pod 安全性标准](/zh-cn/docs/reference/access-authn-authz/psp-to-pod-security-standards/)参考中）
包括：

- `.spec.defaultAllowPrivilegeEscalation`
- `.spec.runtimeClass.defaultRuntimeClassName`
- `.metadata.annotations['seccomp.security.alpha.kubernetes.io/defaultProfileName']`
- `.metadata.annotations['apparmor.security.beta.kubernetes.io/defaultProfileName']`
- `.spec.defaultAddCapabilities` - 尽管理论上是一个混合了变更性与验证性功能的字段，
  这里的设置应该被合并到 `.spec.allowedCapabilities` 中，后者会执行相同的验证操作，
  但不会执行任何变更动作。

{{< caution >}}
删除这些字段可能导致负载缺少所需的配置信息，进而导致一些问题。
参见后文[退出更新的策略](#psp-update-rollout)以获得如何安全地将这些变更上线的建议。
{{< /caution >}}

### 2.b. 去掉 Pod 安全性标准未涉及的选项 {#eliminate-non-standard-options}

PodSecurityPolicy 中有一些字段未被 Pod 安全性准入机制覆盖。如果你必须使用这些选项，
你需要在 Pod 安全性准入之外部署[准入 Webhook](/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/)
以补充这一能力，而这类操作不在本指南范围。

首先，你可以去掉 Pod 安全性标准所未覆盖的那些验证性字段。这些字段
（也列举于[将 PodSecurityPolicy 映射到 Pod 安全性标准](/zh-cn/docs/reference/access-authn-authz/psp-to-pod-security-standards/)参考中，
标记为“无意见”）有：

- `.spec.allowedHostPaths`
- `.spec.allowedFlexVolumes`
- `.spec.allowedCSIDrivers`
- `.spec.forbiddenSysctls`
- `.spec.runtimeClass`

你也可以去掉以下字段，这些字段与 POSIX/UNIX 用户组控制有关。

{{< caution >}}
如果这些字段中存在使用 `MustRunAs` 策略的情况，则意味着对应字段是变更性质的。
去掉相应的字段可能导致负载无法设置所需的用户组，进而带来一些问题。
关于如何安全地将这类变更上线的相关建议，请参阅后文的[推出更新的策略](#psp-update-rollout)部分。
{{< /caution >}}

- `.spec.runAsGroup`
- `.spec.supplementalGroups`
- `.spec.fsGroup`

剩下的变更性字段是为了适当支持 Pod 安全性标准所需要的，因而需要逐个处理：

- `.spec.requiredDropCapabilities` - 需要此字段来为 Restricted 配置去掉 `ALL` 设置。
- `.spec.seLinux` - （仅针对带有 `MustRunAs` 规则的变更性设置）需要此字段来满足
  Baseline 和 Restricted 配置所需要的 SELinux 需求。
- `.spec.runAsUser` - （仅针对带有 `RunAsAny` 规则的非变更性设置）需要此字段来为
  Restricted 配置保证 `RunAsNonRoot`。
- `.spec.allowPrivilegeEscalation` - （如果设置为 `false` 则为变更性设置）
  需要此字段来支持 Restricted 配置。

### 2.c. 推出更新的 PSP    {#psp-update-rollout}

接下来，你可以将更新后的策略推出到你的集群上。在继续操作时，你要非常小心，
因为去掉变更性质的选项可能导致有些工作负载缺少必需的配置。

针对更新后的每个 PodSecurityPolicy：

1. 识别运行于原 PSP 之下的 Pod。可以通过 `kubernetes.io/psp` 注解来完成。
   例如，使用 kubectl：

   ```shell
   PSP_NAME="original" # 设置你要检查的 PSP 的名称
   kubectl get pods --all-namespaces -o jsonpath="{range .items[?(@.metadata.annotations.kubernetes\.io\/psp=='$PSP_NAME')]}{.metadata.namespace} {.metadata.name}{'\n'}{end}"
   ```

2. 比较运行中的 Pod 与原来的 Pod 规约，确定 PodSecurityPolicy 是否更改过这些 Pod。
   对于通过[工作负载资源](/zh-cn/docs/concepts/workloads/controllers/)所创建的 Pod，
   你可以比较 Pod 和控制器资源中的 PodTemplate。如果发现任何变更，则原来的 Pod
   或者 PodTemplate 需要被更新以加上所希望的配置。要审查的字段包括：

   - `.metadata.annotations['container.apparmor.security.beta.kubernetes.io/*']`
     （将 `*` 替换为每个容器的名称）
   - `.spec.runtimeClassName`
   - `.spec.securityContext.fsGroup`
   - `.spec.securityContext.seccompProfile`
   - `.spec.securityContext.seLinuxOptions`
   - `.spec.securityContext.supplementalGroups`
   - 对于容器，在 `.spec.containers[*]` 和 `.spec.initContainers[*]` 之下，检查下面字段：
     - `.securityContext.allowPrivilegeEscalation`
     - `.securityContext.capabilities.add`
     - `.securityContext.capabilities.drop`
     - `.securityContext.readOnlyRootFilesystem`
     - `.securityContext.runAsGroup`
     - `.securityContext.runAsNonRoot`
     - `.securityContext.runAsUser`
     - `.securityContext.seccompProfile`
     - `.securityContext.seLinuxOptions`
3. 创建新的 PodSecurityPolicy。如果存在 Role 或 ClusterRole 对象为用户授权了在所有 PSP
   上使用 `use` 动词的权限，则所使用的的会是新创建的 PSP 而不是其变更性的副本。
4. 更新你的鉴权配置，为访问新的 PSP 授权。在 RBAC 机制下，这意味着需要更新所有为原 PSP
   授予 `use` 访问权限的 Role 或 ClusterRole 对象，使之也对更新后的 PSP 授权。

5. 验证：经过一段时间后，重新执行步骤 1 中所给的命令，查看是否有 Pod 仍在使用原来的 PSP。
   注意，在新的策略被推出到集群之后，Pod 需要被重新创建才可以执行全面验证。
6. （可选）一旦你已经验证原来的 PSP 不再被使用，你就可以删除这些 PSP。

## 3. 更新名字空间     {#update-namespace}

下面的步骤需要在集群中的所有名字空间上执行。所列步骤中的命令使用变量
`$NAMESPACE` 来引用所更新的名字空间。

### 3.a. 识别合适的 Pod 安全级别   {#identify-appropriate-level}

首先请回顾 [Pod 安全性标准](/zh-cn/docs/concepts/security/pod-security-standards/)内容，
并了解三个安全级别。

为你的名字空间选择 Pod 安全性级别有几种方法：

1. **根据名字空间的安全性需求来确定** - 如果你熟悉某名字空间的预期访问级别，
   你可以根据这类需求来选择合适的安全级别，就像大家在为新集群确定安全级别一样。
2. **根据现有的 PodSecurityPolicy 来确定** -
   基于[将 PodSecurityPolicy 映射到 Pod 安全性标准](/zh-cn/docs/reference/access-authn-authz/psp-to-pod-security-standards/)
   参考资料，你可以将各个 PSP 映射到某个 Pod 安全性标准级别。如果你的 PSP 不是基于
   Pod 安全性标准的，你可能或者需要选择一个至少与该 PSP 一样宽松的级别，
   或者选择一个至少与其一样严格的级别。使用下面的命令你可以查看被 Pod 使用的 PSP 有哪些：

   ```sh
   kubectl get pods -n $NAMESPACE -o jsonpath="{.items[*].metadata.annotations.kubernetes\.io\/psp}" | tr " " "\n" | sort -u
   ```
3. **根据现有 Pod 来确定** - 使用[检查 Pod 安全性级别](#verify-pss-level)小节所述策略，
   你可以测试 Baseline 和 Restricted 级别，检查它们是否对于现有负载而言足够宽松，
   并选择二者之间特权级较低的合法级别。

{{< caution >}}
上面的第二和第三种方案是基于 _现有_ Pod 的，因此可能错失那些当前未处于运行状态的
Pod，例如 CronJobs、缩容到零的负载，或者其他尚未全面铺开的负载。
{{< /caution >}}

### 3.b. 检查 Pod 安全性级别   {#verify-pss-level}

一旦你已经为名字空间选择了 Pod 安全性级别（或者你正在尝试多个不同级别），
先进行测试是个不错的主意（如果使用 Privileged 级别，则可略过此步骤）。
Pod 安全性包含若干工具可用来测试和安全地推出安全性配置。

首先，你可以试运行新策略，这个过程可以针对所应用的策略评估当前在名字空间中运行的
Pod，但不会令新策略马上生效：

```sh
# $LEVEL 是要试运行的级别，可以是 "baseline" 或 "restricted"
kubectl label --dry-run=server --overwrite ns $NAMESPACE pod-security.kubernetes.io/enforce=$LEVEL
```

此命令会针对在所提议的级别下不再合法的所有 **现存** Pod 返回警告信息。

第二种办法在抓取当前未运行的负载方面表现的更好：audit 模式。
运行于 audit 模式（而非 enforcing 模式）下时，违反策略级别的 Pod 会被记录到审计日志中，
经过一段时间后可以在日志中查看到，但这些 Pod 不会被拒绝。
warning 模式的工作方式与此类似，不过会立即向用户返回告警信息。
你可以使用下面的命令为名字空间设置 audit 模式的级别：

```sh
kubectl label --overwrite ns $NAMESPACE pod-security.kubernetes.io/audit=$LEVEL
```

当以上两种方法输出意料之外的违例状况时，你就需要或者更新发生违例的负载以满足策略需求，
或者放宽名字空间上的 Pod 安全性级别。

### 3.c. 实施 Pod 安全性级别      {#enforce-pod-security-level}

当你对可以安全地在名字空间上实施的级别比较满意时，你可以更新名字空间来实施所期望的级别：

```sh
kubectl label --overwrite ns $NAMESPACE pod-security.kubernetes.io/enforce=$LEVEL
```

### 3.d. 绕过 PodSecurityPolicy {#bypass-psp}

最后，你可以通过将
{{< example file="policy/privileged-psp.yaml" >}}完全特权的 PSP{{< /example >}}
绑定到某名字空间中所有服务账户上，在名字空间层面绕过所有 PodSecurityPolicy。

```sh
# 下面集群范围的命令只需要执行一次
kubectl apply -f privileged-psp.yaml
kubectl create clusterrole privileged-psp --verb use --resource podsecuritypolicies.policy --resource-name privileged

# 逐个名字空间地禁用
kubectl create -n $NAMESPACE rolebinding disable-psp --clusterrole privileged-psp --group system:serviceaccounts:$NAMESPACE
```

由于特权 PSP 是非变更性的，PSP 准入控制器总是优选非变更性的 PSP，
上面的操作会确保对应名字空间中的所有 Pod 不再会被 PodSecurityPolicy
所更改或限制。

按上述操作逐个名字空间地禁用 PodSecurityPolicy 这种做法的好处是，
如果出现问题，你可以很方便地通过删除 RoleBinding 来回滚所作的更改。
你所要做的只是确保之前存在的 PodSecurityPolicy 还在。

```sh
# 撤销 PodSecurityPolicy 的禁用
kubectl delete -n $NAMESPACE rolebinding disable-psp
```

## 4. 审阅名字空间创建过程  {#review-namespace-creation-process}

现在，现有的名字空间都已被更新，强制实施 Pod 安全性准入，
你应该确保你用来管控新名字空间创建的流程与/或策略也被更新，这样合适的 Pod
安全性配置会被应用到新的名字空间上。

你也可以静态配置 Pod 安全性准入控制器，为尚未打标签的名字空间设置默认的
enforce、audit 与/或 warn 级别。
详细信息可参阅[配置准入控制器](/zh-cn/docs/tasks/configure-pod-container/enforce-standards-admission-controller/#configure-the-admission-controller)页面。

## 5. 禁用 PodSecurityPolicy    {#disable-psp}

最后，你已为禁用 PodSecurityPolicy 做好准备。要禁用 PodSecurityPolicy，
你需要更改 API 服务器上的准入配置：
[我如何关闭某个准入控制器？](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#how-do-i-turn-off-an-admission-controller)

如果需要验证 PodSecurityPolicy 准入控制器不再被启用，你可以通过扮演某个无法访问任何
PodSecurityPolicy 的用户来执行测试（参见
[PodSecurityPolicy 示例](/zh-cn/docs/concepts/security/pod-security-policy/#example)），
或者通过检查 API 服务器的日志来进行验证。在启动期间，API
服务器会输出日志行，列举所挂载的准入控制器插件。

```
I0218 00:59:44.903329      13 plugins.go:158] Loaded 16 mutating admission controller(s) successfully in the following order: NamespaceLifecycle,LimitRanger,ServiceAccount,NodeRestriction,TaintNodesByCondition,Priority,DefaultTolerationSeconds,ExtendedResourceToleration,PersistentVolumeLabel,DefaultStorageClass,StorageObjectInUseProtection,RuntimeClass,DefaultIngressClass,MutatingAdmissionWebhook.
I0218 00:59:44.903350      13 plugins.go:161] Loaded 14 validating admission controller(s) successfully in the following order: LimitRanger,ServiceAccount,PodSecurity,Priority,PersistentVolumeClaimResize,RuntimeClass,CertificateApproval,CertificateSigning,CertificateSubjectRestriction,DenyServiceExternalIPs,ValidatingAdmissionWebhook,ResourceQuota.
```

你应该会看到 `PodSecurity`（在 validating admission controllers 列表中），
并且两个列表中都不应该包含 `PodSecurityPolicy`。

一旦你确定 PSP 准入控制器已被禁用（并且这种状况已经持续了一段时间，
这样你才会比较确定不需要回滚），你就可以放心地删除你的 PodSecurityPolicy
以及所关联的所有 Role、ClusterRole、RoleBinding、ClusterRoleBinding 等对象
（仅需要确保他们不再授予其他不相关的访问权限）。

