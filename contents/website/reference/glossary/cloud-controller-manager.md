---
title: 云控制器管理器（Cloud Controller Manager）
id: cloud-controller-manager
date: 2018-04-12
full_link: /zh-cn/docs/concepts/architecture/cloud-controller/
short_description: >
  将 Kubernetes 与第三方云提供商进行集成的控制平面组件。

aka: 
tags:
- core-object
- architecture
- operation
---

一个 Kubernetes {{<glossary_tooltip text="控制平面" term_id="control-plane" >}}组件，
嵌入了特定于云平台的控制逻辑。
云控制器管理器（Cloud Controller Manager）允许你将你的集群连接到云提供商的 API 之上，
并将与该云平台交互的组件同与你的集群交互的组件分离开来。


通过分离 Kubernetes 和底层云基础设置之间的互操作性逻辑，
`cloud-controller-manager` 组件使云提供商能够以不同于 Kubernetes 主项目的步调发布新特征。
