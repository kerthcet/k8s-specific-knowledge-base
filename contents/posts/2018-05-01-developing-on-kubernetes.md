---
title: 在 Kubernetes 上开发
date: 2018-05-01
slug: developing-on-kubernetes
---


**作者**： [Michael Hausenblas](https://twitter.com/mhausenblas) (Red Hat), [Ilya Dmitrichenko](https://twitter.com/errordeveloper) (Weaveworks)


您将如何开发一个 Kubernetes 应用？也就是说，您如何编写并测试一个要在 Kubernetes 上运行的应用程序？本文将重点介绍在独自开发或者团队协作中，您可能希望了解到的为了成功编写 Kubernetes 应用程序而需面临的挑战，工具和方法。


我们假定您是一位开发人员，有您钟爱的编程语言，编辑器/IDE（集成开发环境），以及可用的测试框架。在针对 Kubernetes 开发应用时，最重要的目标是减少对当前工作流程的影响，改变越少越好，尽量做到最小。举个例子，如果您是 Node.js 开发人员，习惯于那种热重载的环境 - 也就是说您在编辑器里一做保存，正在运行的程序就会自动更新 - 那么跟容器、容器镜像或者镜像仓库打交道，又或是跟 Kubernetes 部署、triggers 以及更多头疼东西打交道，不仅会让人难以招架也真的会让开发过程完全失去乐趣。


在下文中，我们将首先讨论 Kubernetes 总体开发环境，然后回顾常用工具，最后进行三个示例性工具的实践演练。这些工具允许针对 Kubernetes 进行本地应用程序的开发和迭代。


## 您的集群运行在哪里？


作为开发人员，您既需要考虑所针对开发的 Kubernetes 集群运行在哪里，也需要思考开发环境如何配置。概念上，有四种开发模式：

![Dev Modes](/images/blog/2018-05-01-developing-on-kubernetes/dok-devmodes_preview.png)


许多工具支持纯 offline 开发，包括 Minikube、Docker（Mac 版/Windows 版）、Minishift 以及下文中我们将详细讨论的几种。有时，比如说在一个微服务系统中，已经有若干微服务在运行，proxied 模式（通过转发把数据流传进传出集群）就非常合适，Telepresence 就是此类工具的一个实例。live 模式，本质上是您基于一个远程集群进行构建和部署。最后，纯 online 模式意味着您的开发环境和运行集群都是远程的，典型的例子是 [Eclipse Che](https://www.eclipse.org/che/docs/che-7/introduction-to-eclipse-che/) 或者 [Cloud 9](https://github.com/errordeveloper/k9c)。现在让我们仔细看看离线开发的基础：在本地运行 Kubernetes。


[Minikube](/docs/getting-started-guides/minikube/) 在更加喜欢于本地 VM 上运行 Kubernetes 的开发人员中，非常受欢迎。不久前，Docker 的 [Mac](https://docs.docker.com/docker-for-mac/kubernetes/) 版和 [Windows](https://docs.docker.com/docker-for-windows/kubernetes/) 版，都试验性地开始自带 Kubernetes（需要下载 “edge” 安装包）。在两者之间，以下原因也许会促使您选择 Minikube 而不是 Docker 桌面版：


* 您已经安装了 Minikube 并且它运行良好
* 您想等到 Docker 出稳定版本
* 您是 Linux 桌面用户
* 您是 Windows 用户，但是没有配有 Hyper-V 的 Windows 10 Pro


运行一个本地集群，开发人员可以离线工作，不用支付云服务。云服务收费一般不会太高，并且免费的等级也有，但是一些开发人员不喜欢为了使用云服务而必须得到经理的批准，也不愿意支付意想不到的费用，比如说忘了下线而集群在周末也在运转。


有些开发人员却更喜欢远程的 Kubernetes 集群，这样他们通常可以获得更大的计算能力和存储容量，也简化了协同工作流程。您可以更容易的拉上一个同事来帮您调试，或者在团队内共享一个应用的使用。再者，对某些开发人员来说，尽可能的让开发环境类似生产环境至关重要，尤其是您依赖外部厂商的云服务时，如：专有数据库、云对象存储、消息队列、外商的负载均衡器或者邮件投递系统。


总之，无论您选择本地或者远程集群，理由都足够多。这很大程度上取决于您所处的阶段：从早期的原型设计/单人开发到后期面对一批稳定微服务的集成。


既然您已经了解到运行环境的基本选项，那么我们就接着讨论如何迭代式的开发并部署您的应用。


## 常用工具


我们现在回顾既可以允许您可以在 Kubernetes 上开发应用程序又尽可能最小地改变您现有的工作流程的一些工具。我们致力于提供一份不偏不倚的描述，也会提及使用某个工具将会意味着什么。


请注意这很棘手，因为即使在成熟定型的技术中做选择，比如说在 JSON、YAML、XML、REST、gRPC 或者 SOAP 之间做选择，很大程度也取决于您的背景、喜好以及公司环境。在 Kubernetes 生态系统内比较各种工具就更加困难，因为技术发展太快，几乎每周都有新工具面市；举个例子，仅在准备这篇博客的期间，[Gitkube](https://gitkube.sh/) 和 [Watchpod](https://github.com/MinikubeAddon/watchpod) 相继出品。为了进一步覆盖到这些新的，以及一些相关的已推出的工具，例如 [Weave Flux](https://github.com/weaveworks/flux) 和 OpenShift 的 [S2I](https://docs.openshift.com/container-platform/3.9/creating_images/s2i.html)，我们计划再写一篇跟进的博客。

### Draft



[Draft](https://github.com/Azure/draft) 旨在帮助您将任何应用程序部署到 Kubernetes。它能够检测到您的应用所使用的编程语言，并且生成一份 Dockerfile 和 Helm 图表。然后它替您启动构建并且依照 Helm 图表把所生产的镜像部署到目标集群。它也可以让您很容易地设置到 localhost 的端口映射。


这意味着：

* 用户可以任意地自定义 Helm 图表和 Dockerfile 模版，或者甚至创建一个 [custom pack](https://github.com/Azure/draft/blob/master/docs/reference/dep-003.md)（使用 Dockerfile、Helm 图表以及其他）以备后用

* 要想理解一个应用应该怎么构建并不容易，在某些情况下，用户也许需要修改 Draft 生成的 Dockerfile 和 Heml 图表

* 如果使用 [Draft version 0.12.0](https://github.com/Azure/draft/releases/tag/v0.12.0)<sup>1</sup> 或者更老版本，每一次用户想要测试一个改动，他们需要等 Draft 把代码拷贝到集群，运行构建，推送镜像并且发布更新后的图表；这些步骤可能进行得很快，但是每一次用户的改动都会产生一个镜像（无论是否提交到 git ）

* 在 Draft 0.12.0版本，构建是本地进行的
* 用户不能选择 Helm 以外的工具进行部署
* 它可以监控本地的改动并且触发部署，但是这个功能默认是关闭的

* 它允许开发人员使用本地或者远程的 Kubernetes 集群
* 如何部署到生产环境取决于用户， Draft 的作者推荐了他们的另一个项目 - Brigade
* 可以代替 Skaffold， 并且可以和 Squash 一起使用


更多信息：

* [Draft: Kubernetes container development made easy](https://kubernetes.io/blog/2017/05/draft-kubernetes-container-development)
* [Getting Started Guide](https://github.com/Azure/draft/blob/master/docs/getting-started.md)

【1】：此处疑为 0.11.0，因为 0.12.0 已经支持本地构建，见下一条

### Skaffold


[Skaffold](https://github.com/GoogleCloudPlatform/skaffold) 让 CI 集成具有可移植性的，它允许用户采用不同的构建系统，镜像仓库和部署工具。它不同于 Draft，同时也具有一定的可比性。它具有生成系统清单的基本能力，但那不是一个重要功能。Skaffold 易于扩展，允许用户在构建和部署应用的每一步选取相应的工具。


这意味着：

* 模块化设计
* 不依赖于 CI，用户不需要 Docker 或者 Kubernetes 插件
* 没有 CI 也可以工作，也就是说，可以在开发人员的电脑上工作
* 它可以监控本地的改动并且触发部署

* 它允许开发人员使用本地或者远程的 Kubernetes 集群
* 它可以用于部署生产环境，用户可以精确配置，也可以为每一套目标环境提供不同的生产线
* 可以代替 Draft，并且和其他工具一起使用


更多信息：

* [Introducing Skaffold: Easy and repeatable Kubernetes development](https://cloudplatform.googleblog.com/2018/03/introducing-Skaffold-Easy-and-repeatable-Kubernetes-development.html)
* [Getting Started Guide](https://github.com/GoogleCloudPlatform/skaffold#getting-started-with-local-tooling)

### Squash

[Squash](https://github.com/solo-io/squash) 包含一个与 Kubernetes 全面集成的调试服务器，以及一个 IDE 插件。它允许您插入断点和所有的调试操作，就像您所习惯的使用 IDE 调试一个程序一般。它允许您将调试器应用到 Kubernetes 集群中运行的 pod 上，从而让您可以使用 IDE 调试 Kubernetes 集群。


这意味着：

* 不依赖您选择的其它工具
* 需要一组特权 DaemonSet
* 可以和流行 IDE 集成
* 支持 Go、Python、Node.js、Java 和 gdb

* 用户必须确保容器中的应用程序使编译时使用了调试符号
* 可与此处描述的任何其他工具结合使用
* 它可以与本地或远程 Kubernetes 集群一起使用


更多信息：

* [Squash: A Debugger for Kubernetes Apps](https://www.youtube.com/watch?v=5TrV3qzXlgI)
* [Getting Started Guide](https://squash.solo.io/overview/)

### Telepresence

[Telepresence](https://www.telepresence.io/) 使用双向代理将开发人员工作站上运行的容器与远程 Kubernetes 集群连接起来，并模拟集群内环境以及提供对配置映射和机密的访问。它消除了将应用部署到集群的需要，并利用本地容器抽象出网络和文件系统接口，以使其看起来应用好像就在集群中运行，从而改进容器应用程序开发的迭代时间。


这意味着：

* 它不依赖于其它您选取的工具
* 可以同 Squash 一起使用，但是 Squash 必须用于调试集群中的 pods，而传统/本地调试器需要用于调试通过 Telepresence 连接到集群的本地容器
* Telepresence 会产生一些网络延迟

* 它通过辅助进程提供连接 -  sshuttle，基于SSH的一个工具
* 还提供了使用 LD_PRELOAD/DYLD_INSERT_LIBRARIES 的更具侵入性的依赖注入模式
* 它最常用于远程 Kubernetes 集群，但也可以与本地集群一起使用


更多信息：

* [Telepresence: fast, realistic local development for Kubernetes microservices](https://www.telepresence.io/)
* [Getting Started Guide](https://www.telepresence.io/tutorials/docker)
* [How It Works](https://www.telepresence.io/discussion/how-it-works)

### Ksync



[Ksync](https://github.com/vapor-ware/ksync) 在本地计算机和运行在 Kubernetes 中的容器之间同步应用程序代码（和配置），类似于 [oc rsync](https://docs.openshift.com/container-platform/3.9/dev_guide/copy_files_to_container.html) 在 OpenShift 中的角色。它旨在通过消除构建和部署步骤来缩短应用程序开发的迭代时间。



这意味着：

* 它绕过容器图像构建和修订控制
* 使用编译语言的用户必须在 pod（TBC）内运行构建
* 双向同步 - 远程文件会复制到本地目录
* 每次更新远程文件系统时都会重启容器
* 无安全功能 - 仅限开发

* 使用 [Syncthing](https://github.com/syncthing/syncthing)，一个用于点对点同步的 Go 语言库
* 需要一个在集群中运行的特权 DaemonSet
* Node 必须使用带有 overlayfs2 的 Docker  - 在写作本文时，尚不支持其他 CRI 实现


更多信息：

* [Getting Started Guide](https://github.com/vapor-ware/ksync#getting-started)
* [How It Works](https://github.com/vapor-ware/ksync/blob/master/docs/architecture.md)
* [Katacoda scenario to try out ksync in your browser](https://www.katacoda.com/vaporio/scenarios/ksync)
* [Syncthing Specification](https://docs.syncthing.net/specs/)


## 实践演练



我们接下来用于练习使用工具的应用是一个简单的[股市模拟器](https://github.com/kubernauts/dok-example-us)，包含两个微服务：


* `stock-gen`（股市数据生成器）微服务是用 Go 编写的，随机生成股票数据并通过 HTTP 端点 `/ stockdata` 公开
* 第二个微服务，`stock-con`（股市数据消费者）是一个 Node.js 应用程序，它使用来自 `stock-gen` 的股票数据流，并通过 HTTP 端点 `/average/$SYMBOL` 提供股价移动平均线，也提供一个健康检查端点 `/healthz`。


总体上，此应用的默认配置如下图所示：

![Default Setup](/images/blog/2018-05-01-developing-on-kubernetes/dok-architecture_preview.png)


在下文中，我们将选取以上讨论的代表性工具进行实践演练：ksync，具有本地构建的 Minikube 以及 Skaffold。对于每个工具，我们执行以下操作：


* 设置相应的工具，包括部署准备和 `stock-con` 微服务数据的本地读取
* 执行代码更新，即更改 `stock-con` 微服务的 `/healthz` 端点的源代码并观察网页刷新


请注意，我们一直使用 Minikube 的本地 Kubernetes 集群，但是您也可以使用 ksync 和 Skaffold 的远程集群跟随练习。


## 实践演练：ksync


作为准备，安装 [ksync](https://vapor-ware.github.io/ksync/#installation)，然后执行以下步骤配置开发环境：

```
$ mkdir -p $(pwd)/ksync
$ kubectl create namespace dok
$ ksync init -n dok
```


完成基本设置后，我们可以告诉 ksync 的本地客户端监控 Kubernetes 的某个命名空间，然后我们创建一个规范来定义我们想要同步的文件夹（本地的 `$(pwd)/ksync` 和容器中的 `/ app` ）。请注意，目标 pod 是用 selector 参数指定：

```
$ ksync watch -n dok
$ ksync create -n dok --selector=app=stock-con $(pwd)/ksync /app
$ ksync get -n dok
```


现在我们部署股价数据生成器和股价数据消费者微服务：

```
$ kubectl -n=dok apply \
      -f https://raw.githubusercontent.com/kubernauts/dok-example-us/master/stock-gen/app.yaml
$ kubectl -n=dok apply \
      -f https://raw.githubusercontent.com/kubernauts/dok-example-us/master/stock-con/app.yaml
```


一旦两个部署建好并且 pod 开始运行，我们转发 `stock-con` 服务以供本地读取（另开一个终端窗口）：

```
$ kubectl get -n dok po --selector=app=stock-con  \
                     -o=custom-columns=:metadata.name --no-headers |  \
                     xargs -IPOD kubectl -n dok port-forward POD 9898:9898
```


这样，通过定期查询 `healthz` 端点，我们就应该能够从本地机器上读取 `stock-con` 服务，查询命令如下（在一个单独的终端窗口）：

```
$ watch curl localhost:9898/healthz
```


现在，改动 `ksync/stock-con` 目录中的代码，例如改动 [`service.js` 中定义的 `/healthz` 端点代码](https://github.com/kubernauts/dok-example-us/blob/2334ee8fb11f8813370122bd46285cf45bdd4c48/stock-con/service.js#L52)，在其 JSON 形式的响应中新添一个字段并观察 pod 如何更新以及 `curl localhost：9898/healthz` 命令的输出发生何种变化。总的来说，您最后应该看到类似的内容：


![Preview](/images/blog/2018-05-01-developing-on-kubernetes/dok-ksync_preview.png)



### 实践演练：带本地构建的 Minikube



对于以下内容，您需要启动并运行 Minikube，我们将利用 Minikube 自带的 Docker daemon 在本地构建镜像。作为准备，请执行以下操作

```
$ git clone https://github.com/kubernauts/dok-example-us.git && cd dok-example-us
$ eval $(minikube docker-env)
$ kubectl create namespace dok
```


现在我们部署股价数据生成器和股价数据消费者微服务：


```
$ kubectl -n=dok apply -f stock-gen/app.yaml
$ kubectl -n=dok apply -f stock-con/app.yaml
```


一旦两个部署建好并且 pod 开始运行，我们转发 `stock-con` 服务以供本地读取（另开一个终端窗口）并检查 `healthz` 端点的响应：

```
$ kubectl get -n dok po --selector=app=stock-con  \
                     -o=custom-columns=:metadata.name --no-headers |  \
                     xargs -IPOD kubectl -n dok port-forward POD 9898:9898 &
$ watch curl localhost:9898/healthz
```

现在，改一下 `ksync/stock-con` 目录中的代码，例如修改 [`service.js` 中定义的 `/healthz` 端点代码](https://github.com/kubernauts/dok-example-us/blob/2334ee8fb11f8813370122bd46285cf45bdd4c48/stock-con/service.js#L52)，在其 JSON 形式的响应中添加一个字段。在您更新完代码后，最后一步是构建新的容器镜像并启动新部署，如下所示：


```
$ docker build -t stock-con:dev -f Dockerfile .
$ kubectl -n dok set image deployment/stock-con *=stock-con:dev
```

总的来说，您最后应该看到类似的内容：

![Local Preview](/images/blog/2018-05-01-developing-on-kubernetes/dok-minikube-localdev_preview.png)


### 实践演练：Skaffold


要进行此演练，首先需要安装 [Skaffold](https://github.com/GoogleContainerTools/skaffold#installation)。完成后，您可以执行以下步骤来配置开发环境：

```
$ git clone https://github.com/kubernauts/dok-example-us.git && cd dok-example-us
$ kubectl create namespace dok
```

现在我们部署股价数据生成器（但是暂不部署股价数据消费者，此服务将使用 Skaffold 完成）：

```
$ kubectl -n=dok apply -f stock-gen/app.yaml
```



请注意，最初我们在执行 `skaffold dev` 时发生身份验证错误，为避免此错误需要安装[问题322](https://github.com/GoogleContainerTools/skaffold/issues/322) 中所述的修复。本质上，需要将 `〜/.docker/config.json` 的内容改为：


```
{
   "auths": {}
}
```


接下来，我们需要略微改动 `stock-con/app.yaml`，这样 Skaffold 才能正常使用此文件：


在 `stock-con` 部署和服务中添加一个 `namespace` 字段，其值为 `dok`

将容器规范的 `image` 字段更改为 `quay.io/mhausenblas/stock-con`，因为 Skaffold 可以即时管理容器镜像标签。

最终的 stock-con 的 `app.yaml` 文件看起来如下：


```
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  labels:
    app: stock-con
  name: stock-con
  namespace: dok
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: stock-con
    spec:
      containers:
      - name: stock-con
        image: quay.io/mhausenblas/stock-con
        env:
        - name: DOK_STOCKGEN_HOSTNAME
          value: stock-gen
        - name: DOK_STOCKGEN_PORT
          value: "9999"
        ports:
        - containerPort: 9898
          protocol: TCP
        livenessProbe:
          initialDelaySeconds: 2
          periodSeconds: 5
          httpGet:
            path: /healthz
            port: 9898
        readinessProbe:
          initialDelaySeconds: 2
          periodSeconds: 5
          httpGet:
            path: /healthz
            port: 9898
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: stock-con
  name: stock-con
  namespace: dok
spec:
  type: ClusterIP
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 9898
  selector:
    app: stock-con
```

我们能够开始开发之前的最后一步是配置 Skaffold。因此，在 `stock-con/` 目录中创建文件 `skaffold.yaml`，其中包含以下内容：

```
apiVersion: skaffold/v1alpha2
kind: Config
build:
  artifacts:
  - imageName: quay.io/mhausenblas/stock-con
    workspace: .
    docker: {}
  local: {}
deploy:
  kubectl:
    manifests:
      - app.yaml
```

现在我们准备好开始开发了。为此，在 `stock-con/` 目录中执行以下命令：

```
$ skaffold dev
```


上面的命令将触发 `stock-con` 图像的构建和部署。一旦 `stock-con` 部署的 pod 开始运行，我们再次转发 `stock-con` 服务以供本地读取（在单独的终端窗口中）并检查 `healthz` 端点的响应：

```bash
$ kubectl get -n dok po --selector=app=stock-con  \
                     -o=custom-columns=:metadata.name --no-headers |  \
                     xargs -IPOD kubectl -n dok port-forward POD 9898:9898 &
$ watch curl localhost:9898/healthz
```
 
现在，如果您修改一下 `stock-con` 目录中的代码，例如 [`service.js` 中定义的 `/healthz` 端点代码](https://github.com/kubernauts/dok-example-us/blob/2334ee8fb11f8813370122bd46285cf45bdd4c48/stock-con/service.js#L52)，在其 JSON 形式的响应中添加一个字段，您应该看到 Skaffold 可以检测到代码改动并创建新图像以及部署它。您的屏幕看起来应该类似这样：
 
 
![Skaffold Preview](/images/blog/2018-05-01-developing-on-kubernetes/dok-skaffold_preview.png)

至此，您应该对不同的工具如何帮您在 Kubernetes 上开发应用程序有了一定的概念，如果您有兴趣了解有关工具和/或方法的更多信息，请查看以下资源：

* Blog post by Shahidh K Muhammed on [Draft vs Gitkube vs Helm vs Ksonnet vs Metaparticle vs Skaffold](https://blog.hasura.io/draft-vs-gitkube-vs-helm-vs-ksonnet-vs-metaparticle-vs-skaffold-f5aa9561f948) (03/2018)
* Blog post by Gergely Nemeth on [Using Kubernetes for Local Development](https://nemethgergely.com/using-kubernetes-for-local-development/index.html), with a focus on Skaffold (03/2018)
* Blog post by Richard Li on [Locally developing Kubernetes services (without waiting for a deploy)](https://hackernoon.com/locally-developing-kubernetes-services-without-waiting-for-a-deploy-f63995de7b99), with a focus on Telepresence
* Blog post by Abhishek Tiwari on [Local Development Environment for Kubernetes using Minikube](https://abhishek-tiwari.com/local-development-environment-for-kubernetes-using-minikube/) (09/2017)
* Blog post by Aymen El Amri on [Using Kubernetes for Local Development — Minikube](https://medium.com/devopslinks/using-kubernetes-minikube-for-local-development-c37c6e56e3db) (08/2017)
* Blog post by Alexis Richardson on [​GitOps - Operations by Pull Request](https://www.weave.works/blog/gitops-operations-by-pull-request) (08/2017)
* Slide deck [GitOps: Drive operations through git](https://docs.google.com/presentation/d/1d3PigRVt_m5rO89Ob2XZ16bW8lRSkHHH5k816-oMzZo/), with a focus on Gitkube by Tirumarai Selvan (03/2018)
* Slide deck [Developing apps on Kubernetes](https://speakerdeck.com/mhausenblas/developing-apps-on-kubernetes), a talk Michael Hausenblas gave at a CNCF Paris meetup  (04/2018)
* YouTube videos:
    * [TGI Kubernetes 029: Developing Apps with Ksync](https://www.youtube.com/watch?v=QW85Y0Ug3KY )
    * [TGI Kubernetes 030: Exploring Skaffold](https://www.youtube.com/watch?v=McwwWhCXMxc)
    * [TGI Kubernetes 031: Connecting with Telepresence](https://www.youtube.com/watch?v=zezeBAJ_3w8)
    * [TGI Kubernetes 033: Developing with Draft](https://www.youtube.com/watch?v=8B1D7cTMPgA)
* Raw responses to the [Kubernetes Application Survey](https://docs.google.com/spreadsheets/d/12ilRCly2eHKPuicv1P_BD6z__PXAqpiaR-tDYe2eudE/edit) 2018 by SIG Apps


有了这些，我们这篇关于如何在 Kubernetes 上开发应用程序的博客就可以收尾了，希望您有所收获，如果您有反馈和/或想要指出您认为有用的工具，请通过 Twitter 告诉我们：[Ilya](https://twitter.com/errordeveloper) 和 [Michael](https://twitter.com/mhausenblas)
