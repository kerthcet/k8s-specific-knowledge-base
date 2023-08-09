TLS 引导后更新与 kubelet 相关的设置

### 概要

TLS 引导后更新与 kubelet 相关的设置

```
kubeadm init phase kubelet-finalize [flags]
```

### 示例

```
  # 在 TLS 引导后更新与 kubelet 相关的设置
  kubeadm init phase kubelet-finalize all --config
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
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>kubelet-finalize 操作的帮助命令</p></td>
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
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>[实验] 到'真实'主机根文件系统的路径。</p></td>
</tr>

</tbody>
</table>

