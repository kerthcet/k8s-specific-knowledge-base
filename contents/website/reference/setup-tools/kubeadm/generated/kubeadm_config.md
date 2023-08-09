
管理持久化在 ConfigMap 中的 kubeadm 集群的配置


### 概要


kube-system 命名空间里有一个名为 "kubeadm-config" 的 ConfigMap，kubeadm 用它来存储有关集群的内部配置。
kubeadm CLI v1.8.0+ 通过一个配置自动创建该 ConfigMap，这个配置是和 'kubeadm init' 共用的。
但是您如果使用 kubeadm v1.7.x 或更低的版本初始化集群，那么必须使用 'config upload' 命令创建该 ConfigMap。
这是必要的操作，目的是使 'kubeadm upgrade' 能够正确地配置升级后的集群。

```
kubeadm config [flags]
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
<p>config 操作的帮助命令</p>
</td>
</tr>

<tr>
<td colspan="2">
--kubeconfig string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值："/etc/kubernetes/admin.conf"
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>用于和集群通信的 kubeconfig 文件。如果它没有被设置，那么 kubeadm 将会搜索一个已经存在于标准路径的 kubeconfig 文件
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
<p>[实验] 到 '真实' 主机根文件系统的路径。
</td>
</tr>

</tbody>
</table>
