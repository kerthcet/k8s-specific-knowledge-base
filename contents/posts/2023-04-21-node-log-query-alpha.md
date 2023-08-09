---
layout: blog
title: "Kubernetes 1.27: 使用 Kubelet API 查询节点日志"
date: 2023-04-21
slug: node-log-query-alpha
---


**作者：** Aravindh Puthiyaparambil (Red Hat)

**译者：** Xin Li (DaoCloud)

Kubernetes 1.27 引入了一个名为**节点日志查询**的新功能，
可以查看节点上运行的服务的日志。

## 它解决了什么问题？

集群管理员在调试节点上运行的表现不正常的服务时会遇到问题。
他们通常必须通过 SSH 或 RDP 进入节点以查看服务日志以调试问题。
**节点日志查询**功能通过允许集群管理员使用 **kubectl**
查看日志的方式来帮助解决这种情况。这对于 Windows 节点特别有用，
在 Windows 节点中，你会遇到节点进入就绪状态但由于 CNI
错误配置和其他不易通过查看 Pod 状态来辨别的问题而导致容器无法启动的情况。

## 它是如何工作的？

kubelet 已经有一个 **/var/log/** 查看器，可以通过节点代理端点访问。
本功能特性通过一个隔离层对这个端点进行增强，在 Linux 节点上通过
`journalctl` Shell 调用获得日志，在 Windows 节点上通过 `Get-WinEvent` CmdLet 获取日志。
然后它使用命令提供的过滤器来过滤日志。kubelet 还使用启发式方法来检索日志。
如果用户不知道给定的系统服务是记录到文件还是本机系统记录器，
启发式方法首先检查本机操作系统记录器，如果不可用，它会尝试先从 `/var/log/<servicename>`
或 `/var/log/<servicename>.log` 或 `/var/log/<servicename>/<servicename>.log` 检索日志。


在 Linux 上，我们假设服务日志可通过 journald 获得，
并且安装了 `journalctl`。 在 Windows 上，我们假设服务日志在应用程序日志提供程序中可用。
另请注意，只有在你被授权的情况下才能获取节点日志（在 RBAC 中，
这是对 `nodes/proxy` 的 **get** 和 **create** 访问）。
获取节点日志所需的特权也允许特权提升攻击（elevation-of-privilege），
因此请谨慎管理它们。

## 该如何使用它

要使用该功能，请确保为该节点启用了 `NodeLogQuery`
[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)，
并且 kubelet 配置选项 `enableSystemLogHandler` 和 `enableSystemLogQuery` 都设置为 true。
然后，你可以查询所有节点或部分节点的日志。下面是一个从节点检索 kubelet 服务日志的示例：

```shell
# Fetch kubelet logs from a node named node-1.example
kubectl get --raw "/api/v1/nodes/node-1.example/proxy/logs/?query=kubelet"
```

你可以进一步过滤查询以缩小结果范围：

```shell
# Fetch kubelet logs from a node named node-1.example that have the word "error"
kubectl get --raw "/api/v1/nodes/node-1.example/proxy/logs/?query=kubelet&pattern=error"
```

你还可以从 Linux 节点上的 `/var/log/` 获取文件：

```shell
kubectl get --raw "/api/v1/nodes/<insert-node-name-here>/proxy/logs/?query=/<insert-log-file-name-here>"
```

你可以阅读[文档](/zh-cn/docs/concepts/cluster-administration/system-logs/#log-query)获取所有可用选项。

## 如何提供帮助

请使用该功能并通过在 GitHub 上登记问题或通过 Kubernetes Slack
的 [#sig-windows](https://kubernetes.slack.com/archives/C0SJ4AFB7) 频道
或 SIG Windows [邮件列表](https://groups.google.com/g/kubernetes-sig-windows)
联系我们来提供反馈。
