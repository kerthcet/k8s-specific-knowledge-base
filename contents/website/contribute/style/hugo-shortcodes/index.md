---
title: 定制 Hugo 短代码
content_type: concept
weight: 120
---


本页面将介绍 Hugo 自定义短代码，可以用于 Kubernetes Markdown 文档书写。

关于短代码的更多信息可参见 [Hugo 文档](https://gohugo.io/content-management/shortcodes)。


## 功能状态 {#feature-state}

在本站的 Markdown 页面（`.md` 文件）中，你可以加入短代码来展示所描述的功能特性的版本和状态。

### 功能状态示例 {#feature-state-demo}

下面是一个功能状态代码段的演示，表明这个功能已经在最新版 Kubernetes 中稳定了。

```
{{</* feature-state state="stable" */>}}
```

会转换为：

{{< feature-state state="stable" >}}

`state` 的可选值如下：

* alpha
* beta
* deprecated
* stable

### 功能状态代码 {#feature-state-code}

所显示的 Kubernetes 默认为该页或站点版本。
修改 <code>for_k8s_version</code> 短代码参数可以调整要显示的版本。例如：

```
{{</* feature-state for_k8s_version="v1.10" state="beta" */>}}
```

会转换为：

{{< feature-state for_k8s_version="v1.10" state="beta" >}}

## 词汇 {#glossary}

有两种词汇表提示：`glossary_tooltip` 和 `glossary_definition`。

你可以通过加入术语词汇的短代码，来自动更新和替换相应链接中的内容
（[我们的词汇库](/zh-cn/docs/reference/glossary/)）
在浏览在线文档时，术语会显示为超链接的样式，当鼠标移到术语上时，其解释就会显示在提示框中。

除了包含工具提示外，你还可以重用页面内容中词汇表中的定义。

词汇术语的原始数据保存在[词汇目录](https://github.com/kubernetes/website/tree/main/content/en/docs/reference/glossary)，
每个内容文件对应相应的术语解释。

### 词汇演示 {#glossary-demo}

例如下面的代码在 Markdown 中将会转换为
{{< glossary_tooltip text="cluster" term_id="cluster" >}}，然后在提示框中显示。

```
{{</* glossary_tooltip text="cluster" term_id="cluster" */>}}
```
这是一个简短的词汇表定义：

```
{{</* glossary_definition prepend="A cluster is" term_id="cluster" length="short" */>}}
```

呈现为： 
{{< glossary_definition prepend="A cluster is" term_id="cluster" length="short" >}}

你也可以包括完整的定义：

```
{{</* glossary_definition term_id="cluster" length="all" */>}}
```

呈现为： 
{{< glossary_definition term_id="cluster" length="all" >}}

## 链接至 API 参考 {#links-to-api-reference}

你可以使用 `api-reference` 短代码链接到 Kubernetes API 参考页面，例如：
Pod
{{< api-reference page="workload-resources/pod-v1" >}} 参考文件：

```
{{</* api-reference page="workload-resources/pod-v1" */>}}
```

本语句中 `page` 参数的内容是 API 参考页面的 URL 后缀。


你可以通过指定 `anchor` 参数链接到页面中的特定位置，例如到
{{< api-reference page="workload-resources/pod-v1" anchor="PodSpec" >}} 参考，或页面的
{{< api-reference page="workload-resources/pod-v1" anchor="environment-variables" >}}
部分：

```
{{</* api-reference page="workload-resources/pod-v1" anchor="PodSpec" */>}}
{{</* api-reference page="workload-resources/pod-v1" anchor="environment-variables" */>}}
```


你可以通过指定 `text` 参数来更改链接的文本，例如通过链接到页面的
{{< api-reference page="workload-resources/pod-v1" anchor="environment-variables" text="环境变量">}}
部分：

```
{{</* api-reference page="workload-resources/pod-v1" anchor="environment-variables" text="环境变量" */>}}
```


## 表格标题  {#table-captions}

通过添加表格标题，你可以让表格能够被屏幕阅读器读取。
要向表格添加[标题（Caption）](https://www.w3schools.com/tags/tag_caption.asp)，
可用 `table` 短代码包围表格定义，并使用 `caption` 参数给出表格标题。

{{< note >}}
表格标题对屏幕阅读器是可见的，但在标准 HTML 中查看时是不可见的。
{{< /note >}}

下面是一个例子：


```go-html-template
{{</* table caption="配置参数" >}}
参数      | 描述        | 默认值
:---------|:------------|:-------
`timeout` | 请求的超时时长 | `30s`
`logLevel` | 日志输出的级别 | `INFO`
{{< /table */>}}
```

所渲染的表格如下：

{{< table caption="配置参数" >}}
参数      | 描述        | 默认值
:---------|:------------|:-------
`timeout` | 请求的超时时长 | `30s`
`logLevel` | 日志输出的级别 | `INFO`
{{< /table >}}

如果你查看表格的 HTML 输出结果，你会看到 `<table>` 元素
后面紧接着下面的元素：

```html
<caption style="display: none;">配置参数</caption>
```

## 标签页 {#tabs}

在本站的 Markdown 页面（`.md` 文件）中，你可以加入一个标签页集来显示
某解决方案的不同形式。

标签页的短代码包含以下参数：

* `name`： 标签页上显示的名字。
* `codelang`: 如果要在 `tab` 短代码中加入内部内容，需要告知 Hugo 使用的是什么代码语言，方便代码高亮。
* `include`: 标签页中所要包含的文件。如果标签页是在 Hugo 的
  [叶子包](https://gohugo.io/content-management/page-bundles/#leaf-bundles)中定义，
  Hugo 会在包内查找文件（可以是 Hugo 所支持的任何 MIME 类型文件）。
  否则，Hugo 会在当前路径的相对路径下查找所要包含的内容页面。
  注意，在 `include` 页面中不能包含短代码内容，必须要使用自结束（self-closing）语法。
  例如 `{{</* tab name="Content File #1" include="example1" /*/>}}`。
  如果没有在 `codelang` 进行声明的话，Hugo 会根据文件名推测所用的语言。
  默认情况下，非内容文件将会被代码高亮。

* 如果内部内容是 Markdown，你必须要使用 `%` 分隔符来包装标签页。
  例如，`{{%/* tab name="Tab 1" %}}This is **markdown**{{% /tab */%}}`。
* 可以在标签页集中混合使用上面的各种变形。

下面是标签页短代码的示例。

{{< note >}}
内容页面下的 **tabs** 定义中的标签页 **name** 必须是唯一的。
{{< /note >}}

### 标签页演示：代码高亮

```go-text-template
{{</* tabs name="tab_with_code" >}}
{{< tab name="Tab 1" codelang="bash" >}}
echo "This is tab 1."
{{< /tab >}}
{{< tab name="Tab 2" codelang="go" >}}
println "This is tab 2."
{{< /tab >}}
{{< /tabs */>}}
```

会转换为：

{{< tabs name="tab_with_code" >}}
{{< tab name="Tab 1" codelang="bash" >}}
echo "This is tab 1."
{{< /tab >}}
{{< tab name="Tab 2" codelang="go" >}}
println "This is tab 2."
{{< /tab >}}
{{< /tabs >}}

### 标签页演示：内联 Markdown 和 HTML

```go-html-template
{{</* tabs name="tab_with_md" >}}
{{% tab name="Markdown" %}}
这是 **一些 markdown。**
{{< note >}}
它甚至可以包含短代码。
{{< /note >}}
{{% /tab %}}
{{< tab name="HTML" >}}
<div>
	<h3>纯 HTML</h3>
	<p>这是一些 <i>纯</i> HTML。</p>
</div>
{{< /tab >}}
{{< /tabs */>}}
```

会转换为：

{{< tabs name="tab_with_md" >}}
{{% tab name="Markdown" %}}
这是 **一些 markdown。**
{{< note >}}
它甚至可以包含短代码。
{{< /note >}}
{{% /tab %}}
{{< tab name="HTML" >}}
<div>
	<h3>纯 HTML</h3>
	<p>这是一些 <i>纯</i> HTML。</p>
</div>
{{< /tab >}}
{{< /tabs >}}

### 标签页演示：文件嵌套

```go-text-template
{{</* tabs name="tab_with_file_include" >}}
{{< tab name="Content File #1" include="example1" />}}
{{< tab name="Content File #2" include="example2" />}}
{{< tab name="JSON File" include="podtemplate" />}}
{{< /tabs */>}}
```

会转换为：

{{< tabs name="tab_with_file_include" >}}
{{< tab name="Content File #1" include="example1" />}}
{{< tab name="Content File #2" include="example2" />}}
{{< tab name="JSON File" include="podtemplate.json" />}}
{{< /tabs >}}

你可以使用 `{{</* codenew */>}}` 短代码将文件内容嵌入代码块中，
以允许用户下载或复制其内容到他们的剪贴板。
当示例文件的内容是通用的、可复用的，并且希望用户自己尝试使用示例文件时，
可以使用此短代码。

这个短代码有两个命名参数：`language` 和 `file`，
必选参数 `file` 用于指定要显示的文件的路径，
可选参数 `language` 用于指定文件的编程语言。
如果未提供 `language` 参数，短代码将尝试根据文件扩展名推测编程语言。

```none
{{</* codenew language="yaml" file="application/deployment-scale.yaml" */>}}
```

输出是：

{{< codenew language="yaml" file="application/deployment-scale.yaml" >}}

添加新的示例文件（例如 YAML 文件）时，在 `<LANG>/examples/`
子目录之一中创建该文件，其中 `<LANG>` 是页面的语言。
在你的页面的 markdown 文本中，使用 `codenew` 短代码：

```none
{{</* codenew file="<RELATIVE-PATH>/example-yaml>" */>}}
```

其中 `<RELATIVE-PATH>` 是要包含的示例文件的路径，相对于 `examples` 目录。
以下短代码引用位于 `/content/en/examples/configmap/configmaps.yaml` 的 YAML 文件。

```none
{{</* codenew file="configmap/configmaps.yaml" */>}}
```

## 第三方内容标记  {#third-party-content-marker}

运行 Kubernetes 需要第三方软件。例如：你通常需要将
[DNS 服务器](/zh-cn/docs/tasks/administer-cluster/dns-custom-nameservers/#introduction)
添加到集群中，以便名称解析工作。

当我们链接到第三方软件或以其他方式提及它时，我们会遵循[内容指南](/zh-cn/docs/contribute/style/content-guide/)
并标记这些第三方项目。

使用这些短代码会向使用它们的任何文档页面添加免责声明。

### 列表  {#third-party-content-list}

对于有关几个第三方项目的列表，请添加：
```
{{%/* thirdparty-content */%}}
```

在包含所有项目的段落标题正下方。

### 项目  {#third-party-content-item}

如果你有一个列表，其中大多数项目引用项目内软件（例如：Kubernetes 本身，以及单独的
[Descheduler](https://github.com/kubernetes-sigs/descheduler)
组件），那么可以使用不同的形式。

在项目之前，或在特定项目的段落下方添加此短代码：
```
{{%/* thirdparty-content single="true" */%}}
```

## 版本号信息 {#version-strings}

要在文档中生成版本号信息，可以从以下几种短代码中选择。每个短代码可以基于站点配置文件
`hugo.toml` 中的版本参数生成一个版本号取值。最常用的参数为 `latest` 和 `version`。

### `{{</* param "version" */>}}`

`{{</* param "version" */>}}` 短代码可以基于站点参数 `version` 生成 Kubernetes
文档的当前版本号取值。短代码 `param` 允许传入一个站点参数名称，在这里是 `version`。

{{< note >}}
在先前已经发布的文档中，`latest` 和 `version` 参数值并不完全等价。新版本文档发布后，参数
`latest` 会增加，而 `version` 则保持不变。例如，在上一版本的文档中使用 `version` 会得到
`v1.19`，而使用 `latest` 则会得到 `v1.20`。
{{< /note >}}

转换为：

{{< param "version" >}}

### `{{</* latest-version */>}}`

`{{</* latest-version */>}}` 返回站点参数 `latest` 的取值。每当新版本文档发布时，该参数均会被更新。
因此，参数 `latest` 与 `version` 并不总是相同。

转换为：

{{< latest-version >}}

### `{{</* latest-semver */>}}`

`{{</* latest-semver */>}}` 短代码可以生成站点参数 `latest` 不含前缀 `v` 的版本号取值。

转换为：

{{< latest-semver >}}

### `{{</* version-check */>}}`

`{{</* version-check */>}}` 会检查是否设置了页面参数 `min-kubernetes-server-version`
并将其与 `version` 进行比较。

转换为：

{{< version-check >}}

### `{{</* latest-release-notes */>}}`

`{{</* latest-release-notes */>}}` 短代码基于站点参数 `latest` 生成不含前缀 `v`
的版本号取值，并输出该版本更新日志的超链接地址。

转换为：

{{< latest-release-notes >}}

## {{% heading "whatsnext" %}}


* 了解 [Hugo](https://gohugo.io/)。
* 了解[撰写新的话题](/zh-cn/docs/contribute/style/write-new-topic/)。
* 了解[使用页面内容类型](/zh-cn/docs/contribute/style/page-content-types/)。
* 了解[发起 PR](/zh-cn/docs/contribute/new-content/open-a-pr/)。
* 了解[进阶贡献](/zh-cn/docs/contribute/advanced/)。
