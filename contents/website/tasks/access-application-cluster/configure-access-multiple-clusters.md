---
title: 配置对多集群的访问
content_type: task
weight: 30
card:
  name: tasks
  weight: 40
---


本文展示如何使用配置文件来配置对多个集群的访问。
在将集群、用户和上下文定义在一个或多个配置文件中之后，用户可以使用
`kubectl config use-context` 命令快速地在集群之间进行切换。

{{< note >}}
用于配置集群访问的文件有时被称为 **kubeconfig 文件**。
这是一种引用配置文件的通用方式，并不意味着存在一个名为 `kubeconfig` 的文件。
{{< /note >}}

{{< warning >}}
只使用来源可靠的 kubeconfig 文件。使用特制的 kubeconfig 文件可能会导致恶意代码执行或文件暴露。
如果必须使用不受信任的 kubeconfig 文件，请首先像检查 shell 脚本一样仔细检查它。
{{< /warning>}}

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

要检查 {{< glossary_tooltip text="kubectl" term_id="kubectl" >}} 是否安装，
执行 `kubectl version --client` 命令。kubectl 的版本应该与集群的 API
服务器[使用同一次版本号](/zh-cn/releases/version-skew-policy/#kubectl)。


## 定义集群、用户和上下文    {#define-clusters-users-and-contexts}

假设用户有两个集群，一个用于开发工作（development），一个用于测试工作（test）。
在 `development` 集群中，前端开发者在名为 `frontend` 的名字空间下工作，
存储开发者在名为 `storage` 的名字空间下工作。在 `test` 集群中，
开发人员可能在默认名字空间下工作，也可能视情况创建附加的名字空间。
访问开发集群需要通过证书进行认证。
访问测试集群需要通过用户名和密码进行认证。

创建名为 `config-exercise` 的目录。在
`config-exercise` 目录中，创建名为 `config-demo` 的文件，其内容为：

```yaml
apiVersion: v1
kind: Config
preferences: {}

clusters:
- cluster:
  name: development
- cluster:
  name: test

users:
- name: developer
- name: experimenter

contexts:
- context:
  name: dev-frontend
- context:
  name: dev-storage
- context:
  name: exp-test
```

配置文件描述了集群、用户名和上下文。`config-demo` 文件中含有描述两个集群、
两个用户和三个上下文的框架。

进入 `config-exercise` 目录。输入以下命令，将集群详细信息添加到配置文件中：

```shell
kubectl config --kubeconfig=config-demo set-cluster development --server=https://1.2.3.4 --certificate-authority=fake-ca-file
kubectl config --kubeconfig=config-demo set-cluster test --server=https://5.6.7.8 --insecure-skip-tls-verify
```

将用户详细信息添加到配置文件中：

{{< caution >}}
将密码保存到 Kubernetes 客户端配置中有风险。
一个较好的替代方式是使用凭据插件并单独保存这些凭据。
参阅 [client-go 凭据插件](/zh-cn/docs/reference/access-authn-authz/authentication/#client-go-credential-plugins)
{{< /caution >}}

```shell
kubectl config --kubeconfig=config-demo set-credentials developer --client-certificate=fake-cert-file --client-key=fake-key-seefile
kubectl config --kubeconfig=config-demo set-credentials experimenter --username=exp --password=some-password
```

{{< note >}}
- 要删除用户，可以运行 `kubectl --kubeconfig=config-demo config unset users.<name>`
- 要删除集群，可以运行 `kubectl --kubeconfig=config-demo config unset clusters.<name>`
- 要删除上下文，可以运行 `kubectl --kubeconfig=config-demo config unset contexts.<name>`
{{< /note >}}

将上下文详细信息添加到配置文件中：

```shell
kubectl config --kubeconfig=config-demo set-context dev-frontend --cluster=development --namespace=frontend --user=developer
kubectl config --kubeconfig=config-demo set-context dev-storage --cluster=development --namespace=storage --user=developer
kubectl config --kubeconfig=config-demo set-context exp-test --cluster=test --namespace=default --user=experimenter
```

打开 `config-demo` 文件查看添加的详细信息。也可以使用 `config view`
命令进行查看：

```shell
kubectl config --kubeconfig=config-demo view
```

输出展示了两个集群、两个用户和三个上下文：

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority: fake-ca-file
    server: https://1.2.3.4
  name: development
- cluster:
    insecure-skip-tls-verify: true
    server: https://5.6.7.8
  name: test
contexts:
- context:
    cluster: development
    namespace: frontend
    user: developer
  name: dev-frontend
- context:
    cluster: development
    namespace: storage
    user: developer
  name: dev-storage
- context:
    cluster: test
    namespace: default
    user: experimenter
  name: exp-test
current-context: ""
kind: Config
preferences: {}
users:
- name: developer
  user:
    client-certificate: fake-cert-file
    client-key: fake-key-file
- name: experimenter
  user:
    # 文档说明（本注释不属于命令输出）。
    # 将密码保存到 Kubernetes 客户端配置有风险。
    # 一个较好的替代方式是使用凭据插件并单独保存这些凭据。
    # 参阅 https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/authentication/#client-go-credential-plugins
    password: some-password
    username: exp
```

其中的 `fake-ca-file`、`fake-cert-file` 和 `fake-key-file` 是证书文件路径名的占位符。
你需要更改这些值，使之对应你的环境中证书文件的实际路径名。

有时你可能希望在这里使用 BASE64 编码的数据而不是一个个独立的证书文件。
如果是这样，你需要在键名上添加 `-data` 后缀。例如，
`certificate-authority-data`、`client-certificate-data` 和 `client-key-data`。

每个上下文包含三部分（集群、用户和名字空间），例如，
`dev-frontend` 上下文表明：使用 `developer` 用户的凭证来访问 `development` 集群的
`frontend` 名字空间。

设置当前上下文：

```shell
kubectl config --kubeconfig=config-demo use-context dev-frontend
```

现在当输入 `kubectl` 命令时，相应动作会应用于 `dev-frontend` 上下文中所列的集群和名字空间，
同时，命令会使用 `dev-frontend` 上下文中所列用户的凭证。

使用 `--minify` 参数，来查看与当前上下文相关联的配置信息。

```shell
kubectl config --kubeconfig=config-demo view --minify
```

输出结果展示了 `dev-frontend` 上下文相关的配置信息：

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority: fake-ca-file
    server: https://1.2.3.4
  name: development
contexts:
- context:
    cluster: development
    namespace: frontend
    user: developer
  name: dev-frontend
current-context: dev-frontend
kind: Config
preferences: {}
users:
- name: developer
  user:
    client-certificate: fake-cert-file
    client-key: fake-key-file
```

现在假设用户希望在测试集群中工作一段时间。

将当前上下文更改为 `exp-test`：

```shell
kubectl config --kubeconfig=config-demo use-context exp-test
```

现在你发出的所有 `kubectl` 命令都将应用于 `test` 集群的默认名字空间。
同时，命令会使用 `exp-test` 上下文中所列用户的凭证。

查看更新后的当前上下文 `exp-test` 相关的配置：

```shell
kubectl config --kubeconfig=config-demo view --minify
```

最后，假设用户希望在 `development` 集群中的 `storage` 名字空间下工作一段时间。

将当前上下文更改为 `dev-storage`：

```shell
kubectl config --kubeconfig=config-demo use-context dev-storage
```

查看更新后的当前上下文 `dev-storage` 相关的配置：

```shell
kubectl config --kubeconfig=config-demo view --minify
```

## 创建第二个配置文件    {#create-a-second-configuration-file}

在 `config-exercise` 目录中，创建名为 `config-demo-2` 的文件，其中包含以下内容：

```yaml
apiVersion: v1
kind: Config
preferences: {}

contexts:
- context:
    cluster: development
    namespace: ramp
    user: developer
  name: dev-ramp-up
```

上述配置文件定义了一个新的上下文，名为 `dev-ramp-up`。

## 设置 KUBECONFIG 环境变量    {#set-the-kubeconfig-environment-variable}

查看是否有名为 `KUBECONFIG` 的环境变量。
如有，保存 `KUBECONFIG` 环境变量当前的值，以便稍后恢复。
例如：

### Linux

```shell
export KUBECONFIG_SAVED="$KUBECONFIG"
```

### Windows PowerShell

```powershell
$Env:KUBECONFIG_SAVED=$ENV:KUBECONFIG
```

`KUBECONFIG` 环境变量是配置文件路径的列表，该列表在 Linux 和 Mac 中以冒号分隔，
在 Windows 中以分号分隔。
如果有 `KUBECONFIG` 环境变量，请熟悉列表中的配置文件。

临时添加两条路径到 `KUBECONFIG` 环境变量中。例如：

### Linux

```shell
export KUBECONFIG="${KUBECONFIG}:config-demo:config-demo-2"
```

### Windows PowerShell

```powershell
$Env:KUBECONFIG=("config-demo;config-demo-2")
```

在 `config-exercise` 目录中输入以下命令：

```shell
kubectl config view
```

输出展示了 `KUBECONFIG` 环境变量中所列举的所有文件合并后的信息。
特别地，注意合并信息中包含来自 `config-demo-2` 文件的 `dev-ramp-up` 上下文和来自
`config-demo` 文件的三个上下文：

```yaml
contexts:
- context:
    cluster: development
    namespace: frontend
    user: developer
  name: dev-frontend
- context:
    cluster: development
    namespace: ramp
    user: developer
  name: dev-ramp-up
- context:
    cluster: development
    namespace: storage
    user: developer
  name: dev-storage
- context:
    cluster: test
    namespace: default
    user: experimenter
  name: exp-test
```

关于 kubeconfig 文件如何合并的更多信息，
请参考[使用 kubeconfig 文件组织集群访问](/zh-cn/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

## 探索 $HOME/.kube 目录    {#explore-the-home-kube-directory}

如果用户已经拥有一个集群，可以使用 `kubectl` 与集群进行交互，
那么很可能在 `$HOME/.kube` 目录下有一个名为 `config` 的文件。

进入 `$HOME/.kube` 目录，看看那里有什么文件。通常会有一个名为
`config` 的文件，目录中可能还有其他配置文件。请简单地熟悉这些文件的内容。

## 将 $HOME/.kube/config 追加到 KUBECONFIG 环境变量中    {#append-home-kube-config-to-your-kubeconfig-environment-variable}

如果有 `$HOME/.kube/config` 文件，并且还未列在 `KUBECONFIG` 环境变量中，
那么现在将它追加到 `KUBECONFIG` 环境变量中。例如：

### Linux

```shell
export KUBECONFIG="${KUBECONFIG}:${HOME}/.kube/config"
```

### Windows Powershell

```powershell
$Env:KUBECONFIG="$Env:KUBECONFIG;$HOME\.kube\config"
```

在配置练习目录中输入以下命令，查看当前 `KUBECONFIG` 环境变量中列举的所有文件合并后的配置信息：

```shell
kubectl config view
```

## 清理    {#clean-up}

将 `KUBECONFIG` 环境变量还原为原始值。例如：

### Linux

```shell
export KUBECONFIG="$KUBECONFIG_SAVED"
```

### Windows PowerShell

```powershell
$Env:KUBECONFIG=$ENV:KUBECONFIG_SAVED
```

## 检查 kubeconfig 所表示的主体   {#check-the-subject}

你在通过集群的身份验证后将获得哪些属性（用户名、组），这一点并不总是很明显。
如果你同时管理多个集群，这可能会更具挑战性。

对于你所选择的 Kubernetes 客户端上下文，有一个 `kubectl` 子命令可以检查用户名等主体属性：
`kubectl alpha auth whoami`。

更多细节请参阅[通过 API 访问客户端的身份验证信息](/zh-cn/docs/reference/access-authn-authz/authentication/#self-subject-review)。

## {{% heading "whatsnext" %}}

* [使用 kubeconfig 文件组织集群访问](/zh-cn/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
* [kubectl config](/docs/reference/generated/kubectl/kubectl-commands#config)

