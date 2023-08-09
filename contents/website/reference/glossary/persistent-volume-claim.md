---
title: 持久卷申领（Persistent Volume Claim）
id: persistent-volume-claim
date: 2018-04-12
full_link: /zh-cn/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims
short_description: >
  声明在持久卷中定义的存储资源，以便可以将其挂载为容器中的卷。

aka: 
tags:
- core-object
- storage
---


申领{{< glossary_tooltip text="持久卷（PersistentVolume）" term_id="persistent-volume" >}}
中定义的存储资源，以便可以将其挂载为{{< glossary_tooltip text="容器（container）" term_id="container" >}}中的卷。


指定存储的数量，如何访问存储（只读、读写或独占）以及如何回收存储（保留、回收或删除）。
存储本身的详细信息在 PersistentVolume 对象中。
