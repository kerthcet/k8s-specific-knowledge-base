---
title: 证书和证书签名请求
content_type: concept
weight: 25
---


{{< feature-state for_k8s_version="v1.19" state="stable" >}}

Kubernetes 证书和信任包（trust bundle）API 可以通过为 Kubernetes API 的客户端提供编程接口，
实现 [X.509](https://www.itu.int/rec/T-REC-X.509) 凭据的自动化制备，
从而请求并获取证书颁发机构 (CA) 发布的 X.509 {{< glossary_tooltip term_id="certificate" text="证书" >}}。

此外，Kubernetes 还对分发[信任包](#cluster-trust-bundles)提供了实验性（Alpha）支持。


## 证书签名请求   {#certificate-signing-requests}

{{< feature-state for_k8s_version="v1.19" state="stable" >}}

CertificateSigningRequest（CSR）资源用来向指定的签名者申请证书签名，
在最终签名之前，申请可能被批准，也可能被拒绝。

### 请求签名流程 {#request-signing-process}

CertificateSigningRequest 资源类型允许客户端基于签名请求申请发放 X.509 证书。
CertificateSigningRequest 对象在 `spec.request` 字段中包含一个 PEM 编码的 PKCS#10 签名请求。
CertificateSigningRequest 使用 `spec.signerName` 字段标示签名者（请求的接收方）。
注意，`spec.signerName` 在 `certificates.k8s.io/v1` 之后的 API 版本是必填项。
在 Kubernetes v1.22 和以后的版本，客户可以可选地设置 `spec.expirationSeconds`
字段来为颁发的证书设定一个特定的有效期。该字段的最小有效值是 `600`，也就是 10 分钟。

创建完成的 CertificateSigningRequest，要先通过批准，然后才能签名。
根据所选的签名者，CertificateSigningRequest 可能会被
{{< glossary_tooltip text="控制器" term_id="controller" >}}自动批准。
否则，就必须人工批准，
人工批准可以使用 REST API（或 go 客户端），也可以执行 `kubectl certificate approve` 命令。
同样，CertificateSigningRequest 也可能被驳回，
这就相当于通知了指定的签名者，这个证书不能签名。

对于已批准的证书，下一步是签名。
对应的签名控制器首先验证签名条件是否满足，然后才创建证书。
签名控制器然后更新 CertificateSigningRequest，
将新证书保存到现有 CertificateSigningRequest 对象的 `status.certificate` 字段中。
此时，字段 `status.certificate` 要么为空，要么包含一个用 PEM 编码的 X.509 证书。
直到签名完成前，CertificateSigningRequest 的字段 `status.certificate` 都为空。

一旦 `status.certificate` 字段完成填充，请求既算完成，
客户端现在可以从 CertificateSigningRequest 资源中获取已签名的证书的 PEM 数据。
当然如果不满足签名条件，签名者可以拒签。

为了减少集群中遗留的过时的 CertificateSigningRequest 资源的数量，
一个垃圾收集控制器将会周期性地运行。
此垃圾收集器会清除在一段时间内没有改变过状态的 CertificateSigningRequests：

* 已批准的请求：1 小时后自动删除
* 已拒绝的请求：1 小时后自动删除
* 已失败的请求：1 小时后自动删除
* 挂起的请求：24 小时后自动删除
* 所有请求：在颁发的证书过期后自动删除

### 证书签名鉴权   {#authorization}

授权创建 CertificateSigningRequest 和检索 CertificateSigningRequest：

* verbs（动词）: `create`、`get`、`list`、`watch`,
  group（组）：`certificates.k8s.io`，
  resource（资源）：`certificatesigningrequests`

例如：

{{< codenew file="access/certificate-signing-request/clusterrole-create.yaml" >}}

授权批准 CertificateSigningRequest：

* verbs（动词）: `get`、`list`、`watch`，
  group（组）：`certificates.k8s.io`，
  resource（资源）：`certificatesigningrequests`
* verbs（动词）: `update`，
  group（组）：`certificates.k8s.io`，
  resource（资源）：`certificatesigningrequests/approval`
* verbs（动词）：`approve`，
  group（组）：`certificates.k8s.io`，
  resource（资源）：`signers`，
  resourceName：`<signerNameDomain>/<signerNamePath>` 或 `<signerNameDomain>/*`

例如：

{{< codenew file="access/certificate-signing-request/clusterrole-approve.yaml" >}}

授权签名 CertificateSigningRequest：

* verbs（动词）：`get`、`list`、`watch`，
  group（组）：`certificates.k8s.io`，
  resource（资源）：`certificatesigningrequests`
* verbs（动词）：`update`，
  group（组）：`certificates.k8s.io`，
  resource（资源）：`certificatesigningrequests/status`
* verbs（动词）：`sign`，
  group（组）：`certificates.k8s.io`，
  resource（资源）：`signers`，
  resourceName：`<signerNameDomain>/<signerNamePath>` 或 `<signerNameDomain>/*`

{{< codenew file="access/certificate-signing-request/clusterrole-sign.yaml" >}}

## 签名者 {#signers}

签名者抽象地代表可能签署或已签署安全证书的一个或多个实体。

任何要在特定集群以外提供的签名者都应该提供关于签名者工作方式的信息，
以便消费者可以理解这对于 CertifcateSigningRequests 和（如果启用的）
[ClusterTrustBundles](#cluster-trust-bundles) 的意义。此类信息包括：

1. **信任分发**：信任锚点（CA 证书或证书包）是如何分发的。
1. **许可的主体**：当一个受限制的主体（subject）发送请求时，相应的限制和应对手段。
1. **许可的 x509 扩展**：包括 IP subjectAltNames、DNS subjectAltNames、
   Email subjectAltNames、URI subjectAltNames 等，请求一个受限制的扩展项时的应对手段。
1. **许可的密钥用途/扩展的密钥用途**：当用途和签名者在 CSR 中指定的用途不同时，
   相应的限制和应对手段。
1. **过期时间/证书有效期**：过期时间由签名者确定、由管理员配置、还是由 CSR `spec.expirationSeconds` 字段指定等，
   以及签名者决定的过期时间与 CSR `spec.expirationSeconds` 字段不同时的应对手段。
1. **允许/不允许 CA 位**：当 CSR 包含一个签名者并不允许的 CA 证书的请求时，相应的应对手段。

一般来说，当 CSR 被批准通过，且证书被签名后，CertificateSigningRequest
的 `status.certificate` 字段将包含一个 PEM 编码的 X.509 证书。
有些签名者在 `status.certificate` 字段中存储多个证书。
在这种情况下，签名者的说明文档应当指明附加证书的含义。
例如，这是要在 TLS 握手时提供的证书和中继证书。

如果要让**信任锚点**（根证书）可用，应该将其与 CertificateSigningRequest 及其 `status.certificate`
字段分开处理。例如，你可以使用 ClusterTrustBundle。

PKCS#10 签名请求格式并没有一种标准的方法去设置证书的过期时间或者生命期。
因此，证书的过期时间或者生命期必须通过 CSR 对象的 `spec.expirationSeconds` 字段来设置。
当 `spec.expirationSeconds` 没有被指定时，内置的签名者默认使用 `ClusterSigningDuration` 配置选项
（kube-controller-manager 的命令行选项 `--cluster-signing-duration`），该选项的默认值设为 1 年。
当 `spec.expirationSeconds` 被指定时，`spec.expirationSeconds` 和 `ClusterSigningDuration`
中的最小值会被使用。

{{< note >}}
`spec.expirationSeconds` 字段是在 Kubernetes v1.22 中加入的。早期的 Kubernetes 版本并不认识该字段。
v1.22 版本之前的 Kubernetes API 服务器会在创建对象的时候忽略该字段。
{{< /note >}}

### Kubernetes 签名者 {#kubernetes-signers}

Kubernetes 提供了内置的签名者，每个签名者都有一个众所周知的 `signerName`:

1. `kubernetes.io/kube-apiserver-client`：签名的证书将被 API 服务器视为客户证书。
   {{< glossary_tooltip term_id="kube-controller-manager" >}} 不会自动批准它。
   1. 信任分发：签名的证书将被 API 服务器视为客户端证书。CA 证书包不通过任何其他方式分发。
   1. 许可的主体：没有主体限制，但审核人和签名者可以选择不批准或不签署。
      某些主体，比如集群管理员级别的用户或组因部署和安装方式不同而不同，
      所以批准和签署之前需要进行额外仔细审查。
      用来限制 `system:masters` 的 CertificateSubjectRestriction 准入插件默认处于启用状态，
      但它通常不是集群中唯一的集群管理员主体。
   1. 许可的 x509 扩展：允许 subjectAltName 和 key usage 扩展，弃用其他扩展。
   1. 许可的密钥用途：必须包含 `["client auth"]`，但不能包含
      `["digital signature", "key encipherment", "client auth"]` 之外的键。
   1. 过期时间/证书有效期：对于 kube-controller-manager 实现的签名者，
      设置为 `--cluster-signing-duration` 选项和 CSR 对象的 `spec.expirationSeconds` 字段（如有设置该字段）中的最小值。
   1. 允许/不允许 CA 位：不允许。

2. `kubernetes.io/kube-apiserver-client-kubelet`: 签名的证书将被 kube-apiserver 视为客户证书。
   {{< glossary_tooltip term_id="kube-controller-manager" >}} 可以自动批准它。

   1. 信任分发：签名的证书将被 API 服务器视为客户端证书。CA 证书包不通过任何其他方式分发。
   1. 许可的主体：组织名必须是 `["system:nodes"]`，用户名以 "`system:node:`" 开头
   1. 许可的 x509 扩展：允许 key usage 扩展，禁用 subjectAltName 扩展，并删除其他扩展。
   1. 许可的密钥用途：`["key encipherment", "digital signature", "client auth"]`
      或 `["digital signature", "client auth"]`。
   1. 过期时间/证书有效期：对于 kube-controller-manager 实现的签名者，
      设置为 `--cluster-signing-duration` 选项和 CSR 对象的 `spec.expirationSeconds` 字段（如有设置该字段）中的最小值。
   1. 允许/不允许 CA 位：不允许。

3. `kubernetes.io/kubelet-serving`: 签名服务证书，该服务证书被 API 服务器视为有效的 kubelet 服务证书，
   但没有其他保证。{{< glossary_tooltip term_id="kube-controller-manager" >}} 不会自动批准它。
   1. 信任分发：签名的证书必须被 kube-apiserver 认可，可有效的中止 kubelet 连接。CA 证书包不通过任何其他方式分发。
   1. 许可的主体：组织名必须是 `["system:nodes"]`，用户名以 "`system:node:`" 开头
   1. 许可的 x509 扩展：允许 key usage、DNSName/IPAddress subjectAltName 等扩展，
      禁止 EmailAddress、URI subjectAltName 等扩展，并丢弃其他扩展。
      至少有一个 DNS 或 IP 的 SubjectAltName 存在。
   1. 许可的密钥用途：`["key encipherment", "digital signature", "server auth"]`
      或 `["digital signature", "server auth"]`。
   1. 过期时间/证书有效期：对于 kube-controller-manager 实现的签名者，
      设置为 `--cluster-signing-duration` 选项和 CSR 对象的 `spec.expirationSeconds` 字段（如有设置该字段）中的最小值。
   1. 允许/不允许 CA 位：不允许。

4. `kubernetes.io/legacy-unknown`: 不保证信任。Kubernetes 的一些第三方发行版可能会使用它签署的客户端证书。
   稳定版的 CertificateSigningRequest API（`certificates.k8s.io/v1` 以及之后的版本）不允许将
   `signerName` 设置为 `kubernetes.io/legacy-unknown`。
   {{< glossary_tooltip term_id="kube-controller-manager" >}} 不会自动批准这类请求。
   1. 信任分发：没有。这个签名者在 Kubernetes 集群中没有标准的信任或分发。
   1. 许可的主体：全部。
   1. 许可的 x509 扩展：允许 subjectAltName 和 key usage 等扩展，并弃用其他扩展。
   1. 许可的密钥用途：全部。
   1. 过期时间/证书有效期：对于 kube-controller-manager 实现的签名者，
      设置为 `--cluster-signing-duration` 选项和 CSR 对象的 `spec.expirationSeconds` 字段（如有设置该字段）中的最小值。
   1. 允许/不允许 CA 位 - 不允许。

kube-controller-manager 为每个内置签名者实现了[控制平面签名](#signer-control-plane)。
注意：所有这些故障仅在 kube-controller-manager 日志中报告。

{{< note >}}
`spec.expirationSeconds` 字段是在 Kubernetes v1.22 中加入的。早期的 Kubernetes 版本并不认识该字段。
v1.22 版本之前的 Kubernetes API 服务器会在创建对象的时候忽略该字段。
{{< /note >}}

对于这些签名者，信任的分发发生在带外（out of band）。上述信任之外的任何信任都是完全巧合的。
例如，一些发行版可能会将 `kubernetes.io/legacy-unknown` 作为 kube-apiserver 的客户端证书，
但这个做法并不标准。
这些用途都没有以任何方式涉及到 ServiceAccount 中的 Secrets `.data[ca.crt]`。
此 CA 证书包只保证使用默认的服务（`kubernetes.default.svc`）来验证到 API 服务器的连接。

## 签名   {#signing}

### 控制平面签名者    {#signer-control-plane}

Kubernetes 控制平面实现了每一个
[Kubernetes 签名者](/zh-cn/docs/reference/access-authn-authz/certificate-signing-requests/#kubernetes-signers)，
每个签名者的实现都是 kube-controller-manager 的一部分。

{{< note >}}
在 Kubernetes v1.18 之前，
kube-controller-manager 签名所有标记为 approved 的 CSR。
{{< /note >}}

{{< note >}}
`spec.expirationSeconds` 字段是在 Kubernetes v1.22 中加入的。早期的 Kubernetes 版本并不认识该字段。
v1.22 版本之前的 Kubernetes API 服务器会在创建对象的时候忽略该字段。
{{< /note >}}

### 基于 API 的签名者   {#signer-api}

REST API 的用户可以通过向待签名的 CSR 的 `status` 子资源提交更新请求来对 CSR 进行签名。

作为这个请求的一部分，`status.certificate` 字段应设置为已签名的证书。
此字段可包含一个或多个 PEM 编码的证书。

所有的 PEM 块必须具备 "CERTIFICATE" 标签，且不包含文件头，且编码的数据必须是
[RFC5280 第 4 节](https://tools.ietf.org/html/rfc5280#section-4.1)
中描述的 BER 编码的 ASN.1 证书结构。

证书内容示例：

```
-----BEGIN CERTIFICATE-----
MIIDgjCCAmqgAwIBAgIUC1N1EJ4Qnsd322BhDPRwmg3b/oAwDQYJKoZIhvcNAQEL
BQAwXDELMAkGA1UEBhMCeHgxCjAIBgNVBAgMAXgxCjAIBgNVBAcMAXgxCjAIBgNV
BAoMAXgxCjAIBgNVBAsMAXgxCzAJBgNVBAMMAmNhMRAwDgYJKoZIhvcNAQkBFgF4
MB4XDTIwMDcwNjIyMDcwMFoXDTI1MDcwNTIyMDcwMFowNzEVMBMGA1UEChMMc3lz
dGVtOm5vZGVzMR4wHAYDVQQDExVzeXN0ZW06bm9kZToxMjcuMC4wLjEwggEiMA0G
CSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDne5X2eQ1JcLZkKvhzCR4Hxl9+ZmU3
+e1zfOywLdoQxrPi+o4hVsUH3q0y52BMa7u1yehHDRSaq9u62cmi5ekgXhXHzGmm
kmW5n0itRECv3SFsSm2DSghRKf0mm6iTYHWDHzUXKdm9lPPWoSOxoR5oqOsm3JEh
Q7Et13wrvTJqBMJo1GTwQuF+HYOku0NF/DLqbZIcpI08yQKyrBgYz2uO51/oNp8a
sTCsV4OUfyHhx2BBLUo4g4SptHFySTBwlpRWBnSjZPOhmN74JcpTLB4J5f4iEeA7
2QytZfADckG4wVkhH3C2EJUmRtFIBVirwDn39GXkSGlnvnMgF3uLZ6zNAgMBAAGj
YTBfMA4GA1UdDwEB/wQEAwIFoDATBgNVHSUEDDAKBggrBgEFBQcDAjAMBgNVHRMB
Af8EAjAAMB0GA1UdDgQWBBTREl2hW54lkQBDeVCcd2f2VSlB1DALBgNVHREEBDAC
ggAwDQYJKoZIhvcNAQELBQADggEBABpZjuIKTq8pCaX8dMEGPWtAykgLsTcD2jYr
L0/TCrqmuaaliUa42jQTt2OVsVP/L8ofFunj/KjpQU0bvKJPLMRKtmxbhXuQCQi1
qCRkp8o93mHvEz3mTUN+D1cfQ2fpsBENLnpS0F4G/JyY2Vrh19/X8+mImMEK5eOy
o0BMby7byUj98WmcUvNCiXbC6F45QTmkwEhMqWns0JZQY+/XeDhEcg+lJvz9Eyo2
aGgPsye1o3DpyXnyfJWAWMhOz7cikS5X2adesbgI86PhEHBXPIJ1v13ZdfCExmdd
M1fLPhLyR54fGaY+7/X8P9AZzPefAkwizeXwe9ii6/a08vWoiE4=
-----END CERTIFICATE-----
```

非 PEM 内容可能会出现在证书 PEM 块前后的位置，且未经验证，
以允许使用 [RFC7468 第 5.2 节](https://www.rfc-editor.org/rfc/rfc7468#section-5.2)中描述的解释性文本。

当使用 JSON 或 YAML 格式时，此字段是 base-64 编码。
包含上述示例证书的 CertificateSigningRequest 如下所示：

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
...
status:
  certificate: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JS..."
```

## 批准和驳回 {#approval-rejection}

[签名者](#signers)基于 CertificateSigningRequest 签发证书之前，
通常会检查 CSR 的签发是否已被**批准**。

### 控制平面的自动化批准 {#approval-rejection-control-plane}

kube-controller-manager 内建了一个证书批准者，其 signerName 为
`kubernetes.io/kube-apiserver-client-kubelet`，
该批准者将 CSR 上用于节点凭据的各种权限委托给权威认证机构。
kube-controller-manager 将 SubjectAccessReview 资源发送（POST）到 API 服务器，
以便检验批准证书的授权。

### 使用 `kubectl` 批准或驳回   {#approval-rejection-kubectl}

Kubernetes 管理员（拥有足够的权限）可以手工批准（或驳回）CertificateSigningRequests，
此操作使用 `kubectl certificate approve` 和 `kubectl certificate deny` 命令实现。

使用 kubectl 批准一个 CSR：

```shell
kubectl certificate approve <certificate-signing-request-name>
```

同样地，驳回一个 CSR：

```shell
kubectl certificate deny <certificate-signing-request-name>
```

### 使用 Kubernetes API 批准或驳回  {#approval-rejection-api-client}

REST API 的用户可以通过向待批准的 CSR 的 `approval` 子资源提交更新请求来批准 CSR。
例如，你可以编写一个
{{< glossary_tooltip term_id="operator-pattern" text="operator" >}}
来监视特定类型的 CSR，然后发送一个更新来批准它。

当你发出批准或驳回的指令时，根据你期望的状态来选择设置 `Approved` 或 `Denied`。

批准（`Approved`） 的 CSR：

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
...
status:
  conditions:
  - lastUpdateTime: "2020-02-08T11:37:35Z"
    lastTransitionTime: "2020-02-08T11:37:35Z"
    message: Approved by my custom approver controller
    reason: ApprovedByMyPolicy # 你可以将此字段设置为任意字符串
    type: Approved
```

驳回（`Denied`）的 CSR：

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
...
status:
  conditions:
  - lastUpdateTime: "2020-02-08T11:37:35Z"
    lastTransitionTime: "2020-02-08T11:37:35Z"
    message: Denied by my custom approver controller
    reason: DeniedByMyPolicy # 你可以将此字段设置为任意字符串
    type: Denied
```

`status.conditions.reason` 字段通常设置为一个首字母大写的对机器友好的原因码;
这是一个命名约定，但你也可以随你的个人喜好设置。
如果你想添加一个供人类使用的注释，那就用 `status.conditions.message` 字段。

## 集群信任包   {#cluster-trust-bundles}

{{< feature-state for_k8s_version="v1.27" state="alpha" >}}

{{< note >}}
在 Kubernetes {{< skew currentVersion >}} 中，如果想要使用此 API，
必须同时启用 `ClusterTrustBundles` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
**以及** `certificates.k8s.io/v1alpha1` {{< glossary_tooltip text="API 组" term_id="api-group" >}}。
{{< /note >}}

ClusterTrustBundles 是一个作用域为集群的对象，向集群内的对象分发 X.509 信任锚点（根证书）。
此对象旨在与 CertificateSigningRequests 中的[签名者](#signers)概念协同工作。

ClusterTrustBundles 可以使用两种模式：
[签名者关联](#ctb-signer-linked)和[签名者未关联](#ctb-signer-unlinked)。

### 常见属性和验证 {#ctb-common}

所有 ClusterTrustBundle 对象都对其 `trustBundle` 字段的内容进行强大的验证。
该字段必须包含一个或多个经 DER 序列化的 X.509 证书，每个证书都封装在 PEM `CERTIFICATE` 块中。
这些证书必须解析为有效的 X.509 证书。

诸如块间数据和块内标头之类的 PEM 特性在对象验证期间要么被拒绝，要么可能被对象的消费者忽略。
此外，消费者被允许使用自己的任意但稳定的排序方式重新排序 bundle 中的证书。

ClusterTrustBundle 对象应该在集群内被视为全局可读的。
如果集群使用 [RBAC](/zh-cn/docs/reference/access-authn-authz/rbac/) 鉴权，
则所有 ServiceAccount 都具有默认授权，允许它们 **get**、**list** 和 **watch**
所有 ClusterTrustBundle 对象。如果你使用自己的鉴权机制，并且在集群中启用了
ClusterTrustBundles，则应设置等效规则以使这些对象在集群内公开，使这些对象按预期工作。

如果你没有默认在集群中列出集群信任包的权限，则可以扮演具有访问权限的 ServiceAccount，
以查看可用的 ClusterTrustBundle：

```bash
kubectl get clustertrustbundles --as='system:serviceaccount:mynamespace:default'
```

### 签名者关联的 ClusterTrustBundles {#ctb-signer-linked}

签名者关联的 ClusterTrustBundles 与**签名者名称**关联，例如：

```yaml
apiVersion: certificates.k8s.io/v1alpha1
kind: ClusterTrustBundle
metadata:
  name: example.com:mysigner:foo
spec:
  signerName: example.com/mysigner
  trustBundle: "<... PEM data ...>"
```

这些 ClusterTrustBundle 预期由集群中的特定签名者控制器维护，因此它们具有多个安全特性：

* 要创建或更新与一个签名者关联的 ClusterTrustBundle，你必须获准**证明**该签名者
  （自定义鉴权动词 `attest` API 组 `certificates.k8s.io`；资源路径 `signers`）。
  你可以为特定资源名称 `<signerNameDomain>/<signerNamePath>` 或匹配 `<signerNameDomain>/*` 等模式来配置鉴权。
* 与签名者关联的 ClusterTrustBundle **必须**使用从其 `spec.signerName` 字段派生的前缀命名。
  斜杠 (`/`) 被替换为英文冒号 (`:`)，最后追加一个英文冒号。后跟任意名称。
  例如，签名者 `example.com/mysigner` 可以关联到 ClusterTrustBundle `example.com:mysigner:<arbitrary-name>`。

与签名者关联的 ClusterTrustBundle 通常通过组合签名者名称有关的
[字段选择算符](/zh-cn/docs/concepts/overview/working-with-objects/field-selectors/)
或单独使用[标签选择算符](/zh-cn/docs/concepts/overview/working-with-objects/labels/#label-selectors)在工作负载中被消耗。

### 签名者未关联的 ClusterTrustBundles   {#ctb-signer-unlinked}

签名者未关联的 ClusterTrustBundles 具有空白的 `spec.signerName` 字段，例如：

```yaml
apiVersion: certificates.k8s.io/v1alpha1
kind: ClusterTrustBundle
metadata:
  name: foo
spec:
  # 未指定 signerName 所以该字段留空
  trustBundle: "<... PEM data ...>"
```

它们主要用于集群配置场景。每个与签名者未关联的 ClusterTrustBundle 都是一个独立的对象，
与签名者关联的 ClusterTrustBundle 的惯常分组行为形成了对比。

与签名者为关联的 ClusterTrustBundle 没有 `attest` 动词要求。
相反，你可以使用通常的机制（如基于角色的访问控制）直接控制对它们的访问。

为了将它们与与签名者关联的 ClusterTrustBundle 区分开来，与签名者未关联的
ClusterTrustBundle 的名称**必须不**包含英文冒号 (`:`)。


## 如何为用户签发证书   {#normal-user}

为了让普通用户能够通过认证并调用 API，需要执行几个步骤。
首先，该用户必须拥有 Kubernetes 集群签发的证书，
然后将该证书提供给 Kubernetes API。

### 创建私钥 {#create-private-key}

下面的脚本展示了如何生成 PKI 私钥和 CSR。
设置 CSR 的 CN 和 O 属性很重要。CN 是用户名，O 是该用户归属的组。
你可以参考 [RBAC](/zh-cn/docs/reference/access-authn-authz/rbac/) 了解标准组的信息。

```shell
openssl genrsa -out myuser.key 2048
openssl req -new -key myuser.key -out myuser.csr
```

### 创建 CertificateSigningRequest {#create-certificatesigningrequest}

创建一个 CertificateSigningRequest，并通过 kubectl 将其提交到 Kubernetes 集群。
下面是生成 CertificateSigningRequest 的脚本。

```shell
cat <<EOF | kubectl apply -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: myuser
spec:
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZqQ0NBVDRDQVFBd0VURVBNQTBHQTFVRUF3d0dZVzVuWld4aE1JSUJJakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVE4QU1JSUJDZ0tDQVFFQTByczhJTHRHdTYxakx2dHhWTTJSVlRWMDNHWlJTWWw0dWluVWo4RElaWjBOCnR2MUZtRVFSd3VoaUZsOFEzcWl0Qm0wMUFSMkNJVXBGd2ZzSjZ4MXF3ckJzVkhZbGlBNVhwRVpZM3ExcGswSDQKM3Z3aGJlK1o2MVNrVHF5SVBYUUwrTWM5T1Nsbm0xb0R2N0NtSkZNMUlMRVI3QTVGZnZKOEdFRjJ6dHBoaUlFMwpub1dtdHNZb3JuT2wzc2lHQ2ZGZzR4Zmd4eW8ybmlneFNVekl1bXNnVm9PM2ttT0x1RVF6cXpkakJ3TFJXbWlECklmMXBMWnoyalVnald4UkhCM1gyWnVVV1d1T09PZnpXM01LaE8ybHEvZi9DdS8wYk83c0x0MCt3U2ZMSU91TFcKcW90blZtRmxMMytqTy82WDNDKzBERHk5aUtwbXJjVDBnWGZLemE1dHJRSURBUUFCb0FBd0RRWUpLb1pJaHZjTgpBUUVMQlFBRGdnRUJBR05WdmVIOGR4ZzNvK21VeVRkbmFjVmQ1N24zSkExdnZEU1JWREkyQTZ1eXN3ZFp1L1BVCkkwZXpZWFV0RVNnSk1IRmQycVVNMjNuNVJsSXJ3R0xuUXFISUh5VStWWHhsdnZsRnpNOVpEWllSTmU3QlJvYXgKQVlEdUI5STZXT3FYbkFvczFqRmxNUG5NbFpqdU5kSGxpT1BjTU1oNndLaTZzZFhpVStHYTJ2RUVLY01jSVUyRgpvU2djUWdMYTk0aEpacGk3ZnNMdm1OQUxoT045UHdNMGM1dVJVejV4T0dGMUtCbWRSeEgvbUNOS2JKYjFRQm1HCkkwYitEUEdaTktXTU0xMzhIQXdoV0tkNjVoVHdYOWl4V3ZHMkh4TG1WQzg0L1BHT0tWQW9FNkpsYWFHdTlQVmkKdjlOSjVaZlZrcXdCd0hKbzZXdk9xVlA3SVFjZmg3d0drWm89Ci0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400  # one day
  usages:
  - client auth
EOF
```

需要注意的几点:

- `usage` 字段必须是 '`client auth`'
- `expirationSeconds` 可以设置为更长（例如 `864000` 是十天）或者更短（例如 `3600` 是一个小时）
- `request` 字段是 CSR 文件内容的 base64 编码值。
  要得到该值，可以执行命令

  ```shell
  cat myuser.csr | base64 | tr -d "\n"
  ```

### 批准 CertificateSigningRequest    {#approve-certificate-signing-request}

使用 kubectl 创建 CSR 并批准。

获取 CSR 列表：

```shell
kubectl get csr
```

批准 CSR：

```shell
kubectl certificate approve myuser
```

### 取得证书 {#get-the-certificate}

从 CSR 取得证书：

```shell
kubectl get csr/myuser -o yaml
```

证书的内容使用 base64 编码，存放在字段 `status.certificate`。

从 CertificateSigningRequest 导出颁发的证书。

```shell
kubectl get csr myuser -o jsonpath='{.status.certificate}'| base64 -d > myuser.crt
```

### 创建角色和角色绑定 {#create-role-and-role-binding}

创建了证书之后，为了让这个用户能访问 Kubernetes 集群资源，现在就要创建
Role 和 RoleBinding 了。

下面是为这个新用户创建 Role 的示例命令：

```shell
kubectl create role developer --verb=create --verb=get --verb=list --verb=update --verb=delete --resource=pods
```

下面是为这个新用户创建 RoleBinding 的示例命令：

```shell
kubectl create rolebinding developer-binding-myuser --role=developer --user=myuser
```

### 添加到 kubeconfig   {#add-to-kubeconfig}

最后一步是将这个用户添加到 kubeconfig 文件。

首先，你需要添加新的凭据：

```shell
kubectl config set-credentials myuser --client-key=myuser.key --client-certificate=myuser.crt --embed-certs=true

```

然后，你需要添加上下文：

```shell
kubectl config set-context myuser --cluster=kubernetes --user=myuser
```

来测试一下，把上下文切换为 `myuser`：

```shell
kubectl config use-context myuser
```

## {{% heading "whatsnext" %}}

* 参阅 [管理集群中的 TLS 认证](/zh-cn/docs/tasks/tls/managing-tls-in-a-cluster/)
* 查看 kube-controller-manager 中[签名者](https://github.com/kubernetes/kubernetes/blob/32ec6c212ec9415f604ffc1f4c1f29b782968ff1/pkg/controller/certificates/signer/cfssl_signer.go)部分的源代码
* 查看 kube-controller-manager 中[批准者](https://github.com/kubernetes/kubernetes/blob/32ec6c212ec9415f604ffc1f4c1f29b782968ff1/pkg/controller/certificates/approver/sarapprove.go)部分的源代码
* 有关 X.509 本身的详细信息，请参阅 [RFC 5280](https://tools.ietf.org/html/rfc5280#section-3.1) 第 3.1 节
* 有关 PKCS#10 证书签名请求语法的信息，请参阅 [RFC 2986](https://tools.ietf.org/html/rfc2986)
