---
title: 安全检查清单
description: >
  确保 Kubernetes 集群安全的基线检查清单。
content_type: concept
weight: 100
---

本清单旨在提供一个基本的指导列表，其中包含链接，指向各个主题的更为全面的文档。
此清单不求详尽无遗，是预计会不断演化的。

关于如何阅读和使用本文档：

- 主题的顺序并不代表优先级的顺序。
- 在每章节的列表下面的段落中，都详细列举了一些检查清项目。

{{< caution >}}
单靠检查清单是**不够的**，无法获得良好的安全态势。
实现良好的安全态势需要持续的关注和改进，实现安全上有备无患的目标道路漫长，清单可作为征程上的第一步。
对于你的特定安全需求，此清单中的某些建议可能过于严格或过于宽松。
由于 Kubernetes 的安全性并不是“一刀切”的，因此针对每一类检查清单项目都应该做价值评估。
{{< /caution >}}


## 认证和鉴权 {#authentication-authorization}

- [ ] 在启动后 `system:masters` 组不用于用户或组件的身份验证。
- [ ] kube-controller-manager 运行时要启用 `--use-service-account-credentials` 参数。
- [ ] 根证书要受到保护（或离线 CA，或一个具有有效访问控制的托管型在线 CA）。
- [ ] 中级证书和叶子证书的有效期不要超过未来 3 年。
- [ ] 存在定期访问审查的流程，审查间隔不要超过 24 个月。
- [ ] 遵循[基于角色的访问控制良好实践](/zh-cn/docs/concepts/security/rbac-good-practices/)，以获得与身份验证和授权相关的指导。

在启动后，用户和组件都不应以 `system:masters` 身份向 Kubernetes API 进行身份验证。
同样，应避免将任何 kube-controller-manager 以 `system:masters` 运行。
事实上，`system:masters` 应该只用作一个例外机制，而不是管理员用户。

## 网络安全 {#network-security}

- [ ] 使用的 CNI 插件可支持网络策略。
- [ ] 对集群中的所有工作负载应用入站和出站的网络策略。
- [ ] 落实每个名字空间内的默认网络策略，覆盖所有 Pod，拒绝一切访问。
- [ ] 如果合适，使用服务网格来加密集群内的所有通信。
- [ ] 不在互联网上公开 Kubernetes API、kubelet API 和 etcd。
- [ ] 过滤工作负载对云元数据 API 的访问。
- [ ] 限制使用 LoadBalancer 和 ExternalIP。

许多[容器网络接口（Container Network Interface，CNI）插件](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)提供了限制
Pod 可能与之通信的网络资源的功能。
这种限制通常通过[网络策略](/zh-cn/docs/concepts/services-networking/network-policies/)来完成，
网络策略提供了一种名字空间作用域的资源来定义规则。
在每个名字空间中，默认的网络策略会阻塞所有的出入站流量，并选择所有 Pod，
采用允许列表的方法很有用，可以确保不遗漏任何工作负载。

并非所有 CNI 插件都在传输过程中提供加密。
如果所选的插件缺少此功能，一种替代方案是可以使用服务网格来提供该功能。

控制平面的 etcd 数据存储应该实施访问限制控制，并且不要在互联网上公开。
此外，应使用双向 TLS（mTLS）与其进行安全通信。
用在这里的证书机构应该仅用于 etcd。

应该限制外部互联网对 Kubernetes API 服务器未公开的 API 的访问。
请小心，因为许多托管的 Kubernetes 发行版在默认情况下公开了 API 服务器。
当然，你可以使用堡垒机访问服务器。

对 [kubelet](/zh-cn/docs/reference/command-line-tools-reference/kubelet/) API 的访问应该受到限制，
并且不公开，当没有使用 `--config` 参数来设置配置文件时，默认的身份验证和鉴权设置是过于宽松的。

如果使用云服务供应商托管的 Kubernetes，在没有明确需要的情况下，
也应该限制或阻止从 Pod 对云元数据 API `169.254.169.254` 的访问，因为这可能泄露信息。

