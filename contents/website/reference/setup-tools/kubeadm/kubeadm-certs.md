---
title: kubeadm certs
content_type: concept
weight: 90
---

`kubeadm certs` 提供管理证书的工具。关于如何使用这些命令的细节，可参见
[使用 kubeadm 管理证书](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/)。

## kubeadm certs {#cmd-certs}

用来操作 Kubernetes 证书的一组命令。

{{< tabs name="tab-certs" >}}
{{< tab name="概览" include="generated/kubeadm_certs.md" />}}
{{< /tabs >}}

## kubeadm certs renew {#cmd-certs-renew}

你可以使用 `all` 子命令来续订所有 Kubernetes 证书，也可以选择性地续订部分证书。
更多的相关细节，可参见
[手动续订证书](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/#manual-certificate-renewal)。

{{< tabs name="tab-certs-renew" >}}
{{< tab name="renew" include="generated/kubeadm_certs_renew.md" />}}
{{< tab name="all" include="generated/kubeadm_certs_renew_all.md" />}}
{{< tab name="admin.conf" include="generated/kubeadm_certs_renew_admin.conf.md" />}}
{{< tab name="apiserver-etcd-client" include="generated/kubeadm_certs_renew_apiserver-etcd-client.md" />}}
{{< tab name="apiserver-kubelet-client" include="generated/kubeadm_certs_renew_apiserver-kubelet-client.md" />}}
{{< tab name="apiserver" include="generated/kubeadm_certs_renew_apiserver.md" />}}
{{< tab name="controller-manager.conf" include="generated/kubeadm_certs_renew_controller-manager.conf.md" />}}
{{< tab name="etcd-healthcheck-client" include="generated/kubeadm_certs_renew_etcd-healthcheck-client.md" />}}
{{< tab name="etcd-peer" include="generated/kubeadm_certs_renew_etcd-peer.md" />}}
{{< tab name="etcd-server" include="generated/kubeadm_certs_renew_etcd-server.md" />}}
{{< tab name="front-proxy-client" include="generated/kubeadm_certs_renew_front-proxy-client.md" />}}
{{< tab name="scheduler.conf" include="generated/kubeadm_certs_renew_scheduler.conf.md" />}}
{{< /tabs >}}

## kubeadm certs certificate-key {#cmd-certs-certificate-key}

此命令可用来生成一个新的控制面证书密钥。密钥可以作为 `--certificate-key`
标志的取值传递给 [`kubeadm init`](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-init)
和 [`kubeadm join`](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-join)
命令，从而在添加新的控制面节点时能够自动完成证书复制。

{{< tabs name="tab-certs-certificate-key" >}}
{{< tab name="certificate-key" include="generated/kubeadm_certs_certificate-key.md" />}}
{{< /tabs >}}

## kubeadm certs check-expiration {#cmd-certs-check-expiration}

此命令检查 kubeadm 所管理的本地 PKI 中的证书是否以及何时过期。
更多的相关细节，可参见
[检查证书过期](/zh-cn/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/#check-certificate-expiration)。


{{< tabs name="tab-certs-check-expiration" >}}
{{< tab name="check-expiration" include="generated/kubeadm_certs_check-expiration.md" />}}
{{< /tabs >}}

## kubeadm certs generate-csr {#cmd-certs-generate-csr}

此命令可用来为所有控制面证书和 kubeconfig 文件生成密钥和 CSR（签名请求）。
用户可以根据自身需要选择 CA 为 CSR 签名。

{{< tabs name="tab-certs-generate-csr" >}}
{{< tab name="generate-csr" include="generated/kubeadm_certs_generate-csr.md" />}}
{{< /tabs >}}

## {{% heading "whatsnext" %}}

* 用来启动引导 Kubernetes 控制面节点的
  [kubeadm init](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-init/)
  命令
* 用来将节点连接到集群的
  [kubeadm join](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-join/)
  命令
* 用来回滚 `kubeadm init` 或 `kubeadm join` 对当前主机所做修改的
  [kubeadm reset](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-reset/)
  命令

