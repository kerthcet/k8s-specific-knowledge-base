---
title: JSONPath 支持
content_type: concept
weight: 40
---

kubectl 支持 JSONPath 模板。



JSONPath 模板由 {} 包起来的 JSONPath 表达式组成。Kubectl 使用 JSONPath 表达式来过滤 JSON 对象中的特定字段并格式化输出。
除了原始的 JSONPath 模板语法，以下函数和语法也是有效的:

1. 使用双引号将 JSONPath 表达式内的文本引起来。
2. 使用 `range`，`end` 运算符来迭代列表。
3. 使用负片索引后退列表。负索引不会“环绕”列表，并且只要 `-index + listLength> = 0` 就有效。

{{< note >}}
- `$` 运算符是可选的，因为默认情况下表达式总是从根对象开始。

- 结果对象将作为其 String() 函数输出。

{{< /note >}}

给定 JSON 输入:

```json
{
  "kind": "List",
  "items":[
    {
      "kind":"None",
      "metadata":{"name":"127.0.0.1"},
      "status":{
        "capacity":{"cpu":"4"},
        "addresses":[{"type": "LegacyHostIP", "address":"127.0.0.1"}]
      }
    },
    {
      "kind":"None",
      "metadata":{"name":"127.0.0.2"},
      "status":{
        "capacity":{"cpu":"8"},
        "addresses":[
          {"type": "LegacyHostIP", "address":"127.0.0.2"},
          {"type": "another", "address":"127.0.0.3"}
        ]
      }
    }
  ],
  "users":[
    {
      "name": "myself",
      "user": {}
    },
    {
      "name": "e2e",
      "user": {"username": "admin", "password": "secret"}
    }
  ]
}
```

函数            | 描述               | 示例                                                         | 结果
--------------------|---------------------------|-----------------------------------------------------------------|------------------
`text`              | 纯文本            | `kind is {.kind}`                                               | `kind is List`
`@`                 | 当前对象        | `{@}`                                                           | 与输入相同
`.` or `[]`         | 子运算符            | `{.kind}`, `{['kind']}` or `{['name\.type']}`                    | `List`
`..`                | 递归下降         | `{..name}`                                                      | `127.0.0.1 127.0.0.2 myself e2e`
`*`                 | 通配符。获取所有对象 | `{.items[*].metadata.name}`                                     | `[127.0.0.1 127.0.0.2]`
`[start:end:step]`  | 下标运算符        | `{.users[0].name}`                                              | `myself`
`[,]`               | 并集运算符            | `{.items[*]['metadata.name', 'status.capacity']}`               | `127.0.0.1 127.0.0.2 map[cpu:4] map[cpu:8]`
`?()`               | 过滤                    | `{.users[?(@.name=="e2e")].user.password}`                      | `secret`
`range`, `end`      | 迭代列表              | `{range .items[*]}[{.metadata.name}, {.status.capacity}] {end}` | `[127.0.0.1, map[cpu:4]] [127.0.0.2, map[cpu:8]]`
`''`                | 引用解释执行字符串  | `{range .items[*]}{.metadata.name}{'\t'}{end}`                  | `127.0.0.1      127.0.0.2`

使用 `kubectl` 和 JSONPath 表达式的示例:

```shell
kubectl get pods -o json
kubectl get pods -o=jsonpath='{@}'
kubectl get pods -o=jsonpath='{.items[0]}'
kubectl get pods -o=jsonpath='{.items[0].metadata.name}'
kubectl get pods -o=jsonpath="{.items[*]['metadata.name', 'status.capacity']}"
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.startTime}{"\n"}{end}'
```

{{< note >}}
在 Windows 上，对于任何包含空格的 JSONPath 模板，你必须使用双引号（不是上面 bash 所示的单引号）。
反过来，这意味着你必须在模板中的所有文字周围使用单引号或转义的双引号。
例如:

```cmd
C:\> kubectl get pods -o=jsonpath="{range .items[*]}{.metadata.name}{'\t'}{.status.startTime}{'\n'}{end}"
C:\> kubectl get pods -o=jsonpath="{range .items[*]}{.metadata.name}{\"\t\"}{.status.startTime}{\"\n\"}{end}"
```
{{< /note >}}

{{< note >}}
不支持 JSONPath 正则表达式。如需使用正则表达式进行匹配操作，你可以使用如 `jq` 之类的工具。

```shell
# kubectl 的 JSONpath 输出不支持正则表达式
# 下面的命令不会生效
kubectl get pods -o jsonpath='{.items[?(@.metadata.name=~/^test$/)].metadata.name}'

# 下面的命令可以获得所需的结果
kubectl get pods -o json | jq -r '.items[] | select(.metadata.name | test("test-")).spec.containers[].image'
```
{{< /note >}}
