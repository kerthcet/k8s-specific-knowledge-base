

生成用于提供 etcd 服务的证书

### 概要


生成用于提供 etcd 服务的证书，并将其保存到 etcd/server.crt 和 etcd/server.key 文件中。

默认 SAN 为 localhost、127.0.0.1、127.0.0.1、:: 1

如果两个文件都已存在，则 kubeadm 将跳过生成步骤，使用现有文件。

Alpha 免责声明：此命令当前为 alpha 功能。

```
kubeadm init phase certs etcd-server [flags]
```

### 选项

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">
--cert-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值："/etc/kubernetes/pki"
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>保存和存储证书的路径。<p>
</td>
</tr>

<tr>
<td colspan="2">--config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>kubeadm 配置文件的路径。<p>
</td>
</tr>

<tr>
<td colspan="2">--dry-run</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>不做任何更改；只输出将要执行的操作。<p>
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>etcd-server 操作的帮助命令<p>
</td>
</tr>

<tr>
<td colspan="2">
--kubernetes-version string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值："stable-1"
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>为控制平面指定特定的 Kubernetes 版本。<p>
</td>
</tr>

</tbody>
</table>



### 继承于父命令的选项

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
<p>[实验] 到 '真实' 主机根文件系统的路径。<p>
</td>
</tr>

</tbody>
</table>

