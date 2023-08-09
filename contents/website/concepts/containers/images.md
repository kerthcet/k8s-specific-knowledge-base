---
title: 镜像
content_type: concept
weight: 10
hide_summary: true # 在章节索引中单独列出
---


容器镜像（Image）所承载的是封装了应用程序及其所有软件依赖的二进制数据。
容器镜像是可执行的软件包，可以单独运行；该软件包对所处的运行时环境具有良定（Well Defined）的假定。

你通常会创建应用的容器镜像并将其推送到某仓库（Registry），然后在
{{< glossary_tooltip text="Pod" term_id="pod" >}} 中引用它。

本页概要介绍容器镜像的概念。

{{< note >}}
如果你正在寻找 Kubernetes 某个发行版本（如最新次要版本 v{{< skew latestVersion >}}）
的容器镜像，请访问[下载 Kubernetes](/zh-cn/releases/download/)。
{{< /note >}}


## 镜像名称    {#image-names}

容器镜像通常会被赋予 `pause`、`example/mycontainer` 或者 `kube-apiserver` 这类的名称。
镜像名称也可以包含所在仓库的主机名。例如：`fictional.registry.example/imagename`。
还可以包含仓库的端口号，例如：`fictional.registry.example:10443/imagename`。

如果你不指定仓库的主机名，Kubernetes 认为你在使用 Docker 公共仓库。

在镜像名称之后，你可以添加一个**标签（Tag）**（与使用 `docker` 或 `podman` 等命令时的方式相同）。
使用标签能让你辨识同一镜像序列中的不同版本。

镜像标签可以包含小写字母、大写字母、数字、下划线（`_`）、句点（`.`）和连字符（`-`）。
关于在镜像标签中何处可以使用分隔字符（`_`、`-` 和 `.`）还有一些额外的规则。
如果你不指定标签，Kubernetes 认为你想使用标签 `latest`。

## 更新镜像  {#updating-images}

当你最初创建一个 {{< glossary_tooltip text="Deployment" term_id="deployment" >}}、
{{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}}、Pod
或者其他包含 Pod 模板的对象时，如果没有显式设定的话，
Pod 中所有容器的默认镜像拉取策略是 `IfNotPresent`。这一策略会使得
{{< glossary_tooltip text="kubelet" term_id="kubelet" >}}
在镜像已经存在的情况下直接略过拉取镜像的操作。

### 镜像拉取策略   {#image-pull-policy}

容器的 `imagePullPolicy` 和镜像的标签会影响
[kubelet](/zh-cn/docs/reference/command-line-tools-reference/kubelet/) 尝试拉取（下载）指定的镜像。

以下列表包含了 `imagePullPolicy` 可以设置的值，以及这些值的效果：

`IfNotPresent`
: 只有当镜像在本地不存在时才会拉取。

