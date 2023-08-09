---
title: 强制实施 Pod 安全性标准
weight: 40
---



本页提供实施 [Pod 安全标准（Pod Security Standards）](/zh-cn/docs/concepts/security/pod-security-standards)
时的一些最佳实践。


## 使用内置的 Pod 安全性准入控制器

{{< feature-state for_k8s_version="v1.25" state="stable" >}}

[Pod 安全性准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#podsecurity)
尝试替换已被废弃的 PodSecurityPolicies。

### 配置所有集群名字空间    {#configure-all-cluster-namespaces}

完全未经配置的名字空间应该被视为集群安全模型中的重大缺陷。
我们建议花一些时间来分析在每个名字空间中执行的负载的类型，
并通过引用 Pod 安全性标准来确定每个负载的合适级别。
未设置标签的名字空间应该视为尚未被评估。

针对所有名字空间中的所有负载都具有相同的安全性需求的场景，
我们提供了一个[示例](/zh-cn/docs/tasks/configure-pod-container/enforce-standards-namespace-labels/#applying-to-all-namespaces)
用来展示如何批量应用 Pod 安全性标签。

### 拥抱最小特权原则

在一个理想环境中，每个名字空间中的每个 Pod 都会满足 `restricted` 策略的需求。
不过，这既不可能也不现实，某些负载会因为合理的原因而需要特权上的提升。

- 允许 `privileged` 负载的名字空间需要建立并实施适当的访问控制机制。
- 对于运行在特权宽松的名字空间中的负载，需要维护其独特安全性需求的文档。
  如果可能的话，要考虑如何进一步约束这些需求。

### 采用多种模式的策略

Pod 安全性标准准入控制器的 `audit` 和 `warn` 模式（mode）
能够在不影响现有负载的前提下，让该控制器更方便地收集关于 Pod 的重要的安全信息。

针对所有名字空间启用这些模式是一种好的实践，将它们设置为你最终打算 `enforce` 的
 _期望的_ 级别和版本。这一阶段中所生成的警告和审计注解信息可以帮助你到达这一状态。
如果你期望负载的作者能够作出变更以便适应期望的级别，可以启用 `warn` 模式。
如果你希望使用审计日志了监控和驱动变更，以便负载能够适应期望的级别，可以启用 `audit` 模式。

当你将 `enforce` 模式设置为期望的取值时，这些模式在不同的场合下仍然是有用的：

- 通过将 `warn` 设置为 `enforce` 相同的级别，客户可以在尝试创建无法通过合法检查的 Pod
  （或者包含 Pod 模板的资源）时收到警告信息。这些信息会帮助于更新资源使其合规。
- 在将 `enforce` 锁定到特定的非最新版本的名字空间中，将 `audit` 和 `warn`
  模式设置为 `enforce` 一样的级别而非 `latest` 版本，
  这样可以方便看到之前版本所允许但当前最佳实践中被禁止的设置。

## 第三方替代方案     {#third-party-alternatives}

{{% thirdparty-content %}}

Kubernetes 生态系统中也有一些其他强制实施安全设置的替代方案处于开发状态中：

- [Kubewarden](https://github.com/kubewarden).
- [Kyverno](https://kyverno.io/policies/).
- [OPA Gatekeeper](https://github.com/open-policy-agent/gatekeeper).

采用 _内置的_ 方案（例如 PodSecurity 准入控制器）还是第三方工具，
这一决策完全取决于你自己的情况。在评估任何解决方案时，对供应链的信任都是至关重要的。
最终，使用前述方案中的 _任何_ 一种都好过放任自流。

