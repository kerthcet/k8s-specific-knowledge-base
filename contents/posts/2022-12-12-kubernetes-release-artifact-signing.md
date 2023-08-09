---
layout: blog
title: "Kubernetes 1.26: 我们现在正在对二进制发布工件进行签名!"
date: 2022-12-12
slug: kubernetes-release-artifact-signing
---

**作者：** Sascha Grunert

**译者：** XiaoYang Zhang (HUAWEI)

Kubernetes 特别兴趣小组 SIG Release 自豪地宣布，我们正在对所有发布工件进行数字签名，并且
Kubernetes 在这一方面现已达到 **Beta**。

签名工件为终端用户提供了验证下载资源完整性的机会。
它可以直接在客户端减轻中间人攻击，从而确保远程服务工件的可信度。
过去工作的总体目标是定义用于对所有 Kubernetes 相关工件进行签名的工具，
以及为相关项目（例如 [kubernetes-sigs][k-sigs] 中的项目）提供标准签名流程。

[k-sigs]: https://github.com/kubernetes-sigs

我们已经对所有官方发布的容器镜像进行了签名（从 Kubernetes v1.24 开始）。
在 v1.24 版本和 v1.25 版本中，镜像签名是 alpha 版本。
在 v1.26 版本中，我们将所有的 **二进制工件** 也加入到了签名过程中！
这意味着现在所有的[客户端、服务器和源码压缩包][tarballs]、[二进制工件][binaries]、[软件材料清单（SBOM）][sboms]
以及[构建源][provenance]都将使用 [cosign][cosign] 进行签名！
从技术上讲，我们现在将额外的 `*.sig`（签名）和 `*.cert`（证书）文件与工件一起发布以用于验证其完整性。

[tarballs]: https://github.com/kubernetes/kubernetes/blob/release-1.26/CHANGELOG/CHANGELOG-1.26.md#downloads-for-v1260
[binaries]: https://gcsweb.k8s.io/gcs/kubernetes-release/release/v1.26.0/bin
[sboms]: https://dl.k8s.io/release/v1.26.0/kubernetes-release.spdx
[provenance]: https://dl.k8s.io/release/v1.26.0/provenance.json
[cosign]: https://github.com/sigstore/cosign

要验证一个工件，例如 `kubectl`，你可以在下载二进制文件的同时下载签名和证书。
我使用 v1.26 的候选发布版本 `rc.1` 来演示，因为最终版本还没有发布：

```shell
curl -sSfL https://dl.k8s.io/release/v1.26.0-rc.1/bin/linux/amd64/kubectl -o kubectl
curl -sSfL https://dl.k8s.io/release/v1.26.0-rc.1/bin/linux/amd64/kubectl.sig -o kubectl.sig
curl -sSfL https://dl.k8s.io/release/v1.26.0-rc.1/bin/linux/amd64/kubectl.cert -o kubectl.cert
```

然后你可以使用 [`cosign`][cosign] 验证 `kubectl`：

```shell
COSIGN_EXPERIMENTAL=1 cosign verify-blob kubectl --signature kubectl.sig --certificate kubectl.cert
```

```
tlog entry verified with uuid: 5d54b39222e3fa9a21bcb0badd8aac939b4b0d1d9085b37f1f10b18a8cd24657 index: 8173886
Verified OK
```

可用 UUID 查询 [rekor][rekor] 透明日志：

[rekor]: https://github.com/sigstore/rekor

```shell
rekor-cli get --uuid 5d54b39222e3fa9a21bcb0badd8aac939b4b0d1d9085b37f1f10b18a8cd24657
```