`Always`
: 每当 kubelet 启动一个容器时，kubelet 会查询容器的镜像仓库，
  将名称解析为一个镜像[摘要](https://docs.docker.com/engine/reference/commandline/pull/#pull-an-image-by-digest-immutable-identifier)。
  如果 kubelet 有一个容器镜像，并且对应的摘要已在本地缓存，kubelet 就会使用其缓存的镜像；
  否则，kubelet 就会使用解析后的摘要拉取镜像，并使用该镜像来启动容器。

`Never`
: Kubelet 不会尝试获取镜像。如果镜像已经以某种方式存在本地，
  kubelet 会尝试启动容器；否则，会启动失败。
  更多细节见[提前拉取镜像](#pre-pulled-images)。

只要能够可靠地访问镜像仓库，底层镜像提供者的缓存语义甚至可以使 `imagePullPolicy: Always` 高效。
你的容器运行时可以注意到节点上已经存在的镜像层，这样就不需要再次下载。

{{< note >}}
在生产环境中部署容器时，你应该避免使用 `:latest` 标签，因为这使得正在运行的镜像的版本难以追踪，并且难以正确地回滚。

相反，应指定一个有意义的标签，如 `v1.42.0`，和/或者一个摘要。
{{< /note >}}

为了确保 Pod 总是使用相同版本的容器镜像，你可以指定镜像的摘要；
将 `<image-name>:<tag>` 替换为 `<image-name>@<digest>`，例如 `image@sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2`。

当使用镜像标签时，如果镜像仓库修改了代码所对应的镜像标签，可能会出现新旧代码混杂在 Pod 中运行的情况。
镜像摘要唯一标识了镜像的特定版本，因此 Kubernetes 每次启动具有指定镜像名称和摘要的容器时，都会运行相同的代码。
通过摘要指定镜像可固定你运行的代码，这样镜像仓库的变化就不会导致版本的混杂。

有一些第三方的[准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/)
在创建 Pod（和 Pod 模板）时产生变更，这样运行的工作负载就是根据镜像摘要，而不是标签来定义的。
无论镜像仓库上的标签发生什么变化，你都想确保你所有的工作负载都运行相同的代码，那么指定镜像摘要会很有用。

#### 默认镜像拉取策略    {#imagepullpolicy-defaulting}

当你（或控制器）向 API 服务器提交一个新的 Pod 时，你的集群会在满足特定条件时设置 `imagePullPolicy` 字段：

- 如果你省略了 `imagePullPolicy` 字段，并且你为容器镜像指定了摘要，
  那么 `imagePullPolicy` 会自动设置为 `IfNotPresent`。

- 如果你省略了 `imagePullPolicy` 字段，并且容器镜像的标签是 `:latest`，
  `imagePullPolicy` 会自动设置为 `Always`。
- 如果你省略了 `imagePullPolicy` 字段，并且没有指定容器镜像的标签，
  `imagePullPolicy` 会自动设置为 `Always`。
- 如果你省略了 `imagePullPolicy` 字段，并且为容器镜像指定了非 `:latest` 的标签，
  `imagePullPolicy` 就会自动设置为 `IfNotPresent`。

{{< note >}}
容器的 `imagePullPolicy` 的值总是在对象初次 _创建_ 时设置的，
如果后来镜像的标签或摘要发生变化，则不会更新。

例如，如果你用一个 **非** `:latest` 的镜像标签创建一个 Deployment，
并在随后更新该 Deployment 的镜像标签为 `:latest`，则 `imagePullPolicy` 字段 **不会** 变成 `Always`。
你必须手动更改已经创建的资源的拉取策略。
{{< /note >}}

#### 必要的镜像拉取   {#required-image-pull}

如果你想总是强制执行拉取，你可以使用下述的一中方式：

- 设置容器的 `imagePullPolicy` 为 `Always`。
- 省略 `imagePullPolicy`，并使用 `:latest` 作为镜像标签；
  当你提交 Pod 时，Kubernetes 会将策略设置为 `Always`。
- 省略 `imagePullPolicy` 和镜像的标签；
  当你提交 Pod 时，Kubernetes 会将策略设置为 `Always`。
- 启用准入控制器 [AlwaysPullImages](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#alwayspullimages)。

### ImagePullBackOff

当 kubelet 使用容器运行时创建 Pod 时，容器可能因为 `ImagePullBackOff` 导致状态为
[Waiting](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#container-state-waiting)。

`ImagePullBackOff` 状态意味着容器无法启动，
因为 Kubernetes 无法拉取容器镜像（原因包括无效的镜像名称，或从私有仓库拉取而没有 `imagePullSecret`）。
`BackOff` 部分表示 Kubernetes 将继续尝试拉取镜像，并增加回退延迟。

Kubernetes 会增加每次尝试之间的延迟，直到达到编译限制，即 300 秒（5 分钟）。

## 串行和并行镜像拉取  {#serial-and-parallel-image-pulls}

默认情况下，kubelet 以串行方式拉取镜像。
也就是说，kubelet 一次只向镜像服务发送一个镜像拉取请求。
其他镜像拉取请求必须等待，直到正在处理的那个请求完成。

节点独立地做出镜像拉取的决策。即使你使用串行的镜像拉取，两个不同的节点也可以并行拉取相同的镜像。

如果你想启用并行镜像拉取，可以在 [kubelet 配置](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/)
中将字段 `serializeImagePulls` 设置为 false。

当`serializeImagePulls` 设置为 false 时，kubelet 会立即向镜像服务发送镜像拉取请求，多个镜像将同时被拉动。

启用并行镜像拉取时，请确保你的容器运行时的镜像服务可以处理并行镜像拉取。

kubelet 从不代表一个 Pod 并行地拉取多个镜像。

例如，如果你有一个 Pod，它有一个初始容器和一个应用容器，那么这两个容器的镜像拉取将不会并行。
但是，如果你有两个使用不同镜像的 Pod，当启用并行镜像拉取时，kubelet 会代表两个不同的 Pod 并行拉取镜像。

### 最大并行镜像拉取数量  {#maximum-parallel-image-pulls}

{{< feature-state for_k8s_version="v1.27" state="alpha" >}}

当 `serializeImagePulls` 被设置为 false 时，kubelet 默认对同时拉取的最大镜像数量没有限制。
如果你想限制并行镜像拉取的数量，可以在 kubelet 配置中设置字段 `maxParallelImagePulls`。
当 `maxParallelImagePulls` 设置为 _n_ 时，只能同时拉取 _n_ 个镜像，
超过 _n_ 的任何镜像都必须等到至少一个正在进行拉取的镜像拉取完成后，才能拉取。

当启用并行镜像拉取时，限制并行镜像拉取的数量可以防止镜像拉取消耗过多的网络带宽或磁盘 I/O。

你可以将 `maxParallelImagePulls` 设置为大于或等于 1 的正数。
如果将 `maxParallelImagePulls` 设置为大于等于 2，则必须将 `serializeImagePulls` 设置为 false。
kubelet 在无效的 `maxParallelImagePulls` 设置下会启动失败。

## 带镜像索引的多架构镜像  {#multi-architecture-images-with-image-indexes}

除了提供二进制的镜像之外，
容器仓库也可以提供[容器镜像索引](https://github.com/opencontainers/image-spec/blob/master/image-index.md)。
镜像索引可以指向镜像的多个[镜像清单](https://github.com/opencontainers/image-spec/blob/master/manifest.md)，
提供特定于体系结构版本的容器。
这背后的理念是让你可以为镜像命名（例如：`pause`、`example/mycontainer`、`kube-apiserver`）
的同时，允许不同的系统基于它们所使用的机器体系结构取回正确的二进制镜像。

Kubernetes 自身通常在命名容器镜像时添加后缀 `-$(ARCH)`。
为了向前兼容，请在生成较老的镜像时也提供后缀。
这里的理念是为某镜像（如 `pause`）生成针对所有平台都适用的清单时，
生成 `pause-amd64` 这类镜像，以便较老的配置文件或者将镜像后缀硬编码到其中的
YAML 文件也能兼容。

## 使用私有仓库   {#using-a-private-registry}

从私有仓库读取镜像时可能需要密钥。
凭据可以用以下方式提供:

- 配置节点向私有仓库进行身份验证
  - 所有 Pod 均可读取任何已配置的私有仓库
  - 需要集群管理员配置节点
- kubelet 凭据提供程序，动态获取私有仓库的凭据
  - kubelet 可以被配置为使用凭据提供程序 exec 插件来访问对应的私有镜像库
- 预拉镜像
  - 所有 Pod 都可以使用节点上缓存的所有镜像
  - 需要所有节点的 root 访问权限才能进行设置
- 在 Pod 中设置 ImagePullSecrets
  - 只有提供自己密钥的 Pod 才能访问私有仓库
- 特定于厂商的扩展或者本地扩展
  - 如果你在使用定制的节点配置，你（或者云平台提供商）可以实现让节点向容器仓库认证的机制

下面将详细描述每一项。

### 配置 Node 对私有仓库认证  {#configuring-nodes-to-authenticate-to-a-private-registry}

设置凭据的具体说明取决于你选择使用的容器运行时和仓库。
你应该参考解决方案的文档来获取最准确的信息。

有关配置私有容器镜像仓库的示例，
请参阅任务[从私有镜像库中拉取镜像](/zh-cn/docs/tasks/configure-pod-container/pull-image-private-registry)。
该示例使用 Docker Hub 中的私有镜像仓库。

### 用于认证镜像拉取的 kubelet 凭据提供程序  {#kubelet-credential-provider}

{{< note >}}
此方法尤其适合 kubelet 需要动态获取仓库凭据时。
最常用于由云提供商提供的仓库，其中身份认证令牌的生命期是短暂的。
{{< /note >}}

你可以配置 kubelet，以调用插件可执行文件的方式来动态获取容器镜像的仓库凭据。
这是为私有仓库获取凭据最稳健和最通用的方法，但也需要 kubelet 级别的配置才能启用。

有关更多细节请参见[配置 kubelet 镜像凭据提供程序](/docs/tasks/administer-cluster/kubelet-credential-provider/)。

### config.json 说明 {#config-json}

对于 `config.json` 的解释在原始 Docker 实现和 Kubernetes 的解释之间有所不同。
在 Docker 中，`auths` 键只能指定根 URL，而 Kubernetes 允许 glob URLs 以及前缀匹配的路径。
这意味着，像这样的 `config.json` 是有效的：

```json
{
    "auths": {
        "*my-registry.io/images": {
            "auth": "…"
        }
    }
}
```

使用以下语法匹配根 URL （`*my-registry.io`）：

```
pattern:
    { term }

term:
    '*'         匹配任何无分隔符字符序列
    '?'         匹配任意单个非分隔符
    '[' [ '^' ] 字符范围
                  字符集（必须非空）
    c           匹配字符 c （c 不为 '*', '?', '\\', '['）
    '\\' c      匹配字符 c

字符范围:
    c           匹配字符 c （c 不为 '\\', '?', '-', ']'）
    '\\' c      匹配字符 c
    lo '-' hi   匹配字符范围在 lo 到 hi 之间字符
```

现在镜像拉取操作会将每种有效模式的凭据都传递给 CRI 容器运行时。例如下面的容器镜像名称会匹配成功：

- `my-registry.io/images`
- `my-registry.io/images/my-image`
- `my-registry.io/images/another-image`
- `sub.my-registry.io/images/my-image`
- `a.sub.my-registry.io/images/my-image`

kubelet 为每个找到的凭据的镜像按顺序拉取。这意味着在 `config.json` 中可能有多项：

```json
{
    "auths": {
        "my-registry.io/images": {
            "auth": "…"
        },
        "my-registry.io/images/subpath": {
            "auth": "…"
        }
    }
}
```

如果一个容器指定了要拉取的镜像 `my-registry.io/images/subpath/my-image`，
并且其中一个失败，kubelet 将尝试从另一个身份验证源下载镜像。

### 提前拉取镜像   {#pre-pulled-images}

{{< note >}}
该方法适用于你能够控制节点配置的场合。
如果你的云供应商负责管理节点并自动置换节点，这一方案无法可靠地工作。
{{< /note >}}

默认情况下，`kubelet` 会尝试从指定的仓库拉取每个镜像。
但是，如果容器属性 `imagePullPolicy` 设置为 `IfNotPresent` 或者 `Never`，
则会优先使用（对应 `IfNotPresent`）或者一定使用（对应 `Never`）本地镜像。

如果你希望使用提前拉取镜像的方法代替仓库认证，就必须保证集群中所有节点提前拉取的镜像是相同的。

这一方案可以用来提前载入指定的镜像以提高速度，或者作为向私有仓库执行身份认证的一种替代方案。

所有的 Pod 都可以使用节点上提前拉取的镜像。

### 在 Pod 上指定 ImagePullSecrets   {#specifying-imagepullsecrets-on-a-pod}

{{< note >}}
运行使用私有仓库中镜像的容器时，建议使用这种方法。
{{< /note >}}

Kubernetes 支持在 Pod 中设置容器镜像仓库的密钥。
`imagePullSecrets` 必须全部与 Pod 位于同一个名字空间中。
引用的 Secret 必须是 `kubernetes.io/dockercfg` 或 `kubernetes.io/dockerconfigjson` 类型。

#### 使用 Docker Config 创建 Secret   {#creating-a-secret-with-docker-config}

你需要知道用于向仓库进行身份验证的用户名、密码和客户端电子邮件地址，以及它的主机名。
运行以下命令，注意替换适当的大写值：

```shell
kubectl create secret docker-registry <name> \
  --docker-server=DOCKER_REGISTRY_SERVER \
  --docker-username=DOCKER_USER \
  --docker-password=DOCKER_PASSWORD \
  --docker-email=DOCKER_EMAIL
```

如果你已经有 Docker 凭据文件，则可以将凭据文件导入为 Kubernetes
{{< glossary_tooltip text="Secret" term_id="secret" >}}，
而不是执行上面的命令。
[基于已有的 Docker 凭据创建 Secret](/zh-cn/docs/tasks/configure-pod-container/pull-image-private-registry/#registry-secret-existing-credentials)
解释了如何完成这一操作。

如果你在使用多个私有容器仓库，这种技术将特别有用。
原因是 `kubectl create secret docker-registry` 创建的是仅适用于某个私有仓库的 Secret。

{{< note >}}
Pod 只能引用位于自身所在名字空间中的 Secret，因此需要针对每个名字空间重复执行上述过程。
{{< /note >}}

#### 在 Pod 中引用 ImagePullSecrets {#referring-to-an-imagepullsecrets-on-a-pod}

现在，在创建 Pod 时，可以在 Pod 定义中增加 `imagePullSecrets` 部分来引用该 Secret。
`imagePullSecrets` 数组中的每一项只能引用同一名字空间中的 Secret。

例如：

```shell
cat <<EOF > pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: foo
  namespace: awesomeapps
spec:
  containers:
    - name: foo
      image: janedoe/awesomeapp:v1
  imagePullSecrets:
    - name: myregistrykey
EOF

cat <<EOF >> ./kustomization.yaml
resources:
- pod.yaml
EOF
```

你需要对使用私有仓库的每个 Pod 执行以上操作。不过，
设置该字段的过程也可以通过为[服务账号](/zh-cn/docs/tasks/configure-pod-container/configure-service-account/)资源设置
`imagePullSecrets` 来自动完成。
有关详细指令，
可参见[将 ImagePullSecrets 添加到服务账号](/zh-cn/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account)。

你也可以将此方法与节点级别的 `.docker/config.json` 配置结合使用。
来自不同来源的凭据会被合并。

## 使用案例  {#use-cases}

配置私有仓库有多种方案，以下是一些常用场景和建议的解决方案。

1. 集群运行非专有镜像（例如，开源镜像）。镜像不需要隐藏。
   - 使用来自公共仓库的公共镜像
     - 无需配置
     - 某些云厂商会自动为公开镜像提供高速缓存，以便提升可用性并缩短拉取镜像所需时间

2. 集群运行一些专有镜像，这些镜像需要对公司外部隐藏，对所有集群用户可见
   - 使用托管的私有仓库
     - 在需要访问私有仓库的节点上可能需要手动配置
   - 或者，在防火墙内运行一个组织内部的私有仓库，并开放读取权限
     - 不需要配置 Kubernetes
   - 使用控制镜像访问的托管容器镜像仓库服务
     - 与手动配置节点相比，这种方案能更好地处理集群自动扩缩容
   - 或者，在不方便更改节点配置的集群中，使用 `imagePullSecrets`

3. 集群使用专有镜像，且有些镜像需要更严格的访问控制
   - 确保 [AlwaysPullImages 准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#alwayspullimages)被启用。否则，所有 Pod 都可以使用所有镜像。
   - 确保将敏感数据存储在 Secret 资源中，而不是将其打包在镜像里

4. 集群是多租户的并且每个租户需要自己的私有仓库
   - 确保 [AlwaysPullImages 准入控制器](/zh-cn/docs/reference/access-authn-authz/admission-controllers/#alwayspullimages)。否则，所有租户的所有的 Pod 都可以使用所有镜像。
   - 为私有仓库启用鉴权
   - 为每个租户生成访问仓库的凭据，放置在 Secret 中，并将 Secret 发布到各租户的名字空间下。
   - 租户将 Secret 添加到每个名字空间中的 imagePullSecrets

如果你需要访问多个仓库，可以为每个仓库创建一个 Secret。

## 旧版的内置 kubelet 凭据提供程序

在旧版本的 Kubernetes 中，kubelet 与云提供商凭据直接集成。
这使它能够动态获取镜像仓库的凭据。

kubelet 凭据提供程序集成存在三个内置实现：
ACR（Azure 容器仓库）、ECR（Elastic 容器仓库）和 GCR（Google 容器仓库）

有关该旧版机制的更多信息，请阅读你正在使用的 Kubernetes 版本的文档。
从 Kubernetes v1.26 到 v{{< skew latestVersion >}} 不再包含该旧版机制，因此你需要：

- 在每个节点上配置一个 kubelet 镜像凭据提供程序
- 使用 `imagePullSecrets` 和至少一个 Secret 指定镜像拉取凭据

## {{% heading "whatsnext" %}}

* 阅读 [OCI Image Manifest 规范](https://github.com/opencontainers/image-spec/blob/master/manifest.md)。
* 了解[容器镜像垃圾收集](/zh-cn/docs/concepts/architecture/garbage-collection/#container-image-garbage-collection)。
* 了解[从私有仓库拉取镜像](/zh-cn/docs/tasks/configure-pod-container/pull-image-private-registry)。
