---
title: 其他工具
content_type: concept
weight: 150
no_list: true
---


Kubernetes 包含多种工具来帮助你使用 Kubernetes 系统。



## crictl

[`crictl`](https://github.com/kubernetes-sigs/cri-tools)
是用于检查和调试兼容 {{<glossary_tooltip term_id="cri" text="CRI">}} 的容器运行时的命令行接口。

## 仪表盘   {#dashboard}

[`Dashboard`](/zh-cn/docs/tasks/access-application-cluster/web-ui-dashboard/)，
基于 Web 的 Kubernetes 用户界面，
允许你将容器化的应用程序部署到 Kubernetes 集群，
对它们进行故障排查，并管理集群及其资源本身。

## Helm
{{% thirdparty-content single="true" %}}

[Helm](https://helm.sh/)
是一个用于管理预配置 Kubernetes 资源包的工具。这些包被称为“Helm 图表”。

使用 Helm 来：

* 查找和使用打包为 Kubernetes 图表的流行软件
* 将你自己的应用程序共享为 Kubernetes 图表
* 为你的 Kubernetes 应用程序创建可重现的构建
* 智能管理你的 Kubernetes 清单文件
* 管理 Helm 包的发布

## Kompose

[`Kompose`](https://github.com/kubernetes/kompose)
是一个帮助 Docker Compose 用户迁移到 Kubernetes 的工具。


使用 Kompose：

* 将 Docker Compose 文件翻译成 Kubernetes 对象
* 从本地 Docker 开发转到通过 Kubernetes 管理你的应用程序
* 转换 Docker Compose v1 或 v2 版本的 `yaml` 文件或[分布式应用程序包](https://docs.docker.com/compose/bundles/)

## Kui

[`Kui`](https://github.com/kubernetes-sigs/kui)
是一个接受你标准的 `kubectl` 命令行请求并以图形响应的 GUI 工具。

Kui 接受标准的 `kubectl` 命令行工具并以图形响应。
Kui 提供包含可排序表格的 GUI 渲染，而不是 ASCII 表格。

Kui 让你能够：

* 直接点击长的、自动生成的资源名称，而不是复制和粘贴
* 输入 `kubectl` 命令并查看它们的执行，有时甚至比 `kubectl` 本身更快
* 查询 {{<glossary_tooltip text="Job" term_id="job">}} 并查看其执行渲染为瀑布图
* 使用选项卡式 UI 在集群中单击资源

## Minikube

[`minikube`](https://minikube.sigs.k8s.io/docs/)
是一种在你的工作站上本地运行单节点 Kubernetes 集群的工具，用于开发和测试。