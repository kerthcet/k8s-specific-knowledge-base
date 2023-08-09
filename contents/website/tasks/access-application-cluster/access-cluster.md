---
title: 访问集群
weight: 20
content_type: concept
---



本文阐述多种与集群交互的方法。

{{< toc >}}


## 使用 kubectl 完成集群的第一次访问 {#accessing-for-the-first-time-with-kubectl}

当你第一次访问 Kubernetes API 的时候，我们建议你使用 Kubernetes CLI 工具 `kubectl`。

访问集群时，你需要知道集群的地址并且拥有访问的凭证。通常，这些在你通过
[启动安装](/zh-cn/docs/setup/)安装集群时都是自动安装好的，或者其他人安装时
也应该提供了凭证和集群地址。

通过以下命令检查 kubectl 是否知道集群地址及凭证：

```shell
kubectl config view
```

有许多[例子](/zh-cn/docs/reference/kubectl/cheatsheet/)介绍了如何使用 kubectl，
可以在 [kubectl 参考](/zh-cn/docs/reference/kubectl/)中找到更完整的文档。

## 直接访问 REST API {#directly-accessing-the-rest-api}

Kubectl 处理 apiserver 的定位和身份验证。
如果要使用 curl 或 wget 等 http 客户端或浏览器直接访问 REST API，可以通过
多种方式查找和验证：

- 以代理模式运行 kubectl。
  - 推荐此方式。
  - 使用已存储的 apiserver 地址。
  - 使用自签名的证书来验证 apiserver 的身份。杜绝 MITM 攻击。
  - 对 apiserver 进行身份验证。
  - 未来可能会实现智能化的客户端负载均衡和故障恢复。
- 直接向 http 客户端提供位置和凭据。
  - 可选的方案。
  - 适用于代理可能引起混淆的某些客户端类型。
  - 需要引入根证书到你的浏览器以防止 MITM 攻击。

### 使用 kubectl proxy {#using-kubectl-proxy}

以下命令以反向代理的模式运行 kubectl。它处理 apiserver 的定位和验证。
像这样运行：

```shell
kubectl proxy --port=8080
```

