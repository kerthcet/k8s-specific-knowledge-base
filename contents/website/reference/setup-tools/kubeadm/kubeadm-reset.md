---
title: kubeadm reset
content_type: concept
weight: 60
---

该命令尽力还原由 `kubeadm init` 或 `kubeadm join` 所做的更改。


{{< include "generated/kubeadm_reset.md" >}}

### Reset 工作流程 {#reset-workflow}

`kubeadm reset` 负责从使用 `kubeadm init` 或 `kubeadm join` 命令创建的文件中清除节点本地文件系统。
对于控制平面节点，`reset` 还从 etcd 集群中删除该节点的本地 etcd Stacked 部署的成员。

`kubeadm reset phase` 可用于执行上述工作流程的各个阶段。
要跳过阶段列表，你可以使用 `--skip-phases` 参数，该参数的工作方式类似于 `kubeadm join` 和 `kubeadm init` 阶段运行器。

### 外部 etcd 清理

如果使用了外部 etcd，`kubeadm reset` 将不会删除任何 etcd 中的数据。这意味着，如果再次使用相同的 etcd 端点运行 `kubeadm init`，你将看到先前集群的状态。

要清理 etcd 中的数据，建议你使用 etcdctl 这样的客户端，例如：

```bash
etcdctl del "" --prefix
```

更多详情请参考 [etcd 文档](https://github.com/coreos/etcd/tree/master/etcdctl)。


## {{% heading "whatsnext" %}}

* 参考 [kubeadm init](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-init/) 来初始化 Kubernetes 主节点。
* 参考 [kubeadm join](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-join/) 来初始化 Kubernetes 工作节点并加入集群。

