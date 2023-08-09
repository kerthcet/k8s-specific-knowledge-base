---
title: 更改 PersistentVolume 的回收策略
content_type: task
weight: 100
---


本文展示了如何更改 Kubernetes PersistentVolume 的回收策略。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


## 为什么要更改 PersistentVolume 的回收策略

PersistentVolumes 可以有多种回收策略，包括 "Retain"、"Recycle" 和  "Delete"。
对于动态配置的 PersistentVolumes 来说，默认回收策略为 "Delete"。
这表示当用户删除对应的 PersistentVolumeClaim 时，动态配置的 volume 将被自动删除。
如果 volume 包含重要数据时，这种自动行为可能是不合适的。
那种情况下，更适合使用 "Retain" 策略。
使用 "Retain" 时，如果用户删除 PersistentVolumeClaim，对应的 PersistentVolume 不会被删除。
相反，它将变为 Released 状态，表示所有的数据可以被手动恢复。

## 更改 PersistentVolume 的回收策略

1. 列出你集群中的 PersistentVolumes

   ```shell
   kubectl get pv
   ```

   输出类似于这样：

   ```none
   NAME                                       CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM             STORAGECLASS     REASON    AGE
   pvc-b6efd8da-b7b5-11e6-9d58-0ed433a7dd94   4Gi        RWO           Delete          Bound     default/claim1    manual                     10s
   pvc-b95650f8-b7b5-11e6-9d58-0ed433a7dd94   4Gi        RWO           Delete          Bound     default/claim2    manual                     6s
   pvc-bb3ca71d-b7b5-11e6-9d58-0ed433a7dd94   4Gi        RWO           Delete          Bound     default/claim3    manual                     3s
   ```

   这个列表同样包含了绑定到每个卷的 claims 名称，以便更容易的识别动态配置的卷。

2. 选择你的 PersistentVolumes 中的一个并更改它的回收策略：

   ```shell
   kubectl patch pv <your-pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
   ```

   这里的 `<your-pv-name>` 是你选择的 PersistentVolume 的名字。

   {{< note >}}
   在 Windows 系统上，你必须对包含空格的 JSONPath 模板加双引号（而不是像上面
   一样为 Bash 环境使用的单引号）。这也意味着你必须使用单引号或者转义的双引号
   来处理模板中的字面值。例如：

   ```cmd
   kubectl patch pv <your-pv-name> -p "{\"spec\":{\"persistentVolumeReclaimPolicy\":\"Retain\"}}"
   ```
   {{< /note >}}

3. 验证你选择的 PersistentVolume 拥有正确的策略：

   ```shell
   kubectl get pv
   ```

   输出类似于这样：

   ```none
   NAME                                       CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM             STORAGECLASS     REASON    AGE
   pvc-b6efd8da-b7b5-11e6-9d58-0ed433a7dd94   4Gi        RWO           Delete          Bound     default/claim1    manual                     40s
   pvc-b95650f8-b7b5-11e6-9d58-0ed433a7dd94   4Gi        RWO           Delete          Bound     default/claim2    manual                     36s
   pvc-bb3ca71d-b7b5-11e6-9d58-0ed433a7dd94   4Gi        RWO           Retain          Bound     default/claim3    manual                     33s
   ```

   在前面的输出中，你可以看到绑定到申领 `default/claim3` 的卷的回收策略为 `Retain`。
   当用户删除申领 `default/claim3` 时，它不会被自动删除。

## {{% heading "whatsnext" %}}

* 进一步了解 [PersistentVolumes](/zh-cn/docs/concepts/storage/persistent-volumes/)
* 进一步了解 [PersistentVolumeClaims](/zh-cn/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)

### 参考 {#reference}

* {{< api-reference page="config-and-storage-resources/persistent-volume-v1" >}}
  * 注意 PersistentVolume 的 `.spec.persistentVolumeReclaimPolicy`
    [字段](/zh-cn/docs/reference/kubernetes-api/config-and-storage-resources/persistent-volume-v1/#PersistentVolumeSpec)。
* {{< api-reference page="config-and-storage-resources/persistent-volume-claim-v1" >}}

