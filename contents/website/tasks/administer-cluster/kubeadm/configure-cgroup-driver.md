---
title: 配置 cgroup 驱动
content_type: task
weight: 20
---


本页阐述如何配置 kubelet 的 cgroup 驱动以匹配 kubeadm 集群中的容器运行时的 cgroup 驱动。

## {{% heading "prerequisites" %}}

你应该熟悉 Kubernetes 的[容器运行时需求](/zh-cn/docs/setup/production-environment/container-runtimes)。


## 配置容器运行时 cgroup 驱动 {#configuring-the-container-runtime-cgroup-driver}

[容器运行时](/zh-cn/docs/setup/production-environment/container-runtimes)页面提到，
由于 kubeadm 把 kubelet 视为一个
[系统服务](/zh-cn/docs/setup/production-environment/tools/kubeadm/kubelet-integration)来管理，
所以对基于 kubeadm 的安装， 我们推荐使用 `systemd` 驱动，
不推荐 kubelet [默认](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1)的 `cgroupfs` 驱动。

此页还详述了如何安装若干不同的容器运行时，并将 `systemd` 设为其默认驱动。

## 配置 kubelet 的 cgroup 驱动

kubeadm 支持在执行 `kubeadm init` 时，传递一个 `KubeletConfiguration` 结构体。
`KubeletConfiguration` 包含 `cgroupDriver` 字段，可用于控制 kubelet 的 cgroup 驱动。


{{< note >}}
在版本 1.22 及更高版本中，如果用户没有在 `KubeletConfiguration` 中设置 `cgroupDriver` 字段，
`kubeadm` 会将它设置为默认值 `systemd`。
{{< /note >}}

这是一个最小化的示例，其中显式的配置了此字段：

```yaml
# kubeadm-config.yaml
kind: ClusterConfiguration
apiVersion: kubeadm.k8s.io/v1beta3
kubernetesVersion: v1.21.0
---
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
cgroupDriver: systemd
```

这样一个配置文件就可以传递给 kubeadm 命令了：

```shell
kubeadm init --config kubeadm-config.yaml
```

{{< note >}}
Kubeadm 对集群所有的节点，使用相同的 `KubeletConfiguration`。
`KubeletConfiguration` 存放于 `kube-system` 命名空间下的某个 
[ConfigMap](/zh-cn/docs/concepts/configuration/configmap) 对象中。

执行 `init`、`join` 和 `upgrade` 等子命令会促使 kubeadm 
将 `KubeletConfiguration` 写入到文件 `/var/lib/kubelet/config.yaml` 中，
继而把它传递给本地节点的 kubelet。

{{< /note >}}

# 使用 `cgroupfs` 驱动

如仍需使用 `cgroupfs` 且要防止 `kubeadm upgrade` 修改现有系统中
`KubeletConfiguration` 的 cgroup 驱动，你必须显式声明它的值。
此方法应对的场景为：在将来某个版本的 kubeadm 中，你不想使用默认的 `systemd` 驱动。

参阅以下章节“[修改 kubelet 的 ConfigMap](#modify-the-kubelet-configmap) ”，了解显式设置该值的方法。

如果你希望配置容器运行时来使用 `cgroupfs` 驱动，
则必须参考所选容器运行时的文档。

## 迁移到 `systemd` 驱动

要将现有 kubeadm 集群的 cgroup 驱动从 `cgroupfs` 就地升级为 `systemd`，
需要执行一个与 kubelet 升级类似的过程。
该过程必须包含下面两个步骤：

{{< note >}}
还有一种方法，可以用已配置了 `systemd` 的新节点替换掉集群中的老节点。
按这种方法，在加入新节点、确保工作负载可以安全迁移到新节点、及至删除旧节点这一系列操作之前，
只需执行以下第一个步骤。
{{< /note >}}

### 修改 kubelet 的 ConfigMap  {#modify-the-kubelet-configmap}

- 运行 `kubectl edit cm kubelet-config -n kube-system`。
- 修改现有 `cgroupDriver` 的值，或者新增如下式样的字段：

  ```yaml
  cgroupDriver: systemd
  ```
  该字段必须出现在 ConfigMap 的 `kubelet:` 小节下。

### 更新所有节点的 cgroup 驱动

对于集群中的每一个节点：

- 执行命令 `kubectl drain <node-name> --ignore-daemonsets`，以
  [腾空节点](/zh-cn/docs/tasks/administer-cluster/safely-drain-node)
- 执行命令 `systemctl stop kubelet`，以停止 kubelet
- 停止容器运行时
- 修改容器运行时 cgroup 驱动为 `systemd`
- 在文件 `/var/lib/kubelet/config.yaml` 中添加设置 `cgroupDriver: systemd`
- 启动容器运行时
- 执行命令 `systemctl start kubelet`，以启动 kubelet
- 执行命令 `kubectl uncordon <node-name>`，以
  [取消节点隔离](/zh-cn/docs/tasks/administer-cluster/safely-drain-node)

在节点上依次执行上述步骤，确保工作负载有充足的时间被调度到其他节点。

流程完成后，确认所有节点和工作负载均健康如常。
