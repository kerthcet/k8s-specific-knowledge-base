---
api_metadata:
  apiVersion: ""
  import: "k8s.io/api/core/v1"
  kind: "ObjectReference"
content_type: "api_reference"
description: "ObjectReference 包含足够的信息，可以让你检查或修改引用的对象。"
title: "ObjectReference"
weight: 8
auto_generated: true
---




`import "k8s.io/api/core/v1"`


ObjectReference包含足够的信息，允许你检查或修改引用的对象。

<hr>



- **apiVersion** (string)

  被引用者的 API 版本。

- **fieldPath** (string)

  如果引用的是对象的某个对象是整个对象，则该字符串而不是应包含的 JSON/Go 字段有效访问语句，
  例如 `desiredState.manifest.containers[ 2 ]`。例如，如果对象引用针对的是 Pod 中的一个容器，
  此字段取值类似于：`spec.containers{name}`（`name` 指触发的容器的名称），
  或者如果没有指定容器名称，`spec.containers[ 2 ]`（此 Pod 中索引为 2 的容器）。
  选择这种只是为了有一些定义好的语法来引用对象的部分。

- **kind** (string)

  被引用者的类别（kind）。更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **name** (string)

  被引用对象的名称。更多信息： https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

- **namespace** (string)

  被引用对象的名字空间。更多信息： https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/

- **resourceVersion** (string)

  被引用对象的特定资源版本（如果有）。更多信息： https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#concurrency-control-and-consistency

- **uid** (string)

  被引用对象的UID。更多信息： https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#uids

