---
title: 为 Pod 配置服务账号
content_type: task
weight: 120
---


Kubernetes 提供两种完全不同的方式来为客户端提供支持，这些客户端可能运行在你的集群中，
也可能与你的集群的{{< glossary_tooltip text="控制面" term_id="control-plane" >}}相关，
需要向 {{< glossary_tooltip text="API 服务器" term_id="kube-apiserver" >}}完成身份认证。

**服务账号（Service Account）**为 Pod 中运行的进程提供身份标识，
并映射到 ServiceAccount 对象。当你向 API 服务器执行身份认证时，
你会将自己标识为某个**用户（User）**。Kubernetes 能够识别用户的概念，
但是 Kubernetes 自身**并不**提供 User API。

本服务是关于 ServiceAccount 的，而 ServiceAccount 则确实存在于 Kubernetes 的 API 中。
本指南为你展示为 Pod 配置 ServiceAccount 的一些方法。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}


## 使用默认的服务账号访问 API 服务器   {#use-the-default-service-account-to-access-the-api-server}

当 Pod 与 API 服务器联系时，Pod 会被认证为某个特定的 ServiceAccount（例如：`default`）。
在每个{{< glossary_tooltip text="名字空间" term_id="namespace" >}}中，至少存在一个
ServiceAccount。

每个 Kubernetes 名字空间至少包含一个 ServiceAccount：也就是该名字空间的默认服务账号，
名为 `default`。如果你在创建 Pod 时没有指定 ServiceAccount，Kubernetes 会自动将该名字空间中
名为 `default` 的 ServiceAccount 分配给该 Pod。

你可以检视你刚刚创建的 Pod 的细节。例如：

```shell
kubectl get pods/<podname> -o yaml
```

在输出中，你可以看到字段 `spec.serviceAccountName`。当你在创建 Pod 时未设置该字段时，
Kubernetes [自动](/zh-cn/docs/concepts/overview/working-with-objects/object-management/)为
Pod 设置这一属性的取值。

Pod 中运行的应用可以使用这一自动挂载的服务账号凭据来访问 Kubernetes API。
参阅[访问集群](/zh-cn/docs/tasks/access-application-cluster/access-cluster/)以进一步了解。

