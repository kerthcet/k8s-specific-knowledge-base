---
title: 使用 kubeadm 进行证书管理
content_type: task
weight: 10
---


{{< feature-state for_k8s_version="v1.15" state="stable" >}}

由 [kubeadm](/zh-cn/docs/reference/setup-tools/kubeadm/) 生成的客户端证书在 1 年后到期。
本页说明如何使用 kubeadm 管理证书续订，同时也涵盖其他与 kubeadm 证书管理相关的说明。

## {{% heading "prerequisites" %}}

你应该熟悉 [Kubernetes 中的 PKI 证书和要求](/zh-cn/docs/setup/best-practices/certificates/)。



## 使用自定义的证书   {#custom-certificates}

默认情况下，kubeadm 会生成运行一个集群所需的全部证书。
你可以通过提供你自己的证书来改变这个行为策略。

如果要这样做，你必须将证书文件放置在通过 `--cert-dir` 命令行参数或者 kubeadm 配置中的
`certificatesDir` 配置项指明的目录中。默认的值是 `/etc/kubernetes/pki`。

如果在运行 `kubeadm init` 之前存在给定的证书和私钥对，kubeadm 将不会重写它们。
例如，这意味着你可以将现有的 CA 复制到 `/etc/kubernetes/pki/ca.crt` 和
`/etc/kubernetes/pki/ca.key` 中，而 kubeadm 将使用此 CA 对其余证书进行签名。


## 外部 CA 模式   {#external-ca-mode}

只提供了 `ca.crt` 文件但是不提供 `ca.key` 文件也是可以的
（这只对 CA 根证书可用，其它证书不可用）。
如果所有的其它证书和 kubeconfig 文件已就绪，kubeadm 检测到满足以上条件就会激活
"外部 CA" 模式。kubeadm 将会在没有 CA 密钥文件的情况下继续执行。

否则，kubeadm 将独立运行 controller-manager，附加一个
`--controllers=csrsigner` 的参数，并且指明 CA 证书和密钥。

[PKI 证书和要求](/zh-cn/docs/setup/best-practices/certificates/)包括集群使用外部
CA 的设置指南。

## 检查证书是否过期  {#check-certificate-expiration}

你可以使用 `check-expiration` 子命令来检查证书何时过期

```shell
kubeadm certs check-expiration
```

输出类似于以下内容：

```console
CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE AUTHORITY   EXTERNALLY MANAGED
admin.conf                 Dec 30, 2020 23:36 UTC   364d                                    no
apiserver                  Dec 30, 2020 23:36 UTC   364d            ca                      no
apiserver-etcd-client      Dec 30, 2020 23:36 UTC   364d            etcd-ca                 no
apiserver-kubelet-client   Dec 30, 2020 23:36 UTC   364d            ca                      no
controller-manager.conf    Dec 30, 2020 23:36 UTC   364d                                    no
etcd-healthcheck-client    Dec 30, 2020 23:36 UTC   364d            etcd-ca                 no
etcd-peer                  Dec 30, 2020 23:36 UTC   364d            etcd-ca                 no
etcd-server                Dec 30, 2020 23:36 UTC   364d            etcd-ca                 no
front-proxy-client         Dec 30, 2020 23:36 UTC   364d            front-proxy-ca          no
scheduler.conf             Dec 30, 2020 23:36 UTC   364d                                    no

CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY MANAGED
ca                      Dec 28, 2029 23:36 UTC   9y              no
etcd-ca                 Dec 28, 2029 23:36 UTC   9y              no
front-proxy-ca          Dec 28, 2029 23:36 UTC   9y              no
```

该命令显示 `/etc/kubernetes/pki` 文件夹中的客户端证书以及
kubeadm（`admin.conf`、`controller-manager.conf` 和 `scheduler.conf`）
使用的 kubeconfig 文件中嵌入的客户端证书的到期时间/剩余时间。

另外，kubeadm 会通知用户证书是否由外部管理；
在这种情况下，用户应该小心的手动/使用其他工具来管理证书更新。

{{< warning >}}
`kubeadm` 不能管理由外部 CA 签名的证书。
{{< /warning >}}

