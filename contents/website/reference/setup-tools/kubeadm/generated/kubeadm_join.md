
在你希望加入现有集群的任何机器上运行它

### 摘要


当节点加入 kubeadm 初始化的集群时，我们需要建立双向信任。
这个过程可以分解为发现（让待加入节点信任 Kubernetes 控制平面节点）和
TLS 引导（让 Kubernetes 控制平面节点信任待加入节点）两个部分。


有两种主要的发现方案。
第一种方法是使用共享令牌和 API 服务器的 IP 地址。
第二种是以文件形式提供标准 kubeconfig 文件的一个子集。
发现/kubeconfig 文件支持令牌、client-go 鉴权插件（“exec”）、“tokenFile" 和
"authProvider"。该文件可以是本地文件，也可以通过 HTTPS URL 下载。
格式是 `kubeadm join --discovery-token abcdef.1234567890abcdef 1.2.3.4:6443`、
`kubeadm join --discovery-file path/to/file.conf` 或者
`kubeadm join --discovery-file https://url/file.conf`。
只能使用其中一种。
如果发现信息是从 URL 加载的，必须使用 HTTPS。
此外，在这种情况下，主机安装的 CA 包用于验证连接。


如果使用共享令牌进行发现，还应该传递 --discovery-token-ca-cert-hash 参数来验证
Kubernetes 控制平面节点提供的根证书颁发机构（CA）的公钥。
此参数的值指定为 "&lt;hash-type&gt;:&lt;hex-encoded-value&gt;"，
其中支持的哈希类型为 "sha256"。哈希是通过 Subject Public Key Info（SPKI）对象的字节计算的（如 RFC7469）。
这个值可以从 "kubeadm init" 的输出中获得，或者可以使用标准工具进行计算。
可以多次重复 --discovery-token-ca-cert-hash 参数以允许多个公钥。

如果无法提前知道 CA 公钥哈希，则可以通过 --discovery-token-unsafe-skip-ca-verification 参数禁用此验证。
这削弱了 kubeadm 安全模型，因为其他节点可能会模仿 Kubernetes 控制平面节点。


TLS 引导机制也通过共享令牌驱动。
这用于向 Kubernetes 控制平面节点进行临时的身份验证，以提交本地创建的密钥对的证书签名请求（CSR）。
默认情况下，kubeadm 将设置 Kubernetes 控制平面节点自动批准这些签名请求。
这个令牌通过 --tls-bootstrap-token abcdef.1234567890abcdef 参数传入。

通常两个部分会使用相同的令牌。
在这种情况下可以使用 --token 参数，而不是单独指定每个令牌。


"join [api-server-endpoint]" 命令执行下列阶段：

```
preflight              Run join pre-flight checks
control-plane-prepare  Prepare the machine for serving a control plane
  /download-certs        [EXPERIMENTAL] Download certificates shared among control-plane nodes from the kubeadm-certs Secret
  /certs                 Generate the certificates for the new control plane components
  /kubeconfig            Generate the kubeconfig for the new control plane components
  /control-plane         Generate the manifests for the new control plane components
kubelet-start          Write kubelet settings, certificates and (re)start the kubelet
control-plane-join     Join a machine as a control plane instance
  /etcd                  Add a new local etcd member
  /update-status         Register the new control-plane node into the ClusterStatus maintained in the kubeadm-config ConfigMap (DEPRECATED)
  /mark-control-plane    Mark a node as a control-plane
```

```
kubeadm join [api-server-endpoint] [flags]
```

### 选项

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>
<tr>
<td colspan="2">--apiserver-advertise-address string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>如果该节点托管一个新的控制平面实例，则 API 服务器将公布其正在侦听的 IP 地址。如果未设置，则使用默认网络接口。</p>
</td>
</tr>

<tr>
<td colspan="2">
--apiserver-bind-port int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: 6443
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>如果节点应该托管新的控制平面实例，则为 API 服务器要绑定的端口。</p>
</td>
</tr>

<tr>
<td colspan="2">--certificate-key string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>使用此密钥可以解密由 init 上传的证书 secret。</p>
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
<td colspan="2">--control-plane</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>在此节点上创建一个新的控制平面实例</p>
</td>
</tr>

<tr>
<td colspan="2">--cri-socket string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>要连接的 CRI 套接字的路径。如果为空，则 kubeadm 将尝试自动检测此值；
仅当安装了多个 CRI 或具有非标准 CRI 插槽时，才使用此选项。</p>
</td>
</tr>

<tr>
<td colspan="2">--discovery-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>对于基于文件的发现，给出用于加载集群信息的文件或者 URL。</p>
</td>
</tr>

<tr>
<td colspan="2">--discovery-token string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>对于基于令牌的发现，该令牌用于验证从 API 服务器获取的集群信息。</p>
</td>
</tr>

<tr>
<td colspan="2">--discovery-token-ca-cert-hash stringSlice</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>对基于令牌的发现，验证根 CA 公钥是否与此哈希匹配 (格式: "&lt;type&gt;:&lt;value&gt;")。</p>
</td>
</tr>

<tr>
<td colspan="2">--discovery-token-unsafe-skip-ca-verification</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>对于基于令牌的发现，允许在未关联 --discovery-token-ca-cert-hash 参数的情况下添加节点。</p>
</td>
</tr>

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
<p>join 操作的帮助命令</p>
</td>
</tr>

<tr>
<td colspan="2">--ignore-preflight-errors strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>错误将显示为警告的检查列表；例如：'IsPrivilegedUser,Swap'。取值为 'all' 时将忽略检查中的所有错误。</p>
</td>
</tr>

<tr>
<td colspan="2">--node-name string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>指定节点的名称</p>
</td>
</tr>

<tr>
<td colspan="2">--patches string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>包含名为 "target[suffix][+patchtype].extension" 的文件的目录的路径。
例如，"kube-apiserver0+merge.yaml" 或仅仅是 "etcd.json"。
"target" 可以是 “kube-apiserver”、“kube-controller-manager”、“kube-scheduler”、“etcd”、“kubeletconfiguration” 之一，
"patchtype" 可以是 "strategic"、"merge" 或 "json" 之一，并且它们与 kubectl 支持的补丁格式匹配。
默认的 "patchtype" 为 "strategic"。 "extension" 必须为 "json" 或 "yaml"。
"suffix" 是一个可选字符串，可用于确定首先按字母顺序应用哪些补丁。</p>
</td>
</tr>

<tr>
<td colspan="2">--skip-phases strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>要跳过的阶段列表</p>
</td>
</tr>

<tr>
<td colspan="2">--tls-bootstrap-token string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>指定在加入节点时用于临时通过 Kubernetes 控制平面进行身份验证的令牌。</p>
</td>
</tr>

<tr>
<td colspan="2">--token string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<p>如果未提供这些值，则将它们用于 discovery-token 令牌和 tls-bootstrap 令牌。</p>
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
<p>[实验] 指向 '真实' 宿主机根文件系统的路径。</p>
</td>
</tr>

</tbody>
</table>

