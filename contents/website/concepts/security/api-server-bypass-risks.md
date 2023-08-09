---
title: Kubernetes API 服务器旁路风险
description: >
  与 API 服务器及其他组件相关的安全架构信息
content_type: concept
weight: 90
---


Kubernetes API 服务器是外部（用户和服务）与集群交互的主要入口。

API 服务器作为交互的主要入口，还提供了几种关键的内置安全控制，
例如审计日志和{{< glossary_tooltip text="准入控制器" term_id="admission-controller" >}}。
但有一些方式可以绕过这些安全控制从而修改集群的配置或内容。

本页描述了绕过 Kubernetes API 服务器中内置安全控制的几种方式，
以便集群运维人员和安全架构师可以确保这些绕过方式被适当地限制。

## 静态 Pod {#static-pods}

每个节点上的 {{< glossary_tooltip text="kubelet" term_id="kubelet" >}}
会加载并直接管理集群中存储在指定目录中或从特定 URL
获取的[**静态 Pod**](/zh-cn/docs/tasks/configure-pod-container/static-pod) 清单。
API 服务器不管理这些静态 Pod。对该位置具有写入权限的攻击者可以修改从该位置加载的静态 Pod 的配置，或引入新的静态 Pod。

静态 Pod 被限制访问 Kubernetes API 中的其他对象。例如，你不能将静态 Pod 配置为从集群挂载 Secret。
但是，这些 Pod 可以执行其他安全敏感的操作，例如挂载来自下层节点的 `hostPath` 卷。

默认情况下，kubelet 会创建一个{{< glossary_tooltip text="镜像 Pod（Mirror Pod）" term_id="mirror-pod">}}，
以便静态 Pod 在 Kubernetes API 中可见。但是，如果攻击者在创建 Pod 时使用了无效的名字空间名称，
则该 Pod 将在 Kubernetes API 中不可见，只能通过对受影响主机有访问权限的工具发现。

