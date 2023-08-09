---
title: 服务（Service）
feature:
  title: 服务发现与负载均衡
  description: >
    无需修改你的应用程序去使用陌生的服务发现机制。Kubernetes 为容器提供了自己的 IP 地址和一个 DNS 名称，并且可以在它们之间实现负载均衡。
description: >-
  将在集群中运行的应用程序暴露在单个外向端点后面，即使工作负载分散到多个后端也是如此。
content_type: concept
weight: 10
---


{{< glossary_definition term_id="service" length="short" prepend="Kubernetes 中 Service 是" >}}

Kubernetes 中 Service 的一个关键目标是让你无需修改现有应用程序就能使用不熟悉的服务发现机制。
你可以在 Pod 中运行代码，无需顾虑这是为云原生世界设计的代码，还是为已容器化的老应用程序设计的代码。
你可以使用 Service 让一组 Pod 在网络上可用，让客户端能够与其交互。

如果你使用 {{< glossary_tooltip term_id="deployment" >}} 来运行你的应用，
Deployment 可以动态地创建和销毁 Pod。不管是这一刻还是下一刻，
你不知道有多少个这样的 Pod 正在工作以及健康与否；你可能甚至不知道那些健康的 Pod 是如何命名的。
Kubernetes {{< glossary_tooltip term_id="pod" text="Pod" >}} 被创建和销毁以匹配集群的预期状态。
Pod 是临时资源（你不应该期待单个 Pod 既可靠又耐用）。

每个 Pod 获取其自己的 IP 地址（Kubernetes 期待网络插件确保 IP 地址分配）。
对于集群中给定的 Deployment，这一刻运行的这组 Pod 可能不同于下一刻运行应用程序的那组 Pod。

这导致了一个问题： 如果一组 Pod（称为“后端”）为集群内的其他 Pod（称为“前端”）提供功能，
那么前端如何找出并跟踪要连接的 IP 地址，以便前端可以使用提供工作负载的后端部分？


## Kubernetes 中的 Service   {#service-in-k8s}

Service API 是 Kubernetes 的组成部分，它是一种抽象，帮助你通过网络暴露 Pod 组合。
每个 Service 对象定义一个逻辑组的端点（通常这些端点是 Pod）以及如何才能访问这些 Pod 的策略。

举个例子，考虑一个图片处理后端，它运行了 3 个副本。这些副本是可互换的 ——
前端不需要关心它们调用了哪个后端副本。
然而组成这一组后端程序的 Pod 实际上可能会发生变化，
前端客户端不应该也没必要知道，而且也不需要跟踪这一组后端的状态。

Service 定义的抽象能够解耦这种关联。

