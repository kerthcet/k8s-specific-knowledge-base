---
api_metadata:
  apiVersion: "rbac.authorization.k8s.io/v1"
  import: "k8s.io/api/rbac/v1"
  kind: "RoleBinding"
content_type: "api_reference"
description: "RoleBinding 引用一个角色，但不包含它。"
title: "RoleBinding"
weight: 9
auto_generated: false
---
`apiVersion: rbac.authorization.k8s.io/v1`

`import "k8s.io/api/rbac/v1"`

## RoleBinding {#RoleBinding}
RoleBinding 引用一个角色，但不包含它。
RoleBinding 可以引用相同命名空间中的 Role 或全局命名空间中的 ClusterRole。
RoleBinding 通过 Subjects 和所在的命名空间信息添加主体信息。
处于给定命名空间中的 RoleBinding 仅在该命名空间中有效。

<hr>

- **apiVersion**: rbac.authorization.k8s.io/v1

- **kind**: RoleBinding

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)
  标准的对象元数据。

- **roleRef** (RoleRef)，必需
  
  roleRef 可以引用当前命名空间中的 Role 或全局命名空间中的 ClusterRole。
  如果无法解析 roleRef，则 Authorizer 必定返回一个错误。
  
  <a name="RoleRef"></a>
  **roleRef 包含指向正被使用的角色的信息。**
  - **roleRef.apiGroup** (string)，必需
    
    apiGroup 是被引用资源的组
  
  - **roleRef.kind** (string)，必需
    
    kind 是被引用的资源的类别
  
  - **roleRef.name** (string)，必需
    
    name 是被引用的资源的名称
- **subjects** ([]Subject)
  
  subjects 包含角色所适用的对象的引用。
  
  <a name="Subject"></a>
  **Subject 包含对角色绑定所适用的对象或用户标识的引用。其中可以包含直接 API 对象的引用或非对象（如用户名和组名）的值。**
  
  - **subjects.kind** (string)，必需
    
    被引用的对象的类别。
    这个 API 组定义的值是 `User`、`Group` 和 `ServiceAccount`。
    如果 Authorizer 无法识别类别值，则 Authorizer 应报告一个错误。
  - **subjects.name** (string)，必需
    
    被引用的对象的名称。
  
  - **subjects.apiGroup** (string)
    
    apiGroup 包含被引用主体的 API 组。
    对于 ServiceAccount 主体默认为 ""。
    对于 User 和 Group 主体，默认为 "rbac.authorization.k8s.io"。
  
  - **subjects.namespace** (string)
    
    被引用的对象的命名空间。
    如果对象类别是 “User” 或 “Group” 等非命名空间作用域的对象且该值不为空，
    则 Authorizer 应报告一个错误。

## RoleBindingList {#RoleBindingList}
RoleBindingList 是 RoleBinding 的集合。

<hr>

- **apiVersion**: rbac.authorization.k8s.io/v1

- **kind**: RoleBindingList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)
  标准的对象元数据。

- **items** ([]<a href="{{< ref "../authorization-resources/role-binding-v1#RoleBinding" >}}">RoleBinding</a>)，必需
  
  items 是 RoleBinding 的列表。
## 操作 {#Operations}

<hr>

### `get` 读取指定的 RoleBinding

#### HTTP 请求

GET /apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/rolebindings/{name}
#### 参数

- **name** (**路径参数**): string，必需
  
  RoleBinding 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../authorization-resources/role-binding-v1#RoleBinding" >}}">RoleBinding</a>): OK

401: Unauthorized
### `list` 列出或观测类别为 RoleBinding 的对象

#### HTTP 请求

GET /apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/rolebindings
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

200 (<a href="{{< ref "../authorization-resources/role-binding-v1#RoleBindingList" >}}">RoleBindingList</a>): OK

401: Unauthorized
### `list` 列出或观测类别为 RoleBinding 的对象

#### HTTP 请求

GET /apis/rbac.authorization.k8s.io/v1/rolebindings
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

200 (<a href="{{< ref "../authorization-resources/role-binding-v1#RoleBindingList" >}}">RoleBindingList</a>): OK

401: Unauthorized
### `create` 创建 RoleBinding

#### HTTP 请求

POST /apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/rolebindings
#### 参数

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../authorization-resources/role-binding-v1#RoleBinding" >}}">RoleBinding</a>，必需

- **dryRun** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>
#### 响应

200 (<a href="{{< ref "../authorization-resources/role-binding-v1#RoleBinding" >}}">RoleBinding</a>): OK

201 (<a href="{{< ref "../authorization-resources/role-binding-v1#RoleBinding" >}}">RoleBinding</a>): Created

202 (<a href="{{< ref "../authorization-resources/role-binding-v1#RoleBinding" >}}">RoleBinding</a>): Accepted

401: Unauthorized
### `update` 替换指定的 RoleBinding

#### HTTP 请求

PUT /apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/rolebindings/{name}
#### 参数

- **name** (**路径参数**): string，必需
  
  RoleBinding 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../authorization-resources/role-binding-v1#RoleBinding" >}}">RoleBinding</a>，必需

- **dryRun** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>
#### 响应

200 (<a href="{{< ref "../authorization-resources/role-binding-v1#RoleBinding" >}}">RoleBinding</a>): OK

201 (<a href="{{< ref "../authorization-resources/role-binding-v1#RoleBinding" >}}">RoleBinding</a>): Created

401: Unauthorized
### `patch` 部分更新指定的 RoleBinding

#### HTTP 请求

PATCH /apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/rolebindings/{name}
#### 参数

- **name** (**路径参数**): string，必需
  
  RoleBinding 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

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

200 (<a href="{{< ref "../authorization-resources/role-binding-v1#RoleBinding" >}}">RoleBinding</a>): OK

201 (<a href="{{< ref "../authorization-resources/role-binding-v1#RoleBinding" >}}">RoleBinding</a>): Created

401: Unauthorized
### `delete` 删除 RoleBinding

#### HTTP 请求

DELETE /apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/rolebindings/{name}
#### 参数

- **name** (**路径参数**): string，必需
  
  RoleBinding 的名称

- **namespace** (**路径参数**): string，必需
  
  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** (**查询参数**): integer
  
  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (**查询参数**): string
  
  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>
#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): Accepted

401: Unauthorized
### `deletecollection` 删除 RoleBinding 的集合

#### HTTP 请求

DELETE /apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/rolebindings
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