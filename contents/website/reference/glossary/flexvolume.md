---
title: FlexVolume
id: flexvolume
date: 2018-06-25
full_link: /zh-cn/docs/concepts/storage/volumes/#flexvolume
short_description: >
  FlexVolume 是一个已弃用的接口，用于创建树外卷插件。
  {{< glossary_tooltip text="容器存储接口（CSI）" term_id="csi" >}}
  是一个更新的接口，它解决了 FlexVolume 的一些问题。

aka: 
tags:
- storage 
---

FlexVolume 是一个已弃用的接口，用于创建树外卷插件。
{{< glossary_tooltip text="容器存储接口（CSI）" term_id="csi" >}}
是一个更新的接口，它解决了 FlexVolume 的一些问题。


FlexVolume 允许用户编写自己的驱动程序，并在 Kubernetes 中加入对用户自己的数据卷的支持。
FlexVolume 驱动程序的二进制文件和依赖项必须安装在主机上。
这需要 root 权限。如果可能的话，SIG Storage 建议实现
{{< glossary_tooltip text="CSI" term_id="csi" >}} 驱动程序，
因为它解决了 FlexVolume 的限制。

* [Kubernetes 文档中的 FlexVolume](/zh-cn/docs/concepts/storage/volumes/#flexvolume)
* [更多关于 FlexVolume 的信息](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-storage/flexvolume.md)
* [存储供应商的卷插件 FAQ](https://github.com/kubernetes/community/blob/master/sig-storage/volume-plugin-faq.md)
