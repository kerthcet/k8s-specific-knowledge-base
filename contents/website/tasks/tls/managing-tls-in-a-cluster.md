---
title: 管理集群中的 TLS 认证
content_type: task
---

Kubernetes 提供 `certificates.k8s.io` API，可让你配置由你控制的证书颁发机构（CA）
签名的 TLS 证书。 你的工作负载可以使用这些 CA 和证书来建立信任。

`certificates.k8s.io` API使用的协议类似于
[ACME 草案](https://github.com/ietf-wg-acme/acme/)。

{{< note >}}
使用 `certificates.k8s.io` API 创建的证书由指定 [CA](#configuring-your-cluster-to-provide-signing) 颁发。
将集群配置为使用集群根目录 CA 可以达到这个目的，但是你永远不要依赖这一假定。
不要以为这些证书将针对群根目录 CA 进行验证。
{{< /note >}}

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

你需要 `cfssl` 工具。
你可以从 [https://github.com/cloudflare/cfssl/releases](https://github.com/cloudflare/cfssl/releases)
下载 `cfssl`。

本文中某些步骤使用 `jq` 工具。如果你没有 `jq`，你可以通过操作系统的软件源安装，
或者从 [https://stedolan.github.io/jq/](https://stedolan.github.io/jq/) 获取。


## 集群中的 TLS 信任

信任 Pod 中运行的应用程序所提供的[自定义 CA](#configuring-your-cluster-to-provide-signing) 通常需要一些额外的应用程序配置。
你需要将 CA 证书包添加到 TLS 客户端或服务器信任的 CA 证书列表中。
例如，你可以使用 Golang TLS 配置通过解析证书链并将解析的证书添加到
[`tls.Config`](https://pkg.go.dev/crypto/tls#Config) 结构中的 `RootCAs`
字段中。

{{< note >}}
即使自定义 CA 证书可能包含在文件系统中（在 ConfigMap `kube-root-ca.crt` 中），
除了验证内部 Kubernetes 端点之外，你不应将该证书颁发机构用于任何目的。
内部 Kubernetes 端点的一个示例是默认命名空间中名为 `kubernetes` 的服务。

如果你想为你的工作负载使用自定义证书颁发机构，你应该单独生成该 CA，
并使用你的 Pod 有读权限的 [ConfigMap](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap)
分发该 CA 证书。
{{< /note >}}

## 请求证书

以下部分演示如何为通过 DNS 访问的 Kubernetes 服务创建 TLS 证书。

{{< note >}}
本教程使用 CFSSL：Cloudflare's PKI 和 TLS 工具包
[点击此处](https://blog.cloudflare.com/introducing-cfssl/)了解更多信息。
{{< /note >}}

## 创建证书签名请求

通过运行以下命令生成私钥和证书签名请求（或 CSR）:

```shell
cat <<EOF | cfssl genkey - | cfssljson -bare server
{
  "hosts": [
    "my-svc.my-namespace.svc.cluster.local",
    "my-pod.my-namespace.pod.cluster.local",
    "192.0.2.24",
    "10.0.34.2"
  ],
  "CN": "my-pod.my-namespace.pod.cluster.local",
  "key": {
    "algo": "ecdsa",
    "size": 256
  }
}
EOF
```

其中 `192.0.2.24` 是服务的集群 IP，`my-svc.my-namespace.svc.cluster.local`
是服务的 DNS 名称，`10.0.34.2` 是 Pod 的 IP，而
`my-pod.my-namespace.pod.cluster.local` 是 Pod 的 DNS 名称。
你能看到的输出类似于：

```
2022/02/01 11:45:32 [INFO] generate received request
2022/02/01 11:45:32 [INFO] received CSR
2022/02/01 11:45:32 [INFO] generating key: ecdsa-256
2022/02/01 11:45:32 [INFO] encoded CSR
```

此命令生成两个文件；它生成包含 PEM 编码
[PKCS#10](https://tools.ietf.org/html/rfc2986) 证书请求的 `server.csr`，
以及 PEM 编码密钥的 `server-key.pem`，用于待生成的证书。

## 创建证书签名请求（CSR）对象发送到 Kubernetes API

你可以使用以下命令创建 CSR 清单（YAML 格式），并发送到 API 服务器：

```shell
cat <<EOF | kubectl apply -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: my-svc.my-namespace
spec:
  request: $(cat server.csr | base64 | tr -d '\n')
  signerName: example.com/serving
  usages:
  - digital signature
  - key encipherment
  - server auth
EOF
```

请注意，在步骤 1 中创建的 `server.csr` 文件是 base64 编码并存储在
`.spec.request` 字段中的。你还要求提供 “digital signature（数字签名）”，
“密钥加密（key encipherment）” 和 “服务器身份验证（server auth）” 密钥用途，
由 `example.com/serving` 示例签名程序签名的证书。
你也可以要求使用特定的 `signerName`。更多信息可参阅
[支持的签署者名称](/zh-cn/docs/reference/access-authn-authz/certificate-signing-requests/#signers)。

在 API server 中可以看到这些 CSR 处于 Pending 状态。执行下面的命令你将可以看到：

```shell
kubectl describe csr my-svc.my-namespace
```

```none
Name:                   my-svc.my-namespace
Labels:                 <none>
Annotations:            <none>
CreationTimestamp:      Tue, 01 Feb 2022 11:49:15 -0500
Requesting User:        yourname@example.com
Signer:                 example.com/serving
Status:                 Pending
Subject:
        Common Name:    my-pod.my-namespace.pod.cluster.local
        Serial Number:
Subject Alternative Names:
        DNS Names:      my-pod.my-namespace.pod.cluster.local
                        my-svc.my-namespace.svc.cluster.local
        IP Addresses:   192.0.2.24
                        10.0.34.2
Events: <none>
```

## 批准证书签名请求（CSR）  {#get-the-certificate-signing-request-approved}

[证书签名请求](/zh-cn/docs/reference/access-authn-authz/certificate-signing-requests/)
的批准或者是通过自动批准过程完成的，或由集群管理员一次性完成。
如果你被授权批准证书请求，你可以使用 `kubectl` 来手动完成此操作；例如：

```shell
kubectl certificate approve my-svc.my-namespace
```

```none
certificatesigningrequest.certificates.k8s.io/my-svc.my-namespace approved
```

你现在应该能看到如下输出：

```shell
kubectl get csr
```

```none
NAME                  AGE   SIGNERNAME            REQUESTOR              REQUESTEDDURATION   CONDITION
my-svc.my-namespace   10m   example.com/serving   yourname@example.com   <none>              Approved
```

这意味着证书请求已被批准，并正在等待请求的签名者对其签名。

## 签名证书签名请求（CSR） {#sign-the-certificate-signing-request}

接下来，你将扮演证书签署者的角色，颁发证书并将其上传到 API 服务器。

签名者通常会使用其 `signerName` 查看对象的 CertificateSigningRequest API，
检查它们是否已被批准，为这些请求签署证书，并使用已颁发的证书更新 API 对象状态。

### 创建证书颁发机构

你需要授权在新证书上提供数字签名。

首先，通过运行以下命令创建签名证书：

```shell
cat <<EOF | cfssl gencert -initca - | cfssljson -bare ca
{
  "CN": "My Example Signer",
  "key": {
    "algo": "rsa",
    "size": 2048
  }
}
EOF
```

你应该看到类似于以下的输出：

```none
2022/02/01 11:50:39 [INFO] generating a new CA key and certificate from CSR
2022/02/01 11:50:39 [INFO] generate received request
2022/02/01 11:50:39 [INFO] received CSR
2022/02/01 11:50:39 [INFO] generating key: rsa-2048
2022/02/01 11:50:39 [INFO] encoded CSR
2022/02/01 11:50:39 [INFO] signed certificate with serial number 263983151013686720899716354349605500797834580472
```

这会产生一个证书颁发机构密钥文件（`ca-key.pem`）和证书（`ca.pem`）。


### 颁发证书

{{< codenew file="tls/server-signing-config.json" >}}

使用 `server-signing-config.json` 签名配置、证书颁发机构密钥文件和证书来签署证书请求：

```shell
kubectl get csr my-svc.my-namespace -o jsonpath='{.spec.request}' | \
  base64 --decode | \
  cfssl sign -ca ca.pem -ca-key ca-key.pem -config server-signing-config.json - | \
  cfssljson -bare ca-signed-server
```

你应该看到类似于以下的输出：

```
2022/02/01 11:52:26 [INFO] signed certificate with serial number 576048928624926584381415936700914530534472870337
```

这会生成一个签名的服务证书文件，`ca-signed-server.pem`。


### 上传签名证书

最后，在 API 对象的状态中填充签名证书：

```shell
kubectl get csr my-svc.my-namespace -o json | \
  jq '.status.certificate = "'$(base64 ca-signed-server.pem | tr -d '\n')'"' | \
  kubectl replace --raw /apis/certificates.k8s.io/v1/certificatesigningrequests/my-svc.my-namespace/status -f -
```

{{< note >}}
这使用命令行工具 [`jq`](https://stedolan.github.io/jq/)
在 `.status.certificate` 字段中填充 base64 编码的内容。
如果你没有 `jq` 工具，你还可以将 JSON 输出保存到文件中，手动填充此字段，然后上传结果文件。
{{< /note >}}

批准 CSR 并上传签名证书后，运行：

```shell
kubectl get csr
```

输入类似于：

```none
NAME                  AGE   SIGNERNAME            REQUESTOR              REQUESTEDDURATION   CONDITION
my-svc.my-namespace   20m   example.com/serving   yourname@example.com   <none>              Approved,Issued
```

## 下载证书并使用它

现在，作为请求用户，你可以通过运行以下命令下载颁发的证书并将其保存到 `server.crt` 文件中：

CSR 被签署并获得批准后，你应该看到以下内容：

```shell
kubectl get csr my-svc.my-namespace -o jsonpath='{.status.certificate}' \
    | base64 --decode > server.crt
```

现在你可以将 `server.crt` 和 `server-key.pem` 填充到
{{<glossary_tooltip text="Secret" term_id="secret" >}} 中，
稍后你可以将其挂载到 Pod 中（例如，用于提供 HTTPS 的网络服务器）。

```shell
kubectl create secret tls server --cert server.crt --key server-key.pem
```

```none
secret/server created
```

最后，你可以将 `ca.pem` 填充到
{{<glossary_tooltip text="ConfigMap" term_id="configmap" >}}
并将其用作信任根来验证服务证书：

```shell
kubectl create configmap example-serving-ca --from-file ca.crt=ca.pem
```

```none
configmap/example-serving-ca created
```

## 批准证书签名请求（CSR）  {#approving-certificate-signing-requests}

Kubernetes 管理员（具有适当权限）可以使用 `kubectl certificate approve` 和
`kubectl certificate deny` 命令手动批准（或拒绝）证书签名请求（CSR）。
但是，如果你打算大量使用此 API，则可以考虑编写自动化的证书控制器。

{{< caution >}}
批准证书 CSR 的能力决定了在你的环境中谁信任谁。
不应广泛或轻率地授予批准 CSR 的能力。

在授予 `approve` 权限之前，你应该确保自己充分了解批准人的验证要求**和**颁发特定证书的后果。
{{< /caution >}}

无论上述机器或人使用 kubectl，“批准者”的作用是验证 CSR 满足如下两个要求：

1. CSR 的 subject 控制用于签署 CSR 的私钥。这解决了伪装成授权主体的第三方的威胁。
   在上述示例中，此步骤将验证该 Pod 控制了用于生成 CSR 的私钥。
2. CSR 的 subject 被授权在请求的上下文中执行。
   这点用于处理不期望的主体被加入集群的威胁。
   在上述示例中，此步骤将是验证该 Pod 是否被允许加入到所请求的服务中。

当且仅当满足这两个要求时，审批者应该批准 CSR，否则拒绝 CSR。

有关证书批准和访问控制的更多信息，
请阅读[证书签名请求](/zh-cn/docs/reference/access-authn-authz/certificate-signing-requests/)参考页。

## 给集群管理员的一个建议

本页面假设已经为 certificates API 配置了签名者。
Kubernetes 控制器管理器提供了一个签名者的默认实现。要启用它，请为控制器管理器设置
`--cluster-signing-cert-file` 和 `--cluster-signing-key-file` 参数，
使之取值为你的证书机构的密钥对的路径。
