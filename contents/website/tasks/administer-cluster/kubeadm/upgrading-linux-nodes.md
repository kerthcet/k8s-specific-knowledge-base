---
title: 升级 Linux 节点
content_type: task
weight: 100
---


本页讲述了如何升级用 kubeadm 创建的 Linux 工作节点。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

* 你自己要熟悉[升级剩余 kubeadm 集群的过程](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade)。
  你需要先升级控制面节点，再升级 Linux 工作节点。


## 升级工作节点   {#upgrading-worker-nodes}

### 升级 kubeadm   {#upgrade-kubeadm}

升级 kubeadm：

{{< tabs name="k8s_install_kubeadm_worker_nodes" >}}
{{% tab name="Ubuntu、Debian 或 HypriotOS" %}}
```shell
# 将 {{< skew currentVersion >}}.x-00 中的 x 替换为最新的补丁版本
apt-mark unhold kubeadm && \
apt-get update && apt-get install -y kubeadm={{< skew currentVersion >}}.x-00 && \
apt-mark hold kubeadm
```
{{% /tab %}}
{{% tab name="CentOS、RHEL 或 Fedora" %}}
```shell
# 将 {{< skew currentVersion >}}.x-0 中的 x 替换为最新的补丁版本
yum install -y kubeadm-{{< skew currentVersion >}}.x-0 --disableexcludes=kubernetes
```
{{% /tab %}}
{{< /tabs >}}

### 执行 "kubeadm upgrade"    {#call-kubeadm-upgrade}

对于工作节点，下面的命令会升级本地的 kubelet 配置：

```shell
sudo kubeadm upgrade node
```

### 腾空节点   {#drain-node}

将节点标记为不可调度并驱逐所有负载，准备节点的维护：

```shell
# 将 <node-to-drain> 替换为你正腾空的节点的名称
kubectl drain <node-to-drain> --ignore-daemonsets
```

### 升级 kubelet 和 kubectl   {#upgrade-kubelet-and-kubectl}

1. 升级 kubelet 和 kubectl:

   {{< tabs name="k8s_kubelet_and_kubectl" >}}
   {{% tab name="Ubuntu、Debian 或 HypriotOS" %}}
   ```shell
   # 将 {{< skew currentVersion >}}.x-00 中的 x 替换为最新的补丁版本
   apt-mark unhold kubelet kubectl && \
   apt-get update && apt-get install -y kubelet={{< skew currentVersion >}}.x-00 kubectl={{< skew currentVersion >}}.x-00 && \
   apt-mark hold kubelet kubectl
   ```
   {{% /tab %}}
   {{% tab name="CentOS、RHEL 或 Fedora" %}}
   ```shell
   # 将 {{< skew currentVersion >}}.x-0 中的 x 替换为最新的补丁版本
   yum install -y kubelet-{{< skew currentVersion >}}.x-0 kubectl-{{< skew currentVersion >}}.x-0 --disableexcludes=kubernetes
   ```
   {{% /tab %}}
   {{< /tabs >}}

2. 重启 kubelet：

   ```shell
   sudo systemctl daemon-reload
   sudo systemctl restart kubelet
   ```

### 取消对节点的保护   {#uncordon-node}

通过将节点标记为可调度，让节点重新上线：

```shell
# 将 <node-to-uncordon> 替换为你的节点名称
kubectl uncordon <node-to-uncordon>
```

## {{% heading "whatsnext" %}}

* 查阅如何[升级 Windows 节点](/zh-cn/docs/tasks/administer-cluster/kubeadm/upgrading-windows-nodes/)。
