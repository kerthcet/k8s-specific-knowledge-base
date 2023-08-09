---
title: kubeadm join
content_type: concept
weight: 30
---

此命令用来初始化 Kubernetes 工作节点并将其加入集群。


{{< include "generated/kubeadm_join.md" >}}

### join 工作流 {#join-workflow}

`kubeadm join` 初始化 Kubernetes 工作节点或控制平面节点并将其添加到集群中。
对于工作节点，该操作包括以下步骤：

1. kubeadm 从 API 服务器下载必要的集群信息。
   默认情况下，它使用引导令牌和 CA 密钥哈希来验证数据的真实性。
   也可以通过文件或 URL 直接发现根 CA。

2. 一旦知道集群信息，kubelet 就可以开始 TLS 引导过程。

   TLS 引导程序使用共享令牌与 Kubernetes API 服务器进行临时的身份验证，以提交证书签名请求 (CSR)；
   默认情况下，控制平面自动对该 CSR 请求进行签名。

3. 最后，kubeadm 配置本地 kubelet 使用分配给节点的确定标识连接到 API 服务器。

对于控制平面节点，执行额外的步骤：

1. 从集群下载控制平面节点之间共享的证书（如果用户明确要求）。

1. 生成控制平面组件清单、证书和 kubeconfig。

1. 添加新的本地 etcd 成员。

### 使用 kubeadm 的 join phase 命令 {#join-phases}

Kubeadm 允许你使用 `kubeadm join phase` 分阶段将节点加入集群。

要查看阶段和子阶段的有序列表，可以调用 `kubeadm join --help`。
该列表将位于帮助屏幕的顶部，每个阶段旁边都有一个描述。
注意，通过调用 `kubeadm join`，所有阶段和子阶段都将按照此确切顺序执行。

有些阶段具有唯一的标志，因此，如果要查看可用选项列表，请添加 `--help`，例如：

```shell
kubeadm join phase kubelet-start --help
```

