---
title: 资源装箱
content_type: concept
weight: 80
---


在 kube-scheduler 的[调度插件](/zh-cn/docs/reference/scheduling/config/#scheduling-plugins)
`NodeResourcesFit` 中存在两种支持资源装箱（bin packing）的策略：`MostAllocated` 和
`RequestedToCapacityRatio`。


## 使用 MostAllocated 策略启用资源装箱   {#enabling-bin-packing-using-mostallocated-strategy}

`MostAllocated` 策略基于资源的利用率来为节点计分，优选分配比率较高的节点。
针对每种资源类型，你可以设置一个权重值以改变其对节点得分的影响。

要为插件 `NodeResourcesFit` 设置 `MostAllocated` 策略，
可以使用一个类似于下面这样的[调度器配置](/zh-cn/docs/reference/scheduling/config/)：

```yaml
apiVersion: kubescheduler.config.k8s.io/v1beta3
kind: KubeSchedulerConfiguration
profiles:
- pluginConfig:
  - args:
      scoringStrategy:
        resources:
        - name: cpu
          weight: 1
        - name: memory
          weight: 1
        - name: intel.com/foo
          weight: 3
        - name: intel.com/bar
          weight: 3
        type: MostAllocated
    name: NodeResourcesFit
```

要进一步了解其它参数及其默认配置，请参阅
[`NodeResourcesFitArgs`](/zh-cn/docs/reference/config-api/kube-scheduler-config.v1beta3/#kubescheduler-config-k8s-io-v1beta3-NodeResourcesFitArgs)
的 API 文档。

## 使用 RequestedToCapacityRatio 策略来启用资源装箱 {#enabling-bin-packing-using-requestedtocapacityratio}

`RequestedToCapacityRatio` 策略允许用户基于请求值与容量的比率，针对参与节点计分的每类资源设置权重。
这一策略使得用户可以使用合适的参数来对扩展资源执行装箱操作，进而提升大规模集群中稀有资源的利用率。
此策略根据所分配资源的一个配置函数来评价节点。
`NodeResourcesFit` 计分函数中的 `RequestedToCapacityRatio` 可以通过字段
[scoringStrategy](/zh-cn/docs/reference/config-api/kube-scheduler-config.v1beta3/#kubescheduler-config-k8s-io-v1beta3-ScoringStrategy)
来控制。
在 `scoringStrategy` 字段中，你可以配置两个参数：`requestedToCapacityRatio`
和 `resources`。`requestedToCapacityRatio` 参数中的 `shape`
设置使得用户能够调整函数的算法，基于 `utilization` 和 `score` 值计算最少请求或最多请求。
`resources` 参数中包含计分过程中需要考虑的资源的 `name`，以及用来设置每种资源权重的 `weight`。

下面是一个配置示例，使用 `requestedToCapacityRatio` 字段为扩展资源 `intel.com/foo`
和 `intel.com/bar` 设置装箱行为：

```yaml
apiVersion: kubescheduler.config.k8s.io/v1beta3
kind: KubeSchedulerConfiguration
profiles:
- pluginConfig:
  - args:
      scoringStrategy:
        resources:
        - name: intel.com/foo
          weight: 3
        - name: intel.com/bar
          weight: 3
        requestedToCapacityRatio:
          shape:
          - utilization: 0
            score: 0
          - utilization: 100
            score: 10
        type: RequestedToCapacityRatio
    name: NodeResourcesFit
```

使用 kube-scheduler 标志 `--config=/path/to/config/file` 
引用 `KubeSchedulerConfiguration` 文件，可以将配置传递给调度器。

要进一步了解其它参数及其默认配置，可以参阅
[`NodeResourcesFitArgs`](/zh-cn/docs/reference/config-api/kube-scheduler-config.v1beta3/#kubescheduler-config-k8s-io-v1beta3-NodeResourcesFitArgs)
的 API 文档。

### 调整计分函数    {#tuning-the-score-function}

`shape` 用于指定 `RequestedToCapacityRatio` 函数的行为。

```yaml
shape:
  - utilization: 0
    score: 0
  - utilization: 100
    score: 10
```

上面的参数在 `utilization` 为 0% 时给节点评分为 0，在 `utilization` 为
100% 时给节点评分为 10，因此启用了装箱行为。
要启用最少请求（least requested）模式，必须按如下方式反转得分值。

```yaml
shape:
  - utilization: 0
    score: 10
  - utilization: 100
    score: 0
```

`resources` 是一个可选参数，默认值为：

```yaml
resources:
  - name: cpu
    weight: 1
  - name: memory
    weight: 1
```

它可以像下面这样用来添加扩展资源：

```yaml
resources:
  - name: intel.com/foo
    weight: 5
  - name: cpu
    weight: 3
  - name: memory
    weight: 1
```

`weight` 参数是可选的，如果未指定，则设置为 1。
同时，`weight` 不能设置为负值。

### 节点容量分配的评分   {#node-scoring-for-capacity-allocation}

本节适用于希望了解此功能的内部细节的人员。
以下是如何针对给定的一组值来计算节点得分的示例。

请求的资源：

```
intel.com/foo : 2
memory: 256MB
cpu: 2
```

资源权重：

```
intel.com/foo : 5
memory: 1
cpu: 3
```

```
FunctionShapePoint {{0, 0}, {100, 10}}
```

节点 1 配置：

```
可用：
  intel.com/foo: 4
  memory: 1 GB
  cpu: 8

已用：
  intel.com/foo: 1
  memory: 256MB
  cpu: 1
```

节点得分：

```
intel.com/foo  = resourceScoringFunction((2+1),4)
               = (100 - ((4-3)*100/4)
               = (100 - 25)
               = 75                       # requested + used = 75% * available
               = rawScoringFunction(75)
               = 7                        # floor(75/10)

memory         = resourceScoringFunction((256+256),1024)
               = (100 -((1024-512)*100/1024))
               = 50                       # requested + used = 50% * available
               = rawScoringFunction(50)
               = 5                        # floor(50/10)

cpu            = resourceScoringFunction((2+1),8)
               = (100 -((8-3)*100/8))
               = 37.5                     # requested + used = 37.5% * available
               = rawScoringFunction(37.5)
               = 3                        # floor(37.5/10)

NodeScore   =  ((7 * 5) + (5 * 1) + (3 * 3)) / (5 + 1 + 3)
            =  5
```

节点 2 配置：

```
可用：
  intel.com/foo: 8
  memory: 1GB
  cpu: 8

已用：
  intel.com/foo: 2
  memory: 512MB
  cpu: 6
```

节点得分：

```
intel.com/foo  = resourceScoringFunction((2+2),8)
               = (100 - ((8-4)*100/8)
               = (100 - 50)
               = 50
               = rawScoringFunction(50)
               = 5

memory         = resourceScoringFunction((256+512),1024)
               = (100 -((1024-768)*100/1024))
               = 75
               = rawScoringFunction(75)
               = 7

cpu            = resourceScoringFunction((2+6),8)
               = (100 -((8-8)*100/8))
               = 100
               = rawScoringFunction(100)
               = 10

NodeScore   =  ((5 * 5) + (7 * 1) + (10 * 3)) / (5 + 1 + 3)
            =  7
```

## {{% heading "whatsnext" %}}

- 继续阅读[调度器框架](/zh-cn/docs/concepts/scheduling-eviction/scheduling-framework/)
- 继续阅读[调度器配置](/zh-cn/docs/reference/scheduling/config/)
