---
title: 管理资源
content_type: concept
weight: 40
---


你已经部署了应用并通过服务暴露它。然后呢？
Kubernetes 提供了一些工具来帮助管理你的应用部署，包括扩缩容和更新。
我们将更深入讨论的特性包括
[配置文件](/zh-cn/docs/concepts/configuration/overview/)和
[标签](/zh-cn/docs/concepts/overview/working-with-objects/labels/)。


## 组织资源配置   {#organizing-resource-config}

许多应用需要创建多个资源，例如 Deployment 和 Service。
可以通过将多个资源组合在同一个文件中（在 YAML 中以 `---` 分隔）
来简化对它们的管理。例如：

{{< codenew file="application/nginx-app.yaml" >}}

可以用创建单个资源相同的方式来创建多个资源：

```shell
kubectl apply -f https://k8s.io/examples/application/nginx-app.yaml
```

```none
service/my-nginx-svc created
deployment.apps/my-nginx created
```

资源将按照它们在文件中的顺序创建。
因此，最好先指定服务，这样在控制器（例如 Deployment）创建 Pod 时能够
确保调度器可以将与服务关联的多个 Pod 分散到不同节点。

`kubectl apply` 也接受多个 `-f` 参数：

```shell
kubectl apply -f https://k8s.io/examples/application/nginx/nginx-svc.yaml \
  -f https://k8s.io/examples/application/nginx/nginx-deployment.yaml
```

建议的做法是，将同一个微服务或同一应用层相关的资源放到同一个文件中，
将同一个应用相关的所有文件按组存放到同一个目录中。
如果应用的各层使用 DNS 相互绑定，你可以将堆栈的所有组件一起部署。

还可以使用 URL 作为配置源，便于直接使用已经提交到 GitHub 上的配置文件进行部署：

```shell
kubectl apply -f https://k8s.io/examples/application/nginx/nginx-deployment.yaml
```

```none
deployment.apps/my-nginx created
```

## kubectl 中的批量操作  {#bulk-operations-in-kubectl}

资源创建并不是 `kubectl` 可以批量执行的唯一操作。
`kubectl` 还可以从配置文件中提取资源名，以便执行其他操作，
特别是删除你之前创建的资源：

```shell
kubectl delete -f https://k8s.io/examples/application/nginx-app.yaml
```

```none
deployment.apps "my-nginx" deleted
service "my-nginx-svc" deleted
```

在仅有两种资源的情况下，你可以使用"资源类型/资源名"的语法在命令行中
同时指定这两个资源：

```shell
kubectl delete deployments/my-nginx services/my-nginx-svc
```

对于资源数目较大的情况，你会发现使用 `-l` 或 `--selector` 
指定筛选器（标签查询）能很容易根据标签筛选资源：

```shell
kubectl delete deployment,services -l app=nginx
```

```none
deployment.apps "my-nginx" deleted
service "my-nginx-svc" deleted
```

由于 `kubectl` 用来输出资源名称的语法与其所接受的资源名称语法相同，
你可以使用 `$()` 或 `xargs` 进行链式操作：

```shell
kubectl get $(kubectl create -f docs/concepts/cluster-administration/nginx/ -o name | grep service)
kubectl create -f docs/concepts/cluster-administration/nginx/ -o name | grep service | xargs -i kubectl get {}
```

```none
NAME           TYPE           CLUSTER-IP   EXTERNAL-IP   PORT(S)      AGE
my-nginx-svc   LoadBalancer   10.0.0.208   <pending>     80/TCP       0s
```

上面的命令中，我们首先使用 `examples/application/nginx/` 下的配置文件创建资源，
并使用 `-o name` 的输出格式（以"资源/名称"的形式打印每个资源）打印所创建的资源。
然后，我们通过 `grep` 来过滤 "service"，最后再打印 `kubectl get` 的内容。

如果你碰巧在某个路径下的多个子路径中组织资源，那么也可以递归地在所有子路径上
执行操作，方法是在 `--filename,-f` 后面指定 `--recursive` 或者 `-R`。

例如，假设有一个目录路径为 `project/k8s/development`，它保存开发环境所需的
所有{{< glossary_tooltip text="清单" term_id="manifest" >}}，并按资源类型组织：

```none
project/k8s/development
├── configmap
│   └── my-configmap.yaml
├── deployment
│   └── my-deployment.yaml
└── pvc
    └── my-pvc.yaml
```

默认情况下，对 `project/k8s/development` 执行的批量操作将停止在目录的第一级，
而不是处理所有子目录。
如果我们试图使用以下命令在此目录中创建资源，则会遇到一个错误：