Service 针对的这组 Pod 通常由你定义的{{< glossary_tooltip text="选择算符" term_id="selector" >}}来确定。
若想了解定义 Service 端点的其他方式，可以查阅[**不带**选择算符的 Service](#services-without-selectors)。

如果你的工作负载以 HTTP 通信，你可能会选择使用 [Ingress](/zh-cn/docs/concepts/services-networking/ingress/)
来控制 Web 流量如何到达该工作负载。Ingress 不是一种 Service，但它可用作集群的入口点。
Ingress 能让你将路由规则整合到单个资源，这样你就能在单个侦听器之后暴露工作负载的多个组件，在集群中分别运行这些组件。

Kubernetes 所用的 [Gateway](https://gateway-api.sigs.k8s.io/#what-is-the-gateway-api) API
提供了除 Ingress 和 Service 之外的更多功能。你可以添加 Gateway 到你的集群。Gateway 是使用
{{< glossary_tooltip term_id="CustomResourceDefinition" text="CustomResourceDefinitions" >}}
实现的一系列扩展 API。将 Gateway 添加到你的集群后，就可以使用这些 Gateway 配置如何访问集群中正运行的网络服务。

### 云原生服务发现   {#cloud-native-discovery}

如果你想要在应用程序中使用 Kubernetes API 进行服务发现，则可以查询
{{< glossary_tooltip text="API 服务器" term_id="kube-apiserver" >}}用于匹配 EndpointSlices。
只要服务中的这组 Pod 发生变化，Kubernetes 就会为服务更新 EndpointSlices。

对于非本机应用程序，Kubernetes 提供了在应用程序和后端 Pod 之间放置网络端口或负载均衡器的方法。

## 定义 Service   {#defining-a-service}

Service 在 Kubernetes 中是一个{{< glossary_tooltip text="对象" term_id="object" >}}
（与 Pod 或 ConfigMap 类似的对象）。你可以使用 Kubernetes API 创建、查看或修改 Service 定义。
通常你使用 `kubectl` 这类工具来进行这些 API 调用。

例如，假定有一组 Pod，每个 Pod 都在侦听 TCP 端口 9376，同时还被打上 `app.kubernetes.io/name=MyApp` 标签。
你可以定义一个 Service 来发布 TCP 侦听器。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

应用上述清单将创建一个名称为 "my-service" 的新 Service，
该服务[服务类型](#publishing-services-service-types)默认为 ClusterIP。
该服务指向带有标签 `app.kubernetes.io/name: MyApp` 的所有 Pod 的TCP 端口 9376。

Kubernetes 为该服务分配一个 IP 地址（有时称为 “集群 IP”），该 IP 地址由虚拟 IP 地址机制使用。
有关该机制的更多详情，请阅读[虚拟 IP 和服务代理](/zh-cn/docs/reference/networking/virtual-ips/)。

Service 的控制器不断扫描与其选择算符匹配的 Pod，然后对 Service 的 EndpointSlices 集合执行所有必要的更新。

Service 对象的名称必须是有效的
[RFC 1035 标签名称](/zh-cn/docs/concepts/overview/working-with-objects/names#rfc-1035-label-names)。

{{< note >}}
需要注意的是，Service 能够将一个接收 `port` 映射到任意的 `targetPort`。
默认情况下，`targetPort` 将被设置为与 `port` 字段相同的值。
{{< /note >}}

### 端口定义 {#field-spec-ports}

Pod 中的端口定义是有名字的，你可以在 Service 的 `targetPort` 属性中引用这些名称。
例如，我们可以通过以下方式将 Service 的 `targetPort` 绑定到 Pod 端口：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app.kubernetes.io/name: proxy
spec:
  containers:
  - name: nginx
    image: nginx:stable
    ports:
      - containerPort: 80
        name: http-web-svc

---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app.kubernetes.io/name: proxy
  ports:
  - name: name-of-service-port
    protocol: TCP
    port: 80
    targetPort: http-web-svc
```

即使 Service 中使用同一配置名称混合使用多个 Pod，各 Pod 通过不同的端口号支持相同的网络协议，
此功能也可以使用。这为 Service 的部署和演化提供了很大的灵活性。
例如，你可以在新版本中更改 Pod 中后端软件公开的端口号，而不会破坏客户端。

服务的默认协议是 [TCP](/zh-cn/docs/reference/networking/service-protocols/#protocol-tcp)；
你还可以使用任何其他[受支持的协议](/zh-cn/docs/reference/networking/service-protocols/)。

由于许多服务需要公开多个端口，所以 Kubernetes 针对单个服务支持[多个端口定义](#multi-port-services)。
每个端口定义可以具有相同的 `protocol`，也可以具有不同的协议。

### 没有选择算符的 Service   {#services-without-selectors}

由于选择算符的存在，服务最常见的用法是为 Kubernetes Pod 的访问提供抽象，
但是当与相应的 {{<glossary_tooltip term_id="endpoint-slice" text="EndpointSlices">}}
对象一起使用且没有选择算符时，
服务也可以为其他类型的后端提供抽象，包括在集群外运行的后端。

例如：

* 希望在生产环境中使用外部的数据库集群，但测试环境使用自己的数据库。
* 希望服务指向另一个 {{< glossary_tooltip term_id="namespace" >}} 中或其它集群中的服务。
* 你正在将工作负载迁移到 Kubernetes。在评估该方法时，你仅在 Kubernetes 中运行一部分后端。

在任何这些场景中，都能够定义**未**指定与 Pod 匹配的选择算符的 Service。例如：
实例:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

由于此服务没有选择算符，因此不会自动创建相应的 EndpointSlice（和旧版 Endpoint）对象。
你可以通过手动添加 EndpointSlice 对象，将服务映射到运行该服务的网络地址和端口：

```yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: my-service-1 # 按惯例将服务的名称用作 EndpointSlice 名称的前缀
  labels:
    # 你应设置 "kubernetes.io/service-name" 标签。
    # 设置其值以匹配服务的名称
    kubernetes.io/service-name: my-service
addressType: IPv4
ports:
  - name: '' # 留空，因为 port 9376 未被 IANA 分配为已注册端口
    appProtocol: http
    protocol: TCP
    port: 9376
endpoints:
  - addresses:
      - "10.4.5.6" # 此列表中的 IP 地址可以按任何顺序显示
      - "10.1.2.3"
```

#### 自定义 EndpointSlices

当为服务创建 [EndpointSlice](#endpointslices) 对象时，可以为 EndpointSlice 使用任何名称。
命名空间中的每个 EndpointSlice 必须有一个唯一的名称。通过在 EndpointSlice 上设置
`kubernetes.io/service-name` {{< glossary_tooltip text="label" term_id="label" >}}
可以将 EndpointSlice 链接到服务。

{{< note >}}
端点 IP 地址**必须不是** ：本地回路地址（IPv4 的 127.0.0.0/8、IPv6 的 ::1/128）
或链路本地地址（IPv4 的 169.254.0.0/16 和 224.0.0.0/24、IPv6 的 fe80::/64）。

端点 IP 地址不能是其他 Kubernetes 服务的集群 IP，因为
{{< glossary_tooltip term_id ="kube-proxy">}} 不支持将虚拟 IP 作为目标。
{{< /note >}}

对于你自己或在你自己代码中创建的 EndpointSlice，你还应该为
[`endpointslice.kubernetes.io/managed-by`](/zh-cn/docs/reference/labels-annotations-taints/#endpointslicekubernetesiomanaged-by)
标签拣选一个值。如果你创建自己的控制器代码来管理 EndpointSlice，
请考虑使用类似于 `"my-domain.example/name-of-controller"` 的值。
如果你使用的是第三方工具，请使用全小写的工具名称，并将空格和其他标点符号更改为短划线 (`-`)。
如果人们直接使用 `kubectl` 之类的工具来管理 EndpointSlices，请使用描述这种手动管理的名称，
例如 `"staff"` 或 `"cluster-admins"`。你应该避免使用保留值 `"controller"`，
该值标识由 Kubernetes 自己的控制平面管理的 EndpointSlices。

#### 访问没有选择算符的 Service   {#service-no-selector-access}

访问没有选择算符的 Service，与有选择算符的 Service 的原理相同。
在没有选择算符的 Service [示例](#services-without-selectors)中，
流量被路由到 EndpointSlice 清单中定义的两个端点之一：
通过 TCP 协议连接到 10.1.2.3 或 10.4.5.6 的端口 9376。

{{< note >}}
Kubernetes API 服务器不允许代理到未被映射至 Pod 上的端点。由于此约束，当 Service
没有选择算符时，诸如 `kubectl proxy <service-name>` 之类的操作将会失败。这可以防止
Kubernetes API 服务器被用作调用者可能无权访问的端点的代理。
{{< /note >}}

`ExternalName` Service 是 Service 的特例，它没有选择算符，而是使用 DNS 名称。
有关更多信息，请参阅 [ExternalName](#externalname) 一节。

### EndpointSlices

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

[EndpointSlices](/zh-cn/docs/concepts/services-networking/endpoint-slices/)
这些对象表示针对服务的后备网络端点的子集（**切片**）。

你的 Kubernetes 集群会跟踪每个 EndpointSlice 表示的端点数量。
如果服务的端点太多以至于达到阈值，Kubernetes 会添加另一个空的 EndpointSlice 并在其中存储新的端点信息。
默认情况下，一旦现有 EndpointSlice 都包含至少 100 个端点，Kubernetes 就会创建一个新的 EndpointSlice。
在需要添加额外的端点之前，Kubernetes 不会创建新的 EndpointSlice。

参阅 [EndpointSlices](/zh-cn/docs/concepts/services-networking/endpoint-slices/)
了解有关该 API 的更多信息。

### Endpoints

在 Kubernetes API 中，[Endpoints](/zh-cn/docs/reference/kubernetes-api/service-resources/endpoints-v1/)
（该资源类别为复数）定义了网络端点的列表，通常由 Service 引用，以定义可以将流量发送到哪些 Pod。

推荐用 EndpointSlice API 替换 Endpoints。

#### 超出容量的端点

Kubernetes 限制单个 Endpoints 对象中可以容纳的端点数量。
当一个服务有超过 1000 个后备端点时，Kubernetes 会截断 Endpoints 对象中的数据。
由于一个服务可以链接多个 EndpointSlice，所以 1000 个后备端点的限制仅影响旧版的 Endpoints API。

这种情况下，Kubernetes 选择最多 1000 个可能的后端端点来存储到 Endpoints 对象中，并在
Endpoints: [`endpoints.kubernetes.io/over-capacity: truncated`](/zh-cn/docs/reference/labels-annotations-taints/#endpoints-kubernetes-io-over-capacity)
上设置{{< glossary_tooltip text="注解" term_id="annotation" >}}。
如果后端 Pod 的数量低于 1000，控制平面也会移除该注解。

流量仍会发送到后端，但任何依赖旧版 Endpoints API 的负载均衡机制最多只能将流量发送到 1000 个可用的后备端点。

相同的 API 限制意味着你不能手动将 Endpoints 更新为拥有超过 1000 个端点。

### 应用协议    {#application-protocol}

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

`appProtocol` 字段提供了一种为每个 Service 端口指定应用协议的方式。
此字段的取值会被映射到对应的 Endpoints 和 EndpointSlices 对象。

该字段遵循标准的 Kubernetes 标签语法。
其值可以是 [IANA 标准服务名称](https://www.iana.org/assignments/service-names)
或以域名为前缀的名称，如 `mycompany.com/my-custom-protocol`。

### 多端口 Service   {#multi-port-services}

对于某些服务，你需要公开多个端口。
Kubernetes 允许你在 Service 对象上配置多个端口定义。
为服务使用多个端口时，必须提供所有端口名称，以使它们无歧义。
例如：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 9376
    - name: https
      protocol: TCP
      port: 443
      targetPort: 9377
```

{{< note >}}
与一般的 Kubernetes 名称一样，端口名称只能包含小写字母数字字符 和 `-`。
端口名称还必须以字母数字字符开头和结尾。

例如，名称 `123-abc` 和 `web` 有效，但是 `123_abc` 和 `-web` 无效。
{{< /note >}}

## 发布服务（服务类型）      {#publishing-services-service-types}

对一些应用的某些部分（如前端），可能希望将其暴露给 Kubernetes 集群外部的 IP 地址。

Kubernetes `ServiceTypes` 允许指定你所需要的 Service 类型。

可用的 `type` 值及其行为有：

`ClusterIP`
: 通过集群的内部 IP 暴露服务，选择该值时服务只能够在集群内部访问。
  这也是你没有为服务显式指定 `type` 时使用的默认值。
  你可以使用 [Ingress](/zh-cn/docs/concepts/services-networking/ingress/)
  或者 [Gateway API](https://gateway-api.sigs.k8s.io/) 向公众暴露服务。

[`NodePort`](#type-nodeport)
: 通过每个节点上的 IP 和静态端口（`NodePort`）暴露服务。
  为了让节点端口可用，Kubernetes 设置了集群 IP 地址，这等同于你请求 `type: ClusterIP` 的服务。

[`LoadBalancer`](#loadbalancer)
: 使用云提供商的负载均衡器向外部暴露服务。
  Kubernetes 不直接提供负载均衡组件；你必须提供一个，或者将你的 Kubernetes 集群与云提供商集成。

[`ExternalName`](#externalname)
: 将服务映射到 `externalName` 字段的内容（例如，映射到主机名 `api.foo.bar.example`）。
  该映射将集群的 DNS 服务器配置为返回具有该外部主机名值的 `CNAME` 记录。 
  无需创建任何类型代理。

服务 API 中的 `type` 字段被设计为层层递进的形式 - 每个级别都建立在前一个级别基础上。
并不是所有云提供商都如此严格要求的，但 Kubernetes 的 Service API 设计要求满足这一逻辑。

### `type: ClusterIP` {#type-clusterip}

此默认服务类型从你的集群中有意预留的 IP 地址池中分配一个 IP 地址。

其他几种服务类型在 `ClusterIP` 类型的基础上进行构建。

如果你定义的服务将 `.spec.clusterIP` 设置为 `"None"`，则 Kubernetes
不会分配 IP 地址。有关详细信息，请参阅 [headless 服务](#headless-services)。

#### 选择自己的 IP 地址   {#choosing-your-own-ip-address}

在 `Service` 创建的请求中，可以通过设置 `spec.clusterIP` 字段来指定自己的集群 IP 地址。
比如，希望替换一个已经已存在的 DNS 条目，或者遗留系统已经配置了一个固定的 IP 且很难重新配置。

用户选择的 IP 地址必须合法，并且这个 IP 地址在 `service-cluster-ip-range` CIDR 范围内，
这对 API 服务器来说是通过一个标识来指定的。
如果 IP 地址不合法，API 服务器会返回 HTTP 状态码 422，表示值不合法。

阅读[避免冲突](/zh-cn/docs/reference/networking/virtual-ips/#avoiding-collisions)，
了解 Kubernetes 如何协助降低两种不同服务试图使用相同 IP 地址的风险和影响。

### `type: NodePort`  {#type-nodeport}

如果你将 `type` 字段设置为 `NodePort`，则 Kubernetes 控制平面将在
`--service-node-port-range` 标志指定的范围内分配端口（默认值：30000-32767）。
每个节点将那个端口（每个节点上的相同端口号）代理到你的服务中。
你的服务在其 `.spec.ports[*].nodePort` 字段中报告已分配的端口。

使用 NodePort 可以让你自由设置自己的负载均衡解决方案，
配置 Kubernetes 不完全支持的环境，
甚至直接暴露一个或多个节点的 IP 地址。

对于 NodePort 服务，Kubernetes 额外分配一个端口（TCP、UDP 或 SCTP 以匹配服务的协议）。
集群中的每个节点都将自己配置为监听分配的端口并将流量转发到与该服务关联的某个就绪端点。
通过使用适当的协议（例如 TCP）和适当的端口（分配给该服务）连接到所有节点，
你将能够从集群外部使用 `type: NodePort` 服务。

#### 选择你自己的端口   {#nodeport-custom-port}

如果需要特定的端口号，你可以在 `nodePort` 字段中指定一个值。
控制平面将为你分配该端口或报告 API 事务失败。
这意味着你需要自己注意可能发生的端口冲突。
你还必须使用有效的端口号，该端口号在配置用于 NodePort 的范围内。

以下是 `type: NodePort` 服务的一个示例清单，它指定了一个 NodePort 值（在本例中为 30007）：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    # 默认情况下，为了方便起见，`targetPort` 被设置为与 `port` 字段相同的值。
    - port: 80
      targetPort: 80
      # 可选字段
      # 默认情况下，为了方便起见，Kubernetes 控制平面会从某个范围内分配一个端口号（默认：30000-32767）
      nodePort: 30007
```

#### 为 `type: NodePort` 服务自定义 IP 地址配置  {#service-nodeport-custom-listen-address}

你可以在集群中设置节点以使用特定 IP 地址来提供 NodePort 服务。
如果每个节点都连接到多个网络（例如：一个网络用于应用程序流量，另一个网络用于节点和控制平面之间的流量），
你可能需要执行此操作。

如果你要指定特定的 IP 地址来代理端口，可以将 kube-proxy 的 `--nodeport-addresses` 标志或
[kube-proxy 配置文件](/zh-cn/docs/reference/config-api/kube-proxy-config.v1alpha1/)的等效
`nodePortAddresses` 字段设置为特定的 IP 段。

此标志采用逗号分隔的 IP 段列表（例如 `10.0.0.0/8`、`192.0.2.0/25`）来指定 kube-proxy 应视为该节点本地的
IP 地址范围。

例如，如果你使用 `--nodeport-addresses=127.0.0.0/8` 标志启动 kube-proxy，
则 kube-proxy 仅选择 NodePort 服务的环回接口。
`--nodeport-addresses` 的默认值是一个空列表。
这意味着 kube-proxy 应考虑 NodePort 的所有可用网络接口。
（这也与早期的 Kubernetes 版本兼容。）

{{< note >}}
此服务呈现为 `<NodeIP>:spec.ports[*].nodePort` 和 `.spec.clusterIP:spec.ports[*].port`。
如果设置了 kube-proxy 的 `--nodeport-addresses` 标志或 kube-proxy 配置文件中的等效字段，
则 `<NodeIP>` 将是过滤的节点 IP 地址（或可能的 IP 地址）。
{{< /note >}}

### `type: LoadBalancer`  {#loadbalancer}

在使用支持外部负载均衡器的云提供商的服务时，设置 `type` 的值为 `"LoadBalancer"`，
将为 Service 提供负载均衡器。
负载均衡器是异步创建的，关于被提供的负载均衡器的信息将会通过 Service 的
`status.loadBalancer` 字段发布出去。

实例：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
  clusterIP: 10.0.171.239
  type: LoadBalancer
status:
  loadBalancer:
    ingress:
    - ip: 192.0.2.127
```

来自外部负载均衡器的流量将直接重定向到后端 Pod 上，由云提供商决定如何进行负载平衡。

要实现 `type: LoadBalancer` 的服务，Kubernetes 通常首先进行与请求 `type: NodePort` 服务等效的更改。
cloud-controller-manager 组件随后配置外部负载均衡器以将流量转发到已分配的节点端口。

你可以将负载均衡服务配置为[忽略](#load-balancer-nodeport-allocation)分配节点端口，
前提是云提供商实现支持这点。

某些云提供商允许设置 `loadBalancerIP`。
在这些情况下，将根据用户设置的 `loadBalancerIP` 来创建负载均衡器。
如果没有设置 `loadBalancerIP` 字段，将会给负载均衡器指派一个临时 IP。
如果设置了 `loadBalancerIP`，但云提供商并不支持这种特性，那么设置的
`loadBalancerIP` 值将会被忽略掉。

{{< note >}}
针对 Service 的 `.spec.loadBalancerIP` 字段已在 Kubernetes v1.24 中被弃用。

此字段的定义模糊，其含义因实现而异。它也不支持双协议栈联网。
此字段可能会在未来的 API 版本中被移除。

如果你正在集成某云平台，该平台通过（特定于提供商的）注解为 Service 指定负载均衡器 IP 地址，
你应该切换到这样做。

如果你正在为集成到 Kubernetes 的负载均衡器编写代码，请避免使用此字段。
你可以与 [Gateway](https://gateway-api.sigs.k8s.io/) 而不是 Service 集成，
或者你可以在 Service 上定义自己的（特定于提供商的）注解，以指定等效的细节。
{{< /note >}}

#### 混合协议类型的负载均衡器

{{< feature-state for_k8s_version="v1.26" state="stable" >}}

默认情况下，对于 LoadBalancer 类型的服务，当定义了多个端口时，
所有端口必须具有相同的协议，并且该协议必须是受云提供商支持的协议。

当服务中定义了多个端口时，特性门控 `MixedProtocolLBService`
（在 kube-apiserver 1.24 版本默认为启用）
允许 LoadBalancer 类型的服务使用不同的协议。

{{< note >}}
可用于负载均衡服务的协议集由你的云提供商决定，他们可能在
Kubernetes API 强制执行的限制之外另加一些约束。

{{< /note >}}

### 禁用负载均衡器节点端口分配 {#load-balancer-nodeport-allocation}

{{< feature-state for_k8s_version="v1.24" state="stable" >}}

你可以通过设置 `spec.allocateLoadBalancerNodePorts` 为 `false`
对类型为 LoadBalancer 的服务禁用节点端口分配。
这仅适用于直接将流量路由到 Pod 而不是使用节点端口的负载均衡器实现。
默认情况下，`spec.allocateLoadBalancerNodePorts` 为 `true`，
LoadBalancer 类型的服务继续分配节点端口。
如果现有服务已被分配节点端口，将参数 `spec.allocateLoadBalancerNodePorts`
设置为 `false` 时，这些服务上已分配置的节点端口**不会**被自动释放。
你必须显式地在每个服务端口中删除 `nodePorts` 项以释放对应端口。

#### 设置负载均衡器实现的类别 {#load-balancer-class}

{{< feature-state for_k8s_version="v1.24" state="stable" >}}

对于 `type` 设置为 `LoadBalancer` 的 Service，
`spec.loadBalancerClass` 字段允许你不使用云提供商的默认负载均衡器实现，
转而使用指定的负载均衡器实现。

默认情况下，`.spec.loadBalancerClass` 未设置，如果集群使用 `--cloud-provider` 配置了云提供商，
`LoadBalancer` 类型服务会使用云提供商的默认负载均衡器实现。


如果设置了 `.spec.loadBalancerClass`，则假定存在某个与所指定的类相匹配的负载均衡器实现在监视服务变化。
所有默认的负载均衡器实现（例如，由云提供商所提供的）都会忽略设置了此字段的服务。`.spec.loadBalancerClass`
只能设置到类型为 `LoadBalancer` 的 Service 之上，而且一旦设置之后不可变更。

`.spec.loadBalancerClass` 的值必须是一个标签风格的标识符，
可以有选择地带有类似 "`internal-vip`" 或 "`example.com/internal-vip`" 这类前缀。
没有前缀的名字是保留给最终用户的。

#### 内部负载均衡器 {#internal-load-balancer}

在混合环境中，有时有必要在同一(虚拟)网络地址块内路由来自服务的流量。

在水平分割 DNS 环境中，你需要两个服务才能将内部和外部流量都路由到你的端点（Endpoints）。

如要设置内部负载均衡器，请根据你所使用的云运营商，为服务添加以下注解之一：

{{< tabs name="service_tabs" >}}
{{% tab name="Default" %}}
选择一个标签。
{{% /tab %}}
{{% tab name="GCP" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        networking.gke.io/load-balancer-type: "Internal"
[...]
```

{{% /tab %}}
{{% tab name="AWS" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/aws-load-balancer-internal: "true"
[...]
```

{{% /tab %}}
{{% tab name="Azure" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/azure-load-balancer-internal: "true"
[...]
```

{{% /tab %}}
{{% tab name="IBM Cloud" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.kubernetes.io/ibm-load-balancer-cloud-provider-ip-type: "private"
[...]
```

{{% /tab %}}
{{% tab name="OpenStack" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/openstack-internal-load-balancer: "true"
[...]
```

{{% /tab %}}
{{% tab name="百度云" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/cce-load-balancer-internal-vpc: "true"
[...]
```

{{% /tab %}}
{{% tab name="腾讯云" %}}

```yaml
[...]
metadata:
  annotations:
    service.kubernetes.io/qcloud-loadbalancer-internal-subnetid: subnet-xxxxx
[...]
```

{{% /tab %}}
{{% tab name="阿里云" %}}

```yaml
[...]
metadata:
  annotations:
    service.beta.kubernetes.io/alibaba-cloud-loadbalancer-address-type: "intranet"
[...]
```

{{% /tab %}}
{{% tab name="OCI" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/oci-load-balancer-internal: true
[...]
```
{{% /tab %}}
{{< /tabs >}}


### ExternalName 类型         {#externalname}

类型为 ExternalName 的服务将服务映射到 DNS 名称，而不是典型的选择算符，例如 `my-service` 或者 `cassandra`。
你可以使用 `spec.externalName` 参数指定这些服务。

例如，以下 Service 定义将 `prod` 名称空间中的 `my-service` 服务映射到 `my.database.example.com`：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: prod
spec:
  type: ExternalName
  externalName: my.database.example.com
```

{{< note >}}
`type: ExternalName` 的服务接受 IPv4 地址字符串，但将该字符串视为由数字组成的 DNS 名称，
而不是 IP 地址（然而，互联网不允许在 DNS 中使用此类名称）。
类似于 IPv4 地址的外部名称不能由 CoreDNS 或 ingress-nginx 解析，因为外部名称旨在指定规范的 DNS 名称。
DNS 服务器不解析类似于 IPv4 地址的外部名称的服务。

如果你想要将服务直接映射到特定的 IP 地址，请考虑使用[无头 Services](#headless-services)。
{{< /note >}}

当查找主机 `my-service.prod.svc.cluster.local` 时，集群 DNS 服务返回 `CNAME` 记录，
其值为 `my.database.example.com`。
访问 `my-service` 的方式与其他服务的方式相同，但主要区别在于重定向发生在 DNS 级别，而不是通过代理或转发。
如果以后你决定将数据库移到集群中，则可以启动其 Pod，添加适当的选择算符或端点以及更改服务的 `type`。

{{< caution >}}
对于一些常见的协议，包括 HTTP 和 HTTPS，你使用 ExternalName 可能会遇到问题。
如果你使用 ExternalName，那么集群内客户端使用的主机名与 ExternalName 引用的名称不同。

对于使用主机名的协议，此差异可能会导致错误或意外响应。
HTTP 请求将具有源服务器无法识别的 `Host:` 标头；
TLS 服务器将无法提供与客户端连接的主机名匹配的证书。
{{< /caution >}}

## 无头服务（Headless Services）  {#headless-services}

有时不需要或不想要负载均衡，以及单独的 Service IP。
遇到这种情况，可以通过显式指定 Cluster IP（`spec.clusterIP`）的值为 `"None"`
来创建 `Headless` Service。

你可以使用一个无头 Service 与其他服务发现机制进行接口，而不必与 Kubernetes 的实现捆绑在一起。

无头 `Services` 不会获得 Cluster IP，kube-proxy 不会处理这类服务，
而且平台也不会为它们提供负载均衡或路由。
DNS 如何实现自动配置，依赖于 Service 是否定义了选择算符。

### 带选择算符的服务 {#with-selectors}

对定义了选择算符的无头服务，Kubernetes 控制平面在 Kubernetes API 中创建 EndpointSlice 对象，
并且修改 DNS 配置返回 A 或 AAAA 条记录（IPv4 或 IPv6 地址），这些记录直接指向 `Service` 的后端 Pod 集合。

### 无选择算符的服务  {#without-selectors}

对没有定义选择算符的无头服务，控制平面不会创建 EndpointSlice 对象。
然而 DNS 系统会查找和配置以下之一：

* 对于 [`type: ExternalName`](#externalname) 服务，查找和配置其 CNAME 记录
* 对所有其他类型的服务，针对 Service 的就绪端点的所有 IP 地址，查找和配置 DNS A / AAAA 条记录
  * 对于 IPv4 端点，DNS 系统创建 A 条记录。
  * 对于 IPv6 端点，DNS 系统创建 AAAA 条记录。

当你定义无选择算符的无头服务时，`port` 必须与 `targetPort` 匹配。

## 服务发现  {#discovering-services}

对于在集群内运行的客户端，Kubernetes 支持两种主要的服务发现模式：环境变量和 DNS。

### 环境变量   {#environment-variables}

当 Pod 运行在某 Node 上时，kubelet 会为每个活跃的 Service 添加一组环境变量。
kubelet 为 Pod 添加环境变量 `{SVCNAME}_SERVICE_HOST` 和 `{SVCNAME}_SERVICE_PORT`。
这里 Service 的名称被转为大写字母，横线被转换成下划线。
它还支持与 Docker Engine 的 "**[legacy container links](https://docs.docker.com/network/links/)**" 特性兼容的变量
（参阅 [makeLinkVariables](https://github.com/kubernetes/kubernetes/blob/dd2d12f6dc0e654c15d5db57a5f9f6ba61192726/pkg/kubelet/envvars/envvars.go#L72)) 。

举个例子，一个 Service `redis-primary` 暴露了 TCP 端口 6379，
同时被分配了 Cluster IP 地址 10.0.0.11，这个 Service 生成的环境变量如下：

```shell
REDIS_PRIMARY_SERVICE_HOST=10.0.0.11
REDIS_PRIMARY_SERVICE_PORT=6379
REDIS_PRIMARY_PORT=tcp://10.0.0.11:6379
REDIS_PRIMARY_PORT_6379_TCP=tcp://10.0.0.11:6379
REDIS_PRIMARY_PORT_6379_TCP_PROTO=tcp
REDIS_PRIMARY_PORT_6379_TCP_PORT=6379
REDIS_PRIMARY_PORT_6379_TCP_ADDR=10.0.0.11
```

{{< note >}}
当你的 Pod 需要访问某 Service，并且你在使用环境变量方法将端口和集群 IP 发布到客户端
Pod 时，必须在客户端 Pod 出现**之前**创建该 Service。
否则，这些客户端 Pod 中将不会出现对应的环境变量。

如果仅使用 DNS 查找服务的集群 IP，则无需担心此设定问题。
{{< /note >}}

Kubernetes 还支持并提供与 Docker Engine 的
"**[legacy container links](https://docs.docker.com/network/links/)**"
兼容的变量。
你可以阅读 [makeLinkVariables](https://github.com/kubernetes/kubernetes/blob/dd2d12f6dc0e654c15d5db57a5f9f6ba61192726/pkg/kubelet/envvars/envvars.go#L72)
来了解这是如何在 Kubernetes 中实现的。

### DNS

你可以（几乎总是应该）使用[附加组件](/zh-cn/docs/concepts/cluster-administration/addons/)
为 Kubernetes 集群安装 DNS 服务。

支持集群的 DNS 服务器（例如 CoreDNS）监视 Kubernetes API 中的新 Service，并为每个 Service 创建一组 DNS 记录。
如果在整个集群中都启用了 DNS，则所有 Pod 都应该能够通过 DNS 名称自动解析 Service。

例如，如果你在 Kubernetes 命名空间 `my-ns` 中有一个名为 `my-service` 的 Service，
则控制平面和 DNS 服务共同为 `my-service.my-ns` 创建 DNS 记录。
名字空间 `my-ns` 中的 Pod 应该能够通过按名检索 `my-service` 来找到服务
（`my-service.my-ns` 也可以）。

其他名字空间中的 Pod 必须将名称限定为 `my-service.my-ns`。
这些名称将解析为为服务分配的集群 IP。

Kubernetes 还支持命名端口的 DNS SRV（Service）记录。
如果 Service `my-service.my-ns` 具有名为 `http`　的端口，且协议设置为 TCP，
则可以用 `_http._tcp.my-service.my-ns` 执行 DNS SRV 查询以发现 `http` 的端口号以及 IP 地址。

Kubernetes DNS 服务器是唯一的一种能够访问 `ExternalName` 类型的 Service 的方式。
更多关于 `ExternalName` 解析的信息可以查看
[Service 与 Pod 的 DNS](/zh-cn/docs/concepts/services-networking/dns-pod-service/)。

<a id="shortcomings" />
<a id="the-gory-details-of-virtual-ips" />
<a id="proxy-modes" />
<a id="proxy-mode-userspace" />
<a id="proxy-mode-iptables" />
<a id="proxy-mode-ipvs" />
<a id="ips-and-vips" />

## 虚拟 IP 寻址机制   {#virtual-ip-addressing-mechanism}

阅读[虚拟 IP 和 Service 代理](/zh-cn/docs/reference/networking/virtual-ips/)以了解
Kubernetes 提供的使用虚拟 IP 地址公开服务的机制。

### 流量策略

你可以设置 `.spec.internalTrafficPolicy` 和 `.spec.externalTrafficPolicy`
字段来控制 Kubernetes 如何将流量路由到健康（“就绪”）的后端。

有关详细信息，请参阅[流量策略](/zh-cn/docs/reference/networking/virtual-ips/#traffic-policies)。

## 会话的黏性   {#session-stickiness}

如果你想确保来自特定客户端的连接每次都传递到同一个 Pod，你可以配置根据客户端 IP 地址来执行的会话亲和性。
深入了解可阅读[会话亲和性](/zh-cn/docs/reference/networking/virtual-ips/#session-affinity)。

### 外部 IP  {#external-ips}

如果有外部 IP 能够路由到一个或多个集群节点上，则 Kubernetes 服务可以暴露在这些 `externalIPs` 上。
当网络流量到达集群时，如果外部 IP（作为目的 IP 地址）和端口都与该 Service 匹配，Kubernetes
配置的规则和路由会确保流量被路由到该 Service 的端点之一。

定义 Service 时，你可以为任何[服务类型](#publishing-services-service-types)指定 `externalIPs`。

在下面的例子中，名为 `my-service` 的服务可以在 "`198.51.100.32:80`"
（从 `.spec.externalIPs[]` 和 `.spec.ports[].port` 计算）上被客户端使用 TCP 协议访问。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 49152
  externalIPs:
    - 198.51.100.32
```

{{< note >}}
Kubernetes 不管理 `externalIPs` 的分配，这属于集群管理员的职责。
{{< /note >}}

## API 对象   {#api-object}

Service 是 Kubernetes REST API 中的顶级资源。你可以找到有关
[Service 对象 API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#service-v1-core)
的更多详细信息。

<a id="shortcomings" /><a id="#the-gory-details-of-virtual-ips" />

## {{% heading "whatsnext" %}}

进一步学习 Service 及其在 Kubernetes 中所发挥的作用：

* 遵循[使用 Service 连接到应用](/zh-cn/docs/tutorials/services/connect-applications-service/)教程。
* 阅读 [Ingress](/zh-cn/docs/concepts/services-networking/ingress/) 将来自集群外部的 HTTP 和 HTTPS
  请求路由暴露给集群内的服务。
* 阅读 [Gateway](https://gateway-api.sigs.k8s.io/) 作为 Kubernetes 的扩展提供比 Ingress 更大的灵活性。

更多上下文，可以阅读以下内容：

* [虚拟 IP 和 Service 代理](/zh-cn/docs/reference/networking/virtual-ips/)
* [EndpointSlices](/zh-cn/docs/concepts/services-networking/endpoint-slices/)
* Service API 的 [API 参考](/zh-cn/docs/reference/kubernetes-api/service-resources/service-v1/)
* EndpointSlice API 的 [API 参考](/zh-cn/docs/reference/kubernetes-api/service-resources/endpoint-slice-v1/)
* Endpoint API 的 [API 参考](/zh-cn/docs/reference/kubernetes-api/service-resources/endpoints-v1/)
