---
title: 使用 Kubespray 安装 Kubernetes
content_type: concept
weight: 30
---


此快速入门有助于使用 [Kubespray](https://github.com/kubernetes-sigs/kubespray)
安装在 GCE、Azure、OpenStack、AWS、vSphere、Equinix Metal（曾用名 Packet）、Oracle Cloud
Infrastructure（实验性）或 Baremetal 上托管的 Kubernetes 集群。

Kubespray 是由若干 [Ansible](https://docs.ansible.com/) Playbook、
[清单（inventory）](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/ansible.md#inventory)、
制备工具和通用 OS/Kubernetes 集群配置管理任务的领域知识组成的。

Kubespray 提供：

- 高可用性集群
- 可组合属性（例如可选择网络插件）
- 支持大多数流行的 Linux 发行版
  - Flatcar Container Linux
  - Debian Bullseye、Buster、Jessie、Stretch
  - Ubuntu 16.04、18.04、20.04、22.04
  - CentOS/RHEL 7、8、9
  - Fedora 35、36
  - Fedora CoreOS
  - openSUSE Leap 15.x/Tumbleweed
  - Oracle Linux 7、8、9
  - Alma Linux 8、9
  - Rocky Linux 8、9
  - Kylin Linux Advanced Server V10
  - Amazon Linux 2
- 持续集成测试

要选择最适合你的用例的工具，请阅读
[kubeadm](/zh-cn/docs/reference/setup-tools/kubeadm/) 和
[kops](/zh-cn/docs/setup/production-environment/tools/kops/)
之间的[这份比较](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/comparisons.md)。


## 创建集群   {#creating-a-cluster}

### （1/5）满足下层设施要求

按以下[要求](https://github.com/kubernetes-sigs/kubespray#requirements)来配置服务器：

* **Kubernetes** 的最低版本要求为 V1.22
* **在将运行 Ansible 命令的计算机上安装 Ansible v2.11（或更高版本）、Jinja 2.11（或更高版本）和 python-netaddr**
* 目标服务器必须**能够访问 Internet** 才能拉取 Docker 镜像。否则，
  需要其他配置（[请参见离线环境](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/offline-environment.md)）
* 目标服务器配置为允许 **IPv4 转发**
* 如果针对 Pod 和 Service 使用 IPv6，则目标服务器配置为允许 **IPv6 转发**
* **防火墙不是由 kubespray 管理的**。你需要根据需求设置适当的规则策略。为了避免部署过程中出现问题，可以禁用防火墙。
* 如果从非 root 用户帐户运行 kubespray，则应在目标服务器中配置正确的特权升级方法并指定
  `ansible_become` 标志或命令参数 `--become` 或 `-b`

Kubespray 提供以下实用程序来帮助你设置环境：

* 为以下云驱动提供的 [Terraform](https://www.terraform.io/) 脚本：
  * [AWS](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/aws)
  * [OpenStack](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/openstack)
  * [Equinix Metal](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/equinix)

### （2/5）编写清单文件

设置服务器后，请创建一个
[Ansible 的清单文件](https://docs.ansible.com/ansible/latest/network/getting_started/first_inventory.html)。
你可以手动执行此操作，也可以通过动态清单脚本执行此操作。有关更多信息，请参阅
“[建立你自己的清单](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/getting-started.md#building-your-own-inventory)”。

### （3/5）规划集群部署

Kubespray 能够自定义部署的许多方面：

* 选择部署模式： kubeadm 或非 kubeadm
* CNI（网络）插件
* DNS 配置
* 控制平面的选择：本机/可执行文件或容器化
* 组件版本
* Calico 路由反射器
* 组件运行时选项
  * {{< glossary_tooltip term_id="docker" >}}
  * {{< glossary_tooltip term_id="containerd" >}}
  * {{< glossary_tooltip term_id="cri-o" >}}
* 证书生成方式

可以修改[变量文件](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html)以进行
Kubespray 定制。
如果你刚刚开始使用 Kubespray，请考虑使用 Kubespray 默认设置来部署你的集群并探索 Kubernetes。

### （4/5）部署集群

接下来，部署你的集群：

使用 [ansible-playbook](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/getting-started.md#starting-custom-deployment)
进行集群部署。

```shell
ansible-playbook -i your/inventory/inventory.ini cluster.yml -b -v \
  --private-key=~/.ssh/private_key
```

大型部署（超过 100 个节点）
可能需要[特定的调整](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/large-deployments.md)，
以获得最佳效果。

### （5/5）验证部署

Kubespray 提供了一种使用
[Netchecker](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/netcheck.md)
验证 Pod 间连接和 DNS 解析的方法。
Netchecker 确保 netchecker-agents Pod 可以解析 DNS 请求，
并在默认命名空间内对每个请求执行 ping 操作。
这些 Pod 模仿其他工作负载类似的行为，并用作集群运行状况指示器。

## 集群操作   {#cluster-operations}

Kubespray 提供了其他 Playbook 来管理集群： **scale** 和 **upgrade**。

### 扩展集群   {#scale-your-cluster}

你可以通过运行 scale playbook 向集群中添加工作节点。有关更多信息，
请参见 “[添加节点](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/getting-started.md#adding-nodes)”。
你可以通过运行 remove-node playbook 来从集群中删除工作节点。有关更多信息，
请参见 “[删除节点](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/getting-started.md#remove-nodes)”。

### 升级集群   {#upgrade-your-cluster}

你可以通过运行 upgrade-cluster Playbook 来升级集群。有关更多信息，请参见
“[升级](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/upgrades.md)”。

## 清理   {#cleanup}

你可以通过 [reset playbook](https://github.com/kubernetes-sigs/kubespray/blob/master/reset.yml)
重置节点并清除所有与 Kubespray 一起安装的组件。

{{< caution >}}
运行 reset playbook 时，请确保不要意外地将生产集群作为目标！
{{< /caution >}}

## 反馈   {#feedback}

* Slack 频道：[#kubespray](https://kubernetes.slack.com/messages/kubespray/)
  （你可以在[此处](https://slack.k8s.io/)获得邀请）。
* [GitHub 问题](https://github.com/kubernetes-sigs/kubespray/issues)。

## {{% heading "whatsnext" %}}

* 查看有关 Kubespray 的
  [路线图](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/roadmap.md)的计划工作。
* 查阅有关 [Kubespray](https://github.com/kubernetes-sigs/kubespray) 的更多信息。
