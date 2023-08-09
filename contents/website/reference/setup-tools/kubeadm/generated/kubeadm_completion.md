
为指定 Shell（Bash 或 Zsh） 输出 Shell 补全代码


### 概要


为指定的 shell（bash 或 zsh）输出 shell 自动补全代码。
必须激活 shell 代码以提供交互式 kubeadm 命令补全。这可以通过加载 .bash_profile 文件完成。


注意: 此功能依赖于 `bash-completion` 框架。


在 Mac 上使用 homebrew 安装:

```
brew install bash-completion
```

安装后，必须激活 bash_completion。这可以通过在 .bash_profile 文件中添加下面的命令行来完成

```
source $(brew --prefix)/etc/bash_completion
```


如果在 Linux 上没有安装 bash-completion，请通过你的发行版的包管理器安装 `bash-completion` 软件包。


zsh 用户注意事项：[1] zsh 自动补全仅在 &gt;=v5.2 及以上版本中支持。

```
kubeadm completion SHELL [flags]
```


### 示例


```
# 在 Mac 上使用 homebrew 安装 bash completion
brew install bash-completion
printf "\n# Bash completion support\nsource $(brew --prefix)/etc/bash_completion\n" >> $HOME/.bash_profile
source $HOME/.bash_profile

# 将 bash 版本的 kubeadm 自动补全代码加载到当前 shell 中
source <(kubeadm completion bash)

# 将 bash 自动补全完成代码写入文件并且从 .bash_profile 文件加载它
printf "\n# Kubeadm shell completion\nsource '$HOME/.kube/kubeadm_completion.bash.inc'\n" >> $HOME/.bash_profile
source $HOME/.bash_profile

# 将 zsh 版本的 kubeadm 自动补全代码加载到当前 shell 中
source <(kubeadm completion zsh)
```


### 选项

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
completion 操作的帮助命令
</p>
</td>
</tr>

</tbody>
</table>


### 从父命令继承的选项

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--rootfs string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
[实验] 到 '真实' 主机根文件系统的路径。
</p>
</td>
</tr>

</tbody>
</table>

