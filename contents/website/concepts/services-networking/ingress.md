---
title: Ingress
content_type: concept
description: >-
  使用一种能感知协议配置的机制来理解 URI、主机名称、路径和更多 Web 概念，使得 HTTP（或 HTTPS）网络服务可用。
  Ingress 概念允许你通过 Kubernetes API 定义的规则将流量映射到不同的后端。
weight: 30
---

{{< feature-state for_k8s_version="v1.19" state="stable" >}}
{{< glossary_definition term_id="ingress" length="all" >}}


## 术语  {#terminology}

为了表达更加清晰，本指南定义了以下术语：

* 节点（Node）: Kubernetes 集群中的一台工作机器，是集群的一部分。
* 集群（Cluster）: 一组运行由 Kubernetes 管理的容器化应用程序的节点。
  在此示例和在大多数常见的 Kubernetes 部署环境中，集群中的节点都不在公共网络中。
* 边缘路由器（Edge Router）: 在集群中强制执行防火墙策略的路由器。可以是由云提供商管理的网关，也可以是物理硬件。
* 集群网络（Cluster Network）: 一组逻辑的或物理的连接，根据 Kubernetes
  [网络模型](/zh-cn/docs/concepts/cluster-administration/networking/)在集群内实现通信。
* 服务（Service）：Kubernetes {{< glossary_tooltip term_id="service" >}}，
  使用{{< glossary_tooltip text="标签" term_id="label" >}}选择器（selectors）辨认一组 Pod。
  除非另有说明，否则假定服务只具有在集群网络中可路由的虚拟 IP。

## Ingress 是什么？  {#what-is-ingress}

