

将 kubelet 组件配置上传到 ConfigMap

### 概要

将从 kubeadm InitConfiguration 对象提取的 kubelet 配置上传到集群中的
`kubelet-config` ConfigMap。

```
kubeadm init phase upload-config kubelet [flags]
```

### 示例

```
# 将 kubelet 配置从 kubeadm 配置文件上传到集群中的 ConfigMap。
kubeadm init phase upload-config kubelet --config kubeadm.yaml
```

### 选项

<table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
到 kubeadm 配置文件的路径。
</p>
</td>
</tr>

<tr>
<td colspan="2">--cri-socket string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
要连接的 CRI 套接字的路径。如果该值为空，kubeadm 将尝试自动检测；
仅当你安装了多个 CRI 或使用非标准的 CRI 套接字时才应使用此选项。
</p>
</td>
</tr>

<tr>
<td colspan="2">--dry-run</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
不做任何更改；只输出将要执行的操作。
</p>
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
kubelet 操作的帮助命令
</p>
</td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
与集群通信时使用的 kubeconfig 文件。如果未设置该标签，
则可以通过一组标准路径来寻找已有的 kubeconfig 文件。
</p>
</td>
</tr>

</tbody>
</table>

### 从父命令继承的选项

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
<p>[实验] 到 '真实' 主机根文件系统的路径。</p>
</td>
</tr>

</tbody>
</table>

