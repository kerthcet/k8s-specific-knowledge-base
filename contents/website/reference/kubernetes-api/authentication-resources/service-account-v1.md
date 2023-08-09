---
api_metadata:
  apiVersion: "v1"
  import: "k8s.io/api/core/v1"
  kind: "ServiceAccount"
content_type: "api_reference"
description: "ServiceAccount 将以下内容绑定在一起：1. 用户可以理解的名称，也可能是外围系统理解的身份标识 2. 可以验证和授权的主体 3. 一组 Secret。"
title: "ServiceAccount"
weight: 1
auto_generated: true
---



`apiVersion: v1`

`import "k8s.io/api/core/v1"`


## ServiceAccount {#ServiceAccount}

ServiceAccount 将以下内容绑定在一起：
* 用户可以理解的名称，也可能是外围系统理解的身份标识
* 可以验证和授权的主体
* 一组 Secret

<hr>

- **apiVersion**: v1


- **kind**: ServiceAccount


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准对象的元数据，更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **automountServiceAccountToken** (boolean)

  AutomountServiceAccountToken 指示作为此服务帐户运行的 Pod 是否应自动挂载 API 令牌，
  可以在 Pod 级别覆盖。

- **imagePullSecrets** ([]<a href="{{< ref "../common-definitions/local-object-reference#LocalObjectReference" >}}">LocalObjectReference</a>)

  imagePullSecrets 是对同一命名空间中 Secret 的引用列表，用于拉取引用此 ServiceAccount 的 Pod 中的任何镜像。
  imagePullSecrets 与 Secrets 不同，因为 Secrets 可以挂载在 Pod 中，但 imagePullSecrets 只能由 kubelet 访问。
  更多信息： https://kubernetes.io/zh-cn/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod

- **secrets** ([]<a href="{{< ref "../common-definitions/object-reference#ObjectReference" >}}">ObjectReference</a>)

  **补丁策略：基于键 `name` 合并**

  Secrets 是允许使用此 ServiceAccount 运行的 Pod 使用的同一命名空间中的秘密列表。
  仅当此服务帐户的 “kubernetes.io/enforce-mountable-secrets” 注释设置为 “true” 时，Pod 才限于此列表。
  此字段不应用于查找自动生成的服务帐户令牌机密以在 Pod 之外使用。
  相反，可以使用 TokenRequest API 直接请求令牌，或者可以手动创建服务帐户令牌 Secret。
  更多信息： https://kubernetes.io/zh-cn/docs/concepts/configuration/secret

## ServiceAccountList {#ServiceAccountList}

ServiceAccountList 是 ServiceAccount 对象的列表

<hr>

- **apiVersion**: v1


- **kind**: ServiceAccountList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准列表元数据, 更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **items** ([]<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>)，必需

  ServiceAccount 列表，更多信息： https://kubernetes.io/zh-cn/docs/tasks/configure-pod-container/configure-service-account/

## 操作 {#Operations}

<hr>

### `get` 读取指定的 ServiceAccount

#### HTTP 请求

GET /api/v1/namespaces/{namespace}/serviceaccounts/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  ServiceAccount 的名称

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): OK

401: Unauthorized

### `list` 列出或监控 ServiceAccount 类型的对象

#### HTTP 请求

GET /api/v1/namespaces/{namespace}/serviceaccounts

#### 参数

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **allowWatchBookmarks** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


- **labelSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>


- **limit** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

<a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应


200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccountList" >}}">ServiceAccountList</a>): OK

401: Unauthorized

### `list` 列出或监控 ServiceAccount 类型的对象

#### HTTP 请求

GET /api/v1/serviceaccounts

#### 参数

- **allowWatchBookmarks** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


- **labelSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

<a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>


#### 响应

200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccountList" >}}">ServiceAccountList</a>): OK

401: Unauthorized

### `create` 创建一个 ServiceAccount

#### HTTP 请求

POST /api/v1/namespaces/{namespace}/serviceaccounts

#### 参数

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): OK

201 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): Created

202 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): Accepted

401: Unauthorized

`update` 替换指定的ServiceAccount

#### HTTP 请求

PUT /api/v1/namespaces/{namespace}/serviceaccounts/{name}

#### 参数

- **name** (**路径参数**): string, required

  name of the ServiceAccount


- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): OK

201 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): Created

401: Unauthorized

`patch` 部分更新指定的 ServiceAccount

#### HTTP 请求

PATCH /api/v1/namespaces/{namespace}/serviceaccounts/{name}

#### 参数

- **name** (**路径参数**): string，必需

  ServiceAccount 的名称

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, required


- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>


- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应


200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): OK

201 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): Created

401: Unauthorized

### `delete` 删除一个 ServiceAccount
#### HTTP 请求


DELETE /api/v1/namespaces/{namespace}/serviceaccounts/{name}

#### 参数

- **name** (**路径参数**): string，必需

  ServiceAccount 的名称


- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>


- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


- **propagationPolicy** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>


#### 响应

200 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): OK

202 (<a href="{{< ref "../authentication-resources/service-account-v1#ServiceAccount" >}}">ServiceAccount</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 ServiceAccount 的集合

#### HTTP 请求

DELETE /api/v1/namespaces/{namespace}/serviceaccounts

#### 参数

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **continue** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>


- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


- **gracePeriodSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **labelSelector** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>


- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

- **resourceVersion** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

<a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>


#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
