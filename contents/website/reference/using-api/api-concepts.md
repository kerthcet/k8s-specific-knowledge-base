---
title: Kubernetes API 概念
content_type: concept
weight: 20
---

Kubernetes API 是通过 HTTP 提供的基于资源 (RESTful) 的编程接口。
它支持通过标准 HTTP 动词（POST、PUT、PATCH、DELETE、GET）检索、创建、更新和删除主要资源。

对于某些资源，API 包括额外的子资源，允许细粒度授权（例如：将 Pod 的详细信息与检索日志分开），
为了方便或者提高效率，可以以不同的表示形式接受和服务这些资源。

Kubernetes 支持通过 **watch** 实现高效的资源变更通知。
Kubernetes 还提供了一致的列表操作，以便 API 客户端可以有效地缓存、跟踪和同步资源的状态。

你可以在线查看 [API 参考](/zh-cn/docs/reference/kubernetes-api/)，
或继续阅读以了解 API 的一般信息。


## Kubernetes API 术语  {#standard-api-terminology}

Kubernetes 通常使用常见的 RESTful 术语来描述 API 概念：
* **资源类型（Resource Type）** 是 URL 中使用的名称（`pods`、`namespaces`、`services`）
* 所有资源类型都有一个具体的表示（它们的对象模式），称为 **类别（Kind）**
* 资源实例的列表称为 **集合（Collection）**
* 资源类型的单个实例称为 **资源（Resource）**，通常也表示一个 **对象（Object）**
* 对于某些资源类型，API 包含一个或多个 **子资源（sub-resources）**，这些子资源表示为资源下的 URI 路径

