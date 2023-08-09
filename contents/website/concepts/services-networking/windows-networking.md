---
title: Windows 网络
content_type: concept
weight: 110
---
Kubernetes 支持运行 Linux 或 Windows 节点。
你可以在统一集群内混布这两种节点。
本页提供了特定于 Windows 操作系统的网络概述。

## Windows 容器网络 {#networking}

Windows 容器网络通过 [CNI 插件](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)暴露。
Windows 容器网络的工作方式与虚拟机类似。
每个容器都有一个连接到 Hyper-V 虚拟交换机（vSwitch）的虚拟网络适配器（vNIC）。
主机网络服务（Host Networking Service，HNS）和主机计算服务（Host Compute Service，HCS）
协同创建容器并将容器 vNIC 挂接到网络。
HCS 负责管理容器，而 HNS 负责管理以下网络资源：

* 虚拟网络（包括创建 vSwitch）
* Endpoint / vNIC
* 命名空间
* 包括数据包封装、负载均衡规则、ACL 和 NAT 规则在内的策略。

Windows HNS 和 vSwitch 实现命名空间划分，且可以按需为 Pod 或容器创建虚拟 NIC。
然而，诸如 DNS、路由和指标等许多配置将存放在 Windows 注册表数据库中，
而不是像 Linux 将这些配置作为文件存放在 `/etc` 内。
针对容器的 Windows 注册表与主机的注册表是分开的，因此将 `/etc/resolv.conf`
从主机映射到一个容器的类似概念与 Linux 上的效果不同。
这些必须使用容器环境中运行的 Windows API 进行配置。
因此，实现 CNI 时需要调用 HNS，而不是依赖文件映射将网络详情传递到 Pod 或容器中。

## 网络模式 {#network-mode}

Windows 支持五种不同的网络驱动/模式：L2bridge、L2tunnel、Overlay (Beta)、Transparent 和 NAT。
在 Windows 和 Linux 工作节点组成的异构集群中，你需要选择一个同时兼容 Windows 和 Linux 的网络方案。
下表列出了 Windows 支持的树外插件，并给出了何时使用每种 CNI 的建议：

