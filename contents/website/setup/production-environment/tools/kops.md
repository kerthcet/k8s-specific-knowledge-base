---
title: 使用 kOps 安装 Kubernetes
content_type: task
weight: 20
---



本篇快速入门介绍了如何在 AWS 上轻松安装 Kubernetes 集群。
本篇使用了一个名为 [`kOps`](https://github.com/kubernetes/kops) 的工具。

`kOps` 是一个自动化的制备系统：

* 全自动安装流程
* 使用 DNS 识别集群
* 自我修复：一切都在自动扩缩组中运行
* 支持多种操作系统（Amazon Linux、Debian、Flatcar、RHEL、Rocky 和 Ubuntu），
  参考 [images.md](https://github.com/kubernetes/kops/blob/master/docs/operations/images.md)。
* 支持高可用，参考 [high_availability.md](https://github.com/kubernetes/kops/blob/master/docs/operations/high_availability.md)。
* 可以直接提供或者生成 terraform 清单，参考 [terraform.md](https://github.com/kubernetes/kops/blob/master/docs/terraform.md)。

## {{% heading "prerequisites" %}}

* 你必须安装 [kubectl](/zh-cn/docs/tasks/tools/)。
* 你必须安装[安装](https://github.com/kubernetes/kops#installing) `kops`
  到 64 位的（AMD64 和 Intel 64）设备架构上。
* 你必须拥有一个 [AWS 账户](https://docs.aws.amazon.com/zh_cn/polly/latest/dg/setting-up.html)，
  生成 [IAM 秘钥](https://docs.aws.amazon.com/zh_cn/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys)
  并[配置](https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration)
  该秘钥。IAM 用户需要[足够的权限许可](https://github.com/kubernetes/kops/blob/master/docs/getting_started/aws.md#setup-iam-user)。


## 创建集群 {#creating-a-cluster}

### (1/5) 安装 kops

#### 安装

从[下载页面](https://github.com/kubernetes/kops/releases)下载 kops
（从源代码构建也很方便）：

{{< tabs name="kops_installation" >}}
{{% tab name="macOS" %}}

使用下面的命令下载最新发布版本：

```shell
curl -LO https://github.com/kubernetes/kops/releases/download/$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)/kops-darwin-amd64
```

要下载特定版本，使用特定的 kops 版本替换下面命令中的部分：

```shell
$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)
```

例如，要下载 kops v1.20.0，输入：

```shell
curl -LO https://github.com/kubernetes/kops/releases/download/v1.20.0/kops-darwin-amd64
```

令 kops 二进制文件可执行：

```shell
chmod +x kops-darwin-amd64
```

将 kops 二进制文件移到你的 PATH 下：

```shell
sudo mv kops-darwin-amd64 /usr/local/bin/kops
```

你也可以使用 [Homebrew](https://brew.sh/) 安装 kops：

```shell
brew update && brew install kops
```
{{% /tab %}}
{{% tab name="Linux" %}}

使用命令下载最新发布版本：

```shell
curl -LO https://github.com/kubernetes/kops/releases/download/$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)/kops-linux-amd64
```

要下载 kops 的特定版本，用特定的 kops 版本替换下面命令中的部分：

```shell
$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)
```

例如，要下载 kops v1.20 版本，输入：

```shell
curl -LO https://github.com/kubernetes/kops/releases/download/v1.20.0/kops-linux-amd64
```

令 kops 二进制文件可执行：

```shell
chmod +x kops-linux-amd64
```

将 kops 二进制文件移到 PATH 下：

```shell
sudo mv kops-linux-amd64 /usr/local/bin/kops
```

你也可以使用 [Homebrew](https://docs.brew.sh/Homebrew-on-Linux) 来安装 kops。

```shell
brew update && brew install kops
```

{{% /tab %}}
{{< /tabs >}}

### (2/5) 为你的集群创建一个 route53 域名

kops 在集群内部和外部都使用 DNS 进行发现操作，这样你可以从客户端访问
kubernetes API 服务器。

kops 对集群名称有明显的要求：它应该是有效的 DNS 名称。这样一来，你就不会再使集群混乱，
可以与同事明确共享集群，并且无需依赖记住 IP 地址即可访问集群。

你可以，或许应该使用子域名来划分集群。作为示例，我们将使用域名 `useast1.dev.example.com`。
这样，API 服务器端点域名将为 `api.useast1.dev.example.com`。

Route53 托管区域可以服务子域名。你的托管区域可能是 `useast1.dev.example.com`，还有 `dev.example.com` 甚至 `example.com`。
kops 可以与以上任何一种配合使用，因此通常你出于组织原因选择不同的托管区域。
例如，允许你在 `dev.example.com` 下创建记录，但不能在 `example.com` 下创建记录。

假设你使用 `dev.example.com` 作为托管区域。你可以使用
[正常流程](https://docs.aws.amazon.com/zh_cn/Route53/latest/DeveloperGuide/CreatingNewSubdomain.html)
或者使用诸如 `aws route53 create-hosted-zone --name dev.example.com --caller-reference 1`
之类的命令来创建该托管区域。

然后，你必须在父域名中设置你的 DNS 记录，以便该域名中的记录可以被解析。
在这里，你将在 `example.com` 中为 `dev` 创建 DNS 记录。
如果它是根域名，则可以在域名注册机构配置 DNS 记录。
例如，你需要在购买 `example.com` 的地方配置 `example.com`。

检查你的 route53 域已经被正确设置（这是导致问题的最常见原因！）。
如果你安装了 dig 工具，则可以通过运行以下步骤再次检查集群是否配置正确：

`dig NS dev.example.com`

你应该看到 Route53 分配了你的托管区域的 4 条 DNS 记录。

### (3/5) 创建一个 S3 存储桶来存储集群状态

kops 使你即使在安装后也可以管理集群。为此，它必须跟踪已创建的集群及其配置、所使用的密钥等。
此信息存储在 S3 存储桶中。S3 权限用于控制对存储桶的访问。

多个集群可以使用同一 S3 存储桶，并且你可以在管理同一集群的同事之间共享一个
S3 存储桶 - 这比传递 kubecfg 文件容易得多。
但是有权访问 S3 存储桶的任何人都将拥有对所有集群的管理访问权限，
因此你不想在运营团队之外共享它。

因此，通常每个运维团队都有一个 S3 存储桶（而且名称通常对应于上面托管区域的名称！）

在我们的示例中，我们选择 `dev.example.com` 作为托管区域，因此我们选择
`clusters.dev.example.com` 作为 S3 存储桶名称。

* 导出 `AWS_PROFILE` 文件（如果你需要选择一个配置文件用来使 AWS CLI 正常工作）
* 使用 `aws s3 mb s3://clusters.dev.example.com` 创建 S3 存储桶
* 你可以进行 `export KOPS_STATE_STORE=s3://clusters.dev.example.com` 操作，
  然后 kops 将默认使用此位置。
  我们建议将其放入你的 bash profile 文件或类似文件中。

### (4/5) 建立你的集群配置

运行 `kops create cluster` 以创建你的集群配置：

`kops create cluster --zones=us-east-1c useast1.dev.example.com`

kops 将为你的集群创建配置。请注意，它**仅**创建配置，实际上并没有创建云资源。
你将在下一步中使用 `kops update cluster` 进行创建。
这使你有机会查看配置或进行更改。

它打印出可用于进一步探索的命令：

* 使用以下命令列出集群：`kops get cluster`
* 使用以下命令编辑该集群：`kops edit cluster useast1.dev.example.com`
* 使用以下命令编辑你的节点实例组：`kops edit ig --name = useast1.dev.example.com nodes`
* 使用以下命令编辑你的主实例组：`kops edit ig --name = useast1.dev.example.com master-us-east-1c`

如果这是你第一次使用 kops，请花几分钟尝试一下！实例组是一组实例，将被注册为 Kubernetes 节点。
在 AWS 上，这是通过 auto-scaling-groups 实现的。你可以有多个实例组。
例如，你可能想要混合了 Spot 实例和按需实例的节点，或者混合了 GPU 实例和非 GPU 实例的节点。

### (5/5) 在 AWS 中创建集群

运行 `kops update cluster` 以在 AWS 中创建集群：

`kops update cluster useast1.dev.example.com --yes`

这需要几秒钟的时间才能运行，但实际上集群可能需要几分钟才能准备就绪。
每当更改集群配置时，都会使用 `kops update cluster` 工具。
它将在集群中应用你对配置进行的更改，根据需要重新配置 AWS 或者 Kubernetes。

例如，在你运行 `kops edit ig nodes` 之后，然后运行 `kops update cluster --yes`
应用你的配置，有时你还必须运行 `kops rolling-update cluster` 立即回滚更新配置。

如果没有 `--yes` 参数，`kops update cluster` 操作将向你显示其操作的预览效果。这对于生产集群很方便！

### 探索其他附加组件

请参阅[附加组件列表](/zh-cn/docs/concepts/cluster-administration/addons/)探索其他附加组件，
包括用于 Kubernetes 集群的日志记录、监视、网络策略、可视化和控制的工具。

## 清理 {#cleanup}

* 删除集群：`kops delete cluster useast1.dev.example.com --yes`

## {{% heading "whatsnext" %}}

* 了解有关 Kubernetes 的[概念](/zh-cn/docs/concepts/)和
  [`kubectl`](/zh-cn/docs/reference/kubectl/) 的更多信息。
* 参阅 `kOps` [进阶用法](https://kops.sigs.k8s.io/) 获取教程、最佳实践和进阶配置选项。
* 通过 Slack：[社区讨论](https://github.com/kubernetes/kops#other-ways-to-communicate-with-the-contributors)
  参与 `kOps` 社区讨论。
* 通过解决或提出一个 [GitHub Issue](https://github.com/kubernetes/kops/issues) 来为 `kOps` 做贡献。
