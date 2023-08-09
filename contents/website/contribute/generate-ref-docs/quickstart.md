---
title: 参考文档快速入门
linkTitle: Quickstart
content_type: task
weight: 10
hide_summary: true
---


本页讨论如何使用 `update-imported-docs.py` 脚本来生成 Kubernetes 参考文档。
此脚本将构建的配置过程自动化，并为某个发行版本生成参考文档。

## {{% heading "prerequisites" %}}

{{< include "prerequisites-ref-docs.md" >}}

## 获取文档仓库 {#getting-the-docs-repository}

确保你的 `website` 派生仓库与 GitHub 上的 `kubernetes/website` 远程仓库（`main` 分支）保持同步，
并克隆你的派生仓库。

```shell
mkdir github.com
cd github.com
git clone git@github.com:<your_github_username>/website.git
```

确定你的克隆副本的根目录。例如，如果你按照前面的步骤获取了仓库，你的根目录
会是 `github.com/website`。接下来的步骤中，`<web-base>` 用来指代你的根目录。

{{< note>}}
如果你希望更改构建工具和 API 参考资料，
可以阅读[上游贡献指南](/zh-cn/docs/contribute/generate-ref-docs/contribute-upstream)。
{{< /note >}}

## update-imported-docs 的概述   {#overview-of-update-imported-docs}

脚本 `update-imported-docs.py` 位于 `<web-base>/update-imported-docs/` 目录下，
能够生成以下参考文档：

* Kubernetes 组件和工具的参考页面
* `kubectl` 命令参考文档
* Kubernetes API 参考文档

脚本 `update-imported-docs.py` 基于 Kubernetes 源代码生成参考文档。
过程中会在你的机器的 `/tmp` 目录下创建临时目录，克隆所需要的仓库
`kubernetes/kubernetes` 和 `kubernetes-sigs/reference-docs` 到此临时目录。
脚本会将 `GOPATH` 环境变量设置为指向此临时目录。
此外，脚本会设置三个环境变量：

* `K8S_RELEASE`
* `K8S_ROOT`
* `K8S_WEBROOT`

脚本需要两个参数才能成功运行：

* 一个 YAML 配置文件（`reference.yml`）
* 一个发行版本字符串，例如：`1.17`

配置文件中包含 `generate-command` 字段，其中定义了一系列来自于
`kubernetes-sigs/reference-docs/Makefile` 的构建指令。
变量 `K8S_RELEASE` 用来确定所针对的发行版本。

脚本 `update-imported-docs.py` 执行以下步骤：

1. 克隆配置文件中所指定的相关仓库。就生成参考文档这一目的而言，要克隆的仓库默认为
   `kubernetes-sigs/reference-docs`。
1. 在所克隆的仓库下运行命令，准备文档生成器，之后生成 HTML 和 Markdown 文件。
1. 将所生成的 HTML 和 Markdown 文件复制到 `<web-base>` 本地克隆副本中，
   放在配置文件中所指定的目录下。
1. 更新 `kubectl.md` 文件中对 `kubectl` 命令文档的链接，使之指向 `kubectl`
   命令参考中对应的节区。

当所生成的文件已经被放到 `<web-base>` 目录下，你就可以将其提交到你的派生副本中，
并基于所作提交发起[拉取请求（PR）](/docs/contribute/start/)到 kubernetes/website 仓库。

## 配置文件格式 {#configuration-file-format}

每个配置文件可以包含多个被导入的仓库。当必要时，你可以通过手工编辑此文件进行定制。
你也可以通过创建新的配置文件来导入其他文档集合。
下面是 YAML 配置文件的一个例子：

```yaml
repos:
- name: community
  remote: https://github.com/kubernetes/community.git
  branch: master
  files:
  - src: contributors/devel/README.md
    dst: docs/imported/community/devel.md
  - src: contributors/guide/README.md
    dst: docs/imported/community/guide.md
```

通过工具导入的单页面的 Markdown
文档必须遵从[文档样式指南](/zh-cn/docs/contribute/style/style-guide/)。


## 定制 reference.yml   {#customizing-reference-yml}