{{< note >}}
上面的列表中没有包含 `kubelet.conf`，因为 kubeadm 将 kubelet
配置为[自动更新证书](/zh-cn/docs/tasks/tls/certificate-rotation/)。
轮换的证书位于目录 `/var/lib/kubelet/pki`。
要修复过期的 kubelet 客户端证书，请参阅
[kubelet 客户端证书轮换失败](/zh-cn/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/#kubelet-client-cert)。
{{< /note >}}

{{< warning >}}
在通过 `kubeadm init` 创建的节点上，在 kubeadm 1.17
版本之前有一个[缺陷](https://github.com/kubernetes/kubeadm/issues/1753)，
该缺陷使得你必须手动修改 `kubelet.conf` 文件的内容。
`kubeadm init` 操作结束之后，你必须更新 `kubelet.conf` 文件将 `client-certificate-data`
和 `client-key-data` 改为如下所示的内容以便使用轮换后的 kubelet 客户端证书：

```yaml
client-certificate: /var/lib/kubelet/pki/kubelet-client-current.pem
client-key: /var/lib/kubelet/pki/kubelet-client-current.pem
```
{{< /warning >}}

## 自动更新证书 {#automatic-certificate-renewal}

kubeadm
会在控制面[升级](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)的时候更新所有证书。

这个功能旨在解决最简单的用例；如果你对此类证书的更新没有特殊要求，
并且定期执行 Kubernetes 版本升级（每次升级之间的间隔时间少于 1 年），
则 kubeadm 将确保你的集群保持最新状态并保持合理的安全性。

{{< note >}}
最佳的做法是经常升级集群以确保安全。
{{< /note >}}

如果你对证书更新有更复杂的需求，则可通过将 `--certificate-renewal=false` 传递给
`kubeadm upgrade apply` 或者 `kubeadm upgrade node`，从而选择不采用默认行为。

{{< warning >}}
kubeadm 在 1.17 版本之前有一个[缺陷](https://github.com/kubernetes/kubeadm/issues/1818)，
该缺陷导致 `kubeadm update node` 执行时 `--certificate-renewal` 的默认值被设置为 `false`。
在这种情况下，你需要显式地设置 `--certificate-renewal=true`。
{{< /warning >}}

## 手动更新证书 {#manual-certificate-renewal}

你能随时通过 `kubeadm certs renew` 命令手动更新你的证书。

此命令用 CA（或者 front-proxy-CA ）证书和存储在 `/etc/kubernetes/pki` 中的密钥执行更新。

执行完此命令之后你需要重启控制面 Pod。因为动态证书重载目前还不被所有组件和证书支持，所有这项操作是必须的。
[静态 Pod](/zh-cn/docs/tasks/configure-pod-container/static-pod/) 是被本地 kubelet
而不是 API 服务器管理，所以 kubectl 不能用来删除或重启他们。
要重启静态 Pod 你可以临时将清单文件从 `/etc/kubernetes/manifests/` 移除并等待 20 秒
（参考 [KubeletConfiguration 结构](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/)中的
`fileCheckFrequency` 值）。如果 Pod 不在清单目录里，kubelet 将会终止它。
在另一个 `fileCheckFrequency` 周期之后你可以将文件移回去，kubelet 可以完成 Pod
的重建，而组件的证书更新操作也得以完成。

{{< warning >}}
如果你运行了一个 HA 集群，这个命令需要在所有控制面板节点上执行。
{{< /warning >}}

{{< note >}}
`certs renew` 使用现有的证书作为属性（Common Name、Organization、SAN 等）的权威来源，
而不是 `kubeadm-config` ConfigMap。强烈建议使它们保持同步。
{{< /note >}}

`kubeadm certs renew` 提供以下选项：

- Kubernetes 证书通常在一年后到期。

- `--csr-only` 可用于经过一个外部 CA 生成的证书签名请求来更新证书（无需实际替换更新证书）；
  更多信息请参见下节。

- 可以更新单个证书而不是全部证书。

## 用 Kubernetes 证书 API 更新证书 {#renew-certificates-with-the-kubernetes-certificates-api}

本节提供有关如何使用 Kubernetes 证书 API 执行手动证书更新的更多详细信息。

{{< caution >}}
这些是针对需要将其组织的证书基础结构集成到 kubeadm 构建的集群中的用户的高级主题。
如果默认的 kubeadm 配置满足了你的需求，则应让 kubeadm 管理证书。
{{< /caution >}}


### 设置一个签名者（Signer） {#set-up-a-signer}

Kubernetes 证书颁发机构不是开箱即用。你可以配置外部签名者，例如
[cert-manager](https://cert-manager.io/docs/configuration/ca/)，
也可以使用内置签名者。

内置签名者是
[`kube-controller-manager`](/zh-cn/docs/reference/command-line-tools-reference/kube-controller-manager/)
的一部分。

要激活内置签名者，请传递 `--cluster-signing-cert-file` 和 `--cluster-signing-key-file` 参数。

如果你正在创建一个新的集群，你可以使用 kubeadm
的[配置文件](/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/)。

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
controllerManager:
  extraArgs:
    cluster-signing-cert-file: /etc/kubernetes/pki/ca.crt
    cluster-signing-key-file: /etc/kubernetes/pki/ca.key
```

### 创建证书签名请求 (CSR) {#create-certificate-signing-requests-csr}

有关使用 Kubernetes API 创建 CSR 的信息，
请参见[创建 CertificateSigningRequest](/zh-cn/docs/reference/access-authn-authz/certificate-signing-requests/#create-certificatesigningrequest)。

## 通过外部 CA 更新证书 {#renew-certificates-with-external-ca}

本节提供有关如何使用外部 CA 执行手动更新证书的更多详细信息。

为了更好的与外部 CA 集成，kubeadm 还可以生成证书签名请求（CSR）。
CSR 表示向 CA 请求客户的签名证书。
在 kubeadm 术语中，通常由磁盘 CA 签名的任何证书都可以作为 CSR 生成。但是，CA 不能作为 CSR 生成。

### 创建证书签名请求 (CSR) {#create-certificate-signing-requests-csr-1}

你可以通过 `kubeadm certs renew --csr-only` 命令创建证书签名请求。

CSR 和随附的私钥都在输出中给出。
你可以传入一个带有 `--csr-dir` 的目录，将 CSR 输出到指定位置。
如果未指定 `--csr-dir`，则使用默认证书目录（`/etc/kubernetes/pki`）。

证书可以通过 `kubeadm certs renew --csr-only` 来续订。
和 `kubeadm init` 一样，可以使用 `--csr-dir` 标志指定一个输出目录。

CSR 中包含一个证书的名字，域和 IP，但是未指定用法。
颁发证书时，CA 有责任指定[正确的证书用法](/zh-cn/docs/setup/best-practices/certificates/#all-certificates)

* 在 `openssl` 中，这是通过
  [`openssl ca` 命令](https://superuser.com/questions/738612/openssl-ca-keyusage-extension)
  来完成的。
* 在 `cfssl` 中，这是通过
  [在配置文件中指定用法](https://github.com/cloudflare/cfssl/blob/master/doc/cmd/cfssl.txt#L170)
  来完成的。

使用首选方法对证书签名后，必须将证书和私钥复制到 PKI 目录（默认为 `/etc/kubernetes/pki`）。

## 证书机构（CA）轮换 {#certificate-authority-rotation}

kubeadm 并不直接支持对 CA 证书的轮换或者替换。

关于手动轮换或者置换 CA 的更多信息，
可参阅[手动轮换 CA 证书](/zh-cn/docs/tasks/tls/manual-rotation-of-ca-certificates/)。

## 启用已签名的 kubelet 服务证书 {#kubelet-serving-certs}

默认情况下，kubeadm 所部署的 kubelet 服务证书是自签名（Self-Signed）。
这意味着从 [metrics-server](https://github.com/kubernetes-sigs/metrics-server)
这类外部服务发起向 kubelet 的链接时无法使用 TLS 来完成保护。

要在新的 kubeadm 集群中配置 kubelet 以使用被正确签名的服务证书，
你必须向 `kubeadm init` 传递如下最小配置数据：

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
serverTLSBootstrap: true
```

如果你已经创建了集群，你必须通过执行下面的操作来完成适配：

- 找到 `kube-system` 名字空间中名为 `kubelet-config-{{< skew currentVersion >}}`
  的 ConfigMap 并编辑之。
  在该 ConfigMap 中，`kubelet` 键下面有一个
  [KubeletConfiguration](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/)
  文档作为其取值。编辑该 KubeletConfiguration 文档以设置
  `serverTLSBootstrap: true`。
- 在每个节点上，在 `/var/lib/kubelet/config.yaml` 文件中添加
  `serverTLSBootstrap: true` 字段，并使用 `systemctl restart kubelet`
  来重启 kubelet。

字段 `serverTLSBootstrap` 将允许启动引导 kubelet 的服务证书，方式是从
`certificates.k8s.io` API 处读取。这种方式的一种局限在于这些证书的
CSR（证书签名请求）不能被 kube-controller-manager 中默认的签名组件
[`kubernetes.io/kubelet-serving`](/zh-cn/docs/reference/access-authn-authz/certificate-signing-requests/#kubernetes-signers)
批准。需要用户或者第三方控制器来执行此操作。

可以使用下面的命令来查看 CSR：

```shell
kubectl get csr
```

```console
NAME        AGE     SIGNERNAME                        REQUESTOR                      CONDITION
csr-9wvgt   112s    kubernetes.io/kubelet-serving     system:node:worker-1           Pending
csr-lz97v   1m58s   kubernetes.io/kubelet-serving     system:node:control-plane-1    Pending
```

你可以执行下面的操作来批准这些请求：

```shell
kubectl certificate approve <CSR-名称>
```

默认情况下，这些服务证书会在一年后过期。
kubeadm 将 `KubeletConfiguration` 的 `rotateCertificates` 字段设置为
`true`；这意味着证书快要过期时，会生成一组针对服务证书的新的 CSR，而这些
CSR 也要被批准才能完成证书轮换。要进一步了解这里的细节，
可参阅[证书轮换](/zh-cn/docs/reference/access-authn-authz/kubelet-tls-bootstrapping/#certificate-rotation)文档。

如果你在寻找一种能够自动批准这些 CSR 的解决方案，建议你与你的云提供商
联系，询问他们是否有 CSR 签名组件，用来以带外（out-of-band）的方式检查
节点的标识符。

{{% thirdparty-content %}}

也可以使用第三方定制的控制器：

- [kubelet-csr-approver](https://github.com/postfinance/kubelet-csr-approver)

除非既能够验证 CSR 中的 CommonName，也能检查请求的 IP 和域名，
这类控制器还算不得安全的机制。
只有完成彻底的检查，才有可能避免有恶意的、能够访问 kubelet 客户端证书的第三方为任何
IP 或域名请求服务证书。

## 为其他用户生成 kubeconfig 文件 {#kubeconfig-additional-users}

在集群创建过程中，kubeadm 对 `admin.conf` 中的证书进行签名时，将其配置为
`Subject: O = system:masters, CN = kubernetes-admin`。
[`system:masters`](/zh-cn/docs/reference/access-authn-authz/rbac/#user-facing-roles)
是一个例外的超级用户组，可以绕过鉴权层（例如 RBAC）。
强烈建议不要将 `admin.conf` 文件与任何人共享。

你要使用 [`kubeadm kubeconfig user`](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-kubeconfig)
命令为其他用户生成 kubeconfig 文件，这个命令支持命令行参数和
[kubeadm 配置结构](/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/)。
以上命令会将 kubeconfig 打印到终端上，也可以使用 `kubeadm kubeconfig user ... > somefile.conf`
输出到一个文件中。

如下 kubeadm 可以在 `--config` 后加的配置文件示例：

```yaml
# example.yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
# kubernetes 将作为 kubeconfig 中集群名称
clusterName: "kubernetes"
# some-dns-address:6443 将作为集群 kubeconfig 文件中服务地址（IP 或者 DNS 名称）
controlPlaneEndpoint: "some-dns-address:6443"
# 从本地挂载集群的 CA 秘钥和 CA 证书
certificatesDir: "/etc/kubernetes/pki"
```

确保这些设置与所需的目标集群设置相匹配。可以使用以下命令查看现有集群的设置：

```shell
kubectl get cm kubeadm-config -n kube-system -o=jsonpath="{.data.ClusterConfiguration}"
```

以下示例将为在 `appdevs` 组的 `johndoe` 用户创建一个有效期为 24 小时的 kubeconfig 文件：

```shell
kubeadm kubeconfig user --config example.yaml --org appdevs --client-name johndoe --validity-period 24h
```

以下示例将为管理员创建一个有效期有一周的 kubeconfig 文件：

```shell
kubeadm kubeconfig user --config example.yaml --client-name admin --validity-period 168h
```