关于限制使用 LoadBalancer 和 ExternalIP 请参阅
[CVE-2020-8554：中间人使用 LoadBalancer 或 ExternalIP](https://github.com/kubernetes/kubernetes/issues/97076)
和
[DenyServiceExternalIPs 准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#denyserviceexternalips)获取更多信息。

## Pod 安全 {#pod-security}

- [ ] 仅在必要时才授予 `create`、`update`、`patch`、`delete` 工作负载的 RBAC 权限。
- [ ] 对所有名字空间实施适当的 Pod 安全标准策略，并强制执行。
- [ ] 为工作负载设置内存限制值，并确保限制值等于或者不高于请求值。
- [ ] 对敏感工作负载可以设置 CPU 限制。
- [ ] 对于支持 Seccomp 的节点，可以为程序启用合适的系统调用配置文件。
- [ ] 对于支持 AppArmor 或 SELinux 的系统，可以为程序启用合适的配置文件。

RBAC 的授权是至关重要的，
但[不能在足够细的粒度上对 Pod 的资源进行授权](/zh-cn/docs/concepts/security/rbac-good-practices/#workload-creation)，
也不足以对管理 Pod 的任何资源进行授权。
唯一的粒度是资源本身上的 API 动作，例如，对 Pod 的 `create`。
在未指定额外许可的情况下，创建这些资源的权限允许直接不受限制地访问集群的可调度节点。

[Pod 安全性标准](/zh-cn/docs/concepts/security/pod-security-standards/)定义了三种不同的策略：
特权策略（Privileged）、基线策略（Baseline）和限制策略（Restricted），它们限制了 `PodSpec` 中关于安全的字段的设置。
这些标准可以通过默认启用的新的
[Pod 安全性准入](/zh-cn/docs/concepts/security/pod-security-admission/)或第三方准入 Webhook 在名字空间级别强制执行。
请注意，与它所取代的、已被移除的 PodSecurityPolicy 准入机制相反，
[Pod 安全性准入](/zh-cn/docs/concepts/security/pod-security-admission/)可以轻松地与准入 Webhook 和外部服务相结合使用。

`restricted` Pod 安全准入策略是 [Pod 安全性标准](/zh-cn/docs/concepts/security/pod-security-standards/)集中最严格的策略，
可以在[多种种模式下运行](/zh-cn/docs/concepts/security/pod-security-admission/#pod-security-admission-labels-for-namespaces)，
根据最佳安全实践，逐步地采用 `warn`、`audit` 或者 `enforce`
模式以应用最合适的[安全上下文（Security Context）](/zh-cn/docs/tasks/configure-pod-container/security-context/)。
尽管如此，对于特定的用例，应该单独审查 Pod 的[安全上下文](/zh-cn/docs/tasks/configure-pod-container/security-context/)，
以限制 Pod 在预定义的安全性标准之上可能具有的特权和访问权限。

有关 [Pod 安全性](/zh-cn/docs/concepts/security/pod-security-admission/)的实践教程，
请参阅博文 [Kubernetes 1.23：Pod 安全性升级到 Beta](/blog/2021/12/09/pod-security-admission-beta/)。

为了限制一个 Pod 可以使用的内存和 CPU 资源，
应该设置 Pod 在节点上可消费的[内存和 CPU 限制](/zh-cn/docs/concepts/configuration/manage-resources-containers/),
从而防止来自恶意的或已被攻破的工作负载的潜在 DoS 攻击。这种策略可以由准入控制器强制执行。
请注意，CPU 限制设置可能会影响 CPU 用量，从而可能会对自动扩缩功能或效率产生意外的影响，
换言之，系统会在可用的 CPU 资源下最大限度地运行进程。

{{< caution >}}
内存限制高于请求的，可能会使整个节点面临 OOM 问题。
{{< /caution >}}

### 启用 Seccomp {#enabling-seccomp}

Seccomp 通过减少容器内对 Linux 内核的系统调用（System Call）以缩小攻击面，从而提高工作负载的安全性。
Seccomp 过滤器模式借助 BPF 创建了配置文件（Profile），文件中设置对具体系统调用的允许或拒绝，
可以针对单个工作负载上启用这类 Seccomp 配置文件。你可以阅读相应的[安全教程](/zh-cn/docs/tutorials/security/seccomp/)。
此外，[Kubernetes Security Profiles Operator](https://github.com/kubernetes-sigs/security-profiles-operator)
是一个方便在集群中管理和使用 Seccomp 的项目。

从历史背景看，请注意 Docker 自 2016 年以来一直使用[默认的 Seccomp 配置文件](https://docs.docker.com/engine/security/seccomp/)，
仅允许来自 [Docker Engine 1.10](https://www.docker.com/blog/docker-engine-1-10-security/) 的很小的一组系统调用，
但是，在默认情况下 Kubernetes 仍不限制工作负载。
默认的 Seccomp 配置文件也可以在
[containerd](https://github.com/containerd/containerd/blob/main/contrib/seccomp/seccomp_default.go) 中找到。
幸运的是，[Seccomp Default](/blog/2021/08/25/seccomp-default/) 可将默认的 Seccomp 配置文件用于所有工作负载，
这是一项新的 Alpha 功能，现在可以启用和测试了。

{{< note >}}
Seccomp 仅适用于 Linux 节点。
{{< /note >}}

### 启用 AppArmor 或 SELinux {#enabling-appArmor-or-SELinux}

#### AppArmor

[AppArmor](https://apparmor.net/) 是一个 Linux 内核安全模块，
可以提供一种简单的方法来实现强制访问控制（Mandatory Access Control, MAC）并通过系统日志进行更好地审计。
要在 Kubernetes 中[启用 AppArmor](/zh-cn/docs/tutorials/security/apparmor/)，至少需要 1.4 版本。
与 Seccomp 一样，AppArmor 也通过配置文件进行配置，
其中每个配置文件要么在强制（Enforcing）模式下运行，即阻止访问不允许的资源，要么在投诉（Complaining）模式下运行，只报告违规行为。
AppArmor 配置文件是通过注解的方式，以容器为粒度强制执行的，允许进程获得刚好合适的权限。

{{< note >}}
AppArmor 仅在 Linux 节点上可用，
在[一些 Linux 发行版](https://gitlab.com/apparmor/apparmor/-/wikis/home#distributions-and-ports)中已启用。
{{< /note >}}

#### SELinux

[SELinux](https://github.com/SELinuxProject/selinux-notebook/blob/main/src/selinux_overview.md)
也是一个 Linux 内核安全模块，可以提供支持访问控制安全策略的机制，包括强制访问控制（MAC）。
SELinux 标签可以[通过 `securityContext` 节](/zh-cn/docs/tasks/configure-pod-container/security-context/#assign-selinux-labels-to-a-container)指配给容器或 Pod。

{{< note >}}
SELinux 仅在 Linux 节点上可用，
在[一些 Linux 发行版](https://en.wikipedia.org/wiki/Security-Enhanced_Linux#Implementations)中已启用。
{{< /note >}}

## 日志和审计   {#logs-and-auditing}

- [ ] 审计日志（如果启用）将受到保护以防止常规访问。
- [ ] `/logs` API 被禁用（你所运行的 kube-apiserver 设置了 `--enable-logs-handler=false`）。

  Kubernetes 包含一个 `/logs` API 端点，默认启用。
  这个端点允许用户通过 HTTP 来请求 API 服务器的 `/var/log` 目录的内容。
  访问此端点需要身份验证。

允许大范围访问 Kubernetes 日志可能会令安全信息被潜在的攻击者利用。

一个好的做法是设置一个单独的方式来收集和聚合控制平面日志，
并且不要使用 `/logs` API 端点。另一个使用场景是你运行控制平面时启用了 `/logs` API 端点并
（在运行 API 服务器的主机或容器内）将 `/var/log` 的内容限制为仅保存 Kubernetes API 服务器日志。

## Pod 布局 {#pod-placement}

- [ ] Pod 布局是根据应用程序的敏感级别来完成的。
- [ ] 敏感应用程序在节点上隔离运行或使用特定的沙箱运行时运行。

处于不同敏感级别的 Pod，例如，应用程序 Pod 和 Kubernetes API 服务器，应该部署到不同的节点上。
节点隔离的目的是防止应用程序容器的逃逸，进而直接访问敏感度更高的应用，
甚至轻松地改变集群工作机制。
这种隔离应该被强制执行，以防止 Pod 集合被意外部署到同一节点上。
可以通过以下功能实现：

[节点选择器（Node Selector）](/zh-cn/docs/concepts/scheduling-eviction/assign-pod-node/)
: 作为 Pod 规约的一部分来设置的键值对，指定 Pod 可部署到哪些节点。
  通过 [PodNodeSelector](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#podnodeselector)
  准入控制器可以在名字空间和集群级别强制实施节点选择。

[PodTolerationRestriction](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#podtolerationrestriction)
: [容忍度](/zh-cn/docs/concepts/scheduling-eviction/taint-and-toleration/)准入控制器，
  允许管理员设置在名字空间内允许使用的容忍度。
  名字空间中的 Pod 只能使用名字空间对象的注解键上所指定的容忍度，这些键提供默认和允许的容忍度集合。

[RuntimeClass](/zh-cn/docs/concepts/containers/runtime-class/)
: RuntimeClass 是一个用于选择容器运行时配置的特性，容器运行时配置用于运行 Pod 中的容器，
  并以性能开销为代价提供或多或少的主机隔离能力。

## Secrets {#secrets}

- [ ] 不用 ConfigMap 保存机密数据。
- [ ] 为 Secret API 配置静态加密。
- [ ] 如果合适，可以部署和使用一种机制，负责注入保存在第三方存储中的 Secret。
- [ ] 不应该将服务账号令牌挂载到不需要它们的 Pod 中。
- [ ] 使用[绑定的服务账号令牌卷](/zh-cn/docs/reference/access-authn-authz/service-accounts-admin/#bound-service-account-token-volume)，
  而不要使用不会过期的令牌。

Pod 所需的秘密信息应该存储在 Kubernetes Secret 中，而不是像 ConfigMap 这样的替代品中。
存储在 etcd 中的 Secret 资源应该被静态加密。

需要 Secret 的 Pod 应该通过卷自动挂载这些信息，
最好使用 [`emptyDir.medium` 选项](/zh-cn/docs/concepts/storage/volumes/#emptydir)存储在内存中。
该机制还可以用于从第三方存储中注入 Secret 作为卷，如 [Secret Store CSI 驱动](https://secrets-store-csi-driver.sigs.k8s.io/)。
与通过 RBAC 来允许 Pod 服务账号访问 Secret 相比，应该优先使用上述机制。这种机制允许将 Secret 作为环境变量或文件添加到 Pod 中。
请注意，与带访问权限控制的文件相比，由于日志的崩溃转储，以及 Linux 的环境变量的非机密性，环境变量方法可能更容易发生泄漏。

不应该将服务账号令牌挂载到不需要它们的 Pod 中。这可以通过在服务账号内将
[`automountServiceAccountToken`](/zh-cn/docs/tasks/configure-pod-container/configure-service-account/#use-the-default-service-account-to-access-the-api-server)
设置为 `false` 来完成整个名字空间范围的配置，或者也可以单独在 Pod 层面定制。
对于 Kubernetes v1.22 及更高版本，
请使用[绑定服务账号](/zh-cn/docs/reference/access-authn-authz/service-accounts-admin/#bound-service-account-token-volume)作为有时间限制的服务账号凭证。

## 镜像 {#images}

- [ ] 尽量减少容器镜像中不必要的内容。
- [ ] 容器镜像配置为以非特权用户身份运行。
- [ ] 对容器镜像的引用是通过 Sha256 摘要实现的，而不是标签（tags），
  或者[通过准入控制器](/zh-cn/docs/tasks/administer-cluster/verify-signed-artifacts/#verifying-image-signatures-with-admission-controller)在部署时验证镜像的数字签名来验证镜像的来源。
- [ ] 在创建和部署过程中定期扫描容器镜像，并对已知的漏洞软件进行修补。

容器镜像应该包含运行其所打包的程序所需要的最少内容。
最好，只使用程序及其依赖项，基于最小的基础镜像来构建镜像。
尤其是，在生产中使用的镜像不应包含 Shell 或调试工具，
因为可以使用[临时调试容器](/zh-cn/docs/tasks/debug/debug-application/debug-running-pod/#ephemeral-container)进行故障排除。

构建镜像时使用 [Dockerfile 中的 `USER`](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user)
指令直接开始使用非特权用户。
[安全上下文（Security Context）](/zh-cn/docs/tasks/configure-pod-container/security-context/#set-the-security-context-for-a-pod)
允许使用 `runAsUser` 和 `runAsGroup` 来指定使用特定的用户和组来启动容器镜像，
即使没有在镜像清单文件（Manifest）中指定这些配置信息。
不过，镜像层中的文件权限设置可能无法做到在不修改镜像的情况下，使用新的非特权用户来启动进程。

避免使用镜像标签来引用镜像，尤其是 `latest` 标签，因为标签对应的镜像可以在仓库中被轻松地修改。
首选使用完整的 `Sha256` 摘要，该摘要对特定镜像清单文件而言是唯一的。
可以通过 [ImagePolicyWebhook](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#imagepolicywebhook)
强制执行此策略。
镜像签名还可以在部署时由[准入控制器自动验证](/zh-cn/docs/tasks/administer-cluster/verify-signed-artifacts/#verifying-image-signatures-with-admission-controller)，
以验证其真实性和完整性。

扫描容器镜像可以防止关键性的漏洞随着容器镜像一起被部署到集群中。
镜像扫描应在将容器镜像部署到集群之前完成，通常作为 CI/CD 流水线中的部署过程的一部分来完成。
镜像扫描的目的是获取有关容器镜像中可能存在的漏洞及其预防措施的信息，
例如使用[公共漏洞评分系统 （Common Vulnerability Scoring System，CVSS）](https://www.first.org/cvss/)评分。
如果镜像扫描的结果与管道合性规则匹配，则只有经过正确修补的容器镜像才会最终进入生产环境。

## 准入控制器 {#admission-controllers}

- [ ] 选择启用适当的准入控制器。
- [ ] Pod 安全策略由 Pod 安全准入强制执行，或者和 Webhook 准入控制器一起强制执行。
- [ ] 保证准入链插件和 Webhook 的配置都是安全的。

准入控制器可以帮助提高集群的安全性。
然而，由于它们是对 API 服务器的扩展，其自身可能会带来风险，
所以它们[应该得到适当的保护](/blog/2022/01/19/secure-your-admission-controllers-and-webhooks/)。

下面列出了一些准入控制器，可以考虑用这些控制器来增强集群和应用程序的安全状况。
列表中包括了可能在本文档其他部分曾提及的控制器。

第一组准入控制器包括[默认启用的插件](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#which-plugins-are-enabled-by-default)，
除非你知道自己在做什么，否则请考虑保持它们处于被启用的状态：

[`CertificateApproval`](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#certificateapproval)
: 执行额外的授权检查，以确保审批用户具有审批证书请求的权限。

[`CertificateSigning`](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#certificatesigning)
: 执行其他授权检查，以确保签名用户具有签名证书请求的权限。

[`CertificateSubjectRestriction`](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#certificatesubjectrestriction)
: 拒绝将 `group`（或 `organization attribute`）设置为 `system:masters` 的所有证书请求。

[`LimitRanger`](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#limitranger)
: 强制执行 LimitRange API 约束。

[`MutatingAdmissionWebhook`](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#mutatingadmissionwebhook)
: 允许通过 Webhook 使用自定义控制器，这些控制器可能会变更它所审查的请求。

[`PodSecurity`](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#podsecurity)
: Pod Security Policy 的替代品，用于约束所部署 Pod 的安全上下文。

[`ResourceQuota`](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#resourcequota)
: 强制执行资源配额，以防止资源被过度使用。

[`ValidatingAdmissionWebhook`](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#validatingadmissionwebhook)
: 允许通过 Webhook 使用自定义控制器，这些控制器不变更它所审查的请求。

第二组包括默认情况下没有启用、但处于正式发布状态的插件，建议启用这些插件以改善你的安全状况：

[`DenyServiceExternalIPs`](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#denyserviceexternalips)
: 拒绝使用 `Service.spec.externalIPs` 字段，已有的 Service 不受影响，新增或者变更时不允许使用。
  这是 [CVE-2020-8554：中间人使用 LoadBalancer 或 ExternalIP](https://github.com/kubernetes/kubernetes/issues/97076)
  的缓解措施。

[`NodeRestriction`](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#noderestriction)
: 将 kubelet 的权限限制为只能修改其拥有的 Pod API 资源或代表其自身的节点 API 资源。
  此插件还可以防止 kubelet 使用 `node-restriction.kubernetes.io/` 注解，
  攻击者可以使用该注解来访问 kubelet 的凭证，从而影响所控制的节点上的 Pod 布局。

第三组包括默认情况下未启用，但可以考虑在某些场景下启用的插件：

[`AlwaysPullImages`](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#alwayspullimages)
: 强制使用最新版本标记的镜像，并确保部署者有权使用该镜像。

[`ImagePolicyWebhook`](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#imagepolicywebhook)
: 允许通过 Webhook 对镜像强制执行额外的控制。

## 接下来  {#what-is-next}

- [RBAC 良好实践](/zh-cn/docs/concepts/security/rbac-good-practices/)提供有关授权的更多信息。
- [保护集群](/zh-cn/docs/tasks/administer-cluster/securing-a-cluster/)提供如何保护集群免受意外或恶意访问的信息。
- [集群多租户指南](/zh-cn/docs/concepts/security/multi-tenancy/)提供有关多租户的配置选项建议和最佳实践。
- [博文“深入了解 NSA/CISA Kubernetes 强化指南”](/blog/2021/10/05/nsa-cisa-kubernetes-hardening-guidance/#building-secure-container-images)为强化
  Kubernetes 集群提供补充资源。
