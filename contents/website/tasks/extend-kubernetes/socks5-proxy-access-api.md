---
title: 使用 SOCKS5 代理访问 Kubernetes API
content_type: task
weight: 42
min-kubernetes-server-version: v1.24
---

{{< feature-state for_k8s_version="v1.24" state="stable" >}}

本文展示了如何使用 SOCKS5 代理访问远程 Kubernetes 集群的 API。
当你要访问的集群不直接在公共 Internet 上公开其 API 时，这很有用。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

你需要 SSH 客户端软件（`ssh` 工具），并在远程服务器上运行 SSH 服务。
你必须能够登录到远程服务器上的 SSH 服务。


## 任务上下文  {#task-context}

{{< note >}}
此示例使用 SSH 隧道传输流量，SSH 客户端和服务器充当 SOCKS 代理。
你可以使用其他任意类型的 [SOCKS5](https://zh.wikipedia.org/wiki/SOCKS#SOCKS5) 代理代替。
{{</ note >}}

图 1 表示你将在此任务中实现的目标。

* 你有一台在后面的步骤中被称为本地计算机的客户端计算机，你将在这台计算机上创建与
  Kubernetes API 对话的请求。
* Kubernetes 服务器/API 托管在远程服务器上。
* 你将使用 SSH 客户端和服务器软件在本地和远程服务器之间创建安全的 SOCKS5 隧道。
  客户端和 Kubernetes API 之间的 HTTPS 流量将流经 SOCKS5 隧道，该隧道本身通过
  SSH 进行隧道传输。


{{< mermaid >}}
graph LR;

  subgraph local[本地客户端机器]
  client([客户端])-- 本地 <br> 流量.->  local_ssh[本地 SSH <br> SOCKS5 代理];
  end
  ocal_ssh[SSH <br>SOCKS5 <br> 代理]-- SSH 隧道 -->sshd
  
  subgraph remote[远程服务器]
  sshd[SSH <br> 服务器]-- 本地流量 -->service1;
  end
  client([客户端])-. 通过代理传递的 <br> HTTPS 流量 .->service1[Kubernetes API];

  classDef plain fill:#ddd,stroke:#fff,stroke-width:4px,color:#000;
  classDef k8s fill:#326ce5,stroke:#fff,stroke-width:4px,color:#fff;
  classDef cluster fill:#fff,stroke:#bbb,stroke-width:2px,color:#326ce5;
  class ingress,service1,service2,pod1,pod2,pod3,pod4 k8s;
  class client plain;
  class cluster cluster;
{{</ mermaid >}}
图 1. SOCKS5 教程组件

## 使用 SSH 创建 SOCKS5 代理

下面的命令在你的客户端计算机和远程 SOCKS 服务器之间启动一个 SOCKS5 代理：

```shell
# 运行此命令后，SSH 隧道继续在前台运行
ssh -D 1080 -q -N username@kubernetes-remote-server.example
```

* `-D 1080`: 在本地端口 1080 上打开一个 SOCKS 代理。
* `-q`: 静音模式。导致大多数警告和诊断消息被抑制。
* `-N`: 不执行远程命令。仅用于转发端口。
* `username@kubernetes-remote-server.example`：运行 Kubernetes 集群的远程 SSH 服务器（例如：堡垒主机）。

## 客户端配置

要通过代理访问 Kubernetes API 服务器，你必须指示 `kubectl` 通过我们之前创建的 SOCKS5
代理发送查询。
这可以通过设置适当的环境变量或通过 kubeconfig 文件中的 `proxy-url` 属性来实现。
使用环境变量：

```shell
export HTTPS_PROXY=socks5://localhost:1080
```

要始终在特定的 `kubectl` 上下文中使用此设置，请在 `~/.kube/config` 文件中为相关的
`cluster` 条目设置 `proxy-url` 属性。例如：

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LRMEMMW2 # 简化以便阅读
    # “Kubernetes API”服务器，换言之，kubernetes-remote-server.example 的 IP 地址
    server: https://<API_SERVER_IP_ADRESS>:6443
    # 上图中的“SSH SOCKS5代理”（内置 DNS 解析）
    proxy-url: socks5://localhost:1080
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    client-certificate-data: LS0tLS1CR== # 节略，为了便于阅读
    client-key-data: LS0tLS1CRUdJT=      # 节略，为了便于阅读
```

一旦你通过前面提到的 SSH 命令创建了隧道，并定义了环境变量或 `proxy-url` 属性，
你就可以通过该代理与你的集群交互。例如：

```shell
kubectl get pods
```

```console
NAMESPACE     NAME                                     READY   STATUS      RESTARTS   AGE
kube-system   coredns-85cb69466-klwq8                  1/1     Running     0          5m46s
```

{{< note >}}
- 在 `kubectl` 1.24 之前，大多数 `kubectl` 命令在使用 socks 代理时都有效，除了 `kubectl exec`。
- `kubectl` 支持读取 `HTTPS_PROXY` 和 `https_proxy` 环境变量。 这些被其他支持 SOCKS 的程序使用，例如 `curl`。
  因此在某些情况下，在命令行上定义环境变量会更好：
  ```shell
  HTTPS_PROXY=socks5://localhost:1080 kubectl get pods
  ```
- 使用 `proxy-url` 时，代理仅用于相关的 `kubectl` 上下文，而环境变量将影响所有上下文。
- 通过使用 `socks5h` 协议名称而不是上面显示的更广为人知的 `socks5` 协议，
  可以进一步保护 k8s API 服务器主机名免受 DNS 泄漏影响。
  这种情况下，`kubectl` 将要求代理服务器（例如 SSH 堡垒机）解析 k8s API 服务器域名，
  而不是在运行 `kubectl` 的系统上进行解析。
  另外还要注意，使用 `socks5h` 时，像 `https://localhost:6443/api` 这样的 k8s API 服务器 URL 并不是指你的本地客户端计算机。
  相反，它指向的是代理服务器（例如 SSH 堡垒机）上已知的 `localhost`。
{{</ note >}}

## 清理

通过在运行它的终端上按 `CTRL+C` 来停止 SSH 端口转发进程。

在终端中键入 `unset https_proxy` 以停止通过代理转发 http 流量。

## 进一步阅读

* [OpenSSH 远程登录客户端](https://man.openbsd.org/ssh)
