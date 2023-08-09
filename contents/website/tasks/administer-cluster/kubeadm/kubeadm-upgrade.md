---
title: 升级 kubeadm 集群
content_type: task
weight: 40
---


本页介绍如何将 `kubeadm` 创建的 Kubernetes 集群从 {{< skew currentVersionAddMinor -1 >}}.x 版本
升级到 {{< skew currentVersion >}}.x 版本以及从 {{< skew currentVersion >}}.x
升级到 {{< skew currentVersion >}}.y（其中 `y > x`）。略过次版本号的升级是
不被支持的。更多详情请访问[版本偏差策略](/zh-cn/releases/version-skew-policy/)。

要查看 kubeadm 创建的有关旧版本集群升级的信息，请参考以下页面：

- [将 kubeadm 集群从 {{< skew currentVersionAddMinor -2 >}} 升级到 {{< skew currentVersionAddMinor -1 >}}](https://v{{< skew currentVersionAddMinor -1 "-" >}}.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)
- [将 kubeadm 集群从 {{< skew currentVersionAddMinor -3 >}} 升级到 {{< skew currentVersionAddMinor -2 >}}](https://v{{< skew currentVersionAddMinor -2 "-" >}}.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)
- [将 kubeadm 集群从 {{< skew currentVersionAddMinor -4 >}} 升级到 {{< skew currentVersionAddMinor -3 >}}](https://v{{< skew currentVersionAddMinor -3 "-" >}}.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)
- [将 kubeadm 集群从 {{< skew currentVersionAddMinor -5 >}} 升级到 {{< skew currentVersionAddMinor -4 >}}](https://v{{< skew currentVersionAddMinor -4 "-" >}}.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)

升级工作的基本流程如下：

1. 升级主控制平面节点
1. 升级其他控制平面节点
1. 升级工作节点

## {{% heading "prerequisites" %}}

- 务必仔细认真阅读[发行说明](https://git.k8s.io/kubernetes/CHANGELOG)。
- 集群应使用静态的控制平面和 etcd Pod 或者外部 etcd。
- 务必备份所有重要组件，例如存储在数据库中应用层面的状态。
  `kubeadm upgrade` 不会影响你的工作负载，只会涉及 Kubernetes 内部的组件，但备份终究是好的。
- [必须禁用交换分区](https://serverfault.com/questions/684771/best-way-to-disable-swap-in-linux)。

### 附加信息   {#additional-information}

- 下述说明了在升级过程中何时腾空每个节点。如果你正在对任何 kubelet 进行小版本升级，
  你需要先腾空待升级的节点（或多个节点）。对于控制面节点，其上可能运行着 CoreDNS Pod
  或者其它非常重要的负载。更多信息见[腾空节点](/zh-cn/docs/tasks/administer-cluster/safely-drain-node/)。
- 升级后，因为容器规约的哈希值已更改，所有容器都会被重新启动。

- 要验证 kubelet 服务在升级后是否成功重启，可以执行 `systemctl status kubelet`
  或 `journalctl -xeu kubelet` 查看服务日志。
- 不建议使用 `kubeadm upgrade` 的 `--config` 参数和
  [kubeadm 配置 API 类型](/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3)来重新配置集群，
  这样会产生意想不到的结果。
  请按照[重新配置 kubeadm 集群](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-reconfigure)中的步骤来进行。


## 确定要升级到哪个版本   {#determine-which-version-to-upgrade-to}

使用操作系统的包管理器找到最新的补丁版本 Kubernetes {{< skew currentVersion >}}：

{{< tabs name="k8s_install_versions" >}}
{{% tab name="Ubuntu, Debian or HypriotOS" %}}
```shell
# 在列表中查找最新的 {{< skew currentVersion >}} 版本
# 它看起来应该是 {{< skew currentVersion >}}.x-00，其中 x 是最新的补丁版本
apt update
apt-cache madison kubeadm
```

{{% /tab %}}
{{% tab name="CentOS, RHEL or Fedora" %}}
```shell
# 在列表中查找最新的 {{< skew currentVersion >}} 版本
# 它看起来应该是 {{< skew currentVersion >}}.x-0，其中 x 是最新的补丁版本
yum list --showduplicates kubeadm --disableexcludes=kubernetes
```

{{% /tab %}}
{{< /tabs >}}

## 升级控制平面节点  {#upgrading-control-plane-nodes}

控制面节点上的升级过程应该每次处理一个节点。
首先选择一个要先行升级的控制面节点。该节点上必须拥有
`/etc/kubernetes/admin.conf` 文件。

### 执行 “kubeadm upgrade”   {#call-kubeadm-upgrade}

**对于第一个控制面节点**

1. 升级 kubeadm：

   {{< tabs name="k8s_install_kubeadm_first_cp" >}}
   {{% tab name="Ubuntu, Debian or HypriotOS" %}}

   ```shell
   # 用最新的补丁版本号替换 {{< skew currentVersion >}}.x-00 中的 x
   apt-mark unhold kubeadm && \
   apt-get update && apt-get install -y kubeadm={{< skew currentVersion >}}.x-00 && \
   apt-mark hold kubeadm
   ```

   {{% /tab %}}
   {{% tab name="CentOS, RHEL or Fedora" %}}

   ```shell
   # 用最新的补丁版本号替换 {{< skew currentVersion >}}.x-0 中的 x
   yum install -y kubeadm-{{< skew currentVersion >}}.x-0 --disableexcludes=kubernetes
   ```

   {{% /tab %}}
   {{< /tabs >}}

2. 验证下载操作正常，并且 kubeadm 版本正确：

   ```shell
   kubeadm version
   ```

3. 验证升级计划：

   ```shell
   kubeadm upgrade plan
   ```

   此命令检查你的集群是否可被升级，并取回你要升级的目标版本。
   命令也会显示一个包含组件配置版本状态的表格。

   {{< note >}}
   `kubeadm upgrade` 也会自动对 kubeadm 在节点上所管理的证书执行续约操作。
   如果需要略过证书续约操作，可以使用标志 `--certificate-renewal=false`。
   更多的信息，可参阅[证书管理指南](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-certs)。
   {{</ note >}}

   {{< note >}}
   如果 `kubeadm upgrade plan` 给出任何需要手动升级的组件配置，
   用户必须通过 `--config` 命令行标志向 `kubeadm upgrade apply` 命令提供替代的配置文件。
   如果不这样做，`kubeadm upgrade apply` 会出错并退出，不再执行升级操作。
   {{</ note >}}

4. 选择要升级到的目标版本，运行合适的命令。例如：

   ```shell
   # 将 x 替换为你为此次升级所选择的补丁版本号
   sudo kubeadm upgrade apply v{{< skew currentVersion >}}.x
   ```

   一旦该命令结束，你应该会看到：

   ```console
   [upgrade/successful] SUCCESS! Your cluster was upgraded to "v{{< skew currentVersion >}}.x". Enjoy!

   [upgrade/kubelet] Now that your control plane is upgraded, please proceed with upgrading your kubelets if you haven't already done so.
   ```

5. 手动升级你的 CNI 驱动插件。

   你的容器网络接口（CNI）驱动应该提供了程序自身的升级说明。
   参阅[插件](/zh-cn/docs/concepts/cluster-administration/addons/)页面查找你的 CNI 驱动，
   并查看是否需要其他升级步骤。

   如果 CNI 驱动作为 DaemonSet 运行，则在其他控制平面节点上不需要此步骤。

**对于其它控制面节点**

与第一个控制面节点相同，但是使用：

```shell
sudo kubeadm upgrade node
```

而不是：

```shell
sudo kubeadm upgrade apply
```

此外，不需要执行 `kubeadm upgrade plan` 和更新 CNI 驱动插件的操作。

### 腾空节点   {#drain-the-node}

将节点标记为不可调度并驱逐所有负载，准备节点的维护：

```shell
# 将 <node-to-drain> 替换为你要腾空的控制面节点名称
kubectl drain <node-to-drain> --ignore-daemonsets
```

### 升级 kubelet 和 kubectl   {#upgrade-kubelet-and-kubectl}

1. 升级 kubelet 和 kubectl：

   {{< tabs name="k8s_install_kubelet" >}}
   {{% tab name="Ubuntu, Debian or HypriotOS" %}}

   ```shell
   # 用最新的补丁版本替换 {{< skew currentVersion >}}.x-00 中的 x
   apt-mark unhold kubelet kubectl && \
   apt-get update && apt-get install -y kubelet={{< skew currentVersion >}}.x-00 kubectl={{< skew currentVersion >}}.x-00 && \
   apt-mark hold kubelet kubectl
   ```

   {{% /tab %}}
   {{% tab name="CentOS, RHEL or Fedora" %}}

   ```shell
   # 用最新的补丁版本号替换 {{< skew currentVersion >}}.x-00 中的 x
   yum install -y kubelet-{{< skew currentVersion >}}.x-0 kubectl-{{< skew currentVersion >}}.x-0 --disableexcludes=kubernetes
   ```

   {{% /tab %}}
   {{< /tabs >}}

2. 重启 kubelet：

   ```shell
   sudo systemctl daemon-reload
   sudo systemctl restart kubelet
   ```

### 解除节点的保护   {#uncordon-the-node}

通过将节点标记为可调度，让其重新上线：

```shell
# 将 <node-to-uncordon> 替换为你的节点名称
kubectl uncordon <node-to-uncordon>
```

## 升级工作节点   {#upgrade-worker-nodes}

工作节点上的升级过程应该一次执行一个节点，或者一次执行几个节点，
以不影响运行工作负载所需的最小容量。

以下内容演示如何升级 Linux 和 Windows 工作节点：

* [升级 Linux 节点](/zh-cn/docs/tasks/administer-cluster/kubeadm/upgrading-linux-nodes/)
* [升级 Windows 节点](/zh-cn/docs/tasks/administer-cluster/kubeadm/upgrading-windows-nodes/)

## 验证集群的状态   {#verify-the-status-of-the-cluster}

在所有节点上升级 kubelet 后，通过从 kubectl 可以访问集群的任何位置运行以下命令，
验证所有节点是否再次可用：

```shell
kubectl get nodes
```

`STATUS` 应显示所有节点为 `Ready` 状态，并且版本号已经被更新。

## 从故障状态恢复   {#recovering-from-a-failure-state}

如果 `kubeadm upgrade` 失败并且没有回滚，例如由于执行期间节点意外关闭，
你可以再次运行 `kubeadm upgrade`。
此命令是幂等的，并最终确保实际状态是你声明的期望状态。

要从故障状态恢复，你还可以运行 `kubeadm upgrade apply --force` 而无需更改集群正在运行的版本。

在升级期间，kubeadm 向 `/etc/kubernetes/tmp` 目录下的如下备份文件夹写入数据：

- `kubeadm-backup-etcd-<date>-<time>`
- `kubeadm-backup-manifests-<date>-<time>`

`kubeadm-backup-etcd` 包含当前控制面节点本地 etcd 成员数据的备份。
如果 etcd 升级失败并且自动回滚也无法修复，则可以将此文件夹中的内容复制到
`/var/lib/etcd` 进行手工修复。如果使用的是外部的 etcd，则此备份文件夹为空。

`kubeadm-backup-manifests` 包含当前控制面节点的静态 Pod 清单文件的备份版本。
如果升级失败并且无法自动回滚，则此文件夹中的内容可以复制到
`/etc/kubernetes/manifests` 目录实现手工恢复。
如果由于某些原因，在升级前后某个组件的清单未发生变化，则 kubeadm 也不会为之生成备份版本。

## 工作原理   {#how-it-works}

`kubeadm upgrade apply` 做了以下工作：

- 检查你的集群是否处于可升级状态:
  - API 服务器是可访问的
  - 所有节点处于 `Ready` 状态
  - 控制面是健康的
- 强制执行版本偏差策略。
- 确保控制面的镜像是可用的或可拉取到服务器上。
- 如果组件配置要求版本升级，则生成替代配置与/或使用用户提供的覆盖版本配置。
- 升级控制面组件或回滚（如果其中任何一个组件无法启动）。
- 应用新的 `CoreDNS` 和 `kube-proxy` 清单，并强制创建所有必需的 RBAC 规则。
- 如果旧文件在 180 天后过期，将创建 API 服务器的新证书和密钥文件并备份旧文件。

`kubeadm upgrade node` 在其他控制平节点上执行以下操作：

- 从集群中获取 kubeadm `ClusterConfiguration`。
- （可选操作）备份 kube-apiserver 证书。
- 升级控制平面组件的静态 Pod 清单。
- 为本节点升级 kubelet 配置

`kubeadm upgrade node` 在工作节点上完成以下工作：

- 从集群取回 kubeadm `ClusterConfiguration`。
- 为本节点升级 kubelet 配置。
