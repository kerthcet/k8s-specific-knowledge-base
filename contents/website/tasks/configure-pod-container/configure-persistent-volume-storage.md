---
title: 配置 Pod 以使用 PersistentVolume 作为存储
content_type: task
weight: 90
---


本文将向你介绍如何配置 Pod 使用
{{< glossary_tooltip text="PersistentVolumeClaim" term_id="persistent-volume-claim" >}}
作为存储。
以下是该过程的总结：

1. 你作为集群管理员创建由物理存储支持的 PersistentVolume。你不会将该卷与任何 Pod 关联。

1. 你现在以开发人员或者集群用户的角色创建一个 PersistentVolumeClaim，
   它将自动绑定到合适的 PersistentVolume。

1. 你创建一个使用以上 PersistentVolumeClaim 作为存储的 Pod。

## {{% heading "prerequisites" %}}

* 你需要一个包含单个节点的 Kubernetes 集群，并且必须配置
  {{< glossary_tooltip text="kubectl" term_id="kubectl" >}} 命令行工具以便与集群交互。
  如果还没有单节点集群，可以使用
  [Minikube](https://minikube.sigs.k8s.io/docs/) 创建一个。

* 熟悉[持久卷](/zh-cn/docs/concepts/storage/persistent-volumes/)文档。


## 在你的节点上创建一个 index.html 文件  {#create-an-index-file-on-your-node}

打开集群中的某个节点的 Shell。
如何打开 Shell 取决于集群的设置。
例如，如果你正在使用 Minikube，那么可以通过输入 `minikube ssh` 来打开节点的 Shell。

在该节点的 Shell 中，创建一个 `/mnt/data` 目录：

```shell
# 这里假定你的节点使用 "sudo" 来以超级用户角色执行命令
sudo mkdir /mnt/data
```

在 `/mnt/data` 目录中创建一个 index.html 文件：

```shell
# 这里再次假定你的节点使用 "sudo" 来以超级用户角色执行命令
sudo sh -c "echo 'Hello from Kubernetes storage' > /mnt/data/index.html"
```

{{< note >}}
如果你的节点使用某工具而不是 `sudo` 来完成超级用户访问，你可以将上述命令中的 `sudo` 替换为该工具的名称。
{{< /note >}}

测试 `index.html` 文件确实存在：

```shell
cat /mnt/data/index.html
```

输出应该是：

```
Hello from Kubernetes storage
```

现在你可以关闭节点的 Shell 了。

## 创建 PersistentVolume   {#create-a-pv}

在本练习中，你将创建一个 **hostPath** 类型的 PersistentVolume。
Kubernetes 支持用于在单节点集群上开发和测试的 hostPath 类型的 PersistentVolume。
hostPath 类型的 PersistentVolume 使用节点上的文件或目录来模拟网络附加存储。

在生产集群中，你不会使用 hostPath。
集群管理员会提供网络存储资源，比如 Google Compute Engine 持久盘卷、NFS 共享卷或 Amazon Elastic Block Store 卷。
集群管理员还可以使用
[StorageClasses](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#storageclass-v1-storage-k8s-io)
来设置[动态制备存储](/zh-cn/docs/concepts/storage/dynamic-provisioning/)。

下面是 hostPath PersistentVolume 的配置文件：

{{< codenew file="pods/storage/pv-volume.yaml" >}}

此配置文件指定卷位于集群节点上的 `/mnt/data` 路径。
其配置还指定了卷的容量大小为 10 GB，访问模式为 `ReadWriteOnce`，
这意味着该卷可以被单个节点以读写方式安装。
此配置文件还在 PersistentVolume 中定义了
[StorageClass 的名称](/zh-cn/docs/concepts/storage/persistent-volumes/#class)为 `manual`。
它将用于将 PersistentVolumeClaim 的请求绑定到此 PersistentVolume。

创建 PersistentVolume：

```shell
kubectl apply -f https://k8s.io/examples/pods/storage/pv-volume.yaml
```

查看 PersistentVolume 的信息：

```shell
kubectl get pv task-pv-volume
```

输出结果显示该 PersistentVolume 的`状态（STATUS）`为 `Available`。
这意味着它还没有被绑定给 PersistentVolumeClaim。

```
NAME             CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS      CLAIM     STORAGECLASS   REASON    AGE
task-pv-volume   10Gi       RWO           Retain          Available             manual                   4s
```

## 创建 PersistentVolumeClaim   {#create-a-pvc}

下一步是创建一个 PersistentVolumeClaim。
Pod 使用 PersistentVolumeClaim 来请求物理存储。
在本练习中，你将创建一个 PersistentVolumeClaim，它请求至少 3 GB 容量的卷，
该卷至少可以为一个节点提供读写访问。

下面是 PersistentVolumeClaim 的配置文件：

{{< codenew file="pods/storage/pv-claim.yaml" >}}

创建 PersistentVolumeClaim：

```shell
kubectl apply -f https://k8s.io/examples/pods/storage/pv-claim.yaml
```

创建 PersistentVolumeClaim 之后，Kubernetes 控制平面将查找满足申领要求的 PersistentVolume。
如果控制平面找到具有相同 StorageClass 的适当的 PersistentVolume，
则将 PersistentVolumeClaim 绑定到该 PersistentVolume 上。

再次查看 PersistentVolume 信息：

```shell
kubectl get pv task-pv-volume
```

现在输出的 `STATUS` 为 `Bound`。

```
NAME             CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM                   STORAGECLASS   REASON    AGE
task-pv-volume   10Gi       RWO           Retain          Bound     default/task-pv-claim   manual                   2m
```

查看 PersistentVolumeClaim：

```shell
kubectl get pvc task-pv-claim
```

输出结果表明该 PersistentVolumeClaim 绑定了你的 PersistentVolume `task-pv-volume`。

```
NAME            STATUS    VOLUME           CAPACITY   ACCESSMODES   STORAGECLASS   AGE
task-pv-claim   Bound     task-pv-volume   10Gi       RWO           manual         30s
```

## 创建 Pod   {#create-a-pod}

下一步是创建一个使用你的 PersistentVolumeClaim 作为存储卷的 Pod。

下面是此 Pod 的配置文件：

{{< codenew file="pods/storage/pv-pod.yaml" >}}

注意 Pod 的配置文件指定了 PersistentVolumeClaim，但没有指定 PersistentVolume。
对 Pod 而言，PersistentVolumeClaim 就是一个存储卷。

创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/storage/pv-pod.yaml
```

检查 Pod 中的容器是否运行正常：

```shell
kubectl get pod task-pv-pod
```

打开一个 Shell 访问 Pod 中的容器：

```shell
kubectl exec -it task-pv-pod -- /bin/bash
```

在 Shell 中，验证 Nginx 是否正在从 hostPath 卷提供 `index.html` 文件：

```shell
# 一定要在上一步 "kubectl exec" 所返回的 Shell 中执行下面三个命令
apt update
apt install curl
curl http://localhost/
```

输出结果是你之前写到 hostPath 卷中的 `index.html` 文件中的内容：

```
Hello from Kubernetes storage
```

如果你看到此消息，则证明你已经成功地配置了 Pod 使用 PersistentVolumeClaim
的存储。

## 清理    {#clean-up}

删除 Pod、PersistentVolumeClaim 和 PersistentVolume 对象：

```shell
kubectl delete pod task-pv-pod
kubectl delete pvc task-pv-claim
kubectl delete pv task-pv-volume
```

如果你还没有连接到集群中节点的 Shell，可以按之前所做操作，打开一个新的 Shell。

在节点的 Shell 上，删除你所创建的目录和文件：

```shell
# 这里假定你使用 "sudo" 来以超级用户的角色执行命令
sudo rm /mnt/data/index.html
sudo rmdir /mnt/data
```

你现在可以关闭连接到节点的 Shell。

## 在两个地方挂载相同的 persistentVolume   {#mounting-the-same-pv-in-two-places}

{{< codenew file="pods/storage/pv-duplicate.yaml" >}}

你可以在 nginx 容器上执行两个卷挂载:

- `/usr/share/nginx/html` 用于静态网站
- `/etc/nginx/nginx.conf` 作为默认配置


## 访问控制  {#access-control}

使用组 ID（GID）配置的存储仅允许 Pod 使用相同的 GID 进行写入。
GID 不匹配或缺失将会导致无权访问错误。
为了减少与用户的协调，管理员可以对 PersistentVolume 添加 GID 注解。
这样 GID 就能自动添加到使用 PersistentVolume 的任何 Pod 中。

使用 `pv.beta.kubernetes.io/gid` 注解的方法如下所示：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv1
  annotations:
    pv.beta.kubernetes.io/gid: "1234"
```

当 Pod 使用带有 GID 注解的 PersistentVolume 时，注解的 GID 会被应用于 Pod 中的所有容器，
应用的方法与 Pod 的安全上下文中指定的 GID 相同。
每个 GID，无论是来自 PersistentVolume 注解还是来自 Pod 规约，都会被应用于每个容器中运行的第一个进程。

{{< note >}}
当 Pod 使用 PersistentVolume 时，与 PersistentVolume 关联的 GID 不会在 Pod
资源本身的对象上出现。
{{< /note >}}

## {{% heading "whatsnext" %}}

* 进一步了解 [PersistentVolumes](/zh-cn/docs/concepts/storage/persistent-volumes/)
* 阅读[持久存储设计文档](https://git.k8s.io/design-proposals-archive/storage/persistent-storage.md)

### 参考   {#reference}

* [PersistentVolume](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolume-v1-core)
* [PersistentVolumeSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolumespec-v1-core)
* [PersistentVolumeClaim](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolumeclaim-v1-core)
* [PersistentVolumeClaimSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolumeclaimspec-v1-core)
