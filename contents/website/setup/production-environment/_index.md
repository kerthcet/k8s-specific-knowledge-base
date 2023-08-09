---
title: 生产环境
weight: 30
no_list: true
---


生产质量的 Kubernetes 集群需要规划和准备。
如果你的 Kubernetes 集群是用来运行关键负载的，该集群必须被配置为弹性的（Resilient）。
本页面阐述你在安装生产就绪的集群或将现有集群升级为生产用途时可以遵循的步骤。
如果你已经熟悉生产环境安装，因此只关注一些链接，则可以跳到[接下来](#what-s-next)节。


## 生产环境考量  {#production-considerations}

通常，一个生产用 Kubernetes 集群环境与个人学习、开发或测试环境所使用的 Kubernetes 相比有更多的需求。
生产环境可能需要被很多用户安全地访问，需要提供一致的可用性，以及能够与需求变化相适配的资源。

在你决定在何处运行你的生产用 Kubernetes 环境（在本地或者在云端），
以及你希望承担或交由他人承担的管理工作量时，
需要考察以下因素如何影响你对 Kubernetes 集群的需求：

- **可用性**：一个单机的 Kubernetes [学习环境](/zh-cn/docs/setup/#学习环境)
  具有单点失效特点。创建高可用的集群则意味着需要考虑：
  - 将控制面与工作节点分开
  - 在多个节点上提供控制面组件的副本
  - 为针对集群的 {{< glossary_tooltip term_id="kube-apiserver" text="API 服务器" >}}
    的流量提供负载均衡
  - 随着负载的合理需要，提供足够的可用的（或者能够迅速变为可用的）工作节点

- **规模**：如果你预期你的生产用 Kubernetes 环境要承受固定量的请求，
  你可能可以针对所需要的容量来一次性完成安装。
  不过，如果你预期服务请求会随着时间增长，或者因为类似季节或者特殊事件的原因而发生剧烈变化，
  你就需要规划如何处理请求上升时对控制面和工作节点的压力，或者如何缩减集群规模以减少未使用资源的消耗。

- **安全性与访问管理**：在你自己的学习环境 Kubernetes 集群上，你拥有完全的管理员特权。
  但是针对运行着重要工作负载的共享集群，用户账户不止一两个时，
  就需要更细粒度的方案来确定谁或者哪些主体可以访问集群资源。
  你可以使用基于角色的访问控制（[RBAC](/zh-cn/docs/reference/access-authn-authz/rbac/)）
  和其他安全机制来确保用户和负载能够访问到所需要的资源，
  同时确保工作负载及集群自身仍然是安全的。
  你可以通过管理[策略](/zh-cn/docs/concepts/policy/)和
  [容器资源](/zh-cn/docs/concepts/configuration/manage-resources-containers)
  来针对用户和工作负载所可访问的资源设置约束。

在自行构建 Kubernetes 生产环境之前，
请考虑将这一任务的部分或者全部交给[云方案承包服务](/zh-cn/docs/setup/production-environment/turnkey-solutions)提供商或者其他
[Kubernetes 合作伙伴](/zh-cn/partners/)。选项有：

- **无服务**：仅是在第三方设备上运行负载，完全不必管理集群本身。
  你需要为 CPU 用量、内存和磁盘请求等付费。
- **托管控制面**：让供应商决定集群控制面的规模和可用性，并负责打补丁和升级等操作。
- **托管工作节点**：配置一个节点池来满足你的需要，由供应商来确保节点始终可用，并在需要的时候完成升级。
- **集成**：有一些供应商能够将 Kubernetes 与一些你可能需要的其他服务集成，
  这类服务包括存储、容器镜像仓库、身份认证方法以及开发工具等。

无论你是自行构造一个生产用 Kubernetes 集群还是与合作伙伴一起协作，
请审阅下面章节以评估你的需求，因为这关系到你的集群的**控制面**、**工作节点**、**用户访问**以及**负载资源**。

## 生产用集群安装  {#production-cluster-setup}

在生产质量的 Kubernetes 集群中，控制面用不同的方式来管理集群和可以分布到多个计算机上的服务。
每个工作节点则代表的是一个可配置来运行 Kubernetes Pod 的实体。

### 生产用控制面  {#production-control-plane}

最简单的 Kubernetes 集群中，整个控制面和工作节点服务都运行在同一台机器上。
你可以通过添加工作节点来提升环境运算能力，正如
[Kubernetes 组件](/zh-cn/docs/concepts/overview/components/)示意图所示。
如果只需要集群在很短的一段时间内可用，或者可以在某些事物出现严重问题时直接丢弃，
这种配置可能符合你的需要。

如果你需要一个更为持久的、高可用的集群，那么就需要考虑扩展控制面的方式。
根据设计，运行在一台机器上的单机控制面服务不是高可用的。
如果你认为保持集群的正常运行并需要确保它在出错时可以被修复是很重要的，
可以考虑以下步骤：

- **选择部署工具**：你可以使用类似 kubeadm、kops 和 kubespray 这类工具来部署控制面。
  参阅[使用部署工具安装 Kubernetes](/zh-cn/docs/setup/production-environment/tools/)
  以了解使用这类部署方法来完成生产就绪部署的技巧。
  存在不同的[容器运行时](/zh-cn/docs/setup/production-environment/container-runtimes/)
  可供你的部署采用。
- **管理证书**：控制面服务之间的安全通信是通过证书来完成的。
  证书是在部署期间自动生成的，或者你也可以使用自己的证书机构来生成它们。
  参阅 [PKI 证书和需求](/zh-cn/docs/setup/best-practices/certificates/)了解细节。
- **为 API 服务器配置负载均衡**：配置负载均衡器来将外部的 API 请求散布给运行在不同节点上的 API 服务实例。
  参阅[创建外部负载均衡器](/zh-cn/docs/tasks/access-application-cluster/create-external-load-balancer/)了解细节。
- **分离并备份 etcd 服务**：etcd 服务可以运行于其他控制面服务所在的机器上，
  也可以运行在不同的机器上以获得更好的安全性和可用性。
  因为 etcd 存储着集群的配置数据，应该经常性地对 etcd 数据库进行备份，
  以确保在需要的时候你可以修复该数据库。与配置和使用 etcd 相关的细节可参阅
  [etcd FAQ](/https://etcd.io/docs/v3.5/faq/)。
  更多的细节可参阅[为 Kubernetes 运维 etcd 集群](/zh-cn/docs/tasks/administer-cluster/configure-upgrade-etcd/)
  和[使用 kubeadm 配置高可用的 etcd 集群](/zh-cn/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/)。
- **创建多控制面系统**：为了实现高可用性，控制面不应被限制在一台机器上。
  如果控制面服务是使用某 init 服务（例如 systemd）来运行的，每个服务应该至少运行在三台机器上。
  不过，将控制面作为服务运行在 Kubernetes Pod 中可以确保你所请求的个数的服务始终保持可用。
  调度器应该是可容错的，但不是高可用的。
  某些部署工具会安装 [Raft](https://raft.github.io/) 票选算法来对 Kubernetes 服务执行领导者选举。
  如果主节点消失，另一个服务会被选中并接手相应服务。
- **跨多个可用区**：如果保持你的集群一直可用这点非常重要，可以考虑创建一个跨多个数据中心的集群；
  在云环境中，这些数据中心被视为可用区。若干个可用区在一起可构成地理区域。
  通过将集群分散到同一区域中的多个可用区内，即使某个可用区不可用，整个集群能够继续工作的机会也大大增加。
  更多的细节可参阅[跨多个可用区运行](/zh-cn/docs/setup/best-practices/multiple-zones/)。
- **管理演进中的特性**：如果你计划长时间保留你的集群，就需要执行一些维护其健康和安全的任务。
  例如，如果你采用 kubeadm 安装的集群，
  则有一些可以帮助你完成
  [证书管理](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/)
  和[升级 kubeadm 集群](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade)
  的指令。
  参见[管理集群](/zh-cn/docs/tasks/administer-cluster)了解一个 Kubernetes
  管理任务的较长列表。

如要了解运行控制面服务时可使用的选项，可参阅
[kube-apiserver](/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver/)、
[kube-controller-manager](/zh-cn/docs/reference/command-line-tools-reference/kube-controller-manager/) 和
[kube-scheduler](/zh-cn/docs/reference/command-line-tools-reference/kube-scheduler/) 
组件参考页面。
如要了解高可用控制面的例子，可参阅[高可用拓扑结构选项](/zh-cn/docs/setup/production-environment/tools/kubeadm/ha-topology/)、
[使用 kubeadm 创建高可用集群](/zh-cn/docs/setup/production-environment/tools/kubeadm/high-availability/)
以及[为 Kubernetes 运维 etcd 集群](/zh-cn/docs/tasks/administer-cluster/configure-upgrade-etcd/)。
关于制定 etcd 备份计划，可参阅[对 etcd 集群执行备份](/zh-cn/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster)。

### 生产用工作节点   {#production-worker-nodes}

生产质量的工作负载需要是弹性的；它们所依赖的其他组件（例如 CoreDNS）也需要是弹性的。
无论你是自行管理控制面还是让云供应商来管理，你都需要考虑如何管理工作节点
（有时也简称为**节点**）。

- **配置节点**：节点可以是物理机或者虚拟机。如果你希望自行创建和管理节点，
  你可以安装一个受支持的操作系统，之后添加并运行合适的[节点服务](/zh-cn/docs/concepts/overview/components/#node-components)。考虑：
  - 在安装节点时要通过配置适当的内存、CPU 和磁盘读写速率、存储容量来满足你的负载的需求。
  - 是否通用的计算机系统即足够，还是你有负载需要使用 GPU 处理器、Windows 节点或者 VM 隔离。
- **验证节点**：参阅[验证节点配置](/zh-cn/docs/setup/best-practices/node-conformance/)以了解如何确保节点满足加入到 Kubernetes 集群的需求。
- **添加节点到集群中**：如果你自行管理你的集群，你可以通过安装配置你的机器，
  之后或者手动加入集群，或者让它们自动注册到集群的 API 服务器。
  参阅[节点](/zh-cn/docs/concepts/architecture/nodes/)节，了解如何配置 Kubernetes 以便以这些方式来添加节点。
- **扩缩节点**：制定一个扩充集群容量的规划，你的集群最终会需要这一能力。
  参阅[大规模集群考察事项](/zh-cn/docs/setup/best-practices/cluster-large/)
  以确定你所需要的节点数；
  这一规模是基于你要运行的 Pod 和容器个数来确定的。
  如果你自行管理集群节点，这可能意味着要购买和安装你自己的物理设备。
- **节点自动扩缩容**：大多数云供应商支持
  [集群自动扩缩器（Cluster Autoscaler）](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler#readme)
  以便替换不健康的节点、根据需求来增加或缩减节点个数。
  参阅[常见问题](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md)
  了解自动扩缩器的工作方式，并参阅
  [Deployment](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler#deployment)
  了解不同云供应商是如何实现集群自动扩缩器的。
  对于本地集群，有一些虚拟化平台可以通过脚本来控制按需启动新节点。
- **安装节点健康检查**：对于重要的工作负载，你会希望确保节点以及在节点上运行的 Pod 处于健康状态。
  通过使用 [Node Problem Detector](/zh-cn/docs/tasks/debug/debug-cluster/monitor-node-health/)，
  你可以确保你的节点是健康的。

### 生产级用户环境   {#production-user-management}

在生产环境中，情况可能不再是你或者一小组人在访问集群，而是几十上百人需要访问集群。
在学习环境或者平台原型环境中，你可能具有一个可以执行任何操作的管理账号。
在生产环境中，你会需要对不同名字空间具有不同访问权限级别的很多账号。

建立一个生产级别的集群意味着你需要决定如何有选择地允许其他用户访问集群。
具体而言，你需要选择验证尝试访问集群的人的身份标识（身份认证），
并确定他们是否被许可执行他们所请求的操作（鉴权）：

- **认证（Authentication）**：API 服务器可以使用客户端证书、持有者令牌、
  身份认证代理或者 HTTP 基本认证机制来完成身份认证操作。
  你可以选择你要使用的认证方法。通过使用插件，
  API 服务器可以充分利用你所在组织的现有身份认证方法，
  例如 LDAP 或者 Kerberos。
  关于认证 Kubernetes 用户身份的不同方法的描述，
  可参阅[身份认证](/zh-cn/docs/reference/access-authn-authz/authentication/)。
- **鉴权（Authorization）**：当你准备为一般用户执行权限判定时，
  你可能会需要在 RBAC 和 ABAC 鉴权机制之间做出选择。
  参阅[鉴权概述](/zh-cn/docs/reference/access-authn-authz/authorization/)，
  了解对用户账户（以及访问你的集群的服务账户）执行鉴权的不同模式。
  - **基于角色的访问控制**（[RBAC](/zh-cn/docs/reference/access-authn-authz/rbac/)）：
    让你通过为通过身份认证的用户授权特定的许可集合来控制集群访问。
    访问许可可以针对某特定名字空间（Role）或者针对整个集群（ClusterRole）。
    通过使用 RoleBinding 和 ClusterRoleBinding 对象，这些访问许可可以被关联到特定的用户身上。
  - **基于属性的访问控制**（[ABAC](/zh-cn/docs/reference/access-authn-authz/abac/)）：
    让你能够基于集群中资源的属性来创建访问控制策略，基于对应的属性来决定允许还是拒绝访问。
    策略文件的每一行都给出版本属性（apiVersion 和 kind）以及一个规约属性的映射，
    用来匹配主体（用户或组）、资源属性、非资源属性（/version 或 /apis）和只读属性。
    参阅[示例](/zh-cn/docs/reference/access-authn-authz/abac/#examples)以了解细节。

作为在你的生产用 Kubernetes 集群中安装身份认证和鉴权机制的负责人，要考虑的事情如下：

- **设置鉴权模式**：当 Kubernetes API 服务器（[kube-apiserver](/docs/reference/command-line-tools-reference/kube-apiserver/)）启动时，
  所支持的鉴权模式必须使用 `--authorization-mode` 标志配置。
  例如，`kube-apiserver.yaml`（位于 `/etc/kubernetes/manifests` 下）中对应的标志可以设置为 `Node,RBAC`。
  这样就会针对已完成身份认证的请求执行 Node 和 RBAC 鉴权。
- **创建用户证书和角色绑定（RBAC）**：如果你在使用 RBAC 鉴权，用户可以创建由集群 CA 签名的
  CertificateSigningRequest（CSR）。接下来你就可以将 Role 和 ClusterRole 绑定到每个用户身上。
  参阅[证书签名请求](/zh-cn/docs/reference/access-authn-authz/certificate-signing-requests/)了解细节。
- **创建组合属性的策略（ABAC）**：如果你在使用 ABAC 鉴权，
  你可以设置属性组合以构造策略对所选用户或用户组执行鉴权，
  判定他们是否可访问特定的资源（例如 Pod）、名字空间或者 apiGroup。
  进一步的详细信息可参阅[示例](/zh-cn/docs/reference/access-authn-authz/abac/#examples)。
- **考虑准入控制器**：针对指向 API 服务器的请求的其他鉴权形式还包括
  [Webhook 令牌认证](/zh-cn/docs/reference/access-authn-authz/authentication/#webhook-token-authentication)。
  Webhook 和其他特殊的鉴权类型需要通过向 API
  服务器添加[准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/)来启用。

## 为负载资源设置约束  {#set-limits-on-workload-resources}

生产环境负载的需求可能对 Kubernetes 的控制面内外造成压力。
在针对你的集群的负载执行配置时，要考虑以下条目：

- **设置名字空间限制**：为每个名字空间的内存和 CPU 设置配额。
  参阅[管理内存、CPU 和 API 资源](/zh-cn/docs/tasks/administer-cluster/manage-resources/)以了解细节。
  你也可以设置[层次化名字空间](/blog/2020/08/14/introducing-hierarchical-namespaces/)来继承这类约束。
- **为 DNS 请求做准备**：如果你希望工作负载能够完成大规模扩展，你的 DNS 服务也必须能够扩大规模。
  参阅[自动扩缩集群中 DNS 服务](/zh-cn/docs/tasks/administer-cluster/dns-horizontal-autoscaling/)。
- **创建额外的服务账户**：用户账户决定用户可以在集群上执行的操作，服务账号则定义的是在特定名字空间中
  Pod 的访问权限。默认情况下，Pod 使用所在名字空间中的 default 服务账号。
  参阅[管理服务账号](/zh-cn/docs/reference/access-authn-authz/service-accounts-admin/)以了解如何创建新的服务账号。
  例如，你可能需要：
  - 为 Pod 添加 Secret，以便 Pod 能够从某特定的容器镜像仓库拉取镜像。
    参阅[为 Pod 配置服务账号](/zh-cn/docs/tasks/configure-pod-container/configure-service-account/)以获得示例。
  - 为服务账号设置 RBAC 访问许可。参阅[服务账号访问许可](/zh-cn/docs/reference/access-authn-authz/rbac/#service-account-permissions)了解细节。

## {{% heading "whatsnext" %}}

- 决定你是想自行构造自己的生产用 Kubernetes，
  还是从某可用的[云服务外包厂商](/zh-cn/docs/setup/production-environment/turnkey-solutions/)或
  [Kubernetes 合作伙伴](/zh-cn/partners/)获得集群。
- 如果你决定自行构造集群，则需要规划如何处理[证书](/zh-cn/docs/setup/best-practices/certificates/)并为类似
  [etcd](/zh-cn/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/) 和
  [API 服务器](/zh-cn/docs/setup/production-environment/tools/kubeadm/ha-topology/)这些功能组件配置高可用能力。
- 选择使用 [kubeadm](/zh-cn/docs/setup/production-environment/tools/kubeadm/)、
  [kops](/zh-cn/docs/setup/production-environment/tools/kops/) 或
  [Kubespray](/zh-cn/docs/setup/production-environment/tools/kubespray/) 作为部署方法。
- 通过决定[身份认证](/zh-cn/docs/reference/access-authn-authz/authentication/)和[鉴权](/zh-cn/docs/reference/access-authn-authz/authorization/)方法来配置用户管理。
- 通过配置[资源限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/)、
  [DNS 自动扩缩](/zh-cn/docs/tasks/administer-cluster/dns-horizontal-autoscaling/)和[服务账号](/zh-cn/docs/reference/access-authn-authz/service-accounts-admin/)来为应用负载作准备。
