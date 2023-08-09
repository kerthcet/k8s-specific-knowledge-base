---
title: 公开外部 IP 地址以访问集群中应用程序
content_type: tutorial
weight: 10
---


此页面显示如何创建公开外部 IP 地址的 Kubernetes 服务对象。

## {{% heading "prerequisites" %}}

* 安装 [kubectl](/zh-cn/docs/tasks/tools/)。
* 使用 Google Kubernetes Engine 或 Amazon Web Services 等云供应商创建 Kubernetes 集群。
  本教程创建了一个[外部负载均衡器](/zh-cn/docs/tasks/access-application-cluster/create-external-load-balancer/)，
  需要云供应商。
* 配置 `kubectl` 与 Kubernetes API 服务器通信。有关说明，请参阅云供应商文档。

## {{% heading "objectives" %}}

* 运行 Hello World 应用程序的五个实例。
* 创建一个公开外部 IP 地址的 Service 对象。
* 使用 Service 对象访问正在运行的应用程序。


## 为一个在五个 pod 中运行的应用程序创建服务   {#creating-a-service-for-an-app-running-in-five-pods}

1. 在集群中运行 Hello World 应用程序：

   {{< codenew file="service/load-balancer-example.yaml" >}}

   ```shell
   kubectl apply -f https://k8s.io/examples/service/load-balancer-example.yaml
   ```

   
   前面的命令创建一个
   {{< glossary_tooltip text="Deployment" term_id="deployment" >}}
   对象和一个关联的
   {{< glossary_tooltip term_id="replica-set" text="ReplicaSet" >}} 对象。
   ReplicaSet 有五个 {{< glossary_tooltip text="Pod" term_id="pod" >}}，
   每个都运行 Hello World 应用程序。

2. 显示有关 Deployment 的信息：

   ```shell
   kubectl get deployments hello-world
   kubectl describe deployments hello-world
   ```

3. 显示有关 ReplicaSet 对象的信息：

   ```shell
   kubectl get replicasets
   kubectl describe replicasets
   ```

4. 创建公开 Deployment 的 Service 对象：

   ```shell
   kubectl expose deployment hello-world --type=LoadBalancer --name=my-service
   ```

5. 显示有关 Service 的信息：

   ```shell
   kubectl get services my-service
   ```


   输出类似于：

   ```console
   NAME         TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)    AGE
   my-service   LoadBalancer   10.3.245.137   104.198.205.71   8080/TCP   54s
   ```

   {{< note >}}
   `type=LoadBalancer` 服务由外部云服务提供商提供支持，本例中不包含此部分，
   详细信息请参考[此页](/zh-cn/docs/concepts/services-networking/service/#loadbalancer)
   {{< /note >}}

   {{< note >}}
   如果外部 IP 地址显示为 \<pending\>，请等待一分钟再次输入相同的命令。
   {{< /note >}}

6. 显示有关 Service 的详细信息：

   ```shell
   kubectl describe services my-service
   ```


   输出类似于：

   ```console
   Name:           my-service
   Namespace:      default
   Labels:         app.kubernetes.io/name=load-balancer-example
   Annotations:    <none>
   Selector:       app.kubernetes.io/name=load-balancer-example
   Type:           LoadBalancer
   IP:             10.3.245.137
   LoadBalancer Ingress:   104.198.205.71
   Port:           <unset> 8080/TCP
   NodePort:       <unset> 32377/TCP
   Endpoints:      10.0.0.6:8080,10.0.1.6:8080,10.0.1.7:8080 + 2 more...
   Session Affinity:   None
   Events:         <none>
   ```


   记下服务公开的外部 IP 地址（`LoadBalancer Ingress`）。
   在本例中，外部 IP 地址是 104.198.205.71。还要注意 `Port` 和 `NodePort` 的值。
   在本例中，`Port` 是 8080，`NodePort` 是 32377。

7. 在前面的输出中，你可以看到服务有几个端点：
   10.0.0.6:8080、10.0.1.6:8080、10.0.1.7:8080 和另外两个，
   这些都是正在运行 Hello World 应用程序的 Pod 的内部地址。
   要验证这些是 Pod 地址，请输入以下命令：

   ```shell
   kubectl get pods --output=wide
   ```


   输出类似于：

   ```console
   NAME                         ...  IP         NODE
   hello-world-2895499144-1jaz9 ...  10.0.1.6   gke-cluster-1-default-pool-e0b8d269-1afc
   hello-world-2895499144-2e5uh ...  10.0.1.8   gke-cluster-1-default-pool-e0b8d269-1afc
   hello-world-2895499144-9m4h1 ...  10.0.0.6   gke-cluster-1-default-pool-e0b8d269-5v7a
   hello-world-2895499144-o4z13 ...  10.0.1.7   gke-cluster-1-default-pool-e0b8d269-1afc
   hello-world-2895499144-segjf ...  10.0.2.5   gke-cluster-1-default-pool-e0b8d269-cpuc
   ```
8. 使用外部 IP 地址（`LoadBalancer Ingress`）访问 Hello World 应用程序:

   ```shell
   curl http://<external-ip>:<port>
   ```


   其中 `<external-ip>` 是你的服务的外部 IP 地址（`LoadBalancer Ingress`），
   `<port>` 是你的服务描述中的 `port` 的值。
   如果你正在使用 minikube，输入 `minikube service my-service`
   将在浏览器中自动打开 Hello World 应用程序。


   成功请求的响应是一条问候消息：

   ```shell
   Hello Kubernetes!
   ```

## {{% heading "cleanup" %}}

要删除 Service，请输入以下命令：

```shell
kubectl delete services my-service
```

要删除正在运行 Hello World 应用程序的 Deployment、ReplicaSet 和 Pod，请输入以下命令：

```shell
kubectl delete deployment hello-world
```

## {{% heading "whatsnext" %}}

进一步了解[使用 Service 连接到应用](/zh-cn/docs/tutorials/services/connect-applications-service/)。
