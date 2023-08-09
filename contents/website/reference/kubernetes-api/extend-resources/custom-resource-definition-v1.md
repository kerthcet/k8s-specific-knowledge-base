---
api_metadata:
  apiVersion: "apiextensions.k8s.io/v1"
  import: "k8s.io/apiextensions-apiserver/pkg/apis/apiextensions/v1"
  kind: "CustomResourceDefinition"
content_type: "api_reference"
description: "CustomResourceDefinition 表示应在 API 服务器上公开的资源。"
title: "CustomResourceDefinition"
weight: 1
---

`apiVersion: apiextensions.k8s.io/v1`

`import "k8s.io/apiextensions-apiserver/pkg/apis/apiextensions/v1"`

## CustomResourceDefinition {#CustomResourceDefinition}

CustomResourceDefinition 表示应在 API 服务器上公开的资源。其名称必须采用 `<.spec.name>.<.spec.group>` 格式。

<hr>

- **apiVersion**：apiextensions.k8s.io/v1

- **kind**：CustomResourceDefinition

- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)
  标准的对象元数据，更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

  spec 描述了用户希望资源的呈现方式。

- **status** (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinitionStatus" >}}">CustomResourceDefinitionStatus</a>)
  status 表示 CustomResourceDefinition 的实际状态。

## CustomResourceDefinitionSpec {#CustomResourceDefinitionSpec}

CustomResourceDefinitionSpec 描述了用户希望资源的呈现方式。

<hr>

- **group** (string)，必需

  group 是自定义资源的 API 组。自定义资源在 `/apis/<group>/...` 下提供。
  必须与 CustomResourceDefinition 的名称匹配（格式为 `<names.plural>.<group>`）。


- **names** (CustomResourceDefinitionNames)，必需

  names 表示自定义资源的资源和种类名称。

  <a name="CustomResourceDefinitionNames"></a>
  **CustomResourceDefinitionNames 表示提供此 CustomResourceDefinition 资源的名称。**

  - **names.kind** (string)，必需

    kind 是资源的序列化类型。它通常是驼峰命名的单数形式。自定义资源实例将使用此值作为 API 调用中的 `kind` 属性。


  - **names.plural** (string)，必需

    plural 是所提供的资源的复数名称，自定义资源在 `/apis/<group>/<version>/.../<plural>` 下提供。
    必须与 CustomResourceDefinition 的名称匹配（格式为 `<names.plural>.<group>`）。必须全部小写。

  - **names.categories** ([]string)


    categories 是自定义资源所属的分组资源列表（例如 'all'）。
    它在 API 发现文档中发布，并支持客户端像 `kubectl get all` 这样的调用。

  - **names.listKind** (string)


    listKind 是此资源列表的序列化类型。默认为 "`kind`List"。

  - **names.shortNames** ([]string)


    shortNames 是资源的短名称，在 API 发现文档中公开，并支持客户端调用，如 `kubectl get <shortname>`。必须全部小写。

  - **names.singular** (string)


    singular 是资源的单数名称。必须全部小写。默认为小写 `kind`。


- **scope** (string)，必需
  
  scope 表示自定义资源是集群作用域还是命名空间作用域。允许的值为 `Cluster` 和 `Namespaced`。


