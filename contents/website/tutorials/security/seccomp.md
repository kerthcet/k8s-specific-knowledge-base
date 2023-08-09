---
title: 使用 seccomp 限制容器的系统调用
content_type: tutorial
weight: 40
min-kubernetes-server-version: v1.22
---


{{< feature-state for_k8s_version="v1.19" state="stable" >}}

Seccomp 代表安全计算（Secure Computing）模式，自 2.6.12 版本以来，一直是 Linux 内核的一个特性。
它可以用来沙箱化进程的权限，限制进程从用户态到内核态的调用。
Kubernetes 能使你自动将加载到{{< glossary_tooltip text="节点" term_id="node" >}}上的
seccomp 配置文件应用到你的 Pod 和容器。

识别你的工作负载所需要的权限是很困难的。在本篇教程中，
你将了解如何将 seccomp 配置文件加载到本地的 Kubernetes 集群中，
如何将它们应用到 Pod，以及如何开始制作只为容器进程提供必要的权限的配置文件。

## {{% heading "objectives" %}}

* 了解如何在节点上加载 seccomp 配置文件
* 了解如何将 seccomp 配置文件应用到容器上
* 观察容器进程对系统调用的审计
* 观察指定的配置文件缺失时的行为
* 观察违反 seccomp 配置文件的行为
* 了解如何创建细粒度的 seccomp 配置文件
* 了解如何应用容器运行时所默认的 seccomp 配置文件

## {{% heading "prerequisites" %}}

