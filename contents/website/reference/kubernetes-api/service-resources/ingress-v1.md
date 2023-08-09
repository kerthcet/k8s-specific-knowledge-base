---
api_metadata:
  apiVersion: "networking.k8s.io/v1"
  import: "k8s.io/api/networking/v1"
  kind: "Ingress"
content_type: "api_reference"
description: "Ingress 是允许入站连接到达后端定义的端点的规则集合。"
title: "Ingress"
weight: 4
---

`apiVersion: networking.k8s.io/v1`

`import "k8s.io/api/networking/v1"`

## Ingress {#Ingress}

Ingress 是允许入站连接到达后端定义的端点的规则集合。
Ingress 可以配置为向服务提供外部可访问的 URL、负载均衡流量、终止 SSL、提供基于名称的虚拟主机等。

<hr>

- **apiVersion**: networking.k8s.io/v1

- **kind**: Ingress

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../service-resources/ingress-v1#IngressSpec" >}}">IngressSpec</a>)


  spec 是 Ingress 的预期状态。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

- **status** (<a href="{{< ref "../service-resources/ingress-v1#IngressStatus" >}}">IngressStatus</a>)


  status 是 Ingress 的当前状态。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

## IngressSpec {#IngressSpec}

IngressSpec 描述用户希望存在的 Ingress。

<hr>

- **defaultBackend** (<a href="{{< ref "../service-resources/ingress-v1#IngressBackend" >}}">IngressBackend</a>)


  defaultBackend 是负责处理与任何规则都不匹配的请求的后端。
  如果未指定 rules，则必须指定 defaultBackend。
  如果未设置 defaultBackend，则不符合任何 rules 的请求的处理将由 Ingress 控制器决定。

- **ingressClassName** (string)

  ingressClassName 是 IngressClass 集群资源的名称。
  Ingress 控制器实现使用此字段来了解它们是否应该通过传递连接（控制器 -> IngressClass -> Ingress 资源）为该
  Ingress 资源提供服务。尽管 `kubernetes.io/ingress.class` 注解（简单的常量名称）从未正式定义，
  但它被 Ingress 控制器广泛支持，以在 Ingress 控制器和 Ingress 资源之间创建直接绑定。
  新创建的 Ingress 资源应该优先选择使用该字段。但是，即使注解已被正式弃用，
  出于向后兼容性的原因，Ingress 控制器仍应能够处理该注解（如果存在）。

- **rules** ([]IngressRule)


  **Atomic: 将在合并期间被替换**

  rules 是用于配置 Ingress 的主机规则列表。如果未指定或没有规则匹配，则所有流量都将发送到默认后端。


  <a name="IngressRule"></a>
  **IngressRule 表示将指定主机下的路径映射到相关后端服务的规则。
  传入请求首先评估主机匹配，然后路由到与匹配的 IngressRuleValue 关联的后端。**

  - **rules.host** (string)


    host 是 RFC 3986 定义的网络主机的完全限定域名。请注意以下与 RFC 3986 中定义的 URI 的 “host” 部分的偏差：

    1. 不允许 IP。当前 IngressRuleValue 只能应用于父 Ingress Spec 中的 IP。
    2. 由于不允许使用端口，因此不理会 “:” 分隔符。
       当前 Ingress 的端口隐式为：

       - `:80` 用于 http
       - `:443` 用于 https

    这两种情况在未来都可能发生变化。入站请求在通过 IngressRuleValue 处理之前先进行 host 匹配。
    如果主机未指定，Ingress 将根据指定的 IngressRuleValue 规则路由所有流量。


    host 可以是 “精确“ 的，设置为一个不含终止句点的网络主机域名（例如 “foo.bar.com” ），
    也可以是一个 “通配符”，设置为以单个通配符标签为前缀的域名（例如 “*.foo.com”）。
    通配符 “*” 必须单独显示为第一个 DNS 标签，并且仅与单个标签匹配。
    你不能单独使用通配符作为标签（例如，Host=“*”）。请求将按以下方式与主机字段匹配：

    1. 如果 host 是精确匹配的，则如果 http `Host` 标头等于 host 值，则请求与此规则匹配。
    2. 如果 host 是用通配符给出的，那么如果 HTTP `Host` 标头与通配符规则的后缀（删除第一个标签）相同，
       则请求与此规则匹配。

  - **rules.http** (HTTPIngressRuleValue)


    <a name="HTTPIngressRuleValue"></a>
    **HTTPIngressRuleValue 是指向后端的 http 选择算符列表。例如 `http://<host>/<path>?<searchpart> -> 后端`，
    其中 `url` 的部分对应于 RFC 3986，此资源将用于匹配最后一个 “/” 之后和第一个 “?” 之前的所有内容或 “#”。**


    - **rules.http.paths** ([]HTTPIngressPath)，必需


      **Atomic: 将在合并期间被替换**

      paths 是一个将请求映射到后端的路径集合。

      <a name="HTTPIngressPath"></a>
      **HTTPIngressPath 将路径与后端关联。与路径匹配的传入 URL 将转发到后端。**


      - **rules.http.paths.backend** (<a href="{{< ref "../service-resources/ingress-v1#IngressBackend" >}}">IngressBackend</a>)，必需

        backend 定义将流量转发到的引用服务端点。


      - **rules.http.paths.pathType** (string)，必需


        pathType 决定如何解释 path 匹配。pathType 可以是以下值之一：

        * `Exact`：与 URL 路径完全匹配。

        * `Prefix`：根据按 “/” 拆分的 URL 路径前缀进行匹配。
          匹配是按路径元素逐个元素完成。路径元素引用的是路径中由“/”分隔符拆分的标签列表。
          如果每个 p 都是请求路径 p 的元素前缀，则请求与路径 p 匹配。
          请注意，如果路径的最后一个元素是请求路径中的最后一个元素的子字符串，则匹配不成功
          （例如 `/foo/bar` 匹配 `/foo/bar/baz`，但不匹配 `/foo/barbaz`）。

        * ImplementationSpecific：路径匹配的解释取决于 IngressClass。
          实现可以将其视为单独的路径类型，也可以将其视为前缀或确切的路径类型。
          实现需要支持所有路径类型。

      - **rules.http.paths.path** (string)


        path 要与传入请求的路径进行匹配。
        目前，它可以包含 RFC 3986 定义的 URL 的常规 “路径” 部分所不允许的字符。
        路径必须以 “/” 开头，并且在 pathType 值为 “Exact” 或 “Prefix” 时必须存在。

- **tls** ([]IngressTLS)

  **Atomic: 将在合并期间被替换**

  tls 表示 TLS 配置。目前，Ingress 仅支持一个 TLS 端口 443。
  如果此列表的多个成员指定了不同的主机，如果实现 Ingress 的 Ingress 控制器支持 SNI，
  则它们将根据通过 SNI TLS 扩展指定的主机名在同一端口上多路复用。

  <a name="IngressTLS"></a>

  **IngressTLS 描述与 Ingress 相关的传输层安全性。**

  - **tls.hosts** ([]string)


    **Atomic: 将在合并期间被替换**

    hosts 是 TLS 证书中包含的主机列表。
    此列表中的值必须与 tlsSecret 中使用的名称匹配。
    默认为实现此 Ingress 的负载均衡控制器的通配符主机设置（如果未指定）。

  - **tls.secretName** (string)


    secretName 是用于终止端口 443 上 TLS 通信的 Secret 的名称。
    字段是可选的，以允许仅基于 SNI 主机名的 TLS 路由。
    如果侦听器中的 SNI 主机与入口规则使用的 “Host” 标头字段冲突，则 SNI 主机用于终止，Host 标头的值用于路由。

## IngressBackend {#IngressBackend}

IngressBackend 描述给定服务和端口的所有端点。

<hr>


- **resource** (<a href="{{< ref "../common-definitions/typed-local-object-reference#TypedLocalObjectReference" >}}">TypedLocalObjectReference</a>)

  resource 是对 Ingress 对象所在命名空间中另一个 Kubernetes 资源的引用。
  如果指定了 resource，则不得指定 service.name 和 service.port。
  此字段是一个与 `service` 互斥的设置。

- **service** (IngressServiceBackend)


  service 引用一个 Service 作为后端。此字段是一个与 `resource` 互斥的设置。

  <a name="IngressServiceBackend"></a>
  **IngressServiceBackend 引用一个 Kubernetes Service 作为后端。**

  - **service.name** (string)，必需


    name 是引用的服务。服务必须与 Ingress 对象位于同一命名空间中。

  - **service.port** (ServiceBackendPort)

    所引用的服务的端口。IngressServiceBackend 需要端口名或端口号。

    <a name="ServiceBackendPort"></a>
    **ServiceBackendPort 是被引用的服务的端口。**

    - **service.port.name** (string)


      name 是服务上的端口名称。此字段是一个与 `number` 互斥的设置。

    - **service.port.number** (int32)


      number 是服务上的数字形式端口号（例如 80）。此字段是一个与 `name` 互斥的设置。

## IngressStatus {#IngressStatus}

IngressStatus 描述 Ingress 的当前状态。

<hr>

- **loadBalancer** (IngressLoadBalancerStatus)


  loadBalancer 包含负载均衡器的当前状态。

  <a name="IngressLoadBalancerStatus"></a>
  **IngressLoadBalancerStatus 表示负载均衡器的状态。**

  - **loadBalancer.ingress** ([]IngressLoadBalancerIngress)


    ingress 是一个包含负载均衡器入口点的列表。

    <a name="IngressLoadBalancerIngress"></a>
    **IngressLoadBalancerIngress 表示负载均衡器入口点的状态。**

    - **loadBalancer.ingress.hostname** (string)


      hostname 是为基于 DNS 的负载平衡器入口点所设置的主机名。

    - **loadBalancer.ingress.ip** (string)


      ip 是为基于 IP 的负载平衡器入口点设置的 IP。

    - **loadBalancer.ingress.ports** ([]IngressPortStatus)


      **Atomic: 将在合并期间被替换**

      ports 提供有关此 LoadBalancer 公开端口的信息。

      <a name="IngressPortStatus"></a>
      **IngressPortStatus 表示服务端口的错误情况**


      - **loadBalancer.ingress.ports.port** (int32)，必需


        port 是入栈端口的端口号


      - **loadBalancer.ingress.ports.protocol** (string)，必需


        protocol 是入栈端口的协议。支持的值为：“TCP”、“UDP”、“SCTP”。

      - **loadBalancer.ingress.ports.error** (string)


        error 用来记录服务端口的问题。错误的格式应符合以下规则：

        - 应在此文件中指定内置错误码，并且错误码应使用驼峰法命名。
        - 特定于云驱动的错误码名称必须符合 `foo.example.com/CamelCase` 格式。

## IngressList {#IngressList}

IngressList 是 Ingress 的集合。

<hr>

- **items** ([]<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>)，必需

  items 是 Ingress 的列表。


- **apiVersion** (string)

  apiVersion 定义对象表示的版本化模式。
  服务器应将已识别的架构转换为最新的内部值，并且可能会拒绝未识别的值。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources

- **kind** (string)


  kind 是一个字符串值，表示此对象所表示的 REST 资源。
  服务器可以从客户端向其提交请求的端点推断出这一点。不能被更新。采用驼峰编码。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

## 操作 {#Operations}

<hr>

### `get` 读取指定的 Ingress

#### HTTP 请求

GET /apis/networking.k8s.io/v1/namespaces/{namespace}/ingresses/{name}

#### 参数

- **name** (**路径参数**)：string，必需

  Ingress 的名称。


- **namespace** (**路径参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): OK

401: Unauthorized

### `get` 读取指定 Ingress 状态

#### HTTP 请求

GET /apis/networking.k8s.io/v1/namespaces/{namespace}/ingresses/{name}/status

#### 参数

- **name** (**路径参数**)：string，必需

  Ingress 的名称。

- **namespace** (**路径参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): OK

401: Unauthorized

### `list` 列出或监测 Ingress 类型对象

#### HTTP 请求

GET /apis/networking.k8s.io/v1/namespaces/{namespace}/ingresses

#### 参数

- **namespace** (**路径参数**)：string，必需

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

200 (<a href="{{< ref "../service-resources/ingress-v1#IngressList" >}}">IngressList</a>): OK

401: Unauthorized

### `list` 列出或监测 Ingress 类型对象

#### HTTP 请求

GET /apis/networking.k8s.io/v1/ingresses

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

- **resourceVersionMatch** (*in query*): string
-->
- **resourceVersionMatch** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../service-resources/ingress-v1#IngressList" >}}">IngressList</a>): OK

401: Unauthorized

### `create` 创建一个 Ingress

#### HTTP 请求

POST /apis/networking.k8s.io/v1/namespaces/{namespace}/ingresses

#### 参数

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>，必需
  
- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): OK

201 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): Created

202 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): Accepted

401: Unauthorized

### `update` 替换指定的 Ingress

#### HTTP 请求

PUT /apis/networking.k8s.io/v1/namespaces/{namespace}/ingresses/{name}

#### 参数

- **name** (**路径参数**): string，必需

  Ingress 的名称。

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): OK

201 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): Created