[Ingress](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#ingress-v1-networking-k8s-io)
公开从集群外部到集群内[服务](/zh-cn/docs/concepts/services-networking/service/)的
HTTP 和 HTTPS 路由。
流量路由由 Ingress 资源上定义的规则控制。

下面是一个将所有流量都发送到同一 Service 的简单 Ingress 示例：

{{< figure src="/zh-cn/docs/images/ingress.svg" alt="ingress-diagram" class="diagram-large" caption="图. Ingress" link="https://mermaid.live/edit#pako:eNqNkktLAzEQgP9KSC8Ku6XWBxKlJz0IHsQeuz1kN7M2uC-SrA9sb6X26MFLFZGKoCC0CIIn_Td1139halZq8eJlE2a--TI7yRn2YgaYYCc6EDRpod39DSdCyAs4RGqhMRndffRfs6dxc9Euox0NgZR2NhpmF73sqos2XVFD-ctt_vY2uTnPh8PJ4BGV7Ro3ZKOoaH5Li6Bt19r56zi7fM4fupP-oC1BHHEPGnWzGlimruno87qXvd__qjdpw2pXErOlxl7Mmn_j1VkcImb-i0q5BT5KAsoj5PMgICXGmCWViA-BlHzfL_b2MWeqRVaSE8uLg1iQUqVS2ZiTHK7LQrFcXfNg9V8WnZu3eEEqFYjCNCslJdd15zXVmcacODP9TMcqJmBN5zL9VKdt_uLM1ZoBzIVNF8WqM06ELRyCCCln-oWcTVkHqxaE4GCitwx8mgbK0Y-no9E0YVTBNuMqFpj4NJBgYZqquH4aeZgokcIPtMWpvtywoDpfU3_yww" >}}

Ingress 可为 Service 提供外部可访问的 URL、负载均衡流量、终止 SSL/TLS，以及基于名称的虚拟托管。
[Ingress 控制器](/zh-cn/docs/concepts/services-networking/ingress-controllers)
通常负责通过负载均衡器来实现 Ingress，尽管它也可以配置边缘路由器或其他前端来帮助处理流量。

Ingress 不会公开任意端口或协议。
将 HTTP 和 HTTPS 以外的服务公开到 Internet 时，通常使用
[Service.Type=NodePort](/zh-cn/docs/concepts/services-networking/service/#type-nodeport)
或 [Service.Type=LoadBalancer](/zh-cn/docs/concepts/services-networking/service/#loadbalancer)
类型的 Service。

## 环境准备

你必须拥有一个 [Ingress 控制器](/zh-cn/docs/concepts/services-networking/ingress-controllers) 才能满足 Ingress 的要求。
仅创建 Ingress 资源本身没有任何效果。

你可能需要部署 Ingress 控制器，例如 [ingress-nginx](https://kubernetes.github.io/ingress-nginx/deploy/)。
你可以从许多 [Ingress 控制器](/zh-cn/docs/concepts/services-networking/ingress-controllers) 中进行选择。

理想情况下，所有 Ingress 控制器都应符合参考规范。但实际上，不同的 Ingress 控制器操作略有不同。

{{< note >}}
确保你查看了 Ingress 控制器的文档，以了解选择它的注意事项。
{{< /note >}}

## Ingress 资源  {#the-ingress-resource}

一个最小的 Ingress 资源示例：


{{< codenew file="service/networking/minimal-ingress.yaml" >}}

Ingress 需要指定 `apiVersion`、`kind`、 `metadata`和 `spec` 字段。
Ingress 对象的命名必须是合法的 [DNS 子域名名称](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)。
关于如何使用配置文件，请参见[部署应用](/zh-cn/docs/tasks/run-application/run-stateless-application-deployment/)、
[配置容器](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/)、
[管理资源](/zh-cn/docs/concepts/cluster-administration/manage-deployment/)。
Ingress 经常使用注解（annotations）来配置一些选项，具体取决于 Ingress
控制器，例如[重写目标注解](https://github.com/kubernetes/ingress-nginx/blob/main/docs/examples/rewrite/README.md)。
不同的 [Ingress 控制器](/zh-cn/docs/concepts/services-networking/ingress-controllers)支持不同的注解。
查看你所选的 Ingress 控制器的文档，以了解其支持哪些注解。

Ingress [规约](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)
提供了配置负载均衡器或者代理服务器所需的所有信息。
最重要的是，其中包含与所有传入请求匹配的规则列表。
Ingress 资源仅支持用于转发 HTTP(S) 流量的规则。

如果 `ingressClassName` 被省略，那么你应该定义一个[默认 Ingress 类](#default-ingress-class)。

有一些 Ingress 控制器不需要定义默认的 `IngressClass`。比如：Ingress-NGINX
控制器可以通过[参数](https://kubernetes.github.io/ingress-nginx/#what-is-the-flag-watch-ingress-without-class)
`--watch-ingress-without-class` 来配置。
不过仍然[推荐](https://kubernetes.github.io/ingress-nginx/#i-have-only-one-instance-of-the-ingresss-nginx-controller-in-my-cluster-what-should-i-do)
按[下文](#default-ingress-class)所示来设置默认的 `IngressClass`。

### Ingress 规则  {#ingress-rules}

每个 HTTP 规则都包含以下信息：

* 可选的 `host`。在此示例中，未指定 `host`，因此该规则适用于通过指定 IP 地址的所有入站 HTTP 通信。
  如果提供了 `host`（例如 foo.bar.com），则 `rules` 适用于该 `host`。
* 路径列表（例如 `/testpath`），每个路径都有一个由 `service.name` 和 `service.port.name`
  或 `service.port.number` 定义的关联后端。
  在负载均衡器将流量定向到引用的服务之前，主机和路径都必须匹配传入请求的内容。
* `backend`（后端）是 [Service 文档](/zh-cn/docs/concepts/services-networking/service/)中所述的服务和端口名称的组合，
  或者是通过 {{< glossary_tooltip term_id="CustomResourceDefinition" text="CRD" >}}
  方式来实现的[自定义资源后端](#resource-backend)。
  与规则的 `host` 和 `path` 匹配的对 Ingress 的 HTTP（和 HTTPS ）请求将发送到列出的 `backend`。

通常在 Ingress 控制器中会配置 `defaultBackend`（默认后端），以服务于无法与规约中 `path` 匹配的所有请求。

### 默认后端  {#default-backend}

没有设置规则的 Ingress 将所有流量发送到同一个默认后端，而
`.spec.defaultBackend` 则是在这种情况下处理请求的那个默认后端。
`defaultBackend` 通常是
[Ingress 控制器](/zh-cn/docs/concepts/services-networking/ingress-controllers)的配置选项，
而非在 Ingress 资源中指定。
如果未设置任何的 `.spec.rules`，那么必须指定 `.spec.defaultBackend`。
如果未设置 `defaultBackend`，那么如何处理所有与规则不匹配的流量将交由
Ingress 控制器决定（请参考你的 Ingress 控制器的文档以了解它是如何处理那些流量的）。

如果没有 `hosts` 或 `paths` 与 Ingress 对象中的 HTTP 请求匹配，则流量将被路由到默认后端。

### 资源后端  {#resource-backend}

`Resource` 后端是一个引用，指向同一命名空间中的另一个 Kubernetes 资源，将其作为 Ingress 对象。
`Resource` 后端与 Service 后端是互斥的，在二者均被设置时会无法通过合法性检查。
`Resource` 后端的一种常见用法是将所有入站数据导向带有静态资产的对象存储后端。

{{< codenew file="service/networking/ingress-resource-backend.yaml" >}}

创建了如上的 Ingress 之后，你可以使用下面的命令查看它：

```bash
kubectl describe ingress ingress-resource-backend
```

```
Name:             ingress-resource-backend
Namespace:        default
Address:
Default backend:  APIGroup: k8s.example.com, Kind: StorageBucket, Name: static-assets
Rules:
  Host        Path  Backends
  ----        ----  --------
  *
              /icons   APIGroup: k8s.example.com, Kind: StorageBucket, Name: icon-assets
Annotations:  <none>
Events:       <none>
```

### 路径类型  {#path-types}

Ingress 中的每个路径都需要有对应的路径类型（Path Type）。未明确设置 `pathType`
的路径无法通过合法性检查。当前支持的路径类型有三种：

* `ImplementationSpecific`：对于这种路径类型，匹配方法取决于 IngressClass。
  具体实现可以将其作为单独的 `pathType` 处理或者与 `Prefix` 或 `Exact` 类型作相同处理。

* `Exact`：精确匹配 URL 路径，且区分大小写。

* `Prefix`：基于以 `/` 分隔的 URL 路径前缀匹配。匹配区分大小写，并且对路径中的元素逐个完成。
  路径元素指的是由 `/` 分隔符分隔的路径中的标签列表。
  如果每个 **p** 都是请求路径 **p** 的元素前缀，则请求与路径 **p** 匹配。

  {{< note >}}
  如果路径的最后一个元素是请求路径中最后一个元素的子字符串，则不会匹配
  （例如：`/foo/bar` 匹配 `/foo/bar/baz`, 但不匹配 `/foo/barbaz`）。
  {{< /note >}}

### 示例

| 类型   | 路径                            | 请求路径        | 匹配与否？               |
|--------|---------------------------------|-----------------|--------------------------|
| Prefix | `/`                             | （所有路径）    | 是                       |
| Exact  | `/foo`                          | `/foo`          | 是                       |
| Exact  | `/foo`                          | `/bar`          | 否                       |
| Exact  | `/foo`                          | `/foo/`         | 否                       |
| Exact  | `/foo/`                         | `/foo`          | 否                       |
| Prefix | `/foo`                          | `/foo`, `/foo/` | 是                       |
| Prefix | `/foo/`                         | `/foo`, `/foo/` | 是                       |
| Prefix | `/aaa/bb`                       | `/aaa/bbb`      | 否                       |
| Prefix | `/aaa/bbb`                      | `/aaa/bbb`      | 是                       |
| Prefix | `/aaa/bbb/`                     | `/aaa/bbb`      | 是，忽略尾部斜线         |
| Prefix | `/aaa/bbb`                      | `/aaa/bbb/`     | 是，匹配尾部斜线         |
| Prefix | `/aaa/bbb`                      | `/aaa/bbb/ccc`  | 是，匹配子路径           |
| Prefix | `/aaa/bbb`                      | `/aaa/bbbxyz`   | 否，字符串前缀不匹配     |
| Prefix | `/`, `/aaa`                     | `/aaa/ccc`      | 是，匹配 `/aaa` 前缀     |
| Prefix | `/`, `/aaa`, `/aaa/bbb`         | `/aaa/bbb`      | 是，匹配 `/aaa/bbb` 前缀 |
| Prefix | `/`, `/aaa`, `/aaa/bbb`         | `/ccc`          | 是，匹配 `/` 前缀        |
| Prefix | `/aaa`                          | `/ccc`          | 否，使用默认后端         |
| 混合   | `/foo` (Prefix), `/foo` (Exact) | `/foo`          | 是，优选 Exact 类型      |

#### 多重匹配  {#multiple-matches}

在某些情况下，Ingress 中的多条路径会匹配同一个请求。
这种情况下最长的匹配路径优先。
如果仍然有两条同等的匹配路径，则精确路径类型优先于前缀路径类型。

## 主机名通配符   {#hostname-wildcards}

主机名可以是精确匹配（例如 “`foo.bar.com`”）或者使用通配符来匹配
（例如 “`*.foo.com`”）。
精确匹配要求 HTTP `host` 头部字段与 `host` 字段值完全匹配。
通配符匹配则要求 HTTP `host` 头部字段与通配符规则中的后缀部分相同。

| 主机         | host 头部          | 匹配与否？                          |
| ------------ |--------------------| ------------------------------------|
| `*.foo.com`  | `bar.foo.com`      | 基于相同的后缀匹配                  |
| `*.foo.com`  | `baz.bar.foo.com`  | 不匹配，通配符仅覆盖了一个 DNS 标签 |
| `*.foo.com`  | `foo.com`          | 不匹配，通配符仅覆盖了一个 DNS 标签 |

{{< codenew file="service/networking/ingress-wildcard-host.yaml" >}}

## Ingress 类  {#ingress-class}

Ingress 可以由不同的控制器实现，通常使用不同的配置。
每个 Ingress 应当指定一个类，也就是一个对 IngressClass 资源的引用。
IngressClass 资源包含额外的配置，其中包括应当实现该类的控制器名称。

{{< codenew file="service/networking/external-lb.yaml" >}}

IngressClass 中的 `.spec.parameters` 字段可用于引用其他资源以提供额外的相关配置。

参数（`parameters`）的具体类型取决于你在 `.spec.controller` 字段中指定的 Ingress 控制器。

### IngressClass 的作用域

取决于你的 Ingress 控制器，你可能可以使用集群范围设置的参数或某个名字空间范围的参数。

{{< tabs name="tabs_ingressclass_parameter_scope" >}}
{{% tab name="集群作用域" %}}
IngressClass 的参数默认是集群范围的。

如果你设置了 `.spec.parameters` 字段且未设置 `.spec.parameters.scope`
字段，或是将 `.spec.parameters.scope` 字段设为了 `Cluster`，
那么该 IngressClass 所指代的即是一个集群作用域的资源。
参数的 `kind`（和 `apiGroup` 一起）指向一个集群作用域的
API（可能是一个定制资源（Custom Resource）），而它的
`name` 则为此 API 确定了一个具体的集群作用域的资源。

示例：

```yaml
---
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: external-lb-1
spec:
  controller: example.com/ingress-controller
  parameters:
    # 此 IngressClass 的配置定义在一个名为 “external-config-1” 的
    # ClusterIngressParameter（API 组为 k8s.example.net）资源中。
    # 这项定义告诉 Kubernetes 去寻找一个集群作用域的参数资源。
    scope: Cluster
    apiGroup: k8s.example.net
    kind: ClusterIngressParameter
    name: external-config-1
```

{{% /tab %}}
{{% tab name="命名空间作用域" %}}
{{< feature-state for_k8s_version="v1.23" state="stable" >}}

如果你设置了 `.spec.parameters` 字段且将 `.spec.parameters.scope`
字段设为了 `Namespace`，那么该 IngressClass 将会引用一个命名空间作用域的资源。
`.spec.parameters.namespace` 必须和此资源所处的命名空间相同。

参数的 `kind`（和 `apiGroup`
一起）指向一个命名空间作用域的 API（例如：ConfigMap），而它的
`name` 则确定了一个位于你指定的命名空间中的具体的资源。

命名空间作用域的参数帮助集群操作者将控制细分到用于工作负载的各种配置中（比如：负载均衡设置、API
网关定义）。如果你使用集群作用域的参数，那么你必须从以下两项中选择一项执行：

- 每次修改配置，集群操作团队需要批准其他团队的修改。
- 集群操作团队定义具体的准入控制，比如 [RBAC](/zh-cn/docs/reference/access-authn-authz/rbac/)
  角色与角色绑定，以使得应用程序团队可以修改集群作用域的配置参数资源。

IngressClass API 本身是集群作用域的。

这里是一个引用命名空间作用域的配置参数的 IngressClass 的示例：
```yaml
---
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: external-lb-2
spec:
  controller: example.com/ingress-controller
  parameters:
    # 此 IngressClass 的配置定义在一个名为 “external-config” 的
    # IngressParameter（API 组为 k8s.example.com）资源中，
    # 该资源位于 “external-configuration” 命名空间中。
    scope: Namespace
    apiGroup: k8s.example.com
    kind: IngressParameter
    namespace: external-configuration
    name: external-config
```

{{% /tab %}}
{{< /tabs >}}

### 废弃的注解  {#deprecated-annotation}

在 Kubernetes 1.18 版本引入 IngressClass 资源和 `ingressClassName` 字段之前，
Ingress 类是通过 Ingress 中的一个 `kubernetes.io/ingress.class` 注解来指定的。
这个注解从未被正式定义过，但是得到了 Ingress 控制器的广泛支持。

Ingress 中新的 `ingressClassName` 字段是该注解的替代品，但并非完全等价。
该注解通常用于引用实现该 Ingress 的控制器的名称，而这个新的字段则是对一个包含额外
Ingress 配置的 IngressClass 资源的引用，包括 Ingress 控制器的名称。

### 默认 Ingress 类  {#default-ingress-class}

你可以将一个特定的 IngressClass 标记为集群默认 Ingress 类。
将一个 IngressClass 资源的 `ingressclass.kubernetes.io/is-default-class` 注解设置为
`true` 将确保新的未指定 `ingressClassName` 字段的 Ingress 能够分配为这个默认的
IngressClass.

{{< caution >}}
如果集群中有多个 IngressClass 被标记为默认，准入控制器将阻止创建新的未指定
`ingressClassName` 的 Ingress 对象。
解决这个问题只需确保集群中最多只能有一个 IngressClass 被标记为默认。
{{< /caution >}}

有一些 Ingress 控制器不需要定义默认的 `IngressClass`。比如：Ingress-NGINX
控制器可以通过[参数](https://kubernetes.github.io/ingress-nginx/#what-is-the-flag-watch-ingress-without-class)
`--watch-ingress-without-class` 来配置。
不过仍然[推荐](https://kubernetes.github.io/ingress-nginx/#i-have-only-one-instance-of-the-ingresss-nginx-controller-in-my-cluster-what-should-i-do)
设置默认的 `IngressClass`。

{{< codenew file="service/networking/default-ingressclass.yaml" >}}

## Ingress 类型  {#types-of-ingress}

### 由单个 Service 来完成的 Ingress   {#single-service-ingress}

现有的 Kubernetes 概念允许你暴露单个 Service (参见[替代方案](#alternatives))。
你也可以通过指定无规则的**默认后端**来对 Ingress 进行此操作。

{{< codenew file="service/networking/test-ingress.yaml" >}}

如果使用 `kubectl apply -f` 创建此 Ingress，则应该能够查看刚刚添加的 Ingress 的状态：

```shell
kubectl get ingress test-ingress
```

```
NAME           CLASS         HOSTS   ADDRESS         PORTS   AGE
test-ingress   external-lb   *       203.0.113.123   80      59s
```

其中 `203.0.113.123` 是由 Ingress 控制器分配以满足该 Ingress 的 IP。

{{< note >}}
入口控制器和负载平衡器可能需要一两分钟才能分配 IP 地址。
在此之前，你通常会看到地址字段的值被设定为 `<pending>`。
{{< /note >}}

### 简单扇出  {#simple-fanout}

一个扇出（fanout）配置根据请求的 HTTP URI 将来自同一 IP 地址的流量路由到多个 Service。
Ingress 允许你将负载均衡器的数量降至最低。例如，这样的设置：

{{< figure src="/zh-cn/docs/images/ingressFanOut.svg" alt="ingress-fanout-diagram" class="diagram-large" caption="图. Ingress 扇出" link="https://mermaid.live/edit#pako:eNqNUk1v0zAY_iuWewEpyRKnjM5FPY0DEgfEjk0PTvxmtZbGke3woW03NDjuChNCRRyQkMYFidP4NyXlX5DMjroykLg4j_x8vM6j9xhnkgOm-FCxao4ePx0nJUJZIaA0d6ary48_33xvvnyd3fUD9Kg8VKC131wum_Oz5t0r9CBVE7T-9mF9dbV6_3q9XK7efkaBPxFWOXUOD0X3R8FeFEQkDqKYzK6HOJHvT052cilPNKhnIoNoemAB6i_okIThbU_KVO8hf3oIHYUj59F1an_u18VZ8-PTjRhLuyltZiV5NH0i-ewvBLlFEEvE_yKGGwJKbmtlWu9DjqqCiRLloijogHPuaaPkEdBBnucO-88FN3M6rF54mSykooMwDMdbIUcj7SJispvBvf9KabntlKyotQHlkjZWOkjTdDuGbGLsxE1S36jXl9YD4nWldsc1irtj2D39htdumy1l69q-zH3H2MMLUAsmeLuux50uwWYOC0gwbSGHnNWFSXBSnrbSuuLMwEMujFSY5qzQ4GFWG3nwsswwNaqGXrQvWLsgC6c6_Q0zxBrK" >}}

这将需要一个如下所示的 Ingress：

{{< codenew file="service/networking/simple-fanout-example.yaml" >}}

当你使用 `kubectl apply -f` 创建 Ingress 时：

```shell
kubectl describe ingress simple-fanout-example
```

```
Name:             simple-fanout-example
Namespace:        default
Address:          178.91.123.132
Default backend:  default-http-backend:80 (10.8.2.3:8080)
Rules:
  Host         Path  Backends
  ----         ----  --------
  foo.bar.com
               /foo   service1:4200 (10.8.0.90:4200)
               /bar   service2:8080 (10.8.0.91:8080)
Annotations:
  nginx.ingress.kubernetes.io/rewrite-target:  /
Events:
  Type     Reason  Age                From                     Message
  ----     ------  ----               ----                     -------
  Normal   ADD     22s                loadbalancer-controller  default/test
```

Ingress 控制器将提供实现特定的负载均衡器来满足 Ingress，
只要 Service (`service1`，`service2`) 存在。
当它这样做时，你会在 Address 字段看到负载均衡器的地址。

{{< note >}}
取决于你所使用的 [Ingress 控制器](/zh-cn/docs/concepts/services-networking/ingress-controllers/)，
你可能需要创建默认 HTTP 后端[服务](/zh-cn/docs/concepts/services-networking/service/)。
{{< /note >}}

### 基于名称的虚拟托管   {#name-based-virtual-hosting}

基于名称的虚拟主机支持将针对多个主机名的 HTTP 流量路由到同一 IP 地址上。

{{< figure src="/zh-cn/docs/images/ingressNameBased.svg" alt="ingress-namebase-diagram" class="diagram-large" caption="图. 基于名称实现虚拟托管的 Ingress" link="https://mermaid.live/edit#pako:eNqNkk9v0zAYxr-K5V6GlESNU6B4qKdxQOKA2LHpwYnfrNaSOLId_mjbDQ2OXAdMUxEHJKRxQWLaND4NXcq3IJkT2gKTuDiv_Dzv73UevXs4lhwwxTuKFVP06MlmmCMUpwJyszGen364ev2t-vxlcsv10MN8R4HWbnU6q94cVm9fovuRGqHF15PF5eX8-NViNpsffUKeOxLWOW47HOTfHXr3fM8ngecHZHI9pDW57mj_x9nF1ftzihIpvYgpL5bZvgb1VMTgj7dtgboLOuzfCGiaG8gKgPwJIL8Buozsb_98d1h9_7jCtHI7sB5QSO6PH0s--YdA_hKIFYKbhMFSgJzbwJnWW5CgImUiR4lIU9rjnDvaKLkLtJckSVu7zwQ3UzoonjuxTKWivX6_v7kG2R3qFhGQOzHc_i9Kra1T4rTUBlRLWrbSXhRF6xiyxNiJS1KXqNOF1hXEaUJtjusqaI5B8_SVXruHNpS1a_uy9lsr2MEZqIwJXq_yXuMMsZlCBiGmdckhYWVqQhzmB7W1LDgz8IALIxWmCUs1OJiVRm6_yGNMjSqhM20JVq9I1roOfgEKNyn5" >}}

以下 Ingress 让后台负载均衡器基于
[host 头部字段](https://tools.ietf.org/html/rfc7230#section-5.4)来路由请求。

{{< codenew file="service/networking/name-virtual-host-ingress.yaml" >}}

如果你创建的 Ingress 资源没有在 `rules` 中定义的任何 `hosts`，则可以匹配指向
Ingress 控制器 IP 地址的任何网络流量，而无需基于名称的虚拟主机。

例如，以下 Ingress 会将请求 `first.bar.com` 的流量路由到 `service1`，将请求
`second.bar.com` 的流量路由到 `service2`，而所有其他流量都会被路由到 `service3`。

{{< codenew file="service/networking/name-virtual-host-ingress-no-third-host.yaml" >}}

### TLS

你可以通过设定包含 TLS 私钥和证书的{{< glossary_tooltip text="Secret" term_id="secret" >}}
来保护 Ingress。
Ingress 只支持单个 TLS 端口 443，并假定 TLS 连接终止于
Ingress 节点（与 Service 及其 Pod 之间的流量都以明文传输）。
如果 Ingress 中的 TLS 配置部分指定了不同的主机，那么它们将根据通过
SNI TLS 扩展指定的主机名（如果 Ingress 控制器支持 SNI）在同一端口上进行复用。
TLS Secret 的数据中必须包含用于 TLS 的以键名 `tls.crt` 保存的证书和以键名 `tls.key` 保存的私钥。
例如：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: testsecret-tls
  namespace: default
data:
  tls.crt: base64 编码的证书
  tls.key: base64 编码的私钥
type: kubernetes.io/tls
```

在 Ingress 中引用此 Secret 将会告诉 Ingress 控制器使用 TLS 加密从客户端到负载均衡器的通道。
你需要确保创建的 TLS Secret 创建自包含 `https-example.foo.com` 的公用名称（CN）的证书。
这里的公共名称也被称为全限定域名（FQDN）。

{{< note >}}
注意，默认规则上无法使用 TLS，因为需要为所有可能的子域名发放证书。
因此，`tls` 字段中的 `hosts` 的取值需要与 `rules` 字段中的 `host` 完全匹配。
{{< /note >}}

{{< codenew file="service/networking/tls-example-ingress.yaml" >}}

{{< note >}}
各种 Ingress 控制器所支持的 TLS 功能之间存在差异。请参阅有关
[nginx](https://kubernetes.github.io/ingress-nginx/user-guide/tls/)、
[GCE](https://git.k8s.io/ingress-gce/README.md#frontend-https)
或者任何其他平台特定的 Ingress 控制器的文档，以了解 TLS 如何在你的环境中工作。
{{< /note >}}

### 负载均衡  {#load-balancing}

Ingress 控制器启动引导时使用一些适用于所有 Ingress
的负载均衡策略设置，例如负载均衡算法、后端权重方案等。
更高级的负载均衡概念（例如持久会话、动态权重）尚未通过 Ingress 公开。
你可以通过用于服务的负载均衡器来获取这些功能。

值得注意的是，尽管健康检查不是通过 Ingress 直接暴露的，在 Kubernetes
中存在并行的概念，比如
[就绪检查](/zh-cn/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)，
允许你实现相同的目的。
请检查特定控制器的说明文档（例如：[nginx](https://git.k8s.io/ingress-nginx/README.md)、
[GCE](https://git.k8s.io/ingress-gce/README.md#health-checks)）以了解它们是怎样处理健康检查的。

## 更新 Ingress   {#updating-an-ingress}

要更新现有的 Ingress 以添加新的 Host，可以通过编辑资源来对其进行更新：

```shell
kubectl describe ingress test
```

```
Name:             test
Namespace:        default
Address:          178.91.123.132
Default backend:  default-http-backend:80 (10.8.2.3:8080)
Rules:
  Host         Path  Backends
  ----         ----  --------
  foo.bar.com
               /foo   service1:80 (10.8.0.90:80)
Annotations:
  nginx.ingress.kubernetes.io/rewrite-target:  /
Events:
  Type     Reason  Age                From                     Message
  ----     ------  ----               ----                     -------
  Normal   ADD     35s                loadbalancer-controller  default/test
```

```shell
kubectl edit ingress test
```

这一命令将打开编辑器，允许你以 YAML 格式编辑现有配置。
修改它来增加新的主机：

```yaml
spec:
  rules:
  - host: foo.bar.com
    http:
      paths:
      - backend:
          service:
            name: service1
            port:
              number: 80
        path: /foo
        pathType: Prefix
  - host: bar.baz.com
    http:
      paths:
      - backend:
          service:
            name: service2
            port:
              number: 80
        path: /foo
        pathType: Prefix
..
```

保存更改后，kubectl 将更新 API 服务器中的资源，该资源将告诉 Ingress 控制器重新配置负载均衡器。

验证：

```shell
kubectl describe ingress test
```

```
Name:             test
Namespace:        default
Address:          178.91.123.132
Default backend:  default-http-backend:80 (10.8.2.3:8080)
Rules:
  Host         Path  Backends
  ----         ----  --------
  foo.bar.com
               /foo   service1:80 (10.8.0.90:80)
  bar.baz.com
               /foo   service2:80 (10.8.0.91:80)
Annotations:
  nginx.ingress.kubernetes.io/rewrite-target:  /
Events:
  Type     Reason  Age                From                     Message
  ----     ------  ----               ----                     -------
  Normal   ADD     45s                loadbalancer-controller  default/test
```


你也可以通过 `kubectl replace -f` 命令调用修改后的 Ingress yaml 文件来获得同样的结果。

## 跨可用区失败  {#failing-across-availability-zones}

不同的云厂商使用不同的技术来实现跨故障域的流量分布。详情请查阅相关 Ingress 控制器的文档。
请查看相关 [Ingress 控制器](/zh-cn/docs/concepts/services-networking/ingress-controllers)的文档以了解详细信息。

## 替代方案    {#alternatives}

不直接使用 Ingress 资源，也有多种方法暴露 Service：

* 使用 [Service.Type=LoadBalancer](/zh-cn/docs/concepts/services-networking/service/#loadbalancer)
* 使用 [Service.Type=NodePort](/zh-cn/docs/concepts/services-networking/service/#nodeport)

## {{% heading "whatsnext" %}}

* 进一步了解 [Ingress](/zh-cn/docs/reference/kubernetes-api/service-resources/ingress-v1/) API
* 进一步了解 [Ingress 控制器](/zh-cn/docs/concepts/services-networking/ingress-controllers/)
* [使用 NGINX 控制器在 Minikube 上安装 Ingress](/zh-cn/docs/tasks/access-application-cluster/ingress-minikube/)

