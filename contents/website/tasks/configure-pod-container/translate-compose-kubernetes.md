---
title: 将 Docker Compose 文件转换为 Kubernetes 资源
content_type: task
weight: 230
---


Kompose 是什么？它是一个转换工具，可将 compose
（即 Docker Compose）所组装的所有内容转换成容器编排器（Kubernetes 或 OpenShift）可识别的形式。

更多信息请参考 Kompose 官网 [http://kompose.io](http://kompose.io)。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


## 安装 Kompose    {#install-kompose}

我们有很多种方式安装 Kompose。首选方式是从最新的 GitHub 发布页面下载二进制文件。

{{< tabs name="install_ways" >}}
{{% tab name="GitHub 下载" %}}

Kompose 通过 GitHub 发布，发布周期为三星期。
你可以在 [GitHub 发布页面](https://github.com/kubernetes/kompose/releases)上看到所有当前版本。

```shell
# Linux
curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.0/kompose-linux-amd64 -o kompose

# macOS
curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.0/kompose-darwin-amd64 -o kompose

# Windows
curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.0/kompose-windows-amd64.exe -o kompose.exe

chmod +x kompose
sudo mv ./kompose /usr/local/bin/kompose
```

或者，你可以下载 [tar 包](https://github.com/kubernetes/kompose/releases)。

{{% /tab %}}
{{% tab name="基于源代码构建" %}}

用 `go get` 命令从主分支拉取最新的开发变更的方法安装 Kompose。

```shell
go get -u github.com/kubernetes/kompose
```

{{% /tab %}}
{{% tab name="CentOS 包" %}}

Kompose 位于 [EPEL](https://fedoraproject.org/wiki/EPEL) CentOS 代码仓库。
如果你还没有安装并启用 [EPEL](https://fedoraproject.org/wiki/EPEL) 代码仓库，
请运行命令 `sudo yum install epel-release`。

如果你的系统中已经启用了 [EPEL](https://fedoraproject.org/wiki/EPEL)，
你就可以像安装其他软件包一样安装 Kompose。

```bash
sudo yum -y install kompose
```

{{% /tab %}}
{{% tab name="Fedora 包" %}}

Kompose 位于 Fedora 24、25 和 26 的代码仓库。你可以像安装其他软件包一样安装 Kompose。

```bash
sudo dnf -y install kompose
```

{{% /tab %}}
{{% tab name="Homebrew (macOS)" %}}

在 macOS 上你可以通过 [Homebrew](https://brew.sh) 安装 Kompose 的最新版本：

```bash
brew install kompose
```

{{% /tab %}}
{{< /tabs >}}

## 使用 Kompose    {#use-kompose}

只需几步，我们就把你从 Docker Compose 带到 Kubernetes。
你只需要一个现有的 `docker-compose.yml` 文件。

1. 进入 `docker-compose.yml` 文件所在的目录。如果没有，请使用下面这个进行测试。

   ```yaml
   version: "2"

   services:

     redis-master:
       image: registry.k8s.io/redis:e2e
       ports:
         - "6379"

     redis-slave:
       image: gcr.io/google_samples/gb-redisslave:v3
       ports:
         - "6379"
       environment:
         - GET_HOSTS_FROM=dns

     frontend:
       image: gcr.io/google-samples/gb-frontend:v4
       ports:
         - "80:80"
       environment:
         - GET_HOSTS_FROM=dns
       labels:
         kompose.service.type: LoadBalancer
   ```

2. 要将 `docker-compose.yml` 转换为 `kubectl` 可用的文件，请运行 `kompose convert`
   命令进行转换，然后运行 `kubectl apply -f <output file>` 进行创建。

   ```bash
   kompose convert                           
   ```

   输出类似于：

   ```none
   INFO Kubernetes file "frontend-tcp-service.yaml" created 
   INFO Kubernetes file "redis-master-service.yaml" created 
   INFO Kubernetes file "redis-slave-service.yaml" created 
   INFO Kubernetes file "frontend-deployment.yaml" created 
   INFO Kubernetes file "redis-master-deployment.yaml" created 
   INFO Kubernetes file "redis-slave-deployment.yaml" created
   ```

   ```bash
   kubectl apply -f frontend-tcp-service.yaml,redis-master-service.yaml,redis-slave-service.yaml,frontend-deployment.yaml,redis-master-deployment.yaml,redis-slave-deployment.yaml
   ```

   输出类似于：

   ```none
   service/frontend-tcp created
   service/redis-master created
   service/redis-slave created
   deployment.apps/frontend created
   deployment.apps/redis-master created
   deployment.apps/redis-slave created
   ```

   你部署的应用在 Kubernetes 中运行起来了。

3. 访问你的应用。


   如果你在开发过程中使用 `minikube`，请执行：

   ```bash
   minikube service frontend
   ```

   否则，我们要查看一下你的服务使用了什么 IP！

   ```sh
   kubectl describe svc frontend
   ```

   ```none
   Name:                     frontend-tcp
   Namespace:                default
   Labels:                   io.kompose.service=frontend-tcp
   Annotations:              kompose.cmd: kompose convert
                             kompose.service.type: LoadBalancer
                             kompose.version: 1.26.0 (40646f47)
   Selector:                 io.kompose.service=frontend
   Type:                     LoadBalancer
   IP Family Policy:         SingleStack
   IP Families:              IPv4
   IP:                       10.43.67.174
   IPs:                      10.43.67.174
   Port:                     80  80/TCP
   TargetPort:               80/TCP
   NodePort:                 80  31254/TCP
   Endpoints:                10.42.0.25:80
   Session Affinity:         None
   External Traffic Policy:  Cluster
   Events:
     Type    Reason                Age   From                Message
     ----    ------                ----  ----                -------
     Normal  EnsuringLoadBalancer  62s   service-controller  Ensuring load balancer
     Normal  AppliedDaemonSet      62s   service-controller  Applied LoadBalancer DaemonSet kube-system/svclb-frontend-tcp-9362d276
   ```

   如果你使用的是云驱动，你的 IP 将在 `LoadBalancer Ingress` 字段给出。

   ```sh
   curl http://192.0.2.89
   ```

4. 清理。

   你完成示例应用 Deployment 的测试之后，只需在 Shell 中运行以下命令，就能删除用过的资源。

   ```sh
   kubectl delete -f frontend-tcp-service.yaml,redis-master-service.yaml,redis-slave-service.yaml,frontend-deployment.yaml,redis-master-deployment.yaml,redis-slave-deployment.yaml
   ```


## 用户指南  {#user-guide}

- CLI
  - [`kompose convert`](#kompose-convert)

- 文档
  - [其他转换方式](#alternative-conversions)
  - [标签](#labels)
  - [重启](#restart)
  - [Docker Compose 版本](#docker-compose-versions)

Kompose 支持两种驱动：OpenShift 和 Kubernetes。
你可以通过全局选项 `--provider` 选择驱动。如果没有指定，
会将 Kubernetes 作为默认驱动。

## `kompose convert`

Kompose 支持将 V1、V2 和 V3 版本的 Docker Compose 文件转换为 Kubernetes 和 OpenShift 资源对象。

### Kubernetes `kompose convert` 示例    {#kubernetes-kompose-convert-example}

```shell
kompose --file docker-voting.yml convert
```

```none
WARN Unsupported key networks - ignoring
WARN Unsupported key build - ignoring
INFO Kubernetes file "worker-svc.yaml" created
INFO Kubernetes file "db-svc.yaml" created
INFO Kubernetes file "redis-svc.yaml" created
INFO Kubernetes file "result-svc.yaml" created
INFO Kubernetes file "vote-svc.yaml" created
INFO Kubernetes file "redis-deployment.yaml" created
INFO Kubernetes file "result-deployment.yaml" created
INFO Kubernetes file "vote-deployment.yaml" created
INFO Kubernetes file "worker-deployment.yaml" created
INFO Kubernetes file "db-deployment.yaml" created
```

```shell
ls
```

```none
db-deployment.yaml  docker-compose.yml         docker-gitlab.yml  redis-deployment.yaml  result-deployment.yaml  vote-deployment.yaml  worker-deployment.yaml
db-svc.yaml         docker-voting.yml          redis-svc.yaml     result-svc.yaml        vote-svc.yaml           worker-svc.yaml
```

你也可以同时提供多个 docker-compose 文件进行转换：

```shell
kompose -f docker-compose.yml -f docker-guestbook.yml convert
```

```none
INFO Kubernetes file "frontend-service.yaml" created         
INFO Kubernetes file "mlbparks-service.yaml" created         
INFO Kubernetes file "mongodb-service.yaml" created          
INFO Kubernetes file "redis-master-service.yaml" created     
INFO Kubernetes file "redis-slave-service.yaml" created      
INFO Kubernetes file "frontend-deployment.yaml" created      
INFO Kubernetes file "mlbparks-deployment.yaml" created      
INFO Kubernetes file "mongodb-deployment.yaml" created       
INFO Kubernetes file "mongodb-claim0-persistentvolumeclaim.yaml" created
INFO Kubernetes file "redis-master-deployment.yaml" created  
INFO Kubernetes file "redis-slave-deployment.yaml" created   
```

```shell
ls
```

```none
mlbparks-deployment.yaml  mongodb-service.yaml                       redis-slave-service.jsonmlbparks-service.yaml  
frontend-deployment.yaml  mongodb-claim0-persistentvolumeclaim.yaml  redis-master-service.yaml
frontend-service.yaml     mongodb-deployment.yaml                    redis-slave-deployment.yaml
redis-master-deployment.yaml
```

当提供多个 docker-compose 文件时，配置将会合并。任何通用的配置都将被后续文件覆盖。

### OpenShift `kompose convert` 示例    {#openshift-kompose-convert-example}

```sh
kompose --provider openshift --file docker-voting.yml convert
```

```none
WARN [worker] Service cannot be created because of missing port.
INFO OpenShift file "vote-service.yaml" created             
INFO OpenShift file "db-service.yaml" created               
INFO OpenShift file "redis-service.yaml" created            
INFO OpenShift file "result-service.yaml" created           
INFO OpenShift file "vote-deploymentconfig.yaml" created    
INFO OpenShift file "vote-imagestream.yaml" created         
INFO OpenShift file "worker-deploymentconfig.yaml" created  
INFO OpenShift file "worker-imagestream.yaml" created       
INFO OpenShift file "db-deploymentconfig.yaml" created      
INFO OpenShift file "db-imagestream.yaml" created           
INFO OpenShift file "redis-deploymentconfig.yaml" created   
INFO OpenShift file "redis-imagestream.yaml" created        
INFO OpenShift file "result-deploymentconfig.yaml" created  
INFO OpenShift file "result-imagestream.yaml" created  
```

kompose 还支持为服务中的构建指令创建 buildconfig。
默认情况下，它使用当前 git 分支的 remote 仓库作为源仓库，使用当前分支作为构建的源分支。
你可以分别使用 ``--build-repo`` 和 ``--build-branch`` 选项指定不同的源仓库和分支。

```sh
kompose --provider openshift --file buildconfig/docker-compose.yml convert
```

```none
WARN [foo] Service cannot be created because of missing port.
INFO OpenShift Buildconfig using git@github.com:rtnpro/kompose.git::master as source.
INFO OpenShift file "foo-deploymentconfig.yaml" created     
INFO OpenShift file "foo-imagestream.yaml" created          
INFO OpenShift file "foo-buildconfig.yaml" created
```

{{< note >}}
如果使用 ``oc create -f`` 手动推送 OpenShift 工件，则需要确保在构建配置工件之前推送
imagestream 工件，以解决 OpenShift 的这个问题： https://github.com/openshift/origin/issues/4518。
{{< /note >}}

## 其他转换方式    {#alternative-conversions}

默认的 `kompose` 转换会生成 yaml 格式的 Kubernetes
[Deployment](/zh-cn/docs/concepts/workloads/controllers/deployment/) 和
[Service](/zh-cn/docs/concepts/services-networking/service/) 对象。
你可以选择通过 `-j` 参数生成 json 格式的对象。
你也可以替换生成 [Replication Controllers](/zh-cn/docs/concepts/workloads/controllers/replicationcontroller/) 对象、
[DaemonSet](/zh-cn/docs/concepts/workloads/controllers/daemonset/) 或
[Helm](https://github.com/helm/helm) Chart。

```sh
kompose convert -j
```

```none
INFO Kubernetes file "redis-svc.json" created
INFO Kubernetes file "web-svc.json" created
INFO Kubernetes file "redis-deployment.json" created
INFO Kubernetes file "web-deployment.json" created
```

`*-deployment.json` 文件中包含 Deployment 对象。

```sh
kompose convert --replication-controller
```

```none
INFO Kubernetes file "redis-svc.yaml" created
INFO Kubernetes file "web-svc.yaml" created
INFO Kubernetes file "redis-replicationcontroller.yaml" created
INFO Kubernetes file "web-replicationcontroller.yaml" created
```

`*-replicationcontroller.yaml` 文件包含 Replication Controller 对象。
如果你想指定副本数（默认为 1），可以使用 `--replicas` 参数：
`kompose convert --replication-controller --replicas 3`

```shell
kompose convert --daemon-set
```

```none
INFO Kubernetes file "redis-svc.yaml" created
INFO Kubernetes file "web-svc.yaml" created
INFO Kubernetes file "redis-daemonset.yaml" created
INFO Kubernetes file "web-daemonset.yaml" created
```

`*-daemonset.yaml` 文件包含 DaemonSet 对象。

如果你想生成 [Helm](https://github.com/kubernetes/helm) 可用的 Chart，
只需简单的执行下面的命令：

```shell
kompose convert -c
```

```none
INFO Kubernetes file "web-svc.yaml" created
INFO Kubernetes file "redis-svc.yaml" created
INFO Kubernetes file "web-deployment.yaml" created
INFO Kubernetes file "redis-deployment.yaml" created
chart created in "./docker-compose/"
```

```shell
tree docker-compose/
```

```none
docker-compose
├── Chart.yaml
├── README.md
└── templates
    ├── redis-deployment.yaml
    ├── redis-svc.yaml
    ├── web-deployment.yaml
    └── web-svc.yaml
```

这个 Chart 结构旨在为构建 Helm Chart 提供框架。

## 标签   {#labels}

`kompose` 支持 `docker-compose.yml` 文件中用于 Kompose 的标签，
以便在转换时明确定义 Service 的行为。

- `kompose.service.type` 定义要创建的 Service 类型。例如：

  ```yaml
  version: "2"
  services:
    nginx:
      image: nginx
      dockerfile: foobar
      build: ./foobar
      cap_add:
        - ALL
      container_name: foobar
      labels:
        kompose.service.type: nodeport
  ```

- `kompose.service.expose` 定义是否允许从集群外部访问 Service。
  如果该值被设置为 "true"，提供程序将自动设置端点，
  对于任何其他值，该值将被设置为主机名。
  如果在 Service 中定义了多个端口，则选择第一个端口作为公开端口。

  - 如果使用 Kubernetes 驱动，会有一个 Ingress 资源被创建，并且假定已经配置了相应的 Ingress 控制器。
  - 如果使用 OpenShift 驱动，则会有一个 route 被创建。

  例如：

  ```yaml
  version: "2"
  services:
    web:
      image: tuna/docker-counter23
      ports:
       - "5000:5000"
      links:
       - redis
      labels:
        kompose.service.expose: "counter.example.com"
    redis:
      image: redis:3.0
      ports:
       - "6379"
  ```

当前支持的选项有:

| 键                     | 值                                  |
|------------------------|-------------------------------------|
| kompose.service.type   | nodeport / clusterip / loadbalancer |
| kompose.service.expose | true / hostname                     |

{{< note >}}
`kompose.service.type` 标签应该只用 `ports` 来定义，否则 `kompose` 会失败。
{{< /note >}}

## 重启   {#restart}

如果你想创建没有控制器的普通 Pod，可以使用 docker-compose 的 `restart`
结构来指定这一行为。请参考下表了解 `restart` 的不同参数。


| `docker-compose` `restart` | 创建的对象        | Pod `restartPolicy` |
|----------------------------|-------------------|---------------------|
| `""`                       | 控制器对象        | `Always`            |
| `always`                   | 控制器对象        | `Always`            |
| `on-failure`               | Pod               | `OnFailure`         |
| `no`                       | Pod               | `Never`             |

{{< note >}}
控制器对象可以是 `deployment` 或 `replicationcontroller`。
{{< /note >}}

例如，`pival` Service 将在这里变成 Pod。这个容器计算 `pi` 的取值。

```yaml
version: '2'

services:
  pival:
    image: perl
    command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
    restart: "on-failure"
```

### 关于 Deployment Config 的提醒    {#warning-about-deployment-configurations}

如果 Docker Compose 文件中为服务声明了卷，Deployment（Kubernetes）或
DeploymentConfig（OpenShift）策略会从 “RollingUpdate”（默认）变为 “Recreate”。
这样做的目的是为了避免服务的多个实例同时访问卷。

如果 Docker Compose 文件中的服务名包含 `_`（例如 `web_service`），
那么将会被替换为 `-`，服务也相应的会重命名（例如 `web-service`）。
Kompose 这样做的原因是 “Kubernetes” 不允许对象名称中包含 `_`。

请注意，更改服务名称可能会破坏一些 `docker-compose` 文件。

## Docker Compose 版本   {#docker-compose-versions}

Kompose 支持的 Docker Compose 版本包括：1、2 和 3。
对 2.1 和 3.2 版本的支持还有限，因为它们还在实验阶段。

所有三个版本的兼容性列表，
请查看我们的[转换文档](https://github.com/kubernetes/kompose/blob/master/docs/conversion.md)，
文档中列出了所有不兼容的 Docker Compose 关键字。
