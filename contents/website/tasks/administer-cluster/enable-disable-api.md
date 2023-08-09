---
title: 启用/禁用 Kubernetes API
content_type: task
weight: 200
---

本页展示怎么用集群的
{{< glossary_tooltip text="控制平面" term_id="control-plane" >}}.
启用/禁用 API 版本。



通过 API 服务器的命令行参数 `--runtime-config=api/<version>` ，
可以开启/关闭某个指定的 API 版本。
此参数的值是一个逗号分隔的 API 版本列表。
此列表中，后面的值可以覆盖前面的值。

命令行参数 `runtime-config` 支持两个特殊的值（keys）：

- `api/all`：指所有已知的 API
- `api/legacy`：指过时的 API。过时的 API 就是明确地
  [弃用](/zh-cn/docs/reference/using-api/deprecation-policy/)
  的 API。

例如：为了停用除去 v1 版本之外的全部其他 API 版本，
就用参数 `--runtime-config=api/all=false,api/v1=true` 启动 `kube-apiserver`。

## {{% heading "whatsnext" %}}

阅读[完整的文档](/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver/),
以了解 `kube-apiserver` 组件。