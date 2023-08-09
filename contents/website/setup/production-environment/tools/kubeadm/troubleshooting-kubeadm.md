---
title: 对 kubeadm 进行故障排查
content_type: concept
weight: 20
---


与任何程序一样，你可能会在安装或者运行 kubeadm 时遇到错误。
本文列举了一些常见的故障场景，并提供可帮助你理解和解决这些问题的步骤。

如果你的问题未在下面列出，请执行以下步骤：

- 如果你认为问题是 kubeadm 的错误：
  - 转到 [github.com/kubernetes/kubeadm](https://github.com/kubernetes/kubeadm/issues) 并搜索存在的问题。
  - 如果没有问题，请 [打开](https://github.com/kubernetes/kubeadm/issues/new) 并遵循问题模板。

- 如果你对 kubeadm 的工作方式有疑问，可以在 [Slack](https://slack.k8s.io/) 上的 `#kubeadm` 频道提问，
  或者在 [StackOverflow](https://stackoverflow.com/questions/tagged/kubernetes) 上提问。
  请加入相关标签，例如 `#kubernetes` 和 `#kubeadm`，这样其他人可以帮助你。


## 由于缺少 RBAC，无法将 v1.18 Node 加入 v1.17 集群

自从 v1.18 后，如果集群中已存在同名 Node，kubeadm 将禁止 Node 加入集群。
这需要为 bootstrap-token 用户添加 RBAC 才能 GET Node 对象。

但这会导致一个问题，v1.18 的 `kubeadm join` 无法加入由 kubeadm v1.17 创建的集群。

要解决此问题，你有两种选择：

使用 kubeadm v1.18 在控制平面节点上执行 `kubeadm init phase bootstrap-token`。
请注意，这也会启用 bootstrap-token 的其余权限。

或者，也可以使用 `kubectl apply -f ...` 手动应用以下 RBAC：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: kubeadm:get-nodes
rules:
- apiGroups:
  - ""
  resources:
  - nodes
  verbs:
  - get
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kubeadm:get-nodes
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kubeadm:get-nodes
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: system:bootstrappers:kubeadm:default-node-token
```

## 在安装过程中没有找到 `ebtables` 或者其他类似的可执行文件

如果在运行 `kubeadm init` 命令时，遇到以下的警告

```console
[preflight] WARNING: ebtables not found in system path
[preflight] WARNING: ethtool not found in system path
```

那么或许在你的节点上缺失 `ebtables`、`ethtool` 或者类似的可执行文件。
你可以使用以下命令安装它们：

- 对于 Ubuntu/Debian 用户，运行 `apt install ebtables ethtool` 命令。
- 对于 CentOS/Fedora 用户，运行 `yum install ebtables ethtool` 命令。

## 在安装过程中，kubeadm 一直等待控制平面就绪

如果你注意到 `kubeadm init` 在打印以下行后挂起：

```console
[apiclient] Created API client, waiting for the control plane to become ready
```

这可能是由许多问题引起的。最常见的是：

- 网络连接问题。在继续之前，请检查你的计算机是否具有全部联通的网络连接。
- 容器运行时的 cgroup 驱动不同于 kubelet 使用的 cgroup 驱动。要了解如何正确配置 cgroup 驱动，
  请参阅[配置 cgroup 驱动](/zh-cn/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver/)。
- 控制平面上的 Docker 容器持续进入崩溃状态或（因其他原因）挂起。你可以运行 `docker ps` 命令来检查以及 `docker logs`
  命令来检视每个容器的运行日志。
  对于其他容器运行时，请参阅[使用 crictl 对 Kubernetes 节点进行调试](/zh-cn/docs/tasks/debug/debug-cluster/crictl/)。

## 当删除托管容器时 kubeadm 阻塞

如果容器运行时停止并且未删除 Kubernetes 所管理的容器，可能发生以下情况：

```shell
sudo kubeadm reset
```

```console
[preflight] Running pre-flight checks
[reset] Stopping the kubelet service
[reset] Unmounting mounted directories in "/var/lib/kubelet"
[reset] Removing kubernetes-managed containers
(block)
```

一个可行的解决方案是重新启动 Docker 服务，然后重新运行 `kubeadm reset`：
你也可以使用 `crictl` 来调试容器运行时的状态。
参见[使用 CRICTL 调试 Kubernetes 节点](/zh-cn/docs/tasks/debug/debug-cluster/crictl/)。

## Pod 处于 `RunContainerError`、`CrashLoopBackOff` 或者 `Error` 状态

在 `kubeadm init` 命令运行后，系统中不应该有 Pod 处于这类状态。

- 在 `kubeadm init` 命令执行完后，如果有 Pod 处于这些状态之一，请在 kubeadm
  仓库提起一个 issue。`coredns` (或者 `kube-dns`) 应该处于 `Pending` 状态，
  直到你部署了网络插件为止。

- 如果在部署完网络插件之后，有 Pod 处于 `RunContainerError`、`CrashLoopBackOff`
  或 `Error` 状态之一，并且 `coredns` （或者 `kube-dns`）仍处于 `Pending` 状态，
  那很可能是你安装的网络插件由于某种原因无法工作。你或许需要授予它更多的
  RBAC 特权或使用较新的版本。请在 Pod Network 提供商的问题跟踪器中提交问题，
  然后在此处分类问题。

## `coredns` 停滞在 `Pending` 状态

这一行为是 **预期之中** 的，因为系统就是这么设计的。kubeadm 的网络供应商是中立的，
因此管理员应该选择[安装 Pod 的网络插件](/zh-cn/docs/concepts/cluster-administration/addons/)。
你必须完成 Pod 的网络配置，然后才能完全部署 CoreDNS。
在网络被配置好之前，DNS 组件会一直处于 `Pending` 状态。

## `HostPort` 服务无法工作

此 `HostPort` 和 `HostIP` 功能是否可用取决于你的 Pod 网络配置。请联系 Pod 网络插件的作者，
以确认 `HostPort` 和 `HostIP` 功能是否可用。

已验证 Calico、Canal 和 Flannel CNI 驱动程序支持 HostPort。

有关更多信息，请参考 [CNI portmap 文档](https://github.com/containernetworking/plugins/blob/master/plugins/meta/portmap/README.md).

如果你的网络提供商不支持 portmap CNI 插件，你或许需要使用
[NodePort 服务的功能](/zh-cn/docs/concepts/services-networking/service/#type-nodeport)
或者使用 `HostNetwork=true`。

## 无法通过其服务 IP 访问 Pod

- 许多网络附加组件尚未启用 [hairpin 模式](/zh-cn/docs/tasks/debug/debug-application/debug-service/#a-pod-fails-to-reach-itself-via-the-service-ip)
  该模式允许 Pod 通过其服务 IP 进行访问。这是与 [CNI](https://github.com/containernetworking/cni/issues/476) 有关的问题。
  请与网络附加组件提供商联系，以获取他们所提供的 hairpin 模式的最新状态。

- 如果你正在使用 VirtualBox (直接使用或者通过 Vagrant 使用)，你需要
  确保 `hostname -i` 返回一个可路由的 IP 地址。默认情况下，第一个接口连接不能路由的仅主机网络。
  解决方法是修改 `/etc/hosts`，请参考示例 [Vagrantfile](https://github.com/errordeveloper/k8s-playground/blob/22dd39dfc06111235620e6c4404a96ae146f26fd/Vagrantfile#L11)。

## TLS 证书错误

以下错误说明证书可能不匹配。

```none
# kubectl get pods
Unable to connect to the server: x509: certificate signed by unknown authority (possibly because of "crypto/rsa: verification error" while trying to verify candidate authority certificate "kubernetes")
```

- 验证 `$HOME/.kube/config` 文件是否包含有效证书，
  并在必要时重新生成证书。在 kubeconfig 文件中的证书是 base64 编码的。
  该 `base64 --decode` 命令可以用来解码证书，`openssl x509 -text -noout`
  命令可以用于查看证书信息。
- 使用如下方法取消设置 `KUBECONFIG` 环境变量的值：

  ```shell
  unset KUBECONFIG
  ```

  或者将其设置为默认的 `KUBECONFIG` 位置：

  ```shell
  export KUBECONFIG=/etc/kubernetes/admin.conf
  ```

- 另一个方法是覆盖 `kubeconfig` 的现有用户 "管理员"：

  ```shell
  mv  $HOME/.kube $HOME/.kube.bak
  mkdir $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
  ```

## Kubelet 客户端证书轮换失败   {#kubelet-client-cert}

默认情况下，kubeadm 使用 `/etc/kubernetes/kubelet.conf` 中指定的 `/var/lib/kubelet/pki/kubelet-client-current.pem`
符号链接来配置 kubelet 自动轮换客户端证书。如果此轮换过程失败，你可能会在 kube-apiserver 日志中看到诸如
`x509: certificate has expired or is not yet valid` 之类的错误。要解决此问题，你必须执行以下步骤：
1. 从故障节点备份和删除 `/etc/kubernetes/kubelet.conf` 和 `/var/lib/kubelet/pki/kubelet-client*`。
2. 在集群中具有 `/etc/kubernetes/pki/ca.key` 的、正常工作的控制平面节点上
   执行 `kubeadm kubeconfig user --org system:nodes --client-name system:node:$NODE > kubelet.conf`。
   `$NODE` 必须设置为集群中现有故障节点的名称。
   手动修改生成的 `kubelet.conf` 以调整集群名称和服务器端点，
   或传递 `kubeconfig user --config`（此命令接受 `InitConfiguration`）。
   如果你的集群没有 `ca.key`，你必须在外部对 `kubelet.conf` 中的嵌入式证书进行签名。
3. 将得到的 `kubelet.conf` 文件复制到故障节点上，作为 `/etc/kubernetes/kubelet.conf`。
4. 在故障节点上重启 kubelet（`systemctl restart kubelet`），等待 `/var/lib/kubelet/pki/kubelet-client-current.pem` 重新创建。
5. 手动编辑 `kubelet.conf` 指向轮换的 kubelet 客户端证书，方法是将 `client-certificate-data` 和 `client-key-data` 替换为：

    ```yaml
    client-certificate: /var/lib/kubelet/pki/kubelet-client-current.pem
    client-key: /var/lib/kubelet/pki/kubelet-client-current.pem
    ```

6. 重新启动 kubelet。
7. 确保节点状况变为 `Ready`。

## 在 Vagrant 中使用 flannel 作为 Pod 网络时的默认 NIC

以下错误可能表明 Pod 网络中出现问题：

```console
Error from server (NotFound): the server could not find the requested resource
```

- 如果你正在 Vagrant 中使用 flannel 作为 Pod 网络，则必须指定 flannel 的默认接口名称。

  Vagrant 通常为所有 VM 分配两个接口。第一个为所有主机分配了 IP 地址 `10.0.2.15`，用于获得 NATed 的外部流量。

  这可能会导致 flannel 出现问题，它默认为主机上的第一个接口。这导致所有主机认为它们具有相同的公共
  IP 地址。为防止这种情况，传递 `--iface eth1` 标志给 flannel 以便选择第二个接口。

## 容器使用的非公共 IP

在某些情况下 `kubectl logs` 和 `kubectl run` 命令或许会返回以下错误，即便除此之外集群一切功能正常：

```console
Error from server: Get https://10.19.0.41:10250/containerLogs/default/mysql-ddc65b868-glc5m/mysql: dial tcp 10.19.0.41:10250: getsockopt: no route to host
```

- 这或许是由于 Kubernetes 使用的 IP 无法与看似相同的子网上的其他 IP 进行通信的缘故，
  可能是由机器提供商的政策所导致的。
- DigitalOcean 既分配一个共有 IP 给 `eth0`，也分配一个私有 IP 在内部用作其浮动 IP 功能的锚点，
  然而 `kubelet` 将选择后者作为节点的 `InternalIP` 而不是公共 IP。

  使用 `ip addr show` 命令代替 `ifconfig` 命令去检查这种情况，因为 `ifconfig` 命令
  不会显示有问题的别名 IP 地址。或者指定的 DigitalOcean 的 API 端口允许从 droplet 中
  查询 anchor IP：

  ```sh
  curl http://169.254.169.254/metadata/v1/interfaces/public/0/anchor_ipv4/address
  ```

  解决方法是通知 `kubelet` 使用哪个 `--node-ip`。当使用 DigitalOcean 时，可以是公网IP（分配给 `eth0` 的），
  或者是私网IP（分配给 `eth1` 的）。私网 IP 是可选的。
  [kubadm `NodeRegistrationOptions` 结构](/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/#kubeadm-k8s-io-v1beta3-NodeRegistrationOptions)
  的 `KubeletExtraArgs` 部分被用来处理这种情况。

  然后重启 `kubelet`：

  ```shell
  systemctl daemon-reload
  systemctl restart kubelet
  ```

## `coredns` Pod 有 `CrashLoopBackOff` 或者 `Error` 状态

如果有些节点运行的是旧版本的 Docker，同时启用了 SELinux，你或许会遇到 `coredns` Pod 无法启动的情况。
要解决此问题，你可以尝试以下选项之一：

- 升级到 [Docker 的较新版本](/zh-cn/docs/setup/production-environment/container-runtimes/#docker)。

- [禁用 SELinux](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/security-enhanced_linux/sect-security-enhanced_linux-enabling_and_disabling_selinux-disabling_selinux).

- 修改 `coredns` 部署以设置 `allowPrivilegeEscalation` 为 `true`：

```shell
kubectl -n kube-system get deployment coredns -o yaml | \
  sed 's/allowPrivilegeEscalation: false/allowPrivilegeEscalation: true/g' | \
  kubectl apply -f -
```

CoreDNS 处于 `CrashLoopBackOff` 时的另一个原因是当 Kubernetes 中部署的 CoreDNS Pod 检测到环路时。
[有许多解决方法](https://github.com/coredns/coredns/tree/master/plugin/loop#troubleshooting-loops-in-kubernetes-clusters)
可以避免在每次 CoreDNS 监测到循环并退出时，Kubernetes 尝试重启 CoreDNS Pod 的情况。

{{< warning >}}
禁用 SELinux 或设置 `allowPrivilegeEscalation` 为 `true` 可能会损害集群的安全性。
{{< /warning >}}

## etcd Pod 持续重启

如果你遇到以下错误：

```console
rpc error: code = 2 desc = oci runtime error: exec failed: container_linux.go:247: starting container process caused "process_linux.go:110: decoding init error from pipe caused \"read parent: connection reset by peer\""
```

如果你使用 Docker 1.13.1.84 运行 CentOS 7 就会出现这种问题。
此版本的 Docker 会阻止 kubelet 在 etcd 容器中执行。

为解决此问题，请选择以下选项之一：

- 回滚到早期版本的 Docker，例如 1.13.1-75

  ```shell
  yum downgrade docker-1.13.1-75.git8633870.el7.centos.x86_64 docker-client-1.13.1-75.git8633870.el7.centos.x86_64 docker-common-1.13.1-75.git8633870.el7.centos.x86_64
  ```

- 安装较新的推荐版本之一，例如 18.06:

  ```shell
  sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
  yum install docker-ce-18.06.1.ce-3.el7.x86_64
  ```

## 无法将以逗号分隔的值列表传递给 `--component-extra-args` 标志内的参数

`kubeadm init` 标志例如 `--component-extra-args` 允许你将自定义参数传递给像
kube-apiserver 这样的控制平面组件。然而，由于解析 (`mapStringString`) 的基础类型值，此机制将受到限制。

如果你决定传递一个支持多个逗号分隔值（例如
`--apiserver-extra-args "enable-admission-plugins=LimitRanger,NamespaceExists"`）参数，
将出现 `flag: malformed pair, expect string=string` 错误。
发生这种问题是因为参数列表 `--apiserver-extra-args` 预期的是 `key=value` 形式，
而这里的 `NamespacesExists` 被误认为是缺少取值的键名。

一种解决方法是尝试分离 `key=value` 对，像这样：
`--apiserver-extra-args "enable-admission-plugins=LimitRanger,enable-admission-plugins=NamespaceExists"`
但这将导致键 `enable-admission-plugins` 仅有值 `NamespaceExists`。

已知的解决方法是使用 kubeadm
[配置文件](/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/)。

## 在节点被云控制管理器初始化之前，kube-proxy 就被调度了

在云环境场景中，可能出现在云控制管理器完成节点地址初始化之前，kube-proxy 就被调度到新节点了。
这会导致 kube-proxy 无法正确获取节点的 IP 地址，并对管理负载平衡器的代理功能产生连锁反应。

在 kube-proxy Pod 中可以看到以下错误：

```console
server.go:610] Failed to retrieve node IP: host IP unknown; known addresses: []
proxier.go:340] invalid nodeIP, initializing kube-proxy with 127.0.0.1 as nodeIP
```

一种已知的解决方案是修补 kube-proxy DaemonSet，以允许在控制平面节点上调度它，
而不管它们的条件如何，将其与其他节点保持隔离，直到它们的初始保护条件消除：

```shell
kubectl -n kube-system patch ds kube-proxy -p='{ "spec": { "template": { "spec": { "tolerations": [ { "key": "CriticalAddonsOnly", "operator": "Exists" }, { "effect": "NoSchedule", "key": "node-role.kubernetes.io/control-plane" } ] } } } }'
```

此问题的跟踪[在这里](https://github.com/kubernetes/kubeadm/issues/1027)。

## 节点上的 `/usr` 被以只读方式挂载 {#usr-mounted-read-only}

在类似 Fedora CoreOS 或者 Flatcar Container Linux 这类 Linux 发行版本中，
目录 `/usr` 是以只读文件系统的形式挂载的。
在支持 [FlexVolume](https://github.com/kubernetes/community/blob/ab55d85/contributors/devel/sig-storage/flexvolume.md)时，
类似 kubelet 和 kube-controller-manager 这类 Kubernetes 组件使用默认路径
`/usr/libexec/kubernetes/kubelet-plugins/volume/exec/`，
而 FlexVolume 的目录 **必须是可写入的**，该功能特性才能正常工作。
（**注意**：FlexVolume 在 Kubernetes v1.23 版本中已被弃用）

为了解决这个问题，你可以使用 kubeadm 的[配置文件](/zh-cn/docs/reference/config-api/kubeadm-config.v1beta3/) 来配置 FlexVolume 的目录。

在（使用 `kubeadm init` 创建的）主控制节点上，使用 `--config`
参数传入如下文件：

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
nodeRegistration:
  kubeletExtraArgs:
    volume-plugin-dir: "/opt/libexec/kubernetes/kubelet-plugins/volume/exec/"
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
controllerManager:
  extraArgs:
    flex-volume-plugin-dir: "/opt/libexec/kubernetes/kubelet-plugins/volume/exec/"
```

在加入到集群中的节点上，使用下面的文件：

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: JoinConfiguration
nodeRegistration:
  kubeletExtraArgs:
    volume-plugin-dir: "/opt/libexec/kubernetes/kubelet-plugins/volume/exec/"
```

或者，你要可以更改 `/etc/fstab` 使得 `/usr` 目录能够以可写入的方式挂载，
不过请注意这样做本质上是在更改 Linux 发行版的某种设计原则。

## `kubeadm upgrade plan` 输出错误信息 `context deadline exceeded`

在使用 `kubeadm` 来升级某运行外部 etcd 的 Kubernetes 集群时可能显示这一错误信息。
这并不是一个非常严重的一个缺陷，之所以出现此错误信息，原因是老的 kubeadm
版本会对外部 etcd 集群执行版本检查。你可以继续执行 `kubeadm upgrade apply ...`。

这一问题已经在 1.19 版本中得到修复。

## `kubeadm reset` 会卸载 `/var/lib/kubelet`

如果已经挂载了 `/var/lib/kubelet` 目录，执行 `kubeadm reset`
操作的时候会将其卸载。

要解决这一问题，可以在执行了 `kubeadm reset` 操作之后重新挂载
`/var/lib/kubelet` 目录。

这是一个在 1.15 中引入的故障，已经在 1.20 版本中修复。

## 无法在 kubeadm 集群中安全地使用 metrics-server

在 kubeadm 集群中可以通过为 [metrics-server](https://github.com/kubernetes-sigs/metrics-server)
设置 `--kubelet-insecure-tls` 来以不安全的形式使用该服务。
建议不要在生产环境集群中这样使用。

如果你需要在 metrics-server 和 kubelet 之间使用 TLS，会有一个问题，
kubeadm 为 kubelet 部署的是自签名的服务证书。这可能会导致 metrics-server
端报告下面的错误信息：

```console
x509: certificate signed by unknown authority
x509: certificate is valid for IP-foo not IP-bar
```

参见[为 kubelet 启用签名的服务证书](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/#kubelet-serving-certs)
以进一步了解如何在 kubeadm 集群中配置 kubelet 使用正确签名了的服务证书。

另请参阅 [How to run the metrics-server securely](https://github.com/kubernetes-sigs/metrics-server/blob/master/FAQ.md#how-to-run-metrics-server-securely)。