```shell
kubectl apply -f project/k8s/development
```

```none
error: you must provide one or more resources by argument or filename (.json|.yaml|.yml|stdin)
```

正确的做法是，在 `--filename,-f` 后面标明 `--recursive` 或者 `-R` 之后：

```shell
kubectl apply -f project/k8s/development --recursive
```

```none
configmap/my-config created
deployment.apps/my-deployment created
persistentvolumeclaim/my-pvc created
```

`--recursive` 可以用于接受 `--filename,-f` 参数的任何操作，例如：
`kubectl {create,get,delete,describe,rollout}` 等。

有多个 `-f` 参数出现的时候，`--recursive` 参数也能正常工作：

```shell
kubectl apply -f project/k8s/namespaces -f project/k8s/development --recursive
```

```none
namespace/development created
namespace/staging created
configmap/my-config created
deployment.apps/my-deployment created
persistentvolumeclaim/my-pvc created
```

如果你有兴趣进一步学习关于 `kubectl` 的内容，请阅读[命令行工具（kubectl）](/zh-cn/docs/reference/kubectl/)。

## 有效地使用标签  {#using-labels-effectively}

到目前为止我们使用的示例中的资源最多使用了一个标签。
在许多情况下，应使用多个标签来区分集合。

例如，不同的应用可能会为 `app` 标签设置不同的值。
但是，类似 [guestbook 示例](https://github.com/kubernetes/examples/tree/master/guestbook/)
这样的多层应用，还需要区分每一层。前端可以带以下标签：

```yaml
     labels:
        app: guestbook
        tier: frontend
```

Redis 的主节点和从节点会有不同的 `tier` 标签，甚至还有一个额外的 `role` 标签：

```yaml
     labels:
        app: guestbook
        tier: backend
        role: master
```

以及

```yaml
     labels:
        app: guestbook
        tier: backend
        role: slave
```

标签允许我们按照标签指定的任何维度对我们的资源进行切片和切块：

```shell
kubectl apply -f examples/guestbook/all-in-one/guestbook-all-in-one.yaml
kubectl get pods -Lapp -Ltier -Lrole
```

```none
NAME                           READY     STATUS    RESTARTS   AGE       APP         TIER       ROLE
guestbook-fe-4nlpb             1/1       Running   0          1m        guestbook   frontend   <none>
guestbook-fe-ght6d             1/1       Running   0          1m        guestbook   frontend   <none>
guestbook-fe-jpy62             1/1       Running   0          1m        guestbook   frontend   <none>
guestbook-redis-master-5pg3b   1/1       Running   0          1m        guestbook   backend    master
guestbook-redis-slave-2q2yf    1/1       Running   0          1m        guestbook   backend    slave
guestbook-redis-slave-qgazl    1/1       Running   0          1m        guestbook   backend    slave
my-nginx-divi2                 1/1       Running   0          29m       nginx       <none>     <none>
my-nginx-o0ef1                 1/1       Running   0          29m       nginx       <none>     <none>
```

```shell
kubectl get pods -lapp=guestbook,role=slave
```

```none
NAME                          READY     STATUS    RESTARTS   AGE
guestbook-redis-slave-2q2yf   1/1       Running   0          3m
guestbook-redis-slave-qgazl   1/1       Running   0          3m
```

## 金丝雀部署（Canary Deployments）   {#canary-deployments}

另一个需要多标签的场景是用来区分同一组件的不同版本或者不同配置的多个部署。
常见的做法是部署一个使用*金丝雀发布*来部署新应用版本
（在 Pod 模板中通过镜像标签指定），保持新旧版本应用同时运行。
这样，新版本在完全发布之前也可以接收实时的生产流量。

例如，你可以使用 `track` 标签来区分不同的版本。

主要稳定的发行版将有一个 `track` 标签，其值为 `stable`：

```none
name: frontend
replicas: 3
...
labels:
   app: guestbook
   tier: frontend
   track: stable
...
image: gb-frontend:v3
```

然后，你可以创建 guestbook 前端的新版本，让这些版本的 `track` 标签带有不同的值
（即 `canary`），以便两组 Pod 不会重叠：

```none
name: frontend-canary
replicas: 1
...
labels:
   app: guestbook
   tier: frontend
   track: canary
...
image: gb-frontend:v4
```

前端服务通过选择标签的公共子集（即忽略 `track` 标签）来覆盖两组副本，
以便流量可以转发到两个应用：

```yaml
selector:
   app: guestbook
   tier: frontend
```

你可以调整 `stable` 和 `canary` 版本的副本数量，以确定每个版本将接收
实时生产流量的比例（在本例中为 3:1）。
一旦有信心，你就可以将新版本应用的 `track` 标签的值从
`canary` 替换为 `stable`，并且将老版本应用删除。

想要了解更具体的示例，请查看
[Ghost 部署教程](https://github.com/kelseyhightower/talks/tree/master/kubecon-eu-2016/demo#deploy-a-canary)。

## 更新标签  {#updating-labels}

有时，现有的 pod 和其它资源需要在创建新资源之前重新标记。
这可以用 `kubectl label` 完成。
例如，如果想要将所有 nginx pod 标记为前端层，运行：

```shell
kubectl label pods -l app=nginx tier=fe
```

```none
pod/my-nginx-2035384211-j5fhi labeled
pod/my-nginx-2035384211-u2c7e labeled
pod/my-nginx-2035384211-u3t6x labeled
```

首先用标签 "app=nginx" 过滤所有的 Pod，然后用 "tier=fe" 标记它们。
想要查看你刚才标记的 Pod，请运行：

```shell
kubectl get pods -l app=nginx -L tier
```

```none
NAME                        READY     STATUS    RESTARTS   AGE       TIER
my-nginx-2035384211-j5fhi   1/1       Running   0          23m       fe
my-nginx-2035384211-u2c7e   1/1       Running   0          23m       fe
my-nginx-2035384211-u3t6x   1/1       Running   0          23m       fe
```

这将输出所有 "app=nginx" 的 Pod，并有一个额外的描述 Pod 的 tier 的标签列
（用参数 `-L` 或者 `--label-columns` 标明）。

想要了解更多信息，请参考[标签](/zh-cn/docs/concepts/overview/working-with-objects/labels/)和
[`kubectl label`](/docs/reference/generated/kubectl/kubectl-commands/#label)
命令文档。

## 更新注解   {#updating-annotations}

有时，你可能希望将注解附加到资源中。注解是 API 客户端（如工具、库等）
用于检索的任意非标识元数据。这可以通过 `kubectl annotate` 来完成。例如：

```shell
kubectl annotate pods my-nginx-v4-9gw19 description='my frontend running nginx'
kubectl get pods my-nginx-v4-9gw19 -o yaml
```

```shell
apiVersion: v1
kind: pod
metadata:
  annotations:
    description: my frontend running nginx
...
```

想要了解更多信息，请参考[注解](/zh-cn/docs/concepts/overview/working-with-objects/annotations/)和
[`kubectl annotate`](/docs/reference/generated/kubectl/kubectl-commands/#annotate)
命令文档。

## 扩缩你的应用  {#scaling-your-app}

当应用上的负载增长或收缩时，使用 `kubectl` 能够实现应用规模的扩缩。
例如，要将 nginx 副本的数量从 3 减少到 1，请执行以下操作：

```shell
kubectl scale deployment/my-nginx --replicas=1
```

```none
deployment.apps/my-nginx scaled
```

现在，你的 Deployment 管理的 Pod 只有一个了。

```shell
kubectl get pods -l app=nginx
```

```none
NAME                        READY     STATUS    RESTARTS   AGE
my-nginx-2035384211-j5fhi   1/1       Running   0          30m
```

想要让系统自动选择需要 nginx 副本的数量，范围从 1 到 3，请执行以下操作：

```shell
kubectl autoscale deployment/my-nginx --min=1 --max=3
```

```none
horizontalpodautoscaler.autoscaling/my-nginx autoscaled
```

现在，你的 nginx 副本将根据需要自动地增加或者减少。

想要了解更多信息，请参考
[kubectl scale](/docs/reference/generated/kubectl/kubectl-commands/#scale)命令文档、
[kubectl autoscale](/docs/reference/generated/kubectl/kubectl-commands/#autoscale)
命令文档和[水平 Pod 自动伸缩](/zh-cn/docs/tasks/run-application/horizontal-pod-autoscale/)文档。

## 就地更新资源  {#in-place-updates-of-resources}

有时，有必要对你所创建的资源进行小范围、无干扰地更新。

### kubectl apply

建议在源代码管理中维护一组配置文件
（参见[配置即代码](https://martinfowler.com/bliki/InfrastructureAsCode.html)），
这样，它们就可以和应用代码一样进行维护和版本管理。
然后，你可以用 [`kubectl apply`](/docs/reference/generated/kubectl/kubectl-commands/#apply)
将配置变更应用到集群中。

这个命令将会把推送的版本与以前的版本进行比较，并应用你所做的更改，
但是不会自动覆盖任何你没有指定更改的属性。

```shell
kubectl apply -f https://k8s.io/examples/application/nginx/nginx-deployment.yaml
```

```none
deployment.apps/my-nginx configured
```

注意，`kubectl apply` 将为资源增加一个额外的注解，以确定自上次调用以来对配置的更改。
执行时，`kubectl apply` 会在以前的配置、提供的输入和资源的当前配置之间
找出三方差异，以确定如何修改资源。

目前，新创建的资源是没有这个注解的，所以，第一次调用 `kubectl apply` 时
将使用提供的输入和资源的当前配置双方之间差异进行比较。
在第一次调用期间，它无法检测资源创建时属性集的删除情况。
因此，kubectl 不会删除它们。

所有后续的 `kubectl apply` 操作以及其他修改配置的命令，如 `kubectl replace`
和 `kubectl edit`，都将更新注解，并允许随后调用的 `kubectl apply`
使用三方差异进行检查和执行删除。

### kubectl edit

或者，你也可以使用 `kubectl edit` 更新资源：

```shell
kubectl edit deployment/my-nginx
```

这相当于首先 `get` 资源，在文本编辑器中编辑它，然后用更新的版本 `apply` 资源：

```shell
kubectl get deployment my-nginx -o yaml > /tmp/nginx.yaml
vi /tmp/nginx.yaml
# 做一些编辑，然后保存文件

kubectl apply -f /tmp/nginx.yaml
deployment.apps/my-nginx configured

rm /tmp/nginx.yaml
```

这使你可以更加容易地进行更重大的更改。
请注意，可以使用 `EDITOR` 或 `KUBE_EDITOR` 环境变量来指定编辑器。

想要了解更多信息，请参考
[kubectl edit](/docs/reference/generated/kubectl/kubectl-commands/#edit) 文档。

### kubectl patch

你可以使用 `kubectl patch` 来更新 API 对象。此命令支持 JSON patch、
JSON merge patch、以及 strategic merge patch。
请参考[使用 kubectl patch 更新 API 对象](/zh-cn/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch/)和
[kubectl patch](/docs/reference/generated/kubectl/kubectl-commands/#patch)。

## 破坏性的更新  {#disruptive-updates}

在某些情况下，你可能需要更新某些初始化后无法更新的资源字段，或者你可能只想立即进行递归更改，
例如修复 Deployment 创建的不正常的 Pod。若要更改这些字段，请使用 `replace --force`，
它将删除并重新创建资源。在这种情况下，你可以修改原始配置文件：

```shell
kubectl replace -f https://k8s.io/examples/application/nginx/nginx-deployment.yaml --force
```

```none
deployment.apps/my-nginx deleted
deployment.apps/my-nginx replaced
```

## 在不中断服务的情况下更新应用  {#updating-your-app-without-a-service-outage}

在某些时候，你最终需要更新已部署的应用，通常都是通过指定新的镜像或镜像标签，
如上面的金丝雀发布的场景中所示。`kubectl` 支持几种更新操作，
每种更新操作都适用于不同的场景。

我们将指导你通过 Deployment 如何创建和更新应用。

假设你正运行的是 1.14.2 版本的 nginx：

```shell
kubectl create deployment my-nginx --image=nginx:1.14.2
```

```none
deployment.apps/my-nginx created
```

运行 3 个副本（这样新旧版本可以同时存在）

```shell
kubectl scale deployment my-nginx --current-replicas=1 --replicas=3
```

```none
deployment.apps/my-nginx scaled
```

要更新到 1.16.1 版本，只需使用我们前面学到的 kubectl 命令将
`.spec.template.spec.containers[0].image` 从 `nginx:1.14.2` 修改为 `nginx:1.16.1`。

```shell
kubectl edit deployment/my-nginx
```

没错，就是这样！Deployment 将在后台逐步更新已经部署的 nginx 应用。
它确保在更新过程中，只有一定数量的旧副本被开闭，并且只有一定基于所需 Pod 数量的新副本被创建。
想要了解更多细节，请参考 [Deployment](/zh-cn/docs/concepts/workloads/controllers/deployment/)。

## {{% heading "whatsnext" %}}

- 学习[如何使用 `kubectl` 观察和调试应用](/zh-cn/docs/tasks/debug/debug-application/debug-running-pod/)
- 阅读[配置最佳实践和技巧](/zh-cn/docs/concepts/configuration/overview/)
