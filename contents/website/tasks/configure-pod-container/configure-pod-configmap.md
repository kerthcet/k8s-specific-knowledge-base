---
title: 配置 Pod 使用 ConfigMap
content_type: task
weight: 190
card:
  name: tasks
  weight: 50
---

很多应用在其初始化或运行期间要依赖一些配置信息。
大多数时候，存在要调整配置参数所设置的数值的需求。
ConfigMap 是 Kubernetes 的一种机制，可让你将配置数据注入到应用的
{{< glossary_tooltip text="Pod" term_id="pod" >}} 内部。

ConfigMap 概念允许你将配置清单与镜像内容分离，以保持容器化的应用程序的可移植性。
例如，你可以下载并运行相同的{{< glossary_tooltip text="容器镜像" term_id="image" >}}来启动容器，
用于本地开发、系统测试或运行实时终端用户工作负载。

本页提供了一系列使用示例，这些示例演示了如何创建 ConfigMap 以及配置 Pod
使用存储在 ConfigMap 中的数据。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

你需要安装 `wget` 工具。如果你有不同的工具，例如 `curl`，而没有 `wget`，
则需要调整下载示例数据的步骤。


## 创建 ConfigMap    {#create-a-configmap}

你可以使用 `kubectl create configmap` 或者在 `kustomization.yaml` 中的 ConfigMap
生成器来创建 ConfigMap。

### 使用 `kubectl create configmap` 创建 ConfigMap    {#create-a-configmap-using-kubectl-create-configmap}

