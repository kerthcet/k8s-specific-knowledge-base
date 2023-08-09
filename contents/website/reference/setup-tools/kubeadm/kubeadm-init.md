---
title: kubeadm init
content_type: concept
weight: 20
---



此命令初始化一个 Kubernetes 控制平面节点。


{{< include "generated/kubeadm_init.md" >}}

### Init 命令的工作流程 {#init-workflow}

`kubeadm init` 命令通过执行下列步骤来启动一个 Kubernetes 控制平面节点。

1. 在做出变更前运行一系列的预检项来验证系统状态。一些检查项目仅仅触发警告，
   其它的则会被视为错误并且退出 kubeadm，除非问题得到解决或者用户指定了
   `--ignore-preflight-errors=<错误列表>` 参数。

2. 生成一个自签名的 CA 证书来为集群中的每一个组件建立身份标识。
   用户可以通过将其放入 `--cert-dir` 配置的证书目录中（默认为 `/etc/kubernetes/pki`）
   来提供他们自己的 CA 证书以及/或者密钥。
   APIServer 证书将为任何 `--apiserver-cert-extra-sans` 参数值提供附加的 SAN 条目，必要时将其小写。

3. 将 kubeconfig 文件写入 `/etc/kubernetes/` 目录以便 kubelet、控制器管理器和调度器用来连接到
   API 服务器，它们每一个都有自己的身份标识，同时生成一个名为 `admin.conf` 的独立的 kubeconfig
   文件，用于管理操作。

4. 为 API 服务器、控制器管理器和调度器生成静态 Pod 的清单文件。假使没有提供一个外部的 etcd
   服务的话，也会为 etcd 生成一份额外的静态 Pod 清单文件。

   静态 Pod 的清单文件被写入到 `/etc/kubernetes/manifests` 目录；
   kubelet 会监视这个目录以便在系统启动的时候创建 Pod。

   一旦控制平面的 Pod 都运行起来，`kubeadm init` 的工作流程就继续往下执行。

5. 对控制平面节点应用标签和污点标记以便不会在它上面运行其它的工作负载。

6. 生成令牌，将来其他节点可使用该令牌向控制平面注册自己。
   如 [kubeadm token](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-token/) 文档所述，
   用户可以选择通过 `--token` 提供令牌。

7. 为了使得节点能够遵照[启动引导令牌](/zh-cn/docs/reference/access-authn-authz/bootstrap-tokens/)和
   [TLS 启动引导](/zh-cn/docs/reference/access-authn-authz/kubelet-tls-bootstrapping/)
   这两份文档中描述的机制加入到集群中，kubeadm 会执行所有的必要配置：

   - 创建一个 ConfigMap 提供添加集群节点所需的信息，并为该 ConfigMap 设置相关的 RBAC 访问规则。

   - 允许启动引导令牌访问 CSR 签名 API。

   - 配置自动签发新的 CSR 请求。

   更多相关信息，请查看 [kubeadm join](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-join/)。

8. 通过 API 服务器安装一个 DNS 服务器 (CoreDNS) 和 kube-proxy 附加组件。
   在 Kubernetes 版本 1.11 和更高版本中，CoreDNS 是默认的 DNS 服务器。
   请注意，尽管已部署 DNS 服务器，但直到安装 CNI 时才调度它。

   {{< warning >}}
   从 v1.18 开始，在 kubeadm 中使用 kube-dns 的支持已被废弃，并已在 v1.21 版本中移除。
   {{< /warning >}}


### 在 kubeadm 中使用 init 阶段 {#init-phases}

Kubeadm 允许你使用 `kubeadm init phase` 命令分阶段创建控制平面节点。

要查看阶段和子阶段的有序列表，可以调用 `kubeadm init --help`。
该列表将位于帮助屏幕的顶部，每个阶段旁边都有一个描述。
注意，通过调用 `kubeadm init`，所有阶段和子阶段都将按照此确切顺序执行。

某些阶段具有唯一的标志，因此，如果要查看可用选项的列表，请添加 `--help`，例如：

```shell
sudo kubeadm init phase control-plane controller-manager --help
```

你也可以使用 `--help` 查看特定父阶段的子阶段列表：

```shell
sudo kubeadm init phase control-plane --help
```

`kubeadm init` 还公开了一个名为 `--skip-phases` 的参数，该参数可用于跳过某些阶段。
参数接受阶段名称列表，并且这些名称可以从上面的有序列表中获取。

