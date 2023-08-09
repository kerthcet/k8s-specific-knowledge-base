---
title: Event Rate Limit Configuration (v1alpha1)
content_type: tool-reference
package: eventratelimit.admission.k8s.io/v1alpha1
---

## 资源类型  {#resource-types}

- [Configuration](#eventratelimit-admission-k8s-io-v1alpha1-Configuration)

## `Configuration`     {#eventratelimit-admission-k8s-io-v1alpha1-Configuration}

<p>Configuration 为 EventRateLimit 准入控制器提供配置数据。</p>

<table class="table">
<tbody>

<tr><td><code>apiVersion</code><br/>string</td><td><code>eventratelimit.admission.k8s.io/v1alpha1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>Configuration</code></td></tr>

<tr><td><code>limits</code> <B>[Required]</B><br/>
<a href="#eventratelimit-admission-k8s-io-v1alpha1-Limit"><code>[]Limit</code></a>
</td>
<td>
  <p>limits 是为所接收到的事件查询设置的限制。可以针对服务器端接收到的事件设置限制，
按逐个名字空间、逐个用户、或逐个来源+对象组合的方式均可以。
至少需要设置一种限制。</p>
</td>
</tr>
</tbody>
</table>

## `Limit`     {#eventratelimit-admission-k8s-io-v1alpha1-Limit}

**出现在：**

- [Configuration](#eventratelimit-admission-k8s-io-v1alpha1-Configuration)

<p>Limit 是为特定限制类型提供的配置数据。</p>

<table class="table">
<tbody>

<a href="#eventratelimit-admission-k8s-io-v1alpha1-LimitType"><code>LimitType</code></a>
</td>
<td>
  <p>type 是此配置所适用的限制的类型。</p>
</td>
</tr>
<code>int32</code>
</td>
<td>
   <p>qps 是针对此类型的限制每秒钟所允许的事件查询次数。qps 和 burst
字段一起用来确定是否特定的事件查询会被接受。qps 确定的是当超出查询数量的
burst 值时可以接受的查询个数。</p>
</td>
</tr>
<code>int32</code>
</td>
<td>
   <p>burst 是针对此类型限制的突发事件查询数量。qps 和 burst 字段一起使用可用来确定特定的事件查询是否被接受。
burst 字段确定针对特定的事件桶（bucket）可以接受的规模上限。
例如，如果 burst 是 10，qps 是 3，那么准入控制器会在接收 10 个查询之后阻塞所有查询。
每秒钟可以额外允许 3 个查询。如果这一限额未被用尽，则剩余的限额会被顺延到下一秒钟，
直到再次达到 10 个限额的上限。</p>
</td>
</tr>
<tr><td><code>cacheSize</code><br/>
<code>int32</code>
</td>
<td>
   <p>cacheSize 是此类型限制的 LRU 缓存的规模。如果某个事件桶（bucket）被从缓存中剔除，
该事件桶所对应的限额也会被重置。如果后来再次收到针对某个已被剔除的事件桶的查询，
则该事件桶会重新以干净的状态进入缓存，因而获得全量的突发查询配额。</p>
  <p>默认的缓存大小是 4096。</p>
  <p>如果 limitType 是 “server”，则 cacheSize 设置会被忽略。</p>
</td>
</tr>
</tbody>
</table>

## `LimitType`     {#eventratelimit-admission-k8s-io-v1alpha1-LimitType}

（`string` 类型的别名）

**出现在：**

- [Limit](#eventratelimit-admission-k8s-io-v1alpha1-Limit)

<p>LimitType 是限制类型（例如：per-namespace）。</p>