大多数 Kubernetes API
资源类型都是[对象](/zh-cn/docs/concepts/overview/working-with-objects/kubernetes-objects/#kubernetes-objects)：
它们代表集群上某个概念的具体实例，例如 Pod 或名字空间。
少数 API 资源类型是 “虚拟的”，它们通常代表的是操作而非对象本身，
例如权限检查（使用带有 JSON 编码的 `SubjectAccessReview` 主体的 POST 到 `subjectaccessreviews` 资源），
或 Pod 的子资源 `eviction`（用于触发 [API-发起的驱逐](/zh-cn/docs/concepts/scheduling-eviction/api-eviction/)）。


### 对象名字 {#object-names}

你可以通过 API 创建的所有对象都有一个唯一的{{< glossary_tooltip text="名字" term_id="name" >}}，
以允许幂等创建和检索，
但如果虚拟资源类型不可检索或不依赖幂等性，则它们可能没有唯一名称。
在{{< glossary_tooltip text="名字空间" term_id="namespace" >}}内，
同一时刻只能有一个给定类别的对象具有给定名称。
但是，如果你删除该对象，你可以创建一个具有相同名称的新对象。
有些对象没有名字空间（例如：节点），因此它们的名称在整个集群中必须是唯一的。

### API 动词 {#api-verbs}

几乎所有对象资源类型都支持标准 HTTP 动词 - GET、POST、PUT、PATCH 和 DELETE。
Kubernetes 也使用自己的动词，这些动词通常写成小写，以区别于 HTTP 动词。

Kubernetes 使用术语 **list** 来描述返回资源[集合](#collections)，
以区别于通常称为 **get** 的单个资源检索。
如果你发送带有 `?watch` 查询参数的 HTTP GET 请求，
Kubernetes 将其称为 **watch** 而不是 **get**（有关详细信息，请参阅[快速检测更改](#efficient-detection-of-changes)）。

对于 PUT 请求，Kubernetes 在内部根据现有对象的状态将它们分类为 **create** 或 **update**。
**update** 不同于 **patch**；**patch** 的 HTTP 动词是 PATCH。

## 资源 URI {#resource-uris}

所有资源类型要么是集群作用域的（`/apis/GROUP/VERSION/*`），
要么是名字空间作用域的（`/apis/GROUP/VERSION/namespaces/NAMESPACE/*`）。
名字空间作用域的资源类型会在其名字空间被删除时也被删除，
并且对该资源类型的访问是由定义在名字空间域中的授权检查来控制的。

注意： 核心资源使用 `/api` 而不是 `/apis`，并且不包含 GROUP 路径段。

例如:
* `/api/v1/namespaces`
* `/api/v1/pods`
* `/api/v1/namespaces/my-namespace/pods`
* `/apis/apps/v1/deployments`
* `/apis/apps/v1/namespaces/my-namespace/deployments`
* `/apis/apps/v1/namespaces/my-namespace/deployments/my-deployment`

你还可以访问资源集合（例如：列出所有 Node）。以下路径用于检索集合和资源：

* 集群作用域的资源：
  * `GET /apis/GROUP/VERSION/RESOURCETYPE` - 返回指定资源类型的资源的集合
  * `GET /apis/GROUP/VERSION/RESOURCETYPE/NAME` - 返回指定资源类型下名称为 NAME 的资源
* 名字空间作用域的资源：
  * `GET /apis/GROUP/VERSION/RESOURCETYPE` - 返回所有名字空间中指定资源类型的全部实例的集合
  * `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE` - 返回名字空间 NAMESPACE 内给定资源类型的全部实例的集合
  * `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE/NAME` - 返回名字空间 NAMESPACE 中给定资源类型的名称为 NAME 的实例

由于名字空间本身是一个集群作用域的资源类型，你可以通过 `GET /api/v1/namespaces/`
检视所有名字空间的列表（“集合”），使用 `GET /api/v1/namespaces/NAME` 查看特定名字空间的详细信息。

* 集群作用域的子资源：`GET /apis/GROUP/VERSION/RESOURCETYPE/NAME/SUBRESOURCE`
* 名字空间作用域的子资源：`GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE/NAME/SUBRESOURCE`

取决于对象是什么，每个子资源所支持的动词有所不同 - 参见 [API 文档](/zh-cn/docs/reference/kubernetes-api/)以了解更多信息。
跨多个资源来访问其子资源是不可能的 - 如果需要这一能力，则通常意味着需要一种新的虚拟资源类型了。

## 高效检测变更  {#efficient-detection-of-changes}

Kubernetes API 允许客户端对对象或集合发出初始请求，然后跟踪自该初始请求以来的更改：**watch**。
客户端可以发送 **list** 或者 **get** 请求，然后发出后续 **watch** 请求。

为了使这种更改跟踪成为可能，每个 Kubernetes 对象都有一个 `resourceVersion` 字段，
表示存储在底层持久层中的该资源的版本。在检索资源集合（名字空间或集群范围）时，
来自 API 服务器的响应包含一个 `resourceVersion` 值。
客户端可以使用该 `resourceVersion` 来启动对 API 服务器的 **watch**。

当你发送 **watch** 请求时，API 服务器会响应更改流。
这些更改逐项列出了在你指定为 **watch** 请求参数的 `resourceVersion` 之后发生的操作
（例如 **create**、**delete** 和 **update**）的结果。
整个 **watch** 机制允许客户端获取当前状态，然后订阅后续更改，而不会丢失任何事件。

如果客户端 **watch** 连接断开，则该客户端可以从最后返回的 `resourceVersion` 开始新的 **watch** 请求；
客户端还可以执行新的 **get**/**list** 请求并重新开始。有关更多详细信息，请参阅[资源版本语义](#resource-versions)。

例如：

1. 列举给定名字空间中的所有 Pod：

   ```console
   GET /api/v1/namespaces/test/pods
   ---
   200 OK
   Content-Type: application/json

   {
     "kind": "PodList",
     "apiVersion": "v1",
     "metadata": {"resourceVersion":"10245"},
     "items": [...]
   }
   ```

2. 从资源版本 10245 开始，接收影响 _test_ 名字空间中 Pod 的所有 API 操作
   （例如 **create**、**delete**、**apply** 或 **update**）的通知。
   每个更改通知都是一个 JSON 文档。
   HTTP 响应正文（用作 `application/json`）由一系列 JSON 文档组成。

   ```console
   GET /api/v1/namespaces/test/pods?watch=1&resourceVersion=10245
   ---
   200 OK
   Transfer-Encoding: chunked
   Content-Type: application/json

   {
     "type": "ADDED",
     "object": {"kind": "Pod", "apiVersion": "v1", "metadata": {"resourceVersion": "10596", ...}, ...}
   }
   {
     "type": "MODIFIED",
     "object": {"kind": "Pod", "apiVersion": "v1", "metadata": {"resourceVersion": "11020", ...}, ...}
   }
   ...
   ```

给定的 Kubernetes 服务器只会保留一定的时间内发生的历史变更列表。
使用 etcd3 的集群默认保存过去 5 分钟内发生的变更。
当所请求的 **watch** 操作因为资源的历史版本不存在而失败，
客户端必须能够处理因此而返回的状态代码 `410 Gone`，清空其本地的缓存，
重新执行 **get** 或者 **list** 操作，
并基于新返回的 `resourceVersion` 来开始新的 **watch** 操作。

对于订阅集合，Kubernetes 客户端库通常会为 **list** -然后- **watch** 的逻辑提供某种形式的标准工具。
（在 Go 客户端库中，这称为 `反射器（Reflector）`，位于 `k8s.io/client-go/tools/cache` 包中。）

### 监视书签  {#Watch-bookmark}

为了减轻短历史窗口的影响，Kubernetes API 提供了一个名为 `BOOKMARK` 的监视事件。
这是一种特殊的事件，用于标记客户端请求的给定 `resourceVersion` 的所有更改都已发送。
代表 `BOOKMARK` 事件的文档属于请求所请求的类型，但仅包含一个 `.metadata.resourceVersion` 字段。例如：

```console
GET /api/v1/namespaces/test/pods?watch=1&resourceVersion=10245&allowWatchBookmarks=true
---
200 OK
Transfer-Encoding: chunked
Content-Type: application/json

{
  "type": "ADDED",
  "object": {"kind": "Pod", "apiVersion": "v1", "metadata": {"resourceVersion": "10596", ...}, ...}
}
...
{
  "type": "BOOKMARK",
  "object": {"kind": "Pod", "apiVersion": "v1", "metadata": {"resourceVersion": "12746"} }
}
```

作为客户端，你可以在 **watch** 请求中设置 `allowWatchBookmarks=true` 查询参数来请求 `BOOKMARK` 事件，
但你不应假设书签会在任何特定时间间隔返回，即使要求时，客户端也不能假设 API 服务器会发送任何 `BOOKMARK` 事件。

## 流式列表  {#streaming-lists}

{{< feature-state for_k8s_version="v1.27" state="alpha" >}}

在大型集群检索某些资源类型的集合可能会导致控制平面的资源使用量（主要是 RAM）显著增加。
为了减轻其影响并简化 **list** + **watch** 模式的用户体验，
Kubernetes 1.27 版本引入了一个 alpha 功能，支持在 **watch** 请求中请求初始状态
（之前在 **list** 请求中请求）。

如果启用了 `WatchList` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)，
可以通过在 **watch** 请求中指定 `sendInitialEvents=true` 作为查询字符串参数来实现这一功能。
如果指定了这个参数，API 服务器将使用合成的初始事件（类型为 `ADDED`）来启动监视流，
以构建所有现有对象的完整状态；如果请求还带有 `allowWatchBookmarks=true` 选项，
则继续发送 [`BOOKMARK` 事件](/zh-cn/docs/reference/using-api/api-concepts/#watch-bookmarks)。
BOOKMARK 事件包括已被同步的资源版本。
发送 BOOKMARK 事件后，API 服务器会像处理所有其他 **watch** 请求一样继续执行。

当你在查询字符串中设置 `sendInitialEvents=true` 时，
Kubernetes 还要求你将 `resourceVersionMatch` 的值设置为 `NotOlderThan`。
如果你在查询字符串中提供 `resourceVersion` 而没有提供值或者根本没有提供这个参数，
这一请求将被视为 **一致性读（Consistent Read）** 请求；
当状态至少被同步到开始处理一致性读操作时，才会发送 BOOKMARK 事件。
如果你（在查询字符串中）指定了 `resourceVersion`，则只要需要等状态同步到所给资源版本时，
BOOKMARK 事件才会被发送。

### 示例  {#example-streaming-lists}

举个例子：你想监视一组 Pod。对于该集合，当前资源版本为 10245，并且有两个 Pod：`foo` 和 `bar`。
接下来你发送了以下请求（通过使用 `resourceVersion=` 设置空的资源版本来明确请求 **一致性读**），
这样做的结果是可能收到如下事件序列：

```console
GET /api/v1/namespaces/test/pods?watch=1&sendInitialEvents=true&allowWatchBookmarks=true&resourceVersion=&resourceVersionMatch=NotOlderThan
---
200 OK
Transfer-Encoding: chunked
Content-Type: application/json

{
  "type": "ADDED",
  "object": {"kind": "Pod", "apiVersion": "v1", "metadata": {"resourceVersion": "8467", "name": "foo"}, ...}
}
{
  "type": "ADDED",
  "object": {"kind": "Pod", "apiVersion": "v1", "metadata": {"resourceVersion": "5726", "name": "bar"}, ...}
}
{
  "type": "BOOKMARK",
  "object": {"kind": "Pod", "apiVersion": "v1", "metadata": {"resourceVersion": "10245"} }
}
...
<followed by regular watch stream starting from resourceVersion="10245">
```

## 响应压缩   {#response-compression}

{{< feature-state for_k8s_version="v1.16" state="beta" >}}

`APIResponseCompression` 是一个选项，允许 API 服务器压缩 **get** 和 **list** 请求的响应，
减少占用的网络带宽并提高大规模集群的性能。此选项自 Kubernetes 1.16 以来默认启用，
可以通过在 API 服务器上的 `--feature-gates` 标志中包含 `APIResponseCompression=false` 来禁用。

特别是对于大型资源或[集合](/zh-cn/docs/reference/using-api/api-concepts/#collections)，
API 响应压缩可以显著减小其响应的大小。例如，针对 Pod 的 **list** 请求可能会返回数百 KB 甚至几 MB 的数据，
具体大小取决于 Pod 数量及其属性。通过压缩响应，可以节省网络带宽并降低延迟。

要验证 `APIResponseCompression` 是否正常工作，你可以使用一个 `Accept-Encoding`
头向 API 服务器发送一个 **get** 或 **list** 请求，并检查响应大小和头信息。例如：

```console
GET /api/v1/pods
Accept-Encoding: gzip
---
200 OK
Content-Type: application/json
content-encoding: gzip
...
```

`content-encoding` 头表示响应使用 `gzip` 进行了压缩。

## 分块检视大体量结果  {#retrieving-large-results-sets-in-chunks}

{{< feature-state for_k8s_version="v1.9" state="beta" >}}

在较大规模集群中，检索某些资源类型的集合可能会导致非常大的响应，从而影响服务器和客户端。
例如，一个集群可能有数万个 Pod，每个 Pod 大约相当于 2 KiB 的编码 JSON。
跨所有名字空间检索所有 Pod 可能会导致非常大的响应 (10-20MB) 并消耗大量服务器资源。

如果你没有明确禁用 `APIListChunking` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)，
Kubernetes API 服务器支持将单个大型集合请求分解为许多较小块的能力，同时保持总请求的一致性。

你可以请求 API 服务器通过使用页（Kubernetes 将其称为“块（Chunk）”）的方式来处理 **list**，
完成单个集合的响应。
要以块的形式检索单个集合，针对集合的请求支持两个查询参数 `limit` 和 `continue`，
并且从集合元 `metadata` 字段中的所有 **list** 操作返回响应字段 `continue`。
客户端应该指定他们希望在每个带有 `limit` 的块中接收的条目数上限，如果集合中有更多资源，
服务器将在结果中返回 `limit` 资源并包含一个 `continue` 值。

作为 API 客户端，你可以在下一次请求时将 `continue` 值传递给 API 服务器，
以指示服务器返回下一页（_块_）结果。继续下去直到服务器返回一个空的 `continue` 值，
你可以检索整个集合。

与 **watch** 操作类似，`continue` 令牌也会在很短的时间（默认为 5 分钟）内过期，
并在无法返回更多结果时返回 `410 Gone` 代码。
这时，客户端需要从头开始执行上述检视操作或者忽略 `limit` 参数。

例如，如果集群上有 1253 个 Pod，客户端希望每次收到包含至多 500 个 Pod
的数据块，它应按下面的步骤来请求数据块：

1. 列举集群中所有 Pod，每次接收至多 500 个 Pod：

   ```console
   GET /api/v1/pods?limit=500
   ---
   200 OK
   Content-Type: application/json

   {
     "kind": "PodList",
     "apiVersion": "v1",
     "metadata": {
       "resourceVersion":"10245",
       "continue": "ENCODED_CONTINUE_TOKEN",
       "remainingItemCount": 753,
       ...
     },
     "items": [...] // returns pods 1-500
   }
   ```

2. 继续前面的调用，返回下一组 500 个 Pod：

   ```console
   GET /api/v1/pods?limit=500&continue=ENCODED_CONTINUE_TOKEN
   ---
   200 OK
   Content-Type: application/json

   {
     "kind": "PodList",
     "apiVersion": "v1",
     "metadata": {
       "resourceVersion":"10245",
       "continue": "ENCODED_CONTINUE_TOKEN_2",
       "remainingItemCount": 253,
       ...
     },
     "items": [...] // returns pods 501-1000
   }
   ```

3. 继续前面的调用，返回最后 253 个 Pod：

   ```console
   GET /api/v1/pods?limit=500&continue=ENCODED_CONTINUE_TOKEN_2
   ---
   200 OK
   Content-Type: application/json

   {
     "kind": "PodList",
     "apiVersion": "v1",
     "metadata": {
       "resourceVersion":"10245",
       "continue": "", // continue token is empty because we have reached the end of the list
       ...
     },
     "items": [...] // returns pods 1001-1253
   }
   ```

请注意，集合的 `resourceVersion` 在每个请求中保持不变，
这表明服务器正在向你显示 Pod 的一致快照。
在版本 `10245` 之后创建、更新或删除的 Pod 将不会显示，
除非你在没有继续令牌的情况下发出单独的 **list** 请求。
这使你可以将大请求分成更小的块，然后对整个集合执行 **watch** 操作，而不会丢失任何更新。

`remainingItemCount` 是集合中未包含在此响应中的后续项目的数量。
如果 **list** 请求包含标签或字段{{< glossary_tooltip text="选择器" term_id="selector">}}，
则剩余项目的数量是未知的，并且 API 服务器在其响应中不包含 `remainingItemCount` 字段。
如果 **list** 是完整的（因为它没有分块，或者因为这是最后一个块），没有更多的剩余项目，
API 服务器在其响应中不包含 `remainingItemCount` 字段。
`remainingItemCount` 的用途是估计集合的大小。

## 集合 {#collections}

在 Kubernetes 术语中，你从 **list** 中获得的响应是一个“集合（Collections）”。
然而，Kubernetes 为不同类型资源的集合定义了具体类型。
集合的类别名是针对资源类别的，并附加了 `List`。

当你查询特定类型的 API 时，该查询返回的所有项目都属于该类型。
例如，当你 **list** Service 对象时，集合响应的 `kind` 设置为
[`ServiceList`](/zh-cn/docs/reference/kubernetes-api/service-resources/service-v1/#ServiceList)；
该集合中的每个项目都代表一个 Service。例如：

```
GET /api/v1/services
```
```yaml
{
  "kind": "ServiceList",
  "apiVersion": "v1",
  "metadata": {
    "resourceVersion": "2947301"
  },
  "items": [
    {
      "metadata": {
        "name": "kubernetes",
        "namespace": "default",
...
      "metadata": {
        "name": "kube-dns",
        "namespace": "kube-system",
...
```

Kubernetes API 中定义了数十种集合类型（如 `PodList`、`ServiceList` 和 `NodeList`）。
你可以从 [Kubernetes API](/zh-cn/docs/reference/kubernetes-api/) 文档中获取有关每种集合类型的更多信息。

一些工具，例如 `kubectl`，对于 Kubernetes 集合的表现机制与 Kubernetes API 本身略有不同。
因为 `kubectl` 的输出可能包含来自 API 级别的多个 **list** 操作的响应，
所以 `kubectl` 使用 `kind: List` 表示项目列表。例如：

```shell
kubectl get services -A -o yaml
```
```yaml
apiVersion: v1
kind: List
metadata:
  resourceVersion: ""
  selfLink: ""
items:
- apiVersion: v1
  kind: Service
  metadata:
    creationTimestamp: "2021-06-03T14:54:12Z"
    labels:
      component: apiserver
      provider: kubernetes
    name: kubernetes
    namespace: default
...
- apiVersion: v1
  kind: Service
  metadata:
    annotations:
      prometheus.io/port: "9153"
      prometheus.io/scrape: "true"
    creationTimestamp: "2021-06-03T14:54:14Z"
    labels:
      k8s-app: kube-dns
      kubernetes.io/cluster-service: "true"
      kubernetes.io/name: CoreDNS
    name: kube-dns
    namespace: kube-system
```

{{< note >}}
请记住，Kubernetes API 没有名为 `List` 的 `kind`。

`kind: List` 是一个客户端内部实现细节，用于处理可能属于不同类别的对象的集合。
在自动化或其他代码中避免依赖 `kind: List`。
{{< /note >}}

## 以表格形式接收资源  {#receiving-resources-as-tables}

当你执行 `kubectl get` 时，默认的输出格式是特定资源类型的一个或多个实例的简单表格形式。
过去，客户端需要重复 `kubectl` 中所实现的表格输出和描述输出逻辑，以执行简单的对象列表操作。
该方法的一些限制包括处理某些对象时的不可忽视逻辑。
此外，API 聚合或第三方资源提供的类型在编译时是未知的。
这意味着必须为客户端无法识别的类型提供通用实现。

为了避免上述各种潜在的局限性，客户端可以请求服务器端返回对象的表格（Table）
表现形式，从而将打印输出的特定细节委托给服务器。
Kubernetes API 实现标准的 HTTP 内容类型（Content Type）协商：为 `GET`
调用传入一个值为 `application/json;as=Table;g=meta.k8s.io;v=v1` 的 `Accept`
头部即可请求服务器以 Table 的内容类型返回对象。

例如，以 Table 格式列举集群中所有 Pod：

```console
GET /api/v1/pods
Accept: application/json;as=Table;g=meta.k8s.io;v=v1
---
200 OK
Content-Type: application/json

{
    "kind": "Table",
    "apiVersion": "meta.k8s.io/v1",
    ...
    "columnDefinitions": [
        ...
    ]
}
```

对于在控制平面上不存在定制的 Table 定义的 API 资源类型而言，服务器会返回一个默认的
Table 响应，其中包含资源的 `name` 和 `creationTimestamp` 字段。

```console
GET /apis/crd.example.com/v1alpha1/namespaces/default/resources
---
200 OK
Content-Type: application/json
...

{
    "kind": "Table",
    "apiVersion": "meta.k8s.io/v1",
    ...
    "columnDefinitions": [
        {
            "name": "Name",
            "type": "string",
            ...
        },
        {
            "name": "Created At",
            "type": "date",
            ...
        }
    ]
}
```

并非所有 API 资源类型都支持 Table 响应；
例如，{{< glossary_tooltip term_id="CustomResourceDefinition" text="CustomResourceDefinitions" >}} 可能没有定义字段到表的映射，
[扩展核心 Kubernetes API](/zh-cn/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)
的 APIService 可能根本不提供 Table 响应。
如果你正在实现使用 Table 信息并且必须针对所有资源类型（包括扩展）工作的客户端，
你应该在 `Accept` 请求头中指定多种内容类型的请求。例如：

```console
Accept: application/json;as=Table;g=meta.k8s.io;v=v1, application/json
```

## 资源的其他表示形式  {#alternate-representations-of-resources}

默认情况下，Kubernetes 返回序列化为 JSON 的对象，内容类型为 `application/json`。
这是 API 的默认序列化格式。
但是，客户端可能会使用更有效的 [Protobuf 表示](#protobuf-encoding) 请求这些对象，
以获得更好的大规模性能。Kubernetes API 实现标准的 HTTP 内容类型协商：
带有 `Accept` 请求头部的 `GET` 调用会请求服务器尝试以你的首选媒体类型返回响应，
而将 Protobuf 中的对象发送到服务器以进行 `PUT` 或 `POST` 调用意味着你必须适当地设置
`Content-Type` 请求头。

如果支持请求的格式，服务器将返回带有 `Content-Type` 标头的响应，
如果不支持你请求的媒体类型，则返回 `406 Not Acceptable` 错误。
所有内置资源类型都支持 `application/json` 媒体类型。

有关每个 API 支持的内容类型列表，请参阅 Kubernetes [API 参考](/zh-cn/docs/reference/kubernetes-api/)。

例如：

1. 以 Protobuf 格式列举集群上的所有 Pod：

   ```console
   GET /api/v1/pods
   Accept: application/vnd.kubernetes.protobuf
   ---
   200 OK
   Content-Type: application/vnd.kubernetes.protobuf

   ... binary encoded PodList object
   ```

2. 通过向服务器发送 Protobuf 编码的数据创建 Pod，但请求以 JSON 形式接收响应：

   ```console
   POST /api/v1/namespaces/test/pods
   Content-Type: application/vnd.kubernetes.protobuf
   Accept: application/json
   ... binary encoded Pod object
   ---
   200 OK
   Content-Type: application/json

   {
     "kind": "Pod",
     "apiVersion": "v1",
     ...
   }
   ```

并非所有 API 资源类型都支持 Protobuf；具体来说，
Protobuf 不适用于定义为 {{< glossary_tooltip term_id="CustomResourceDefinition" text="CustomResourceDefinitions" >}}
或通过{{< glossary_tooltip text="聚合层" term_id="aggregation-layer" >}}提供服务的资源。
作为客户端，如果你可能需要使用扩展类型，则应在请求 `Accept` 请求头中指定多种内容类型以支持回退到 JSON。
例如：

```console
Accept: application/vnd.kubernetes.protobuf, application/json
```

### Kubernetes Protobuf 编码 {#protobuf-encoding}

Kubernetes 使用封套形式来对 Protobuf 响应进行编码。
封套外层由 4 个字节的特殊数字开头，便于从磁盘文件或 etcd 中辩识 Protobuf
格式的（而不是 JSON）数据。
接下来存放的是 Protobuf 编码的封套消息，其中描述下层对象的编码和类型，最后
才是对象本身。

封套格式如下：

```console
四个字节的特殊数字前缀：
  字节 0-3: "k8s\x00" [0x6b, 0x38, 0x73, 0x00]

使用下面 IDL 来编码的 Protobuf 消息：
  message Unknown {
    // typeMeta 应该包含 "kind" 和 "apiVersion" 的字符串值，就像
    // 对应的 JSON 对象中所设置的那样
    optional TypeMeta typeMeta = 1;

    // raw 中将保存用 protobuf 序列化的完整对象。
    // 参阅客户端库中为指定 kind 所作的 protobuf 定义
    optional bytes raw = 2;

    // contentEncoding 用于 raw 数据的编码格式。未设置此值意味着没有特殊编码。
    optional string contentEncoding = 3;

    // contentType 包含 raw 数据所采用的序列化方法。
    // 未设置此值意味着 application/vnd.kubernetes.protobuf，且通常被忽略
    optional string contentType = 4;
  }

  message TypeMeta {
    // apiVersion 是 type 对应的组名/版本
    optional string apiVersion = 1;
    // kind 是对象模式定义的名称。此对象应该存在一个 protobuf 定义。
    optional string kind = 2;
  }
```

{{< note >}}
收到 `application/vnd.kubernetes.protobuf` 格式响应的客户端在响应与预期的前缀不匹配时应该拒绝响应，
因为将来的版本可能需要以某种不兼容的方式更改序列化格式，
并且这种更改是通过变更前缀完成的。
{{< /note >}}

## 资源删除  {#resource-deletion}

当你 **delete** 资源时，操作将分两个阶段进行。

1. 终结（finalization）
2. 移除

```yaml
{
  "kind": "ConfigMap",
  "apiVersion": "v1",
  "metadata": {
    "finalizers": {"url.io/neat-finalization", "other-url.io/my-finalizer"},
    "deletionTimestamp": nil,
  }
}
```

当客户端第一次发送 **delete** 请求删除资源时，`.metadata.deletionTimestamp` 设置为当前时间。
一旦设置了 `.metadata.deletionTimestamp`，
作用于终结器的外部控制器可以在任何时间以任何顺序开始执行它们的清理工作。

终结器之间 **不存在** 强制的执行顺序，因为这会带来卡住 `.metadata.finalizers` 的重大风险。

`.metadata.finalizers` 字段是共享的：任何有权限的参与者都可以重新排序。
如果终结器列表是按顺序处理的，那么这可能会导致这样一种情况：
在列表中负责第一个终结器的组件正在等待列表中稍后负责终结器的组件产生的某些信号
（字段值、外部系统或其他），从而导致死锁。

如果没有强制排序，终结者可以在它们之间自由排序，并且不易受到列表中排序变化的影响。

当最后一个终结器也被移除时，资源才真正从 etcd 中移除。

## 单个资源 API  {#single-resource-api}

Kubernetes API 动词 **get**、**create**、**apply**、**update**、**patch**、**delete** 和 **proxy** 仅支持单一资源。
这些具有单一资源支持的动词不支持在有序或无序列表或事务中一起提交多个资源。

当客户端（包括 kubectl）对一组资源进行操作时，客户端会发出一系列单资源 API 请求，
然后在需要时聚合响应。

相比之下，Kubernetes API 动词 **list** 和 **watch** 允许获取多个资源，
而 **deletecollection** 允许删除多个资源。

## 字段校验    {#field-validation}

Kubernetes 总是校验字段的类型。例如，如果 API 中的某个字段被定义为数值，
你就不能将该字段设置为文本类型的值。如果某个字段被定义为字符串数组，你只能提供数组。
有些字段可以忽略，有些字段必须填写。忽略 API 请求中的必填字段会报错。

如果请求中带有集群控制面无法识别的额外字段，API 服务器的行为会更加复杂。

默认情况下，如果接收到的输入信息中含有 API 服务器无法识别的字段，API 服务器会丢弃该字段
（例如： `PUT` 请求中的 JSON 主体）。

API 服务器会在两种情况下丢弃 HTTP 请求中提供的字段。

这些情况是：

1. 相关资源的 OpenAPI 模式定义中没有该字段，因此无法识别该字段（有种例外情形是，
   {{< glossary_tooltip term_id="CustomResourceDefinition" text="CRD" >}}
   通过 `x-kubernetes-preserve-unknown-fields` 显式选择不删除未知字段）。

2. 字段在对象中重复出现。

### 检查无法识别或重复的字段  {#setting-the-field-validation-level}

  {{< feature-state for_k8s_version="v1.27" state="stable" >}}

从 1.25 开始，当使用可以提交数据的 HTTP 动词（`POST`、`PUT` 和 `PATCH`）时，
将通过服务器上的校验检测到对象中无法识别或重复的字段。
校验的级别可以是 `Ignore`、`Warn`（默认值） 和 `Strict` 之一。
`Ignore`
: 使 API 服务器像没有遇到错误字段一样成功处理请求，丢弃所有的未知字段和重复字段，并且不发送丢弃字段的通知。

`Warn`
:（默认值）使 API 服务器成功处理请求，并向客户端发送告警信息。告警信息通过 `Warning:` 响应头发送，
并为每个未知字段或重复字段添加一条告警信息。有关告警和相关的 Kubernetes API 的信息，
可参阅博文[告警：增加实用告警功能](/blog/2020/09/03/warnings/)。

`Strict`
: API 服务器检测到任何未知字段或重复字段时，拒绝处理请求并返回 400 Bad Request 错误。
来自 API 服务器的响应消息列出了 API 检测到的所有未知字段或重复字段。

字段校验级别可通过查询参数 `fieldValidation` 来设置。

{{< note >}}
如果你提交的请求中设置了一个无法被识别的字段，并且该请求存在因其他原因引起的不合法
（例如，请求为某已知字段提供了一个字符串值，而 API 期望该字段为整数），
那么 API 服务器会以 400 Bad Request 错误作出响应，但不会提供有关未知或重复字段的任何信息
（仅提供它首先遇到的致命错误）。

在这种情况下，不管你设置哪种字段校验级别，你总会收到出错响应。
{{< /note >}}

向服务器提交请求的工具（例如 `kubectl`）可能会设置自己的默认值，与 API 服务器默认使用的 `Warn`
校验层级不同。

`kubectl` 工具使用 `--validate` 标志设置字段校验层级。
该字段可取的值包括 `ignore`、`warn` 和 `strict`，同时还接受值 `true`（相当于 `strict`）和
`false`（相当于 `ignore`）。
kubectl 默认的校验设置是 `--validate=true` ，这意味着执行严格的服务端字段校验。

当 kubectl 无法连接到启用字段校验的 API 服务器（Kubernetes 1.27 之前的 API 服务器）时，
将回退到使用客户端的字段校验。
客户端校验将在 kubectl 未来版本中被完全删除。
{{< note >}}
在 Kubernetes 1.25 之前，`kubectl --validate` 是用来开启或关闭客户端校验的布尔标志的命令。
{{< /note >}}

## 试运行  {#dry-run}

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

当你使用可以修改资源的 HTTP 动词（`POST`、`PUT`、`PATCH` 和 `DELETE`）时，
你可以在 **试运行（dry run）** 模式下提交你的请求。
试运行模式有助于通过典型的请求阶段（准入链、验证、合并冲突）评估请求，直到将对象持久化到存储中。
请求的响应正文尽可能接近非试运行响应。Kubernetes 保证试运行请求不会被持久化存储或产生任何其他副作用。

### 发起试运行请求  {#make-a-dry-run-request}

通过设置 `dryRun` 查询参数触发试运行。此参数是一个字符串，用作枚举，唯一可接受的值是：

[未设置值]
: 允许副作用。你可以使用 `?dryRun` 或 `?dryRun&pretty=true` 之类的查询字符串请求此操作。
  响应是最终会被持久化的对象，或者如果请求不能被满足则会出现一个错误。

`All`
: 每个阶段都正常运行，除了防止副作用的最终存储阶段。

当你设置 `?dryRun=All` 时，将运行任何相关的{{< glossary_tooltip text="准入控制器" term_id="admission-controller" >}}，
验证准入控制器检查经过变更的请求，针对 `PATCH` 请求执行合并、设置字段默认值等操作，并进行模式验证。
更改不会持久化到底层存储，但本应持久化的最终对象仍会与正常状态代码一起返回给用户。

如果请求的非试运行版本会触发具有副作用的准入控制器，则该请求将失败，而不是冒不希望的副作用的风险。
所有内置准入控制插件都支持试运行。
此外，准入 Webhook 还可以设置[配置对象](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#validatingwebhook-v1-admissionregistration-k8s-io)
的 `sideEffects` 字段为 `None`，借此声明它们没有副作用。

{{< note >}}
如果 webhook 确实有副作用，则应该将 `sideEffects` 字段设置为 “NoneOnDryRun”。
如果还修改了 webhook 以理解 AdmissionReview 中的 DryRun 字段，
并防止对标记为试运行的任何请求产生副作用，则该更改是适当的。
{{< /note >}}

这是一个使用 `?dryRun=All` 的试运行请求的示例：

```console
POST /api/v1/namespaces/test/pods?dryRun=All
Content-Type: application/json
Accept: application/json
```


响应会与非试运行模式请求的响应看起来相同，只是某些生成字段的值可能会不同。

### 生成值  {#generated-values}

对象的某些值通常是在对象被写入数据库之前生成的。很重要的一点是不要依赖试运行请求为这些字段所设置的值，
因为试运行模式下所得到的这些值与真实请求所获得的值很可能不同。这类字段有：

* `name`：如果设置了 `generateName` 字段，则 `name` 会获得一个唯一的随机名称
* `creationTimestamp` / `deletionTimestamp`：记录对象的创建/删除时间
* `UID`：[唯一标识](/zh-cn/docs/concepts/overview/working-with-objects/names/#uids)对象，
  取值随机生成（非确定性）
* `resourceVersion`：跟踪对象的持久化（存储）版本
* 变更性准入控制器所设置的字段
* 对于 `Service` 资源：`kube-apiserver` 为 `Service` 对象分配的端口和 IP 地址

### 试运行的授权    {#dry-run-authorization}

试运行和非试运行请求的鉴权是完全相同的。因此，要发起一个试运行请求，
你必须被授权执行非试运行请求。

例如，要在 Deployment 对象上试运行 **patch** 操作，你必须具有对 Deployment 执行 **patch** 操作的访问权限，
如下面的 {{< glossary_tooltip text="RBAC" term_id="rbac">}} 规则所示：

```yaml
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["patch"]
```

参阅[鉴权概述](/zh-cn/docs/reference/access-authn-authz/authorization/)以了解鉴权细节。

## 服务器端应用  {#server-side-apply}

Kubernetes 的[服务器端应用](/zh-cn/docs/reference/using-api/server-side-apply/)功能允许控制平面跟踪新创建对象的托管字段。
服务端应用为管理字段冲突提供了清晰的模式，提供了服务器端 `Apply` 和 `Update` 操作，
并替换了 `kubectl apply` 的客户端功能。

服务端应用的 API 动词是 **apply**。有关详细信息，
请参阅[服务器端应用](/zh-cn/docs/reference/using-api/server-side-apply/)。

## 资源版本   {#resource-versions}

资源版本是标识服务器内部对象版本的字符串。
客户端可以使用资源版本来确定对象何时更改，
或者在获取、列出和监视资源时表达数据一致性要求。
资源版本必须被客户端视为不透明的，并且未经修改地传回服务器。

你不能假设资源版本是数字的或可排序的。
API 客户端只能比较两个资源版本的相等性（这意味着你不能比较资源版本的大于或小于关系）。

### metadata 中的 `resourceVersion`  {#resourceVersion-in-metadata}

客户端在资源中查找资源版本，这些资源包括来自用于 **watch** 的响应流资源，或者使用 **list** 枚举的资源。

[v1.meta/ObjectMeta](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#objectmeta-v1-meta) -
资源的 `metadata.resourceVersion` 值标明该实例上次被更改时的资源版本。

[v1.meta/ListMeta](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#listmeta-v1-meta) - 资源集合即
**list** 操作的响应）的 `metadata.resourceVersion` 所标明的是 list 响应被构造时的资源版本。

### 查询字符串中的 `resourceVersion` 参数   {#the-resourceversion-parameter}

**get**、**list** 和 **watch** 操作支持 `resourceVersion` 参数。
从 v1.19 版本开始，Kubernetes API 服务器支持 **list** 请求的 `resourceVersionMatch` 参数。

API 服务器根据你请求的操作和 `resourceVersion` 的值对 `resourceVersion` 参数进行不同的解释。
如果你设置 `resourceVersionMatch` 那么这也会影响匹配发生的方式。


### **get** 和 **list** 语义   {#semantics-for-get-and-list}

对于 **get** 和 **list** 而言，`resourceVersion` 的语义为：

**get:**

| resourceVersion 未设置 | resourceVersion="0" | resourceVersion="\<非零值\>" |
|-----------------------|---------------------|----------------------------------------|
| 最新版本               | 任何版本            | 不老于给定版本                         |

**list:**

从 v1.19 版本开始，Kubernetes API 服务器支持 **list** 请求的 `resourceVersionMatch` 参数。
如果同时设置 `resourceVersion` 和 `resourceVersionMatch`，
则 `resourceVersionMatch` 参数确定 API 服务器如何解释 `resourceVersion`。

在 **list** 请求上设置 `resourceVersion` 时，你应该始终设置 `resourceVersionMatch` 参数。
但是，请准备好处理响应的 API 服务器不知道 `resourceVersionMatch` 并忽略它的情况。

除非你对一致性有着非常强烈的需求，使用 `resourceVersionMatch=NotOlderThan`
同时为 `resourceVersion` 设定一个已知值是优选的交互方式，因为与不设置
`resourceVersion` 和 `resourceVersionMatch` 相比，这种配置可以取得更好的集群性能和可扩缩性。
后者需要提供带票选能力的读操作。

设置 `resourceVersionMatch` 参数而不设置 `resourceVersion` 参数是不合法的。

下表解释了具有各种 `resourceVersion` 和 `resourceVersionMatch` 组合的 **list** 请求的行为：

{{< table caption="list 操作的 resourceVersionMatch 与分页参数" >}}

| resourceVersionMatch 参数               | 分页参数                        | resourceVersion 未设置  | resourceVersion="0"                     | resourceVersion="\<非零值\>"     |
|-----------------------------------------|---------------------------------|-------------------------|-----------------------------------------|----------------------------------|
| **未设置**            | **limit 未设置**                      | 最新版本                | 任意版本                                | 不老于指定版本                   |
| **未设置**            | limit=\<n\>, **continue 未设置**        | 最新版本                | 任意版本                                | 精确匹配                         |
| **未设置**           | limit=\<n\>, continue=\<token\>     | 从 token 开始、精确匹配 | 非法请求，视为从 token 开始、精确匹配  | 非法请求，返回 HTTP `400 Bad Request` |
| `resourceVersionMatch=Exact` [1]         | **limit 未设置**                      | 非法请求                | 非法请求                                | 精确匹配                         |
| `resourceVersionMatch=Exact` [1]         | limit=\<n\>, **continue 未设置**        | 非法请求                | 非法请求                                | 精确匹配                         |
| `resourceVersionMatch=NotOlderThan` [1]  | **limit 未设置**             | 非法请求                | 任意版本                                | 不老于指定版本                   |
| `resourceVersionMatch=NotOlderThan` [1]  | limit=\<n\>, **continue 未设置** | 非法请求                | 任意版本                                | 不老于指定版本                   |

{{< /table >}}

{{< note >}}
如果你的集群的 API 服务器不支持 `resourceVersionMatch` 参数，
则行为与你未设置它时相同。
{{< /note >}}

**get** 和 **list** 的语义是：

任意版本
: 返回任何资源版本的数据。最新可用资源版本优先，但不需要强一致性；
  可以提供任何资源版本的数据。由于分区或过时的缓存，
  请求可能返回客户端先前观察到的更旧资源版本的数据，特别是在高可用性配置中。
  不能容忍这种情况的客户不应该使用这种语义。

最新版本
: 返回最新资源版本的数据。
  返回的数据必须一致（详细说明：通过仲裁读取从 etcd 提供）。



不老于指定版本
: 返回数据至少与提供的 `resourceVersion` 一样新。
  最新的可用数据是首选，但可以提供不早于提供的 `resourceVersion` 的任何数据。
  对于对遵守 `resourceVersionMatch` 参数的服务器的 **list** 请求，
  这保证了集合的 `.metadata.resourceVersion` 不早于请求的 `resourceVersion`，
  但不保证该集合中任何项目的 `.metadata.resourceVersion`。


精确匹配
: 以提供的确切资源版本返回数据。如果提供的 `resourceVersion` 不可用，
  则服务器以 HTTP 410 “Gone”响应。对于对支持 `resourceVersionMatch` 参数的服务器的 **list** 请求，
  这可以保证集合的 `.metadata.resourceVersion` 与你在查询字符串中请求的 `resourceVersion` 相同。
  该保证不适用于该集合中任何项目的 `.metadata.resourceVersion`。

从 token 开始、精确匹配
: 返回初始分页 **list** 调用的资源版本的数据。
  返回的 _Continue 令牌_ 负责跟踪最初提供的资源版本，最初提供的资源版本用于在初始分页 **list** 之后的所有分页 **list** 中。


{{< note >}}
当你 **list** 资源并收到集合响应时，
响应包括集合的[列表元数据](/docs/reference/generated/kubernetes-api/v{{<skew currentVersion >}}/#listmeta-v1-meta)。
以及该集合中每个项目的[对象元数据](/docs/reference/generated/kubernetes-api/v{{<skew currentVersion >}}/#objectmeta-v1-meta)。
对于在集合响应中找到的单个对象，`.metadata.resourceVersion` 跟踪该对象的最后更新时间，
而不是对象在服务时的最新程度。
{{< /note >}}


当使用 `resourceVersionMatch=NotOlderThan` 并设置了限制时，
客户端必须处理 HTTP 410 “Gone” 响应。
例如，客户端可能会使用更新的 `resourceVersion` 重试或回退到 `resourceVersion=""`。

当使用 `resourceVersionMatch=Exact` 并且未设置限制时，
客户端必须验证集合的 `.metadata.resourceVersion` 是否与请求的 `resourceVersion` 匹配，
并处理不匹配的情况。例如，客户端可能会退回到设置了限制的请求。

### **watch** 语义   {#semantics-for-watch}

对于 **watch** 操作而言，资源版本的语义如下：

**watch：**


{{< table caption="watch 操作的 resourceVersion 设置" >}}

| resourceVersion 未设置    | resourceVersion="0"      | resourceVersion="\<非零值\>" |
|---------------------------|--------------------------|------------------------------|
| 读取状态并从最新版本开始  | 读取状态并从任意版本开始 | 从指定版本开始               |

{{< /table >}}

**watch** 操作语义的含义如下：

读取状态并从任意版本开始
: {{< caution >}}
  以这种方式初始化的监视可能会返回任意陈旧的数据。
  请在使用之前查看此语义，并尽可能支持其他语义。
  {{< /caution >}}
  在任何资源版本开始 **watch**；首选可用的最新资源版本，但不是必需的。允许任何起始资源版本。
  由于分区或过时的缓存，**watch** 可能从客户端之前观察到的更旧的资源版本开始，
  特别是在高可用性配置中。不能容忍这种明显倒带的客户不应该用这种语义启动 **watch**。
  为了建立初始状态，**watch** 从起始资源版本中存在的所有资源实例的合成 “添加” 事件开始。
  以下所有监视事件都针对在 **watch** 开始的资源版本之后发生的所有更改。

读取状态并从最新版本开始
: 从最近的资源版本开始 **watch**，
  它必须是一致的（详细说明：通过仲裁读取从 etcd 提供服务）。
  为了建立初始状态，**watch** 从起始资源版本中存在的所有资源实例的合成 “添加” 事件开始。
  以下所有监视事件都针对在 **watch** 开始的资源版本之后发生的所有更改。

从指定版本开始
: 以确切的资源版本开始 **watch**。监视事件适用于提供的资源版本之后的所有更改。
  与 “Get State and Start at Most Recent” 和 “Get State and Start at Any” 不同，
  **watch** 不会以所提供资源版本的合成 “添加” 事件启动。
  由于客户端提供了资源版本，因此假定客户端已经具有起始资源版本的初始状态。

### "410 Gone" 响应     {#410-gone-responses}

服务器不需要提供所有老的资源版本，在客户端请求的是早于服务器端所保留版本的
`resourceVersion` 时，可以返回 HTTP `410 (Gone)` 状态码。
客户端必须能够容忍 `410 (Gone)` 响应。
参阅[高效检测变更](#efficient-detection-of-changes)以了解如何在监测资源时处理
`410 (Gone)` 响应。

如果所请求的 `resourceVersion` 超出了可应用的 `limit`，
那么取决于请求是否是通过高速缓存来满足的，API 服务器可能会返回一个 `410 Gone` HTTP 响应。

### 不可用的资源版本  {#unavailable-resource-versions}

服务器不需要提供无法识别的资源版本。
如果你请求了 **list** 或 **get** API 服务器无法识别的资源版本，则 API 服务器可能会：

* 短暂等待资源版本可用，如果提供的资源版本在合理的时间内仍不可用，
  则应超时并返回 `504 (Gateway Timeout)`；
* 使用 `Retry-After` 响应标头进行响应，指示客户端在重试请求之前应等待多少秒。

如果你请求 API 服务器无法识别的资源版本，
kube-apiserver 还会使用 “Too large resource version” 消息额外标识其错误响应。

如果你对无法识别的资源版本发出 **watch** 请求，
API 服务器可能会无限期地等待（直到请求超时）资源版本变为可用。
