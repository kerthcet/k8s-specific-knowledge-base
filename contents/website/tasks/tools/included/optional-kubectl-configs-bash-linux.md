---
title: "Linux 系统中的 Bash 自动补全功能"
description: "Linux 系统中 Bash 自动补全功能的一些可选配置。"
headless: true
_build:
  list: never
  render: never
  publishResources: false
---

### 简介 {#introduction}

kubectl 的 Bash 补全脚本可以用命令 `kubectl completion bash` 生成。
在 Shell 中导入（Sourcing）补全脚本，将启用 kubectl 自动补全功能。

然而，补全脚本依赖于工具 [**bash-completion**](https://github.com/scop/bash-completion)，
所以要先安装它（可以用命令 `type _init_completion` 检查 bash-completion 是否已安装）。

### 安装 bash-completion {#install-bash-comletion}

很多包管理工具均支持 bash-completion（参见[这里](https://github.com/scop/bash-completion#installation)）。
可以通过 `apt-get install bash-completion` 或 `yum install bash-completion` 等命令来安装它。

上述命令将创建文件 `/usr/share/bash-completion/bash_completion`，它是 bash-completion 的主脚本。
依据包管理工具的实际情况，你需要在 `~/.bashrc` 文件中手工导入此文件。

要查看结果，请重新加载你的 Shell，并运行命令 `type _init_completion`。
如果命令执行成功，则设置完成，否则将下面内容添加到文件 `~/.bashrc` 中：

```bash
source /usr/share/bash-completion/bash_completion
```

重新加载 Shell，再输入命令 `type _init_completion` 来验证 bash-completion 的安装状态。

### 启动 kubectl 自动补全功能 {#enable-kubectl-autocompletion}

#### Bash

你现在需要确保一点：kubectl 补全脚本已经导入（sourced）到 Shell 会话中。
可以通过以下两种方法进行设置：

{{< tabs name="kubectl_bash_autocompletion" >}}
{{< tab name="当前用户" codelang="bash" >}}
echo 'source <(kubectl completion bash)' >>~/.bashrc
{{< /tab >}}
{{< tab name="系统全局" codelang="bash" >}}
kubectl completion bash | sudo tee /etc/bash_completion.d/kubectl > /dev/null
sudo chmod a+r /etc/bash_completion.d/kubectl
{{< /tab >}}
{{< /tabs >}}

如果 kubectl 有关联的别名，你可以扩展 Shell 补全来适配此别名：

```bash
echo 'alias k=kubectl' >>~/.bashrc
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc
```

{{< note >}}
bash-completion 负责导入 `/etc/bash_completion.d` 目录中的所有补全脚本。
{{< /note >}}

两种方式的效果相同。重新加载 Shell 后，kubectl 自动补全功能即可生效。
若要在当前 Shell 会话中启用 Bash 补全功能，源引 `~/.bashrc` 文件：

```bash
source ~/.bashrc
```