参阅 [kubectl proxy](/docs/reference/generated/kubectl/kubectl-commands/#proxy)
获取更多详细信息。

然后，你可以使用 curl、wget 或浏览器访问 API，如果是 IPv6 则用 [::1] 替换 localhost，
如下所示：

```shell
curl http://localhost:8080/api/
```

输出类似于：

```json
{
  "kind": "APIVersions",
  "versions": [
    "v1"
  ],
  "serverAddressByClientCIDRs": [
    {
      "clientCIDR": "0.0.0.0/0",
      "serverAddress": "10.0.1.149:443"
    }
  ]
}
```


### 不使用 kubectl proxy {#without-kubectl-proxy}

使用 `kubectl apply` 和 `kubectl describe secret ...` 及 grep 和剪切操作来为 default 服务帐户创建令牌，如下所示：

首先，创建 Secret，请求默认 ServiceAccount 的令牌：

```shell
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: default-token
  annotations:
    kubernetes.io/service-account.name: default
type: kubernetes.io/service-account-token
EOF
```

接下来，等待令牌控制器使用令牌填充 Secret：

```shell
while ! kubectl describe secret default-token | grep -E '^token' >/dev/null; do
  echo "waiting for token..." >&2
  sleep 1
done
```

捕获并使用生成的令牌：

```shell
APISERVER=$(kubectl config view --minify | grep server | cut -f 2- -d ":" | tr -d " ")
TOKEN=$(kubectl describe secret default-token | grep -E '^token' | cut -f2 -d':' | tr -d " ")
curl $APISERVER/api --header "Authorization: Bearer $TOKEN" --insecure
```

输出类似于：

```json
{
  "kind": "APIVersions",
  "versions": [
    "v1"
  ],
  "serverAddressByClientCIDRs": [
    {
      "clientCIDR": "0.0.0.0/0",
      "serverAddress": "10.0.1.149:443"
    }
  ]
}
```

`jsonpath` 方法实现：

```shell
APISERVER=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')
TOKEN=$(kubectl get secret default-token -o jsonpath='{.data.token}' | base64 --decode)
curl $APISERVER/api --header "Authorization: Bearer $TOKEN" --insecure
```

输出类似于：

```json
{
  "kind": "APIVersions",
  "versions": [
    "v1"
  ],
  "serverAddressByClientCIDRs": [
    {
      "clientCIDR": "0.0.0.0/0",
      "serverAddress": "10.0.1.149:443"
    }
  ]
}
```

上面的例子使用了 `--insecure` 参数，这使得它很容易受到 MITM 攻击。
当 kubectl 访问集群时，它使用存储的根证书和客户端证书来访问服务器
（它们安装在 `~/.kube` 目录中）。
由于集群证书通常是自签名的，因此可能需要特殊配置才能让你的 http 客户端使用根证书。

在一些集群中，apiserver 不需要身份验证；它可能只服务于 localhost，或者被防火墙保护，
这个没有一定的标准。
[配置对 API 的访问](/zh-cn/docs/concepts/security/controlling-access/)
描述了集群管理员如何进行配置。此类方法可能与未来的高可用性支持相冲突。

## 以编程方式访问 API {#programmatic-access-to-the-api}

Kubernetes 官方提供对 [Go](#go-client) 和 [Python](#python-client) 的客户端库支持。

### Go 客户端 {#go-client}

* 想要获得这个库，请运行命令：`go get k8s.io/client-go@kubernetes-<kubernetes-version-number>`，
  有关详细安装说明，请参阅 [INSTALL.md](https://github.com/kubernetes/client-go/blob/master/INSTALL.md#for-the-casual-user)。
  请参阅 [https://github.com/kubernetes/client-go](https://github.com/kubernetes/client-go#compatibility-matrix) 以查看支持的版本。
* 基于这个 client-go 客户端库编写应用程序。
  请注意，client-go 定义了自己的 API 对象，因此如果需要，请从 client-go 而不是从主存储库
  导入 API 定义，例如，`import "k8s.io/client-go/kubernetes"` 才是对的。

Go 客户端可以像 kubectl CLI 一样使用相同的
[kubeconfig 文件](/zh-cn/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
来定位和验证 apiserver。可参阅
[示例](https://git.k8s.io/client-go/examples/out-of-cluster-client-configuration/main.go)。

如果应用程序以 Pod 的形式部署在集群中，那么请参阅
[下一章](#accessing-the-api-from-a-pod)。

### Python 客户端 {#python-client}

如果想要使用 [Python 客户端](https://github.com/kubernetes-client/python)，
请运行命令：`pip install kubernetes`。参阅
[Python Client Library page](https://github.com/kubernetes-client/python)
以获得更详细的安装参数。

Python 客户端可以像 kubectl CLI 一样使用相同的
[kubeconfig 文件](/zh-cn/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
来定位和验证 apiserver，可参阅
[示例](https://github.com/kubernetes-client/python/tree/master/examples)。

### 其它语言 {#other-languages}

目前有多个[客户端库](/zh-cn/docs/reference/using-api/client-libraries/)
为其它语言提供访问 API 的方法。
参阅其它库的相关文档以获取他们是如何验证的。

### 从 Pod 中访问 API   {#accessing-the-api-from-a-pod}

当你从 Pod 中访问 API 时，定位和验证 API 服务器会有些许不同。

请参阅[从 Pod 中访问 API](/zh-cn/docs/tasks/run-application/access-api-from-pod/)
了解更多详情。


## 访问集群上运行的服务  {#accessing-services-running-on-the-cluster}

上一节介绍了如何连接到 Kubernetes API 服务器。
有关连接到 Kubernetes 集群上运行的其他服务的信息，请参阅
[访问集群服务](/zh-cn/docs/tasks/access-application-cluster/access-cluster-services/)。

## 请求重定向 {#requesting-redirects}

重定向功能已弃用并被删除。请改用代理（见下文）。

## 多种代理 {#so-many-proxies}

使用 Kubernetes 时可能会遇到几种不同的代理：

1. [kubectl 代理](#directly-accessing-the-rest-api)：

   - 在用户的桌面或 Pod 中运行
   - 代理从本地主机地址到 Kubernetes apiserver
   - 客户端到代理将使用 HTTP
   - 代理到 apiserver 使用 HTTPS
   - 定位 apiserver
   - 添加身份验证头部

2. [apiserver 代理](/zh-cn/docs/tasks/access-application-cluster/access-cluster-services/#discovering-builtin-services)：

   - 内置于 apiserver 中
   - 将集群外部的用户连接到集群 IP，否则这些 IP 可能无法访问
   - 运行在 apiserver 进程中
   - 客户端代理使用 HTTPS（也可配置为 http）
   - 代理将根据可用的信息决定使用 HTTP 或者 HTTPS 代理到目标
   - 可用于访问节点、Pod 或服务
   - 在访问服务时进行负载平衡

3. [kube proxy](/zh-cn/docs/concepts/services-networking/service/#ips-and-vips)：

   - 运行在每个节点上
   - 代理 UDP 和 TCP
   - 不能代理 HTTP
   - 提供负载均衡
   - 只能用来访问服务

4. 位于 apiserver 之前的 Proxy/Load-balancer：

   - 存在和实现因集群而异（例如 nginx）
   - 位于所有客户和一个或多个 apiserver 之间
   - 如果有多个 apiserver，则充当负载均衡器

5. 外部服务上的云负载均衡器：

   - 由一些云提供商提供（例如 AWS ELB，Google Cloud Load Balancer）
   - 当 Kubernetes 服务类型为 `LoadBalancer` 时自动创建
   - 只使用 UDP/TCP
   - 具体实现因云提供商而异。

除了前两种类型之外，Kubernetes 用户通常不需要担心任何其他问题。
集群管理员通常会确保后者的正确配置。
