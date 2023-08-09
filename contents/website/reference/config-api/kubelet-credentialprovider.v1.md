---
title: Kubelet CredentialProvider (v1)
content_type: tool-reference
package: credentialprovider.kubelet.k8s.io/v1
---

## 资源类型  {#resource-types}

- [CredentialProviderRequest](#credentialprovider-kubelet-k8s-io-v1-CredentialProviderRequest)
- [CredentialProviderResponse](#credentialprovider-kubelet-k8s-io-v1-CredentialProviderResponse)

## `CredentialProviderRequest`     {#credentialprovider-kubelet-k8s-io-v1-CredentialProviderRequest}

<p>
CredentialProviderRequest 包含 kubelet 需要通过身份验证才能访问的镜像。
kubelet 将此请求对象通过 stdin 传递到插件。
通常，插件应优先使用所收到的 apiVersion 作出响应。
</p>

<table class="table">
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>credentialprovider.kubelet.k8s.io/v1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>CredentialProviderRequest</code></td></tr>
    
  
<code>string</code>
</td>
<td>
<p>
image 是作为凭据提供程序插件请求的一部分所拉取的容器镜像。
这些插件可以选择解析镜像以提取获取凭据所需的任何信息。
</p>

</td>
</tr>
</tbody>
</table>

## `CredentialProviderResponse`     {#credentialprovider-kubelet-k8s-io-v1-CredentialProviderResponse}

<p>
CredentialProviderResponse 中包含 kubelet 应针对原始请求中所给镜像来使用的凭据。
kubelet 将通过 stdout 读取来自插件的响应。
此响应应被设置为与 CredentialProviderRequest 相同的 apiVersion。
</p>

<table class="table">
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>credentialprovider.kubelet.k8s.io/v1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>CredentialProviderResponse</code></td></tr>
    
  
<a href="#credentialprovider-kubelet-k8s-io-v1-PluginCacheKeyType"><code>PluginCacheKeyType</code></a>
</td>
<td>
<p>
cacheKeyType 标示了基于请求中提供的镜像要使用的缓存键的类型。
缓存键类型有三个有效值：Image、Registry 和 Global。
如果所指定的值无效，则此响应不会被 kubelet 使用。
</p>
</td>
</tr>
<tr><td><code>cacheDuration</code><br/>
<a href="https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
<p>
cacheDuration 标示所提供的凭据可被缓存的持续期。
kubelet 将使用此字段为 AuthConfig 中的凭据设置内存中缓存持续期。
如果为空，kubelet 将使用 CredentialProviderConfig 中提供的 defaultCacheDuration。
如果设置为 0，kubelet 将不再缓存提供的 AuthConfig。
</p>
</td>
</tr>
<tr><td><code>auth</code><br/>
<a href="#credentialprovider-kubelet-k8s-io-v1-AuthConfig"><code>map[string]k8s.io/kubelet/pkg/apis/credentialprovider/v1.AuthConfig</code></a>
</td>
<td>
<p>
auth 是一个映射，包含传递给 kubelet 的身份验证信息。
映射中每个键都是一个匹配镜像字符串（更多内容见下文）。
相应的 authConfig 值应该对匹配此键的所有镜像有效。
如果无法为请求的镜像返回有效凭据，则插件应将此字段设置为空。
</p>
<p>
映射中的每个主键都可以包含端口和路径。
域名中可以使用 Glob 通配，但不能在端口或路径中使用 Glob。
Glob 支持类似 <code>&ast;.k8s.io</code> 或 <code>k8s.&ast;.io</code> 这类子域以及 <code>k8s.&ast;</code> 这类顶级域。
也支持匹配的部分子域，例如 <code>app&ast;.k8s.io</code>。
每个 Glob 只能匹配一个子域段，因此 <code>&ast;.io</code> 与 <code>&ast;.k8s.io</code> 不匹配。
</p>
<p>
当满足以下所有条件时，kubelet 将根据主键来匹配镜像：
</p>
<ul>
<li>两者都包含相同数量的域名部分，并且每个部分都匹配。</li>
<li>imageMatch 的 URL 路径必须是目标镜像 URL 路径的前缀。</li>
<li>如果 imageMatch 包含端口，则此端口也必须在镜像中匹配。</li>
</ul>
<p>
当返回多个主键时，kubelet 将以相反的顺序遍历所有主键，以便：
</p>
  <ul>
  <li>较长键出现在具有相同前缀的较短键前面。</li>
  <li>非通配符键出现在具有相同前缀的通配符键之前。</li>
  </ul>
<p>对于任一给定的匹配项，kubelet 将尝试用提供的凭据拉取镜像，并在第一次成功通过身份验证的拉取之后停止。</p>
<p>示例键：</p>
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

## `AuthConfig`     {#credentialprovider-kubelet-k8s-io-v1-AuthConfig}

**出现在：**

- [CredentialProviderResponse](#credentialprovider-kubelet-k8s-io-v1-CredentialProviderResponse)

<p>
AuthConfig 包含针对容器镜像仓库的身份验证信息。
目前仅支持基于用户名/密码的身份验证，但未来可能添加更多的身份验证机制。
</p>

<table class="table">
<tbody>

<code>string</code>
</td>
<td>
<p>
username 是对容器镜像仓库身份验证所用的用户名。
空白用户名是有效的。
</p>
</td>
</tr>
<code>string</code>
</td>
<td>
<p>
password 是对容器镜像仓库身份验证所用的密码。
空白密码是有效的。
</p>
</td>
</tr>
</tbody>
</table>

## `PluginCacheKeyType`     {#credentialprovider-kubelet-k8s-io-v1-PluginCacheKeyType}

（`string` 的别名）

**出现在：**

- [CredentialProviderResponse](#credentialprovider-kubelet-k8s-io-v1-CredentialProviderResponse)
  