为了完成本篇教程中的所有步骤，你必须安装 [kind](/zh-cn/docs/tasks/tools/#kind)
和 [kubectl](/zh-cn/docs/tasks/tools/#kubectl)。

本篇教程演示的某些示例仍然是 Beta 状态（自 v1.25 起），另一些示例则仅使用 seccomp 正式发布的功能。
你应该确保，针对你使用的版本，
[正确配置](https://kind.sigs.k8s.io/docs/user/quick-start/#setting-kubernetes-version)了集群。

本篇教程也使用了 `curl` 工具来下载示例到你的计算机上。
你可以使用其他自己偏好的工具来自适应这些步骤。

{{< note >}}
无法将 seccomp 配置文件应用于在容器的 `securityContext` 中设置了 `privileged: true` 的容器。
特权容器始终以 `Unconfined` 的方式运行。
{{< /note >}}


## 下载示例 seccomp 配置文件  {#download-profiles}

这些配置文件的内容将在稍后进行分析，
现在先将它们下载到名为 `profiles/` 的目录中，以便将它们加载到集群中。

{{< tabs name="tab_with_code" >}}
{{< tab name="audit.json" >}}
{{< codenew file="pods/security/seccomp/profiles/audit.json" >}}
{{< /tab >}}
{{< tab name="violation.json" >}}
{{< codenew file="pods/security/seccomp/profiles/violation.json" >}}
{{< /tab >}}
{{< tab name="fine-grained.json" >}}
{{< codenew file="pods/security/seccomp/profiles/fine-grained.json" >}}
{{< /tab >}}
{{< /tabs >}}

执行这些命令：

```shell
mkdir ./profiles
curl -L -o profiles/audit.json https://k8s.io/examples/pods/security/seccomp/profiles/audit.json
curl -L -o profiles/violation.json https://k8s.io/examples/pods/security/seccomp/profiles/violation.json
curl -L -o profiles/fine-grained.json https://k8s.io/examples/pods/security/seccomp/profiles/fine-grained.json
ls profiles
```

你应该看到在最后一步的末尾列出有三个配置文件：

```
audit.json  fine-grained.json  violation.json
```

## 使用 kind 创建本地 Kubernetes 集群 {#create-a-local-kubernetes-cluster-with-kind}

为简单起见，[kind](https://kind.sigs.k8s.io/) 可用来创建加载了 seccomp 配置文件的单节点集群。
Kind 在 Docker 中运行 Kubernetes，因此集群的每个节点都是一个容器。
这允许将文件挂载到每个容器的文件系统中，类似于将文件加载到节点上。

{{< codenew file="pods/security/seccomp/kind.yaml" >}}

下载该示例 kind 配置，并将其保存到名为 `kind.yaml` 的文件中：

```shell
curl -L -O https://k8s.io/examples/pods/security/seccomp/kind.yaml
```

你可以通过设置节点的容器镜像来设置特定的 Kubernetes 版本。
有关此类配置的更多信息，
参阅 kind 文档中[节点](https://kind.sigs.k8s.io/docs/user/configuration/#nodes)小节。
本篇教程假定你正在使用 Kubernetes {{< param "version" >}}。

作为 Beta 特性，你可以将 Kubernetes
配置为使用{{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}默认首选的配置文件，
而不是回退到 `Unconfined`。
如果你想尝试，请在继续之前参阅
[启用使用 `RuntimeDefault` 作为所有工作负载的默认 seccomp 配置文件](#enable-runtimedefault-as-default)。

有了 kind 配置后，使用该配置创建 kind 集群：

```shell
kind create cluster --config=kind.yaml
```

新的 Kubernetes 集群准备就绪后，找出作为单节点集群运行的 Docker 容器：

```shell
docker ps
```

你应该看到输出中名为 `kind-control-plane` 的容器正在运行。
输出类似于：

```
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                       NAMES
6a96207fed4b        kindest/node:v1.18.2   "/usr/local/bin/entr…"   27 seconds ago      Up 24 seconds       127.0.0.1:42223->6443/tcp   kind-control-plane
```

如果观察该容器的文件系统，
你应该会看到 `profiles/` 目录已成功加载到 kubelet 的默认 seccomp 路径中。
使用 `docker exec` 在 Pod 中运行命令：

```shell
# 将 6a96207fed4b 更改为你从 “docker ps” 看到的容器 ID
docker exec -it 6a96207fed4b ls /var/lib/kubelet/seccomp/profiles
```

```
audit.json  fine-grained.json  violation.json
```

你已验证这些 seccomp 配置文件可用于在 kind 中运行的 kubelet。

## 启用使用 `RuntimeDefault` 作为所有工作负载的默认 seccomp 配置文件 {#enable-runtimedefault-as-default}

{{< feature-state state="stable" for_k8s_version="v1.27" >}}

要使用 Seccomp（安全计算模式）配置文件采用默认设置这一行为，你必须使用在想要启用此行为的每个节点上启用
`--seccomp-default`
[命令行标志](/zh-cn/docs/reference/command-line-tools-reference/kubelet)来运行 kubelet。

如果启用，kubelet 将会默认使用 `RuntimeDefault` seccomp 配置文件，
（这一配置文明是由容器运行时定义的），而不是使用 `Unconfined`（禁用 seccomp）模式。
默认的配置文件旨在提供一组限制性较强且能保留工作负载功能的安全默认值。
不同容器运行时及其不同发布版本之间的默认配置文件可能有所不同，
例如在比较来自 CRI-O 和 containerd 的配置文件时。

{{< note >}}
启用该功能既不会更改 Kubernetes `securityContext.seccompProfile` API 字段，
也不会添加已弃用的工作负载注解。
这为用户提供了随时回滚的可能性，而且无需实际更改工作负载配置。
[`crictl inspect`](https://github.com/kubernetes-sigs/cri-tools)
之类的工具可用于验证容器正在使用哪个 seccomp 配置文件。
{{< /note >}}

与其他工作负载相比，某些工作负载可能需要更少的系统调用限制。
这意味着即使使用 `RuntimeDefault` 配置文件，它们也可能在运行时失败。
要应对此类故障，你可以：

- 将工作负载显式运行为 `Unconfined`。
- 禁用节点的 `SeccompDefault` 特性。还要确保工作负载被调度到禁用该特性的节点上。
- 为工作负载创建自定义 seccomp 配置文件。

如果你将此特性引入到类似的生产集群中，
Kubernetes 项目建议你在部分节点上启用此特性门控，
然后在整个集群范围内推出更改之前，测试工作负载执行情况。

你可以在相关的 Kubernetes 增强提案（KEP）
中找到可能的升级和降级策略的更详细信息:
[默认启用 Seccomp](https://github.com/kubernetes/enhancements/tree/9a124fd29d1f9ddf2ff455c49a630e3181992c25/keps/sig-node/2413-seccomp-by-default#upgrade--downgrade-strategy)。

Kubernetes {{< skew currentVersion >}} 允许你配置 Seccomp 配置文件，
当 Pod 的规约未定义特定的 Seccomp 配置文件时应用该配置文件。
但是，你仍然需要为要使用它的每个节点启用此默认设置。

如果你正在运行 Kubernetes {{< skew currentVersion >}}
集群并希望启用该特性，请使用 `--seccomp-default` 命令行参数运行 kubelet，
或通过 [kubelet 配置文件](/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/)启用。

要在 [kind](https://kind.sigs.k8s.io) 启用特性门控，
请确保 `kind` 提供所需的最低 Kubernetes 版本，
并[在 kind 配置中](https://kind.sigs.k8s.io/docs/user/quick-start/#enable-feature-gates-in-your-cluster)
启用了 `SeccompDefault` 特性：

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    image: kindest/node:v1.23.0@sha256:49824ab1727c04e56a21a5d8372a402fcd32ea51ac96a2706a12af38934f81ac
    kubeadmConfigPatches:
      - |
        kind: JoinConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            seccomp-default: "true"
  - role: worker
    image: kindest/node:v1.23.0@sha256:49824ab1727c04e56a21a5d8372a402fcd32ea51ac96a2706a12af38934f81ac
    kubeadmConfigPatches:
      - |
        kind: JoinConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            seccomp-default: "true"
```

如果集群已就绪，则运行一个 Pod：

```shell
kubectl run --rm -it --restart=Never --image=alpine alpine -- sh
```

现在应该附加了默认的 seccomp 配置文件。
这可以通过使用 `docker exec` 为 kind 上的容器运行 `crictl inspect` 来验证：

```shell
docker exec -it kind-worker bash -c \
    'crictl inspect $(crictl ps --name=alpine -q) | jq .info.runtimeSpec.linux.seccomp'
```

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64", "SCMP_ARCH_X86", "SCMP_ARCH_X32"],
  "syscalls": [
    {
      "names": ["..."]
    }
  ]
}
```

## 创建使用容器运行时默认 seccomp 配置文件的 Pod {#create-pod-that-uses-the-container-runtime-default-seccomp-profile}

大多数容器运行时都提供了一组合理的、默认被允许或默认被禁止的系统调用。
你可以通过将 Pod 或容器的安全上下文中的 seccomp 类型设置为 `RuntimeDefault`
来为你的工作负载采用这些默认值。

{{< note >}}
如果你已经启用了 `seccompDefault` [配置](/zh-cn/docs/reference/config-api/kubelet-config.v1beta1/)，
只要没有指定其他 seccomp 配置文件，那么 Pod 就会使用 `RuntimeDefault` seccomp 配置文件。
否则，默认值为 `Unconfined`。
{{< /note >}}

这是一个 Pod 的清单，它要求其所有容器使用 `RuntimeDefault` seccomp 配置文件：

{{< codenew file="pods/security/seccomp/ga/default-pod.yaml" >}}

创建此 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/security/seccomp/ga/default-pod.yaml
```

```shell
kubectl get pod default-pod
```

此 Pod 应该显示为已成功启动：

```
NAME        READY   STATUS    RESTARTS   AGE
default-pod 1/1     Running   0          20s
```

最后，你看到一切正常之后，请清理：

```shell
kubectl delete pod default-pod --wait --now
```

## 使用 seccomp 配置文件创建 Pod 以进行系统调用审计 {#create-a-pod-with-a-seccomp-profile-for-syscall-auditing}

首先，将 `audit.json` 配置文件应用到新的 Pod 上，该配置文件将记录进程的所有系统调用。

这是该 Pod 的清单：

{{< codenew file="pods/security/seccomp/ga/audit-pod.yaml" >}}

{{< note >}}
旧版本的 Kubernetes 允许你使用{{< glossary_tooltip text="注解" term_id="annotation" >}}配置
seccomp 行为。Kubernetes {{< skew currentVersion >}} 仅支持使用位于 `.spec.securityContext`
内的字段来配置 seccomp。本教程将阐述这个方法。
{{< /note >}}

在集群中创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/security/seccomp/ga/audit-pod.yaml
```

此配置文件不限制任何系统调用，因此 Pod 应该成功启动。

```shell
kubectl get pod/audit-pod
```

```
NAME        READY   STATUS    RESTARTS   AGE
audit-pod   1/1     Running   0          30s
```

为了能够与容器暴露的端点交互，
创建一个 NodePort 类型的 {{< glossary_tooltip text="Service" term_id="service" >}}，
允许从 kind 控制平面容器内部访问端点。

```shell
kubectl expose pod audit-pod --type NodePort --port 5678
```

检查 Service 在节点上分配的端口。

```shell
kubectl get service audit-pod
```

输出类似于：

```
NAME        TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
audit-pod   NodePort   10.111.36.142   <none>        5678:32373/TCP   72s
```

现在，你可以使用 `curl` 从 kind 控制平面容器内部访问该端点，位于该服务所公开的端口上。
使用 `docker exec` 在属于该控制平面容器的容器中运行 `curl` 命令：

```shell
# 将 6a96207fed4b 更改为你从 “docker ps” 看到的控制平面容器 ID
docker exec -it 6a96207fed4b curl localhost:32373
```

```
just made some syscalls!
```

你可以看到该进程正在运行，但它实际上进行了哪些系统调用？
因为这个 Pod 在本地集群中运行，你应该能够在 `/var/log/syslog` 中看到它们。
打开一个新的终端窗口并 `tail` 来自 `http-echo` 的调用的输出：

```shell
tail -f /var/log/syslog | grep 'http-echo'
```

你应该已经看到了一些由 `http-echo` 进行的系统调用的日志，
如果你在控制平面容器中 `curl` 端点，你会看到更多的写入。

例如：

```
Jul  6 15:37:40 my-machine kernel: [369128.669452] audit: type=1326 audit(1594067860.484:14536): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=51 compat=0 ip=0x46fe1f code=0x7ffc0000
Jul  6 15:37:40 my-machine kernel: [369128.669453] audit: type=1326 audit(1594067860.484:14537): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=54 compat=0 ip=0x46fdba code=0x7ffc0000
Jul  6 15:37:40 my-machine kernel: [369128.669455] audit: type=1326 audit(1594067860.484:14538): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=202 compat=0 ip=0x455e53 code=0x7ffc0000
Jul  6 15:37:40 my-machine kernel: [369128.669456] audit: type=1326 audit(1594067860.484:14539): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=288 compat=0 ip=0x46fdba code=0x7ffc0000
Jul  6 15:37:40 my-machine kernel: [369128.669517] audit: type=1326 audit(1594067860.484:14540): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=0 compat=0 ip=0x46fd44 code=0x7ffc0000
Jul  6 15:37:40 my-machine kernel: [369128.669519] audit: type=1326 audit(1594067860.484:14541): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=270 compat=0 ip=0x4559b1 code=0x7ffc0000
Jul  6 15:38:40 my-machine kernel: [369188.671648] audit: type=1326 audit(1594067920.488:14559): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=270 compat=0 ip=0x4559b1 code=0x7ffc0000
Jul  6 15:38:40 my-machine kernel: [369188.671726] audit: type=1326 audit(1594067920.488:14560): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=202 compat=0 ip=0x455e53 code=0x7ffc0000
```

通过查看每一行的 `syscall=` 条目，你可以开始了解 `http-echo` 进程所需的系统调用。
虽然这些不太可能包含它使用的所有系统调用，但它可以作为此容器的 seccomp 配置文件的基础。

在转到下一部分之前清理该 Pod 和 Service：

```shell
kubectl delete service audit-pod --wait
kubectl delete pod audit-pod --wait --now
```

## 使用导致违规的 seccomp 配置文件创建 Pod {#create-pod-with-a-seccomp-profile-that-causes-violation}

出于演示目的，将配置文件应用于不允许任何系统调用的 Pod 上。

此演示的清单是：

{{< codenew file="pods/security/seccomp/ga/violation-pod.yaml" >}}

尝试在集群中创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/security/seccomp/ga/violation-pod.yaml
```

Pod 已创建，但存在问题。
如果你检查 Pod 状态，你应该看到它没有启动。

```shell
kubectl get pod/violation-pod
```

```
NAME            READY   STATUS             RESTARTS   AGE
violation-pod   0/1     CrashLoopBackOff   1          6s
```

如上例所示，`http-echo` 进程需要相当多的系统调用。
这里 seccomp 已通过设置 `"defaultAction": "SCMP_ACT_ERRNO"` 被指示为在发生任何系统调用时报错。
这是非常安全的，但消除了做任何有意义的事情的能力。
你真正想要的是只给工作负载它们所需要的权限。

在转到下一部分之前清理该 Pod：

```shell
kubectl delete pod violation-pod --wait --now
```

## 使用只允许必要的系统调用的 seccomp 配置文件创建 Pod {#create-pod-with-a-seccomp-profile-that-only-allows-necessary-syscalls}

如果你看一看 `fine-grained.json` 配置文件，
你会注意到第一个示例的 syslog 中看到的一些系统调用，
其中配置文件设置为 `"defaultAction": "SCMP_ACT_LOG"`。
现在的配置文件设置 `"defaultAction": "SCMP_ACT_ERRNO"`，
但在 `"action": "SCMP_ACT_ALLOW"` 块中明确允许一组系统调用。
理想情况下，容器将成功运行，并且你看到没有消息发送到 `syslog`。

此示例的清单是：

{{< codenew file="pods/security/seccomp/ga/fine-pod.yaml" >}}

在你的集群中创建 Pod：

```shell
kubectl apply -f https://k8s.io/examples/pods/security/seccomp/ga/fine-pod.yaml
```

```shell
kubectl get pod fine-pod
```

此 Pod 应该显示为已成功启动：

```
NAME        READY   STATUS    RESTARTS   AGE
fine-pod   1/1     Running   0          30s
```

打开一个新的终端窗口并使用 `tail` 来监视提到来自 `http-echo` 的调用的日志条目：

```shell
# 你计算机上的日志路径可能与 “/var/log/syslog” 不同
tail -f /var/log/syslog | grep 'http-echo'
```

接着，使用 NodePort Service 公开 Pod：

```shell
kubectl expose pod fine-pod --type NodePort --port 5678
```

检查节点上的 Service 分配了什么端口：

```shell
kubectl get service fine-pod
```

输出类似于：

```
NAME        TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
fine-pod    NodePort   10.111.36.142   <none>        5678:32373/TCP   72s
```

使用 `curl` 从 kind 控制平面容器内部访问端点：

```shell
# 将 6a96207fed4b 更改为你从 “docker ps” 看到的控制平面容器 ID
docker exec -it 6a96207fed4b curl localhost:32373
```

```
just made some syscalls!
```

你应该在 `syslog` 中看不到任何输出。
这是因为配置文件允许所有必要的系统调用，并指定如果调用列表之外的系统调用应发生错误。
从安全角度来看，这是一种理想的情况，但需要在分析程序时付出一些努力。
如果有一种简单的方法可以在不需要太多努力的情况下更接近这种安全性，那就太好了。

在转到下一部分之前清理该 Pod 和服务：

```shell
kubectl delete service fine-pod --wait
kubectl delete pod fine-pod --wait --now
```

## {{% heading "whatsnext" %}}

你可以了解有关 Linux seccomp 的更多信息：

* [seccomp 概述](https://lwn.net/Articles/656307/)
* [Docker 的 Seccomp 安全配置文件](https://docs.docker.com/engine/security/seccomp/)
