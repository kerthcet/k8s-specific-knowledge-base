---
title: 使用 kubeadm API 定制组件
content_type: concept
weight: 40
---


本页面介绍了如何自定义 kubeadm 部署的组件。
你可以使用 `ClusterConfiguration` 结构中定义的参数，或者在每个节点上应用补丁来定制控制平面组件。
你可以使用 `KubeletConfiguration` 和 `KubeProxyConfiguration` 结构分别定制 kubelet 和 kube-proxy 组件。

所有这些选项都可以通过 kubeadm 配置 API 实现。
有关配置中的每个字段的详细信息，你可以导航到我们的
[API 参考页面](/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/) 。

{{< note >}}
kubeadm 目前不支持对 CoreDNS 部署进行定制。
你必须手动更新 `kube-system/coredns` {{< glossary_tooltip text="ConfigMap" term_id="configmap" >}}
并在更新后重新创建 CoreDNS {{< glossary_tooltip text="Pod" term_id="pod" >}}。
或者，你可以跳过默认的 CoreDNS 部署并部署你自己的 CoreDNS 变种。
有关更多详细信息，请参阅[在 kubeadm 中使用 init phase](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-init/#init-phases).
{{< /note >}}

{{< note >}}

要重新配置已创建的集群，请参阅[重新配置 kubeadm 集群](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-reconfigure)。
{{< /note >}}


## 使用 `ClusterConfiguration` 中的标志自定义控制平面   {#customizing-the-control-plane-with-flags-in-clusterconfiguration}

kubeadm `ClusterConfiguration` 对象为用户提供了一种方法，
用以覆盖传递给控制平面组件（如 APIServer、ControllerManager、Scheduler 和 Etcd）的默认参数。
各组件配置使用如下字段定义：

- `apiServer`
- `controllerManager`
- `scheduler`
- `etcd`

这些结构包含一个通用的 `extraArgs` 字段，该字段由 `key: value` 组成。
要覆盖控制平面组件的参数：

1.  将适当的字段 `extraArgs` 添加到配置中。
2.  向字段 `extraArgs` 添加要覆盖的参数值。
3.  用 `--config <YOUR CONFIG YAML>` 运行 `kubeadm init`。

{{< note >}}
你可以通过运行 `kubeadm config print init-defaults` 并将输出保存到你所选的文件中，
以默认值形式生成 `ClusterConfiguration` 对象。
{{< /note >}}

{{< note >}}
`ClusterConfiguration` 对象目前在 kubeadm 集群中是全局的。
这意味着你添加的任何标志都将应用于同一组件在不同节点上的所有实例。
要在不同节点上为每个组件应用单独的配置，你可以使用[补丁](#patches)。
{{< /note >}}

{{< note >}}
当前不支持重复的参数（keys）或多次传递相同的参数 `--foo`。
要解决此问题，你必须使用[补丁](#patches)。
{{< /note >}}

### APIServer 参数   {#apiserver-flags}

有关详细信息，请参阅 [kube-apiserver 参考文档](/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver/)。

使用示例：

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
kubernetesVersion: v1.16.0
apiServer:
  extraArgs:
    anonymous-auth: "false"
    enable-admission-plugins: AlwaysPullImages,DefaultStorageClass
    audit-log-path: /home/johndoe/audit.log
```

### ControllerManager 参数   {#controllermanager-flags}

有关详细信息，请参阅 [kube-controller-manager 参考文档](/zh-cn/docs/reference/command-line-tools-reference/kube-controller-manager/)。

使用示例：

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
kubernetesVersion: v1.16.0
controllerManager:
  extraArgs:
    cluster-signing-key-file: /home/johndoe/keys/ca.key
    deployment-controller-sync-period: "50"
```

## Scheduler 参数   {#scheduler-flags}

有关详细信息，请参阅 [kube-scheduler 参考文档](/zh-cn/docs/reference/command-line-tools-reference/kube-scheduler/)。

使用示例：

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
kubernetesVersion: v1.16.0
scheduler:
  extraArgs:
    config: /etc/kubernetes/scheduler-config.yaml
  extraVolumes:
    - name: schedulerconfig
      hostPath: /home/johndoe/schedconfig.yaml
      mountPath: /etc/kubernetes/scheduler-config.yaml
      readOnly: true
      pathType: "File"
```
### Etcd 参数   {#etcd-flags} 

有关详细信息，请参阅 [etcd 服务文档](https://etcd.io/docs/).

使用示例：

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
etcd:
  local:
    extraArgs:
      election-timeout: 1000
```
## 使用补丁定制   {#patches}

{{< feature-state for_k8s_version="v1.22" state="beta" >}}

Kubeadm 允许将包含补丁文件的目录传递给各个节点上的 `InitConfiguration` 和 `JoinConfiguration`。
这些补丁可被用作组件配置写入磁盘之前的最后一个自定义步骤。

可以使用 `--config <你的 YAML 格式控制文件>` 将配置文件传递给 `kubeadm init`：

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
patches:
  directory: /home/user/somedir
```

{{< note >}}
对于 `kubeadm init`，你可以传递一个包含 `ClusterConfiguration` 和 `InitConfiguration` 的文件，以 `---` 分隔。
{{< /note >}}

你可以使用 `--config <你的 YAML 格式配置文件>` 将配置文件传递给 `kubeadm join`：

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: JoinConfiguration
patches:
  directory: /home/user/somedir
```

补丁目录必须包含名为 `target[suffix][+patchtype].extension` 的文件。
例如，`kube-apiserver0+merge.yaml` 或只是 `etcd.json`。

- `target` 可以是 `kube-apiserver`、`kube-controller-manager`、`kube-scheduler`、`etcd` 和 `kubeletconfiguration` 之一。
- `patchtype` 可以是 `strategy`、`merge` 或 `json` 之一，并且这些必须匹配
  [kubectl 支持](/zh-cn/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch) 的补丁格式。
  默认补丁类型是 `strategic` 的。
- `extension` 必须是 `json` 或 `yaml`。
- `suffix` 是一个可选字符串，可用于确定首先按字母数字应用哪些补丁。

{{< note >}}
如果你使用 `kubeadm upgrade` 升级 kubeadm 节点，你必须再次提供相同的补丁，以便在升级后保留自定义配置。
为此，你可以使用 `--patches` 参数，该参数必须指向同一目录。 `kubeadm upgrade` 目前不支持用于相同目的的 API 结构配置。
{{< /note >}}

## 自定义 kubelet  {#kubelet}

要自定义 kubelet，你可以在同一配置文件中的 `ClusterConfiguration` 或 `InitConfiguration`
之外添加一个 [`KubeletConfiguration`](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/)，用 `---` 分隔。
然后可以将此文件传递给 `kubeadm init`，kubeadm 会将相同的
`KubeletConfiguration` 配置应用于集群中的所有节点。

要在基础 `KubeletConfiguration` 上应用特定节点的配置，你可以使用
[`kubeletconfiguration` 补丁定制](#patches)。

或者你可以使用 `kubelet` 参数进行覆盖，方法是将它们传递到 `InitConfiguration` 和 `JoinConfiguration` 
支持的 `nodeRegistration.kubeletExtraArgs` 字段中。一些 kubelet 参数已被弃用，
因此在使用这些参数之前，请在 [kubelet 参考文档](/zh-cn/docs/reference/command-line-tools-reference/kubelet) 中检查它们的状态。


更多详情，请参阅[使用 kubeadm 配置集群中的每个 kubelet](/zh-cn/docs/setup/production-environment/tools/kubeadm/kubelet-integration)

## 自定义 kube-proxy   {#customizing-kube-proxy}

要自定义 kube-proxy，你可以在 `ClusterConfiguration` 或 `InitConfiguration`
之外添加一个由 `---` 分隔的 `KubeProxyConfiguration`， 传递给 `kubeadm init`。

可以导航到 [API 参考页面](/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/)查看更多详情，

{{< note >}}
kubeadm 将 kube-proxy 部署为 {{< glossary_tooltip text="DaemonSet" term_id="daemonset" >}}，
这意味着 `KubeProxyConfiguration` 将应用于集群中的所有 kube-proxy 实例。
{{< /note >}}


