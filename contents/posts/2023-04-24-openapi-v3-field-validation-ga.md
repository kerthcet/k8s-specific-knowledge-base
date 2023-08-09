---
layout: blog
title: "Kubernetes 1.27：服务器端字段校验和 OpenAPI V3 进阶至 GA"
date: 2023-04-24
slug: openapi-v3-field-validation-ga
---

**作者**：Jeffrey Ying (Google), Antoine Pelisse (Google)

**译者**：Michael Yao (DaoCloud)

在 Kubernetes v1.8 之前，YAML 文件中的拼写错误、缩进错误或其他小错误可能会产生灾难性后果
（例如像在 `replica: 1000` 中忘记了结尾的字母 “s”，可能会导致宕机。
因为该值会被忽略并且丢失，并强制将副本重置回 1）。当时解决这个问题的办法是：
在 kubectl 中获取 OpenAPI v2 并在应用之前使用 OpenAPI v2 来校验字段是否正确且存在。
不过当时没有自定义资源定义 (CRD)，相关代码是在当时那样的假设下编写的。
之后引入了 CRD，发现校验代码缺乏灵活性，迫使 CRD 在公开其模式定义时做出了一些艰难的决策，
使得我们进入了不良校验造成不良 OpenAPI，不良 OpenAPI 无法校验的循环。
随着新的 OpenAPI v3 和服务器端字段校验在 1.27 中进阶至 GA，我们现在已经解决了这两个问题。

服务器端字段校验针对通过 create、update 和 patch 请求发送到 apiserver 上的资源进行校验，
此特性是在 Kubernetes v1.25 中添加的，在 v1.26 时进阶至 Beta，
如今在 v1.27 进阶至 GA。它在服务器端提供了 kubectl 校验的所有功能。

[OpenAPI](https://swagger.io/specification/) 是一个标准的、与编程语言无关的接口，
用于发现 Kubernetes 集群支持的操作集和类型集。
OpenAPI v3 是 OpenAPI 的最新标准，它是自 Kubernetes 1.5 开始支持的
[OpenAPI v2](https://kubernetes.io/blog/2016/12/kubernetes-supports-openapi/)
的改进版本。对 OpenAPI v3 的支持是在 Kubernetes v1.23 中添加的，
v1.24 时进阶至 Beta，如今在 v1.27 进阶至 GA。

## OpenAPI v3

### OpenAPI v3 相比 v2 提供了什么？

#### 插件类型

Kubernetes 对 OpenAPI v2 中不能表示或有时在 Kubernetes 生成的 OpenAPI v2
中未表示的某些字段提供了注解。最明显地，OpenAPI v3 发布了 “default” 字段，
而在 OpenAPI v2 中被省略。表示多种类型的单个类型也能在 OpenAPI v3 中使用
oneOf 字段被正确表达。这包括针对 IntOrString 和 Quantity 的合理表示。

#### CRD

在 Kubernetes 中，自定义资源定义 (CRD) 使用结构化的 OpenAPI v3 模式定义，
无法在不损失某些字段的情况下将其表示为 OpenAPI v2。这些包括
nullable、default、anyOf、oneOf、not 等等。OpenAPI v3 是
CustomResourceDefinition 结构化模式定义的完全无损表示。

### 如何使用？

Kubernetes API 服务器的 `/openapi/v3` 端点包含了 OpenAPI v3 的根发现文档。
为了减少传输的数据量，OpenAPI v3 文档以 group-version 的方式进行分组，
不同的文档可以通过 `/openapi/v3/apis/<group>/<version>` 和 `/openapi/v3/api/v1`
（表示旧版 group）进行访问。有关此端点的更多信息请参阅
[Kubernetes API 文档](/zh-cn/docs/concepts/overview/kubernetes-api/)。

众多使用 OpenAPI 的客户侧组件已更新到了 v3，包括整个 kubectl 和服务器端应用。
在 [client-go](https://github.com/kubernetes/client-go/blob/release-1.27/openapi3/root.go)
中也提供了 OpenAPI V3 Golang 客户端。

## 服务器端字段校验

查询参数 `fieldValidation` 可用于指示服务器应执行的字段校验级别。
如果此参数未被传递，服务器端字段校验默认采用 `Warn` 模式。

- Strict：严格的字段校验，在验证失败时报错
- Warn：执行字段校验，但错误会以警告的形式给出，而不是使请求失败
- Ignore：不执行服务器端的字段校验

kubectl 将跳过客户端校验，并将自动使用 `Strict` 模式下的服务器端字段校验。
控制器默认使用 `Warn` 模式进行服务器端字段校验。

使用客户端校验时，由于 OpenAPI v2 中缺少某些字段，所以我们必须更加宽容，
以免拒绝可能有效的对象。而在服务器端校验中，所有这些问题都被修复了。
可以在[此处](/zh-cn/docs/reference/using-api/api-concepts/#field-validation)找到更多文档。

## 未来展望

随着服务器端字段校验和 OpenAPI v3 以 GA 发布，我们引入了更准确的 Kubernetes 资源表示。
建议使用服务器端字段校验而非客户端校验，但是通过 OpenAPI v3，
客户端可以在必要时自行实现其自身的校验（“左移”），我们保证 OpenAPI 发布的是完全无损的模式定义。

现在的一些工作将进一步改善通过 OpenAPI 提供的信息，例如
[CEL 校验和准入](/zh-cn/docs/reference/using-api/cel/)以及对内置类型的 OpenAPI 注解。

使用在 OpenAPI v3 中的类型信息还可以构建许多其他工具来编写和转换资源。

## 如何参与？

这两个特性由 SIG API Machinery 社区驱动，欢迎加入 Slack 频道 \#sig-api-machinery，
请查阅[邮件列表](https://groups.google.com/g/kubernetes-sig-api-machinery)，
我们每周三 11:00 AM PT 在 Zoom 上召开例会。

我们对所有曾帮助设计、实现和审查这两个特性的贡献者们表示衷心的感谢。

- Alexander Zielenski
- Antoine Pelisse
- Daniel Smith
- David Eads
- Jeffrey Ying
- Jordan Liggitt
- Kevin Delgado
- Sean Sullivan
