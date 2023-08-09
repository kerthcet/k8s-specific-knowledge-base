---
title: 字段选择器
content_type: concept
weight: 70
---

“字段选择器（Field selectors）”允许你根据一个或多个资源字段的值筛选
Kubernetes {{< glossary_tooltip text="对象" term_id="object" >}}。
下面是一些使用字段选择器查询的例子：

* `metadata.name=my-service`
* `metadata.namespace!=default`
* `status.phase=Pending`

下面这个 `kubectl` 命令将筛选出
[`status.phase`](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase)
字段值为 `Running` 的所有 Pod：

```shell
kubectl get pods --field-selector status.phase=Running
```

{{< note >}}
字段选择器本质上是资源“过滤器（Filters）”。默认情况下，字段选择器/过滤器是未被应用的，
这意味着指定类型的所有资源都会被筛选出来。
这使得 `kubectl get pods` 和 `kubectl get pods --field-selector ""`
这两个 `kubectl` 查询是等价的。

{{< /note >}}

## 支持的字段  {#supported-fields}

不同的 Kubernetes 资源类型支持不同的字段选择器。
所有资源类型都支持 `metadata.name` 和 `metadata.namespace` 字段。
使用不被支持的字段选择器会产生错误。例如：

```shell
kubectl get ingress --field-selector foo.bar=baz
```

```
Error from server (BadRequest): Unable to find "ingresses" that match label selector "", field selector "foo.bar=baz": "foo.bar" is not a known field selector: only "metadata.name", "metadata.namespace"
```

## 支持的操作符   {#supported-operators}

你可在字段选择器中使用 `=`、`==` 和 `!=` （`=` 和 `==` 的意义是相同的）操作符。
例如，下面这个 `kubectl` 命令将筛选所有不属于 `default` 命名空间的 Kubernetes 服务：

```shell
kubectl get services  --all-namespaces --field-selector metadata.namespace!=default
```

## 链式选择器   {#chained-selectors}

同[标签](/zh-cn/docs/concepts/overview/working-with-objects/labels/)和其他选择器一样，
字段选择器可以通过使用逗号分隔的列表组成一个选择链。
下面这个 `kubectl` 命令将筛选 `status.phase` 字段不等于 `Running` 同时
`spec.restartPolicy` 字段等于 `Always` 的所有 Pod：

```shell
kubectl get pods --field-selector=status.phase!=Running,spec.restartPolicy=Always
```

## 多种资源类型   {#multiple-resource-types}

你能够跨多种资源类型来使用字段选择器。
下面这个 `kubectl` 命令将筛选出所有不在 `default` 命名空间中的 StatefulSet 和 Service：

```shell
kubectl get statefulsets,services --all-namespaces --field-selector metadata.namespace!=default
```
