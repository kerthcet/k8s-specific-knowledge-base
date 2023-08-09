---
title: 从 dockershim 迁移遥测和安全代理
content_type: task 
weight: 60
---


{{% thirdparty-content %}}

Kubernetes 对与 Docker Engine 直接集成的支持已被弃用且已经被删除。
大多数应用程序不直接依赖于托管容器的运行时。但是，仍然有大量的遥测和监控代理依赖
docker 来收集容器元数据、日志和指标。
本文汇总了一些信息和链接：信息用于阐述如何探查这些依赖，链接用于解释如何迁移这些代理去使用通用的工具或其他容器运行。

## 遥测和安全代理 {#telemetry-and-security-agents}

在 Kubernetes 集群中，有几种不同的方式来运行遥测或安全代理。
一些代理在以 DaemonSet 的形式运行或直接在节点上运行时，直接依赖于 Docker Engine。

### 为什么有些遥测代理会与 Docker Engine 通信？

从历史上看，Kubernetes 是专门为与 Docker Engine 一起工作而编写的。
Kubernetes 负责网络和调度，依靠 Docker Engine
在节点上启动并运行容器（在 Pod 内）。一些与遥测相关的信息，例如 pod 名称，
只能从 Kubernetes 组件中获得。其他数据，例如容器指标，不是容器运行时的责任。
早期遥测代理需要查询容器运行时**和** Kubernetes 以报告准确的信息。
随着时间的推移，Kubernetes 获得了支持多种运行时的能力，
现在支持任何兼容[容器运行时接口](/zh-cn/docs/concepts/architecture/cri/)的运行时。

