---
title: Kubernetes 对象管理
content_type: concept
weight: 20
---

`kubectl` 命令行工具支持多种不同的方式来创建和管理 Kubernetes
{{< glossary_tooltip text="对象" term_id="object" >}}。
本文档概述了不同的方法。
阅读 [Kubectl book](https://kubectl.docs.kubernetes.io/zh/) 来了解 kubectl
管理对象的详细信息。


## 管理技巧

{{< warning >}}
应该只使用一种技术来管理 Kubernetes 对象。混合和匹配技术作用在同一对象上将导致未定义行为。
{{< /warning >}}

| 管理技术       | 作用于   | 建议的环境 | 支持的写者 | 学习难度 |
|----------------|----------|------------|------------|----------|
| 指令式命令     | 活跃对象 | 开发项目   | 1+         | 最低     |
| 指令式对象配置 | 单个文件 | 生产项目   | 1          | 中等     |
| 声明式对象配置 | 文件目录 | 生产项目   | 1+         | 最高     |

## 指令式命令

使用指令式命令时，用户可以在集群中的活动对象上进行操作。用户将操作传给
`kubectl` 命令作为参数或标志。

这是开始或者在集群中运行一次性任务的推荐方法。因为这个技术直接在活跃对象
上操作，所以它不提供以前配置的历史记录。

### 例子

通过创建 Deployment 对象来运行 nginx 容器的实例：

```sh
kubectl create deployment nginx --image nginx
```

### 权衡

与对象配置相比的优点：

- 命令用单个动词表示。
- 命令仅需一步即可对集群进行更改。

与对象配置相比的缺点：

- 命令不与变更审查流程集成。
- 命令不提供与更改关联的审核跟踪。
- 除了实时内容外，命令不提供记录源。
- 命令不提供用于创建新对象的模板。

## 指令式对象配置

在指令式对象配置中，kubectl 命令指定操作（创建，替换等），可选标志和
至少一个文件名。指定的文件必须包含 YAML 或 JSON 格式的对象的完整定义。

有关对象定义的详细信息，请查看
[API 参考](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/)。

{{< warning >}}
`replace` 指令式命令将现有规范替换为新提供的规范，并放弃对配置文件中
缺少的对象的所有更改。此方法不应与对象规约被独立于配置文件进行更新的
资源类型一起使用。比如类型为 `LoadBalancer` 的服务，它的 `externalIPs` 
字段就是独立于集群配置进行更新。
{{< /warning >}}

### 例子

创建配置文件中定义的对象：

```sh
kubectl create -f nginx.yaml
```

删除两个配置文件中定义的对象：

```sh
kubectl delete -f nginx.yaml -f redis.yaml
```

通过覆盖活动配置来更新配置文件中定义的对象：

```sh
kubectl replace -f nginx.yaml
```

### 权衡

与指令式命令相比的优点：

- 对象配置可以存储在源控制系统中，比如 Git。
- 对象配置可以与流程集成，例如在推送和审计之前检查更新。
- 对象配置提供了用于创建新对象的模板。

与指令式命令相比的缺点：

- 对象配置需要对对象架构有基本的了解。
- 对象配置需要额外的步骤来编写 YAML 文件。

与声明式对象配置相比的优点：

- 指令式对象配置行为更加简单易懂。
- 从 Kubernetes 1.5 版本开始，指令对象配置更加成熟。

与声明式对象配置相比的缺点：

- 指令式对象配置更适合文件，而非目录。
- 对活动对象的更新必须反映在配置文件中，否则会在下一次替换时丢失。

## 声明式对象配置

使用声明式对象配置时，用户对本地存储的对象配置文件进行操作，但是用户
未定义要对该文件执行的操作。
`kubectl` 会自动检测每个文件的创建、更新和删除操作。
这使得配置可以在目录上工作，根据目录中配置文件对不同的对象执行不同的操作。

{{< note >}}
声明式对象配置保留其他编写者所做的修改，即使这些更改并未合并到对象配置文件中。
可以通过使用 `patch` API 操作仅写入观察到的差异，而不是使用 `replace` API
操作来替换整个对象配置来实现。
{{< /note >}}

### 例子

处理 `configs` 目录中的所有对象配置文件，创建并更新活跃对象。
可以首先使用 `diff` 子命令查看将要进行的更改，然后在进行应用：

```sh
kubectl diff -f configs/
kubectl apply -f configs/
```

递归处理目录：

```sh
kubectl diff -R -f configs/
kubectl apply -R -f configs/
```

### 权衡

与指令式对象配置相比的优点：

- 对活动对象所做的更改即使未合并到配置文件中，也会被保留下来。
- 声明性对象配置更好地支持对目录进行操作并自动检测每个文件的操作类型（创建，修补，删除）。

与指令式对象配置相比的缺点：

- 声明式对象配置难于调试并且出现异常时结果难以理解。
- 使用 diff 产生的部分更新会创建复杂的合并和补丁操作。

## {{% heading "whatsnext" %}}


- [使用指令式命令管理 Kubernetes 对象](/zh-cn/docs/tasks/manage-kubernetes-objects/imperative-command/)
- [使用配置文件对 Kubernetes 对象进行命令式管理](/zh-cn/docs/tasks/manage-kubernetes-objects/imperative-config/)
- [使用配置文件对 Kubernetes 对象进行声明式管理](/zh-cn/docs/tasks/manage-kubernetes-objects/declarative-config/)
- [使用 Kustomize 对 Kubernetes 对象进行声明式管理](/zh-cn/docs/tasks/manage-kubernetes-objects/kustomization/)
- [Kubectl 命令参考](/docs/reference/generated/kubectl/kubectl-commands/)
- [Kubectl Book](https://kubectl.docs.kubernetes.io/zh/)
- [Kubernetes API 参考](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/)