401: Unauthorized

### `update` 替换指定 Ingress 的状态

#### HTTP 请求

PUT /apis/networking.k8s.io/v1/namespaces/{namespace}/ingresses/{name}/status

#### 参数

- **name** (**路径参数**)：string，必需

  Ingress 的名称。

- **namespace** (**路径参数**)：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): OK

201 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 Ingress

#### HTTP 请求

PATCH /apis/networking.k8s.io/v1/namespaces/{namespace}/ingresses/{name}

#### 参数

- **name** (**路径参数**)：string，必需

  Ingress 的名称。

- **namespace** (**路径参数**)：string，必需

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

200 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): OK

201 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): Created

401: Unauthorized

### `patch` 部分更新指定 Ingress 的状态

#### HTTP 请求

PATCH /apis/networking.k8s.io/v1/namespaces/{namespace}/ingresses/{name}/status

#### 参数

- **name** (**路径参数**)：string，必需

  Ingress 的名称。

- **namespace** (**路径参数**)：string，必需

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

200 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): OK

201 (<a href="{{< ref "../service-resources/ingress-v1#Ingress" >}}">Ingress</a>): Created

401: Unauthorized

### `delete` 删除一个 Ingress

#### HTTP 请求

DELETE /apis/networking.k8s.io/v1/namespaces/{namespace}/ingresses/{name}

#### 参数

- **name** (**路径参数**)：string，必需

  Ingress 的名称。

- **namespace** (**路径参数**)：string，必需

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

### `deletecollection` 删除 Ingress 的集合

#### HTTP 请求

DELETE /apis/networking.k8s.io/v1/namespaces/{namespace}/ingresses

#### 参数

- **namespace** (**路径参数**)：string，必需

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

- **timeoutSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
