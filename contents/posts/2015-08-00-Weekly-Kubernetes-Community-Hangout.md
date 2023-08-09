---
title: " Kubernetes 社区每周环聊笔记——2015 年 7 月 31 日 "
date: 2015-08-04
slug: weekly-kubernetes-community-hangout
---


每周，Kubernetes 贡献社区都会通过Google 环聊虚拟开会。我们希望任何有兴趣的人都知道本论坛讨论的内容。

这是今天会议的笔记：

* 私有镜像仓库演示 - Muhammed

    * 将 docker-registry 作为 RC/Pod/Service 运行

    * 在每个节点上运行代理

    * 以 localhost:5000 访问

    * 讨论：

        * 我们应该在可能的情况下通过 GCS 或 S3 支持它吗？

        * 在每个节点上运行由 $object_store 支持的真实镜像仓库

        * DNS 代替 localhost？

            * 分解 docker 镜像字符串？

            * 更像 DNS 策略吗？

* 运行大型集群 - Joe

    * 三星渴望看到大规模 O(1000)

        * 从 AWS 开始

    * RH 也有兴趣 - 需要测试计划

    * 计划下周：讨论工作组

    * 如果您有兴趣加入有关集群可扩展性的对话，请发送邮件至[joe@0xBEDA.com][4]


* 资源 API 提案 - Clayton

    * 新东西需要更多资源信息

    * 关于资源 API 的提案 - 向 apiserver 询问有关pod的信息

    * 发送反馈至：#11951

    * 关于快照，时间序列和聚合的讨论

* 容器化 kubelet - Clayton

    * 打开 pull

    * Docker挂载传播 - RH 带有补丁

    * 有关整个系统引导程序的大问题

        * 双：引导docker /系统docker

    * Kube-in-docker非常好，但可能并不关键

        * 做些小事以取得进步

        * 对 docker 施加压力
* Web UI（preilly）

    * Web UI 放在哪里？

        * 确定将其拆分出去

        * 将其用作容器镜像

        * 作为 kube 发布过程的一部分构建映像

        * vendor回来了吗？也许吧，也许不是。

    * DNS将被拆分吗？

        * 可能更紧密地集成在一起，而不是

    * 其他潜在的衍生产品：

        * apiserver

        * clients
