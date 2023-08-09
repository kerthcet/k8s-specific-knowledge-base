---
title: 容器运行时接口（CRI）
content_type: concept
weight: 60
---


CRI 是一个插件接口，它使 kubelet 能够使用各种容器运行时，无需重新编译集群组件。

你需要在集群中的每个节点上都有一个可以正常工作的{{<glossary_tooltip text="容器运行时" term_id="container-runtime">}}，
这样 {{< glossary_tooltip text="kubelet" term_id="kubelet" >}} 能启动
{{< glossary_tooltip text="Pod" term_id="pod" >}} 及其容器。

{{< glossary_definition prepend="容器运行时接口（CRI）是" term_id="container-runtime-interface" length="all" >}}

## API {#api}

{{< feature-state for_k8s_version="v1.23" state="stable" >}}

当通过 gRPC 连接到容器运行时，kubelet 将充当客户端。运行时和镜像服务端点必须在容器运行时中可用，
可以使用 `--image-service-endpoint` 
[命令行标志](/zh-cn/docs/reference/command-line-tools-reference/kubelet)在 kubelet 中单独配置。

对 Kubernetes v{{< skew currentVersion >}}，kubelet 偏向于使用 CRI `v1` 版本。
如果容器运行时不支持 CRI 的 `v1` 版本，那么 kubelet 会尝试协商较老的、仍被支持的所有版本。
v{{< skew currentVersion >}} 版本的 kubelet 也可协商 CRI `v1alpha2` 版本，但该版本被视为已弃用。
如果 kubelet 无法协商出可支持的 CRI 版本，则 kubelet 放弃并且不会注册为节点。

## 升级  {#upgrading}

升级 Kubernetes 时，kubelet 会尝试在组件重启时自动选择最新的 CRI 版本。
如果失败，则将如上所述进行回退。如果由于容器运行时已升级而需要 gRPC 重拨，
则容器运行时还必须支持最初选择的版本，否则重拨预计会失败。
这需要重新启动 kubelet。

## {{% heading "whatsnext" %}}

- 了解更多有关 CRI [协议定义](https://github.com/kubernetes/cri-api/blob/c75ef5b/pkg/apis/runtime/v1/api.proto)