| 网络驱动 | 描述 | 容器数据包修改 | 网络插件 | 网络插件特点 |
| -------------- | ----------- | ------------------------------ | --------------- | ------------------------------ |
| L2bridge       | 容器挂接到一个外部 vSwitch。容器挂接到下层网络，但物理网络不需要了解容器的 MAC，因为这些 MAC 在入站/出站时被重写。 | MAC 被重写为主机 MAC，可使用 HNS OutboundNAT 策略将 IP 重写为主机 IP。 | [win-bridge](https://github.com/containernetworking/plugins/tree/master/plugins/main/windows/win-bridge)、[Azure-CNI](https://github.com/Azure/azure-container-networking/blob/master/docs/cni.md)、Flannel host-gateway 使用 win-bridge| win-bridge 使用 L2bridge 网络模式，将容器连接到主机的下层，提供最佳性能。节点间连接需要用户定义的路由（UDR）。 |
| L2Tunnel | 这是 L2bridge 的一种特例，但仅用在 Azure 上。所有数据包都会被发送到应用了 SDN 策略的虚拟化主机。 | MAC 被重写，IP 在下层网络上可见。| [Azure-CNI](https://github.com/Azure/azure-container-networking/blob/master/docs/cni.md) | Azure-CNI 允许将容器集成到 Azure vNET，允许容器充分利用 [Azure 虚拟网络](https://azure.microsoft.com/zh-cn/services/virtual-network/)所提供的能力集合。例如，安全地连接到 Azure 服务或使用 Azure NSG。参考 [azure-cni 了解有关示例](https://docs.microsoft.com/zh-cn/azure/aks/concepts-network#azure-cni-advanced-networking)。 |
| Overlay | 容器被赋予一个 vNIC，连接到外部 vSwitch。每个上层网络都有自己的 IP 子网，由自定义 IP 前缀进行定义。该上层网络驱动使用 VXLAN 封装。 | 用外部头进行封装。 | [win-overlay](https://github.com/containernetworking/plugins/tree/master/plugins/main/windows/win-overlay)、Flannel VXLAN（使用 win-overlay） | 当需要将虚拟容器网络与主机的下层隔离时（例如出于安全原因），应使用 win-overlay。如果你的数据中心的 IP 个数有限，可以将 IP 在不同的上层网络中重用（带有不同的 VNID 标记）。在 Windows Server 2019 上这个选项需要 [KB4489899](https://support.microsoft.com/zh-cn/help/4489899)。 |
| Transparent（[ovn-kubernetes](https://github.com/openvswitch/ovn-kubernetes) 的特殊用例） | 需要一个外部 vSwitch。容器挂接到一个外部 vSwitch，由后者通过逻辑网络（逻辑交换机和路由器）实现 Pod 内通信。 | 数据包通过 [GENEVE](https://datatracker.ietf.org/doc/draft-gross-geneve/) 或 [STT](https://datatracker.ietf.org/doc/draft-davie-stt/) 隧道进行封装，以到达其它主机上的 Pod。  <br/> 数据包基于 OVN 网络控制器提供的隧道元数据信息被转发或丢弃。<br/>南北向通信使用 NAT。 | [ovn-kubernetes](https://github.com/openvswitch/ovn-kubernetes) | [通过 ansible 部署](https://github.com/openvswitch/ovn-kubernetes/tree/master/contrib)。通过 Kubernetes 策略可以实施分布式 ACL。支持 IPAM。无需 kube-proxy 即可实现负载均衡。无需 iptables/netsh 即可进行 NAT。 |
| NAT（**Kubernetes 中未使用**） | 容器被赋予一个 vNIC，连接到内部 vSwitch。DNS/DHCP 是使用一个名为 [WinNAT 的内部组件](https://techcommunity.microsoft.com/t5/virtualization/windows-nat-winnat-capabilities-and-limitations/ba-p/382303)实现的 | MAC 和 IP 重写为主机 MAC/IP。 | [nat](https://github.com/Microsoft/windows-container-networking/tree/master/plugins/nat) | 放在此处保持完整性。 |

如上所述，Windows 通过 [VXLAN 网络后端](https://github.com/coreos/flannel/blob/master/Documentation/backends.md#vxlan)（**Beta 支持**；委派给 win-overlay）
和 [host-gateway 网络后端](https://github.com/coreos/flannel/blob/master/Documentation/backends.md#host-gw)（稳定支持；委派给 win-bridge）
也[支持](https://github.com/flannel-io/cni-plugin#windows-support-experimental) [Flannel](https://github.com/coreos/flannel) 的 [CNI 插件](https://github.com/flannel-io/cni-plugin)。

此插件支持委派给参考 CNI 插件（win-overlay、win-bridge）之一，配合使用 Windows
上的 Flannel 守护程序（Flanneld），以便自动分配节点子网租赁并创建 HNS 网络。
该插件读取自己的配置文件（cni.conf），并聚合 FlannelD 生成的 subnet.env 文件中的环境变量。
然后，委派给网络管道的参考 CNI 插件之一，并将包含节点分配子网的正确配置发送给 IPAM 插件（例如：`host-local`）。

对于 Node、Pod 和 Service 对象，TCP/UDP 流量支持以下网络流：

* Pod → Pod（IP）
* Pod → Pod（名称）
* Pod → Service（集群 IP）
* Pod → Service（PQDN，但前提是没有 "."）
* Pod → Service（FQDN）
* Pod → 外部（IP）
* Pod → 外部（DNS）
* Node → Pod
* Pod → Node

## IP 地址管理（IPAM） {#ipam}

Windows 支持以下 IPAM 选项：

* [host-local](https://github.com/containernetworking/plugins/tree/master/plugins/ipam/host-local)
* [azure-vnet-ipam](https://github.com/Azure/azure-container-networking/blob/master/docs/ipam.md)（仅适用于 azure-cni）
* [Windows Server IPAM](https://docs.microsoft.com/zh-cn/windows-server/networking/technologies/ipam/ipam-top)（未设置 IPAM 时的回滚选项）

## 负载均衡和 Service {#load-balancing-and-services}

Kubernetes {{< glossary_tooltip text="Service" term_id="service" >}} 是一种抽象：定义了逻辑上的一组 Pod 和一种通过网络访问这些 Pod 的方式。
在包含 Windows 节点的集群中，你可以使用以下类别的 Service：

* `NodePort`
* `ClusterIP`
* `LoadBalancer`
* `ExternalName`

Windows 容器网络与 Linux 网络有着很重要的差异。
更多细节和背景信息，参考 [Microsoft Windows 容器网络文档](https://docs.microsoft.com/zh-cn/virtualization/windowscontainers/container-networking/architecture)。

在 Windows 上，你可以使用以下设置来配置 Service 和负载均衡行为：

{{< table caption="Windows Service 设置" >}}
| 功能特性 | 描述 | 支持的 Windows 操作系统最低版本 | 启用方式 |
| ------- | ----------- | -------------------------- | ------------- |
| 会话亲和性 | 确保每次都将来自特定客户端的连接传递到同一个 Pod。 | Windows Server 2022 | 将 `service.spec.sessionAffinity` 设为 “ClientIP” |
| Direct Server Return (DSR) | 在负载均衡模式中 IP 地址修正和 LBNAT 直接发生在容器 vSwitch 端口；服务流量到达时源 IP 设置为原始 Pod IP。 | Windows Server 2019 | 在 kube-proxy 中设置以下标志：`--feature-gates="WinDSR=true" --enable-dsr=true` |
| 保留目标（Preserve-Destination） | 跳过服务流量的 DNAT，从而在到达后端 Pod 的数据包中保留目标服务的虚拟 IP。也会禁用节点间的转发。 | Windows Server，version 1903 | 在服务注解中设置 `"preserve-destination": "true"` 并在 kube-proxy 中启用 DSR。 |
| IPv4/IPv6 双栈网络 | 进出集群和集群内通信都支持原生的 IPv4 间与 IPv6 间流量 | Windows Server 2019 | 参考 [IPv4/IPv6 双栈](/zh-cn/docs/concepts/services-networking/dual-stack/#windows-support)。 |
| 客户端 IP 保留 | 确保入站流量的源 IP 得到保留。也会禁用节点间转发。 |  Windows Server 2019  | 将 `service.spec.externalTrafficPolicy` 设置为 “Local” 并在 kube-proxy 中启用 DSR。 |
{{< /table >}}

{{< warning >}} 
如果目的地节点在运行 Windows Server 2022，则上层网络的 NodePort Service 存在已知问题。
要完全避免此问题，可以使用 `externalTrafficPolicy: Local` 配置服务。

在安装了 KB5005619 的 Windows Server 2022 或更高版本上，采用 L2bridge 网络时
Pod 间连接存在已知问题。
要解决此问题并恢复 Pod 间连接，你可以在 kube-proxy 中禁用 WinDSR 功能。

这些问题需要操作系统修复。
有关更新，请参考 https://github.com/microsoft/Windows-Containers/issues/204。
{{< /warning >}}

## 限制 {#limitations}

Windows 节点**不支持**以下网络功能：

* 主机网络模式
* 从节点本身访问本地 NodePort（可以从其他节点或外部客户端进行访问）
* 为同一 Service 提供 64 个以上后端 Pod（或不同目的地址）
* 在连接到上层网络的 Windows Pod 之间使用 IPv6 通信
* 非 DSR 模式中的本地流量策略（Local Traffic Policy）

* 通过 `win-overlay`、`win-bridge` 使用 ICMP 协议，或使用 Azure-CNI 插件进行出站通信。  
  具体而言，Windows 数据平面（[VFP](https://www.microsoft.com/research/project/azure-virtual-filtering-platform/)）不支持 ICMP 数据包转换，这意味着：
  * 指向同一网络内目的地址的 ICMP 数据包（例如 Pod 间的 ping 通信）可正常工作；
  * TCP/UDP 数据包可正常工作；
  * 通过远程网络指向其它地址的 ICMP 数据包（例如通过 ping 从 Pod 到外部公网的通信）无法被转换，
    因此无法被路由回到这些数据包的源点；
  * 由于 TCP/UDP 数据包仍可被转换，所以在调试与外界的连接时，
    你可以将 `ping <destination>` 替换为 `curl <destination>`。

其他限制：

* 由于缺少 `CHECK` 实现，Windows 参考网络插件 win-bridge 和 win-overlay 未实现
[CNI 规约](https://github.com/containernetworking/cni/blob/master/SPEC.md) 的 v0.4.0 版本。
* Flannel VXLAN CNI 插件在 Windows 上有以下限制：
  * 使用 Flannel v0.12.0（或更高版本）时，节点到 Pod 的连接仅适用于本地 Pod。
  * Flannel 仅限于使用 VNI 4096 和 UDP 端口 4789。
  有关这些参数的更多详细信息，请参考官方的 [Flannel VXLAN](https://github.com/coreos/flannel/blob/master/Documentation/backends.md#vxlan) 后端文档。