一些代理和 Docker 工具紧密绑定。比如代理会用到
[`docker ps`](https://docs.docker.com/engine/reference/commandline/ps/)
或 [`docker top`](https://docs.docker.com/engine/reference/commandline/top/)
这类命令来列出容器和进程，用
[`docker logs`](https://docs.docker.com/engine/reference/commandline/logs/)
订阅 Docker 的日志。
如果现有集群中的节点使用 Docker Engine，在你切换到其它容器运行时的时候，
这些命令将不再起作用。

### 识别依赖于 Docker Engine 的 DaemonSet {#identify-docker-dependency}

如果某 Pod 想调用运行在节点上的 `dockerd`，该 Pod 必须满足以下两个条件之一：

- 将包含 Docker 守护进程特权套接字的文件系统挂载为一个{{< glossary_tooltip text="卷" term_id="volume" >}}；或
- 直接以卷的形式挂载 Docker 守护进程特权套接字的特定路径。

举例来说：在 COS 镜像中，Docker 通过 `/var/run/docker.sock` 开放其 Unix 域套接字。
这意味着 Pod 的规约中需要包含 `hostPath` 卷以挂载 `/var/run/docker.sock`。

下面是一个 shell 示例脚本，用于查找包含直接映射 Docker 套接字的挂载点的 Pod。
你也可以删掉 `grep '/var/run/docker.sock'` 这一代码片段以查看其它挂载信息。

```bash
kubectl get pods --all-namespaces \
-o=jsonpath='{range .items[*]}{"\n"}{.metadata.namespace}{":\t"}{.metadata.name}{":\t"}{range .spec.volumes[*]}{.hostPath.path}{", "}{end}{end}' \
| sort \
| grep '/var/run/docker.sock'
```

{{< note >}}
对于 Pod 来说，访问宿主机上的 Docker 还有其他方式。
例如，可以挂载 `/var/run` 的父目录而非其完整路径
（就像[这个例子](https://gist.github.com/itaysk/7bc3e56d69c4d72a549286d98fd557dd)）。
上述脚本只检测最常见的使用方式。
{{< /note >}}

### 检测节点代理对 Docker 的依赖性 {#detecting-docker-dependency-from-node-agents}

在你的集群节点被定制、且在各个节点上均安装了额外的安全和遥测代理的场景下，
一定要和代理的供应商确认：该代理是否依赖于 Docker。

### 遥测和安全代理的供应商 {#telemetry-and-security-agent-vendors}

本节旨在汇总有关可能依赖于容器运行时的各种遥测和安全代理的信息。

我们通过
[谷歌文档](https://docs.google.com/document/d/1ZFi4uKit63ga5sxEiZblfb-c23lFhvy6RXVPikS8wf0/edit#)
提供了为各类遥测和安全代理供应商准备的持续更新的迁移指导。
请与供应商联系，获取从 dockershim 迁移的最新说明。

## 从 dockershim 迁移 {#migration-from-dockershim}

### [Aqua](https://www.aquasec.com)

无需更改：在运行时变更时可以无缝切换运行。

### [Datadog](https://www.datadoghq.com/product/)

如何迁移： 
[Kubernetes 中对于 Docker 的弃用](https://docs.datadoghq.com/agent/guide/docker-deprecation/) 
名字中包含以下字符串的 Pod 可能访问 Docker Engine：

- `datadog-agent`
- `datadog`
- `dd-agent`

### [Dynatrace](https://www.dynatrace.com/)

如何迁移：
[在 Dynatrace 上从 Docker-only 迁移到通用容器指标](https://community.dynatrace.com/t5/Best-practices/Migrating-from-Docker-only-to-generic-container-metrics-in/m-p/167030#M49)

Containerd 支持公告：[在基于 containerd 的 Kubernetes 环境的获取容器的自动化全栈可见性](https://www.dynatrace.com/news/blog/get-automated-full-stack-visibility-into-containerd-based-kubernetes-environments/)
CRI-O 支持公告：[在基于 CRI-O 的 Kubernetes 环境获取容器的自动化全栈可见性（测试版）](https://www.dynatrace.com/news/blog/get-automated-full-stack-visibility-into-your-cri-o-kubernetes-containers-beta/)

名字中包含以下字符串的 Pod 可能访问 Docker：
- `dynatrace-oneagent`

### [Falco](https://falco.org)

如何迁移：
[迁移 Falco 从 dockershim](https://falco.org/docs/getting-started/deployment/#docker-deprecation-in-kubernetes)
Falco 支持任何与 CRI 兼容的运行时（默认配置中使用 containerd）；该文档解释了所有细节。

名字中包含以下字符串的 Pod 可能访问 Docker：
- `falco`


### [Prisma Cloud Compute](https://docs.paloaltonetworks.com/prisma/prisma-cloud.html)

在依赖于 CRI（非 Docker）的集群上安装 Prisma Cloud 时，查看
[Prisma Cloud 提供的文档](https://docs.paloaltonetworks.com/prisma/prisma-cloud/prisma-cloud-admin-compute/install/install_kubernetes.html)。

名字中包含以下字符串的 Pod 可能访问 Docker：

- `twistlock-defender-ds`


### [SignalFx (Splunk)](https://www.splunk.com/en_us/investor-relations/acquisitions/signalfx.html)

SignalFx Smart Agent（已弃用）在 Kubernetes 集群上使用了多种不同的监视器，
包括 `kubernetes-cluster`，`kubelet-stats/kubelet-metrics`，`docker-container-stats`。
`kubelet-stats` 监视器此前已被供应商所弃用，现支持 `kubelet-metrics`。
`docker-container-stats` 监视器受 dockershim 移除的影响。
不要为 `docker-container-stats` 监视器使用 Docker Engine 之外的运行时。

如何从依赖 dockershim 的代理迁移：
1. 从[所配置的监视器](https://github.com/signalfx/signalfx-agent/blob/main/docs/monitor-config.md)中移除 `docker-container-stats`。
   注意，若节点上已经安装了 Docker，在非 dockershim 环境中启用此监视器后会导致报告错误的指标；
   如果节点未安装 Docker，则无法获得指标。
2. [启用和配置 `kubelet-metrics`](https://github.com/signalfx/signalfx-agent/blob/main/docs/monitors/kubelet-metrics.md) 监视器。

{{< note >}}
收集的指标会发生变化。具体请查看你的告警规则和仪表盘。
{{< /note >}}

名字中包含以下字符串的 Pod 可能访问 Docker：
- `signalfx-agent`

### Yahoo Kubectl Flame

Flame 不支持 Docker 以外的容器运行时，具体可见 [https://github.com/yahoo/kubectl-flame/issues/51](https://github.com/yahoo/kubectl-flame/issues/51)