```
LogID: c0d23d6ad406973f9559f3ba2d1ca01f84147d8ffc5b8445c224f98b9591801d
Index: 8173886
IntegratedTime: 2022-11-30T18:59:07Z
UUID: 24296fb24b8ad77a5d54b39222e3fa9a21bcb0badd8aac939b4b0d1d9085b37f1f10b18a8cd24657
Body: {
  "HashedRekordObj": {
    "data": {
      "hash": {
        "algorithm": "sha256",
        "value": "982dfe7eb5c27120de6262d30fa3e8029bc1da9e632ce70570e9c921d2851fc2"
      }
    },
    "signature": {
      "content": "MEQCIH0e1/0svxMoLzjeyhAaLFSHy5ZaYy0/2iQl2t3E0Pj4AiBsWmwjfLzrVyp9/v1sy70Q+FHE8miauOOVkAW2lTYVug==",
      "publicKey": {
        "content": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUN2akNDQWthZ0F3SUJBZ0lVRldab0pLSUlFWkp3LzdsRkFrSVE2SHBQdi93d0NnWUlLb1pJemowRUF3TXcKTnpFVk1CTUdBMVVFQ2hNTWMybG5jM1J2Y21VdVpHVjJNUjR3SEFZRFZRUURFeFZ6YVdkemRHOXlaUzFwYm5SbApjbTFsWkdsaGRHVXdIaGNOTWpJeE1UTXdNVGcxT1RBMldoY05Nakl4TVRNd01Ua3dPVEEyV2pBQU1Ga3dFd1lICktvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUVDT3h5OXBwTFZzcVFPdHJ6RFgveTRtTHZSeU1scW9sTzBrS0EKTlJDM3U3bjMreHorYkhvWVkvMUNNRHpJQjBhRTA3NkR4ZWVaSkhVaWFjUXU4a0dDNktPQ0FXVXdnZ0ZoTUE0RwpBMVVkRHdFQi93UUVBd0lIZ0RBVEJnTlZIU1VFRERBS0JnZ3JCZ0VGQlFjREF6QWRCZ05WSFE0RUZnUVV5SmwxCkNlLzIzNGJmREJZQ2NzbXkreG5qdnpjd0h3WURWUjBqQkJnd0ZvQVUzOVBwejFZa0VaYjVxTmpwS0ZXaXhpNFkKWkQ4d1FnWURWUjBSQVFIL0JEZ3dOb0UwYTNKbGJDMXpkR0ZuYVc1blFHczRjeTF5Wld4bGJtY3RjSEp2WkM1cApZVzB1WjNObGNuWnBZMlZoWTJOdmRXNTBMbU52YlRBcEJnb3JCZ0VFQVlPL01BRUJCQnRvZEhSd2N6b3ZMMkZqClkyOTFiblJ6TG1kdmIyZHNaUzVqYjIwd2dZb0dDaXNHQVFRQjFua0NCQUlFZkFSNkFIZ0FkZ0RkUFRCcXhzY1IKTW1NWkhoeVpaemNDb2twZXVONDhyZitIaW5LQUx5bnVqZ0FBQVlUSjZDdlJBQUFFQXdCSE1FVUNJRXI4T1NIUQp5a25jRFZpNEJySklXMFJHS0pqNkQyTXFGdkFMb0I5SmNycXlBaUVBNW4xZ283cmQ2U3ZVeXNxeldhMUdudGZKCllTQnVTZHF1akVySFlMQTUrZTR3Q2dZSUtvWkl6ajBFQXdNRFpnQXdZd0l2Tlhub3pyS0pWVWFESTFiNUlqa1oKUWJJbDhvcmlMQ1M4MFJhcUlBSlJhRHNCNTFUeU9iYTdWcGVYdThuTHNjVUNNREU4ZmpPZzBBc3ZzSXp2azNRUQo0c3RCTkQrdTRVV1UrcjhYY0VxS0YwNGJjTFQwWEcyOHZGQjRCT2x6R204K093PT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo="
      }
    }
  }
}
```

`HashedRekordObj.signature.content` 应与 `kubectl.sig` 的内容匹配，
`HashedRekordObj.signature.publicKey.content` 应与 `kubectl.cert` 的内容匹配。
也可以指定远程证书和签名的位置而不下载它们：

```shell
COSIGN_EXPERIMENTAL=1 cosign verify-blob kubectl \
    --signature https://dl.k8s.io/release/v1.26.0-rc.1/bin/linux/amd64/kubectl.sig \
    --certificate https://dl.k8s.io/release/v1.26.0-rc.1/bin/linux/amd64/kubectl.cert
```

```
tlog entry verified with uuid: 5d54b39222e3fa9a21bcb0badd8aac939b4b0d1d9085b37f1f10b18a8cd24657 index: 8173886
Verified OK
```

有关如何[验证已签名的 Kubernetes 工件][docs]的官方文档中概述了所有提到的步骤以及如何验证容器镜像。
在下一个即将发布的 Kubernetes 版本中，我们将通过确保真正对所有 Kubernetes 工件进行签名来使之在全球更加成熟。
除此之外，我们正在考虑使用 Kubernetes 自有的基础设施来进行签名（根信任）和验证（透明日志）过程。

[docs]: /zh-cn/docs/tasks/administer-cluster/verify-signed-artifacts

## 参与其中  {#getting-involved}

如果你有兴趣为 SIG Release 做贡献，请考虑申请即将推出的 v1.27 影子计划（观看 [k-dev][k-dev]
上的公告）或参加我们的[周例会][meeting]。

我们期待着在未来的 Kubernetes 版本中做出更多了不起的改变。例如，我们正在致力于
[Kubernetes 发布过程中的 SLSA 3 级合规性][slsa]或将 [kubernetes/kubernetes 默认分支名称重命名为 `main`][kkmain]。

感谢你阅读这篇博文！我想借此机会向所有参与的 SIG Release 人员表示特别地感谢，感谢他们及时推出这一功能！

欢迎使用 [SIG Release 邮件列表][mail]或 [#sig-release][slack] Slack 频道与我们联系。

[mail]: https://groups.google.com/g/kubernetes-sig-release
[slsa]: https://github.com/kubernetes/enhancements/issues/3027
[kkmain]: https://github.com/kubernetes/enhancements/issues/2853
[slack]: http://slack.k8s.io
[k-dev]: https://groups.google.com/a/kubernetes.io/g/dev
[meeting]: http://bit.ly/k8s-sig-release-meeting

## 附加资源  {#additional-resources}
- [签名发布工件增强提案](https://github.com/kubernetes/enhancements/issues/3031)
