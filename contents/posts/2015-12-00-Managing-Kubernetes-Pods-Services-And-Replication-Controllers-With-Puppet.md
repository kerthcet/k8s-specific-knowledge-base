---
title: "使用 Puppet 管理 Kubernetes Pod、Service 和 Replication Controller"
date: 2015-12-17
slug: managing-kubernetes-pods-services-and-replication-controllers-with-puppet
---


_今天的嘉宾帖子是由 IT 自动化领域的领导者 Puppet Labs 的高级软件工程师 Gareth Rushgrove 撰写的。Gareth告诉我们一个新的 Puppet 模块，它帮助管理 Kubernetes 中的资源。_

熟悉[Puppet]的人(https://github.com/puppetlabs/puppet)可能使用它来管理主机上的文件、包和用户。但是Puppet首先是一个配置管理工具，配置管理是一个比管理主机级资源更广泛的规程。配置管理的一个很好的定义是它旨在解决四个相关的问题：标识、控制、状态核算和验证审计。这些问题存在于任何复杂系统的操作中，并且有了新的[Puppet Kubernetes module](https://forge.puppetlabs.com/garethr/kubernetes)，我们开始研究如何为 Kubernetes 解决这些问题。


### Puppet Kubernetes 模块

Puppet kubernetes 模块目前假设您已经有一个 kubernetes 集群 [启动并运行]](http://kubernetes.io/gettingstarted/)。它的重点是管理 Kubernetes中的资源，如 Pods、Replication Controllers 和 Services，而不是（现在）管理底层的 kubelet 或 etcd services。下面是描述 Puppet’s DSL 中一个 Pod 的简短代码片段。


```
kubernetes_pod { 'sample-pod':
  ensure => present,
  metadata => {
    namespace => 'default',
  },
  spec => {
    containers => [{
      name => 'container-name',
      image => 'nginx',
    }]
  },
}
```

如果您熟悉 YAML 文件格式，您可能会立即识别该结构。 该接口故意采取相同的格式以帮助在不同格式之间进行转换 — 事实上，为此提供支持的代码是从Kubernetes API Swagger自动生成的。 运行上面的代码，假设我们将其保存为 pod.pp，就像下面这样简单：


```
puppet apply pod.pp
```


身份验证使用标准的 kubectl 配置文件。您可以在模块的自述文件中找到完整的[README](https://github.com/garethr/garethr-kubernetes/blob/master/README.md)。

Kubernetes 有很多资源，来自 Pods、 Services、 Replication Controllers 和 Service Accounts。您可以在[Puppet 中的 kubernetes 留言簿示例](https://puppetlabs.com/blog/kubernetes-guestbook-example-puppet)文章中看到管理这些资源的模块示例。这演示了如何将规范的 hello-world 示例转换为使用 Puppet代码。


然而，使用 Puppet 的一个主要优点是，您可以创建自己的更高级别和更特定于业务的接口，以连接 kubernetes 管理的应用程序。例如，对于留言簿，可以创建如下内容：

```
guestbook { 'myguestbook':
  redis_slave_replicas => 2,
  frontend_replicas => 3,
  redis_master_image => 'redis',
  redis_slave_image => 'gcr.io/google_samples/gb-redisslave:v1',
  frontend_image => 'gcr.io/google_samples/gb-frontend:v3',
}
```


您可以在Puppet博客文章[在 Puppet 中为 Kubernetes 构建自己的抽象](https://puppetlabs.com/blog/building-your-own-abstractions-kubernetes-puppet)中阅读更多关于使用 Puppet 定义的类型的信息，并看到更多的代码示例。


### 结论

使用 Puppet 而不仅仅是使用标准的 YAML 文件和 kubectl 的优点是：


- 能够创建自己的抽象，以减少重复和设计更高级别的用户界面，如上面的留言簿示例。
- 使用 Puppet 的开发工具验证代码和编写单元测试。
- 与 Puppet Server 等其他工具配合，以确保代码中的模型与集群的状态匹配，并与 PuppetDB 配合工作，以存储报告和跟踪更改。
- 能够针对 Kubernetes API 重复运行相同的代码，以检测任何更改或修正配置。


值得注意的是，大多数大型组织都将拥有非常异构的环境，运行各种各样的软件和操作系统。拥有统一这些离散系统的单一工具链可以使采用 Kubernetes 等新技术变得更加容易。


可以肯定地说，Kubernetes提供了一组优秀的组件来构建云原生系统。使用 Puppet，您可以解决在生产中运行任何复杂系统所带来的一些操作和配置管理问题。[告诉我们](mailto:gareth@puppetlabs.com)如果您试用了该模块，您会有什么想法，以及您希望在将来看到哪些支持。


Gareth Rushgrove，Puppet Labs 高级软件工程师

