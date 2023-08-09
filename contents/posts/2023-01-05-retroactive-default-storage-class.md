---
layout: blog
title: "Kubernetes v1.26：可追溯的默认 StorageClass"
date: 2023-01-05
slug: retroactive-default-storage-class
---

**作者：** Roman Bednář (Red Hat)

**译者：** Michael Yao (DaoCloud)

Kubernetes v1.25 引入了一个 Alpha 特性来更改默认 StorageClass 被分配到 PersistentVolumeClaim (PVC) 的方式。
启用此特性后，你不再需要先创建默认 StorageClass，再创建 PVC 来分配类。
此外，任何未分配 StorageClass 的 PVC 都可以在后续被更新。此特性在 Kubernetes v1.26 中已进阶至 Beta。

有关如何使用的更多细节，请参阅 Kubernetes
文档[可追溯的默认 StorageClass 赋值](/zh-cn/docs/concepts/storage/persistent-volumes/#retroactive-default-storageclass-assignment)，
你还可以阅读了解为什么 Kubernetes 项目做了此项变更。

## 为什么 StorageClass 赋值需要改进  {#why-did-sc-assignment-need-improvements}

用户可能已经熟悉在创建时将默认 StorageClasses 分配给**新** PVC 的这一类似特性。
这个目前由[准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#defaultstorageclass)处理。

但是，如果在创建 PVC 时没有定义默认 StorageClass 会怎样？
那用户最终将得到一个永远不会被赋予存储类的 PVC。结果是没有存储会被制备，而 PVC 有时也会“卡在”这里。
一般而言，两个主要场景可能导致 PVC “卡住”，并在后续造成更多问题。让我们仔细看看这两个场景。

### 更改默认 StorageClass  {#changing-default-storageclass}

启用这个 Alpha 特性后，管理员想要更改默认 StorageClass 时会有两个选项：

1. 在移除与 PVC 关联的旧 StorageClass 之前，创建一个新的 StorageClass 作为默认值。
   这将导致在短时间内出现两个默认值。此时，如果用户要创建一个 PersistentVolumeClaim，
   并将 storageClassName 设置为 <code>null</code>（指代默认 StorageClass），
   则最新的默认 StorageClass 将被选中并指定给这个 PVC。

2. 先移除旧的默认值再创建一个新的默认 StorageClass。这将导致短时间内没有默认值。
   接下来如果用户创建一个 PersistentVolumeClaim，并将 storageClassName 设置为 <code>null</code>
   （指代默认 StorageClass），则 PVC 将永远处于 <code>Pending</code> 状态。
   一旦默认 StorageClass 可用，用户就不得不通过删除并重新创建 PVC 来修复这个问题。

### 集群安装期间的资源顺序  {#resource-ordering-during-cluster-installation}

如果集群安装工具需要创建镜像仓库这种有存储要求的资源，很难进行合适地排序。
这是因为任何有存储要求的 Pod 都将依赖于默认 StorageClass 的存在与否。
如果默认 StorageClass 未被定义，Pod 创建将失败。

## 发生了什么变化  {#what-changed}

我们更改了 PersistentVolume (PV) 控制器，以便将默认 StorageClass 指定给
storageClassName 设置为 `null` 且未被绑定的所有 PersistentVolumeClaim。
我们还修改了 API 服务器中的 PersistentVolumeClaim 准入机制，允许将取值从未设置值更改为实际的 StorageClass 名称。

### Null `storageClassName` 与 `storageClassName: ""` - 有什么影响？ {#null-vs-empty-string}

此特性被引入之前，这两种赋值就其行为而言是相同的。storageClassName 设置为 `null` 或 `""`
的所有 PersistentVolumeClaim 都会被绑定到 storageClassName 也设置为 `null` 或
`""` 的、已有的 PersistentVolume 资源。

启用此新特性时，我们希望保持此行为，但也希望能够更新 StorageClass 名称。
考虑到这些限制，此特性更改了 `null` 的语义。
具体而言，如果有一个默认 StorageClass，`null` 将可被理解为 “给我一个默认值”，
而 `""` 表示 “给我 StorageClass 名称也是 `""` 的 PersistentVolume”，
所以行为将保持不变。

综上所述，我们更改了 `null` 的语义，使其行为取决于默认 StorageClass 定义的存在或缺失。

下表显示了所有这些情况，更好地描述了 PVC 何时绑定及其 StorageClass 何时被更新。

<table>
  <caption>使用默认 StorageClass 时的 PVC 绑定行为</caption>
  <thead>
     <tr>
        <th colspan="2"></th>
        <th>PVC <tt>storageClassName</tt> = <code>""</code></th>
        <th>PVC <tt>storageClassName</tt> = <code>null</code></th>
     </tr>
  </thead>
  <tbody>
     <tr>
        <td rowspan="2">未设置默认存储类</td>
        <td>PV <tt>storageClassName</tt> = <code>""</code></td>
        <td>binds</td>
        <td>binds</td>
     </tr>
     <tr>
        <td>PV without <tt>storageClassName</tt></td>
        <td>binds</td>
        <td>binds</td>
     </tr>
     <tr>
        <td rowspan="2">设置了默认存储类</td>
        <td>PV <tt>storageClassName</tt> = <code>""</code></td>
        <td>binds</td>
        <td>存储类更新</td>
     </tr>
     <tr>
        <td>PV without <tt>storageClassName</tt></td>
        <td>binds</td>
        <td>存储类更新</td>
     </tr>
  </tbody>
</table>

## 如何使用  {#how-to-use-it}

如果你想测试这个 Alpha 特性，你需要在 kube-controller-manager 和 kube-apiserver 中启用相关特性门控。
你可以使用 `--feature-gates` 命令行参数：

```
--feature-gates="...,RetroactiveDefaultStorageClass=true"
```

### 测试演练  {#test-drive}

如果你想看到此特性发挥作用并验证它在集群中是否正常工作，你可以尝试以下步骤：

1. 定义一个基本的 PersistentVolumeClaim：

   ```yaml
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: pvc-1
   spec:
     accessModes:
     - ReadWriteOnce
     resources:
       requests:
         storage: 1Gi
   ```

2. 在没有默认 StorageClass 时创建 PersistentVolumeClaim。
   PVC 不会制备或绑定（除非当前已存在一个合适的 PV），PVC 将保持在 `Pending` 状态。

   ```shell
   kubectl get pvc
   ```

   输出类似于： 
   ```console
   NAME      STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
   pvc-1     Pending
   ```

3. 将某个 StorageClass 配置为默认值。

   ```shell
   kubectl patch sc -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
   ```


   输出类似于：
   ```console
   storageclass.storage.k8s.io/my-storageclass patched
   ```

4. 确认 PersistentVolumeClaims 现在已被正确制备，并且已使用新的默认 StorageClass 进行了可追溯的更新。

   ```shell
   kubectl get pvc
   ```


   输出类似于：
   ```console
   NAME      STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      AGE
   pvc-1     Bound    pvc-06a964ca-f997-4780-8627-b5c3bf5a87d8   1Gi        RWO            my-storageclass   87m
   ```

### 新指标  {#new-metrics}

为了帮助你了解该特性是否按预期工作，我们还引入了一个新的 `retroactive_storageclass_total`
指标来显示 PV 控制器尝试更新 PersistentVolumeClaim 的次数，以及
`retroactive_storageclass_errors_total` 来显示这些尝试失败了多少次。

## 欢迎参与   {#getting-involved}

我们始终欢迎新的贡献者，如果你想参与其中，欢迎加入
[Kubernetes Storage Special Interest Group（存储特别兴趣小组）](https://github.com/kubernetes/community/tree/master/sig-storage) (SIG)。

如果你想分享反馈，可以在我们的[公开 Slack 频道](https://app.slack.com/client/T09NY5SBT/C09QZFCE5)上反馈。

特别感谢所有提供精彩评论、分享宝贵见解并帮助实现此特性的贡献者们（按字母顺序排列）：

- Deep Debroy ([ddebroy](https://github.com/ddebroy))
- Divya Mohan ([divya-mohan0209](https://github.com/divya-mohan0209))
- Jan Šafránek ([jsafrane](https://github.com/jsafrane/))
- Joe Betz ([jpbetz](https://github.com/jpbetz))
- Jordan Liggitt ([liggitt](https://github.com/liggitt))
- Michelle Au ([msau42](https://github.com/msau42))
- Seokho Son ([seokho-son](https://github.com/seokho-son))
- Shannon Kularathna ([shannonxtreme](https://github.com/shannonxtreme))
- Tim Bannister ([sftim](https://github.com/sftim))
- Tim Hockin ([thockin](https://github.com/thockin))
- Wojciech Tyczynski ([wojtek-t](https://github.com/wojtek-t))
- Xing Yang ([xing-yang](https://github.com/xing-yang))
