生成所有静态 Pod 清单文件

### 概要

生成所有的静态 Pod 清单文件

```
kubeadm init phase control-plane all [flags]
```

### 示例

```
# 为控制平面组件生成静态 Pod 清单文件，其功能等效于 kubeadm init 生成的文件。
kubeadm init phase control-plane all

# 使用从某配置文件中读取的选项为生成静态 Pod 清单文件。
kubeadm init phase control-plane all --config config.yaml
```

### 选项

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--apiserver-advertise-address string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
API 服务器所公布的其正在监听的 IP 地址。如果未设置，将使用默认的网络接口。
</p>
</td>
</tr>

<tr>
<td colspan="2">--apiserver-bind-port int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值：6443</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
API 服务器要绑定的端口。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
形式为 &lt;flagname&gt;=&lt;value&gt; 的一组额外参数，用来传递给 API 服务器，
或者覆盖其默认配置值
</p>
</td>
</tr>

<tr>
<td colspan="2">
--cert-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值："/etc/kubernetes/pki"
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
存储证书的路径。
</p>
</td>
</tr>

<tr>
<td colspan="2">--config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
kubeadm 配置文件的路径。
</p>
</td>
</tr>

<tr>
<td colspan="2">--control-plane-endpoint string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
为控制平面选择一个稳定的 IP 地址或者 DNS 名称。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
一组形式为 &lt;flagname&gt;=&lt;value&gt; 的额外参数，用来传递给控制管理器（Controller Manager）
或覆盖其默认设置值
</p>
</td>
</tr>

<tr>
<td colspan="2">--dry-run</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
不做任何更改；只输出将要执行的操作。
</td>
</tr>

<tr>
<td colspan="2">--feature-gates string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
一组用来描述各种特性门控的键值（key=value）对。选项是：
<br/>EtcdLearnerMode=true|false (ALPHA - 默认值=false)
<br/>PublicKeysECDSA=true|false (ALPHA - 默认值=false)
<br/>RootlessControlPlane=true|false (ALPHA - 默认值=false)
</p>
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
all 操作的帮助命令
</p>
</td>
</tr>

<tr>
<td colspan="2">
--image-repository string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值："registry.k8s.io"
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
选择用于拉取控制平面镜像的容器仓库
</p>
</td>
</tr>

<tr>
<td colspan="2">
--kubernetes-version string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值："stable-1"
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
为控制平面选择指定的 Kubernetes 版本。
</p>
</td>
</tr>

<tr>
<td colspan="2">--patches string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
包含名为 &quot;target[suffix][+patchtype].extension&quot; 的文件的目录的路径。
例如，&quot;kube-apiserver0+merge.yaml&quot;或是简单的 &quot;etcd.json&quot;。
&quot;target&quot; 可以是 &quot;kube-apiserver&quot;、&quot;kube-controller-manager&quot;、&quot;kube-scheduler&quot;、&quot;etcd&quot;、&quot;kubeletconfiguration&quot; 之一。
&quot;patchtype&quot; 可以是 &quot;strategic&quot;、&quot;merge&quot; 或者 &quot;json&quot; 之一，
并且它们与 kubectl 支持的补丁格式相匹配。
默认的 &quot;patchtype&quot; 是 &quot;strategic&quot;。
&quot;extension&quot; 必须是 &quot;json&quot; 或 &quot;yaml&quot;。
&quot;suffix&quot; 是一个可选字符串，可用于确定首先按字母顺序应用哪些补丁。
</p>
</td>
</tr>

<tr>
<td colspan="2">--pod-network-cidr string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
指定 Pod 网络的 IP 地址范围。如果设置了此标志，控制平面将自动地为每个节点分配 CIDR。
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
一组形式为 &lt;flagname&gt;=&lt;value&gt; 的额外参数，用来传递给调度器（Scheduler）
或覆盖其默认设置值

传递给调度器（scheduler）一组额外的参数或者以 &lt;flagname&gt;=&lt;value&gt; 形式覆盖其默认值。
<p>
</td>
</tr>

<tr>
<td colspan="2">
--service-cidr string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值："10.96.0.0/12"
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
为服务 VIP 选择 IP 地址范围。
</p>
</td>
</tr>

</tbody>
</table>

### 从父指令继承的选项

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--rootfs string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
[实验] 指向'真实'宿主机的根文件系统的路径。
</p>
</td>
</tr>

</tbody>
</table>

