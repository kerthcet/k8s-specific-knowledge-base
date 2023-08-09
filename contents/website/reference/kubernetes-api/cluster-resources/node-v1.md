---
api_metadata:
  apiVersion: "v1"
  import: "k8s.io/api/core/v1"
  kind: "Node"
content_type: "api_reference"
description: "Node 是 Kubernetes 中的工作节点。"
title: "Node"
weight: 1
---

`apiVersion: v1`

`import "k8s.io/api/core/v1"`

## Node {#Node}

Node 是 Kubernetes 中的工作节点。
每个节点在缓存中（即在 etcd 中）都有一个唯一的标识符。

<hr>

- **apiVersion**: v1

- **kind**: Node

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../cluster-resources/node-v1#NodeSpec" >}}">NodeSpec</a>)

  spec 定义节点的行为。
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

- **status** (<a href="{{< ref "../cluster-resources/node-v1#NodeStatus" >}}">NodeStatus</a>)

  此节点的最近观测状态。由系统填充。只读。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

## NodeSpec {#NodeSpec}

NodeSpec 描述了创建节点时使用的属性。

<hr>

- **configSource** (NodeConfigSource)

  已弃用：以前用于为 DynamicKubeletConfig 功能指定节点配置的来源。此功能已删除。

  <a name="NodeConfigSource"></a>
  **NodeConfigSource 指定节点配置的来源。指定一个子字段（不包括元数据）必须为非空。此 API 自 1.22的版本起已被弃用**

  - **configSource.configMap** (ConfigMapNodeConfigSource)


    configMap 是对 Node 的 ConfigMap 的引用。

    <a name="ConfigMapNodeConfigSource"></a>

    ConfigMapNodeConfigSource 包含引用某 ConfigMap 作为节点配置源的信息。
    此 API 自 1.22 版本起已被弃用： https://git.k8s.io/enhancements/keps/sig-node/281-dynamic-kubelet-configuration


    - **configSource.configMap.kubeletConfigKey** (string), 必需

      kubeletConfigKey 声明所引用的 ConfigMap 的哪个键对应于 KubeletConfiguration 结构体，
      该字段在所有情况下都是必需的。


    - **configSource.configMap.name** (string), 必需

      name 是被引用的 ConfigMap 的 metadata.name。
      此字段在所有情况下都是必需的。


    - **configSource.configMap.namespace** (string), 必需

      namespace 是所引用的 ConfigMap 的 metadata.namespace。
      此字段在所有情况下都是必需的。

    - **configSource.configMap.resourceVersion** (string)


      resourceVersion 是所引用的 ConfigMap 的 metadata.resourceVersion。
      该字段在 Node.spec 中是禁止的，在 Node.status 中是必需的。

    - **configSource.configMap.uid** (string)


      uid 是所引用的 ConfigMap 的 metadata.uid。
      该字段在 Node.spec 中是禁止的，在 Node.status 中是必需的。

- **externalID** (string)

  已弃用。并非所有 kubelet 都会设置此字段。
  1.13 的版本之后会删除该字段。参见： https://issues.k8s.io/61966

- **podCIDR** (string)

  podCIDR 表示分配给节点的 Pod IP 范围。

- **podCIDRs** ([]string)

  podCIDRs 表示分配给节点以供该节点上的 Pod 使用的 IP 范围。
  如果指定了该字段，则第 0 个条目必须与 podCIDR 字段匹配。
  对于 IPv4 和 IPv6，它最多可以包含 1 个值。

- **providerID** (string)

  云提供商分配的节点ID，格式为：\<ProviderName>://\<ProviderSpecificNodeID>

- **taints** ([]Taint)

  如果设置了，则为节点的污点。

  <a name="Taint"></a>
  **此污点附加到的节点对任何不容忍污点的 Pod 都有 “影响”。**


  - **taints.effect** (string), 必需

    必需的。污点对不容忍污点的 Pod 的影响。合法的 effect 值有 NoSchedule、PreferNoSchedule 和 NoExecute。


  - **taints.key** (string), 必需

    必需的。被应用到节点上的污点的键。

  - **taints.timeAdded** (Time)


    timeAdded 表示添加污点的时间。它仅适用于 NoExecute 的污点。

    <a name="Time"></a>

    **Time 是 time.Time 的包装器，它支持对 YAML 和 JSON 的正确编组。
    time 包的许多工厂方法提供了包装器。**

  - **taints.value** (string)


    与污点键对应的污点值。

- **unschedulable** (boolean)


  unschedulable 控制新 Pod 的节点可调度性。
  默认情况下，节点是可调度的。
  更多信息： https://kubernetes.io/zh-cn/docs/concepts/architecture/nodes/#manual-node-administration

## NodeStatus {#NodeStatus}

NodeStatus 是有关节点当前状态的信息。

<hr>

- **addresses** ([]NodeAddress)

  **补丁策略：根据 `type` 键执行合并操作**

  节点可到达的地址列表。从云提供商处查询（如果有）。
  更多信息： https://kubernetes.io/zh-cn/docs/concepts/architecture/nodes/#addresses
  
  注意：该字段声明为可合并，但合并键不够唯一，合并时可能导致数据损坏。
  调用者应改为使用完全替换性质的补丁操作。
  有关示例，请参见 https://pr.k8s.io/79391。

  消费者应假设地址可以在节点的生命期内发生变化。
  然而在一些例外情况下这是不可能的，例如在自身状态中继承 Node 地址的 Pod
  或 downward API (status.hostIP) 的消费者。

  <a name="NodeAddress"></a>
  **NodeAddress 包含节点地址的信息。**


  - **addresses.address** (string), 必需

    节点地址。


  - **addresses.type** (string), 必需

    节点地址类型，Hostname、ExternalIP 或 InternalIP 之一。
   
- **allocatable** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

  allocatable 表示节点的可用于调度的资源。默认为容量。

- **capacity** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

  capacity 代表一个节点的总资源。
  更多信息： https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes/#capacity

- **conditions** ([]NodeCondition)

  **补丁策略：根据 `type` 键执行合并操作**

  conditions 是当前观测到的节点状况的数组。
  更多信息： https://kubernetes.io/zh-cn/docs/concepts/architecture/nodes/#condition

  <a name="NodeCondition"></a>
  **NodeCondition 包含节点状况的信息。**


  - **conditions.status** (string), 必需

    状况的状态为 True、False、Unknown 之一。
  

  - **conditions.type** (string), 必需

    节点状况的类型。

  - **conditions.lastHeartbeatTime** (Time)


    给定状况最近一次更新的时间。

    <a name="Time"></a>

    Time 是 time.Time 的包装器，它支持对 YAML 和 JSON 的正确编组。
    time 包的许多工厂方法提供了包装器。

  - **conditions.lastTransitionTime** (Time)


    状况最近一次从一种状态转换到另一种状态的时间。

    <a name="Time"></a>

    Time 是 time.Time 的包装器，它支持对 YAML 和 JSON 的正确编组。
    time 包的许多工厂方法提供了包装器。

  - **conditions.message** (string)


    指示有关上次转换详细信息的人类可读消息。

  - **conditions.reason** (string)


    （简要）状况最后一次转换的原因。

- **config** (NodeConfigStatus)

  通过动态 Kubelet 配置功能分配给节点的配置状态。

  <a name="NodeConfigStatus"></a>
  **NodeConfigStatus 描述了由 Node.spec.configSource 分配的配置的状态。**

  - **config.active** (NodeConfigSource)


    active 报告节点正在使用的检查点配置。
    active 将代表已分配配置的当前版本或当前 LastKnownGood 配置，具体取决于尝试使用已分配配置是否会导致错误。

    <a name="NodeConfigSource"></a>

    **NodeConfigSource 指定节点配置的来源。指定一个子字段（不包括元数据）必须为非空。此 API 自 1.22 版本起已弃用**

    - **config.active.configMap** (ConfigMapNodeConfigSource)


      configMap 是对 Node 的 ConfigMap 的引用。

      <a name="ConfigMapNodeConfigSource"></a>

      ConfigMapNodeConfigSource 包含引用某 ConfigMap 作为节点配置源的信息。
      此 API 自 1.22 版本起已被弃用： https://git.k8s.io/enhancements/keps/sig-node/281-dynamic-kubelet-configuration


      - **config.active.configMap.kubeletConfigKey** (string), 必需

        kubeletConfigKey 声明所引用的 ConfigMap 的哪个键对应于 KubeletConfiguration 结构体，
        该字段在所有情况下都是必需的。


      - **config.active.configMap.name** (string), 必需

        name 是所引用的 ConfigMap 的 metadata.name。
        此字段在所有情况下都是必需的。


      - **config.active.configMap.namespace** (string), 必需

        namespace 是所引用的 ConfigMap 的 metadata.namespace。
        此字段在所有情况下都是必需的。

      - **config.active.configMap.resourceVersion** (string)


        resourceVersion 是所引用的 ConfigMap 的 metadata.resourceVersion。
        该字段在 Node.spec 中是禁止的，在 Node.status 中是必需的。

      - **config.active.configMap.uid** (string)


        uid 是所引用的 ConfigMap 的 metadata.uid。
        该字段在 Node.spec 中是禁止的，在 Node.status 中是必需的。

  - **config.assigned** (NodeConfigSource)


    assigned 字段报告节点将尝试使用的检查点配置。
    当 Node.spec.configSource 被更新时，节点将所关联的配置负载及指示预期配置的记录通过检查点操作加载到本地磁盘。
    节点参考这条记录来选择它的配置检查点，并在 assigned 中报告这条记录。
    仅在记录被保存到磁盘后才会更新 status 中的 assigned。
    当 kubelet 重新启动时，它会尝试通过加载和验证由 assigned 标识的检查点有效负载来使 assigned 配置成为 active 配置。

    <a name="NodeConfigSource"></a>

    **NodeConfigSource 指定节点配置的来源。指定一个子字段（不包括元数据）必须为非空。此 API 自 1.22 版本起已弃用**

    - **config.assigned.configMap** (ConfigMapNodeConfigSource)


      configMap 是对 Node 的 ConfigMap 的引用。

      <a name="ConfigMapNodeConfigSource"></a>

      ConfigMapNodeConfigSource 包含引用某 ConfigMap 为节点配置源的信息。
      此 API 自 1.22 版本起已被弃用： https://git.k8s.io/enhancements/keps/sig-node/281-dynamic-kubelet-configuration


      - **config.assigned.configMap.kubeletConfigKey** (string), 必需

        kubeletConfigKey 声明所引用的 ConfigMap 的哪个键对应于 KubeletConfiguration 结构体，
        该字段在所有情况下都是必需的。


      - **config.assigned.configMap.name** (string), 必需

        name 是所引用的 ConfigMap 的 metadata.name。
        此字段在所有情况下都是必需的。


      - **config.assigned.configMap.namespace** (string), 必需

        namespace 是所引用的 ConfigMap 的 metadata.namespace。
        此字段在所有情况下都是必需的。

      - **config.assigned.configMap.resourceVersion** (string)


        resourceVersion 是所引用的 ConfigMap 的 metadata.resourceVersion。
        该字段在 Node.spec 中是禁止的，在 Node.status 中是必需的。

      - **config.assigned.configMap.uid** (string)


        uid 是所引用的 ConfigMap 的 metadata.uid。
        该字段在 Node.spec 中是禁止的，在 Node.status 中是必需的。

  - **config.error** (string)


    error 描述了在 spec.configSource 与活动配置间协调时发生的所有问题。
    可能会发生的情况，例如，尝试将 spec.configSource 通过检查点操作复制到到本地 assigned 记录时，
    尝试对与 spec.configSource 关联的有效负载执行检查点操作，尝试加​​载或验证 assigned 的配置时。
    同步配置时可能会在不同位置发生错误，较早的错误（例如下载或检查点错误）不会导致回滚到 LastKnownGood，
    并且可能会在 Kubelet 重试后解决。
    后期发生的错误（例如加载或验证检查点配置）将导致回滚到 LastKnownGood。
    在后一种情况下，通常可以通过修复 spec.sonfigSource 中 assigned 配置来解决错误。
    你可以通过在 Kubelet 日志中搜索错误消息来找到更多的调试信息。
    error 是错误状态的人类可读描述；机器可以检查 error 是否为空，但不应依赖跨 Kubelet 版本的 error 文本的稳定性。

  - **config.lastKnownGood** (NodeConfigSource)
    

    lastKnownGood 报告节点在尝试使用 assigned 配置时遇到错误时将回退到的检查点配置。
    当节点确定 assigned 配置稳定且正确时，assigned 配置会成为 lastKnownGood 配置。
    这当前实施为从更新分配配置的本地记录开始的 10 分钟浸泡期。
    如果在此期间结束时分配的配置依旧处于活动状态，则它将成为 lastKnownGood。
    请注意，如果 spec.configSource 重置为 nil（使用本地默认值），
    LastKnownGood 也会立即重置为 nil，因为始终假定本地默认配置是好的。
    你不应该对节点确定配置稳定性和正确性的方法做出假设，因为这可能会在将来发生变化或变得可配置。

    <a name="NodeConfigSource"></a>

    **NodeConfigSource 指定节点配置的来源。指定一个子字段（不包括元数据）必须为非空。此 API 自 1.22 版本起已弃用**

    - **config.lastKnownGood.configMap** (ConfigMapNodeConfigSource)


      configMap 是对 Node 的 ConfigMap 的引用。

      <a name="ConfigMapNodeConfigSource"></a>

      ConfigMapNodeConfigSource 包含引用某 ConfigMap 作为节点配置源的信息。
      此 API 自 1.22 版本起已被弃用： https://git.k8s.io/enhancements/keps/sig-node/281-dynamic-kubelet-configuration

      - **config.lastKnownGood.configMap.kubeletConfigKey** (string), 必需

        kubeletConfigKey 声明所引用的 ConfigMap 的哪个键对应于 KubeletConfiguration 结构体，
        该字段在所有情况下都是必需的。


      - **config.lastKnownGood.configMap.name** (string), 必需

        name 是所引用的 ConfigMap 的 metadata.name。
        此字段在所有情况下都是必需的。


      - **config.lastKnownGood.configMap.namespace** (string), 必需

        namespace 是所引用的 ConfigMap 的 metadata.namespace。
        此字段在所有情况下都是必需的。

      - **config.lastKnownGood.configMap.resourceVersion** (string)


        resourceVersion 是所引用的 ConfigMap 的 metadata.resourceVersion。
        该字段在 Node.spec 中是禁止的，在 Node.status 中是必需的。

      - **config.lastKnownGood.configMap.uid** (string)


        uid 是所引用的 ConfigMap 的 metadata.uid。
        该字段在 Node.spec 中是禁止的，在 Node.status 中是必需的。

- **daemonEndpoints** (NodeDaemonEndpoints)

  在节点上运行的守护进程的端点。

  <a name="NodeDaemonEndpoints"></a>
  **NodeDaemonEndpoints 列出了节点上运行的守护进程打开的端口。**

  - **daemonEndpoints.kubeletEndpoint** (DaemonEndpoint)


    Kubelet 正在侦听的端点。

    <a name="DaemonEndpoint"></a>

    **DaemonEndpoint 包含有关单个 Daemon 端点的信息。**


    - **daemonEndpoints.kubeletEndpoint.Port** (int32), 必需

      给定端点的端口号。

- **images** ([]ContainerImage)

  该节点上的容器镜像列表。

  <a name="ContainerImage"></a>
  **描述一个容器镜像**

  - **images.names** ([]string)


    已知此镜像的名称。
    例如 ["kubernetes.example/hyperkube:v1.0.7", "cloud-vendor.registry.example/cloud-vendor/hyperkube:v1.0.7"]

  - **images.sizeBytes** (int64)


    镜像的大小（以字节为单位）。

- **nodeInfo** (NodeSystemInfo)

  用于唯一标识节点的 ids/uuids 集。
  更多信息： https://kubernetes.io/zh-cn/docs/concepts/architecture/nodes/#info

  <a name="NodeSystemInfo"></a>
  **NodeSystemInfo 是一组用于唯一标识节点的 ids/uuids。**


  - **nodeInfo.architecture** (string), 必需

    节点报告的 architecture。


  - **nodeInfo.bootID** (string), 必需

    节点报告的 bootID。


  - **nodeInfo.containerRuntimeVersion** (string), 必需

    节点通过运行时远程 API 报告的 ContainerRuntime 版本（例如 containerd://1.4.2）。


  - **nodeInfo.kernelVersion** (string), 必需

    节点来自 “uname -r” 报告的内核版本（例如 3.16.0-0.bpo.4-amd64）。


  - **nodeInfo.kubeProxyVersion** (string), 必需

    节点报告的 KubeProxy 版本。


  - **nodeInfo.kubeletVersion** (string), 必需

    节点报告的 Kubelet 版本。


  - **nodeInfo.machineID** (string), 必需

    节点上报的 machineID。
    对于集群中的唯一机器标识，此字段是首选。
    从 man(5) machine-id 了解更多信息： http://man7.org/linux/man-pages/man5/machine-id.5.html


  - **nodeInfo.operatingSystem** (string), 必需

    节点上报的操作系统。


  - **nodeInfo.osImage** (string), 必需

    节点从 /etc/os-release 报告的操作系统映像（例如 Debian GNU/Linux 7 (wheezy)）。


  - **nodeInfo.systemUUID** (string), 必需

    节点报告的 systemUUID。
    对于唯一的机器标识 MachineID 是首选。
    此字段特定于 Red Hat 主机 https://access.redhat.com/documentation/en-us/red_hat_subscription_management/1/html/rhsm/uuid

- **phase** (string)

  NodePhase 是最近观测到的节点的生命周期阶段。
  更多信息： https://kubernetes.io/zh-cn/docs/concepts/architecture/nodes/#phase
  
  该字段从未填充，现在已被弃用。

- **volumesAttached** ([]AttachedVolume)

  附加到节点的卷的列表。

  <a name="AttachedVolume"></a>
  **AttachedVolume 描述附加到节点的卷**


   - **volumesAttached.devicePath** (string), 必需

     devicePath 表示卷应该可用的设备路径。


  - **volumesAttached.name** (string), 必需

    附加卷的名称。

- **volumesInUse** ([]string)

  节点正在使用（安装）的可附加卷的列表。

## NodeList {#NodeList}

NodeList 是已注册到 master 的所有节点的完整列表。

<hr>

- **apiVersion**: v1

- **kind**: NodeList

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  标准的列表元数据。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **items** ([]<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>), 必需

  节点的列表。

## 操作 {#Operations}

<hr>

### `get` 读取指定节点

#### HTTP 请求

GET /api/v1/nodes/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  节点的名称。

- **pretty** (**路径参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

401: Unauthorized

### `get` 读取指定节点的状态

#### HTTP 请求

GET /api/v1/nodes/{name}/status

#### 参数

- **name** (**路径参数**): string, 必需

  节点的名称。

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

401: Unauthorized

### `list` 列出或监视节点类型的对象

#### HTTP 请求

GET /api/v1/nodes

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

200 (<a href="{{< ref "../cluster-resources/node-v1#NodeList" >}}">NodeList</a>): OK

401: Unauthorized

### `create` 创建一个节点

#### HTTP 请求

POST /api/v1/nodes

#### 参数

- **body**: <a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

201 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): Created

202 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): Accepted

401: Unauthorized

### `update` 替换指定节点

#### HTTP 请求

PUT /api/v1/nodes/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  节点的名称。

- **body**: <a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

201 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): Created

401: Unauthorized

### `update` 替换指定节点的状态

#### HTTP 请求

PUT /api/v1/nodes/{name}/status

#### 参数

- **name** (**路径参数**): string, 必需

  节点的名称。

- **body**: <a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>, 必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

201 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): Created

401: Unauthorized

### `patch` 部分更新指定节点

#### HTTP 请求

PATCH /api/v1/nodes/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  节点的名称。

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, 必需

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

200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

201 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): Created

401: Unauthorized

### `patch` 部分更新指定节点的状态

#### HTTP 请求

PATCH /api/v1/nodes/{name}/status

#### 参数

- **name** (**路径参数**): string, 必需

  节点的名称。

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, 必需

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

200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

201 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): Created

401: Unauthorized

### `delete` 删除一个节点

#### HTTP 请求

DELETE /api/v1/nodes/{name}

#### 参数

- **name** (**路径参数**): string, 必需

  节点的名称。

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

### `deletecollection` 删除节点的集合

#### HTTP 请求

DELETE /api/v1/nodes

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
