---
api_metadata:
  apiVersion: "authentication.k8s.io/v1beta1"
  import: "k8s.io/api/authentication/v1beta1"
  kind: "SelfSubjectReview"
content_type: "api_reference"
description: "SelfSubjectReview 包含 kube-apiserver 所拥有的与发出此请求的用户有关的用户信息。"
title: "SelfSubjectReview v1beta1"
weight: 6
---

`apiVersion: authentication.k8s.io/v1beta1`

`import "k8s.io/api/authentication/v1beta1"`

## SelfSubjectReview {#SelfSubjectReview}

SelfSubjectReview 包含 kube-apiserver 所拥有的与发出此请求的用户有关的用户信息。
使用伪装时，用户将收到被伪装用户的用户信息。
如果使用伪装或请求头部进行身份验证，则所有额外的键都将被忽略大小写并以小写形式返回结果。

<hr>

- **apiVersion**: authentication.k8s.io/v1beta1

- **kind**: SelfSubjectReview

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **status** (<a href="{{< ref "../authentication-resources/self-subject-review-v1beta1#SelfSubjectReviewStatus" >}}">SelfSubjectReviewStatus</a>)

  status 由服务器以用户属性进行填充。

## SelfSubjectReviewStatus {#SelfSubjectReviewStatus}

SelfSubjectReviewStatus 由 kube-apiserver 进行填充并发送回用户。

<hr>

- **userInfo** (UserInfo)

  发出此请求的用户的用户属性。

  <a name="UserInfo"></a>
  **userInfo 包含实现 user.Info 接口所需的用户相关信息。**

  - **userInfo.extra** (map[string][]string)


    由身份认证组件提供的所有附加信息。

  - **userInfo.groups** ([]string)


    此用户所属的用户组的名称。

  - **userInfo.uid** (string)


    跨时间标识此用户的唯一值。如果此用户被删除且另一个同名用户被添加，他们将具有不同的 UID。

  - **userInfo.username** (string)


    在所有活跃用户中标识此用户的名称。

## 操作 {#Operations}

<hr>

### `create` 创建 SelfSubjectReview

#### HTTP 请求

POST /apis/authentication.k8s.io/v1beta1/selfsubjectreviews

#### 参数

- **body**: <a href="{{< ref "../authentication-resources/self-subject-review-v1beta1#SelfSubjectReview" >}}">SelfSubjectReview</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../authentication-resources/self-subject-review-v1beta1#SelfSubjectReview" >}}">SelfSubjectReview</a>): OK

201 (<a href="{{< ref "../authentication-resources/self-subject-review-v1beta1#SelfSubjectReview" >}}">SelfSubjectReview</a>): Created

202 (<a href="{{< ref "../authentication-resources/self-subject-review-v1beta1#SelfSubjectReview" >}}">SelfSubjectReview</a>): Accepted

401: Unauthorized
