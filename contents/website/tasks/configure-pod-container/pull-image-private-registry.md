---
title: 从私有仓库拉取镜像
content_type: task
weight: 130
---



本文介绍如何使用 {{< glossary_tooltip text="Secret" term_id="secret" >}} 
从私有的镜像仓库或代码仓库拉取镜像来创建 Pod。
有很多私有镜像仓库正在使用中。这个任务使用的镜像仓库是
[Docker Hub](https://www.docker.com/products/docker-hub)。

{{% thirdparty-content single="true" %}}

## {{% heading "prerequisites" %}}

* {{< include "task-tutorial-prereqs.md" >}}


* 要进行此练习，你需要 `docker` 命令行工具和一个知道密码的 
[Docker ID](https://docs.docker.com/docker-id/)。
* 如果你要使用不同的私有的镜像仓库，你需要有对应镜像仓库的命令行工具和登录信息。


## 登录 Docker 镜像仓库  {#log-in-to-docker-hub}

在个人电脑上，要想拉取私有镜像必须在镜像仓库上进行身份验证。

使用 `docker` 命令工具来登录到 Docker Hub。
更多详细信息，请查阅
[Docker ID accounts](https://docs.docker.com/docker-id/#log-in) 中的 **log in** 部分。

```shell
docker login
```

当出现提示时，输入你的 Docker ID 和登录凭证（访问令牌、
或 Docker ID 的密码）。

登录过程会创建或更新保存有授权令牌的 `config.json` 文件。
查看 [Kubernetes 中如何解析这个文件](/zh-cn/docs/concepts/containers/images#config-json)。

查看 `config.json` 文件：

```shell
cat ~/.docker/config.json
```

输出结果包含类似于以下内容的部分：

```json
{
    "auths": {
        "https://index.docker.io/v1/": {
            "auth": "c3R...zE2"
        }
    }
}
```

{{< note >}}
如果使用 Docker 凭证仓库，则不会看到 `auth` 条目，看到的将是以仓库名称作为值的 `credsStore` 条目。
在这种情况下，你可以直接创建一个 Secret。请参阅[在命令行上提供凭证来创建 Secret](#create-a-secret-by-providing-credentials-on-the-command-line)。
{{< /note >}}

## 创建一个基于现有凭证的 Secret  {#registry-secret-existing-credentials}

Kubernetes 集群使用 `kubernetes.io/dockerconfigjson` 类型的
Secret 来通过镜像仓库的身份验证，进而提取私有镜像。

如果你已经运行了 `docker login` 命令，你可以复制该镜像仓库的凭证到 Kubernetes:

```shell
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=<path/to/.docker/config.json> \
    --type=kubernetes.io/dockerconfigjson
```

如果你需要更多的设置（例如，为新 Secret 设置名字空间或标签），
则可以在存储 Secret 之前对它进行自定义。
请务必：

- 将 data 项中的名称设置为 `.dockerconfigjson`
- 使用 base64 编码方法对 Docker 配置文件进行编码，然后粘贴该字符串的内容，作为字段
  `data[".dockerconfigjson"]` 的值
- 将 `type` 设置为 `kubernetes.io/dockerconfigjson`

示例：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myregistrykey
  namespace: awesomeapps
data:
  .dockerconfigjson: UmVhbGx5IHJlYWxseSByZWVlZWVlZWVlZWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGx5eXl5eXl5eXl5eXl5eXl5eXl5eSBsbGxsbGxsbGxsbGxsbG9vb29vb29vb29vb29vb29vb29vb29vb29vb25ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubmdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cgYXV0aCBrZXlzCg==
type: kubernetes.io/dockerconfigjson
```

如果你收到错误消息：`error: no objects passed to create`，
这可能意味着 base64 编码的字符串是无效的。如果你收到类似
`Secret "myregistrykey" is invalid: data[.dockerconfigjson]: invalid value ...`
的错误消息，则表示数据中的 base64 编码字符串已成功解码，
但无法解析为 `.docker/config.json` 文件。

## 在命令行上提供凭证来创建 Secret  {#create-a-secret-by-providing-credentials-on-the-command-line}

创建 Secret，命名为 `regcred`：

```shell
kubectl create secret docker-registry regcred \
  --docker-server=<你的镜像仓库服务器> \
  --docker-username=<你的用户名> \
  --docker-password=<你的密码> \
  --docker-email=<你的邮箱地址>
```

在这里：

* `<your-registry-server>` 是你的私有 Docker 仓库全限定域名（FQDN）。
  DockerHub 使用 `https://index.docker.io/v1/`。
* `<your-name>` 是你的 Docker 用户名。
* `<your-pword>` 是你的 Docker 密码。
* `<your-email>` 是你的 Docker 邮箱。

这样你就成功地将集群中的 Docker 凭证设置为名为 `regcred` 的 Secret。

{{< note >}}
在命令行上键入 Secret 可能会将它们存储在你的 shell 历史记录中而不受保护，
并且这些 Secret 信息也可能在 `kubectl` 运行期间对你 PC 上的其他用户可见。
{{< /note >}}

## 检查 Secret `regcred`  {#inspecting-the-secret-regcred}

要了解你创建的 `regcred` Secret 的内容，可以用 YAML 格式进行查看：

```shell
kubectl get secret regcred --output=yaml
```

输出和下面类似：

```yaml
apiVersion: v1
data:
  .dockerconfigjson: eyJodHRwczovL2luZGV4L ... J0QUl6RTIifX0=
kind: Secret
metadata:
  ...
  name: regcred
  ...
data:
  .dockerconfigjson: eyJodHRwczovL2luZGV4L ... J0QUl6RTIifX0=
type: kubernetes.io/dockerconfigjson
```

`.dockerconfigjson` 字段的值是 Docker 凭证的 base64 表示。

要了解 `dockerconfigjson` 字段中的内容，请将 Secret 数据转换为可读格式：

```shell
kubectl get secret regcred --output="jsonpath={.data.\.dockerconfigjson}" | base64 --decode
```

输出和下面类似：

```json
{"auths":{"your.private.registry.example.com":{"username":"janedoe","password":"xxxxxxxxxxx","email":"jdoe@example.com","auth":"c3R...zE2"}}}
```

要了解 `auth` 字段中的内容，请将 base64 编码过的数据转换为可读格式：

```shell
echo "c3R...zE2" | base64 --decode
```

输出结果中，用户名和密码用 `:` 链接，类似下面这样：

```none
janedoe:xxxxxxxxxxx
```

注意，Secret 数据包含与本地 `~/.docker/config.json` 文件类似的授权令牌。

这样你就已经成功地将 Docker 凭证设置为集群中的名为 `regcred` 的 Secret。

## 创建一个使用你的 Secret 的 Pod  {#create-a-pod-that-uses-your-secret}

下面是一个 Pod 配置清单示例，该示例中 Pod 需要访问你的 Docker 凭证 `regcred`：

{{< codenew file="pods/private-reg-pod.yaml" >}}


将上述文件下载到你的计算机中：

```shell
curl -L -o my-private-reg-pod.yaml https://k8s.io/examples/pods/private-reg-pod.yaml
```

在 `my-private-reg-pod.yaml` 文件中，使用私有仓库的镜像路径替换 `<your-private-image>`，例如：

```none
your.private.registry.example.com/janedoe/jdoe-private:v1
```

要从私有仓库拉取镜像，Kubernetes 需要凭证。
配置文件中的 `imagePullSecrets` 字段表明 Kubernetes 应该通过名为 `regcred` 的 Secret 获取凭证。

创建使用了你的 Secret 的 Pod，并检查它是否正常运行：

```shell
kubectl apply -f my-private-reg-pod.yaml
kubectl get pod private-reg
```

## {{% heading "whatsnext" %}}


* 进一步了解 [Secret](/zh-cn/docs/concepts/configuration/secret/)
  * 或阅读 {{< api-reference page="config-and-storage-resources/secret-v1" >}} 的 API 参考
* 进一步了解[使用私有仓库](/zh-cn/docs/concepts/containers/images/#using-a-private-registry)
* 进一步了解[为服务账户添加拉取镜像凭证](/zh-cn/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account)
* 查看 [kubectl 创建 docker-registry 凭证](/docs/reference/generated/kubectl/kubectl-commands/#-em-secret-docker-registry-em-)
* 查看 Pod [容器定义](/zh-cn/docs/reference/kubernetes-api/workload-resources/pod-v1/#containers)中的 `imagePullSecrets` 字段。
