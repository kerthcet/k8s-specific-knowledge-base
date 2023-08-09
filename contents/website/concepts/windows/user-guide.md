---
title: Kubernetes 中的 Windows 容器调度指南
content_type: concept
weight: 75
---


在许多组织中运行的服务和应用程序中，Windows 应用程序构成了很大一部分。
本指南将引导你完成在 Kubernetes 中配置和部署 Windows 容器的步骤。


## 目标  {#objectives}

* 配置 Deployment 样例以在 Windows 节点上运行 Windows 容器
* 在 Kubernetes 中突出 Windows 特定的功能

## 在你开始之前  {#before-you-begin}

* 创建一个 Kubernetes 集群，其中包含一个控制平面和一个运行 Windows Server 的工作节点。
* 务必请注意，在 Kubernetes 上创建和部署服务和工作负载的行为方式与 Linux 和 Windows 容器的行为方式大致相同。
  与集群交互的 [kubectl 命令](/zh-cn/docs/reference/kubectl/)是一致的。
  下一小节的示例旨在帮助你快速开始使用 Windows 容器。

## 快速开始：部署 Windows 容器  {#getting-started-deploying-a-windows-container}

以下示例 YAML 文件部署了一个在 Windows 容器内运行的简单 Web 服务器的应用程序。

创建一个名为 `win-webserver.yaml` 的 Service 规约，其内容如下：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: win-webserver
  labels:
    app: win-webserver
spec:
  ports:
    # 此 Service 服务的端口
    - port: 80
      targetPort: 80
  selector:
    app: win-webserver
  type: NodePort
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: win-webserver
  name: win-webserver
spec:
  replicas: 2
  selector:
    matchLabels:
      app: win-webserver
  template:
    metadata:
      labels:
        app: win-webserver
      name: win-webserver
    spec:
     containers:
      - name: windowswebserver
        image: mcr.microsoft.com/windows/servercore:ltsc2019
        command:
        - powershell.exe
        - -command
        - "<#code used from https://gist.github.com/19WAS85/5424431#> ; $$listener = New-Object System.Net.HttpListener ; $$listener.Prefixes.Add('http://*:80/') ; $$listener.Start() ; $$callerCounts = @{} ; Write-Host('Listening at http://*:80/') ; while ($$listener.IsListening) { ;$$context = $$listener.GetContext() ;$$requestUrl = $$context.Request.Url ;$$clientIP = $$context.Request.RemoteEndPoint.Address ;$$response = $$context.Response ;Write-Host '' ;Write-Host('> {0}' -f $$requestUrl) ;  ;$$count = 1 ;$$k=$$callerCounts.Get_Item($$clientIP) ;if ($$k -ne $$null) { $$count += $$k } ;$$callerCounts.Set_Item($$clientIP, $$count) ;$$ip=(Get-NetAdapter | Get-NetIpAddress); $$header='<html><body><H1>Windows Container Web Server</H1>' ;$$callerCountsString='' ;$$callerCounts.Keys | % { $$callerCountsString+='<p>IP {0} callerCount {1} ' -f $$ip[1].IPAddress,$$callerCounts.Item($$_) } ;$$footer='</body></html>' ;$$content='{0}{1}{2}' -f $$header,$$callerCountsString,$$footer ;Write-Output $$content ;$$buffer = [System.Text.Encoding]::UTF8.GetBytes($$content) ;$$response.ContentLength64 = $$buffer.Length ;$$response.OutputStream.Write($$buffer, 0, $$buffer.Length) ;$$response.Close() ;$$responseStatus = $$response.StatusCode ;Write-Host('< {0}' -f $$responseStatus)  } ; "
     nodeSelector:
      kubernetes.io/os: windows
