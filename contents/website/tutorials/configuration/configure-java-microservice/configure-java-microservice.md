---
title: "使用 MicroProfile、ConfigMaps、Secrets 实现外部化应用配置"
content_type: tutorial
weight: 10
---


在本教程中，你会学到如何以及为什么要实现外部化微服务应用配置。
具体来说，你将学习如何使用 Kubernetes ConfigMaps 和 Secrets 设置环境变量，
然后在 MicroProfile config 中使用它们。

## {{% heading "prerequisites" %}}

### 创建 Kubernetes ConfigMaps 和 Secrets  {#creating-kubernetes-configmaps-secrets}
在 Kubernetes 中，为 docker 容器设置环境变量有几种不同的方式，比如：
Dockerfile、kubernetes.yml、Kubernetes ConfigMaps、和 Kubernetes Secrets。
在本教程中，你将学到怎么用后两个方式去设置你的环境变量，而环境变量的值将注入到你的微服务里。
使用 ConfigMaps 和 Secrets 的一个好处是他们能在多个容器间复用，
比如赋值给不同的容器中的不同环境变量。

ConfigMaps 是存储非机密键值对的 API 对象。
在互动教程中，你会学到如何用 ConfigMap 来保存应用名字。
ConfigMap 的更多信息，你可以在[这里](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/)找到文档。

Secrets 尽管也用来存储键值对，但区别于 ConfigMaps 的是：它针对机密/敏感数据，且存储格式为 Base64 编码。
secrets 的这种特性使得它适合于存储证书、密钥、令牌，上述内容你将在交互教程中实现。
Secrets 的更多信息，你可以在[这里](/zh-cn/docs/concepts/configuration/secret/)找到文档。


### 从代码外部化配置
外部化应用配置之所以有用处，是因为配置常常根据环境的不同而变化。
为了实现此功能，我们用到了 Java 上下文和依赖注入（Contexts and Dependency Injection, CDI）、MicroProfile 配置。
MicroProfile config 是 MicroProfile 的功能特性，
是一组开放 Java 技术，用于开发、部署云原生微服务。

CDI 提供一套标准的依赖注入能力，使得应用程序可以由相互协作的、松耦合的 beans 组装而成。
MicroProfile Config 为 app 和微服务提供从各种来源，比如应用、运行时、环境，获取配置参数的标准方法。
基于来源定义的优先级，属性可以自动的合并到单独一组应用可以通过 API 访问到的属性。
CDI & MicroProfile 都会被用在互动教程中，
用来从 Kubernetes ConfigMaps 和 Secrets 获得外部提供的属性，并注入应用程序代码中。

很多开源框架、运行时支持 MicroProfile Config。
对于整个互动教程，你都可以使用开放的库、灵活的开源 Java 运行时，去构建并运行云原生的 apps 和微服务。
然而，任何 MicroProfile 兼容的运行时都可以用来做替代品。


## {{% heading "objectives" %}}

* 创建 Kubernetes ConfigMap 和 Secret
* 使用 MicroProfile Config 注入微服务配置

  

## 示例：使用 MicroProfile、ConfigMaps、Secrets 实现外部化应用配置

[启动互动教程](/zh-cn/docs/tutorials/configuration/configure-java-microservice/configure-java-microservice-interactive/) 
