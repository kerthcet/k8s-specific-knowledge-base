---
title: 访问集群上运行的服务
content_type: task
weight: 140
---

本文展示了如何连接 Kubernetes 集群上运行的服务。

## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


## 访问集群上运行的服务  {#accessing-services-running-on-the-cluster}

在 Kubernetes 里，[节点](/zh-cn/docs/concepts/architecture/nodes/)、
[Pod](/zh-cn/docs/concepts/workloads/pods/) 和
[服务](/zh-cn/docs/concepts/services-networking/service/) 都有自己的 IP。
许多情况下，集群上的节点 IP、Pod IP 和某些服务 IP 是路由不可达的，
所以不能从集群之外访问它们，例如从你自己的台式机。

### 连接方式   {#ways-to-connect}

你有多种可选方式从集群外连接节点、Pod 和服务：

- 通过公网 IP 访问服务
  - 使用类型为 `NodePort` 或 `LoadBalancer` 的服务，可以从外部访问它们。
    请查阅[服务](/zh-cn/docs/concepts/services-networking/service/) 和
    [kubectl expose](/docs/reference/generated/kubectl/kubectl-commands/#expose) 文档。
  - 取决于你的集群环境，你可以仅把服务暴露在你的企业网络环境中，也可以将其暴露在
    因特网上。需要考虑暴露的服务是否安全，它是否有自己的用户认证？
  - 将 Pod 放置于服务背后。如果要访问一个副本集合中特定的 Pod，例如用于调试目的，
    请给 Pod 指定一个独特的标签并创建一个新服务选择该标签。
  - 大部分情况下，都不需要应用开发者通过节点 IP 直接访问节点。
- 通过 Proxy 动词访问服务、节点或者 Pod
  - 在访问远程服务之前，利用 API 服务器执行身份认证和鉴权。
    如果你的服务不够安全，无法暴露到因特网中，或者需要访问节点 IP 上的端口，
    又或者出于调试目的，可使用这种方式。
  - 代理可能给某些应用带来麻烦
  - 此方式仅适用于 HTTP/HTTPS
  - 进一步的描述在[这里](#manually-constructing-apiserver-proxy-urls)
  - 从集群中的 node 或者 pod 访问。
- 从集群中的一个节点或 Pod 访问
  - 运行一个 Pod，然后使用
    [kubectl exec](/docs/reference/generated/kubectl/kubectl-commands/#exec)
    连接到它的 Shell。从那个 Shell 连接其他的节点、Pod 和 服务
  - 某些集群可能允许你 SSH 到集群中的节点。你可能可以从那儿访问集群服务。
    这是一个非标准的方式，可能在一些集群上能工作，但在另一些上却不能。
    浏览器和其他工具可能已经安装也可能没有安装。集群 DNS 可能不会正常工作。

### 发现内置服务   {#discovering-builtin-services}

典型情况下，kube-system 名字空间中会启动集群的几个服务。
使用 `kubectl cluster-info` 命令获取这些服务的列表：

```shell
kubectl cluster-info
```

输出类似于：

```
Kubernetes master is running at https://192.0.2.1
elasticsearch-logging is running at https://192.0.2.1/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy
kibana-logging is running at https://192.0.2.1/api/v1/namespaces/kube-system/services/kibana-logging/proxy
kube-dns is running at https://192.0.2.1/api/v1/namespaces/kube-system/services/kube-dns/proxy
grafana is running at https://192.0.2.1/api/v1/namespaces/kube-system/services/monitoring-grafana/proxy
heapster is running at https://192.0.2.1/api/v1/namespaces/kube-system/services/monitoring-heapster/proxy
```

这一输出显示了用 proxy 动词访问每个服务时可用的 URL。例如，此集群
（使用 Elasticsearch）启用了集群层面的日志。如果提供合适的凭据，可以通过
`https://192.0.2.1/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/`
访问，或通过一个 `kubectl proxy` 来访问：
`http://localhost:8080/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/`。

{{< note >}}
请参阅[使用 Kubernetes API 访问集群](/zh-cn/docs/tasks/administer-cluster/access-cluster-api/#accessing-the-cluster-api)
了解如何传递凭据或如何使用 `kubectl proxy`。
{{< /note >}}

#### 手动构建 API 服务器代理 URLs   {#manually-constructing-apiserver-proxy-urls}

如前所述，你可以使用 `kubectl cluster-info` 命令取得服务的代理 URL。
为了创建包含服务末端、后缀和参数的代理 URLs，你可以在服务的代理 URL 中添加：
`http://`*`kubernetes_master_address`*`/api/v1/namespaces/`*`namespace_name`*`/services/`*`service_name[:port_name]`*`/proxy`

如果还没有为你的端口指定名称，你可以不用在 URL 中指定 *port_name*。
对于命名和未命名端口，你还可以使用端口号代替 *port_name*。

默认情况下，API 服务器使用 HTTP 为你的服务提供代理。 要使用 HTTPS，请在服务名称前加上 `https:`：
`http://<kubernetes_master_address>/api/v1/namespaces/<namespace_name>/services/<service_name>/proxy`
URL 的 `<service_name>` 段支持的格式为：
* `<service_name>` - 使用 http 代理到默认或未命名端口
* `<service_name>:<port_name>` - 使用 http 代理到指定的端口名称或端口号
* `https:<service_name>:` -  使用 https 代理到默认或未命名端口（注意尾随冒号）
* `https:<service_name>:<port_name>` - 使用 https 代理到指定的端口名称或端口号

##### 示例   {#examples}

* 如要访问 Elasticsearch 服务末端 `_search?q=user:kimchy`，你可以使用以下地址：

  ```
  http://192.0.2.1/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/_search?q=user:kimchy
  ```

* 如要访问 Elasticsearch 集群健康信息`_cluster/health?pretty=true`，你可以使用以下地址：

  ```
  https://192.0.2.1/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/_cluster/health?pretty=true
  ```

    健康信息与下面的例子类似：

    ```json
    {
      "cluster_name" : "kubernetes_logging",
      "status" : "yellow",
      "timed_out" : false,
      "number_of_nodes" : 1,
      "number_of_data_nodes" : 1,
      "active_primary_shards" : 5,
      "active_shards" : 5,
      "relocating_shards" : 0,
      "initializing_shards" : 0,
      "unassigned_shards" : 5
    }
    ```

* 如要访问 **https** Elasticsearch 服务健康信息 `_cluster/health?pretty=true`，你可以使用以下地址：

  ```
  https://192.0.2.1/api/v1/namespaces/kube-system/services/https:elasticsearch-logging:/proxy/_cluster/health?pretty=true
  ```

#### 通过 Web 浏览器访问集群中运行的服务    {#uusing-web-browsers-to-access-services-running-on-the-cluster}

你或许能够将 API 服务器代理的 URL 放入浏览器的地址栏，然而：

  - Web 服务器通常不能传递令牌，所以你可能需要使用基本（密码）认证。
    API 服务器可以配置为接受基本认证，但你的集群可能并没有这样配置。
  - 某些 Web 应用可能无法工作，特别是那些使用客户端 Javascript 构造 URL 的
    应用，所构造的 URL 可能并不支持代理路径前缀。
