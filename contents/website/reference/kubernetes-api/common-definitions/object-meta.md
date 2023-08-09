---
api_metadata:
  apiVersion: ""
  import: "k8s.io/apimachinery/pkg/apis/meta/v1"
  kind: "ObjectMeta"
content_type: "api_reference"
description: "ObjectMeta 是所有持久化资源必须具有的元数据，其中包括用户必须创建的所有对象。"
title: "ObjectMeta"
weight: 7
---


`import "k8s.io/apimachinery/pkg/apis/meta/v1"`

ObjectMeta 是所有持久化资源必须具有的元数据，其中包括用户必须创建的所有对象。

<hr>

- **name** (string)


  name 在命名空间内必须是唯一的。创建资源时需要，尽管某些资源可能允许客户端请求自动地生成适当的名称。
  名称主要用于创建幂等性和配置定义。无法更新。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names#names

- **generateName** (string)

  generateName 是一个可选前缀，由服务器使用，**仅在**未提供 name 字段时生成唯一名称。
  如果使用此字段，则返回给客户端的名称将与传递的名称不同。该值还将与唯一的后缀组合。
  提供的值与 name 字段具有相同的验证规则，并且可能会根据所需的后缀长度被截断，以使该值在服务器上唯一。
  
  如果指定了此字段并且生成的名称存在，则服务器将不会返回 409 ——相反，它将返回 201 Created 或 500，
  原因是 ServerTimeout 指示在分配的时间内找不到唯一名称，客户端应重试（可选，在 Retry-After 标头中指定的时间之后）。
  
  仅在未指定 name 时应用。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#idempotency

- **namespace** (string)


  namespace 定义了一个值空间，其中每个名称必须唯一。空命名空间相当于 “default” 命名空间，但 “default” 是规范表示。
  并非所有对象都需要限定在命名空间中——这些对象的此字段的值将为空。
  
  必须是 DNS_LABEL。无法更新。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/namespaces

- **labels** (map[string]string)


  可用于组织和分类（确定范围和选择）对象的字符串键和值的映射。
  可以匹配 ReplicationController 和 Service 的选择算符。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/labels

- **annotations** (map[string]string)


  annotations 是一个非结构化的键值映射，存储在资源中，可以由外部工具设置以存储和检索任意元数据。
  它们不可查询，在修改对象时应保留。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/annotations

### 系统字段 {#System}

- **finalizers** ([]string)


  在从注册表中删除对象之前该字段必须为空。
  每个条目都是负责的组件的标识符，各组件将从列表中删除自己对应的条目。
  如果对象的 deletionTimestamp 非空，则只能删除此列表中的条目。
  终结器可以按任何顺序处理和删除。**没有**按照顺序执行，
  因为它引入了终结器卡住的重大风险。finalizers 是一个共享字段，
  任何有权限的参与者都可以对其进行重新排序。如果按顺序处理终结器列表，
  那么这可能导致列表中第一个负责终结器的组件正在等待列表中靠后负责终结器的组件产生的信号（字段值、外部系统或其他），
  从而导致死锁。在没有强制排序的情况下，终结者可以在它们之间自由排序，
  并且不容易受到列表中排序更改的影响。

- **managedFields** ([]ManagedFieldsEntry)


  managedFields 将 workflow-id 和版本映射到由该工作流管理的字段集。
  这主要用于内部管理，用户通常不需要设置或理解该字段。
  工作流可以是用户名、控制器名或特定应用路径的名称，如 “ci-cd”。
  字段集始终存在于修改对象时工作流使用的版本。

  <a name="ManagedFieldsEntry"></a>
  **ManagedFieldsEntry 是一个 workflow-id，一个 FieldSet，也是该字段集适用的资源的组版本。**

  - **managedFields.apiVersion** (string)


    apiVersion 定义此字段集适用的资源的版本。
    格式是 “group/version”，就像顶级 apiVersion 字段一样。
    必须跟踪字段集的版本，因为它不能自动转换。

  - **managedFields.fieldsType** (string)


    FieldsType 是不同字段格式和版本的鉴别器。
    目前只有一个可能的值：“FieldsV1”

  - **managedFields.fieldsV1** (FieldsV1)


    FieldsV1 包含类型 “FieldsV1” 中描述的第一个 JSON 版本格式。

    <a name="FieldsV1"></a>
    FieldsV1 以 JSON 格式将一组字段存储在像 Trie 这样的数据结构中。
    
    每个键或是 `.` 表示字段本身，并且始终映射到一个空集，
    或是一个表示子字段或元素的字符串。该字符串将遵循以下四种格式之一：

    1. `f:<name>`，其中 `<name>` 是结构中字段的名称，或映射中的键
    2. `v:<value>`，其中 `<value>` 是列表项的精确 json 格式值
    3. `i:<index>`，其中 `<index>` 是列表中项目的位置
    4. `k:<keys>`，其中 `<keys>` 是列表项的关键字段到其唯一值的映射。
    如果一个键映射到一个空的 Fields 值，则该键表示的字段是集合的一部分。
    
    确切的格式在 sigs.k8s.io/structured-merge-diff 中定义。

  - **managedFields.manager** (string)

    manager 是管理这些字段的工作流的标识符。

  - **managedFields.operation** (string)


    operation 是导致创建此 managedFields 表项的操作类型。
    此字段的仅有合法值是 “Apply” 和 “Update”。

  - **managedFields.subresource** (string)


    subresource 是用于更新该对象的子资源的名称，如果对象是通过主资源更新的，则为空字符串。
    该字段的值用于区分管理者，即使他们共享相同的名称。例如，状态更新将不同于使用相同管理者名称的常规更新。
    请注意，apiVersion 字段与 subresource 字段无关，它始终对应于主资源的版本。

  - **managedFields.time** (Time)


    time 是添加 managedFields 条目时的时间戳。
    如果一个字段被添加、管理器更新任一所属字段值或移除一个字段，该时间戳也会更新。
    从此条目中移除一个字段时该时间戳不会更新，因为另一个管理器将它接管了。

    <a name="Time"></a>
    **time 是 time.Time 的包装类，支持正确地序列化为 YAML 和 JSON。
    为 time 包提供的许多工厂方法提供了包装类。**

