---
title: kubeadm upgrade phase
weight: 90
content_type: concept
---

在 Kubernetes v1.15.0 版本中，kubeadm 引入了对 `kubeadm upgrade node` 阶段的初步支持。其他 `kubeadm upgrade` 子命令如 `apply` 等阶段将在未来发行版中添加。


## kubeadm upgrade node phase {#cmd-node-phase}


使用此阶段，可以选择执行辅助控制平面或工作节点升级的单独步骤。请注意，`kubeadm upgrade apply` 命令仍然必须在主控制平面节点上调用。

{{< tabs name="tab-phase" >}}
{{< tab name="phase" include="generated/kubeadm_upgrade_node_phase.md" />}}
{{< tab name="preflight" include="generated/kubeadm_upgrade_node_phase_preflight.md" />}}
{{< tab name="control-plane" include="generated/kubeadm_upgrade_node_phase_control-plane.md" />}}
{{< tab name="kubelet-config" include="generated/kubeadm_upgrade_node_phase_kubelet-config.md" />}}
{{< /tabs >}}

## {{% heading "whatsnext" %}}

* [kubeadm init](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-init/) 引导一个 Kubernetes 控制平面节点
* [kubeadm join](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-join/) 将节点加入到集群
* [kubeadm reset](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-reset/) 还原 `kubeadm init` 或 `kubeadm join` 命令对主机所做的任何更改
* [kubeadm upgrade](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-upgrade/) 升级 kubeadm 节点
* [kubeadm alpha](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-alpha/) 尝试实验性功能
