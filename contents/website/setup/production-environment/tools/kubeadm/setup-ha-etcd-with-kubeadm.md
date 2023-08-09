---
title: 使用 kubeadm 创建一个高可用 etcd 集群
content_type: task
weight: 70
---



{{< note >}}
在本指南中，使用 kubeadm 作为外部 etcd 节点管理工具，请注意 kubeadm 不计划支持此类节点的证书更换或升级。
对于长期规划是使用 [etcdadm](https://github.com/kubernetes-sigs/etcdadm) 增强工具来管理这些方面。
{{< /note >}}


默认情况下，kubeadm 在每个控制平面节点上运行一个本地 etcd 实例。也可以使用外部的 etcd 集群，并在不同的主机上提供 etcd 实例。
这两种方法的区别在 [高可用拓扑的选项](/zh-cn/docs/setup/production-environment/tools/kubeadm/ha-topology) 页面中阐述。


这个任务将指导你创建一个由三个成员组成的高可用外部 etcd 集群，该集群在创建过程中可被 kubeadm 使用。

## {{% heading "prerequisites" %}}

- 三个可以通过 2379 和 2380 端口相互通信的主机。本文档使用这些作为默认端口。不过，它们可以通过 kubeadm 的配置文件进行自定义。
- 每个主机必须安装 systemd 和 bash 兼容的 shell。
- 每台主机必须[安装有容器运行时、kubelet 和 kubeadm](/zh-cn/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)。
- 每个主机都应该能够访问 Kubernetes 容器镜像仓库 (registry.k8s.io)，
或者使用 `kubeadm config images list/pull` 列出/拉取所需的 etcd 镜像。
本指南将把 etcd 实例设置为由 kubelet 管理的[静态 Pod](/zh-cn/docs/tasks/configure-pod-container/static-pod/)。
- 一些可以用来在主机间复制文件的基础设施。例如 `ssh` 和 `scp` 就可以满足需求。


## 建立集群

一般来说，是在一个节点上生成所有证书并且只分发这些**必要**的文件到其它节点上。

{{< note >}}
kubeadm 包含生成下述证书所需的所有必要的密码学工具；在这个例子中，不需要其他加密工具。
{{< /note >}}

{{< note >}}
下面的例子使用 IPv4 地址，但是你也可以使用 IPv6 地址配置 kubeadm、kubelet 和 etcd。一些 Kubernetes 选项支持双协议栈，但是 etcd 不支持。
关于 Kubernetes 双协议栈支持的更多细节，请参见 [kubeadm 的双栈支持](/zh-cn/docs/setup/production-environment/tools/kubeadm/dual-stack-support/)。
{{< /note >}}

1. 将 kubelet 配置为 etcd 的服务管理器。

   {{< note >}}
   你必须在要运行 etcd 的所有主机上执行此操作。
   {{< /note >}}
   由于 etcd 是首先创建的，因此你必须通过创建具有更高优先级的新文件来覆盖
   kubeadm 提供的 kubelet 单元文件。

   ```sh
   cat << EOF > /etc/systemd/system/kubelet.service.d/kubelet.conf
   # 将下面的 "systemd" 替换为你的容器运行时所使用的 cgroup 驱动。
   # kubelet 的默认值为 "cgroupfs"。
   # 如果需要的话，将 "containerRuntimeEndpoint" 的值替换为一个不同的容器运行时。
   #
   apiVersion: kubelet.config.k8s.io/v1beta1
   kind: KubeletConfiguration
   authentication:
     anonymous:
       enabled: false
     webhook:
       enabled: false
   authorization:
     mode: AlwaysAllow
   cgroupDriver: systemd
   address: 127.0.0.1
   containerRuntimeEndpoint: unix:///var/run/containerd/containerd.sock
   staticPodPath: /etc/kubernetes/manifests
   EOF
   
   cat << EOF > /etc/systemd/system/kubelet.service.d/20-etcd-service-manager.conf
   [Service]
   ExecStart=
   ExecStart=/usr/bin/kubelet --config=/etc/systemd/system/kubelet.service.d/kubelet.conf
   Restart=always
   EOF

   systemctl daemon-reload
   systemctl restart kubelet
   ```

   检查 kubelet 的状态以确保其处于运行状态：

   ```shell
   systemctl status kubelet
   ```

2. 为 kubeadm 创建配置文件。

   使用以下脚本为每个将要运行 etcd 成员的主机生成一个 kubeadm 配置文件。

   ```sh
   # 使用你的主机 IP 替换 HOST0、HOST1 和 HOST2 的 IP 地址
   export HOST0=10.0.0.6
   export HOST1=10.0.0.7
   export HOST2=10.0.0.8

   # 使用你的主机名更新 NAME0、NAME1 和 NAME2
   export NAME0="infra0"
   export NAME1="infra1"
   export NAME2="infra2"

   # 创建临时目录来存储将被分发到其它主机上的文件
   mkdir -p /tmp/${HOST0}/ /tmp/${HOST1}/ /tmp/${HOST2}/

   HOSTS=(${HOST0} ${HOST1} ${HOST2})
   NAMES=(${NAME0} ${NAME1} ${NAME2})

   for i in "${!HOSTS[@]}"; do
   HOST=${HOSTS[$i]}
   NAME=${NAMES[$i]}
   cat << EOF > /tmp/${HOST}/kubeadmcfg.yaml
   ---
   apiVersion: "kubeadm.k8s.io/v1beta3"
   kind: InitConfiguration
   nodeRegistration:
       name: ${NAME}
   localAPIEndpoint:
       advertiseAddress: ${HOST}
   ---
   apiVersion: "kubeadm.k8s.io/v1beta3"
   kind: ClusterConfiguration
   etcd:
       local:
           serverCertSANs:
           - "${HOST}"
           peerCertSANs:
           - "${HOST}"
           extraArgs:
               initial-cluster: ${NAMES[0]}=https://${HOSTS[0]}:2380,${NAMES[1]}=https://${HOSTS[1]}:2380,${NAMES[2]}=https://${HOSTS[2]}:2380
               initial-cluster-state: new
               name: ${NAME}
               listen-peer-urls: https://${HOST}:2380
               listen-client-urls: https://${HOST}:2379
               advertise-client-urls: https://${HOST}:2379
               initial-advertise-peer-urls: https://${HOST}:2380
   EOF
   done
   ```

3. 生成证书颁发机构

   如果你已经拥有 CA，那么唯一的操作是复制 CA 的 `crt` 和 `key` 文件到
   `etc/kubernetes/pki/etcd/ca.crt` 和 `/etc/kubernetes/pki/etcd/ca.key`。
   复制完这些文件后继续下一步，“为每个成员创建证书”。

   如果你还没有 CA，则在 `$HOST0`（你为 kubeadm 生成配置文件的位置）上运行此命令。

   ```shell
   kubeadm init phase certs etcd-ca
   ```

   这一操作创建如下两个文件：

   - `/etc/kubernetes/pki/etcd/ca.crt`
   - `/etc/kubernetes/pki/etcd/ca.key`

4. 为每个成员创建证书

   ```shell
   kubeadm init phase certs etcd-server --config=/tmp/${HOST2}/kubeadmcfg.yaml
   kubeadm init phase certs etcd-peer --config=/tmp/${HOST2}/kubeadmcfg.yaml
   kubeadm init phase certs etcd-healthcheck-client --config=/tmp/${HOST2}/kubeadmcfg.yaml
   kubeadm init phase certs apiserver-etcd-client --config=/tmp/${HOST2}/kubeadmcfg.yaml
   cp -R /etc/kubernetes/pki /tmp/${HOST2}/
   # 清理不可重复使用的证书
   find /etc/kubernetes/pki -not -name ca.crt -not -name ca.key -type f -delete

   kubeadm init phase certs etcd-server --config=/tmp/${HOST1}/kubeadmcfg.yaml
   kubeadm init phase certs etcd-peer --config=/tmp/${HOST1}/kubeadmcfg.yaml
   kubeadm init phase certs etcd-healthcheck-client --config=/tmp/${HOST1}/kubeadmcfg.yaml
   kubeadm init phase certs apiserver-etcd-client --config=/tmp/${HOST1}/kubeadmcfg.yaml
   cp -R /etc/kubernetes/pki /tmp/${HOST1}/
   find /etc/kubernetes/pki -not -name ca.crt -not -name ca.key -type f -delete

   kubeadm init phase certs etcd-server --config=/tmp/${HOST0}/kubeadmcfg.yaml
   kubeadm init phase certs etcd-peer --config=/tmp/${HOST0}/kubeadmcfg.yaml
   kubeadm init phase certs etcd-healthcheck-client --config=/tmp/${HOST0}/kubeadmcfg.yaml
   kubeadm init phase certs apiserver-etcd-client --config=/tmp/${HOST0}/kubeadmcfg.yaml
   # 不需要移动 certs 因为它们是给 HOST0 使用的

   # 清理不应从此主机复制的证书
   find /tmp/${HOST2} -name ca.key -type f -delete
   find /tmp/${HOST1} -name ca.key -type f -delete
   ```

5. 复制证书和 kubeadm 配置

   证书已生成，现在必须将它们移动到对应的主机。

   ```shell
   USER=ubuntu
   HOST=${HOST1}
   scp -r /tmp/${HOST}/* ${USER}@${HOST}:
   ssh ${USER}@${HOST}
   USER@HOST $ sudo -Es
   root@HOST $ chown -R root:root pki
   root@HOST $ mv pki /etc/kubernetes/
   ```

6. 确保已经所有预期的文件都存在

   `$HOST0` 所需文件的完整列表如下：

   ```none
   /tmp/${HOST0}
   └── kubeadmcfg.yaml
   ---
   /etc/kubernetes/pki
   ├── apiserver-etcd-client.crt
   ├── apiserver-etcd-client.key
   └── etcd
       ├── ca.crt
       ├── ca.key
       ├── healthcheck-client.crt
       ├── healthcheck-client.key
       ├── peer.crt
       ├── peer.key
       ├── server.crt
       └── server.key
   ```

   在 `$HOST1` 上：

   ```console
   $HOME
   └── kubeadmcfg.yaml
   ---
   /etc/kubernetes/pki
   ├── apiserver-etcd-client.crt
   ├── apiserver-etcd-client.key
   └── etcd
       ├── ca.crt
       ├── healthcheck-client.crt
       ├── healthcheck-client.key
       ├── peer.crt
       ├── peer.key
       ├── server.crt
       └── server.key
   ```

   在 `$HOST2` 上：

   ```console
   $HOME
   └── kubeadmcfg.yaml
   ---
   /etc/kubernetes/pki
   ├── apiserver-etcd-client.crt
   ├── apiserver-etcd-client.key
   └── etcd
       ├── ca.crt
       ├── healthcheck-client.crt
       ├── healthcheck-client.key
       ├── peer.crt
       ├── peer.key
       ├── server.crt
       └── server.key
   ```

7. 创建静态 Pod 清单

   既然证书和配置已经就绪，是时候去创建清单了。
   在每台主机上运行 `kubeadm` 命令来生成 etcd 使用的静态清单。

   ```shell
   root@HOST0 $ kubeadm init phase etcd local --config=/tmp/${HOST0}/kubeadmcfg.yaml
   root@HOST1 $ kubeadm init phase etcd local --config=$HOME/kubeadmcfg.yaml
   root@HOST2 $ kubeadm init phase etcd local --config=$HOME/kubeadmcfg.yaml
   ```

8. 可选：检查集群运行状况

   如果 `etcdctl` 不可用，你可以在容器镜像内运行此工具。
   你可以使用 `crictl run` 这类工具直接在容器运行时执行此操作，而不是通过 Kubernetes。

   ```sh
   ETCDCTL_API=3 etcdctl \
   --cert /etc/kubernetes/pki/etcd/peer.crt \
   --key /etc/kubernetes/pki/etcd/peer.key \
   --cacert /etc/kubernetes/pki/etcd/ca.crt \
   --endpoints https://${HOST0}:2379 endpoint health
   ...
   https://[HOST0 IP]:2379 is healthy: successfully committed proposal: took = 16.283339ms
   https://[HOST1 IP]:2379 is healthy: successfully committed proposal: took = 19.44402ms
   https://[HOST2 IP]:2379 is healthy: successfully committed proposal: took = 35.926451ms
   ```

   - 将 `${HOST0}` 设置为要测试的主机的 IP 地址。

## {{% heading "whatsnext" %}}

一旦拥有了一个正常工作的 3 成员的 etcd 集群，
你就可以基于[使用 kubeadm 外部 etcd 的方法](/zh-cn/docs/setup/production-environment/tools/kubeadm/high-availability/)，
继续部署一个高可用的控制平面。
