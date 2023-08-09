---
title: 迁移多副本的控制面以使用云控制器管理器
linkTitle: 迁移多副本的控制面以使用云控制器管理器
content_type: task
weight: 250
---



{{< glossary_definition term_id="cloud-controller-manager" length="all">}}

## 背景

作为[云驱动提取工作](/blog/2019/04/17/the-future-of-cloud-providers-in-kubernetes/)
的一部分，所有特定于云的控制器都必须移出 `kube-controller-manager`。
所有在 `kube-controller-manager` 中运行云控制器的现有集群必须迁移到特定于云厂商的
`cloud-controller-manager` 中运行这些控制器。

领导者迁移（Leader Migration）提供了一种机制，使得 HA 集群可以通过这两个组件之间共享资源锁，
在升级多副本的控制平面时，安全地将“特定于云”的控制器从 `kube-controller-manager` 迁移到
`cloud-controller-manager`。
对于单节点控制平面，或者在升级过程中可以容忍控制器管理器不可用的情况，则不需要领导者迁移，
亦可以忽略本指南。

领导者迁移可以通过在 `kube-controller-manager` 或 `cloud-controller-manager` 上设置
`--enable-leader-migration` 来启用。
领导者迁移仅在升级期间适用，并且在升级完成后可以安全地禁用或保持启用状态。

本指南将引导你手动将控制平面从内置的云驱动的 `kube-controller-manager` 升级为
同时运行 `kube-controller-manager` 和 `cloud-controller-manager`。
如果使用某种工具来部署和管理集群，请参阅对应工具和云驱动的文档以获取迁移的具体说明。

## {{% heading "prerequisites" %}}

假定控制平面正在运行 Kubernetes 版本 N，要升级到版本 N+1。
尽管可以在同一版本内进行迁移，但理想情况下，迁移应作为升级的一部分执行，
以便可以配置的变更可以与发布版本变化对应起来。
N 和 N+1 的确切版本值取决于各个云厂商。例如，如果云厂商构建了一个可与 Kubernetes 1.24
配合使用的 `cloud-controller-manager`，则 N 可以为 1.23，N+1 可以为 1.24。

控制平面节点应运行 `kube-controller-manager` 并启用领导者选举，这也是默认设置。
在版本 N 中，树内云驱动必须设置 `--cloud-provider` 标志，而且 `cloud-controller-manager`
应该尚未部署。

树外云驱动必须已经构建了一个实现了领导者迁移的 `cloud-controller-manager`。
如果云驱动导入了 v0.21.0 或更高版本的 `k8s.io/cloud-provider` 和 `k8s.io/controller-manager`，
则可以进行领导者迁移。
但是，对 v0.22.0 以下的版本，领导者迁移是一项 Alpha 阶段功能，需要在 `cloud-controller-manager`
中启用特性门控 `ControllerManagerLeaderMigration`。

本指南假定每个控制平面节点的 kubelet 以静态 Pod 的形式启动 `kube-controller-manager`
和 `cloud-controller-manager`，静态 Pod 的定义在清单文件中。
如果组件以其他设置运行，请相应地调整这里的步骤。

关于鉴权，本指南假定集群使用 RBAC。如果其他鉴权模式授予 `kube-controller-manager`
和 `cloud-controller-manager` 组件权限，请以与该模式匹配的方式授予所需的访问权限。


### 授予访问迁移租约的权限

控制器管理器的默认权限仅允许访问其主租约（Lease）对象。为了使迁移正常进行，
需要授权它访问其他 Lease 对象。

你可以通过修改 `system::leader-locking-kube-controller-manager` 角色来授予
`kube-controller-manager` 对 Lease API 的完全访问权限。
本任务指南假定迁移 Lease 的名称为 `cloud-provider-extraction-migration`。

```shell
kubectl patch -n kube-system role 'system::leader-locking-kube-controller-manager' -p '{"rules": [ {"apiGroups":[ "coordination.k8s.io"], "resources": ["leases"], "resourceNames": ["cloud-provider-extraction-migration"], "verbs": ["create", "list", "get", "update"] } ]}' --type=merge
```

对 `system::leader-locking-cloud-controller-manager` 角色执行相同的操作。

```shell
kubectl patch -n kube-system role 'system::leader-locking-cloud-controller-manager' -p '{"rules": [ {"apiGroups":[ "coordination.k8s.io"], "resources": ["leases"], "resourceNames": ["cloud-provider-extraction-migration"], "verbs": ["create", "list", "get", "update"] } ]}' --type=merge
```

### 初始领导者迁移配置

领导者迁移可以选择使用一个表示如何将控制器分配给不同管理器的配置文件。
目前，对于树内云驱动，`kube-controller-manager` 运行 `route`、`service` 和
`cloud-node-lifecycle`。以下示例配置显示的是这种分配。