例如：

```shell
sudo kubeadm init phase control-plane all --config=configfile.yaml
sudo kubeadm init phase etcd local --config=configfile.yaml
# 你现在可以修改控制平面和 etcd 清单文件
sudo kubeadm init --skip-phases=control-plane,etcd --config=configfile.yaml
```

该示例将执行的操作是基于 `configfile.yaml` 中的配置在 `/etc/kubernetes/manifests`
中写入控制平面和 etcd 的清单文件。
这允许你修改文件，然后使用 `--skip-phases` 跳过这些阶段。
通过调用最后一个命令，你将使用自定义清单文件创建一个控制平面节点。

{{< feature-state for_k8s_version="v1.22" state="beta" >}}

或者，你可以使用 `InitConfiguration` 下的 `skipPhases` 字段。

### 结合一份配置文件来使用 kubeadm init {#config-file}

{{< caution >}}
配置文件的功能仍然处于 beta 状态并且在将来的版本中可能会改变。
{{< /caution >}}

通过一份配置文件而不是使用命令行参数来配置 `kubeadm init` 命令是可能的，
但是一些更加高级的功能只能够通过配置文件设定。
这份配置文件通过 `--config` 选项参数指定的，
它必须包含 `ClusterConfiguration` 结构，并可能包含更多由 `---\n` 分隔的结构。
在某些情况下，可能不允许将 `--config` 与其他标志混合使用。

可以使用 [kubeadm config print](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-config/)
命令打印出默认配置。

如果你的配置没有使用最新版本，
**推荐**使用 [kubeadm config migrate](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-config/)
命令进行迁移。

关于配置的字段和用法的更多信息，你可以访问 [API 参考页面](/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/)。

### 使用 kubeadm init 时设置特性门控 {#feature-gates}

Kubeadm 支持一组独有的特性门控，只能在 `kubeadm init` 创建集群期间使用。
这些特性可以控制集群的行为。特性门控会在毕业到 GA 后被移除。

