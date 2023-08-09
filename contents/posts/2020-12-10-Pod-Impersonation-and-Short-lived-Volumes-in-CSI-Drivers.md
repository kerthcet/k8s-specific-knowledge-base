---
layout: blog
title: 'Kubernetes 1.20：CSI 驱动程序中的 Pod 身份假扮和短时卷'
date: 2020-12-18
slug: kubernetes-1.20-pod-impersonation-short-lived-volumes-in-csi
---

**作者**: Shihang Zhang（谷歌）

通常，当 [CSI](https://github.com/container-storage-interface/spec/blob/baa71a34651e5ee6cb983b39c03097d7aa384278/spec.md) 驱动程序挂载
诸如 Secret 和证书之类的凭据时，它必须通过存储提供者的身份认证才能访问这些凭据。
然而，对这些凭据的访问是根据 Pod 的身份而不是 CSI 驱动程序的身份来控制的。 
因此，CSI 驱动程序需要某种方法来取得 Pod 的服务帐户令牌。

当前，有两种不是那么理想的方法来实现这一目的，要么通过授予 CSI 驱动程序使用 TokenRequest API 的权限，要么直接从主机文件系统中读取令牌。

两者都存在以下缺点：

- 违反最少特权原则
- 每个 CSI 驱动程序都需要重新实现获取 Pod 的服务帐户令牌的逻辑

第二种方式问题更多，因为：

- 令牌的受众默认为 kube-apiserver
- 该令牌不能保证可用（例如，`AutomountServiceAccountToken=false`）
- 该方法不适用于以与 Pod 不同的（非 root 用户）用户身份运行的 CSI 驱动程序。请参见
  [服务帐户令牌的文件许可权部分](https://github.com/kubernetes/enhancements/blob/f40c24a5da09390bd521be535b38a4dbab09380c/keps/sig-storage/20180515-svcacct-token-volumes.md#file-permission)
- 该令牌可能是旧的 Kubernetes 服务帐户令牌，如果 `BoundServiceAccountTokenVolume=false`，该令牌不会过期。

Kubernetes 1.20 引入了一个内测功能 `CSIServiceAccountToken` 以改善安全状况。这项新功能允许 CSI 驱动程序接收 Pod 的[绑定服务帐户令牌](https://github.com/kubernetes/enhancements/blob/master/keps/sig-auth/1205-bound-service-account-tokens/README.md)。

此功能还提供了一个重新发布卷的能力，以便可以刷新短时卷。

## Pod 身份假扮

### 使用 GCP APIs

使用 [Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)，Kubernetes 服务帐户可以在访问 Google Cloud API 时验证为 Google 服务帐户。
如果 CSI 驱动程序要代表其为挂载卷的 Pod 访问 GCP API，则可以使用 Pod 的服务帐户令牌来
[交换 GCP 令牌](https://cloud.google.com/iam/docs/reference/sts/rest)。启用功能 `CSIServiceAccountToken` 后，
可通过 `NodePublishVolume` RPC 调用中的卷上下文来访问 Pod 的服务帐户令牌。例如：通过 [Secret 存储 CSI 驱动](https://github.com/GoogleCloudPlatform/secrets-store-csi-driver-provider-gcp)
访问 [Google Secret Manager](https://cloud.google.com/secret-manager/)。

### 使用Vault

如果用户将 [Kubernetes 作为身份验证方法](https://www.vaultproject.io/docs/auth/kubernetes)配置，
则 Vault 使用 `TokenReview` API 来验证 Kubernetes 服务帐户令牌。
对于使用 Vault 作为资源提供者的 CSI 驱动程序，它们需要将 Pod 的服务帐户提供给 Vault。
例如，[Secret 存储 CSI 驱动](https://github.com/hashicorp/secrets-store-csi-driver-provider-vault)和
[证书管理器 CSI 驱动](https://github.com/jetstack/cert-manager-csi)。

## 短时卷

为了使诸如证书之类的短时卷保持有效，CSI 驱动程序可以在其 `CSIDriver` 对象中指定 `RequiresRepublish=true`，
以使 kubelet 定期针对已挂载的卷调用 `NodePublishVolume`。
这些重新发布操作使 CSI 驱动程序可以确保卷内容是最新的。

## 下一步

此功能是 Alpha 版，预计将在 1.21 版中移至 Beta 版。 请参阅以下 KEP 和 CSI 文档中的更多内容：

- [KEP-1855: CSI 驱动程序的服务帐户令牌](https://github.com/kubernetes/enhancements/blob/master/keps/sig-storage/1855-csi-driver-service-account-token/README.md)
- [令牌请求](https://kubernetes-csi.github.io/docs/token-requests.html)

随时欢迎您提供反馈!
- SIG-Auth [定期开会](https://github.com/kubernetes/community/tree/master/sig-auth#meetings)，可以通过 [Slack 和邮件列表](https://github.com/kubernetes/community/tree/master/sig-auth#contact)加入
- SIG-Storage [定期开会](https://github.com/kubernetes/community/tree/master/sig-storage#meetings)，可以通过 [Slack 和邮件列表](https://github.com/kubernetes/community/tree/master/sig-storage#contact)加入

