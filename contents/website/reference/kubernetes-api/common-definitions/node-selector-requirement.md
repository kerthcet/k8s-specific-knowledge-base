---
api_metadata:
  apiVersion: ""
  import: "k8s.io/api/core/v1"
  kind: "NodeSelectorRequirement"
content_type: "api_reference"
description: 节点选择算符需求是一个选择算符，其中包含值集、主键以及一个将键和值集关联起来的操作符。
title: "NodeSelectorRequirement"
weight: 5
---


`import "k8s.io/api/core/v1"`

节点选择算符需求是一个选择算符，其中包含值集、主键以及一个将键和值集关联起来的操作符。

<hr>

- **key** (string)，必需

  选择算符所适用的标签主键。

- **operator** (string)，必需

  代表主键与值集之间的关系。合法的 operator 值包括 `In`、`NotIn`、`Exists`、`DoesNotExist`、`Gt` 和 `Lt`。
 
- **values** ([]string)

  一个由字符串值组成的数组。如果 operator 是 `In` 或 `NotIn`，则 values 数组不能为空。
  如果 operator 为 `Exists` 或 `DoesNotExist`，则 values 数组只能为空。
  如果 operator 为 `Gt` 或 `Lt`，则 values 数组只能包含一个元素，并且该元素会被解释为整数。
  在执行策略性合并补丁操作时，此数组会被整体替换。

