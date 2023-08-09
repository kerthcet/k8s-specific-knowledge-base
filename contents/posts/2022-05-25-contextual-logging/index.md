---
layout: blog
title: "Kubernetes 1.24 中的上下文日志记录"
date: 2022-05-25
slug: contextual-logging
---

**作者:** Patrick Ohly (Intel)

[结构化日志工作组](https://github.com/kubernetes/community/blob/master/wg-structured-logging/README.md)
在 Kubernetes 1.24 中为日志基础设施添加了新功能。这篇博文解释了开发者如何利用这些功能使日志输出更有用，
以及他们如何参与改进 Kubernetes。

## 结构化日志记录

[结构化日志](https://github.com/kubernetes/enhancements/blob/master/keps/sig-instrumentation/1602-structured-logging/README.md)
记录的目标是用具有明确定义的语法的日志条目来取代 C 风格的格式化和由此产生的不透明的日志字符串，用于分别存储消息和参数，例如，作为一个 JSON 结构。

当使用传统的 klog 文本输出格式进行结构化日志调用时，字符串最初使用 `\n` 转义序列打印，除非嵌入到结构中。
对于结构体，日志条目仍然可以跨越多行，没有干净的方法将日志流拆分为单独的条目：

```
I1112 14:06:35.783529  328441 structured_logging.go:51] "using InfoS" longData={Name:long Data:Multiple
lines
with quite a bit
of text. internal:0}
I1112 14:06:35.783549  328441 structured_logging.go:52] "using InfoS with\nthe message across multiple lines" int=1 stringData="long: Multiple\nlines\nwith quite a bit\nof text." str="another value"
```

现在，`<` 和 `>` 标记以及缩进用于确保在行首的 klog 标头处拆分是可靠的，并且生成的输出是人类可读的：

```
I1126 10:31:50.378204  121736 structured_logging.go:59] "using InfoS" longData=<
	{Name:long Data:Multiple
	lines
	with quite a bit
	of text. internal:0}
 >
I1126 10:31:50.378228  121736 structured_logging.go:60] "using InfoS with\nthe message across multiple lines" int=1 stringData=<
	long: Multiple
	lines
	with quite a bit
	of text.
 > str="another value"
```

请注意，日志消息本身带有引号。它是一个用于标识日志条目的固定字符串，因此应避免使用换行符。

在 Kubernetes 1.24 之前，kube-scheduler 中的一些日志调用仍然使用 `klog.Info` 处理多行字符串，
以避免不可读的输出。现在所有日志调用都已更新以支持结构化日志记录。

## 上下文日志记录

[上下文日志](https://github.com/kubernetes/enhancements/blob/master/keps/sig-instrumentation/3077-contextual-logging/README.md)
基于 [go-logr API](https://github.com/go-logr/logr#a-minimal-logging-api-for-go)。
关键的想法是，库被其调用者传递给一个记录器实例，并使用它来记录，而不是访问一个全局记录器。
二进制文件决定了日志的实现，而不是库。go-logr API 是围绕着结构化的日志记录而设计的，并支持将额外的信息附加到一个记录器上。


这使得以下用例成为可能：

- 调用者可以将附加信息附加到记录器：
  - [`WithName`](https://pkg.go.dev/github.com/go-logr/logr#Logger.WithName) 添加前缀
  - [`WithValues`](https://pkg.go.dev/github.com/go-logr/logr#Logger.WithValues) 添加键/值对
  
  当将此扩展记录器传递给函数并且函数使用它而不是全局记录器时，附加信息随后将包含在所有日志条目中，而无需修改生成日志条目的代码。
  这在高度并行的应用程序中很有用，在这些应用程序中，由于不同操作的输出会交错，因此很难识别某个操作的所有日志条目。

- 运行单元测试时，可以将日志输出与当前测试关联起来。当测试失败时，`go test` 只显示失败测试的日志输出。
默认情况下，该输出也可以更详细，因为它不会显示成功的测试。这些测试可以在不交错输出的情况下并行运行。

上下文日志记录的设计决策之一是允许将记录器作为值附加到 `context.Context`。
由于记录器封装了调用的预期记录的所有方面，它是上下文的**部分**，而不仅仅是**使用**它。 
一个实际的优势是许多 API 已经有一个 `ctx` 参数，或者添加一个具有其他优势，例如能够摆脱函数内部的 `context.TODO()` 调用。

另一个决定是不破坏与 klog v2 的兼容性：

- 在已设置上下文日志记录的二进制文件中使用传统 klog 日志记录调用的库将通过二进制文件选择的日志记录后端工作和记录。
  但是，这样的日志输出不会包含额外的信息，并且在单元测试中不能很好地工作，因此应该修改库以支持上下文日志记录。 
  结构化日志记录的[迁移指南](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-instrumentation/migration-to-structured-logging.md)
  已扩展为也涵盖上下文日志记录。

- 当一个库支持上下文日志并从其上下文中检索一个记录器时，它仍将在不初始化上下文日志的二进制文件中工作，
  因为它将获得一个通过 klog 记录的记录器。

在 Kubernetes 1.24 中，上下文日志是一个新的 Alpha 特性，以 `ContextualLogging` 作为特性门控。
禁用时（默认），用于上下文日志记录的新 klog API 调用（见下文）变为无操作，以避免性能或功能回归。

尚未转换任何 Kubernetes 组件。 Kubernetes 存储库中的[示例程序](https://github.com/kubernetes/kubernetes/blob/v1.24.0-beta.0/staging/src/k8s.io/component-base/logs/example/cmd/logger.go)
演示了如何在一个二进制文件中启用上下文日志记录，以及输出如何取决于该二进制文件的参数：

```console
$ cd $GOPATH/src/k8s.io/kubernetes/staging/src/k8s.io/component-base/logs/example/cmd/
$ go run . --help
...
      --feature-gates mapStringBool  A set of key=value pairs that describe feature gates for alpha/experimental features. Options are:
                                     AllAlpha=true|false (ALPHA - default=false)
                                     AllBeta=true|false (BETA - default=false)
                                     ContextualLogging=true|false (ALPHA - default=false)
$ go run . --feature-gates ContextualLogging=true
...
I0404 18:00:02.916429  451895 logger.go:94] "example/myname: runtime" foo="bar" duration="1m0s"
I0404 18:00:02.916447  451895 logger.go:95] "example: another runtime" foo="bar" duration="1m0s"
```

`example` 前缀和 `foo="bar"` 是由记录 `runtime` 消息和 `duration="1m0s"` 值的函数的调用者添加的。

针对 klog 的示例代码包括一个单元测试[示例](https://github.com/kubernetes/klog/blob/v2.60.1/ktesting/example/example_test.go)
以及每个测试的输出。
## klog 增强功能

### 上下文日志 API

以下调用管理记录器的查找：

[`FromContext`](https://pkg.go.dev/k8s.io/klog/v2#FromContext)
：来自 `context` 参数，回退到全局记录器

[`Background`](https://pkg.go.dev/k8s.io/klog/v2#Background)
：全局后备，无意支持上下文日志记录

[`TODO`](https://pkg.go.dev/k8s.io/klog/v2#TODO)
：全局回退，但仅作为一个临时解决方案，直到该函数得到扩展能够通过其参数接受一个记录器

[`SetLoggerWithOptions`](https://pkg.go.dev/k8s.io/klog/v2#SetLoggerWithOptions)
：更改后备记录器；当使用[`ContextualLogger(true)`](https://pkg.go.dev/k8s.io/klog/v2#ContextualLogger) 调用时,
记录器已准备好被直接调用，在这种情况下，记录将无需执行通过 klog

为了支持 Kubernetes 中的特性门控机制，klog 对相应的 go-logr 调用进行了包装调用，并使用了一个全局布尔值来控制它们的行为：

- [`LoggerWithName`](https://pkg.go.dev/k8s.io/klog/v2#LoggerWithName)
- [`LoggerWithValues`](https://pkg.go.dev/k8s.io/klog/v2#LoggerWithValues)
- [`NewContext`](https://pkg.go.dev/k8s.io/klog/v2#NewContext)
- [`EnableContextualLogging`](https://pkg.go.dev/k8s.io/klog/v2#EnableContextualLogging)

在 Kubernetes 代码中使用这些函数是通过 linter 检查强制执行的。 
上下文日志的 klog 默认是启用该功能，因为它在 klog 中被认为是稳定的。
只有在 Kubernetes 二进制文件中，该默认值才会被覆盖，并且（在某些二进制文件中）通过 `--feature-gate` 参数进行控制。

### ktesting 记录器

新的 [ktesting](https://pkg.go.dev/k8s.io/klog/v2@v2.60.1/ktesting)
包使用 klog 的文本输出格式通过 `testing.T` 实现日志记录。它有一个 [single API call](https://pkg.go.dev/k8s.io/klog/v2@v2.60.1/ktesting#NewTestContext)
用于检测测试用例和[支持命令行标志](https://pkg.go.dev/k8s.io/klog/v2@v2.60.1/ktesting/init)。

### klogr

[`klog/klogr`](https://pkg.go.dev/k8s.io/klog/v2@v2.60.1/klogr) 继续受支持，默认行为不变：
它使用其格式化结构化日志条目拥有自己的自定义格式并通过 klog 打印结果。

但是，不鼓励这种用法，因为这种格式既不是机器可读的（与 zapr 生成的真实 JSON 输出相比，Kubernetes 使用的 go-logr 实现）也不是人类友好的（与 klog 文本格式相比）。

相反，应该使用选择 klog 文本格式的 [`WithFormat(FormatKlog)`](https://pkg.go.dev/k8s.io/klog/v2@v2.60.1/klogr#WithFormat)
创建一个 klogr 实例。 一个更简单但结果相同的构造方法是新的 [`klog.NewKlogr`](https://pkg.go.dev/k8s.io/klog/v2#NewKlogr)。 
这是 klog 在未配置任何其他内容时作为后备返回的记录器。


### 可重用输出测试

许多 go-logr 实现都有非常相似的单元测试，它们检查某些日志调用的结果。
如果开发人员不知道某些警告，例如调用时会出现恐慌的 `String` 函数，那么很可能缺少对此类警告的处理和单元测试。

[`klog.test`](https://pkg.go.dev/k8s.io/klog/v2@v2.60.1/test) 是一组可重用的测试用例，可应用于 go-logr 实现。

### 输出刷新

klog 用于在 `init` 期间无条件地启动一个 goroutine，它以硬编码的时间间隔刷新缓冲数据。
现在 goroutine 仅按需启动（即当写入具有缓冲的文件时）并且可以使用 [`StopFlushDaemon`](https://pkg.go.dev/k8s.io/klog/v2#StopFlushDaemon) 
和 [`StartFlushDaemon`](https://pkg.go.dev/k8s.io/klog/v2#StartFlushDaemon)。

当 go-logr 实现缓冲数据时，可以通过使用 [`FlushLogger`](https://pkg.go.dev/k8s.io/klog/v2#FlushLogger) 
选项注册记录器来将刷新该数据集成到 [`klog.Flush`](https://pkg.go.dev/k8s.io/klog/v2#Flush) 中。

### 其他各种变化

有关所有其他增强功能的描述，请参见 [发行说明](https://github.com/kubernetes/klog/releases)。

## 日志检查

最初设计为结构化日志调用的 linter，[`logcheck`] 工具已得到增强，还支持上下文日志记录和传统的 klog 日志调用。 
这些增强检查已经在 Kubernetes 中发现了错误，例如使用格式字符串和参数调用 `klog.Info` 而不是 `klog.Infof`。

它可以作为插件包含在 `golangci-lint` 调用中，这就是 
[Kubernetes 现在使用它的方式](https://github.com/kubernetes/kubernetes/commit/17e3c555c5115f8c9176bae10ba45baa04d23a7b)，或者单独调用。

我们正在 [移动工具](https://github.com/kubernetes/klog/issues/312)
到一个新的存储库中，因为它与 klog 没有真正的关系，并且应该正确跟踪和标记它的发布。

## 下一步

[Structured Logging WG](https://github.com/kubernetes/community/tree/master/wg-structured-logging)
一直在寻找新的贡献者。 从 C 风格的日志记录迁移现在将一步一步地针对结构化的上下文日志记录，
以减少整体代码流失和 PR 数量。 更改日志调用是对 Kubernetes 的良好贡献，也是了解各个不同领域代码的机会。