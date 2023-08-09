---
title: 通过文件将 Pod 信息呈现给容器
content_type: task
weight: 40
---


此页面描述 Pod 如何使用
[`downwardAPI` 卷](/zh-cn/docs/concepts/storage/volumes/#downwardapi)
把自己的信息呈现给 Pod 中运行的容器。
`downwardAPI` 卷可以呈现 Pod 和容器的字段。

在 Kubernetes 中，有两种方式可以将 Pod 和容器字段呈现给运行中的容器：

* [环境变量](/zh-cn/docs/tasks/inject-data-application/environment-variable-expose-pod-information/#the-downward-api)
* 本页面所述的卷文件

这两种呈现 Pod 和容器字段的方式都称为 **downward API**。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}


## 存储 Pod 字段   {#store-pod-fields}

在这部分的练习中，你将创建一个包含一个容器的 Pod，并将 Pod 级别的字段作为文件投射到正在运行的容器中。
Pod 的清单如下：

{{< codenew file="pods/inject/dapi-volume.yaml" >}}

在 Pod 清单中，你可以看到 Pod 有一个 `downwardAPI` 类型的卷，并且挂载到容器中的
`/etc/podinfo` 目录。

查看 `downwardAPI` 下面的 `items` 数组。
数组的每个元素定义一个 `downwardAPI` 卷。
第一个元素指示 Pod 的 `metadata.labels` 字段的值保存在名为 `labels` 的文件中。
第二个元素指示 Pod 的 `annotations` 字段的值保存在名为 `annotations` 的文件中。

{{< note >}}
本示例中的字段是 Pod 字段，不是 Pod 中容器的字段。
{{< /note >}}

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/inject/dapi-volume.yaml
```

验证 Pod 中的容器运行正常：

```shell
kubectl get pods
```

查看容器的日志：

```shell
kubectl logs kubernetes-downwardapi-volume-example
```

输出显示 `labels` 文件和 `annotations` 文件的内容：

```
cluster="test-cluster1"
rack="rack-22"
zone="us-est-coast"

build="two"
builder="john-doe"
```

进入 Pod 中运行的容器，打开一个 Shell：

```shell
kubectl exec -it kubernetes-downwardapi-volume-example -- sh
```

在该 Shell中，查看 `labels` 文件：

```shell
/# cat /etc/podinfo/labels
```

输出显示 Pod 的所有标签都已写入 `labels` 文件。

```
cluster="test-cluster1"
rack="rack-22"
zone="us-est-coast"
```

同样，查看 `annotations` 文件：

```shell
/# cat /etc/podinfo/annotations
```

查看 `/etc/podinfo` 目录下的文件：

```shell
/# ls -laR /etc/podinfo
```

在输出中可以看到，`labels` 和 `annotations` 文件都在一个临时子目录中。
在这个例子中，这个临时子目录为 `..2982_06_02_21_47_53.299460680`。
在 `/etc/podinfo` 目录中，`..data` 是指向该临时子目录的符号链接。
另外在 `/etc/podinfo` 目录中，`labels` 和 `annotations` 也是符号链接。

```
drwxr-xr-x  ... Feb 6 21:47 ..2982_06_02_21_47_53.299460680
lrwxrwxrwx  ... Feb 6 21:47 ..data -> ..2982_06_02_21_47_53.299460680
lrwxrwxrwx  ... Feb 6 21:47 annotations -> ..data/annotations
lrwxrwxrwx  ... Feb 6 21:47 labels -> ..data/labels

/etc/..2982_06_02_21_47_53.299460680:
total 8
-rw-r--r--  ... Feb  6 21:47 annotations
-rw-r--r--  ... Feb  6 21:47 labels
```

用符号链接可实现元数据的动态原子性刷新；更新将写入一个新的临时目录，
然后通过使用 [rename(2)](http://man7.org/linux/man-pages/man2/rename.2.html)
完成 `..data` 符号链接的原子性更新。

{{< note >}}
如果容器以
[subPath](/zh-cn/docs/concepts/storage/volumes/#using-subpath) 卷挂载方式来使用
Downward API，则该容器无法收到更新事件。
{{< /note >}}

退出 Shell：

```shell
/# exit
```

## 存储容器字段   {#store-container-fields}

前面的练习中，你使用 downward API 使 Pod 级别的字段可以被 Pod 内正在运行的容器访问。
接下来这个练习，你将只传递由 Pod 定义的部分的字段到 Pod 内正在运行的容器中，
但这些字段取自特定[容器](/zh-cn/docs/reference/kubernetes-api/workload-resources/pod-v1/#Container)而不是整个 Pod。
下面是一个同样只有一个容器的 Pod 的清单：

{{< codenew file="pods/inject/dapi-volume-resources.yaml" >}}

在这个清单中，你可以看到 Pod 有一个
[`downwardAPI` 卷](/zh-cn/docs/concepts/storage/volumes/#downwardapi)，
并且这个卷会挂载到 Pod 内的单个容器的 `/etc/podinfo` 目录。

查看 `downwardAPI` 下面的 `items` 数组。
数组的每个元素定义一个 `downwardAPI` 卷。

第一个元素指定在名为 `client-container` 的容器中，
以 `1m` 所指定格式的 `limits.cpu` 字段的值应推送到名为 `cpu_limit` 的文件中。
`divisor` 字段是可选的，默认值为 `1`。1 的除数表示 CPU 资源的核数或内存资源的字节数。

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/inject/dapi-volume-resources.yaml
```

打开一个 Shell，进入 Pod 中运行的容器：

```shell
kubectl exec -it kubernetes-downwardapi-volume-example-2 -- sh
```

在 Shell 中，查看 `cpu_limit` 文件：

```shell
# 在容器内的 Shell 中运行
cat /etc/podinfo/cpu_limit
```

你可以使用同样的命令查看 `cpu_request`、`mem_limit` 和 `mem_request` 文件。


## 投射键名到指定路径并且指定文件权限   {#project-keys-to-specific-paths-and-file-permissions}

你可以将键名投射到指定路径并且指定每个文件的访问权限。
更多信息，请参阅 [Secret](/zh-cn/docs/concepts/configuration/secret/)。

## {{% heading "whatsnext" %}}

* 参阅 Pod [`spec`](/zh-cn/docs/reference/kubernetes-api/workload-resources/pod-v1/#PodSpec)
  API 的定义，其中包括了容器（Pod 的一部分）的定义。
* 参阅你可以使用 downward API 公开的[可用字段](/zh-cn/docs/concepts/workloads/pods/downward-api/#available-fields)列表。

阅读旧版的 API 参考中关于卷的内容：
* 参阅
  [`Volume`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#volume-v1-core)
  API 定义，该 API 在 Pod 中定义通用卷以供容器访问。
* 参阅
  [`DownwardAPIVolumeSource`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#downwardapivolumesource-v1-core)
  API 定义，该 API 定义包含 Downward API 信息的卷。
* 参阅
  [`DownwardAPIVolumeFile`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#downwardapivolumefile-v1-core)
  API 定义，该 API 包含对对象或资源字段的引用，用于在 Downward API 卷中填充文件。
* 参阅
  [`ResourceFieldSelector`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#resourcefieldselector-v1-core)
  API 定义，该 API 指定容器资源及其输出格式。

