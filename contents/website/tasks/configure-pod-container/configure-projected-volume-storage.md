---
title: 配置 Pod 使用投射卷作存储
content_type: task
weight: 100
---



本文介绍怎样通过[`projected`](/zh-cn/docs/concepts/storage/volumes/#projected) 卷将现有的多个卷资源挂载到相同的目录。
当前，`secret`、`configMap`、`downwardAPI` 和 `serviceAccountToken` 卷可以被投射。

{{< note >}}
`serviceAccountToken` 不是一种卷类型
{{< /note >}}

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}



## 为 Pod 配置投射卷

本练习中，你将使用本地文件来创建用户名和密码 {{< glossary_tooltip text="Secret" term_id="secret" >}}，
然后创建运行一个容器的 Pod，
该 Pod 使用[`projected`](/zh-cn/docs/concepts/storage/volumes/#projected) 卷将 Secret 挂载到相同的路径下。

下面是 Pod 的配置文件：

{{< codenew file="pods/storage/projected.yaml" >}}

   创建 Secret:

   ```shell
   # 创建包含用户名和密码的文件:
   echo -n "admin" > ./username.txt
   echo -n "1f2d1e2e67df" > ./password.txt

   # 在 Secret 中引用上述文件
   kubectl create secret generic user --from-file=./username.txt
   kubectl create secret generic pass --from-file=./password.txt
   ```

   创建 Pod：

   ```shell
   kubectl apply -f https://k8s.io/examples/pods/storage/projected.yaml
   ```

   确认 Pod 中的容器运行正常，然后监视 Pod 的变化：

   ```shell
   kubectl get --watch pod test-projected-volume
   ```

   输出结果和下面类似：

   ```
   NAME                    READY     STATUS    RESTARTS   AGE
   test-projected-volume   1/1       Running   0          14s
   ```

   在另外一个终端中，打开容器的 shell：

   ```shell
   kubectl exec -it test-projected-volume -- /bin/sh
   ```

   在 shell 中，确认 `projected-volume` 目录包含你的投射源：

   ```shell
   ls /projected-volume/
   ```
## 清理

删除 Pod 和 Secret:

```shell
kubectl delete pod test-projected-volume
kubectl delete secret user pass
```

## {{% heading "whatsnext" %}}


* 进一步了解[`projected`](/zh-cn/docs/concepts/storage/volumes/#projected) 卷。
* 阅读[一体卷](https://git.k8s.io/design-proposals-archive/node/all-in-one-volume.md)设计文档。