如果静态 Pod 无法通过准入控制，kubelet 不会将 Pod 注册到 API 服务器。但该 Pod 仍然在节点上运行。
有关更多信息，请参阅 [kubeadm issue #1541](https://github.com/kubernetes/kubeadm/issues/1541#issuecomment-487331701)。

### 缓解措施 {#static-pods-mitigations}

- 仅在节点需要时[启用 kubelet 静态 Pod 清单功能](/zh-cn/docs/tasks/configure-pod-container/static-pod/#static-pod-creation)。
- 如果节点使用静态 Pod 功能，请将对静态 Pod 清单目录或 URL 的文件系统的访问权限限制为需要访问的用户。
- 限制对 kubelet 配置参数和文件的访问，以防止攻击者设置静态 Pod 路径或 URL。
- 定期审计并集中报告所有对托管静态 Pod 清单和 kubelet 配置文件的目录或 Web 存储位置的访问。

## kubelet API {#kubelet-api}

kubelet 提供了一个 HTTP API，通常暴露在集群工作节点上的 TCP 端口 10250 上。
在某些 Kubernetes 发行版中，API 也可能暴露在控制平面节点上。
对 API 的直接访问允许公开有关运行在节点上的 Pod、这些 Pod 的日志以及在节点上运行的每个容器中执行命令的信息。

当 Kubernetes 集群用户具有对 `Node` 对象子资源 RBAC 访问权限时，该访问权限可用作与 kubelet API 交互的授权。
实际的访问权限取决于授予了哪些子资源访问权限，详见
[kubelet 鉴权](/zh-cn/docs/reference/access-authn-authz/kubelet-authn-authz/#kubelet-authorization)。

对 kubelet API 的直接访问不受准入控制影响，也不会被 Kubernetes 审计日志记录。
能直接访问此 API 的攻击者可能会绕过能检测或防止某些操作的控制机制。

kubelet API 可以配置为以多种方式验证请求。
默认情况下，kubelet 的配置允许匿名访问。大多数 Kubernetes 提供商将默认值更改为使用 Webhook 和证书身份认证。
这使得控制平面能够确保调用者访问 `Node` API 资源或子资源是经过授权的。但控制平面不能确保默认的匿名访问也是如此。

### 缓解措施 {#mitigations}

- 使用 [RBAC](/zh-cn/docs/reference/access-authn-authz/rbac/) 等机制限制对 `Node` API 对象的子资源的访问。
  只在有需要时才授予此访问权限，例如监控服务。
- 限制对 kubelet 端口的访问。只允许指定和受信任的 IP 地址段访问该端口。
- 确保将
  [kubelet 身份验证](/zh-cn/docs/reference/access-authn-authz/kubelet-authn-authz/#kubelet-authentication)
  设置为 Webhook 或证书模式。
- 确保集群上未启用不作身份认证的“只读” Kubelet 端口。

## etcd API {#the-etcd-api}

Kubernetes 集群使用 etcd 作为数据存储。`etcd` 服务监听 TCP 端口 2379。
只有 Kubernetes API 服务器和你所使用的备份工具需要访问此存储。对该 API 的直接访问允许公开或修改集群中保存的数据。

对 etcd API 的访问通常通过客户端证书身份认证来管理。
由 etcd 信任的证书颁发机构所颁发的任何证书都可以完全访问 etcd 中存储的数据。

对 etcd 的直接访问不受 Kubernetes 准入控制的影响，也不会被 Kubernetes 审计日志记录。
具有对 API 服务器的 etcd 客户端证书私钥的读取访问权限（或可以创建一个新的受信任的客户端证书）
的攻击者可以通过访问集群 Secret 或修改访问规则来获得集群管理员权限。
即使不提升其 Kubernetes RBAC 权限，可以修改 etcd 的攻击者也可以在集群内检索所有 API 对象或创建新的工作负载。

许多 Kubernetes 提供商配置 etcd 为使用双向 TLS（客户端和服务器都验证彼此的证书以进行身份验证）。
尽管存在该特性，但目前还没有被广泛接受的 etcd API 鉴权实现。
由于缺少鉴权模型，任何具有对 etcd 的客户端访问权限的证书都可以用于获得对 etcd 的完全访问权限。
通常，仅用于健康检查的 etcd 客户端证书也可以授予完全读写访问权限。

### 缓解措施 {#etcd-api-mitigations}

- 确保 etcd 所信任的证书颁发机构仅用于该服务的身份认证。
- 控制对 etcd 服务器证书的私钥以及 API 服务器的客户端证书和密钥的访问。
- 考虑在网络层面限制对 etcd 端口的访问，仅允许来自特定和受信任的 IP 地址段的访问。

## 容器运行时套接字 {#runtime-socket}

在 Kubernetes 集群中的每个节点上，与容器交互的访问都由容器运行时控制。
通常，容器运行时会公开一个 kubelet 可以访问的 UNIX 套接字。
具有此套接字访问权限的攻击者可以启动新容器或与正在运行的容器进行交互。

在集群层面，这种访问造成的影响取决于在受威胁节点上运行的容器是否可以访问 Secret 或其他机密数据，
攻击者可以使用这些机密数据将权限提升到其他工作节点或控制平面组件。

### 缓解措施 {#runtime-socket-mitigations}

- 确保严格控制对容器运行时套接字所在的文件系统访问。如果可能，限制为仅 `root` 用户可访问。
- 使用 Linux 内核命名空间等机制将 kubelet 与节点上运行的其他组件隔离。
- 确保限制或禁止使用包含容器运行时套接字的 [`hostPath` 挂载](/zh-cn/docs/concepts/storage/volumes/#hostpath)，
  无论是直接挂载还是通过挂载父目录挂载。此外，`hostPath` 挂载必须设置为只读，以降低攻击者绕过目录限制的风险。
- 限制用户对节点的访问，特别是限制超级用户对节点的访问。
