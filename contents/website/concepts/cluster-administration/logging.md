---
title: 日志架构
content_type: concept
weight: 60
---

应用日志可以让你了解应用内部的运行状况。日志对调试问题和监控集群活动非常有用。
大部分现代化应用都有某种日志记录机制。同样地，容器引擎也被设计成支持日志记录。
针对容器化应用，最简单且最广泛采用的日志记录方式就是写入标准输出和标准错误流。

但是，由容器引擎或运行时提供的原生功能通常不足以构成完整的日志记录方案。

例如，如果发生容器崩溃、Pod 被逐出或节点宕机等情况，你可能想访问应用日志。

在集群中，日志应该具有独立的存储，并且其生命周期与节点、Pod 或容器的生命周期相独立。
这个概念叫[集群级的日志](#cluster-level-logging-architectures)。

集群级日志架构需要一个独立的后端用来存储、分析和查询日志。
Kubernetes 并不为日志数据提供原生的存储解决方案。
相反，有很多现成的日志方案可以集成到 Kubernetes 中。
下面各节描述如何在节点上处理和存储日志。


## Pod 和容器日志   {#basic-logging-in-kubernetes}

Kubernetes 从正在运行的 Pod 中捕捉每个容器的日志。

此示例使用带有一个容器的 `Pod` 的清单，该容器每秒将文本写入标准输出一次。

{{< codenew file="debug/counter-pod.yaml" >}}

要运行此 Pod，请执行以下命令：

```shell
kubectl apply -f https://k8s.io/examples/debug/counter-pod.yaml
```

输出为：

```console
pod/counter created
```

要获取这些日志，请执行以下 `kubectl logs` 命令：

```shell
kubectl logs counter
```

输出类似于：

```console
0: Fri Apr  1 11:42:23 UTC 2022
1: Fri Apr  1 11:42:24 UTC 2022
2: Fri Apr  1 11:42:25 UTC 2022
```

你可以使用 `kubectl logs --previous` 从容器的先前实例中检索日志。
如果你的 Pod 有多个容器，请如下通过将容器名称追加到该命令并使用 `-c`
标志来指定要访问哪个容器的日志：

```shell
kubectl logs counter -c count
```

详见 [`kubectl logs` 文档](/docs/reference/generated/kubectl/kubectl-commands#logs)。

### 节点的容器日志处理方式   {#how-nodes-handle-container-logs}

![节点级别的日志记录](/images/docs/user-guide/logging/logging-node-level.png)

容器运行时对写入到容器化应用程序的 `stdout` 和 `stderr` 流的所有输出进行处理和转发。
不同的容器运行时以不同的方式实现这一点；不过它们与 kubelet 的集成都被标准化为 **CRI 日志格式**。

默认情况下，如果容器重新启动，kubelet 会保留一个终止的容器及其日志。
如果一个 Pod 被逐出节点，所对应的所有容器及其日志也会被逐出。

kubelet 通过 Kubernetes API 的特殊功能将日志提供给客户端访问。
访问这个日志的常用方法是运行 `kubectl logs`。

### 日志轮转   {#log-rotation}

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

你可以配置 kubelet 令其自动轮转日志。

如果配置轮转，kubelet 负责轮转容器日志并管理日志目录结构。
kubelet（使用 CRI）将此信息发送到容器运行时，而运行时则将容器日志写到给定位置。

你可以使用 [kubelet 配置文件](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/)配置两个
kubelet [配置选项](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)、
`containerLogMaxSize` 和 `containerLogMaxFiles`。
这些设置分别允许你分别配置每个日志文件大小的最大值和每个容器允许的最大文件数。

当类似于基本日志示例一样运行 [`kubectl logs`](/docs/reference/generated/kubectl/kubectl-commands#logs) 时，
节点上的 kubelet 会处理请求并直接从日志文件读取。kubelet 将返回该日志文件的内容。

{{< note >}}
只有最新的日志文件的内容可以通过 `kubectl logs` 获得。

例如，如果 Pod 写入 40 MiB 的日志，并且 kubelet 在 10 MiB 之后轮转日志，
则运行 `kubectl logs` 将最多返回 10 MiB 的数据。
{{< /note >}}

### 系统组件日志   {#system-component-logs}

系统组件有两种类型：通常在容器中运行的组件和直接参与容器运行的组件。例如：

* kubelet 和容器运行时不在容器中运行。kubelet 运行你的容器
  （一起按 {{< glossary_tooltip text="Pod" term_id="pod" >}} 分组）
* Kubernetes 调度器、控制器管理器和 API 服务器在 Pod 中运行
  （通常是{{< glossary_tooltip text="静态 Pod" term_id="static-pod" >}}。
  etcd 组件在控制平面中运行，最常见的也是作为静态 Pod。
  如果你的集群使用 kube-proxy，则通常将其作为 `DaemonSet` 运行。

### 日志位置   {#log-location-node}

kubelet 和容器运行时写入日志的方式取决于节点使用的操作系统：

{{< tabs name="log_location_node_tabs" >}}
{{% tab name="Linux" %}}

在使用 systemd 的 Linux 节点上，kubelet 和容器运行时默认写入 journald。
你要使用 `journalctl` 来阅读 systemd 日志；例如：`journalctl -u kubelet`。

如果 systemd 不存在，kubelet 和容器运行时将写入到 `/var/log` 目录中的 `.log` 文件。
如果你想将日志写入其他地方，你可以通过辅助工具 `kube-log-runner` 间接运行 kubelet，
并使用该工具将 kubelet 日志重定向到你所选择的目录。

kubelet 始终指示你的容器运行时将日志写入 `/var/log/pods` 中的目录。

有关 `kube-log-runner` 的更多信息，请阅读[系统日志](/zh-cn/docs/concepts/cluster-administration/system-logs/#klog)。

{{% /tab %}}
{{% tab name="Windows" %}}

默认情况下，kubelet 将日志写入目录 `C:\var\logs` 中的文件（注意这不是 `C:\var\log`）。

尽管 `C:\var\log` 是这些日志的 Kubernetes 默认位置，
但一些集群部署工具会将 Windows 节点设置为将日志放到 `C:\var\log\kubelet`。

如果你想将日志写入其他地方，你可以通过辅助工具 `kube-log-runner` 间接运行 kubelet，
并使用该工具将 kubelet 日志重定向到你所选择的目录。

但是，kubelet 总是指示你的容器运行时在目录 `C:\var\log\pods` 中写入日志。

有关 `kube-log-runner` 的更多信息，请阅读[系统日志](/zh-cn/docs/concepts/cluster-administration/system-logs/#klog)。
{{% /tab %}}
{{< /tabs >}}


对于在 Pod 中运行的 Kubernetes 集群组件，其日志会写入 `/var/log` 目录中的文件，
相当于绕过默认的日志机制（组件不会写入 systemd 日志）。
你可以使用 Kubernetes 的存储机制将持久存储映射到运行该组件的容器中。

有关 etcd 及其日志的详细信息，请查阅 [etcd 文档](https://etcd.io/docs/)。
同样，你可以使用 Kubernetes 的存储机制将持久存储映射到运行该组件的容器中。

{{< note >}}
如果你部署 Kubernetes 集群组件（例如调度器）以将日志记录到从父节点共享的卷中，
则需要考虑并确保这些日志被轮转。 **Kubernetes 不管理这种日志轮转**。

你的操作系统可能会自动实现一些日志轮转。例如，如果你将目录 `/var/log` 共享到一个组件的静态 Pod 中，
则节点级日志轮转会将该目录中的文件视同为 Kubernetes 之外的组件所写入的文件。

一些部署工具会考虑日志轮转并将其自动化；而其他一些工具会将此留给你来处理。
{{< /note >}}

## 集群级日志架构   {#cluster-level-logging-architectures}

虽然 Kubernetes 没有为集群级日志记录提供原生的解决方案，但你可以考虑几种常见的方法。
以下是一些选项：

* 使用在每个节点上运行的节点级日志记录代理。
* 在应用程序的 Pod 中，包含专门记录日志的边车（Sidecar）容器。
* 将日志直接从应用程序中推送到日志记录后端。

### 使用节点级日志代理   {#using-a-node-logging-agent}

![使用节点级日志代理](/images/docs/user-guide/logging/logging-with-node-agent.png)

你可以通过在每个节点上使用**节点级的日志记录代理**来实现集群级日志记录。
日志记录代理是一种用于暴露日志或将日志推送到后端的专用工具。
通常，日志记录代理程序是一个容器，它可以访问包含该节点上所有应用程序容器的日志文件的目录。

由于日志记录代理必须在每个节点上运行，推荐以 `DaemonSet` 的形式运行该代理。

节点级日志在每个节点上仅创建一个代理，不需要对节点上的应用做修改。

容器向标准输出和标准错误输出写出数据，但在格式上并不统一。
节点级代理收集这些日志并将其进行转发以完成汇总。

### 使用边车容器运行日志代理   {#sidecar-container-with-logging-agent}

你可以通过以下方式之一使用边车（Sidecar）容器：

* 边车容器将应用程序日志传送到自己的标准输出。
* 边车容器运行一个日志代理，配置该日志代理以便从应用容器收集日志。

#### 传输数据流的边车容器

![带数据流容器的边车容器](/images/docs/user-guide/logging/logging-with-streaming-sidecar.png)

利用边车容器，写入到自己的 `stdout` 和 `stderr` 传输流，
你就可以利用每个节点上的 kubelet 和日志代理来处理日志。
边车容器从文件、套接字或 journald 读取日志。
每个边车容器向自己的 `stdout` 和 `stderr` 流中输出日志。

这种方法允许你将日志流从应用程序的不同部分分离开，其中一些可能缺乏对写入
`stdout` 或 `stderr` 的支持。重定向日志背后的逻辑是最小的，因此它的开销不大。
另外，因为 `stdout` 和 `stderr` 由 kubelet 处理，所以你可以使用内置的工具 `kubectl logs`。

例如，某 Pod 中运行一个容器，且该容器使用两个不同的格式写入到两个不同的日志文件。
下面是这个 Pod 的清单：

{{< codenew file="admin/logging/two-files-counter-pod.yaml" >}}

不建议在同一个日志流中写入不同格式的日志条目，即使你成功地将其重定向到容器的 `stdout` 流。
相反，你可以创建两个边车容器。每个边车容器可以从共享卷跟踪特定的日志文件，
并将文件内容重定向到各自的 `stdout` 流。

下面是运行两个边车容器的 Pod 的清单：

{{< codenew file="admin/logging/two-files-counter-pod-streaming-sidecar.yaml" >}}

现在当你运行这个 Pod 时，你可以运行如下命令分别访问每个日志流：

```shell
kubectl logs counter count-log-1
```

输出类似于：

```console
0: Fri Apr  1 11:42:26 UTC 2022
1: Fri Apr  1 11:42:27 UTC 2022
2: Fri Apr  1 11:42:28 UTC 2022
...
```

```shell
kubectl logs counter count-log-2
```

输出类似于：

```console
Fri Apr  1 11:42:29 UTC 2022 INFO 0
Fri Apr  1 11:42:30 UTC 2022 INFO 0
Fri Apr  1 11:42:31 UTC 2022 INFO 0
...
```

如果你在集群中安装了节点级代理，由代理自动获取上述日志流，而无需任何进一步的配置。
如果你愿意，你可以将代理配置为根据源容器解析日志行。

即使对于 CPU 和内存使用率较低的 Pod（CPU 为几毫核，内存为几兆字节），将日志写入一个文件，
将这些日志流写到 `stdout` 也有可能使节点所需的存储量翻倍。
如果你有一个写入特定文件的应用程序，则建议将 `/dev/stdout` 设置为目标文件，而不是采用流式边车容器方法。

边车容器还可用于轮转应用程序本身无法轮转的日志文件。
这种方法的一个例子是定期运行 `logrotate` 的小容器。
但是，直接使用 `stdout` 和 `stderr` 更直接，而将轮转和保留策略留给 kubelet。

集群中安装的节点级代理会自动获取这些日志流，而无需进一步配置。
如果你愿意，你也可以配置代理程序来解析源容器的日志行。

注意，尽管 CPU 和内存使用率都很低（以多个 CPU 毫核指标排序或者按内存的兆字节排序），
向文件写日志然后输出到 `stdout` 流仍然会成倍地增加磁盘使用率。
如果你的应用向单一文件写日志，通常最好设置 `/dev/stdout` 作为目标路径，
而不是使用流式的边车容器方式。

如果应用程序本身不能轮转日志文件，则可以通过边车容器实现。
这种方式的一个例子是运行一个小的、定期轮转日志的容器。
然而，还是推荐直接使用 `stdout` 和 `stderr`，将日志的轮转和保留策略交给 kubelet。

### 具有日志代理功能的边车容器

![含日志代理的边车容器](/images/docs/user-guide/logging/logging-with-sidecar-agent.png)

如果节点级日志记录代理程序对于你的场景来说不够灵活，
你可以创建一个带有单独日志记录代理的边车容器，将代理程序专门配置为与你的应用程序一起运行。

{{< note >}}
在边车容器中使用日志代理会带来严重的资源损耗。
此外，你不能使用 `kubectl logs` 访问日志，因为日志并没有被 kubelet 管理。
{{< /note >}}

下面是两个配置文件，可以用来实现一个带日志代理的边车容器。
第一个文件包含用来配置 fluentd 的
[ConfigMap](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/)。

{{< codenew file="admin/logging/fluentd-sidecar-config.yaml" >}}

{{< note >}}
你可以将此示例配置中的 fluentd 替换为其他日志代理，从应用容器内的其他来源读取数据。
{{< /note >}}

第二个清单描述了一个运行 fluentd 边车容器的 Pod。
该 Pod 挂载一个卷，flutend 可以从这个卷上拣选其配置数据。

{{< codenew file="admin/logging/two-files-counter-pod-agent-sidecar.yaml" >}}

### 从应用中直接暴露日志目录   {#exposing-logs-directly-from-the-application}

![直接从应用程序暴露日志](/images/docs/user-guide/logging/logging-from-application.png)

从各个应用中直接暴露和推送日志数据的集群日志机制已超出 Kubernetes 的范围。

## {{% heading "whatsnext" %}}

* 阅读有关 [Kubernetes 系统日志](/zh-cn/docs/concepts/cluster-administration/system-logs/)的信息
* 进一步了解[追踪 Kubernetes 系统组件](/zh-cn/docs/concepts/cluster-administration/system-traces/)
* 了解当 Pod 失效时如何[定制 Kubernetes 记录的终止消息](/zh-cn/docs/tasks/debug/debug-application/determine-reason-pod-failure/#customizing-the-termination-message)
