
打印用于 'kubeadm init' 的默认 init 配置

### 概要


此命令打印对象，例如用于 'kubeadm init' 的默认 init 配置对象。


<p>请注意，Bootstrap Token 字段之类的敏感值已替换为 "abcdef.0123456789abcdef" 之类的占位符值以通过验证，但不执行创建令牌的实际计算。

```
kubeadm config print init-defaults [flags]
```


### 选项

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--component-configs strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>组件配置 API 对象的逗号分隔列表，打印其默认值。可用值：[KubeProxyConfiguration KubeletConfiguration]。如果未设置此参数，则不会打印任何组件配置。</p>
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>init-defaults 操作的帮助命令</p>
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
<p>与集群通信时使用的 kubeconfig 文件。如果未设置该参数，则可以在一组标准位置中搜索现有的 kubeconfig 文件。</p>
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

