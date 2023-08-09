---
title: 鉴权概述
content_type: concept
weight: 60
---


了解有关 Kubernetes 鉴权的更多信息，包括使用支持的鉴权模块创建策略的详细信息。


在 Kubernetes 中，你必须在鉴权（授予访问权限）之前进行身份验证（登录），有关身份验证的信息，
请参阅[访问控制概述](/zh-cn/docs/concepts/security/controlling-access/).

Kubernetes 期望请求中存在 REST API 常见的属性。
这意味着 Kubernetes 鉴权适用于现有的组织范围或云提供商范围的访问控制系统，
除了 Kubernetes API 之外，它还可以处理其他 API。

## 确定是允许还是拒绝请求  {#determine-whether-a-request-is-allowed-or-denied}

Kubernetes 使用 API 服务器对 API 请求进行鉴权。
它根据所有策略评估所有请求属性来决定允许或拒绝请求。
一个 API 请求的所有部分都必须被某些策略允许才能继续。
这意味着默认情况下拒绝权限。

（尽管 Kubernetes 使用 API 服务器，但是依赖于特定对象种类的特定字段的访问控制
和策略由准入控制器处理。）

当系统配置了多个鉴权模块时，Kubernetes 将按顺序使用每个模块。
如果任何鉴权模块批准或拒绝请求，则立即返回该决定，并且不会与其他鉴权模块协商。
如果所有模块对请求没有意见，则拒绝该请求。
被拒绝响应返回 HTTP 状态代码 403。

## 审查你的请求属性

Kubernetes 仅审查以下 API 请求属性：

