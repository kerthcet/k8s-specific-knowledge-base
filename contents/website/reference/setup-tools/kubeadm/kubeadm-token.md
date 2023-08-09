---
title: kubeadm token
content_type: concept
weight: 70
---



如[使用引导令牌进行身份验证](/zh-cn/docs/reference/access-authn-authz/bootstrap-tokens/)所描述的，引导令牌用于在即将加入集群的节点和主节点间建立双向认证。


`kubeadm init` 创建了一个有效期为 24 小时的令牌，下面的命令允许你管理令牌，也可以创建和管理新的令牌。



## kubeadm token create {#cmd-token-create}
{{< include "generated/kubeadm_token_create.md" >}}

## kubeadm token delete {#cmd-token-delete}
{{< include "generated/kubeadm_token_delete.md" >}}

## kubeadm token generate {#cmd-token-generate}
{{< include "generated/kubeadm_token_generate.md" >}}

## kubeadm token list {#cmd-token-list}
{{< include "generated/kubeadm_token_list.md" >}}


## {{% heading "whatsnext" %}}

* [kubeadm join](/zh-cn/docs/reference/setup-tools/kubeadm/kubeadm-join/) 引导 Kubernetes 工作节点并将其加入集群
