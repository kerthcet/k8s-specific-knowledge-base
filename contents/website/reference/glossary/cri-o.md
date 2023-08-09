---
title: CRI-O
id: cri-o
date: 2019-05-14
full_link: https://cri-o.io/#what-is-cri-o
short_description: >
  专用于 Kubernetes 的轻量级容器运行时软件

aka:
tags:
- tool
---
该工具可让你通过 Kubernetes CRI 使用 OCI 容器运行时。


CRI-O 是 {{< glossary_tooltip text="CRI" term_id="cri" >}} 的一种实现，
使得你可以使用与开放容器倡议（Open Container Initiative；OCI）
[运行时规范](https://www.github.com/opencontainers/runtime-spec)
兼容的{{< glossary_tooltip text="容器" term_id="container" >}}。

部署 CRI-O 允许 Kubernetes 使用任何符合 OCI 要求的运行时作为容器运行时
去运行 {{< glossary_tooltip text="Pod" term_id="pod" >}}，
并从远程容器仓库获取 OCI 容器镜像。
