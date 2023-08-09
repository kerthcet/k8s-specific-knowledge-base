---
title: 探索 Pod 及其端点的终止行为
content_type: tutorial
weight: 60
---


一旦你参照[使用 Service 连接到应用](/zh-cn/docs/tutorials/services/connect-applications-service/)中概述的那些步骤使用
Service 连接到了你的应用，你就有了一个持续运行的多副本应用暴露在了网络上。
本教程帮助你了解 Pod 的终止流程，探索实现连接排空的几种方式。


## Pod 及其端点的终止过程   {#termination-process-for-pods-and-endpoints}

你经常会遇到需要终止 Pod 的场景，例如为了升级或缩容。
为了改良应用的可用性，实现一种合适的活跃连接排空机制变得重要。

本教程将通过使用一个简单的 nginx Web 服务器演示此概念，
解释 Pod 终止的流程及其与相应端点状态和移除的联系。


## 端点终止的示例流程   {#example-flow-with-endpoint-termination}

以下是 [Pod 终止](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)文档中所述的流程示例。

假设你有包含单个 nginx 副本（仅用于演示目的）的一个 Deployment 和一个 Service：

{{< codenew file="service/pod-with-graceful-termination.yaml" >}}

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      terminationGracePeriodSeconds: 120 # 超长优雅期
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        lifecycle:
          preStop:
            exec:
              # 实际生产环境中的 Pod 终止可能需要执行任何时长，但不会超过 terminationGracePeriodSeconds。
              # 在本例中，只需挂起至少 terminationGracePeriodSeconds 所指定的持续时间，
              # 在 120 秒时容器将被强制终止。
              # 请注意，在所有这些时间点 nginx 都将继续处理请求。
              command: [
                "/bin/sh", "-c", "sleep 180"
              ]

---

apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

一旦 Pod 和 Service 开始运行，你就可以获取对应的所有 EndpointSlices 的名称：

```shell
kubectl get endpointslice
```

输出类似于：

```none
NAME                  ADDRESSTYPE   PORTS   ENDPOINTS                 AGE
nginx-service-6tjbr   IPv4          80      10.12.1.199,10.12.1.201   22m
```

你可以查看其 status 并验证已经有一个端点被注册：

```shell
kubectl get endpointslices -o json -l kubernetes.io/service-name=nginx-service
```

输出类似于：

```none
{
    "addressType": "IPv4",
    "apiVersion": "discovery.k8s.io/v1",
    "endpoints": [
        {
            "addresses": [
                "10.12.1.201"
            ],
            "conditions": {
                "ready": true,
                "serving": true,
                "terminating": false
                          }
        }
    ]
}
```

现在让我们终止这个 Pod 并验证该 Pod 正在遵从体面终止期限的配置进行终止：

```shell
kubectl delete pod nginx-deployment-7768647bf9-b4b9s
```

查看所有 Pod：

```shell
kubectl get pods
```

输出类似于：

```none
NAME                                READY   STATUS        RESTARTS      AGE
nginx-deployment-7768647bf9-b4b9s   1/1     Terminating   0             4m1s
nginx-deployment-7768647bf9-rkxlw   1/1     Running       0             8s
```

你可以看到新的 Pod 已被调度。

当系统在为新的 Pod 创建新的端点时，旧的端点仍处于 Terminating 状态：

```shell
kubectl get endpointslice -o json nginx-service-6tjbr
```

输出类似于：

```none
{
    "addressType": "IPv4",
    "apiVersion": "discovery.k8s.io/v1",
    "endpoints": [
        {
            "addresses": [
                "10.12.1.201"
            ],
            "conditions": {
                "ready": false,
                "serving": true,
                "terminating": true
            },
            "nodeName": "gke-main-default-pool-dca1511c-d17b",
            "targetRef": {
                "kind": "Pod",
                "name": "nginx-deployment-7768647bf9-b4b9s",
                "namespace": "default",
                "uid": "66fa831c-7eb2-407f-bd2c-f96dfe841478"
            },
            "zone": "us-central1-c"
        },
    ]
        {
            "addresses": [
                "10.12.1.202"
            ],
            "conditions": {
                "ready": true,
                "serving": true,
                "terminating": false
            },
            "nodeName": "gke-main-default-pool-dca1511c-d17b",
            "targetRef": {
                "kind": "Pod",
                "name": "nginx-deployment-7768647bf9-rkxlw",
                "namespace": "default",
                "uid": "722b1cbe-dcd7-4ed4-8928-4a4d0e2bbe35"
            },
            "zone": "us-central1-c"
        }
}
```

这种设计使得应用可以在终止期间公布自己的状态，而客户端（如负载均衡器）则可以实现连接排空功能。
这些客户端可以检测到正在终止的端点，并为这些端点实现特殊的逻辑。

在 Kubernetes 中，正在终止的端点始终将其 `ready` 状态设置为 `false`。
这是为了满足向后兼容的需求，确保现有的负载均衡器不会将 Pod 用于常规流量。
如果需要排空正被终止的 Pod 上的流量，可以将 `serving` 状况作为实际的就绪状态。

当 Pod 被删除时，旧的端点也会被删除。

## {{% heading "whatsnext" %}}

* 了解如何[使用 Service 连接到应用](/zh-cn/docs/tutorials/services/connect-applications-service/)
* 进一步了解[使用 Service 访问集群中的应用](/zh-cn/docs/tasks/access-application-cluster/service-access-application-cluster/)
* 进一步了解[使用 Service 把前端连接到后端](/zh-cn/docs/tasks/access-application-cluster/connecting-frontend-backend/)
* 进一步了解[创建外部负载均衡器](/zh-cn/docs/tasks/access-application-cluster/create-external-load-balancer/)