- **versions** ([]CustomResourceDefinitionVersion)，必需

  versions 是自定义资源的所有 API 版本的列表。版本名称用于计算服务版本在 API 发现中列出的顺序。
  如果版本字符串与 Kubernetes 的版本号形式类似，则它将被排序在非 Kubernetes 形式版本字符串之前。
  Kubernetes 的版本号字符串按字典顺序排列。Kubernetes 版本号以 “v” 字符开头，
  后面是一个数字（主版本），然后是可选字符串 “alpha” 或 “beta” 和另一个数字（次要版本）。
  它们首先按 GA > beta > alpha 排序（其中 GA 是没有 beta 或 alpha 等后缀的版本），然后比较主要版本，
  最后是比较次要版本。版本排序列表示例：v10、v2、v1、v11beta2、v10beta3、v3beta1、v12alpha1、v11alpha2、foo1、foo10。

  <a name="CustomResourceDefinitionVersion"></a>
  **CustomResourceDefinitionVersion 描述 CRD 的一个版本。**

  - **versions.name** (string)，必需

    name 是版本名称，例如 “v1”、“v2beta1” 等。如果 `served` 是 true，自定义资源在
    `/apis/<group>/<version>/...` 版本下提供。


  - **versions.served** (boolean)，必需

    served 是用于启用/禁用该版本通过 REST API 提供服务的标志。


  - **versions.storage** (boolean)，必需

    storage 表示在将自定义资源持久保存到存储时，应使用此版本。有且仅有一个版本的 storage=true。

  - **versions.additionalPrinterColumns** ([]CustomResourceColumnDefinition)


    additionalPrinterColumns 表示在表输出中返回的附加列。
    有关详细信息，请参阅 https://kubernetes.io/zh-cn/docs/reference/using-api/api-concepts/#receiving-resources-as-tables。
    如果没有指定列，则显示自定义资源存活时间（AGE）列。
  
    <a name="CustomResourceColumnDefinition"></a>

    **CustomResourceColumnDefinition 指定用于服务器端打印的列。**

    - **versions.additionalPrinterColumns.jsonPath** (string)，必需

      jsonPath 是一个简单的 JSON 路径（使用数组表示法），它对每个自定义资源进行评估，以生成该列的值。


    - **versions.additionalPrinterColumns.name** (string)，必需

      name 是便于阅读的列名称。


    - **versions.additionalPrinterColumns.type** (string)，必需

      type 是此列的 OpenAPI 类型定义。有关详细信息，
      请参阅 https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#data-types

    - **versions.additionalPrinterColumns.description** (string)


      description 是该列的可读性描述。

    - **versions.additionalPrinterColumns.format** (string)


      format 是这个列的可选 OpenAPI 类型定义。'name' 格式应用于主标识符列，以帮助客户端识别列是资源名称。
      有关详细信息，请参阅 https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#data-types。

    - **versions.additionalPrinterColumns.priority** (int32)


      priority 是一个定义此列相对于其他列的相对重要性的整数。数字越低，优先级越高。
      在空间有限的情况下，可以省略的列的优先级应大于 0。

  - **versions.deprecated** (boolean)


    deprecated 表示此版本的自定义资源 API 已弃用。设置为 true 时，对此版本的 API
    请求会在服务器响应头信息中带有警告（warning）信息。此值默认为 false。

  - **versions.deprecationWarning** (string)


    deprecationWarning 会覆盖返回给 API 客户端的默认警告。只能在 `deprecated` 为 true 时设置。
    默认警告表示此版本已弃用，建议使用最新的同等或更高稳定性版本（如果存在）。

  - **versions.schema** (CustomResourceValidation)


    schema 描述了用于验证、精简和默认此版本的自定义资源的模式。  

    <a name="CustomResourceValidation"></a>

    **CustomResourceValidation 是 CustomResources 的验证方法列表。**  

    - **versions.schema.openAPIV3Schema** (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#JSONSchemaProps" >}}">JSONSchemaProps</a>)


      openAPIV3Schema 是用于验证和精简的 OpenAPI v3 模式。

  - **versions.subresources** (CustomResourceSubresources)


    subresources 指定此版本已定义的自定义资源具有哪些子资源。  

    <a name="CustomResourceSubresources"></a>

    **CustomResourceSubresources 定义了 CustomResources 子资源的状态和规模。**  

    - **versions.subresources.scale** (CustomResourceSubresourceScale)


      scale 表示自定义资源应该提供一个 `/scale` 子资源，该子资源返回一个 `autoscaling/v1` Scale 对象。

      <a name="CustomResourceSubresourceScale"></a>

      **CustomResourceSubresourceScale 定义了如何为 CustomResources 的 scale 子资源提供服务。**

      - **versions.subresources.scale.specReplicasPath** (string)，必需

        specReplicasPath 定义对应于 Scale 的自定义资源内的 JSON 路径 `spec.replicas`。
        只允许没有数组表示法的 JSON 路径。必须是 `.spec` 下的 JSON 路径。
        如果自定义资源中的给定路径下没有值，那么 GET `/scale` 子资源将返回错误。


      - **versions.subresources.scale.statusReplicasPath** (string)，必需

        statusReplicasPath 定义对应于 Scale 的自定义资源内的 JSON 路径 `status.replicas`。
        只允许不带数组表示法的 JSON 路径。必须是 `.status` 下的 JSON 路径。
        如果自定义资源中给定路径下没有值，则 `/scale` 子资源中的 `status.replicas` 值将默认为 0。

      - **versions.subresources.scale.labelSelectorPath** (string)


        labelSelectorPath 定义对应于 Scale 的自定义资源内的 JSON 路径 `status.selector`。
        只允许不带数组表示法的 JSON 路径。必须是 `.status` 或 `.spec` 下的路径。
        必须设置为与 HorizontalPodAutoscaler 一起使用。
        此 JSON 路径指向的字段必须是字符串字段（不是复杂的选择器结构），其中包含字符串形式的序列化标签选择器。
        更多信息： https://kubernetes.io/zh-cn/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions#scale-subresource。
        如果自定义资源中给定路径下没有值，则 `/scale` 子资源中的 `status.selector` 默认值为空字符串。

    - **versions.subresources.status** (CustomResourceSubresourceStatus)


      status 表示自定义资源应该为 `/status` 子资源服务。当启用时：

      1. 对自定义资源主端点的请求会忽略对对象 `status` 节的改变；
      2. 对自定义资源 `/status` 子资源的请求忽略对对象 `status` 节以外的任何变化。

      <a name="CustomResourceSubresourceStatus"></a>

      CustomResourceSubresourceStatus 定义了如何为自定义资源提供 status 子资源。
      状态由 CustomResource 中的 `.status` JSON 路径表示。设置后，

      * 为自定义资源提供一个 `/status` 子资源。
      * 向 `/status` 子资源发出的 PUT 请求时，需要提供自定义资源对象，服务器端会忽略对 status 节以外的任何内容更改。
      * 对自定义资源的 PUT/POST/PATCH 请求会忽略对 status 节的更改。

- **conversion** (CustomResourceConversion)

  conversion 定义了 CRD 的转换设置。

  <a name="CustomResourceConversion"></a>

  **CustomResourceConversion 描述了如何转换不同版本的自定义资源。**

  - **conversion.strategy** (string)，必需

    strategy 指定如何在版本之间转换自定义资源。允许的值为：

    - `"None"`：转换器仅更改 apiVersion 并且不会触及自定义资源中的任何其他字段。
    - `"Webhook"`：API 服务器将调用外部 Webhook 进行转换。此选项需要其他信息。这要求
      spec.preserveUnknownFields 为 false，并且设置 spec.conversion.webhook。

  - **conversion.webhook** (WebhookConversion)


    webhook 描述了如何调用转换 Webhook。当 `strategy` 设置为 `"Webhook"` 时有效。

    <a name="WebhookConversion"></a>

    **WebhookConversion 描述了如何调用转换 Webhook**

    - **conversion.webhook.conversionReviewVersions** ([]string)，必需

      conversionReviewVersions 是 Webhook 期望的 `ConversionReview` 版本的有序列表。
      API 服务器将使用它支持的列表中的第一个版本。如果 API 服务器不支持此列表中指定的版本，则自定义资源的转换将失败。
      如果持久化的 Webhook 配置指定了允许的版本但其中不包括 API 服务器所了解的任何版本，则对 Webhook 的调用将失败。

    - **conversion.webhook.clientConfig** (WebhookClientConfig)


      如果 strategy 是 `Webhook`， 那么 clientConfig 是关于如何调用 Webhook 的说明。

      <a name="WebhookClientConfig"></a>

      **WebhookClientConfig 包含与 Webhook 建立 TLS 连接的信息。**

      - **conversion.webhook.clientConfig.caBundle** ([]byte)


        caBundle 是一个 PEM 编码的 CA 包，用于验证 Webhook 服务器的服务证书。
        如果未指定，则使用 API 服务器上的系统根证书。

      - **conversion.webhook.clientConfig.service** (ServiceReference)


        service 是对此 Webhook 服务的引用。必须指定 service 或 url 字段之一。

        如果在集群中运行 Webhook，那么你应该使用 `service`。

        <a name="ServiceReference"></a>

        **ServiceReference 保存对 Service.legacy.k8s.io 的一个引用。**

        - **conversion.webhook.clientConfig.service.name** (string)，必需

          name 是服务的名称。必需。


        - **conversion.webhook.clientConfig.service.namespace** (string)，必需

          namespace 是服务的命名空间。必需。

        - **conversion.webhook.clientConfig.service.path** (string)


          path 是一个可选的 URL 路径，Webhook 将通过该路径联系服务。

        - **conversion.webhook.clientConfig.service.port** (int32)


          port 是 Webhook 联系的可选服务端口。`port` 应该是一个有效的端口号（1-65535，包含）。
          为实现向后兼容，默认端口号为 443。

      - **conversion.webhook.clientConfig.url** (string)


        url 以标准 URL 的形式（`scheme://host:port/path`）给出 Webhook 的位置。`url` 或 `service` 必须指定一个且只能指定一个。


        `host` 不应引用集群中运行的服务；若使用集群内服务应改为使用 `service` 字段。
        host 值可能会通过外部 DNS 解析（例如，`kube-apiserver` 无法解析集群内 DNS，因为这将违反分层规则）。
        `host` 也可能是 IP 地址。


        请注意，使用 `localhost` 或 `127.0.0.1` 作为 `host` 是有风险的，
        除非你非常小心地在所有运行 API 服务器的主机上运行这个 Webhook，因为这些 API 服务器可能需要调用这个 Webhook。
        这样的安装可能是不可移植的，也就是说，不容易在一个新的集群中复现。


        scheme 必须是 "https"；URL 必须以 "https://" 开头。

        路径（path）是可选的，如果存在，则可以是 URL 中允许的任何字符串。
        你可以使用路径传递一个任意字符串给 Webhook，例如，一个集群标识符。

        不允许使用用户或基本认证，例如 "user:password@"，是不允许的。片段（"#..."）和查询参数（"?..."）也是不允许的。

- **preserveUnknownFields** (boolean)


  preserveUnknownFields 表示将对象写入持久性存储时应保留 OpenAPI 模式中未规定的对象字段。
  apiVersion、kind、元数据（metadata）和元数据中的已知字段始终保留。不推荐使用此字段，而建议在
  `spec.versions[*].schema.openAPIV3Schema` 中设置 `x-preserve-unknown-fields` 为 true。
  更多详细信息参见： https://kubernetes.io/zh-cn/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#field-pruning

## JSONSchemaProps {#JSONSchemaProps}

JSONSchemaProps 是JSON 模式（JSON-Schema），遵循其规范草案第 4 版（http://json-schema.org/）。

<hr>

- **$ref** (string)

- **$schema** (string)

- **additionalItems** (JSONSchemaPropsOrBool)

  <a name="JSONSchemaPropsOrBool"></a>
  **JSONSchemaPropsOrBool 表示 JSONSchemaProps 或布尔值。布尔属性默认为 true。**

- **additionalProperties** (JSONSchemaPropsOrBool)

  <a name="JSONSchemaPropsOrBool"></a>
  **JSONSchemaPropsOrBool 表示 JSONSchemaProps 或布尔值。布尔属性默认为 true。**  

- **allOf** ([]<a href="{{< ref "../extend-resources/custom-resource-definition-v1#JSONSchemaProps" >}}">JSONSchemaProps</a>)

- **anyOf** ([]<a href="{{< ref "../extend-resources/custom-resource-definition-v1#JSONSchemaProps" >}}">JSONSchemaProps</a>)

- **default** (JSON)

  default 是未定义对象字段的默认值。设置默认值操作是 CustomResourceDefaulting 特性门控所控制的一个 Beta 特性。
  应用默认值设置时要求 spec.preserveUnknownFields 为 false。

  <a name="JSON"></a>
  **JSON 表示任何有效的 JSON 值。支持以下类型：bool、int64、float64、string、[]interface{}、map[string]interface{} 和 nil。**

- **definitions** (map[string]<a href="{{< ref "../extend-resources/custom-resource-definition-v1#JSONSchemaProps" >}}">JSONSchemaProps</a>)

- **dependencies** (map[string]JSONSchemaPropsOrStringArray)

  <a name="JSONSchemaPropsOrStringArray"></a>
  **JSONSchemaPropsOrStringArray 表示 JSONSchemaProps 或字符串数组。**

- **description** (string)

- **enum** ([]JSON)

  <a name="JSON"></a>
  **JSON 表示任何有效的 JSON 值。支持以下类型：bool、int64、float64、string、[]interface{}、map[string]interface{} 和 nil。**

- **example** (JSON)

  <a name="JSON"></a>
  **JSON 表示任何有效的 JSON 值。支持以下类型：bool、int64、float64、string、[]interface{}、map[string]interface{} 和 nil。**

- **exclusiveMaximum** (boolean)

- **exclusiveMinimum** (boolean)

- **externalDocs** (ExternalDocumentation)

  <a name="ExternalDocumentation"></a>
  **ExternalDocumentation 允许引用外部资源作为扩展文档。**

  - **externalDocs.description** (string)

  - **externalDocs.url** (string)

- **format** (string)

  format 是 OpenAPI v3 格式字符串。未知格式将被忽略。以下格式会被验证合法性：

  - bsonobjectid：一个 bson 对象的 ID，即一个 24 个字符的十六进制字符串
  - uri：由 Go 语言 net/url.ParseRequestURI 解析得到的 URI
  - email：由 Go 语言 net/mail.ParseAddress 解析得到的电子邮件地址
  - hostname：互联网主机名的有效表示，由 RFC 1034 第 3.1 节 [RFC1034] 定义
  - ipv4：由 Go 语言 net.ParseIP 解析得到的 IPv4 协议的 IP
  - ipv6：由 Go 语言 net.ParseIP 解析得到的 IPv6 协议的 IP
  - cidr: 由 Go 语言 net.ParseCIDR 解析得到的 CIDR
  - mac：由 Go 语言 net.ParseMAC 解析得到的一个 MAC 地址
  - uuid：UUID，允许大写字母，满足正则表达式 (?i)^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$
  - uuid3：UUID3，允许大写字母，满足正则表达式 (?i)^[0-9a-f]{8}-?[0-9a-f]{4}-?3[0-9a-f]{3}-?[0-9a-f]{4}-?[0-9a-f]{12}$
  - uuid4：UUID4，允许大写字母，满足正则表达式 (?i)^[0-9a-f]{8}-?[0-9a-f]{4}-?4[0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}$
  - uuid5：UUID5，允许大写字母，满足正则表达式 (?i)^[0-9a-f]{8}-?[0-9a-f]{4}-?5[0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}$
  - isbn：一个 ISBN10 或 ISBN13 数字字符串，如 "0321751043" 或 "978-0321751041"
  - isbn10：一个 ISBN10 数字字符串，如 "0321751043"
  - isbn13: 一个 ISBN13 号码字符串，如 "978-0321751041"
  - creditcard：信用卡号码，满足正则表达式 ^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$，其中混合任意非数字字符
  - ssn：美国社会安全号码，满足正则表达式 ^\d{3}[- ]?\d{2}[- ]?\d{4}$
  - hexcolor：一个十六进制的颜色编码，如 "#FFFFFF"，满足正则表达式 ^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$
  - rgbcolor：一个 RGB 颜色编码 例如 "rgb(255,255,255)"
  - byte：base64 编码的二进制数据
  - password: 任何类型的字符串
  - date：类似 "2006-01-02" 的日期字符串，由 RFC3339 中的完整日期定义
  - duration：由 Go 语言 time.ParseDuration 解析的持续时长字符串，如 "22 ns"，或与 Scala 持续时间格式兼容。
  - datetime：一个日期时间字符串，如 "2014-12-15T19:30:20.000Z"，由 RFC3339 中的 date-time 定义。

- **id** (string)

- **items** (JSONSchemaPropsOrArray)

  <a name="JSONSchemaPropsOrArray"></a>
  **JSONSchemaPropsOrArray 表示可以是 JSONSchemaProps 或 JSONSchemaProps 数组的值。这里目的主要用于序列化。**  

- **maxItems** (int64)

- **maxLength** (int64)

- **maxProperties** (int64)

- **maximum** (double)

- **minItems** (int64)

- **minLength** (int64)

- **minProperties** (int64)

- **minimum** (double)

- **multipleOf** (double)

- **not** (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#JSONSchemaProps" >}}">JSONSchemaProps</a>)

- **nullable** (boolean)

- **oneOf** ([]<a href="{{< ref "../extend-resources/custom-resource-definition-v1#JSONSchemaProps" >}}">JSONSchemaProps</a>)

- **pattern** (string)

- **patternProperties** (map[string]<a href="{{< ref "../extend-resources/custom-resource-definition-v1#JSONSchemaProps" >}}">JSONSchemaProps</a>)

- **properties** (map[string]<a href="{{< ref "../extend-resources/custom-resource-definition-v1#JSONSchemaProps" >}}">JSONSchemaProps</a>)

- **required** ([]string)

- **title** (string)

- **type** (string)

- **uniqueItems** (boolean)

- **x-kubernetes-embedded-resource** (boolean)

  x-kubernetes-embedded-resource 定义该值是一个嵌入式 Kubernetes runtime.Object，具有 TypeMeta 和 ObjectMeta。
  类型必须是对象。允许进一步限制嵌入对象。会自动验证 kind、apiVersion 和 metadata 等字段值。
  x-kubernetes-preserve-unknown-fields 允许为 true，但如果对象已完全指定
  （除 kind、apiVersion、metadata 之外），则不必为 true。

- **x-kubernetes-int-or-string** (boolean)

  x-kubernetes-int-or-string 指定此值是整数或字符串。如果为 true，则允许使用空类型，
  并且如果遵循以下模式之一，则允许作为 anyOf 的子类型：

  1) anyOf:
     - type: integer
     - type: string
  2) allOf:
     - anyOf:
       - type: integer
       - type: string

     - （可以有选择地包含其他类型）

- **x-kubernetes-list-map-keys** ([]string)

  X-kubernetes-list-map-keys 通过指定用作 map 索引的键来使用 x-kubernetes-list-type `map` 注解数组。

  这个标签必须只用于 "x-kubernetes-list-type" 扩展设置为 "map" 的列表。
  而且，为这个属性指定的值必须是子结构的标量类型的字段（不支持嵌套）。

  指定的属性必须是必需的或具有默认值，以确保所有列表项都存在这些属性。

- **x-kubernetes-list-type** (string)

  x-kubernetes-list-type 注解一个数组以进一步描述其拓扑。此扩展名只能用于列表，并且可能有 3 个可能的值：  


  1. `atomic`：
        列表被视为单个实体，就像标量一样。原子列表在更新时将被完全替换。这个扩展可以用于任何类型的列表（结构，标量，…）。
  2. `set`：
        set 是不能有多个具有相同值的列表。每个值必须是标量、具有 x-kubernetes-map-type
        `atomic` 的对象或具有 x-kubernetes-list-type `atomic` 的数组。
  3. `map`：
     这些列表类似于映射表，因为它们的元素具有用于标识它们的非索引键。合并时保留顺序。
     map 标记只能用于元数类型为 object 的列表。
  数组默认为原子数组。

- **x-kubernetes-map-type** (string)

  x-kubernetes-map-type 注解一个对象以进一步描述其拓扑。此扩展只能在 type 为 object 时使用，并且可能有 2 个可能的值：  


  1) `granular`：
        这些 map 是真实的映射（键值对），每个字段都是相互独立的（它们都可以由不同的角色来操作）。
        这是所有 map 的默认行为。
  2) `atomic`：map 被视为单个实体，就像标量一样。原子 map 更新后将被完全替换。

- **x-kubernetes-preserve-unknown-fields** (boolean)


  x-kubernetes-preserve-unknown-fields 针对未在验证模式中指定的字段，禁止 API 服务器的解码步骤剪除这些字段。
  这一设置对字段的影响是递归的，但在模式中指定了嵌套 properties 或 additionalProperties 时，会切换回正常的字段剪除行为。
  该值可为 true 或 undefined，不能为 false。

- **x-kubernetes-validations** ([]ValidationRule)


  **补丁策略：基于键 `rule` 合并**

  **Map：合并时将保留 rule 键的唯一值**

  x-kubernetes-validations 描述了用 CEL 表达式语言编写的验证规则列表。此字段是 Alpha 级别。
  使用此字段需要启用 `CustomResourceValidationExpressions` 特性门控。

  <a name="ValidationRule"></a>

  **ValidationRule 描述用 CEL 表达式语言编写的验证规则。**

  - **x-kubernetes-validations.rule** (string)，必需


    rule 表示将由 CEL 评估的表达式。参考： https://github.com/google/cel-spec。
    rule 的作用域为模式中的 x-kubernetes-validation 扩展所在的位置。CEL 表达式中的 `self` 与作用域值绑定。
    例子：rule 的作用域是一个具有状态子资源的资源根：{"rule": "self.status.actual \<= self.spec.maxDesired"}。


    如果 rule 的作用域是一个带有属性的对象，那么该对象的可访问属性是通过 `self` 进行字段选择的，
    并且可以通过 `has(self.field)` 来检查字段是否存在。在 CEL 表达式中，Null 字段被视为不存在的字段。
    如果该 rule 的作用域是一个带有附加属性的对象（例如一个 map），那么该 map 的值可以通过
    `self[mapKey]`来访问，map 是否包含某主键可以通过 `mapKey in self` 来检查。
    map 中的所有条目都可以通过 CEL 宏和函数（如 `self.all(...)`）访问。
    如果 rule 的作用域是一个数组，数组的元素可以通过 `self[i]` 访问，也可以通过宏和函数访问。
    如果 rule 的作用域为标量，`self` 绑定到标量值。举例：

    - rule 作用域为对象映射：{"rule": "self.components['Widget'].priority \< 10"}
    - rule 作用域为整数列表：{"rule": "self.values.all(value, value >= 0 && value \< 100)"}
    - rule 作用域为字符串值：{"rule": "self.startsWith('kube')"}


    `apiVersion`、`kind`、`metadata.name` 和 `metadata.generateName` 总是可以从对象的根和任何带
    x-kubernetes-embedded-resource 注解的对象访问。其他元数据属性都无法访问。


    在 CEL 表达式中无法访问通过 x-kubernetes-preserve-unknown-fields 保存在自定义资源中的未知数据。
    这包括：

    - 由包含 x-kubernetes-preserve-unknown-fields 的对象模式所保留的未知字段值；
    - 属性模式为 "未知类型" 的对象属性。"未知类型" 递归定义为：

      - 没有设置 type 但 x-kubernetes-preserve-unknown-fields 设置为 true 的模式。
      - 条目模式为"未知类型"的数组。
      - additionalProperties 模式为"未知类型"的对象。


    只有名称符合正则表达式 `[a-zA-Z_.-/][a-zA-Z0-9_.-/]*`  的属性才可被访问。
    在表达式中访问属性时，可访问的属性名称根据以下规则进行转义：

    - '__' 转义为 '__underscores__'
    - '.' 转义为 '__dot__'
    - '-' 转义为 '__dash__'
    - '/' 转义为 '__slash__'
    - 恰好匹配 CEL 保留关键字的属性名称转义为 '__{keyword}__' 。这里的关键字具体包括：
        "true"，"false"，"null"，"in"，"as"，"break"，"const"，"continue"，"else"，"for"，"function"，"if"，
        "import"，"let"，"loop"，"package"，"namespace"，"return"。
    举例：

      - 规则访问名为 "namespace" 的属性：`{"rule": "self.__namespace__ > 0"}`
      - 规则访问名为 "x-prop" 的属性：`{"rule": "self.x__dash__prop > 0"}`
      - 规则访问名为 "redact__d" 的属性：`{"rule": "self.redact__underscores__d > 0"}`


    对 x-kubernetes-list-type 为 'set' 或 'map' 的数组进行比较时忽略元素顺序，如：[1, 2] == [2, 1]。
    使用 x-kubernetes-list-type 对数组进行串接使用下列类型的语义：

    - 'set'：`X + Y` 执行合并，其中 `X` 保留所有元素的数组位置，并附加不相交的元素 `Y`，保留其局部顺序。
    - 'map'：`X + Y` 执行合并，保留 `X` 中所有键的数组位置，但当 `X` 和 `Y` 的键集相交时，会被 `Y` 中的值覆盖。
      添加 `Y` 中具有不相交键的元素，保持其局顺序。

  - **x-kubernetes-validations.message** (string)


    message 表示验证失败时显示的消息。如果规则包含换行符，则需要该消息。消息不能包含换行符。
    如果未设置，则消息为 "failed rule: {Rule}"，如："must be a URL with the host matching spec.host"

  - **x-kubernetes-validations.messageExpression** (string)

    messageExpression 声明一个 CEL 表达式，其计算结果是此规则失败时返回的验证失败消息。
    由于 messageExpression 用作失败消息，因此它的值必须是一个字符串。
    如果在规则中同时存在 message 和 messageExpression，则在验证失败时使用 messageExpression。
    如果是 messageExpression 出现运行时错误，则会记录运行时错误，并生成验证失败消息，
    就好像未设置 messageExpression 字段一样。如果 messageExpression 求值为空字符串、
    只包含空格的字符串或包含换行符的字符串，则验证失败消息也将像未设置 messageExpression 字段一样生成，
    并记录 messageExpression 生成空字符串/只包含空格的字符串/包含换行符的字符串的事实。
    messageExpression 可以访问的变量与规则相同；唯一的区别是返回类型。
    例如："x must be less than max ("+string(self.max)+")"。

## CustomResourceDefinitionStatus {#CustomResourceDefinitionStatus}

CustomResourceDefinitionStatus 表示 CustomResourceDefinition 的状态。

<hr>

- **acceptedNames** (CustomResourceDefinitionNames)


  acceptedNames 是实际用于服务发现的名称。它们可能与规约（spec）中的名称不同。

  <a name="CustomResourceDefinitionNames"></a>

  **CustomResourceDefinitionNames 表示提供此 CustomResourceDefinition 资源的名称。**

  - **acceptedNames.kind** (string)，必需

    kind 是资源的序列化类型。它通常是驼峰命名的单数形式。自定义资源实例将使用此值作为 API 调用中的 `kind` 属性。


  - **acceptedNames.plural** (string)，必需

    plural 是所提供的资源的复数名称，自定义资源在 `/apis/<group>/<version>/.../<plural>` 下提供。
    必须与 CustomResourceDefinition 的名称匹配（格式为 `<names.plural>.<group>`）。必须全部小写。

  - **acceptedNames.categories** ([]string)


    categories 是此自定义资源所属的分组资源列表（例如 'all'）。
    它在 API 发现文档中发布，并被客户端用于支持像 `kubectl get all` 这样的调用。

  - **acceptedNames.listKind** (string)


    listKind 是此资源列表的序列化类型。默认为 "`<kind>List`"。  

  - **acceptedNames.shortNames** ([]string)


    shortNames 是资源的短名称，在 API 发现文档中公开，并支持客户端调用，如 `kubectl get <shortname>`。必须全部小写。  

  - **acceptedNames.singular** (string)


    singular 是资源的单数名称。必须全部小写。默认为小写形式的 `kind`。

- **conditions** ([]CustomResourceDefinitionCondition)


  **Map：合并时将保留 type 键的唯一值**

  conditions 表示 CustomResourceDefinition 特定方面的状态

  <a name="CustomResourceDefinitionCondition"></a>

  **CustomResourceDefinitionCondition 包含此 Pod 当前状况的详细信息。**

  - **conditions.status** (string)，必需

    status 表示状况（Condition）的状态，取值为 True、False 或 Unknown 之一。


  - **conditions.type** (string)，必需

    type 是条件的类型。类型包括：Established、NamesAccepted 和 Terminating。

  - **conditions.lastTransitionTime** (Time)


    lastTransitionTime 是上一次发生状况状态转换的时间。

    <a name="Time"></a>

    **Time 是对 time.Time 的封装。Time 支持对 YAML 和 JSON 进行正确封包。为 time 包的许多函数方法提供了封装器。**

  - **conditions.message** (string)


    message 是有关上次转换的详细可读信息。

  - **conditions.reason** (string)


    reason 表述状况上次转换原因的、驼峰格式命名的、唯一的一个词。

- **storedVersions** ([]string)


  storedVersions 列出了曾经被持久化的所有 CustomResources 版本。跟踪这些版本可以为 etcd 中的存储版本提供迁移路径。
  该字段是可变的，因此迁移控制器可以完成到另一个版本的迁移（确保存储中没有遗留旧对象），然后从该列表中删除其余版本。
  当版本在此列表中时，则不能从 `spec.versions` 中删除。

## CustomResourceDefinitionList {#CustomResourceDefinitionList}
CustomResourceDefinitionList 是 CustomResourceDefinition 对象的列表。

<hr>


- **items** ([]<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>)，必需

  items 列出单个 CustomResourceDefinition 对象。

- **apiVersion** (string)


  apiVersion 定义对象表示的版本化模式。服务器应将已识别的模式转换为最新的内部值，并可能拒绝未识别的值。
  更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources

- **kind** (string)


  kind 是一个字符串值，表示该对象所表示的 REST 资源。服务器可以从客户端提交请求的端点推断出 REST 资源。
  不能被更新。驼峰命名。更多信息：
  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)


  标准的对象元数据，更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

## Operations {#Operations}

<hr>

### `get` 读取指定的 CustomResourceDefinition

#### HTTP 请求

GET /apis/apiextensions.k8s.io/v1/customresourcedefinitions/{name}

#### 参数

- **name** （**路径参数**）：string，必需

  CustomResourceDefinition 的名称。


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): OK

401: Unauthorized

### `get` 读取指定 CustomResourceDefinition 的状态

#### HTTP 请求

GET /apis/apiextensions.k8s.io/v1/customresourcedefinitions/{name}/status

#### 参数

- **name** （**路径参数**）：string，必需

  CustomResourceDefinition 的名称。


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): OK

401: Unauthorized

### `list` 列出或观察 CustomResourceDefinition 类型的对象

#### HTTP 请求

GET /apis/apiextensions.k8s.io/v1/customresourcedefinitions

#### 参数


  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>


  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>


  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>


  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>


  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>


  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>


  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>

#### 响应

200 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinitionList" >}}">CustomResourceDefinitionList</a>): OK

