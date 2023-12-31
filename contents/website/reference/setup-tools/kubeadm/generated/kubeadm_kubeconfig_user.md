
为其他用户输出一个 kubeconfig 文件。

### 概要

为其他用户输出一个 kubeconfig 文件。

```
kubeadm alpha kubeconfig user [flags]
```

```
  # 为一个名为 foo 的其他用户输出 kubeconfig 文件
  kubeadm kubeconfig user --client-name=foo
```

```
  # 使用 kubeadm 配置文件 bar 为另一个名为 foo 的用户输出 kubeconfig 文件
  kubeadm alpha kubeconfig user --client-name=foo --config=bar
```

-->
### 示例

```
# 使用名为 bar 的 kubeadm 配置文件为名为 foo 的另一用户输出 kubeconfig 文件
kubeadm kubeconfig user --client-name=foo --config=bar
```

### 选项

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--client-name string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
用户名。如果生成客户端证书，则用作其 CN。
</td>
</tr>

<tr>
<td colspan="2">--config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
指向 kubeadm 配置文件的路径
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
user 操作的帮助命令
</td>
</tr>

<tr>
<td colspan="2">--org strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
客户端证书的组织。如果创建客户端证书，此值将用作其 O 字段值。
</td>
</tr>

<tr>
<td colspan="2">--token string</td>
</tr>

<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
应该用此令牌做为 kubeconfig 的身份验证机制，而不是客户端证书
</td>
</tr>

<tr>
<td colspan="2">--validity-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 8760h0m0s</td>
</tr>
<tr>
<p>
客户证书的合法期限。所设置值为相对当前时间的偏移。
</p></td>
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
[实验] 指向 '真实' 宿主机的根目录。
</td>
</tr>

</tbody>
</table>

