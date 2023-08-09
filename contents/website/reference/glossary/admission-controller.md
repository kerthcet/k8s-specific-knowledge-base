---
title: 准入控制器（Admission Controller）
id: admission-controller
date: 2019-06-28
full_link: /zh-cn/docs/reference/access-authn-authz/admission-controllers/
short_description: >
 在对象持久化之前拦截 Kubernetes API 服务器请求的一段代码。
aka:
tags:
- extension
- security
---

在对象持久化之前拦截 Kubernetes API 服务器请求的一段代码。


准入控制器可针对 Kubernetes API 服务器进行配置，可以执行“验证（validating）“、“变更（mutating）“或两者都执行。
任何准入控制器都可以拒绝访问请求。
变更控制器可以修改其允许的对象，验证控制器则不可以。

* [Kubernetes 文档中的准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/)
