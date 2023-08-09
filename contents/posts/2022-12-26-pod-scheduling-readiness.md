---
layout: blog
title: "Kubernetes 1.26：Pod 调度就绪态"
date: 2022-12-26
slug: pod-scheduling-readiness-alpha
---


**作者：** Wei Huang (Apple), Abdullah Gharaibeh (Google)

**译者：** XiaoYang Zhang (HuaWei)

Kubernetes 1.26 引入了一个新的 Pod 特性：**调度门控**。
在 Kubernetes 中，调度门控是通知调度器何时可以考虑 Pod 调度的关键。

## 它解决了什么问题？

当 Pod 被创建时，调度器会不断尝试寻找适合它的节点。这个无限循环一直持续到调度程序为 Pod 找到节点，或者 Pod 被删除。

长时间无法被调度的 Pod（例如，被某些外部事件阻塞的 Pod）会浪费调度周期。
一个调度周期可能需要约 20ms 或更长时间，这取决于 Pod 的调度约束的复杂度。
因此，大量浪费的被调度周期会严重影响调度器的性能。请参阅下面 “调度器” 框中的箭头。

{{< mermaid >}}
graph LR;
  pod((新 Pod))-->queue
  subgraph 调度器
    queue(调度器队列)
    sched_cycle[/调度周期/]
    schedulable{可调度?}
    
    queue==>|弹出|sched_cycle
    sched_cycle==>schedulable
    schedulable==>|否|queue
    subgraph note [循环浪费在不断重新安排 'unready' 状态的 Pod 上]
    end
  end
  
 classDef plain fill:#ddd,stroke:#fff,stroke-width:1px,color:#000;
 classDef k8s fill:#326ce5,stroke:#fff,stroke-width:1px,color:#fff;
 classDef Scheduler fill:#fff,stroke:#bbb,stroke-width:2px,color:#326ce5;
 classDef note fill:#edf2ae,stroke:#fff,stroke-width:1px;
 class queue,sched_cycle,schedulable k8s;
 class pod plain;
 class note note;
 class Scheduler Scheduler;
{{< /mermaid >}}

调度门控有助于解决这个问题。它允许声明新创建的 Pod 尚未准备好进行调度。
当 Pod 上设置了调度门控时，调度程序会忽略该 Pod，从而避免不必要的调度尝试。
如果你在集群中安装了 Cluster Autoscaler，这些 Pod 也将被忽略。

清除门控是外部控制器的责任，外部控制器知道何时应考虑对 Pod 进行调度（例如，配额管理器）。

{{< mermaid >}}
graph LR;
  pod((新 Pod))-->queue
  subgraph 调度器
    queue(调度器队列)
    sched_cycle[/调度周期/]
    schedulable{可调度?}
    popout{弹出?}
    
    queue==>|PreEnqueue 检查|popout
    popout-->|是|sched_cycle
    popout==>|否|queue
    sched_cycle-->schedulable
    schedulable-->|否|queue
    subgraph note [控制 Pod 调度的开关]
    end
  end
  
 classDef plain fill:#ddd,stroke:#fff,stroke-width:1px,color:#000;
 classDef k8s fill:#326ce5,stroke:#fff,stroke-width:1px,color:#fff;
 classDef Scheduler fill:#fff,stroke:#bbb,stroke-width:2px,color:#326ce5;
 classDef note fill:#edf2ae,stroke:#fff,stroke-width:1px;
 classDef popout fill:#f96,stroke:#fff,stroke-width:1px;
 class queue,sched_cycle,schedulable k8s;
 class pod plain;
 class note note;
 class popout popout;
 class Scheduler Scheduler;
{{< /mermaid >}}

## 它是如何工作的？

总体而言，调度门控的工作方式与 Finalizer 非常相似。具有非空 `spec.schedulingGates` 字段的 Pod
的状态将显示为 `SchedulingGated`，并阻止被调度。请注意，添加多个门控是可以的，但它们都应该在创建 Pod
时添加（例如，你可以将它们作为规约的一部分或者通过变更性质的 Webhook）。

```
NAME       READY   STATUS            RESTARTS   AGE
test-pod   0/1     SchedulingGated   0          10s
```

要清除这些门控，你可以通过删除 Pod 的 `schedulingGates` 字段中的所有条目来更新 Pod。
不需要一次性移除所有门控，但是，只有当所有门控都移除后，调度器才会开始考虑对 Pod 进行调度。

在后台，调度门控以 PreEnqueue 调度器插件的方式实现，这是调度器框架的新扩展点，在每个调度周期开始时调用。

## 用例

此特性所支持的一个重要使用场景是动态配额管理。Kubernetes 支持[资源配额](/zh-cn/docs/concepts/policy/resource-quotas/)，
但是 API Server 会在你尝试创建 Pod 时强制执行配额。例如，如果一个新的 Pod 超过了 CPU 配额，它就会被拒绝。
API Server 不会对 Pod 进行排队；因此，无论是谁创建了 Pod，都需要不断尝试重新创建它。
这意味着在资源可用和 Pod 实际运行之间会有延迟，或者意味着由于不断尝试，会增加 API Server 和 Scheduler 的负载。

调度门控允许外部配额管理器解决 ResourceQuota 的上述限制。具体来说，
管理员可以（使用变更性质的 Webhook）为集群中创建的所有 Pod 添加一个
`example.com/quota-check` 调度门控。当存在用于启动 Pod 的配额时，管理器将移除此门控

## 接下来

要使用此特性，必须在 API Server 和调度器中启用 `PodScheduleingReadiness` 特性门控。
非常欢迎你对其进行测试并告诉我们（SIG Scheduling）你的想法！

## 附加资源

- Kubernetes 文档中的 [Pod 调度就绪态](/zh-cn/docs/concepts/scheduling-eviction/pod-scheduling-readiness/)
- [Kubernetes 增强提案](https://github.com/kubernetes/enhancements/blob/master/keps/sig-scheduling/3521-pod-scheduling-readiness/README.md)