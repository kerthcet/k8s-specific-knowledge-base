---
title: 网络插件
content_type: concept
weight: 10
---


Kubernetes {{< skew currentVersion >}} 支持用于集群联网的[容器网络接口](https://github.com/containernetworking/cni) (CNI) 插件。
你必须使用和你的集群相兼容并且满足你的需求的 CNI 插件。
在更广泛的 Kubernetes 生态系统中你可以使用不同的插件（开源和闭源）。

要实现 [Kubernetes 网络模型](/zh-cn/docs/concepts/services-networking/#the-kubernetes-network-model)，你需要一个 CNI 插件。

你必须使用与 [v0.4.0](https://github.com/containernetworking/cni/blob/spec-v0.4.0/SPEC.md)
或更高版本的 CNI 规范相符合的 CNI 插件。
Kubernetes 推荐使用一个兼容 [v1.0.0](https://github.com/containernetworking/cni/blob/spec-v1.0.0/SPEC.md)
CNI 规范的插件（插件可以兼容多个规范版本）。


## 安装   {#installation}

在网络语境中，容器运行时（Container Runtime）是在节点上的守护进程，
被配置用来为 kubelet 提供 CRI 服务。具体而言，容器运行时必须配置为加载所需的
CNI 插件，从而实现 Kubernetes 网络模型。

{{< note >}}
在 Kubernetes 1.24 之前，CNI 插件也可以由 kubelet 使用命令行参数 `cni-bin-dir`
和 `network-plugin` 管理。Kubernetes 1.24 移除了这些命令行参数，
CNI 的管理不再是 kubelet 的工作。

如果你在移除 dockershim 之后遇到问题，
请参阅[排查 CNI 插件相关的错误](/zh-cn/docs/tasks/administer-cluster/migrating-from-dockershim/troubleshooting-cni-plugin-related-errors/)。
{{< /note >}}

要了解容器运行时如何管理 CNI 插件的具体信息，可参见对应容器运行时的文档，例如：

- [containerd](https://github.com/containerd/containerd/blob/main/script/setup/install-cni)
- [CRI-O](https://github.com/cri-o/cri-o/blob/main/contrib/cni/README.md)

要了解如何安装和管理 CNI 插件的具体信息，可参阅对应的插件或
[网络驱动（Networking Provider）](/zh-cn/docs/concepts/cluster-administration/networking/#how-to-implement-the-kubernetes-networking-model)
的文档。

## 网络插件要求   {#network-plugin-requirements}

对于插件开发人员以及时常会构建并部署 Kubernetes 的用户而言，
插件可能也需要特定的配置来支持 kube-proxy。
iptables 代理依赖于 iptables，插件可能需要确保 iptables 能够监控容器的网络通信。
例如，如果插件将容器连接到 Linux 网桥，插件必须将 `net/bridge/bridge-nf-call-iptables`
sysctl 参数设置为 `1`，以确保 iptables 代理正常工作。
如果插件不使用 Linux 网桥，而是使用类似于 Open vSwitch 或者其它一些机制，
它应该确保为代理对容器通信执行正确的路由。

默认情况下，如果未指定 kubelet 网络插件，则使用 `noop` 插件，
该插件设置 `net/bridge/bridge-nf-call-iptables=1`，以确保简单的配置
（如带网桥的 Docker）与 iptables 代理正常工作。

### 本地回路 CNI   {#loopback-cni}

除了安装到节点上用于实现 Kubernetes 网络模型的 CNI 插件外，Kubernetes
还需要容器运行时提供一个本地回路接口 `lo`，用于各个沙箱（Pod 沙箱、虚机沙箱……）。
实现本地回路接口的工作可以通过复用
[CNI 本地回路插件](https://github.com/containernetworking/plugins/blob/master/plugins/main/loopback/loopback.go)来实现，
也可以通过开发自己的代码来实现
（参阅 [CRI-O 中的示例](https://github.com/cri-o/ocicni/blob/release-1.24/pkg/ocicni/util_linux.go#L91)）。

### 支持 hostPort   {#support-hostport}

CNI 网络插件支持 `hostPort`。你可以使用官方
[portmap](https://github.com/containernetworking/plugins/tree/master/plugins/meta/portmap)
插件，它由 CNI 插件团队提供，或者使用你自己的带有 portMapping 功能的插件。

如果你想要启动 `hostPort` 支持，则必须在 `cni-conf-dir` 指定 `portMappings capability`。
例如：

```json
{
  "name": "k8s-pod-network",
  "cniVersion": "0.4.0",
  "plugins": [
    {
      "type": "calico",
      "log_level": "info",
      "datastore_type": "kubernetes",
      "nodename": "127.0.0.1",
      "ipam": {
        "type": "host-local",
        "subnet": "usePodCidr"
      },
      "policy": {
        "type": "k8s"
      },
      "kubernetes": {
        "kubeconfig": "/etc/cni/net.d/calico-kubeconfig"
      }
    },
    {
      "type": "portmap",
      "capabilities": {"portMappings": true},
      "externalSetMarkChain": "KUBE-MARK-MASQ"
    }
  ]
}
```

### 支持流量整形   {#support-traffic-shaping}

**实验功能**

CNI 网络插件还支持 Pod 入站和出站流量整形。
你可以使用 CNI 插件团队提供的
[bandwidth](https://github.com/containernetworking/plugins/tree/master/plugins/meta/bandwidth)
插件，也可以使用你自己的具有带宽控制功能的插件。

如果你想要启用流量整形支持，你必须将 `bandwidth` 插件添加到 CNI 配置文件
（默认是 `/etc/cni/net.d`）并保证该可执行文件包含在你的 CNI 的 bin
文件夹内 (默认为 `/opt/cni/bin`)。

```json
{
  "name": "k8s-pod-network",
  "cniVersion": "0.4.0",
  "plugins": [
    {
      "type": "calico",
      "log_level": "info",
      "datastore_type": "kubernetes",
      "nodename": "127.0.0.1",
      "ipam": {
        "type": "host-local",
        "subnet": "usePodCidr"
      },
      "policy": {
        "type": "k8s"
      },
      "kubernetes": {
        "kubeconfig": "/etc/cni/net.d/calico-kubeconfig"
      }
    },
    {
      "type": "bandwidth",
      "capabilities": {"bandwidth": true}
    }
  ]
}
```

现在，你可以将 `kubernetes.io/ingress-bandwidth` 和 `kubernetes.io/egress-bandwidth`
注解添加到 Pod 中。例如：

```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    kubernetes.io/ingress-bandwidth: 1M
    kubernetes.io/egress-bandwidth: 1M
...
```

## {{% heading "whatsnext" %}}
