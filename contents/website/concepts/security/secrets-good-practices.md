---
title: Kubernetes Secret 良好实践
description: >
  帮助集群管理员和应用开发者更好管理 Secret 的原理和实践。
content_type: concept
weight: 70
---


{{<glossary_definition prepend="在 Kubernetes 中，Secret 是这样一个对象："
term_id="secret" length="all">}}

以下良好实践适用于集群管理员和应用开发者。遵从这些指导方针有助于提高 Secret 对象中敏感信息的安全性，
还可以更有效地管理你的 Secret。


## 集群管理员   {#cluster-administrators}

本节提供了集群管理员可用于提高集群中机密信息安全性的良好实践。

### 配置静态加密   {#configure-encryption-at-rest}

默认情况下，Secret 对象以非加密的形式存储在 {{<glossary_tooltip term_id="etcd" text="etcd">}} 中。
你配置对在 `etcd` 中存储的 Secret 数据进行加密。相关的指导信息，
请参阅[静态加密 Secret 数据](/zh-cn/docs/tasks/administer-cluster/encrypt-data/)。

### 配置 Secret 资源的最小特权访问   {#least-privilege-secrets}

当规划诸如 Kubernetes
{{<glossary_tooltip term_id="rbac" text="基于角色的访问控制">}} [(RBAC)](/zh-cn/docs/reference/access-authn-authz/rbac/)
这类访问控制机制时，需要注意访问 `Secret` 对象的以下指导信息。
你还应遵从 [RBAC 良好实践](/zh-cn/docs/concepts/security/rbac-good-practices)中的其他指导信息。

- **组件**：限制仅最高特权的系统级组件可以执行 `watch` 或 `list` 访问。
  仅在组件的正常行为需要时才授予对 Secret 的 `get` 访问权限。
- **人员**：限制对 Secret 的 `get`、`watch` 或 `list` 访问权限。仅允许集群管理员访问 `etcd`。
  这包括只读访问。对于更复杂的访问控制，例如使用特定注解限制对 Secret 的访问，请考虑使用第三方鉴权机制。

{{< caution >}}
授予对 Secret 的 `list` 访问权限将意味着允许对应主体获取 Secret 的内容。
{{< /caution >}}

如果一个用户可以创建使用某 Secret 的 Pod，则该用户也可以看到该 Secret 的值。
即使集群策略不允许用户直接读取 Secret，同一用户也可能有权限运行 Pod 进而暴露该 Secret。
你可以检测或限制具有此访问权限的用户有意或无意地暴露 Secret 数据所造成的影响。
这里有一些建议：

* 使用生命期短暂的 Secret
* 实现对特定事件发出警报的审计规则，例如同一用户并发读取多个 Secret 时发出警报

### 改进 etcd 管理策略   {#improve-etcd-management-policies}

不再使用 `etcd` 所使用的持久存储时，考虑擦除或粉碎这些数据。

如果存在多个 `etcd` 实例，则在实例之间配置加密的 SSL/TLS 通信以保护传输中的 Secret 数据。

### 配置对外部 Secret 的访问权限   {#configure-access-to-external-secrets}

{{% thirdparty-content %}}

你可以使用第三方 Secret 存储提供商将机密数据保存在你的集群之外，然后配置 Pod 访问该信息。
[Kubernetes Secret 存储 CSI 驱动](https://secrets-store-csi-driver.sigs.k8s.io/)是一个 DaemonSet，
它允许 kubelet 从外部存储中检索 Secret，并将 Secret 作为卷挂载到特定的、你授权访问数据的 Pod。

有关支持的提供商列表，请参阅
[Secret 存储 CSI 驱动的提供商](https://secrets-store-csi-driver.sigs.k8s.io/concepts.html#provider-for-the-secrets-store-csi-driver)。

## 开发者   {#developers}

本节为开发者提供了构建和部署 Kubernetes 资源时用于改进机密数据安全性的良好实践。

### 限制特定容器集合才能访问 Secret     {#restrict-secret-access-to-specific-containers}

如果你在一个 Pod 中定义了多个容器，且仅其中一个容器需要访问 Secret，则可以定义卷挂载或环境变量配置，
这样其他容器就不会有访问该 Secret 的权限。

### 读取后保护 Secret 数据   {#protect-secret-data-after-reading}

应用程序从一个环境变量或一个卷读取机密信息的值后仍然需要保护这些值。
例如，你的应用程序必须避免以明文记录 Secret 数据，还必须避免将这些数据传输给不受信任的一方。

### 避免共享 Secret 清单   {#avoid-shareing-secret-manifests}

如果你通过{{< glossary_tooltip text="清单（Manifest）" term_id="manifest" >}}配置 Secret，
同时将该 Secret 数据编码为 base64，
那么共享此文件或将其检入一个源代码仓库就意味着有权读取该清单的所有人都能使用该 Secret。

{{<caution>}}
Base64 编码 **不是** 一种加密方法，它没有为纯文本提供额外的保密机制。
{{</caution>}}
