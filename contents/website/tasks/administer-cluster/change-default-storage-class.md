---
title: 改变默认 StorageClass
content_type: task
weight: 90
---

本文展示了如何改变默认的 Storage Class，它用于为没有特殊需求的 PersistentVolumeClaims 配置 volumes。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


## 为什么要改变默认存储类？

取决于安装模式，你的 Kubernetes 集群可能和一个被标记为默认的已有 StorageClass 一起部署。
这个默认的 StorageClass 以后将被用于动态的为没有特定存储类需求的 PersistentVolumeClaims 
配置存储。更多细节请查看
[PersistentVolumeClaim 文档](/zh-cn/docs/concepts/storage/persistent-volumes/#perspersistentvolumeclaims)。

预先安装的默认 StorageClass 可能不能很好的适应你期望的工作负载；例如，它配置的存储可能太过昂贵。
如果是这样的话，你可以改变默认 StorageClass，或者完全禁用它以防止动态配置存储。

删除默认 StorageClass 可能行不通，因为它可能会被你集群中的扩展管理器自动重建。
请查阅你的安装文档中关于扩展管理器的细节，以及如何禁用单个扩展。


## 改变默认 StorageClass

1. 列出你的集群中的 StorageClasses：

   ```shell
   kubectl get storageclass
   ```

   输出类似这样：

   ```bash
   NAME                 PROVISIONER               AGE
   standard (default)   kubernetes.io/gce-pd      1d
   gold                 kubernetes.io/gce-pd      1d
   ```

   默认 StorageClass 以 `(default)` 标记。

2. 标记默认 StorageClass  非默认：
  
   默认 StorageClass 的注解 `storageclass.kubernetes.io/is-default-class` 设置为 `true`。
   注解的其它任意值或者缺省值将被解释为 `false`。

   要标记一个 StorageClass 为非默认的，你需要改变它的值为 `false`： 
   
   ```bash
   kubectl patch storageclass standard -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
   ```

   这里的 `standard` 是你选择的 StorageClass 的名字。

3. 标记一个 StorageClass 为默认的：

   和前面的步骤类似，你需要添加/设置注解 `storageclass.kubernetes.io/is-default-class=true`。

   ```bash
   kubectl patch storageclass <your-class-name> -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
   ```

   请注意，最多只能有一个 StorageClass 能够被标记为默认。
   如果它们中有两个或多个被标记为默认，Kubernetes 将忽略这个注解，
   也就是它将表现为没有默认 StorageClass。

4. 验证你选用的 StorageClass 为默认的：

   ```bash
   kubectl get storageclass
   ```

   输出类似这样：

   ```
   NAME             PROVISIONER               AGE
   standard         kubernetes.io/gce-pd      1d
   gold (default)   kubernetes.io/gce-pd      1d
   ```

## {{% heading "whatsnext" %}}

* 进一步了解 [PersistentVolumes](/zh-cn/docs/concepts/storage/persistent-volumes/)

