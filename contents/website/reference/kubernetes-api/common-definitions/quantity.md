---
api_metadata:
  apiVersion: ""
  import: "k8s.io/apimachinery/pkg/api/resource"
  kind: "Quantity"
content_type: "api_reference"
description: "数量（Quantity）是数字的定点表示。"
title: "Quantity"
weight: 10
---

`import "k8s.io/apimachinery/pkg/api/resource"`

数量（Quantity）是数字的定点表示。
除了 String() 和 AsInt64() 的访问接口之外，
它以 JSON 和 YAML 形式提供方便的打包和解包方法。

序列化格式如下：

```
<quantity>        ::= <signedNumber><suffix>
  (注意 <suffix> 可能为空，例如 <decimalSI> 的 "" 情形。) </br>
<digit>           ::= 0 | 1 | ... | 9 </br>
<digits>          ::= <digit> | <digit><digits> </br>
<number>          ::= <digits> | <digits>.<digits> | <digits>. | .<digits> </br>
<sign>            ::= "+" | "-" </br>
<signedNumber>    ::= <number> | <sign><number> </br>
<suffix>          ::= <binarySI> | <decimalExponent> | <decimalSI> </br>
<binarySI>        ::= Ki | Mi | Gi | Ti | Pi | Ei 
  (国际单位制度；查阅： http://physics.nist.gov/cuu/Units/binary.html)</br>
<decimalSI>       ::= m | "" | k | M | G | T | P | E 
  (注意，1024 = 1ki 但 1000 = 1k；我没有选择大写。) </br>
<decimalExponent> ::= "e" <signedNumber> | "E" <signedNumber> </br>
```

无论使用三种指数形式中哪一种，没有数量可以表示大于 2<sup>63</sup>-1 的数，也不可能超过 3 个小数位。
更大或更精确的数字将被截断或向上取整（例如：0.1m 将向上取整为 1m）。
如果将来我们需要更大或更小的数量，可能会扩展。

当从字符串解析数量时，它将记住它具有的后缀类型，并且在序列化时将再次使用相同类型。

在序列化之前，数量将以“规范形式”放置。这意味着指数或者后缀将被向上或向下调整（尾数相应增加或减少），并确保：

- 没有精度丢失
- 不会输出小数数字
- 指数（或后缀）尽可能大。

除非数量是负数，否则将省略正负号。

例如：

- 1.5 将会被序列化成 “1500m”
- 1.5Gi 将会被序列化成 “1536Mi”

请注意，数量永远**不会**在内部以浮点数表示。这是本设计的重中之重。

只要它们格式正确，非规范值仍将解析，但将以其规范形式重新输出（所以应该总是使用规范形式，否则不要执行 diff 比较）。

这种格式旨在使得很难在不撰写某种特殊处理代码的情况下使用这些数字，进而希望实现者也使用定点实现。

<hr>
