---
title: 运行一个单实例有状态应用
content_type: tutorial
weight: 20
---


本文介绍在 Kubernetes 中如何使用 PersistentVolume 和 Deployment 运行一个单实例有状态应用。该应用是 MySQL.

## {{% heading "objectives" %}}

* 在你的环境中创建一个引用磁盘的 PersistentVolume
* 创建一个 MySQL Deployment.
* 在集群内以一个已知的 DNS 名称将 MySQL 暴露给其他 Pod

## {{% heading "prerequisites" %}}

* {{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}
* {{< include "default-storage-class-prereqs.md" >}}


## 部署 MySQL   {#deploy-mysql}

你可以通过创建一个 Kubernetes Deployment 并使用 PersistentVolumeClaim 将其连接到
某已有的 PV 卷来运行一个有状态的应用。
例如，这里的 YAML 描述的是一个运行 MySQL 的 Deployment，其中引用了 PVC 申领。
文件为 /var/lib/mysql 定义了加载卷，并创建了一个 PVC 申领，寻找一个 20G 大小的卷。
该申领可以通过现有的满足需求的卷来满足，也可以通过动态供应卷的机制来满足。

注意：在配置的 YAML 文件中定义密码的做法是不安全的。具体安全解决方案请参考
[Kubernetes Secrets](/zh-cn/docs/concepts/configuration/secret/).

{{< codenew file="application/mysql/mysql-deployment.yaml" >}}
{{< codenew file="application/mysql/mysql-pv.yaml" >}}

1. 部署 YAML 文件中定义的 PV 和 PVC：

   ```shell
   kubectl apply -f https://k8s.io/examples/application/mysql/mysql-pv.yaml
   ```

2. 部署 YAML 文件中定义的 Deployment：

   ```shell
   kubectl apply -f https://k8s.io/examples/application/mysql/mysql-deployment.yaml
   ```

3. 展示 Deployment 相关信息:

   ```shell
   kubectl describe deployment mysql
   ```

   输出类似于：

   ```
   Name:                 mysql
   Namespace:            default
   CreationTimestamp:    Tue, 01 Nov 2016 11:18:45 -0700
   Labels:               app=mysql
   Annotations:          deployment.kubernetes.io/revision=1
   Selector:             app=mysql
   Replicas:             1 desired | 1 updated | 1 total | 0 available | 1 unavailable
   StrategyType:         Recreate
   MinReadySeconds:      0
   Pod Template:
     Labels:       app=mysql
     Containers:
      mysql:
       Image:      mysql:5.6
       Port:       3306/TCP
       Environment:
         MYSQL_ROOT_PASSWORD:      password
       Mounts:
         /var/lib/mysql from mysql-persistent-storage (rw)
     Volumes:
      mysql-persistent-storage:
       Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
       ClaimName:  mysql-pv-claim
       ReadOnly:   false
   Conditions:
     Type          Status  Reason
     ----          ------  ------
     Available     False   MinimumReplicasUnavailable
     Progressing   True    ReplicaSetUpdated
   OldReplicaSets:       <none>
   NewReplicaSet:        mysql-63082529 (1/1 replicas created)
   Events:
     FirstSeen    LastSeen    Count    From                SubobjectPath    Type        Reason            Message
     ---------    --------    -----    ----                -------------    --------    ------            -------
     33s          33s         1        {deployment-controller }             Normal      ScalingReplicaSet Scaled up replica set mysql-63082529 to 1
   ```

4. 列举出 Deployment 创建的 pods:

   ```shell
   kubectl get pods -l app=mysql
   ```

   输出类似于：

   ```
   NAME                   READY     STATUS    RESTARTS   AGE
   mysql-63082529-2z3ki   1/1       Running   0          3m
   ```

5. 查看 PersistentVolumeClaim：

   ```shell
   kubectl describe pvc mysql-pv-claim
   ```

   输出类似于：

   ```
   Name:         mysql-pv-claim
   Namespace:    default
   StorageClass:
   Status:       Bound
   Volume:       mysql-pv-volume
   Labels:       <none>
   Annotations:    pv.kubernetes.io/bind-completed=yes
                   pv.kubernetes.io/bound-by-controller=yes
   Capacity:     20Gi
   Access Modes: RWO
   Events:       <none>
   ```

## 访问 MySQL 实例   {#accessing-the-mysql-instance}

前面 YAML 文件中创建了一个允许集群内其他 Pod 访问的数据库服务。该服务中选项
`clusterIP: None` 让服务 DNS 名称直接解析为 Pod 的 IP 地址。
当在一个服务下只有一个 Pod 并且不打算增加 Pod 的数量这是最好的.

运行 MySQL 客户端以连接到服务器:

```shell
kubectl run -it --rm --image=mysql:5.6 --restart=Never mysql-client -- mysql -h mysql -ppassword
```

此命令在集群内创建一个新的 Pod 并运行 MySQL 客户端，并通过 Service 连接到服务器。
如果连接成功，你就知道有状态的 MySQL 数据库正处于运行状态。

```
Waiting for pod default/mysql-client-274442439-zyp6i to be running, status is Pending, pod ready: false
If you don't see a command prompt, try pressing enter.

mysql>
```

## 更新   {#updating}

Deployment 中镜像或其他部分同往常一样可以通过 `kubectl apply` 命令更新。
以下是特定于有状态应用的一些注意事项:

* 不要对应用进行规模扩缩。这里的设置仅适用于单实例应用。下层的 PersistentVolume
  仅只能挂载到一个 Pod 上。对于集群级有状态应用，请参考
  [StatefulSet 文档](/zh-cn/docs/concepts/workloads/controllers/statefulset/).
* 在 Deployment 的 YAML 文件中使用 `strategy:` `type: Recreate`。
  该选项指示 Kubernetes _不_ 使用滚动升级。滚动升级无法工作，因为这里一次不能
  运行多个 Pod。在使用更新的配置文件创建新的 Pod 前，`Recreate` 策略将
  保证先停止第一个 Pod。

## 删除 Deployment    {#deleting-a-deployment}

通过名称删除部署的对象:

```shell
kubectl delete deployment,svc mysql
kubectl delete pvc mysql-pv-claim
kubectl delete pv mysql-pv-volume
```

如果通过手动的方式供应 PersistentVolume, 那么也需要手动删除它以释放下层资源。
如果是用动态供应方式创建的 PersistentVolume，在删除 PersistentVolumeClaim 后
PersistentVolume 将被自动删除。
一些存储服务（比如 EBS 和 PD）也会在 PersistentVolume 被删除时自动回收下层资源。

## {{% heading "whatsnext" %}}

* 欲进一步了解 Deployment 对象，请参考 [Deployment 对象](/zh-cn/docs/concepts/workloads/controllers/deployment/)
* 进一步了解[部署应用](/zh-cn/docs/tasks/run-application/run-stateless-application-deployment/)

* 参阅 [kubectl run 文档](/docs/reference/generated/kubectl/kubectl-commands/#run)

* 参阅[卷](/zh-cn/docs/concepts/storage/volumes/)和[持久卷](/zh-cn/docs/concepts/storage/persistent-volumes/)
