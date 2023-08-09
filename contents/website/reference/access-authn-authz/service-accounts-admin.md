---
title: 管理服务账号
content_type: concept
weight: 50
---


**ServiceAccount** 为 Pod 中运行的进程提供了一个身份。

Pod 内的进程可以使用其关联服务账号的身份，向集群的 API 服务器进行身份认证。

有关服务账号的介绍，
请参阅[配置服务账号](/zh-cn/docs/tasks/configure-pod-container/configure-service-account/)。

本任务指南阐述有关 ServiceAccount 的几个概念。
本指南还讲解如何获取或撤销代表 ServiceAccount 的令牌。


## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

为了能够准确地跟随这些步骤，确保你有一个名为 `examplens` 的名字空间。
如果你没有，运行以下命令创建一个名字空间：

```shell
kubectl create namespace examplens
```

## 用户账号与服务账号  {#user-accounts-versus-service-accounts}

Kubernetes 区分用户账号和服务账号的概念，主要基于以下原因：

- 用户账号是针对人而言的。而服务账号是针对运行在 Pod 中的应用进程而言的，
  在 Kubernetes 中这些进程运行在容器中，而容器是 Pod 的一部分。
- 用户账号是全局性的。其名称在某集群中的所有名字空间中必须是唯一的。
  无论你查看哪个名字空间，代表用户的特定用户名都代表着同一个用户。
  在 Kubernetes 中，服务账号是名字空间作用域的。
  两个不同的名字空间可以包含具有相同名称的 ServiceAccount。
- 通常情况下，集群的用户账号可能会从企业数据库进行同步，
  创建新用户需要特殊权限，并且涉及到复杂的业务流程。
  服务账号创建有意做得更轻量，允许集群用户为了具体的任务按需创建服务账号。
  将 ServiceAccount 的创建与新用户注册的步骤分离开来，
  使工作负载更易于遵从权限最小化原则。
- 对人员和服务账号审计所考虑的因素可能不同；这种分离更容易区分不同之处。
- 针对复杂系统的配置包可能包含系统组件相关的各种服务账号的定义。
  因为服务账号的创建约束不多并且有名字空间域的名称，所以这种配置通常是轻量的。

## 绑定的服务账号令牌卷机制  {#bound-service-account-token-volume}

{{< feature-state for_k8s_version="v1.22" state="stable" >}}

