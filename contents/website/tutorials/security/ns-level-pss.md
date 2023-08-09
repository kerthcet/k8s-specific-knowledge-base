---
title: 在名字空间级别应用 Pod 安全标准
content_type: tutorial
weight: 20
---


{{% alert title="Note" %}}
本教程仅适用于新集群。
{{% /alert %}}

Pod 安全准入（PSA）在 v1.23 及更高版本默认启用，
因为它[升级到测试版（beta）](/blog/2021/12/09/pod-security-admission-beta/)。
Pod 安全准入是在创建 Pod 时应用
[Pod 安全标准](/zh-cn/docs/concepts/security/pod-security-standards/)的准入控制器。
在本教程中，你将应用 `baseline` Pod 安全标准，每次一个名字空间。

你还可以在集群级别一次将 Pod 安全标准应用于多个名称空间。
有关说明，请参阅[在集群级别应用 Pod 安全标准](/zh-cn/docs/tutorials/security/cluster-level-pss/)。

## {{% heading "prerequisites" %}}

在你的工作站中安装以下内容：

- [KinD](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- [kubectl](/zh-cn/docs/tasks/tools/)

## 创建集群  {#create-cluster}

2. 按照如下方式创建一个 `KinD` 集群：

   ```shell
   kind create cluster --name psa-ns-level
   ```

   输出类似于：

   ```
   Creating cluster "psa-ns-level" ...
    ✓ Ensuring node image (kindest/node:v{{< skew currentPatchVersion >}}) 🖼 
    ✓ Preparing nodes 📦  
    ✓ Writing configuration 📜 
    ✓ Starting control-plane 🕹️ 
    ✓ Installing CNI 🔌 
    ✓ Installing StorageClass 💾 
   Set kubectl context to "kind-psa-ns-level"
   You can now use your cluster with:

   kubectl cluster-info --context kind-psa-ns-level

   Not sure what to do next? 😅  Check out https://kind.sigs.k8s.io/docs/user/quick-start/
   ```

1. 将 kubectl 上下文设置为新集群：

   ```shell
   kubectl cluster-info --context kind-psa-ns-level
   ```

   输出类似于：

   ```
   Kubernetes control plane is running at https://127.0.0.1:50996
   CoreDNS is running at https://127.0.0.1:50996/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

   To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
   ```

## 创建名字空间  {#create-a-namespace}

创建一个名为 `example` 的新名字空间：

```shell
kubectl create ns example
```

输出类似于：

```
namespace/example created
```

## 为该命名空间启用 Pod 安全标准检查  {#enable-pod-security-standards-checking-for-that-namespace}

1. 使用内置 Pod 安全准入所支持的标签在此名字空间上启用 Pod 安全标准。
   在这一步中，我们将根据最新版本（默认值）对基线 Pod 安全标准发出警告。

   ```shell
   kubectl label --overwrite ns example \
      pod-security.kubernetes.io/warn=baseline \
      pod-security.kubernetes.io/warn-version=latest
   ```

1. 你可以使用标签在任何名字空间上配置多个 Pod 安全标准检查。
   以下命令将强制（`enforce`） 执行基线（`baseline`）Pod 安全标准，
   但根据最新版本（默认值）对受限（`restricted`）Pod 安全标准执行警告（`warn`）和审核（`audit`）。

   ```shell
   kubectl label --overwrite ns example \
     pod-security.kubernetes.io/enforce=baseline \
     pod-security.kubernetes.io/enforce-version=latest \
     pod-security.kubernetes.io/warn=restricted \
     pod-security.kubernetes.io/warn-version=latest \
     pod-security.kubernetes.io/audit=restricted \
     pod-security.kubernetes.io/audit-version=latest
   ```

## 验证 Pod 安全标准  {#verify-the-pod-security-standards}

1. 在 `example` 名字空间中创建一个基线 Pod：

   ```shell
   kubectl apply -n example -f https://k8s.io/examples/security/example-baseline-pod.yaml
   ```
   Pod 确实启动正常；输出包括一条警告信息。例如：

   ```
   Warning: would violate PodSecurity "restricted:latest": allowPrivilegeEscalation != false (container "nginx" must set securityContext.allowPrivilegeEscalation=false), unrestricted capabilities (container "nginx" must set securityContext.capabilities.drop=["ALL"]), runAsNonRoot != true (pod or container "nginx" must set securityContext.runAsNonRoot=true), seccompProfile (pod or container "nginx" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
   pod/nginx created
   ```

1. 在 `default` 名字空间中创建一个基线 Pod：

   ```shell
   kubectl apply -n default -f https://k8s.io/examples/security/example-baseline-pod.yaml
   ```

   输出类似于：

   ```
   pod/nginx created
   ```

Pod 安全标准实施和警告设置仅被应用到 `example` 名字空间。
以上 Pod 安全标准仅被应用到 `example` 名字空间。
你可以在没有警告的情况下在 `default` 名字空间中创建相同的 Pod。

## 清理  {#clean-up}

现在通过运行以下命令删除你上面创建的集群：

```shell
kind delete cluster --name psa-ns-level
```

## {{% heading "whatsnext" %}}

- 运行一个 [shell 脚本](/examples/security/kind-with-namespace-level-baseline-pod-security.sh)
  一次执行所有前面的步骤。

   1. 创建 KinD 集群
   2. 创建新的名字空间
   3. 在 `enforce` 模式下应用 `baseline` Pod 安全标准，
      同时在 `warn` 和 `audit` 模式下应用 `restricted` Pod 安全标准。
   4. 创建一个应用以下 Pod 安全标准的新 Pod

- [Pod 安全准入](/zh-cn/docs/concepts/security/pod-security-admission/)
- [Pod 安全标准](/zh-cn/docs/concepts/security/pod-security-standards/)
- [在集群级别应用 Pod 安全标准](/zh-cn/docs/tutorials/security/cluster-level-pss/)
