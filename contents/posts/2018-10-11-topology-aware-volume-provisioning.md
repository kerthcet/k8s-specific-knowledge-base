---
layout: blog
title: 'Kubernetes 中的拓扑感知数据卷供应'
date: 2018-10-11
slug: topology-aware-volume-provisioning-in-kubernetes
---

**作者**: Michelle Au（谷歌）

通过提供拓扑感知动态卷供应功能，具有持久卷的多区域集群体验在 Kubernetes 1.12
中得到了改进。此功能使得 Kubernetes 在动态供应卷时能做出明智的决策，方法是从调度器获得为
Pod 提供数据卷的最佳位置。在多区域集群环境，这意味着数据卷能够在满足你的 Pod
运行需要的合适的区域被供应，从而允许你跨故障域轻松部署和扩展有状态工作负载，从而提供高可用性和容错能力。

## 以前的挑战

在此功能被提供之前，在多区域集群中使用区域化的持久磁盘（例如 AWS ElasticBlockStore、
Azure Disk、GCE PersistentDisk）运行有状态工作负载存在许多挑战。动态供应独立于 Pod
调度处理，这意味着只要你创建了一个 PersistentVolumeClaim（PVC），一个卷就会被供应。
这也意味着供应者不知道哪些 Pod 正在使用该卷，也不清楚任何可能影响调度的 Pod 约束。

这导致了不可调度的 Pod，因为在以下区域中配置了卷：

* 没有足够的 CPU 或内存资源来运行 Pod
* 与节点选择器、Pod 亲和或反亲和策略冲突
* 由于污点（taint）不能运行 Pod

另一个常见问题是，使用多个持久卷的非有状态 Pod 可能会在不同的区域中配置每个卷，从而导致一个不可调度的 Pod。

次优的解决方法包括节点超配，或在正确的区域中手动创建卷，但这会造成难以动态部署和扩展有状态工作负载的问题。

拓扑感知动态供应功能解决了上述所有问题。

## 支持的卷类型

在 1.12 中，以下驱动程序支持拓扑感知动态供应：

* AWS EBS
* Azure Disk
* GCE PD（包括 Regional PD）
* CSI（alpha） - 目前只有 GCE PD CSI 驱动实现了拓扑支持

## 设计原则

虽然最初支持的插件集都是基于区域的，但我们设计此功能时遵循 Kubernetes 跨环境可移植性的原则。
拓扑规范是通用的，并使用类似于基于标签的规范，如 Pod nodeSelectors 和 nodeAffinity。
该机制允许你定义自己的拓扑边界，例如内部部署集群中的机架，而无需修改调度程序以了解这些自定义拓扑。

此外，拓扑信息是从 Pod 规范中抽象出来的，因此 Pod 不需要了解底层存储系统的拓扑特征。
这意味着你可以在多个集群、环境和存储系统中使用相同的 Pod 规范。

## 入门

要启用此功能，你需要做的就是创建一个将 `volumeBindingMode` 设置为 `WaitForFirstConsumer` 的 StorageClass：

```
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: topology-aware-standard
provisioner: kubernetes.io/gce-pd
volumeBindingMode: WaitForFirstConsumer
parameters:
  type: pd-standard
```

这个新设置表明卷配置器不立即创建卷，而是等待使用关联的 PVC 的 Pod 通过调度运行。
请注意，不再需要指定以前的 StorageClass `zone` 和 `zones` 参数，因为现在在哪个区域中配置卷由 Pod 策略决定。

接下来，使用此 StorageClass 创建一个 Pod 和 PVC。
此过程与之前相同，但在 PVC 中指定了不同的 StorageClass。
以下是一个假设示例，通过指定许多 Pod 约束和调度策略来演示新功能特性：

* 一个 Pod 多个 PVC
* 跨子区域的节点亲和
* 同一区域 Pod 反亲和

```
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:   
  serviceName: "nginx"
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: failure-domain.beta.kubernetes.io/zone
                operator: In
                values:
                - us-central1-a
                - us-central1-f
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - nginx
            topologyKey: failure-domain.beta.kubernetes.io/zone
      containers:
      - name: nginx
        image: gcr.io/google_containers/nginx-slim:0.8
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
        - name: logs
          mountPath: /logs
 volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: topology-aware-standard
      resources:
        requests:
          storage: 10Gi
  - metadata:
      name: logs
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: topology-aware-standard
      resources:
        requests:
          storage: 1Gi
```

之后，你可以看到根据 Pod 设置的策略在区域中配置卷：

```
$ kubectl get pv -o=jsonpath='{range .items[*]}{.spec.claimRef.name}{"\t"}{.metadata.labels.failure\-domain\.beta\.kubernetes\.io/zone}{"\n"}{end}'
www-web-0       us-central1-f
logs-web-0      us-central1-f
www-web-1       us-central1-a
logs-web-1      us-central1-a
```

## 我怎样才能了解更多？

有关拓扑感知动态供应功能的官方文档可在此处获取：
https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode

有关 CSI 驱动程序的文档，请访问： https://kubernetes-csi.github.io/docs/

## 下一步是什么？

我们正积极致力于改进此功能以支持：

* 更多卷类型，包括本地卷的动态供应
* 动态容量可附加计数和每个节点的容量限制

## 我如何参与？

如果你对此功能有反馈意见或有兴趣参与设计和开发，请加入
[Kubernetes 存储特别兴趣小组](https://github.com/kubernetes/community/tree/master/sig-storage)（SIG）。
我们正在快速成长，并始终欢迎新的贡献者。

特别感谢帮助推出此功能的所有贡献者，包括 Cheng Xing ([verult](https://github.com/verult))、
Chuqiang Li ([lichuqiang](https://github.com/lichuqiang))、David Zhu ([davidz627](https://github.com/davidz627))、
Deep Debroy ([ddebroy](https://github.com/ddebroy))、Jan Šafránek ([jsafrane](https://github.com/jsafrane))、
Jordan Liggitt ([liggitt](https://github.com/liggitt))、Michelle Au ([msau42](https://github.com/msau42))、
Pengfei Ni ([feiskyer](https://github.com/feiskyer))、Saad Ali ([saad-ali](https://github.com/saad-ali))、
Tim Hockin ([thockin](https://github.com/thockin))，以及 Yecheng Fu ([cofyc](https://github.com/cofyc))。
