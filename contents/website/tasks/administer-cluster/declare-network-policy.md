---
title: 声明网络策略
min-kubernetes-server-version: v1.8
content_type: task
weight: 180
---


本文可以帮助你开始使用 Kubernetes 的
[NetworkPolicy API](/zh-cn/docs/concepts/services-networking/network-policies/)
声明网络策略去管理 Pod 之间的通信

{{% thirdparty-content %}}

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

你首先需要有一个支持网络策略的 Kubernetes 集群。已经有许多支持 NetworkPolicy 的网络提供商，包括：

* [Antrea](/zh-cn/docs/tasks/administer-cluster/network-policy-provider/antrea-network-policy/)
* [Calico](/zh-cn/docs/tasks/administer-cluster/network-policy-provider/calico-network-policy/)
* [Cilium](/zh-cn/docs/tasks/administer-cluster/network-policy-provider/cilium-network-policy/)
* [Kube-router](/zh-cn/docs/tasks/administer-cluster/network-policy-provider/kube-router-network-policy/)
* [Romana](/zh-cn/docs/tasks/administer-cluster/network-policy-provider/romana-network-policy/)
* [Weave 网络](/zh-cn/docs/tasks/administer-cluster/network-policy-provider/weave-network-policy/)


## 创建一个`nginx` Deployment 并且通过服务将其暴露

为了查看 Kubernetes 网络策略是怎样工作的，可以从创建一个`nginx` Deployment 并且通过服务将其暴露开始

```shell
kubectl create deployment nginx --image=nginx
```

```none
deployment.apps/nginx created
```

将此 Deployment 以名为 `nginx` 的 Service 暴露出来：

```shell
kubectl expose deployment nginx --port=80
```

```none
service/nginx exposed
```

上述命令创建了一个带有一个 nginx 的 Deployment，并将之通过名为 `nginx` 的
Service 暴露出来。名为 `nginx` 的 Pod 和 Deployment 都位于 `default`
名字空间内。

```shell
kubectl get svc,pod
```
```none
NAME                        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
service/kubernetes          10.100.0.1    <none>        443/TCP    46m
service/nginx               10.100.0.16   <none>        80/TCP     33s

NAME                        READY         STATUS        RESTARTS   AGE
pod/nginx-701339712-e0qfq   1/1           Running       0          35s
```

## 通过从 Pod 访问服务对其进行测试

你应该可以从其它的 Pod 访问这个新的 `nginx` 服务。
要从 default 命名空间中的其它 Pod 来访问该服务。可以启动一个 busybox 容器：

```shell
kubectl run busybox --rm -ti --image=busybox:1.28 -- /bin/sh
```

在你的 Shell 中，运行下面的命令：

```shell
wget --spider --timeout=1 nginx
```

```none
Connecting to nginx (10.100.0.16:80)
remote file exists
```

## 限制 `nginx` 服务的访问

如果想限制对 `nginx` 服务的访问，只让那些拥有标签 `access: true` 的 Pod 访问它，
那么可以创建一个如下所示的 NetworkPolicy 对象：

{{< codenew file="service/networking/nginx-policy.yaml" >}}

NetworkPolicy 对象的名称必须是一个合法的
[DNS 子域名](/zh-cn/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

{{< note >}}
NetworkPolicy 中包含选择策略所适用的 Pods 集合的 `podSelector`。
你可以看到上面的策略选择的是带有标签 `app=nginx` 的 Pods。
此标签是被自动添加到 `nginx` Deployment 中的 Pod 上的。
如果 `podSelector` 为空，则意味着选择的是名字空间中的所有 Pods。
{{< /note >}}

## 为服务指定策略

使用 kubectl 根据上面的 `nginx-policy.yaml` 文件创建一个 NetworkPolicy：

```shell
kubectl apply -f https://k8s.io/examples/service/networking/nginx-policy.yaml
```
```none
networkpolicy.networking.k8s.io/access-nginx created
```

## 测试没有定义访问标签时访问服务

如果你尝试从没有设定正确标签的 Pod 中去访问 `nginx` 服务，请求将会超时：

```shell
kubectl run busybox --rm -ti --image=busybox:1.28 -- /bin/sh
```

在 Shell 中运行命令：

```shell
wget --spider --timeout=1 nginx
```

```none
Connecting to nginx (10.100.0.16:80)
wget: download timed out
```

## 定义访问标签后再次测试

创建一个拥有正确标签的 Pod，你将看到请求是被允许的：

```shell
kubectl run busybox --rm -ti --labels="access=true" --image=busybox:1.28 -- /bin/sh
```
在 Shell 中运行命令：

```shell
wget --spider --timeout=1 nginx
```

```none
Connecting to nginx (10.100.0.16:80)
remote file exists
```