领导者迁移可以不指定配置的情况下启用。请参阅[默认配置](#default-configuration) 
以获取更多详细信息。

```yaml
kind: LeaderMigrationConfiguration
apiVersion: controllermanager.config.k8s.io/v1
leaderName: cloud-provider-extraction-migration
controllerLeaders:
  - name: route
    component: kube-controller-manager
  - name: service
    component: kube-controller-manager
  - name: cloud-node-lifecycle
    component: kube-controller-manager
```

或者，由于控制器可以在任一控制器管理器下运行，因此将双方的 `component` 设置为 `*`
可以使迁移双方的配置文件保持一致。

```yaml
# 通配符版本
kind: LeaderMigrationConfiguration
apiVersion: controllermanager.config.k8s.io/v1
leaderName: cloud-provider-extraction-migration
controllerLeaders:
  - name: route
    component: *
  - name: service
    component: *
  - name: cloud-node-lifecycle
    component: *
```

在每个控制平面节点上，请将如上内容保存到 `/etc/leadermigration.conf` 中，
并更新 `kube-controller-manager` 清单，以便将文件挂载到容器内的同一位置。
另外，请更新同一清单，添加以下参数：

- `--enable-leader-migration` 在控制器管理器上启用领导者迁移
- `--leader-migration-config=/etc/leadermigration.conf` 设置配置文件

在每个节点上重新启动 `kube-controller-manager`。这时，`kube-controller-manager`
已启用领导者迁移，为迁移准备就绪。

### 部署云控制器管理器

在版本 N+1 中，如何将控制器分配给不同管理器的预期分配状态可以由新的配置文件表示，
如下所示。请注意，各个 `controllerLeaders` 的 `component` 字段从 `kube-controller-manager`
更改为 `cloud-controller-manager`。
或者，使用上面提到的通配符版本，它具有相同的效果。

```yaml
kind: LeaderMigrationConfiguration
apiVersion: controllermanager.config.k8s.io/v1
leaderName: cloud-provider-extraction-migration
controllerLeaders:
  - name: route
    component: cloud-controller-manager
  - name: service
    component: cloud-controller-manager
  - name: cloud-node-lifecycle
    component: cloud-controller-manager
```

当创建版本 N+1 的控制平面节点时，应将如上内容写入到 `/etc/leadermigration.conf`。
你需要更新 `cloud-controller-manager` 的清单，以与版本 N 的 `kube-controller-manager`
相同的方式挂载配置文件。
类似地，添加 `--enable-leader-migration`
和 `--leader-migration-config=/etc/leadermigration.conf` 到 `cloud-controller-manager`
的参数中。

使用已更新的 `cloud-controller-manager` 清单创建一个新的 N+1 版本的控制平面节点，
同时设置 `kube-controller-manager` 的 `--cloud-provider` 标志为 `external`。
版本为 N+1 的 `kube-controller-manager` 不能启用领导者迁移，
因为在使用外部云驱动的情况下，它不再运行已迁移的控制器，因此不参与迁移。

请参阅[云控制器管理器管理](/zh-cn/docs/tasks/administer-cluster/running-cloud-controller/) 
了解有关如何部署 `cloud-controller-manager` 的更多细节。

### 升级控制平面

现在，控制平面同时包含 N 和 N+1 版本的节点。
版本 N 的节点仅运行 `kube-controller-manager`，而版本 N+1 的节点同时运行
`kube-controller-manager` 和 `cloud-controller-manager`。
根据配置所指定，已迁移的控制器在版本 N 的 `kube-controller-manager` 或版本
N+1 的 `cloud-controller-manager` 下运行，具体取决于哪个控制器管理器拥有迁移租约对象。
任何时候都不会有同一个控制器在两个控制器管理器下运行。

以滚动的方式创建一个新的版本为 N+1 的控制平面节点，并将版本 N 中的一个关闭，
直到控制平面仅包含版本为 N+1 的节点。
如果需要从 N+1 版本回滚到 N 版本，则将 `kube-controller-manager` 启用了领导者迁移的、
且版本为 N 的节点添加回控制平面，每次替换 N+1 版本中的一个，直到只有版本 N 的节点为止。

### （可选）禁用领导者迁移 {#disable-leader-migration}

现在，控制平面已经完成升级，同时运行版本 N+1 的 `kube-controller-manager`
和 `cloud-controller-manager`。领导者迁移的任务已经结束，可以被安全地禁用以节省一个
Lease 资源。在将来可以安全地重新启用领导者迁移，以完成回滚。

在滚动管理器中，更新 `cloud-controller-manager` 的清单以同时取消设置
`--enable-leader-migration` 和 `--leader-migration-config=` 标志，并删除
`/etc/leadermigration.conf` 的挂载，最后删除 `/etc/leadermigration.conf`。
要重新启用领导者迁移，请重新创建配置文件，并将其挂载和启用领导者迁移的标志添加回到
`cloud-controller-manager`。

### 默认配置 {#default-configuration}

从 Kubernetes 1.22 开始，领导者迁移提供了一个默认配置，它适用于控制器与管理器间默认的分配关系。
可以通过设置 `--enable-leader-migration`，但不设置 `--leader-migration-config=`
来启用默认配置。

对于 `kube-controller-manager` 和 `cloud-controller-manager`，如果没有用参数来启用树内云驱动或者改变控制器属主，
则可以使用默认配置来避免手动创建配置文件。

### 特殊情况：迁移节点 IPAM 控制器 {#node-ipam-controller-migration}

如果你的云供应商提供了节点 IPAM 控制器的实现，你应该切换到 `cloud-controller-manager` 中的实现。
通过在其标志中添加 `--controllers=*,-nodeipam` 来禁用 N+1 版本的 `kube-controller-manager` 中的节点 IPAM 控制器。
然后将 `nodeipam` 添加到迁移的控制器列表中。

```yaml
# 通配符版本，带有 nodeipam
kind: LeaderMigrationConfiguration
apiVersion: controllermanager.config.k8s.io/v1
leaderName: cloud-provider-extraction-migration
controllerLeaders:
  - name: route
    component: *
  - name: service
    component: *
  - name: cloud-node-lifecycle
    component: *
  - name: nodeipam
-   component: *
```

## {{% heading "whatsnext" %}}
- 阅读[领导者迁移控制器管理器](https://github.com/kubernetes/enhancements/tree/master/keps/sig-cloud-provider/2436-controller-manager-leader-migration)
  改进建议提案。