打开 `<web-base>/update-imported-docs/reference.yml` 文件进行编辑。
在不了解参考文档构造命令的情况下，不要更改 `generate-command` 字段的内容。
你一般不需要更新 `reference.yml` 文件。不过也有时候上游的源代码发生变化，
导致需要对配置文件进行更改（例如：Golang 版本依赖或者第三方库发生变化）。
如果你遇到类似问题，请在 [Kubernetes Slack 的 #sig-docs 频道](https://kubernetes.slack.com)
联系 SIG-Docs 团队。

{{< note >}}
注意，`generate-command` 是一个可选项，用来运行指定命令或者短脚本以在仓库内生成文档。
{{< /note >}}

在 `reference.yml` 文件中，`files` 属性包含了一组 `src` 和 `dst` 字段。
`src` 字段给出在所克隆的 `kubernetes-sigs/reference-docs` 构造目录中生成的
Markdown 文件的位置，而 `dst` 字段则给出了对应文件要复制到的、所克隆的
`kubernetes/website` 仓库中的位置。例如：

```yaml
repos:
- name: reference-docs
  remote: https://github.com/kubernetes-sigs/reference-docs.git
  files:
  - src: gen-compdocs/build/kube-apiserver.md
    dst: content/en/docs/reference/command-line-tools-reference/kube-apiserver.md
  ...
```

注意，如果从同一源目录中有很多文件要复制到目标目录，你可以在为 `src`
所设置的值中使用通配符。这时，为 `dst` 所设置的值必须是目录名称。例如：

```yaml
  files:
  - src: gen-compdocs/build/kubeadm*.md
    dst: content/en/docs/reference/setup-tools/kubeadm/generated/
```

## 运行 update-imported-docs 工具   {#running-the-update-imported-docs-tool}

你可以用如下方式运行 `update-imported-docs.py` 工具：

```shell
cd <web-base>/update-imported-docs
./update-imported-docs.py <configuration-file.yml> <release-version>
```

例如：

```shell
./update-imported-docs.py reference.yml 1.17
```

## 修复链接   {#fixing-links}

配置文件 `release.yml` 中包含用来修复相对链接的指令。
若要修复导入文件中的相对链接，将 `gen-absolute-links` 属性设置为 `true`。你可以在
[`release.yml`](https://github.com/kubernetes/website/blob/main/update-imported-docs/release.yml)
文件中找到示例。

## 添加并提交 kubernetes/website 中的变更   {#adding-and-committing-changes-in-k8s-website}

枚举新生成并复制到 `<web-base>` 的文件：

```shell
cd <web-base>
git status
```

输出显示新生成和已修改的文件。取决于上游源代码的修改多少，
所生成的输出也会不同。

### 生成的 Kubernetes 组件文档

```
content/en/docs/reference/command-line-tools-reference/cloud-controller-manager.md
content/en/docs/reference/command-line-tools-reference/kube-apiserver.md
content/en/docs/reference/command-line-tools-reference/kube-controller-manager.md
content/en/docs/reference/command-line-tools-reference/kube-proxy.md
content/en/docs/reference/command-line-tools-reference/kube-scheduler.md
content/en/docs/reference/setup-tools/kubeadm/generated/kubeadm.md
content/en/docs/reference/kubectl/kubectl.md
```

### 生成的 kubectl 命令参考文件

```
static/docs/reference/generated/kubectl/kubectl-commands.html
static/docs/reference/generated/kubectl/navData.js
static/docs/reference/generated/kubectl/scroll.js
static/docs/reference/generated/kubectl/stylesheet.css
static/docs/reference/generated/kubectl/tabvisibility.js
static/docs/reference/generated/kubectl/node_modules/bootstrap/dist/css/bootstrap.min.css
static/docs/reference/generated/kubectl/node_modules/highlight.js/styles/default.css
static/docs/reference/generated/kubectl/node_modules/jquery.scrollto/jquery.scrollTo.min.js
static/docs/reference/generated/kubectl/node_modules/jquery/dist/jquery.min.js
static/docs/reference/generated/kubectl/css/font-awesome.min.css
```

### 生成的 Kubernetes API 参考目录与文件

```
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/index.html
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/js/navData.js
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/js/scroll.js
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/js/query.scrollTo.min.js
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/css/font-awesome.min.css
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/css/bootstrap.min.css
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/css/stylesheet.css
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/fonts/FontAwesome.otf
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/fonts/fontawesome-webfont.eot
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/fonts/fontawesome-webfont.svg
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/fonts/fontawesome-webfont.ttf
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/fonts/fontawesome-webfont.woff
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/fonts/fontawesome-webfont.woff2
```

运行 `git add` 和 `git commit` 提交文件。

## 创建拉取请求 {#creating-a-pull-request}

接下来创建一个对 `kubernetes/website` 仓库的拉取请求（PR）。
监视所创建的 PR，并根据需要对评阅意见给出反馈。
继续监视该 PR 直到其被合并为止。

当你的 PR 被合并几分钟之后，你所做的对参考文档的变更就会出现
[发布的文档](/zh-cn/docs/home/)上。

## {{% heading "whatsnext" %}}

要手动设置所需的构造仓库，执行构建目标，以生成各个参考文档，可参考下面的指南：

* [为 Kubernetes 组件和工具生成参考文档](/zh-cn/docs/contribute/generate-ref-docs/kubernetes-components/)
* [为 kubectl 命令生成参考文档](/zh-cn/docs/contribute/generate-ref-docs/kubectl/)
* [为 Kubernetes API 生成参考文档](/zh-cn/docs/contribute/generate-ref-docs/kubernetes-api/)

