---
title: kubeadm upgrade
content_type: concept
weight: 40
---

`kubeadm upgrade` 是一个对用户友好的命令，它将复杂的升级逻辑包装在一个命令后面，支持升级的规划和实际执行。


## kubeadm upgrade 指南

[本文档](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)概述
使用 kubeadm 执行升级的步骤。
与 kubeadm 旧版本相关的文档，请参阅 Kubernetes 网站的旧版文档。

你可以使用 `kubeadm upgrade diff` 来查看将应用于静态 Pod 清单的更改。

在 Kubernetes v1.15.0 和更高版本中，`kubeadm upgrade apply` 和 `kubeadm upgrade node`
也将自动续订该节点上的 kubeadm 托管证书，包括存储在 kubeconfig 文件中的证书。
要选择退出，可以传递参数 `--certificate-renewal=false`。
有关证书续订的更多详细信息请参见[证书管理文档](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-certs)。


{{< note >}}
`kubeadm upgrade apply` 和 `kubeadm upgrade plan` 命令都具有遗留的 `--config` 标志，
可以在执行特定控制平面节点的规划或升级时重新配置集群。
请注意，升级工作流不是为这种情况而设计的，并且有意外结果的报告。
{{</ note >}}

## kubeadm upgrade plan {#cmd-upgrade-plan}
{{< include "generated/kubeadm_upgrade_plan.md" >}}

## kubeadm upgrade apply  {#cmd-upgrade-apply}
{{< include "generated/kubeadm_upgrade_apply.md" >}}

## kubeadm upgrade diff {#cmd-upgrade-diff}
{{< include "generated/kubeadm_upgrade_diff.md" >}}

## kubeadm upgrade node {#cmd-upgrade-node}
{{< include "generated/kubeadm_upgrade_node.md" >}}

## {{% heading "whatsnext" %}}

* 如果你使用 kubeadm v1.7.x 或更低版本初始化集群，则可以参考
  [kubeadm 配置](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-config/)
  配置集群用于 `kubeadm upgrade`。