你可以使用 `--feature-gates` 标志来为 `kubeadm init` 设置特性门控，
或者你可以在用 `--config`
传递[配置文件](/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/#kubeadm-k8s-io-v1beta3-ClusterConfiguration)时添加条目到 `featureGates` 字段中。

直接传递 [Kubernetes 核心组件的特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates)给 kubeadm 是不支持的。
相反，可以通过[使用 kubeadm API 的自定义组件](/zh-cn/docs/setup/production-environment/tools/kubeadm/control-plane-flags/)来传递。

特性门控的列表：

{{< table caption="kubeadm 特性门控" >}}
特性 | 默认值 | Alpha | Beta | GA
:-------|:--------|:------|:-----|:----
`PublicKeysECDSA` | `false` | 1.19 | - | -
`RootlessControlPlane` | `false` | 1.22 | - | -
`UnversionedKubeletConfigMap` | `true` | 1.22 | 1.23 | 1.25
{{< /table >}}

{{< note >}}
一旦特性门控变成了 GA，它的值会被默认锁定为 `true`。
{{< /note >}}

特性门控的描述：

`PublicKeysECDSA`
: 可用于创建集群时使用 ECDSA 证书而不是默认 RSA 算法。
支持用 `kubeadm certs renew` 更新现有 ECDSA 证书，
但你不能在集群运行期间或升级期间切换 RSA 和 ECDSA 算法。

`RootlessControlPlane`
: 设置此标志来配置 kubeadm 所部署的控制平面组件中的静态 Pod 容器
`kube-apiserver`、`kube-controller-manager`、`kube-scheduler` 和 `etcd` 以非 root 用户身份运行。
如果未设置该标志，则这些组件以 root 身份运行。
你可以在升级到更新版本的 Kubernetes 之前更改此特性门控的值。

`UnversionedKubeletConfigMap`
: 此标志控制 kubeadm 存储 kubelet 配置数据的 {{<glossary_tooltip text="ConfigMap" term_id="configmap" >}} 的名称。
在未指定此标志或设置为 `true` 的情况下，此 ConfigMap 被命名为 `kubelet-config`。
如果将此标志设置为 `false`，则此 ConfigMap 的名称会包括 Kubernetes 的主要版本和次要版本（例如：`kubelet-config-{{< skew currentVersion >}}`）。
Kubeadm 会确保用于读写 ConfigMap 的 RBAC 规则适合你设置的值。
当 kubeadm 写入此 ConfigMap 时（在 `kubeadm init` 或 `kubeadm upgrade apply` 期间），
kubeadm 根据 `UnversionedKubeletConfigMap` 的设置值来执行操作。
当读取此 ConfigMap 时（在 `kubeadm join`、`kubeadm reset`、`kubeadm upgrade ...` 期间），
kubeadm 尝试首先使用无版本（后缀）的 ConfigMap 名称；
如果不成功，kubeadm 将回退到使用该 ConfigMap 的旧（带版本号的）名称。

### 添加 kube-proxy 参数 {#kube-proxy}

kubeadm 配置中有关 kube-proxy 的说明请查看：

- [kube-proxy 参考](/zh-cn/docs/reference/config-api/kube-proxy-config.v1alpha1/)

使用 kubeadm 启用 IPVS 模式的说明请查看：

- [IPVS](https://github.com/kubernetes/kubernetes/blob/master/pkg/proxy/ipvs/README.md)

### 向控制平面组件传递自定义的命令行参数 {#control-plane-flags}

有关向控制平面组件传递命令行参数的说明请查看：

- [控制平面命令行参数](/zh-cn/docs/setup/production-environment/tools/kubeadm/control-plane-flags/)

### 在没有互联网连接的情况下运行 kubeadm {#without-internet-connection}

要在没有互联网连接的情况下运行 kubeadm，你必须提前拉取所需的控制平面镜像。

你可以使用 `kubeadm config images` 子命令列出并拉取镜像：

```shell
kubeadm config images list
kubeadm config images pull
```

你可以通过 `--config` 把 [kubeadm 配置文件](#config-file) 传递给上述命令来控制
`kubernetesVersion` 和 `imageRepository` 字段。

kubeadm 需要的所有默认 `registry.k8s.io` 镜像都支持多种硬件体系结构。

### 使用自定义的镜像 {#custom-images}

默认情况下，kubeadm 会从 `registry.k8s.io` 仓库拉取镜像。如果请求的 Kubernetes 版本是 CI 标签
（例如 `ci/latest`），则使用 `gcr.io/k8s-staging-ci-images`。

你可以通过使用[带有配置文件的 kubeadm](#config-file) 来重写此操作。
允许的自定义功能有：

* 提供影响镜像版本的 `kubernetesVersion`。
* 使用其他的 `imageRepository` 来代替 `registry.k8s.io`。
* 为 etcd 或 CoreDNS 提供特定的 `imageRepository` 和 `imageTag`。

由于向后兼容的原因，使用 `imageRepository` 所指定的定制镜像库可能与默认的
`registry.k8s.io` 镜像路径不同。例如，某镜像的子路径可能是 `registry.k8s.io/subpath/image`，
但使用自定义仓库时默认为 `my.customrepository.io/image`。

确保将镜像推送到 kubeadm 可以使用的自定义仓库的路径中，你必须：

* 使用 `kubeadm config images {list|pull}` 从 `registry.k8s.io` 的默认路径中拉取镜像。
* 将镜像推送到 `kubeadm config images list --config=config.yaml` 的路径，
  其中 `config.yaml` 包含自定义的 `imageRepository` 和/或用于 etcd 和 CoreDNS 的 `imageTag`。
* 将相同的 `config.yaml` 传递给 `kubeadm init`。

#### 定制沙箱（pause）镜像  {#custom-pause-image}

如果需要为这些组件设置定制的镜像，
你需要在你的{{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}中完成一些配置。
参阅你的容器运行时的文档以了解如何改变此设置。
对于某些容器运行时而言，
你可以在[容器运行时](/zh-cn/docs/setup/production-environment/container-runtimes/)主题下找到一些建议。

### 将控制平面证书上传到集群  {#uploading-control-plane-certificates-to-the-cluster}

通过将参数 `--upload-certs` 添加到 `kubeadm init`，你可以将控制平面证书临时上传到集群中的 Secret。
请注意，此 Secret 将在 2 小时后自动过期。这些证书使用 32 字节密钥加密，可以使用 `--certificate-key` 指定该密钥。
通过将 `--control-plane` 和 `--certificate-key` 传递给 `kubeadm join`，
可以在添加其他控制平面节点时使用相同的密钥下载证书。

以下阶段命令可用于证书到期后重新上传证书：

```shell
kubeadm init phase upload-certs --upload-certs --config=SOME_YAML_FILE
```
{{< note >}}
在使用 `--config`
传递[配置文件](https://kubernetes.io/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/)时，
可以在 `InitConfiguration` 中提供预定义的 `certificateKey`。
{{< /note >}}

如果未将预定义的证书密钥传递给 `kubeadm init` 和 `kubeadm init phase upload-certs`，
则会自动生成一个新密钥。

以下命令可用于按需生成新密钥：

```shell
kubeadm certs certificate-key
```

### 使用 kubeadm 管理证书  {#certificate-management-with-kubeadm}

有关使用 kubeadm 进行证书管理的详细信息，
请参阅[使用 kubeadm 进行证书管理](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/)。
该文档包括有关使用外部 CA、自定义证书和证书续订的信息。

### 管理 kubeadm 为 kubelet 提供的 systemd 配置文件 {#kubelet-drop-in}

`kubeadm` 包自带了关于 `systemd` 如何运行 `kubelet` 的配置文件。
请注意 `kubeadm` 客户端命令行工具永远不会修改这份 `systemd` 配置文件。
这份 `systemd` 配置文件属于 kubeadm DEB/RPM 包。

有关更多信息，请阅读[管理 systemd 的 kubeadm 内嵌文件](/zh-cn/docs/setup/production-environment/tools/kubeadm/kubelet-integration/#the-kubelet-drop-in-file-for-systemd)。

### 结合 CRI 运行时使用 kubeadm   {#use-kubeadm-with-cri-runtimes}

默认情况下，kubeadm 尝试检测你的容器运行环境。有关此检测的更多详细信息，请参见
[kubeadm CRI 安装指南](/zh-cn/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#installing-runtime)。

### 设置节点的名称  {#setting-the-node-name}

默认情况下，`kubeadm` 基于机器的主机地址分配一个节点名称。你可以使用 `--node-name` 参数覆盖此设置。
此标识将合适的 [`--hostname-override`](/zh-cn/docs/reference/command-line-tools-reference/kubelet/#options)
值传递给 kubelet。

要注意，重载主机名可能会[与云驱动发生冲突](https://github.com/kubernetes/website/pull/8873)。

### kubeadm 自动化   {#automating-kubeadm}

除了像文档
[kubeadm 基础教程](/zh-cn/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)中所描述的那样，
将从 `kubeadm init` 取得的令牌复制到每个节点，你还可以并行地分发令牌以实现更简单的自动化。
要实现自动化，你必须知道控制平面节点启动后将拥有的 IP 地址，或使用 DNS 名称或负载均衡器的地址。

1. 生成一个令牌。这个令牌必须采用的格式为：`<6 个字符的字符串>.<16 个字符的字符串>`。
   更加正式的说法是，它必须符合正则表达式：`[a-z0-9]{6}\.[a-z0-9]{16}`。

   kubeadm 可以为你生成一个令牌：

   ```shell
   kubeadm token generate
   ```

2. 使用这个令牌同时启动控制平面节点和工作节点。这些节点一旦运行起来应该就会互相寻找对方并且形成集群。
   同样的 `--token` 参数可以同时用于 `kubeadm init` 和 `kubeadm join` 命令。

3. 当接入其他控制平面节点时，可以对 `--certificate-key` 执行类似的操作。可以使用以下方式生成密钥：

   ```shell
   kubeadm certs certificate-key
   ```

一旦集群启动起来，你就可以从控制平面节点的 `/etc/kubernetes/admin.conf` 文件获取管理凭证，
并使用这个凭证同集群通信。

注意这种搭建集群的方式在安全保证上会有一些宽松，因为这种方式不允许使用
`--discovery-token-ca-cert-hash` 来验证根 CA 的哈希值
（因为当配置节点的时候，它还没有被生成）。
更多信息请参阅 [kubeadm join](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-join/) 文档。

## {{% heading "whatsnext" %}}

* 进一步阅读了解 [kubeadm init 阶段](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/)
* [kubeadm join](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-join/)
  启动一个 Kubernetes 工作节点并且将其加入到集群
* [kubeadm upgrade](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-upgrade/)
  将 Kubernetes 集群升级到新版本
* [kubeadm reset](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-reset/)
  恢复 `kubeadm init` 或 `kubeadm join` 命令对节点所作的变更
