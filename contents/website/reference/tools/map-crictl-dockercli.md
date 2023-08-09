---
title: 从 Docker 命令行映射到 crictl
content_type: reference
weight: 10
---


{{% thirdparty-content %}}

`crictl` 是兼容 {{<glossary_tooltip term_id="cri" text="CRI">}}的容器运行时的一种命令行接口。
你可以使用它来在 Kubernetes 节点上检视和调试容器运行时和应用。
`crictl` 及其源代码都托管在
[cri-tools](https://github.com/kubernetes-sigs/cri-tools) 仓库中。

本页面提供一份参考资料，用来将 `docker` 命令行工具的常用命令映射到
`crictl` 的等价命令。

## 从 docker 命令行映射到 crictl   {#mapping-from-docker-cli-to-crictl}

映射表格中列举的确切版本是 `docker` 命令行的 v1.40 版本和 `crictl` 的 v1.19.0 版本。
这一列表不是完备的。例如，其中并未包含实验性质的 `docker` 命令。

{{< note >}}
`crictl` 的输出格式类似于 `docker` 命令行，只是对于某些命令而言会有部分列缺失。
如果你的命令输出会被程序解析，请确保你认真查看了对应的命令输出。
{{< /note >}}

### 获得调试信息   {#retrieve-debugging-information}

{{< table caption="docker 命令行与 crictl 的映射 - 获得调试信息" >}}
docker CLI | crictl | 描述 | 不支持的功能
-- | -- | -- | --
`attach` | `attach` | 挂接到某运行中的容器 | `--detach-keys`, `--sig-proxy`
`exec` | `exec` | 在运行中的容器内执行命令 | `--privileged`, `--user`, `--detach-keys`
`images` | `images` | 列举镜像 |  
`info` | `info` | 显示系统范围的信息 |  
`inspect` | `inspect`, `inspecti` | 返回容器、镜像或任务的底层信息 |  
`logs` | `logs` | 取回容器的日志数据  | `--details`
`ps` | `ps` | 列举容器  |  
`stats` | `stats` | 显示容器资源用量统计的动态数据流 | 列：NET/BLOCK I/O、PIDs
`version` | `version` | 显示运行时（Docker、ContainerD 或其他）的版本信息 | 
{{< /table >}}

### 执行变更    {#perform-changes}

{{< table caption="docker 命令行与 crictl 的映射 - 执行变更" >}}
docker CLI | crictl | 描述 | 不支持的功能
-- | -- | -- | --
`create` | `create` | 创建一个新容器 |  
`kill` | `stop` (超时值为 0) | 杀死一个或多个运行中的容器 | `--signal`
`pull` | `pull` | 从某镜像库拉取镜像或仓库 | `--all-tags`, `--disable-content-trust`
`rm` | `rm` | 移除一个或者多个容器 |  
`rmi` | `rmi` | 移除一个或者多个镜像 |  
`run` | `run` | 在一个新的容器中执行命令 |  
`start` | `start` | 启动一个或多个已停止的容器 | `--detach-keys`
`stop` | `stop` | 停止一个或多个运行中的容器 |  
`update` | `update` | 更新一个或多个容器的配置 | `--restart`、`--blkio-weight` 以 CRI 所不支持的资源约束
{{< /table >}}

### 仅被 crictl 支持的命令   {#supported-only-in-crictl}

{{< table caption="docker 命令行与 crictl 的映射 - 仅被 crictl 支持的命令" >}}
crictl | 描述
-- | --
`imagefsinfo` | 返回镜像文件系统信息
`inspectp` | 显示一个或多个 Pod 的状态
`port-forward` | 将本地端口转发到 Pod
`pods` | 列举 Pod
`runp` | 运行一个新的 Pod
`rmp` | 删除一个或多个 Pod
`stopp` | 停止一个或多个运行中的 Pod
{{< /table >}}
