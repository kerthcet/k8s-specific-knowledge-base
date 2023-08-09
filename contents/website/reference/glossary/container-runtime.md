---
title: 容器运行时（Container Runtime）
id: container-runtime
date: 2019-06-05
full_link: /zh-cn/docs/setup/production-environment/container-runtimes
short_description: >
 容器运行时是负责运行容器的软件。

aka:
tags:
- fundamental
- workload
---

容器运行环境是负责运行容器的软件。


Kubernetes 支持许多容器运行环境，例如
{{< glossary_tooltip term_id="containerd" >}}、
{{< glossary_tooltip term_id="cri-o" >}}
以及 [Kubernetes CRI (容器运行环境接口)](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-node/container-runtime-interface.md)
的其他任何实现。