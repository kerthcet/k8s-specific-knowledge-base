---
title: 容器环境变量（Container Environment Variables）
id: container-env-variables
date: 2018-04-12
full_link: /zh-cn/docs/concepts/containers/container-environment/
short_description: >
  容器环境变量提供了 name=value 形式的、运行容器化应用所必须的一些重要信息。

aka: 
tags:
- fundamental
---

容器环境变量提供了 name=value 形式的、在 {{< glossary_tooltip text="Pod" term_id="pod" >}} 中运行的容器所必须的一些重要信息。
  

容器环境变量为运行中的容器化应用提供必要的信息，同时还提供与{{< glossary_tooltip text="容器" term_id="container" >}}重要资源相关的其他信息，例如：文件系统信息、容器自身的信息以及其他像服务端点（Service endpoints）这样的集群资源信息。
