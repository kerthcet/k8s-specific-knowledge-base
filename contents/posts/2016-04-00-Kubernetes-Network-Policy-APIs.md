---
title: “SIG-Networking：1.3 版本引入 Kubernetes 网络策略 API”
date: 2016-04-18
slug: kubernetes-network-policy-apis
---

_编者注：本周我们将推出 [Kubernetes 特殊兴趣小组](https://github.com/kubernetes/kubernetes/wiki/Special-Interest-Groups-(SIGs))、
Network-SIG 小组今天的帖子描述了 1.3 版中的网络策略 API-安全，隔离和多租户策略。_


自去年下半年以来，[Kubernetes SIG-Networking](https://kubernetes.slack.com/messages/sig-network/) 一直在定期开会，致力于将网络策略引入 Kubernetes，我们开始看到这个努力的结果。

许多用户面临的一个问题是，Kubernetes 的开放访问网络策略不适用于需要对访问容器或服务的流量进行更精确控制的应用程序。
如今，这种应用可能是多层应用，其中仅允许来自某个相邻层的流量。
但是，随着新的云原生应用不断通过组合微服务构建出来，对服务间流动的数据进行控制的能力变得更加重要。

在大多数 IaaS 环境（公共和私有）中，通过允许 VM 加入“安全组（Security Group）”来提供这种控制，
其中“安全组”成员的流量由网络策略或访问控制列表（ ACL ）定义，并由网络数据包过滤器实施。

SIG-Networking 开始这项工作时的第一步是辩识需要特定网络隔离以增强安全性的
[特定用例场景](https://docs.google.com/document/d/1blfqiH4L_fpn33ZrnQ11v7LcYP0lmpiJ_RaapAPBbNU/edit?pref=2&pli=1#)。
确保所定义的 API 适用于这些简单和常见的用例非常重要，因为它们为在 Kubernetes 内
实现更复杂的网络策略以支持多租户奠定了基础。

基于这些场景，团队考虑了几种可能的方法，并定义了一个最小的
[策略规范](https://docs.google.com/document/d/1qAm-_oSap-f1d6a-xRTj6xaH1sYQBfK36VyjB5XOZug/edit) 。
基本思想是，如果按命名空间启用了隔离，则特定流量类型被允许时会选择特定的 Pod。

快速支持此实验性 API 的最简单方法是对 API 服务器的 ThirdPartyResource 扩展，今天在 Kubernetes 1.2 中就可以实现。

如果您不熟悉它的工作方式，则可以通过定义 ThirdPartyResources 来扩展 Kubernetes API ，ThirdPartyResources 在指定的 URL 上创建一个新的 API 端点。

#### third-party-res-def.yaml 

```
kind: ThirdPartyResource
apiVersion: extensions/v1beta1
metadata:
name: network-policy.net.alpha.kubernetes.io
description: "Network policy specification"
versions:
- name: v1alpha1
 ```

```
$kubectl create -f third-party-res-def.yaml
 ```

这将创建一个 API 端点（每个名称空间一个）：

```
/net.alpha.kubernetes.io/v1alpha1/namespace/default/networkpolicys/
 ```
 
第三方网络控制器现在可以在这些端点上进行侦听，并在创建，修改或删除资源时根据需要做出反应。
_注意：在即将发布的 Kubernetes 1.3 版本中-当网络政策 API 以 beta 形式发布时-无需创建如上所示的 ThirdPartyResource API 端点。_


默认情况下，网络隔离处于关闭状态，以便所有Pod都能正常通信。
但是，重要的是要知道，启用网络隔离后，所有命名空间中所有容器的所有流量都会被阻止，这意味着启用隔离将改变容器的行为


通过在名称空间上定义 _network-isolation_ 注解来启用网络隔离，如下所示：

```
net.alpha.kubernetes.io/network-isolation: [on | off]
 ```
 
启用网络隔离后，**必须应用**显式网络策略才能启用 Pod 通信。

可以将策略规范应用于命名空间，以定义策略的详细信息，如下所示：

```
POST /apis/net.alpha.kubernetes.io/v1alpha1/namespaces/tenant-a/networkpolicys/

{
"kind": "NetworkPolicy",
"metadata": {
"name": "pol1"
},
"spec": {
"allowIncoming": {
"from": [
{ "pods": { "segment": "frontend" } }
],
"toPorts": [
{ "port": 80, "protocol": "TCP" }
]
},
"podSelector": { "segment": "backend" }
}
}
 ```
 
在此示例中，‘ **tenant-a** ’名称空间将按照指示应用策略‘ **pol1** ’。
具体而言，带有**segment**标签 ‘ **后端** ’ 的容器将允许接收来自带有“segment**标签‘ **frontend** ’的容器的端口80上的TCP流量。

现今，[Romana](http://romana.io/), [OpenShift](https://www.openshift.com/), [OpenContrail](http://www.opencontrail.org/) 和 [Calico](http://projectcalico.org/) 支持应用于名称空间和容器的网络策略。
思科和 VMware 也在努力实施。
Romana 和 Calico 最近都在 KubeCon 上使用 Kubernetes 1.2 演示了这些功能。
你可以在此处观看他们的演讲：[Romana](https://www.youtube.com/watch?v=f-dLKtK6qCs) ([slides](http://www.slideshare.net/RomanaProject/kubecon-london-2016-ronana-cloud-native-sdn))， [Calico](https://www.youtube.com/watch?v=p1zfh4N4SX0) ([slides](http://www.slideshare.net/kubecon/kubecon-eu-2016-secure-cloudnative-networking-with-project-calico))。&nbsp;

**它是如何工作的？**

每个解决方案都有其自己的特定实现细节。
今天，他们依靠某种形式的主机执行机制，但是将来的实现也可以构建为在虚拟机管理程序上，甚至直接由网络本身应用策略构建。&nbsp;

外部策略控制软件（具体情况因实现而异）将监视新 API 终结点是否正在创建容器和/或正在应用新策略。
当发生需要配置策略的事件时，侦听器将识别出更改，并且控制器将通过配置接口并应用策略来做出响应。&nbsp;
下图显示了 API 侦听器和策略控制器，它通过主机代理在本地应用网络策略来响应更新。
主机上的网络接口由主机上的 CNI 插件配置（未显示）。

 ![controller.jpg](https://lh5.googleusercontent.com/zMEpLMYmask-B-rYWnbMyGb0M7YusPQFPS6EfpNOSLbkf-cM49V7rTDBpA6k9-Zdh2soMul39rz9rHFJfL-jnEn_mHbpg0E1WlM-wjU-qvQu9KDTQqQ9uBmdaeWynDDNhcT3UjX5)

如果您由于网络隔离和/或安全性问题而一直拒绝使用 Kubernetes 开发应用程序，那么这些新的网络策略将为您提供所需的控制功能大有帮助。
无需等到 Kubernetes 1.3，因为网络策略现在作为实验性 API 可用，已启用 ThirdPartyResource。

如果您对 Kubernetes 和网络感兴趣，有几种参与方式-请通过以下方式加入我们：

- 我们的 [Networking Slack 频道](https://kubernetes.slack.com/messages/sig-network/)&nbsp;
- 我们的 [Kubernetes Networking Special Interest Group](https://groups.google.com/forum/#!forum/kubernetes-sig-network) 电子邮件列表&nbsp;


网络“特殊兴趣小组”，每两周一次，在太平洋时间下午 3 点（15：00）在[SIG-Networking 环聊](https://zoom.us/j/5806599998)开会。&nbsp;


_--Pani Networks 联合创始人 Chris Marino_  
