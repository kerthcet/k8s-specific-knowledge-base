---
title: 用节点亲和性把 Pod 分配到节点
min-kubernetes-server-version: v1.10
content_type: task
weight: 160
---

本页展示在 Kubernetes 集群中，如何使用节点亲和性把 Kubernetes Pod 分配到特定节点。

## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}




## 给节点添加标签

1. 列出集群中的节点及其标签：

    ```shell
    kubectl get nodes --show-labels
    ```
    

    输出类似于此：

    ```
    NAME      STATUS    ROLES    AGE     VERSION        LABELS
    worker0   Ready     <none>   1d      v1.13.0        ...,kubernetes.io/hostname=worker0
    worker1   Ready     <none>   1d      v1.13.0        ...,kubernetes.io/hostname=worker1
    worker2   Ready     <none>   1d      v1.13.0        ...,kubernetes.io/hostname=worker2
    ```

2. 选择一个节点，给它添加一个标签：

    ```shell
    kubectl label nodes <your-node-name> disktype=ssd
    ```


    其中 `<your-node-name>` 是你所选节点的名称。

3. 验证你所选节点具有 `disktype=ssd` 标签：

    ```shell
    kubectl get nodes --show-labels
    ```


    输出类似于此：

    ```
    NAME      STATUS    ROLES    AGE     VERSION        LABELS
    worker0   Ready     <none>   1d      v1.13.0        ...,disktype=ssd,kubernetes.io/hostname=worker0
    worker1   Ready     <none>   1d      v1.13.0        ...,kubernetes.io/hostname=worker1
    worker2   Ready     <none>   1d      v1.13.0        ...,kubernetes.io/hostname=worker2
    ```


    在前面的输出中，可以看到 `worker0` 节点有一个 `disktype=ssd` 标签。

## 依据强制的节点亲和性调度 Pod  {#schedule-a-Pod-using-required-node-affinity}

下面清单描述了一个 Pod，它有一个节点亲和性配置 `requiredDuringSchedulingIgnoredDuringExecution`，`disktype=ssd`。
这意味着 pod 只会被调度到具有 `disktype=ssd` 标签的节点上。

{{< codenew file="pods/pod-nginx-required-affinity.yaml" >}}

1. 执行（Apply）此清单来创建一个调度到所选节点上的 Pod：

    ```shell
    kubectl apply -f https://k8s.io/examples/pods/pod-nginx-required-affinity.yaml
    ```

2. 验证 Pod 已经在所选节点上运行：

    ```shell
    kubectl get pods --output=wide
    ```


    输出类似于此：

    ```
    NAME     READY     STATUS    RESTARTS   AGE    IP           NODE
    nginx    1/1       Running   0          13s    10.200.0.4   worker0
    ```
    
## 使用首选的节点亲和性调度 Pod {#schedule-a-Pod-using-preferred-node-affinity}

本清单描述了一个 Pod，它有一个节点亲和性设置 `preferredDuringSchedulingIgnoredDuringExecution`，`disktype: ssd`。
这意味着 Pod 将首选具有 `disktype=ssd` 标签的节点。

{{< codenew file="pods/pod-nginx-preferred-affinity.yaml" >}}

1. 执行此清单创建一个会调度到所选节点上的 Pod：
    
    ```shell
    kubectl apply -f https://k8s.io/examples/pods/pod-nginx-preferred-affinity.yaml
    ```

2. 验证 Pod 是否在所选节点上运行：
   
    ```shell
    kubectl get pods --output=wide
    ```


    输出类似于此：
    
    ```
    NAME     READY     STATUS    RESTARTS   AGE    IP           NODE
    nginx    1/1       Running   0          13s    10.200.0.4   worker0
    ```



## {{% heading "whatsnext" %}}

进一步了解[节点亲和性](/zh-cn/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity)。