401: Unauthorized

### `create` 创建一个 CustomResourceDefinition

#### HTTP 请求

POST /apis/apiextensions.k8s.io/v1/customresourcedefinitions

#### 参数

- **body**: <a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>，必需


  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): OK

201 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): Created

202 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): Accepted

401: Unauthorized

### `update` 替换指定的 CustomResourceDefinition

#### HTTP 请求

PUT /apis/apiextensions.k8s.io/v1/customresourcedefinitions/{name}

#### 参数

- **name** （**路径参数**）：string，必需

  CustomResourceDefinition 的名称。

- **body**: <a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>，必需


  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): OK

201 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): Created

401: Unauthorized

### `update` 替换指定 CustomResourceDefinition 的状态

#### HTTP 请求

PUT /apis/apiextensions.k8s.io/v1/customresourcedefinitions/{name}/status

#### 参数

- **name** （**路径参数**）：string，必需

  CustomResourceDefinition 的名称。

- **body**: <a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>，必需


  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): OK

201 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): Created

401: Unauthorized

### `patch` 部分更新指定的 CustomResourceDefinition

#### HTTP 请求

PATCH /apis/apiextensions.k8s.io/v1/customresourcedefinitions/{name}

#### 参数

- **name** （**路径参数**）：string，必需

  CustomResourceDefinition 的名称。

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需


  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): OK

