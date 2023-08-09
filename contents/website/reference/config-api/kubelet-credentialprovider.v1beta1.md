---
title: Kubelet CredentialProvider (v1beta1)
content_type: tool-reference
package: credentialprovider.kubelet.k8s.io/v1beta1
---

## 资源类型   {#resource-types}

- [CredentialProviderRequest](#credentialprovider-kubelet-k8s-io-v1beta1-CredentialProviderRequest)
- [CredentialProviderResponse](#credentialprovider-kubelet-k8s-io-v1beta1-CredentialProviderResponse)

## `CredentialProviderRequest`     {#credentialprovider-kubelet-k8s-io-v1beta1-CredentialProviderRequest}

<p>
CredentialProviderRequest 包含 kubelet 需要进行身份验证的镜像。
Kubelet 会通过标准输入将此请求对象传递给插件。一般来说，插件倾向于用它们所收到的相同的 apiVersion 来响应。
</p>

<table class="table">
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>credentialprovider.kubelet.k8s.io/v1beta1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>CredentialProviderRequest</code></td></tr>
    
  
<code>string</code>
</td>
<td>
   <p>
   <code>image</code> 是容器镜像，作为凭据提供程序插件请求的一部分。
   插件可以有选择地解析镜像以提取获取凭据所需的任何信息。
   </p>
</td>
</tr>
</tbody>
</table>

## `CredentialProviderResponse`     {#credentialprovider-kubelet-k8s-io-v1beta1-CredentialProviderResponse}

<p>
CredentialProviderResponse 持有 kubelet 应用于原始请求中提供的指定镜像的凭据。
kubelet 将通过标准输出读取插件的响应。此响应的 apiVersion 值应设置为与 CredentialProviderRequest 中 apiVersion 值相同。
</p>


<table class="table">
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>credentialprovider.kubelet.k8s.io/v1beta1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>CredentialProviderResponse</code></td></tr>
    
  
<a href="#credentialprovider-kubelet-k8s-io-v1beta1-PluginCacheKeyType"><code>PluginCacheKeyType</code></a>
</td>
<td>
   <p>
   <code>cacheKeyType</code> 表明基于请求中所给镜像而要使用的缓存键类型。缓存键类型有三个有效值：
   Image、Registry 和 Global。如果指定了无效值，则 kubelet 不会使用该响应。
   </p>
</td>
</tr>
<tr><td><code>cacheDuration</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   <p>
   <code>cacheDuration</code> 表示所提供的凭据应该被缓存的时间。kubelet 使用这个字段为
   <code>auth</code> 中的凭据设置内存中数据的缓存时间。如果为空，kubelet 将使用 CredentialProviderConfig
   中提供的 defaultCacheDuration。如果设置为 0，kubelet 将不会缓存所提供的 <code>auth</code> 数据。
   </p>
</td>
</tr>
<tr><td><code>auth</code><br/>
<a href="#credentialprovider-kubelet-k8s-io-v1beta1-AuthConfig"><code>map[string]k8s.io/kubelet/pkg/apis/credentialprovider/v1beta1.AuthConfig</code></a>
</td>
<td>
   <p>
   <code>auth</code> 是一个映射，其中包含传递到 kubelet 的身份验证信息。
   每个键都是一个匹配镜像字符串（下面将对此进行详细介绍）。相应的 authConfig 值应该对所有与此键匹配的镜像有效。
   如果不能为请求的镜像返回有效的凭据，插件应将此字段设置为 null。
   </p>
   <p>
   映射中每个键值都是一个正则表达式，可以选择包含端口和路径。
   域名部分可以包含通配符，但在端口或路径中不能使用通配符。
   支持通配符作为子域，如 <code>&ast;.k8s.io</code> 或 <code>k8s.&ast;.io</code>，以及顶级域，如 <code>k8s.&ast;</code>。
   还支持匹配部分子域，如 <code>app&ast;.k8s.io</code>。每个通配符只能匹配一个子域段，
   因此 <code>&ast;.io</code> 不匹配 <code>&ast;.k8s.io</code>。
   </p>
   <p>
   当满足以下所有条件时，kubelet 会将镜像与键值匹配：
   </p>
   <ul>
    <li>两者都包含相同数量的域部分，并且每个部分都匹配。</li>
    <li><code>imageMatch</code> 的 URL 路径必须是目标镜像的 URL 路径的前缀。</li>
    <li>如果 <code>imageMatch</code> 包含端口，则该端口也必须在镜像中匹配。</li>
   </ul>
   <p>
   当返回多个键（key）时，kubelet 会倒序遍历所有键，这样：
   </p>
   <ul>
    <li>具有相同前缀的较长键位于较短键之前</li>
    <li>具有相同前缀的非通配符键位于通配符键之前。</li>
   </ul>
   <p>
   对于任何给定的匹配，kubelet 将尝试使用提供的凭据进行镜像拉取，并在第一次成功验证后停止拉取。
   </p>
   <p>键值示例：</p>
<ul>
<li>123456789.dkr.ecr.us-east-1.amazonaws.com</li>
<li>&ast;.azurecr.io</li>
<li>gcr.io</li>
<li>&ast;.&ast;.registry.io</li>
<li>registry.io:8080/path</li>
</ul>
</td>
</tr>
</tbody>
</table>

## `AuthConfig`     {#credentialprovider-kubelet-k8s-io-v1beta1-AuthConfig}
    
**出现在：**

- [CredentialProviderResponse](#credentialprovider-kubelet-k8s-io-v1beta1-CredentialProviderResponse)

AuthConfig 包含容器仓库的身份验证信息。目前仅支持基于用户名/密码的身份验证，但未来可能会添加更多身份验证机制。

<table class="table">
<tbody>
    
  
<code>string</code>
</td>
<td>
   <p>
   <code>username</code> 是用于向容器仓库进行身份验证的用户名。空的用户名是合法的。
   </p>
</td>
</tr>
<code>string</code>
</td>
<td>
   <p>
   <code>password</code> 是用于向容器仓库进行身份验证的密码。空密码是合法的。
   </p>
</td>
</tr>
</tbody>
</table>

## `PluginCacheKeyType`     {#credentialprovider-kubelet-k8s-io-v1beta1-PluginCacheKeyType}

（<code>string</code> 数据类型的别名）

**出现在：**

- [CredentialProviderResponse](#credentialprovider-kubelet-k8s-io-v1beta1-CredentialProviderResponse)