默认情况下，Kubernetes 控制平面（特别是 [ServiceAccount 准入控制器](#serviceaccount-admission-controller)）
添加一个[投射卷](/zh-cn/docs/concepts/storage/projected-volumes/)到 Pod，
此卷包括了访问 Kubernetes API 的令牌。

以下示例演示如何查找已启动的 Pod：

```yaml
...
  - name: kube-api-access-<随机后缀>
    projected:
      sources:
        - serviceAccountToken:
            path: token # 必须与应用所预期的路径匹配
        - configMap:
            items:
              - key: ca.crt
                path: ca.crt
            name: kube-root-ca.crt
        - downwardAPI:
            items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
```

该清单片段定义了由三个数据源组成的投射卷。在当前场景中，每个数据源也代表该卷内的一条独立路径。这三个数据源是：

1. `serviceAccountToken` 数据源，包含 kubelet 从 kube-apiserver 获取的令牌。
   kubelet 使用 TokenRequest API 获取有时间限制的令牌。为 TokenRequest 服务的这个令牌会在
   Pod 被删除或定义的生命周期（默认为 1 小时）结束之后过期。该令牌绑定到特定的 Pod，
   并将其 audience（受众）设置为与 `kube-apiserver` 的 audience 相匹配。
   这种机制取代了之前基于 Secret 添加卷的机制，之前 Secret 代表了针对 Pod 的 ServiceAccount 但不会过期。
1. `configMap` 数据源。ConfigMap 包含一组证书颁发机构数据。
   Pod 可以使用这些证书来确保自己连接到集群的 kube-apiserver（而不是连接到中间件或意外配置错误的对等点上）。
1. `downwardAPI` 数据源，用于查找包含 Pod 的名字空间的名称，
   并使该名称信息可用于在 Pod 内运行的应用程序代码。

Pod 内挂载这个特定卷的所有容器都可以访问上述信息。

{{< note >}}
没有特定的机制可以使通过 TokenRequest 签发的令牌无效。
如果你不再信任为某个 Pod 绑定的服务账号令牌，
你可以删除该 Pod。删除 Pod 将使其绑定的服务账号令牌过期。
{{< /note >}}

## 手动管理 ServiceAccount 的 Secret   {#manual-secret-management-for-serviceaccounts}

v1.22 之前的 Kubernetes 版本会自动创建凭据访问 Kubernetes API。
这种更老的机制基于先创建令牌 Secret，然后将其挂载到正运行的 Pod 中。

在包括 Kubernetes v{{< skew currentVersion >}} 在内最近的几个版本中，使用
[TokenRequest](/zh-cn/docs/reference/kubernetes-api/authentication-resources/token-request-v1/)
API [直接获得](#bound-service-account-token-volume) API 凭据，
并使用投射卷挂载到 Pod 中。使用这种方法获得的令牌具有绑定的生命周期，
当挂载的 Pod 被删除时这些令牌将自动失效。

你仍然可以[手动创建](/zh-cn/docs/tasks/configure-pod-container/configure-service-account/#manually-create-an-api-token-for-a-serviceaccount)
Secret 来保存服务账号令牌；例如在你需要一个永不过期的令牌的时候。

一旦你手动创建一个 Secret 并将其关联到 ServiceAccount，
Kubernetes 控制平面就会自动将令牌填充到该 Secret 中。

{{< note >}}
尽管存在手动创建长久 ServiceAccount 令牌的机制，但还是推荐使用
[TokenRequest](/zh-cn/docs/reference/kubernetes-api/authentication-resources/token-request-v1/)
获得短期的 API 访问令牌。
{{< /note >}}

## 控制平面细节   {#control-plane-details}

ServiceAccount 控制器管理名字空间内的 ServiceAccount，
并确保每个活跃的名字空间中都存在名为 `default` 的 ServiceAccount。

### 令牌控制器   {#token-controller}

服务账号令牌控制器作为 `kube-controller-manager` 的一部分运行，以异步的形式工作。
其职责包括：

- 监测 ServiceAccount 的删除并删除所有相应的服务账号令牌 Secret。
- 监测服务账号令牌 Secret 的添加，保证相应的 ServiceAccount 存在，
  如有需要，向 Secret 中添加令牌。
- 监测服务账号令牌 Secret 的删除，如有需要，从相应的 ServiceAccount 中移除引用。

你必须通过 `--service-account-private-key-file` 标志为
`kube-controller-manager`的令牌控制器传入一个服务账号私钥文件。
该私钥用于为所生成的服务账号令牌签名。同样地，你需要通过
`--service-account-key-file` 标志将对应的公钥通知给
kube-apiserver。公钥用于在身份认证过程中校验令牌。

### ServiceAccount 准入控制器   {#serviceaccount-admission-controller}

对 Pod 的改动通过一个被称为[准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/)的插件来实现。
它是 API 服务器的一部分。当 Pod 被创建时，该准入控制器会同步地修改 Pod。
如果该插件处于激活状态（在大多数发行版中都是默认激活的），当 Pod 被创建时它会进行以下操作：

1. 如果该 Pod 没有设置 `.spec.serviceAccountName`，
   准入控制器为新来的 Pod 将 ServiceAccount 的名称设为 `default`。
2. 准入控制器保证新来的 Pod 所引用的 ServiceAccount 确实存在。
   如果没有 ServiceAccount 具有匹配的名称，则准入控制器拒绝新来的 Pod。
   这个检查甚至适用于 `default` ServiceAccount。
3. 如果服务账号的 `automountServiceAccountToken` 字段或 Pod 的
   `automountServiceAccountToken` 字段都未显式设置为 `false`：
   - 准入控制器变更新来的 Pod，添加一个包含 API
     访问令牌的额外{{< glossary_tooltip text="卷" term_id="volume" >}}。
   - 准入控制器将 `volumeMount` 添加到 Pod 中的每个容器，
     忽略已为 `/var/run/secrets/kubernetes.io/serviceaccount` 路径定义的卷挂载的所有容器。
     对于 Linux 容器，此卷挂载在 `/var/run/secrets/kubernetes.io/serviceaccount`；
     在 Windows 节点上，此卷挂载在等价的路径上。
4. 如果新来 Pod 的规约不包含任何 `imagePullSecrets`，则准入控制器添加 `imagePullSecrets`，
   并从 `ServiceAccount` 进行复制。

### TokenRequest API

{{< feature-state for_k8s_version="v1.22" state="stable" >}}

你使用 ServiceAccount 的
[TokenRequest](/zh-cn/docs/reference/kubernetes-api/authentication-resources/token-request-v1/)
子资源为该 ServiceAccount 获取有时间限制的令牌。
你不需要调用它来获取在容器中使用的 API 令牌，
因为 kubelet 使用**投射卷**对此进行了设置。

如果你想要从 `kubectl` 使用 TokenRequest API，
请参阅[为 ServiceAccount 手动创建 API 令牌](/zh-cn/docs/tasks/configure-pod-container/configure-service-account/#manually-create-an-api-token-for-a-serviceaccount)。

Kubernetes 控制平面（特别是 ServiceAccount 准入控制器）向 Pod 添加了一个投射卷，
kubelet 确保该卷包含允许容器作为正确 ServiceAccount 进行身份认证的令牌。

（这种机制取代了之前基于 Secret 添加卷的机制，之前 Secret 代表了 Pod 所用的 ServiceAccount 但不会过期。）

以下示例演示如何查找已启动的 Pod：

```yaml
...
  - name: kube-api-access-<random-suffix>
    projected:
      defaultMode: 420 # 这个十进制数等同于八进制 0644
      sources:
        - serviceAccountToken:
            expirationSeconds: 3607
            path: token
        - configMap:
            items:
              - key: ca.crt
                path: ca.crt
            name: kube-root-ca.crt
        - downwardAPI:
            items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
```

该清单片段定义了由三个数据源信息组成的投射卷。

1. `serviceAccountToken` 数据源，包含 kubelet 从 kube-apiserver 获取的令牌。
   kubelet 使用 TokenRequest API 获取有时间限制的令牌。为 TokenRequest 服务的这个令牌会在
   Pod 被删除或定义的生命周期（默认为 1 小时）结束之后过期。在令牌过期之前，kubelet 还会刷新该令牌。
   该令牌绑定到特定的 Pod，并将其 audience（受众）设置为与 `kube-apiserver` 的 audience 相匹配。
1. `configMap` 数据源。ConfigMap 包含一组证书颁发机构数据。
   Pod 可以使用这些证书来确保自己连接到集群的 kube-apiserver（而不是连接到中间件或意外配置错误的对等点上）。
1. `downwardAPI` 数据源。这个 `downwardAPI` 卷获得包含 Pod 的名字空间的名称，
   并使该名称信息可用于在 Pod 内运行的应用程序代码。

挂载此卷的 Pod 内的所有容器均可以访问上述信息。

## 创建额外的 API 令牌   {#create-token}

{{< caution >}}
只有[令牌请求](#tokenrequest-api)机制不合适，才需要创建长久的 API 令牌。
令牌请求机制提供有时间限制的令牌；因为随着这些令牌过期，它们对信息安全方面的风险也会降低。
{{< /caution >}}

要为 ServiceAccount 创建一个不过期、持久化的 API 令牌，
请创建一个类型为 `kubernetes.io/service-account-token` 的 Secret，
附带引用 ServiceAccount 的注解。控制平面随后生成一个长久的令牌，
并使用生成的令牌数据更新该 Secret。

以下是此类 Secret 的示例清单：

{{< codenew file="secret/serviceaccount/mysecretname.yaml" >}}

若要基于此示例创建 Secret，运行以下命令：

```shell
kubectl -n examplens create -f https://k8s.io/examples/secret/serviceaccount/mysecretname.yaml
```

若要查看该 Secret 的详细信息，运行以下命令：

```shell
kubectl -n examplens describe secret mysecretname
```

输出类似于：

```
Name:           mysecretname
Namespace:      examplens
Labels:         <none>
Annotations:    kubernetes.io/service-account.name=myserviceaccount
                kubernetes.io/service-account.uid=8a85c4c4-8483-11e9-bc42-526af7764f64

Type:   kubernetes.io/service-account-token

Data
====
ca.crt:         1362 bytes
namespace:      9 bytes
token:          ...
```

如果你在 `examplens` 名字空间中启动一个新的 Pod，它可以使用你刚刚创建的
`myserviceaccount` service-account-token Secret。

## 删除/废止 ServiceAccount 令牌   {#delete-token}

如果你知道 Secret 的名称且该 Secret 包含要移除的令牌：

```shell
kubectl delete secret name-of-secret
```

否则，先找到 ServiceAccount 所用的 Secret。

```shell
# 此处假设你已有一个名为 'examplens' 的名字空间
kubectl -n examplens get serviceaccount/example-automated-thing -o yaml
```

输出类似于：

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"ServiceAccount","metadata":{"annotations":{},"name":"example-automated-thing","namespace":"examplens"}}
  creationTimestamp: "2019-07-21T07:07:07Z"
  name: example-automated-thing
  namespace: examplens
  resourceVersion: "777"
  selfLink: /api/v1/namespaces/examplens/serviceaccounts/example-automated-thing
  uid: f23fd170-66f2-4697-b049-e1e266b7f835
secrets:
  - name: example-automated-thing-token-zyxwv
```

随后删除你现在知道名称的 Secret：

```shell
kubectl -n examplens delete secret/example-automated-thing-token-zyxwv
```

控制平面发现 ServiceAccount 缺少其 Secret，并创建一个替代项：

```shell
kubectl -n examplens get serviceaccount/example-automated-thing -o yaml
```

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"ServiceAccount","metadata":{"annotations":{},"name":"example-automated-thing","namespace":"examplens"}}
  creationTimestamp: "2019-07-21T07:07:07Z"
  name: example-automated-thing
  namespace: examplens
  resourceVersion: "1026"
  selfLink: /api/v1/namespaces/examplens/serviceaccounts/example-automated-thing
  uid: f23fd170-66f2-4697-b049-e1e266b7f835
secrets:
  - name: example-automated-thing-token-4rdrh
```

## 清理    {#clean-up}

如果创建了一个 `examplens` 名字空间进行试验，你可以移除它：

```shell
kubectl delete namespace examplens
```

## {{% heading "whatsnext" %}}

- 查阅有关[投射卷](/zh-cn/docs/concepts/storage/projected-volumes/)的更多细节。
