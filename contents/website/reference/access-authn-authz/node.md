---
title: 使用 Node 鉴权
content_type: concept
weight: 90
---


节点鉴权是一种特殊用途的鉴权模式，专门对 kubelet 发出的 API 请求进行授权。



## 概述   {#overview}

节点鉴权器允许 kubelet 执行 API 操作。包括：

读取操作：

* services
* endpoints
* nodes
* pods
* 与绑定到 kubelet 节点的 Pod 相关的 Secret、ConfigMap、PersistentVolumeClaim 和持久卷

写入操作：

* 节点和节点状态（启用 `NodeRestriction` 准入插件以限制 kubelet 只能修改自己的节点）
* Pod 和 Pod 状态 (启用 `NodeRestriction` 准入插件以限制 kubelet 只能修改绑定到自身的 Pod)
* 事件

身份认证与鉴权相关的操作：

* 对于基于 TLS 的启动引导过程时使用的
  [certificationsigningrequests API](/zh-cn/docs/reference/access-authn-authz/certificate-signing-requests/)
  的读/写权限
* 为委派的身份验证/鉴权检查创建 TokenReview 和 SubjectAccessReview 的能力

在将来的版本中，节点鉴权器可能会添加或删除权限，以确保 kubelet 具有正确操作所需的最小权限集。

为了获得节点鉴权器的授权，kubelet 必须使用一个凭证以表示它在 `system:nodes`
组中，用户名为 `system:node:<nodeName>`。上述的组名和用户名格式要与
[kubelet TLS 启动引导](/zh-cn/docs/reference/access-authn-authz/kubelet-tls-bootstrapping/)
过程中为每个 kubelet 创建的标识相匹配。

`<nodeName>` 的值**必须**与 kubelet 注册的节点名称精确匹配。默认情况下，节点名称是由
`hostname` 提供的主机名，或者通过 kubelet `--hostname-override`
[选项](/zh-cn/docs/reference/command-line-tools-reference/kubelet/) 覆盖。
但是，当使用 `--cloud-provider` kubelet 选项时，具体的主机名可能由云提供商确定，
忽略本地的 `hostname` 和 `--hostname-override` 选项。有关
kubelet 如何确定主机名的详细信息，请参阅
[kubelet 选项参考](/zh-cn/docs/reference/command-line-tools-reference/kubelet/)。

要启用节点鉴权器，请使用 `--authorization-mode=Node` 启动 API 服务器。

要限制 kubelet 可以写入的 API 对象，请使用
`--enable-admission-plugins=...,NodeRestriction,...` 启动 API 服务器，从而启用
[NodeRestriction](/zh-cn/docs/reference/access-authn-authz/admission-controllers#NodeRestriction)
准入插件。

## 迁移考虑因素   {#migration-considerations}

### 在 `system:nodes` 组之外的 kubelet   {#kubelets-outside-the-system-nodes-group}

`system:nodes` 组之外的 kubelet 不会被 `Node` 鉴权模式授权，并且需要继续通过当前授权它们的机制来授权。
节点准入插件不会限制来自这些 kubelet 的请求。

### 具有无差别用户名的 kubelet   {#kubelets-with-undifferentiated-usernames}

在一些部署中，kubelet 具有 `system:nodes` 组的凭证，
但是无法给出它们所关联的节点的标识，因为它们没有 `system:node:...` 格式的用户名。
这些 kubelet 不会被 `Node` 鉴权模式授权，并且需要继续通过当前授权它们的任何机制来授权。

因为默认的节点标识符实现不会把它当作节点身份标识，`NodeRestriction`
准入插件会忽略来自这些 kubelet 的请求。

### 相对于以前使用 RBAC 的版本的更新   {#upgrades-from-previous-versions-using-rbac}

升级的 1.7 之前的使用 [RBAC](/zh-cn/docs/reference/access-authn-authz/rbac/)
的集群将继续按原样运行，因为 `system:nodes` 组绑定已经存在。

如果集群管理员希望开始使用 `Node` 鉴权器和 `NodeRestriction` 准入插件来限制节点对
API 的访问，这一需求可以通过下列操作来完成且不会影响已部署的应用：

1. 启用 `Node` 鉴权模式 (`--authorization-mode=Node,RBAC`) 和 `NodeRestriction` 准入插件
2. 确保所有 kubelet 的凭据符合组/用户名要求
3. 审核 API 服务器日志以确保 `Node` 鉴权器不会拒绝来自 kubelet 的请求（日志中没有持续的 `NODE DENY` 消息）
4. 删除 `system:node` 集群角色绑定

### RBAC 节点权限   {#rbac-node-permissions}

在 1.6 版本中，当使用 [RBAC 鉴权模式](/zh-cn/docs/reference/access-authn-authz/rbac/)
时，`system:nodes` 集群角色会被自动绑定到 `system:node` 组。

在 1.7 版本中，不再推荐将 `system:nodes` 组自动绑定到 `system:node`
角色，因为节点鉴权器通过对 Secret 和 ConfigMap 访问的额外限制完成了相同的任务。
如果同时启用了 `Node` 和 `RBAC` 鉴权模式，1.7 版本则不会创建 `system:nodes`
组到 `system:node` 角色的自动绑定。

在 1.8 版本中，绑定将根本不会被创建。

使用 RBAC 时，将继续创建 `system:node` 集群角色，以便与将其他用户或组绑定到该角色的部署方法兼容。
