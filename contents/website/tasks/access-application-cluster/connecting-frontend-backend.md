---
title: 使用 Service 把前端连接到后端
content_type: tutorial
weight: 70
---



本任务会描述如何创建前端（Frontend）微服务和后端（Backend）微服务。后端微服务是一个 hello 欢迎程序。
前端通过 nginx 和一个 Kubernetes {{< glossary_tooltip term_id="service" text="服务" >}}
暴露后端所提供的服务。

## {{% heading "objectives" %}}

* 使用部署对象（Deployment object）创建并运行一个 `hello` 后端微服务
* 使用一个 Service 对象将请求流量发送到后端微服务的多个副本
* 同样使用一个 Deployment 对象创建并运行一个 `nginx` 前端微服务
* 配置前端微服务将请求流量发送到后端微服务
* 使用 `type=LoadBalancer` 的 Service 对象将前端微服务暴露到集群外部

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

本任务使用[外部负载均衡服务](/zh-cn/docs/tasks/access-application-cluster/create-external-load-balancer/)，
所以需要对应的可支持此功能的环境。如果你的环境不能支持，你可以使用
[NodePort](/zh-cn/docs/concepts/services-networking/service/#type-nodeport)
类型的服务代替。


### 使用部署对象（Deployment）创建后端   {#creating-the-backend-using-a-deployment}

后端是一个简单的 hello 欢迎微服务应用。这是后端应用的 Deployment 配置文件：

{{< codenew file="service/access/backend-deployment.yaml" >}}

创建后端 Deployment：

```shell
kubectl apply -f https://k8s.io/examples/service/access/backend-deployment.yaml
```

查看后端的 Deployment 信息：

```shell
kubectl describe deployment backend
```

输出类似于：

```
Name:                           backend
Namespace:                      default
CreationTimestamp:              Mon, 24 Oct 2016 14:21:02 -0700
Labels:                         app=hello
                                tier=backend
                                track=stable
Annotations:                    deployment.kubernetes.io/revision=1
Selector:                       app=hello,tier=backend,track=stable
Replicas:                       3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:                   RollingUpdate
MinReadySeconds:                0
RollingUpdateStrategy:          1 max unavailable, 1 max surge
Pod Template:
  Labels:       app=hello
                tier=backend
                track=stable
  Containers:
   hello:
    Image:              "gcr.io/google-samples/hello-go-gke:1.0"
    Port:               80/TCP
    Environment:        <none>
    Mounts:             <none>
  Volumes:              <none>
Conditions:
  Type          Status  Reason
  ----          ------  ------
  Available     True    MinimumReplicasAvailable
  Progressing   True    NewReplicaSetAvailable
OldReplicaSets:                 <none>
NewReplicaSet:                  hello-3621623197 (3/3 replicas created)
Events:
...
```

### 创建 `hello` Service 对象   {#creating-the-hello-service-object}

将请求从前端发送到后端的关键是后端 Service。Service 创建一个固定 IP 和 DNS 解析名入口，
使得后端微服务总是可达。Service 使用
{{< glossary_tooltip text="选择算符" term_id="selector" >}} 
来寻找目标 Pod。

首先，浏览 Service 的配置文件：

{{< codenew file="service/access/backend-service.yaml" >}}

配置文件中，你可以看到名为 `hello` 的 Service 将流量路由到包含 `app: hello`
和 `tier: backend` 标签的 Pod。

创建后端 Service：

```shell
kubectl apply -f https://k8s.io/examples/service/access/backend-service.yaml
```

此时，你已经有了一个运行着 `hello` 应用的三个副本的 `backend` Deployment，你也有了
一个 Service 用于路由网络流量。不过，这个服务在集群外部无法访问也无法解析。

### 创建前端   {#creating-the-frontend}

现在你已经有了运行中的后端应用，你可以创建一个可在集群外部访问的前端，并通过代理
前端的请求连接到后端。

前端使用被赋予后端 Service 的 DNS 名称将请求发送到后端工作 Pods。这一 DNS
名称为 `hello`，也就是 `examples/service/access/backend-service.yaml` 配置
文件中 `name` 字段的取值。

前端 Deployment 中的 Pods 运行一个 nginx 镜像，这个已经配置好的镜像会将请求转发
给后端的 `hello` Service。下面是  nginx 的配置文件：

{{< codenew file="service/access/frontend-nginx.conf" >}}

与后端类似，前端用包含一个 Deployment 和一个 Service。后端与前端服务之间的一个
重要区别是前端 Service 的配置文件包含了 `type: LoadBalancer`，也就是说，Service
会使用你的云服务商的默认负载均衡设备，从而实现从集群外访问的目的。

{{< codenew file="service/access/frontend-service.yaml" >}}

{{< codenew file="service/access/frontend-deployment.yaml" >}}


创建前端 Deployment 和 Service：

```shell
kubectl apply -f https://k8s.io/examples/service/access/frontend-deployment.yaml
kubectl apply -f https://k8s.io/examples/service/access/frontend-service.yaml
```

通过输出确认两个资源都已经被创建：

```
deployment.apps/frontend created
service/frontend created
```

{{< note >}}
这个 nginx 配置文件是被打包在
[容器镜像](/examples/service/access/Dockerfile) 里的。
更好的方法是使用
[ConfigMap](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/)，
这样的话你可以更轻易地更改配置。
{{< /note >}}

### 与前端 Service 交互   {#interact-with-the-frontend-service}

一旦你创建了 LoadBalancer 类型的 Service，你可以使用这条命令查看外部 IP：

```shell
kubectl get service frontend --watch
```

外部 IP 字段的生成可能需要一些时间。如果是这种情况，外部 IP 会显示为 `<pending>`。

```
NAME       TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)  AGE
frontend   LoadBalancer   10.51.252.116   <pending>     80/TCP   10s
```

当外部 IP 地址被分配可用时，配置会更新，在 `EXTERNAL-IP` 头部下显示新的 IP：

```
NAME       TYPE           CLUSTER-IP      EXTERNAL-IP        PORT(S)  AGE
frontend   LoadBalancer   10.51.252.116   XXX.XXX.XXX.XXX    80/TCP   1m
```

这一新的 IP 地址就可以用来从集群外与 `frontend` 服务交互了。


### 通过前端发送流量   {#send-traffic-through-the-frontend}

前端和后端已经完成连接了。你可以使用 curl 命令通过你的前端 Service 的外部
IP 访问服务端点。

```shell
curl http://${EXTERNAL_IP} # 将 EXTERNAL_IP 替换为你之前看到的外部 IP
```

输出显示后端生成的消息：

```json
{"message":"Hello"}
```

## {{% heading "cleanup" %}}

要删除服务，输入下面的命令：

```shell
kubectl delete services frontend backend
```

要删除在前端和后端应用中运行的 Deployment、ReplicaSet 和 Pod，输入下面的命令：

```shell
kubectl delete deployment frontend backend
```

## {{% heading "whatsnext" %}}

* 进一步了解 [Service](/zh-cn/docs/concepts/services-networking/service/)
* 进一步了解 [ConfigMap](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/)
* 进一步了解 [Service 和 Pods 的 DNS](/zh-cn/docs/concepts/services-networking/dns-pod-service/)
