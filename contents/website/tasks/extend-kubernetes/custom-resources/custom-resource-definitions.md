---
title: 使用 CustomResourceDefinition 扩展 Kubernetes API
content_type: task
min-kubernetes-server-version: 1.16
weight: 20
---

本页展示如何使用
[CustomResourceDefinition](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#customresourcedefinition-v1-apiextensions-k8s-io)
将[定制资源（Custom Resource）](/zh-cn/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
安装到 Kubernetes API 上。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

如果你在使用较老的、仍处于被支持范围的 Kubernetes 版本，
请切换到该版本的文档查看对于你的集群而言有用的建议。


## 创建 CustomResourceDefinition  {#create-a-customresourcedefinition}

当你创建新的 CustomResourceDefinition（CRD）时，Kubernetes API 服务器会为你所指定的每个版本生成一个新的
RESTful 资源路径。
基于 CRD 对象所创建的自定义资源可以是名字空间作用域的，也可以是集群作用域的，
取决于 CRD 对象 `spec.scope` 字段的设置。

与其它的内置对象一样，删除名字空间也将删除该名字空间中的所有自定义对象。
CustomResourceDefinitions 本身是无名字空间的，可在所有名字空间中访问。

例如，如果你将下面的 CustomResourceDefinition 保存到 `resourcedefinition.yaml`
文件：

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  # 名字必需与下面的 spec 字段匹配，并且格式为 '<名称的复数形式>.<组名>'
  name: crontabs.stable.example.com
spec:
  # 组名称，用于 REST API: /apis/<组>/<版本>
  group: stable.example.com
  # 列举此 CustomResourceDefinition 所支持的版本
  versions:
    - name: v1
      # 每个版本都可以通过 served 标志来独立启用或禁止
      served: true
      # 其中一个且只有一个版本必需被标记为存储版本
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                cronSpec:
                  type: string
                image:
                  type: string
                replicas:
                  type: integer
  # 可以是 Namespaced 或 Cluster
  scope: Namespaced
  names:
    # 名称的复数形式，用于 URL：/apis/<组>/<版本>/<名称的复数形式>
    plural: crontabs
    # 名称的单数形式，作为命令行使用时和显示时的别名
    singular: crontab
    # kind 通常是单数形式的驼峰命名（CamelCased）形式。你的资源清单会使用这一形式。
    kind: CronTab
    # shortNames 允许你在命令行使用较短的字符串来匹配资源
    shortNames:
    - ct
```

之后创建它：

```shell
kubectl apply -f resourcedefinition.yaml
```

这样一个新的受名字空间约束的 RESTful API 端点会被创建在：

```
/apis/stable.example.com/v1/namespaces/*/crontabs/...
```

此端点 URL 自此可以用来创建和管理定制对象。对象的 `kind` 将是来自你上面创建时
所用的 spec 中指定的 `CronTab`。

创建端点的操作可能需要几秒钟。你可以监测你的 CustomResourceDefinition 的
`Established` 状况变为 true，或者监测 API 服务器的发现信息等待你的资源出现在
那里。

## 创建定制对象   {#create-custom-objects}

在创建了 CustomResourceDefinition 对象之后，你可以创建定制对象（Custom
Objects）。定制对象可以包含定制字段。这些字段可以包含任意的 JSON 数据。
在下面的例子中，在类别为 `CronTab` 的定制对象中，设置了`cronSpec` 和 `image`
定制字段。类别 `CronTab` 来自你在上面所创建的 CRD 的规约。

如果你将下面的 YAML 保存到 `my-crontab.yaml`：

```yaml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  name: my-new-cron-object
spec:
  cronSpec: "* * * * */5"
  image: my-awesome-cron-image
```

并执行创建命令：

```shell
kubectl apply -f my-crontab.yaml
```

你就可以使用 kubectl 来管理你的 CronTab 对象了。例如：

```shell
kubectl get crontab
```

应该会输出如下列表：

```none
NAME                 AGE
my-new-cron-object   6s
```

使用 kubectl 时，资源名称是大小写不敏感的，而且你既可以使用 CRD 中所定义的单数
形式或复数形式，也可以使用其短名称：

```shell
kubectl get ct -o yaml
```

你可以看到输出中包含了你创建定制对象时在 YAML 文件中指定的定制字段 `cronSpec`
和 `image`：

```yaml
apiVersion: v1
items:
- apiVersion: stable.example.com/v1
  kind: CronTab
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"stable.example.com/v1","kind":"CronTab","metadata":{"annotations":{},"name":"my-new-cron-object","namespace":"default"},"spec":{"cronSpec":"* * * * */5","image":"my-awesome-cron-image"}}
    creationTimestamp: "2021-06-20T07:35:27Z"
    generation: 1
    name: my-new-cron-object
    namespace: default
    resourceVersion: "1326"
    uid: 9aab1d66-628e-41bb-a422-57b8b3b1f5a9
  spec:
    cronSpec: '* * * * */5'
    image: my-awesome-cron-image
kind: List
metadata:
  resourceVersion: ""
  selfLink: ""
```

## 删除 CustomResourceDefinition    {#delete-a-customresourcedefinition}

当你删除某 CustomResourceDefinition 时，服务器会卸载其 RESTful API
端点，并删除服务器上存储的所有定制对象。

```shell
kubectl delete -f resourcedefinition.yaml
kubectl get crontabs
```

```none
Error from server (NotFound): Unable to list {"stable.example.com" "v1" "crontabs"}: the server could not
find the requested resource (get crontabs.stable.example.com)
```

如果你在以后创建相同的 CustomResourceDefinition 时，该 CRD 会是一个空的结构。

## 设置结构化的模式   {#specifying-a-structural-schema}

CustomResource 对象在定制字段中保存结构化的数据，这些字段和内置的字段
`apiVersion`、`kind` 和 `metadata` 等一起存储，不过内置的字段都会被 API
服务器隐式完成合法性检查。有了 [OpenAPI v3.0 检查](#validation)
能力之后，你可以设置一个模式（Schema），在创建和更新定制对象时，这一模式会被用来
对对象内容进行合法性检查。参阅下文了解这类模式的细节和局限性。

在 `apiextensions.k8s.io/v1` 版本中，CustomResourceDefinition 的这一结构化模式
定义是必需的。
在 CustomResourceDefinition 的 beta 版本中，结构化模式定义是可选的。

结构化模式本身是一个 [OpenAPI v3.0 验证模式](#validation)，其中：

1. 为对象根（root）设置一个非空的 type 值（藉由 OpenAPI 中的 `type`），对每个
   object 节点的每个字段（藉由 OpenAPI 中的 `properties` 或 `additionalProperties`）以及
   array 节点的每个条目（藉由 OpenAPI 中的 `items`）也要设置非空的 type 值，
   除非：
   * 节点包含属性 `x-kubernetes-int-or-string: true`
   * 节点包含属性 `x-kubernetes-preserve-unknown-fields: true`
2. 对于 object 的每个字段或 array 中的每个条目，如果其定义中包含 `allOf`、`anyOf`、`oneOf`
   或 `not`，则模式也要指定这些逻辑组合之外的字段或条目（试比较例 1 和例 2)。
3. 在 `allOf`、`anyOf`、`oneOf` 或 `not` 上下文内不设置 `description`、`type`、`default`、
   `additionalProperties` 或者 `nullable`。此规则的例外是
   `x-kubernetes-int-or-string` 的两种模式（见下文）。
4. 如果 `metadata` 被设置，则只允许对 `metadata.name` 和 `metadata.generateName` 设置约束。

非结构化的例 1:

```none
allOf:
- properties:
    foo:
      ...
```

违反了第 2 条规则。下面的是正确的：

```none
properties:
  foo:
    ...
allOf:
- properties:
    foo:
      ...
```

非结构化的例 2：

```none
allOf:
- items:
    properties:
      foo:
        ...
```

违反了第 2 条规则。下面的是正确的：

```none
items:
  properties:
    foo:
      ...
allOf:
- items:
    properties:
      foo:
        ...
```

非结构化的例 3：

```none
properties:
  foo:
    pattern: "abc"
  metadata:
    type: object
    properties:
      name:
        type: string
        pattern: "^a"
      finalizers:
        type: array
        items:
          type: string
          pattern: "my-finalizer"
anyOf:
- properties:
    bar:
      type: integer
      minimum: 42
  required: ["bar"]
  description: "foo bar object"
```

不是一个结构化的模式，因为其中存在以下违例：

* 根节点缺失 type 设置（规则 1）
* `foo` 的 type 缺失（规则 1）
* `anyOf` 中的 `bar` 未在外部指定（规则 2）
* `bar` 的 `type` 位于 `anyOf` 中（规则 3）
* `anyOf` 中设置了 `description` （规则 3）
* `metadata.finalizers` 不可以被限制 (规则 4）

作为对比，下面的 YAML 所对应的模式则是结构化的：

```yaml
type: object
description: "foo bar object"
properties:
  foo:
    type: string
    pattern: "abc"
  bar:
    type: integer
  metadata:
    type: object
    properties:
      name:
        type: string
        pattern: "^a"
anyOf:
- properties:
    bar:
      minimum: 42
  required: ["bar"]
```

如果违反了结构化模式规则，CustomResourceDefinition 的 `NonStructural`
状况中会包含报告信息。

### 字段剪裁     {#field-pruning}

CustomResourceDefinition 在集群的持久性存储
{{< glossary_tooltip term_id="etcd" text="etcd">}}
中保存经过合法性检查的资源数据。
就像原生的 Kubernetes 资源，例如 {{< glossary_tooltip text="ConfigMap" term_id="configmap" >}}，
如果你指定了 API 服务器所无法识别的字段，则该未知字段会在保存资源之前被
**剪裁（Pruned）** 掉（删除）。

从 `apiextensions.k8s.io/v1beta1` 转换到 `apiextensions.k8s.io/v1` 的 CRD
可能没有结构化的模式定义，因此其 `spec.preserveUnknownFields` 可能为 `true`。

对于使用 `apiextensions.k8s.io/v1beta1` 且将 `spec.preserveUnknownFields` 设置为 `true`
创建的旧 CustomResourceDefinition 对象，有以下表现：

* 裁剪未启用。
* 可以存储任意数据。

为了与 `apiextensions.k8s.io/v1` 兼容，将你的定制资源定义更新为：

1. 使用结构化的 OpenAPI 模式。
2. `spec.preserveUnknownFields` 设置为 `false`。

如果你将下面的 YAML 保存到 `my-crontab.yaml` 文件：

```yaml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  name: my-new-cron-object
spec:
  cronSpec: "* * * * */5"
  image: my-awesome-cron-image
  someRandomField: 42
```

并创建之：

```shell
kubectl create --validate=false -f my-crontab.yaml -o yaml
```

输出类似于：

```yaml
apiVersion: stable.example.com/v1
kind: CronTab
metadata:
  creationTimestamp: 2017-05-31T12:56:35Z
  generation: 1
  name: my-new-cron-object
  namespace: default
  resourceVersion: "285"
  uid: 9423255b-4600-11e7-af6a-28d2447dc82b
spec:
  cronSpec: '* * * * */5'
  image: my-awesome-cron-image
```

注意其中的字段 `someRandomField` 已经被剪裁掉。

本例中通过 `--validate=false` 命令行选项 关闭了客户端的合法性检查以展示 API 服务器的行为，
因为 [OpenAPI 合法性检查模式也会发布到](#publish-validation-schema-in-openapi-v2)
客户端，`kubectl` 也会检查未知的字段并在对象被发送到 API
服务器之前就拒绝它们。

#### 控制剪裁   {#controlling-pruning}

默认情况下，定制资源的所有版本中的所有未规定的字段都会被剪裁掉。
通过在结构化的 OpenAPI v3 [检查模式定义](#specifying-a-structural-schema)
中为特定字段的子树添加 `x-kubernetes-preserve-unknown-fields: true` 属性，
可以选择不对其执行剪裁操作。

例如：

```yaml
type: object
properties:
  json:
    x-kubernetes-preserve-unknown-fields: true
```

字段 `json` 可以保存任何 JSON 值，其中内容不会被剪裁掉。

你也可以部分地指定允许的 JSON 数据格式；例如：

```yaml
type: object
properties:
  json:
    x-kubernetes-preserve-unknown-fields: true
    type: object
    description: this is arbitrary JSON
```

通过这样设置，JSON 中只能设置 `object` 类型的值。

对于所指定的每个属性（或 `additionalProperties`），剪裁会再次被启用。

```yaml
type: object
properties:
  json:
    x-kubernetes-preserve-unknown-fields: true
    type: object
    properties:
      spec:
        type: object
        properties:
          foo:
            type: string
          bar:
            type: string
```

对于上述定义，如果提供的数值如下：

```yaml
json:
  spec:
    foo: abc
    bar: def
    something: x
  status:
    something: x
```

则该值会被剪裁为：

```yaml
json:
  spec:
    foo: abc
    bar: def
  status:
    something: x
```

这意味着所指定的 `spec` 对象中的 `something` 字段被剪裁掉，而其外部的内容都被保留。

### IntOrString

模式定义中标记了 `x-kubernetes-int-or-string: true` 的节点不受前述规则 1
约束，因此下面的定义是结构化的模式：

```yaml
type: object
properties:
  foo:
    x-kubernetes-int-or-string: true
```

此外，所有这类节点也不再受规则 3 约束，也就是说，下面两种模式是被允许的
（注意，仅限于这两种模式，不支持添加新字段的任何其他变种）：

```none
x-kubernetes-int-or-string: true
anyOf:
  - type: integer
  - type: string
...
```

和

```none
x-kubernetes-int-or-string: true
allOf:
  - anyOf:
      - type: integer
      - type: string
  - ... # zero or more
...
```

在以上两种规约中，整数值和字符串值都会被认为是合法的。

在[合法性检查模式定义的发布时](#publish-validation-schema-in-openapi-v2)，
`x-kubernetes-int-or-string: true` 会被展开为上述两种模式之一。

### RawExtension

RawExtensions（就像在
[k8s.io/apimachinery](https://github.com/kubernetes/apimachinery/blob/03ac7a9ade429d715a1a46ceaa3724c18ebae54f/pkg/runtime/types.go#L94)
项目中 `runtime.RawExtension` 所定义的那样）
可以保存完整的 Kubernetes 对象，也就是，其中会包含 `apiVersion` 和 `kind`
字段。

通过 `x-kubernetes-embedded-resource: true` 来设定这些嵌套对象的规约
（无论是完全无限制还是部分指定都可以）是可能的。例如：

```yaml
type: object
properties:
  foo:
    x-kubernetes-embedded-resource: true
    x-kubernetes-preserve-unknown-fields: true
```

这里，字段 `foo` 包含一个完整的对象，例如：

```none
foo:
  apiVersion: v1
  kind: Pod
  spec:
    ...
```

由于字段上设置了 `x-kubernetes-preserve-unknown-fields: true`，其中的内容不会
被剪裁。不过，在这个语境中，`x-kubernetes-preserve-unknown-fields: true` 的
使用是可选的。

设置了 `x-kubernetes-embedded-resource: true` 之后，`apiVersion`、`kind` 和
`metadata` 都是隐式设定并隐式完成合法性验证。

## 提供 CRD 的多个版本   {#serving-multiple-versions-of-a-crd}

关于如何为你的 CustomResourceDefinition 提供多个版本的支持，
以及如何将你的对象从一个版本迁移到另一个版本，
详细信息可参阅 [CustomResourceDefinition 的版本管理](/zh-cn/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/)。


## 高级主题     {#advanced-topics}

### Finalizers

**Finalizer** 能够让控制器实现异步的删除前（Pre-delete）回调。
与内置对象类似，定制对象也支持 Finalizer。

你可以像下面一样为定制对象添加 Finalizer：

```yaml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  finalizers:
  - stable.example.com/finalizer
```

自定义 Finalizer 的标识符包含一个域名、一个正向斜线和 finalizer 的名称。
任何控制器都可以在任何对象的 finalizer 列表中添加新的 finalizer。

对带有 Finalizer 的对象的第一个删除请求会为其 `metadata.deletionTimestamp`
设置一个值，但不会真的删除对象。一旦此值被设置，`finalizers` 列表中的表项只能被移除。
在列表中仍然包含 finalizer 时，无法强制删除对应的对象。

当 `metadata.deletionTimestamp` 字段被设置时，监视该对象的各个控制器会执行它们所能处理的
finalizer，并在完成处理之后将其从列表中移除。
每个控制器负责将其 finalizer 从列表中删除。

`metadata.deletionGracePeriodSeconds` 的取值控制对更新的轮询周期。

一旦 finalizers 列表为空时，就意味着所有 finalizer 都被执行过，
Kubernetes 会最终删除该资源，

### 合法性检查    {#validation}

定制资源是通过
[OpenAPI v3 模式定义](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#schemaObject)
来执行合法性检查的，当启用[验证规则特性](#validation-rules)时，通过 `x-kubernetes-validations` 验证，
你可以通过使用[准入控制 Webhook](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#validatingadmissionwebhook)
来添加额外的合法性检查逻辑。

此外，对模式定义存在以下限制：

- 以下字段不可设置：

  - `definitions`
  - `dependencies`
  - `deprecated`
  - `discriminator`
  - `id`
  - `patternProperties`
  - `readOnly`
  - `writeOnly`
  - `xml`
  - `$ref`

- 字段 `uniqueItems` 不可设置为 `true`
- 字段 `additionalProperties` 不可设置为 `false`
- 字段 `additionalProperties` 与 `properties` 互斥，不可同时使用

当[验证规则特性](#validation-rules)被启用并且 CustomResourceDefinition
模式是一个[结构化的模式定义](#specifying-a-structural-schema)时，
`x-kubernetes-validations`
扩展可以使用[通用表达式语言 (CEL)](https://github.com/google/cel-spec)表达式来验证定制资源。

关于对某些 CustomResourceDefinition 特性所必需的限制，
可参见[结构化的模式定义](#specifying-a-structural-schema)小节。

模式定义是在 CustomResourceDefinition 中设置的。在下面的例子中，
CustomResourceDefinition 对定制对象执行以下合法性检查：

- `spec.cronSpec` 必须是一个字符串，必须是正则表达式所描述的形式；
- `spec.replicas` 必须是一个整数，且其最小值为 1、最大值为 10。

将此 CustomResourceDefinition 保存到 `resourcedefinition.yaml` 文件中：

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.stable.example.com
spec:
  group: stable.example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        # openAPIV3Schema 是验证自定义对象的模式。
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                cronSpec:
                  type: string
                  pattern: '^(\d+|\*)(/\d+)?(\s+(\d+|\*)(/\d+)?){4}$'
                image:
                  type: string
                replicas:
                  type: integer
                  minimum: 1
                  maximum: 10
  scope: Namespaced
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
    shortNames:
    - ct
```

并创建 CustomResourceDefinition：

```shell
kubectl apply -f resourcedefinition.yaml
```

对于一个创建 CronTab 类别对象的定制对象的请求而言，如果其字段中包含非法值，则
该请求会被拒绝。
在下面的例子中，定制对象中包含带非法值的字段：

- `spec.cronSpec` 与正则表达式不匹配
- `spec.replicas` 数值大于 10。

如果你将下面的 YAML 保存到 `my-crontab.yaml`：

```yaml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  name: my-new-cron-object
spec:
  cronSpec: "* * * *"
  image: my-awesome-cron-image
  replicas: 15
```

并尝试创建定制对象：

```shell
kubectl apply -f my-crontab.yaml
```

你会看到下面的错误信息：

```console
The CronTab "my-new-cron-object" is invalid: []: Invalid value: map[string]interface {}{"apiVersion":"stable.example.com/v1", "kind":"CronTab", "metadata":map[string]interface {}{"name":"my-new-cron-object", "namespace":"default", "deletionTimestamp":interface {}(nil), "deletionGracePeriodSeconds":(*int64)(nil), "creationTimestamp":"2017-09-05T05:20:07Z", "uid":"e14d79e7-91f9-11e7-a598-f0761cb232d1", "clusterName":""}, "spec":map[string]interface {}{"cronSpec":"* * * *", "image":"my-awesome-cron-image", "replicas":15}}:
validation failure list:
spec.cronSpec in body should match '^(\d+|\*)(/\d+)?(\s+(\d+|\*)(/\d+)?){4}$'
spec.replicas in body should be less than or equal to 10
```

如果所有字段都包含合法值，则对象创建的请求会被接受。

将下面的 YAML 保存到 `my-crontab.yaml` 文件：

```yaml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  name: my-new-cron-object
spec:
  cronSpec: "* * * * */5"
  image: my-awesome-cron-image
  replicas: 5
```

并创建定制对象：

```shell
kubectl apply -f my-crontab.yaml
crontab "my-new-cron-object" created
```
## 验证规则

{{< feature-state state="beta" for_k8s_version="v1.25" >}}

验证规则从 1.25 开始处于 Beta 状态，
默认情况下，`CustomResourceValidationExpressions` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
是被启用的，以便根据**验证规则**来验证定制资源。
对于 [`kube-apiserver`](/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver/) 组件，
特性门控显式设置为 false 来禁用此特性。

这个特性只有在模式是[结构化的模式](#specifying-a-structural-schema)时才可用。

验证规则使用[通用表达式语言（CEL）](https://github.com/google/cel-spec)来验证定制资源的值。
验证规则使用 `x-kubernetes-validations` 扩展包含在 `CustomResourceDefinition` 模式定义中。

规则的作用域是模式定义中 `x-kubernetes-validations` 扩展所在的位置。
CEL 表达式中的 `self` 变量被绑定到限定作用域的取值。

所有验证规则都是针对当前对象的：不支持跨对象或有状态的验证规则。

例如:

```none
  ...
  openAPIV3Schema:
    type: object
    properties:
      spec:
        type: object
        x-kubernetes-validations:
          - rule: "self.minReplicas <= self.replicas"
            message: "replicas should be greater than or equal to minReplicas."
          - rule: "self.replicas <= self.maxReplicas"
            message: "replicas should be smaller than or equal to maxReplicas."
        properties:
          ...
          minReplicas:
            type: integer
          replicas:
            type: integer
          maxReplicas:
            type: integer
        required:
          - minReplicas
          - replicas
          - maxReplicas
```

将拒绝创建这个定制资源的请求:

```yaml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  name: my-new-cron-object
spec:
  minReplicas: 0
  replicas: 20
  maxReplicas: 10
```

返回响应为：

```
The CronTab "my-new-cron-object" is invalid:
* spec: Invalid value: map[string]interface {}{"maxReplicas":10, "minReplicas":0, "replicas":20}: replicas should be smaller than or equal to maxReplicas.
```

`x-kubernetes-validations` 可以有多条规则。

`x-kubernetes-validations` 下的 `rule` 代表将由 CEL 评估的表达式。

`message` 代表验证失败时显示的信息。如果消息没有设置，上述响应将是：

```
The CronTab "my-new-cron-object" is invalid:
* spec: Invalid value: map[string]interface {}{"maxReplicas":10, "minReplicas":0, "replicas":20}: failed rule: self.replicas <= self.maxReplicas
```

当 CRD 被创建/更新时，验证规则被编译。
如果验证规则的编译失败，CRD 的创建/更新请求将失败。
编译过程也包括类型检查。

编译失败：

- `no_matching_overload`：此函数没有参数类型的重载。

  例如，像 `self == true` 这样的规则对一个整数类型的字段将得到错误：

  ```
  Invalid value: apiextensions.ValidationRule{Rule:"self == true", Message:""}: compilation failed: ERROR: \<input>:1:6: found no matching overload for '_==_' applied to '(int, bool)'
  ```

- `no_such_field`：不包含所需的字段。

  例如，针对一个不存在的字段，像 `self.nonExistingField > 0` 这样的规则将返回错误：

  ```
  Invalid value: apiextensions.ValidationRule{Rule:"self.nonExistingField > 0", Message:""}: compilation failed: ERROR: \<input>:1:5: undefined field 'nonExistingField'
  ```

- `invalid argument`：对宏的无效参数。

  例如，像 `has(self)` 这样的规则将返回错误：

  ```
  Invalid value: apiextensions.ValidationRule{Rule:"has(self)", Message:""}: compilation failed: ERROR: <input>:1:4: invalid argument to has() macro
  ```

验证规则例子：

| 规则                                                                             | 目的                                                                             |
| ----------------                                                                 | ------------                                                                     |
| `self.minReplicas <= self.replicas && self.replicas <= self.maxReplicas`         | 验证定义副本数的三个字段大小顺序是否正确                                             |
| `'Available' in self.stateCounts`                                                | 验证 map 中是否存在键名为 `Available`的条目                                   |
| `(size(self.list1) == 0) != (size(self.list2) == 0)`                             | 验证两个 list 之一是非空的，但不是二者都非空                                   |
| <code>!('MY_KEY' in self.map1) &#124;&#124; self['MY_KEY'].matches('^[a-zA-Z]*$')</code>               | 如果某个特定的 key 在 map 中，验证 map 中这个 key 的 value |
| `self.envars.filter(e, e.name = 'MY_ENV').all(e, e.value.matches('^[a-zA-Z]*$')` | 验证一个 listMap 中主键 'name' 为 'MY_ENV' 'value' 的表项，检查其取值 'value'             |
| `has(self.expired) && self.created + self.ttl < self.expired`    | 验证 'Expired' 日期是否晚于 'Create' 日期加上 'ttl' 持续时间                   |
| `self.health.startsWith('ok')`                                                   | 验证 'health' 字符串字段有前缀 'ok'             |
| `self.widgets.exists(w, w.key == 'x' && w.foo < 10)`                             | 验证 key 为 'x' 的 listMap 项的 'foo' 属性是否小于 10                             |
| `type(self) == string ? self == '100%' : self == 1000`                           | 在 int 型和 string 型两种情况下验证 int-or-string 字段                           |
| `self.metadata.name.startsWith(self.prefix)`                                     | 验证对象的名称是否具有另一个字段值的前缀                                         |
| `self.set1.all(e, !(e in self.set2))`                                            | 验证两个 listSet 是否不相交                                                      |
| `size(self.names) == size(self.details) && self.names.all(n, n in self.details)` | 验证 'details' map 是由 'names' listSet 的项目所决定的。                         |
| `size(self.clusters.filter(c, c.name == self.primary)) == 1`                     | 验证 'primary' 属性仅在 'clusters' listMap 中出现一次且只有一次           |

参考：[CEL 中支持的求值](https://github.com/google/cel-spec/blob/v0.6.0/doc/langdef.md#evaluation)

- 如果规则的作用域是某资源的根，则它可以对 CRD 的 OpenAPIv3 模式表达式中声明的任何字段进行字段选择，
  以及 `apiVersion`、`kind`、`metadata.name` 和 `metadata.generateName`。
  这包括在同一表达式中对 `spec` 和 `status` 的字段进行选择：

  ```none
    ...
    openAPIV3Schema:
      type: object
      x-kubernetes-validations:
        - rule: "self.status.availableReplicas >= self.spec.minReplicas"
      properties:
          spec:
            type: object
            properties:
              minReplicas:
                type: integer
              ...
          status:
            type: object
            properties:
              availableReplicas:
                type: integer
  ```

- 如果规则的作用域是具有属性的对象，那么可以通过 `self.field` 对该对象的可访问属性进行字段选择，
  而字段存在与否可以通过 `has(self.field)` 来检查。
  在 CEL 表达式中，Null 值的字段被视为不存在的字段。

  ```none
    ...
    openAPIV3Schema:
      type: object
      properties:
        spec:
          type: object
          x-kubernetes-validations:
            - rule: "has(self.foo)"
          properties:
            ...
            foo:
              type: integer
  ```

- 如果规则的作用域是一个带有 additionalProperties 的对象（即map），那么 map 的值
  可以通过 `self[mapKey]` 访问，map 的包含性可以通过 `mapKey in self` 检查，
  map 中的所有条目可以通过 CEL 宏和函数如 `self.all(...)` 访问。

  ```none
    ...
    openAPIV3Schema:
      type: object
      properties:
        spec:
          type: object
          x-kubernetes-validations:
            - rule: "self['xyz'].foo > 0"
          additionalProperties:
            ...
            type: object
            properties:
              foo:
                type: integer
  ```

- 如果规则的作用域是 array，则 array 的元素可以通过 `self[i]` 访问，也可以通过宏和函数访问。

  ```none
    ...
    openAPIV3Schema:
      type: object
      properties:
        ...
        foo:
          type: array
          x-kubernetes-validations:
            - rule: "size(self) == 1"
          items:
            type: string
  ```

- 如果规则的作用域为标量，则 `self` 将绑定到标量值。

  ```none
    ...
    openAPIV3Schema:
      type: object
      properties:
        spec:
          type: object
          properties:
            ...
            foo:
              type: integer
              x-kubernetes-validations:
              - rule: "self > 0"
  ```

例子：

| 规则作用域字段类型     | 规则示例             |
| -----------------------| -----------------------|
| 根对象            | `self.status.actual <= self.spec.maxDesired`|
| 对象映射         | `self.components['Widget'].priority < 10`|
| 整数列表       | `self.values.all(value, value >= 0 && value < 100)`|
| 字符串                 | `self.startsWith('kube')`|

`apiVersion`、`kind`、`metadata.name` 和 `metadata.generateName`
始终可以从对象的根目录和任何带有 `x-kubernetes-embedded-resource` 注解的对象访问。
其他元数据属性都不可访问。

通过 `x-kubernetes-preserve-unknown-fields` 保存在定制资源中的未知数据在 CEL 表达中无法访问。
这包括：

  - 使用 `x-kubernetes-preserve-unknown-fields` 的对象模式保留的未知字段值。
  - 属性模式为"未知类型（Unknown Type）"的对象属性。一个"未知类型"被递归定义为：

    - 一个没有类型的模式，`x-kubernetes-preserve-unknown-fields` 设置为 true。
    - 一个数组，其中项目模式为"未知类型"
    - 一个 additionalProperties 模式为"未知类型"的对象

只有 `[a-zA-Z_.-/][a-zA-Z0-9_.-/]*` 形式的属性名是可访问的。
当在表达式中访问时，可访问的属性名称会根据以下规则进行转义：

| 转义序列                | 属性名称等效为        |
| ----------------------- | ----------------------|
| `__underscores__`       | `__`                  |
| `__dot__`               | `.`                   |
|`__dash__`               | `-`                   |
| `__slash__`             | `/`                   |
| `__{keyword}__`         | [CEL 保留关键字](https://github.com/google/cel-spec/blob/v0.6.0/doc/langdef.md#syntax)       |

注意：CEL 保留关键字需要与要转义的确切属性名匹配(例如，单词 `sprint` 中的 `int` 不会转义)。

转义的例子：

|属性名           | 转义属性名规则                      |
| ----------------| -----------------------             |
| namespace       | `self.__namespace__ > 0`            |
| x-prop          | `self.x__dash__prop > 0`            |
| redact__d       | `self.redact__underscores__d > 0`   |
| string          | `self.startsWith('kube')`           |

`set` 或 `map` 的 `x-Kubernetes-list-type` 的数组的等值比较会忽略元素顺序，即 `[1，2] == [2，1]`。
使用 `x-kubernetes-list-type` 对数组进行串联时，使用 List 类型的语义：

- `set`：`X + Y` 执行一个并集操作，其中 `X` 中所有元素的数组位置被保留，
  `Y` 中不相交的元素被追加，保留其部分顺序。

- `map`：`X + Y`执行合并，其中 `X` 中所有键的数组位置被保留，
  但当 `X` 和 `Y` 的键集相交时，其值被 `Y` 中的值覆盖。
  `Y` 中键值不相交的元素被附加，保留其部分顺序。

以下是 OpenAPIV3 和 CEL 类型之间的声明类型映射：

| OpenAPIv3 类型                                     | CEL 类型                                                                                                                     |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 带有 Properties 的对象                           | 对象 / "消息类型"                                                                                                      |
| 带有 AdditionalProperties 的对象                 | map                                                                                                                          |
| 带有 x-kubernetes-embedded-type 的对象           | 对象 / "消息类型"，'apiVersion'、'kind'、'metadata.name' 和 'metadata.generateName' 都隐式包含在模式中 |
| 带有 x-kubernetes-preserve-unknown-fields 的对象 | 对象 / "消息类型"，未知字段无法从 CEL 表达式中访问                                                 |
| x-kubernetes-int-or-string                         | 可能是整数或字符串的动态对象，可以用 `type(value)` 来检查类型                                |
| 数组                                            | list                                                                                                                         |
| 带有 x-kubernetes-list-type=map 的数组           | 列表，基于集合等值和唯一键名保证的 map 组成                                                                          |
| 带有 x-kubernetes-list-type=set 的数组            | 列表，基于集合等值和唯一键名保证的 set 组成                                                                        |
| 布尔值                                          | boolean                                                                                                                      |
| 数字 (各种格式)                             | double                                                                                                                       |
| 整数 (各种格式)                            | int (64)                                                                                                                     |
| 'null'                                             | null_type                                                                                                                    |
| 字符串                                           | string                                                                                                                       |
| 带有 format=byte （base64 编码）字符串         | bytes                                                                                                                        |
| 带有 format=date 字符串                          | timestamp (google.protobuf.Timestamp)                                                                                        |
| 带有 format=datetime 字符串                      | timestamp (google.protobuf.Timestamp)                                                                                        |
| 带有 format=duration 字符串                      | duration (google.protobuf.Duration)                                                                                          |

参考：[CEL 类型](https://github.com/google/cel-spec/blob/v0.6.0/doc/langdef.md#values)、
[OpenAPI 类型](https://swagger.io/specification/#data-types)、
[Kubernetes 结构化模式](/zh-cn/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#specifying-a-structural-schema)。

#### `messageExpression` 字段  {#the-messageExpression-field}

`message` 字段定义因验证规则失败时提示的字符串，与它类似，
`messageExpression` 允许你使用 CEL 表达式构造消息字符串。
这使你可以在验证失败消息中插入更详细的信息。`messageExpression`
必须计算为字符串，并且可以使用在 `rule` 字段中可用的变量。
例如：

```yaml
x-kubernetes-validations:
- rule: "self.x <= self.maxLimit"
  messageExpression: '"x exceeded max limit of " + string(self.maxLimit)'
```

请记住，CEL 字符串连接（`+` 运算符）不会自动转换为字符串。
如果你有一个非字符串标量，请使用 `string(<value>)` 函数将标量转换为字符串，如上例所示。

`messageExpression` 必须计算为一个字符串，并且在编写 CRD 时进行检查。
请注意，可以在同一个规则上设置 `message` 和 `messageExpression`，如果两者都存在，则将使用 `messageExpression`。
但是，如果 `messageExpression` 计算出错，则将使用 `message` 中定义的字符串，而 `messageExpression` 的错误将被打印到日志。
如果在 `messageExpression` 中定义的 CEL 表达式产生一个空字符串或包含换行符的字符串，也会发生这种回退。

如果满足上述条件之一且未设置 `message` 字段，则将使用默认的检查失败消息。

`messageExpression` 是一个 CEL 表达式，因此[验证函数的资源使用](#resource-use-by-validation-functions)中列出的限制也适用于它。
如果在 `messageExpression` 执行期间由于资源限制而导致计算停止，则不会执行进一步的检查规则。

#### 验证函数   {#available-validation-functions}

可用的函数包括：

  - CEL 标准函数，在[标准定义列表](https://github.com/google/cel-spec/blob/v0.7.0/doc/langdef.md#list-of-standard-definitions)中定义
  - CEL 标准[宏](https://github.com/google/cel-spec/blob/v0.7.0/doc/langdef.md#macros)
  - CEL [扩展字符串函数库](https://pkg.go.dev/github.com/google/cel-go@v0.11.2/ext#Strings)
  - Kubernetes [CEL 扩展库](https://pkg.go.dev/k8s.io/apiextensions-apiserver@v0.24.0/pkg/apiserver/schema/cel/library#pkg-functions)

#### 转换规则

包含引用标识符 `oldSself` 的表达式的规则被隐式视为 **转换规则（Transition Rule）**。
转换规则允许模式作者阻止两个原本有效的状态之间的某些转换。例如：

```yaml
type: string
enum: ["low", "medium", "high"]
x-kubernetes-validations:
- rule: "!(self == 'high' && oldSelf == 'low') && !(self == 'low' && oldSelf == 'high')"
  message: cannot transition directly between 'low' and 'high'
```

与其他规则不同，转换规则仅适用于满足以下条件的操作：

- 更新现有对象的操作。转换规则从不适用于创建操作。

- 旧的值和新的值都存在。仍然可以通过在父节点上放置转换规则来检查值是否已被添加或移除。
  转换规则从不应用于定制资源创建。当被放置在可选字段上时，转换规则将不适用于设置或取消设置该字段的更新操作。

- 被转换规则验证的模式节点的路径必须解析到一个在旧对象和新对象之间具有可比性的节点。
  例如，列表项和它们的后代（`spec.foo[10].bar`）不一定能在现有对象和后来对同一对象的更新之间产生关联。

如果一个模式节点包含一个永远不能应用的转换规则，在 CRD 写入时将会产生错误，例如：
"*path*: update rule *rule* cannot be set on schema because the schema or its parent
schema is not mergeable"。

转换规则只允许在模式的 **可关联部分（Correlatable Portions）** 中使用。
如果所有 `array` 父模式都是 `x-kubernetes-list-type=map`类型的，那么该模式的一部分就是可关联的；
任何 `set` 或者 `atomic` 数组父模式都不支持确定性地将 `self` 与 `oldSelf` 关联起来。

这是一些转换规则的例子：

{{< table caption="转换规则样例" >}}
| 用例                                                 | 规则
| --------                                             | --------
| 不可变                                               | `self.foo == oldSelf.foo`
| 赋值后禁止修改/删除                                  | `oldSelf != 'bar' \|\| self == 'bar'` or `!has(oldSelf.field) \|\| has(self.field)`
| 仅附加的 set                                         | `self.all(element, element in oldSelf)`
| 如果之前的值为 X，则新值只能为 A 或 B，不能为 Y 或 Z | `oldSelf != 'X' \|\| self in ['A', 'B']`
| 单调（非递减）计数器                                   | `self >= oldSelf`
{{< /table >}}

#### 验证函数的资源使用  {#resource-use-by-validation-functions}

当你创建或更新一个使用验证规则的 CustomResourceDefinition 时，
API 服务器会检查运行这些验证规则可能产生的影响。
如果一个规则的执行成本过高，API 服务器会拒绝创建或更新操作，并返回一个错误信息。
运行时也使用类似的系统来观察解释器的行动。如果解释器执行了太多的指令，规则的执行将被停止，并且会产生一个错误。
每个 CustomResourceDefinition 也被允许有一定数量的资源来完成其所有验证规则的执行。
如果在创建时估计其规则的总和超过了这个限制，那么也会发生验证错误。

如果你只指定那些无论输入量有多大都要花费相同时间的规则，你不太可能遇到验证的资源预算问题。
例如，一个断言 `self.foo == 1` 的规则本身不存在因为资源预算组验证而导致被拒绝的风险。
但是，如果 `foo` 是一个字符串，而你定义了一个验证规则 `self.foo.contains("someString")`，
这个规则需要更长的时间来执行，取决于 `foo` 有多长。
另一个例子是如果 `foo` 是一个数组，而你指定了验证规则 `self.foo.all(x, x > 5)`。
如果没有给出 `foo` 的长度限制，成本系统总是假设最坏的情况，这将发生在任何可以被迭代的事物上（list、map 等）。

因此，通过 `maxItems`，`maxProperties` 和 `maxLength` 进行限制被认为是最佳实践，
以在验证规则中处理任何内容，以防止在成本估算期间验证错误。例如，给定具有一个规则的模式：

```yaml
openAPIV3Schema:
  type: object
  properties:
    foo:
      type: array
      items:
        type: string
      x-kubernetes-validations:
        - rule: "self.all(x, x.contains('a string'))"
```

API 服务器以验证预算为由拒绝该规则，并显示错误：

```
spec.validation.openAPIV3Schema.properties[spec].properties[foo].x-kubernetes-validations[0].rule: Forbidden:
CEL rule exceeded budget by more than 100x (try simplifying the rule, or adding maxItems, maxProperties, and
maxLength where arrays, maps, and strings are used)
```

这个拒绝会发生是因为 `self.all` 意味着对 `foo` 中的每一个字符串调用 `contains()`，
而这又会检查给定的字符串是否包含 `'a string'`。如果没有限制，这是一个非常昂贵的规则。

如果你不指定任何验证限制，这个规则的估计成本将超过每条规则的成本限制。
但如果你在适当的地方添加限制，该规则将被允许：

```yaml
openAPIV3Schema:
  type: object
  properties:
    foo:
      type: array
      maxItems: 25
      items:
        type: string
        maxLength: 10
      x-kubernetes-validations:
        - rule: "self.all(x, x.contains('a string'))"
```

成本评估系统除了考虑规则本身的估计成本外，还考虑到规则将被执行的次数。
例如，下面这个规则的估计成本与前面的例子相同（尽管该规则现在被定义在单个数组项上）：

```yaml
openAPIV3Schema:
  type: object
  properties:
    foo:
      type: array
      maxItems: 25
      items:
        type: string
        x-kubernetes-validations:
          - rule: "self.contains('a string'))"
        maxLength: 10
```

如果在一个列表内部的一个列表有一个使用 `self.all` 的验证规则，那就会比具有相同规则的非嵌套列表的成本高得多。
一个在非嵌套列表中被允许的规则可能需要在两个嵌套列表中设置较低的限制才能被允许。
例如，即使没有设置限制，下面的规则也是允许的：

```yaml
openAPIV3Schema:
  type: object
  properties:
    foo:
      type: array
      items:
        type: integer
    x-kubernetes-validations:
      - rule: "self.all(x, x == 5)"
```

但是同样的规则在下面的模式中（添加了一个嵌套数组）产生了一个验证错误：

```yaml
openAPIV3Schema:
  type: object
  properties:
    foo:
      type: array
      items:
        type: array
        items:
          type: integer
        x-kubernetes-validations:
          - rule: "self.all(x, x == 5)"
```

这是因为 `foo` 的每一项本身就是一个数组，而每一个子数组依次调用 `self.all`。
在使用验证规则的地方，尽可能避免嵌套的列表和字典。

### 设置默认值   {#defaulting}

{{< note >}}
要使用设置默认值功能，你的 CustomResourceDefinition 必须使用 API 版本 `apiextensions.k8s.io/v1`。
{{< /note >}}

设置默认值的功能允许在 [OpenAPI v3 合法性检查模式定义](#validation)中设置默认值：

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.stable.example.com
spec:
  group: stable.example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        # openAPIV3Schema 是用来检查定制对象的模式定义
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                cronSpec:
                  type: string
                  pattern: '^(\d+|\*)(/\d+)?(\s+(\d+|\*)(/\d+)?){4}$'
                  default: "5 0 * * *"
                image:
                  type: string
                replicas:
                  type: integer
                  minimum: 1
                  maximum: 10
                  default: 1
  scope: Namespaced
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
    shortNames:
    - ct
```

使用此 CRD 定义时，`cronSpec` 和 `replicas` 都会被设置默认值：

```yaml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  name: my-new-cron-object
spec:
  image: my-awesome-cron-image
```

会生成：

```yaml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  name: my-new-cron-object
spec:
  cronSpec: "5 0 * * *"
  image: my-awesome-cron-image
  replicas: 1
```

默认值设定的行为发生在定制对象上：

* 在向 API 服务器发送的请求中，基于请求版本的设定设置默认值；
* 在从 etcd 读取对象时，使用存储版本来设置默认值；
* 在 Mutating 准入控制插件执行非空的补丁操作时，基于准入 Webhook 对象
  版本设置默认值。

从 etcd 中读取数据时所应用的默认值设置不会被写回到 etcd 中。
需要通过 API 执行更新请求才能将这种方式设置的默认值写回到 etcd。

默认值一定会被剪裁（除了 `metadata` 字段的默认值设置），且必须通过所提供的模式定义的检查。

针对 `x-kubernetes-embedded-resource: true` 节点（或者包含 `metadata` 字段的结构的默认值）
的 `metadata` 字段的默认值设置不会在 CustomResourceDefinition 创建时被剪裁，
而是在处理请求的字段剪裁阶段被删除。

#### 设置默认值和字段是否可为空（Nullable）   {#defaulting-and-nullable}

对于未设置其 nullable 标志的字段或者将该标志设置为 `false` 的字段，其空值（Null）
会在设置默认值之前被剪裁掉。如果对应字段存在默认值，则默认值会被赋予该字段。
当 `nullable` 被设置为 `true` 时，字段的空值会被保留，且不会在设置默认值时被覆盖。

例如，给定下面的 OpenAPI 模式定义：

```yaml
type: object
properties:
  spec:
    type: object
    properties:
      foo:
        type: string
        nullable: false
        default: "default"
      bar:
        type: string
        nullable: true
      baz:
        type: string
```

像下面这样创建一个为 `foo`、`bar` 和 `baz` 设置空值的对象时：

```yaml
spec:
  foo: null
  bar: null
  baz: null
```

其结果会是这样：

```yaml
spec:
  foo: "default"
  bar: null
```

其中的 `foo` 字段被剪裁掉并重新设置默认值，因为该字段是不可为空的。
`bar` 字段的 `nullable: true` 使得其能够保有其空值。
`baz` 字段则被完全剪裁掉，因为该字段是不可为空的，并且没有默认值设置。

### 以 OpenAPI 形式发布合法性检查模式  {#publish-validation-schema-in-openapi}

CustomResourceDefinition 的[结构化的](#specifying-a-structural-schema)、
[启用了剪裁的](#field-pruning) [OpenAPI v3 合法性检查模式](#validation)会在
Kubernetes API 服务器上作为
[OpenAPI 3](/zh-cn/docs/concepts/overview/kubernetes-api/#openapi-and-swagger-definitions)
和 OpenAPI v2 发布出来。建议使用 OpenAPI v3 文档，因为它是 CustomResourceDefinition OpenAPI v3
验证模式的无损表示，而 OpenAPI v2 表示有损转换。

[kubectl](/zh-cn/docs/reference/kubectl/) 命令行工具会基于所发布的模式定义来执行客户端的合法性检查
（`kubectl create` 和 `kubectl apply`），为定制资源的模式定义提供解释（`kubectl explain`）。
所发布的模式还可被用于其他目的，例如生成客户端或者生成文档。

#### Compatibility with OpenAPI V2

为了与 OpenAPI V2 兼容，OpenAPI v3 验证模式会对 OpenAPI v2 模式进行有损转换。
该模式显示在 [OpenAPI v2 规范](/zh-cn/docs/concepts/overview/kubernetes-api/#openapi-and-swagger-definitions)中的
`definitions` 和` paths` 字段中。
OpenAPI v3 合法性检查模式定义会被转换为 OpenAPI v2 模式定义，并出现在
[OpenAPI v2 规范](/zh-cn/docs/concepts/overview/kubernetes-api/#openapi-and-swagger-definitions)的
`definitions` 和 `paths` 字段中。

在转换过程中会发生以下修改，目的是保持与 1.13 版本以前的 kubectl 工具兼容。
这些修改可以避免 kubectl 过于严格，以至于拒绝它无法理解的 OpenAPI 模式定义。
转换过程不会更改 CRD 中定义的合法性检查模式定义，因此不会影响到
API 服务器中的[合法性检查](#validation)。

1. 以下字段会被移除，因为它们在 OpenAPI v2 中不支持。

   - 字段 `allOf`、`anyOf`、`oneOf` 和 `not` 会被删除

2. 如果设置了 `nullable: true`，我们会丢弃 `type`、`nullable`、`items` 和 `properties`
   OpenAPI v2 无法表达 Nullable。为了避免 kubectl 拒绝正常的对象，这一转换是必要的。

### 额外的打印列    {#additional-printer-columns}

`kubectl` 工具依赖服务器端的输出格式化。你的集群的 API 服务器决定 `kubectl
get` 命令要显示的列有哪些。
你可以为 CustomResourceDefinition 定制这些要打印的列。
下面的例子添加了 `Spec`、`Replicas` 和 `Age` 列：

将此 CustomResourceDefinition 保存到 `resourcedefinition.yaml` 文件：

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.stable.example.com
spec:
  group: stable.example.com
  scope: Namespaced
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
    shortNames:
    - ct
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              cronSpec:
                type: string
              image:
                type: string
              replicas:
                type: integer
    additionalPrinterColumns:
    - name: Spec
      type: string
      description: The cron spec defining the interval a CronJob is run
      jsonPath: .spec.cronSpec
    - name: Replicas
      type: integer
      description: The number of jobs launched by the CronJob
      jsonPath: .spec.replicas
    - name: Age
      type: date
      jsonPath: .metadata.creationTimestamp
```

创建 CustomResourceDefinition：

```shell
kubectl apply -f resourcedefinition.yaml
```

使用前文中的 `my-crontab.yaml` 创建一个实例。

启用服务器端打印输出：

```shell
kubectl get crontab my-new-cron-object
```

注意输出中的 `NAME`、`SPEC`、`REPLICAS` 和 `AGE` 列：

```
NAME                 SPEC        REPLICAS   AGE
my-new-cron-object   * * * * *   1          7s
```

{{< note >}}
`NAME` 列是隐含的，不需要在 CustomResourceDefinition 中定义。
{{< /note >}}

#### 优先级    {#priority}

每个列都包含一个 `priority`（优先级）字段。当前，优先级用来区分标准视图（Standard
View）和宽视图（Wide View）（使用 `-o wide` 标志）中显示的列：

- 优先级为 `0` 的列会在标准视图中显示。
- 优先级大于 `0` 的列只会在宽视图中显示。

#### 类型    {#type}

列的 `type` 字段可以是以下值之一
（比较 [OpenAPI v3 数据类型](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#dataTypes)）：

- `integer` – 非浮点数字
- `number` – 浮点数字
- `string` – 字符串
- `boolean` – `true` 或 `false`
- `date` – 显示为以自此时间戳以来经过的时长

如果定制资源中的值与列中指定的类型不匹配，该值会被忽略。
你可以通过定制资源的合法性检查来确保取值类型是正确的。

#### 格式    {#format}

列的 `format` 字段可以是以下值之一：

- `int32`
- `int64`
- `float`
- `double`
- `byte`
- `date`
- `date-time`
- `password`

列的 `format` 字段控制 `kubectl` 打印对应取值时采用的风格。

### 子资源     {#subresources}

定制资源支持 `/status` 和 `/scale` 子资源。

通过在 CustomResourceDefinition 中定义 `status` 和 `scale`，
可以有选择地启用这些子资源。

#### Status 子资源  {#status-subresource}

当启用了 status 子资源时，对应定制资源的 `/status` 子资源会被暴露出来。

- status 和 spec 内容分别用定制资源内的 `.status` 和 `.spec` JSON 路径来表达；
- 对 `/status` 子资源的 `PUT` 请求要求使用定制资源对象作为其输入，但会忽略
  status 之外的所有内容。
- 对 `/status` 子资源的 `PUT` 请求仅对定制资源的 status 内容进行合法性检查。
- 对定制资源的 `PUT`、`POST`、`PATCH` 请求会忽略 status 内容的改变。
- 对所有变更请求，除非改变是针对 `.metadata` 或 `.status`，`.metadata.generation`
  的取值都会增加。
- 在 CRD OpenAPI 合法性检查模式定义的根节点，只允许存在以下结构：

  - `description`
  - `example`
  - `exclusiveMaximum`
  - `exclusiveMinimum`
  - `externalDocs`
  - `format`
  - `items`
  - `maximum`
  - `maxItems`
  - `maxLength`
  - `minimum`
  - `minItems`
  - `minLength`
  - `multipleOf`
  - `pattern`
  - `properties`
  - `required`
  - `title`
  - `type`
  - `uniqueItems`

#### Scale 子资源   {#scale-subresource}

当启用了 scale 子资源时，定制资源的 `/scale` 子资源就被暴露出来。
针对 `/scale` 所发送的对象是 `autoscaling/v1.Scale`。

为了启用 scale 子资源，CustomResourceDefinition 定义了以下字段：

- `specReplicasPath` 指定定制资源内与 `scale.spec.replicas` 对应的 JSON 路径。

  - 此字段为必需值。
  - 只可以使用 `.spec` 下的 JSON 路径，只可使用带句点的路径。
  - 如果定制资源的 `specReplicasPath` 下没有取值，则针对 `/scale` 子资源执行 GET
    操作时会返回错误。

- `statusReplicasPath` 指定定制资源内与 `scale.status.replicas` 对应的 JSON 路径。

  - 此字段为必需值。
  - 只可以使用 `.status` 下的 JSON 路径，只可使用带句点的路径。
  - 如果定制资源的 `statusReplicasPath` 下没有取值，则针对 `/scale`
    子资源的副本个数状态值默认为 0。

- `labelSelectorPath` 指定定制资源内与 `Scale.Status.Selector` 对应的 JSON 路径。

  - 此字段为可选值。
  - 此字段必须设置才能使用 HPA 和 VPA。
  - 只可以使用 `.status` 或 `.spec` 下的 JSON 路径，只可使用带句点的路径。
  - 如果定制资源的 `labelSelectorPath` 下没有取值，则针对 `/scale`
    子资源的选择算符状态值默认为空字符串。
  - 此 JSON 路径所指向的字段必须是一个字符串字段（而不是复合的选择算符结构），
    其中包含标签选择算符串行化的字符串形式。

在下面的例子中，`status` 和 `scale` 子资源都被启用。

将此 CustomResourceDefinition 保存到 `resourcedefinition.yaml` 文件：

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.stable.example.com
spec:
  group: stable.example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                cronSpec:
                  type: string
                image:
                  type: string
                replicas:
                  type: integer
            status:
              type: object
              properties:
                replicas:
                  type: integer
                labelSelector:
                  type: string
      # subresources 描述定制资源的子资源
      subresources:
        # status 启用 status 子资源
        status: {}
        # scale 启用 scale 子资源
        scale:
          # specReplicasPath 定义定制资源中对应 scale.spec.replicas 的 JSON 路径
          specReplicasPath: .spec.replicas
          # statusReplicasPath 定义定制资源中对应 scale.status.replicas 的 JSON 路径 
          statusReplicasPath: .status.replicas
          # labelSelectorPath  定义定制资源中对应 scale.status.selector 的 JSON 路径 
          labelSelectorPath: .status.labelSelector
  scope: Namespaced
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
    shortNames:
    - ct
```

之后创建此 CustomResourceDefinition：

```shell
kubectl apply -f resourcedefinition.yaml
```

CustomResourceDefinition 对象创建完毕之后，你可以创建定制对象，。

如果你将下面的 YAML 保存到 `my-crontab.yaml` 文件：

```yaml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  name: my-new-cron-object
spec:
  cronSpec: "* * * * */5"
  image: my-awesome-cron-image
  replicas: 3
```

并创建定制对象：

```shell
kubectl apply -f my-crontab.yaml
```

那么会创建新的、命名空间作用域的 RESTful  API 端点：

```none
/apis/stable.example.com/v1/namespaces/*/crontabs/status
```

和

```none
/apis/stable.example.com/v1/namespaces/*/crontabs/scale
```

定制资源可以使用 `kubectl scale` 命令来扩缩其规模。
例如下面的命令将前面创建的定制资源的 `.spec.replicas` 设置为 5：

```shell
kubectl scale --replicas=5 crontabs/my-new-cron-object
crontabs "my-new-cron-object" scaled

kubectl get crontabs my-new-cron-object -o jsonpath='{.spec.replicas}'
5
```

你可以使用 [PodDisruptionBudget](/zh-cn/docs/tasks/run-application/configure-pdb/)
来保护启用了 scale 子资源的定制资源。

### 分类   {#categories}

分类（Categories）是定制资源所归属的分组资源列表（例如，`all`）。
你可以使用 `kubectl get <分类名称>` 来列举属于某分类的所有资源。

下面的示例在 CustomResourceDefinition 中将 `all` 添加到分类列表中，
并展示了如何使用 `kubectl get all` 来输出定制资源：

将下面的 CustomResourceDefinition 保存到 `resourcedefinition.yaml` 文件中：

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.stable.example.com
spec:
  group: stable.example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                cronSpec:
                  type: string
                image:
                  type: string
                replicas:
                  type: integer
  scope: Namespaced
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
    shortNames:
    - ct
    # categories 是定制资源所归属的分类资源列表
    categories:
    - all
```

之后创建此 CRD：

```shell
kubectl apply -f resourcedefinition.yaml
```

创建了 CustomResourceDefinition 对象之后，你可以创建定制对象。

将下面的 YAML 保存到 `my-crontab.yaml` 中：

```yaml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  name: my-new-cron-object
spec:
  cronSpec: "* * * * */5"
  image: my-awesome-cron-image
```

并创建定制对象：

```shell
kubectl apply -f my-crontab.yaml
```

你可以在使用 `kubectl get` 时指定分类：

```shell
kubectl get all
```

输出中将包含类别为 `CronTab` 的定制资源：

```none
NAME                          AGE
crontabs/my-new-cron-object   3s
```

## {{% heading "whatsnext" %}}

* 阅读了解[定制资源](/zh-cn/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
* 参阅 [CustomResourceDefinition](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#customresourcedefinition-v1-apiextensions-k8s-io)
* 参阅支持 CustomResourceDefinition 的[多个版本](/zh-cn/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/)