当 Pod 被身份认证为某个 ServiceAccount 时，
其访问能力取决于所使用的[鉴权插件和策略](/zh-cn/docs/reference/access-authn-authz/authorization/#authorization-modules)。

### 放弃 API 凭据的自动挂载   {#opt-out-of-api-credential-automounting}

如果你不希望 {{< glossary_tooltip text="kubelet" term_id="kubelet" >}} 自动挂载某
ServiceAccount 的 API 访问凭据，你可以选择不采用这一默认行为。
通过在 ServiceAccount 对象上设置 `automountServiceAccountToken: false`，可以放弃在
`/var/run/secrets/kubernetes.io/serviceaccount/token` 处自动挂载该服务账号的 API 凭据。

例如：

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: build-robot
automountServiceAccountToken: false
...
```
你也可以选择不给特定 Pod 自动挂载 API 凭据：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  serviceAccountName: build-robot
  automountServiceAccountToken: false
  ...
```

如果 ServiceAccount 和 Pod 的 `.spec` 都设置了 `automountServiceAccountToken` 值，
则 Pod 上 spec 的设置优先于服务账号的设置。

## 使用多个服务账号   {#use-multiple-service-accounts}

每个名字空间都至少有一个 ServiceAccount：名为 `default` 的默认 ServiceAccount 资源。
你可以用下面的命令列举你[当前名字空间](/zh-cn/docs/concepts/overview/working-with-objects/namespaces/#setting-the-namespace-preference)
中的所有 ServiceAccount 资源：

```shell
kubectl get serviceaccounts
```

输出类似于：

```
NAME      SECRETS    AGE
default   1          1d
```

你可以像这样来创建额外的 ServiceAccount 对象：

```shell
kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: build-robot
EOF
```

ServiceAccount 对象的名字必须是一个有效的
[DNS 子域名](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

如果你查询服务账号对象的完整信息，如下所示：

```shell
kubectl get serviceaccounts/build-robot -o yaml
```

输出类似于：

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: 2019-06-16T00:12:34Z
  name: build-robot
  namespace: default
  resourceVersion: "272500"
  uid: 721ab723-13bc-11e5-aec2-42010af0021e
```

你可以使用鉴权插件来[设置服务账号的访问许可](/zh-cn/docs/reference/access-authn-authz/rbac/#service-account-permissions)。

要使用非默认的服务账号，将 Pod 的 `spec.serviceAccountName` 字段设置为你想用的服务账号名称。

只能在创建 Pod 时或者为新 Pod 指定模板时，你才可以设置 `serviceAccountName`。
你不能更新已经存在的 Pod 的 `.spec.serviceAccountName` 字段。

{{< note >}}
`.spec.serviceAccount` 字段是 `.spec.serviceAccountName` 的已弃用别名。
如果要从工作负载资源中删除这些字段，请在
[Pod 模板](/zh-cn/docs/concepts/workloads/pods#pod-templates)上将这两个字段显式设置为空。
{{< /note >}}

### 清理  {#cleanup-use-multiple-service-accounts}

如果你尝试了创建前文示例中所给的 `build-robot` ServiceAccount，
你可以通过运行下面的命令来完成清理操作：

```shell
kubectl delete serviceaccount/build-robot
```

## 手动为 ServiceAccount 创建 API 令牌 {#manually-create-an-api-token-for-a-serviceaccount}

假设你已经有了一个前文所提到的名为 "build-robot" 的服务账号。
你可以使用 `kubectl` 为该 ServiceAccount 获得一个时间上受限的 API 令牌：

```shell
kubectl create token build-robot
```

这一命令的输出是一个令牌，你可以使用该令牌来将身份认证为对应的 ServiceAccount。
你可以使用 `kubectl create token` 命令的 `--duration` 参数来请求特定的令牌有效期
（实际签发的令牌的有效期可能会稍短一些，也可能会稍长一些）。

{{< note >}}
Kubernetes 在 v1.22 版本之前自动创建用来访问 Kubernetes API 的长期凭据。
这一较老的机制是基于创建令牌 Secret 对象来实现的，Secret 对象可被挂载到运行中的 Pod 内。
在最近的版本中，包括 Kubernetes v{{< skew currentVersion >}}，API 凭据可以直接使用
[TokenRequest](/zh-cn/docs/reference/kubernetes-api/authentication-resources/token-request-v1/) API
来获得，并使用一个[投射卷](/zh-cn/docs/reference/access-authn-authz/service-accounts-admin/#bound-service-account-token-volume)挂载到
Pod 中。使用此方法获得的令牌具有受限的生命期长度，并且能够在挂载它们的 Pod
被删除时自动被废弃。

你仍然可以通过手动方式来创建服务账号令牌 Secret 对象，例如你需要一个永远不过期的令牌时。
不过，使用 [TokenRequest](/zh-cn/docs/reference/kubernetes-api/authentication-resources/token-request-v1/)
子资源来获得访问 API 的令牌的做法仍然是推荐的方式。
{{< /note >}}

### 手动为 ServiceAccount 创建长期有效的 API 令牌 {#manually-create-a-long-lived-api-token-for-a-serviceaccount}

如果你需要为 ServiceAccount 获得一个 API 令牌，你可以创建一个新的、带有特殊注解
`kubernetes.io/service-account.name` 的 Secret 对象。

```shell
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: build-robot-secret
  annotations:
    kubernetes.io/service-account.name: build-robot
type: kubernetes.io/service-account-token
EOF
```

如果你通过下面的命令来查看 Secret：

```shell
kubectl get secret/build-robot-secret -o yaml
```

你可以看到 Secret 中现在包含针对 "build-robot" ServiceAccount 的 API 令牌。

鉴于你所设置的注解，控制面会自动为该 ServiceAccount 生成一个令牌，并将其保存到相关的 Secret
中。控制面也会为已删除的 ServiceAccount 执行令牌清理操作。

```shell
kubectl describe secrets/build-robot-secret
```

输出类似于这样：

```
Name:           build-robot-secret
Namespace:      default
Labels:         <none>
Annotations:    kubernetes.io/service-account.name: build-robot
                kubernetes.io/service-account.uid: da68f9c6-9d26-11e7-b84e-002dc52800da

Type:   kubernetes.io/service-account-token

Data
====
ca.crt:         1338 bytes
namespace:      7 bytes
token:          ...
```

{{< note >}}
这里将 `token` 的内容抹去了。

注意在你的终端或者计算机屏幕可能被旁观者看到的场合，不要显示
`kubernetes.io/service-account-token` 的内容。
{{< /note >}}

当你删除一个与某 Secret 相关联的 ServiceAccount 时，Kubernetes 的控制面会自动清理该
Secret 中长期有效的令牌。

## 为服务账号添加 ImagePullSecrets    {#add-imagepullsecrets-to-a-service-account}

首先，[生成一个 imagePullSecret](/zh-cn/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod)；
接下来，验证该 Secret 已被创建。例如：

- 按[为 Pod 设置 imagePullSecret](/zh-cn/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod)
  所描述的，生成一个镜像拉取 Secret：

  ```shell
  kubectl create secret docker-registry myregistrykey --docker-server=DUMMY_SERVER \
          --docker-username=DUMMY_USERNAME --docker-password=DUMMY_DOCKER_PASSWORD \
          --docker-email=DUMMY_DOCKER_EMAIL
  ```

- 检查该 Secret 已经被创建。

  ```shell
  kubectl get secrets myregistrykey
  ```

  输出类似于这样：

  ```
  NAME             TYPE                              DATA    AGE
  myregistrykey    kubernetes.io/.dockerconfigjson   1       1d
  ```

### 将镜像拉取 Secret 添加到服务账号   {#add-image-pull-secret-to-service-account}

接下来更改名字空间的默认服务账号，将该 Secret 用作 imagePullSecret。

```shell
kubectl patch serviceaccount default -p '{"imagePullSecrets": [{"name": "myregistrykey"}]}'
```

你也可以通过手动编辑该对象来实现同样的效果：

```shell
kubectl edit serviceaccount/default
```

`sa.yaml` 文件的输出类似于：

你所选择的文本编辑器会被打开，展示如下所示的配置：

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: 2021-07-07T22:02:39Z
  name: default
  namespace: default
  resourceVersion: "243024"
  uid: 052fb0f4-3d50-11e5-b066-42010af0d7b6
```

使用你的编辑器，删掉包含 `resourceVersion` 主键的行，添加包含 `imagePullSecrets:`
的行并保存文件。对于 `uid` 而言，保持其取值与你读到的值一样。

当你完成这些变更之后，所编辑的 ServiceAccount 看起来像是这样：

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: 2021-07-07T22:02:39Z
  name: default
  namespace: default
  uid: 052fb0f4-3d50-11e5-b066-42010af0d7b6
imagePullSecrets:
  - name: myregistrykey
```

### 检查 imagePullSecrets 已经被设置到新 Pod 上  {#verify-that-imagepullsecrets-are-set-for-new-pods}

现在，在当前名字空间中创建新 Pod 并使用默认 ServiceAccount 时，
新 Pod 的 `spec.imagePullSecrets` 会被自动设置。

```shell
kubectl run nginx --image=nginx --restart=Never
kubectl get pod nginx -o=jsonpath='{.spec.imagePullSecrets[0].name}{"\n"}'
```

输出为：

```
myregistrykey
```

## 服务账号令牌卷投射   {#service-account-token-volume-projection}

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

{{< note >}}
为了启用令牌请求投射，你必须为 `kube-apiserver` 设置以下命令行参数：

`--service-account-issuer`
: 定义服务账号令牌发放者的身份标识（Identifier）。你可以多次指定
  `--service-account-issuer` 参数，对于需要变更发放者而又不想带来业务中断的场景，
  这样做是有用的。如果这个参数被多次指定，其第一个参数值会被用来生成令牌，
  而所有参数值都会被用来确定哪些发放者是可接受的。你所运行的 Kubernetes
  集群必须是 v1.22 或更高版本才能多次指定 `--service-account-issuer`。

`--service-account-key-file`
: 给出某文件的路径，其中包含 PEM 编码的 x509 RSA 或 ECDSA 私钥或公钥，用来检查 ServiceAccount
  的令牌。所指定的文件中可以包含多个秘钥，并且你可以多次使用此参数，每个参数值为不同的文件。
  多次使用此参数时，由所给的秘钥之一签名的令牌会被 Kubernetes API 服务器认为是合法令牌。

`--service-account-signing-key-file`
: 指向某文件的路径，其中包含当前服务账号令牌发放者的私钥。
  此发放者使用此私钥来签署所发放的 ID 令牌。

`--api-audiences` (可以省略)
: 为 ServiceAccount 令牌定义其受众（Audiences）。
  服务账号令牌身份检查组件会检查针对 API 访问所使用的令牌，
  确认令牌至少是被绑定到这里所给的受众之一。
  如果 `api-audiences` 被多次指定，则针对所给的多个受众中任何目标的令牌都会被
  Kubernetes API 服务器当做合法的令牌。如果你指定了 `--service-account-issuer`
  参数，但沒有設置 `--api-audiences`，则控制面认为此参数的默认值为一个只有一个元素的列表，
  且该元素为令牌发放者的 URL。

{{< /note >}}

kubelet 还可以将 ServiceAccount 令牌投射到 Pod 中。你可以指定令牌的期望属性，
例如受众和有效期限。这些属性在 default ServiceAccount 令牌上**无法**配置。
当 Pod 或 ServiceAccount 被删除时，该令牌也将对 API 无效。

你可以使用类型为 `ServiceAccountToken` 的[投射卷](/zh-cn/docs/concepts/storage/volumes/#projected)
来为 Pod 的 `spec` 配置此行为。

### 启动使用服务账号令牌投射的 Pod  {#launch-a-pod-using-service-account-token-projection}

要为某 Pod 提供一个受众为 `vault` 并且有效期限为 2 小时的令牌，你可以定义一个与下面类似的
Pod 清单：

{{< codenew file="pods/pod-projected-svc-token.yaml" >}}

创建此 Pod：

```shell
kubectl create -f https://k8s.io/examples/pods/pod-projected-svc-token.yaml
```

kubelet 组件会替 Pod 请求令牌并将其保存起来；通过将令牌存储到一个可配置的路径以使之在
Pod 内可用；在令牌快要到期的时候刷新它。kubelet 会在令牌存在期达到其 TTL 的 80%
的时候或者令牌生命期超过 24 小时的时候主动请求将其轮换掉。

应用负责在令牌被轮换时重新加载其内容。通常而言，周期性地（例如，每隔 5 分钟）
重新加载就足够了，不必跟踪令牌的实际过期时间。

## 发现服务账号分发者

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

如果你在你的集群中已经为 ServiceAccount 启用了[令牌投射](#serviceaccount-token-volume-projection)，
那么你也可以利用其发现能力。Kubernetes 提供一种方式来让客户端将一个或多个外部系统进行联邦，
作为**标识提供者（Identity Provider）**，而这些外部系统的角色是**依赖方（Relying Party）**。

{{< note >}}
分发者的 URL 必须遵从
[OIDC 发现规范](https://openid.net/specs/openid-connect-discovery-1_0.html)。
实现上，这意味着 URL 必须使用 `https` 模式，并且必须在路径
`{service-account-issuer}/.well-known/openid-configuration`
处给出 OpenID 提供者（Provider）的配置信息。

如果 URL 没有遵从这一规范，ServiceAccount 分发者发现末端末端就不会被注册也无法访问。
{{< /note >}}

当此特性被启用时，Kubernetes API 服务器会通过 HTTP 发布一个 OpenID 提供者配置文档。
该配置文档发布在 `/.well-known/openid-configuration` 路径。
这里的 OpenID 提供者配置（OpenID Provider Configuration）有时候也被称作
“发现文档（Discovery Document）”。
Kubernetes API 服务器也通过 HTTP 在 `/openid/v1/jwks` 处发布相关的
JSON Web Key Set（JWKS）。

{{< note >}}
对于在 `/.well-known/openid-configuration` 和 `/openid/v1/jwks` 上给出的响应而言，
其设计上是保证与 OIDC 兼容的，但并不严格遵从 OIDC 的规范。
响应中所包含的文档进包含对 Kubernetes 服务账号令牌进行校验所必需的参数。
{{< /note >}}

使用 {{< glossary_tooltip text="RBAC" term_id="rbac">}} 的集群都包含一个的默认
RBAC ClusterRole, 名为 `system:service-account-issuer-discovery`。
默认的 RBAC ClusterRoleBinding 将此角色分配给 `system:serviceaccounts` 组，
所有 ServiceAccount 隐式属于该组。这使得集群上运行的 Pod
能够通过它们所挂载的服务账号令牌访问服务账号发现文档。
此外，管理员可以根据其安全性需要以及期望集成的外部系统，选择是否将该角色绑定到
`system:authenticated` 或 `system:unauthenticated`。

JWKS 响应包含依赖方可以用来验证 Kubernetes 服务账号令牌的公钥数据。
依赖方先会查询 OpenID 提供者配置，之后使用返回响应中的 `jwks_uri` 来查找 JWKS。

在很多场合，Kubernetes API 服务器都不会暴露在公网上，不过对于缓存并向外提供 API
服务器响应数据的公开末端而言，用户或者服务提供商可以选择将其暴露在公网上。
在这种环境中，可能会重载 OpenID 提供者配置中的
`jwks_uri`，使之指向公网上可用的末端地址，而不是 API 服务器的地址。
这时需要向 API 服务器传递 `--service-account-jwks-uri` 参数。
与分发者 URL 类似，此 JWKS URI 也需要使用 `https` 模式。

## {{% heading "whatsnext" %}}

另请参见：

- 阅读[为集群管理员提供的服务账号指南](/zh-cn/docs/reference/access-authn-authz/service-accounts-admin/)
- 阅读 [Kubernetes中的鉴权](/zh-cn/docs/reference/access-authn-authz/authorization/)
- 阅读 [Secret](/zh-cn/docs/concepts/configuration/secret/) 的概念
  - 或者学习[使用 Secret 来安全地分发凭据](/zh-cn/docs/tasks/inject-data-application/distribute-credentials-secure/)
  - 不过也要注意，使用 Secret 来完成 ServiceAccount 身份验证的做法已经过时。
    建议的替代做法是执行 [ServiceAccount 令牌卷投射](#service-account-token-volume-projection).
- 阅读理解[投射卷](/zh-cn/docs/tasks/configure-pod-container/configure-projected-volume-storage/)
- 关于 OIDC 发现的相关背景信息，阅读[服务账号签署密钥检索 KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-auth/1393-oidc-discovery)
  这一 Kubernetes 增强提案
- 阅读 [OIDC 发现规范](https://openid.net/specs/openid-connect-discovery-1_0.html)
