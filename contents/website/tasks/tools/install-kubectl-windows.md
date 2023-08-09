---
title: 在 Windows 上安装 kubectl
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: Windows 安装 kubectl
---

## {{% heading "prerequisites" %}}

kubectl 版本和集群版本之间的差异必须在一个小版本号内。
例如：v{{< skew currentVersion >}} 版本的客户端能与 v{{< skew currentVersionAddMinor -1 >}}、
v{{< skew currentVersionAddMinor 0 >}} 和 v{{< skew currentVersionAddMinor 1 >}} 版本的控制面通信。
用最新兼容版的 kubectl 有助于避免不可预见的问题。

## 在 Windows 上安装 kubectl {#install-kubectl-on-windows}

在 Windows 系统中安装 kubectl 有如下几种方法：

- [用 curl 在 Windows 上安装 kubectl](#install-kubectl-binary-with-curl-on-windows)
- [在 Windows 上用 Chocolatey、Scoop 或 winget 安装](#install-nonstandard-package-tools)

### 用 curl 在 Windows 上安装 kubectl {#install-kubectl-binary-with-curl-on-windows}


1. 下载最新补丁版 {{< skew currentVersion >}}：
   [kubectl {{< skew currentPatchVersion >}}](https://dl.k8s.io/release/v{{< skew currentPatchVersion >}}/bin/windows/amd64/kubectl.exe)。

   如果你已安装了 `curl`，也可以使用此命令：

   ```powershell
   curl.exe -LO "https://dl.k8s.io/release/v{{< skew currentPatchVersion >}}/bin/windows/amd64/kubectl.exe"
   ```

   {{< note >}}
   要想找到最新稳定的版本（例如：为了编写脚本），可以看看这里 [https://dl.k8s.io/release/stable.txt](https://dl.k8s.io/release/stable.txt)。
   {{< /note >}}

2. 验证该可执行文件（可选步骤）
   
   下载 `kubectl` 校验和文件：

   ```powershell
   curl.exe -LO "https://dl.k8s.io/v{{< skew currentPatchVersion >}}/bin/windows/amd64/kubectl-convert.exe.sha256"
   ```

   基于校验和文件，验证 `kubectl` 的可执行文件：

   - 在命令行环境中，手工对比 `CertUtil` 命令的输出与校验和文件：

     ```cmd
     CertUtil -hashfile kubectl.exe SHA256
     type kubectl.exe.sha256
     ```

   - 用 PowerShell 自动验证，用运算符 `-eq` 来直接取得 `True` 或 `False` 的结果：

     ```powershell
     $(Get-FileHash -Algorithm SHA256 .\kubectl.exe).Hash -eq $(Get-Content .\kubectl.exe.sha256)
     ```


3. 将 `kubectl` 二进制文件夹追加或插入到你的 `PATH` 环境变量中。

4. 测试一下，确保此 `kubectl` 的版本和期望版本一致：

   ```cmd
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

{{< note >}}
[Windows 版的 Docker Desktop](https://docs.docker.com/docker-for-windows/#kubernetes)
将其自带版本的 `kubectl` 添加到 `PATH`。
如果你之前安装过 Docker Desktop，可能需要把此 `PATH` 条目置于 Docker Desktop 安装的条目之前，
或者直接删掉 Docker Desktop 的 `kubectl`。
{{< /note >}}

### 在 Windows 上用 Chocolatey、Scoop 或 winget 安装 {#install-nonstandard-package-tools}

1. 要在 Windows 上安装 kubectl，你可以使用包管理器 [Chocolatey](https://chocolatey.org)、
   命令行安装器 [Scoop](https://scoop.sh) 或包管理器 [winget](https://learn.microsoft.com/zh-cn/windows/package-manager/winget/)。

   {{< tabs name="kubectl_win_install" >}}
   {{% tab name="choco" %}}
   ```powershell
   choco install kubernetes-cli
   ```
   {{% /tab %}}
   {{% tab name="scoop" %}}
   ```powershell
   scoop install kubectl
   ```
   {{% /tab %}}
   {{% tab name="winget" %}}
   ```powershell
   winget install -e --id Kubernetes.kubectl
   ```
   {{% /tab %}}
   {{< /tabs >}}

2. 测试一下，确保安装的是最新版本：

   ```powershell
   kubectl version --client
   ```

3. 导航到你的 home 目录：

   ```powershell
   # 当你用 cmd.exe 时，则运行： cd %USERPROFILE%
   cd ~
   ```

4. 创建目录 `.kube`：

   ```powershell
   mkdir .kube
   ```

5. 切换到新创建的目录 `.kube`：

   ```powershell
   cd .kube
   ```

6. 配置 kubectl，以接入远程的 Kubernetes 集群：

   ```powershell
   New-Item config -type file
   ```

{{< note >}}
编辑配置文件，你需要先选择一个文本编辑器，比如 Notepad。
{{< /note >}}

## 验证 kubectl 配置 {#verify-kubectl-configration}

{{< include "included/verify-kubectl.md" >}}

## kubectl 可选配置和插件 {#optional-kubectl-configurations}

### 启用 shell 自动补全功能 {#enable-shell-autocompletion}

kubectl 为 Bash、Zsh、Fish 和 PowerShell 提供自动补全功能，可以为你节省大量的输入。

下面是设置 PowerShell 自动补全功能的操作步骤。

{{< include "included/optional-kubectl-configs-pwsh.md" >}}

### 安装 `kubectl convert` 插件   {#install-kubectl-convert-plugin}

{{< include "included/kubectl-convert-overview.md" >}}

1. 用以下命令下载最新发行版：

   ```powershell
   curl.exe -LO "https://dl.k8s.io/release/v{{< skew currentPatchVersion >}}/bin/windows/amd64/kubectl-convert.exe"
   ```

2. 验证该可执行文件（可选步骤）。

   下载 `kubectl-convert` 校验和文件：

   ```powershell
   curl.exe -LO "https://dl.k8s.io/v{{< skew currentPatchVersion >}}/bin/windows/amd64/kubectl-convert.exe.sha256"
   ```

   基于校验和验证 `kubectl-convert` 的可执行文件：

   - 用提示的命令对 `CertUtil` 的输出和下载的校验和文件进行手动比较。
   
     ```cmd
     CertUtil -hashfile kubectl-convert.exe SHA256
     type kubectl-convert.exe.sha256
     ```


   - 使用 PowerShell `-eq` 操作使验证自动化，获得 `True` 或者 `False` 的结果：
   
     ```powershell
     $($(CertUtil -hashfile .\kubectl-convert.exe SHA256)[1] -replace " ", "") -eq $(type .\kubectl-convert.exe.sha256)
     ```

3. 将 `kubectl-convert` 二进制文件夹附加或添加到你的 `PATH` 环境变量中。

4. 验证插件是否安装成功。

   ```shell
   kubectl convert --help
   ```

   如果你没有看到任何错误就代表插件安装成功了。

5. 安装插件后，清理安装文件：

   ```powershell
   del kubectl-convert.exe kubectl-convert.exe.sha256
   ```

## {{% heading "whatsnext" %}}

{{< include "included/kubectl-whats-next.md" >}}
