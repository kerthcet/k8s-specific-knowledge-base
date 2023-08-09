---
title: 使用服务来访问集群中的应用
content_type: tutorial
weight: 60
---


本文展示如何创建一个 Kubernetes 服务对象，能让外部客户端访问在集群中运行的应用。
该服务为一个应用的两个运行实例提供负载均衡。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

## {{% heading "objectives" %}}

* 运行 Hello World 应用的两个实例。
* 创建一个服务对象来暴露 NodePort。
* 使用服务对象来访问正在运行的应用。


## 为运行在两个 Pod 中的应用创建一个服务   {#creating-a-service-for-an-app-running-in-two-pods}

这是应用程序部署的配置文件：

{{< codenew file="service/access/hello-application.yaml" >}}

1. 在你的集群中运行一个 Hello World 应用。
   使用上面的文件创建应用程序 Deployment：

   ```shell
   kubectl apply -f https://k8s.io/examples/service/access/hello-application.yaml
   ```


   上面的命令创建一个
   {{< glossary_tooltip text="Deployment" term_id="deployment" >}} 对象
   和一个关联的 {{< glossary_tooltip term_id="replica-set" text="ReplicaSet" >}} 对象。
   这个 ReplicaSet 有两个 {{< glossary_tooltip text="Pod" term_id="pod" >}}，
   每个 Pod 都运行着 Hello World 应用。

2. 展示 Deployment 的信息：

   ```shell
   kubectl get deployments hello-world
   kubectl describe deployments hello-world
   ```

3. 展示你的 ReplicaSet 对象信息：

   ```shell
   kubectl get replicasets
   kubectl describe replicasets
   ```

4. 创建一个服务对象来暴露 Deployment：

   ```shell
   kubectl expose deployment hello-world --type=NodePort --name=example-service
   ```

5. 展示 Service 信息：

   ```shell
   kubectl describe services example-service
   ```

   输出类似于：

   ```none
   Name:                   example-service
   Namespace:              default
   Labels:                 run=load-balancer-example
   Annotations:            <none>
   Selector:               run=load-balancer-example
   Type:                   NodePort
   IP:                     10.32.0.16
   Port:                   <unset> 8080/TCP
   TargetPort:             8080/TCP
   NodePort:               <unset> 31496/TCP
   Endpoints:              10.200.1.4:8080,10.200.2.5:8080
   Session Affinity:       None
   Events:                 <none>
   ```

   注意服务中的 NodePort 值。例如在上面的输出中，NodePort 值是 31496。

6. 列出运行 Hello World 应用的 Pod：

   ```shell
   kubectl get pods --selector="run=load-balancer-example" --output=wide
   ```


   输出类似于：

   ```none
   NAME                           READY   STATUS    ...  IP           NODE
   hello-world-2895499144-bsbk5   1/1     Running   ...  10.200.1.4   worker1
   hello-world-2895499144-m1pwt   1/1     Running   ...  10.200.2.5   worker2
   ```

7. 获取运行 Hello World 的 pod 的其中一个节点的公共 IP 地址。如何获得此地址取决于你设置集群的方式。
   例如，如果你使用的是 Minikube，则可以通过运行 `kubectl cluster-info` 来查看节点地址。
   如果你使用的是 Google Compute Engine 实例，
   则可以使用 `gcloud compute instances list` 命令查看节点的公共地址。

8. 在你选择的节点上，创建一个防火墙规则以开放节点端口上的 TCP 流量。
   例如，如果你的服务的 NodePort 值为 31568，请创建一个防火墙规则以允许 31568 端口上的 TCP 流量。
   不同的云提供商提供了不同方法来配置防火墙规则。

9. 使用节点地址和 node port 来访问 Hello World 应用：

   ```shell
   curl http://<public-node-ip>:<node-port>
   ```

   这里的 `<public-node-ip>` 是你节点的公共 IP 地址，`<node-port>` 是你服务的 NodePort 值。
   对于请求成功的响应是一个 hello 消息：

   ```none
   Hello Kubernetes!
   ```

## 使用服务配置文件   {#using-a-service-configuration-file}

作为 `kubectl expose` 的替代方法，
你可以使用[服务配置文件](/zh-cn/docs/concepts/services-networking/service/)来创建服务。

## {{% heading "cleanup" %}}

想要删除服务，输入以下命令：

```shell
kubectl delete services example-service
```

想要删除运行 Hello World 应用的 Deployment、ReplicaSet 和 Pod，输入以下命令：

```shell
kubectl delete deployment hello-world
```

## {{% heading "whatsnext" %}}

跟随教程[使用 Service 连接到应用](/zh-cn/docs/tutorials/services/connect-applications-service/)。
