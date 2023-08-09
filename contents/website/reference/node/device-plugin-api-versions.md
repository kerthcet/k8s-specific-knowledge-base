---
content_type: "reference"
title: Kubelet 设备管理器 API 版本
weight: 10
---

本页详述了 Kubernetes
[设备插件 API](https://github.com/kubernetes/kubelet/tree/master/pkg/apis/deviceplugin)
与不同版本的 Kubernetes 本身之间的版本兼容性。

## 兼容性矩阵   {#compatibility-matrix}

|                 |  `v1alpha1` | `v1beta1`   |
|-----------------|-------------|-------------|
| Kubernetes 1.21 |  -          | ✓           |
| Kubernetes 1.22 |  -          | ✓           |
| Kubernetes 1.23 |  -          | ✓           |
| Kubernetes 1.24 |  -          | ✓           |
| Kubernetes 1.25 |  -          | ✓           |
| Kubernetes 1.26 |  -          | ✓           |

简要说明：

* `✓` 设备插件 API 和 Kubernetes 版本中的特性或 API 对象完全相同。
* `+` 设备插件 API 具有 Kubernetes 集群中可能不存在的特性或 API 对象，
  不是因为设备插件 API 添加了额外的新 API 调用，就是因为服务器移除了旧的 API 调用。
  但它们的共同点是（大多数其他 API）都能工作。
  请注意，Alpha API 可能会在次要版本的迭代过程中消失或出现重大变更。
* `-` Kubernetes 集群具有设备插件 API 无法使用的特性，不是因为服务器添加了额外的 API 调用，
  就是因为设备插件 API 移除了旧的 API 调用。但它们的共同点是（大多数 API）都能工作。
