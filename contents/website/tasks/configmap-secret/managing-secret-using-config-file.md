---
title: 使用配置文件管理 Secret
content_type: task
weight: 20
description: 使用资源配置文件创建 Secret 对象。
---


## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}


## 创建 Secret  {#create-the-config-file}

你可以先用 JSON 或 YAML 格式在一个清单文件中定义 `Secret` 对象，然后创建该对象。
[Secret](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#secret-v1-core)
资源包含 2 个键值对：`data` 和 `stringData`。
`data` 字段用来存储 base64 编码的任意数据。
提供 `stringData` 字段是为了方便，它允许 Secret 使用未编码的字符串。
`data` 和 `stringData` 的键必须由字母、数字、`-`、`_` 或 `.` 组成。

以下示例使用 `data` 字段在 Secret 中存储两个字符串：

1. 将这些字符串转换为 base64：

   ```shell
   echo -n 'admin' | base64
   echo -n '1f2d1e2e67df' | base64
   ```

   {{< note >}}
   Secret 数据的 JSON 和 YAML 序列化结果是以 base64 编码的。
   换行符在这些字符串中无效，必须省略。
   在 Darwin/macOS 上使用 `base64` 工具时，用户不应该使用 `-b` 选项分割长行。
   相反地，Linux 用户**应该**在 `base64` 地命令中添加 `-w 0` 选项，
   或者在 `-w` 选项不可用的情况下，输入 `base64 | tr -d '\n'`。
   {{< /note >}}

   输出类似于：

   ```
   YWRtaW4=
   MWYyZDFlMmU2N2Rm
   ```
2. 创建清单：

   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: mysecret
   type: Opaque
   data:
     username: YWRtaW4=
     password: MWYyZDFlMmU2N2Rm
   ```
   注意，Secret 对象的名称必须是有效的 [DNS 子域名](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)。

3. 使用 [`kubectl apply`](/docs/reference/generated/kubectl/kubectl-commands#apply) 创建 Secret：

   ```shell
   kubectl apply -f ./secret.yaml
   ```

   输出类似于：

   ```
   secret/mysecret created
   ```
若要验证 Secret 被创建以及想要解码 Secret 数据，
请参阅[使用 kubectl 管理 Secret](/zh-cn/docs/tasks/configmap-secret/managing-secret-using-kubectl/#verify-the-secret)

### 创建 Secret 时提供未编码的数据  {#specify-unencoded-data-when-creating-a-secret}

对于某些场景，你可能希望使用 `stringData` 字段。
这个字段可以将一个非 base64 编码的字符串直接放入 Secret 中，
当创建或更新该 Secret 时，此字段将被编码。

上述用例的实际场景可能是这样：当你部署应用时，使用 Secret 存储配置文件，
你希望在部署过程中，填入部分内容到该配置文件。

例如，如果你的应用程序使用以下配置文件:

```yaml
apiUrl: "https://my.api.com/api/v1"
username: "<user>"
password: "<password>"
```

你可以使用以下定义将其存储在 Secret 中:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
stringData:
  config.yaml: |
    apiUrl: "https://my.api.com/api/v1"
    username: <user>
    password: <password>
```

当你检索 Secret 数据时，此命令将返回编码的值，并不是你在 `stringData` 中提供的纯文本值。

例如，如果你运行以下命令：

```shell
kubectl get secret mysecret -o yaml
```

输出类似于：

```yaml
apiVersion: v1
data:
  config.yaml: YXBpVXJsOiAiaHR0cHM6Ly9teS5hcGkuY29tL2FwaS92MSIKdXNlcm5hbWU6IHt7dXNlcm5hbWV9fQpwYXNzd29yZDoge3twYXNzd29yZH19
kind: Secret
metadata:
  creationTimestamp: 2018-11-15T20:40:59Z
  name: mysecret
  namespace: default
  resourceVersion: "7225"
  uid: c280ad2e-e916-11e8-98f2-025000000001
type:
```

### 同时指定 `data` 和 `stringData` {#specifying-both-data-and-stringdata}

如果你在 `data` 和 `stringData` 中设置了同一个字段，则使用来自 `stringData` 中的值。

例如，如果你定义以下 Secret：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  username: YWRtaW4=
stringData:
  username: administrator
```

所创建的 `Secret` 对象如下：

```yaml
apiVersion: v1
data:
  username: YWRtaW5pc3RyYXRvcg==
kind: Secret
metadata:
  creationTimestamp: 2018-11-15T20:46:46Z
  name: mysecret
  namespace: default
  resourceVersion: "7579"
  uid: 91460ecb-e917-11e8-98f2-025000000001
type: Opaque
```

`YWRtaW5pc3RyYXRvcg==` 解码成 `administrator`。

## 编辑 Secret {#edit-secret}

要编辑使用清单创建的 Secret 中的数据，请修改清单中的 `data` 或 `stringData` 字段并将此清单文件应用到集群。
你可以编辑现有的 `Secret` 对象，除非它是[不可变的](/zh-cn/docs/concepts/configuration/secret/#secret-immutable)。

例如，如果你想将上一个示例中的密码更改为 `birdsarentreal`，请执行以下操作：

1. 编码新密码字符串：

   ```shell
   echo -n 'birdsarentreal' | base64
   ```

   输出类似于：

   ```
   YmlyZHNhcmVudHJlYWw=
   ```

2. 使用你的新密码字符串更新 `data` 字段：

   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: mysecret
   type: Opaque
   data:
     username: YWRtaW4=
     password: YmlyZHNhcmVudHJlYWw=
   ```

3. 将清单应用到你的集群：

   ```shell
   kubectl apply -f ./secret.yaml
   ```

   输出类似于：

   ```
   secret/mysecret configured
   ```

Kubernetes 更新现有的 `Secret` 对象。具体而言，`kubectl` 工具发现存在一个同名的现有 `Secret` 对象。
`kubectl` 获取现有对象，计划对其进行更改，并将更改后的 `Secret` 对象提交到你的集群控制平面。

如果你指定了 `kubectl apply --server-side`，则 `kubectl`
使用[服务器端应用（Server-Side Apply）](/zh-cn/docs/reference/using-api/server-side-apply/)。

## 清理    {#clean-up}

删除你创建的 Secret：

```shell
kubectl delete secret mysecret
```

## {{% heading "whatsnext" %}}

- 进一步阅读 [Secret 概念](/zh-cn/docs/concepts/configuration/secret/)
- 了解如何[使用 `kubectl` 管理 Secret](/zh-cn/docs/tasks/configmap-secret/managing-secret-using-kubectl/)
- 了解如何[使用 kustomize 管理 Secret](/zh-cn/docs/tasks/configmap-secret/managing-secret-using-kustomize/)
