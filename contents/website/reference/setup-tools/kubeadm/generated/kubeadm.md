


kubeadm: 轻松创建一个安全的 Kubernetes 集群
### 摘要


```
┌──────────────────────────────────────────────────────────┐
│ KUBEADM                                                  │
│ 轻松创建一个安全的 Kubernetes 集群                       │
│                                                          │
│ 给我们反馈意见的地址：                                   │
│ https://github.com/kubernetes/kubeadm/issues             │
└──────────────────────────────────────────────────────────┘
```


用途示例：


创建一个有两台机器的集群，包含一个主节点（用来控制集群），和一个工作节点（运行你的工作负载，像 Pod 和 Deployment）。


```
┌──────────────────────────────────────────────────────────┐
│ 在第一台机器上：                                         │
├──────────────────────────────────────────────────────────┤
│ control-plane# kubeadm init                              │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 在第二台机器上：                                         │
├──────────────────────────────────────────────────────────┤
│ worker# kubeadm join &lt;arguments-returned-from-init&gt;│
└──────────────────────────────────────────────────────────┘
```

你可以重复第二步，向集群添加更多机器。


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
<p>kubeadm 操作的帮助信息<p>
</td>
</tr>

<tr>
<td colspan="2">--rootfs string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>[实验] 指向 '真实' 宿主机根文件系统的路径。<p>
</td>
</tr>

</tbody>
</table>

