---
title: 通过配置文件设置 Kubelet 参数
content_type: task
weight: 330
---


通过保存在硬盘的配置文件设置 kubelet 的部分配置参数，这可以作为命令行参数的替代。

建议通过配置文件的方式提供参数，因为这样可以简化节点部署和配置管理。


## 创建配置文件   {#create-config-file}

[`KubeletConfiguration`](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/)
结构体定义了可以通过文件配置的 Kubelet 配置子集，

配置文件必须是这个结构体中参数的 JSON 或 YAML 表现形式。
确保 kubelet 可以读取该文件。

下面是一个 Kubelet 配置文件示例：

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
address: "192.168.0.8"
port: 20250
serializeImagePulls: false
evictionHard:
    memory.available:  "200Mi"
```

在这个示例中, Kubelet 被设置为在地址 192.168.0.8 端口 20250 上提供服务，以并行方式拉取镜像，
当可用内存低于 200Mi 时, kubelet 将会开始驱逐 Pod。
由于仅配置了四个 evictionHard 阈值之一，因此其他 evictionHard 阈值被重置为 0，而不是使用其内置默认值。
没有声明的其余配置项都将使用默认值，除非使用命令行参数来重载。
命令行中的参数将会覆盖配置文件中的对应值。

{{< note >}}
在示例中，通过只更改 evictionHard 的一个参数的默认值，
其他参数的默认值将不会被继承，他们会被设置为零。如果要提供自定义值，你应该分别设置所有阈值。
{{< /note >}}

## 启动通过配置文件配置的 Kubelet 进程   {#start-kubelet-via-config-file}

{{< note >}}
如果你使用 kubeadm 初始化你的集群，在使用 `kubeadm init` 创建你的集群的时候请使用 kubelet-config。
更多细节请阅读[使用 kubeadm 配置 kubelet](/zh-cn/docs/setup/production-environment/tools/kubeadm/kubelet-integration/)
{{< /note >}}

启动 Kubelet 需要将 `--config` 参数设置为 Kubelet 配置文件的路径。Kubelet 将从此文件加载其配置。

请注意，命令行参数与配置文件有相同的值时，就会覆盖配置文件中的该值。
这有助于确保命令行 API 的向后兼容性。

请注意，kubelet 配置文件中的相对文件路径是相对于 kubelet 配置文件的位置解析的，
而命令行参数中的相对路径是相对于 kubelet 的当前工作目录解析的。

请注意，命令行参数和 Kubelet 配置文件的某些默认值不同。
如果设置了 `--config`，并且没有通过命令行指定值，则 `KubeletConfiguration`
版本的默认值生效。在上面的例子中，version 是 `kubelet.config.k8s.io/v1beta1`。


## {{% heading "whatsnext" %}}

- 参阅 [`KubeletConfiguration`](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/)
  进一步学习 kubelet 的配置。
