---
title: 示例：使用持久卷部署 WordPress 和 MySQL
content_type: tutorial
weight: 20
card:
  name: tutorials
  weight: 40
  title: "有状态应用示例: 带持久卷的 Wordpress"
---

本示例描述了如何通过 Minikube 在 Kubernetes 上安装 WordPress 和 MySQL。
这两个应用都使用 PersistentVolumes 和 PersistentVolumeClaims 保存数据。

[PersistentVolume](/zh-cn/docs/concepts/storage/persistent-volumes/)（PV）是在集群里由管理员手动制备或
Kubernetes 通过 [StorageClass](/zh-cn/docs/concepts/storage/storage-classes) 动态制备的一块存储。
[PersistentVolumeClaim](/zh-cn/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)
是用户对存储的请求，该请求可由某个 PV 来满足。
PersistentVolumes 和 PersistentVolumeClaims 独立于 Pod 生命周期而存在，
在 Pod 重启、重新调度甚至删除过程中用于保存数据。

{{< warning >}}
这种部署并不适合生产场景，因为它使用的是单实例 WordPress 和 MySQL Pod。
在生产场景中，请考虑使用 [WordPress Helm Chart](https://github.com/bitnami/charts/tree/master/bitnami/wordpress)
部署 WordPress。
{{< /warning >}}

{{< note >}}
本教程中提供的文件使用 GA Deployment API，并且特定于 kubernetes 1.9 或更高版本。
如果你希望将本教程与 Kubernetes 的早期版本一起使用，请相应地更新 API 版本，或参考本教程的早期版本。
{{< /note >}}

## {{% heading "objectives" %}}

* 创建 PersistentVolumeClaims 和 PersistentVolumes
* 创建 `kustomization.yaml` 以使用
  * Secret 生成器
  * MySQL 资源配置
  * WordPress 资源配置
* `kubectl apply -k ./` 来应用整个 kustomization 目录
* 清理

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

此例在 `kubectl` 1.27 或者更高版本有效。

下载下面的配置文件：

1. [mysql-deployment.yaml](/examples/application/wordpress/mysql-deployment.yaml)

2. [wordpress-deployment.yaml](/examples/application/wordpress/wordpress-deployment.yaml)


## 创建 PersistentVolumeClaims 和 PersistentVolumes

MySQL 和 Wordpress 都需要一个 PersistentVolume 来存储数据。
它们的 PersistentVolumeClaims 将在部署步骤中创建。

许多集群环境都安装了默认的 StorageClass。如果在 PersistentVolumeClaim 中未指定 StorageClass，
则使用集群的默认 StorageClass。

创建 PersistentVolumeClaim 时，将根据 StorageClass 配置动态制备一个 PersistentVolume。

{{< warning >}}
在本地集群中，默认的 StorageClass 使用 `hostPath` 制备程序。`hostPath` 卷仅适用于开发和测试。
使用 `hostPath` 卷时，你的数据位于 Pod 调度到的节点上的 `/tmp` 中，并且不会在节点之间移动。
如果 Pod 死亡并被调度到集群中的另一个节点，或者该节点重新启动，则数据将丢失。
{{< /warning >}}

{{< note >}}
如果要建立需要使用 `hostPath` 制备程序的集群，
则必须在 `controller-manager` 组件中设置 `--enable-hostpath-provisioner` 标志。
{{< /note >}}

{{< note >}}
如果你已经有运行在 Google Kubernetes Engine 的集群，
请参考[此指南](https://cloud.google.com/kubernetes-engine/docs/tutorials/persistent-disk)。
{{< /note >}}

## 创建 kustomization.yaml

### 创建 Secret 生成器

[Secret](/zh-cn/docs/concepts/configuration/secret/) 是存储诸如密码或密钥之类敏感数据的对象。
从 1.14 开始，`kubectl` 支持使用一个 kustomization 文件来管理 Kubernetes 对象。
你可以通过 `kustomization.yaml` 中的生成器创建一个 Secret。

通过以下命令在 `kustomization.yaml` 中添加一个 Secret 生成器。
你需要将 `YOUR_PASSWORD` 替换为自己要用的密码。

```shell
cat <<EOF >./kustomization.yaml
secretGenerator:
- name: mysql-pass
  literals:
  - password=YOUR_PASSWORD
EOF
```

## 补充 MySQL 和 WordPress 的资源配置

以下清单文件描述的是一个单实例的 MySQL Deployment。MySQL 容器将 PersistentVolume 挂载在 `/var/lib/mysql`。
`MYSQL_ROOT_PASSWORD` 环境变量根据 Secret 设置数据库密码。

{{< codenew file="application/wordpress/mysql-deployment.yaml" >}}

以下清单文件描述的是一个单实例 WordPress Deployment。WordPress 容器将 PersistentVolume
挂载到 `/var/www/html`，用于保存网站数据文件。
`WORDPRESS_DB_HOST` 环境变量设置上面定义的 MySQL Service 的名称，WordPress 将通过 Service 访问数据库。
`WORDPRESS_DB_PASSWORD` 环境变量根据使用 kustomize 生成的 Secret 设置数据库密码。

{{< codenew file="application/wordpress/wordpress-deployment.yaml" >}}

1. 下载 MySQL Deployment 配置文件。

   ```shell
   curl -LO https://k8s.io/examples/application/wordpress/mysql-deployment.yaml
   ```

2. 下载 WordPress 配置文件。

   ```shell
   curl -LO https://k8s.io/examples/application/wordpress/wordpress-deployment.yaml
   ```

3. 将上述内容追加到 `kustomization.yaml` 文件。

   ```shell
   cat <<EOF >>./kustomization.yaml
   resources:
     - mysql-deployment.yaml
     - wordpress-deployment.yaml
   EOF
   ```

## 应用和验证

`kustomization.yaml` 包含用于部署 WordPress 网站以及 MySQL 数据库的所有资源。你可以通过以下方式应用目录：

```shell
kubectl apply -k ./
```

现在，你可以验证所有对象是否存在。

1. 通过运行以下命令验证 Secret 是否存在：

   ```shell
   kubectl get secrets
   ```


   响应应如下所示：

   ```
   NAME                    TYPE                                  DATA   AGE
   mysql-pass-c57bb4t7mf   Opaque                                1      9s
   ```

2. 验证是否已动态制备 PersistentVolume：

   ```shell
   kubectl get pvc
   ```

   {{< note >}}

   制备和绑定 PV 可能要花费几分钟。
   {{< /note >}}


   响应应如下所示：

   ```
   NAME             STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS       AGE
   mysql-pv-claim   Bound     pvc-8cbd7b2e-4044-11e9-b2bb-42010a800002   20Gi       RWO            standard           77s
   wp-pv-claim      Bound     pvc-8cd0df54-4044-11e9-b2bb-42010a800002   20Gi       RWO            standard           77s
   ```

3. 通过运行以下命令来验证 Pod 是否正在运行：

   ```shell
   kubectl get pods
   ```

   {{< note >}}

   等待 Pod 状态变成 `RUNNING` 可能会花费几分钟。
   {{< /note >}}


   响应应如下所示：

   ```
   NAME                               READY     STATUS    RESTARTS   AGE
   wordpress-mysql-1894417608-x5dzt   1/1       Running   0          40s
   ```

4. 通过运行以下命令来验证 Service 是否正在运行：

   ```shell
   kubectl get services wordpress
   ```


   响应应如下所示：

   ```
   NAME        TYPE            CLUSTER-IP   EXTERNAL-IP   PORT(S)        AGE
   wordpress   LoadBalancer    10.0.0.89    <pending>     80:32406/TCP   4m
   ```

   {{< note >}}

   Minikube 只能通过 NodePort 公开服务。EXTERNAL-IP 始终处于 pending 状态。
   {{< /note >}}

5. 运行以下命令以获取 WordPress 服务的 IP 地址：

   ```shell
   minikube service wordpress --url
   ```

   响应应如下所示：

   ```
   http://1.2.3.4:32406
   ```

6. 复制 IP 地址，然后将页面加载到浏览器中来查看你的站点。

   你应该看到类似于以下屏幕截图的 WordPress 设置页面。

   ![wordpress-init](https://raw.githubusercontent.com/kubernetes/examples/master/mysql-wordpress-pd/WordPress.png)

   {{< warning >}}
   不要在此页面上保留 WordPress 安装。如果其他用户找到了它，他们可以在你的实例上建立一个网站并使用它来提供恶意内容。<br/><br/>
   通过创建用户名和密码来安装 WordPress 或删除你的实例。
   {{< /warning >}}

## {{% heading "cleanup" %}}

1. 运行以下命令删除你的 Secret、Deployment、Service 和 PersistentVolumeClaims：

   ```shell
   kubectl delete -k ./
   ```

## {{% heading "whatsnext" %}}

* 进一步了解[自省与调试](/zh-cn/docs/tasks/debug/debug-application/debug-running-pod/)
* 进一步了解 [Job](/zh-cn/docs/concepts/workloads/controllers/job/)
* 进一步了解[端口转发](/zh-cn/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)
* 了解如何[获得容器的 Shell](/zh-cn/docs/tasks/debug/debug-application/get-shell-running-container/)
