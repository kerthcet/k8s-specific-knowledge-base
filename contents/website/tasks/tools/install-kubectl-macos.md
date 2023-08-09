---
title: 在 macOS 系统上安装和设置 kubectl
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: 在 macOS 系统上安装 kubectl
---

## {{% heading "prerequisites" %}}

kubectl 版本和集群之间的差异必须在一个小版本号之内。
例如：v{{< skew currentVersion >}} 版本的客户端能与 v{{< skew currentVersionAddMinor -1 >}}、
v{{< skew currentVersionAddMinor 0 >}} 和 v{{< skew currentVersionAddMinor 1 >}} 版本的控制面通信。
用最新兼容版本的 kubectl 有助于避免不可预见的问题。

## 在 macOS 系统上安装 kubectl {#install-kubectl-on-macos}

在 macOS 系统上安装 kubectl 有如下方法：

- [在 macOS 系统上安装 kubectl](#install-kubectl-on-macos)
  - [用 curl 在 macOS 系统上安装 kubectl](#install-kubectl-binary-with-curl-on-macos)
  - [用 Homebrew 在 macOS 系统上安装](#install-with-homebrew-on-macos)
  - [用 Macports 在 macOS 系统上安装](#install-with-macports-on-macos)
- [验证 kubectl 配置](#verify-kubectl-configuration)
- [可选的 kubectl 配置和插件](#optional-kubectl-configurations-and-plugins)
  - [启用 shell 自动补全功能](#enable-shell-autocompletion)
  - [安装 `kubectl convert` 插件](#install-kubectl-convert-plugin)

### 用 curl 在 macOS 系统上安装 kubectl {#install-kubectl-binary-with-curl-on-macos}

1. 下载最新的发行版：

   {{< tabs name="download_binary_macos" >}}
   {{< tab name="Intel" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
   {{< /tab >}}
   {{< tab name="Apple Silicon" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
   {{< /tab >}}
   {{< /tabs >}}

   {{< note >}}
   如果需要下载某个指定的版本，用该指定版本号替换掉命令的这个部分：`$(curl -L -s https://dl.k8s.io/release/stable.txt)`。
   例如：要为 Intel macOS 系统下载 {{< skew currentPatchVersion >}} 版本，则输入：

   ```bash
   curl -LO "https://dl.k8s.io/release/v{{< skew currentPatchVersion >}}/bin/darwin/amd64/kubectl"
   ```

   对于 Apple Silicon 版本的 macOS，输入：

   ```bash
   curl -LO "https://dl.k8s.io/release/v{{< skew currentPatchVersion >}}/bin/darwin/arm64/kubectl"
   ```
   {{< /note >}}

2. 验证可执行文件（可选操作）

   下载 kubectl 的校验和文件：

   {{< tabs name="download_checksum_macos" >}}
   {{< tab name="Intel" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl.sha256"
   {{< /tab >}}
   {{< tab name="Apple Silicon" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl.sha256"
   {{< /tab >}}
   {{< /tabs >}}

   根据校验和文件，验证 kubectl：

   ```bash
   echo "$(cat kubectl.sha256)  kubectl" | shasum -a 256 --check
   ```

   验证通过时，输出如下：

   ```console
   kubectl: OK
   ```

   验证失败时，`shasum` 将以非零值退出，并打印如下输出：

   ```console
   kubectl: FAILED
   shasum: WARNING: 1 computed checksum did NOT match
   ```

   {{< note >}}
   下载的 kubectl 与校验和文件版本要相同。
   {{< /note >}}

3. 将 kubectl 置为可执行文件：

   ```bash
   chmod +x ./kubectl
   ```

4. 将可执行文件 kubectl 移动到系统可寻址路径 `PATH` 内的一个位置：

   ```bash
   sudo mv ./kubectl /usr/local/bin/kubectl
   sudo chown root: /usr/local/bin/kubectl
   ```

   {{< note >}}
   确保 `/usr/local/bin` 在你的 PATH 环境变量中。
   {{< /note >}}

5. 测试一下，确保你安装的是最新的版本：

   ```bash
   kubectl version --client
   ```

   {{< note >}}
   上面的命令会产生一个警告：

   ```
   WARNING: This version information is deprecated and will be replaced with the output from kubectl version --short.
   ```
   
   你可以忽略这个警告。你只检查你所安装的 `kubectl` 的版本。
   {{< /note >}}

   或者使用下面命令来查看版本的详细信息：

   ```cmd
   kubectl version --client --output=yaml
   ```

1. 安装插件后，清理安装文件：

   ```bash
   rm kubectl kubectl.sha256
   ```
### 用 Homebrew 在 macOS 系统上安装 {#install-with-homebrew-on-macos}

如果你是 macOS 系统，且用的是 [Homebrew](https://brew.sh/) 包管理工具，
则可以用 Homebrew 安装 kubectl。

1. 运行安装命令：

   ```bash
   brew install kubectl
   ```

   或

   ```bash
   brew install kubernetes-cli
   ```

2. 测试一下，确保你安装的是最新的版本：

   ```bash
   kubectl version --client
   ```

### 用 Macports 在 macOS 系统上安装 {#install-with-macports-on-macos}

如果你用的是 macOS，且用 [Macports](https://macports.org/) 包管理工具，则你可以用 Macports 安装 kubectl。

1. 运行安装命令：

   ```bash
   sudo port selfupdate
   sudo port install kubectl
   ```

2. 测试一下，确保你安装的是最新的版本：

   ```bash
   kubectl version --client
   ```

## 验证 kubectl 配置 {#verify-kubectl-configuration}

{{< include "included/verify-kubectl.md" >}}

## 可选的 kubectl 配置和插件 {#optional-kubectl-configurations-and-plugins}

### 启用 shell 自动补全功能 {#enable-shell-autocompletion}

kubectl 为 Bash、Zsh、Fish 和 PowerShell 提供自动补全功能，可以为你节省大量的输入。

下面是为 Bash、Fish 和 Zsh 设置自动补全功能的操作步骤。

{{< tabs name="kubectl_autocompletion" >}}
{{< tab name="Bash" include="included/optional-kubectl-configs-bash-mac.md" />}}
{{< tab name="Fish" include="included/optional-kubectl-configs-fish.md" />}}
{{< tab name="Zsh" include="included/optional-kubectl-configs-zsh.md" />}}
{{< /tabs >}}

### 安装 `kubectl convert` 插件   {#install-kubectl-convert-plugin}

{{< include "included/kubectl-convert-overview.md" >}}

1. 用以下命令下载最新发行版：

   {{< tabs name="download_convert_binary_macos" >}}
   {{< tab name="Intel" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl-convert"
   {{< /tab >}}
   {{< tab name="Apple Silicon" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl-convert"
   {{< /tab >}}
   {{< /tabs >}}

2. 验证该可执行文件（可选步骤）

   下载 kubectl-convert 校验和文件：

   {{< tabs name="download_convert_checksum_macos" >}}
   {{< tab name="Intel" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl-convert.sha256"
   {{< /tab >}}
   {{< tab name="Apple Silicon" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl-convert.sha256"
   {{< /tab >}}
   {{< /tabs >}}

   基于校验和，验证 kubectl-convert 的可执行文件：

   ```bash
   echo "$(cat kubectl-convert.sha256)  kubectl-convert" | shasum -a 256 --check
   ```

   验证通过时，输出为：

   ```console
   kubectl-convert: OK
   ```

   验证失败时，`sha256` 将以非零值退出，并打印输出类似于：

   ```console
   kubectl-convert: FAILED
   shasum: WARNING: 1 computed checksum did NOT match
   ```

   {{< note >}}
   下载相同版本的可执行文件和校验和。
   {{< /note >}}

3. 使 kubectl-convert 二进制文件可执行

   ```bash
   chmod +x ./kubectl-convert
   ```

4. 将 kubectl-convert 可执行文件移动到系统 `PATH` 环境变量中的一个位置。

   ```bash
   sudo mv ./kubectl-convert /usr/local/bin/kubectl-convert
   sudo chown root: /usr/local/bin/kubectl-convert
   ```

   {{< note >}}
   确保你的 PATH 环境变量中存在 `/usr/local/bin`
   {{< /note >}}

5. 验证插件是否安装成功

   ```shell
   kubectl convert --help
   ```

   如果你没有看到任何错误就代表插件安装成功了。

6. 安装插件后，清理安装文件：

   ```bash
   rm kubectl-convert kubectl-convert.sha256
   ```

### 在 macOS 上卸载 kubectl   {#uninstall-kubectl-on-macos}

根据你安装 `kubectl` 的方式，使用以下某种方法来卸载：

### 使用命令行卸载 kubectl   {#uninstall-kubectl-using-cli}

1. 找到你系统上的 `kubectl` 可执行文件：

   ```bash
   where kubectl
   ```

2. 移除 `kubectl` 可执行文件：

   ```bash
   sudo rm <path>
   ```

   将 `<path>` 替换为上一步中找到的 `kubectl` 可执行文件的路径。
   例如，`sudo rm /usr/local/bin/kubectl`。

### 使用 Homebrew 卸载 kubectl    {#uninstall-kubectl-using-homebrew}

如果你使用 Homebrew 安装了 `kubectl`，运行以下命令：

```bash
brew remove kubectl
```

## {{% heading "whatsnext" %}}

{{< include "included/kubectl-whats-next.md" >}}
