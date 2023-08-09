---
title: 使用 kubectl patch 更新 API 对象
description: 使用 kubectl patch 更新 Kubernetes API 对象。做一个策略性的合并 patch 或 JSON 合并 patch。
content_type: task
weight: 50
---



这个任务展示如何使用 `kubectl patch` 就地更新 API 对象。
这个任务中的练习演示了一个策略性合并 patch 和一个 JSON 合并 patch。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


## 使用策略合并 patch 更新 Deployment    {#use-a-strategic-merge-patch-to-update-a-deployment}

下面是具有两个副本的 Deployment 的配置文件。每个副本是一个 Pod，有一个容器：

{{< codenew file="application/deployment-patch.yaml" >}}

创建 Deployment：

```shell
kubectl apply -f https://k8s.io/examples/application/deployment-patch.yaml
```

查看与 Deployment 相关的 Pod：

```shell
kubectl get pods
```

输出显示 Deployment 有两个 Pod。`1/1` 表示每个 Pod 有一个容器：

```
NAME                        READY     STATUS    RESTARTS   AGE
patch-demo-28633765-670qr   1/1       Running   0          23s
patch-demo-28633765-j5qs3   1/1       Running   0          23s
```

把运行的 Pod 的名字记下来。稍后，你将看到这些 Pod 被终止并被新的 Pod 替换。

此时，每个 Pod 都有一个运行 nginx 镜像的容器。现在假设你希望每个 Pod 有两个容器：一个运行 nginx，另一个运行 redis。

创建一个名为 `patch-file.yaml` 的文件。内容如下：

```yaml
spec:
  template:
    spec:
      containers:
      - name: patch-demo-ctr-2
        image: redis
```

修补你的 Deployment：

```shell
kubectl patch deployment patch-demo --patch-file patch-file.yaml
```
查看修补后的 Deployment：

```shell
kubectl get deployment patch-demo --output yaml
```

输出显示 Deployment 中的 PodSpec 有两个容器：

```yaml
containers:
- image: redis
  imagePullPolicy: Always
  name: patch-demo-ctr-2
  ...
- image: nginx
  imagePullPolicy: Always
  name: patch-demo-ctr
  ...
```

查看与 patch Deployment 相关的 Pod：

```shell
kubectl get pods
```

输出显示正在运行的 Pod 与以前运行的 Pod 有不同的名称。Deployment 终止了旧的 Pod，
并创建了两个符合更新后的 Deployment 规约的新 Pod。`2/2` 表示每个 Pod 有两个容器:

```
NAME                          READY     STATUS    RESTARTS   AGE
patch-demo-1081991389-2wrn5   2/2       Running   0          1m
patch-demo-1081991389-jmg7b   2/2       Running   0          1m
```

仔细查看其中一个 patch-demo Pod：

```shell
kubectl get pod <your-pod-name> --output yaml
```

输出显示 Pod 有两个容器：一个运行 nginx，一个运行 redis：

```
containers:
- image: redis
  ...
- image: nginx
  ...
```

### 策略性合并类的 patch 的说明    {#notes-on-the-strategic-merge-patch}

你在前面的练习中所做的 patch 称为 `策略性合并 patch（Strategic Merge Patch）`。
请注意，patch 没有替换 `containers` 列表。相反，它向列表中添加了一个新 Container。换句话说，
patch 中的列表与现有列表合并。当你在列表中使用策略性合并 patch 时，并不总是这样。
在某些情况下，列表是替换的，而不是合并的。

对于策略性合并 patch，列表可以根据其 patch 策略进行替换或合并。
patch 策略由 Kubernetes 源代码中字段标记中的 `patchStrategy` 键的值指定。
例如，`PodSpec` 结构体的 `Containers` 字段的 `patchStrategy` 为 `merge`：

```go
type PodSpec struct {
  ...
  Containers []Container `json:"containers" patchStrategy:"merge" patchMergeKey:"name" ...`
  ...
}
```

你还可以在
[OpenApi 规范](https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json)中看到
patch 策略：

```yaml
"io.k8s.api.core.v1.PodSpec": {
    ...,
    "containers": {
        "description": "List of containers belonging to the pod.  ...."
    },
    "x-kubernetes-patch-merge-key": "name",
    "x-kubernetes-patch-strategy": "merge"
}
```

