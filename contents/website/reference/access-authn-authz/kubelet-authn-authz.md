---
title: Kubelet 认证/鉴权
weight: 110
---

## 概述  {#overview}

kubelet 的 HTTPS 端点公开了 API，
这些 API 可以访问敏感度不同的数据，
并允许你在节点上和容器内以不同级别的权限执行操作。

本文档介绍了如何对 kubelet 的 HTTPS 端点的访问进行认证和鉴权。

## Kubelet 身份认证   {#kubelet-authentication}

默认情况下，未被已配置的其他身份认证方法拒绝的对 kubelet 的 HTTPS 端点的请求会被视为匿名请求，
并被赋予 `system:anonymous` 用户名和 `system:unauthenticated` 组。

要禁用匿名访问并向未经身份认证的请求发送 `401 Unauthorized` 响应，请执行以下操作：

* 带 `--anonymous-auth=false` 标志启动 kubelet

要对 kubelet 的 HTTPS 端点启用 X509 客户端证书认证：

* 带 `--client-ca-file` 标志启动 kubelet，提供一个 CA 证书包以供验证客户端证书
* 带 `--kubelet-client-certificate` 和 `--kubelet-client-key` 标志启动 API 服务器
* 有关更多详细信息，请参见
  [API 服务器身份验证文档](/zh-cn/docs/reference/access-authn-authz/authentication/#x509-client-certs)

要启用 API 持有者令牌（包括服务帐户令牌）以对 kubelet 的 HTTPS 端点进行身份验证，请执行以下操作：

* 确保在 API 服务器中启用了 `authentication.k8s.io/v1beta1` API 组
* 带 `--authentication-token-webhook` 和 `--kubeconfig` 标志启动 kubelet
* kubelet 调用已配置的 API 服务器上的 `TokenReview` API，以根据持有者令牌确定用户信息

## Kubelet 鉴权   {#kubelet-authorization}

任何成功通过身份验证的请求（包括匿名请求）之后都会被鉴权。
默认的鉴权模式为 `AlwaysAllow`，它允许所有请求。

细分对 kubelet API 的访问权限可能有多种原因：

* 启用了匿名身份验证，但是应限制匿名用户调用 kubelet API 的能力
* 启用了持有者令牌认证，但应限制任意 API 用户（如服务帐户）调用 kubelet API 的能力
* 启用了客户端证书身份验证，但仅应允许已配置的 CA 签名的某些客户端证书使用 kubelet API

要细分对 kubelet API 的访问权限，请将鉴权委派给 API 服务器：

* 确保在 API 服务器中启用了 `authorization.k8s.io/v1beta1` API 组
* 带 `--authorization-mode=Webhook` 和 `--kubeconfig` 标志启动 kubelet
* kubelet 调用已配置的 API 服务器上的 `SubjectAccessReview` API，
  以确定每个请求是否得到鉴权

kubelet 使用与 API 服务器相同的
[请求属性](/zh-cn/docs/reference/access-authn-authz/authorization/#review-your-request-attributes)
方法对 API 请求执行鉴权。

请求的动词根据传入请求的 HTTP 动词确定：

HTTP 动词 | 请求动词
----------|---------------
POST      | create
GET, HEAD | get
PUT       | update
PATCH     | patch
DELETE    | delete

资源和子资源是根据传入请求的路径确定的：

Kubelet API  | 资源 | 子资源
-------------|----------|------------
/stats/\*     | nodes    | stats
/metrics/\*   | nodes    | metrics
/logs/\*      | nodes    | log
/spec/\*      | nodes    | spec
**其它所有**  | nodes    | proxy

名字空间和 API 组属性始终是空字符串，
资源名称始终是 kubelet 的 `Node` API 对象的名称。

在此模式下运行时，请确保传递给 API 服务器的由 `--kubelet-client-certificate` 和
`--kubelet-client-key` 标志标识的用户具有以下属性的鉴权：

* verb=\*, resource=nodes, subresource=proxy
* verb=\*, resource=nodes, subresource=stats
* verb=\*, resource=nodes, subresource=log
* verb=\*, resource=nodes, subresource=spec
* verb=\*, resource=nodes, subresource=metrics