```

{{< note >}}
端口映射也是支持的，但为简单起见，此示例将容器的端口 80 直接暴露给服务。
{{< /note >}}

1. 检查所有节点是否健康

   ```bash
   kubectl get nodes
   ```

1. 部署 Service 并监视 Pod 更新：

   ```bash
   kubectl apply -f win-webserver.yaml
   kubectl get pods -o wide -w
   ```

   当 Service 被正确部署时，两个 Pod 都被标记为就绪（Ready）。要退出 watch 命令，请按 Ctrl+C。

1. 检查部署是否成功。请验证：

   * 当执行 `kubectl get pods` 命令时，能够从 Linux 控制平面所在的节点上列出两个 Pod。
   * 跨网络的节点到 Pod 通信，从 Linux 控制平面所在的节点上执行 `curl` 命令来访问
     Pod IP 的 80 端口以检查 Web 服务器响应。
   * Pod 间通信，使用 `docker exec` 或 `kubectl exec`
     命令进入容器，并在 Pod 之间（以及跨主机，如果你有多个 Windows 节点）相互进行 ping 操作。
   * Service 到 Pod 的通信，在 Linux 控制平面所在的节点以及独立的 Pod 中执行 `curl`
     命令来访问虚拟的服务 IP（在 `kubectl get services` 命令下查看）。
   * 服务发现，执行 `curl` 命令来访问带有 Kubernetes
     [默认 DNS 后缀](/zh-cn/docs/concepts/services-networking/dns-pod-service/#services)的服务名称。
   * 入站连接，在 Linux 控制平面所在的节点上或集群外的机器上执行 `curl` 命令来访问 NodePort 服务。
   * 出站连接，使用 `kubectl exec`，从 Pod 内部执行 `curl` 访问外部 IP。

{{< note >}}
由于当前 Windows 平台的网络堆栈限制，Windows 容器主机无法访问调度到其上的 Service 的 IP。
只有 Windows Pod 能够访问 Service IP。
{{< /note >}}

## 可观察性  {#observability}

### 捕捉来自工作负载的日志  {#capturing-logs-from-workloads}

日志是可观察性的重要元素；它们使用户能够深入了解工作负载的运行情况，并且是解决问题的关键因素。
由于 Windows 容器和 Windows 容器中的工作负载与 Linux 容器的行为不同，因此用户很难收集日志，从而限制了操作可见性。
例如，Windows 工作负载通常配置为记录到 ETW（Windows 事件跟踪）或向应用程序事件日志推送条目。
[LogMonitor](https://github.com/microsoft/windows-container-tools/tree/master/LogMonitor)
是一个微软开源的工具，是监视 Windows 容器内所配置的日志源的推荐方法。
LogMonitor 支持监视事件日志、ETW 提供程序和自定义应用程序日志，将它们传送到 STDOUT 以供 `kubectl logs <pod>` 使用。

按照 LogMonitor GitHub 页面中的说明，将其二进制文件和配置文件复制到所有容器，
并为 LogMonitor 添加必要的入口点以将日志推送到标准输出（STDOUT）。

## 配置容器用户  {#configuring-container-user}

### 使用可配置的容器用户名  {#using-configurable-container-usernames}

Windows 容器可以配置为使用不同于镜像默认值的用户名来运行其入口点和进程。
[在这里](/zh-cn/docs/tasks/configure-pod-container/configure-runasusername/)了解更多信息。

### 使用组托管服务帐户（GMSA）管理工作负载身份  {#managing-workload-identity-with-group-managed-service-accounts}

Windows 容器工作负载可以配置为使用组托管服务帐户（Group Managed Service Accounts，GMSA）。
组托管服务帐户是一种特定类型的活动目录（Active Directory）帐户，可提供自动密码管理、
简化的服务主体名称（Service Principal Name，SPN）管理，以及将管理委派给多个服务器上的其他管理员的能力。
配置了 GMSA 的容器可以携带使用 GMSA 配置的身份访问外部活动目录域资源。
在[此处](/zh-cn/docs/tasks/configure-pod-container/configure-gmsa/)了解有关为 Windows
容器配置和使用 GMSA 的更多信息。

## 污点和容忍度  {#taints-and-tolerations}

用户需要使用某种污点（Taint）和节点选择器的组合，以便将 Linux 和 Windows 工作负载各自调度到特定操作系统的节点。
下面概述了推荐的方法，其主要目标之一是该方法不应破坏现有 Linux 工作负载的兼容性。

从 1.25 开始，你可以（并且应该）将每个 Pod 的 `.spec.os.name` 设置为 Pod 中的容器设计所用于的操作系统。
对于运行 Linux 容器的 Pod，将 `.spec.os.name` 设置为 `linux`。
对于运行 Windows 容器的 Pod，将 `.spec.os.name` 设置为 `windows`。

调度器在将 Pod 分配到节点时并不使用 `.spec.os.name` 的值。
你应该使用正常的 Kubernetes 机制[将 Pod 分配给节点](/zh-cn/docs/concepts/scheduling-eviction/assign-pod-node/)，
以确保集群的控制平面将 Pod 放置到运行适当操作系统的节点上。

`.spec.os.name` 值对 Windows Pod 的调度没有影响，
因此仍然需要污点和容忍以及节点选择器来确保 Windows Pod 落在适当的 Windows 节点。

### 确保特定于操作系统的工作负载落到合适的容器主机上  {#ensuring-os-specific-workloads-land-on-the-appropriate-container-host}

用户可以使用污点（Taint）和容忍度（Toleration）确保将 Windows 容器调度至合适的主机上。
现在，所有的 Kubernetes 节点都有以下默认标签：

* kubernetes.io/os = [windows|linux]
* kubernetes.io/arch = [amd64|arm64|...]

如果 Pod 规约没有指定像 `"kubernetes.io/os": windows` 这样的 nodeSelector，
则 Pod 可以被调度到任何主机上，Windows 或 Linux。
这可能会有问题，因为 Windows 容器只能在 Windows 上运行，而 Linux 容器只能在 Linux 上运行。
最佳实践是使用 nodeSelector。

但是，我们了解到，在许多情况下，用户已经预先存在大量 Linux 容器部署，
以及现成配置的生态系统，例如社区中的 Helm Chart 包和程序化的 Pod 生成案例，例如 Operator。
在这些情况下，你可能不愿更改配置来添加节点选择器。
另一种方法是使用污点。因为 kubelet 可以在注册过程中设置污点，
所以可以很容易地修改为，当只能在 Windows 上运行时，自动添加污点。

例如：`--register-with-taints='os=windows:NoSchedule'`

通过向所有 Windows 节点添加污点，任何负载都不会被调度到这些节点上（包括现有的 Linux Pod）。
为了在 Windows 节点上调度 Windows Pod，它需要 nodeSelector 和匹配合适的容忍度来选择 Windows。

```yaml
nodeSelector:
    kubernetes.io/os: windows
    node.kubernetes.io/windows-build: '10.0.17763'
