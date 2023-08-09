---
api_metadata:
  apiVersion: "v1"
  import: "k8s.io/api/core/v1"
  kind: "Service"
content_type: "api_reference"
description: "Service 是软件服务（例如 mysql）的命名抽象，包含代理要侦听的本地端口（例如 3306）和一个选择算符，选择算符用来确定哪些 Pod 将响应通过代理发送的请求。"
title: Service
weight: 1
---


`apiVersion: v1`

`import "k8s.io/api/core/v1”`

## Service {#Service}

Service 是软件服务（例如 mysql）的命名抽象，包含代理要侦听的本地端口（例如 3306）和一个选择算符，
选择算符用来确定哪些 Pod 将响应通过代理发送的请求。

<hr>

- **apiVersion**: v1

- **kind**: Service

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)


  标准的对象元数据。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../service-resources/service-v1#ServiceSpec" >}}">ServiceSpec</a>)


  spec 定义 Service 的行为。https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

- **status**（<a href="{{< ref "../service-resources/service-v1#ServiceStatus" >}}">ServiceStatus</a>）


  最近观察到的 Service 状态。由系统填充。只读。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

## ServiceSpec {#ServiceSpec}

ServiceSpec 描述用户在服务上创建的属性。

<hr>

- **selector** (map[string]string)


  将 Service 流量路由到具有与此 selector 匹配的标签键值对的 Pod。
  如果为空或不存在，则假定该服务有一个外部进程管理其端点，Kubernetes 不会修改该端点。
  仅适用于 ClusterIP、NodePort 和 LoadBalancer 类型。如果类型为 ExternalName，则忽略。
  更多信息： https://kubernetes.io/docs/concepts/services-networking/service/

- **ports** ([]ServicePort)


  **Patch strategy：基于键 `type` 合并**

  **Map：合并时将保留 type 键的唯一值**

  此 Service 公开的端口列表。
  更多信息： https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies

  <a name="ServicePort"></a>


  **ServicePort 包含有关 ServicePort 的信息。**


  - **ports.port** (int32)，必需

    Service 将公开的端口。


  - **ports.targetPort** (IntOrString)

    在 Service 所针对的 Pod 上要访问的端口号或名称。
    编号必须在 1 到 65535 的范围内。名称必须是 IANA_SVC_NAME。
    如果此值是一个字符串，将在目标 Pod 的容器端口中作为命名端口进行查找。
    如果未指定字段，则使用 "port” 字段的值（直接映射）。
    对于 clusterIP 为 None 的服务，此字段将被忽略，
    应忽略不设或设置为 "port” 字段的取值。
    更多信息： https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service

    <a name="IntOrString"></a>


    IntOrString 是一种可以保存 int32 或字符串的类型。
    在 JSON 或 YAML 编组和解组中使用时，它会生成或使用内部类型。
    例如，这允许您拥有一个可以接受名称或数字的 JSON 字段。

  - **ports.protocol** (string)


    此端口的 IP 协议。支持 “TCP”、“UDP” 和 “SCTP”。默认为 TCP。

  - **ports.name** (string)


    Service 中此端口的名称。这必须是 DNS_LABEL。
    ServiceSpec 中的所有端口的名称都必须唯一。
    在考虑 Service 的端点时，这一字段值必须与 EndpointPort 中的 `name` 字段相同。
    如果此服务上仅定义一个 ServicePort，则为此字段为可选。

  - **ports.nodePort** (int32)


    当类型为 NodePort 或 LoadBalancer 时，Service 公开在节点上的端口，
    通常由系统分配。如果指定了一个在范围内且未使用的值，则将使用该值，否则操作将失败。
    如果在创建的 Service 需要该端口时未指定该字段，则会分配端口。
    如果在创建不需要该端口的 Service时指定了该字段，则会创建失败。
    当更新 Service 时，如果不再需要此字段（例如，将类型从 NodePort 更改为 ClusterIP），这个字段将被擦除。
    更多信息： https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport

  - **ports.appProtocol** (string)


    此端口的应用协议，遵循标准的 Kubernetes 标签语法，无前缀名称按照 IANA 标准服务名称
    （参见 RFC-6335 和 https://www.iana.org/assignments/service-names）。
    非标准协议应该使用前缀名称，如 mycompany.com/my-custom-protocol。

