---
title: 使用 HostAliases 向 Pod /etc/hosts 文件添加条目
content_type: task
weight: 60
min-kubernetes-server-version: 1.7
---



当 DNS 配置以及其它选项不合理的时候，通过向 Pod 的 `/etc/hosts` 文件中添加条目，
可以在 Pod 级别覆盖对主机名的解析。你可以通过 PodSpec 的 HostAliases
字段来添加这些自定义条目。

建议通过使用 HostAliases 来进行修改，因为该文件由 Kubelet 管理，并且
可以在 Pod 创建/重启过程中被重写。


## 默认 hosts 文件内容

让我们从一个 Nginx Pod 开始，该 Pod 被分配一个 IP：

```shell
kubectl run nginx --image nginx
```

```
pod/nginx created
```

检查 Pod IP：

```shell
kubectl get pods --output=wide
```

```
NAME     READY     STATUS    RESTARTS   AGE    IP           NODE
nginx    1/1       Running   0          13s    10.200.0.4   worker0
```

主机文件的内容如下所示：

```shell
kubectl exec nginx -- cat /etc/hosts
```

```
# Kubernetes-managed hosts file.
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
fe00::0	ip6-mcastprefix
fe00::1	ip6-allnodes
fe00::2	ip6-allrouters
10.200.0.4	nginx
```

默认情况下，`hosts` 文件只包含 IPv4 和 IPv6 的样板内容，像 `localhost` 和主机名称。

## 通过 HostAliases 增加额外条目

除了默认的样板内容，你可以向 `hosts` 文件添加额外的条目。
例如，要将 `foo.local`、`bar.local` 解析为 `127.0.0.1`，
将 `foo.remote`、 `bar.remote` 解析为 `10.1.2.3`，你可以在
`.spec.hostAliases` 下为 Pod 配置 HostAliases。

{{< codenew file="service/networking/hostaliases-pod.yaml" >}}

你可以使用以下命令用此配置启动 Pod：

```shell
kubectl apply -f https://k8s.io/examples/service/networking/hostaliases-pod.yaml
```

```
pod/hostaliases-pod created
```

检查 Pod 详情，查看其 IPv4 地址和状态：

```shell
kubectl get pod --output=wide
```

```
NAME                READY     STATUS      RESTARTS   AGE       IP              NODE
hostaliases-pod     0/1       Completed   0          6s        10.200.0.5      worker0
```

`hosts` 文件的内容看起来类似如下所示：

```shell
kubectl logs hostaliases-pod
```

```
# Kubernetes-managed hosts file.
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
fe00::0	ip6-mcastprefix
fe00::1	ip6-allnodes
fe00::2	ip6-allrouters
10.200.0.5	hostaliases-pod

# Entries added by HostAliases.
127.0.0.1	foo.local	bar.local
10.1.2.3	foo.remote	bar.remote
```

在最下面额外添加了一些条目。

## 为什么 kubelet 管理 hosts 文件？{#why-does-kubelet-manage-the-hosts-file}

kubelet 管理每个Pod 容器的 `hosts` 文件，以防止容器运行时在容器已经启动后修改文件。
由于历史原因，Kubernetes 总是使用 Docker Engine 作为其容器运行时，而 Docker Engine 
将在容器启动后修改 `/etc/hosts` 文件。

当前的 Kubernetes 可以使用多种容器运行时；即便如此，kubelet 管理在每个容器中创建 hosts文件，
以便你使用任何容器运行时运行容器时，结果都符合预期。

{{< caution >}}
请避免手工更改容器内的 hosts 文件内容。

如果你对 hosts 文件做了手工修改，这些修改都会在容器退出时丢失。
{{< /caution >}}