* **用户** —— 身份验证期间提供的 `user` 字符串。
* **组** —— 经过身份验证的用户所属的组名列表。
* **额外信息** —— 由身份验证层提供的任意字符串键到字符串值的映射。
* **API** —— 指示请求是否针对 API 资源。
* **请求路径** —— 各种非资源端点的路径，如 `/api` 或 `/healthz`。
* **API 请求动词** —— API 动词 `get`、`list`、`create`、`update`、`patch`、`watch`、
  `proxy`、`redirect`、`delete` 和 `deletecollection` 用于资源请求。
  要确定资源 API 端点的请求动词，请参阅[确定请求动词](#determine-the-request-verb)。
* **HTTP 请求动词** —— HTTP 动词 `get`、`post`、`put` 和 `delete` 用于非资源请求。
* **资源** —— 正在访问的资源的 ID 或名称（仅限资源请求）- 
  对于使用 `get`、`update`、`patch` 和 `delete` 动词的资源请求，你必须提供资源名称。
* **子资源** —— 正在访问的子资源（仅限资源请求）。
* **名字空间** —— 正在访问的对象的名称空间（仅适用于名字空间资源请求）。
* **API 组** —— 正在访问的 {{< glossary_tooltip text="API 组" term_id="api-group" >}}
  （仅限资源请求）。空字符串表示[核心 API 组](/zh-cn/docs/reference/using-api/#api-groups)。

## 确定请求动词  {#determine-the-request-verb}

**非资源请求**

对于 `/api/v1/...` 或 `/apis/<group>/<version>/...`
之外的端点的请求被视为 “非资源请求（Non-Resource Requests）”，
并使用该请求的 HTTP 方法的小写形式作为其请求动词。

例如，对 `/api` 或 `/healthz` 这类端点的 `GET` 请求将使用 `get` 作为其动词。

**资源请求**

要确定对资源 API 端点的请求动词，需要查看所使用的 HTTP 动词以及该请求是针对单个资源还是一组资源：

HTTP 动词 | 请求动词
----------|---------------
POST      | create
GET, HEAD | get （针对单个资源）、list（针对集合）
PUT       | update
PATCH     | patch
DELETE    | delete（针对单个资源）、deletecollection（针对集合）

{{< caution >}}
`get`、`list` 和 `watch` 动作都可以返回一个资源的完整详细信息。就返回的数据而言，它们是等价的。
例如，对 `secrets` 使用 `list` 仍然会显示所有已返回资源的 `data` 属性。
{{< /caution >}}

Kubernetes 有时使用专门的动词以对额外的权限进行鉴权。例如：

* [RBAC](/zh-cn/docs/reference/access-authn-authz/rbac/#privilege-escalation-prevention-and-bootstrapping)
  * 对 `rbac.authorization.k8s.io` API 组中 `roles` 和 `clusterroles` 资源的 `bind`
    和 `escalate` 动词
* [身份认证](/zh-cn/docs/reference/access-authn-authz/authentication/)
  * 对核心 API 组中 `users`、`groups` 和 `serviceaccounts` 以及 `authentication.k8s.io`
    API 组中的 `userextras` 所使用的 `impersonate` 动词。

## 鉴权模块  {#authorization-modules}

* **Node** —— 一个专用鉴权模式，根据调度到 kubelet 上运行的 Pod 为 kubelet 授予权限。
  要了解有关使用节点鉴权模式的更多信息，请参阅[节点鉴权](/zh-cn/docs/reference/access-authn-authz/node/)。
* **ABAC** —— 基于属性的访问控制（ABAC）定义了一种访问控制范型，通过使用将属性组合在一起的策略，
  将访问权限授予用户。策略可以使用任何类型的属性（用户属性、资源属性、对象，环境属性等）。
  要了解有关使用 ABAC 模式的更多信息，请参阅
  [ABAC 模式](/zh-cn/docs/reference/access-authn-authz/abac/)。
* **RBAC** —— 基于角色的访问控制（RBAC）
  是一种基于企业内个人用户的角色来管理对计算机或网络资源的访问的方法。
  在此上下文中，权限是单个用户执行特定任务的能力，
  例如查看、创建或修改文件。要了解有关使用 RBAC 模式的更多信息，请参阅
  [RBAC 模式](/zh-cn/docs/reference/access-authn-authz/rbac/)。
  * 被启用之后，RBAC（基于角色的访问控制）使用 `rbac.authorization.k8s.io` API
    组来驱动鉴权决策，从而允许管理员通过 Kubernetes API 动态配置权限策略。
  * 要启用 RBAC，请使用 `--authorization-mode = RBAC` 启动 API 服务器。
* **Webhook** —— WebHook 是一个 HTTP 回调：发生某些事情时调用的 HTTP POST；
  通过 HTTP POST 进行简单的事件通知。
  实现 WebHook 的 Web 应用程序会在发生某些事情时将消息发布到 URL。
  要了解有关使用 Webhook 模式的更多信息，请参阅
  [Webhook 模式](/zh-cn/docs/reference/access-authn-authz/webhook/)。

#### 检查 API 访问   {#checking-api-access}

`kubectl` 提供 `auth can-i` 子命令，用于快速查询 API 鉴权。
该命令使用 `SelfSubjectAccessReview` API 来确定当前用户是否可以执行给定操作，
无论使用何种鉴权模式该命令都可以工作。

```shell
kubectl auth can-i create deployments --namespace dev
```

输出类似于：

```
yes
```

```shell
kubectl auth can-i create deployments --namespace prod
```

输出类似于：

```
no
```

管理员可以将此与[用户扮演（User Impersonation）](/zh-cn/docs/reference/access-authn-authz/authentication/#user-impersonation)
结合使用，以确定其他用户可以执行的操作。

```bash
kubectl auth can-i list secrets --namespace dev --as dave
```

输出类似于：

```
no
```

类似地，检查名字空间 `dev` 里的 `dev-sa` 服务账户是否可以列举名字空间 `target` 里的 Pod：

```bash
kubectl auth can-i list pods \
	--namespace target \
	--as system:serviceaccount:dev:dev-sa
```

输出类似于：

```
yes
```

`SelfSubjectAccessReview` 是 `authorization.k8s.io` API 组的一部分，它将 API
服务器鉴权公开给外部服务。该组中的其他资源包括：

* `SubjectAccessReview` - 对任意用户的访问进行评估，而不仅仅是当前用户。
  当鉴权决策被委派给 API 服务器时很有用。例如，kubelet 和扩展 API
  服务器使用它来确定用户对自己的 API 的访问权限。
* `LocalSubjectAccessReview` - 与 `SubjectAccessReview` 类似，但仅限于特定的名字空间。
* `SelfSubjectRulesReview` - 返回用户可在名字空间内执行的操作集的审阅。
  用户可以快速汇总自己的访问权限，或者用于 UI 中的隐藏/显示动作。

可以通过创建普通的 Kubernetes 资源来查询这些 API，其中返回对象的响应 "status"
字段是查询的结果。

```bash
kubectl create -f - -o yaml << EOF
apiVersion: authorization.k8s.io/v1
kind: SelfSubjectAccessReview
spec:
  resourceAttributes:
    group: apps
    name: deployments
    verb: create
    namespace: dev
EOF
```

生成的 `SelfSubjectAccessReview` 为：

```yaml
apiVersion: authorization.k8s.io/v1
kind: SelfSubjectAccessReview
metadata:
  creationTimestamp: null
spec:
  resourceAttributes:
    group: apps
    name: deployments
    namespace: dev
    verb: create
status:
  allowed: true
  denied: false
```

## 为你的鉴权模块设置参数  {#using-flags-for-your-authorization-module}

你必须在策略中包含一个参数标志，以指明你的策略包含哪个鉴权模块：

可以使用的参数有：

* `--authorization-mode=ABAC` 基于属性的访问控制（ABAC）模式允许你使用本地文件配置策略。
* `--authorization-mode=RBAC` 基于角色的访问控制（RBAC）模式允许你使用
  Kubernetes API 创建和存储策略。
* `--authorization-mode=Webhook` WebHook 是一种 HTTP 回调模式，允许你使用远程
  REST 端点管理鉴权。
* `--authorization-mode=Node` 节点鉴权是一种特殊用途的鉴权模式，专门对
  kubelet 发出的 API 请求执行鉴权。
* `--authorization-mode=AlwaysDeny` 该标志阻止所有请求。仅将此标志用于测试。
* `--authorization-mode=AlwaysAllow` 此标志允许所有请求。仅在你不需要 API 请求的鉴权时才使用此标志。

你可以选择多个鉴权模块。模块按顺序检查，以便较靠前的模块具有更高的优先级来允许或拒绝请求。

## 通过创建或编辑工作负载提升权限 {#privilege-escalation-via-pod-creation}

能够在名字空间中创建或者编辑 Pod 的用户，
无论是直接操作还是通过[控制器](/zh-cn/docs/concepts/architecture/controller/)
（例如，一个 Operator）来操作，都可以提升他们在该名字空间内的权限。

{{< caution >}}
系统管理员在授予对工作负载的创建或编辑的权限时要小心。
关于这些权限如何被误用的详细信息请参阅
[提升途径](#escalation-paths)
{{< /caution >}}

### 特权提升途径 {#escalation-paths}

- 挂载该名字空间内的任意 Secret
  - 可以用来访问其他工作负载专用的 Secret
  - 可以用来获取权限更高的服务账号的令牌
- 使用该名字空间内的任意服务账号
  - 可以用另一个工作负载的身份来访问 Kubernetes API（伪装）
  - 可以执行该服务账号的任意特权操作
- 挂载该名字空间里其他工作负载专用的 ConfigMap
  - 可以用来获取其他工作负载专用的信息，例如数据库主机名。
- 挂载该名字空间里其他工作负载的卷
  - 可以用来获取其他工作负载专用的信息，并且更改它。

{{< caution >}}
系统管理员在部署改变以上部分的 CRD 的时候要小心。
它们可能会打开权限提升的途径。
在决定你的 RBAC 控制时应该考虑这方面的问题。
{{< /caution >}}


## {{% heading "whatsnext" %}}

* 要了解有关身份验证的更多信息，
  请参阅[控制对 Kubernetes API 的访问](/zh-cn/docs/concepts/security/controlling-access/)中的
  **身份验证**  部分。
* 要了解有关准入控制的更多信息，请参阅[使用准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/)。