tolerations:
    - key: "os"
      operator: "Equal"
      value: "windows"
      effect: "NoSchedule"
```

### 处理同一集群中的多个 Windows 版本  {#handling-multiple-windows-versions-in-the-same-cluster}

每个 Pod 使用的 Windows Server 版本必须与节点的版本匹配。
如果要在同一个集群中使用多个 Windows Server 版本，则应设置额外的节点标签和节点选择器。

Kubernetes 1.17 自动添加了一个新标签 `node.kubernetes.io/windows-build` 来简化这一点。
如果你运行的是旧版本，则建议手动将此标签添加到 Windows 节点。

此标签反映了需要匹配以实现兼容性的 Windows 主要、次要和内部版本号。
以下是目前用于每个 Windows Server 版本的值。

| 产品名称                              |   构建号                |
|--------------------------------------|------------------------|
| Windows Server 2019                  | 10.0.17763             |
| Windows Server, Version 20H2         | 10.0.19042             |
| Windows Server 2022                  | 10.0.20348             |

### 使用 RuntimeClass 进行简化  {#simplifying-with-runtimeclass}

[RuntimeClass] 可用于简化使用污点和容忍度的流程。
集群管理员可以创建一个用于封装这些污点和容忍度的 `RuntimeClass` 对象。

1. 将此文件保存到 `runtimeClasses.yml`。它包括针对 Windows 操作系统、架构和版本的 `nodeSelector`。

   ```yaml
   ---
   apiVersion: node.k8s.io/v1
   kind: RuntimeClass
   metadata:
     name: windows-2019
   handler: example-container-runtime-handler
   scheduling:
     nodeSelector:
       kubernetes.io/os: 'windows'
       kubernetes.io/arch: 'amd64'
       node.kubernetes.io/windows-build: '10.0.17763'
     tolerations:
     - effect: NoSchedule
       key: os
       operator: Equal
       value: "windows"
   ```

1. 以集群管理员身份运行 `kubectl create -f runtimeClasses.yml`
1. 根据情况，向 Pod 规约中添加 `runtimeClassName: windows-2019`

   例如：

   ```yaml
   ---
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: iis-2019
     labels:
       app: iis-2019
   spec:
     replicas: 1
     template:
       metadata:
         name: iis-2019
         labels:
           app: iis-2019
       spec:
         runtimeClassName: windows-2019
         containers:
         - name: iis
           image: mcr.microsoft.com/windows/servercore/iis:windowsservercore-ltsc2019
           resources:
             limits:
               cpu: 1
               memory: 800Mi
             requests:
               cpu: .1
               memory: 300Mi
           ports:
             - containerPort: 80
    selector:
       matchLabels:
         app: iis-2019
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: iis
   spec:
     type: LoadBalancer
     ports:
     - protocol: TCP
       port: 80
     selector:
       app: iis-2019
   ```

[RuntimeClass]: /zh-cn/docs/concepts/containers/runtime-class/
