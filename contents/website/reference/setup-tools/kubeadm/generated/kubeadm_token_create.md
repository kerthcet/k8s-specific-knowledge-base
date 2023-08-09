
在服务器上创建引导令牌


### 概要


这个命令将为你创建一个引导令牌。
你可以设置此令牌的用途，"有效时间" 和可选的人性化的描述。

这里的 [token] 是指将要生成的实际令牌。
该令牌应该是一个通过安全机制生成的随机令牌，形式为 "[a-z0-9]{6}.[a-z0-9]{16}"。
如果没有给出 [token]，kubeadm 将生成一个随机令牌。

```
kubeadm token create [token]
```


### 选项

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--certificate-key string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
当与 “--print-join-command” 一起使用时，打印作为控制平面加入集群时所需的所有 “kubeadm join” 标志。
要创建新的证书密钥，你必须使用 “kubeadm init phase upload-certs --upload-certs”。
</p></td>
</tr>

<tr>
<td colspan="2">--config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
kubeadm 配置文件的路径。
</p>
</td>
</tr>

<tr>
<td colspan="2">--description string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
针对令牌用途的人性化的描述。
</p>
</td>
</tr>

<tr>
<td colspan="2">
<p>
--groups stringSlice&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值：[system:bootstrappers:kubeadm:default-node-token]
</p>
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
此令牌用于身份验证时将进行身份验证的其他组。必须匹配  "\\Asystem:bootstrappers:[a-z0-9:-]{0,255}[a-z0-9]\\z"
</p>
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
create 操作的帮助命令
</p>
</td>
</tr>

<tr>
<td colspan="2">--print-join-command</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
不仅仅打印令牌，而是打印使用令牌加入集群所需的完整 'kubeadm join' 参数。
</p>
</td>
</tr>

<tr>
<td colspan="2">
--ttl duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值：24h0m0s
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
令牌有效时间，超过该时间令牌被自动删除。(例如： 1s, 2m, 3h)。如果设置为 '0'，令牌将永远不过期。
</p>
</td>
</tr>

<tr>
<td colspan="2">
--usages stringSlice&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值：[signing,authentication]
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
描述可以使用此令牌的方式。你可以多次使用 `--usages` 或者提供一个以逗号分隔的选项列表。合法选项有: [signing,authentication]
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
<td colspan="2">--dry-run</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>
是否启用 `dry-run` 运行模式
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
用于和集群通信的 KubeConfig 文件。如果它没有被设置，那么 kubeadm 将会搜索一个已经存在于标准路径的 KubeConfig 文件。
</p>
</td>
</tr>

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