类似于 [kubeadm init phase](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-init/#init-phases) 命令，
`kubeadm join phase` 允许你使用 `--skip-phases` 标志跳过阶段列表。

例如：

```shell
sudo kubeadm join --skip-phases=preflight --config=config.yaml
```

{{< feature-state for_k8s_version="v1.22" state="beta" >}}

或者，你可以使用 `JoinConfiguration` 中的 `skipPhases` 字段。

### 发现要信任的集群 CA {#discovering-what-cluster-ca-to-trust}

Kubeadm 的发现有几个选项，每个选项都有安全性上的优缺点。
适合你的环境的正确方法取决于节点是如何准备的以及你对网络的安全性期望
和节点的生命周期特点。

#### 带 CA 锁定模式的基于令牌的发现 {#token-based-discovery-with-ca-pinning}

这是 kubeadm 的默认模式。
在这种模式下，kubeadm 下载集群配置（包括根 CA）并使用令牌验证它，
并且会验证根 CA 的公钥与所提供的哈希是否匹配，
以及 API 服务器证书在根 CA 下是否有效。

CA 键哈希格式为 `sha256:<hex_encoded_hash>`。
默认情况下，哈希值会打印在 `kubeadm init` 命令输出的末尾
或者从 `kubeadm token create --print-join-command` 命令的输出信息中返回。
它使用标准格式（请参考 [RFC7469](https://tools.ietf.org/html/rfc7469#section-2.4)）
并且也能通过第三方工具或者制备系统进行计算。
例如，使用 OpenSSL CLI：

```shell
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
```

**`kubeadm join` 命令示例**

对于工作节点：

```shell
kubeadm join --discovery-token abcdef.1234567890abcdef --discovery-token-ca-cert-hash sha256:1234..cdef 1.2.3.4:6443
```

对于控制面节点：

```shell
kubeadm join --discovery-token abcdef.1234567890abcdef --discovery-token-ca-cert-hash sha256:1234..cdef --control-plane 1.2.3.4:6443
```

如果使用 `--upload-certs` 调用 `kubeadm init` 命令，
你也可以对控制平面节点调用带 `--certificate-key` 参数的 `join` 命令，
将证书复制到该节点。


**优势：**

- 允许引导节点安全地发现控制平面节点的信任根，即使其他工作节点或网络受到损害。

- 方便手动执行，因为所需的所有信息都可放到一个 `kubeadm join` 命令中。


**劣势：**

- CA 哈希通常在控制平面节点被提供之前是不知道的，这使得构建使用 kubeadm 的自动化配置工具更加困难。
  通过预先生成 CA，你可以解除这个限制。

#### 无 CA 锁定模式的基于令牌的发现 {#token-based-discovery-without-ca-pinning}

此模式仅依靠对称令牌来签署 (HMAC-SHA256) 为控制平面建立信任根的发现信息。
要使用该模式，加入节点必须使用
`--discovery-token-unsafe-skip-ca-verification`
跳过 CA 公钥的哈希验证。
如果可以，你应该考虑使用其他模式。

**`kubeadm join` 命令示例**

```shell
kubeadm join --token abcdef.1234567890abcdef --discovery-token-unsafe-skip-ca-verification 1.2.3.4:6443
```


**优势**

- 仍然可以防止许多网络级攻击。

- 可以提前生成令牌并与控制平面节点和工作节点共享，这样控制平面节点和工作节点就可以并行引导而无需协调。
  这允许它在许多配置场景中使用。


**劣势**

- 如果攻击者能够通过某些漏洞窃取引导令牌，那么他们可以使用该令牌（连同网络级访问）
  为其它处于引导过程中的节点提供假冒的控制平面节点。
  在你的环境中，这可能是一个适当的折衷方法，也可能不是。

#### 基于 HTTPS 或文件发现 {#file-or-https-based-discovery}

这种方案提供了一种带外方式在控制平面节点和引导节点之间建立信任根。
如果使用 kubeadm 构建自动配置，请考虑使用此模式。
发现文件的格式为常规的 Kubernetes
[kubeconfig](/zh-cn/docs/tasks/access-application-cluster/configure-access-multiple-clusters/) 文件。

如果发现文件不包含凭据，则将使用 TLS 发现令牌。

**`kubeadm join` 命令示例：**

- `kubeadm join --discovery-file path/to/file.conf`（本地文件）

- `kubeadm join --discovery-file https://url/file.conf`（远程 HTTPS URL）


**优势：**

- 允许引导节点安全地发现控制平面节点的信任根，即使网络或其他工作节点受到损害。


**劣势：**

- 要求你有某种方法将发现信息从控制平面节点传送到引导节点。
  如果发现文件包含凭据，你必须对其保密并通过安全通道进行传输。
  这可能通过你的云提供商或供应工具来实现。

#### 将自定义 kubelet 凭据与 `kubeadm join` 结合使用

要允许 `kubeadm join` 使用预定义的 kubelet 凭据并跳过客户端 TLS 引导程序和新节点的 CSR 批准：

1. 从集群中带有 `/etc/kubernetes/pki/ca.key` 的工作控制平面节点执行
   `kubeadm kubeconfig user --org system:nodes --client-name system:node:$NODE > kubelet.conf`。
   `$NODE` 必须设置为新节点的名称。
2. 手动修改生成的 `kubelet.conf` 以调整集群名称和服务器端点，
   或运行 `kubeadm kubeconfig user --config`（它接受 `InitConfiguration`）。

如果集群没有 `ca.key` 文件，你必须在外部对 `kubelet.conf` 中嵌入的证书进行签名。

1. 将生成的 `kubelet.conf` 复制为新节点上的 `/etc/kubernetes/kubelet.conf`。
2. 在新节点上带着标志
   `--ignore-preflight-errors=FileAvailable--etc-kubernetes-kubelet.conf` 执行 `kubeadm join`。

### 确保你的安装更加安全 {#securing-more}

Kubeadm 的默认值可能不适用于所有人。
本节说明如何以牺牲可用性为代价来加强 kubeadm 安装。

#### 关闭节点客户端证书的自动批准 {#turning-off-auto-approval-of-node-client-certificates}

默认情况下，Kubernetes 启用了 CSR 自动批准器，如果在身份验证时使用启动引导令牌，
它会批准对 kubelet 的任何客户端证书的请求。
如果不希望集群自动批准 kubelet 客户端证书，可以通过执行以下命令关闭它：

```shell
kubectl delete clusterrolebinding kubeadm:node-autoapprove-bootstrap
```

关闭后，`kubeadm join` 操作将会被阻塞，直到管理员已经手动批准了在途中的 CSR 才会继续：

1. 使用 `kubectl get csr`，你可以看到原来的 CSR 处于 Pending 状态。

   ```shell
   kubectl get csr
   ```

   输出类似于：

   ```
   NAME                                                   AGE       REQUESTOR                 CONDITION
   node-csr-c69HXe7aYcqkS1bKmH4faEnHAWxn6i2bHZ2mD04jZyQ   18s       system:bootstrap:878f07   Pending
   ```

2. `kubectl certificate approve` 允许管理员批准 CSR。
   此操作告知证书签名控制器向请求者颁发一个证书，该证书具有 CSR 中所请求的那些属性。

   ```shell
   kubectl certificate approve node-csr-c69HXe7aYcqkS1bKmH4faEnHAWxn6i2bHZ2mD04jZyQ
   ```

   输出类似于：

   ```
   certificatesigningrequest "node-csr-c69HXe7aYcqkS1bKmH4faEnHAWxn6i2bHZ2mD04jZyQ" approved
   ```

3. 这会将 CRS 资源更改为 Active 状态。

   ```shell
   kubectl get csr
   ```

   输出类似于：

   ```
   NAME                                                   AGE       REQUESTOR                 CONDITION
   node-csr-c69HXe7aYcqkS1bKmH4faEnHAWxn6i2bHZ2mD04jZyQ   1m        system:bootstrap:878f07   Approved,Issued
   ```

这迫使工作流只有在运行了 `kubectl certificate approve` 后，`kubeadm join` 才能成功。

#### 关闭对 `cluster-info` ConfigMap 的公开访问 {#turning-off-public-access-to-the-cluster-info-configmap}

为了实现使用令牌作为唯一验证信息的加入工作流，默认情况下会公开带有验证控制平面节点标识所需数据的 ConfigMap。
虽然此 ConfigMap 中没有私有数据，但一些用户可能希望无论如何都关闭它。
这样做需要禁用 `kubeadm join` 工作流的 `--discovery-token` 参数。
以下是实现步骤：

* 从 API 服务器获取 `cluster-info` 文件：

```shell
kubectl -n kube-public get cm cluster-info -o jsonpath='{.data.kubeconfig}' | tee cluster-info.yaml
```

输出类似于：

```yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: <ca-cert>
    server: https://<ip>:<port>
  name: ""
contexts: []
current-context: ""
preferences: {}
users: []
```


* 使用 `cluster-info.yaml` 文件作为 `kubeadm join --discovery-file` 参数。

* 关闭 `cluster-info` ConfigMap 的公开访问：

  ```shell
  kubectl -n kube-public delete rolebinding kubeadm:bootstrap-signer-clusterinfo
  ```

这些命令应该在执行 `kubeadm init` 之后、在 `kubeadm join` 之前执行。

### 使用带有配置文件的 kubeadm join {#config-file}

{{< caution >}}
配置文件目前是 beta 功能，在将来的版本中可能会变动。
{{< /caution >}}

可以用配置文件替代命令行参数的方法配置 `kubeadm join`，一些进阶功能也只有在使用配置文件时才可选用。
该文件通过 `--config` 参数来传递，并且文件中必须包含 `JoinConfiguration` 结构。
在某些情况下，不允许将 `--config` 与其他标志混合使用。

使用 [kubeadm config print](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-config/#cmd-config-print)
命令可以打印默认配置。

如果你的配置没有使用最新版本，
**推荐**使用 [kubeadm config migrate](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-config/#cmd-config-migrate)
命令转换。

有关配置的字段和用法的更多信息，你可以导航到我们的
[API 参考页](/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/)。

## {{% heading "whatsnext" %}}

* [kubeadm init](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-init/)
  初始化 Kubernetes 控制平面节点。
* [kubeadm token](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-token/)
  管理 `kubeadm join` 的令牌。
* [kubeadm reset](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-reset/)
  将 `kubeadm init` 或 `kubeadm join` 对主机的更改恢复到之前状态。
