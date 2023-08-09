---
title: 在 Minikube 环境中使用 NGINX Ingress 控制器配置 Ingress
content_type: task
weight: 110
min-kubernetes-server-version: 1.19
---


[Ingress](/zh-cn/docs/concepts/services-networking/ingress/)是一种 API 对象，
其中定义了一些规则使得集群中的服务可以从集群外访问。
[Ingress 控制器](/zh-cn/docs/concepts/services-networking/ingress-controllers/)负责满足
Ingress 中所设置的规则。

本节为你展示如何配置一个简单的 Ingress，根据 HTTP URI 将服务请求路由到服务 `web` 或 `web2`。

## {{% heading "prerequisites" %}}

本教程假设你正在使用 `minikube` 运行一个本地 Kubernetes 集群。
参阅[安装工具](/zh-cn/docs/tasks/tools/#minikube)了解如何安装 `minikube`。

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

如果你使用的是较早的 Kubernetes 版本，请切换到该版本的文档。

### 创建一个 Minikube 集群  {#create-minikube-cluster}

如果你还未在本地搭建集群，运行 `minikube start` 创建集群。


## 启用 Ingress 控制器   {#enable-ingress-controller}

1. 为了启用 NGINIX Ingress 控制器，可以运行下面的命令：

   ```shell
   minikube addons enable ingress
   ```

2. 检查验证 NGINX Ingress 控制器处于运行状态：

   ```shell
   kubectl get pods -n ingress-nginx
   ```

   {{< note >}}
   最多可能需要等待一分钟才能看到这些 Pod 运行正常。
   {{< /note >}}

   输出类似于：

   ```none
   NAME                                        READY   STATUS      RESTARTS    AGE
   ingress-nginx-admission-create-g9g49        0/1     Completed   0          11m
   ingress-nginx-admission-patch-rqp78         0/1     Completed   1          11m
   ingress-nginx-controller-59b45fb494-26npt   1/1     Running     0          11m
   ```

## 部署一个 Hello World 应用  {#deploy-hello-world}

1. 使用下面的命令创建一个 Deployment：

   ```shell
   kubectl create deployment web --image=gcr.io/google-samples/hello-app:1.0
   ```

   输出：

   ```none
   deployment.apps/web created
   ```

2. 将 Deployment 暴露出来：

   ```shell
   kubectl expose deployment web --type=NodePort --port=8080
   ```

   输出类似于：

   ```none
   service/web exposed
   ```

3. 验证 Service 已经创建，并且可以从节点端口访问：

   ```shell
   kubectl get service web
   ```

   输出类似于：

   ```none
   NAME      TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   web       NodePort   10.104.133.249   <none>        8080:31637/TCP   12m
   ```

4. 使用节点端口信息访问服务：

   ```shell
   minikube service web --url
   ```

   输出类似于：

   ```none
   http://172.17.0.15:31637
   ```

   输出类似于：

   ```none
   Hello, world!
   Version: 1.0.0
   Hostname: web-55b8c6998d-8k564
   ```

   你现在应该可以通过 Minikube 的 IP 地址和节点端口来访问示例应用了。
   下一步是让自己能够通过 Ingress 资源来访问应用。

## 创建一个 Ingress   {#create-ingress}

下面是一个定义 Ingress 的配置文件，负责通过 `hello-world.info`
将请求转发到你的服务。

1. 根据下面的 YAML 创建文件 `example-ingress.yaml`：

   {{< codenew file="service/networking/example-ingress.yaml" >}}

2. 通过运行下面的命令创建 Ingress 对象：

   ```shell
   kubectl apply -f https://k8s.io/examples/service/networking/example-ingress.yaml
   ```

   输出类似于：

   ```none
   ingress.networking.k8s.io/example-ingress created
   ```

3. 验证 IP 地址已被设置：

   ```shell
   kubectl get ingress
   ```

   {{< note >}}
   此操作可能需要几分钟时间。
   {{< /note >}}

   接下来你将会在 `ADDRESS` 列中看到 IPv4 地址，例如：

   ```none
   NAME              CLASS    HOSTS              ADDRESS        PORTS   AGE
   example-ingress   <none>   hello-world.info   172.17.0.15    80      38s
   ```

4. 验证 Ingress 控制器能够转发请求流量：

   ```shell
   curl --resolve "hello-world.info:80:$( minikube ip )" -i http://hello-world.info
   ```

   你应该看到类似输出：

   ```none
   Hello, world!
   Version: 1.0.0
   Hostname: web-55b8c6998d-8k564
   ```


   你也可以从浏览器访问 `hello-world.info`。

   * **可选**

     查看 Minikube 报告的外部 IP 地址：

     ```shell
     minikube ip
     ```


     将类似以下这一行添加到你计算机上的  `/etc/hosts` 文件的末尾（需要管理员访问权限）：

     ```none
     172.17.0.15 hello-world.info
     ```

     {{< note >}}
     更改 IP 地址以匹配 `minikube ip` 的输出。
     {{< /note >}}


     更改完成后，在浏览器中访问 URL `hello-world.info`，请求将被发送到 Minikube。

## 创建第二个 Deployment  {#create-second-deployment}

1. 使用下面的命令创建第二个 Deployment：

   ```shell
   kubectl create deployment web2 --image=gcr.io/google-samples/hello-app:2.0
   ```

   输出类似于：

   ```none
   deployment.apps/web2 created
   ```

2. 将第二个 Deployment 暴露出来：

   ```shell
   kubectl expose deployment web2 --port=8080 --type=NodePort
   ```

   输出类似于：

   ```none
   service/web2 exposed
   ```

## 编辑现有的 Ingress {#edit-ingress}

1. 编辑现有的 `example-ingress.yaml`，在文件最后添加以下行：

   ```yaml
   - path: /v2
     pathType: Prefix
     backend:
       service:
         name: web2
         port:
           number: 8080
   ```

2. 应用变更：

   ```shell
   kubectl apply -f example-ingress.yaml
   ```

   输出类似于：

   ```none
   ingress.networking/example-ingress configured
   ```

## 测试你的 Ingress  {#test-ingress}

1. 访问 Hello World 应用的第一个版本：

   ```shell
   curl --resolve "hello-world.info:80:$( minikube ip )" -i http://hello-world.info
   ```

   输出类似于：

   ```none
   Hello, world!
   Version: 1.0.0
   Hostname: web-55b8c6998d-8k564
   ```

2. 访问 Hello World 应用的第二个版本：

   ```shell
   curl --resolve "hello-world.info:80:$( minikube ip )" -i http://hello-world.info/v2
   ```

   输出类似于：

   ```none
   Hello, world!
   Version: 2.0.0
   Hostname: web2-75cd47646f-t8cjk
   ```

   {{< note >}}
   如果你执行了更新 `/etc/hosts` 的可选步骤，你也可以从你的浏览器中访问
   `hello-world.info` 和 `hello-world.info/v2`。
   {{< /note >}}

## {{% heading "whatsnext" %}}

* 进一步了解 [Ingress](/zh-cn/docs/concepts/services-networking/ingress/)
* 进一步了解 [Ingress 控制器](/zh-cn/docs/concepts/services-networking/ingress-controllers/)
* 进一步了解[服务](/zh-cn/docs/concepts/services-networking/service/)
