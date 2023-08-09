---
title: 命令行工具 (kubectl)
content_type: reference
weight: 110
no_list: true
card:
  name: reference
  weight: 20
---

{{< glossary_definition prepend="Kubernetes 提供" term_id="kubectl" length="short" >}}

这个工具叫做 `kubectl`。


针对配置信息，`kubectl` 在 `$HOME/.kube` 目录中查找一个名为 `config` 的配置文件。
你可以通过设置 `KUBECONFIG` 环境变量或设置
[`--kubeconfig`](/zh-cn/docs/concepts/configuration/organize-cluster-access-kubeconfig/)

参数来指定其它 [kubeconfig](/zh-cn/docs/concepts/configuration/organize-cluster-access-kubeconfig/) 文件。

本文概述了 `kubectl` 语法和命令操作描述，并提供了常见的示例。
有关每个命令的详细信息，包括所有受支持的参数和子命令，
请参阅 [kubectl](/docs/reference/generated/kubectl/kubectl-commands/) 参考文档。

有关安装说明，请参见[安装 kubectl](/zh-cn/docs/tasks/tools/#kubectl)；
如需快速指南，请参见[备忘单](/zh-cn/docs/reference/kubectl/cheatsheet/)。
如果你更习惯使用 `docker` 命令行工具，
[Docker 用户的 `kubectl`](/zh-cn/docs/reference/kubectl/docker-cli-to-kubectl/)
介绍了一些 Kubernetes 的等价命令。

## 语法   {#syntax}

使用以下语法从终端窗口运行 `kubectl` 命令：

```shell
kubectl [command] [TYPE] [NAME] [flags]
```

其中 `command`、`TYPE`、`NAME` 和 `flags` 分别是：

* `command`：指定要对一个或多个资源执行的操作，例如 `create`、`get`、`describe`、`delete`。

* `TYPE`：指定[资源类型](#resource-types)。资源类型不区分大小写，
  可以指定单数、复数或缩写形式。例如，以下命令输出相同的结果：

   ```shell
   kubectl get pod pod1
   kubectl get pods pod1
   kubectl get po pod1
   ```

* `NAME`：指定资源的名称。名称区分大小写。
  如果省略名称，则显示所有资源的详细信息。例如：`kubectl get pods`。

  在对多个资源执行操作时，你可以按类型和名称指定每个资源，或指定一个或多个文件：

 * 要按类型和名称指定资源：

  * 要对所有类型相同的资源进行分组，请执行以下操作：`TYPE1 name1 name2 name<#>`。<br/>
    例子：`kubectl get pod example-pod1 example-pod2`

  * 分别指定多个资源类型：`TYPE1/name1 TYPE1/name2 TYPE2/name3 TYPE<#>/name<#>`。<br/>
    例子：`kubectl get pod/example-pod1 replicationcontroller/example-rc1`

 * 用一个或多个文件指定资源：`-f file1 -f file2 -f file<#>`

  * [使用 YAML 而不是 JSON](/zh-cn/docs/concepts/configuration/overview/#general-configuration-tips)，
    因为 YAML 对用户更友好, 特别是对于配置文件。<br/>
    例子：`kubectl get -f ./pod.yaml`

* `flags`： 指定可选的参数。例如，可以使用 `-s` 或 `--server` 参数指定
  Kubernetes API 服务器的地址和端口。

{{< caution >}}
从命令行指定的参数会覆盖默认值和任何相应的环境变量。
{{< /caution >}}

如果你需要帮助，在终端窗口中运行 `kubectl help`。

## 集群内身份验证和命名空间覆盖   {#in-cluster-authentication-and-namespace-overrides}

默认情况下，`kubectl` 命令首先确定它是否在 Pod 中运行，从而被视为在集群中运行。
它首先检查 `KUBERNETES_SERVICE_HOST` 和 `KUBERNETES_SERVICE_PORT` 环境变量以及
`/var/run/secrets/kubernetes.io/serviceaccount/token` 中是否存在服务帐户令牌文件。
如果三个条件都被满足，则假定在集群内进行身份验证。

为保持向后兼容性，如果在集群内身份验证期间设置了 `POD_NAMESPACE`
环境变量，它将覆盖服务帐户令牌中的默认命名空间。
任何依赖默认命名空间的清单或工具都会受到影响。

**`POD_NAMESPACE` 环境变量**

如果设置了 `POD_NAMESPACE` 环境变量，对命名空间资源的 CLI 操作对象将使用该变量值作为默认值。
例如，如果该变量设置为 `seattle`，`kubectl get pods` 将返回 `seattle` 命名空间中的 Pod。
这是因为 Pod 是一个命名空间资源，且命令中没有提供命名空间。

直接使用 `--namespace <value>` 会覆盖此行为。

**kubectl 如何处理 ServiceAccount 令牌**

假设：
* 有 Kubernetes 服务帐户令牌文件挂载在
  `/var/run/secrets/kubernetes.io/serviceaccount/token` 上，并且
* 设置了 `KUBERNETES_SERVICE_HOST` 环境变量，并且
* 设置了 `KUBERNETES_SERVICE_PORT` 环境变量，并且
* 你没有在 kubectl 命令行上明确指定命名空间。

然后 kubectl 假定它正在你的集群中运行。
kubectl 工具查找该 ServiceAccount 的命名空间
（该命名空间与 Pod 的命名空间相同）并针对该命名空间进行操作。
这与集群外运行的情况不同；
当 kubectl 在集群外运行并且你没有指定命名空间时，
kubectl 命令会针对你在客户端配置中为当前上下文设置的命名空间进行操作。
要为你的 kubectl 更改默认的命名空间，你可以使用以下命令：

```shell
kubectl config set-context --current --namespace=<namespace-name>
```

## 操作   {#operations}

下表包含所有 kubectl 操作的简短描述和普通语法：

操作             | 语法      |       描述
-------------------- | -------------------- | --------------------
`alpha`    | `kubectl alpha SUBCOMMAND [flags]` | 列出与 alpha 特性对应的可用命令，这些特性在 Kubernetes 集群中默认情况下是不启用的。
`annotate`    | <code>kubectl annotate (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) KEY_1=VAL_1 ... KEY_N=VAL_N [--overwrite] [--all] [--resource-version=version] [flags]</code> | 添加或更新一个或多个资源的注解。
`api-resources`    | `kubectl api-resources [flags]` | 列出可用的 API 资源。
`api-versions`    | `kubectl api-versions [flags]` | 列出可用的 API 版本。
`apply`            | `kubectl apply -f FILENAME [flags]`| 从文件或 stdin 对资源应用配置更改。
`attach`        | `kubectl attach POD -c CONTAINER [-i] [-t] [flags]` | 挂接到正在运行的容器，查看输出流或与容器（stdin）交互。
`auth`    | `kubectl auth [flags] [options]` | 检查授权。
`autoscale`    | <code>kubectl autoscale (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) [--min=MINPODS] --max=MAXPODS [--cpu-percent=CPU] [flags]</code> | 自动扩缩由副本控制器管理的一组 pod。
`certificate`    | `kubectl certificate SUBCOMMAND [options]` | 修改证书资源。
`cluster-info`    | `kubectl cluster-info [flags]` | 显示有关集群中主服务器和服务的端口信息。
`completion`    | `kubectl completion SHELL [options]` | 为指定的 Shell（Bash 或 Zsh）输出 Shell 补齐代码。
`config`        | `kubectl config SUBCOMMAND [flags]` | 修改 kubeconfig 文件。有关详细信息，请参阅各个子命令。
`convert`    | `kubectl convert -f FILENAME [options]` | 在不同的 API 版本之间转换配置文件。配置文件可以是 YAML 或 JSON 格式。注意 - 需要安装 `kubectl-convert` 插件。
`cordon`    | `kubectl cordon NODE [options]` | 将节点标记为不可调度。
`cp`    | `kubectl cp <file-spec-src> <file-spec-dest> [options]` | 从容器复制文件、目录或将文件、目录复制到容器。
`create`        | `kubectl create -f FILENAME [flags]` | 从文件或 stdin 创建一个或多个资源。
`delete`        |  <code>kubectl delete (-f FILENAME &#124; TYPE [NAME &#124; /NAME &#124; -l label &#124; --all]) [flags]</code> |  基于文件、标准输入或通过指定标签选择器、名称、资源选择器或资源本身，删除资源。
`describe`    | <code>kubectl describe (-f FILENAME &#124; TYPE [NAME_PREFIX &#124; /NAME &#124; -l label]) [flags]</code> | 显示一个或多个资源的详细状态。
`diff`        | `kubectl diff -f FILENAME [flags]`| 在当前起作用的配置和文件或标准输之间作对比 (**BETA**)
`drain`    | `kubectl drain NODE [options]` | 腾空节点以准备维护。
`edit`        | <code>kubectl edit (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) [flags]</code> | 使用默认编辑器编辑和更新服务器上一个或多个资源的定义。
`events`      | `kubectl events` | 列举事件。
`exec`        | `kubectl exec POD [-c CONTAINER] [-i] [-t] [flags] [-- COMMAND [args...]]` | 对 Pod 中的容器执行命令。
`explain`    | `kubectl explain  [--recursive=false] [flags]` | 获取多种资源的文档。例如 Pod、Node、Service 等。
`expose`        | <code>kubectl expose (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) [--port=port] [--protocol=TCP&#124;UDP] [--target-port=number-or-name] [--name=name] [--external-ip=external-ip-of-service] [--type=type] [flags]</code> | 将副本控制器、服务或 Pod 作为新的 Kubernetes 服务暴露。
`get`        | <code>kubectl get (-f FILENAME &#124; TYPE [NAME &#124; /NAME &#124; -l label]) [--watch] [--sort-by=FIELD] [[-o &#124; --output]=OUTPUT_FORMAT] [flags]</code> | 列出一个或多个资源。
`kustomize`    | <code>kubectl kustomize <dir> [flags] [options]` </code> | 列出从 kustomization.yaml 文件中的指令生成的一组 API 资源。参数必须是包含文件的目录的路径，或者是 git 存储库 URL，其路径后缀相对于存储库根目录指定了相同的路径。
`label`        | <code>kubectl label (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) KEY_1=VAL_1 ... KEY_N=VAL_N [--overwrite] [--all] [--resource-version=version] [flags]</code> | 添加或更新一个或多个资源的标签。
`logs`        | `kubectl logs POD [-c CONTAINER] [--follow] [flags]` |  打印 Pod 中容器的日志。
`options`    | `kubectl options` | 全局命令行选项列表，这些选项适用于所有命令。
`patch`        | <code>kubectl patch (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) --patch PATCH [flags]</code> | 使用策略合并流程更新资源的一个或多个字段。
`plugin`    | `kubectl plugin [flags] [options]` | 提供用于与插件交互的实用程序。
`port-forward`    | `kubectl port-forward POD [LOCAL_PORT:]REMOTE_PORT [...[LOCAL_PORT_N:]REMOTE_PORT_N] [flags]` | 将一个或多个本地端口转发到一个 Pod。
`proxy`        | `kubectl proxy [--port=PORT] [--www=static-dir] [--www-prefix=prefix] [--api-prefix=prefix] [flags]` | 运行访问 Kubernetes API 服务器的代理。
`replace`        | `kubectl replace -f FILENAME` |  基于文件或标准输入替换资源。
`rollout`    | `kubectl rollout SUBCOMMAND [options]` | 管理资源的上线。有效的资源类型包括：Deployment、 DaemonSet 和 StatefulSet。
`run`        | <code>kubectl run NAME --image=image [--env="key=value"] [--port=port] [--dry-run=server &#124; client &#124; none] [--overrides=inline-json] [flags]</code> | 在集群上运行指定的镜像。
`scale`        | <code>kubectl scale (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) --replicas=COUNT [--resource-version=version] [--current-replicas=count] [flags]</code> | 更新指定副本控制器的大小。
`set`    | `kubectl set SUBCOMMAND [options]` | 配置应用资源。
`taint`    | `kubectl taint NODE NAME KEY_1=VAL_1:TAINT_EFFECT_1 ... KEY_N=VAL_N:TAINT_EFFECT_N [options]` | 更新一个或多个节点上的污点。
`top`    | `kubectl top [flags] [options]` | 显示资源（CPU、内存、存储）的使用情况。
`uncordon`    | `kubectl uncordon NODE [options]` | 将节点标记为可调度。
`version`        | `kubectl version [--client] [flags]` | 显示运行在客户端和服务器上的 Kubernetes 版本。
`wait`    | <code>kubectl wait ([-f FILENAME] &#124; resource.group/resource.name &#124; resource.group [(-l label &#124; --all)]) [--for=delete&#124;--for condition=available] [options]</code> | 实验特性：等待一种或多种资源的特定状况。

了解更多有关命令操作的信息，
请参阅 [kubectl](/zh-cn/docs/reference/kubectl/kubectl/) 参考文档。

## 资源类型   {#resource-types}

下表列出所有受支持的资源类型及其缩写别名。

(以下输出可以通过 `kubectl api-resources` 获取，内容以 Kubernetes 1.25.0 版本为准。)

| 资源名 | 缩写名 | API 版本 | 按命名空间 | 资源类型 |
|---|---|---|---|---|
| `bindings` |  | v1 | true | Binding |
| `componentstatuses` | `cs` | v1 | false | ComponentStatus |
| `configmaps` | `cm` | v1 | true | ConfigMap |
| `endpoints` | `ep` | v1 | true | Endpoints |
| `events` | `ev` | v1 | true | Event |
| `limitranges` | `limits` | v1 | true | LimitRange |
| `namespaces` | `ns` | v1 | false | Namespace |
| `nodes` | `no` | v1 | false | Node |
| `persistentvolumeclaims` | `pvc` | v1 | true | PersistentVolumeClaim |
| `persistentvolumes` | `pv` | v1 | false | PersistentVolume |
| `pods` | `po` | v1 | true | Pod |
| `podtemplates` |  | v1 | true | PodTemplate |
| `replicationcontrollers` | `rc` | v1 | true | ReplicationController |
| `resourcequotas` | `quota` | v1 | true | ResourceQuota |
| `secrets` |  | v1 | true | Secret |
| `serviceaccounts` | `sa` | v1 | true | ServiceAccount |
| `services` | `svc` | v1 | true | Service |
| `mutatingwebhookconfigurations` |  | admissionregistration.k8s.io/v1 | false | MutatingWebhookConfiguration |
| `validatingwebhookconfigurations` |  | admissionregistration.k8s.io/v1 | false | ValidatingWebhookConfiguration |
| `customresourcedefinitions` | `crd,crds` | apiextensions.k8s.io/v1 | false | CustomResourceDefinition |
| `apiservices` |  | apiregistration.k8s.io/v1 | false | APIService |
| `controllerrevisions` |  | apps/v1 | true | ControllerRevision |
| `daemonsets` | `ds` | apps/v1 | true | DaemonSet |
| `deployments` | `deploy` | apps/v1 | true | Deployment |
| `replicasets` | `rs` | apps/v1 | true | ReplicaSet |
| `statefulsets` | `sts` | apps/v1 | true | StatefulSet |
| `tokenreviews` |  | authentication.k8s.io/v1 | false | TokenReview |
| `localsubjectaccessreviews` |  | authorization.k8s.io/v1 | true | LocalSubjectAccessReview |
| `selfsubjectaccessreviews` |  | authorization.k8s.io/v1 | false | SelfSubjectAccessReview |
| `selfsubjectrulesreviews` |  | authorization.k8s.io/v1 | false | SelfSubjectRulesReview |
| `subjectaccessreviews` |  | authorization.k8s.io/v1 | false | SubjectAccessReview |
| `horizontalpodautoscalers` | `hpa` | autoscaling/v2 | true | HorizontalPodAutoscaler |
| `cronjobs` | `cj` | batch/v1 | true | CronJob |
| `jobs` |  | batch/v1 | true | Job |
| `certificatesigningrequests` | `csr` | certificates.k8s.io/v1 | false | CertificateSigningRequest |
| `leases` |  | coordination.k8s.io/v1 | true | Lease |
| `endpointslices` |  | discovery.k8s.io/v1 | true | EndpointSlice |
| `events` | `ev` | events.k8s.io/v1 | true | Event |
| `flowschemas` |  | flowcontrol.apiserver.k8s.io/v1beta2 | false | FlowSchema |
| `prioritylevelconfigurations` |  | flowcontrol.apiserver.k8s.io/v1beta2 | false | PriorityLevelConfiguration |
| `ingressclasses` |  | networking.k8s.io/v1 | false | IngressClass |
| `ingresses` | `ing` | networking.k8s.io/v1 | true | Ingress |
| `networkpolicies` | `netpol` | networking.k8s.io/v1 | true | NetworkPolicy |
| `runtimeclasses` |  | node.k8s.io/v1 | false | RuntimeClass |
| `poddisruptionbudgets` | `pdb` | policy/v1 | true | PodDisruptionBudget |
| `podsecuritypolicies` | `psp` | policy/v1beta1 | false | PodSecurityPolicy |
| `clusterrolebindings` |  | rbac.authorization.k8s.io/v1 | false | ClusterRoleBinding |
| `clusterroles` |  | rbac.authorization.k8s.io/v1 | false | ClusterRole |
| `rolebindings` |  | rbac.authorization.k8s.io/v1 | true | RoleBinding |
| `roles` |  | rbac.authorization.k8s.io/v1 | true | Role |
| `priorityclasses` | `pc` | scheduling.k8s.io/v1 | false | PriorityClass |
| `csidrivers` |  | storage.k8s.io/v1 | false | CSIDriver |
| `csinodes` |  | storage.k8s.io/v1 | false | CSINode |
| `csistoragecapacities` |  | storage.k8s.io/v1 | true | CSIStorageCapacity |
| `storageclasses` | `sc` | storage.k8s.io/v1 | false | StorageClass |
| `volumeattachments` |  | storage.k8s.io/v1 | false | VolumeAttachment |

## 输出选项   {#output-options}

有关如何格式化或排序某些命令的输出的信息，请参阅以下章节。有关哪些命令支持不同输出选项的详细信息，
请参阅 [kubectl](/zh-cn/docs/reference/kubectl/kubectl/) 参考文档。

### 格式化输出   {#formatting-output}

所有 `kubectl` 命令的默认输出格式都是人类可读的纯文本格式。要以特定格式在终端窗口输出详细信息，
可以将 `-o` 或 `--output` 参数添加到受支持的 `kubectl` 命令中。

#### 语法

```shell
kubectl [command] [TYPE] [NAME] -o <output_format>
```

取决于具体的 `kubectl` 操作，支持的输出格式如下：

输出格式  |  描述
--------------| -----------
`-o custom-columns=<spec>` | 使用逗号分隔的[自定义列](#custom-columns)列表打印表。
`-o custom-columns-file=<filename>` | 使用 `<filename>` 文件中的[自定义列](#custom-columns)模板打印表。
`-o json`     | 输出 JSON 格式的 API 对象
`-o jsonpath=<template>` | 打印 [jsonpath](/zh-cn/docs/reference/kubectl/jsonpath/) 表达式定义的字段
`-o jsonpath-file=<filename>` | 打印 `<filename>` 文件中 [jsonpath](/zh-cn/docs/reference/kubectl/jsonpath/) 表达式定义的字段。
`-o name`     | 仅打印资源名称而不打印任何其他内容。
`-o wide`     | 以纯文本格式输出，包含所有附加信息。对于 Pod 包含节点名。
`-o yaml`     | 输出 YAML 格式的 API 对象。

##### 示例

在此示例中，以下命令将单个 Pod 的详细信息输出为 YAML 格式的对象：

```shell
kubectl get pod web-pod-13je7 -o yaml
```
请记住：有关每个命令支持哪种输出格式的详细信息，
请参阅 [kubectl](/zh-cn/docs/reference/kubectl/kubectl/) 参考文档。

#### 自定义列   {#custom-columns}

要定义自定义列并仅将所需的详细信息输出到表中，可以使用 `custom-columns` 选项。
你可以选择内联定义自定义列或使用模板文件：`-o custom-columns=<spec>` 或 `-o custom-columns-file=<filename>`。

##### 示例

内联：

```shell
kubectl get pods <pod-name> -o custom-columns=NAME:.metadata.name,RSRC:.metadata.resourceVersion
```

模板文件：

```shell
kubectl get pods <pod-name> -o custom-columns-file=template.txt
```

其中，`template.txt` 文件包含：

```
NAME          RSRC
metadata.name metadata.resourceVersion
```

运行这两个命令之一的结果类似于：

```
NAME           RSRC
submit-queue   610995
```

#### Server-side 列

`kubectl` 支持从服务器接收关于对象的特定列信息。
这意味着对于任何给定的资源，服务器将返回与该资源相关的列和行，以便客户端打印。
通过让服务器封装打印的细节，这允许在针对同一集群使用的客户端之间提供一致的人类可读输出。

此功能默认启用。要禁用它，请将该 `--server-print=false` 参数添加到 `kubectl get` 命令中。

##### 例子

要打印有关 Pod 状态的信息，请使用如下命令：

```shell
kubectl get pods <pod-name> --server-print=false
```

输出类似于：

```
NAME       AGE
pod-name   1m
```

### 排序列表对象

要将对象排序后输出到终端窗口，可以将 `--sort-by` 参数添加到支持的 `kubectl` 命令。
通过使用 `--sort-by` 参数指定任何数字或字符串字段来对对象进行排序。
要指定字段，请使用 [jsonpath](/zh-cn/docs/reference/kubectl/jsonpath/) 表达式。

#### 语法

```shell
kubectl [command] [TYPE] [NAME] --sort-by=<jsonpath_exp>
```

##### 示例

要打印按名称排序的 Pod 列表，请运行：

```shell
kubectl get pods --sort-by=.metadata.name
```

## 示例：常用操作

使用以下示例集来帮助你熟悉运行常用 kubectl 操作：

`kubectl apply` - 以文件或标准输入为准应用或更新资源。

```shell
# 使用 example-service.yaml 中的定义创建服务。
kubectl apply -f example-service.yaml

# 使用 example-controller.yaml 中的定义创建 replication controller。
kubectl apply -f example-controller.yaml

# 使用 <directory> 路径下的任意 .yaml、.yml 或 .json 文件 创建对象。
kubectl apply -f <directory>
```

`kubectl get` - 列出一个或多个资源。


```shell
# 以纯文本输出格式列出所有 Pod。
kubectl get pods

# 以纯文本输出格式列出所有 Pod，并包含附加信息(如节点名)。
kubectl get pods -o wide

# 以纯文本输出格式列出具有指定名称的副本控制器。提示：你可以使用别名 'rc' 缩短和替换 'replicationcontroller' 资源类型。
kubectl get replicationcontroller <rc-name>

# 以纯文本输出格式列出所有副本控制器和服务。
kubectl get rc,services

# 以纯文本输出格式列出所有守护程序集，包括未初始化的守护程序集。
kubectl get ds --include-uninitialized

# 列出在节点 server01 上运行的所有 Pod
kubectl get pods --field-selector=spec.nodeName=server01
```

`kubectl describe` - 显示一个或多个资源的详细状态，默认情况下包括未初始化的资源。


```shell
# 显示名为 <pod-name> 的 Pod 的详细信息。
kubectl describe nodes <node-name>

# 显示名为 <pod-name> 的 Pod 的详细信息。
kubectl describe pods/<pod-name>

# 显示由名为 <rc-name> 的副本控制器管理的所有 Pod 的详细信息。
# 记住：副本控制器创建的任何 Pod 都以副本控制器的名称为前缀。
kubectl describe pods <rc-name>

# 描述所有的 Pod
kubectl describe pods
```

{{< note >}}

`kubectl get` 命令通常用于检索同一资源类别的一个或多个资源。
它具有丰富的参数，允许你使用 `-o` 或 `--output` 参数自定义输出格式。
你可以指定 `-w` 或 `--watch` 参数以开始监测特定对象的更新。
`kubectl describe` 命令更侧重于描述指定资源的许多相关方面。它可以调用对 `API 服务器` 的多个 API 调用来为用户构建视图。
例如，该 `kubectl describe node` 命令不仅检索有关节点的信息，还检索在其上运行的 Pod 的摘要，为节点生成的事件等。

{{< /note >}}

`kubectl delete` - 基于文件、标准输入或通过指定标签选择器、名称、资源选择器或资源来删除资源。


```shell
# 使用 pod.yaml 文件中指定的类型和名称删除 Pod。
kubectl delete -f pod.yaml

# 删除所有带有 '<label-key>=<label-value>' 标签的 Pod 和服务。
kubectl delete pods,services -l <label-key>=<label-value>

# 删除所有 Pod，包括未初始化的 Pod。
kubectl delete pods --all
```

`kubectl exec` - 对 Pod 中的容器执行命令。


```shell
# 从 Pod <pod-name> 中获取运行 'date' 的输出。默认情况下，输出来自第一个容器。
kubectl exec <pod-name> -- date

# 运行输出 'date' 获取在 Pod <pod-name> 中容器 <container-name> 的输出。
kubectl exec <pod-name> -c <container-name> -- date

# 获取一个交互 TTY 并在 Pod  <pod-name> 中运行 /bin/bash。默认情况下，输出来自第一个容器。
kubectl exec -ti <pod-name> -- /bin/bash
```

`kubectl logs` - 打印 Pod 中容器的日志。


```shell
# 返回 Pod <pod-name> 的日志快照。
kubectl logs <pod-name>

# 从 Pod <pod-name> 开始流式传输日志。这类似于 'tail -f' Linux 命令。
kubectl logs -f <pod-name>
```

`kubectl diff` - 查看集群建议更新的差异。

```shell
# “pod.json”中包含的差异资源。
kubectl diff -f pod.json

# 从标准输入读取的差异文件。
cat service.yaml | kubectl diff -f -
```

## 示例：创建和使用插件

使用以下示例来帮助你熟悉编写和使用 `kubectl` 插件：

```shell
# 用任何语言创建一个简单的插件，并为生成的可执行文件命名
# 以前缀 "kubectl-" 开始
cat ./kubectl-hello
```


```shell
#!/bin/sh

# 这个插件打印单词 "hello world"
echo "hello world"
```

这个插件写好了，把它变成可执行的：
```bash
sudo chmod a+x ./kubectl-hello

# 并将其移动到路径中的某个位置
sudo mv ./kubectl-hello /usr/local/bin
sudo chown root:root /usr/local/bin

# 你现在已经创建并"安装了"一个 kubectl 插件。
# 你可以开始使用这个插件，从 kubectl 调用它，就像它是一个常规命令一样
kubectl hello
```

```
hello world
```
```shell
# 你可以"卸载"一个插件，只需从你的 $PATH 中删除它
sudo rm /usr/local/bin/kubectl-hello
```

为了查看可用的所有 `kubectl` 插件，你可以使用 `kubectl plugin list` 子命令：

```shell
kubectl plugin list
```
输出类似于：

```
The following kubectl-compatible plugins are available:

/usr/local/bin/kubectl-hello
/usr/local/bin/kubectl-foo
/usr/local/bin/kubectl-bar
```
`kubectl plugin list` 指令也可以向你告警哪些插件被运行，或是被其它插件覆盖了，例如：

```shell
sudo chmod -x /usr/local/bin/kubectl-foo # 删除执行权限
kubectl plugin list
```

```
The following kubectl-compatible plugins are available:

/usr/local/bin/kubectl-hello
/usr/local/bin/kubectl-foo
  - warning: /usr/local/bin/kubectl-foo identified as a plugin, but it is not executable
/usr/local/bin/kubectl-bar

error: one plugin warning was found
```

你可以将插件视为在现有 kubectl 命令之上构建更复杂功能的一种方法：

```shell
cat ./kubectl-whoami
```

接下来的几个示例假设你已经将 `kubectl-whoami` 设置为以下内容：

```shell
#!/bin/bash

#这个插件利用 `kubectl config` 命令基于当前所选上下文输出当前用户的信息
kubectl config view --template='{{ range .contexts }}{{ if eq .name "'$(kubectl config current-context)'" }}Current user: {{ printf "%s\n" .context.user }}{{ end }}{{ end }}'
```

运行以上命令将为你提供一个输出，其中包含 KUBECONFIG 文件中当前上下文的用户：

```shell
#!/bin/bash
# 使文件成为可执行的
sudo chmod +x ./kubectl-whoami

# 然后移动到你的路径中
sudo mv ./kubectl-whoami /usr/local/bin

kubectl whoami
Current user: plugins-user
```

## {{% heading "whatsnext" %}}

* 阅读 `kubectl` 参考文档：
  * kubectl [命令参考](/zh-cn/docs/reference/kubectl/kubectl/)
  * 参考[命令行参数](/docs/reference/generated/kubectl/kubectl-commands/)
* 学习关于 [`kubectl` 使用约定](/zh-cn/docs/reference/kubectl/conventions/)
* 阅读 kubectl 中的 [JSONPath 支持](/zh-cn/docs/reference/kubectl/jsonpath/)
* 了解如何[使用插件扩展 kubectl](/zh-cn/docs/tasks/extend-kubectl/kubectl-plugins)
  * 查看更多[示例 CLI 插件](https://github.com/kubernetes/sample-cli-plugin)。