你可以在 [Kubernetes API 文档](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core)
中看到 patch 策略。

创建一个名为 `patch-file-tolerations.yaml` 的文件。内容如下:

```yaml
spec:
  template:
    spec:
      tolerations:
      - effect: NoSchedule
        key: disktype
        value: ssd
```

对 Deployment 执行 patch 操作：

```shell
kubectl patch deployment patch-demo --patch-file patch-file-tolerations.yaml
```

查看修补后的 Deployment：

```shell
kubectl get deployment patch-demo --output yaml
```

输出结果显示 Deployment 中的 PodSpec 只有一个容忍度设置：

```yaml
tolerations:
- effect: NoSchedule
  key: disktype
  value: ssd
```

请注意，PodSpec 中的 `tolerations` 列表被替换，而不是合并。这是因为 PodSpec 的 `tolerations`
的字段标签中没有 `patchStrategy` 键。所以策略合并 patch 操作使用默认的 patch 策略，也就是 `replace`。

```go
type PodSpec struct {
  ...
  Tolerations []Toleration `json:"tolerations,omitempty" protobuf:"bytes,22,opt,name=tolerations"`
  ...
}
```

## 使用 JSON 合并 patch 更新 Deployment    {#use-a-json-merge-patch-to-update-a-deployment}

策略性合并 patch 不同于 [JSON 合并 patch](https://tools.ietf.org/html/rfc7386)。
使用 JSON 合并 patch，如果你想更新列表，你必须指定整个新列表。新的列表完全取代现有的列表。

`kubectl patch` 命令有一个 `type` 参数，你可以将其设置为以下值之一：

<table>
  <tr><th>参数值</th><th>合并类型</th></tr>
  <tr><td>json</td><td><a href="https://tools.ietf.org/html/rfc6902">JSON Patch, RFC 6902</a></td></tr>
  <tr><td>merge</td><td><a href="https://tools.ietf.org/html/rfc7386">JSON Merge Patch, RFC 7386</a></td></tr>
  <tr><td>strategic</td><td>策略合并 patch</td></tr>
</table>

有关 JSON patch 和 JSON 合并 patch 的比较，查看
[JSON patch 和 JSON 合并 patch](https://erosb.github.io/post/json-patch-vs-merge-patch/)。

`type` 参数的默认值是 `strategic`。在前面的练习中，我们做了一个策略性的合并 patch。

下一步，在相同的 Deployment 上执行 JSON 合并 patch。创建一个名为 `patch-file-2` 的文件。内容如下：

```yaml
spec:
  template:
    spec:
      containers:
      - name: patch-demo-ctr-3
        image: gcr.io/google-samples/node-hello:1.0
```

在 patch 命令中，将 `type` 设置为 `merge`：

```shell
kubectl patch deployment patch-demo --type merge --patch-file patch-file-2.yaml
```

查看修补后的 Deployment：

```shell
kubectl get deployment patch-demo --output yaml
```

patch 中指定的 `containers` 列表只有一个 Container。
输出显示你所给出的 Container 列表替换了现有的 `containers` 列表。

```yaml
spec:
  containers:
  - image: gcr.io/google-samples/node-hello:1.0
    ...
    name: patch-demo-ctr-3
```

列出正运行的 Pod：

```shell
kubectl get pods
```

在输出中，你可以看到已经终止了现有的 Pod，并创建了新的 Pod。`1/1` 表示每个新 Pod 只运行一个容器。

```shell
NAME                          READY     STATUS    RESTARTS   AGE
patch-demo-1307768864-69308   1/1       Running   0          1m
patch-demo-1307768864-c86dc   1/1       Running   0          1m
```

## 使用带 retainKeys 策略的策略合并 patch 更新 Deployment    {#use-strategic-merge-patch-to-update-a-deployment-using-the-retainkeys-strategy}

{{< codenew file="application/deployment-retainkeys.yaml" >}}

创建 Deployment：

```shell
kubectl apply -f https://k8s.io/examples/application/deployment-retainkeys.yaml
```

这时，Deployment 被创建，并使用 `RollingUpdate` 策略。

创建一个名为 `patch-file-no-retainkeys.yaml` 的文件，内容如下：

```yaml
spec:
  strategy:
    type: Recreate
```

修补你的 Deployment:

```shell
kubectl patch deployment retainkeys-demo --type strategic --patch-file patch-file-no-retainkeys.yaml
```

在输出中，你可以看到，当 `spec.strategy.rollingUpdate` 已经拥有取值定义时，
将其 `type` 设置为 `Recreate` 是不可能的。

```
The Deployment "retainkeys-demo" is invalid: spec.strategy.rollingUpdate: Forbidden: may not be specified when strategy `type` is 'Recreate'
```

更新 `type` 取值的同时移除 `spec.strategy.rollingUpdate`
现有值的方法是为策略性合并操作设置 `retainKeys` 策略：

创建另一个名为 `patch-file-retainkeys.yaml` 的文件，内容如下：

```yaml
spec:
  strategy:
    $retainKeys:
    - type
    type: Recreate
```

使用此 patch，我们表达了希望只保留 `strategy` 对象的 `type` 键。
这样，在 patch 操作期间 `rollingUpdate` 会被删除。

使用新的 patch 重新修补 Deployment：

```shell
kubectl patch deployment retainkeys-demo --type strategic --patch-file patch-file-retainkeys.yaml
```

检查 Deployment 的内容：

```shell
kubectl get deployment retainkeys-demo --output yaml
```

输出显示 Deployment 中的 `strategy` 对象不再包含 `rollingUpdate` 键：

```yaml
spec:
  strategy:
    type: Recreate
  template:
```

### 关于使用 retainKeys 策略的策略合并 patch 操作的说明    {#notes-on-the-strategic-merge-patch-using-the-retainkeys-strategy}

在前文练习中所执行的称作 **带 `retainKeys` 策略的策略合并 patch（Strategic Merge
Patch with retainKeys Strategy）**。
这种方法引入了一种新的 `$retainKey` 指令，具有如下策略：

- 其中包含一个字符串列表；
- 所有需要被保留的字段必须在 `$retainKeys` 列表中给出；
- 对于已有的字段，会和对象上对应的内容合并；
- 在修补操作期间，未找到的字段都会被清除；
- 列表 `$retainKeys` 中的所有字段必须 patch 操作所给字段的超集，或者与之完全一致。

策略 `retainKeys` 并不能对所有对象都起作用。它仅对那些 Kubernetes 源码中
`patchStrategy` 字段标志值包含 `retainKeys` 的字段有用。
例如 `DeploymentSpec` 结构的 `Strategy` 字段就包含了 `patchStrategy` 为
`retainKeys` 的标志。

```go
type DeploymentSpec struct {
  ...
  // +patchStrategy=retainKeys
  Strategy DeploymentStrategy `json:"strategy,omitempty" patchStrategy:"retainKeys" ...`
  ...
}
```

你也可以查看
[OpenAPI 规范](https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json)中的
`retainKeys` 策略：

```yaml
"io.k8s.api.apps.v1.DeploymentSpec": {
    ...,
    "strategy": {
        "$ref": "#/definitions/io.k8s.api.apps.v1.DeploymentStrategy",
        "description": "The deployment strategy to use to replace existing pods with new ones.",
        "x-kubernetes-patch-strategy": "retainKeys"
    },
    ....
}
```

而且你也可以在
[Kubernetes API 文档](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#deploymentspec-v1-apps)中看到
`retainKey` 策略。

### kubectl patch 命令的其他形式    {#alternate-forms-of-the-kubectl-patch-command}

`kubectl patch` 命令使用 YAML 或 JSON。它可以接受以文件形式提供的补丁，也可以接受直接在命令行中给出的补丁。

创建一个文件名称是 `patch-file.json` 内容如下：

```json
{
   "spec": {
      "template": {
         "spec": {
            "containers": [
               {
                  "name": "patch-demo-ctr-2",
                  "image": "redis"
               }
            ]
         }
      }
   }
}
```

以下命令是等价的：

```shell
kubectl patch deployment patch-demo --patch-file patch-file.yaml
kubectl patch deployment patch-demo --patch 'spec:\n template:\n  spec:\n   containers:\n   - name: patch-demo-ctr-2\n     image: redis'

kubectl patch deployment patch-demo --patch-file patch-file.json
kubectl patch deployment patch-demo --patch '{"spec": {"template": {"spec": {"containers": [{"name": "patch-demo-ctr-2","image": "redis"}]}}}}'
```
### 使用 `kubectl patch` 和 `--subresource` 更新一个对象的副本数   {#scale-kubectl-patch}

{{< feature-state for_k8s_version="v1.24" state="alpha" >}}

使用 kubectl 命令（如 get、patch、edit 和 replace）时带上 `--subresource=[subresource-name]` 标志，
可以获取和更新资源的 `status` 和 `scale` 子资源（适用于 kubectl v1.24 或更高版本）。
这个标志可用于带有 `status` 或 `scale` 子资源的所有 API 资源 (内置资源和 CR 资源)。
Deployment 是支持这些子资源的其中一个例子。

下面是有两个副本的 Deployment 的清单。

{{< codenew file="application/deployment.yaml" >}}

创建 Deployment：

```shell
kubectl apply -f https://k8s.io/examples/application/deployment.yaml
```

查看与 Deployment 关联的 Pod：

```shell
kubectl get pods -l app=nginx
```

在输出中，你可以看到此 Deployment 有两个 Pod。例如：

```
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-7fb96c846b-22567   1/1     Running   0          47s
nginx-deployment-7fb96c846b-mlgns   1/1     Running   0          47s
```

现在用 `--subresource=[subresource-name]` 标志修补此 Deployment：

```shell
kubectl patch deployment nginx-deployment --subresource='scale' --type='merge' -p '{"spec":{"replicas":3}}'
```

输出为：

```shell
scale.autoscaling/nginx-deployment patched
```

查看与你所修补的 Deployment 关联的 Pod：

```shell
kubectl get pods -l app=nginx
```

在输出中，你可以看到一个新的 Pod 被创建，因此现在你有 3 个正在运行的 Pod。

```
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-7fb96c846b-22567   1/1     Running   0          107s
nginx-deployment-7fb96c846b-lxfr2   1/1     Running   0          14s
nginx-deployment-7fb96c846b-mlgns   1/1     Running   0          107s
```

查看所修补的 Deployment：

```shell
kubectl get deployment nginx-deployment -o yaml
```

```yaml
...
spec:
  replicas: 3
  ...
status:
  ...
  availableReplicas: 3
  readyReplicas: 3
  replicas: 3
```

{{< note >}}
如果你运行 `kubectl patch` 并指定 `--subresource` 标志时，所针对的是不支持特定子资源的资源，
则 API 服务器会返回一个 404 Not Found 错误。
{{< /note >}}

## 总结    {#summary}

在本练习中，你使用 `kubectl patch` 更改了 Deployment 对象的当前配置。
你没有更改最初用于创建 Deployment 对象的配置文件。
用于更新 API 对象的其他命令包括
[`kubectl annotate`](/docs/reference/generated/kubectl/kubectl-commands/#annotate)、
[`kubectl edit`](/docs/reference/generated/kubectl/kubectl-commands/#edit)、
[`kubectl replace`](/docs/reference/generated/kubectl/kubectl-commands/#replace)、
[`kubectl scale`](/docs/reference/generated/kubectl/kubectl-commands/#scale) 和
[`kubectl apply`](/docs/reference/generated/kubectl/kubectl-commands/#apply)。

{{< note >}}
定制资源不支持策略性合并 patch。
{{< /note >}}

## {{% heading "whatsnext" %}}

* [Kubernetes 对象管理](/zh-cn/docs/concepts/overview/working-with-objects/object-management/)
* [使用指令式命令管理 Kubernetes 对象](/zh-cn/docs/tasks/manage-kubernetes-objects/imperative-command/)
* [使用配置文件对 Kubernetes 对象进行命令式管理](/zh-cn/docs/tasks/manage-kubernetes-objects/imperative-config/)
* [使用配置文件对 Kubernetes 对象进行声明式管理](/zh-cn/docs/tasks/manage-kubernetes-objects/declarative-config/)

