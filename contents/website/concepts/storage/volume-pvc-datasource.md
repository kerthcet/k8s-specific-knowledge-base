---
title: CSI 卷克隆
content_type: concept
weight: 70
---



本文档介绍 Kubernetes 中克隆现有 CSI 卷的概念。阅读前建议先熟悉
[卷](/zh-cn/docs/concepts/storage/volumes)。


## 介绍

{{< glossary_tooltip text="CSI" term_id="csi" >}} 卷克隆功能增加了通过在
`dataSource` 字段中指定存在的
{{< glossary_tooltip text="PVC" term_id="persistent-volume-claim" >}}，
来表示用户想要克隆的 {{< glossary_tooltip term_id="volume" >}}。

克隆（Clone），意思是为已有的 Kubernetes 卷创建副本，它可以像任何其它标准卷一样被使用。
唯一的区别就是配置后，后端设备将创建指定完全相同的副本，而不是创建一个“新的”空卷。

从 Kubernetes API 的角度看，克隆的实现只是在创建新的 PVC 时，
增加了指定一个现有 PVC 作为数据源的能力。源 PVC 必须是 bound
状态且可用的（不在使用中）。

用户在使用该功能时，需要注意以下事项：

* 克隆支持（`VolumePVCDataSource`）仅适用于 CSI 驱动。
* 克隆支持仅适用于 动态供应器。
* CSI 驱动可能实现，也可能未实现卷克隆功能。
* 仅当 PVC 与目标 PVC 存在于同一命名空间（源和目标 PVC 必须在相同的命名空间）时，才可以克隆 PVC。
* 支持用一个不同存储类进行克隆。
    - 目标卷和源卷可以是相同的存储类，也可以不同。
    - 可以使用默认的存储类，也可以在 spec 中省略 storageClassName 字段。
* 克隆只能在两个使用相同 VolumeMode 设置的卷中进行
  （如果请求克隆一个块存储模式的卷，源卷必须也是块存储模式）。

## 制备

克隆卷与其他任何 PVC 一样配置，除了需要增加 dataSource 来引用同一命名空间中现有的 PVC。

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
    name: clone-of-pvc-1
    namespace: myns
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: cloning
  resources:
    requests:
      storage: 5Gi
  dataSource:
    kind: PersistentVolumeClaim
    name: pvc-1
```

{{< note >}}
你必须为 `spec.resources.requests.storage` 指定一个值，并且你指定的值必须大于或等于源卷的值。
{{< /note >}}

结果是一个名称为 `clone-of-pvc-1` 的新 PVC 与指定的源 `pvc-1` 拥有相同的内容。

## 使用

一旦新的 PVC 可用，被克隆的 PVC 像其他 PVC 一样被使用。
可以预期的是，新创建的 PVC 是一个独立的对象。
可以独立使用、克隆、快照或删除它，而不需要考虑它的原始数据源 PVC。
这也意味着，源没有以任何方式链接到新创建的 PVC，它也可以被修改或删除，而不会影响到新创建的克隆。