- **ownerReferences** ([]OwnerReference)


  **补丁策略：根据 `uid` 键执行合并操作**

  此对象所依赖的对象列表。如果列表中的所有对象都已被删除，则该对象将被垃圾回收。
  如果此对象由控制器管理，则此列表中的条目将指向此控制器，controller 字段设置为 true。
  管理控制器不能超过一个。

  <a name="OwnerReference"></a>
  **OwnerReference 包含足够可以让你识别属主对象的信息。
  属主对象必须与依赖对象位于同一命名空间中，或者是集群作用域的，因此没有命名空间字段。**

    被引用资源的 API 版本。


    被引用资源的类别。更多信息：
    https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds



    被引用资源的名称。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names/



    被引用资源的 uid。更多信息：
    https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names#uids

  - **ownerReferences.blockOwnerDeletion** (boolean)

    如果为 true，**并且** 如果属主具有 “foregroundDeletion” 终结器，
    则在删除此引用之前，无法从键值存储中删除属主。
    默认为 false。要设置此字段，用户需要属主的 “delete” 权限，
    否则将返回 422 (Unprocessable Entity)。

  - **ownerReferences.controller** (boolean)

    如果为 true，则此引用指向管理的控制器。

### 只读字段 {#Read-only}

- **creationTimestamp** (Time)

  creationTimestamp 是一个时间戳，表示创建此对象时的服务器时间。
  不能保证在单独的操作中按发生前的顺序设置。
  客户端不得设置此值。它以 RFC3339 形式表示，并采用 UTC。
  
  由系统填充。只读。列表为空。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

  <a name="Time"></a>
  **time 是 time.Time 的包装类，支持正确地序列化为 YAML 和 JSON。
  为 time 包提供的许多工厂方法提供了包装类。**

- **deletionGracePeriodSeconds** (int64)

  此对象从系统中删除之前允许正常终止的秒数。
  仅当设置了 deletionTimestamp 时才设置。
  只能缩短。只读。

- **deletionTimestamp** (Time)


  deletionTimestamp 是删除此资源的 RFC 3339 日期和时间。
  该字段在用户请求体面删除时由服务器设置，客户端不能直接设置。
  一旦 finalizers 列表为空，该资源预计将在此字段中的时间之后被删除
  （不再从资源列表中可见，并且无法通过名称访问）。
  只要 finalizers 列表包含项目，就阻止删除。一旦设置了 deletionTimestamp，
  该值可能不会被取消设置或在未来进一步设置，尽管它可能会缩短或在此时间之前可能会删除资源。
  例如，用户可能要求在 30 秒内删除一个 Pod。
  Kubelet 将通过向 Pod 中的容器发送体面的终止信号来做出反应。
  30 秒后，Kubelet 将向容器发送硬终止信号（SIGKILL），
  并在清理后从 API 中删除 Pod。在网络存在分区的情况下，
  此对象可能在此时间戳之后仍然存在，直到管理员或自动化进程可以确定资源已完全终止。
  如果未设置，则未请求体面删除该对象。
  
  请求体面删除时由系统填充。只读。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

  <a name="Time"></a>
  **Time 是 time.Time 的包装类，支持正确地序列化为 YAML 和 JSON。
  为 time 包提供的许多工厂方法提供了包装类。**

- **generation** (int64)

  表示期望状态的特定生成的序列号。由系统填充。只读。

- **resourceVersion** (string)

  一个不透明的值，表示此对象的内部版本，客户端可以使用该值来确定对象是否已被更改。
  可用于乐观并发、变更检测以及对资源或资源集的监听操作。
  客户端必须将这些值视为不透明的，且未更改地传回服务器。
  它们可能仅对特定资源或一组资源有效。
  
  由系统填充。只读。客户端必须将值视为不透明。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#concurrency-control-and-consistency

- **selfLink** (string)

  selfLink 是表示此对象的 URL。由系统填充。只读。
  
  **已弃用**。Kubernetes 将在 1.20 版本中停止传播该字段，并计划在 1.21 版本中删除该字段。

- **uid** (string)


  UID 是该对象在时间和空间上的唯一值。它通常由服务器在成功创建资源时生成，并且不允许使用 PUT 操作更改。
  
  由系统填充。只读。更多信息：
  https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/names#uids
