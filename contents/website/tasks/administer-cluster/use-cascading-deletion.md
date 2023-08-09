---
title: 在集群中使用级联删除
content_type: task
weight: 360
---



本页面向你展示如何设置在你的集群执行{{<glossary_tooltip text="垃圾收集" term_id="garbage-collection">}}
时要使用的[级联删除](/zh-cn/docs/concepts/architecture/garbage-collection/#cascading-deletion)
类型。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

你还需要[创建一个 Deployment 示例](/zh-cn/docs/tasks/run-application/run-stateless-application-deployment/#creating-and-exploring-an-nginx-deployment)
以试验不同类型的级联删除。你需要为每种级联删除类型来重建 Deployment。

## 检查 Pod 上的属主引用    {#check-owner-references-on-your-pods}

检查确认你的 Pods 上存在 `ownerReferences` 字段：

```shell 
kubectl get pods -l app=nginx --output=yaml
```

输出中包含 `ownerReferences` 字段，类似这样：

```yaml
apiVersion: v1
    ...
    ownerReferences:
    - apiVersion: apps/v1
      blockOwnerDeletion: true
      controller: true
      kind: ReplicaSet
      name: nginx-deployment-6b474476c4
      uid: 4fdcd81c-bd5d-41f7-97af-3a3b759af9a7
    ...
```

## 使用前台级联删除    {#use-foreground-cascading-deletion}

默认情况下，Kubernetes 使用[后台级联删除](/zh-cn/docs/concepts/architecture/garbage-collection/#background-deletion)
以删除依赖某对象的其他对象。取决于你的集群所运行的 Kubernetes 版本，
你可以使用 `kubectl` 或者 Kubernetes API 来切换到前台级联删除。
{{<version-check>}}


你可以使用 `kubectl` 或者 Kubernetes API 来基于前台级联删除来删除对象。

**使用 kubectl**

运行下面的命令：


```shell
kubectl delete deployment nginx-deployment --cascade=foreground
```

**使用 Kubernetes API**

1. 启动一个本地代理会话：

   ```shell
   kubectl proxy --port=8080
   ```

2. 使用 `curl` 来触发删除操作：

   ```shell
   curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/deployments/nginx-deployment \
       -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
       -H "Content-Type: application/json"
   ```

   输出中包含 `foregroundDeletion` {{<glossary_tooltip text="finalizer" term_id="finalizer">}}，
   类似这样：

   ```
   "kind": "Deployment",
   "apiVersion": "apps/v1",
   "metadata": {
       "name": "nginx-deployment",
       "namespace": "default",
       "uid": "d1ce1b02-cae8-4288-8a53-30e84d8fa505",
       "resourceVersion": "1363097",
       "creationTimestamp": "2021-07-08T20:24:37Z",
       "deletionTimestamp": "2021-07-08T20:27:39Z",
       "finalizers": [
         "foregroundDeletion"
       ]
       ...
   ```


## 使用后台级联删除 {#use-background-cascading-deletion}

1. [创建一个 Deployment 示例](/zh-cn/docs/tasks/run-application/run-stateless-application-deployment/#creating-and-exploring-an-nginx-deployment)。
1. 基于你的集群所运行的 Kubernetes 版本，使用 `kubectl` 或者 Kubernetes API 来删除 Deployment。
   {{<version-check>}}


你可以使用 `kubectl` 或者 Kubernetes API 来执行后台级联删除方式的对象删除操作。

Kubernetes 默认采用后台级联删除方式，如果你在运行下面的命令时不指定
`--cascade` 标志或者 `propagationPolicy` 参数时，用这种方式来删除对象。

**使用 kubectl**

运行下面的命令：

```shell
kubectl delete deployment nginx-deployment --cascade=background
```

**使用 Kubernetes API**

1. 启动一个本地代理会话：

   ```shell
   kubectl proxy --port=8080
   ```

2. 使用 `curl` 来触发删除操作：

   ```shell
   curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/deployments/nginx-deployment \
       -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Background"}' \
       -H "Content-Type: application/json"
   ```

   输出类似于：

   ```
   "kind": "Status",
   "apiVersion": "v1",
   ...
   "status": "Success",
   "details": {
       "name": "nginx-deployment",
       "group": "apps",
       "kind": "deployments",
       "uid": "cc9eefb9-2d49-4445-b1c1-d261c9396456"
   }
   ```


## 删除属主对象和孤立的依赖对象   {#set-orphan-deletion-policy}

默认情况下，当你告诉 Kubernetes 删除某个对象时，
{{<glossary_tooltip text="控制器" term_id="controller">}} 也会删除依赖该对象
的其他对象。
取决于你的集群所运行的 Kubernetes 版本，你也可以使用 `kubectl` 或者 Kubernetes
API 来让 Kubernetes *孤立* 这些依赖对象。{{<version-check>}}


**使用 kubectl**

运行下面的命令：

```shell
kubectl delete deployment nginx-deployment --cascade=orphan
```

**使用 Kubernetes API**

1. 启动一个本地代理会话：

   ```shell
   kubectl proxy --port=8080
   ```

2. 使用 `curl` 来触发删除操作：

   ```shell
   curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/deployments/nginx-deployment \
       -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Orphan"}' \
       -H "Content-Type: application/json"
   ```

   输出中在 `finalizers` 字段中包含 `orphan`，如下所示：

   ```
   "kind": "Deployment",
   "apiVersion": "apps/v1",
   "namespace": "default",
   "uid": "6f577034-42a0-479d-be21-78018c466f1f",
   "creationTimestamp": "2021-07-09T16:46:37Z",
   "deletionTimestamp": "2021-07-09T16:47:08Z",
   "deletionGracePeriodSeconds": 0,
   "finalizers": [
     "orphan"
   ],
   ...
   ```


你可以检查 Deployment 所管理的 Pods 仍然处于运行状态：

```shell
kubectl get pods -l app=nginx
```

## {{% heading "whatsnext" %}}

* 了解 Kubernetes 中的[属主与依赖](/zh-cn/docs/concepts/overview/working-with-objects/owners-dependents/)
* 了解 Kubernetes [finalizers](/zh-cn/docs/concepts/overview/working-with-objects/finalizers/)
* 了解[垃圾收集](/zh-cn/docs/concepts/architecture/garbage-collection/).

