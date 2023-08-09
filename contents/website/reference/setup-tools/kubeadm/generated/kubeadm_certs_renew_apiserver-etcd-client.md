
续订 apiserver 用于访问 etcd 的证书

### 概要

续订 apiserver 用于访问 etcd 的证书。

无论证书的到期日期如何，续订都会无条件地进行；SAN 等额外属性将基于现有文件/证书，因此无需重新提供它们。

默认情况下，续订尝试使用在 kubeadm 所管理的本地 PKI 中的证书颁发机构；作为替代方案，
可以使用 K8s 证书 API 进行证书更新，或者作为最后一个选择来生成 CSR 请求。

续订后，为了使更改生效，需要重新启动控制平面组件，并最终重新分发更新的证书，以防文件在其他地方使用。

```
kubeadm certs renew apiserver-etcd-client [flags]
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
<p>存储证书的路径。</p>
</td>
</tr>

<tr>
<td colspan="2">--config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>kubeadm 配置文件的路径。</p>
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>apiserver-etcd-client 操作的帮助命令</p>
</td>
</tr>

<tr>
<td colspan="2">
--kubeconfig string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值："/etc/kubernetes/admin.conf"
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>与集群通信时使用的 kubeconfig 文件。
如果未设置该参数，则可以在一组标准位置中搜索现有的 kubeconfig 文件。</p>
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
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>[实验] 到 '真实' 主机根文件系统的路径。</p>
</td>
</tr>

</tbody>
</table>