201 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): Created

401: Unauthorized

### `patch` 部分更新指定 CustomResourceDefinition 的状态

#### HTTP 请求

PATCH /apis/apiextensions.k8s.io/v1/customresourcedefinitions/{name}/status

#### 参数

- **name** （**路径参数**）：string，必需

  CustomResourceDefinition 的名称。

- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>，必需


  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldValidation" >}}">fieldValidation</a>


  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>

#### 响应

200 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): OK

201 (<a href="{{< ref "../extend-resources/custom-resource-definition-v1#CustomResourceDefinition" >}}">CustomResourceDefinition</a>): Created

401: Unauthorized

### `delete` 删除一个 CustomResourceDefinition

#### HTTP 请求

DELETE /apis/apiextensions.k8s.io/v1/customresourcedefinitions/{name}

#### 参数

- **name** （**路径参数**）：string，必需
  
  CustomResourceDefinition 的名称。

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>


  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): Accepted

401: Unauthorized

### `deletecollection` 删除 CustomResourceDefinition 的集合

#### HTTP 请求

DELETE /apis/apiextensions.k8s.io/v1/customresourcedefinitions

#### 参数

- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>


  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>


  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>


  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>


  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>


  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>


  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>


  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>


  <a href="{{< ref "../common-parameters/common-parameters#sendInitialEvents" >}}">sendInitialEvents</a>


  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>

#### 响应

200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized
