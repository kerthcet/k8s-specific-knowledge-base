---
title: 重新配置 kubeadm 集群
content_type: task
weight: 30
---

kubeadm 不支持自动重新配置部署在托管节点上的组件的方式。 
一种自动化的方法是使用自定义的 
[operator](/zh-cn/docs/concepts/extend-kubernetes/operator/)。

要修改组件配置，你必须手动编辑磁盘上关联的集群对象和文件。
本指南展示了实现 kubeadm 集群重新配置所需执行的正确步骤顺序。

## {{% heading "prerequisites" %}}

- 你需要一个使用 kubeadm 部署的集群
- 拥有管理员凭据（`/etc/kubernetes/admin.conf`）
  和从安装了 kubectl 的主机到集群中正在运行的 kube-apiserver 的网络连接
- 在所有主机上安装文本编辑器


## 重新配置集群

kubeadm 在 ConfigMap 和其他对象中写入了一组集群范围的组件配置选项。 
这些对象必须手动编辑，可以使用命令 `kubectl edit`。

`kubectl edit` 命令将打开一个文本编辑器，你可以在其中直接编辑和保存对象。
你可以使用环境变量 `KUBECONFIG` 和 `KUBE_EDITOR` 来指定 kubectl
使用的 kubeconfig 文件和首选文本编辑器的位置。

例如：
```
KUBECONFIG=/etc/kubernetes/admin.conf KUBE_EDITOR=nano kubectl edit <parameters>
```

{{< note >}}
保存对这些集群对象的任何更改后，节点上运行的组件可能不会自动更新。 
以下步骤将指导你如何手动执行该操作。
{{< /note >}}

{{< warning >}}

ConfigMaps 中的组件配置存储为非结构化数据（YAML 字符串）。 这意味着在更新
ConfigMap 的内容时不会执行验证。 你必须小心遵循特定组件配置的文档化 API 格式， 
并避免引入拼写错误和 YAML 缩进错误。
{{< /warning >}}

### 应用集群配置更改

#### 更新 `ClusterConfiguration`

在集群创建和升级期间，kubeadm 将其
[`ClusterConfiguration`](/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/)
写入 `kube-system` 命名空间中名为 `kubeadm-config` 的 ConfigMap。

要更改 `ClusterConfiguration` 中的特定选项，你可以使用以下命令编辑 ConfigMap：

```shell
kubectl edit cm -n kube-system kubeadm-config
```

配置位于 `data.ClusterConfiguration` 键下。

{{< note >}}
`ClusterConfiguration` 包括各种影响单个组件配置的选项， 例如
kube-apiserver、kube-scheduler、kube-controller-manager、
CoreDNS、etcd 和 kube-proxy。 对配置的更改必须手动反映在节点组件上。
{{< /note >}}

#### 在控制平面节点上反映 `ClusterConfiguration` 更改

kubeadm 将控制平面组件作为位于 `/etc/kubernetes/manifests`
目录中的静态 Pod 清单进行管理。
对 `apiServer`、`controllerManager`、`scheduler` 或 `etcd`键下的
`ClusterConfiguration` 的任何更改都必须反映在控制平面节点上清单目录中的关联文件中。


此类更改可能包括:
- `extraArgs` - 需要更新传递给组件容器的标志列表
- `extraMounts` - 需要更新组件容器的卷挂载
- `*SANs` - 需要使用更新的主题备用名称编写新证书

在继续进行这些更改之前，请确保你已备份目录 `/etc/kubernetes/`。


要编写新证书，你可以使用：

```shell
kubeadm init phase certs <component-name> --config <config-file>
```

要在 `/etc/kubernetes/manifests` 中编写新的清单文件，你可以使用：

```shell
kubeadm init phase control-plane <component-name> --config <config-file>
```

`<config-file>` 内容必须与更新后的 `ClusterConfiguration` 匹配。
`<component-name>` 值必须是组件的名称。

{{< note >}}
更新 `/etc/kubernetes/manifests` 中的文件将告诉 kubelet 重新启动相应组件的静态 Pod。
尝试一次对一个节点进行这些更改，以在不停机的情况下离开集群。
{{< /note >}}

### 应用 kubelet 配置更改

#### 更新 `KubeletConfiguration`

在集群创建和升级期间，kubeadm 将其 
[`KubeletConfiguration`](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/) 
写入 `kube-system` 命名空间中名为 `kubelet-config` 的 ConfigMap。
你可以使用以下命令编辑 ConfigMap：

```shell
kubectl edit cm -n kube-system kubelet-config
```

配置位于 `data.kubelet` 键下。

#### 反映 kubelet 的更改

要反映 kubeadm 节点上的更改，你必须执行以下操作：

- 登录到 kubeadm 节点
- 运行 `kubeadm upgrade node phase kubelet-config` 下载最新的
  `kubelet-config` ConfigMap 内容到本地文件 `/var/lib/kubelet/config.conf`
- 编辑文件 `/var/lib/kubelet/kubeadm-flags.env` 以使用标志来应用额外的配置
- 使用 `systemctl restart kubelet` 重启 kubelet 服务

{{< note >}}
一次执行一个节点的这些更改，以允许正确地重新安排工作负载。
{{< /note >}}

{{< note >}}
在 `kubeadm upgrade` 期间，kubeadm 从 `kubelet-config` ConfigMap
下载 `KubeletConfiguration` 并覆盖 `/var/lib/kubelet/config.conf` 的内容。
这意味着节点本地配置必须通过`/var/lib/kubelet/kubeadm-flags.env`中的标志或在
kubeadm upgrade` 后手动更新`/var/lib/kubelet/config.conf`的内容来应用，然后重新启动 kubelet。
{{< /note >}}

### 应用 kube-proxy 配置更改

#### 更新 `KubeProxyConfiguration`

在集群创建和升级期间，kubeadm 将其写入
[`KubeProxyConfiguration`](/zh-cn/docs/reference/config-api/kube-proxy-config.v1alpha1/) 
在名为 `kube-proxy` 的 `kube-system` 命名空间中的 ConfigMap 中。

此 ConfigMap 由 `kube-system` 命名空间中的 `kube-proxy` DaemonSet 使用。

要更改 `KubeProxyConfiguration` 中的特定选项，你可以使用以下命令编辑 ConfigMap：

```shell
kubectl edit cm -n kube-system kube-proxy
```

配置位于 `data.config.conf` 键下。

#### 反映 kube-proxy 的更改

更新 `kube-proxy` ConfigMap 后，你可以重新启动所有 kube-proxy Pod：

获取 Pod 名称：

```shell
kubectl get po -n kube-system | grep kube-proxy
```

使用以下命令删除 Pod：

```shell
kubectl delete po -n kube-system <pod-name>
```

将创建使用更新的 ConfigMap 的新 Pod。

{{< note >}}
由于 kubeadm 将 kube-proxy 部署为 DaemonSet，因此不支持特定于节点的配置。
{{< /note >}}

### 应用 CoreDNS 配置更改

#### 更新 CoreDNS 的 Deployment 和 Service

kubeadm 将 CoreDNS 部署为名为 `coredns` 的 Deployment，并使用 Service `kube-dns`，
两者都在 `kube-system` 命名空间中。

要更新任何 CoreDNS 设置，你可以编辑 Deployment 和 Service：


```shell
kubectl edit deployment -n kube-system coredns
kubectl edit service -n kube-system kube-dns
```

#### 反映 CoreDNS 的更改

应用 CoreDNS 更改后，你可以删除 CoreDNS Pod。

获取 Pod 名称：

```shell
kubectl get po -n kube-system | grep coredns
```

使用以下命令删除 Pod：

```shell
kubectl delete po -n kube-system <pod-name>
```

将创建具有更新的 CoreDNS 配置的新 Pod。

{{< note >}}
kubeadm 不允许在集群创建和升级期间配置 CoreDNS。
这意味着如果执行了 `kubeadm upgrade apply`，你对 
CoreDNS 对象的更改将丢失并且必须重新应用。
{{< /note >}}

## 持久化重新配置

在受管节点上执行 `kubeadm upgrade` 期间，kubeadm 
可能会覆盖在创建集群（重新配置）后应用的配置。

### 持久化 Node 对象重新配置

kubeadm 在特定 Kubernetes 节点的 Node 对象上写入标签、污点、CRI 
套接字和其他信息。要更改此 Node 对象的任何内容，你可以使用：

```shell
kubectl edit no <node-name>
```

在 `kubeadm upgrade` 期间，此类节点的内容可能会被覆盖。
如果你想在升级后保留对 Node 对象的修改，你可以准备一个
[kubectl patch](/zh-cn/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch/)
并将其应用到 Node 对象：

```shell
kubectl patch no <node-name> --patch-file <patch-file>
```

#### 持久化控制平面组件重新配置

控制平面配置的主要来源是存储在集群中的 `ClusterConfiguration` 对象。
要扩展静态 Pod 清单配置，可以使用 
[patches](/zh-cn/docs/setup/production-environment/tools/kubeadm/control-plane-flags/#patches)。

这些补丁文件必须作为文件保留在控制平面节点上，以确保它们可以被 
`kubeadm upgrade ... --patches <directory>` 使用。

如果对 `ClusterConfiguration` 和磁盘上的静态 Pod 清单进行了重新配置，则必须相应地更新节点特定补丁集。

#### 持久化 kubelet 重新配置

对存储在 `/var/lib/kubelet/config.conf` 中的 `KubeletConfiguration` 
所做的任何更改都将在 `kubeadm upgrade` 时因为下载集群范围内的 `kubelet-config`
ConfigMap 的内容而被覆盖。
要持久保存 kubelet 节点特定的配置，文件`/var/lib/kubelet/config.conf` 
必须在升级后手动更新，或者文件`/var/lib/kubelet/kubeadm-flags.env` 可以包含标志。
kubelet 标志会覆盖相关的 `KubeletConfiguration` 选项，但请注意，有些标志已被弃用。

更改 `/var/lib/kubelet/config.conf` 或 `/var/lib/kubelet/kubeadm-flags.env` 
后需要重启 kubelet。


## {{% heading "whatsnext" %}}

- [升级 kubeadm 集群](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade)
- [使用 kubeadm API 自定义组件](/zh-cn/docs/setup/production-environment/tools/kubeadm/control-plane-flags)
- [使用 kubeadm 管理证书](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-certs)
- [进一步了解 kubeadm 设置](/zh-cn/docs/reference/setup-tools/kubeadm/)
