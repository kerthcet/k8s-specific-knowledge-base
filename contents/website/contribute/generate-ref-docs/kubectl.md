---
title: 为 kubectl 命令集生成参考文档
content_type: task
weight: 90
---




本页面描述了如何生成 `kubectl` 命令参考。


{{< note >}}
本主题描述了如何为 [kubectl 命令](/docs/reference/generated/kubectl/kubectl-commands)
生成参考文档，如 [kubectl apply](/docs/reference/generated/kubectl/kubectl-commands#apply) 和
[kubectl taint](/docs/reference/generated/kubectl/kubectl-commands#taint)。
本主题没有讨论如何生成 [kubectl](/docs/reference/generated/kubectl/kubectl-commands/) 组件选项的参考页面。
相关说明请参见[为 Kubernetes 组件和工具生成参考页面](/zh-cn/docs/contribute/generate-ref-docs/kubernetes-components/)。
{{< /note >}}

## {{% heading "prerequisites" %}}

{{< include "prerequisites-ref-docs.md" >}}


## 配置本地仓库

创建本地工作区并设置你的 `GOPATH`。

```shell
mkdir -p $HOME/<workspace>
export GOPATH=$HOME/<workspace>
```

获取以下仓库的本地克隆：

```shell
go get -u github.com/spf13/pflag
go get -u github.com/spf13/cobra
go get -u gopkg.in/yaml.v2
go get -u kubernetes-incubator/reference-docs
```

如果你还没有获取过 `kubernetes/website` 仓库，现在获取之：

```shell
git clone https://github.com/<your-username>/website $GOPATH/src/github.com/<your-username>/website
```

克隆 kubernetes/kubernetes 仓库作为 k8s.io/kubernetes：

```shell
git clone https://github.com/kubernetes/kubernetes $GOPATH/src/k8s.io/kubernetes
```

从 `$GOPATH/src/k8s.io/kubernetes/vendor/github.com` 中移除 spf13 软件包。

```shell
rm -rf $GOPATH/src/k8s.io/kubernetes/vendor/github.com/spf13
```

kubernetes/kubernetes 仓库提供对 kubectl 和 kustomize 源代码的访问。

* 确定 [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) 仓库的本地主目录。
  例如，如果按照前面的步骤来获取该仓库，则主目录是 `$GOPATH/src/k8s.io/kubernetes.`。
  下文将该目录称为 `<k8s-base>`。

* 确定 [kubernetes/website](https://github.com/kubernetes/website) 仓库的本地主目录。
  例如，如果按照前面的步骤来获取该仓库，则主目录是 `$GOPATH/src/github.com/<your-username>/website`。
  下文将该目录称为 `<web-base>`。

* 确定 [kubernetes-sigs/reference-docs](https://github.com/kubernetes-sigs/reference-docs)
  仓库的本地主目录。例如，如果按照前面的步骤来获取该仓库，则主目录是
  `$GOPATH/src/github.com/kubernetes-sigs/reference-docs`。
  下文将该目录称为 `<rdocs-base>`。

在本地的 k8s.io/kubernetes 仓库中，检出感兴趣的分支并确保它是最新的。例如，
如果你想要生成 Kubernetes {{< skew prevMinorVersion >}}.0 的文档，可以使用以下命令：

```shell
cd <k8s-base>
git checkout v{{< skew prevMinorVersion >}}.0
git pull https://github.com/kubernetes/kubernetes {{< skew prevMinorVersion >}}.0
```

如果不需要编辑 `kubectl`
源码，请按照说明[配置构建变量](#setting-build-variables)。

## 编辑 kubectl 源码

kubectl 命令的参考文档是基于 kubectl 源码自动生成的。如果想要修改参考文档，可以从修改
kubectl 源码中的一个或多个注释开始。在本地 kubernetes/kubernetes 仓库中进行修改，然后向
[github.com/kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) 的 master
分支提交 PR。


[PR 56673](https://github.com/kubernetes/kubernetes/pull/56673/files) 是一个对 kubectl
源码中的笔误进行修复的 PR 示例。

跟踪你的 PR，并回应评审人的评论。继续跟踪你的 PR，直到它合入到 kubernetes/kubernetes 仓库的目标分支中。

## 以 cherry-pick 方式将你的修改合入已发布分支

你的修改已合入 master 分支中，该分支用于开发下一个 Kubernetes 版本。
如果你希望修改部分出现在已发布的 Kubernetes 版本文档中，则需要提议将它们以
cherry-pick 方式合入已发布分支。


例如，假设 master 分支正用于开发 Kubernetes {{< skew currentVersion >}} 版本，
而你希望将修改合入到 release-{{< skew prevMinorVersion >}} 版本分支。
相关的操作指南，请参见
[提议一个 cherry-pick](https://git.k8s.io/community/contributors/devel/sig-release/cherry-picks.md)。

跟踪你的 cherry-pick PR，直到它合入到已发布分支中。


{{< note >}}
提议一个 cherry-pick 需要你有在 PR 中设置标签和里程碑的权限。
如果你没有，你需要与有权限为你设置标签和里程碑的人合作完成。
{{< /note >}}

## 设置构建变量 {#setting-build-variables}

进入 `<rdocs-base>` 目录, 打开 `Makefile` 进行编辑：

* 设置 `K8S_ROOT` 为 `<k8s-base>`。
* 设置 `K8S_WEBROOT` 为 `<web-base>`。
* 设置 `K8S_RELEASE` 为要构建文档的版本。
  例如，如果你想为 Kubernetes {{< skew prevMinorVersion >}} 构建文档，
  请将 `K8S_RELEASE` 设置为 {{< skew prevMinorVersion >}}。

例如：

```
export K8S_WEBROOT=$(GOPATH)/src/github.com/<your-username>/website
export K8S_ROOT=$(GOPATH)/src/k8s.io/kubernetes
export K8S_RELEASE={{< skew prevMinorVersion >}}
```

## 创建版本目录

构建目标 `createversiondirs` 会生成一个版本目录并将 kubectl 参考配置文件复制到该目录中。
版本目录的名字模式为 `v<major>_<minor>`。

在 `<rdocs-base>` 目录下，执行下面的命令：

```shell
cd <rdocs-base>
make createversiondirs
```

## 从 kubernetes/kubernetes 检出一个分支

在本地 `<k8s-base>` 仓库中，检出你想要生成文档的、包含 Kubernetes 版本的分支。
例如，如果希望为 Kubernetes {{< skew prevMinorVersion >}}.0 版本生成文档，
请检出 `v{{< skew prevMinorVersion >}}` 标记。
确保本地分支是最新的。

```shell
cd <k8s-base>
git checkout v{{< skew prevMinorVersion >}}.0
git pull https://github.com/kubernetes/kubernetes v{{< skew prevMinorVersion >}}.0
```

## 运行文档生成代码

在本地的 `<rdocs-base>` 目录下，运行 `copycli` 构建目标。此命令以 `root` 账号运行：

```shell
cd <rdocs-base>
make copycli
```

`copycli` 命令将清理暂存目录，生成 kubectl 命令文件，并将整理后的 kubectl 参考 HTML 页面和
文件复制到 `<web-base>`。

## 找到生成的文件

验证是否已生成以下两个文件：

```shell
[ -e "<rdocs-base>/gen-kubectldocs/generators/build/index.html" ] && echo "index.html built" || echo "no index.html"
[ -e "<rdocs-base>/gen-kubectldocs/generators/build/navData.js" ] && echo "navData.js built" || echo "no navData.js"
```

## 找到复制的文件

确认所有生成的文件都已复制到你的 `<web-base>`：

```shell
cd <web-base>
git status
```

输出应包括修改后的文件：

```
static/docs/reference/generated/kubectl/kubectl-commands.html
static/docs/reference/generated/kubectl/navData.js
```


此外，输出可能还包含：

```
static/docs/reference/generated/kubectl/scroll.js
static/docs/reference/generated/kubectl/stylesheet.css
static/docs/reference/generated/kubectl/tabvisibility.js
static/docs/reference/generated/kubectl/node_modules/bootstrap/dist/css/bootstrap.min.css
static/docs/reference/generated/kubectl/node_modules/highlight.js/styles/default.css
static/docs/reference/generated/kubectl/node_modules/jquery.scrollto/jquery.scrollTo.min.js
static/docs/reference/generated/kubectl/node_modules/jquery/dist/jquery.min.js
static/docs/reference/generated/kubectl/node_modules/font-awesome/css/font-awesome.min.css
```

## 在本地测试文档

在本地 `<web-base>` 中构建 Kubernetes 文档。

```shell
cd <web-base>
git submodule update --init --recursive --depth 1 # if not already done
make container-serve
```

查看[本地预览](https://localhost:1313/docs/reference/generated/kubectl/kubectl-commands/)。

## 在 kubernetes/website 中添加和提交更改

运行 `git add` 和 `git commit` 提交修改文件。

## 创建 PR

对 `kubernetes/website` 仓库创建 PR。跟踪你的 PR，并根据需要回应评审人的评论。
继续跟踪你的 PR，直到它被合入。

在 PR 合入的几分钟后，你更新的参考主题将出现在[已发布文档](/zh-cn/docs/home/)中。

## {{% heading "whatsnext" %}}

* [生成参考文档快速入门](/zh-cn/docs/contribute/generate-ref-docs/quickstart/)
* [为 Kubernetes 组件和工具生成参考文档](/zh-cn/docs/contribute/generate-ref-docs/kubernetes-components/)
* [为 Kubernetes API 生成参考文档](/zh-cn/docs/contribute/generate-ref-docs/kubernetes-api/)

