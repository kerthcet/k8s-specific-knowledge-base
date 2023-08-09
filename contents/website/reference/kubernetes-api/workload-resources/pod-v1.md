---
api_metadata:
  apiVersion: "v1"
  import: "k8s.io/api/core/v1"
  kind: "Pod"
content_type: "api_reference"
description: "Pod 是可以在主机上运行的容器的集合。"
title: "Pod"
weight: 1
---

`apiVersion: v1`

`import "k8s.io/api/core/v1"`

## Pod {#Pod}

Pod 是可以在主机上运行的容器的集合。此资源由客户端创建并调度到主机上。

<hr>

- **apiVersion**: v1

- **kind**: Pod

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  标准的对象元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../workload-resources/pod-v1#PodSpec" >}}">PodSpec</a>)

  对 Pod 预期行为的规约。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

- **status** (<a href="{{< ref "../workload-resources/pod-v1#PodStatus" >}}">PodStatus</a>)
  
  最近观察到的 Pod 状态。这些数据可能不是最新的。由系统填充。只读。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

## PodSpec {#PodSpec}

PodSpec 是对 Pod 的描述。

<hr>

### 容器  {#containers}

- **containers** ([]<a href="{{< ref "../workload-resources/pod-v1#Container" >}}">Container</a>)，必需

  **补丁策略：基于 `name` 键合并**
  
  属于 Pod 的容器列表。当前无法添加或删除容器。Pod 中必须至少有一个容器。无法更新。

- **initContainers** ([]<a href="{{< ref "../workload-resources/pod-v1#Container" >}}">Container</a>)

  **补丁策略：基于 `name` 键合并**

  属于 Pod 的 Init 容器列表。Init 容器在容器启动之前按顺序执行。
  如果任何一个 Init 容器发生故障，则认为该 Pod 失败，并根据其 restartPolicy 处理。
  Init 容器或普通容器的名称在所有容器中必须是唯一的。
  Init 容器不可以有生命周期操作、就绪态探针、存活态探针或启动探针。
  在调度过程中会考虑 Init 容器的资源需求，方法是查找每种资源类型的最高请求/限制，
  然后使用该值的最大值或正常容器的资源请求的总和。
  对资源限制以类似的方式应用于 Init 容器。当前无法添加或删除 Init 容器。无法更新。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/init-containers/

- **ephemeralContainers** ([]<a href="{{< ref "../workload-resources/pod-v1#EphemeralContainer" >}}">EphemeralContainer</a>)

  **补丁策略：基于 `name` 键合并**
  
  在此 Pod 中运行的临时容器列表。临时容器可以在现有的 Pod 中运行，以执行用户发起的操作，例如调试。
  此列表在创建 Pod 时不能指定，也不能通过更新 Pod 规约来修改。
  要将临时容器添加到现有 Pod，请使用 Pod 的 `ephemeralcontainers` 子资源。

- **imagePullSecrets** ([]<a href="{{< ref "../common-definitions/local-object-reference#LocalObjectReference" >}}">LocalObjectReference</a>)

  **补丁策略：基于 `name` 键合并**

  imagePullSecrets 是对同一名字空间中 Secret 的引用的列表，用于拉取此 Pod 规约中使用的任何镜像，此字段可选。
  如果指定，这些 Secret 将被传递给各个镜像拉取组件（Puller）实现供其使用。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/containers/images#specifying-imagepullsecrets-on-a-pod

- **enableServiceLinks** (boolean)

  enableServiceLinks 指示是否应将有关服务的信息注入到 Pod 的环境变量中，服务连接的语法与
  Docker links 的语法相匹配。可选。默认为 true。

- **os** (PodOS)

  指定 Pod 中容器的操作系统。如果设置了此属性，则某些 Pod 和容器字段会受到限制。
  
  如果 os 字段设置为 `linux`，则必须不能设置以下字段：
  
  - `securityContext.windowsOptions`


  如果 os 字段设置为 `windows`，则必须不能设置以下字段：

  - `spec.hostPID`
  - `spec.hostIPC`
  - `spec.hostUsers`
  - `spec.securityContext.seLinuxOptions`
  - `spec.securityContext.seccompProfile`
  - `spec.securityContext.fsGroup`
  - `spec.securityContext.fsGroupChangePolicy`
  - `spec.securityContext.sysctls`
  - `spec.shareProcessNamespace`
  - `spec.securityContext.runAsUser`
  - `spec.securityContext.runAsGroup`
  - `spec.securityContext.supplementalGroups`
  - `spec.containers[*].securityContext.seLinuxOptions`
  - `spec.containers[*].securityContext.seccompProfile`
  - `spec.containers[*].securityContext.capabilities`
  - `spec.containers[*].securityContext.readOnlyRootFilesystem`
  - `spec.containers[*].securityContext.privileged`
  - `spec.containers[*].securityContext.allowPrivilegeEscalation`
  - `spec.containers[*].securityContext.procMount`
  - `spec.containers[*].securityContext.runAsUser`
  - `spec.containers[*].securityContext.runAsGroup`
  
  <a name="PodOS"></a>
  
  **PodOS 定义一个 Pod 的操作系统参数。**


  - **os.name** (string)，必需

    name 是操作系统的名称。当前支持的值是 `linux` 和 `windows`。
    将来可能会定义附加值，并且可以是以下之一：
    https://github.com/opencontainers/runtime-spec/blob/master/config.md#platform-specific-configuration
    客户端应该期望处理附加值并将此字段无法识别时视其为 `os: null`。

### 卷

- **volumes** ([]<a href="{{< ref "../config-and-storage-resources/volume#Volume" >}}">Volume</a>)

  **补丁策略：retainKeys，基于键 `name` 合并**
  
  可以由属于 Pod 的容器挂载的卷列表。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/storage/volumes

### 调度

- **nodeSelector** (map[string]string)

  nodeSelector 是一个选择算符，这些算符必须取值为 true 才能认为 Pod 适合在节点上运行。
  选择算符必须与节点的标签匹配，以便在该节点上调度 Pod。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/configuration/assign-pod-node/

- **nodeName** (string)

  nodeName 是将此 Pod 调度到特定节点的请求。
  如果字段值不为空，调度器只是直接将这个 Pod 调度到所指定节点上，假设节点符合资源要求。

- **affinity** (Affinity)

  如果指定了，则作为 Pod 的调度约束。

  <a name="Affinity"></a>
  **Affinity 是一组亲和性调度规则。**


  - **affinity.nodeAffinity** (<a href="{{< ref "../workload-resources/pod-v1#NodeAffinity" >}}">NodeAffinity</a>)

    描述 Pod 的节点亲和性调度规则。

  - **affinity.podAffinity** (<a href="{{< ref "../workload-resources/pod-v1#PodAffinity" >}}">PodAffinity</a>)

    描述 Pod 亲和性调度规则（例如，将此 Pod 与其他一些 Pod 放在同一节点、区域等）。

  - **affinity.podAntiAffinity** (<a href="{{< ref "../workload-resources/pod-v1#PodAntiAffinity" >}}">PodAntiAffinity</a>)

    描述 Pod 反亲和性调度规则（例如，避免将此 Pod 与其他一些 Pod 放在相同的节点、区域等）。

- **tolerations** ([]Toleration)

  如果设置了此字段，则作为 Pod 的容忍度。

  <a name="Toleration"></a>
  **这个 Toleration 所附加到的 Pod 能够容忍任何使用匹配运算符 `<operator>` 匹配三元组 `<key,value,effect>` 所得到的污点。**


  - **tolerations.key** (string)

    key 是容忍度所适用的污点的键名。此字段为空意味着匹配所有的污点键。
    如果 key 为空，则 operator 必须为 `Exists`；这种组合意味着匹配所有值和所有键。
    

  - **tolerations.operator** (string)

    operator 表示 key 与 value 之间的关系。有效的 operator 取值是 `Exists` 和 `Equal`。默认为 `Equal`。
    `Exists` 相当于 value 为某种通配符，因此 Pod 可以容忍特定类别的所有污点。


  - **tolerations.value** (string)

    value 是容忍度所匹配的污点值。如果 operator 为 `Exists`，则此 value 值应该为空，
    否则 value 值应该是一个正常的字符串。


  - **tolerations.effect** (string)

    effect 指示要匹配的污点效果。空值意味著匹配所有污点效果。如果要设置此字段，允许的值为
    `NoSchedule`、`PreferNoSchedule` 和 `NoExecute` 之一。


  - **tolerations.tolerationSeconds** (int64)

    tolerationSeconds 表示容忍度（effect 必须是 `NoExecute`，否则此字段被忽略）容忍污点的时间长度。
    默认情况下，此字段未被设置，这意味着会一直能够容忍对应污点（不会发生驱逐操作）。
    零值和负值会被系统当做 0 值处理（立即触发驱逐）。

- **schedulerName** (string)

  如果设置了此字段，则 Pod 将由指定的调度器调度。如果未指定，则使用默认调度器来调度 Pod。

- **runtimeClassName** (string)

  runtimeClassName 引用 `node.k8s.io` 组中的一个 RuntimeClass 对象，该 RuntimeClass 将被用来运行这个 Pod。
  如果没有 RuntimeClass 资源与所设置的类匹配，则 Pod 将不会运行。
  如果此字段未设置或为空，将使用 "旧版" RuntimeClass。
  "旧版" RuntimeClass 可以视作一个隐式的运行时类，其定义为空，会使用默认运行时处理程序。
  更多信息：
  https://git.k8s.io/enhancements/keps/sig-node/585-runtime-class

- **priorityClassName** (string)

  如果设置了此字段，则用来标明 Pod 的优先级。
  `"system-node-critical"` 和 `"system-cluster-critical"` 是两个特殊关键字，
  分别用来表示两个最高优先级，前者优先级更高一些。
  任何其他名称都必须通过创建具有该名称的 PriorityClass 对象来定义。
  如果未指定此字段，则 Pod 优先级将为默认值。如果没有默认值，则为零。

- **priority** (int32)

  优先级值。各种系统组件使用该字段来确定 Pod 的优先级。当启用 Priority 准入控制器时，
  该控制器会阻止用户设置此字段。准入控制器基于 priorityClassName 设置来填充此字段。
  字段值越高，优先级越高。

- **preemptionPolicy** (string)

  preemptionPolicy 是用来抢占优先级较低的 Pod 的策略。取值为 `"Never"`、`"PreemptLowerPriority"` 之一。
  如果未设置，则默认为 `"PreemptLowerPriority"`。

- **topologySpreadConstraints** ([]TopologySpreadConstraint)

  **补丁策略：基于 `topologyKey` 键合并**
  
  **映射：`topologyKey, whenUnsatisfiable` 键组合的唯一值 將在合并期间保留**
  
  TopologySpreadConstraints 描述一组 Pod 应该如何跨拓扑域来分布。调度器将以遵从此约束的方式来调度 Pod。
  所有 topologySpreadConstraints 条目会通过逻辑与操作进行组合。

  <a name="TopologySpreadConstraint"></a>
  **TopologySpreadConstraint 指定如何在规定的拓扑下分布匹配的 Pod。**


  - **topologySpreadConstraints.maxSkew** (int32)，必需

    maxSkew 描述 Pod 可能分布不均衡的程度。当 `whenUnsatisfiable=DoNotSchedule` 时，
    此字段值是目标拓扑中匹配的 Pod 数量与全局最小值之间的最大允许差值。
    全局最小值是候选域中匹配 Pod 的最小数量，如果候选域的数量小于 `minDomains`，则为零。
    例如，在一个包含三个可用区的集群中，maxSkew 设置为 1，具有相同 `labelSelector` 的 Pod 分布为 2/2/1：
    在这种情况下，全局最小值为 1。

    ```
    | zone1 | zone2 | zone3 |
    | PP    | PP    |  P    |
    ```

    - 如果 maxSkew 为 1，传入的 Pod 只能调度到 "zone3"，变成 2/2/2；
      将其调度到 "zone1"（"zone2"）将使"zone1"（"zone2"）上的实际偏差（Actual Skew）为 3-1，进而违反
      maxSkew 限制（1）。
    - 如果 maxSkew 为 2，则可以将传入的 Pod 调度到任何区域。

    当 `whenUnsatisfiable=ScheduleAnyway` 时，此字段被用来给满足此约束的拓扑域更高的优先级。

    此字段是一个必填字段。默认值为 1，不允许为 0。


  - **topologySpreadConstraints.topologyKey** (string)，必需

    topologyKey 是节点标签的键名。如果节点的标签中包含此键名且键值亦相同，则被认为在相同的拓扑域中。
    我们将每个 `<键, 值>` 视为一个 "桶（Bucket）"，并尝试将数量均衡的 Pod 放入每个桶中。
    我们定义域（Domain）为拓扑域的特定实例。
    此外，我们定义一个候选域（Eligible Domain）为其节点与 nodeAffinityPolicy 和 nodeTaintsPolicy 的要求匹配的域。
    例如，如果 topologyKey 是 `"kubernetes.io/hostname"`，则每个 Node 都是该拓扑的域。
    而如果 topologyKey 是 `"topology.kubernetes.io/zone"`，则每个区域都是该拓扑的一个域。
    这是一个必填字段。


  - **topologySpreadConstraints.whenUnsatisfiable** (string)，必需

    whenUnsatisfiable 表示如果 Pod 不满足分布约束，如何处理它。

    - `DoNotSchedule`（默认）：告诉调度器不要调度它。
    - `ScheduleAnyway`：告诉调度器将 Pod 调度到任何位置，但给予能够降低偏差的拓扑更高的优先级。

    当且仅当该 Pod 的每个可能的节点分配都会违反某些拓扑对应的 "maxSkew" 时，
    才认为传入 Pod 的约束是 "不可满足的"。

    例如，在一个包含三个区域的集群中，maxSkew 设置为 1，具有相同 labelSelector 的 Pod 分布为 3/1/1：

    ```
    | zone1 | zone2 | zone3 |
    | P P P | P     | P     |
    ```

    如果 whenUnsatisfiable 设置为 `DoNotSchedule`，则传入的 Pod 只能调度到 "zone2"（"zone3"），
    Pod 分布变成 3/2/1（3/1/2），因为 "zone2"（"zone3"）上的实际偏差（Actual Skew） 为 2-1，
    满足 maxSkew 约束（1）。
    换句话说，集群仍然可以不平衡，但调度器不会使其**更加地**不平衡。

    这是一个必填字段。


  - **topologySpreadConstraints.labelSelector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)

    labelSelector 用于识别匹配的 Pod。对匹配此标签选择算符的 Pod 进行计数，
    以确定其相应拓扑域中的 Pod 数量。

  - **topologySpreadConstraints.matchLabelKeys** ([]string)

    **原子性：将在合并期间被替换**
    
    matchLabelKeys 是一组 Pod 标签键，用于通过计算 Pod 分布方式来选择 Pod。
    新 Pod 标签中不存在的键将被忽略。这些键用于从新来的 Pod 标签中查找值，这些键值标签与 labelSelector 进行逻辑与运算，
    通过计算 Pod 的分布方式来选择现有 Pod 的组。matchLabelKeys 和 labelSelector
    中禁止存在相同的键。未设置 labelSelector 时无法设置 matchLabelKeys。
    新来的 Pod 标签中不存在的键将被忽略。null 或空的列表意味着仅与 labelSelector 匹配。

    这是一个 Beta 字段，需要启用 MatchLabelKeysInPodTopologySpread 特性门控（默认启用）。

  - **topologySpreadConstraints.minDomains** (int32)

    minDomains 表示符合条件的域的最小数量。当符合拓扑键的候选域个数小于 minDomains 时，
    Pod 拓扑分布特性会将 "全局最小值" 视为 0，然后进行偏差的计算。
    当匹配拓扑键的候选域的数量等于或大于 minDomains 时，此字段的值对调度没有影响。
    因此，当候选域的数量少于 minDomains 时，调度程序不会将超过 maxSkew 个 Pods 调度到这些域。
    如果字段值为 nil，所表达的约束为 minDomains 等于 1。
    字段的有效值为大于 0 的整数。当字段值不为 nil 时，whenUnsatisfiable 必须为 `DoNotSchedule`。
    
    例如，在一个包含三个区域的集群中，maxSkew 设置为 2，minDomains 设置为 5，具有相同 labelSelector
    的 Pod 分布为 2/2/2：

    ```
    | zone1 | zone2 | zone3 |
    | PP    | PP    | PP    |
    ```

    域的数量小于 5（minDomains 取值），因此"全局最小值"被视为 0。
    在这种情况下，无法调度具有相同 labelSelector 的新 Pod，因为如果基于新 Pod 计算的偏差值将为
    3（3-0）。将这个 Pod 调度到三个区域中的任何一个，都会违反 maxSkew 约束。
    
    此字段是一个 Beta 字段，需要启用 MinDomainsInPodTopologySpread 特性门控（默认被启用）。


  - **topologySpreadConstraints.nodeAffinityPolicy** (string)

    nodeAffinityPolicy 表示我们在计算 Pod 拓扑分布偏差时将如何处理 Pod 的 nodeAffinity/nodeSelector。
    选项为：
    - Honor：只有与 nodeAffinity/nodeSelector 匹配的节点才会包括到计算中。
    - Ignore：nodeAffinity/nodeSelector 被忽略。所有节点均包括到计算中。

    如果此值为 nil，此行为等同于 Honor 策略。
    这是通过 NodeInclusionPolicyInPodTopologySpread 特性标志默认启用的 Beta 级别特性。

  - **topologySpreadConstraints.nodeTaintsPolicy** (string)

    nodeTaintsPolicy 表示我们在计算 Pod 拓扑分布偏差时将如何处理节点污点。选项为：
    - Honor：包括不带污点的节点以及新来 Pod 具有容忍度且带有污点的节点。
    - Ignore：节点污点被忽略。包括所有节点。
    
    如果此值为 nil，此行为等同于 Ignore 策略。
    这是通过 NodeInclusionPolicyInPodTopologySpread 特性标志默认启用的 Beta 级别特性。

- **overhead** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

  overhead 表示与用指定 RuntimeClass 运行 Pod 相关的资源开销。
  该字段将由 RuntimeClass 准入控制器在准入时自动填充。
  如果启用了 RuntimeClass 准入控制器，则不得在 Pod 创建请求中设置 overhead 字段。
  RuntimeClass 准入控制器将拒绝已设置 overhead 字段的 Pod 创建请求。
  如果在 Pod 规约中配置并选择了 RuntimeClass，overhead 字段将被设置为对应 RuntimeClass 中定义的值，
  否则将保持不设置并视为零。更多信息：
  https://git.k8s.io/enhancements/keps/sig-node/688-pod-overhead/README.md


### 生命周期

- **restartPolicy** (string)

  Pod 内所有容器的重启策略。`Always`、`OnFailure`、`Never` 之一。
  在某些情况下，可能只允许这些值的一个子集。默认为 `Always`。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy

- **terminationGracePeriodSeconds** (int64)

  可选字段，表示 Pod 需要体面终止的所需的时长（以秒为单位）。字段值可以在删除请求中减少。
  字段值必须是非负整数。零值表示收到 kill 信号则立即停止（没有机会关闭）。
  如果此值为 nil，则将使用默认宽限期。
  宽限期是从 Pod 中运行的进程收到终止信号后，到进程被 kill 信号强制停止之前，Pod 可以继续存在的时间（以秒为单位）。
  应该将此值设置为比你的进程的预期清理时间更长。默认为 30 秒。

- **activeDeadlineSeconds** (int64)

  在系统将主动尝试将此 Pod 标记为已失败并杀死相关容器之前，Pod 可能在节点上活跃的时长；
  市场计算基于 startTime 计算间（以秒为单位）。字段值必须是正整数。

- **readinessGate** ([]PodReadinessGate)

  如果设置了此字段，则将评估所有就绪门控（Readiness Gate）以确定 Pod 就绪状况。
  当所有容器都已就绪，并且就绪门控中指定的所有状况的 status 都为 "true" 时，Pod 被视为就绪。
  更多信息： https://git.k8s.io/enhancements/keps/sig-network/580-pod-readiness-gates

  <a name="PodReadinessGate"></a>
  **PodReadinessGate 包含对 Pod 状况的引用**


  - **readinessGates.conditionType** (string)，必需

    conditionType 是指 Pod 的状况列表中类型匹配的状况。

### 主机名和名称解析

- **hostname**  (string)

  指定 Pod 的主机名。如果此字段未指定，则 Pod 的主机名将设置为系统定义的值。

- **setHostnameAsFQDN** (boolean)

  如果为 true，则 Pod 的主机名将配置为 Pod 的 FQDN，而不是叶名称（默认值）。
  在 Linux 容器中，这意味着将内核的 hostname 字段（struct utsname 的 nodename 字段）设置为 FQDN。
  在 Windows 容器中，这意味着将注册表项 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters`
  的 hostname 键设置为 FQDN。如果 Pod 没有 FQDN，则此字段不起作用。
  默认为 false。

- **subdomain** (string)

  如果设置了此字段，则完全限定的 Pod 主机名将是 `<hostname>.<subdomain>.<Pod 名字空间>.svc.<集群域名>`。
  如果未设置此字段，则该 Pod 将没有域名。

- **hostAliases** ([]HostAlias)

  **补丁策略：基于 `ip` 键合并**
  
  hostAliases 是一个可选的列表属性，包含要被注入到 Pod 的 hosts 文件中的主机和 IP 地址。
  这仅对非 hostNetwork Pod 有效。

  <a name="HostAlias"></a>
  **HostAlias 结构保存 IP 和主机名之间的映射，这些映射将作为 Pod 的 hosts 文件中的条目注入。**


  - **hostAliases.hostnames** ([]string)

    指定 IP 地址对应的主机名。

  - **hostAliases.ip** (string)

    主机文件条目的 IP 地址。

- **dnsConfig** (PodDNSConfig)

  指定 Pod 的 DNS 参数。此处指定的参数将被合并到基于 dnsPolicy 生成的 DNS 配置中。

  <a name="PodDNSConfig"></a>
  **PodDNSConfig 定义 Pod 的 DNS 参数，这些参数独立于基于 dnsPolicy 生成的参数。**


  - **dnsConfig.nameservers** ([]string)

    DNS 名字服务器的 IP 地址列表。此列表将被追加到基于 dnsPolicy 生成的基本名字服务器列表。
    重复的名字服务器将被删除。


  - **dnsConfig.options** ([]PodDNSConfigOption)

    DNS 解析器选项列表。此处的选项将与基于 dnsPolicy 所生成的基本选项合并。重复的条目将被删除。
    options 中所给出的解析选项将覆盖基本 dnsPolicy 中出现的对应选项。

    <a name="PodDNSConfigOption"></a>

    **PodDNSConfigOption 定义 Pod 的 DNS 解析器选项。**


    - **dnsConfig.options.name** (string)

      必需字段。

    - **dnsConfig.options.value** (string)

      选项取值。


  - **dnsConfig.searches** ([]string)

    用于主机名查找的 DNS 搜索域列表。这一列表将被追加到基于 dnsPolicy 生成的基本搜索路径列表。
    重复的搜索路径将被删除。

- **dnsPolicy** (string)

  为 Pod 设置 DNS 策略。默认为 `"ClusterFirst"`。
  有效值为 `"ClusterFirstWithHostNet"`、`"ClusterFirst"`、`"Default"` 或 `"None"`。
  dnsConfig 字段中给出的 DNS 参数将与使用 dnsPolicy 字段所选择的策略合并。
  要针对 hostNetwork 的 Pod 设置 DNS 选项，你必须将 DNS 策略显式设置为 `"ClusterFirstWithHostNet"`。

### 主机名字空间

- **hostNetwork** (boolean)

  为此 Pod 请求主机层面联网支持。使用主机的网络名字空间。
  如果设置了此选项，则必须指定将使用的端口。默认为 false。

- **hostPID** (boolean)

  使用主机的 PID 名字空间。可选：默认为 false。

- **hostIPC** (boolean)

  使用主机的 IPC 名字空间。可选：默认为 false。

- **shareProcessNamespace** (boolean)

  在 Pod 中的所有容器之间共享单个进程名字空间。设置了此字段之后，容器将能够查看来自同一 Pod 中其他容器的进程并发出信号，
  并且每个容器中的第一个进程不会被分配 PID 1。`hostPID` 和 `shareProcessNamespace` 不能同时设置。
  可选：默认为 false。

### 服务账号

- **serviceAccountName** (string)

  serviceAccountName 是用于运行此 Pod 的服务账号的名称。更多信息：
  https://kubernetes.io/zh-cn/docs/tasks/configure-pod-container/configure-service-account/

- **automountServiceAccountToken** (boolean)

  automountServiceAccountToken 指示是否应自动挂载服务帐户令牌。

### 安全上下文


- **securityContext** (PodSecurityContext)

  SecurityContext 包含 Pod 级别的安全属性和常见的容器设置。
  可选：默认为空。每个字段的默认值见类型描述。


  <a name="PodSecurityContext"></a>
  **PodSecurityContext 包含 Pod 级别的安全属性和常用容器设置。**
  **一些字段也存在于 `container.securityContext` 中。`container.securityContext`**
  **中的字段值优先于 PodSecurityContext 的字段值。**


  - **securityContext.runAsUser** (int64)

    运行容器进程入口点（Entrypoint）的 UID。如果未指定，则默认为镜像元数据中指定的用户。
    也可以在 SecurityContext 中设置。
    如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在对应容器中所设置的 SecurityContext 值优先。
    注意，`spec.os.name` 为 "windows" 时不能设置此字段。


  - **securityContext.runAsNonRoot** (boolean)

    指示容器必须以非 root 用户身份运行。如果为 true，kubelet 将在运行时验证镜像，
    以确保它不会以 UID 0（root）身份运行。如果镜像中确实使用 root 账号启动，则容器无法被启动。
    如果此字段未设置或为 false，则不会执行此类验证。也可以在 SecurityContext 中设置。
    如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在 SecurityContext 中指定的值优先。


  - **securityContext.runAsGroup** (int64)

    运行容器进程入口点（Entrypoint）的 GID。如果未设置，则使用运行时的默认值。
    也可以在 SecurityContext 中设置。如果同时在 SecurityContext 和 PodSecurityContext 中设置，
    则在对应容器中设置的 SecurityContext 值优先。
    注意，`spec.os.name` 为 "windows" 时不能设置该字段。


  - **securityContext.supplementalGroups** ([]int64)
  
    此字段包含将应用到每个容器中运行的第一个进程的组列表。
    容器进程的组成员身份取决于容器的主 GID、fsGroup（如果指定了的话）
    和在容器镜像中为容器进程的 uid 定义的组成员身份，以及这里所给的列表。

    如果未指定，则不会向任何容器添加其他组。
    注意，在容器镜像中为容器进程的 uid 定义的组成员身份仍然有效，
    即使它们未包含在此列表中也是如此。
    注意，当 `spec.os.name` 为 `windows` 时，不能设置此字段。


  - **securityContext.fsGroup** (int64)

    应用到 Pod 中所有容器的特殊补充组。某些卷类型允许 kubelet 将该卷的所有权更改为由 Pod 拥有：
    
    1. 文件系统的属主 GID 将是 fsGroup 字段值
    2. `setgid` 位已设置（在卷中创建的新文件将归 fsGroup 所有）
    3. 权限位将与 `rw-rw----` 进行按位或操作
    
    如果未设置此字段，kubelet 不会修改任何卷的所有权和权限。
    注意，`spec.os.name` 为 "windows" 时不能设置此字段。


  - **securityContext.fsGroupChangePolicy** (string)

    fsGroupChangePolicy 定义了在卷被在 Pod 中暴露之前更改其属主和权限的行为。
    此字段仅适用于支持基于 fsGroup 的属主权（和权限）的卷类型。它不会影响临时卷类型，
    例如：`secret`、`configmap` 和 `emptydir`。
    有效值为 `"OnRootMismatch"` 和 `"Always"`。如果未设置，则使用 `"Always"`。
    注意，`spec.os.name` 为 "windows" 时不能设置此字段。


  - **securityContext.seccompProfile** (SeccompProfile)

    此 Pod 中的容器使用的 seccomp 选项。注意，`spec.os.name` 为 "windows" 时不能设置此字段。


    **SeccompProfile 定义 Pod 或容器的 seccomp 配置文件设置。只能设置一个配置文件源。**


    - **securityContext.seccompProfile.type** (string)，必需

      type 标明将应用哪种 seccomp 配置文件。有效的选项有：

      - `Localhost` - 应使用在节点上的文件中定义的配置文件。
      - `RuntimeDefault` - 应使用容器运行时默认配置文件。
      - `Unconfined` - 不应应用任何配置文件。


    - **securityContext.seccompProfile.localhostProfile** (string)

      localhostProfile 指示应使用在节点上的文件中定义的配置文件。该配置文件必须在节点上预先配置才能工作。
      必须是相对于 kubelet 配置的 seccomp 配置文件位置的下降路径。
      仅当 type 为 `"Localhost"` 时才必须设置。


  - **securityContext.seLinuxOptions** (SELinuxOptions)

    应用于所有容器的 SELinux 上下文。如果未设置，容器运行时将为每个容器分配一个随机 SELinux 上下文。
    也可以在 SecurityContext 中设置。
    如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在对应容器中设置的 SecurityContext 值优先。
    注意，`spec.os.name` 为 "windows" 时不能设置该字段。


    <a name="SELinuxOptions"></a>
    **SELinuxOptions 是要应用于容器的标签**


    - **securityContext.seLinuxOptions.level** (string)

      level 是应用于容器的 SELinux 级别标签。

    - **securityContext.seLinuxOptions.role** (string)

      role 是应用于容器的 SELinux 角色标签。

    - **securityContext.seLinuxOptions.type** (string)

      type 是适用于容器的 SELinux 类型标签。

    - **securityContext.seLinuxOptions.user** (string)

      user 是应用于容器的 SELinux 用户标签。


  - **securityContext.sysctls** ([]Sysctl)

    sysctls 包含用于 Pod 的名字空间 sysctl 列表。具有不受（容器运行时）支持的 sysctl 的 Pod 可能无法启动。
    注意，`spec.os.name` 为 "windows" 时不能设置此字段。


    <a name="Sysctl"></a>
    **Sysctl 定义要设置的内核参数**


    - **securityContext.sysctls.name** (string)，必需

      要设置的属性的名称。

    - **securityContext.sysctls.value** (string)，必需

      要设置的属性值。


  - **securityContext.windowsOptions** (WindowsSecurityContextOptions)

    要应用到所有容器上的、特定于 Windows 的设置。
    如果未设置此字段，将使用容器的 SecurityContext 中的选项。
    如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在 SecurityContext 中指定的值优先。
    注意，`spec.os.name` 为 "linux" 时不能设置该字段。


    <a name="WindowsSecurityContextOptions"></a>
    **WindowsSecurityContextOptions 包含特定于 Windows 的选项和凭据。**


    - **securityContext.windowsOptions.gmsaCredentialSpec** (string)

      gmsaCredentialSpec 是 [GMSA 准入 Webhook](https://github.com/kubernetes-sigs/windows-gmsa)
      内嵌由 gmsaCredentialSpecName 字段所指定的 GMSA 凭证规约内容的地方。

    - **securityContext.windowsOptions.gmsaCredentialSpecName** (string)

      gmsaCredentialSpecName 是要使用的 GMSA 凭证规约的名称。


    - **securityContext.windowsOptions.hostProcess** (boolean)

      hostProcess 确定容器是否应作为"主机进程"容器运行。
      此字段是 Alpha 级别的，只有启用 WindowsHostProcessContainers 特性门控的组件才会理解此字段。
      在不启用该功能门控的前提下设置了此字段，将导致验证 Pod 时发生错误。
      一个 Pod 的所有容器必须具有相同的有效 hostProcess 值（不允许混合设置了 hostProcess
      的容器和未设置 hostProcess 容器）。
      此外，如果 hostProcess 为 true，则 hostNetwork 也必须设置为 true。


    - **securityContext.windowsOptions.runAsUserName** (string)

      Windows 中用来运行容器进程入口点的用户名。如果未设置，则默认为镜像元数据中指定的用户。
      也可以在 PodSecurityContext 中设置。
      如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在 SecurityContext 中指定的值优先。

### Alpha 级别

- **hostUsers** (boolean)

  使用主机的用户名字空间。可选：默认为 true。如果设置为 true 或不存在，则 Pod 将运行在主机的用户名字空间中，
  当 Pod 需要仅对主机用户名字空间可用的一个特性时这会很有用，例如使用 CAP_SYS_MODULE 加载内核模块。
  当设置为 false 时，会为该 Pod 创建一个新的用户名字空间。
  设置为 false 对于缓解容器逃逸漏洞非常有用，可防止允许实际在主机上没有 root 特权的用户以 root 运行他们的容器。
  此字段是 Alpha 级别的字段，只有启用 UserNamespacesSupport 特性的服务器才能使用此字段。

- **resourceClaims** ([]PodResourceClaim)

  **补丁策略：retainKeys，基于键 `name` 合并**

  **映射：键 `name` 的唯一值将在合并过程中保留**

  resourceClaims 定义了在允许 Pod 启动之前必须分配和保留哪些 ResourceClaims。
  这些资源将可供那些按名称使用它们的容器使用。

  这是一个 Alpha 特性的字段，需要启用 DynamicResourceAllocation 特性门控来开启此功能。

  此字段不可变更。

  <a name="PodResourceClaim"></a>
  **PodResourceClaim 通过 ClaimSource 引用一个 ResourceClaim。
  它为 ClaimSource 添加一个名称，作为 Pod 内 ResourceClaim 的唯一标识。
  需要访问 ResourceClaim 的容器可使用此名称引用它。**

  - **resourceClaims.name** (string), 必需

    在 Pod 中，`name` 是此资源声明的唯一标识。此字段值必须是 DNS_LABEL。

  - **resourceClaims.source** (ClaimSource)

    `source` 描述了在哪里可以找到 `resourceClaim`。

    <a name="ClaimSource"></a>
    
    **ClaimSource 描述对 ResourceClaim 的引用。**

    **应该设置且仅设置如下字段之一。此类型的消费者必须将空对象视为具有未知值。**

    
    - **resourceClaims.source.resourceClaimName** (string)

      resourceClaimName 是与此 Pod 位于同一命名空间中的 ResourceClaim 对象的名称。

    - **resourceClaims.source.resourceClaimTemplateName** (string)

      resourceClaimTemplateName 是与此 Pod 位于同一命名空间中的 `ResourceClaimTemplate` 对象的名称。

    
      该模板将用于创建一个新的 ResourceClaim，新的 ResourceClaim 将被绑定到此 Pod。
      删除此 Pod 时，ResourceClaim 也将被删除。ResourceClaim 
      的名称将为 \<Pod 名称>-\<资源名称>，其中 \<资源名称>
      是 PodResourceClaim.name。如果串接起来的名称对于 ResourceClaim
      无效（例如太长），Pod 的验证机制将拒绝该 Pod。

      
      不属于此 Pod 但与此名称重名的现有 ResourceClaim 不会被用于此 Pod，
      以避免错误地使用不相关的资源。Pod 的调度和启动动作会因此而被阻塞，
      直到不相关的 ResourceClaim 被删除。

      
      此字段是不可变更的，创建 ResourceClaim 后控制平面不会对相应的 ResourceClaim 进行任何更改。
- **schedulingGates** ([]PodSchedulingGate)

  **补丁策略：基于 `name` 键合并**

  **映射：键 `name` 的唯一值将在合并过程中保留**
   
  
  schedulingGates 是一个不透明的值列表，如果指定，将阻止调度 Pod。
  如果 schedulingGates 不为空，则 Pod 将保持 SchedulingGated 状态，调度程序将不会尝试调度 Pod。
 
  SchedulingGates 只能在 Pod 创建时设置，并且只能在创建之后删除。 

  此特性为 Beta 特性，需要通过 PodSchedulingReadiness 特性门控启用。

  <a name="PodSchedulingGate"></a>
  
  **PodSchedulingGate 与 Pod 相关联以保护其调度。**

  - **schedulingGates.name** (string)，必需
  
    调度门控的名称，每个调度门控的 `name` 字段取值必须唯一。



### 已弃用

- **serviceAccount** (string)

  deprecatedServiceAccount 是 serviceAccountName 的弃用别名。此字段已被弃用：应改用 serviceAccountName。

## 容器 {#Container}

要在 Pod 中运行的单个应用容器。

<hr>

- **name** (string)，必需

  指定为 DNS_LABEL 的容器的名称。Pod 中的每个容器都必须有一个唯一的名称 (DNS_LABEL)。无法更新。

### 镜像 {#image}


- **image** (string)

  容器镜像名称。更多信息： https://kubernetes.io/zh-cn/docs/concepts/containers/images。
  此字段是可选的，以允许更高层的配置管理进行默认设置或覆盖工作负载控制器（如 Deployment 和 StatefulSets）
  中的容器镜像。

- **imagePullPolicy** (string)

  镜像拉取策略。`"Always"`、`"Never"`、`"IfNotPresent"` 之一。如果指定了 `:latest` 标签，则默认为 `"Always"`，
  否则默认为 `"IfNotPresent"`。无法更新。更多信息： 
  https://kubernetes.io/zh-cn/docs/concepts/containers/images#updating-images


### Entrypoint


- **command** ([]string)

  入口点数组。不在 Shell 中执行。如果未提供，则使用容器镜像的 `ENTRYPOINT`。
  变量引用 `$(VAR_NAME)` 使用容器的环境进行扩展。如果无法解析变量，则输入字符串中的引用将保持不变。
  `$$` 被简化为 `$`，这允许转义 `$(VAR_NAME)` 语法：即 `"$$(VAR_NAME)" ` 将产生字符串字面值 `"$(VAR_NAME)"`。
  无论变量是否存在，转义引用都不会被扩展。无法更新。更多信息： 
  https://kubernetes.io/zh-cn/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell


- **args** ([]string)

  entrypoint 的参数。如果未提供，则使用容器镜像的 `CMD` 设置。变量引用 `$(VAR_NAME)` 使用容器的环境进行扩展。
  如果无法解析变量，则输入字符串中的引用将保持不变。`$$` 被简化为 `$`，这允许转义 `$(VAR_NAME)` 语法：
  即 `"$$(VAR_NAME)"` 将产生字符串字面值 `"$(VAR_NAME)"`。无论变量是否存在，转义引用都不会被扩展。无法更新。
  更多信息： 
  https://kubernetes.io/zh-cn/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell


- **workingDir** (string)

  容器的工作目录。如果未指定，将使用容器运行时的默认值，默认值可能在容器镜像中配置。无法更新。


### 端口


- **ports**（[]ContainerPort）

  **补丁策略：基于 `containerPort` 键合并**
  
  **映射：键 `containerPort, protocol` 组合的唯一值将在合并期间保留**
  
  要从容器暴露的端口列表。此处不指定端口不会阻止该端口被暴露。
  任何侦听容器内默认 `"0.0.0.0"` 地址的端口都可以从网络访问。使用策略合并补丁来修改此数组可能会破坏数据。
  更多细节请参阅 https://github.com/kubernetes/kubernetes/issues/108255。
  无法更新。

  <a name="ContainerPort"></a>
  **ContainerPort 表示单个容器中的网络端口。**


  - **ports.containerPort** (int32)，必需

    要在 Pod 的 IP 地址上公开的端口号。这必须是有效的端口号，0 \< x \< 65536。

  - **ports.hostIP** (string)

    绑定外部端口的主机 IP。


  - **ports.hostPort** (int32)

    要在主机上公开的端口号。如果指定，此字段必须是一个有效的端口号，0 \< x \< 65536。
    如果设置了 hostNetwork，此字段值必须与 containerPort 匹配。大多数容器不需要设置此字段。

  - **ports.name** (string)

    如果设置此字段，这必须是 IANA_SVC_NAME 并且在 Pod 中唯一。
    Pod 中的每个命名端口都必须具有唯一的名称。服务可以引用的端口的名称。


  - **ports.protocol** (string)

    端口协议。必须是 `UDP`、`TCP` 或 `SCTP`。默认为 `TCP`。


### 环境变量


- **env**（[]EnvVar）

  **补丁策略：基于 `name` 键合并**
  
  要在容器中设置的环境变量列表。无法更新。

  <a name="EnvVar"></a>
  **EnvVar 表示容器中存在的环境变量。**


  - **env.name** (string)，必需

    环境变量的名称。必须是 C_IDENTIFIER。


  - **env.value** (string)

    变量引用 `$(VAR_NAME)` 使用容器中先前定义的环境变量和任何服务环境变量进行扩展。
    如果无法解析变量，则输入字符串中的引用将保持不变。
    `$$` 会被简化为 `$`，这允许转义 `$(VAR_NAME)` 语法：即 `"$$(VAR_NAME)"` 将产生字符串字面值 `"$(VAR_NAME)"`。
    无论变量是否存在，转义引用都不会被扩展。默认为 ""。


  - **env.valueFrom** (EnvVarSource)

    环境变量值的来源。如果 value 值不为空，则不能使用。


    **EnvVarSource 表示 envVar 值的来源。**


    - **env.valueFrom.configMapKeyRef** (ConfigMapKeySelector)

      选择某个 ConfigMap 的一个主键。


      - **env.valueFrom.configMapKeyRef.key** (string)，必需

        要选择的主键。

      - **env.valueFrom.configMapKeyRef.name** (string)

        被引用者的名称。更多信息：
        https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/#names

      - **env.valueFrom.configMapKeyRef.optional** (boolean)

        指定 ConfigMap 或其主键是否必须已经定义。


    - **env.valueFrom.fieldRef** (<a href="{{< ref "../common-definitions/object-field-selector#ObjectFieldSelector" >}}">ObjectFieldSelector</a>)

      选择 Pod 的一个字段：支持 `metadata.name`、`metadata.namespace`、`metadata.labels['<KEY>']`、
      `metadata.annotations['<KEY>']`、`spec.nodeName`、`spec.serviceAccountName`、`status.hostIP`
      `status.podIP`、`status.podIPs`。


    - **env.valueFrom.resourceFieldRef** (<a href="{{< ref "../common-definitions/resource-field-selector#ResourceFieldSelector" >}}">ResourceFieldSelector</a>)

      选择容器的资源：目前仅支持资源限制和请求（`limits.cpu`、`limits.memory`、`limits.ephemeral-storage`、
      `requests.cpu`、`requests.memory` 和 `requests.ephemeral-storage`）。


    - **env.valueFrom.secretKeyRef** (SecretKeySelector)

      在 Pod 的名字空间中选择 Secret 的主键。

      <a name="SecretKeySelector"></a>

      **SecretKeySelector 选择一个 Secret 的主键。**


      - **env.valueFrom.secretKeyRef.key** (string)，必需

        要选择的 Secret 的主键。必须是有效的主键。

      - **env.valueFrom.secretKeyRef.name** (string)

        被引用 Secret 的名称。更多信息：
        https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/#names

      - **env.valueFrom.secretKeyRef.optional** (boolean)

        指定 Secret 或其主键是否必须已经定义。

- **envFrom** ([]EnvFromSource)

  用来在容器中填充环境变量的数据源列表。在源中定义的键必须是 C_IDENTIFIER。
  容器启动时，所有无效主键都将作为事件报告。
  当一个键存在于多个源中时，与最后一个来源关联的值将优先。
  由 env 定义的条目中，与此处键名重复者，以 env 中定义为准。无法更新。

  <a name="EnvFromSource"></a>
  **EnvFromSource 表示一组 ConfigMaps 的来源**


  - **envFrom.configMapRef** (ConfigMapEnvSource)

    要从中选择主键的 ConfigMap。

    <a name="ConfigMapEnvSource"></a>
    ConfigMapEnvSource 选择一个 ConfigMap 来填充环境变量。目标 ConfigMap 的
    data 字段的内容将键值对表示为环境变量。


    - **envFrom.configMapRef.name** (string)

      被引用的 ConfigMap 的名称。更多信息：
      https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/#names

    - **envFrom.configMapRef.optional** (boolean)

      指定 ConfigMap 是否必须已经定义。


  - **envFrom.prefix** (string)

    附加到 ConfigMap 中每个键名之前的可选标识符。必须是 C_IDENTIFIER。

  - **envFrom.secretRef** (SecretEnvSource)

    要从中选择主键的 Secret。

    SecretEnvSource 选择一个 Secret 来填充环境变量。
    目标 Secret 的 data 字段的内容将键值对表示为环境变量。


    - **envFrom.secretRef.name** (string)

      被引用 Secret 的名称。更多信息：
      https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/#names

    - **envFrom.secretRef.optional** (boolean)

      指定 Secret 是否必须已经定义。


### 卷


- **volumeMounts** ([]VolumeMount)

  **补丁策略：基于 `mountPath` 键合并**
  
  要挂载到容器文件系统中的 Pod 卷。无法更新。

  VolumeMount 描述在容器中安装卷。


  - **volumeMounts.mountPath** (string)，必需

    容器内卷的挂载路径。不得包含 ':'。

  - **volumeMounts.name** (string)，必需

    此字段必须与卷的名称匹配。

  - **volumeMounts.mountPropagation** (string)

    mountPropagation 确定挂载如何从主机传播到容器，及如何反向传播。
    如果未设置，则使用 `MountPropagationNone`。该字段在 1.10 中是 Beta 版。


  - **volumeMounts.readOnly** (boolean)

    如果为 true，则以只读方式挂载，否则（false 或未设置）以读写方式挂载。默认为 false。

  - **volumeMounts.subPath** (boolean)

    卷中的路径，容器中的卷应该这一路径安装。默认为 ""（卷的根）。

  - **volumeMounts.subPathExpr** (string)

    应安装容器卷的卷内的扩展路径。行为类似于 subPath，但环境变量引用 `$(VAR_NAME)`
    使用容器的环境进行扩展。默认为 ""（卷的根）。`subPathExpr` 和 `subPath` 是互斥的。


- **volumeDevices** ([]VolumeDevice)

  **补丁策略：基于 `devicePath` 键合并**
  
  volumeDevices 是容器要使用的块设备列表。

  <a name="VolumeDevice"></a>
  volumeDevice 描述了容器内原始块设备的映射。


  - **volumeDevices.devicePath** (string)，必需

    devicePath 是设备将被映射到的容器内的路径。

  - **volumeDevices.name** (string)，必需

    name 必须与 Pod 中的 persistentVolumeClaim 的名称匹配


### 资源


- **resources**（ResourceRequirements）

  此容器所需的计算资源。无法更新。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/

  ResourceRequirements 描述计算资源需求。

  
  - **resources.claims** ([]ResourceClaim)

    **映射：键 `name` 的唯一值将在合并过程中保留**

    claims 列出此容器使用的资源名称，资源名称在 `spec.resourceClaims` 中定义。

    
    这是一个 Alpha 特性字段，需要启用 DynamicResourceAllocation 功能门控开启此特性。

    此字段不可变更，只能在容器级别设置。

    <a name="ResourceClaim"></a>
    
      **ResourceClaim 引用 `PodSpec.resourceClaims` 中的一项。**

    - **resources.claims.name** (string)，必需
      
      `name` 必须与使用该字段 Pod 的 `pod.spec.resourceClaims`
      中的一个条目的名称相匹配。它使该资源在容器内可用。


  - **resources.limits** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

    limits 描述所允许的最大计算资源用量。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/

  - **resources.requests** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

    requests 描述所需的最小计算资源量。如果容器省略了 requests，但明确设定了 limits，
    则 requests 默认值为 limits 值，否则为实现定义的值。请求不能超过限制。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/

- **resizePolicy** ([]ContainerResizePolicy)

  **原子性: 将在合并期间被替换**

  容器的资源调整策略。

  <a name="ContainerResizePolicy"></a>
  **ContainerResizePolicy 表示容器的资源大小调整策略**

  - **resizePolicy.resourceName** (string), 必需

    该资源调整策略适用的资源名称。支持的值：cpu、memory。

  
  - **resizePolicy.restartPolicy** (string), 必需

    重启策略，会在调整指定资源大小时使用该策略。如果未指定，则默认为 NotRequired。

### 生命周期


- **lifecycle** (Lifecycle)

  管理系统应对容器生命周期事件采取的行动。无法更新。

  Lifecycle 描述管理系统为响应容器生命周期事件应采取的行动。
  对于 postStart 和 preStop 生命周期处理程序，容器的管理会阻塞，直到操作完成，
  除非容器进程失败，在这种情况下处理程序被中止。


  - **lifecycle.postStart** (<a href="{{< ref "../workload-resources/pod-v1#LifecycleHandler" >}}">LifecycleHandler</a>)

    创建容器后立即调用 postStart。如果处理程序失败，则容器将根据其重新启动策略终止并重新启动。
    容器的其他管理阻塞直到钩子完成。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/containers/container-lifecycle-hooks/#container-hooks


  - **lifecycle.preStop** (<a href="{{< ref "../workload-resources/pod-v1#LifecycleHandler" >}}">LifecycleHandler</a>)

    preStop 在容器因 API 请求或管理事件（如存活态探针/启动探针失败、抢占、资源争用等）而终止之前立即调用。
    如果容器崩溃或退出，则不会调用处理程序。Pod 的终止宽限期倒计时在 preStop 钩子执行之前开始。
    无论处理程序的结果如何，容器最终都会在 Pod 的终止宽限期内终止（除非被终结器延迟）。
    容器的其他管理会阻塞，直到钩子完成或达到终止宽限期。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/containers/container-lifecycle-hooks/#container-hooks


- **terminationMessagePath** (string)

  可选字段。挂载到容器文件系统的一个路径，容器终止消息写入到该路径下的文件中。
  写入的消息旨在成为简短的最终状态，例如断言失败消息。如果大于 4096 字节，将被节点截断。
  所有容器的总消息长度将限制为 12 KB。默认为 `/dev/termination-log`。无法更新。

- **terminationMessagePolicy** (string)

  指示应如何填充终止消息。字段值 `File` 将使用 terminateMessagePath 的内容来填充成功和失败的容器状态消息。
  如果终止消息文件为空并且容器因错误退出，`FallbackToLogsOnError` 将使用容器日志输出的最后一块。
  日志输出限制为 2048 字节或 80 行，以较小者为准。默认为 `File`。无法更新。

- **livenessProbe** (<a href="{{< ref "../workload-resources/pod-v1#Probe" >}}">Probe</a>)

  定期探针容器活跃度。如果探针失败，容器将重新启动。无法更新。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle#container-probes

- **readinessProbe** (<a href="{{< ref "../workload-resources/pod-v1#Probe" >}}">Probe</a>)

  定期探测容器服务就绪情况。如果探针失败，容器将被从服务端点中删除。无法更新。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle#container-probes

- **startupProbe** (<a href="{{< ref "../workload-resources/pod-v1#Probe" >}}">Probe</a>)

  startupProbe 表示 Pod 已成功初始化。如果设置了此字段，则此探针成功完成之前不会执行其他探针。
  如果这个探针失败，Pod 会重新启动，就像存活态探针失败一样。
  这可用于在 Pod 生命周期开始时提供不同的探针参数，此时加载数据或预热缓存可能需要比稳态操作期间更长的时间。
  这无法更新。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle#container-probes

### 安全上下文

- **securityContext** (SecurityContext)

  SecurityContext 定义了容器应该运行的安全选项。如果设置，SecurityContext 的字段将覆盖
  PodSecurityContext 的等效字段。更多信息：
  https://kubernetes.io/zh-cn/docs/tasks/configure-pod-container/security-context/

  SecurityContext 保存将应用于容器的安全配置。某些字段在 SecurityContext 和 PodSecurityContext 中都存在。
  当两者都设置时，SecurityContext 中的值优先。


  - **securityContext.runAsUser** (int64)

    运行容器进程入口点的 UID。如果未指定，则默认为镜像元数据中指定的用户。
    也可以在 PodSecurityContext 中设置。
    如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在 SecurityContext 中指定的值优先。
    注意，`spec.os.name` 为 "windows" 时不能设置该字段。


  - **securityContext.runAsNonRoot** (boolean)

    指示容器必须以非 root 用户身份运行。
    如果为 true，kubelet 将在运行时验证镜像，以确保它不会以 UID 0（root）身份运行，如果是，则无法启动容器。
    如果未设置或为 false，则不会执行此类验证。也可以在 PodSecurityContext 中设置。
    如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在 SecurityContext 中指定的值优先。


  - **securityContext.runAsGroup** (int64)

    运行容器进程入口点的 GID。如果未设置，则使用运行时默认值。也可以在 PodSecurityContext 中设置。
    如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在 SecurityContext 中指定的值优先。
    注意，`spec.os.name` 为 "windows" 时不能设置该字段。


  - **securityContext.readOnlyRootFilesystem** (boolean)

    此容器是否具有只读根文件系统。默认为 false。注意，`spec.os.name` 为 "windows" 时不能设置该字段。


  - **securityContext.procMount** (string)

    procMount 表示用于容器的 proc 挂载类型。默认值为 `DefaultProcMount`，
    它针对只读路径和掩码路径使用容器运行时的默认值。此字段需要启用 ProcMountType 特性门控。
    注意，`spec.os.name` 为 "windows" 时不能设置此字段。


  - **securityContext.privileged** (boolean)

    以特权模式运行容器。特权容器中的进程本质上等同于主机上的 root。默认为 false。
    注意，`spec.os.name` 为 "windows" 时不能设置此字段。


  - **securityContext.allowPrivilegeEscalation** (boolean)

    allowPrivilegeEscalation 控制进程是否可以获得比其父进程更多的权限。此布尔值直接控制是否在容器进程上设置
    `no_new_privs` 标志。allowPrivilegeEscalation 在容器处于以下状态时始终为 true：

    1. 以特权身份运行
    2. 具有 `CAP_SYS_ADMIN`

    请注意，当 `spec.os.name` 为 "windows" 时，无法设置此字段。


  - **securityContext.capabilities** (Capabilities)

    运行容器时添加或放弃的权能（Capabilities）。默认为容器运行时所授予的权能集合。
    注意，`spec.os.name` 为 "windows" 时不能设置此字段。

    **在运行中的容器中添加和放弃 POSIX 权能。**

    - **securityContext.capabilities.add** ([]string)

      新增权能。

    - **securityContext.capabilities.drop** ([]string)

      放弃权能。


  - **securityContext.seccompProfile** (SeccompProfile)

    此容器使用的 seccomp 选项。如果在 Pod 和容器级别都提供了 seccomp 选项，则容器级别的选项会覆盖 Pod 级别的选项设置。
    注意，`spec.os.name` 为 "windows" 时不能设置此字段。

    **SeccompProfile 定义 Pod 或容器的 seccomp 配置文件设置。只能设置一个配置文件源。**


    - **securityContext.seccompProfile.type** (string)，必需

      type 指示应用哪种 seccomp 配置文件。有效的选项有：
      
      - `Localhost` - 应使用在节点上的文件中定义的配置文件。
      - `RuntimeDefault` - 应使用容器运行时的默认配置文件。
      - `Unconfined` - 不应用任何配置文件。
     

    - **securityContext.seccompProfile.localhostProfile** (string)

      localhostProfile 指示应使用的在节点上的文件，文件中定义了配置文件。
      该配置文件必须在节点上先行配置才能使用。
      必须是相对于 kubelet 所配置的 seccomp 配置文件位置下的下级路径。
      仅当 type 为 "Localhost" 时才必须设置。


  - **securityContext.seLinuxOptions** (SELinuxOptions)

    要应用到容器上的 SELinux 上下文。如果未设置此字段，容器运行时将为每个容器分配一个随机的 SELinux 上下文。
    也可以在 PodSecurityContext 中设置。如果同时在 SecurityContext 和 PodSecurityContext 中设置，
    则在 SecurityContext 中指定的值优先。注意，`spec.os.name` 为 "windows" 时不能设置此字段。

    <a name="SELinuxOptions"></a>
    **SELinuxOptions 是要应用到容器上的标签。**


    - **securityContext.seLinuxOptions.level** （string）

      level 是应用于容器的 SELinux 级别标签。

    - **securityContext.seLinuxOptions.role** （string）

      role 是应用于容器的 SELinux 角色标签。

    - **securityContext.seLinuxOptions.type** （string）

      type 是适用于容器的 SELinux 类型标签。

    - **securityContext.seLinuxOptions.user** （string）

      user 是应用于容器的 SELinux 用户标签。


  - **securityContext.windowsOptions** （WindowsSecurityContextOptions）

    要应用于所有容器上的特定于 Windows 的设置。如果未指定，将使用 PodSecurityContext 中的选项。
    如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在 SecurityContext 中指定的值优先。
    注意，`spec.os.name` 为 "linux" 时不能设置此字段。

    <a name="WindowsSecurityContextOptions"></a>
    **WindowsSecurityContextOptions 包含特定于 Windows 的选项和凭据。**


    - **securityContext.windowsOptions.gmsaCredentialSpec** （string）

      gmsaCredentialSpec 是 [GMSA 准入 Webhook](https://github.com/kubernetes-sigs/windows-gmsa)
      内嵌由 gmsaCredentialSpecName 字段所指定的 GMSA 凭证规约的内容的地方。


    - **securityContext.windowsOptions.hostProcess** （boolean）

      hostProcess 确定容器是否应作为 "主机进程" 容器运行。
      此字段是 Alpha 级别的，只有启用 WindowsHostProcessContainers 特性门控的组件才会处理。
      设置此字段而不启用特性门控是，在验证 Pod 时将发生错误。
      一个 Pod 的所有容器必须具有相同的有效 hostProcess 值（不允许混合设置了 hostProcess 容器和未设置 hostProcess 的容器）。
      此外，如果 hostProcess 为 true，则 hostNetwork 也必须设置为 true。


    - **securityContext.windowsOptions.runAsUserName** （string）

      Windows 中运行容器进程入口点的用户名。如果未指定，则默认为镜像元数据中指定的用户。
      也可以在 PodSecurityContext 中设置。
      如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在 SecurityContext 中指定的值优先。

### 调试

- **stdin** （boolean）

  此容器是否应在容器运行时为 stdin 分配缓冲区。如果未设置，从容器中的 stdin 读取将始终导致 EOF。
  默认为 false。

- **stdinOnce** （boolean）

  容器运行时是否应在某个 attach 打开 stdin 通道后关闭它。当 stdin 为 true 时，stdin 流将在多个 attach 会话中保持打开状态。
  如果 stdinOnce 设置为 true，则 stdin 在容器启动时打开，在第一个客户端连接到 stdin 之前为空，
  然后保持打开并接受数据，直到客户端断开连接，此时 stdin 关闭并保持关闭直到容器重新启动。
  如果此标志为 false，则从 stdin 读取的容器进程将永远不会收到 EOF。默认为 false。

- **tty** （boolean）
  这个容器是否应该为自己分配一个 TTY，同时需要设置 `stdin` 为真。默认为 false。

## EphemeralContainer {#EphemeralContainer}

EphemeralContainer 是一个临时容器，你可以将其添加到现有 Pod 以用于用户发起的活动，例如调试。
临时容器没有资源或调度保证，它们在退出或 Pod 被移除或重新启动时不会重新启动。
如果临时容器导致 Pod 超出其资源分配，kubelet 可能会驱逐 Pod。

要添加临时容器，请使用现有 Pod 的 `ephemeralcontainers` 子资源。临时容器不能被删除或重新启动。

<hr>

- **name** (string)，必需

  以 DNS_LABEL 形式设置的临时容器的名称。此名称在所有容器、Init 容器和临时容器中必须是唯一的。

- **targetContainerName** (string)

  如果设置，则为 Pod 规约中此临时容器所针对的容器的名称。临时容器将在该容器的名字空间（IPC、PID 等）中运行。
  如果未设置，则临时容器使用 Pod 规约中配置的名字空间。
  
  容器运行时必须实现对此功能的支持。如果运行时不支持名字空间定位，则设置此字段的结果是未定义的。

### 镜像

- **image** (string)

  容器镜像名称。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/containers/images

- **imagePullPolicy** (string)

  镜像拉取策略。取值为 `Always`、`Never`、`IfNotPresent` 之一。
  如果指定了 `:latest` 标签，则默认为 `Always`，否则默认为 `IfNotPresent`。
  无法更新。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/containers/images#updating-images

### 入口点

- **command** ([]string)

  入口点数组。不在 Shell 中执行。如果未提供，则使用镜像的 `ENTRYPOINT`。
  变量引用 `$(VAR_NAME)` 使用容器的环境进行扩展。如果无法解析变量，则输入字符串中的引用将保持不变。
  `$$` 被简化为 `$`，这允许转义 `$(VAR_NAME)` 语法：即 `"$$(VAR_NAME)"` 将产生字符串字面值 `"$(VAR_NAME)"`。
  无论变量是否存在，转义引用都不会被扩展。无法更新。更多信息：
  https://kubernetes.io/zh-cn/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

- **args** （[]string）

  entrypoint 的参数。如果未提供，则使用镜像的 `CMD`。
  变量引用 `$(VAR_NAME)` 使用容器的环境进行扩展。如果无法解析变量，则输入字符串中的引用将保持不变。
  `$$` 被简化为 `$`，这允许转义 `$(VAR_NAME)` 语法：即 `"$$(VAR_NAME)"` 将产生字符串字面值 `"$(VAR_NAME)"`。
  无论变量是否存在，转义引用都不会被扩展。无法更新。更多信息：
  https://kubernetes.io/zh-cn/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

- **workingDir** (string)

  容器的工作目录。如果未指定，将使用容器运行时的默认值，默认值可能在容器镜像中配置。无法更新。

### 环境变量

- **env**（[]EnvVar）

  **补丁策略：基于 `name` 键合并**
  
  要在容器中设置的环境变量列表。无法更新。

  <a name="EnvVar"></a>
  **EnvVar 表示容器中存在的环境变量。**


  - **env.name** (string)，必需

    环境变量的名称。必须是 C_IDENTIFIER。

  - **env.value** (string)

    变量引用 `$(VAR_NAME)` 使用容器中先前定义的环境变量和任何服务环境变量进行扩展。
    如果无法解析变量，则输入字符串中的引用将保持不变。
    `$$` 被简化为 `$`，这允许转义 `$(VAR_NAME)` 语法：即 `"$$(VAR_NAME)"` 将产生字符串字面值 `"$(VAR_NAME)"`。
    无论变量是否存在，转义引用都不会被扩展。默认为 ""。


  - **env.valueFrom** （EnvVarSource）

    环境变量值的来源。如果取值不为空，则不能使用。

    **EnvVarSource 表示 envVar 值的源。**


    - **env.valueFrom.configMapKeyRef** （ConfigMapKeySelector）

      选择 ConfigMap 的主键。

      <a name="ConfigMapKeySelector"></a>
      **选择 ConfigMap 的主键。**


      - **env.valueFrom.configMapKeyRef.key** (string)，必需

        选择的主键。

      - **env.valueFrom.configMapKeyRef.name**（string）

        所引用 ConfigMap 的名称。更多信息：
        https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/#names


      - **env.valueFrom.configMapKeyRef.optional** （boolean）

        指定是否 ConfigMap 或其键必须已经被定义。


    - **env.valueFrom.fieldRef** （<a href="{{< ref "../common-definitions/object-field-selector#ObjectFieldSelector" >}}">ObjectFieldSelector</a>）

      选择 Pod 的一个字段：支持 `metadata.name`、`metadata.namespace`、`metadata.labels['<KEY>']`、
      `metadata.annotations['<KEY>']`、`spec.nodeName`、`spec.serviceAccountName`、`status.hostIP`、
      `status.podIP`、`status.podIPs`。


    - **env.valueFrom.resourceFieldRef** （<a href="{{< ref "../common-definitions/resource-field-selector#ResourceFieldSelector" >}}">ResourceFieldSelector</a>）

      选择容器的资源：当前仅支持资源限制和请求（`limits.cpu`、`limits.memory`、`limits.ephemeral-storage`、
      `requests.cpu`、`requests.memory` 和 `requests.ephemeral-storage`）。


    - **env.valueFrom.secretKeyRef** （SecretKeySelector）

      在 Pod 的名字空间中选择某 Secret 的主键。

      <a name="SecretKeySelector"></a>
      **SecretKeySelector 选择某 Secret 的主键。**


      - **env.valueFrom.secretKeyRef.key** (string)，必需

        要从 Secret 中选择的主键。必须是有效的主键。

      - **env.valueFrom.secretKeyRef.name**（string）

        被引用 Secret 名称。更多信息：
        https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/#names

      - **env.valueFrom.secretKeyRef.optional** （boolean）

        指定 Secret 或其主键是否必须已经定义。

- **envFrom** （[]EnvFromSource）

  在容器中填充环境变量的来源列表。在来源中定义的键名必须是 C_IDENTIFIER。
  容器启动时，所有无效键都将作为事件报告。当一个键存在于多个来源中时，与最后一个来源关联的值将优先。
  如果有重复主键，env 中定义的值将优先。无法更新。

  <a name="EnvFromSource"></a>
  **EnvFromSource 表示一组 ConfigMap 来源**


  - **envFrom.configMapRef** （ConfigMapEnvSource）

    要从中选择的 ConfigMap。

    <a name="ConfigMapEnvSource"></a>
    **ConfigMapEnvSource 选择一个 ConfigMap 来填充环境变量。目标 ConfigMap 的 data 字段的内容将键值对表示为环境变量。**


    - **envFrom.configMapRef.name**（string）

      被引用的 ConfigMap 名称。更多信息：
      https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/#names

    - **envFrom.configMapRef.optional** （boolean）

      指定所引用的 ConfigMap 是否必须已经定义。


  - **envFrom.prefix** （string）

    要在 ConfigMap 中的每个键前面附加的可选标识符。必须是C_IDENTIFIER。


  - **envFrom.secretRef** （SecretEnvSource）

    可供选择的 Secret。

    <a name="SecretEnvSource"></a>
    **SecretEnvSource 选择一个 Secret 来填充环境变量。目标 Secret 的 data 字段的内容将键值对表示为环境变量。**


    - **envFrom.secretRef.name**（string）

      被引用 ConfigMap 的名称。更多信息：
      https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/#names

    - **envFrom.secretRef.optional** （boolean）

      指定是否 Secret 必须已经被定义。

### 卷


- **volumeMounts** ([]VolumeMount)

  **补丁策略：基于 `mountPath` 键合并**
  
  要挂载到容器文件系统中的 Pod 卷。临时容器不允许子路径挂载。无法更新。

  **VolumeMount 描述在容器中卷的挂载。**


  - **volumeMounts.mountPath** (string)，必需

    容器内应安装卷的路径。不得包含 ':'。

  - **volumeMounts.name** (string)，必需

    此字段必须与卷的名称匹配。


  - **volumeMounts.mountPropagation** （string）

    mountPropagation 确定装载如何从主机传播到容器，及反向传播选项。
    如果未设置，则使用 `None`。此字段在 1.10 中为 Beta 字段。

  - **volumeMounts.readOnly** （boolean）

    如果为 true，则挂载卷为只读，否则为读写（false 或未指定）。默认值为 false。


  - **volumeMounts.subPath** （string）

    卷中的路径名，应该从该路径挂在容器的卷。默认为 "" （卷的根）。

  - **volumeMounts.subPathExpr** （string）

    应安装容器卷的卷内的扩展路径。行为类似于 `subPath`，但环境变量引用 `$(VAR_NAME)`
    使用容器的环境进行扩展。默认为 ""（卷的根）。`subPathExpr` 和 `SubPath` 是互斥的。

- **volumeDevices** ([]VolumeDevice)

  **补丁策略：基于 `devicePath` 键合并**
  
  volumeDevices 是容器要使用的块设备列表。

  <a name="VolumeDevice"></a>
  **volumeDevice 描述容器内原始块设备的映射。**


  - **volumeDevices.devicePath** (string)，必需

    devicePath 是设备将被映射到的容器内的路径。

  - **volumeDevices.name** (string)，必需

    name 必须与 Pod 中的 persistentVolumeClaim 的名称匹配。

- **resizePolicy** ([]ContainerResizePolicy)

  **原子性: 将在合并期间被替换**

  容器的资源调整策略。

  <a name="ContainerResizePolicy"></a>
  **ContainerResizePolicy 表示容器的资源大小调整策略**

  - **resizePolicy.resourceName** (string), 必需

    该资源调整策略适用的资源名称。支持的值：cpu、memory。

  
  - **resizePolicy.restartPolicy** (string), 必需

    重启策略，会在调整指定资源大小时使用该策略。如果未指定，则默认为 NotRequired。

### 生命周期

- **terminationMessagePath** (string)

  可选字段。挂载到容器文件系统的路径，用于写入容器终止消息的文件。
  写入的消息旨在成为简短的最终状态，例如断言失败消息。如果超出 4096 字节，将被节点截断。
  所有容器的总消息长度将限制为 12 KB。默认为 `/dev/termination-log`。无法更新。

- **terminationMessagePolicy** (string)

  指示应如何填充终止消息。字段值为 `File` 表示将使用 `terminateMessagePath`
  的内容来填充成功和失败的容器状态消息。
  如果终止消息文件为空并且容器因错误退出，字段值 `FallbackToLogsOnError`
  表示将使用容器日志输出的最后一块。日志输出限制为 2048 字节或 80 行，以较小者为准。
  默认为 `File`。无法更新。


### 调试

- **stdin** （boolean）

  是否应在容器运行时内为此容器 stdin 分配缓冲区。
  如果未设置，从容器中的 stdin 读数据将始终导致 EOF。默认为 false。

- **stdinOnce** （boolean）

  容器运行时是否应在某个 attach 操作打开 stdin 通道后关闭它。
  当 stdin 为 true 时，stdin 流将在多个 attach 会话中保持打开状态。
  如果 stdinOnce 设置为 true，则 stdin 在容器启动时打开，在第一个客户端连接到 stdin 之前为空，
  然后保持打开并接受数据，直到客户端断开连接，此时 stdin 关闭并保持关闭直到容器重新启动。
  如果此标志为 false，则从 stdin 读取的容器进程将永远不会收到 EOF。默认为 false。

- **tty** (boolean)

  这个容器是否应该为自己分配一个 TTY，也需要 stdin 为 true。默认为 false。

### 安全上下文

- **securityContext** (SecurityContext)

  可选字段。securityContext 定义了运行临时容器的安全选项。
  如果设置了此字段，SecurityContext 的字段将覆盖 PodSecurityContext 的等效字段。

  SecurityContext 保存将应用于容器的安全配置。
  一些字段在 SecurityContext 和 PodSecurityContext 中都存在。
  当两者都设置时，SecurityContext 中的值优先。


  - **securityContext.runAsUser** （int64）

    运行容器进程入口点的 UID。如果未指定，则默认为镜像元数据中指定的用户。
    也可以在 PodSecurityContext 中设置。如果同时在 SecurityContext 和 PodSecurityContext
    中设置，则在 SecurityContext 中指定的值优先。
    注意，`spec.os.name` 为 "windows" 时不能设置该字段。


  - **securityContext.runAsNonRoot** （boolean）

    指示容器必须以非 root 用户身份运行。如果为 true，Kubelet 将在运行时验证镜像，
    以确保它不会以 UID 0（root）身份运行，如果是，则无法启动容器。
    如果未设置或为 false，则不会执行此类验证。也可以在 PodSecurityContext 中设置。
    如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在 SecurityContext
    中指定的值优先。


  - **securityContext.runAsGroup** （int64）

    运行容器进程入口点的 GID。如果未设置，则使用运行时默认值。也可以在 PodSecurityContext 中设置。
    如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在 SecurityContext
    中指定的值优先。注意，`spec.os.name` 为 "windows" 时不能设置该字段。


  - **securityContext.readOnlyRootFilesystem** （boolean）

    此容器是否具有只读根文件系统。
    默认为 false。注意，`spec.os.name` 为 "windows" 时不能设置该字段。


  - **securityContext.procMount** （string）

    procMount 表示用于容器的 proc 挂载类型。默认值为 DefaultProcMount，
    它将容器运行时默认值用于只读路径和掩码路径。这需要启用 ProcMountType 特性门控。
    注意，`spec.os.name` 为 "windows" 时不能设置该字段。


  - **securityContext.privileged** （boolean）

    以特权模式运行容器。特权容器中的进程本质上等同于主机上的 root。默认为 false。
    注意，`spec.os.name` 为 "windows" 时不能设置该字段。


  - **securityContext.allowPrivilegeEscalation** （boolean）

    allowPrivilegeEscalation 控制进程是否可以获得比其父进程更多的权限。
    此布尔值直接控制是否在容器进程上设置 `no_new_privs` 标志。allowPrivilegeEscalation
    在容器处于以下状态时始终为 true：

    1. 以特权身份运行
    2. 具有 `CAP_SYS_ADMIN` 权能

    请注意，当 `spec.os.name` 为 "windows" 时，无法设置此字段。


  - **securityContext.capabilities** (Capabilities)

    运行容器时添加/放弃的权能。默认为容器运行时授予的默认权能集。
    注意，`spec.os.name` 为 "windows" 时不能设置此字段。

    **在运行中的容器中添加和放弃 POSIX 权能。**


    - **securityContext.capabilities.add** （[]string）

      新增的权能。

    - **securityContext.capabilities.drop** （[]string）

      放弃的权能。


  - **securityContext.seccompProfile** （SeccompProfile）

    此容器使用的 seccomp 选项。如果在 Pod 和容器级别都提供了 seccomp 选项，
    则容器选项会覆盖 Pod 选项。注意，`spec.os.name` 为 "windows" 时不能设置该字段。

    **SeccompProfile 定义 Pod 或容器的 seccomp 配置文件设置。只能设置一个配置文件源。**


    - **securityContext.seccompProfile.type** (string)，必需

      type 指示将应用哪种 seccomp 配置文件。有效的选项是：
      
      - `Localhost` - 应使用在节点上的文件中定义的配置文件。
      - `RuntimeDefault` - 应使用容器运行时默认配置文件。
      - `Unconfined` - 不应应用任何配置文件。

     
    - **securityContext.seccompProfile.localhostProfile** （string）

      localhostProfile 指示应使用在节点上的文件中定义的配置文件。
      该配置文件必须在节点上预先配置才能工作。
      必须是相对于 kubelet 配置的 seccomp 配置文件位置下的子路径。
      仅当 type 为 "Localhost" 时才必须设置。


  - **securityContext.seLinuxOptions** （SELinuxOptions）

    要应用于容器的 SELinux 上下文。如果未指定，容器运行时将为每个容器分配一个随机
    SELinux 上下文。也可以在 PodSecurityContext 中设置。
    如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在 SecurityContext
    中指定的值优先。注意，`spec.os.name` 为 "windows" 时不能设置此字段。

    <a name="SELinuxOptions"></a>
    **SELinuxOptions 是要应用于容器的标签**


    - **securityContext.seLinuxOptions.level** （string）

      level 是应用于容器的 SELinux 级别标签。

    - **securityContext.seLinuxOptions.role** （string）

      role 是应用于容器的 SELinux 角色标签。

    - **securityContext.seLinuxOptions.type** （string）

      type 是适用于容器的 SELinux 类型标签。

    - **securityContext.seLinuxOptions.user** （string）

      user 是应用于容器的 SELinux 用户标签。


  - **securityContext.windowsOptions** （WindowsSecurityContextOptions）

    要应用到所有容器上的特定于 Windows 的设置。如果未指定，将使用 PodSecurityContext 中的选项。
    如果同时在 SecurityContext 和 PodSecurityContext 中设置，则在 SecurityContext
    中指定的值优先。注意，`spec.os.name` 为 "linux" 时不能设置此字段。

    <a name="WindowsSecurityContextOptions"></a>
    **WindowsSecurityContextOptions 包含特定于 Windows 的选项和凭据。**


    - **securityContext.windowsOptions.gmsaCredentialSpec** （string）

      gmsaCredentialSpec 是 [GMSA 准入 Webhook](https://github.com/kubernetes-sigs/windows-gmsa)
      内嵌由 gmsaCredentialSpecName 字段所指定的 GMSA 凭证规约内容的地方。

    - **securityContext.windowsOptions.gmsaCredentialSpecName** （string）

      gmsaCredentialSpecName 是要使用的 GMSA 凭证规约的名称。


    - **securityContext.windowsOptions.hostProcess** （boolean）

      hostProcess 确定容器是否应作为 "主机进程" 容器运行。此字段是 Alpha 级别的，只有启用了
      WindowsHostProcessContainers 特性门控的组件才会处理此字段。
      设置此字段而未启用特性门控的话，在验证 Pod 时将引发错误。
      一个 Pod 的所有容器必须具有相同的有效 hostProcess 值
      （不允许混合设置了 hostProcess 的容器和未设置 hostProcess 的容器）。
      此外，如果 hostProcess 为 true，则 hostNetwork 也必须设置为 true。


    - **securityContext.windowsOptions.runAsUserName** （string）

      Windows 中运行容器进程入口点的用户名。如果未指定，则默认为镜像元数据中指定的用户。
      也可以在 PodSecurityContext 中设置。如果同时在 SecurityContext 和 PodSecurityContext
      中设置，则在 SecurityContext 中指定的值优先。

### 不允许


- **ports**（[]ContainerPort）

  **补丁策略：基于 `containerPort` 键合并**
  
  **映射：键 `containerPort, protocol` 组合的唯一值将在合并期间保留**
  
  临时容器不允许使用端口。

  <a name="ContainerPort"></a>
  **ContainerPort 表示单个容器中的网络端口。**


  - **ports.containerPort** （int32），必需

    要在容器的 IP 地址上公开的端口号。这必须是有效的端口号 0 \< x \< 65536。

  - **ports.hostIP** （string）

    要将外部端口绑定到的主机 IP。


  - **ports.hostPort** （int32）

    要在主机上公开的端口号。如果设置了，则作为必须是一个有效的端口号，0 \< x \< 65536。
    如果指定了 hostNetwork，此值必须与 containerPort 匹配。大多数容器不需要这个配置。

 
  - **ports.name**（string）

    如果指定了，则作为端口的名称。必须是 IANA_SVC_NAME 并且在 Pod 中是唯一的。
    Pod 中的每个命名端口都必须具有唯一的名称。服务可以引用的端口的名称。

  - **ports.protocol** （string）

    端口协议。必须是 `UDP`、`TCP` 或 `SCTP` 之一。默认为 `TCP`。

- **resources** (ResourceRequirements)

  临时容器不允许使用资源。临时容器使用已分配给 Pod 的空闲资源。

  **ResourceRequirements 描述计算资源的需求。**

  
  - **resources.claims** ([]ResourceClaim)

    **映射：键 `name` 的唯一值将在合并过程中保留**

    claims 列出了此容器使用的资源名称，资源名称在 `spec.resourceClaims` 中定义。

    
    这是一个 Alpha 特性字段，需要启用 DynamicResourceAllocation 功能门控开启此特性。

    此字段不可变更，只能在容器级别设置。

    <a name="ResourceClaim"></a>
    
    **ResourceClaim 引用 `PodSpec.ResourceClaims` 中的一项。**

    - **resources.claims.name** (string)，必需
      
      `name` 必须与使用该字段 Pod 的 `pod.spec.resourceClaims`
      中的一个条目的名称相匹配。它使该资源在容器内可用。


  - **resources.limits** （map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>）

    limits 描述所允许的最大计算资源量。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/


  - **resources.requests** （map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>）

    requests 描述所需的最小计算资源量。如果对容器省略了 requests，则默认其资源请求值为 limits
    （如果已显式指定）的值，否则为实现定义的值。请求不能超过限制。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/configuration/manage-resources-containers/

- **lifecycle** (Lifecycle)

  临时容器不允许使用生命周期。

  生命周期描述了管理系统为响应容器生命周期事件应采取的行动。
  对于 postStart 和 preStop 生命周期处理程序，容器的管理会阻塞，直到操作完成，
  除非容器进程失败，在这种情况下处理程序被中止。


  - **lifecycle.postStart** （<a href="{{< ref "../workload-resources/pod-v1#LifecycleHandler" >}}">LifecycleHandler</a>）

    创建容器后立即调用 postStart。如果处理程序失败，则容器将根据其重新启动策略终止并重新启动。
    容器的其他管理阻塞直到钩子完成。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/containers/container-lifecycle-hooks/#container-hooks


  - **lifecycle.preStop** （<a href="{{< ref "../workload-resources/pod-v1#LifecycleHandler" >}}">LifecycleHandler</a>）

    preStop 在容器因 API 请求或管理事件（例如：存活态探针/启动探针失败、抢占、资源争用等）
    而终止之前立即调用。如果容器崩溃或退出，则不会调用处理程序。
    Pod 的终止宽限期倒计时在 preStop 钩子执行之前开始。
    无论处理程序的结果如何，容器最终都会在 Pod 的终止宽限期内终止（除非被终结器延迟）。
    容器的其他管理会阻塞，直到钩子完成或达到终止宽限期。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/containers/container-lifecycle-hooks/#container-hooks


- **livenessProbe** （<a href="{{< ref "../workload-resources/pod-v1#Probe" >}}">Probe</a>）

  临时容器不允许使用探针。

- **readyProbe** （<a href="{{< ref "../workload-resources/pod-v1#Probe" >}}">Probe</a>）

  临时容器不允许使用探针。

- **startupProbe** （<a href="{{< ref "../workload-resources/pod-v1#Probe" >}}">Probe</a>）

  临时容器不允许使用探针。


## LifecycleHandler {#LifecycleHandler}

LifecycleHandler 定义了应在生命周期挂钩中执行的特定操作。
必须指定一个且只能指定一个字段，tcpSocket 除外。

<hr>

- **exec** （execAction）

  Exec 指定要执行的操作。

  <a name="ExecAction"></a>
  **ExecAction 描述了 "在容器中运行" 操作。**


  - **exec.command** （[]string）

    command 是要在容器内执行的命令行，命令的工作目录是容器文件系统中的根目录（'/'）。
    该命令只是被通过 `exec` 执行，而不会单独启动一个 Shell 来运行，因此传统的
    Shell 指令（'|' 等）将不起作用。要使用某 Shell，你需要显式调用该 Shell。
    退出状态 0 被视为活动/健康，非零表示不健康。


- **httpGet** （HTTPGetAction）

  HTTPGet 指定要执行的 HTTP 请求。

  <a name="HTTPGetAction"></a>
  **HTTPGetAction 描述基于 HTTP Get 请求的操作。**


  - **httpGet.port** （IntOrString），必需

    要在容器上访问的端口的名称或编号。数字必须在 1 到 65535 的范围内。名称必须是 IANA_SVC_NAME。

    <a name="IntOrString"></a>
    **IntOrString 是一种可以包含 int32 或字符串值的类型。在 JSON 或 YAML 封组和取消编组时，
    它会生成或使用内部类型。例如，这允许你拥有一个可以接受名称或数字的 JSON 字段。**


  - **httpGet.host** （string）

    要连接的主机名，默认为 Pod IP。你可能想在 `httpHeaders` 中设置 "Host"。

  - **httpGet.httpHeaders** （[]HTTPHeader）

    要在请求中设置的自定义标头。HTTP 允许重复的标头。

    <a name="HTTPHeader"></a>
    **HTTPHeader 描述了在 HTTP 探针中使用的自定义标头**


    - **httpGet.httpHeaders.name** (string)，必需

      HTTP 头部字段名称。

    - **httpGet.httpHeaders.value** (string)，必需

      HTTP 头部字段取值。

 
  - **httpGet.path** （string）

    HTTP 服务器上的访问路径。

  - **httpGet.scheme** （string）

    用于连接到主机的方案。默认为 `HTTP`。

- **tcpSocket** （TCPSocketAction）

  已弃用。不再支持 `tcpSocket` 作为 LifecycleHandler，但为向后兼容保留之。
  当指定 `tcp` 处理程序时，此字段不会被验证，而生命周期回调将在运行时失败。

  <a name="TCPSocketAction"></a>
  **TCPSocketAction 描述基于打开套接字的动作。**


  - **tcpSocket.port** (IntOrString)，必需

    容器上要访问的端口的编号或名称。端口号必须在 1 到 65535 的范围内。
    名称必须是 IANA_SVC_NAME。

    <a name="IntOrString"></a>
    
    **IntOrString 是一种可以保存 int32 或字符串值的类型。在 JSON 或 YAML 编组和解组中使用时，
    会生成或使用内部类型。例如，这允许你拥有一个可以接受名称或数字的 JSON 字段。**


  - **tcpSocket.host** （string）

    可选字段。要连接的主机名，默认为 Pod IP。

## NodeAffinity {#NodeAffinity}

节点亲和性是一组节点亲和性调度规则。

<hr>


- **preferredDuringSchedulingIgnoredDuringExecution** （[]PreferredSchedulingTerm）

  调度程序会更倾向于将 Pod 调度到满足该字段指定的亲和性表达式的节点，
  但它可能会选择违反一个或多个表达式的节点。最优选的节点是权重总和最大的节点，
  即对于满足所有调度要求（资源请求、requiredDuringScheduling 亲和表达式等）的每个节点，
  通过迭代该字段的元素来计算总和如果节点匹配相应的 matchExpressions，则将 "权重" 添加到总和中； 
  具有最高总和的节点是最优选的。

  空的首选调度条件匹配所有具有隐式权重 0 的对象（即它是一个 no-op 操作）。
  null 值的首选调度条件不匹配任何对象（即也是一个 no-op 操作）。


  - **preferredDuringSchedulingIgnoredDuringExecution.preference** (NodeSelectorTerm)，必需

    与相应权重相关联的节点选择条件。

    null 值或空值的节点选择条件不会匹配任何对象。这些条件的请求按逻辑与操作组合。
    TopologySelectorTerm 类型实现了 NodeSelectorTerm 的一个子集。


    - **preferredDuringSchedulingIgnoredDuringExecution.preference.matchExpressions** （[]<a href="{{< ref "../common-definitions/node-selector-requirement" >}}">NodeSelectorRequirement</a>）

      按节点标签列出的节点选择条件列表。

    - **preferredDuringSchedulingIgnoredDuringExecution.preference.matchFields** （[]<a href="{{< ref "../common-definitions/node-selector-requirement" >}}">NodeSelectorRequirement</a>）

      按节点字段列出的节点选择要求列表。


  - **preferredDuringSchedulingIgnoredDuringExecution.weight** (int32)，必需

    与匹配相应的 nodeSelectorTerm 相关的权重，范围为 1-100。


- **requiredDuringSchedulingIgnoredDuringExecution** （NodeSelector）

  如果在调度时不满足该字段指定的亲和性要求，则不会将 Pod 调度到该节点上。
  如果在 Pod 执行期间的某个时间点不再满足此字段指定的亲和性要求（例如：由于更新），
  系统可能会或可能不会尝试最终将 Pod 从其节点中逐出。

  <a name="NodeSelector"></a>
  **一个节点选择器代表一个或多个标签查询结果在一组节点上的联合；换言之，
  它表示由节点选择器项表示的选择器的逻辑或组合。**


  - **requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms** ([]NodeSelectorTerm)，必需

    必需的字段。节点选择条件列表。这些条件按逻辑或操作组合。

    null 值或空值的节点选择器条件不匹配任何对象。这里的条件是按逻辑与操作组合的。
    TopologySelectorTerm 类型实现了 NodeSelectorTerm 的一个子集。


    - **requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms.matchExpressions** （[]<a href="{{< ref "../common-definitions/node-selector-requirement" >}}">NodeSelectorRequirement</a>）

      按节点标签列出的节点选择器需求列表。

    - **requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms.matchFields** （[]<a href="{{< ref "../common-definitions/node-selector-requirement" >}}">NodeSelectorRequirement</a>）

      按节点字段列出的节点选择器要求列表。

## PodAffinity {#PodAffinity}

Pod 亲和性是一组 Pod 间亲和性调度规则。

<hr>


- **preferredDuringSchedulingIgnoredDuringExecution** ([]WeightedPodAffinityTerm)

  调度器会更倾向于将 Pod 调度到满足该字段指定的亲和性表达式的节点，
  但它可能会选择违反一个或多个表达式的节点。最优选择是权重总和最大的节点，
  即对于满足所有调度要求（资源请求、`requiredDuringScheduling` 亲和表达式等）的每个节点，
  通过迭代该字段的元素来计算总和，如果节点具有与相应 `podAffinityTerm`
  匹配的 Pod，则将“权重”添加到总和中； 
  具有最高总和的节点是最优选的。

  <a name="WeightedPodAffinityTerm"></a>
  **所有匹配的 WeightedPodAffinityTerm 字段的权重都是按节点累计的，以找到最优选的节点。**


  - **preferredDuringSchedulingIgnoredDuringExecution.podAffinityTerm** (PodAffinityTerm)，必需

    必需的字段。一个 Pod 亲和性条件，对应一个与相应的权重值。

    <a name="PodAffinityTerm"></a>
    定义一组 Pod（即那些与给定名字空间相关的标签选择算符匹配的 Pod 集合），
    当前 Pod 应该与所选 Pod 集合位于同一位置（亲和性）或位于不同位置（反亲和性），
    其中“在同一位置”意味着运行在一个节点上，其键 `topologyKey` 的标签值与运行所选 Pod
    集合中的某 Pod 的任何节点上的标签值匹配。


    - **preferredDuringSchedulingIgnoredDuringExecution.podAffinityTerm.topologyKey** (string)，必需

      此 Pod 应与指定名字空间中与标签选择算符匹配的 Pod 集合位于同一位置（亲和性）
      或位于不同位置（反亲和性），这里的“在同一位置”意味着运行在一个节点上，其键名为
      `topologyKey` 的标签值与运行所选 Pod 集合中的某 Pod 的任何节点上的标签值匹配。
      不允许使用空的 `topologyKey`。


    - **preferredDuringSchedulingIgnoredDuringExecution.podAffinityTerm.labelSelector** （<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>）

      对一组资源的标签查询，在这里资源为 Pod。


    - **preferredDuringSchedulingIgnoredDuringExecution.podAffinityTerm.namespaceSelector** （<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>）

      对条件所适用的名字空间集合的标签查询。
      此条件会被应用到此字段所选择的名字空间和 namespaces 字段中列出的名字空间的组合之上。
      选择算符为 null 和 namespaces 列表为 null 值或空表示“此 Pod 的名字空间”。
      空的选择算符 ({}) 可用来匹配所有名字空间。


    - **preferredDuringSchedulingIgnoredDuringExecution.podAffinityTerm.namespaces** （[]string）

      namespaces 指定此条件所适用的名字空间，是一个静态列表。
      此条件会被应用到 namespaces 字段中列出的名字空间和由 namespaceSelector 选中的名字空间上。
      namespaces 列表为 null 或空，以及 namespaceSelector 值为 null 均表示“此 Pod 的名字空间”。


  - **preferredDuringSchedulingIgnoredDuringExecution.weight** (int32)，必需

    weight 是匹配相应 `podAffinityTerm` 条件的权重，范围为 1-100。


- **requiredDuringSchedulingIgnoredDuringExecution** （[]PodAffinityTerm）

  如果在调度时不满足该字段指定的亲和性要求，则该 Pod 不会被调度到该节点上。
  如果在 Pod 执行期间的某个时间点不再满足此字段指定的亲和性要求（例如：由于 Pod 标签更新），
  系统可能会也可能不会尝试最终将 Pod 从其节点中逐出。
  当此列表中有多个元素时，每个 `podAffinityTerm` 对应的节点列表是取其交集的，即必须满足所有条件。

  <a name="PodAffinityTerm"></a>
  定义一组 Pod（即那些与给定名字空间相关的标签选择算符匹配的 Pod 集合），当前 Pod 应该与该
  Pod 集合位于同一位置（亲和性）或不位于同一位置（反亲和性）。
  这里的“位于同一位置”含义是运行在一个节点上。基于 `topologyKey` 字段所给的标签键名，
  检查所选 Pod 集合中各个 Pod 所在的节点上的标签值，标签值相同则认作“位于同一位置”。


  - **requiredDuringSchedulingIgnoredDuringExecution.topologyKey** (string)，必需

    此 Pod 应与指定名字空间中与标签选择算符匹配的 Pod 集合位于同一位置（亲和性）
    或不位于同一位置（反亲和性），
    这里的“位于同一位置”含义是运行在一个节点上。基于 `topologyKey` 字段所给的标签键名，
    检查所选 Pod 集合中各个 Pod 所在的节点上的标签值，标签值相同则认作“位于同一位置”。
    不允许使用空的 `topologyKey`。


  - **requiredDuringSchedulingIgnoredDuringExecution.labelSelector** （<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>）

    对一组资源的标签查询，在这里资源为 Pod。


  - **requiredDuringSchedulingIgnoredDuringExecution.namespaceSelector** （<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>）

    对条件所适用的名字空间集合的标签查询。
    当前条件将应用于此字段选择的名字空间和 namespaces 字段中列出的名字空间。
    选择算符为 null 和 namespaces 列表为 null 或空值表示“此 Pod 的名字空间”。
    空选择算符 ({}) 能够匹配所有名字空间。



  - **requiredDuringSchedulingIgnoredDuringExecution.namespaces** （[]string）

    namespaces 指定当前条件所适用的名字空间名称的静态列表。
    当前条件适用于此字段中列出的名字空间和由 namespaceSelector 选中的名字空间。
    namespaces 列表为 null 或空，以及 namespaceSelector 为 null 表示“此 Pod 的名字空间”。

## PodAntiAffinity {#PodAntiAffinity}

Pod 反亲和性是一组 Pod 间反亲和性调度规则。

<hr>

- **preferredDuringSchedulingIgnoredDuringExecution** ([]WeightedPodAffinityTerm)

  调度器更倾向于将 Pod 调度到满足该字段指定的反亲和性表达式的节点，
  但它可能会选择违反一个或多个表达式的节点。
  最优选的节点是权重总和最大的节点，即对于满足所有调度要求（资源请求、`requiredDuringScheduling`
  反亲和性表达式等）的每个节点，通过遍历元素来计算总和如果节点具有与相应 `podAffinityTerm`
  匹配的 Pod，则此字段并在总和中添加"权重"；具有最高加和的节点是最优选的。

  <a name="WeightedPodAffinityTerm"></a>
  **所有匹配的 WeightedPodAffinityTerm 字段的权重都是按节点添加的，以找到最优选的节点。**


  - **preferredDuringSchedulingIgnoredDuringExecution.podAffinityTerm** (PodAffinityTerm)，必需

    必需的字段。一个 Pod 亲和性条件，与相应的权重相关联。

    <a name="PodAffinityTerm"></a>
    定义一组 Pod（即那些与给定名字空间相关的标签选择算符匹配的 Pod 集合），
    当前 Pod 应该与所选 Pod 集合位于同一位置（亲和性）或不位于同一位置（反亲和性），
    其中 "在同一位置" 意味着运行在一个节点上，其键 `topologyKey` 的标签值与运行所选 Pod
    集合中的某 Pod 的任何节点上的标签值匹配。


    - **preferredDuringSchedulingIgnoredDuringExecution.podAffinityTerm.topologyKey** (string)，必需

      此 Pod 应与指定名字空间中与标签选择算符匹配的 Pod 集合位于同一位置（亲和性）
      或不位于同一位置（反亲和性），这里的 "在同一位置" 意味着运行在一个节点上，其键名为
      `topologyKey` 的标签值与运行所选 Pod 集合中的某 Pod 的任何节点上的标签值匹配。
      不允许使用空的 `topologyKey`。


    - **preferredDuringSchedulingIgnoredDuringExecution.podAffinityTerm.labelSelector** （<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>）

      对一组资源的标签查询，在这里资源为 Pod。


    - **preferredDuringSchedulingIgnoredDuringExecution.podAffinityTerm.namespaceSelector** （<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>）

      对条件所适用的名字空间集合的标签查询。
      此条件会被应用到此字段所选择的名字空间和 namespaces 字段中列出的名字空间的组合之上。
      选择算符为 null 和 namespaces 列表为 null 值或空表示 "此 Pod 的名字空间"。
      空的选择算符 ({}) 可用来匹配所有名字空间。


    - **preferredDuringSchedulingIgnoredDuringExecution.podAffinityTerm.namespaces** （[]string）

      namespaces 指定此条件所适用的名字空间，是一个静态列表。
      此条件会被应用到 namespaces 字段中列出的名字空间和由 namespaceSelector 选中的名字空间上。
      namespaces 列表为 null 或空，以及 namespaceSelector 值为 null 均表示 "此 Pod 的名字空间"。


  - **preferredDuringSchedulingIgnoredDuringExecution.weight** (int32)，必需

    weight 是匹配相应 `podAffinityTerm` 条件的权重，范围为 1-100。


- **requiredDuringSchedulingIgnoredDuringExecution** （[]PodAffinityTerm）

  如果在调度时不满足该字段指定的反亲和性要求，则该 Pod 不会被调度到该节点上。
  如果在 Pod 执行期间的某个时间点不再满足此字段指定的反亲和性要求（例如：由于 Pod 标签更新），
  系统可能会或可能不会尝试最终将 Pod 从其节点中逐出。
  当有多个元素时，每个 `podAffinityTerm` 对应的节点列表是取其交集的，即必须满足所有条件。

  <a name="PodAffinityTerm"></a>
  定义一组 Pod（即那些与给定名字空间相关的标签选择算符匹配的 Pod 集合），当前 Pod 应该与该
  Pod 集合位于同一位置（亲和性）或不位于同一位置（反亲和性）。
  这里的 "位于同一位置" 含义是运行在一个节点上。基于 `topologyKey` 字段所给的标签键名，
  检查所选 Pod 集合中各个 Pod 所在的节点上的标签值，标签值相同则认作 "位于同一位置"。


  - **requiredDuringSchedulingIgnoredDuringExecution.topologyKey** (string)，必需

    此 Pod 应与指定名字空间中与标签选择算符匹配的 Pod 集合位于同一位置（亲和性）
    或不位于同一位置（反亲和性），
    这里的 "位于同一位置" 含义是运行在一个节点上。基于 `topologyKey` 字段所给的标签键名，
    检查所选 Pod 集合中各个 Pod 所在的节点上的标签值，标签值相同则认作 "位于同一位置"。
    不允许使用空的 `topologyKey`。


  - **requiredDuringSchedulingIgnoredDuringExecution.labelSelector** （<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>）

    对一组资源的标签查询，在这里资源为 Pod。


  - **requiredDuringSchedulingIgnoredDuringExecution.namespaceSelector** （<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>）

    对条件所适用的名字空间集合的标签查询。
    当前条件将应用于此字段选择的名字空间和 namespaces 字段中列出的名字空间。
    选择算符为 null 和 namespaces 列表为 null 或空值表示 “此 Pod 的名字空间”。
    空选择算符 ({}) 能够匹配所有名字空间。



  - **requiredDuringSchedulingIgnoredDuringExecution.namespaces** （[]string）

    namespaces 指定当前条件所适用的名字空间名称的静态列表。
    当前条件适用于此字段中列出的名字空间和由 namespaceSelector 选中的名字空间。
    namespaces 列表为 null 或空，以及 namespaceSelector 为 null 表示 “此 Pod 的名字空间”。


## 探针 {#Probe}

探针描述了要对容器执行的健康检查，以确定它是否处于活动状态或准备好接收流量。

<hr>

- **exec** （execAction）

  exec 指定要执行的操作。

  <a name="ExecAction"></a>
  **ExecAction 描述了 "在容器中运行" 操作。**


  - **exec.command** （[]string）

    command 是要在容器内执行的命令行，命令的工作目录是容器文件系统中的根目录（'/'）。
    该命令只是通过 `exec` 执行，而不会启动 Shell，因此传统的 Shell 指令（'|' 等）将不起作用。
    要使用某 Shell，你需要显式调用该 Shell。
    退出状态 0 被视为存活/健康，非零表示不健康。

- **httpGet** （HTTPGetAction）

  httpGet 指定要执行的 HTTP 请求。

  <a name="HTTPGetAction"></a>
  **HTTPGetAction 描述基于 HTTP Get 请求的操作。**


  - **httpGet.port** (IntOrString)，必需

    容器上要访问的端口的名称或端口号。端口号必须在 1 到 65535 内。名称必须是 IANA_SVC_NAME。

    <a name="IntOrString"></a>
    `IntOrString` 是一种可以保存 int32 或字符串值的类型。在 JSON 或 YAML 编组和解组时，
    它会生成或使用内部类型。例如，这允许你拥有一个可以接受名称或数字的 JSON 字段。


  - **httpGet.host** （string）

    要连接的主机名，默认为 Pod IP。你可能想在 `httpHeaders` 中设置 "Host"。


  - **httpGet.httpHeaders** （[]HTTPHeader）

    要在请求中设置的自定义 HTTP 标头。HTTP 允许重复的标头。

    <a name="HTTPHeader"></a>
    **HTTPHeader 描述了在 HTTP 探针中使用的自定义标头。**


    - **httpGet.httpHeaders.name** (string)，必需

      HTTP 头部域名称。

    - **httpGet.httpHeaders.value** (string)，必需

      HTTP 头部域值。

 
  - **httpGet.path** （string）

    HTTP 服务器上的访问路径。

  - **httpGet.scheme** （string）

    用于连接到主机的方案。默认为 HTTP。


- **tcpSocket** （TCPSocketAction）

  tcpSocket 指定涉及 TCP 端口的操作。

  <a name="TCPSocketAction"></a>
  **`TCPSocketAction` 描述基于打开套接字的动作。**


  - **tcpSocket.port** (IntOrString)，必需

    容器上要访问的端口的端口号或名称。端口号必须在 1 到 65535 内。名称必须是 IANA_SVC_NAME。

    <a name="IntOrString"></a>
    IntOrString 是一种可以保存 int32 或字符串的类型。在 JSON 或 YAML 编组和解组时，
    它会生成或使用内部类型。例如，这允许你拥有一个可以接受名称或数字的 JSON 字段。


  - **tcpSocket.host** （string）

    可选字段。要连接的主机名，默认为 Pod IP。

- **初始延迟秒** （int32）

  容器启动后启动存活态探针之前的秒数。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle#container-probes


- **terminationGracePeriodSeconds** （int64）

  Pod 需要在探针失败时体面终止所需的时间长度（以秒为单位），为可选字段。
  宽限期是 Pod 中运行的进程收到终止信号后，到进程被终止信号强制停止之前的时间长度（以秒为单位）。
  你应该将此值设置为比你的进程的预期清理时间更长。
  如果此值为 nil，则将使用 Pod 的 `terminateGracePeriodSeconds`。
  否则，此值将覆盖 Pod 规约中设置的值。字段值值必须是非负整数。
  零值表示收到终止信号立即停止（没有机会关闭）。
  这是一个 Beta 字段，需要启用 ProbeTerminationGracePeriod 特性门控。最小值为 1。
  如果未设置，则使用 `spec.terminationGracePeriodSeconds`。

- **periodSeconds** (int32)

  探针的执行周期（以秒为单位）。默认为 10 秒。最小值为 1。

- **timeoutSeconds** (int32)

  探针超时的秒数。默认为 1 秒。最小值为 1。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle#container-probes

- **failureThreshold** (int32)

  探针成功后的最小连续失败次数，超出此阈值则认为探针失败。默认为 3。最小值为 1。

- **successThreshold** (int32)

  探针失败后最小连续成功次数，超过此阈值才会被视为探针成功。默认为 1。
  存活性探针和启动探针必须为 1。最小值为 1。

- **grpc** （GRPCAction）

  GRPC 指定涉及 GRPC 端口的操作。

  <a name="GRPCAction"></a>


  - **grpc.port** （int32），必需

    gRPC 服务的端口号。数字必须在 1 到 65535 的范围内。

  - **grpc.service** （string）

    service 是要放置在 gRPC 运行状况检查请求中的服务的名称
    （请参见 https://github.com/grpc/grpc/blob/master/doc/health-checking.md）。
    
    如果未指定，则默认行为由 gRPC 定义。

## PodStatus {#PodStatus}

PodStatus 表示有关 Pod 状态的信息。状态内容可能会滞后于系统的实际状态，
尤其是在托管 Pod 的节点无法联系控制平面的情况下。

<hr>

- **nominatedNodeName** (string)

  仅当此 Pod 抢占节点上的其他 Pod 时才设置 `nominatedNodeName`，
  但抢占操作的受害者会有体面终止期限，因此此 Pod 无法立即被调度。
  此字段不保证 Pod 会在该节点上调度。
  如果其他节点更早进入可用状态，调度器可能会决定将 Pod 放置在其他地方。
  调度器也可能决定将此节点上的资源分配给优先级更高的、在抢占操作之后创建的 Pod。
  因此，当 Pod 被调度时，该字段可能与 Pod 规约中的 nodeName 不同。

- **hostIP** (string)

  Pod 被调度到的主机的 IP 地址。如果尚未被调度，则为字段为空。

- **startTime** (Time)

  kubelet 确认 Pod 对象的日期和时间，格式遵从 RFC 3339。
  此时间点处于 kubelet 为 Pod 拉取容器镜像之前。

  Time 是 `time.Time` 的包装器，支持正确编组为 YAML 和 JSON。
  time 包所提供的许多工厂方法都有包装器。

- **phase** (string)

  Pod 的 phase 是对 Pod 在其生命周期中所处位置的简单、高级摘要。
  conditions 数组、reason 和 message 字段以及各个容器的 status 数组包含有关 Pod
  状态的进一步详细信息。phase 的取值有五种可能性：
  
  - `Pending`：Pod 已被 Kubernetes 系统接受，但尚未创建容器镜像。
   这包括 Pod 被调度之前的时间以及通过网络下载镜像所花费的时间。
  - `Running`：Pod 已经被绑定到某个节点，并且所有的容器都已经创建完毕。至少有一个容器仍在运行，或者正在启动或重新启动过程中。
  - `Succeeded`：Pod 中的所有容器都已成功终止，不会重新启动。
  - `Failed`：Pod 中的所有容器都已终止，并且至少有一个容器因故障而终止。
    容器要么以非零状态退出，要么被系统终止。
  - `Unknown`：由于某种原因无法获取 Pod 的状态，通常是由于与 Pod 的主机通信时出错。

  
  更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle#pod-phase

- **message** (string)

   一条人类可读的消息，标示有关 Pod 为何处于这种情况的详细信息。

- **reason** (string)

   一条简短的驼峰式命名的消息，指示有关 Pod 为何处于此状态的详细信息。例如 'Evicted'。


- **podIP** （string）

   分配给 Pod 的 IP 地址。至少在集群内可路由。如果尚未分配则为空。

- **podIPs** （[]PodIP）

  **补丁策略：基于 `ip` 键合并**
  
  podIPs 保存分配给 Pod 的 IP 地址。如果指定了该字段，则第 0 个条目必须与 podIP 字段值匹配。
  Pod 最多可以为 IPv4 和 IPv6 各分配 1 个值。如果尚未分配 IP，则此列表为空。

  <a name="PodIP"></a>
  podIPs 字段中每个条目的 IP 地址信息。每个条目都包含：

    `ip` 字段：给出分配给 Pod 的 IP 地址。该 IP 地址至少在集群内可路由。


  - **podIP.ip** （string）

     ip 是分配给 Pod 的 IP 地址（IPv4 或 IPv6）。

- **conditions** ([]PodCondition)

   **补丁策略：基于 `ip` 键合并**
  
   Pod 的当前服务状态。更多信息：
   https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle#pod-conditions

  <a name="PodCondition"></a>
   **PodCondition 包含此 Pod 当前状况的详细信息。**

   - **conditions.status** (string)，必需

    status 是 condition 的状态。可以是 `True`、`False`、`Unknown` 之一。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle#pod-conditions

  - **conditions.type** (string)，必需

    type 是 condition 的类型。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle#pod-conditions


  - **conditions.lastProbeTime** (Time)

    上次探测 Pod 状况的时间。

    Time 是 `time.Time` 的包装器，支持正确编组为 YAML 和 JSON。
    time 包所提供的许多工厂方法都有包装器。


  - **conditions.lastTransitionTime** (Time)

    上次 Pod 状况从一种状态变为另一种状态的时间。

    Time 是 `time.Time` 的包装器，支持正确编组为 YAML 和 JSON。
    time 包所提供的许多工厂方法都有包装器。


  - **conditions.message** (string)

    标示有关上次状况变化的详细信息的、人类可读的消息。

  - **conditions.reason** (string)

    condition 最近一次变化的唯一、一个单词、驼峰式命名原因。

- **qosClass** （string）

   根据资源要求分配给 Pod 的服务质量 (QOS) 分类。有关可用的 QOS 类，请参阅 PodQOSClass 类型。
   更多信息： https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-qos/#quality-of-service-classes


- **initContainerStatuses** （[]ContainerStatus）

  该列表在清单中的每个 Init 容器中都有一个条目。最近成功的 Init 容器会将 ready 设置为 true，
  最近启动的容器将设置 startTime。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle#pod-and-container-status

  **ContainerStatus 包含此容器当前状态的详细信息。**

- **containerStatuses** （[]ContainerStatus）

  清单中的每个容器状态在该列表中都有一个条目。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle#pod-and-container-status

  **ContainerStatus 包含此容器当前状态的详细信息。**
    
- **ephemeralContainerStatuses** （[]ContainerStatus）

  已在此 Pod 中运行的任何临时容器的状态。

  <a name="ContainerStatus"></a>
  **ContainerStatus 包含此容器当前状态的详细信息。**

- **resize** (string)

  Pod 容器所需的资源大小调整状态。如果没有待处理的资源调整大小，则它为空。
  对容器资源的任何更改都会自动将其设置为"建议"值。

## PodList {#PodList}

PodList 是 Pod 的列表。

<hr>

- **items** （[]<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>），必需

  Pod 列表。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md

- **apiVersion** （string）

  apiVersion 定义对象表示的版本化模式。服务器应将已识别的模式转换为最新的内部值，
  并可能拒绝无法识别的值。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources

- **kind**（string）

  kind 是一个字符串值，表示此对象表示的 REST 资源。服务器可以从客户端提交请求的端点推断出资源类别。
  无法更新。采用驼峰式命名。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **metadata** （<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>）

  标准的列表元数据。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

## 操作 {#Operations}

<hr>

### `get` 读取指定的 Pod

#### HTTP 请求

GET /api/v1/namespaces/{namespace}/pods/{name}

#### 参数

- **name** (**路径参数**): string，必需

  Pod 的名称

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): OK

401: Unauthorized

### `get` 读取指定 Pod 的 ephemeralcontainers

#### HTTP 请求

GET /api/v1/namespaces/{namespace}/pods/{name}/ephemeralcontainers

#### 参数

- **name** (**路径参数**): string，必需

  Pod 的名称

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): OK

401: Unauthorized


### `get` 读取指定 Pod 的日志

#### HTTP 请求

GET /api/v1/namespaces/{namespace}/pods/{name}/log

#### 参数

- **name** (**路径参数**): string，必需

  Pod 的名称。

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **container** (**查询参数**): string

  为其流式传输日志的容器。如果 Pod 中有一个容器，则默认为仅容器。

- **follow** (**查询参数**)：boolean

  跟踪 Pod 的日志流。默认为 false。

- **insecureSkipTLSVerifyBackend** (**查询参数**)：boolean

  `insecureSkipTLSVerifyBackend` 表示 API 服务器不应确认它所连接的后端的服务证书的有效性。
  这将使 API 服务器和后端之间的 HTTPS 连接不安全。
  这意味着 API 服务器无法验证它接收到的日志数据是否来自真正的 kubelet。
  如果 kubelet 配置为验证 API 服务器的 TLS 凭据，这并不意味着与真实 kubelet
  的连接容易受到中间人攻击（例如，攻击者无法拦截来自真实 kubelet 的实际日志数据）。

- **limitBytes** (**查询参数**): integer

  如果设置，则表示在终止日志输出之前从服务器读取的字节数。
  设置此参数可能导致无法显示完整的最后一行日志记录，并且可能返回略多于或略小于指定限制。

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **previous** (**查询参数**)：boolean

  返回之前终止了的容器的日志。默认为 false。

- **sinceSeconds** (**查询参数**): integer

  显示日志的当前时间之前的相对时间（以秒为单位）。如果此值早于 Pod 启动时间，
  则仅返回自 Pod 启动以来的日志。如果此值是将来的值，则不会返回任何日志。
  只能指定 `sinceSeconds` 或 `sinceTime` 之一。

- **tailLines** (**查询参数**): integer

  如果设置，则从日志末尾开始显示的行数。如果未指定，则从容器创建或 `sinceSeconds` 或
  `sinceTime` 时刻显示日志。

- **timestamps** (**查询参数**)：boolean

  如果为 true，则在每行日志输出的开头添加 RFC3339 或 RFC3339Nano 时间戳。默认为 false。

#### 响应

200 (string): OK

401: Unauthorized

### `get` 读取指定 Pod 的状态

#### HTTP 请求

GET /api/v1/namespaces/{namespace}/pods/{name}/status

#### 参数

- **name** (**路径参数**): string，必需

  Pod 的名称

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): OK

401: Unauthorized

### `list` 列出或观察 Pod 种类的对象

#### HTTP 请求

GET /api/v1/namespaces/{namespace}/pods

#### 参数

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **allowWatchBookmarks** (**查询参数**)：boolean

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

- **watch** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应


200 (<a href="{{< ref "../workload-resources/pod-v1#PodList" >}}">PodList</a>): OK

401: Unauthorized

### `list` 列出或观察 Pod 种类的对象

#### HTTP 请求

GET /api/v1/pods

#### 参数

- **allowWatchBookmarks** (**查询参数**)：boolean

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


- **timeoutSeconds** (**查询参数**)：integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

- **watch** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-v1#PodList" >}}">PodList</a>): OK

401: Unauthorized

### `create` 创建一个 Pod
#### HTTP 请求

POST /api/v1/namespaces/{namespace}/pods

#### 参数

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**：<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): OK

201 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): Created

202 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): Accepted

401: Unauthorized

### `update` 替换指定的 Pod

#### HTTP 请求

PUT /api/v1/namespaces/{namespace}/pods/{name}

#### 参数

- **name** (**路径参数**): string，必需

  Pod 的名称。

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**：<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): OK

201 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): Created

401: Unauthorized

### `update` 替换指定 Pod 的 ephemeralcontainers

#### HTTP 请求

PUT /api/v1/namespaces/{namespace}/pods/{name}/ephemeralcontainers

#### 参数

- **name** (**路径参数**): string，必需

  Pod 的名称

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**：<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): OK

201 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): Created

401: Unauthorized

### `update` 替换指定 Pod 的状态

#### HTTP 请求

PUT /api/v1/namespaces/{namespace}/pods/{name}/status

#### 参数

- **name** (**路径参数**): string，必需

  Pod 的名称

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**：<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): OK

201 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): Created

401: Unauthorized

### `patch` 部分更新指定 Pod

#### HTTP 请求

PATCH /api/v1/namespaces/{namespace}/pods/{name}

#### 参数

- **name** (**路径参数**): string，必需

  Pod 的名称

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**：<a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): OK

201 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): Created

401: Unauthorized

### `patch` 部分更新指定 Pod 的 ephemeralcontainers

#### HTTP 请求

PATCH /api/v1/namespaces/{namespace}/pods/{name}/ephemeralcontainers

#### 参数

- **name** (**路径参数**): string，必需

  Pod 的名称。

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**：<a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

- **dryRun** (**查询参数**): string

   <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): OK

201 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): Created

401: Unauthorized

### `patch` 部分更新指定 Pod 的状态

#### HTTP 请求

PATCH /api/v1/namespaces/{namespace}/pods/{name}/status

#### 参数

- **name** (**路径参数**): string，必需

  Pod 的名称。

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**：<a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **fieldManager** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>

- **fieldValidation** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>

- **force** (**查询参数**)：boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>

- **pretty** (**查询参数**)：string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): OK

201 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): Created

401: Unauthorized

### `delete` 删除一个 Pod

#### HTTP 请求

DELETE /api/v1/namespaces/{namespace}/pods/{name}

#### 参数

- **name** (**路径参数**): string，必需

  Pod 的名称。

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**：<a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

- **dryRun** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>

- **gracePeriodSeconds** (**查询参数**): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>

- **pretty** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

- **propagationPolicy** (**查询参数**): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### 响应

200 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): OK

202 (<a href="{{< ref "../workload-resources/pod-v1#Pod" >}}">Pod</a>): Accepted

401: Unauthorize

### `deletecollection` 删除 Pod 的集合

#### HTTP 请求

DELETE /api/v1/namespaces/{namespace}/pods

#### 参数

- **namespace** (**路径参数**): string，必需

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>

- **body**：<a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

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

