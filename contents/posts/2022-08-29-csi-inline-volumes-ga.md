---
layout: blog
title: "Kubernetes 1.25：CSI 内联存储卷正式发布"
date: 2022-08-29
slug: csi-inline-volumes-ga
---

**作者：** Jonathan Dobson (Red Hat)

CSI 内联存储卷是在 Kubernetes 1.15 中作为 Alpha 功能推出的，并从 1.16 开始成为 Beta 版本。
我们很高兴地宣布，这项功能在 Kubernetes 1.25 版本中正式发布（GA）。

CSI 内联存储卷与其他类型的临时卷相似，如 `configMap`、`downwardAPI` 和 `secret`。
重要的区别是，存储是由 CSI 驱动提供的，它允许使用第三方供应商提供的临时存储。
卷被定义为 Pod 规约的一部分，并遵循 Pod 的生命周期，这意味着卷随着 Pod 的调度而创建，并随着 Pod 的销毁而销毁。


## 1.25 版本有什么新内容？

1.25 版本修复了几个与 CSI 内联存储卷相关的漏洞，
并且 [CSIInlineVolume 特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
已正式发布，锁定为 `True`。
因为没有新的 API 变化，所以除了这些错误修复外，使用该功能 Beta 版本的用户应该不会注意到任何重大变化。

- [#89290 - CSI inline volumes should support fsGroup](https://github.com/kubernetes/kubernetes/issues/89290)
- [#79980 - CSI volume reconstruction does not work for ephemeral volumes](https://github.com/kubernetes/kubernetes/issues/79980)

## 何时使用此功能

CSI 内联存储卷是为简单的本地卷准备的，这种本地卷应该跟随 Pod 的生命周期。
它们对于使用 CSI 驱动为 Pod 提供 Secret、配置数据或其他特殊用途的存储可能很有用。

在以下情况下，CSI 驱动不适合内联使用：
- 卷需要持续的时间超过 Pod 的生命周期
- 卷快照、克隆或卷扩展是必需的
- CSI 驱动需要 `volumeAttributes` 字段，此字段应该限制给管理员使用

## 如何使用此功能

为了使用这个功能，`CSIDriver` 规约必须明确将 `Ephemeral` 列举为 `volumeLifecycleModes` 的参数之一。
下面是一个来自 [Secrets Store CSI Driver](https://github.com/kubernetes-sigs/secrets-store-csi-driver) 的简单例子。

```
apiVersion: storage.k8s.io/v1
kind: CSIDriver
metadata:
  name: secrets-store.csi.k8s.io
spec:
  podInfoOnMount: true
  attachRequired: false
  volumeLifecycleModes:
  - Ephemeral
```

所有 Pod 规约都可以引用该 CSI 驱动来创建一个内联卷，如下例所示。

```
kind: Pod
apiVersion: v1
metadata:
  name: my-csi-app-inline
spec:
  containers:
    - name: my-frontend
      image: busybox
      volumeMounts:
      - name: secrets-store-inline
        mountPath: "/mnt/secrets-store"
        readOnly: true
      command: [ "sleep", "1000000" ]
  volumes:
    - name: secrets-store-inline
      csi:
        driver: secrets-store.csi.k8s.io
        readOnly: true
        volumeAttributes:
          secretProviderClass: "my-provider"
```

如果驱动程序支持一些卷属性，你也可以将这些属性作为 Pod `spec` 的一部分。

```
      csi:
        driver: block.csi.vendor.example
        volumeAttributes:
          foo: bar
```

## 使用案例示例

支持 `Ephemeral` 卷生命周期模式的两个现有 CSI 驱动是 Secrets Store CSI 驱动和 Cert-Manager CSI 驱动。

[Secrets Store CSI Driver](https://github.com/kubernetes-sigs/secrets-store-csi-driver)
允许用户将 Secret 作为内联卷从外部挂载到一个 Pod 中。
当密钥存储在外部管理服务或 Vault 实例中时，这可能很有用。

[Cert-Manager CSI Driver](https://github.com/cert-manager/csi-driver) 与 [cert-manager](https://cert-manager.io/) 协同工作，
无缝地请求和挂载证书密钥对到一个 Pod 中。这使得证书可以在应用 Pod 中自动更新。


## 安全考虑因素

应特别考虑哪些 CSI 驱动可作为内联卷使用。
`volumeAttributes` 通常通过 `StorageClass` 控制，并可能包含应限制给集群管理员的属性。
允许 CSI 驱动用于内联临时卷意味着任何有权限创建 Pod 的用户也可以通过 Pod 规约向驱动提供 `volumeAttributes` 字段。

集群管理员可以选择从 CSIDriver 规约中的 `volumeLifecycleModes` 中省略（或删除） `Ephemeral`，
以防止驱动被用作内联临时卷，或者使用[准入 Webhook](/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/) 来限制驱动的使用。

## 参考资料

关于此功能的更多信息，请参阅：

- [Kubernetes 文档](/zh-cn/docs/concepts/storage/ephemeral-volumes/#csi-ephemeral-volumes)
- [CSI 文档](https://kubernetes-csi.github.io/docs/ephemeral-local-volumes.html)
- [KEP-596](https://github.com/kubernetes/enhancements/blob/master/keps/sig-storage/596-csi-inline-volumes/README.md)
- [CSI 内联存储卷的 Beta 阶段博客文章](https://kubernetes.io/blog/2020/01/21/csi-ephemeral-inline-volumes/)

