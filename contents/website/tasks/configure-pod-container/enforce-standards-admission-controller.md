---
title: 通过配置内置准入控制器实施 Pod 安全标准
content_type: task
weight: 240
---

Kubernetes 提供一种内置的[准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#podsecurity)
用来强制实施 [Pod 安全性标准](/zh-cn/docs/concepts/security/pod-security-standards)。
你可以配置此准入控制器来设置集群范围的默认值和[豁免选项](/zh-cn/docs/concepts/security/pod-security-admission/#exemptions)。

## {{% heading "prerequisites" %}}

Pod 安全性准入（Pod Security Admission）在 Kubernetes v1.22 作为 Alpha 特性发布，
在 Kubernetes v1.23 中作为 Beta 特性默认可用。从 1.25 版本起，
此特性进阶至正式发布（Generally Available）。

{{% version-check %}}

如果未运行 Kubernetes {{< skew currentVersion >}}，
你可以切换到与当前运行的 Kubernetes 版本所对应的文档。

## 配置准入控制器    {#configure-the-admission-controller}

{{< note >}}
`pod-security.admission.config.k8s.io/v1` 配置需要 v1.25+。
对于 v1.23 和 v1.24，使用
[v1beta1](https://v1-24.docs.kubernetes.io/zh-cn/docs/tasks/configure-pod-container/enforce-standards-admission-controller/)。
对于 v1.22，使用
[v1alpha1](https://v1-22.docs.kubernetes.io/docs/tasks/configure-pod-container/enforce-standards-admission-controller/)。
{{< /note >}}

```yaml
apiVersion: apiserver.config.k8s.io/v1 # 查阅兼容性说明
kind: AdmissionConfiguration
plugins:
- name: PodSecurity
  configuration:
    apiVersion: pod-security.admission.config.k8s.io/v1
    kind: PodSecurityConfiguration
    # 当未设置 mode 标签时会应用的默认设置
    #
    # level 标签必须是以下取值之一：
    # - "privileged" (默认)
    # - "baseline"
    # - "restricted"
    #
    # version 标签必须是如下取值之一：
    # - "latest" (默认) 
    # - 诸如 "v{{< skew currentVersion>}}" 这类版本号
    defaults:
      enforce: "privileged"
      enforce-version: "latest"
      audit: "privileged"
      audit-version: "latest"
      warn: "privileged"
      warn-version: "latest"
    exemptions:
      # 要豁免的已认证用户名列表
      usernames: []
      # 要豁免的运行时类名称列表
      runtimeClasses: []
      # 要豁免的名字空间列表
      namespaces: []
```


{{< note >}}
上面的清单需要通过 `——admission-control-config-file` 指定到 kube-apiserver。
{{< /note >}}

{{< note >}}
上面的清单需要通过 `--admission-control-config-file` 指定给 kube-apiserver。
{{< /note >}}

