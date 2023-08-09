
删除本地 etcd 成员。

### 概要

删除控制平面节点的本地 etcd 成员。

```
kubeadm reset phase remove-etcd-member [flags]
```

### 选项

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--dry-run</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
不做任何更改；只输出将要执行的操作。
</p></td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
remove-etcd-member 的帮助信息
</p></td>
</tr>

<tr>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
与集群通信时使用的 Kubeconfig 文件。如果未设置该标志，则可以在默认位置中查找现有的 Kubeconfig 文件。
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
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
[实验] 到'真实'主机根文件系统的路径。
</p>
</td>
</tr>

</tbody>
</table>
