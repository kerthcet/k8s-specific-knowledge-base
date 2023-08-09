---
title: kube-apiserver 配置 (v1alpha1)
content_type: tool-reference
package: apiserver.k8s.io/v1alpha1
---

<p>包 v1alpha1 包含 API 的 v1alpha1 版本。</p>

## 资源类型   {#resource-types}

- [AdmissionConfiguration](#apiserver-k8s-io-v1alpha1-AdmissionConfiguration)
- [EgressSelectorConfiguration](#apiserver-k8s-io-v1alpha1-EgressSelectorConfiguration)
- [TracingConfiguration](#apiserver-k8s-io-v1alpha1-TracingConfiguration)

## `AdmissionConfiguration`     {#apiserver-k8s-io-v1alpha1-AdmissionConfiguration}

<p>
AdmissionConfiguration 为准入控制器提供版本化的配置信息。
</p>

<table class="table">
<tbody>

<tr><td><code>apiVersion</code><br/>string</td><td><code>apiserver.k8s.io/v1alpha1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>AdmissionConfiguration</code></td></tr>

<tr><td><code>plugins</code><br/>
<a href="#apiserver-k8s-io-v1alpha1-AdmissionPluginConfiguration"><code>[]AdmissionPluginConfiguration</code></a>
</td>
<td>
   <p>
   <code>plugins</code> 允许用户为每个准入控制插件指定设置。
   </p>
</td>
</tr>
</tbody>
</table>

## `EgressSelectorConfiguration`     {#apiserver-k8s-io-v1alpha1-EgressSelectorConfiguration}

<p>
EgressSelectorConfiguration 为 Egress 选择算符客户端提供版本化的配置选项。
</p>

<table class="table">
<tbody>

<tr><td><code>apiVersion</code><br/>string</td><td><code>apiserver.k8s.io/v1alpha1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>EgressSelectorConfiguration</code></td></tr>

<tr><td><code>egressSelections</code> <B>[必需]</B><br/>
<a href="#apiserver-k8s-io-v1alpha1-EgressSelection"><code>[]EgressSelection</code></a>
</td>
<td>
   <p>
   <code>connectionServices</code> 包含一组 Egress 选择算符客户端配置选项。
   </p>
</td>
</tr>
</tbody>
</table>

## `TracingConfiguration`     {#apiserver-k8s-io-v1alpha1-TracingConfiguration}

<p>
TracingConfiguration 为跟踪客户端提供版本化的配置信息。
</p>

<table class="table">
<tbody>

<tr><td><code>apiVersion</code><br/>string</td><td><code>apiserver.k8s.io/v1alpha1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>TracingConfiguration</code></td></tr>

<tr><td><code>TracingConfiguration</code> <B>[必需]</B><br/>
<a href="#TracingConfiguration"><code>TracingConfiguration</code></a>
</td>
<td>
（<code>TracingConfiguration</code> 的成员嵌入到这种类型中。）
   <p>
   嵌入组件配置中的跟踪配置结构体。
   </p>
</td>
</tr>
</tbody>
</table>

## `AdmissionPluginConfiguration`     {#apiserver-k8s-io-v1alpha1-AdmissionPluginConfiguration}

**出现在：**

- [AdmissionConfiguration](#apiserver-k8s-io-v1alpha1-AdmissionConfiguration)

<p>
AdmissionPluginConfiguration 为某个插件提供配置信息。
</p>

<table class="table">
<tbody>

<tr><td><code>name</code> <B>[必需]</B><br/>
<code>string</code>
</td>
<td>
   <p>
   <code>name</code> 是准入控制器的名称。此名称必须与所注册的准入插件名称匹配。
   </p>
</td>
</tr>
<tr><td><code>path</code><br/>
<code>string</code>
</td>
<td>
   <p>
   <code>path</code> 为指向包含插件配置数据的配置文件的路径。
   </p>
</td>
</tr>
<tr><td><code>configuration</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/runtime#Unknown"><code>k8s.io/apimachinery/pkg/runtime.Unknown</code></a>
</td>
<td>
   <p>
   <code>configuration</code> 是一个嵌入的配置对象，用作插件的配置数据来源。
   如果设置了此字段，则使用此字段而不是指向配置文件的路径。
   </p>
</td>
</tr>
</tbody>
</table>

## `Connection`     {#apiserver-k8s-io-v1alpha1-Connection}

**出现在：**

- [EgressSelection](#apiserver-k8s-io-v1alpha1-EgressSelection)

<p>
Connection 提供某个 Egress 选择客户端的配置信息。
</p>

<table class="table">
<tbody>

<tr><td><code>proxyProtocol</code> <B>[必需]</B><br/>
<a href="#apiserver-k8s-io-v1alpha1-ProtocolType"><code>ProtocolType</code></a>
</td>
<td>
   <p>
   <code>proxyProtocol</code> 是客户端连接到 konnectivity 服务器所使用的协议。
   </p>
</td>
</tr>
<tr><td><code>transport</code><br/>
<a href="#apiserver-k8s-io-v1alpha1-Transport"><code>Transport</code></a>
</td>
<td>
   <p>
   <code>transport</code> 定义的是传输层的配置。我们使用这个配置来联系 konnectivity 服务器。
   当 <code>proxyProtocol</code> 是 HTTPConnect 或 GRPC 时需要设置此字段。
   </p>
</td>
</tr>
</tbody>
</table>

## `EgressSelection`     {#apiserver-k8s-io-v1alpha1-EgressSelection}

**出现在：**

- [EgressSelectorConfiguration](#apiserver-k8s-io-v1alpha1-EgressSelectorConfiguration)

EgressSelection 为某个 Egress 选择客户端提供配置信息。
</p>

<table class="table">
<tbody>

<tr><td><code>name</code> <B>[必需]</B><br/>
<code>string</code>
</td>
<td>
   <p>
  <code>name</code> 是 Egress 选择器的名称。当前支持的取值有 &quot;controlplane&quot;，
  &quot;master&quot;，&quot;etcd&quot; 和 &quot;cluster&quot;。
  &quot;master&quot; Egress 选择器已被弃用，推荐使用 &quot;controlplane&quot;。
  </p>
</td>
</tr>
<tr><td><code>connection</code> <B>[必需]</B><br/>
<a href="#apiserver-k8s-io-v1alpha1-Connection"><code>Connection</code></a>
</td>
<td>
   <p>
   <code>connection</code> 是用来配置 Egress 选择器的配置信息。
   </p>
</td>
</tr>
</tbody>
</table>

## `ProtocolType`     {#apiserver-k8s-io-v1alpha1-ProtocolType}

（`string` 类型的别名）

**出现在：**

- [Connection](#apiserver-k8s-io-v1alpha1-Connection)

<p>
ProtocolType 是 <code>connection.protocolType</code> 的合法值集合。
</p>

## `TCPTransport`     {#apiserver-k8s-io-v1alpha1-TCPTransport}

**出现在：**

- [Transport](#apiserver-k8s-io-v1alpha1-Transport)

<p>
TCPTransport 提供使用 TCP 连接 konnectivity 服务器时需要的信息。
</p>

<table class="table">
<tbody>

<tr><td><code>url</code> <B>[必需]</B><br/>
<code>string</code>
</td>
<td>
   <p>
   <code>url</code> 是要连接的 konnectivity 服务器的位置。例如 &quot;https://127.0.0.1:8131&quot;。
   </p>
</td>
</tr>
<tr><td><code>tlsConfig</code><br/>
<a href="#apiserver-k8s-io-v1alpha1-TLSConfig"><code>TLSConfig</code></a>
</td>
<td>
   <p>
   <code>tlsConfig</code> 是使用 TLS 来连接 konnectivity 服务器时需要的信息。
   </p>
</td>
</tr>
</tbody>
</table>

## `TLSConfig`     {#apiserver-k8s-io-v1alpha1-TLSConfig}

**出现在：**

- [TCPTransport](#apiserver-k8s-io-v1alpha1-TCPTransport)

<p>
TLSConfig 为连接 konnectivity 服务器提供身份认证信息。仅用于 TCPTransport。
</p>

<table class="table">
<tbody>

<tr><td><code>caBundle</code><br/>
<code>string</code>
</td>
<td>
   <p>
   <code>caBundle</code> 是指向用来确定与 konnectivity 服务器间信任欢喜的 CA 证书包的文件位置。
   当 <code>tcpTransport.url</code> 前缀为 "http://" 时必须不设置，或者设置为空。
   如果 <code>tcpTransport.url</code> 前缀为 "https://" 并且此字段未设置，则默认使用系统的信任根。
   </p>
</td>
</tr>
<tr><td><code>clientKey</code><br/>
<code>string</code>
</td>
<td>
   <code>clientKey</code> 是与 konnectivity 服务器进行 mtls 握手时使用的客户端秘钥文件位置。
   如果 `tcp.url` 前缀为 <code>http://</code>，必须不指定或者为空；
   如果 `tcp.url` 前缀为 <code>https://</code>，必须设置。
   </p>
</td>
</tr>
<tr><td><code>clientCert</code><br/>
<code>string</code>
</td>
<td>
   <p>
   <code>clientCert</code> 是与 konnectivity 服务器进行 mtls 握手时使用的客户端证书文件位置。
   如果 `tcp.url` 前缀为 <code>http://</code>，必须不指定或者为空；
   如果 `tcp.url` 前缀为 <code>https://</code>，必须设置。
   </p>
</td>
</tr>
</tbody>
</table>

## `Transport`     {#apiserver-k8s-io-v1alpha1-Transport}

**出现在：**

- [Connection](#apiserver-k8s-io-v1alpha1-Connection)


<p>
Transport 定义联系 konnectivity 服务器时要使用的传输层配置。
</p>

<table class="table">
<tbody>

<tr><td><code>tcp</code><br/>
<a href="#apiserver-k8s-io-v1alpha1-TCPTransport"><code>TCPTransport</code></a>
</td>
<td>
   <p>
   <code>tcp</code> 包含通过 TCP 与 konnectivity 服务器通信时使用的 TCP 配置。
   目前使用 TCP 传输时不支持 GRPC 的 <code>proxyProtocol</code>。
   <code>tcp</code> 和 <code>uds</code> 二者至少设置一个。
   </p>
</td>
</tr>
<tr><td><code>uds</code><br/>
<a href="#apiserver-k8s-io-v1alpha1-UDSTransport"><code>UDSTransport</code></a>
</td>
<td>
   <p>
   <code>uds</code> 包含通过 UDS 与 konnectivity 服务器通信时使用的 UDS 配置。
   <code>tcp</code> 和 <code>uds</code> 二者至少设置一个。
   </p>
</td>
</tr>
</tbody>
</table>

## `UDSTransport`     {#apiserver-k8s-io-v1alpha1-UDSTransport}

**出现在：**

- [Transport](#apiserver-k8s-io-v1alpha1-Transport)

<p>
UDSTransport 设置通过 UDS 连接 konnectivity 服务器时需要的信息。
</p>

<table class="table">
<tbody>


<tr><td><code>udsName</code> <B>[必需]</B><br/>
<code>string</code>
</td>
<td>
   <p>
   <code>udsName</code> 是与 konnectivity 服务器连接时使用的 UNIX 域套接字名称。
   字段取值不要求包含 <code>unix://</code> 前缀。
   （例如：<code>/etc/srv/kubernetes/konnectivity-server/konnectivity-server.socket</code>）
   </p>
</td>
</tr>
</tbody>
</table>

## `TracingConfiguration`     {#TracingConfiguration}

**出现在：**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)

- [TracingConfiguration](#apiserver-k8s-io-v1alpha1-TracingConfiguration)

<p>
TracingConfiguration 为 OpenTelemetry 跟踪客户端提供了不同版本的配置。
</p>

<table class="table">
<tbody>

<tr><td><code>endpoint</code><br/>
<code>string</code>
</td>
<td>
   <p>
   采集器的端点，此组件将向其报告跟踪信息。
   连接不安全，目前不支持 TLS。
   推荐不设置，端点为 otlp grpc 默认值 localhost:4317。
</p>
</td>
</tr>
<tr><td><code>samplingRatePerMillion</code><br/>
<code>int32</code>
</td>
<td>
   <p>
   SamplingRatePerMillion 是每百万 span 中采集的样本数。
   推荐不设置。如果不设置，采集器将继承其父级 span 的采样率，否则不进行采样。
</p>
</td>
</tr>
</tbody>
</table>
