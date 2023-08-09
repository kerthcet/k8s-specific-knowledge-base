---
title: 你好，Minikube
content_type: tutorial
weight: 5
menu:
  main:
    title: "Get Started"
    weight: 10
    post: >
      <p>准备好动手操作了么？构建一个简单的 Kubernetes 集群来运行示例应用。</p>
card:
  name: tutorials
  weight: 10
---


本教程向你展示如何使用 Minikube 在 Kubernetes 上运行一个应用示例。
教程提供了容器镜像，使用 NGINX 来对所有请求做出回应。

## {{% heading "objectives" %}}

* 将一个示例应用部署到 Minikube。
* 运行应用程序。
* 查看应用日志。

## {{% heading "prerequisites" %}}

本教程假设你已经安装了 `minikube`。
有关安装说明，请参阅 [minikube start](https://minikube.sigs.k8s.io/docs/start/)。

你还需要安装 `kubectl`。
有关安装说明，请参阅[安装工具](/zh-cn/docs/tasks/tools/#kubectl)。


## 创建 Minikube 集群  {#create-a-minikube-cluster}

```shell
minikube start
```

## 打开仪表板  {#open-the-dashboard}

打开 Kubernetes 仪表板。你可以通过两种不同的方式执行此操作：

{{< tabs name="dashboard" >}}
{{% tab name="启动浏览器" %}}
打开一个**新的**终端，然后运行：
```shell
# 启动一个新的终端，并保持此命令运行。
minikube dashboard
```

现在，切换回运行 `minikube start` 的终端。

{{< note >}}
`dashboard` 命令启用仪表板插件，并在默认的 Web 浏览器中打开代理。
你可以在仪表板上创建 Kubernetes 资源，例如 Deployment 和 Service。

如果你以 root 用户身份在环境中运行，
请参见[使用 URL 打开仪表板](#open-dashboard-with-url)。

默认情况下，仪表板只能从内部 Kubernetes 虚拟网络中访问。
`dashboard` 命令创建一个临时代理，使仪表板可以从 Kubernetes 虚拟网络外部访问。

要停止代理，请运行 `Ctrl+C` 退出该进程。仪表板仍在运行中。
命令退出后，仪表板仍然在 Kubernetes 集群中运行。
你可以再次运行 `dashboard` 命令创建另一个代理来访问仪表板。
{{< /note >}}

{{% /tab %}}
{{% tab name="URL 复制粘贴" %}}

如果你不想 Minikube 为你打开 Web 浏览器，可以使用 `--url` 标志运行仪表板命令。
`minikube` 会输出一个 URL，你可以在你喜欢的浏览器中打开该 URL。

打开一个**新的**终端，然后运行：

```shell
# 启动一个新的终端，并保持此命令运行。
minikube dashboard --url
```

现在，切换回运行 `minikube start` 的终端。

{{% /tab %}}
{{< /tabs >}}

## 创建 Deployment  {#create-a-deployment}

Kubernetes [**Pod**](/zh-cn/docs/concepts/workloads/pods/)
是由一个或多个为了管理和联网而绑定在一起的容器构成的组。本教程中的 Pod 只有一个容器。
Kubernetes [**Deployment**](/zh-cn/docs/concepts/workloads/controllers/deployment/)
检查 Pod 的健康状况，并在 Pod 中的容器终止的情况下重新启动新的容器。
Deployment 是管理 Pod 创建和扩展的推荐方法。

1. 使用 `kubectl create` 命令创建管理 Pod 的 Deployment。该 Pod 根据提供的 Docker
   镜像运行容器。

   ```shell
   # 运行包含 Web 服务器的测试容器镜像
   kubectl create deployment hello-node --image=registry.k8s.io/e2e-test-images/agnhost:2.39 -- /agnhost netexec --http-port=8080
   ```

2. 查看 Deployment：

   ```shell
   kubectl get deployments
   ```


   输出结果类似于这样：

   ```
   NAME         READY   UP-TO-DATE   AVAILABLE   AGE
   hello-node   1/1     1            1           1m
   ```

3. 查看 Pod：

   ```shell
   kubectl get pods
   ```


   输出结果类似于这样：

   ```
   NAME                          READY     STATUS    RESTARTS   AGE
   hello-node-5f76cf6ccf-br9b5   1/1       Running   0          1m
   ```

4. 查看集群事件：

   ```shell
   kubectl get events
   ```

5. 查看 `kubectl` 配置：

   ```shell
   kubectl config view
   ```

{{< note >}}
有关 `kubectl` 命令的更多信息，请参阅 [kubectl 概述](/zh-cn/docs/reference/kubectl/)。
{{< /note >}}

## 创建 Service  {#create-a-service}

默认情况下，Pod 只能通过 Kubernetes 集群中的内部 IP 地址访问。
要使得 `hello-node` 容器可以从 Kubernetes 虚拟网络的外部访问，你必须将 Pod
暴露为 Kubernetes [**Service**](/zh-cn/docs/concepts/services-networking/service/)。

1. 使用 `kubectl expose` 命令将 Pod 暴露给公网：

   ```shell
   kubectl expose deployment hello-node --type=LoadBalancer --port=8080
   ```


   这里的 `--type=LoadBalancer` 参数表明你希望将你的 Service 暴露到集群外部。

   测试镜像中的应用程序代码仅监听 TCP 8080 端口。
   如果你用 `kubectl expose` 暴露了其它的端口，客户端将不能访问其它端口。

2. 查看你创建的 Service：

   ```shell
   kubectl get services
   ```


   输出结果类似于这样:

   ```
   NAME         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
   hello-node   LoadBalancer   10.108.144.78   <pending>     8080:30369/TCP   21s
   kubernetes   ClusterIP      10.96.0.1       <none>        443/TCP          23m
   ```


   对于支持负载均衡器的云服务平台而言，平台将提供一个外部 IP 来访问该服务。
   在 Minikube 上，`LoadBalancer` 使得服务可以通过命令 `minikube service` 访问。

3. 运行下面的命令：

   ```shell
   minikube service hello-node
   ```

   这将打开一个浏览器窗口，为你的应用程序提供服务并显示应用的响应。

## 启用插件   {#enable-addons}

Minikube 有一组内置的{{< glossary_tooltip text="插件" term_id="addons" >}}，
可以在本地 Kubernetes 环境中启用、禁用和打开。

1. 列出当前支持的插件：

   ```shell
   minikube addons list
   ```

   输出结果类似于这样：

   ```
   addon-manager: enabled
   dashboard: enabled
   default-storageclass: enabled
   efk: disabled
   freshpod: disabled
   gvisor: disabled
   helm-tiller: disabled
   ingress: disabled
   ingress-dns: disabled
   logviewer: disabled
   metrics-server: disabled
   nvidia-driver-installer: disabled
   nvidia-gpu-device-plugin: disabled
   registry: disabled
   registry-creds: disabled
   storage-provisioner: enabled
   storage-provisioner-gluster: disabled
   ```

2. 启用插件，例如 `metrics-server`：

   ```shell
   minikube addons enable metrics-server
   ```


   输出结果类似于这样：

   ```
   The 'metrics-server' addon is enabled
   ```

3. 查看通过安装该插件所创建的 Pod 和 Service：

   ```shell
   kubectl get pod,svc -n kube-system
   ```


   输出结果类似于这样：

   ```
   NAME                                        READY     STATUS    RESTARTS   AGE
   pod/coredns-5644d7b6d9-mh9ll                1/1       Running   0          34m
   pod/coredns-5644d7b6d9-pqd2t                1/1       Running   0          34m
   pod/metrics-server-67fb648c5                1/1       Running   0          26s
   pod/etcd-minikube                           1/1       Running   0          34m
   pod/influxdb-grafana-b29w8                  2/2       Running   0          26s
   pod/kube-addon-manager-minikube             1/1       Running   0          34m
   pod/kube-apiserver-minikube                 1/1       Running   0          34m
   pod/kube-controller-manager-minikube        1/1       Running   0          34m
   pod/kube-proxy-rnlps                        1/1       Running   0          34m
   pod/kube-scheduler-minikube                 1/1       Running   0          34m
   pod/storage-provisioner                     1/1       Running   0          34m

   NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)             AGE
   service/metrics-server         ClusterIP   10.96.241.45    <none>        80/TCP              26s
   service/kube-dns               ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP       34m
   service/monitoring-grafana     NodePort    10.99.24.54     <none>        80:30002/TCP        26s
   service/monitoring-influxdb    ClusterIP   10.111.169.94   <none>        8083/TCP,8086/TCP   26s
   ```

4. 禁用 `metrics-server`：

   ```shell
   minikube addons disable metrics-server
   ```


   输出结果类似于这样：

   ```
   metrics-server was successfully disabled
   ```

## 清理  {#clean-up}

现在可以清理你在集群中创建的资源：

```shell
kubectl delete service hello-node
kubectl delete deployment hello-node
```

停止 Minikube 集群：

```shell
minikube stop
```

可选地，删除 Minikube 虚拟机（VM）：

```shell
# 可选的
minikube delete
```

如果你还想使用 Minikube 进一步学习 Kubernetes，那就不需要删除 Minikube。

## {{% heading "whatsnext" %}}

* 进一步了解 [Deployment 对象](/zh-cn/docs/concepts/workloads/controllers/deployment/)。
* 进一步了解[部署应用](/zh-cn/docs/tasks/run-application/run-stateless-application-deployment/)。
* 进一步了解 [Service 对象](/zh-cn/docs/concepts/services-networking/service/)。

