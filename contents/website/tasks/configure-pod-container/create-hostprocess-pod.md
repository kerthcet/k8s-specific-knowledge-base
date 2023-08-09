---
title: 创建 Windows HostProcess Pod
content_type: task
weight: 50
min-kubernetes-server-version: 1.23
---


{{< feature-state for_k8s_version="v1.26" state="stable" >}}

Windows HostProcess 容器让你能够在 Windows 主机上运行容器化负载。
这类容器以普通的进程形式运行，但能够在具有合适用户特权的情况下，
访问主机网络名字空间、存储和设备。HostProcess 容器可用来在 Windows
节点上部署网络插件、存储配置、设备插件、kube-proxy 以及其他组件，
同时不需要配置专用的代理或者直接安装主机服务。

类似于安装安全补丁、事件日志收集等这类管理性质的任务可以在不需要集群操作员登录到每个
Windows 节点的前提下执行。HostProcess 容器可以以主机上存在的任何用户账号来运行，
也可以以主机所在域中的用户账号运行，这样管理员可以通过用户许可权限来限制资源访问。
尽管文件系统和进程隔离都不支持，在启动容器时会在主机上创建一个新的卷，
为其提供一个干净的、整合的工作空间。HostProcess 容器也可以基于现有的 Windows
基础镜像来制作，并且不再有 Windows 服务器容器所带有的那些
[兼容性需求](https://docs.microsoft.com/virtualization/windowscontainers/deploy-containers/version-compatibility)，
这意味着基础镜像的版本不必与主机操作系统的版本匹配。
不过，仍然建议你像使用 Windows 服务器容器负载那样，使用相同的基础镜像版本，
这样你就不会有一些未使用的镜像占用节点上的存储空间。HostProcess 容器也支持
在容器卷内执行[卷挂载](#volume-mounts)。

### 我何时该使用 Windows HostProcess 容器？

- 当你准备执行需要访问主机上网络名字空间的任务时，HostProcess
  容器能够访问主机上的网络接口和 IP 地址。
- 当你需要访问主机上的资源，如文件系统、事件日志等等。
- 需要安装特定的设备驱动或者 Windows 服务时。
- 需要对管理任务和安全策略进行整合时。使用 HostProcess 容器能够缩小 Windows
  节点上所需要的特权范围。

## {{% heading "prerequisites" %}}


本任务指南是特定于 Kubernetes v{{< skew currentVersion >}} 的。
如果你运行的不是 Kubernetes v{{< skew currentVersion >}}，请移步访问正确
版本的 Kubernetes 文档。

在 Kubernetes v{{< skew currentVersion >}} 中，HostProcess 容器功能特性默认是启用的。
kubelet 会直接与 containerd 通信，通过 CRI 将主机进程标志传递过去。
你可以使用 containerd 的最新版本（v1.6+）来运行 HostProcess 容器。
参阅[如何安装 containerd](/zh-cn/docs/setup/production-environment/container-runtimes/#containerd)。

## 限制   {#limitations}

以下限制是与 Kubernetes v{{< skew currentVersion >}} 相关的：

- HostProcess 容器需要 containerd 1.6 或更高版本的
  {{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}，
  推荐 containerd 1.7。
- HostProcess Pods 只能包含 HostProcess 容器。这是在 Windows 操作系统上的约束；
  非特权的 Windows 容器不能与主机 IP 名字空间共享虚拟网卡（vNIC）。
- HostProcess 在主机上以一个进程的形式运行，除了通过 HostProcess
  用户账号所实施的资源约束外，不提供任何形式的隔离。HostProcess 容器不支持文件系统或
  Hyper-V 隔离。
- 卷挂载是被支持的，并且要花在到容器卷下。参见[卷挂载](#volume-mounts)。
- 默认情况下有一组主机用户账号可供 HostProcess 容器使用。
  参见[选择用户账号](#choosing-a-user-account)。
- 对资源约束（磁盘、内存、CPU 个数）的支持与主机上进程相同。
- **不支持**命名管道或者 UNIX 域套接字形式的挂载，需要使用主机上的路径名来访问
  （例如，\\\\.\\pipe\\\*）。
  
## HostProcess Pod 配置需求   {#hostprocess-pod-configuration-requirements}

启用 Windows HostProcess Pod 需要在 Pod 安全配置中设置合适的选项。
在 [Pod
安全标准](/zh-cn/docs/concepts/security/pod-security-standards)中所定义的策略中，
HostProcess Pod 默认是不被 basline 和 restricted 策略支持的。因此建议
HostProcess 运行在与 privileged 模式相看齐的策略下。

当运行在 privileged 策略下时，下面是要启用 HostProcess Pod 创建所需要设置的选项：

<table>
  <thead>
    <tr>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap"><a href="/zh-cn/docs/concepts/security/pod-security-standards"><tt>securityContext.windowsOptions.hostProcess</tt></a></td>
      <td>
        Windows Pods 提供运行<a href="/zh-cn/docs/tasks/configure-pod-container/create-hostprocess-pod">
        HostProcess 容器</a>的能力，这类容器能够具有对 Windows 节点的特权访问权限。</p>
        <ul>
          <li><code>true</code></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><a href="/zh-cn/docs/concepts/security/pod-security-standards"><tt>hostNetwork</tt></a></td>
      <td>
        Pod 容器 HostProcess 容器必须使用主机的网络名字空间。
        </p>
        <ul>
          <li><code>true</code></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><a href="/zh-cn/docs/tasks/configure-pod-container/configure-runasusername/"><tt>securityContext.windowsOptions.runAsUserName</tt></a></td>
      <td>
        关于 HostProcess 容器所要使用的用户的规约，需要设置在 Pod 的规约中。
        </p>
        <ul>
          <li><code>NT AUTHORITY\SYSTEM</code></li>
          <li><code>NT AUTHORITY\Local service</code></li>
          <li><code>NT AUTHORITY\NetworkService</code></li>
          <li>
          本地用户组名称（参见下文）
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><a href="/zh-cn/docs/concepts/security/pod-security-standards"><tt>runAsNonRoot</tt></a></td>
      <td>
        因为 HostProcess 容器有访问主机的特权，<tt>runAsNonRoot</tt> 字段不可以设置为 true。
        </p>
        <ul>
          <li><code>false</code></li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

### 配置清单示例（片段）   {#manifest-example}

```yaml
spec:
  securityContext:
    windowsOptions:
      hostProcess: true
      runAsUserName: "NT AUTHORITY\\Local service"
  hostNetwork: true
  containers:
  - name: test
    image: image1:latest
    command:
      - ping
      - -t
      - 127.0.0.1
  nodeSelector:
    "kubernetes.io/os": windows
```

## 卷挂载    {#volume-mounts}

HostProcess 容器支持在容器卷空间中挂载卷的能力。
卷挂载行为将因节点所使用的 containerd 运行时版本而异。

### containerd v1.6

在容器内运行的应用能够通过相对或者绝对路径直接访问卷挂载。
环境变量 `$CONTAINER_SANDBOX_MOUNT_POINT` 在容器创建时被设置为指向容器卷的绝对主机路径。
相对路径是基于 `.spec.containers.volumeMounts.mountPath` 配置来推导的。

容器内支持通过下面的路径结构来访问服务账号令牌：

- `.\var\run\secrets\kubernetes.io\serviceaccount\`
- `$CONTAINER_SANDBOX_MOUNT_POINT\var\run\secrets\kubernetes.io\serviceaccount\`

### containerd v1.7（及更高版本）   {#containerd-v1-7-and-greater}

容器内运行的应用可以通过 volumeMount 指定的 `mountPath` 直接访问卷挂载
（就像 Linux 和非 HostProcess Windows 容器一样）。

为了向后兼容性，卷也可以通过使用由 containerd v1.6 配置的相同相对路径进行访问。

例如，要在容器中访问服务帐户令牌，你将使用以下路径之一：

- `c:\var\run\secrets\kubernetes.io\serviceaccount`
- `/var/run/secrets/kubernetes.io/serviceaccount/`
- `$CONTAINER_SANDBOX_MOUNT_POINT\var\run\secrets\kubernetes.io\serviceaccount\`

## 资源限制    {#resource-limits}

资源限制（磁盘、内存、CPU 个数）作用到任务之上，并在整个任务上起作用。
例如，如果内存限制设置为 10MB，任何 HostProcess 任务对象所分配的内存不会超过 10MB。
这一行为与其他 Windows 容器类型相同。资源限制的设置方式与编排系统或容器运行时无关。
唯一的区别是用来跟踪资源所进行的磁盘资源用量的计算，出现差异的原因是因为
HostProcess 容器启动引导的方式造成的。

## 选择用户账号  {#choosing-a-user-account}

### 系统账号   {#system-accounts}

默认情况下，HostProcess 容器支持以三种被支持的 Windows 服务账号之一来运行：

- **[LocalSystem](https://docs.microsoft.com/windows/win32/services/localsystem-account)**
- **[LocalService](https://docs.microsoft.com/windows/win32/services/localservice-account)**
- **[NetworkService](https://docs.microsoft.com/windows/win32/services/networkservice-account)**

你应该为每个 HostProcess 容器选择一个合适的 Windows 服务账号，尝试限制特权范围，
避免给主机代理意外的（甚至是恶意的）伤害。LocalSystem 服务账号的特权级
在三者之中最高，只有在绝对需要的时候才应该使用。只要可能，应该使用
LocalService 服务账号，因为该账号在三者中特权最低。

### 本地账号   {#local-accounts}

取决于配置，HostProcess 容器也能够以本地用户账号运行，
从而允许节点操作员为工作负载提供细粒度的访问权限。

要以本地用户运行 HostProcess 容器，必须首先在节点上创建一个本地用户组，
并在部署中在 `runAsUserName` 字段中指定该本地用户组的名称。
在初始化 HostProcess 容器之前，将创建一个新的**临时**本地用户账号，并加入到指定的用户组中，
使用这个账号来运行容器。这样做有许多好处，包括不再需要管理本地用户账号的密码。
作为服务账号运行的初始 HostProcess 容器可用于准备用户组，以供后续的 HostProcess 容器使用。

{{< note >}}
以本地用户账号运行 HostProcess 容器需要 containerd v1.7+。
{{< /note >}}

例如：

1. 在节点上创建本地用户组（这可以在另一个 HostProcess 容器中完成）。

   ```cmd
   net localgroup hpc-localgroup /add
   ```

2. 为本地用户组授予访问所需资源的权限。这可以通过使用
   [icacls](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/icacls)
   这类工具达成。

3. 针对 Pod 或个别容器，将 `runAsUserName` 设置为本地用户组的名称。

   ```yaml
   securityContext:
     windowsOptions:
       hostProcess: true
       runAsUserName: hpc-localgroup
   ```

4. 调度 Pod！

## HostProcess 容器的基础镜像   {#base-image-for-hostprocess-containers}

HostProcess 容器可以基于任何现有的
[Windows Container 基础镜像](https://learn.microsoft.com/zh-cn/virtualization/windowscontainers/manage-containers/container-base-images)进行构建。

此外，还专为 HostProcess 容器创建了一个新的基础镜像！有关更多信息，请查看
[windows-host-process-containers-base-image github 项目](https://github.com/microsoft/windows-host-process-containers-base-image#overview)。

## HostProcess 容器的故障排查   {#troubleshooting-hostprocess-containers}

- HostProcess 容器因
  `failed to create user process token: failed to logon user: Access is denied.: unknown`
  启动失败。

  确保 containerd 以 `LocalSystem` 或 `LocalService` 服务帐户运行。
  用户账号（即使是管理员账号）没有权限为任何支持的[用户账号](#choosing-a-user-account)创建登录令牌。
