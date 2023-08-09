---
title: 使用 Secret 安全地分发凭证
content_type: task
weight: 50
min-kubernetes-server-version: v1.6
---

本文展示如何安全地将敏感数据（如密码和加密密钥）注入到 Pod 中。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

### 将 Secret 数据转换为 base-64 形式   {#convert-your-secret-data-to-a-base64-representation}

假设用户想要有两条 Secret 数据：用户名 `my-app` 和密码 `39528$vdg7Jb`。
首先使用 [Base64 编码](https://www.base64encode.org/)将用户名和密码转化为 base-64 形式。
下面是一个使用常用的 base64 程序的示例：

```shell
echo -n 'my-app' | base64
echo -n '39528$vdg7Jb' | base64
```

结果显示 base-64 形式的用户名为 `bXktYXBw`，
base-64 形式的密码为 `Mzk1MjgkdmRnN0pi`。

{{< caution >}}
使用你的操作系统所能信任的本地工具以降低使用外部工具的风险。
{{< /caution >}}


## 创建 Secret   {#create-a-secret}

这里是一个配置文件，可以用来创建存有用户名和密码的 Secret：

{{< codenew file="pods/inject/secret.yaml" >}}

1. 创建 Secret：

   ```shell
   kubectl apply -f https://k8s.io/examples/pods/inject/secret.yaml
   ```

2. 查看 Secret 相关信息：

   ```shell
   kubectl get secret test-secret
   ```

   输出：

   ```
   NAME          TYPE      DATA      AGE
   test-secret   Opaque    2         1m
   ```

3. 查看 Secret 相关的更多详细信息：

   ```shell
   kubectl describe secret test-secret
   ```

   输出：

   ```
   Name:       test-secret
   Namespace:  default
   Labels:     <none>
   Annotations:    <none>

   Type:   Opaque

   Data
   ====
   password:   13 bytes
   username:   7 bytes
   ```

### 直接用 kubectl 创建 Secret   {#create-a-secret-directly-with-kubectl}

如果你希望略过 Base64 编码的步骤，你也可以使用 `kubectl create secret`
命令直接创建 Secret。例如：

```shell
kubectl create secret generic test-secret --from-literal='username=my-app' --from-literal='password=39528$vdg7Jb'
```

这是一种更为方便的方法。
前面展示的详细分解步骤有助于了解究竟发生了什么事情。

## 创建一个可以通过卷访问 Secret 数据的 Pod   {#create-a-pod-that-has-access-to-the-secret-data-through-a-volume}

这里是一个可以用来创建 Pod 的配置文件：

{{< codenew file="pods/inject/secret-pod.yaml" >}}

   创建 Pod：

   ```shell
   kubectl apply -f https://k8s.io/examples/pods/inject/secret-pod.yaml
   ```

   确认 Pod 正在运行：

   ```shell
   kubectl get pod secret-test-pod
   ```

   输出：

   ```
   NAME              READY     STATUS    RESTARTS   AGE
   secret-test-pod   1/1       Running   0          42m
   ```

   获取一个 Shell 进入 Pod 中运行的容器：

   ```shell
   kubectl exec -i -t secret-test-pod -- /bin/bash
   ```

   Secret 数据通过挂载在 `/etc/secret-volume` 目录下的卷暴露在容器中。

   在 Shell 中，列举 `/etc/secret-volume` 目录下的文件：

   ```shell
   # 在容器中 Shell 运行下面命令
   ls /etc/secret-volume
   ```

   输出包含两个文件，每个对应一个 Secret 数据条目：

   ```
   password username
   ```

   在 Shell 中，显示 `username` 和 `password` 文件的内容：

   ```shell
   # 在容器中 Shell 运行下面命令
   echo "$( cat /etc/secret-volume/username )"
   echo "$( cat /etc/secret-volume/password )"
   ```

   输出为用户名和密码：

   ```
   my-app
   39528$vdg7Jb
   ```
修改你的镜像或命令行，使程序在 `mountPath` 目录下查找文件。
Secret `data` 映射中的每个键都成为该目录中的文件名。

### 映射 Secret 键到特定文件路径    {#project-secret-keys-to-specific-file-paths}

你还可以控制卷内 Secret 键的映射路径。
使用 `.spec.volumes[].secret.items` 字段来改变每个键的目标路径。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/foo"
      readOnly: true
  volumes:
  - name: foo
    secret:
      secretName: mysecret
      items:
      - key: username
        path: my-group/my-username
```

当你部署此 Pod 时，会发生以下情况：

- 来自 `mysecret` 的键 `username` 可以在路径 `/etc/foo/my-group/my-username`
  下供容器使用，而不是路径 `/etc/foo/username`。
- 来自该 Secret 的键 `password` 没有映射到任何路径。


如果你使用 `.spec.volumes[].secret.items` 明确地列出键，请考虑以下事项：

- 只有在 `items` 字段中指定的键才会被映射。
- 要使用 Secret 中全部的键，那么全部的键都必须列在 `items` 字段中。
- 所有列出的键必须存在于相应的 Secret 中。否则，该卷不被创建。

### 为 Secret 键设置 POSIX 权限

你可以为单个 Secret 键设置 POSIX 文件访问权限位。
如果不指定任何权限，默认情况下使用 `0644`。
你也可以为整个 Secret 卷设置默认的 POSIX 文件模式，需要时你可以重写单个键的权限。

例如，可以像这样指定默认模式：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/foo"
  volumes:
  - name: foo
    secret:
      secretName: mysecret
      defaultMode: 0400
```

Secret 被挂载在 `/etc/foo` 目录下；所有由 Secret 卷挂载创建的文件的访问许可都是 `0400`。

{{< note >}}
如果使用 JSON 定义 Pod 或 Pod 模板，请注意 JSON 规范不支持数字的八进制形式，
因为 JSON 将 `0400` 视为**十进制**的值 `400`。
在 JSON 中，要改为使用十进制的 `defaultMode`。
如果你正在编写 YAML，则可以用八进制编写 `defaultMode`。
{{< /note >}}

## 使用 Secret 数据定义容器变量   {#define-container-env-var-using-secret-data}

在你的容器中，你可以以环境变量的方式使用 Secret 中的数据。

如果容器已经使用了在环境变量中的 Secret，除非容器重新启动，否则容器将无法感知到 Secret 的更新。
有第三方解决方案可以在 Secret 改变时触发容器重启。


### 使用来自 Secret 中的数据定义容器变量   {#define-a-container-env-var-with-data-from-a-single-secret}

- 定义环境变量为 Secret 中的键值偶对：

  ```shell
  kubectl create secret generic backend-user --from-literal=backend-username='backend-admin'
  ```

- 在 Pod 规约中，将 Secret 中定义的值 `backend-username` 赋给 `SECRET_USERNAME` 环境变量。

  {{< codenew file="pods/inject/pod-single-secret-env-variable.yaml" >}}

- 创建 Pod：

  ```shell
  kubectl create -f https://k8s.io/examples/pods/inject/pod-single-secret-env-variable.yaml
  ```

- 在 Shell 中，显示容器环境变量 `SECRET_USERNAME` 的内容：

  ```shell
  kubectl exec -i -t env-single-secret -- /bin/sh -c 'echo $SECRET_USERNAME'
   ```

  输出为：
  ```
  backend-admin
  ```

### 使用来自多个 Secret 的数据定义环境变量   {#define-container-env-var-with-data-from-multi-secrets}

- 和前面的例子一样，先创建 Secret：

  ```shell
  kubectl create secret generic backend-user --from-literal=backend-username='backend-admin'
  kubectl create secret generic db-user --from-literal=db-username='db-admin'
  ```

- 在 Pod 规约中定义环境变量：

  {{< codenew file="pods/inject/pod-multiple-secret-env-variable.yaml" >}}

- 创建 Pod：

  ```shell
  kubectl create -f https://k8s.io/examples/pods/inject/pod-multiple-secret-env-variable.yaml
  ```

- 在你的 Shell 中，显示容器环境变量的内容：

  ```shell
  kubectl exec -i -t envvars-multiple-secrets -- /bin/sh -c 'env | grep _USERNAME'
  ```
  输出：
  ```
  DB_USERNAME=db-admin
  BACKEND_USERNAME=backend-admin
  ```

## 将 Secret 中的所有键值偶对定义为环境变量   {#configure-all-key-value-pairs-in-a-secret-as-container-env-var}

{{< note >}}
此功能在 Kubernetes 1.6 版本之后可用。
{{< /note >}}

- 创建包含多个键值偶对的 Secret：

  ```shell
  kubectl create secret generic test-secret --from-literal=username='my-app' --from-literal=password='39528$vdg7Jb'
  ```

- 使用 `envFrom` 来将 Secret 中的所有数据定义为环境变量。
  Secret 中的键名成为容器中的环境变量名：

  {{< codenew file="pods/inject/pod-secret-envFrom.yaml" >}}

- 创建 Pod：

  ```shell
  kubectl create -f https://k8s.io/examples/pods/inject/pod-secret-envFrom.yaml
  ```

- 在 Shell 中，显示环境变量 `username` 和 `password` 的内容：

  ```shell
  kubectl exec -i -t envfrom-secret -- /bin/sh -c 'echo "username: $username\npassword: $password\n"'
  ```
  
  输出为：

  ```
  username: my-app
  password: 39528$vdg7Jb
  ```

### 参考   {#references}

- [Secret](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#secret-v1-core)
- [Volume](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#volume-v1-core)
- [Pod](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#pod-v1-core)

## {{% heading "whatsnext" %}}

- 进一步了解 [Secret](/zh-cn/docs/concepts/configuration/secret/)。
- 了解[卷](/zh-cn/docs/concepts/storage/volumes/)。
