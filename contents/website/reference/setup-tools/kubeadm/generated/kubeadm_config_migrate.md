
从文件中读取旧版本的 kubeadm 配置的 API 类型，并为新版本输出类似的配置对象


### 概要


此命令允许您在 CLI 工具中将本地旧版本的配置对象转换为最新支持的版本，而无需变更集群中的任何内容。在此版本的 kubeadm 中，支持以下 API 版本：
- kubeadm.k8s.io/v1beta3


因此，无论您在此处传递 --old-config 参数的版本是什么，当写入到 stdout 或 --new-config （如果已指定）时，
都会读取、反序列化、默认、转换、验证和重新序列化 API 对象。


换句话说，如果您将此文件传递给 "kubeadm init"，则该命令的输出就是 kubeadm 实际上在内部读取的内容。

```
kubeadm config migrate [flags]
```


### 选项

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>migrate 操作的帮助信息</p>
</td>
</tr>

<tr>
<td colspan="2">--new-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>使用新的 API 版本生成的 kubeadm 配置文件的路径。这个路径是可选的。如果没有指定，输出将被写到 stdout。</p>
</td>
</tr>

<tr>
<td colspan="2">--old-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>使用旧 API 版本且应转换的 kubeadm 配置文件的路径。此参数是必需的。</p>
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
<td colspan="2">
--kubeconfig string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值："/etc/kubernetes/admin.conf"
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>用于和集群通信的 kubeconfig 文件。如果未设置，那么 kubeadm 将会搜索一个已经存在于标准路径的 kubeconfig 文件。</p>
</td>
</tr>

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

