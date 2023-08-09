---
title: 部署和访问 Kubernetes 仪表板（Dashboard）
content_type: concept
weight: 10
card:
  name: tasks
  weight: 30
  title: 使用 Web 界面 Dashboard
  description: 部署并访问 Web 界面（Kubernetes 仪表板）。
---


Dashboard 是基于网页的 Kubernetes 用户界面。
你可以使用 Dashboard 将容器应用部署到 Kubernetes 集群中，也可以对容器应用排错，还能管理集群资源。
你可以使用 Dashboard 获取运行在集群中的应用的概览信息，也可以创建或者修改 Kubernetes 资源
（如 Deployment，Job，DaemonSet 等等）。
例如，你可以对 Deployment 实现弹性伸缩、发起滚动升级、重启 Pod 或者使用向导创建新的应用。

Dashboard 同时展示了 Kubernetes 集群中的资源状态信息和所有报错信息。

![Kubernetes Dashboard UI](/images/docs/ui-dashboard.png)


## 部署 Dashboard UI   {#deploying-the-dashboard-ui}
默认情况下不会部署 Dashboard。可以通过以下命令部署：

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

## 访问 Dashboard 用户界面   {#accessing-the-dashboard-ui}

为了保护你的集群数据，默认情况下，Dashboard 会使用最少的 RBAC 配置进行部署。
当前，Dashboard 仅支持使用 Bearer 令牌登录。
要为此样本演示创建令牌，你可以按照
[创建示例用户](https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md)
上的指南进行操作。

{{< warning >}}
在教程中创建的样本用户将具有管理特权，并且仅用于教育目的。
{{< /warning >}}

### 命令行代理   {#command-line-proxy}

你可以使用 `kubectl` 命令行工具来启用 Dashboard 访问，命令如下：

```
kubectl proxy
```

kubectl 会使得 Dashboard 可以通过 [http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/) 访问。

UI _只能_ 通过执行这条命令的机器进行访问。更多选项参见 `kubectl proxy --help`。

{{< note >}}
Kubeconfig 身份验证方法**不**支持外部身份提供程序或基于 x509 证书的身份验证。
{{< /note >}}

## 欢迎界面   {#welcome-view}

当访问空集群的 Dashboard 时，你会看到欢迎界面。
页面包含一个指向此文档的链接，以及一个用于部署第一个应用程序的按钮。
此外，你可以看到在默认情况下有哪些默认系统应用运行在 `kube-system`
[名字空间](/zh-cn/docs/tasks/administer-cluster/namespaces/) 中，比如 Dashboard 自己。

![Kubernetes Dashboard 欢迎页面](/images/docs/ui-dashboard-zerostate.png)

## 部署容器化应用   {#deploying-containerized-applications}

通过一个简单的部署向导，你可以使用 Dashboard 将容器化应用作为一个 Deployment 和可选的
Service 进行创建和部署。你可以手工指定应用的详细配置，或者上传一个包含应用配置的 YAML
或 JSON _清单_文件。

点击任何页面右上角的 **CREATE** 按钮以开始。

### 指定应用的详细配置   {#specifying-application-details}

部署向导需要你提供以下信息：

- **应用名称**（必填）：应用的名称。内容为 `应用名称` 的
  [标签](/zh-cn/docs/concepts/overview/working-with-objects/labels/)
  会被添加到任何将被部署的 Deployment 和 Service。

  在选定的 Kubernetes [名字空间](/zh-cn/docs/tasks/administer-cluster/namespaces/) 中，
  应用名称必须唯一。必须由小写字母开头，以数字或者小写字母结尾，
  并且只含有小写字母、数字和中划线（-）。小于等于24个字符。开头和结尾的空格会被忽略。

- **容器镜像**（必填）：公共镜像仓库上的 Docker
  [容器镜像](/zh-cn/docs/concepts/containers/images/) 或者私有镜像仓库
  （通常是 Google Container Registry 或者 Docker Hub）的 URL。容器镜像参数说明必须以冒号结尾。

- **Pod 的数量**（必填）：你希望应用程序部署的 Pod 的数量。值必须为正整数。

  系统会创建一个 [Deployment](/zh-cn/docs/concepts/workloads/controllers/deployment/)
  以保证集群中运行期望的 Pod 数量。

- **服务**（可选）：对于部分应用（比如前端），你可能想对外暴露一个
  [Service](/zh-cn/docs/concepts/services-networking/service/)，这个 Service
  可能用的是集群之外的公网 IP 地址（外部 Service）。

  {{< note >}}
  对于外部服务，你可能需要开放一个或多个端口才行。
  {{< /note >}}

  其它只能对集群内部可见的 Service 称为内部 Service。
  
  不管哪种 Service 类型，如果你选择创建一个 Service，而且容器在一个端口上开启了监听（入向的），
  那么你需要定义两个端口。创建的 Service 会把（入向的）端口映射到容器可见的目标端口。
  该 Service 会把流量路由到你部署的 Pod。支持 TCP 协议和 UDP 协议。
  这个 Service 的内部 DNS 解析名就是之前你定义的应用名称的值。

如果需要，你可以打开 **Advanced Options** 部分，这里你可以定义更多设置：

- **描述**：这里你输入的文本会作为一个
  [注解](/zh-cn/docs/concepts/overview/working-with-objects/annotations/)
  添加到 Deployment，并显示在应用的详细信息中。

- **标签**：应用默认使用的
  [标签](/zh-cn/docs/concepts/overview/working-with-objects/labels/) 是应用名称和版本。
  你可以为 Deployment、Service（如果有）定义额外的标签，比如 release（版本）、
  environment（环境）、tier（层级）、partition（分区） 和 release track（版本跟踪）。

  例子：

  ```conf
  release=1.0
  tier=frontend
  environment=pod
  track=stable
  ```

