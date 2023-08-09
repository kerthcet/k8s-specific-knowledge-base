---
title: 使用 ConfigMap 来配置 Redis
content_type: tutorial
---


这篇文档基于[配置 Pod 以使用 ConfigMap](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/)
这个任务，提供了一个使用 ConfigMap 来配置 Redis 的真实案例。



## {{% heading "objectives" %}}



* 使用 Redis 配置的值创建一个 ConfigMap
* 创建一个 Redis Pod，挂载并使用创建的 ConfigMap
* 验证配置已经被正确应用





## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

* 此页面上显示的示例适用于 `kubectl` 1.14 及以上的版本。
* 理解[配置 Pod 以使用 ConfigMap](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/)。





## 真实世界的案例：使用 ConfigMap 来配置 Redis    {#real-world-example-configuring-redis-using-a-configmap}

按照下面的步骤，使用 ConfigMap 中的数据来配置 Redis 缓存。

首先创建一个配置模块为空的 ConfigMap：

```shell
cat <<EOF >./example-redis-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: example-redis-config
data:
  redis-config: ""
EOF
```

应用上面创建的 ConfigMap 以及 Redis pod 清单：

```shell
kubectl apply -f example-redis-config.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/website/main/content/en/examples/pods/config/redis-pod.yaml
```

检查 Redis pod 清单的内容，并注意以下几点：

* 由 `spec.volumes[1]` 创建一个名为 `config` 的卷。
* `spec.volumes[1].items[0]` 下的 `key` 和 `path` 会将来自 `example-redis-config`
  ConfigMap 中的 `redis-config` 密钥公开在 `config` 卷上一个名为 `redis.conf` 的文件中。
* 然后 `config` 卷被 `spec.containers[0].volumeMounts[1]` 挂载在 `/redis-master`。

这样做的最终效果是将上面 `example-redis-config` 配置中 `data.redis-config`
的数据作为 Pod 中的 `/redis-master/redis.conf` 公开。

{{< codenew file="pods/config/redis-pod.yaml" >}}

检查创建的对象：

```shell
kubectl get pod/redis configmap/example-redis-config 
```

你应该可以看到以下输出：

```
NAME        READY   STATUS    RESTARTS   AGE
pod/redis   1/1     Running   0          8s

NAME                             DATA   AGE
configmap/example-redis-config   1      14s
```

回顾一下，我们在 `example-redis-config` ConfigMap 保留了空的 `redis-config` 键：

```shell
kubectl describe configmap/example-redis-config
```

你应该可以看到一个空的 `redis-config` 键：

```shell
Name:         example-redis-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
redis-config:
```

使用 `kubectl exec` 进入 pod，运行 `redis-cli` 工具检查当前配置：

```shell
kubectl exec -it redis -- redis-cli
```

查看 `maxmemory`：

```shell
127.0.0.1:6379> CONFIG GET maxmemory
```

它应该显示默认值 0：

```shell
1) "maxmemory"
2) "0"
```

同样，查看 `maxmemory-policy`：

```shell
127.0.0.1:6379> CONFIG GET maxmemory-policy
```

它也应该显示默认值 `noeviction`：

```shell
1) "maxmemory-policy"
2) "noeviction"
```

现在，向 `example-redis-config` ConfigMap 添加一些配置：

{{< codenew file="pods/config/example-redis-config.yaml" >}}

应用更新的 ConfigMap:

```shell
kubectl apply -f example-redis-config.yaml
```

确认 ConfigMap 已更新：

```shell
kubectl describe configmap/example-redis-config
```

你应该可以看到我们刚刚添加的配置：

```shell
Name:         example-redis-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
redis-config:
----
maxmemory 2mb
maxmemory-policy allkeys-lru
```

通过 `kubectl exec` 使用 `redis-cli` 再次检查 Redis Pod，查看是否已应用配置：

```shell
kubectl exec -it redis -- redis-cli
```

查看 `maxmemory`：

```shell
127.0.0.1:6379> CONFIG GET maxmemory
```

它保持默认值 0：

```shell
1) "maxmemory"
2) "0"
```

同样，`maxmemory-policy` 保留为默认设置 `noeviction`：

```shell
127.0.0.1:6379> CONFIG GET maxmemory-policy
```

返回：

```shell
1) "maxmemory-policy"
2) "noeviction"
```

配置值未更改，因为需要重新启动 Pod 才能从关联的 ConfigMap 中获取更新的值。
让我们删除并重新创建 Pod：

```shell
kubectl delete pod redis
kubectl apply -f https://raw.githubusercontent.com/kubernetes/website/main/content/en/examples/pods/config/redis-pod.yaml
```

现在，最后一次重新检查配置值：

```shell
kubectl exec -it redis -- redis-cli
```

查看 `maxmemory`：

```shell
127.0.0.1:6379> CONFIG GET maxmemory
```

现在，它应该返回更新后的值 2097152：

```shell
1) "maxmemory"
2) "2097152"
```

同样，`maxmemory-policy` 也已更新：

```shell
127.0.0.1:6379> CONFIG GET maxmemory-policy
```

现在它反映了期望值 `allkeys-lru`：

```shell
1) "maxmemory-policy"
2) "allkeys-lru"
```

删除创建的资源，清理你的工作：

```shell
kubectl delete pod/redis configmap/example-redis-config
```

## {{% heading "whatsnext" %}}


* 了解有关 [ConfigMaps](/zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/) 的更多信息。