- **type** (string)


  type 确定 Service 的公开方式。默认为 ClusterIP。
  有效选项为 ExternalName、ClusterIP、NodePort 和 LoadBalancer。
  “ClusterIP” 为端点分配一个集群内部 IP 地址用于负载均衡。
  Endpoints 由 selector 确定，如果未设置 selector，则需要通过手动构造 Endpoints 或 EndpointSlice 的对象来确定。
  如果 clusterIP 为 “None”，则不分配虚拟 IP，并且 Endpoints 作为一组端点而不是虚拟 IP 发布。
  “NodePort” 建立在 ClusterIP 之上，并在每个节点上分配一个端口，该端口路由到与 clusterIP 相同的 Endpoints。
  “LoadBalancer” 基于 NodePort 构建并创建一个外部负载均衡器（如果当前云支持），该负载均衡器路由到与 clusterIP 相同的 Endpoints。
  “externalName” 将此 Service 别名为指定的 externalName。其他几个字段不适用于 ExternalName Service。
  更多信息： https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types

- **ipFamilies** ([]string)


  **原子: 将在合并期间被替换**


  iPFamilies 是分配给此服务的 IP 协议（例如 IPv4、IPv6）的列表。
  该字段通常根据集群配置和 ipFamilyPolicy 字段自动设置。
  如果手动指定该字段，且请求的协议在集群中可用，且 ipFamilyPolicy 允许，则使用；否则服务创建将失败。
  该字段修改是有条件的：它允许添加或删除辅助 IP 协议，但不允许更改服务的主要 IP 协议。
  有效值为 “IPv4” 和 “IPv6”。
  该字段仅适用于 ClusterIP、NodePort 和 LoadBalancer 类型的服务，并且确实可用于“无头”服务。
  更新服务设置类型为 ExternalName 时，该字段将被擦除。


  该字段最多可以包含两个条目（双栈系列，按任意顺序）。
  如果指定，这些协议栈必须对应于 clusterIPs 字段的值。
  clusterIP 和 ipFamilies 都由 ipFamilyPolicy 字段管理。

- **ipFamilyPolicy** (string)


  iPFamilyPolicy 表示此服务请求或要求的双栈特性。
  如果没有提供值，则此字段将被设置为 SingleStack。
  服务可以是 “SingleStack”（单个 IP 协议）、
  “PreferDualStack”（双栈配置集群上的两个 IP 协议或单栈集群上的单个 IP 协议）
  或 “RequireDualStack”（双栈上的两个 IP 协议配置的集群，否则失败）。
  ipFamilies 和 clusterIPs 字段取决于此字段的值。
  更新服务设置类型为 ExternalName 时，此字段将被擦除。


- **clusterIP** (string)


  clusterIP 是服务的 IP 地址，通常是随机分配的。
  如果地址是手动指定的，在范围内（根据系统配置），且没有被使用，它将被分配给服务，否则创建服务将失败。
  clusterIP 一般不会被更改，除非 type 被更改为 ExternalName
  （ExternalName 需要 clusterIP 为空）或 type 已经是 ExternalName 时，可以更改 clusterIP（在这种情况下，可以选择指定此字段）。
  可选值 “None”、空字符串 (“”) 或有效的 IP 地址。
  clusterIP 为 “None” 时会生成“无头服务”（无虚拟 IP），这在首选直接 Endpoint 连接且不需要代理时很有用。
  仅适用于 ClusterIP、NodePort、和 LoadBalancer 类型的服务。
  如果在创建 ExternalName 类型的 Service 时指定了 clusterIP，则创建将失败。
  更新 Service type 为 ExternalName 时，clusterIP 会被移除。
  更多信息： https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies

