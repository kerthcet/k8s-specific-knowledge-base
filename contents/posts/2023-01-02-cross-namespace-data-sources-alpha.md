---
layout: blog
title: "Kubernetes v1.26：对跨名字空间存储数据源的 Alpha 支持"
date: 2023-01-02
slug: cross-namespace-data-sources-alpha
---

**作者：** Takafumi Takahashi (Hitachi Vantara)

**译者：** Michael Yao (DaoCloud)

上个月发布的 Kubernetes v1.26 引入了一个 Alpha 特性，允许你在源数据属于不同的名字空间时为
PersistentVolumeClaim 指定数据源。启用这个新特性后，你在新 PersistentVolumeClaim 的
`dataSourceRef` 字段中指定名字空间。一旦 Kubernetes 发现访问权限正常，新的 PersistentVolume
就可以从其他名字空间中指定的存储源填充其数据。在 Kubernetes v1.26 之前，如果集群已启用了
`AnyVolumeDataSource` 特性，你可能已经从**相同的**名字空间中的数据源制备新卷。
但这仅适用于同一名字空间中的数据源，因此用户无法基于一个名字空间中的数据源使用另一个名字空间中的声明来制备
PersistentVolume。为了解决这个问题，Kubernetes v1.26 在 PersistentVolumeClaim API 的
`dataSourceRef` 字段中添加了一个新的 Alpha `namespace` 字段。

## 工作原理   {#how-it-works}

一旦 csi-provisioner 发现数据源是使用具有非空名字空间名称的 `dataSourceRef` 指定的，
它就会检查由 PersistentVolumeClaim 的 `.spec.dataSourceRef.namespace`
字段指定的名字空间内所授予的所有引用，以便确定可以访问数据源。
如果有 ReferenceGrant 允许访问，则 csi-provisioner 会基于数据源来制备卷。

## 试用   {#trying-it-out}

使用跨名字空间卷制备时以下事项是必需的：

* 为 kube-apiserver 和 kube-controller-manager 启用 `AnyVolumeDataSource` 和
  `CrossNamespaceVolumeDataSource` [特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
* 为特定的 `VolumeSnapShot` 控制器安装 CRD
* 安装 CSI Provisioner 控制器并启用 `CrossNamespaceVolumeDataSource` 特性门控
* 安装 CSI 驱动程序
* 为 ReferenceGrants 安装 CRD

## 完整演练  {#putting-it-all-together}

要查看其工作方式，你可以安装样例并进行试用。
此样例使用 prod 名字空间中的 VolumeSnapshot 在 dev 名字空间中创建 PVC。
这是一个简单的例子。想要在真实世界中使用，你可能要用更复杂的方法。

### 这个例子的假设  {#example-assumptions}

* 部署你的 Kubernetes 集群时启用 `AnyVolumeDataSource` 和 `CrossNamespaceVolumeDataSource` 特性门控
* 有两个名字空间：dev 和 prod
* CSI 驱动程序被部署
* 在 **prod** 名字空间中存在一个名为 `new-snapshot-demo` 的 VolumeSnapshot
* ReferenceGrant CRD（源于 Gateway API 项目）已被部署

### 为 CSI Provisioner 授予 ReferenceGrants 读取权限  {#grant-referencegrants-read-permission-to-csi-provisioner}

仅当 CSI 驱动程序具有 `CrossNamespaceVolumeDataSource` 控制器功能时才需要访问 ReferenceGrants。
对于此示例，外部制备器对于 `referencegrants`（API 组 `gateway.networking.k8s.io`）需要
**get**、**list** 和 **watch** 权限。

```yaml
  - apiGroups: ["gateway.networking.k8s.io"]
    resources: ["referencegrants"]
    verbs: ["get", "list", "watch"]
```

### 为 CSI Provisioner 启用 CrossNamespaceVolumeDataSource 特性门控   {#enable-cnvds-feature-for-csi-provisioner}

将 `--feature-gates=CrossNamespaceVolumeDataSource=true` 添加到 csi-provisioner 命令行。
例如，使用此清单片段重新定义容器：

```yaml
      - args:
        - -v=5
        - --csi-address=/csi/csi.sock
        - --feature-gates=Topology=true
        - --feature-gates=CrossNamespaceVolumeDataSource=true
        image: csi-provisioner:latest
        imagePullPolicy: IfNotPresent
        name: csi-provisioner
```

### 创建 ReferenceGrant   {#create-a-referencegrant}

以下是 ReferenceGrant 示例的清单。

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: ReferenceGrant
metadata:
  name: allow-prod-pvc
  namespace: prod
spec:
  from:
  - group: ""
    kind: PersistentVolumeClaim
    namespace: dev
  to:
  - group: snapshot.storage.k8s.io
    kind: VolumeSnapshot
    name: new-snapshot-demo
```

### 通过使用跨名字空间数据源创建 PersistentVolumeClaim   {#create-a-pvc-by-using-cross-ns-data-source}

Kubernetes 在 dev 上创建 PersistentVolumeClaim，CSI 驱动程序从 prod 上的快照填充在
dev 上使用的 PersistentVolume。

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: example-pvc
  namespace: dev
spec:
  storageClassName: example
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  dataSourceRef:
    apiGroup: snapshot.storage.k8s.io
    kind: VolumeSnapshot
    name: new-snapshot-demo
    namespace: prod
  volumeMode: Filesystem
```

## 怎样了解更多   {#how-can-i-learn-more}

增强提案
[Provision volumes from cross-namespace snapshots](https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/3294-provision-volumes-from-cross-namespace-snapshots)
包含了此特性的历史和技术实现的大量细节。

若想参与，请加入
[Kubernetes 存储特别兴趣小组 (SIG)](https://github.com/kubernetes/community/tree/master/sig-storage)
帮助我们增强此特性。SIG 内有许多好点子，我们很高兴能有更多！

## 致谢   {#acknowledgments}

制作出色的软件需要优秀的团队。
特别感谢以下人员对 CrossNamespaceVolumeDataSouce 特性的深刻见解、周密考量和宝贵贡献：

* Michelle Au (msau42)
* Xing Yang (xing-yang)
* Masaki Kimura (mkimuram)
* Tim Hockin (thockin)
* Ben Swartzlander (bswartz)
* Rob Scott (robscott)
* John Griffith (j-griffith)
* Michael Henriksen (mhenriks)
* Mustafa Elbehery (Elbehery)

很高兴与大家一起工作。
