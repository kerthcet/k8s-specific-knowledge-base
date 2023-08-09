---
title: 为 Windows 的 Pod 和容器配置 RunAsUserName
content_type: task
weight: 40
---



{{< feature-state for_k8s_version="v1.18" state="stable" >}}

本页展示如何为运行为在 Windows 节点上运行的 Pod 和容器配置 `RunAsUserName`。
大致相当于 Linux 上的 `runAsUser`，允许在容器中以与默认值不同的用户名运行应用。

## {{% heading "prerequisites" %}}

你必须有一个 Kubernetes 集群，并且 kubectl 必须能和集群通信。
集群应该要有 Windows 工作节点，将在其中调度运行 Windows 工作负载的 pod 和容器。

## 为 Pod 设置 Username    {#set-the-username-for-a-pod}

要指定运行 Pod 容器时所使用的用户名，请在 Pod 声明中包含 `securityContext`
([PodSecurityContext](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podsecuritycontext-v1-core)) 字段，
并在其内部包含 `windowsOptions`
([WindowsSecurityContextOptions](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#windowssecuritycontextoptions-v1-core))
字段的 `runAsUserName` 字段。


你为 Pod 指定的 Windows SecurityContext 选项适用于该 Pod 中（包括 init 容器）的所有容器。

这儿有一个已经设置了 `runAsUserName` 字段的 Windows Pod 的配置文件：

{{< codenew file="windows/run-as-username-pod.yaml" >}}


创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/windows/run-as-username-pod.yaml
```


验证 Pod 容器是否在运行：

```shell
kubectl get pod run-as-username-pod-demo
```


获取该容器的 shell：

```shell
kubectl exec -it run-as-username-pod-demo -- powershell
```


检查运行 shell 的用户的用户名是否正确：

```powershell
echo $env:USERNAME
```


输出结果应该是这样：

```
ContainerUser
```


## 为容器设置 Username    {#set-the-username-for-a-container}

要指定运行容器时所使用的用户名，请在容器清单中包含 `securityContext`
([SecurityContext](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#securitycontext-v1-core))
字段，并在其内部包含 `windowsOptions`
（[WindowsSecurityContextOptions](/docs/reference/generated/kubernetes-api/{{< param
"version" >}}/#windowssecuritycontextoptions-v1-core)）
字段的 `runAsUserName` 字段。

你为容器指定的 Windows SecurityContext 选项仅适用于该容器，并且它会覆盖 Pod 级别设置。

这里有一个 Pod 的配置文件，其中只有一个容器，并且在 Pod 级别和容器级别都设置了 `runAsUserName`：

{{< codenew file="windows/run-as-username-container.yaml" >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/windows/run-as-username-container.yaml
```

验证 Pod 容器是否在运行：

```shell
kubectl get pod run-as-username-container-demo
```

获取该容器的 shell：

```shell
kubectl exec -it run-as-username-container-demo -- powershell
```

检查运行 shell 的用户的用户名是否正确（应该是容器级别设置的那个）：

```powershell
echo $env:USERNAME
```

输出结果应该是这样：

```
ContainerAdministrator
```

## Windows Username 的局限性    {#windows-username-limitations}

想要使用此功能，在 `runAsUserName` 字段中设置的值必须是有效的用户名。
它必须是 `DOMAIN\USER` 这种格式，其中 `DOMAIN\` 是可选的。
Windows 用户名不区分大小写。此外，关于 `DOMAIN` 和 `USER` 还有一些限制：

- `runAsUserName` 字段不能为空，并且不能包含控制字符（ASCII 值：`0x00-0x1F`、`0x7F`）
- `DOMAIN` 必须是 NetBios 名称或 DNS 名称，每种名称都有各自的局限性：
  - NetBios 名称：最多 15 个字符，不能以 `.`（点）开头，并且不能包含以下字符：`\ / : * ? " < > |`
  - DNS 名称：最多 255 个字符，只能包含字母、数字、点和中划线，并且不能以 `.`（点）或 `-`（中划线）开头和结尾。
- `USER` 最多不超过 20 个字符，不能 **只** 包含点或空格，并且不能包含以下字符：`" / \ [ ] : ; | = , + * ? < > @`

`runAsUserName` 字段接受的值的一些示例：`ContainerAdministrator`、`ContainerUser`、
`NT AUTHORITY\NETWORK SERVICE`、`NT AUTHORITY\LOCAL SERVICE`。

关于这些限制的更多信息，可以查看[这里](https://support.microsoft.com/en-us/help/909264/naming-conventions-in-active-directory-for-computers-domains-sites-and)和[这里](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.localaccounts/new-localuser?view=powershell-5.1)。

## {{% heading "whatsnext" %}}

* [Kubernetes 中调度 Windows 容器的指南](/zh-cn/docs/concepts/windows/user-guide/)
* [使用组托管服务帐户（GMSA）管理工作负载身份](/zh-cn/docs/concepts/windows/user-guide/#managing-workload-identity-with-group-managed-service-accounts)
* [Windows 下 pod 和容器的 GMSA 配置](/zh-cn/docs/tasks/configure-pod-container/configure-gmsa/)
