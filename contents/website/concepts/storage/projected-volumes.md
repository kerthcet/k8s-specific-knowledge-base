---
title: 投射卷
content_type: concept
weight: 21 # 跟在持久卷之后
---



本文档描述 Kubernetes 中的**投射卷（Projected Volumes）**。
建议先熟悉[卷](/zh-cn/docs/concepts/storage/volumes/)概念。


## 介绍    {#introduction}

一个 `projected` 卷可以将若干现有的卷源映射到同一个目录之上。

目前，以下类型的卷源可以被投射：

* [`secret`](/zh-cn/docs/concepts/storage/volumes/#secret)
* [`downwardAPI`](/zh-cn/docs/concepts/storage/volumes/#downwardapi)
* [`configMap`](/zh-cn/docs/concepts/storage/volumes/#configmap)
* [`serviceAccountToken`](#serviceaccounttoken)

所有的卷源都要求处于 Pod 所在的同一个名字空间内。更多详细信息，
可参考[一体化卷](https://git.k8s.io/design-proposals-archive/node/all-in-one-volume.md)设计文档。

### 带有 Secret、DownwardAPI 和 ConfigMap 的配置示例 {#example-configuration-secret-downwardapi-configmap}

{{< codenew file="pods/storage/projected-secret-downwardapi-configmap.yaml" >}}

### 带有非默认权限模式设置的 Secret 的配置示例 {#example-configuration-secrets-nondefault-permission-mode}

{{< codenew file="pods/storage/projected-secrets-nondefault-permission-mode.yaml" >}}

每个被投射的卷源都列举在规约中的 `sources` 下面。参数几乎相同，只有两个例外：

* 对于 Secret，`secretName` 字段被改为 `name` 以便于 ConfigMap 的命名一致；
* `defaultMode` 只能在投射层级设置，不能在卷源层级设置。不过，正如上面所展示的，
  你可以显式地为每个投射单独设置 `mode` 属性。

## serviceAccountToken 投射卷 {#serviceaccounttoken}

你可以将当前[服务账号](/zh-cn/docs/reference/access-authn-authz/authentication/#service-account-tokens)的令牌注入到
Pod 中特定路径下。例如：

{{< codenew file="pods/storage/projected-service-account-token.yaml" >}}

示例 Pod 中包含一个投射卷，其中包含注入的服务账号令牌。
此 Pod 中的容器可以使用该令牌访问 Kubernetes API 服务器， 使用
[Pod 的 ServiceAccount](/zh-cn/docs/tasks/configure-pod-container/configure-service-account/)
进行身份验证。`audience` 字段包含令牌所针对的受众。
收到令牌的主体必须使用令牌受众中所指定的某个标识符来标识自身，否则应该拒绝该令牌。
此字段是可选的，默认值为 API 服务器的标识。

字段 `expirationSeconds` 是服务账号令牌预期的生命期长度。默认值为 1 小时，
必须至少为 10 分钟（600 秒）。管理员也可以通过设置 API 服务器的命令行参数
`--service-account-max-token-expiration` 来为其设置最大值上限。
`path` 字段给出与投射卷挂载点之间的相对路径。

{{< note >}}
以 [`subPath`](/zh-cn/docs/concepts/storage/volumes/#using-subpath)
形式使用投射卷源的容器无法收到对应卷源的更新。
{{< /note >}}

## 与 SecurityContext 间的关系    {#securitycontext-interactions}

关于在投射的服务账号卷中处理文件访问权限的[提案](https://git.k8s.io/enhancements/keps/sig-storage/2451-service-account-token-volumes#proposal)
介绍了如何使得所投射的文件具有合适的属主访问权限。

### Linux

在包含了投射卷并在
[`SecurityContext`](/zh-cn/docs/reference/kubernetes-api/workload-resources/pod-v1/#security-context)
中设置了 `RunAsUser` 属性的 Linux Pod 中，投射文件具有正确的属主属性设置，
其中包含了容器用户属主。

当 Pod 中的所有容器在其
[`PodSecurityContext`](/zh-cn/docs/reference/kubernetes-api/workload-resources/pod-v1/#security-context)
或容器
[`SecurityContext`](/zh-cn/docs/reference/kubernetes-api/workload-resources/pod-v1/#security-context-1)
中设置了相同的 `runAsUser` 时，kubelet 将确保 `serviceAccountToken`
卷的内容归该用户所有，并且令牌文件的权限模式会被设置为 `0600`。

{{< note >}}
在某 Pod 被创建后为其添加的{{< glossary_tooltip text="临时容器" term_id="ephemeral-container" >}}**不会**更改创建该
Pod 时设置的卷权限。

如果 Pod 的 `serviceAccountToken` 卷权限被设为 `0600`
是因为 Pod 中的其他所有容器都具有相同的 `runAsUser`，
则临时容器必须使用相同的 `runAsUser` 才能读取令牌。
{{< /note >}}

### Windows

在包含了投射卷并在 `SecurityContext` 中设置了 `RunAsUsername` 的 Windows Pod 中,
由于 Windows 中用户账号的管理方式问题，文件的属主无法正确设置。
Windows 在名为安全账号管理器（Security Account Manager，SAM）
的数据库中保存本地用户和组信息。每个容器会维护其自身的 SAM 数据库实例，
宿主系统无法窥视到容器运行期间数据库内容。Windows 容器被设计用来运行操作系统的用户态部分，
与宿主系统之间隔离，因此维护了一个虚拟的 SAM 数据库。
所以，在宿主系统上运行的 kubelet 无法动态为虚拟的容器账号配置宿主文件的属主。
如果需要将宿主机器上的文件与容器共享，建议将它们放到挂载于 `C:\` 之外的独立卷中。

默认情况下，所投射的文件会具有如下例所示的属主属性设置：

```powershell
PS C:\> Get-Acl C:\var\run\secrets\kubernetes.io\serviceaccount\..2021_08_31_22_22_18.318230061\ca.crt | Format-List

Path   : Microsoft.PowerShell.Core\FileSystem::C:\var\run\secrets\kubernetes.io\serviceaccount\..2021_08_31_22_22_18.318230061\ca.crt
Owner  : BUILTIN\Administrators
Group  : NT AUTHORITY\SYSTEM
Access : NT AUTHORITY\SYSTEM Allow  FullControl
         BUILTIN\Administrators Allow  FullControl
         BUILTIN\Users Allow  ReadAndExecute, Synchronize
Audit  :
Sddl   : O:BAG:SYD:AI(A;ID;FA;;;SY)(A;ID;FA;;;BA)(A;ID;0x1200a9;;;BU)
```

这意味着，所有类似 `ContainerAdministrator` 的管理员用户都具有读、写和执行访问权限，
而非管理员用户将具有读和执行访问权限。

{{< note >}}
总体而言，为容器授予访问宿主系统的权限这种做法是不推荐的，因为这样做可能会打开潜在的安全性攻击之门。

在创建 Windows Pod 时，如果在其 `SecurityContext` 中设置了 `RunAsUser`，
Pod 会一直阻塞在 `ContainerCreating` 状态。因此，建议不要在 Windows
节点上使用仅针对 Linux 的 `RunAsUser` 选项。
{{< /note >}}

