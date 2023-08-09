---
title: 文档样式指南
linktitle: 样式指南
content_type: concept
weight: 40
---


本页讨论 Kubernetes 文档的样式指南。
这些仅仅是指南而不是规则。
你可以自行决定，且欢迎使用 PR 来为此文档提供修改意见。

关于为 Kubernetes 文档贡献新内容的更多信息，
可以参考[文档内容指南](/zh-cn/docs/contribute/style/content-guide/)。

样式指南的变更是 SIG Docs 团队集体决定。
如要提议更改或新增条目，请先将其添加到下一次 SIG Docs
例会的[议程表](https://bit.ly/sig-docs-agenda)上，并按时参加会议讨论。


{{< note >}}
Kubernetes 文档使用带调整的 [Goldmark Markdown 解释器](https://github.com/yuin/goldmark/)
和一些 [Hugo 短代码](/zh-cn/docs/contribute/style/hugo-shortcodes/)来支持词汇表项、Tab
页以及特性门控标注。
{{< /note >}}

## 语言 {#language}

Kubernetes 文档已经被翻译为多个语种
（参见 [本地化 README](https://github.com/kubernetes/website/blob/main/README.md#localization-readmemds)）。

[本地化 Kubernetes 文档](/zh-cn/docs/contribute/localization/)描述了如何为一种新的语言提供本地化文档。

英语文档使用美国英语的拼写和语法。

{{< comment >}}[如果你在翻译本页面，你可以忽略关于美国英语的这一条。]{{< /comment >}}

## 文档格式标准 {#documentation-formatting-standards}

### 对 API 对象使用大写驼峰式命名法  {#use-upper-camel-case-for-api-objects}

当你与指定的 API 对象进行交互时，
使用[大写驼峰式命名法](https://zh.wikipedia.org/wiki/%E9%A7%9D%E5%B3%B0%E5%BC%8F%E5%A4%A7%E5%B0%8F%E5%AF%AB)，
也被称为帕斯卡拼写法（PascalCase）。
你可以在 [API 参考](/zh-cn/docs/reference/kubernetes-api/)中看到不同的大小写形式，例如 "configMap"。
在编写通用文档时，最好使用大写驼峰形式，将之称作 "ConfigMap"。

通常在讨论 API 对象时，使用
[句子式大写](https://docs.microsoft.com/en-us/style-guide/text-formatting/using-type/use-sentence-style-capitalization)。

下面的例子关注的是大小写问题。关于如何格式化 API 对象名称的更多信息，
可参考相关的[代码风格](#code-style-inline-code)指南。

{{< table caption = "使用 Pascal 风格大小写来给出 API 对象的约定" >}}
可以 | 不可以
:--| :-----
该 HorizontalPodAutoscaler 负责... | 该 Horizontal pod autoscaler 负责...
每个 PodList 是一个 Pod 组成的列表。 | 每个 Pod List 是一个由 Pod 组成的列表。
该 Volume 对象包含一个 `hostPath` 字段。 | 此卷对象包含一个 hostPath 字段。
每个 ConfigMap 对象都是某个名字空间的一部分。| 每个 configMap 对象是某个名字空间的一部分。
要管理机密数据，可以考虑使用 Secret API。 | 要管理机密数据，可以考虑使用秘密 API。
{{< /table >}}

### 在占位符中使用尖括号

用尖括号表示占位符，让读者知道占位符表示的是什么。例如：

显示有关 Pod 的信息：

```shell
kubectl describe pod <Pod 名称> -n <名字空间>
```

如果名字空间被忽略，默认为 `default`，你可以省略 '-n' 参数。

### 用粗体字表现用户界面元素

{{< table caption = "以粗体表示用户界面元素" >}}
可以 | 不可以
:--| :-----
点击 **Fork**。 | 点击 "Fork"。
选择 **Other**。 | 选择 "Other"。
{{< /table >}}

### 定义或引入新术语时使用斜体

{{< table caption = "新术语约定" >}}
可以 | 不可以
:--| :-----
每个 _集群_  是一组节点 ... | 每个“集群”是一组节点 ...
这些组件构成了 _控制面_。 | 这些组件构成了 **控制面**。
{{< /table >}}

{{< note >}}
注意：这一条不适用于中文本地化，中文本地化过程中通常将英文斜体改为粗体。
{{< /note >}}

### 使用代码样式表现文件名、目录和路径

{{< table caption = "文件名、目录和路径约定" >}}
可以 | 不可以
:--| :-----
打开 `envars.yaml` 文件 | 打开 envars.yaml 文件
进入到 `/docs/tutorials` 目录 | 进入到 /docs/tutorials 目录
打开 `/_data/concepts.yaml` 文件 | 打开 /\_data/concepts.yaml 文件
{{< /table >}}

### 在引号内使用国际标准标点

{{< table caption = "标点符号约定" >}}
可以 | 不可以
:--| :-----
事件记录中都包含对应的“stage”。 | 事件记录中都包含对应的“stage。”
此副本称作一个“fork”。| 此副本称作一个“fork。”
{{< /table >}}

## 行间代码格式    {#inline-code-formatting}

### 为行间代码、命令与 API 对象使用代码样式  {#code-style-inline-code}

对于 HTML 文档中的行间代码，使用 `<code>` 标记。
在 Markdown 文档中，使用反引号（`` ` ``）。

{{< table caption = "行间代码、命令和 API 对象约定" >}}
可以 | 不可以
:--| :-----
`kubectl run` 命令会创建一个 `Pod` | "kubectl run" 命令会创建一个 Pod。
每个节点上的 kubelet 都会获得一个 `Lease` | 每个节点上的 kubelet 都会获得一个 lease…
一个 `PersistentVolume` 代表持久存储 | 一个 Persistent Volume 代表持久存储…
在声明式管理中，使用 `kubectl apply`。 | 在声明式管理中，使用 "kubectl apply"。
用三个反引号来（\`\`\`）标示代码示例 | 用其他语法来标示代码示例。
使用单个反引号来标示行间代码。例如：`var example = true`。 | 使用两个星号（`**`）或者一个下划线（`_`）来标示行间代码。例如：**var example = true**。
在多行代码块之前和之后使用三个反引号标示隔离的代码块。 | 使用多行代码块来创建示意图、流程图或者其他表示。
使用符合上下文的有意义的变量名。 | 使用诸如 'foo'、'bar' 和 'baz' 这类无意义且无语境的变量名。
删除代码中行尾空白。 | 在代码中包含行尾空白，因为屏幕抓取工具通常也会抓取空白字符。
{{< /table >}}

{{< note >}}
网站支持为代码示例使用语法加亮，不过指定语法加亮是可选的。
代码段的语法加亮要遵从[对比度指南](https://www.w3.org/WAI/WCAG21/quickref/?versions=2.0&showtechniques=141%2C143#contrast-minimum)
{{< /note >}}

### 为对象字段名和名字空间使用代码风格

{{< table caption = "对象字段名约定" >}}
可以 | 不可以
:--| :-----
在配置文件中设置 `replicas` 字段的值。 | 在配置文件中设置 "replicas" 字段的值。
`exec` 字段的值是一个 ExecAction 对象。 | "exec" 字段的值是一个 ExecAction 对象。
在 `kube-system` 名字空间中以 DaemonSet 形式运行此进程。 | 在 kube-system 名字空间中以 DaemonSet 形式运行此进程。
{{< /table >}}

### 用代码样式书写 Kubernetes 命令工具和组件名

{{< table caption = "Kubernetes 命令工具和组件名" >}}
可以 | 不可以
:--| :-----
`kubelet` 维持节点稳定性。 | kubelet 负责维护节点稳定性。
`kubectl` 处理 API 服务器的定位和身份认证。| kubectl 处理 API 服务器的定位和身份认证。
使用该证书运行进程 `kube-apiserver --client-ca-file=FILENAME`。| 使用证书运行进程 kube-apiserver --client-ca-file=FILENAME。|
{{< /table >}}

### 用工具或组件名称开始一句话

{{< table caption = "工具或组件名称使用约定" >}}
可以 | 不可以
:--| :-----
The `kubeadm` tool bootstraps and provisions machines in a cluster. | `kubeadm` tool bootstraps and provisions machines in a cluster.
The kube-scheduler is the default scheduler for Kubernetes. | kube-scheduler is the default scheduler for Kubernetes.
{{< /table >}}

### 尽量使用通用描述而不是组件名称

{{< table caption = "组件名称与通用描述" >}}
可以 | 不可以
:--| :-----
Kubernetes API 服务器提供 OpenAPI 规范。| apiserver 提供 OpenAPI 规范。
聚合 API 是下级 API 服务器。 | 聚合 API 是下级 APIServer。
{{< /table >}}

### 使用普通样式表达字符串和整数字段值

对于字符串或整数，使用正常样式，不要带引号。

{{< table caption = "字符串和整数字段值约定" >}}
可以 | 不可以
:--| :-----
将 `imagePullPolicy` 设置为 Always。 | 将 `imagePullPolicy` 设置为 "Always"。
将 `image` 设置为 nginx:1.16。 | 将 `image` 设置为 `nginx:1.16`。
将 `replicas` 字段值设置为 2。 | 将 `replicas` 字段值设置为 `2`。
{{< /table >}}

## 引用 Kubernetes API 资源   {#referring-to-kubernetes-api-resources}

本节讨论我们如何在文档中引用 API 资源。

### 有关 “资源” 的阐述

Kubernetes 使用 “resource” 一词来指代 API 资源，例如 `pod`、`deployment` 等。
我们还使用 “resource” 来谈论 CPU 和内存请求和限制。
所以始终将 API 资源称为 “API resources” 以避免与 CPU 和内存资源混淆。

### 何时使用 Kubernetes API 术语

不同 Kubernetes API 术语的说明如下：

- 资源类型：API URL 中使用的名称（如 `pods`、`namespaces`）
- 资源：资源类型的单个实例（如 `pod`、`secret`）
- 对象：作为 “意向记录” 的资源。对象是集群特定部分的期望状态，
  该状态由 Kubernetes 控制平面负责维护。

在文档中引用 API 资源时始终使用 “资源” 或 “对象”。
例如，使用 “一个 `Secret` 对象” 而不是 “一个 `Secret`”。

### API 资源名称

始终使用[大写驼峰式命名法](https://zh.wikipedia.org/wiki/%E9%A7%9D%E5%B3%B0%E5%BC%8F%E5%A4%A7%E5%B0%8F%E5%AF%AB)
（PascalCase）和代码格式来表达 API 资源名称。

对于 HTML 文档中的内联代码，请使用 `<code>` 标记。
在 Markdown 文档中，使用反引号 (`` ` ``)。

不要将 API 对象的名称切分成多个单词。
例如请使用 `PodTemplateList` 而非 `Pod Template List`。

有关 PascalCase 和代码格式的更多信息，
请查看[对 API 对象使用大写驼峰式命名法](/zh-cn/docs/contribute/style/style-guide/#use-upper-camel-case-for-api-objects)
和[针对内嵌代码、命令与 API 对象使用代码样式](/zh-cn/docs/contribute/style/style-guide/#code-style-inline-code)。

有关 Kubernetes API 术语的更多信息，
请查看 [Kubernetes API 术语](/zh-cn/docs/reference/using-api/api-concepts/#standard-api-terminology)的相关指南。

## 代码段格式   {#code-snippet-formatting}

### 不要包含命令行提示符   {#do-not-include-the-command-promot}

{{< table caption = "命令行提示符约定" >}}
可以 | 不可以
:--| :-----
kubectl get pods | $ kubectl get pods
{{< /table >}}

### 将命令和输出分开   {#separate-commands-from-output}

例如：

验证 Pod 已经在你所选的节点上运行：

```shell
kubectl get pods --output=wide
```

输出类似于：

```console
NAME     READY     STATUS    RESTARTS   AGE    IP           NODE
nginx    1/1       Running   0          13s    10.200.0.4   worker0
```

### 为 Kubernetes 示例给出版本   {#versioning-kubernetes-examples}

代码示例或者配置示例如果包含版本信息，应该与对应的文字描述一致。

如果所给的信息是特定于具体版本的，需要在
[任务模板](/zh-cn/docs/contribute/style/page-content-types/#task)
或[教程模板](/zh-cn/docs/contribute/style/page-content-types/#tutorial)
的 `prerequisites` 小节定义 Kubernetes 版本。
页面保存之后，`prerequisites` 小节会显示为 **开始之前**。

如果要为任务或教程页面指定 Kubernetes 版本，可以在文件的前言部分包含
`min-kubernetes-server-version` 信息。

如果示例 YAML 是一个独立文件，找到并审查包含该文件的主题页面。
确认使用该独立 YAML 文件的主题都定义了合适的版本信息。
如果独立的 YAML 文件没有在任何主题中引用，可以考虑删除该文件，
而不是继续更新它。

例如，如果你在编写一个教程，与 Kubernetes 1.8 版本相关。那么你的 Markdown
文件的文件头应该开始起来像这样：

```yaml
---
title: <教程标题>
min-kubernetes-server-version: v1.8
---
```

在代码和配置示例中，不要包含其他版本的注释信息。
尤其要小心不要在示例中包含不正确的注释信息，例如：

```yaml
apiVersion: v1 # 早期版本使用...
kind: Pod
...
```
## Kubernetes.io 术语列表   {#kubernetes-io-word-list}

以下特定于 Kubernetes 的术语和词汇在使用时要保持一致性。

{{< table caption = "Kubernetes.io 词汇表" >}}
术语 | 用法
:--- | :----
Kubernetes | Kubernetes 的首字母要保持大写。
Docker | Docker 的首字母要保持大写。
SIG Docs | SIG Docs 是正确拼写形式，不要用 SIG-DOCS 或其他变体。
On-premises | On-premises 或 On-prem 而不是 On-premise 或其他变体。
{{< /table >}}

## 短代码（Shortcodes） {#shortcodes}

Hugo [短代码（Shortcodes）](https://gohugo.io/content-management/shortcodes)
有助于创建比较漂亮的展示效果。我们的文档支持三个不同的这类短代码。
**注意** `{{</* note */>}}`、**小心** `{{</* caution */>}}` 和 **警告** `{{</* warning */>}}`。

1. 将要突出显示的文字用短代码的开始和结束形式包围。
2. 使用下面的语法来应用某种样式：

   ```none
   {{</* note */>}}
   不需要前缀；短代码会自动添加前缀（注意：、小心：等）
   {{</* /note */>}}
   ```

   输出的样子是：

   {{< note >}}
   你所选择的标记决定了文字的前缀。
   {{< /note >}}

### 注释（Note） {#note}

使用短代码 `{{</* note */>}}` 来突出显示某种提示或者有助于读者的信息。

例如:

```
{{</* note */>}}
在这类短代码中仍然 _可以_ 使用 Markdown 语法。
{{</* /note */>}}
```

输出为：

{{< note >}}
在这类短代码中仍然 _可以_ 使用 Markdown 语法。
{{< /note >}}

你可以在列表中使用 `{{</* note */>}}`：

```
1. 在列表中使用 note 短代码

1. 带嵌套 note 的第二个条目

   {{</* note */>}}
   警告、小心和注意短代码可以嵌套在列表中，但是要缩进四个空格。
   参见[常见短代码问题](#common-shortcode-issues)。
   {{</* /note */>}}

1. 列表中第三个条目

1. 列表中第四个条目
```

其输出为：

1. 在列表中使用 note 短代码

1. 带嵌套 note 的第二个条目

    {{< note >}}
    警告、小心和注释短代码可以嵌套在列表中，但是要缩进四个空格。
    参见[常见短代码问题](#common-shortcode-issues)。
    {{< /note >}}

1. 列表中第三个条目

1. 列表中第四个条目

### 小心（Caution）  {#caution}

使用 `{{</* caution */>}}` 短代码来引起读者对某段信息的重视，以避免遇到问题。

例如：

```
{{</* caution */>}}
此短代码样式仅对标记之上的一行起作用。
{{</* /caution */>}}
```

其输出为：

{{< caution >}}
此短代码样式仅对标记之上的一行起作用。
{{< /caution >}}

### 警告（Warning）  {#warning}

使用 `{{</* warning */>}}` 来表明危险或者必须要重视的一则信息。

例如：

```
{{</* warning */>}}
注意事项
{{</* /warning */>}}
```

其输出为：

{{< warning >}}
注意事项
{{< /warning >}}

## 常见的短代码问题  {#common-shortcode-issues}

### 编号列表   {#ordered-lists}

短代码会打乱编号列表的编号，除非你在信息和标志之前都缩进四个空格。

例如：

```
1. 预热到 350˚F
1. 准备好面糊，倒入烘烤盘
    {{</* note */>}}给盘子抹上油可以达到最佳效果。{{</* /note */>}}
1. 烘烤 20 到 25 分钟，或者直到满意为止。
```

其输出结果为：

1. 预热到 350˚F
1. 准备好面糊，倒入烘烤盘
   {{< note >}}给盘子抹上油可以达到最佳效果。{{< /note >}}
1. 烘烤 20 到 25 分钟，或者直到满意为止。

### Include 语句   {#include-statements}

如果短代码出现在 include 语境中，会导致网站无法构建。
你必须将他们插入到上级文档中，分别将开始标记和结束标记插入到 include 语句之前和之后。
例如：

```
{{</* note */>}}
{{</* include "task-tutorial-prereqs.md" */>}}
{{</* /note */>}}
```

## Markdown 元素 {#markdown-elements}

### 换行  {#line-breaks}

使用单一换行符来隔离块级内容，例如标题、列表、图片、代码块以及其他元素。
这里的例外是二级标题，必须有两个换行符。
二级标题紧随一级标题（或标题），中间没有段落或文字。

两行的留白有助于在代码编辑器中查看整个内容的结构组织。

### 大标题和小标题  {#headings}

访问文档的读者可能会使用屏幕抓取程序或者其他辅助技术。
[屏幕抓取器](https://en.wikipedia.org/wiki/Screen_reader)是一种线性输出设备,
它们每次输出页面上的一个条目。
如果页面上内容过多，你可以使用标题来为页面组织结构。
页面的良好结构对所有读者都有帮助，使得他们更容易浏览或者过滤感兴趣的内容。

{{< table caption = "标题约定" >}}
可以 | 不可以
:--| :-----
更新页面或博客在前言部分中的标题。 | 使用一级标题。因为 Hugo 会自动将页面前言部分的标题转化为一级标题。
使用编号的标题以便内容组织有一个更有意义的结构。| 使用四级到六级标题，除非非常有必要这样。如果你要编写的内容有非常多细节，可以尝试拆分成多个不同页面。
在非博客内容页面中使用井号（`#`）| 使用下划线 `---` 或 `===` 来标记一级标题。
页面正文中的小标题采用正常语句的大小写。例如：**Extend kubectl with plugins** | 页面正文中的小标题采用首字母大写的大标题式样。例如：**Extend Kubectl With Plugins**
头部的页面标题采用大标题的式样。例如：`title: Kubernetes API Server Bypass Risks` | 头部的页面标题采用正常语句的大小写。例如不要使用 `title: Kubernetes API server bypass risks`
{{< /table >}}

### 段落    {#paragraphs}

{{< table caption = "段落约定" >}}
可以 | 不可以
:--| :-----
尝试不要让段落超出 6 句话。 | 用空格来缩进第一段。例如，段落前面的三个空格⋅⋅⋅会将段落缩进。
使用三个连字符（`---`）来创建水平线。使用水平线来分隔段落内容。例如，在故事中切换场景或者在上下文中切换主题。 | 使用水平线来装饰页面。
{{< /table >}}

### 链接   {#links}

{{< table caption = "链接约定" >}}
可以 | 不可以
:--| :-----
插入超级链接时给出它们所链接到的目标内容的上下文。例如：你的机器上某些端口处于开放状态。参见<a href="#check-required-ports">检查所需端口</a>了解更详细信息。| 使用“点击这里”等模糊的词语。例如：你的机器上某些端口处于打开状态。参见<a href="#check-required-ports">这里</a>了解详细信息。
编写 Markdown 风格的链接：`[链接文本](URL)`。例如：`[Hugo 短代码](/zh-cn/docs/contribute/style/hugo-shortcodes/#table-captions)`，输出是 [Hugo 短代码](/zh-cn/docs/contribute/style/hugo-shortcodes/#table-captions)。 | 编写 HTML 风格的超级链接：`<a href="/media/examples/link-element-example.css" target="_blank">访问我们的教程！</a>`，或者创建会打开新 Tab 页签或新窗口的链接。例如：`[网站示例](https://example.com){target="_blank"}`。
{{< /table >}}

### 列表  {#lists}

将一组相互关联的内容组织到一个列表中，以便表达这些条目彼此之间有先后顺序或者某种相互关联关系。
当屏幕抓取器遇到列表时，无论该列表是否有序，它会告知用户存在一组枚举的条目。
用户可以使用箭头键来上下移动，浏览列表中条目。
网站导航链接也可以标记成列表条目，因为说到底他们也是一组相互关联的链接而已。

- 如果列表中一个或者多个条目是完整的句子，则在每个条目末尾添加句号。
  出于一致性考虑，一般要么所有条目要么没有条目是完整句子。

  {{< note >}}
  编号列表如果是不完整的介绍性句子的一部分，可以全部用小写字母，并按照
  每个条目都是句子的一部分来看待和处理。
  {{< /note >}}

- 在编号列表中，使用数字 1（`1.`）。

- 对非排序列表，使用加号（`+`）、星号（`*`）、或者减号（`-`）。

- 在每个列表之后留一个空行。

- 对于嵌套的列表，相对缩进四个空格（例如，⋅⋅⋅⋅）。

- 列表条目可能包含多个段落。每个后续段落都要缩进或者四个空格或者一个制表符。

### 表格  {#tables}

数据表格的语义用途是呈现表格化的数据。
用户可以快速浏览表格，但屏幕抓取器需要逐行地处理数据。
表格标题可以用来给数据表提供一个描述性的标题。
辅助技术使用 HTML 表格标题元素来在页面结构中辨识表格内容。

- 使用 [Hugo 短代码](/zh-cn/docs/contribute/style/hugo-shortcodes/#table-captions)为表格添加标题。

## 内容最佳实践   {#content-best-practices}

本节包含一些建议的最佳实践，用来开发清晰、明确一致的文档内容。

### 使用现在时态

{{< table caption = "使用现在时态" >}}
可以 | 不可以
:--| :-----
此命令启动代理。| 此命令将启动一个代理。
{{< /table >}}

例外：如果需要使用过去时或将来时来表达正确含义时，是可以使用的。

### 使用主动语态

{{< table caption = "使用主动语态" >}}
可以 | 不可以
:--| :-----
你可以使用浏览器来浏览 API。| API 可以被使用浏览器来浏览。
YAML 文件给出副本个数。 | 副本个数是在 YAML 文件中给出的。
{{< /table >}}  

例外：如果主动语态会导致句子很难构造时，可以使用被动语态。

### 使用简单直接的语言

使用简单直接的语言。避免不必要的短语，例如说“请”。

{{< table caption = "使用简单直接语言" >}}
可以 | 不可以
:--| :-----
要创建 ReplicaSet，... | 如果你想要创建 ReplicaSet，...
参看配置文件。 | 请自行查看配置文件。
查看 Pod。| 使用下面的命令，我们将会看到 Pod。
{{< /table >}}  

### 将读者称为“你”

{{< table caption = "将读者称为“你”" >}}
可以 | 不可以
:--| :-----
你可以通过 ... 创建一个 Deployment。 | 通过...我们将创建一个 Deployment。
在前面的输出中，你可以看到... | 在前面的输出中，我们可以看到...
{{< /table >}}  

### 避免拉丁短语

尽可能使用英语而不是拉丁语缩写。

{{< table caption = "避免拉丁语短语" >}}
可以 | 不可以
:--| :-----
例如，... | e.g., ...
也就是说，...| i.e., ...
{{< /table >}}

例外：使用 etc. 表示等等。

## 应避免的模式   {#patterns-to-avoid}

### 避免使用“我们”

在句子中使用“我们”会让人感到困惑，因为读者可能不知道这里的
“我们”指的是谁。

{{< table caption = "要避免的模式" >}}
可以 | 不可以
:--| :-----
版本 1.4 包含了 ... | 在 1.4 版本中，我们添加了 ...
Kubernetes 为 ... 提供了一项新功能。 | 我们提供了一项新功能...
本页面教你如何使用 Pod。| 在本页中，我们将会学到如何使用 Pod。
{{< /table >}}

### 避免使用俚语或行话

对某些读者而言，英语是其外语。
避免使用一些俚语或行话有助于他们更方便的理解内容。

{{< table caption = "避免使用俚语或行话" >}}
可以 | 不可以
:--| :-----
Internally, ... | Under the hood, ...
Create a new cluster. | Turn up a new cluster.
{{< /table >}}

### 避免关于将来的陈述

要避免对将来作出承诺或暗示。如果你需要讨论的是 Alpha 功能特性，
可以将相关文字放在一个单独的标题下，标示为 Alpha 版本信息。

此规则的一个例外是对未来版本中计划移除的已废弃功能选项的文档。
此类文档的例子之一是[已弃用 API 迁移指南](/zh-cn/docs/reference/using-api/deprecation-guide/)。

### 避免使用很快就会过时的表达

避免使用一些很快就会过时的陈述，例如“目前”、“新的”。
今天而言是新的功能，过了几个月之后就不再是新的了。

{{< table caption = "避免使用很快过时的表达" >}}
可以 | 不可以
:--| :-----
在版本 1.4 中，... | 在当前版本中，...
联邦功能特性提供 ... | 新的联邦功能特性提供 ...
{{< /table >}}  

### 避免使用隐含用户对某技术有一定理解的词汇

避免使用“只是”、“仅仅”、“简单”、“很容易地”、“很简单”这类词汇。
这些词并没有提升文档的价值。

{{< table caption = "避免无意义词汇的注意事项" >}}
可以 | 不可以
:--| :-----
在 ... 中包含一个命令 | 只需要在... 中包含一个命令
运行容器 ... | 只需运行该容器...
你可以移除... | 你可以很容易地移除...
这些步骤... | 这些简单的步骤...
{{< /table >}}

## {{% heading "whatsnext" %}}

* 了解[编写新主题](/zh-cn/docs/contribute/style/write-new-topic/)。
* 了解[页面内容类型](/zh-cn/docs/contribute/style/page-content-types/)。
* 了解[定制 Hugo 短代码](/zh-cn/docs/contribute/style/hugo-shortcodes/)。
* 了解[发起 PR](/zh-cn/docs/contribute/new-content/open-a-pr/)。
