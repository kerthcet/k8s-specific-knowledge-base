---
api_metadata:
  apiVersion: "networking.k8s.io/v1"
  import: "k8s.io/api/networking/v1"
  kind: "IngressClass"
content_type: "api_reference"
description: "IngressClass 代表 Ingress 的类，被 Ingress 的规约引用。"
title: "IngressClass"
weight: 5
---


`apiVersion: networking.k8s.io/v1`

`import "k8s.io/api/networking/v1"`

## IngressClass {#IngressClass}

IngressClass 代表 Ingress 的类，被 Ingress 的规约引用。
`ingressclass.kubernetes.io/is-default-class`
注解可以用来标明一个 IngressClass 应该被视为默认的 Ingress 类。
当某个 IngressClass 资源将此注解设置为 true 时，
没有指定类的新 Ingress 资源将被分配到此默认类。

<hr>

- **apiVersion**: networking.k8s.io/v1

- **kind**: IngressClass

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的列表元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../service-resources/ingress-class-v1#IngressClassSpec" >}}">IngressClassSpec</a>)

  spec 是 IngressClass 的期望状态。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

## IngressClassSpec {#IngressClassSpec}

IngressClassSpec 提供有关 Ingress 类的信息。

<hr>

- **controller** (string)

  
  controller 是指应该处理此类的控制器名称。
  这允许由同一控制器控制不同“口味”。例如，对于同一个实现的控制器你可能有不同的参数。
  此字段应该指定为长度不超过 250 个字符的域前缀路径，例如 “acme.io/ingress-controller”。
  该字段是不可变的。

- **parameters** (IngressClassParametersReference)

  
  parameters 是指向控制器中包含额外配置的自定义资源的链接。
  如果控制器不需要额外的属性，这是可选的。

  <a name="IngressClassParametersReference"></a>
  **IngressClassParametersReference 标识一个 API 对象。这可以用来指定一个集群或者命名空间范围的资源**


  - **parameters.kind** (string)，必需
    
    kind 是被引用资源的类型。


  - **parameters.name** (string)，必需

    name 是被引用资源的名称。

  - **parameters.apiGroup** (string)

    apiGroup 是被引用资源的组。
    如果未指定 apiGroup，则被指定的 kind 必须在核心 API 组中。
    对于任何其他第三方类型，apiGroup 是必需的。

  - **parameters.namespace** (string)

    namespace 是被引用资源的命名空间。
    当范围被设置为 “namespace” 时，此字段是必需的；
    当范围被设置为 “Cluster” 时，此字段必须不设置。

  - **parameters.scope** (string)

    scope 表示是否引用集群或者命名空间范围的资源。
    这可以设置为“集群”（默认）或者“命名空间”。

## IngressClassList {#IngressClassList}

IngressClassList 是 IngressClasses 的集合。

<hr>

- **apiVersion**: networking.k8s.io/v1

- **kind**: IngressClassList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据。

- **items** ([]<a href="{{< ref "../service-resources/ingress-class-v1#IngressClass" >}}">IngressClass</a>)，必需

  items 是 IngressClasses 的列表。

## 操作 {#Operations}

<hr>

### `get` 读取指定的 IngressClass

#### HTTP 请求

GET /apis/networking.k8s.io/v1/ingressclasses/{name}

#### 参数

- **name** （**路径参数**）：string，必需

  IngressClass 的名称

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/ingress-class-v1#IngressClass" >}}">IngressClass</a>): OK

401: Unauthorized

### `list` 列出或监视 IngressClass 类型的对象

#### HTTP 请求

GET /apis/networking.k8s.io/v1/ingressclasses

#### 参数

- **allowWatchBookmarks** （**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** （**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** （**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** （**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../service-resources/ingress-class-v1#IngressClassList" >}}">IngressClassList</a>): OK

401: Unauthorized

### `create` 创建一个 IngressClass

#### HTTP 请求

POST /apis/networking.k8s.io/v1/ingressclasses

#### 参数

- **body**: <a href="{{< ref "../service-resources/ingress-class-v1#IngressClass" >}}">IngressClass</a>，必需

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/ingress-class-v1#IngressClass" >}}">IngressClass</a>): OK

201 (<a href="{{< ref "../service-resources/ingress-class-v1#IngressClass" >}}">IngressClass</a>): Created

202 (<a href="{{< ref "../service-resources/ingress-class-v1#IngressClass" >}}">IngressClass</a>): Accepted

401: Unauthorized

### `update` 替换指定的 IngressClass

#### HTTP 请求

PUT /apis/networking.k8s.io/v1/ingressclasses/{name}

#### 参数

- **name** （**路径参数**）：string，必需

  IngressClass 的名称

- **body**: <a href="{{< ref "../service-resources/ingress-class-v1#IngressClass" >}}">IngressClass</a>，必需

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/ingress-class-v1#IngressClass" >}}">IngressClass</a>): OK

201 (<a href="{{< ref "../service-resources/ingress-class-v1#IngressClass" >}}">IngressClass</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 IngressClass

#### HTTP 请求

PATCH /apis/networking.k8s.io/v1/ingressclasses/{name}

#### 参数

- **name** （**路径参数**）：string，必需

  IngressClass 的名称

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** （**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/ingress-class-v1#IngressClass" >}}">IngressClass</a>): OK

201 (<a href="{{< ref "../service-resources/ingress-class-v1#IngressClass" >}}">IngressClass</a>): Created

401: Unauthorized

### `delete` 删除一个 IngressClass

#### HTTP 请求

DELETE /apis/networking.k8s.io/v1/ingressclasses/{name}

#### 参数

- **name** （**路径参数**）：string，必需

  IngressClass 的名称

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** （**查询字符串**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 IngressClass 的集合

DELETE /apis/networking.k8s.io/v1/ingressclasses

#### 参数

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **continue** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **dryRun** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **gracePeriodSeconds** （**查询字符串**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **labelSelector** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit** （**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

- **resourceVersion** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch** （**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** （**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