- **clusterIPs** ([]string)

  **原子: 将在合并期间被替换**


  clusterIPs 是分配给该 Service 的 IP 地址列表，通常是随机分配的。
  如果地址是手动指定的，在范围内（根据系统配置），且没有被使用，它将被分配给 Service；否则创建 Service 失败。
  clusterIP 一般不会被更改，除非 type 被更改为 ExternalName
  （ExternalName 需要 clusterIPs 为空）或 type 已经是 ExternalName 时，可以更改 clusterIPs（在这种情况下，可以选择指定此字段）。
  可选值 “None”、空字符串 (“”) 或有效的 IP 地址。
  clusterIPs 为 “None” 时会生成“无头服务”（无虚拟 IP），这在首选直接 Endpoint 连接且不需要代理时很有用。
  适用于 ClusterIP、NodePort、和 LoadBalancer 类型的服务。
  如果在创建 ExternalName 类型的 Service 时指定了 clusterIPs，则会创建失败。
  更新 Service type 为 ExternalName 时，该字段将被移除。如果未指定此字段，则将从 clusterIP 字段初始化。
  如果指定 clusterIPs，客户端必须确保 clusterIPs[0] 和 clusterIP 一致。


  clusterIPs 最多可包含两个条目（双栈系列，按任意顺序）。
  这些 IP 必须与 ipFamilies 的值相对应。
  clusterIP 和 ipFamilies 都由 ipFamilyPolicy 管理。
  更多信息： https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies

- **externalIPs** ([]string)


  externalIPs 是一个 IP 列表，集群中的节点会为此 Service 接收针对这些 IP 地址的流量。
  这些 IP 不被 Kubernetes 管理。用户需要确保流量可以到达具有此 IP 的节点。
  一个常见的例子是不属于 Kubernetes 系统的外部负载均衡器。

- **sessionAffinity** (string)


  支持 “ClientIP” 和 “None”。用于维护会话亲和性。
  启用基于客户端 IP 的会话亲和性。必须是 ClientIP 或 None。默认为 None。
  更多信息： https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies

- **loadBalancerIP** (string)


  仅适用于服务类型: LoadBalancer。此功能取决于底层云提供商是否支持负载均衡器。
  如果云提供商不支持该功能，该字段将被忽略。
  已弃用: 该字段信息不足，且其含义因实现而异，而且不支持双栈。
  从 Kubernetes v1.24 开始，鼓励用户在可用时使用特定于实现的注释。在未来的 API 版本中可能会删除此字段。

- **loadBalancerSourceRanges** ([]string)


  如果设置了此字段并且被平台支持，将限制通过云厂商的负载均衡器的流量到指定的客户端 IP。
  如果云提供商不支持该功能，该字段将被忽略。
  更多信息： https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/

- **loadBalancerClass** (string)


  loadBalancerClass 是此 Service 所属的负载均衡器实现的类。
  如果设置了此字段，则字段值必须是标签风格的标识符，带有可选前缀，例如 ”internal-vip” 或 “example.com/internal-vip”。
  无前缀名称是为最终用户保留的。该字段只能在 Service 类型为 “LoadBalancer” 时设置。
  如果未设置此字段，则使用默认负载均衡器实现。默认负载均衡器现在通常通过云提供商集成完成，但应适用于任何默认实现。
  如果设置了此字段，则假定负载均衡器实现正在监测具有对应负载均衡器类的 Service。
  任何默认负载均衡器实现（例如云提供商）都应忽略设置此字段的 Service。
  只有在创建或更新的 Service 的 type 为 “LoadBalancer” 时，才可设置此字段。
  一经设定，不可更改。当 Service 的 type 更新为 “LoadBalancer” 之外的其他类型时，此字段将被移除。

