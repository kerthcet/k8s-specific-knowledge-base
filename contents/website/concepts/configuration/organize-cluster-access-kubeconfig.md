---
title: 使用 kubeconfig 文件组织集群访问
content_type: concept
weight: 60
---


使用 kubeconfig 文件来组织有关集群、用户、命名空间和身份认证机制的信息。
`kubectl` 命令行工具使用 kubeconfig 文件来查找选择集群所需的信息，并与集群的 API 服务器进行通信。

{{< note >}}
用于配置集群访问的文件称为 **kubeconfig 文件**。
这是引用到配置文件的通用方法，并不意味着有一个名为 `kubeconfig` 的文件。
{{< /note >}}

{{< warning >}}
请务必仅使用来源可靠的 kubeconfig 文件。使用特制的 kubeconfig 文件可能会导致恶意代码执行或文件暴露。
如果必须使用不受信任的 kubeconfig 文件，请首先像检查 Shell 脚本一样仔细检查此文件。
{{< /warning>}}

默认情况下，`kubectl` 在 `$HOME/.kube` 目录下查找名为 `config` 的文件。
你可以通过设置 `KUBECONFIG` 环境变量或者设置
[`--kubeconfig`](/docs/reference/generated/kubectl/kubectl/)参数来指定其他 kubeconfig 文件。

有关创建和指定 kubeconfig 文件的分步说明，
请参阅[配置对多集群的访问](/zh-cn/docs/tasks/access-application-cluster/configure-access-multiple-clusters)。


## 支持多集群、用户和身份认证机制   {#support-clusters-users-and-authn}

假设你有多个集群，并且你的用户和组件以多种方式进行身份认证。比如：

- 正在运行的 kubelet 可能使用证书在进行认证。
- 用户可能通过令牌进行认证。
- 管理员可能拥有多个证书集合提供给各用户。

使用 kubeconfig 文件，你可以组织集群、用户和命名空间。你还可以定义上下文，以便在集群和命名空间之间快速轻松地切换。

## 上下文（Context）   {#context}

通过 kubeconfig 文件中的 *context* 元素，使用简便的名称来对访问参数进行分组。
每个 context 都有三个参数：cluster、namespace 和 user。
默认情况下，`kubectl` 命令行工具使用 **当前上下文** 中的参数与集群进行通信。

选择当前上下文：

```shell
kubectl config use-context
```

## KUBECONFIG 环境变量   {#kubeconfig-env-var}

`KUBECONFIG` 环境变量包含一个 kubeconfig 文件列表。
对于 Linux 和 Mac，此列表以英文冒号分隔。对于 Windows，此列表以英文分号分隔。
`KUBECONFIG` 环境变量不是必需的。
如果 `KUBECONFIG` 环境变量不存在，`kubectl` 将使用默认的 kubeconfig 文件：`$HOME/.kube/config`。

如果 `KUBECONFIG` 环境变量存在，`kubectl` 将使用 `KUBECONFIG` 环境变量中列举的文件合并后的有效配置。

## 合并 kubeconfig 文件   {#merge-kubeconfig-files}

要查看配置，输入以下命令：

```shell
kubectl config view
```

如前所述，输出可能来自单个 kubeconfig 文件，也可能是合并多个 kubeconfig 文件的结果。

以下是 `kubectl` 在合并 kubeconfig 文件时使用的规则。

1. 如果设置了 `--kubeconfig` 参数，则仅使用指定的文件。不进行合并。此参数只能使用一次。

   否则，如果设置了 `KUBECONFIG` 环境变量，将它用作应合并的文件列表。根据以下规则合并 `KUBECONFIG` 环境变量中列出的文件：

   * 忽略空文件名。
   * 对于内容无法反序列化的文件，产生错误信息。
   * 第一个设置特定值或者映射键的文件将生效。
   * 永远不会更改值或者映射键。示例：保留第一个文件的上下文以设置 `current-context`。
     示例：如果两个文件都指定了 `red-user`，则仅使用第一个文件的 `red-user` 中的值。
     即使第二个文件在 `red-user` 下有非冲突条目，也要丢弃它们。

   有关设置 `KUBECONFIG` 环境变量的示例，
   请参阅[设置 KUBECONFIG 环境变量](/zh-cn/docs/tasks/access-application-cluster/configure-access-multiple-clusters/#set-the-kubeconfig-environment-variable)。

   否则，使用默认的 kubeconfig 文件（`$HOME/.kube/config`），不进行合并。

2. 根据此链中的第一个匹配确定要使用的上下文。

    1. 如果存在上下文，则使用 `--context` 命令行参数。
    2. 使用合并的 kubeconfig 文件中的 `current-context`。

   这种场景下允许空上下文。

3. 确定集群和用户。此时，可能有也可能没有上下文。根据此链中的第一个匹配确定集群和用户，
   这将运行两次：一次用于用户，一次用于集群。

   1. 如果存在用户或集群，则使用命令行参数：`--user` 或者 `--cluster`。
   2. 如果上下文非空，则从上下文中获取用户或集群。

   这种场景下用户和集群可以为空。

4. 确定要使用的实际集群信息。此时，可能有也可能没有集群信息。
   基于此链构建每个集群信息；第一个匹配项会被采用：

   1. 如果存在集群信息，则使用命令行参数：`--server`、`--certificate-authority` 和 `--insecure-skip-tls-verify`。
   2. 如果合并的 kubeconfig 文件中存在集群信息属性，则使用这些属性。
   3. 如果没有 server 配置，则配置无效。

5. 确定要使用的实际用户信息。使用与集群信息相同的规则构建用户信息，但对于每个用户只允许使用一种身份认证技术：

   1. 如果存在用户信息，则使用命令行参数：`--client-certificate`、`--client-key`、`--username`、`--password` 和 `--token`。
   2. 使用合并的 kubeconfig 文件中的 `user` 字段。
   3. 如果存在两种冲突技术，则配置无效。

6. 对于仍然缺失的任何信息，使用其对应的默认值，并可能提示输入身份认证信息。

## 文件引用   {#file-reference}

kubeconfig 文件中的文件和路径引用是相对于 kubeconfig 文件的位置。
命令行上的文件引用是相对于当前工作目录的。
在 `$HOME/.kube/config` 中，相对路径按相对路径存储，而绝对路径按绝对路径存储。

## 代理   {#proxy}

你可以在 `kubeconfig` 文件中，为每个集群配置 `proxy-url` 来让 `kubectl` 使用代理，例如：

```yaml
apiVersion: v1
kind: Config

clusters:
- cluster:
    proxy-url: http://proxy.example.org:3128
    server: https://k8s.example.org/k8s/clusters/c-xxyyzz
  name: development

users:
- name: developer

contexts:
- context:
  name: development
```

## {{% heading "whatsnext" %}}

* [配置对多集群的访问](/zh-cn/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)
* [`kubectl config`](/docs/reference/generated/kubectl/kubectl-commands#config)
