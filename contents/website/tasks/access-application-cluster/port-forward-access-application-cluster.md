---
title: 使用端口转发来访问集群中的应用
content_type: task
weight: 40
min-kubernetes-server-version: v1.10
---


本文展示如何使用 `kubectl port-forward` 连接到在 Kubernetes 集群中运行的 MongoDB 服务。
这种类型的连接对数据库调试很有用。

## {{% heading "prerequisites" %}}

* {{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}
* 安装 [MongoDB Shell](https://www.mongodb.com/try/download/shell)。


## 创建 MongoDB Deployment 和服务   {#creating-mongodb-deployment-and-service}

1. 创建一个运行 MongoDB 的 Deployment：

   ```shell
   kubectl apply -f https://k8s.io/examples/application/mongodb/mongo-deployment.yaml
   ```

   成功执行的命令的输出可以证明创建了 Deployment：

   ```
   deployment.apps/mongo created
   ```

   查看 Pod 状态，检查其是否准备就绪：

   ```shell
   kubectl get pods
   ```

   输出显示创建的 Pod：

   ```
   NAME                     READY   STATUS    RESTARTS   AGE
   mongo-75f59d57f4-4nd6q   1/1     Running   0          2m4s
   ```

   查看 Deployment 状态：

   ```shell
   kubectl get deployment
   ```

   输出显示创建的 Deployment：

   ```
   NAME    READY   UP-TO-DATE   AVAILABLE   AGE
   mongo   1/1     1            1           2m21s
   ```

   该 Deployment 自动管理一个 ReplicaSet。查看该 ReplicaSet 的状态：

   ```shell
   kubectl get replicaset
   ```

   输出显示 ReplicaSet 已被创建：

   ```
   NAME               DESIRED   CURRENT   READY   AGE
   mongo-75f59d57f4   1         1         1       3m12s
   ```

2. 创建一个在网络上公开的 MongoDB 服务：

   ```shell
   kubectl apply -f https://k8s.io/examples/application/mongodb/mongo-service.yaml
   ```

   成功执行的命令的输出可以证明 Service 已经被创建：

   ```
   service/mongo created
   ```

   检查所创建的 Service：

   ```shell
   kubectl get service mongo
   ```

   输出显示已被创建的 Service：

   ```
   NAME    TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)     AGE
   mongo   ClusterIP   10.96.41.183   <none>        27017/TCP   11s
   ```

3. 验证 MongoDB 服务是否运行在 Pod 中并且在监听 27017 端口：

   ```shell
   # 将 mongo-75f59d57f4-4nd6q 改为 Pod 的名称
   kubectl get pod mongo-75f59d57f4-4nd6q --template='{{(index (index .spec.containers 0).ports 0).containerPort}}{{"\n"}}'
   ```

   输出应该显示对应 Pod 中 MongoDB 的端口：

   ```
   27017
   ```

   27017 是分配给 MongoDB 的互联网 TCP 端口。

## 转发一个本地端口到 Pod 端口   {#forward-a-local-port-to-a-port-on-the-pod}

1. `kubectl port-forward` 允许使用资源名称
   （例如 Pod 名称）来选择匹配的 Pod 来进行端口转发。

   ```shell
   # 将 mongo-75f59d57f4-4nd6q 改为 Pod 的名称
   kubectl port-forward mongo-75f59d57f4-4nd6q 28015:27017
   ```

   这相当于

   ```shell
   kubectl port-forward pods/mongo-75f59d57f4-4nd6q 28015:27017
   ```

   或者

   ```shell
   kubectl port-forward deployment/mongo 28015:27017
   ```

   或者

   ```shell
   kubectl port-forward replicaset/mongo-75f59d57f4 28015:27017
   ```

   或者

   ```shell
   kubectl port-forward service/mongo 28015:27017
   ```

   以上所有命令都有效。输出类似于：

   ```
   Forwarding from 127.0.0.1:28015 -> 27017
   Forwarding from [::1]:28015 -> 27017
   ```

   {{< note >}}
   `kubectl port-forward` 不会返回。你需要打开另一个终端来继续这个练习。
   {{< /note >}}


2. 启动 MongoDB 命令行接口：

   ```shell
   mongosh --port 28015
   ```

3. 在 MongoDB 命令行提示符下，输入 `ping` 命令：

   ```
   db.runCommand( { ping: 1 } )
   ```

   成功的 ping 请求应该返回：

   ```
   { ok: 1 }
   ```

### （可选操作）让 _kubectl_ 来选择本地端口 {#let-kubectl-choose-local-port}

如果你不需要指定特定的本地端口，你可以让 `kubectl` 来选择和分配本地端口，
这样你就不需要管理本地端口冲突。该命令使用稍微不同的语法：

```shell
kubectl port-forward deployment/mongo :27017
```

`kubectl` 工具会找到一个未被使用的本地端口号（避免使用低段位的端口号，
因为他们可能会被其他应用程序使用）。输出类似于：

```
Forwarding from 127.0.0.1:63753 -> 27017
Forwarding from [::1]:63753 -> 27017
```


## 讨论  {#discussion}

与本地 28015 端口建立的连接将被转发到运行 MongoDB 服务器的 Pod 的 27017 端口。
通过此连接，你可以使用本地工作站来调试在 Pod 中运行的数据库。

{{< note >}}
`kubectl port-forward` 仅实现了 TCP 端口 支持。
在 [issue 47862](https://github.com/kubernetes/kubernetes/issues/47862)
中跟踪了对 UDP 协议的支持。
{{< /note >}}

## {{% heading "whatsnext" %}}

进一步了解 [kubectl port-forward](/docs/reference/generated/kubectl/kubectl-commands/#port-forward)。