你可以使用 `kubectl create configmap` 命令基于[目录](#create-configmaps-from-directories)、
[文件](#create-configmaps-from-files)或者[字面值](#create-configmaps-from-literal-values)来创建
ConfigMap：

```shell
kubectl create configmap <映射名称> <数据源>
```

其中，`<映射名称>` 是为 ConfigMap 指定的名称，`<数据源>` 是要从中提取数据的目录、
文件或者字面值。ConfigMap 对象的名称必须是合法的
[DNS 子域名](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

在你基于文件来创建 ConfigMap 时，`<数据源>` 中的键名默认取自文件的基本名，
而对应的值则默认为文件的内容。

你可以使用 [`kubectl describe`](/docs/reference/generated/kubectl/kubectl-commands/#describe) 或者
[`kubectl get`](/docs/reference/generated/kubectl/kubectl-commands/#get) 获取有关 ConfigMap 的信息。

#### 基于一个目录来创建 ConfigMap     {#create-configmaps-from-directories}

你可以使用 `kubectl create configmap` 基于同一目录中的多个文件创建 ConfigMap。
当你基于目录来创建 ConfigMap 时，kubectl 识别目录下文件名可以作为合法键名的文件，
并将这些文件打包到新的 ConfigMap 中。普通文件之外的所有目录项都会被忽略
（例如：子目录、符号链接、设备、管道等等）。

{{< note >}}
用于创建 ConfigMap 的每个文件名必须由可接受的字符组成，即：字母（`A` 到 `Z` 和
`a` 到 `z`）、数字（`0` 到 `9`）、'-'、'_'或'.'。
如果在一个目录中使用 `kubectl create configmap`，而其中任一文件名包含不可接受的字符，
则 `kubectl` 命令可能会失败。

`kubectl` 命令在遇到不合法的文件名时不会打印错误。

{{< /note >}}

创建本地目录：

```shell
mkdir -p configure-pod-container/configmap/
```

现在，下载示例的配置并创建 ConfigMap：

```shell
# 将示例文件下载到 `configure-pod-container/configmap/` 目录
wget https://kubernetes.io/examples/configmap/game.properties -O configure-pod-container/configmap/game.properties
wget https://kubernetes.io/examples/configmap/ui.properties -O configure-pod-container/configmap/ui.properties

# 创建 ConfigMap
kubectl create configmap game-config --from-file=configure-pod-container/configmap/
```

以上命令将 `configure-pod-container/configmap` 目录下的所有文件，也就是
`game.properties` 和 `ui.properties` 打包到 game-config ConfigMap
中。你可以使用下面的命令显示 ConfigMap 的详细信息：

```shell
kubectl describe configmaps game-config
```

输出类似以下内容：

```
Name:         game-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
game.properties:
----
enemies=aliens
lives=3
enemies.cheat=true
enemies.cheat.level=noGoodRotten
secret.code.passphrase=UUDDLRLRBABAS
secret.code.allowed=true
secret.code.lives=30
ui.properties:
----
color.good=purple
color.bad=yellow
allow.textmode=true
how.nice.to.look=fairlyNice
```

`configure-pod-container/configmap/` 目录中的 `game.properties` 和 `ui.properties`
文件出现在 ConfigMap 的 `data` 部分。

```shell
kubectl get configmaps game-config -o yaml
```

输出类似以下内容:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2022-02-18T18:52:05Z
  name: game-config
  namespace: default
  resourceVersion: "516"
  uid: b4952dc3-d670-11e5-8cd0-68f728db1985
data:
  game.properties: |
    enemies=aliens
    lives=3
    enemies.cheat=true
    enemies.cheat.level=noGoodRotten
    secret.code.passphrase=UUDDLRLRBABAS
    secret.code.allowed=true
    secret.code.lives=30
  ui.properties: |
    color.good=purple
    color.bad=yellow
    allow.textmode=true
    how.nice.to.look=fairlyNice
```

#### 基于文件创建 ConfigMap   {#create-configmaps-from-files}

你可以使用 `kubectl create configmap` 基于单个文件或多个文件创建 ConfigMap。

例如：

```shell
kubectl create configmap game-config-2 --from-file=configure-pod-container/configmap/game.properties
```

将产生以下 ConfigMap:

```shell
kubectl describe configmaps game-config-2
```

输出类似以下内容:

```
Name:         game-config-2
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
game.properties:
----
enemies=aliens
lives=3
enemies.cheat=true
enemies.cheat.level=noGoodRotten
secret.code.passphrase=UUDDLRLRBABAS
secret.code.allowed=true
secret.code.lives=30
```

你可以多次使用 `--from-file` 参数，从多个数据源创建 ConfigMap。

```shell
kubectl create configmap game-config-2 --from-file=configure-pod-container/configmap/game.properties --from-file=configure-pod-container/configmap/ui.properties
```

你可以使用以下命令显示 `game-config-2` ConfigMap 的详细信息：

```shell
kubectl describe configmaps game-config-2
```

输出类似以下内容:

```
Name:         game-config-2
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
game.properties:
----
enemies=aliens
lives=3
enemies.cheat=true
enemies.cheat.level=noGoodRotten
secret.code.passphrase=UUDDLRLRBABAS
secret.code.allowed=true
secret.code.lives=30
ui.properties:
----
color.good=purple
color.bad=yellow
allow.textmode=true
how.nice.to.look=fairlyNice
```

使用 `--from-env-file` 选项基于 env 文件创建 ConfigMap，例如：

```shell
# Env 文件包含环境变量列表。其中适用以下语法规则:
# 这些语法规则适用：
#   Env 文件中的每一行必须为 VAR=VAL 格式。
#   以＃开头的行（即注释）将被忽略。
#   空行将被忽略。
#   引号不会被特殊处理（即它们将成为 ConfigMap 值的一部分）。

# 将示例文件下载到 `configure-pod-container/configmap/` 目录
wget https://kubernetes.io/examples/configmap/game-env-file.properties -O configure-pod-container/configmap/game-env-file.properties
wget https://kubernetes.io/examples/configmap/ui-env-file.properties -O configure-pod-container/configmap/ui-env-file.properties

# Env 文件 `game-env-file.properties` 如下所示
cat configure-pod-container/configmap/game-env-file.properties
enemies=aliens
lives=3
allowed="true"

# This comment and the empty line above it are ignored
```

```shell
kubectl create configmap game-config-env-file \
       --from-env-file=configure-pod-container/configmap/game-env-file.properties
```

将产生以下 ConfigMap。查看 ConfigMap：

```shell
kubectl get configmap game-config-env-file -o yaml
```

输出类似以下内容：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2019-12-27T18:36:28Z
  name: game-config-env-file
  namespace: default
  resourceVersion: "809965"
  uid: d9d1ca5b-eb34-11e7-887b-42010a8002b8
data:
  allowed: '"true"'
  enemies: aliens
  lives: "3"
```

从 Kubernetes 1.23 版本开始，`kubectl` 支持多次指定 `--from-env-file` 参数来从多个数据源创建
ConfigMap。

```shell
kubectl create configmap config-multi-env-files \
        --from-env-file=configure-pod-container/configmap/game-env-file.properties \
        --from-env-file=configure-pod-container/configmap/ui-env-file.properties
```

将产生以下 ConfigMap:

```shell
kubectl get configmap config-multi-env-files -o yaml
```

输出类似以下内容:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2019-12-27T18:38:34Z
  name: config-multi-env-files
  namespace: default
  resourceVersion: "810136"
  uid: 252c4572-eb35-11e7-887b-42010a8002b8
data:
  allowed: '"true"'
  color: purple
  enemies: aliens
  how: fairlyNice
  lives: "3"
  textmode: "true"
```

#### 定义从文件创建 ConfigMap 时要使用的键    {#define-the-key-to-use-when-generating-a-configmap-from-a-file}

在使用 `--from-file` 参数时，你可以定义在 ConfigMap 的 `data` 部分出现键名，
而不是按默认行为使用文件名：

```shell
kubectl create configmap game-config-3 --from-file=<我的键名>=<文件路径>
```

`<我的键名>` 是你要在 ConfigMap 中使用的键名，`<文件路径>` 是你想要键所表示的数据源文件的位置。

例如:

```shell
kubectl create configmap game-config-3 --from-file=game-special-key=configure-pod-container/configmap/game.properties
```

将产生以下 ConfigMap:

```shell
kubectl get configmaps game-config-3 -o yaml
```

输出类似以下内容：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2022-02-18T18:54:22Z
  name: game-config-3
  namespace: default
  resourceVersion: "530"
  uid: 05f8da22-d671-11e5-8cd0-68f728db1985
data:
  game-special-key: |
    enemies=aliens
    lives=3
    enemies.cheat=true
    enemies.cheat.level=noGoodRotten
    secret.code.passphrase=UUDDLRLRBABAS
    secret.code.allowed=true
    secret.code.lives=30
```

#### 根据字面值创建 ConfigMap         {#create-configmaps-from-literal-values}

你可以将 `kubectl create configmap` 与 `--from-literal` 参数一起使用，
通过命令行定义文字值：

```shell
kubectl create configmap special-config --from-literal=special.how=very --from-literal=special.type=charm
```

你可以传入多个键值对。命令行中提供的每对键值在 ConfigMap 的 `data` 部分中均表示为单独的条目。

```shell
kubectl get configmaps special-config -o yaml
```

输出类似以下内容:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2022-02-18T19:14:38Z
  name: special-config
  namespace: default
  resourceVersion: "651"
  uid: dadce046-d673-11e5-8cd0-68f728db1985
data:
  special.how: very
  special.type: charm
```

### 基于生成器创建 ConfigMap    {#create-a-configmap-from-generator}

你还可以基于生成器（Generators）创建 ConfigMap，然后将其应用于集群的 API 服务器上创建对象。
生成器应在目录内的 `kustomization.yaml` 中指定。

#### 基于文件生成 ConfigMap    {#generate-configmaps-from-files}

例如，要基于 `configure-pod-container/configmap/game.properties`
文件生成一个 ConfigMap：

```shell
# 创建包含 ConfigMapGenerator 的 kustomization.yaml 文件
cat <<EOF >./kustomization.yaml
configMapGenerator:
- name: game-config-4
  labels:
    game-config: config-4
  files:
  - configure-pod-container/configmap/game.properties
EOF
```

应用（Apply）kustomization 目录创建 ConfigMap 对象：

```shell
kubectl apply -k .
```

```
configmap/game-config-4-m9dm2f92bt created
```

你可以像这样检查 ConfigMap 已经被创建：

```shell
kubectl get configmap
```
```
NAME                       DATA   AGE
game-config-4-m9dm2f92bt   1      37s
```

也可以这样：

```shell
kubectl describe configmaps/game-config-4-m9dm2f92bt
```
```
Name:         game-config-4-m9dm2f92bt
Namespace:    default
Labels:       game-config=config-4
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"v1","data":{"game.properties":"enemies=aliens\nlives=3\nenemies.cheat=true\nenemies.cheat.level=noGoodRotten\nsecret.code.p...

Data
====
game.properties:
----
enemies=aliens
lives=3
enemies.cheat=true
enemies.cheat.level=noGoodRotten
secret.code.passphrase=UUDDLRLRBABAS
secret.code.allowed=true
secret.code.lives=30
Events:  <none>
```

请注意，生成的 ConfigMap 名称具有通过对内容进行散列而附加的后缀，
这样可以确保每次修改内容时都会生成新的 ConfigMap。

#### 定义从文件生成 ConfigMap 时要使用的键    {#define-the-key-to-use-when-generating-a-configmap-from-a-file}

在 ConfigMap 生成器中，你可以定义一个非文件名的键名。
例如，从 `configure-pod-container/configmap/game.properties` 文件生成 ConfigMap，
但使用 `game-special-key` 作为键名：

```shell
# 创建包含 ConfigMapGenerator 的 kustomization.yaml 文件
cat <<EOF >./kustomization.yaml
configMapGenerator:
- name: game-config-5
  labels:
    game-config: config-5
  files:
  - game-special-key=configure-pod-container/configmap/game.properties
EOF
```

应用 Kustomization 目录创建 ConfigMap 对象。

```shell
kubectl apply -k .
```
```
configmap/game-config-5-m67dt67794 created
```

#### 基于字面值生成 ConfigMap    {#generate-configmaps-from-literals}

此示例向你展示如何使用 Kustomize 和 kubectl，基于两个字面键/值对
`special.type=charm` 和 `special.how=very` 创建一个 `ConfigMap`。
为了实现这一点，你可以配置 `ConfigMap` 生成器。
创建（或替换）`kustomization.yaml`，使其具有以下内容。

```yaml
---
# 基于字面创建 ConfigMap 的 kustomization.yaml 内容
configMapGenerator:
- name: special-config-2
  literals:
  - special.how=very
  - special.type=charm
EOF
```

应用 Kustomization 目录创建 ConfigMap 对象。

```shell
kubectl apply -k .
```
```
configmap/special-config-2-c92b5mmcf2 created
```

## 临时清理    {#interim-cleanup}

在继续之前，清理你创建的一些 ConfigMap：

```bash
kubectl delete configmap special-config
kubectl delete configmap env-config
kubectl delete configmap -l 'game-config in (config-4,config-5)’
```

现在你已经学会了定义 ConfigMap，你可以继续下一节，学习如何将这些对象与 Pod 一起使用。

---

## 使用 ConfigMap 数据定义容器环境变量    {#define-container-environment-variables-using-configmap-data}

### 使用单个 ConfigMap 中的数据定义容器环境变量    {#define-a-container-environment-variable-with-data-from-a-single-configmap}

1. 在 ConfigMap 中将环境变量定义为键值对:

   ```shell
   kubectl create configmap special-config --from-literal=special.how=very
   ```

2. 将 ConfigMap 中定义的 `special.how` 赋值给 Pod 规约中的 `SPECIAL_LEVEL_KEY` 环境变量。

   {{< codenew file="pods/pod-single-configmap-env-variable.yaml" >}}

   创建 Pod:

   ```shell
   kubectl create -f https://kubernetes.io/examples/pods/pod-single-configmap-env-variable.yaml
   ```

   现在，Pod 的输出包含环境变量 `SPECIAL_LEVEL_KEY=very`。

### 使用来自多个 ConfigMap 的数据定义容器环境变量    {#define-container-environment-variables-with-data-from-multiple-configmaps}

与前面的示例一样，首先创建 ConfigMap。
这是你将使用的清单：

{{< codenew file="configmap/configmaps.yaml" >}}

* 创建 ConfigMap:

  ```shell
  kubectl create -f https://kubernetes.io/examples/configmap/configmaps.yaml
  ```

* 在 Pod 规约中定义环境变量。

  {{< codenew file="pods/pod-multiple-configmap-env-variable.yaml" >}}

  创建 Pod:

  ```shell
  kubectl create -f https://kubernetes.io/examples/pods/pod-multiple-configmap-env-variable.yaml
  ```

  现在，Pod 的输出包含环境变量 `SPECIAL_LEVEL_KEY=very` 和 `LOG_LEVEL=INFO`。

  一旦你乐意继续前进，删除该 Pod：

  ```shell
  kubectl delete pod dapi-test-pod --now
  ```

## 将 ConfigMap 中的所有键值对配置为容器环境变量    {#configure-all-key-value-pairs-in-a-configmap-as-container-environment-variables}

* 创建一个包含多个键值对的 ConfigMap。

  {{< codenew file="configmap/configmap-multikeys.yaml" >}}

  创建 ConfigMap:

  ```shell
  kubectl create -f https://kubernetes.io/examples/configmap/configmap-multikeys.yaml
  ```

* 使用 `envFrom` 将所有 ConfigMap 的数据定义为容器环境变量，ConfigMap
  中的键成为 Pod 中的环境变量名称。

  {{< codenew file="pods/pod-configmap-envFrom.yaml" >}}

  创建 Pod:

  ```shell
  kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-envFrom.yaml
  ```

  现在，Pod 的输出包含环境变量 `SPECIAL_LEVEL=very` 和 `SPECIAL_TYPE=charm`。

  一旦你乐意继续前进，删除该 Pod：

  ```shell
  kubectl delete pod dapi-test-pod --now
  ```

## 在 Pod 命令中使用 ConfigMap 定义的环境变量    {#use-configmap-defined-environment-variables-in-pod-commands}

你可以使用 `$(VAR_NAME)` Kubernetes 替换语法在容器的 `command` 和 `args`
属性中使用 ConfigMap 定义的环境变量。

例如，以下 Pod 清单：

{{< codenew file="pods/pod-configmap-env-var-valueFrom.yaml" >}}

通过运行下面命令创建该 Pod：

```shell
kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-env-var-valueFrom.yaml
```

此 Pod 在 `test-container` 容器中产生以下输出:

```
very charm
```

一旦你乐意继续前进，删除该 Pod：

```shell
kubectl delete pod dapi-test-pod --now
```

## 将 ConfigMap 数据添加到一个卷中    {#add-configmap-data-to-a-volume}

如基于文件创建 [ConfigMap](#create-configmaps-from-files) 中所述，当你使用
`--from-file` 创建 ConfigMap 时，文件名成为存储在 ConfigMap 的 `data` 部分中的键，
文件内容成为键对应的值。

本节中的示例引用了一个名为 `special-config` 的 ConfigMap：

{{< codenew file="configmap/configmap-multikeys.yaml" >}}

创建 ConfigMap:

```shell
kubectl create -f https://kubernetes.io/examples/configmap/configmap-multikeys.yaml
```

### 使用存储在 ConfigMap 中的数据填充卷    {#populate-a-volume-with-data-stored-in-a-configmap}

在 Pod 规约的 `volumes` 部分下添加 ConfigMap 名称。
这会将 ConfigMap 数据添加到 `volumeMounts.mountPath` 所指定的目录
（在本例中为 `/etc/config`）。
`command` 部分列出了名称与 ConfigMap 中的键匹配的目录文件。

{{< codenew file="pods/pod-configmap-volume.yaml" >}}

创建 Pod:

```shell
kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-volume.yaml
```

Pod 运行时，命令 `ls /etc/config/` 产生下面的输出：

```
SPECIAL_LEVEL
SPECIAL_TYPE
```

文本数据会展现为 UTF-8 字符编码的文件。如果使用其他字符编码，
可以使用 `binaryData`（详情参阅 [ConfigMap 对象](/zh-cn/docs/concepts/configuration/configmap/#configmap-object)）。

{{< note >}}

如果该容器镜像的 `/etc/config`
目录中有一些文件，卷挂载将使该镜像中的这些文件无法访问。
{{< /note >}}

一旦你乐意继续前进，删除该 Pod：

```shell
kubectl delete pod dapi-test-pod --now
```

### 将 ConfigMap 数据添加到卷中的特定路径    {#add-configmap-data-to-a-specific-path-in-the-volume}

使用 `path` 字段为特定的 ConfigMap 项目指定预期的文件路径。
在这里，ConfigMap 中键 `SPECIAL_LEVEL` 的内容将挂载在 `config-volume`
卷中 `/etc/config/keys` 文件中。

{{< codenew file="pods/pod-configmap-volume-specific-key.yaml" >}}

创建 Pod：

```shell
kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-volume-specific-key.yaml
```

当 Pod 运行时，命令 `cat /etc/config/keys` 产生以下输出：

```
very
```

{{< caution >}}
如前，`/etc/config/` 目录中所有先前的文件都将被删除。
{{< /caution >}}

删除该 Pod:

```shell
kubectl delete pod dapi-test-pod --now
```


### 映射键到指定路径并设置文件访问权限    {#project-keys-to-specific-paths-and-file-permissions}

你可以将指定键名投射到特定目录，也可以逐个文件地设定访问权限。
[Secret](/zh-cn/docs/concepts/configuration/secret/#using-secrets-as-files-from-a-pod)
指南中为这一语法提供了解释。

### 可选引用    {#optional-references}

ConfigMap 引用可以被标记为**可选**。
如果 ConfigMap 不存在，则挂载的卷将为空。
如果 ConfigMap 存在，但引用的键不存在，则挂载点下的路径将不存在。
有关更多信息，请参阅[可选 ConfigMap](#optional-configmaps) 细节。

### 挂载的 ConfigMap 会被自动更新    {#mounted-configMaps-are-updated-automatically}

当已挂载的 ConfigMap 被更新时，所投射的内容最终也会被更新。
这适用于 Pod 启动后可选引用的 ConfigMap 重新出现的情况。

Kubelet 在每次定期同步时都会检查所挂载的 ConfigMap 是否是最新的。
然而，它使用其基于 TTL 机制的本地缓存来获取 ConfigMap 的当前值。
因此，从 ConfigMap 更新到新键映射到 Pod 的总延迟可能与 kubelet
同步周期（默认为1分钟）+ kubelet 中 ConfigMap 缓存的 TTL（默认为1分钟）一样长。
你可以通过更新 Pod 的一个注解来触发立即刷新。

{{< note >}}
使用 ConfigMap 作为 [subPath](/zh-cn/docs/concepts/storage/volumes/#using-subpath)
卷的容器将不会收到 ConfigMap 更新。
{{< /note >}}


## 了解 ConfigMap 和 Pod    {#understanding-configmaps-and-pods}

ConfigMap API 资源将配置数据存储为键值对。
数据可以在 Pod 中使用，也可以用来提供系统组件（如控制器）的配置。
ConfigMap 与 [Secret](/zh-cn/docs/concepts/configuration/secret/) 类似，
但是提供的是一种处理不含敏感信息的字符串的方法。
用户和系统组件都可以在 ConfigMap 中存储配置数据。

{{< note >}}
ConfigMap 应该引用属性文件，而不是替换它们。可以将 ConfigMap 理解为类似于 Linux
`/etc` 目录及其内容的东西。例如，如果你基于 ConfigMap 创建
[Kubernetes 卷](/zh-cn/docs/concepts/storage/volumes/)，则 ConfigMap
中的每个数据项都由该数据卷中的某个独立的文件表示。
{{< /note >}}

ConfigMap 的 `data` 字段包含配置数据。如下例所示，它可以简单
（如用 `--from-literal` 的单个属性定义）或复杂
（如用 `--from-file` 的配置文件或 JSON blob 定义）。

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2016-02-18T19:14:38Z
  name: example-config
  namespace: default
data:
  # 使用 --from-literal 定义的简单属性
  example.property.1: hello
  example.property.2: world
  # 使用 --from-file 定义复杂属性的例子
  example.property.file: |-
    property.1=value-1
    property.2=value-2
    property.3=value-3
```

当 `kubectl` 从非 ASCII 或 UTF-8 编码的输入创建 ConfigMap 时，
该工具将这些输入放入 ConfigMap 的 `binaryData` 字段，而不是 `data` 字段。
文本和二进制数据源都可以组合在一个 ConfigMap 中。

如果你想查看 ConfigMap 中的 `binaryData` 键（及其值），
可以运行 `kubectl get configmap -o jsonpath='{.binaryData}' <name>`。

Pod 可以从使用 `data` 或 `binaryData` 的 ConfigMap 中加载数据。

### 可选的 ConfigMap {#optional-configmaps}

你可以在 Pod 规约中将对 ConfigMap 的引用标记为 **可选（optional）**。
如果 ConfigMap 不存在，那么它在 Pod 中为其提供数据的配置（例如：环境变量、挂载的卷）将为空。
如果 ConfigMap 存在，但引用的键不存在，那么数据也是空的。

例如，以下 Pod 规约将 ConfigMap 中的环境变量标记为可选：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
    - name: test-container
      image: gcr.io/google_containers/busybox
      command: ["/bin/sh", "-c", "env"]
      env:
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              name: a-config
              key: akey
              optional: true # 将环境变量标记为可选
  restartPolicy: Never
```

当你运行这个 Pod 并且名称为 `a-config` 的 ConfigMap 不存在时，输出空值。
当你运行这个 Pod 并且名称为 `a-config` 的 ConfigMap 存在，
但是在 ConfigMap 中没有名称为 `akey` 的键时，控制台输出也会为空。
如果你确实在名为 `a-config` 的 ConfigMap 中为 `akey` 设置了键值，
那么这个 Pod 会打印该值，然后终止。

你也可以在 Pod 规约中将 ConfigMap 提供的卷和文件标记为可选。
此时 Kubernetes 将总是为卷创建挂载路径，即使引用的 ConfigMap 或键不存在。
例如，以下 Pod 规约将所引用得 ConfigMap 的卷标记为可选：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
    - name: test-container
      image: gcr.io/google_containers/busybox
      command: ["/bin/sh", "-c", "ls /etc/config"]
      volumeMounts:
      - name: config-volume
        mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: no-config
        optional: true # 将引用的 ConfigMap 的卷标记为可选
  restartPolicy: Never
```

### 限制   {#restrictions}

- 在 Pod 规约中引用某个 `ConfigMap` 之前，必须先创建这个对象，
  或者在 Pod 规约中将 ConfigMap 标记为 `optional`（请参阅[可选的 ConfigMaps](#optional-configmaps)）。
  如果所引用的 ConfigMap 不存在，并且没有将应用标记为 `optional` 则 Pod 将无法启动。
  同样，引用 ConfigMap 中不存在的主键也会令 Pod 无法启动，除非你将 Configmap 标记为 `optional`。

- 如果你使用 `envFrom` 来基于 ConfigMap 定义环境变量，那么无效的键将被忽略。
  Pod 可以被启动，但无效名称将被记录在事件日志中（`InvalidVariableNames`）。
  日志消息列出了每个被跳过的键。例如:

  ```shell
  kubectl get events
  ```

  输出与此类似:
  ```
  LASTSEEN FIRSTSEEN COUNT NAME          KIND  SUBOBJECT  TYPE      REASON                            SOURCE                MESSAGE
  0s       0s        1     dapi-test-pod Pod              Warning   InvalidEnvironmentVariableNames   {kubelet, 127.0.0.1}  Keys [1badkey, 2alsobad] from the EnvFrom configMap default/myconfig were skipped since they are considered invalid environment variable names.
  ```

- ConfigMap 位于确定的{{< glossary_tooltip term_id="namespace" text="名字空间" >}}中。
  每个 ConfigMap 只能被同一名字空间中的 Pod 引用.

- 你不能将 ConfigMap 用于{{< glossary_tooltip text="静态 Pod" term_id="static-pod" >}}，
  因为 Kubernetes 不支持这种用法。

## {{% heading "cleanup" %}}

删除你创建那些的 ConfigMap 和 Pod：

```bash
kubectl delete configmaps/game-config configmaps/game-config-2 configmaps/game-config-3 \
               configmaps/game-config-env-file
kubectl delete pod dapi-test-pod --now

# 你可能已经删除了下一组内容
kubectl delete configmaps/special-config configmaps/env-config
kubectl delete configmap -l 'game-config in (config-4,config-5)’
```

如果你创建了一个目录 `configure-pod-container` 并且不再需要它，你也应该删除这个目录，
或者将该目录移动到回收站/删除文件的位置。

## {{% heading "whatsnext" %}}

* 浏览[使用 ConfigMap 配置 Redis](/zh-cn/docs/tutorials/configuration/configure-redis-using-configmap/)
  真实示例。
