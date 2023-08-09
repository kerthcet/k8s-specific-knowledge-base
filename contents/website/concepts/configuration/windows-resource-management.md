---
title: Windows 节点的资源管理
content_type: concept
weight: 75
---

本页概述了 Linux 和 Windows 在资源管理方式上的区别。

在 Linux 节点上，{{< glossary_tooltip text="cgroup" term_id="cgroup" >}} 用作资源控制的 Pod 边界。
在这个边界内创建容器以便于隔离网络、进程和文件系统。
Linux cgroup API 可用于收集 CPU、I/O 和内存使用统计数据。

与此相反，Windows 中每个容器对应一个[**作业对象**](https://docs.microsoft.com/zh-cn/windows/win32/procthread/job-objects)，
与系统命名空间过滤器一起使用，将所有进程包含在一个容器中，提供与主机的逻辑隔离。
（作业对象是一种 Windows 进程隔离机制，不同于 Kubernetes 提及的 {{< glossary_tooltip term_id="job" text="Job" >}})。

如果没有命名空间过滤，就无法运行 Windows 容器。
这意味着在主机环境中无法让系统特权生效，因此特权容器在 Windows 上不可用。
容器不能使用来自主机的标识，因为安全帐户管理器（Security Account Manager，SAM）是独立的。

## 内存管理 {#resource-management-memory}

Windows 不像 Linux 一样提供杀手（killer）机制，杀死内存不足的进程。
Windows 始终将所有用户态内存分配视为虚拟内存，并强制使用页面文件（pagefile）。

Windows 节点不会为进程过量使用内存。
最终结果是 Windows 不会像 Linux 那样达到内存不足的情况，Windows 将进程页面放到磁盘，
不会因为内存不足（OOM）而终止进程。
如果内存配置过量且所有物理内存都已耗尽，则换页性能就会降低。
## CPU 管理 {#resource-management-cpu}

Windows 可以限制为不同进程分配的 CPU 时间长度，但无法保证最小的 CPU 时间长度。

在 Windows 上，kubelet 支持使用命令行标志来设置 kubelet 进程的[调度优先级](https://docs.microsoft.com/zh-cn/windows/win32/procthread/scheduling-priorities)：
`--windows-priorityclass`。
与 Windows 主机上运行的其他进程相比，此标志允许 kubelet 进程获取更多的 CPU 时间片。
有关允许值及其含义的更多信息，请访问 [Windows 优先级类](https://docs.microsoft.com/zh-cn/windows/win32/procthread/scheduling-priorities#priority-class)。
为了确保运行的 Pod 不会耗尽 kubelet 的 CPU 时钟周期，
要将此标志设置为 `ABOVE_NORMAL_PRIORITY_CLASS` 或更高。

## 资源预留 {#resource-reservation}

为了满足操作系统、容器运行时和 kubelet 等 Kubernetes 主机进程使用的内存和 CPU，
你可以（且应该）用 `--kube-reserved` 和/或 `--system-reserved` kubelet 标志来预留内存和 CPU 资源。
在 Windows 上，这些值仅用于计算节点的[可分配](/zh-cn/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable)资源。

{{< caution >}}
在你部署工作负载时，需对容器设置内存和 CPU 资源的限制。
这也会从 `NodeAllocatable` 中减去，帮助集群范围的调度器决定哪些 Pod 放到哪些节点上。

若调度 Pod 时未设置限制值，可能对 Windows 节点过量配置资源。
在极端情况下，这会让节点变得不健康。
{{< /caution >}}

在 Windows 上，一种好的做法是预留至少 2GiB 的内存。

要决定预留多少 CPU，需明确每个节点的最大 Pod 密度，
并监控节点上运行的系统服务的 CPU 使用率，然后选择一个满足工作负载需求的值。
