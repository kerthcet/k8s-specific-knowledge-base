---
title: 安全上下文（Security Context）
id: security-context
date: 2018-04-12
full_link: /zh-cn/docs/tasks/configure-pod-container/security-context/
short_description: >
  securityContext 字段定义 Pod 或容器的特权和访问控制设置，包括运行时 UID 和 GID。

aka: 
tags:
- security
---



securityContext 字段定义 {{< glossary_tooltip text="Pod" term_id="pod" >}} 或
{{< glossary_tooltip text="容器" term_id="container" >}}的特权和访问控制设置。



在一个 `securityContext` 字段中，你可以设置进程所属用户和用户组、权限相关设置。你也可以设置安全策略（例如：SELinux、AppArmor、seccomp）。	


`PodSpec.securityContext` 字段配置会应用到一个 Pod 中的所有的 container 。														 