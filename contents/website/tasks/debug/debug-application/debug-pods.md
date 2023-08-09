---
title: 调试 Pod
content_type: task
weight: 10
---


本指南帮助用户调试那些部署到 Kubernetes 上后没有正常运行的应用。
本指南 **并非** 指导用户如何调试集群。
如果想调试集群的话，请参阅[这里](/zh-cn/docs/tasks/debug/debug-cluster)。


## 诊断问题   {#diagnosing-the-problem}

故障排查的第一步是先给问题分类。问题是什么？是关于 Pod、Replication Controller 还是 Service？

* [调试 Pod](#debugging-pods)
* [调试 Replication Controller](#debugging-replication-controllers)
* [调试 Service](#debugging-services)

### 调试 Pod   {#debugging-pods}

调试 Pod 的第一步是查看 Pod 信息。用如下命令查看 Pod 的当前状态和最近的事件：

```shell
kubectl describe pods ${POD_NAME}
```

查看一下 Pod 中的容器所处的状态。这些容器的状态都是 `Running` 吗？最近有没有重启过？

后面的调试都是要依靠 Pod 的状态的。

#### Pod 停滞在 Pending 状态  {#my-pod-stays-pending}

如果一个 Pod 停滞在 `Pending` 状态，表示 Pod 没有被调度到节点上。
通常这是因为某种类型的资源不足导致无法调度。
查看上面的 `kubectl describe ...` 命令的输出，其中应该显示了为什么没被调度的原因。
常见原因如下：

* **资源不足**：
  你可能耗尽了集群上所有的 CPU 或内存。此时，你需要删除 Pod、调整资源请求或者为集群添加节点。
  更多信息请参阅[计算资源文档](/zh-cn/docs/concepts/configuration/manage-resources-containers/)

* **使用了 `hostPort`**：
  如果绑定 Pod 到 `hostPort`，那么能够运行该 Pod 的节点就有限了。
  多数情况下，`hostPort` 是非必要的，而应该采用 Service 对象来暴露 Pod。
  如果确实需要使用 `hostPort`，那么集群中节点的个数就是所能创建的 Pod
  的数量上限。

#### Pod 停滞在 Waiting 状态  {#my-pod-stays-waiting}

如果 Pod 停滞在 `Waiting` 状态，则表示 Pod 已经被调度到某工作节点，但是无法在该节点上运行。
同样，`kubectl describe ...` 命令的输出可能很有用。
`Waiting` 状态的最常见原因是拉取镜像失败。要检查的有三个方面：

* 确保镜像名字拼写正确。
* 确保镜像已被推送到镜像仓库。
* 尝试手动是否能拉取镜像。例如，如果你在你的 PC 上使用 Docker，请运行 `docker pull <镜像>`。

#### Pod 处于 Crashing 或别的不健康状态   {#my-pod-is-crashing-or-otherwise-unhealthy}

一旦 Pod 被调度，
就可以采用[调试运行中的 Pod](/zh-cn/docs/tasks/debug/debug-application/debug-running-pod/)
中的方法来进一步调试。

#### Pod 处于 Running 态但是没有正常工作

如果 Pod 行为不符合预期，很可能 Pod 描述（例如你本地机器上的 `mypod.yaml`）中有问题，
并且该错误在创建 Pod 时被忽略掉，没有报错。
通常，Pod 的定义中节区嵌套关系错误、字段名字拼错的情况都会引起对应内容被忽略掉。
例如，如果你误将 `command` 写成 `commnd`，Pod 虽然可以创建，
但它不会执行你期望它执行的命令行。

可以做的第一件事是删除你的 Pod，并尝试带有 `--validate` 选项重新创建。
例如，运行 `kubectl apply --validate -f mypod.yaml`。
如果 `command` 被误拼成 `commnd`，你将会看到下面的错误信息：

```shell
I0805 10:43:25.129850   46757 schema.go:126] unknown field: commnd
I0805 10:43:25.129973   46757 schema.go:129] this may be a false alarm, see https://github.com/kubernetes/kubernetes/issues/6842
pods/mypod
```


接下来就要检查的是 API 服务器上的 Pod 与你所期望创建的是否匹配
（例如，你原本使用本机上的一个 YAML 文件来创建 Pod）。
例如，运行 `kubectl get pods/mypod -o yaml > mypod-on-apiserver.yaml`，
之后手动比较 `mypod.yaml` 与从 API 服务器取回的 Pod 描述。
从 API 服务器处获得的 YAML 通常包含一些创建 Pod 所用的 YAML 中不存在的行，这是正常的。
不过，如果如果源文件中有些行在 API 服务器版本中不存在，则意味着
Pod 规约是有问题的。

### 调试副本控制器  {#debugging-replication-controllers}

副本控制器相对比较简单直接。它们要么能创建 Pod，要么不能。
如果不能创建 Pod，请参阅[上述说明](#debugging-pods)调试 Pod。

你也可以使用 `kubectl describe rc ${CONTROLLER_NAME}` 命令来检视副本控制器相关的事件。

### 调试 Service   {#debugging-services}

服务支持在多个 Pod 间负载均衡。
有一些常见的问题可以造成服务无法正常工作。
以下说明将有助于调试服务的问题。

首先，验证服务是否有端点。对于每一个 Service 对象，API 服务器为其提供对应的
`endpoints` 资源。

通过如下命令可以查看 endpoints 资源：

```shell
kubectl get endpoints ${SERVICE_NAME}
```

确保 Endpoints 与服务成员 Pod 个数一致。
例如，如果你的 Service 用来运行 3 个副本的 nginx 容器，你应该会在 Service 的 Endpoints
中看到 3 个不同的 IP 地址。

#### 服务缺少 Endpoints   {#my-service-is-missing-endpoints}

如果没有 Endpoints，请尝试使用 Service 所使用的标签列出 Pod。
假定你的服务包含如下标签选择算符：

```yaml
...
spec:
  - selector:
     name: nginx
     type: frontend
```

你可以使用如下命令列出与选择算符相匹配的 Pod，并验证这些 Pod 是否归属于创建的服务：

```shell
kubectl get pods --selector=name=nginx,type=frontend
```

验证 Pod 的 `containerPort` 与服务的 `targetPort` 是否匹配。

#### 网络流量未被转发  {#network-traffic-is-not-forwarded}

请参阅[调试 Service](/zh-cn/docs/tasks/debug/debug-application/debug-service/) 了解更多信息。

## {{% heading "whatsnext" %}}

如果上述方法都不能解决你的问题，
请按照[调试 Service 文档](/zh-cn/docs/tasks/debug/debug-application/debug-service/)中的介绍，
确保你的 `Service` 处于 Running 状态，有 `Endpoints` 被创建，`Pod` 真的在提供服务；
DNS 服务已配置并正常工作，iptables 规则也已安装并且 `kube-proxy` 也没有异常行为。

你也可以访问[故障排查文档](/zh-cn/docs/tasks/debug/)来获取更多信息。
