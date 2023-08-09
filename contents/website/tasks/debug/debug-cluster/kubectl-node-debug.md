---
title: 用 Kubectl 调试 Kubernetes 节点
content_type: task
min-kubernetes-server-version: 1.20
---


本页演示如何使用 `kubectl debug` 命令调试在 Kubernetes
集群上运行的[节点](/zh-cn/docs/concepts/architecture/nodes/)。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

你需要有权限创建 Pod 并将这些新 Pod 分配到任意节点。
你还需要被授权创建能够访问主机上文件系统的 Pod。


## 使用 `kubectl debug node` 调试节点  {#debugging-a-node-using-kubectl-debug-node}

使用 `kubectl debug node` 命令将 Pod 部署到要排查故障的节点上。
此命令在你无法使用 SSH 连接节点时比较有用。
当 Pod 被创建时，Pod 会在节点上打开一个交互的 Shell。
要在名为 “mynode” 的节点上创建一个交互式 Shell，运行：

```shell
kubectl debug node/mynode -it --image=ubuntu
```

```console
Creating debugging pod node-debugger-mynode-pdx84 with container debugger on node mynode.
If you don't see a command prompt, try pressing enter.
root@mynode:/#
```

调试命令有助于收集信息和排查问题。
你可能使用的命令包括 `ip`、`ifconfig`、`nc`、`ping` 和 `ps` 等等。
你还可以从各种包管理器安装 `mtr`、`tcpdump` 和 `curl` 等其他工具。

{{< note >}}
这些调试命令会因调试 Pod 所使用的镜像不同而有些差别，并且这些命令可能需要被安装。
{{< /note >}}

用于调试的 Pod 可以访问节点的根文件系统，该文件系统挂载在 Pod 中的 `/host` 路径。
如果你在 filesystem 名字空间中运行 kubelet，
则正调试的 Pod 将看到此名字空间的根，而不是整个节点的根。
对于典型的 Linux 节点，你可以查看以下路径找到一些重要的日志：

`/host/var/log/kubelet.log`
: 负责在节点上运行容器的 `kubelet` 所产生的日志。

`/host/var/log/kube-proxy.log`
: 负责将流量导向到 Service 端点的 `kube-proxy` 所产生的日志。

`/host/var/log/containerd.log`
: 在节点上运行的 `containerd` 进程所产生的日志。

`/host/var/log/syslog`
: 显示常规消息以及系统相关信息。

`/host/var/log/kern.log`
: 显示内核日志。

当在节点上创建一个调试会话时，需谨记：

* `kubectl debug` 根据节点的名称自动生成新 Pod 的名称。
* 节点的根文件系统将被挂载在 `/host`。
* 尽管容器运行在主机 IPC、Network 和 PID 名字空间中，但 Pod 没有特权。
  这意味着读取某些进程信息可能会失败，这是因为访问这些信息仅限于超级用户 (superuser)。
  例如，`chroot /host` 将失败。如果你需要一个有特权的 Pod，请手动创建。

## {{% heading "cleanup" %}}

当你使用正调试的 Pod 完成时，将其删除：

```shell
kubectl get pods
```

```none
NAME                          READY   STATUS       RESTARTS   AGE
node-debugger-mynode-pdx84    0/1     Completed    0          8m1s
```

```shell
# 相应更改 Pod 名称
kubectl delete pod node-debugger-mynode-pdx84 --now
```

```none
pod "node-debugger-mynode-pdx84" deleted
```

{{< note >}}
如果节点停机（网络断开或 kubelet 宕机且无法启动等），则 `kubectl debug node` 命令将不起作用。
这种情况下请检查[调试关闭/无法访问的节点](/zh-cn/docs/tasks/debug/debug-cluster/#example-debugging-a-down-unreachable-node)。
{{< /note >}}
