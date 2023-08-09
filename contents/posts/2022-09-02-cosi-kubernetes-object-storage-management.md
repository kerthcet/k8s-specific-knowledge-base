---
layout: blog
title: "COSI 简介：使用 Kubernetes API 管理对象存储"
date: 2022-09-02
slug: cosi-kubernetes-object-storage-management
---


**作者：** Sidhartha Mani ([Minio, Inc](https://min.io))

本文介绍了容器对象存储接口 (COSI)，它是在 Kubernetes 中制备和使用对象存储的一个标准。
它是 Kubernetes v1.25 中的一个 Alpha 功能。

文件和块存储通过 [Container Storage Interface](https://kubernetes.io/blog/2019/01/15/container-storage-interface-ga/) (CSI)
被视为 Kubernetes 生态系统中的一等公民。
使用 CSI 卷的工作负载可以享受跨供应商和跨 Kubernetes 集群的可移植性优势，
而无需更改应用程序清单。对象存储不存在等效标准。

近年来，对象存储作为文件系统和块设备的替代存储形式越来越受欢迎。
对象存储范式促进了计算和存储的分解，这是通过网络而不是本地提供数据来完成的。
分解的架构允许计算工作负载是无状态的，从而使它们更易于管理、扩展和自动化。

## COSI

COSI 旨在标准化对象存储的使用，以提供以下好处：

* Kubernetes 原生 - 使用 Kubernetes API 来制备、配置和管理 Bucket
* 自助服务 - 明确划分管理和运营 (DevOps)，为 DevOps 人员赋予自助服务能力
* 可移植性 - 通过跨 Kubernetes 集群和跨对象存储供应商的可移植性实现供应商中立性

**跨供应商的可移植性只有在两家供应商都支持通用数据路径 API 时才有可能。
例如，可以从 AWS S3 移植到 Ceph，或从 AWS S3 移植到 MinIO 以及反向操作，因为它们都使用 S3 API。
但是无法从 AWS S3 和 Google Cloud 的 GCS 移植，反之亦然。**

## 架构

COSI 由三个部分组成：

* COSI 控制器管理器
* COSI 边车
* COSI 驱动程序

COSI 控制器管理器充当处理 COSI API 对象更改的主控制器，它负责处理 Bucket 创建、更新、删除和访问管理的请求。
每个 Kubernetes 集群都需要一个控制器管理器实例。即使集群中使用了多个对象存储提供程序，也只需要一个。

COSI 边车充当 COSI API 请求和供应商特定 COSI 驱动程序之间的转换器。
该组件使用供应商驱动程序应满足的标准化 gRPC 协议。

COSI 驱动程序是供应商特定组件，它接收来自 sidecar 的请求并调用适当的供应商 API 以创建 Bucket、 
管理其生命周期及对它们的访问。

## 接口

COSI 接口 以 Bucket 为中心，因为 Bucket 是对象存储的抽象单元。COSI 定义了三个旨在管理它们的 Kubernetes API

* Bucket
* BucketClass
* BucketClaim

此外，还定义了另外两个用于管理对 Bucket 的访问的 API：

* BucketAccess
* BucketAccessClass

简而言之，Bucket 和 BucketClaim 可以认为分别类似于 PersistentVolume 和 PersistentVolumeClaim。
BucketClass 在文件/块设备世界中对应的是 StorageClass。

由于对象存储始终通过网络进行身份验证，因此需要访问凭证才能访问 Bucket。
BucketAccess 和 BucketAccessClass 这两个 API 用于表示访问凭证和身份验证策略。
有关这些 API 的更多信息可以在官方 COSI 提案中找到 - https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/1979-object-storage-support

## 自助服务

除了提供 kubernetes-API 驱动的 Bucket 管理之外，COSI 还旨在使 DevOps 人员能够自行配置和管理 Bucket，
而无需管理员干预。这进一步使开发团队能够实现更快的周转时间和更快的上市时间。

COSI 通过在两个不同的利益相关者（即管理员（admin）和集群操作员）之间划分 Bucket 配置步骤来实现这一点。
管理员将负责就如何配置 Bucket 以及如何获取 Bucket 的访问权限设置广泛的策略和限制。
集群操作员可以在管理员设置的限制内自由创建和使用 Bucket。

例如，集群操作员可以使用管理策略将最大预置容量限制为 100GB，并且允许开发人员创建 Bucket 并将数据存储到该限制。
同样对于访问凭证，管理员将能够限制谁可以访问哪些 Bucket，并且开发人员将能够访问他们可用的所有 Bucket。

## 可移植性

COSI 的第三个目标是实现 Bucket 管理的供应商中立性。COSI 支持两种可移植性：

* 跨集群
* 跨提供商

跨集群可移植性允许在一个集群中配置的 Bucket 在另一个集群中可用。这仅在对象存储后端本身可以从两个集群访问时才有效。

跨提供商可移植性是指允许组织或团队无缝地从一个对象存储提供商迁移到另一个对象存储提供商，
而无需更改应用程序定义（PodTemplates、StatefulSets、Deployment 等）。这只有在源和目标提供者使用相同的数据时才有可能。

**COSI 不处理数据迁移，因为它超出了其范围。如果提供者之间的移植也需要迁移数据，则需要采取其他措施来确保数据可用性。**

## 接下来

令人惊叹的 sig-storage-cosi 社区一直在努力将 COSI 标准带入 Alpha 状态。
我们期待很多供应商加入编写 COSI 驱动程序并与 COSI 兼容！

我们希望为 COSI Bucket 添加更多身份验证机制，我们正在设计高级存储桶共享原语、多集群存储桶管理等等。
未来有很多伟大的想法和机会！

请继续关注接下来的内容，如果你有任何问题、意见或建议分解的架构允许计算工作负载是无状态

* 在 Kubernetes 上与我们讨论 [Slack:#sig-storage-cosi](https://kubernetes.slack.com/archives/C017EGC1C6N)
* 参加我们的 [Zoom 会议](https://zoom.us/j/614261834?pwd=Sk1USmtjR2t0MUdjTGVZeVVEV1BPQT09)，每周四太平洋时间 10:00
* 参与 [bucket API 提案 PR](https://github.com/kubernetes/enhancements/pull/2813) 提出你的想法、建议等。

