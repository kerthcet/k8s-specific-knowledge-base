---
title: Windows 节点的安全性
content_type: concept
weight: 40
---


本篇介绍特定于 Windows 操作系统的安全注意事项和最佳实践。


## 保护节点上的 Secret 数据   {#protection-for-secret-data-on-nodes}

在 Windows 上，来自 Secret 的数据以明文形式写入节点的本地存储
（与在 Linux 上使用 tmpfs / 内存中文件系统不同）。
作为集群操作员，你应该采取以下两项额外措施：

1. 使用文件 ACL 来保护 Secret 的文件位置。
2. 使用 [BitLocker](https://docs.microsoft.com/windows/security/information-protection/bitlocker/bitlocker-how-to-deploy-on-windows-server)
   进行卷级加密。

## 容器用户   {#container-users}

可以为 Windows Pod 或容器指定 [RunAsUsername](/zh-cn/docs/tasks/configure-pod-container/configure-runasusername)
以作为特定用户执行容器进程。这大致相当于 [RunAsUser](/zh-cn/docs/concepts/security/pod-security-policy/#users-and-groups)。

Windows 容器提供两个默认用户帐户，ContainerUser 和 ContainerAdministrator。
在微软的 **Windows 容器安全** 文档
[何时使用 ContainerAdmin 和 ContainerUser 用户帐户](https://docs.microsoft.com/zh-cn/virtualization/windowscontainers/manage-containers/container-security#when-to-use-containeradmin-and-containeruser-user-accounts)
中介绍了这两个用户帐户之间的区别。

在容器构建过程中，可以将本地用户添加到容器镜像中。

{{< note >}}
* 基于 [Nano Server](https://hub.docker.com/_/microsoft-windows-nanoserver) 的镜像默认以 `ContainerUser` 运行
* 基于 [Server Core](https://hub.docker.com/_/microsoft-windows-servercore) 的镜像默认以 `ContainerAdministrator` 运行
{{< /note >}}

Windows 容器还可以通过使用[组管理的服务账号](/zh-cn/docs/tasks/configure-pod-container/configure-gmsa/)作为
Active Directory 身份运行。

## Pod 级安全隔离   {#pod-level-security-isolation}

Windows 节点不支持特定于 Linux 的 Pod 安全上下文机制（例如 SELinux、AppArmor、Seccomp 或自定义 POSIX 权能字）。

Windows 上[不支持](/zh-cn/docs/concepts/windows/intro/#compatibility-v1-pod-spec-containers-securitycontext)特权容器。
然而，可以在 Windows 上使用 [HostProcess 容器](/zh-cn/docs/tasks/configure-pod-container/create-hostprocess-pod)来执行
Linux 上特权容器执行的许多任务。
