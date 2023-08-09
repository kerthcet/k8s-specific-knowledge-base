---
title: 检查移除 Dockershim 是否对你有影响
content_type: task
weight: 50
---



Kubernetes 的 `dockershim` 组件使得你可以把 Docker 用作 Kubernetes 的
{{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}。
在 Kubernetes v1.24 版本中，内建组件 `dockershim` 被移除。

本页讲解你的集群把 Docker 用作容器运行时的运作机制，
并提供使用 `dockershim` 时，它所扮演角色的详细信息，
继而展示了一组操作，可用来检查移除 `dockershim` 对你的工作负载是否有影响。

## 检查你的应用是否依赖于 Docker {#find-docker-dependencies}

即使你是通过 Docker 创建的应用容器，也不妨碍你在其他任何容器运行时上运行这些容器。
这种使用 Docker 的方式并不构成对 Docker 作为一个容器运行时的依赖。

当用了别的容器运行时之后，Docker 命令可能不工作，或者产生意外的输出。
下面是判定你是否依赖于 Docker 的方法。

1. 确认没有特权 Pod 执行 Docker 命令（如 `docker ps`）、重新启动 Docker
   服务（如 `systemctl restart docker.service`）或修改 Docker 配置文件
   `/etc/docker/daemon.json`。
2. 检查 Docker 配置文件（如 `/etc/docker/daemon.json`）中容器镜像仓库的镜像（mirror）站点设置。
   这些配置通常需要针对不同容器运行时来重新设置。
3. 检查确保在 Kubernetes 基础设施之外的节点上运行的脚本和应用程序没有执行 Docker 命令。
   可能的情况有：
   - SSH 到节点排查故障；
   - 节点启动脚本；
   - 直接安装在节点上的监控和安全代理。
4. 检查执行上述特权操作的第三方工具。
   详细操作请参考[从 dockershim 迁移遥测和安全代理](/zh-cn/docs/tasks/administer-cluster/migrating-from-dockershim/migrating-telemetry-and-security-agents)。
5. 确认没有对 dockershim 行为的间接依赖。这是一种极端情况，不太可能影响你的应用。
   一些工具很可能被配置为使用了 Docker 特性，比如，基于特定指标发警报，
   或者在故障排查指令的一个环节中搜索特定的日志信息。
   如果你有此类配置的工具，需要在迁移之前，在测试集群上测试这类行为。

## Docker 依赖详解 {#role-of-dockershim}

[容器运行时](/zh-cn/docs/concepts/containers/#container-runtimes)是一个软件，
用来运行组成 Kubernetes Pod 的容器。
Kubernetes 负责编排和调度 Pod；在每一个节点上，{{< glossary_tooltip text="kubelet" term_id="kubelet" >}}
使用抽象的容器运行时接口，所以你可以任意选用兼容的容器运行时。

在早期版本中，Kubernetes 提供的兼容性支持一个容器运行时：Docker。
在 Kubernetes 后来的发展历史中，集群运营人员希望采用别的容器运行时。
于是 CRI 被设计出来满足这类灵活性需求 - 而 kubelet 亦开始支持 CRI。
然而，因为 Docker 在 CRI 规范创建之前就已经存在，Kubernetes 就创建了一个适配器组件 `dockershim`。
dockershim 适配器允许 kubelet 与 Docker 交互，就好像 Docker 是一个 CRI 兼容的运行时一样。

你可以阅读博文
[Kubernetes 正式支持集成 Containerd](/blog/2018/05/24/kubernetes-containerd-integration-goes-ga/)。

![Dockershim 和 Containerd CRI 的实现对比图](/images/blog/2018-05-24-kubernetes-containerd-integration-goes-ga/cri-containerd.png)

切换到 Containerd 容器运行时可以消除掉中间环节。
所有相同的容器都可由 Containerd 这类容器运行时来运行。
但是现在，由于直接用容器运行时调度容器，它们对 Docker 是不可见的。
因此，你以前用来检查这些容器的 Docker 工具或漂亮的 UI 都不再可用。

你不能再使用 `docker ps` 或 `docker inspect` 命令来获取容器信息。
由于你不能列出容器，因此你不能获取日志、停止容器，甚至不能通过 `docker exec` 在容器中执行命令。

{{< note >}}
如果你在用 Kubernetes 运行工作负载，最好通过 Kubernetes API 停止容器，
而不是通过容器运行时来停止它们（此建议适用于所有容器运行时，不仅仅是针对 Docker）。
{{< /note >}}

你仍然可以下载镜像，或者用 `docker build` 命令创建它们。
但用 Docker 创建、下载的镜像，对于容器运行时和 Kubernetes，均不可见。
为了在 Kubernetes 中使用，需要把镜像推送（push）到某镜像仓库。

## 已知问题  {#known-issues}

### 一些文件系统指标缺失并且指标格式不同  {#some-filesystem-metrics-are-missing-and-the-metrics-format-is-different}

Kubelet `/metrics/cadvisor` 端点提供 Prometheus 指标，
如 [Kubernetes 系统组件指标](/zh-cn/docs/concepts/cluster-administration/system-metrics/) 中所述。
如果你安装了一个依赖该端点的指标收集器，你可能会看到以下问题：

- Docker 节点上的指标格式为 `k8s_<container-name>_<pod-name>_<namespace>_<pod-uid>_<restart-count>`，
  但其他运行时的格式不同。例如，在 containerd 节点上它是 `<container-id>`。
- 一些文件系统指标缺失，如下所示：

  ```
  container_fs_inodes_free
  container_fs_inodes_total
  container_fs_io_current
  container_fs_io_time_seconds_total
  container_fs_io_time_weighted_seconds_total
  container_fs_limit_bytes
  container_fs_read_seconds_total
  container_fs_reads_merged_total
  container_fs_sector_reads_total
  container_fs_sector_writes_total
  container_fs_usage_bytes
  container_fs_write_seconds_total
  container_fs_writes_merged_total
  ```

#### 解决方法  {#workaround}

你可以通过使用 [cAdvisor](https://github.com/google/cadvisor) 作为一个独立的守护程序来缓解这个问题。

1. 找到名称格式为 `vX.Y.Z-containerd-cri` 的最新
   [cAdvisor 版本](https://github.com/google/cadvisor/releases)（例如 `v0.42.0-containerd-cri`）。
2. 按照 [cAdvisor Kubernetes Daemonset](https://github.com/google/cadvisor/tree/master/deploy/kubernetes)
   中的步骤来创建守护进程。
3. 将已安装的指标收集器指向使用 cAdvisor 的 `/metrics` 端点。
   该端点提供了全套的 [Prometheus 容器指标](https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md)。

替代方案：

- 使用替代的第三方指标收集解决方案。
- 从 Kubelet 摘要 API 收集指标，该 API 在 `/stats/summary` 提供服务。

## {{% heading "whatsnext" %}}

- 阅读[从 dockershim 迁移](/zh-cn/docs/tasks/administer-cluster/migrating-from-dockershim/)，
  以了解你的下一步工作。
- 阅读[弃用 Dockershim 的常见问题](/zh-cn/blog/2020/12/02/dockershim-faq/)，了解更多信息。