- **名字空间**：Kubernetes 支持多个虚拟集群依附于同一个物理集群。
  这些虚拟集群被称为
  [名字空间](/zh-cn/docs/tasks/administer-cluster/namespaces/)，
  可以让你将资源划分为逻辑命名的组。

  Dashboard 通过下拉菜单提供所有可用的名字空间，并允许你创建新的名字空间。
  名字空间的名称最长可以包含 63 个字母或数字和中横线（-），但是不能包含大写字母。

  名字空间的名称不能只包含数字。如果名字被设置成一个数字，比如 10，pod 就

  在名字空间创建成功的情况下，默认会使用新创建的名字空间。如果创建失败，那么第一个名字空间会被选中。

- **镜像拉取 Secret**：如果要使用私有的 Docker 容器镜像，需要拉取
  [Secret](/zh-cn/docs/concepts/configuration/secret/) 凭证。

  Dashboard 通过下拉菜单提供所有可用的 Secret，并允许你创建新的 Secret。
  Secret 名称必须遵循 DNS 域名语法，比如 `new.image-pull.secret`。
  Secret 的内容必须是 base64 编码的，并且在一个
  [`.dockercfg`](/zh-cn/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod)
  文件中声明。Secret 名称最大可以包含 253 个字符。
  
  在镜像拉取 Secret 创建成功的情况下，默认会使用新创建的 Secret。
  如果创建失败，则不会使用任何 Secret。

- **CPU 需求（核数）** 和 **内存需求（MiB）**：你可以为容器定义最小的
  [资源限制](/zh-cn/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)。
  默认情况下，Pod 没有 CPU 和内存限制。

- **运行命令**和**运行命令参数**：默认情况下，你的容器会运行 Docker 镜像的默认
  [入口命令](/zh-cn/docs/tasks/inject-data-application/define-command-argument-container/)。
  你可以使用 command 选项覆盖默认值。

- **以特权模式运行**：这个设置决定了在
  [特权容器](/zh-cn/docs/concepts/workloads/pods/#privileged-mode-for-containers)
  中运行的进程是否像主机中使用 root 运行的进程一样。
  特权容器可以使用诸如操纵网络堆栈和访问设备的功能。

- **环境变量**：Kubernetes 通过
  [环境变量](/zh-cn/docs/tasks/inject-data-application/environment-variable-expose-pod-information/)
  暴露 Service。你可以构建环境变量，或者将环境变量的值作为参数传递给你的命令。
  它们可以被应用用于查找 Service。值可以通过  `$(VAR_NAME)` 语法关联其他变量。

### 上传 YAML 或者 JSON 文件   {#uploading-a-yaml-or-json-file}

Kubernetes 支持声明式配置。所有的配置都存储在清单文件
（YAML 或者 JSON 配置文件）中。这些
清单使用 Kubernetes [API](/zh-cn/docs/concepts/overview/kubernetes-api/) 定义的资源模式。

作为一种替代在部署向导中指定应用详情的方式，你可以在一个或多个清单文件中定义应用，并且使用
Dashboard 上传文件。

## 使用 Dashboard   {#using-dashboard}

以下各节描述了 Kubernetes Dashboard UI 视图；包括它们提供的内容，以及怎么使用它们。

### 导航   {#navigation}

当在集群中定义 Kubernetes 对象时，Dashboard 会在初始视图中显示它们。
默认情况下只会显示 _默认_ 名字空间中的对象，可以通过更改导航栏菜单中的名字空间筛选器进行改变。

Dashboard 展示大部分 Kubernetes 对象，并将它们分组放在几个菜单类别中。

#### 管理概述   {#admin-overview}

集群和名字空间管理的视图，Dashboard 会列出节点、名字空间和持久卷，并且有它们的详细视图。
节点列表视图包含从所有节点聚合的 CPU 和内存使用的度量值。
详细信息视图显示了一个节点的度量值，它的规格、状态、分配的资源、事件和这个节点上运行的 Pod。

#### 负载   {#workloads}

显示选中的名字空间中所有运行的应用。
视图按照负载类型（例如：Deployment、ReplicaSet、StatefulSet）罗列应用，并且每种负载都可以单独查看。
列表总结了关于负载的可执行信息，比如一个 ReplicaSet 的就绪状态的 Pod 数量，或者目前一个 Pod 的内存用量。

工作负载的详情视图展示了对象的状态、详细信息和相互关系。
例如，ReplicaSet 所控制的 Pod，或者 Deployment 所关联的新 ReplicaSet 和
HorizontalPodAutoscalers。

#### 服务   {#services}

展示允许暴露给外网服务和允许集群内部发现的 Kubernetes 资源。
因此，Service 和 Ingress 视图展示他们关联的 Pod、给集群连接使用的内部端点和给外部用户使用的外部端点。

#### 存储   {#storage}

存储视图展示持久卷申领（PVC）资源，这些资源被应用程序用来存储数据。

#### ConfigMap 和 Secret {#config-maps-and-secrets}

展示的所有 Kubernetes 资源是在集群中运行的应用程序的实时配置。
通过这个视图可以编辑和管理配置对象，并显示那些默认隐藏的 Secret。

#### 日志查看器   {#logs-viewer}

Pod 列表和详细信息页面可以链接到 Dashboard 内置的日志查看器。
查看器可以深入查看属于同一个 Pod 的不同容器的日志。

![日志浏览](/images/docs/ui-dashboard-logs-view.png)

## {{% heading "whatsnext" %}}

更多信息，参见 [Kubernetes Dashboard 项目页面](https://github.com/kubernetes/dashboard).
