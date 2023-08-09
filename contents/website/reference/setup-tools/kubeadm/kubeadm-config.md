---
title: kubeadm config
content_type: concept
weight: 50
---

在 `kubeadm init` 执行期间，kubeadm 将 `ClusterConfiguration` 对象上传
到你的集群的 `kube-system` 名字空间下名为 `kubeadm-config` 的 ConfigMap 对象中。
然后在 `kubeadm join`、`kubeadm reset` 和 `kubeadm upgrade` 执行期间读取此配置。 

你可以使用 `kubeadm config print` 命令打印默认静态配置，
kubeadm 运行 `kubeadm init` and `kubeadm join` 时将使用此配置。

{{< note >}}
此命令的输出旨在作为示例。你必须手动编辑此命令的输出来适配你的设置。
删除你不确定的字段，kubeadm 将通过检查主机来尝试在运行时给它们设默认值。
{{< /note >}}

更多有关 `init` 和 `join` 的信息请浏览[使用带配置文件的 kubeadm init](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-init/#config-file)
或[使用带配置文件的 kubeadm join](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-join/#config-file)。

有关使用 kubeadm 的配置 API 的更多信息，
请浏览[使用 kubeadm API 来自定义组件](/zh-cn/docs/setup/production-environment/tools/kubeadm/control-plane-flags)。

你可以使用 `kubeadm config migrate` 来转换旧配置文件，
把其中已弃用的 API 版本更新为受支持的 API 版本。

`kubeadm config images list` 和 `kubeadm config images pull` 可以用来列出和拉取 kubeadm 所需的镜像。

## kubeadm config print {#cmd-config-print}
{{< include "generated/kubeadm_config_print.md" >}}

## kubeadm config print init-defaults {#cmd-config-print-init-defaults}
{{< include "generated/kubeadm_config_print_init-defaults.md" >}}

## kubeadm config print join-defaults {#cmd-config-print-join-defaults}
{{< include "generated/kubeadm_config_print_join-defaults.md" >}}

## kubeadm config migrate {#cmd-config-migrate}
{{< include "generated/kubeadm_config_migrate.md" >}}

## kubeadm config images list {#cmd-config-images-list}
{{< include "generated/kubeadm_config_images_list.md" >}}

## kubeadm config images pull {#cmd-config-images-pull}
{{< include "generated/kubeadm_config_images_pull.md" >}}

## {{% heading "whatsnext" %}}


* [kubeadm upgrade](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-upgrade/)
  将 Kubernetes 集群升级到更新版本 [kubeadm upgrade]


