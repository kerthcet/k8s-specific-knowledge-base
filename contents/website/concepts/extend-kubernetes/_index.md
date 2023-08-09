---
title: 扩展 Kubernetes
weight: 999  # 这一节应放在最后
description: 改变你的 Kubernetes 集群的行为的若干方法。
feature:
  title: 为扩展性设计
  description: >
    无需更改上游源码即可扩展你的 Kubernetes 集群。
content_type: concept
no_list: true
---


Kubernetes 是高度可配置且可扩展的。因此，大多数情况下，
你不需要派生自己的 Kubernetes 副本或者向项目代码提交补丁。

本指南描述定制 Kubernetes 的可选方式。主要针对的读者是希望了解如何针对自身工作环境需要来调整
Kubernetes 的{{< glossary_tooltip text="集群管理者" term_id="cluster-operator" >}}。
对于那些充当{{< glossary_tooltip text="平台开发人员" term_id="platform-developer" >}}的开发人员或
Kubernetes 项目的{{< glossary_tooltip text="贡献者" term_id="contributor" >}}而言，
他们也会在本指南中找到有用的介绍信息，了解系统中存在哪些扩展点和扩展模式，
以及它们所附带的各种权衡和约束等等。

定制化的方法主要可分为[配置](#configuration)和[扩展](#extensions)两种。
前者主要涉及更改命令行参数、本地配置文件或者 API 资源；
后者则需要额外运行一些程序、网络服务或两者。
本文主要关注**扩展**。

## 配置   {#configuration}

**配置文件**和**命令参数**的说明位于在线文档的[参考](/zh-cn/docs/reference/)一节，
每个可执行文件一个页面：

* [`kube-apiserver`](/zh-cn/docs/reference/command-line-tools-reference/kube-apiserver/)
* [`kube-controller-manager`](/zh-cn/docs/reference/command-line-tools-reference/kube-controller-manager/)
* [`kube-scheduler`](/zh-cn/docs/reference/command-line-tools-reference/kube-scheduler/)
* [`kubelet`](/zh-cn/docs/reference/command-line-tools-reference/kubelet/)
* [`kube-proxy`](/zh-cn/docs/reference/command-line-tools-reference/kube-proxy/)

在托管的 Kubernetes 服务中或者受控安装的发行版本中，命令参数和配置文件不总是可以修改的。
即使它们是可修改的，通常其修改权限也仅限于集群操作员。
此外，这些内容在将来的 Kubernetes 版本中很可能发生变化，设置新参数或配置文件可能需要重启进程。
有鉴于此，应该在没有其他替代方案时才会使用这些命令参数和配置文件。

诸如 [ResourceQuota](/zh-cn/docs/concepts/policy/resource-quotas/)、
[NetworkPolicy](/zh-cn/docs/concepts/services-networking/network-policies/)
和基于角色的访问控制（[RBAC](/zh-cn/docs/reference/access-authn-authz/rbac/)）
等**内置策略 API** 都是以声明方式配置策略选项的内置 Kubernetes API。
即使在托管的 Kubernetes 服务和受控的 Kubernetes 安装环境中，API 通常也是可用的。
内置策略 API 遵循与 Pod 这类其他 Kubernetes 资源相同的约定。
当你使用[稳定版本](/zh-cn/docs/reference/using-api/#api-versioning)的策略 API，
它们与其他 Kubernetes API 一样，采纳的是一种[预定义的支持策略](/zh-cn/docs/reference/using-api/deprecation-policy/)。
出于以上原因，在条件允许的情况下，基于策略 API 的方案应该优先于**配置文件**和**命令参数**。

## 扩展    {#extensions}

扩展（Extensions）是一些扩充 Kubernetes 能力并与之深度集成的软件组件。
它们调整 Kubernetes 的工作方式使之支持新的类型和新的硬件种类。

大多数集群管理员会使用一种托管的 Kubernetes 服务或者其某种发行版本。
这类集群通常都预先安装了扩展。因此，大多数 Kubernetes 用户不需要安装扩展，
至于需要自己编写新的扩展的情况就更少了。

### 扩展模式   {#extension-patterns}

Kubernetes 从设计上即支持通过编写客户端程序来将其操作自动化。
任何能够对 Kubernetes API 发出读写指令的程序都可以提供有用的自动化能力。
**自动化组件**可以运行在集群上，也可以运行在集群之外。
通过遵从本文中的指南，你可以编写高度可用的、运行稳定的自动化组件。
自动化组件通常可以用于所有 Kubernetes 集群，包括托管的集群和受控的安装环境。

编写客户端程序有一种特殊的{{< glossary_tooltip term_id="controller" text="控制器（Controller）" >}}模式，
能够与 Kubernetes 很好地协同工作。控制器通常会读取某个对象的 `.spec`，或许还会执行一些操作，
之后更新对象的 `.status`。

控制器是 Kubernetes API 的客户端。当 Kubernetes 充当客户端且调用某远程服务时，
Kubernetes 将此称作 **Webhook**。该远程服务称作 **Webhook 后端**。
与定制的控制器相似，Webhook 也会引入失效点（Point of Failure）。

{{< note >}}
在 Kubernetes 之外，“Webhook” 这个词通常是指一种异步通知机制，
其中 Webhook 调用将用作对另一个系统或组件的单向通知。
在 Kubernetes 生态系统中，甚至同步的 HTTP 调用也经常被描述为 “Webhook”。
{{< /note >}}

在 Webhook 模型中，Kubernetes 向远程服务发起网络请求。
在另一种称作**可执行文件插件（Binary Plugin）** 模型中，Kubernetes 执行某个可执行文件（程序）。
这些可执行文件插件由 kubelet（例如，[CSI 存储插件](https://kubernetes-csi.github.io/docs/)和
[CNI 网络插件](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)）
和 kubectl 使用。

### 扩展点   {#extension-points}

下图展示了 Kubernetes 集群中的这些扩展点及其访问集群的客户端。


{{< figure src="/docs/concepts/extend-kubernetes/extension-points.png"
    alt="用符号表示的七个编号的 Kubernetes 扩展点"
    class="diagram-large" caption="Kubernetes 扩展点" >}}

#### 图示要点   {#key-to-the-figure}

1. 用户通常使用 `kubectl` 与 Kubernetes API 交互。
   [插件](#client-extensions)定制客户端的行为。
   有一些通用的扩展可以应用到不同的客户端，还有一些特定的方式可以扩展 `kubectl`。

2. API 服务器处理所有请求。API 服务器中的几种扩展点能够使用户对请求执行身份认证、
   基于其内容阻止请求、编辑请求内容、处理删除操作等等。
   这些扩展点在 [API 访问扩展](#api-access-extensions)节详述。

3. API 服务器能提供各种类型的**资源（Resources）** 服务。
   诸如 `pods` 的**内置资源类型**是由 Kubernetes 项目所定义的，无法改变。
   请查阅 [API 扩展](#api-extensions)了解如何扩展 Kubernetes API。

4. Kubernetes 调度器负责[决定](/zh-cn/docs/concepts/scheduling-eviction/assign-pod-node/)
   Pod 要放置到哪些节点上执行。有几种方式来扩展调度行为，这些方法将在[调度器扩展](#scheduling-extensions)节中展开说明。

5. Kubernetes 中的很多行为都是通过称为{{< glossary_tooltip term_id="controller" text="控制器（Controller）" >}}的程序来实现的，
   这些程序也都是 API 服务器的客户端。控制器常常与定制资源结合使用。
   进一步了解请查阅[结合使用新的 API 与自动化组件](#combining-new-apis-with-automation)和[更改内置资源](#changing-built-in-resources)。

6. Kubelet 运行在各个服务器（节点）上，帮助 Pod 展现为虚拟的服务器并在集群网络中拥有自己的 IP。
   [网络插件](#network-plugins)使得 Kubernetes 能够采用不同实现技术来连接 Pod 网络。

7. 你可以使用[设备插件](#device-plugins)集成定制硬件或其他专用的节点本地设施，
   使得这些设施可用于集群中运行的 Pod。Kubelet 包括了对使用设备插件的支持。

   kubelet 也会为 Pod 及其容器增加或解除{{< glossary_tooltip text="卷" term_id="volume" >}}的挂载。
   你可以使用[存储插件](#storage-plugins)增加对新存储类别和其他卷类型的支持。

#### 扩展点选择流程图   {#extension-flowchart}

如果你无法确定从何处入手，下面的流程图可能对你有些帮助。
注意，某些方案可能需要同时采用几种类型的扩展。

{{< figure src="/zh-cn/docs/concepts/extend-kubernetes/flowchart.png"
    alt="附带使用场景问题和实现指南的流程图。绿圈表示是；红圈表示否。"
    class="diagram-large" caption="选择一个扩展方式的流程图指导" >}}

---

## 客户端扩展   {#client-extensions}

kubectl 所用的插件是单独的二进制文件，用于添加或替换特定子命令的行为。
`kubectl` 工具还可以与[凭据插件](/zh-cn/docs/reference/access-authn-authz/authentication/#client-go-credential-plugins)集成。
这些扩展只影响单个用户的本地环境，因此不能强制执行站点范围的策略。

如果你要扩展 `kubectl` 工具，请阅读[用插件扩展 kubectl](/zh-cn/docs/tasks/extend-kubectl/kubectl-plugins/)。

## API 扩展  {#api-extensions}

### 定制资源对象   {#custom-resource-definitions}

如果你想要定义新的控制器、应用配置对象或者其他声明式 API，并且使用 Kubernetes
工具（如 `kubectl`）来管理它们，可以考虑向 Kubernetes 添加**定制资源**。

关于定制资源的更多信息，可参见[定制资源概念指南](/zh-cn/docs/concepts/extend-kubernetes/api-extension/custom-resources/)。

### API 聚合层   {#api-aggregation-layer}

你可以使用 Kubernetes 的
[API 聚合层](/zh-cn/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)将
Kubernetes API 与其他服务集成，例如[指标](/zh-cn/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/)。

### 结合使用新 API 与自动化组件 {#combinding-new-apis-with-automation}

定制资源 API 与控制回路的组合称作{{< glossary_tooltip term_id="controller" text="控制器" >}}模式。
如果你的控制器代替人工操作员根据所需状态部署基础设施，那么控制器也可以遵循
{{<glossary_tooltip text="Operator 模式" term_id="operator-pattern" >}}。
Operator 模式用于管理特定的应用；通常，这些应用需要维护状态并需要仔细考虑状态的管理方式。

你还可以创建自己的定制 API 和控制回路来管理其他资源（例如存储）或定义策略（例如访问控制限制）。

### 更改内置资源   {#changing-built-in-resources}

当你通过添加定制资源来扩展 Kubernetes 时，所添加的资源总是会被放在一个新的 API 组中。
你不可以替换或更改现有的 API 组。添加新的 API 不会直接让你影响现有
API（如 Pod）的行为，不过 **API 访问扩展**能够实现这点。

## API 访问扩展    {#api-access-extensions}

当请求到达 Kubernetes API 服务器时，首先要经过**身份认证**，之后是**鉴权**操作，
再之后要经过若干类型的**准入控制**（某些请求实际上未通过身份认证，需要特殊处理）。
参见[控制 Kubernetes API 访问](/zh-cn/docs/concepts/security/controlling-access/)以了解此流程的细节。

Kubernetes 身份认证/授权流程中的每个步骤都提供了扩展点。

### 身份认证    {#authentication}

[身份认证](/zh-cn/docs/reference/access-authn-authz/authentication/)负责将所有请求中的头部或证书映射到发出该请求的客户端的用户名。

Kubernetes 提供若干内置的身份认证方法。它也可以运行在某种身份认证代理的后面，
并且可以将来自 `Authorization:` 头部的令牌发送到某个远程服务
（[认证 Webhook](/zh-cn/docs/reference/access-authn-authz/authentication/#webhook-token-authentication)
来执行验证操作，以备内置方法无法满足你的要求。

### 鉴权    {#authorization}

[鉴权](/zh-cn/docs/reference/access-authn-authz/authorization/)操作负责确定特定的用户是否可以读、写 API
资源或对其执行其他操作。此操作仅在整个资源集合的层面进行。
换言之，它不会基于对象的特定字段作出不同的判决。

如果内置的鉴权选项无法满足你的需要，
你可以使用[鉴权 Webhook](/zh-cn/docs/reference/access-authn-authz/webhook/) 来调用用户提供的代码，
执行定制的鉴权决定。

### 动态准入控制  {#dynamic-admission-control}

请求的鉴权操作结束之后，如果请求的是写操作，
还会经过[准入控制](/zh-cn/docs/reference/access-authn-authz/admission-controllers/)处理步骤。
除了内置的处理步骤，还存在一些扩展点：

* [镜像策略 Webhook](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#imagepolicywebhook)
  能够限制容器中可以运行哪些镜像。
* 为了执行任意的准入控制决定，
  可以使用一种通用的[准入 Webhook](/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/#admission-webhooks)
  机制。这类准入 Webhook 可以拒绝创建或更新请求。
  一些准入 Webhook 会先修改传入的请求数据，才会由 Kubernetes 进一步处理这些传入请求数据。

## 基础设施扩展    {#infrastructure-extensions}

### 设备插件   {#device-plugins}

**设备插件**允许一个节点通过[设备插件](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)发现新的
Node 资源（除了内置的类似 CPU 和内存这类资源之外）。

### 存储插件  {#storage-plugins}

{{< glossary_tooltip text="容器存储接口" term_id="csi" >}} (CSI) 插件提供了一种扩展
Kubernetes 的方式使其支持新类别的卷。
这些卷可以由持久的外部存储提供支持，可以提供临时存储，还可以使用文件系统范型为信息提供只读接口。

Kubernetes 还包括对 [FlexVolume](/zh-cn/docs/concepts/storage/volumes/#flexvolume-deprecated)
插件的支持，该插件自 Kubernetes v1.23 起被弃用（被 CSI 替代）。

FlexVolume 插件允许用户挂载 Kubernetes 本身不支持的卷类型。
当你运行依赖于 FlexVolume 存储的 Pod 时，kubelet 会调用一个二进制插件来挂载该卷。
归档的 [FlexVolume](https://git.k8s.io/design-proposals-archive/storage/flexvolume-deployment.md)
设计提案对此方法有更多详细说明。

[Kubernetes 存储供应商的卷插件 FAQ](https://github.com/kubernetes/community/blob/master/sig-storage/volume-plugin-faq.md#kubernetes-volume-plugin-faq-for-storage-vendors)
包含了有关存储插件的通用信息。

### 网络插件   {#network-plugins}

你的 Kubernetes 集群需要一个**网络插件**才能拥有一个正常工作的 Pod 网络，
才能支持 Kubernetes 网络模型的其他方面。

[网络插件](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)可以让
Kubernetes 使用不同的网络拓扑和技术。

### Kubelet 镜像凭据提供程序插件   {#kubelet-image-credential-provider-plugins}

{{< feature-state for_k8s_version="v1.26" state="stable" >}}
Kubelet 镜像凭据提供程序是 Kubelet 动态检索镜像仓库凭据的插件。
当你从与配置匹配的容器镜像仓库中拉取镜像时，这些凭据将被使用。

这些插件可以与外部服务通信或使用本地文件来获取凭据。这样，kubelet
就不需要为每个仓库都设置静态凭据，并且可以支持各种身份验证方法和协议。

有关插件配置的详细信息，请参阅
[配置 kubelet 镜像凭据提供程序](/zh-cn/docs/tasks/administer-cluster/kubelet-credential-provider/)。

## 调度扩展   {#scheduling-extensions}

调度器是一种特殊的控制器，负责监视 Pod 变化并将 Pod 分派给节点。
默认的调度器可以被整体替换掉，同时继续使用其他 Kubernetes 组件。
或者也可以在同一时刻使用[多个调度器](/zh-cn/docs/tasks/extend-kubernetes/configure-multiple-schedulers/)。

这是一项非同小可的任务，几乎绝大多数 Kubernetes
用户都会发现其实他们不需要修改调度器。

你可以控制哪些[调度插件](/zh-cn/docs/reference/scheduling/config/#scheduling-plugins)处于激活状态，
或将插件集关联到名字不同的[调度器配置文件](/zh-cn/docs/reference/scheduling/config/#multiple-profiles)上。
你还可以编写自己的插件，与一个或多个 kube-scheduler
的[扩展点](/zh-cn/docs/concepts/scheduling-eviction/scheduling-framework/#extension-points)集成。

最后，内置的 `kube-scheduler` 组件支持
[Webhook](https://git.k8s.io/design-proposals-archive/scheduling/scheduler_extender.md)，
从而允许远程 HTTP 后端（调度器扩展）来为 kube-scheduler 选择的 Pod 所在节点执行过滤和优先排序操作。

{{< note >}}
你只能使用调度器扩展程序 Webhook 来影响节点过滤和节点优先排序；
其他扩展点无法通过集成 Webhook 获得。
{{< /note >}}

## {{% heading "whatsnext" %}}

* 进一步了解基础设施扩展
  * [设备插件](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)
  * [网络插件](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
  * CSI [存储插件](https://kubernetes-csi.github.io/docs/)
* 进一步了解 [kubectl 插件](/zh-cn/docs/tasks/extend-kubectl/kubectl-plugins/)
* 进一步了解[定制资源](/zh-cn/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
* 进一步了解[扩展 API 服务器](/zh-cn/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)
* 进一步了解[动态准入控制](/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/)
* 进一步了解 [Operator 模式](/zh-cn/docs/concepts/extend-kubernetes/operator/)

