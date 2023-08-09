---
title: kubeadm join phase
weight: 90
---


`kubeadm join phase` 使你能够调用 `join` 过程的基本原子步骤。
因此，如果希望执行自定义操作，可以让 kubeadm 做一些工作，然后由用户来补足剩余操作。

`kubeadm join phase` 与
[kubeadm join 工作流程](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-join/#join-workflow)
一致，后台都使用相同的代码。

## kubeadm join phase {#cmd-join-phase}

{{< tabs name="tab-phase" >}}
{{< tab name="phase" include="generated/kubeadm_join_phase.md" />}}
{{< /tabs >}}

## kubeadm join phase preflight {#cmd-join-phase-preflight}

使用此命令可以在即将加入集群的节点上执行启动前检查。

{{< tabs name="tab-preflight" >}}
{{< tab name="preflight" include="generated/kubeadm_join_phase_preflight.md" />}}
{{< /tabs >}}

## kubeadm join phase control-plane-prepare {#cmd-join-phase-control-plane-prepare}

使用此阶段，你可以准备一个作为控制平面的节点。

{{< tabs name="tab-control-plane-prepare" >}}
{{< tab name="control-plane-prepare" include="generated/kubeadm_join_phase_control-plane-prepare.md" />}}
{{< tab name="all" include="generated/kubeadm_join_phase_control-plane-prepare_all.md" />}}
{{< tab name="download-certs" include="generated/kubeadm_join_phase_control-plane-prepare_download-certs.md" />}}
{{< tab name="certs" include="generated/kubeadm_join_phase_control-plane-prepare_certs.md" />}}
{{< tab name="kubeconfig" include="generated/kubeadm_join_phase_control-plane-prepare_kubeconfig.md" />}}
{{< tab name="control-plane" include="generated/kubeadm_join_phase_control-plane-prepare_control-plane.md" />}}
{{< /tabs >}}

## kubeadm join phase kubelet-start {#cmd-join-phase-kubelet-start}

使用此阶段，你可以配置 kubelet 设置、证书和（重新）启动 kubelet。

{{< tabs name="tab-kubelet-start" >}}
{{< tab name="kubelet-start" include="generated/kubeadm_join_phase_kubelet-start.md" />}}
{{< /tabs >}}

## kubeadm join phase control-plane-join {#cmd-join-phase-control-plane-join}

使用此阶段，你可以将节点作为控制平面实例加入。

{{< tabs name="tab-control-plane-join" >}}
{{< tab name="control-plane-join" include="generated/kubeadm_join_phase_control-plane-join.md" />}}
{{< tab name="all" include="generated/kubeadm_join_phase_control-plane-join_all.md" />}}
{{< tab name="etcd" include="generated/kubeadm_join_phase_control-plane-join_etcd.md" />}}
{{< tab name="update-status" include="generated/kubeadm_join_phase_control-plane-join_update-status.md" />}}
{{< tab name="mark-control-plane" include="generated/kubeadm_join_phase_control-plane-join_mark-control-plane.md" />}}
{{< /tabs >}}

## {{% heading "whatsnext" %}}

* [kubeadm init](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-init/)
  引导 Kubernetes 控制平面节点
* [kubeadm join](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-join/)
  将节点添加到集群
* [kubeadm reset](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-reset/)
  恢复通过 `kubeadm init` 或 `kubeadm join` 操作对主机所做的任何更改
* [kubeadm alpha](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-alpha/)
  尝试实验性功能
