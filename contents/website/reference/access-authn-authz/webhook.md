---
title: Webhook 模式
content_type: concept
weight: 100
---


WebHook 是一种 HTTP 回调：某些条件下触发的 HTTP POST 请求；通过 HTTP POST
发送的简单事件通知。一个基于 web 应用实现的 WebHook 会在特定事件发生时把消息发送给特定的 URL。



具体来说，当在判断用户权限时，`Webhook` 模式会使 Kubernetes 查询外部的 REST 服务。

## 配置文件格式 {#configuration-file-format}

`Webhook` 模式需要一个 HTTP 配置文件，通过
`--authorization-webhook-config-file=SOME_FILENAME` 的参数声明。

配置文件的格式使用
[kubeconfig](/zh-cn/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)。
在该文件中，“users” 代表着 API 服务器的 webhook，而 “cluster” 代表着远程服务。

使用 HTTPS 客户端认证的配置例子：

```yaml
# Kubernetes API 版本
apiVersion: v1
# API 对象种类
kind: Config
# clusters 代表远程服务。
clusters:
  - name: name-of-remote-authz-service
    cluster:
      # 对远程服务进行身份认证的 CA。
      certificate-authority: /path/to/ca.pem
      # 远程服务的查询 URL。必须使用 'https'。
      server: https://authz.example.com/authorize

# users 代表 API 服务器的 webhook 配置
users:
  - name: name-of-api-server
    user:
      client-certificate: /path/to/cert.pem # webhook plugin 使用 cert
      client-key: /path/to/key.pem          # cert 所对应的 key

# kubeconfig 文件必须有 context。需要提供一个给 API 服务器。
current-context: webhook
contexts:
- context:
    cluster: name-of-remote-authz-service
    user: name-of-api-server
  name: webhook
```

## 请求载荷 {#request-payloads}

在做认证决策时，API 服务器会 POST 一个 JSON 序列化的 `authorization.k8s.io/v1beta1` `SubjectAccessReview`
对象来描述这个动作。这个对象包含了描述用户请求的字段，同时也包含了需要被访问资源或请求特征的具体信息。

需要注意的是 webhook API 对象与其他 Kubernetes API
对象一样都同样都遵从[版本兼容规则](/zh-cn/docs/concepts/overview/kubernetes-api/)。
实施人员应该了解 beta 对象的更宽松的兼容性承诺，同时确认请求的 "apiVersion" 字段能被正确地反序列化。
此外，API 服务器还必须启用 `authorization.k8s.io/v1beta1` API 扩展组 (`--runtime-config=authorization.k8s.io/v1beta1=true`)。

一个请求内容的例子：

```json
{
  "apiVersion": "authorization.k8s.io/v1beta1",
  "kind": "SubjectAccessReview",
  "spec": {
    "resourceAttributes": {
      "namespace": "kittensandponies",
      "verb": "get",
      "group": "unicorn.example.org",
      "resource": "pods"
    },
    "user": "jane",
    "group": [
      "group1",
      "group2"
    ]
  }
}
```

期待远程服务填充请求的 `status` 字段并响应允许或禁止访问。响应主体的 `spec` 字段被忽略，可以省略。允许的响应将返回:

```json
{
  "apiVersion": "authorization.k8s.io/v1beta1",
  "kind": "SubjectAccessReview",
  "status": {
    "allowed": true
  }
}
```

为了禁止访问，有两种方法。

在大多数情况下，第一种方法是首选方法，它指示授权 webhook 不允许或对请求 “无意见”。
但是，如果配置了其他授权者，则可以给他们机会允许请求。如果没有其他授权者，或者没有一个授权者，则该请求被禁止。webhook 将返回：

```json
{
  "apiVersion": "authorization.k8s.io/v1beta1",
  "kind": "SubjectAccessReview",
  "status": {
    "allowed": false,
    "reason": "user does not have read access to the namespace"
  }
}
```

第二种方法立即拒绝其他配置的授权者进行短路评估。仅应由对集群的完整授权者配置有详细了解的 webhook 使用。webhook 将返回：

```json
{
  "apiVersion": "authorization.k8s.io/v1beta1",
  "kind": "SubjectAccessReview",
  "status": {
    "allowed": false,
    "denied": true,
    "reason": "user does not have read access to the namespace"
  }
}
```

对于非资源的路径访问是这么发送的:

```json
{
  "apiVersion": "authorization.k8s.io/v1beta1",
  "kind": "SubjectAccessReview",
  "spec": {
    "nonResourceAttributes": {
      "path": "/debug",
      "verb": "get"
    },
    "user": "jane",
    "group": [
      "group1",
      "group2"
    ]
  }
}
```

非资源类的路径包括：`/api`、`/apis`、`/metrics`、`/logs`、`/debug`、
`/healthz`、`/livez`、`/openapi/v2`、`/readyz`、和 `/version`。
客户端需要访问 `/api`、`/api/*`、`/apis`、`/apis/*` 和 `/version` 以便
能发现服务器上有什么资源和版本。对于其他非资源类的路径访问在没有 REST API 访问限制的情况下拒绝。

更多信息可以参考 authorization.v1beta1 API 对象和
[webhook.go](https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apiserver/plugin/pkg/authorizer/webhook/webhook.go)。

