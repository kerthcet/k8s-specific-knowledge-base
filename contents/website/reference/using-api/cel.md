---
title: Kubernetes 中的通用表达式语言
content_type: concept
weight: 35
min-kubernetes-server-version: 1.25
---


[通用表达式语言 (Common Expression Language, CEL)](https://github.com/google/cel-go)
用于声明 Kubernetes API 的验证规则、策略规则和其他限制或条件。

CEL 表达式在{{< glossary_tooltip text="API 服务器" term_id="kube-apiserver" >}}中直接进行评估，
这使得 CEL 成为许多可扩展性用例的便捷替代方案，而无需使用类似 Webhook 这种进程外机制。
只要控制平面的 API 服务器组件保持可用状态，你的 CEL 表达式就会继续执行。


## 语言概述 {#language-overview}

[CEL 语言](https://github.com/google/cel-spec/blob/master/doc/langdef.md)的语法直观简单，
类似于 C、C++、Java、JavaScript 和 Go 中的表达式。

CEL 的设计目的是嵌入应用程序中。每个 CEL "程序" 都是一个单独的表达式，其评估结果为单个值。
CEL 表达式通常是短小的 "一行式"，可以轻松嵌入到 Kubernetes API 资源的字符串字段中。

对 CEL 程序的输入是各种 “变量”。包含 CEL 的每个 Kubernetes API 字段都在 API
文档中声明了字段可使用哪些变量。例如，在 CustomResourceDefinitions 的
`x-kubernetes-validations[i].rules` 字段中，`self` 和 `oldSelf` 变量可用，
并且分别指代要由 CEL 表达式验证的自定义资源数据的前一个状态和当前状态。
其他 Kubernetes API 字段可能声明不同的变量。请查阅 API 字段的 API 文档以了解该字段可使用哪些变量。

CEL 表达式示例：

{{< table caption="CEL 表达式例子和每个表达式的用途" >}}
| 规则 | 用途 |
|---------------------------------------------------------------------------|--------------------------------------------------------------|
| `self.minReplicas <= self.replicas && self.replicas <= self.maxReplicas`  | 验证定义副本的三个字段被正确排序                                   |
| `'Available' in self.stateCounts`                                         | 验证映射中存在主键为 'Available' 的条目                           |
| `(self.list1.size() == 0) != (self.list2.size() == 0)`                    | 验证两个列表中有一个非空，但不是两个都非空                           |
| `self.envars.filter(e, e.name = 'MY_ENV').all(e, e.value.matches('^[a-zA-Z]*$')` | 验证 listMap 条目的 'value' 字段，其主键字段 'name' 是 'MY_ENV' |
| `has(self.expired) && self.created + self.ttl < self.expired`             | 验证 'expired' 日期在 'create' 日期加上 'ttl' 持续时间之后         |
| `self.health.startsWith('ok')`                                            | 验证 'health' 字符串字段具有前缀 'ok'                             |
| `self.widgets.exists(w, w.key == 'x' && w.foo < 10)`                      | 验证具有键 'x' 的 listMap 项的 'foo' 属性小于 10                  |
| `type(self) == string ? self == '99%' : self == 42`                       | 验证 int-or-string 字段是否同时具备 int 和 string 的属性           |
| `self.metadata.name == 'singleton'`                                       | 验证某对象的名称与特定的值匹配（使其成为一个特例）                     |
| `self.set1.all(e, !(e in self.set2))`                                     | 验证两个 listSet 不相交                                          |
| `self.names.size() == self.details.size() && self.names.all(n, n in self.details)` | 验证 'details' 映射是由 'names' listSet 中的各项键入的 |
{{< /table >}}

## CEL 社区库 {#cel-community-libraries}

Kubernetes CEL 表达式能够访问以下 CEL 社区库：

- [标准定义列表](https://github.com/google/cel-spec/blob/master/doc/langdef.md#list-of-standard-definitions)中定义的
  CEL 标准函数
- CEL 标准[宏](https://github.com/google/cel-spec/blob/v0.7.0/doc/langdef.md#macros)
- CEL [扩展字符串函数库](https://pkg.go.dev/github.com/google/cel-go/ext#Strings)

## Kubernetes CEL 库 {#kubernetes-cel-libraries}

除了 CEL 社区库之外，Kubernetes 还包括在 Kubernetes 中使用 CEL 时所有可用的 CEL 库。

### Kubernetes 列表库 {#kubernetes-list-library}

列表库包括 `indexOf` 和 `lastIndexOf`，这两个函数的功能类似于同名的字符串函数。
这些函数返回提供的元素在列表中的第一个或最后一个位置索引。

列表库还包括 `min`、`max` 和 `sum`。
`sum` 可以用于所有数字类型以及持续时间类型。
`min` 和 `max` 可用于所有可比较的类型。

`isSorted` 也作为一个便捷的函数提供，并且支持所有可比较的类型。

例如：

{{< table caption="使用列表库函数的 CEL 表达式例子" >}}
| CEL 表达式                                                                          | 用途 |
|------------------------------------------------------------------------------------|-----------------------------------|
| `names.isSorted()`                                                                 | 验证名称列表是否按字母顺序排列         |
| `items.map(x, x.weight).sum() == 1.0`                                              | 验证对象列表的 “weight” 总和为 1.0   |
| `lowPriorities.map(x, x.priority).max() < highPriorities.map(x, x.priority).min()` | 验证两组优先级不重叠                 |
| `names.indexOf('should-be-first') == 1`                                            | 如果是特定值，则使用列表中的第一个名称  |

更多信息请查阅 Go 文档：
[Kubernetes 列表库](https://pkg.go.dev/k8s.io/apiextensions-apiserver/pkg/apiserver/schema/cel/library#Lists)。
{{< /table >}}

### Kubernetes 正则表达式库 {#kubernete-regex-library}

除了 CEL 标准库提供的 `matches` 函数外，正则表达式库还提供了 `find` 和 `findAll`，
使得更多种类的正则表达式运算成为可能。

例如：

{{< table caption="使用正则表达式库函数的 CEL 表达式例子" >}}
| CEL 表达式                                                   | 用途                       |
|-------------------------------------------------------------|----------------------------|
| `"abc 123".find('[0-9]*')`                                  | 找到字符串中的第一个数字       |
| `"1, 2, 3, 4".findAll('[0-9]*').map(x, int(x)).sum() < 100` | 验证字符串中的数字之和小于 100 |
{{< /table >}}

更多信息请查阅 Go 文档：
[Kubernetes 正则表达式库](https://pkg.go.dev/k8s.io/apiextensions-apiserver/pkg/apiserver/schema/cel/library#Regex)。

### Kubernetes URL 库 {#kubernetes-url-library}

为了更轻松、更安全地处理 URL，添加了以下函数：

- `isURL(string)` 按照
  [Go 的 net/url](https://pkg.go.dev/net/url#URL)
  检查字符串是否是一个有效的 URL。该字符串必须是一个绝对 URL。
- `url(string) URL` 将字符串转换为 URL，如果字符串不是一个有效的 URL，则返回错误。

一旦通过 `url` 函数解析，所得到的 URL 对象就具有
`getScheme`、`getHost`、`getHostname`、`getPort`、`getEscapedPath` 和 `getQuery` 访问器。

例如：

{{< table caption="使用 URL 库函数的 CEL 表达式例子" >}}
| CEL 表达式                                                       | 用途                                |
|-----------------------------------------------------------------|------------------------------------|
| `url('https://example.com:80/').getHost()`                      | 获取 URL 的 'example.com:80' 主机部分 |
| `url('https://example.com/path with spaces/').getEscapedPath()` | 返回 '/path%20with%20spaces/'       |
{{< /table >}}

更多信息请查阅 Go 文档：
[Kubernetes URL 库](https://pkg.go.dev/k8s.io/apiextensions-apiserver/pkg/apiserver/schema/cel/library#URLs)。

### Kubernetes 鉴权组件库

在 API 中使用 CEL 表达式，可以使用类型为 `Authorizer` 的变量，
这个鉴权组件可用于对请求的主体（已认证用户）执行鉴权检查。

API 资源检查的过程如下：

1. 指定要检查的组和资源：`Authorizer.group(string).resource(string) ResourceCheck`
2. 可以调用以下任意组合的构建器函数（Builder Function），以进一步缩小鉴权检查范围。
   注意这些函数将返回接收者的类型，并且可以串接起来：
   - `ResourceCheck.subresource(string) ResourceCheck`
   - `ResourceCheck.namespace(string) ResourceCheck`
   - `ResourceCheck.name(string) ResourceCheck` 
3. 调用 `ResourceCheck.check(verb string) Decision` 来执行鉴权检查。
4. 调用 `allowed() bool` 或 `reason() string` 来查验鉴权检查的结果。

对非资源访问的鉴权过程如下：

1. 仅指定路径：`Authorizer.path(string) PathCheck`
1. 调用 `PathCheck.check(httpVerb string) Decision` 来执行鉴权检查。
1. 调用 `allowed() bool` 或 `reason() string` 来查验鉴权检查的结果。

对于服务账号执行鉴权检查的方式：

- `Authorizer.serviceAccount(namespace string, name string) Authorizer`

{{< table caption="使用 URL 库函数的 CEL 表达式示例" >}}
| CEL 表达式                                       | 用途                                           |
|-------------------------------------------------|------------------------------------------------|
| `authorizer.group('').resource('pods').namespace('default').check('create').allowed()`  | 如果主体（用户或服务账号）被允许在 `default` 名字空间中创建 Pod，返回 true。 |
| `authorizer.path('/healthz').check('get').allowed()`   | 检查主体（用户或服务账号）是否有权限向 /healthz API 路径发出 HTTP GET 请求。 |
| `authorizer.serviceAccount('default', 'myserviceaccount').resource('deployments').check('delete').allowed()` | 检查服务账号是否有权限删除 Deployment。 |
{{< /table >}}

更多信息请参阅 Go 文档：
[Kubernetes Authz library](https://pkg.go.dev/k8s.io/apiserver/pkg/cel/library#Authz)。

## 类型检查 {#type-checking}

CEL 是一种[逐渐类型化的语言](https://github.com/google/cel-spec/blob/master/doc/langdef.md#gradual-type-checking)。

一些 Kubernetes API 字段包含完全经过类型检查的 CEL 表达式。
例如，[CustomResourceDefinitions 验证规则](/zh-cn/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#validation-rules)就是完全经过类型检查的。

一些 Kubernetes API 字段包含部分经过类型检查的 CEL 表达式。
部分经过类型检查的表达式是指一些变量是静态类型，而另一些变量是动态类型的表达式。
例如在 [ValidatingAdmissionPolicies](/zh-cn/docs/reference/access-authn-authz/validating-admission-policy/)
的 CEL 表达式中，`request` 变量是有类型的，但 `object` 变量是动态类型的。
因此，包含 `request.namex` 的表达式将无法通过类型检查，因为 `namex` 字段未定义。
然而，即使对于 `object` 所引用的资源种类没有定义 `namex` 字段，
`object.namex` 也会通过类型检查，因为 `object` 是动态类型。

在 CEL 中，`has()` 宏可用于检查动态类型变量的字段是否可访问，然后再尝试访问该字段的值。
例如：

```cel
has(object.namex) ? object.namex == 'special' : request.name == 'special'
```

## 类型系统集成 {#type-system-integration}

{{< table caption="表格显示了 OpenAPIv3 类型和 CEL 类型之间的关系" >}}
| OpenAPIv3 类型                                      | CEL 类型                                                                                          |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------|
| 设置了 properties 的 'object'                       | object / "message type" (`type(<object>)` 评估为 `selfType<uniqueNumber>.path.to.object.from.self` |
| 设置了 AdditionalProperties 的 'object'             | map                                                                                               |
| 设置了 x-kubernetes-embedded-type 的 'object'       | object / "message type"，'apiVersion'、'kind'、'metadata.name' 和 'metadata.generateName' 被隐式包含在模式中 |
| 设置了 x-kubernetes-preserve-unknown-fields 的 'object' | object / "message type"，CEL 表达式中不可访问的未知字段                                            |
| x-kubernetes-int-or-string                      | int 或 string 的并集，`self.intOrString < 100 \|\| self.intOrString == '50%'` 对于 `50` 和 `"50%"`都评估为 true |
| 'array'                                        | list                                                                                                 |
| 设置了 x-kubernetes-list-type=map 的 'array'    | list，具有基于 Equality 和唯一键保证的 map                                                               |
| 设置了 x-kubernetes-list-type=set 的 'array'    | list，具有基于 Equality 和唯一条目保证的 set                                                             |
| 'boolean'                                     | boolean                                                                                              |
| 'number' (所有格式)                            | double                                                                                                |
| 'integer' (所有格式)                           | int (64)                                                                                              |
| **非等价 **                                    | uint (64)                                                                                             |
| 'null'                                        | null_type                                                                                             |
| 'string'                                      | string                                                                                                |
| 设置了 format=byte 的 'string'（以 base64 编码） | bytes                                                                                                 |
| 设置了 format=date 的 'string'                 | timestamp (google.protobuf.Timestamp)                                                                 |
| 设置了 format=datetime 的 'string'             | timestamp (google.protobuf.Timestamp)                                                                 |
| 设置了 format=duration 的 'string'             | duration (google.protobuf.Duration)                                                                   |
{{< /table >}}

另见：[CEL 类型](https://github.com/google/cel-spec/blob/v0.6.0/doc/langdef.md#values)、
[OpenAPI 类型](https://swagger.io/specification/#data-types)、
[Kubernetes 结构化模式](/zh-cn/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#specifying-a-structural-schema)。

`x-kubernetes-list-type` 为 `set` 或 `map` 的数组进行相等比较时会忽略元素顺序。
例如，如果这些数组代表 Kubernetes 的 `set` 值，则 `[1, 2] == [2, 1]`。

使用 `x-kubernetes-list-type` 的数组进行串接时，使用 list 类型的语义：

- `set`：`X + Y` 执行并集操作，保留 `X` 中所有元素的数组位置，
  将 `Y` 中非交集元素追加到 `X` 中，保留它们的部分顺序。
- `map`：`X + Y` 执行合并操作，保留 `X` 中所有键的数组位置，
  但是当 `X` 和 `Y` 的键集相交时，将 `Y` 中的值覆盖 `X` 中的值。
  将 `Y` 中非交集键的元素附加到 `X` 中，保留它们的部分顺序。

## 转义 {#escaping}

仅形如 `[a-zA-Z_.-/][a-zA-Z0-9_.-/]*` 的 Kubernetes 资源属性名可以从 CEL 中访问。
当在表达式中访问可访问的属性名时，会根据以下规则进行转义：

{{< table caption="CEL 标识符转义规则表" >}}
| 转义序列            | 等价的属性名                                                                              |
|-------------------|------------------------------------------------------------------------------------------|
| `__underscores__` | `__`                                                                                     |
| `__dot__`         | `.`                                                                                      |
| `__dash__`        | `-`                                                                                      |
| `__slash__`       | `/`                                                                                      |
| `__{keyword}__` | [CEL **保留的** 关键字](https://github.com/google/cel-spec/blob/v0.6.0/doc/langdef.md#syntax) |
{{< /table >}}

当你需要转义 CEL 的任一 **保留的** 关键字时，你需要使用下划线转义来完全匹配属性名
（例如，`sprint` 这个单词中的 `int` 不会被转义，也不需要被转义）。

转义示例：

{{< table caption="转义的 CEL 标识符例子" >}}
| 属性名称       | 带有转义的属性名称的规则              |
|---------------|-----------------------------------|
| `namespace`   | `self.__namespace__ > 0`          |
| `x-prop`      | `self.x__dash__prop > 0`          |
| `redact__d`   | `self.redact__underscores__d > 0` |
| `string`      | `self.startsWith('kube')`         |
{{< /table >}}

## 资源约束 {#resource-constraints}

CEL 不是图灵完备的，提供了多种生产安全控制手段来限制执行时间。
CEL 的**资源约束**特性提供了关于表达式复杂性的反馈，并帮助保护 API 服务器免受过度的资源消耗。
CEL 的资源约束特性用于防止 CEL 评估消耗过多的 API 服务器资源。

资源约束特性的一个关键要素是 CEL 定义的**成本单位**，它是一种跟踪 CPU 利用率的方式。
成本单位独立于系统负载和硬件。成本单位也是确定性的；对于任何给定的 CEL 表达式和输入数据，
由 CEL 解释器评估表达式将始终产生相同的成本。

CEL 的许多核心运算具有固定成本。例如比较（例如 `<`）这类最简单的运算成本为 1。
有些运算具有更高的固定成本，例如列表字面声明具有 40 个成本单位的固定基础成本。

调用本地代码实现的函数时，基于运算的时间复杂度估算其成本。
举例而言：`match` 和 `find` 这类使用正则表达式的运算使用
`length(regexString)*length(inputString)` 的近似成本进行估算。
这个近似的成本反映了 Go 的 RE2 实现的最坏情况的时间复杂度。

### 运行时成本预算 {#runtime-cost-budget}

所有由 Kubernetes 评估的 CEL 表达式都受到运行时成本预算的限制。
运行时成本预算是通过在解释 CEL 表达式时增加成本单元计数器来计算实际 CPU 利用率的估算值。
如果 CEL 解释器执行的指令太多，将超出运行时成本预算，表达式的执行将停止，并将出现错误。

一些 Kubernetes 资源定义了额外的运行时成本预算，用于限制多个表达式的执行。
如果所有表达式的成本总和超过预算，表达式的执行将停止，并将出现错误。
例如，自定义资源的验证具有针对验证自定义资源所评估的所有
[验证规则](/zh-cn/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#validation-rules)的
**每个验证** 运行时成本预算。

### 估算的成本限制 {#estimated-cost-limits}

对于某些 Kubernetes 资源，API 服务器还可能检查 CEL 表达式的最坏情况估计运行时间是否过于昂贵而无法执行。
如果是，则 API 服务器会拒绝包含 CEL 表达式的创建或更新操作，以防止 CEL 表达式被写入 API 资源。
此特性提供了更强的保证，即写入 API 资源的 CEL 表达式将在运行时进行评估，而不会超过运行时成本预算。
