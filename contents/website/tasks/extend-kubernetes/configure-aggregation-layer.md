---
title: 配置聚合层
content_type: task
weight: 10
---


配置[聚合层](/zh-cn/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)可以允许
Kubernetes apiserver 使用其它 API 扩展，这些 API 不是核心 Kubernetes API 的一部分。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

{{< note >}}
要使聚合层在你的环境中正常工作以支持代理服务器和扩展 apiserver 之间的相互 TLS 身份验证，
需要满足一些设置要求。Kubernetes 和 kube-apiserver 具有多个 CA，
因此请确保代理是由聚合层 CA 签名的，而不是由 Kubernetes 通用 CA 签名的。
{{< /note >}}

{{< caution >}}
对不同的客户端类型重复使用相同的 CA 会对集群的功能产生负面影响。
有关更多信息，请参见 [CA 重用和冲突](#ca-reusage-and-conflicts)。
{{< /caution >}}


## 身份认证流程   {#authentication-flow}

与自定义资源定义（CRD）不同，除标准的 Kubernetes apiserver 外，Aggregation API
还涉及另一个服务器：扩展 apiserver。
Kubernetes apiserver 将需要与你的扩展 apiserver 通信，并且你的扩展 apiserver
也需要与 Kubernetes apiserver 通信。
为了确保此通信的安全，Kubernetes apiserver 使用 x509 证书向扩展 apiserver 认证。

本节介绍身份认证和鉴权流程的工作方式以及如何配置它们。

大致流程如下：

1. Kubernetes apiserver：对发出请求的用户身份认证，并对请求的 API 路径执行鉴权。
2. Kubernetes apiserver：将请求转发到扩展 apiserver
3. 扩展 apiserver：认证来自 Kubernetes apiserver 的请求
4. 扩展 apiserver：对来自原始用户的请求鉴权
5. 扩展 apiserver：执行

本节的其余部分详细描述了这些步骤。

该流程可以在下图中看到。

![聚合层认证流程](/images/docs/aggregation-api-auth-flow.png)

以上泳道的来源可以在本文档的源码中找到。



### Kubernetes Apiserver 认证和授权   {#kubernetes-apiserver-authentication-and-authorization}

由扩展 apiserver 服务的对 API 路径的请求以与所有 API 请求相同的方式开始：
与 Kubernetes apiserver 的通信。该路径已通过扩展 apiserver 在
Kubernetes apiserver 中注册。

用户与 Kubernetes apiserver 通信，请求访问路径。
Kubernetes apiserver 使用它的标准认证和授权配置来对用户认证，以及对特定路径的鉴权。

有关对 Kubernetes 集群认证的概述，
请参见[对集群认证](/zh-cn/docs/reference/access-authn-authz/authentication/)。
有关对 Kubernetes 集群资源的访问鉴权的概述，
请参见[鉴权概述](/zh-cn/docs/reference/access-authn-authz/authorization/)。

到目前为止，所有内容都是标准的 Kubernetes API 请求，认证与鉴权。

Kubernetes apiserver 现在准备将请求发送到扩展 apiserver。

### Kubernetes Apiserver 代理请求   {#kubernetes-apiserver-proxies-the-request}

Kubernetes apiserver 现在将请求发送或代理到注册以处理该请求的扩展 apiserver。
为此，它需要了解几件事：

1. Kubernetes apiserver 应该如何向扩展 apiserver 认证，以通知扩展
   apiserver 通过网络发出的请求来自有效的 Kubernetes apiserver？

2. Kubernetes apiserver 应该如何通知扩展 apiserver
   原始请求已通过认证的用户名和组？

为提供这两条信息，你必须使用若干标志来配置 Kubernetes apiserver。

#### Kubernetes Apiserver 客户端认证

Kubernetes apiserver 通过 TLS 连接到扩展 apiserver，并使用客户端证书认证。
你必须在启动时使用提供的标志向 Kubernetes apiserver 提供以下内容：

* 通过 `--proxy-client-key-file` 指定私钥文件
* 通过 `--proxy-client-cert-file` 签名的客户端证书文件
* 通过 `--requestheader-client-ca-file` 签署客户端证书文件的 CA 证书
* 通过 `--requestheader-allowed-names` 在签署的客户端证书中有效的公用名（CN）

Kubernetes apiserver 将使用由 `--proxy-client-*-file` 指示的文件来向扩展 apiserver认证。
为了使合规的扩展 apiserver 能够将该请求视为有效，必须满足以下条件：

1. 连接必须使用由 CA 签署的客户端证书，该证书的证书位于 `--requestheader-client-ca-file` 中。
2. 连接必须使用客户端证书，该客户端证书的 CN 是 `--requestheader-allowed-names` 中列出的证书之一。

{{< note >}}
你可以将此选项设置为空白，即为`--requestheader-allowed-names=""`。
这将向扩展 apiserver 指示**任何** CN 都是可接受的。
{{< /note >}}

使用这些选项启动时，Kubernetes apiserver 将：

1. 使用它们向扩展 apiserver 认证。
2. 在 `kube-system` 命名空间中创建一个名为
   `extension-apiserver-authentication` 的 ConfigMap，
   它将在其中放置 CA 证书和允许的 CN。
   反过来，扩展 apiserver 可以检索这些内容以验证请求。

请注意，Kubernetes apiserver 使用相同的客户端证书对所有扩展 apiserver 认证。
它不会为每个扩展 apiserver 创建一个客户端证书，而是创建一个证书作为
Kubernetes apiserver 认证。所有扩展 apiserver 请求都重复使用相同的请求。

#### 原始请求用户名和组

当 Kubernetes apiserver 将请求代理到扩展 apiserver 时，
它将向扩展 apiserver 通知原始请求已成功通过其验证的用户名和组。
它在其代理请求的 HTTP 头部中提供这些。你必须将要使用的标头名称告知
Kubernetes apiserver。

* 通过 `--requestheader-username-headers` 标明用来保存用户名的头部
* 通过 `--requestheader-group-headers` 标明用来保存 group 的头部
* 通过 `--requestheader-extra-headers-prefix` 标明用来保存拓展信息前缀的头部

这些头部名称也放置在 `extension-apiserver-authentication` ConfigMap 中，
因此扩展 apiserver 可以检索和使用它们。

### 扩展 Apiserver 认证请求    {#extension-apiserver-authenticates-the-request}

扩展 apiserver 在收到来自 Kubernetes apiserver 的代理请求后，
必须验证该请求确实确实来自有效的身份验证代理，
该认证代理由 Kubernetes apiserver 履行。扩展 apiserver 通过以下方式对其认证：

1. 如上所述，从 `kube-system` 中的 ConfigMap 中检索以下内容：

   * 客户端 CA 证书
   * 允许名称（CN）列表
   * 用户名，组和其他信息的头部

2. 使用以下证书检查 TLS 连接是否已通过认证：

   * 由其证书与检索到的 CA 证书匹配的 CA 签名。
   * 在允许的 CN 列表中有一个 CN，除非列表为空，在这种情况下允许所有 CN。
   * 从适当的头部中提取用户名和组。

如果以上均通过，则该请求是来自合法认证代理（在本例中为 Kubernetes apiserver）
的有效代理请求。

请注意，扩展 apiserver 实现负责提供上述内容。
默认情况下，许多扩展 apiserver 实现利用 `k8s.io/apiserver/` 软件包来做到这一点。
也有一些实现可能支持使用命令行选项来覆盖这些配置。

为了具有检索 configmap 的权限，扩展 apiserver 需要适当的角色。
在 `kube-system` 名字空间中有一个默认角色
`extension-apiserver-authentication-reader` 可用于设置。

### 扩展 Apiserver 对请求鉴权   {#extensions-apiserver-authorizes-the-request}

扩展 apiserver 现在可以验证从标头检索的`user/group`是否有权执行给定请求。
通过向 Kubernetes apiserver 发送标准
[SubjectAccessReview](/zh-cn/docs/reference/access-authn-authz/authorization/) 请求来实现。

为了使扩展 apiserver 本身被鉴权可以向 Kubernetes apiserver 提交 SubjectAccessReview 请求，
它需要正确的权限。
Kubernetes 包含一个具有相应权限的名为 `system:auth-delegator` 的默认 `ClusterRole`，
可以将其授予扩展 apiserver 的服务帐户。

### 扩展 Apiserver 执行   {#enable-kubernetes-apiserver-flags}

如果 `SubjectAccessReview` 通过，则扩展 apiserver 执行请求。

## 启用 Kubernetes Apiserver 标志

通过以下 `kube-apiserver` 标志启用聚合层。
你的服务提供商可能已经为你完成了这些工作：

```
    --requestheader-client-ca-file=<path to aggregator CA cert>
    --requestheader-allowed-names=front-proxy-client
    --requestheader-extra-headers-prefix=X-Remote-Extra-
    --requestheader-group-headers=X-Remote-Group
    --requestheader-username-headers=X-Remote-User
    --proxy-client-cert-file=<path to aggregator proxy cert>
    --proxy-client-key-file=<path to aggregator proxy key>
```

### CA 重用和冲突  {#ca-reusage-and-conflicts}

Kubernetes apiserver 有两个客户端 CA 选项：

* `--client-ca-file`
* `--requestheader-client-ca-file`

这些功能中的每个功能都是独立的；如果使用不正确，可能彼此冲突。

* `--client-ca-file`：当请求到达 Kubernetes apiserver 时，如果启用了此选项，
  则 Kubernetes apiserver 会检查请求的证书。
  如果它是由 `--client-ca-file` 引用的文件中的 CA 证书之一签名的，
  并且用户是公用名 `CN=` 的值，而组是组织 `O=` 的取值，则该请求被视为合法请求。
  请参阅[关于 TLS 身份验证的文档](/zh-cn/docs/reference/access-authn-authz/authentication/#x509-client-certs)。

* `--requestheader-client-ca-file`：当请求到达 Kubernetes apiserver 时，
  如果启用此选项，则 Kubernetes apiserver 会检查请求的证书。
  如果它是由文件引用中的 --requestheader-client-ca-file 所签署的 CA 证书之一签名的，
  则该请求将被视为潜在的合法请求。
  然后，Kubernetes apiserver 检查通用名称 `CN=` 是否是
  `--requestheader-allowed-names` 提供的列表中的名称之一。
  如果名称允许，则请求被批准；如果不是，则请求被拒绝。

如果同时提供了 `--client-ca-file` 和 `--requestheader-client-ca-file`，
则首先检查 `--requestheader-client-ca-file` CA，然后再检查 `--client-ca-file`。
通常，这些选项中的每一个都使用不同的 CA（根 CA 或中间 CA）。
常规客户端请求与 `--client-ca-file` 相匹配，而聚合请求要与
`--requestheader-client-ca-file` 相匹配。
但是，如果两者都使用同一个 CA，则通常会通过 `--client-ca-file`
传递的客户端请求将失败，因为 CA 将与 `--requestheader-client-ca-file`
中的 CA 匹配，但是通用名称 `CN=` 将不匹配 `--requestheader-allowed-names`
中可接受的通用名称之一。
这可能导致你的 kubelet 和其他控制平面组件以及最终用户无法向 Kubernetes
apiserver 认证。

因此，请对用于控制平面组件和最终用户鉴权的 `--client-ca-file` 选项和
用于聚合 apiserver 鉴权的 `--requestheader-client-ca-file` 选项使用
不同的 CA 证书。

{{< warning >}}
除非你了解风险和保护 CA 用法的机制，否则 **不要** 重用在不同上下文中使用的 CA。
{{< /warning >}}

如果你未在运行 API 服务器的主机上运行 kube-proxy，则必须确保使用以下
`kube-apiserver` 标志启用系统：

```
--enable-aggregator-routing=true
```

### 注册 APIService 对象   {#register-apiservice-objects}

你可以动态配置将哪些客户端请求代理到扩展 apiserver。以下是注册示例：

```yaml
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata:
  name: <注释对象名称>
spec:
  group: <扩展 Apiserver 的 API 组名>
  version: <扩展 Apiserver 的 API 版本>
  groupPriorityMinimum: <APIService 对应组的优先级, 参考 API 文档>
  versionPriority: <版本在组中的优先排序, 参考 API 文档>
  service:
    namespace: <拓展 Apiserver 服务的名字空间>
    name: <拓展 Apiserver 服务的名称>
  caBundle: <PEM 编码的 CA 证书，用于对 Webhook 服务器的证书签名>
```

APIService
对象的名称必须是合法的[路径片段名称](/zh-cn/docs/concepts/overview/working-with-objects/names#path-segment-names)。

#### 调用扩展 apiserver

一旦 Kubernetes apiserver 确定应将请求发送到扩展 apiserver，
它需要知道如何调用它。

`service` 部分是对扩展 apiserver 的服务的引用。
服务的名字空间和名字是必需的。端口是可选的，默认为 443。

下面是一个扩展 apiserver 的配置示例，它被配置为在端口 `1234` 上调用。
并针对 ServerName `my-service-name.my-service-namespace.svc`
使用自定义的 CA 包来验证 TLS 连接使用自定义 CA 捆绑包的
`my-service-name.my-service-namespace.svc`。

```yaml
apiVersion: apiregistration.k8s.io/v1
kind: APIService
...
spec:
  ...
  service:
    namespace: my-service-namespace
    name: my-service-name
    port: 1234
  caBundle: "Ci0tLS0tQk...<base64-encoded PEM bundle>...tLS0K"
...
```

## {{% heading "whatsnext" %}}


* 使用聚合层[安装扩展 API 服务器](/zh-cn/docs/tasks/extend-kubernetes/setup-extension-api-server/)。
* 有关高级概述，请参阅[使用聚合层扩展 Kubernetes API](/zh-cn/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)。
* 了解如何[使用自定义资源扩展 Kubernetes API](/zh-cn/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)。