- **externalName** (string)


  externalName 是发现机制将返回的外部引用，作为此服务的别名（例如 DNS CNAME 记录）。
  不涉及代理。必须是小写的 RFC-1123 主机名 (https://tools.ietf.org/html/rfc1123)，
  并且要求 `type` 为 “ExternalName”。

- **externalTrafficPolicy** (string)

  externalTrafficPolicy 描述了节点如何分发它们在 Service 的“外部访问”地址
  （NodePort、ExternalIP 和 LoadBalancer IP）接收到的服务流量。
  如果设置为 “Local”，代理将以一种假设外部负载均衡器将负责在节点之间服务流量负载均衡，
  因此每个节点将仅向服务的节点本地端点传递流量，而不会伪装客户端源 IP。
 （将丢弃错误发送到没有端点的节点的流量。）
  “Cluster” 默认值使用负载均衡路由到所有端点的策略（可能会根据拓扑和其他特性进行修改）。
  请注意，从集群内部发送到 External IP 或 LoadBalancer IP 的流量始终具有 “Cluster” 语义，
  但是从集群内部发送到 NodePort 的客户端需要在选择节点时考虑流量路由策略。

- **internalTrafficPolicy** (string)

  InternalTrafficPolicy 描述节点如何分发它们在 ClusterIP 上接收到的服务流量。
  如果设置为 “Local”，代理将假定 Pod 只想与在同一节点上的服务端点通信，如果没有本地端点，它将丢弃流量。
  “Cluster” 默认将流量路由到所有端点（可能会根据拓扑和其他特性进行修改）。

- **healthCheckNodePort** (int32)

  healthCheckNodePort 指定 Service 的健康检查节点端口。
  仅适用于 type 为 LoadBalancer 且 externalTrafficPolicy 设置为 Local 的情况。
  如果为此字段设定了一个值，该值在合法范围内且没有被使用，则使用所指定的值。
  如果未设置此字段，则自动分配字段值。外部系统（例如负载平衡器）可以使用此端口来确定给定节点是否拥有此服务的端点。
  在创建不需要 healthCheckNodePort 的 Service 时指定了此字段，则 Service 创建会失败。
  要移除 healthCheckNodePort，需要更改 Service 的 type。
  该字段一旦设置就无法更改。

- **publishNotReadyAddresses** (boolean)


  publishNotReadyAddresses 表示任何处理此 Service 端点的代理都应忽略任何准备就绪/未准备就绪的指示。
  设置此字段的主要场景是为 StatefulSet 的服务提供支持，使之能够为其 Pod 传播 SRV DNS 记录，以实现对等发现。
  为 Service 生成 Endpoints 和 EndpointSlice 资源的 Kubernetes 控制器对字段的解读是，
  即使 Pod 本身还没有准备好，所有端点都可被视为 “已就绪”。
  对于代理而言，如果仅使用 Kubernetes 通过 Endpoints 或 EndpointSlice 资源所生成的端点，
  则可以安全地假设这种行为。

- **sessionAffinityConfig** (SessionAffinityConfig)

  sessionAffinityConfig 包含会话亲和性的配置。

  <a name="SessionAffinityConfig"></a>

  **SessionAffinityConfig 表示会话亲和性的配置。**

  - **sessionAffinityConfig.clientIP** (ClientIPConfig)

    
    clientIP 包含基于客户端 IP 的会话亲和性的配置。

    <a name="ClientIPConfig"></a>
  

    ClientIPConfig 表示基于客户端 IP 的会话亲和性的配置。

    - **sessionAffinityConfig.clientIP.timeoutSeconds** (int32)


      timeoutSeconds 指定 ClientIP 类型会话的维系时间秒数。
      如果 ServiceAffinity == "ClientIP"，则该值必须 >0 && <=86400（1 天）。默认值为 10800（3 小时）。

- **allocateLoadBalancerNodePorts** (boolean)


  allocateLoadBalancerNodePorts 定义了是否会自动为 LoadBalancer 类型的 Service 分配 NodePort。默认为 true。
  如果集群负载均衡器不依赖 NodePort，则可以设置此字段为 false。
  如果调用者（通过指定一个值）请求特定的 NodePort，则无论此字段如何，都会接受这些请求。
  该字段只能设置在 type 为 LoadBalancer 的 Service 上，如果 type 更改为任何其他类型，该字段将被移除。

## ServiceStatus {#ServiceStatus}

ServiceStatus 表示 Service 的当前状态。

<hr>

- **conditions** ([]Condition)


  **Patch strategy: 在 `type` 上合并**

  **Map: 键类型的唯一值将在合并期间保留**

  服务的当前状态。

  <a name="Condition"></a>


  **condition 包含此 API 资源某一方面当前的状态详细信息。**

  
  - **conditions.lastTransitionTime**（Time），必需

    lastTransitionTime 是状况最近一次状态转化的时间。
    变化应该发生在下层状况发生变化的时候。如果不知道下层状况发生变化的时间，
    那么使用 API 字段更改的时间是可以接受的。

    <a name="Time"></a>
  

    Time 是 time.Time 的包装类，支持正确地序列化为 YAML 和 JSON。
    为 time 包提供的许多工厂方法提供了包装类。


  - **conditions.message** (string)，必需


    message 是人类可读的消息，有关转换的详细信息，可以是空字符串。


  - **conditions.reason** (string)，必需

  
    reason 包含一个程序标识符，指示 condition 最后一次转换的原因。
    特定条件类型的生产者可以定义该字段的预期值和含义，以及这些值是否被视为有保证的 API。
    该值应该是 CamelCase 字符串且不能为空。


  - **conditions.status** (string)，必需


    condition 的状态，True、False、Unknown 之一。


  - **conditions.type** (string)，必需


    CamelCase 或 foo.example.com/CamelCase 中的条件类型。

  - **conditions.observedGeneration** (int64)


    observedGeneration 表示设置 condition 基于的 .metadata.generation 的过期次数。
    例如，如果 .metadata.generation 当前为 12，但 .status.conditions[x].observedGeneration 为 9，
    则 condition 相对于实例的当前状态已过期。

- **loadBalancer** (LoadBalancerStatus)


  loadBalancer 包含负载均衡器的当前状态（如果存在）。

  <a name="LoadBalancerStatus"></a>


  **LoadBalancerStatus 表示负载均衡器的状态。**

  - **loadBalancer.ingress** ([]LoadBalancerIngress)

  
    ingress 是一个包含负载均衡器 Ingress 点的列表。Service 的流量需要被发送到这些 Ingress 点。

    <a name="LoadBalancerIngress"></a>
  

    **LoadBalancerIngress 表示负载平衡器入口点的状态: 用于服务的流量是否被发送到入口点。**

    - **loadBalancer.ingress.hostname** (string)


      hostname 是为基于 DNS 的负载均衡器 Ingress 点（通常是 AWS 负载均衡器）设置的。

    - **loadBalancer.ingress.ip** (string)


      ip 是为基于 IP 的负载均衡器 Ingress 点（通常是 GCE 或 OpenStack 负载均衡器）设置的。

    - **loadBalancer.ingress.ports** ([]PortStatus)


      **Atomic: 将在合并期间被替换**


      ports 是 Service 的端口列表。如果设置了此字段，Service 中定义的每个端口都应该在此列表中。

      <a name="PortStatus"></a>


      - **loadBalancer.ingress.ports.port** (int32)，必需


        port 是所记录的服务端口状态的端口号。


      - **loadBalancer.ingress.ports.protocol** (string)，必需


        protocol 是所记录的服务端口状态的协议。支持的值为：“TCP”、”UDP”、“SCTP”。

      - **loadBalancer.ingress.ports.error** (string)


        error 是记录 Service 端口的问题。
        错误的格式应符合以下规则:  
        - 内置错误原因应在此文件中指定，应使用 CamelCase 名称。
        - 云提供商特定错误原因的名称必须符合格式 foo.example.com/CamelCase。

## ServiceList {#ServiceList}


ServiceList 包含一个 Service 列表。

<hr>

- **apiVersion**: v1

- **kind**: Service 列表

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准列表元数据。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds


- **items**（[]<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>），必需


  Service 列表


## 操作  {#operations}

<hr>


### `get` 读取指定的 Service

#### HTTP 请求

GET /api/v1/namespaces/{namespace}/services/{name}

#### 参数

- **name** (**查询参数**)：string，必需

  Service 名称

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: OK

401: Unauthorized


### `get` 读取指定 Service 的状态

#### HTTP 请求

GET /api/v1/namespaces/{namespace}/services/{name}/status


#### 参数

- **name** (**路径参数**)：string，必需


  Service 名称

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: OK

401: Unauthorized


### `list` 列出或监测 Service 类型的对象

#### HTTP 请求

GET /api/v1/namespaces/{namespace}/services


#### 参数

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **allowWatchBookmarks**（**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch**（**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>


#### 响应

200（<a href="{{< ref "../service-resources/service-v1#ServiceList" >}}">ServiceList</a>）: OK

401: Unauthorized


### `list` 列出或监测 Service 类型的对象

#### HTTP 请求

GET /api/v1/services


#### 参数

- **allowWatchBookmarks**（**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>

- **continue**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **fieldSelector**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **labelSelector**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **resourceVersion**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch**（**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>


#### 响应

200（<a href="{{< ref "../service-resources/service-v1#ServiceList" >}}">ServiceList</a>）: OK

401: Unauthorized


### `create` 创建一个 Service

#### HTTP 请求

POST /api/v1/namespaces/{namespace}/services


#### 参数

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: OK

201（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: Created

202（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: Accepted

401: Unauthorized


### `update` 替换指定的 Service

#### HTTP 请求

PUT /api/v1/namespaces/{namespace}/services/{name}


#### 参数

- **name** (**路径参数**)：string，必需


  Service 名称

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: OK

201（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: Created

401: Unauthorized


### `update` 替换指定 Service 的状态

#### HTTP 请求

PUT /api/v1/namespaces/{namespace}/services/{name}/status


#### 参数

- **name** (**路径参数**)：string，必需


  Service 名称

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: OK

201（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: Created

401: Unauthorized


### `patch` 部分更新指定的 Service

#### HTTP 请求

PATCH /api/v1/namespaces/{namespace}/services/{name}


#### 参数

- **name** (**路径参数**)：string，必需


  Service 名称

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force**（**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: OK

201（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: Created

401: Unauthorized

### `patch` 部分更新指定 Service 的状态

#### HTTP 请求

PATCH /api/v1/namespaces/{namespace}/services/{name}/status


#### 参数

- **name** (**路径参数**)：string，必需


  Service 名称

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force**（**查询参数**）：boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


#### 响应

200（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: OK

201（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: Created

401: Unauthorized


### `delete` 删除 Service

#### HTTP 请求

DELETE /api/v1/namespaces/{namespace}/services/{name}


#### 参数

- **name** (**路径参数**)：string，必需


  Service 名称

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **正文**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>


#### 响应

200（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: OK

202（<a href="{{< ref "../service-resources/service-v1#Service" >}}">Service</a>）: Accepted

401: Unauthorized


### `deletecollection` 删除 Service 集合

#### HTTP 请求

DELETE /api/v1/namespaces/{namespace}/services


#### 参数

- **namespace**（**路径参数**）：string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **continue**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>

- **dryRun**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldSelector**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>

- **gracePeriodSeconds**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **labelSelector**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>

- **limit**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>

- **pretty**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

- **resourceVersion**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>

- **resourceVersionMatch**（**查询参数**）：string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>

- **sendInitialEvents** (**查询参数**): boolean

  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>

- **timeoutSeconds**（**查询参数**）：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>


#### 响应

200（<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>）: OK

401: Unauthorized
