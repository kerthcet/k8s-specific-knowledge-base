---
title: 为 Windows Pod 和容器配置 GMSA
content_type: task
weight: 30
---

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

本页展示如何为将运行在 Windows 节点上的 Pod 和容器配置
[组管理的服务账号（Group Managed Service Accounts，GMSA）](https://docs.microsoft.com/zh-cn/windows-server/security/group-managed-service-accounts/group-managed-service-accounts-overview)。
组管理的服务账号是活动目录（Active Directory）的一种特殊类型，
提供自动化的密码管理、简化的服务主体名称（Service Principal Name，SPN）
管理以及跨多个服务器将管理操作委派给其他管理员等能力。

在 Kubernetes 环境中，GMSA 凭据规约配置为 Kubernetes 集群范围的自定义资源
（Custom Resources）形式。Windows Pod 以及各 Pod 中的每个容器可以配置为使用 GMSA
来完成基于域（Domain）的操作（例如，Kerberos 身份认证），以便与其他 Windows 服务相交互。

## {{% heading "prerequisites" %}}

你需要一个 Kubernetes 集群，以及 `kubectl` 命令行工具，
且工具必须已配置为能够与你的集群通信。集群预期包含 Windows 工作节点。
本节讨论需要为每个集群执行一次的初始操作。

### 安装 GMSACredentialSpec CRD

你需要在集群上配置一个用于 GMSA 凭据规约资源的
[CustomResourceDefinition](/zh-cn/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)(CRD)，
以便定义类型为 `GMSACredentialSpec` 的自定义资源。首先下载 GMSA CRD
[YAML](https://github.com/kubernetes-sigs/windows-gmsa/blob/master/admission-webhook/deploy/gmsa-crd.yml)
并将其保存为 `gmsa-crd.yaml`。接下来执行 `kubectl apply -f gmsa-crd.yaml` 安装 CRD。

### 安装 Webhook 来验证 GMSA 用户

你需要为 Kubernetes 集群配置两个 Webhook，在 Pod 或容器级别填充和检查
GMSA 凭据规约引用。

1. 一个修改模式（Mutating）的 Webhook，将对 GMSA 的引用（在 Pod 规约中体现为名字）
   展开为完整凭据规约的 JSON 形式，并保存回 Pod 规约中。

1. 一个验证模式（Validating）的 Webhook，确保对 GMSA 的所有引用都是已经授权给
   Pod 的服务账号使用的。

安装以上 Webhook 及其相关联的对象需要执行以下步骤：

1. 创建一个证书密钥对（用于允许 Webhook 容器与集群通信）

1. 安装一个包含如上证书的 Secret

1. 创建一个包含核心 Webhook 逻辑的 Deployment

1. 创建引用该 Deployment 的 Validating Webhook 和 Mutating Webhook 配置

你可以使用[这个脚本](https://github.com/kubernetes-sigs/windows-gmsa/blob/master/admission-webhook/deploy/deploy-gmsa-webhook.sh)
来部署和配置上述 GMSA Webhook 及相关联的对象。你还可以在运行脚本时设置 `--dry-run=server`
选项以便审查脚本将会对集群做出的变更。

脚本所使用的 [YAML 模板](https://github.com/kubernetes-sigs/windows-gmsa/blob/master/admission-webhook/deploy/gmsa-webhook.yml.tpl)
也可用于手动部署 Webhook 及相关联的对象，不过需要对其中的参数作适当替换。


## 在活动目录中配置 GMSA 和 Windows 节点

在配置 Kubernetes 中的 Pod 以使用 GMSA 之前，需要按
[Windows GMSA 文档](https://docs.microsoft.com/en-us/windows-server/security/group-managed-service-accounts/getting-started-with-group-managed-service-accounts#BKMK_Step1)
中描述的那样先在活动目录中准备好期望的 GMSA。
Windows 工作节点（作为 Kubernetes 集群的一部分）需要被配置到活动目录中，以便访问与期望的
GSMA 相关联的秘密凭据数据。这一操作的描述位于
[Windows GMSA 文档](https://docs.microsoft.com/en-us/windows-server/security/group-managed-service-accounts/getting-started-with-group-managed-service-accounts#to-add-member-hosts-using-the-set-adserviceaccount-cmdlet)
中。

## 创建 GMSA 凭据规约资源

当（如前所述）安装了 GMSACredentialSpec CRD 之后，你就可以配置包含 GMSA
凭据规约的自定义资源了。GMSA 凭据规约中并不包含秘密或敏感数据。
其中包含的信息主要用于容器运行时，便于后者向 Windows 描述容器所期望的 GMSA。
GMSA 凭据规约可以使用
[PowerShell 脚本](https://github.com/kubernetes-sigs/windows-gmsa/tree/master/scripts/GenerateCredentialSpecResource.ps1)
以 YAML 格式生成。

下面是手动以 JSON 格式生成 GMSA 凭据规约并对其进行 YAML 转换的步骤：

1. 导入 CredentialSpec [模块](https://github.com/MicrosoftDocs/Virtualization-Documentation/blob/live/windows-server-container-tools/ServiceAccounts/CredentialSpec.psm1)：`ipmo CredentialSpec.psm1`

1. 使用 `New-CredentialSpec` 来创建一个 JSON 格式的凭据规约。
   要创建名为 `WebApp1` 的 GMSA 凭据规约，调用
   `New-CredentialSpec -Name WebApp1 -AccountName WebApp1 -Domain $(Get-ADDomain -Current LocalComputer)`。

1. 使用 `Get-CredentialSpec` 来显示 JSON 文件的路径。

1. 将凭据规约从 JSON 格式转换为 YAML 格式，并添加必要的头部字段
   `apiVersion`、`kind`、`metadata` 和 `credspec`，使其成为一个可以在
   Kubernetes 中配置的 GMSACredentialSpec 自定义资源。

下面的 YAML 配置描述的是一个名为 `gmsa-WebApp1` 的 GMSA 凭据规约：

```yaml
apiVersion: windows.k8s.io/v1
kind: GMSACredentialSpec
metadata:
  name: gmsa-WebApp1  # 这是随意起的一个名字，将用作引用
credspec:
  ActiveDirectoryConfig:
    GroupManagedServiceAccounts:
    - Name: WebApp1   # GMSA 账号的用户名
      Scope: CONTOSO  # NETBIOS 域名
    - Name: WebApp1   # GMSA 账号的用户名
      Scope: contoso.com # DNS 域名
  CmsPlugins:
  - ActiveDirectory
  DomainJoinConfig:
    DnsName: contoso.com  # DNS 域名
    DnsTreeName: contoso.com # DNS 域名根
    Guid: 244818ae-87ac-4fcd-92ec-e79e5252348a  # GUID
    MachineAccountName: WebApp1 # GMSA 账号的用户名
    NetBiosName: CONTOSO  # NETBIOS 域名
    Sid: S-1-5-21-2126449477-2524075714-3094792973 # GMSA 的 SID
```

上面的凭据规约资源可以保存为 `gmsa-Webapp1-credspec.yaml`，之后使用
`kubectl apply -f gmsa-Webapp1-credspec.yml` 应用到集群上。

## 配置集群角色以启用对特定 GMSA 凭据规约的 RBAC

你需要为每个 GMSA 凭据规约资源定义集群角色。
该集群角色授权某主体（通常是一个服务账号）对特定的 GMSA 资源执行 `use` 动作。
下面的示例显示的是一个集群角色，对前文创建的凭据规约 `gmsa-WebApp1` 执行鉴权。
将此文件保存为 `gmsa-webapp1-role.yaml` 并执行 `kubectl apply -f gmsa-webapp1-role.yaml`。

```yaml
# 创建集群角色读取凭据规约
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: webapp1-role
rules:
- apiGroups: ["windows.k8s.io"]
  resources: ["gmsacredentialspecs"]
  verbs: ["use"]
  resourceNames: ["gmsa-WebApp1"]
```

## 将角色指派给要使用特定 GMSA 凭据规约的服务账号

你需要将某个服务账号（Pod 配置所对应的那个）绑定到前文创建的集群角色上。
这一绑定操作实际上授予该服务账号使用所指定的 GMSA 凭据规约资源的访问权限。
下面显示的是一个绑定到集群角色 `webapp1-role` 上的 default 服务账号，
使之能够使用前面所创建的 `gmsa-WebApp1` 凭据规约资源。

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: allow-default-svc-account-read-on-gmsa-WebApp1
  namespace: default
subjects:
- kind: ServiceAccount
  name: default
  namespace: default
roleRef:
  kind: ClusterRole
  name: webapp1-role
  apiGroup: rbac.authorization.k8s.io
```

## 在 Pod 规约中配置 GMSA 凭据规约引用

Pod 规约字段 `securityContext.windowsOptions.gmsaCredentialSpecName`
可用来设置对指定 GMSA 凭据规约自定义资源的引用。
设置此引用将会配置 Pod 中的所有容器使用所给的 GMSA。
下面是一个 Pod 规约示例，其中包含了对 `gmsa-WebApp1` 凭据规约的引用：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    run: with-creds
  name: with-creds
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      run: with-creds
  template:
    metadata:
      labels:
        run: with-creds
    spec:
      securityContext:
        windowsOptions:
          gmsaCredentialSpecName: gmsa-webapp1
      containers:
      - image: mcr.microsoft.com/windows/servercore/iis:windowsservercore-ltsc2019
        imagePullPolicy: Always
        name: iis
      nodeSelector:
        kubernetes.io/os: windows
```

Pod 中的各个容器也可以使用对应容器的 `securityContext.windowsOptions.gmsaCredentialSpecName`
字段来设置期望使用的 GMSA 凭据规约。例如：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    run: with-creds
  name: with-creds
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      run: with-creds
  template:
    metadata:
      labels:
        run: with-creds
    spec:
      containers:
      - image: mcr.microsoft.com/windows/servercore/iis:windowsservercore-ltsc2019
        imagePullPolicy: Always
        name: iis
        securityContext:
          windowsOptions:
            gmsaCredentialSpecName: gmsa-Webapp1
      nodeSelector:
        kubernetes.io/os: windows
```

当 Pod 规约中填充了 GMSA 相关字段（如上所述），在集群中应用 Pod 规约时会依次发生以下事件：

1. Mutating Webhook 解析对 GMSA 凭据规约资源的引用，并将其全部展开，
   得到 GMSA 凭据规约的实际内容。

1. Validating Webhook 确保与 Pod 相关联的服务账号有权在所给的 GMSA 凭据规约上执行 `use` 动作。

1. 容器运行时为每个 Windows 容器配置所指定的 GMSA 凭据规约，
   这样容器就可以以活动目录中该 GMSA 所代表的身份来执行操作，使用该身份来访问域中的服务。

## 使用主机名或 FQDN 对网络共享进行身份验证

如果你在使用主机名或 FQDN 从 Pod 连接到 SMB 共享时遇到问题，但能够通过其 IPv4 地址访问共享，
请确保在 Windows 节点上设置了以下注册表项。

```cmd
reg add "HKLM\SYSTEM\CurrentControlSet\Services\hns\State" /v EnableCompartmentNamespace /t REG_DWORD /d 1
```

然后需要重新创建正在运行的 Pod 以使行为更改生效。有关如何使用此注册表项的更多信息，
请参见[此处](https://github.com/microsoft/hcsshim/blob/885f896c5a8548ca36c88c4b87fd2208c8d16543/internal/uvm/create.go#L74-L83)。

## 故障排查

如果在你的环境中配置 GMSA 时遇到了困难，你可以采取若干步骤来排查可能的故障。

首先，确保 credspec 已传递给 Pod。为此，你需要先运行 `exec`
进入到你的一个 Pod 中并检查 `nltest.exe /parentdomain` 命令的输出。

在下面的例子中，Pod 未能正确地获得凭据规约：

```PowerShell
kubectl exec -it iis-auth-7776966999-n5nzr powershell.exe
```

`nltest.exe /parentdomain` 导致以下错误：

```output
Getting parent domain failed: Status = 1722 0x6ba RPC_S_SERVER_UNAVAILABLE
```

如果 Pod 未能正确获得凭据规约，则下一步就要检查与域之间的通信。
首先，从 Pod 内部快速执行一个 nslookup 操作，找到域根。

这一操作会告诉我们三件事情：

1. Pod 能否访问域控制器（DC）
1. DC 能否访问 Pod
1. DNS 是否正常工作

如果 DNS 和通信测试通过，接下来你需要检查是否 Pod 已经与域之间建立了安全通信通道。
要执行这一检查，你需要再次通过 `exec` 进入到你的 Pod 中并执行 `nltest.exe /query` 命令。

```PowerShell
nltest.exe /query
```

结果输出如下：

```output
I_NetLogonControl failed: Status = 1722 0x6ba RPC_S_SERVER_UNAVAILABLE
```

这告诉我们，由于某种原因，Pod 无法使用 credspec 中指定的帐户登录到域。
你可以尝试通过运行以下命令来修复安全通道：

```PowerShell
nltest /sc_reset:domain.example
```

如果命令成功，你将看到类似以下内容的输出：

```output
Flags: 30 HAS_IP  HAS_TIMESERV
Trusted DC Name \\dc10.domain.example
Trusted DC Connection Status Status = 0 0x0 NERR_Success
The command completed successfully
```

如果以上命令修复了错误，你可以通过将以下生命周期回调添加到你的 Pod 规约中来自动执行该步骤。
如果这些操作没有修复错误，你将需要再次检查你的 credspec 并确认它是正确和完整的。

```yaml
        image: registry.domain.example/iis-auth:1809v1
        lifecycle:
          postStart:
            exec:
              command: ["powershell.exe","-command","do { Restart-Service -Name netlogon } while ( $($Result = (nltest.exe /query); if ($Result -like '*0x0 NERR_Success*') {return $true} else {return $false}) -eq $false)"]
        imagePullPolicy: IfNotPresent
```

如果你向你的 Pod 规约中添加如上所示的 `lifecycle` 节，则 Pod
会自动执行所列举的命令来重启 `netlogon` 服务，直到 `nltest.exe /query`
命令返回时没有错误信息。
