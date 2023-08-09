---
title: 保护集群
content_type: task
weight: 320
---


本文档涉及与保护集群免受意外或恶意访问有关的主题，并对总体安全性提出建议。

## {{% heading "prerequisites" %}}

* {{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


## 控制对 Kubernetes API 的访问

因为 Kubernetes 是完全通过 API 驱动的，所以，控制和限制谁可以通过 API 访问集群，
以及允许这些访问者执行什么样的 API 动作，就成为了安全控制的第一道防线。

### 为所有 API 交互使用传输层安全（TLS）

Kubernetes 期望集群中所有的 API 通信在默认情况下都使用 TLS 加密，
大多数安装方法也允许创建所需的证书并且分发到集群组件中。
请注意，某些组件和安装方法可能使用 HTTP 来访问本地端口，
管理员应该熟悉每个组件的设置，以识别可能不安全的流量。

### API 认证

安装集群时，选择一个 API 服务器的身份验证机制，去使用与之匹配的公共访问模式。
例如，小型的单用户集群可能希望使用简单的证书或静态承载令牌方法。
更大的集群则可能希望整合现有的、OIDC、LDAP 等允许用户分组的服务器。

所有 API 客户端都必须经过身份验证，即使它是基础设施的一部分，比如节点、代理、调度程序和卷插件。
这些客户端通常使用 [服务帐户](/zh-cn/docs/reference/access-authn-authz/service-accounts-admin/)
或 X509 客户端证书，并在集群启动时自动创建或是作为集群安装的一部分进行设置。

如果你希望获取更多信息，请参考[认证参考文档](/zh-cn/docs/reference/access-authn-authz/authentication/)。

### API 授权

一旦通过身份认证，每个 API 的调用都将通过鉴权检查。
Kubernetes 集成[基于角色的访问控制（RBAC）](/zh-cn/docs/reference/access-authn-authz/rbac/)组件，
将传入的用户或组与一组绑定到角色的权限匹配。
这些权限将动作（get、create、delete）和资源（Pod、Service、Node）进行组合，并可在名字空间或者集群范围生效。
Kubernetes 提供了一组可直接使用的角色，这些角色根据客户可能希望执行的操作提供合理的责任划分。
建议你同时使用 [Node](/zh-cn/docs/reference/access-authn-authz/node/) 和
[RBAC](/zh-cn/docs/reference/access-authn-authz/rbac/) 两个鉴权组件，再与
[NodeRestriction](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#noderestriction)
准入插件结合使用。

与身份验证一样，简单而广泛的角色可能适合于较小的集群，但是随着更多的用户与集群交互，
可能需要将团队划分到有更多角色限制的、
单独的{{< glossary_tooltip text="名字空间" term_id="namespace" >}}中去。

就鉴权而言，很重要的一点是理解对象上的更新操作如何导致在其它地方发生对应行为。
例如，用户可能不能直接创建 Pod，但允许他们通过创建 Deployment 来创建这些 Pod，
这将让他们间接创建这些 Pod。
同样地，从 API 删除一个节点将导致调度到这些节点上的 Pod 被中止，并在其他节点上重新创建。
原生的角色设计代表了灵活性和常见用例之间的平衡，但须限制的角色应该被仔细审查，
以防止意外的权限升级。如果内置的角色无法满足你的需求，则可以根据使用场景需要创建特定的角色。

如果你希望获取更多信息，请参阅[鉴权参考](/zh-cn/docs/reference/access-authn-authz/authorization/)。

## 控制对 Kubelet 的访问

Kubelet 公开 HTTPS 端点，这些端点提供了对节点和容器的强大的控制能力。
默认情况下，Kubelet 允许对此 API 进行未经身份验证的访问。

生产级别的集群应启用 Kubelet 身份认证和授权。

进一步的信息，请参考
[Kubelet 身份验证/授权参考](/zh-cn/docs/reference/access-authn-authz/kubelet-authn-authz/)。

## 控制运行时负载或用户的能力

Kubernetes 中的授权故意设计成较高抽象级别，侧重于对资源的粗粒度行为。
更强大的控制是 **策略** 的形式呈现的，根据使用场景限制这些对象如何作用于集群、自身和其他资源。

### 限制集群上的资源使用

[资源配额（Resource Quota）](/zh-cn/docs/concepts/policy/resource-quotas/)限制了赋予命名空间的资源的数量或容量。
资源配额通常用于限制名字空间可以分配的 CPU、内存或持久磁盘的数量，
但也可以控制每个名字空间中存在多少个 Pod、Service 或 Volume。

[限制范围（Limit Range）](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)
限制上述某些资源的最大值或者最小值，以防止用户使用类似内存这样的通用保留资源时请求不合理的过高或过低的值，
或者在没有指定的情况下提供默认限制。

### 控制容器运行的特权

Pod 定义包含了一个[安全上下文](/zh-cn/docs/tasks/configure-pod-container/security-context/)，
用于描述一些访问请求，如以某个节点上的特定 Linux 用户（如 root）身份运行，
以特权形式运行，访问主机网络，以及一些在宿主节点上不受约束地运行的其它控制权限等等。

你可以配置 [Pod 安全准入](/zh-cn/docs/concepts/security/pod-security-admission/)来在某个
{{< glossary_tooltip text="名字空间" term_id="namespace" >}}中
强制实施特定的
[Pod 安全标准（Pod Security Standard）](/zh-cn/docs/concepts/security/pod-security-standards/)，
或者检查安全上的缺陷。

一般来说，大多数应用程序需要对主机资源的有限制的访问，
这样它们可以在不访问主机信息的情况下，成功地以 root 账号（UID 0）运行。
但是，考虑到与 root 用户相关的特权，在编写应用程序容器时，你应该使用非 root 用户运行。
类似地，希望阻止客户端应用程序从其容器中逃逸的管理员，应该应用 **Baseline**
或 **Restricted** Pod 安全标准。


### 防止容器加载不需要的内核模块   {#preventing-containers-from-loading-unwanted-kernel-modules}
如果在某些情况下，Linux 内核会根据需要自动从磁盘加载内核模块，
这类情况的例子有挂接了一个硬件或挂载了一个文件系统。
与 Kubernetes 特别相关的是，即使是非特权的进程也可能导致某些网络协议相关的内核模块被加载，
而这只需创建一个适当类型的套接字。
这就可能允许攻击者利用管理员假定未使用的内核模块中的安全漏洞。

为了防止特定模块被自动加载，你可以将它们从节点上卸载或者添加规则来阻止这些模块。
在大多数 Linux 发行版上，你可以通过创建类似 `/etc/modprobe.d/kubernetes-blacklist.conf`
这种文件来做到这一点，其中的内容如下所示：

```
# DCCP is unlikely to be needed, has had multiple serious
# vulnerabilities, and is not well-maintained.
blacklist dccp

# SCTP is not used in most Kubernetes clusters, and has also had
# vulnerabilities in the past.
blacklist sctp
```

为了更大范围地阻止内核模块被加载，你可以使用 Linux 安全模块（如 SELinux）
来彻底拒绝容器的 `module_request` 权限，从而防止在任何情况下系统为容器加载内核模块。
（Pod 仍然可以使用手动加载的模块，或者使用由内核代表某些特权进程所加载的模块。）

### 限制网络访问

基于名字空间的[网络策略](/zh-cn/docs/tasks/administer-cluster/declare-network-policy/)
允许应用程序作者限制其它名字空间中的哪些 Pod 可以访问自身名字空间内的 Pod 和端口。
现在已经有许多支持网络策略的
[Kubernetes 网络驱动](/zh-cn/docs/concepts/cluster-administration/networking/)。

配额（Quota）和限制范围（Limit Range）也可用于控制用户是否可以请求节点端口或负载均衡服务。
在很多集群上，节点端口和负载均衡服务也可控制用户的应用程序是否在集群之外可见。

此外也可能存在一些基于插件或基于环境的网络规则，能够提供额外的保护能力。
例如各节点上的防火墙、物理隔离集群节点以防止串扰或者高级的网络策略等。

### 限制云元数据 API 访问

云平台（AWS、Azure、GCE 等）经常将 metadata 本地服务暴露给实例。
默认情况下，这些 API 可由运行在实例上的 Pod 访问，并且可以包含
该云节点的凭据或配置数据（如 kubelet 凭据）。
这些凭据可以用于在集群内升级或在同一账户下升级到其他云服务。

在云平台上运行 Kubernetes 时，需要限制对实例凭据的权限，使用
[网络策略](/zh-cn/docs/tasks/administer-cluster/declare-network-policy/)
限制 Pod 对元数据 API 的访问，并避免使用配置数据来传递机密信息。

### 控制 Pod 可以访问的节点

默认情况下，对 Pod 可以运行在哪些节点上是没有任何限制的。
Kubernetes 给最终用户提供了
一组丰富的策略用于[控制 Pod 所放置的节点位置](/zh-cn/docs/concepts/scheduling-eviction/assign-pod-node/)，
以及[基于污点的 Pod 放置和驱逐](/zh-cn/docs/concepts/scheduling-eviction/taint-and-toleration/)。
对于许多集群，使用这些策略来分离工作负载可以作为一种约定，要求作者遵守或者通过工具强制。

对于管理员，Beta 阶段的准入插件 `PodNodeSelector` 可用于强制某名字空间中的 Pod
使用默认的或特定的节点选择算符。
如果最终用户无法改变名字空间，这一机制可以有效地限制特定工作负载中所有 Pod 的放置位置。

## 保护集群组件免受破坏

本节描述保护集群免受破坏的一些常用模式。

### 限制访问 etcd

拥有对 API 的 etcd 后端的写访问权限相当于获得了整个集群的 root 权限，
读访问权限也可能被利用，实现相当快速的权限提升。
对于从 API 服务器访问其 etcd 服务器，管理员应该总是使用比较强的凭证，如通过 TLS
客户端证书来实现双向认证。
通常，我们建议将 etcd 服务器隔离到只有 API 服务器可以访问的防火墙后面。

{{< caution >}}
允许集群中其它组件对整个主键空间（keyspace）拥有读或写权限去访问 etcd 实例，
相当于授予这些组件集群管理员的访问权限。
对于非主控组件，强烈推荐使用不同的 etcd 实例，或者使用 etcd 的访问控制列表
来限制这些组件只能读或写主键空间的一个子集。
{{< /caution >}}

### 启用审计日志

[审计日志](/zh-cn/docs/tasks/debug/debug-cluster/audit/)是 Beta 特性，
负责记录 API 操作以便在发生破坏时进行事后分析。
建议启用审计日志，并将审计文件归档到安全服务器上。

### 限制使用 Alpha 和 Beta 特性

Kubernetes 的 Alpha 和 Beta 特性还在努力开发中，可能存在导致安全漏洞的缺陷或错误。
要始终评估 Alpha 和 Beta 特性可能给你的安全态势带来的风险。
当你怀疑存在风险时，可以禁用那些不需要使用的特性。

### 经常轮换基础设施证书

一项机密信息或凭据的生命期越短，攻击者就越难使用该凭据。
在证书上设置较短的生命期并实现自动轮换是控制安全的一个好方法。
使用身份验证提供程序时，应该使用那些可以控制所发布令牌的合法时长的提供程序，
并尽可能设置较短的生命期。
如果在外部集成场景中使用服务帐户令牌，则应该经常性地轮换这些令牌。
例如，一旦引导阶段完成，就应该撤销用于配置节点的引导令牌，或者取消它的授权。

### 在启用第三方集成之前，请先审查它们

许多集成到 Kubernetes 的第三方软件或服务都可能改变你的集群的安全配置。
启用集成时，在授予访问权限之前，你应该始终检查扩展所请求的权限。
例如，许多安全性集成中可能要求查看集群上的所有 Secret 的访问权限，
本质上该组件便成为了集群的管理员。
当有疑问时，如果可能的话，将要集成的组件限制在某指定名字空间中运行。

如果执行 Pod 创建操作的组件能够在 `kube-system` 这类名字空间中创建 Pod，
则这类组件也可能获得意外的权限，因为这些 Pod 可以访问服务账户的 Secret，
或者，如果对应服务帐户被授权访问宽松的
[PodSecurityPolicy](/zh-cn/docs/concepts/security/pod-security-policy/)，
它们就能以较高的权限运行。

如果你使用 [Pod 安全准入](/zh-cn/docs/concepts/security/pod-security-admission/)，
并且允许任何组件在一个允许执行特权 Pod 的名字空间中创建 Pod，这些 Pod
就可能从所在的容器中逃逸，利用被拓宽的访问权限来实现特权提升。

你不应该允许不可信的组件在任何系统名字空间（名字以 `kube-` 开头）中创建 Pod，
也不允许它们在访问权限授权可被利用来提升特权的名字空间中创建 Pod。

### 对 Secret 进行静态加密

一般情况下，etcd 数据库包含了通过 Kubernetes API 可以访问到的所有信息，
并且可能为攻击者提供对你的集群的状态的较多的可见性。
你要始终使用经过充分审查的备份和加密方案来加密备份数据，
并考虑在可能的情况下使用全盘加密。

对于 Kubernetes API 中的信息，Kubernetes 支持可选的[静态数据加密](/zh-cn/docs/tasks/administer-cluster/encrypt-data/)。
这让你可以确保当 Kubernetes 存储对象（例如 `Secret` 或 `ConfigMap`）的数据时，API 服务器写入的是加密的对象。
这种加密意味着即使有权访问 etcd 备份数据的某些人也无法查看这些对象的内容。
在 Kubernetes {{< skew currentVersion >}} 中，你也可以加密自定义资源；
针对以 CustomResourceDefinition 形式定义的扩展 API，对其执行静态加密的能力作为 v1.26
版本的一部分已添加到 Kubernetes。

### 接收安全更新和报告漏洞的警报

请加入 [kubernetes-announce](https://groups.google.com/forum/#!forum/kubernetes-announce)
组，这样你就能够收到有关安全公告的邮件。有关如何报告漏洞的更多信息，
请参见[安全报告](/zh-cn/docs/reference/issues-security/security/)页面。

## {{% heading "whatsnext" %}}

- 阅读[安全检查清单](/zh-cn/docs/concepts/security/security-checklist/)了解有关
  Kubernetes 安全指南的更多信息。

