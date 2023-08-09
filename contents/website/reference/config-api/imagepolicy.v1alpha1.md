---
title: Image Policy API (v1alpha1)
content_type: tool-reference
package: imagepolicy.k8s.io/v1alpha1
---

## 资源类型   {#resource-types}

- [ImageReview](#imagepolicy-k8s-io-v1alpha1-ImageReview)

## `ImageReview`     {#imagepolicy-k8s-io-v1alpha1-ImageReview}

<p>ImageReview 检查某个 Pod 中是否可以使用某些镜像。</p>

<table class="table">
<tbody>

<tr><td><code>apiVersion</code><br/>string</td><td><code>imagepolicy.k8s.io/v1alpha1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>ImageReview</code></td></tr>

<tr><td><code>metadata</code><br/>
<a href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#objectmeta-v1-meta"><code>meta/v1.ObjectMeta</code></a>
</td>
<td>
  <p>标准的对象元数据。更多信息：https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata</p>
  参阅 Kubernetes API 文档了解 <code>metadata</code> 字段的内容。
</td>

</tr>
<tr><td><code>spec</code> <B>[必需]</B><br/>
<a href="#imagepolicy-k8s-io-v1alpha1-ImageReviewSpec"><code>ImageReviewSpec</code></a>
</td>
<td>
  <p>spec 中包含与被评估的 Pod 相关的信息。</p>
</td>
</tr>
<tr><td><code>status</code><br/>
<a href="#imagepolicy-k8s-io-v1alpha1-ImageReviewStatus"><code>ImageReviewStatus</code></a>
</td>
<td>
  <p>status 由后台负责填充，用来标明 Pod 是否会被准入。</p>
</td>
</tr>
</tbody>
</table>

## `ImageReviewContainerSpec`     {#imagepolicy-k8s-io-v1alpha1-ImageReviewContainerSpec}

**出现在：**

- [ImageReviewSpec](#imagepolicy-k8s-io-v1alpha1-ImageReviewSpec)

<p>ImageReviewContainerSpec 是对 Pod 创建请求中的某容器的描述。</p>


<table class="table">
<tbody>

<tr><td><code>image</code><br/>
<code>string</code>
</td>
<td>
  <p>此字段的格式可以是 image:tag 或 image@SHA:012345679abcdef。</p>
</td>
</tr>
</tbody>
</table>

## `ImageReviewSpec`     {#imagepolicy-k8s-io-v1alpha1-ImageReviewSpec}

**出现在：**

- [ImageReview](#imagepolicy-k8s-io-v1alpha1-ImageReview)

<p>ImageReviewSpec 是对 Pod 创建请求的描述。</p>

<table class="table">
<tbody>

<tr><td><code>containers</code><br/>
<a href="#imagepolicy-k8s-io-v1alpha1-ImageReviewContainerSpec"><code>[]ImageReviewContainerSpec</code></a>
</td>
<td>
  <p>containers 是一个列表，其中包含正被创建的 Pod 中各容器的信息子集。</p>
</td>
</tr>
<tr><td><code>annotations</code><br/>
<code>map[string]string</code>
</td>
<td>
  <p>annotations 是一个键值对列表，内容抽取自 Pod 的注解（annotations）。
其中仅包含与模式 <code>*.image-policy.k8s.io/*</code> 匹配的键。
每个 Webhook 后端要负责决定如何解释这些注解（如果有的话）。</p>

</td>
</tr>
<tr><td><code>namespace</code><br/>
<code>string</code>
</td>
<td>
  <p>namespace 是 Pod 创建所针对的名字空间。</p>
</td>
</tr>
</tbody>
</table>

## `ImageReviewStatus`     {#imagepolicy-k8s-io-v1alpha1-ImageReviewStatus}

**出现在：**

- [ImageReview](#imagepolicy-k8s-io-v1alpha1-ImageReview)

<p>ImageReviewStatus 是针对 Pod 创建请求所作的评估结果。</p>

<table class="table">
<tbody>

<tr><td><code>allowed</code> <B>[必需]</B><br/>
<code>bool</code>
</td>
<td>
  <p>allowed 表明所有镜像都可以被运行。</p>
</td>
</tr>
<tr><td><code>reason</code><br/>
<code>string</code>
</td>
<td>
  <p>若 <code>allowed</code> 不是 false，<code>reason</code> 应该为空。
否则其中应包含出错信息的简短描述。Kubernetes 在向用户展示此信息时可能会截断过长的错误文字。</p>
</td>
</tr>
<tr><td><code>auditAnnotations</code><br/>
<code>map[string]string</code>
</td>
<td>
  <p>auditAnnotations 会被通过 <code>AddAnnotation</code> 添加到准入控制器的 attributes 对象上。
注解键应该不含前缀，换言之，准入控制器会添加合适的前缀。</p>
</td>
</tr>
</tbody>
</table>

