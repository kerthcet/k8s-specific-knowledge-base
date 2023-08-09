---
title: kube-apiserver 配置 (v1beta1)
content_type: tool-reference
package: apiserver.k8s.io/v1beta1
---

<p>v1beta1 包是 v1beta1 版本的 API。</p>

## 资源类型   {#resource-types}

- [EgressSelectorConfiguration](#apiserver-k8s-io-v1beta1-EgressSelectorConfiguration)
- [TracingConfiguration](#apiserver-k8s-io-v1beta1-TracingConfiguration)

## `EgressSelectorConfiguration`     {#apiserver-k8s-io-v1beta1-EgressSelectorConfiguration}

<p>
EgressSelectorConfiguration 为 Egress 选择算符客户端提供版本化的配置选项。
</p>

<table class="table">
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>apiserver.k8s.io/v1beta1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>EgressSelectorConfiguration</code></td></tr>

<a href="#apiserver-k8s-io-v1beta1-EgressSelection"><code>[]EgressSelection</code></a>
</td>
<td>
   <p>
   connectionServices 包含一组 Egress 选择算符客户端配置选项。
   </p>
</td>
</tr>
</tbody>
</table>

## `TracingConfiguration`     {#apiserver-k8s-io-v1beta1-TracingConfiguration}

<p>
TracingConfiguration 为跟踪客户端提供版本化的配置信息。
</p>

<table class="table">
<tbody>

<tr><td><code>apiVersion</code><br/>string</td><td><code>apiserver.k8s.io/v1beta1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>TracingConfiguration</code></td></tr>

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

## `Connection`     {#apiserver-k8s-io-v1beta1-Connection}

**出现在：**

- [EgressSelection](#apiserver-k8s-io-v1beta1-EgressSelection)

<p>
Connection 提供某个 Egress 选择客户端的配置信息。
</p>

<table class="table">
<tbody>

<a href="#apiserver-k8s-io-v1beta1-ProtocolType"><code>ProtocolType</code></a>
</td>
<td>
   <p>
   proxyProtocol 是客户端连接到 konnectivity 服务器所使用的协议。
   </p>
</td>
</tr>
<tr><td><code>transport</code><br/>
<a href="#apiserver-k8s-io-v1beta1-Transport"><code>Transport</code></a>
</td>
<td>
   <p>
   transport 定义的是传输层的配置。我们使用这个配置来联系 konnectivity 服务器。
   当 proxyProtocol 是 HTTPConnect 或 GRPC 时需要设置此字段。
   </p>
</td>
</tr>
</tbody>
</table>

## `EgressSelection`     {#apiserver-k8s-io-v1beta1-EgressSelection}

**出现在：**

- [EgressSelectorConfiguration](#apiserver-k8s-io-v1beta1-EgressSelectorConfiguration)

<p>
EgressSelection 为某个 Egress 选择客户端提供配置信息。
</p>

<table class="table">
<tbody>
  
<code>string</code>
</td>
<td>
   <p>
   name 是 Egress 选择算符的名称。当前支持的取值有 &quot;controlplane&quot;，
   &quot;master&quot;，&quot;etcd&quot; 和 &quot;cluster&quot;。
   &quot;master&quot; Egress 选择算符已被弃用，推荐使用 &quot;controlplane&quot;。
   </p>
</td>
</tr>
<a href="#apiserver-k8s-io-v1beta1-Connection"><code>Connection</code></a>
</td>
<td>
   <p>
   connection 是用来配置 Egress 选择算符的配置信息。
   </p>
</td>
</tr>
</tbody>
</table>

## `ProtocolType`     {#apiserver-k8s-io-v1beta1-ProtocolType}
   
（`string` 类型的别名）

**出现在：**

- [Connection](#apiserver-k8s-io-v1beta1-Connection)

<p>
ProtocolType 是 connection.protocolType 的合法值集合。
</p>

## `TCPTransport`     {#apiserver-k8s-io-v1beta1-TCPTransport}

**出现在：**

- [Transport](#apiserver-k8s-io-v1beta1-Transport)

<p>
TCPTransport 提供使用 TCP 连接 konnectivity 服务器时需要的信息。
</p>

<table class="table">
<tbody>

<code>string</code>
</td>
<td>
   <p>
   url 是要连接的 konnectivity 服务器的位置。例如 &quot;https://127.0.0.1:8131&quot;。
   </p>
</td>
</tr>
<tr><td><code>tlsConfig</code><br/>
<a href="#apiserver-k8s-io-v1beta1-TLSConfig"><code>TLSConfig</code></a>
</td>
<td>
   <p>
   tlsConfig 是使用 TLS 来连接 konnectivity 服务器时需要的信息。
   </p>
</td>
</tr>
</tbody>
</table>

## `TLSConfig`     {#apiserver-k8s-io-v1beta1-TLSConfig}

**出现在：**

- [TCPTransport](#apiserver-k8s-io-v1beta1-TCPTransport)

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
   caBundle 是指向用来确定与 konnectivity 服务器间信任关系的 CA 证书包的文件位置。
   如果 TCPTransport.URL 前缀为 "http://" 时必须不设置，或者设置为空。
   如果 TCPTransport.URL 前缀为 "https://" 并且此字段未设置，则默认使用系统的信任根。
   </p>
</td>
</tr>
<tr><td><code>clientKey</code><br/>
<code>string</code>
</td>
<td>
   clientKey 是与 konnectivity 服务器进行 mtls 握手时使用的客户端秘钥文件位置。
   如果 TCPTransport.URL 前缀为 http://，必须不指定或者为空；
   如果 TCPTransport.URL 前缀为 https://，必须设置。
   </p>
</td>
</tr>
<tr><td><code>clientCert</code><br/>
<code>string</code>
</td>
<td>
   <p>
   <code>clientCert</code> 是与 konnectivity 服务器进行 mtls 握手时使用的客户端证书文件位置。
   如果 TCPTransport.URL 前缀为 http://，必须不指定或者为空；
   如果 TCPTransport.URL 前缀为 https://，必须设置。
   </p>
</td>
</tr>
</tbody>
</table>

## `Transport`     {#apiserver-k8s-io-v1beta1-Transport}

**出现在：**

- [Connection](#apiserver-k8s-io-v1beta1-Connection)

<p>
Transport 定义联系 konnectivity 服务器时要使用的传输层配置。
</p>

<table class="table">
<tbody>

<tr><td><code>tcp</code><br/>
<a href="#apiserver-k8s-io-v1beta1-TCPTransport"><code>TCPTransport</code></a>
</td>
<td>
   <p>
   tcp 包含通过 TCP 与 konnectivity 服务器通信时使用的 TCP 配置。
   目前使用 TCP 传输时不支持 GRPC 的 proxyProtocol。
   tcp 和 uds 二者至少设置一个。
   </p>
</td>
</tr>
<tr><td><code>uds</code><br/>
<a href="#apiserver-k8s-io-v1beta1-UDSTransport"><code>UDSTransport</code></a>
</td>
<td>
   <p>
   uds 包含通过 UDS 与 konnectivity 服务器通信时使用的 UDS 配置。
   tcp 和 uds 二者至少设置一个。
   </p>
</td>
</tr>
</tbody>
</table>

## `UDSTransport`     {#apiserver-k8s-io-v1beta1-UDSTransport}

**出现在：**

- [Transport](#apiserver-k8s-io-v1beta1-Transport)

<p>
UDSTransport 设置通过 UDS 连接 konnectivity 服务器时需要的信息。
</p>

<table class="table">
<tbody>

<code>string</code>
</td>
<td>
   <p>
   udsName 是与 konnectivity 服务器连接时使用的 UNIX 域套接字名称。
   字段取值不要求包含 unix:// 前缀。
   （例如：/etc/srv/kubernetes/konnectivity-server/konnectivity-server.socket）
   </p>
</td>
</tr>
</tbody>
</table>  

## `TracingConfiguration`     {#TracingConfiguration}
   
**出现在：**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)

- [TracingConfiguration](#apiserver-k8s-io-v1alpha1-TracingConfiguration)

- [TracingConfiguration](#apiserver-k8s-io-v1beta1-TracingConfiguration)

<p>
TracingConfiguration 为 OpenTelemetry 跟踪客户端提供了不同版本的配置。
</p>

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
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
   samplingRatePerMillion 是每百万 span 中采集的样本数。
   推荐不设置。如果不设置，采集器将继承其父级 span 的采样率，否则不进行采样。
   </p>
</td>
</tr>
</tbody>
</table>