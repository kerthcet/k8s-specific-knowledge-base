---
title: 升级 Windows 节点
min-kubernetes-server-version: 1.17
content_type: task
weight: 110
---


{{< feature-state for_k8s_version="v1.18" state="beta" >}}

本页解释如何升级用 kubeadm 创建的 Windows 节点。

## {{% heading "prerequisites" %}}
 
{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

* 熟悉[更新 kubeadm 集群中的其余组件](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade)。
  在升级你的 Windows 节点之前你会想要升级控制面节点。

## 升级工作节点   {#upgrading-worker-nodes}

### 升级 kubeadm    {#upgrade-kubeadm}

1. 在 Windows 节点上升级 kubeadm：

   ```powershell
   # 将 {{< skew currentPatchVersion >}} 替换为你希望的版本
   curl.exe -Lo <kubeadm.exe 路径>  "https://dl.k8s.io/v{{< skew currentPatchVersion >}}/bin/windows/amd64/kubeadm.exe"
   ```

### 腾空节点   {#drain-the-node}

1. 在一个能访问到 Kubernetes API 的机器上，将 Windows 节点标记为不可调度并
   驱逐其上的所有负载，以便准备节点维护操作：

   ```shell
   # 将 <要腾空的节点> 替换为你要腾空的节点的名称
   kubectl drain <要腾空的节点> --ignore-daemonsets
   ```

   你应该会看到类似下面的输出：

   ```
   node/ip-172-31-85-18 cordoned
   node/ip-172-31-85-18 drained
   ```

### 升级 kubelet 配置   {#upgrade-the-kubelet-configuration}

1. 在 Windows 节点上，执行下面的命令来同步新的 kubelet 配置：

   ```powershell
   kubeadm upgrade node
   ```

### 升级 kubelet 和 kube-proxy   {#upgrade-kubelet-and-kube-proxy}

1. 在 Windows 节点上升级并重启 kubelet：

   ```powershell
   stop-service kubelet
   curl.exe -Lo <kubelet.exe 路径> "https://dl.k8s.io/v{{< skew currentPatchVersion >}}/bin/windows/amd64/kubelet.exe"
   restart-service kubelet
   ```

2. 在 Windows 节点上升级并重启 kube-proxy：

   ```powershell
   stop-service kube-proxy
   curl.exe -Lo <kube-proxy.exe 路径> "https://dl.k8s.io/v{{< skew currentPatchVersion >}}/bin/windows/amd64/kube-proxy.exe"
   restart-service kube-proxy
   ```

{{< note >}}
如果你是在 Pod 内的 HostProcess 容器中运行 kube-proxy，而不是作为 Windows 服务，
你可以通过应用更新版本的 kube-proxy 清单文件来升级 kube-proxy。
{{< /note >}}

### 对节点执行 uncordon 操作   {#uncordon-the-node}

1. 从一台能够访问到 Kubernetes API 的机器上，通过将节点标记为可调度，使之
   重新上线：

   ```shell
   # 将 <要腾空的节点> 替换为你的节点名称
   kubectl uncordon <要腾空的节点>
   ```

## {{% heading "whatsnext" %}}


* 查看如何[升级 Linux 节点](/zh-cn/docs/tasks/administer-cluster/kubeadm/upgrading-linux-nodes/)。