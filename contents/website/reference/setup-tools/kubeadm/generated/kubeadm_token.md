
管理引导令牌


### 概要


此命令管理引导令牌（bootstrap token）。它是可选的，仅适用于高级用例。


简而言之，引导令牌（bootstrap token）用于在客户端和服务器之间建立双向信任。
当客户端（例如，即将加入集群的节点）需要时，可以使用引导令牌相信正在与之通信的服务器。
然后可以使用具有 “签名” 的引导令牌。


引导令牌还可以作为一种允许对 API 服务器进行短期身份验证的方法（令牌用作 API 服务器信任客户端的方式），例如用于执行 TLS 引导程序。


引导令牌准确来说是什么？

- 它是位于 kube-system 命名空间中类型为 “bootstrap.kubernetes.io/token” 的一个 Secret。
- 引导令牌的格式必须为 “[a-z0-9]{6}.[a-z0-9]{16}”，前一部分是公共令牌 ID，而后者是令牌秘钥，必须在任何情况下都保密！
- 必须将 Secret 的名称命名为 “bootstrap-token-(token-id)”。


你可以在此处阅读有关引导令牌（bootstrap token）的更多信息：
  /docs/admin/bootstrap-tokens/

```
kubeadm token [flags]
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
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
是否启用 `dry-run` 模式
</p>
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
token 操作的帮助命令
</p>
</td>
</tr>

<tr>
<td colspan="2">
--kubeconfig string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值："/etc/kubernetes/admin.conf"
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
与集群通信时使用的 kubeconfig 文件。如果未设置，则搜索一组标准位置以查找现有 kubeconfig 文件。
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
[实验] 指向 '真实' 宿主机根文件系统的路径。
</p>
</td>
</tr>

</tbody>
</table>
