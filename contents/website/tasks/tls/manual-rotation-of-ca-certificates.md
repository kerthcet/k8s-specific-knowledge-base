---
title: 手动轮换 CA 证书
content_type: task
---


本页展示如何手动轮换证书机构（CA）证书。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

- 要了解 Kubernetes 中用户认证的更多信息，参阅
  [认证](/zh-cn/docs/reference/access-authn-authz/authentication)；
- 要了解与 CA 证书最佳实践有关的更多信息，
  参阅[单根 CA](/zh-cn/docs/setup/best-practices/certificates/#single-root-ca)。


## 手动轮换 CA 证书  {#rotate-the-ca-certificates-manually}

{{< caution >}}
确保备份你的证书目录、配置文件以及其他必要文件。

这里的方法假定 Kubernetes 的控制面通过运行多个 API 服务器以高可用配置模式运行。
另一假定是 API 服务器可体面地终止，因而客户端可以彻底地与一个 API 服务器断开
连接并连接到另一个 API 服务器。

如果集群中只有一个 API 服务器，则在 API 服务器重启期间会经历服务中断期。
{{< /caution >}}

1. 将新的 CA 证书和私钥（例如：`ca.crt`、`ca.key`、`front-proxy-ca.crt` 和
   `front-proxy-client.key`）分发到所有控制面节点，放在其 Kubernetes 证书目录下。

2. 更新 {{< glossary_tooltip text="kube-controller-manager" term_id="kube-controller-manager" >}}
   的 `--root-ca-file` 标志，使之同时包含老的和新的 CA，之后重启
   kube-controller-manager。

   自此刻起，所创建的所有{{< glossary_tooltip text="ServiceAccount" term_id="service-account" >}}
   都会获得同时包含老的 CA 和新的 CA 的 Secret。

   {{< note >}}
   kube-controller-manager 标志 `--client-ca-file` 和 `--cluster-signing-cert-file`
   所引用的文件不能是 CA 证书包。如果这些标志和 `--root-ca-file` 指向同一个 `ca.crt` 包文件
   （包含老的和新的 CA 证书），你将会收到出错信息。
   要解决这个问题，可以将新的 CA 证书复制到单独的文件中，并将 `--client-ca-file` 和
   `--cluster-signing-cert-file` 标志指向该副本。一旦 `ca.crt` 不再是证书包文件，
   就可以恢复有问题的标志指向  `ca.crt` 并删除该副本。

   kubeadm 的 [Issue 1350](https://github.com/kubernetes/kubeadm/issues/1350)
   在跟踪一个导致 kube-controller-manager 无法接收 CA 证书包的问题。
   {{< /note >}}

3. 等待该控制器管理器更新服务账号 Secret 中的 `ca.crt`，使之同时包含老的和新的 CA 证书。

   如果在 API 服务器使用新的 CA 之前启动了新的 Pod，这些新的 Pod
   也会获得此更新并且同时信任老的和新的 CA 证书。

4. 重启所有使用集群内配置的 Pod（例如：kube-proxy、CoreDNS 等），以便这些 Pod
   能够使用与 ServiceAccount 相关联的 Secret 中的、已更新的证书机构数据。

   * 确保 CoreDNS、kube-proxy 和其他使用集群内配置的 Pod 都正按预期方式工作。

5. 将老的和新的 CA 都追加到 `kube-apiserver` 配置的 `--client-ca-file` 和
   `--kubelet-certificate-authority` 标志所指的文件。

6. 将老的和新的 CA 都追加到 `kube-scheduler` 配置的 `--client-ca-file` 标志所指的文件。

7. 通过替换 `client-certificate-data` 和 `client-key-data` 中的内容，更新用户账号的证书。

   有关为独立用户账号创建证书的更多信息，可参阅
   [为用户帐号配置证书](/zh-cn/docs/setup/best-practices/certificates/#configure-certificates-for-user-accounts)。

   另外，还要更新 kubeconfig 文件中的 `certificate-authority-data` 节，
   使之包含 Base64 编码的老的和新的证书机构数据。

8. 更新 {{< glossary_tooltip term_id="cloud-controller-manager" >}} 的 `--root-ca-file`
   标志值，使之同时包含老的和新的 CA，之后重新启动 cloud-controller-manager。

   {{< note >}}
   如果你的集群中不包含 cloud-controller-manager，你可以略过这一步。
   {{< /note >}}

9. 遵循下列步骤执行滚动更新

   1. 重新启动所有其他[被聚合的 API 服务器](/zh-cn/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)
      或者 Webhook 处理程序，使之信任新的 CA 证书。

   2. 在所有节点上更新 kubelet 配置中的 `clientCAFile` 所指文件以及 `kubelet.conf` 中的
      `certificate-authority-data` 并重启 kubelet 以同时使用老的和新的 CA 证书。

      如果你的 kubelet 并未使用客户端证书轮换，则在所有节点上更新 `kubelet.conf` 中
      `client-certificate-data` 和 `client-key-data` 以及 kubelet
      客户端证书文件（通常位于 `/var/lib/kubelet/pki` 目录下）

   3. 使用用新的 CA 签名的证书
       （`apiserver.crt`、`apiserver-kubelet-client.crt` 和 `front-proxy-client.crt`）
      来重启 API 服务器。
      你可以使用现有的私钥，也可以使用新的私钥。
      如果你改变了私钥，则要将更新的私钥也放到 Kubernetes 证书目录下。

      由于集群中的 Pod 既信任老的 CA 也信任新的 CA，Pod 中的客户端会经历短暂的连接断开状态，
      之后再使用新的 CA 所签名的证书连接到新的 API 服务器。

      * 重启 {{< glossary_tooltip term_id="kube-scheduler" text="kube-scheduler" >}} 以使用并信任新的
        CA 证书。
      * 确保控制面组件的日志中没有 TLS 相关的错误信息。

      {{< note >}}
      要使用 `openssl` 命令行为集群生成新的证书和私钥，可参阅
      [证书（`openssl`）](/zh-cn/docs/tasks/administer-cluster/certificates/#openssl)。
      你也可以使用[`cfssl`](/zh-cn/docs/tasks/administer-cluster/certificates/#cfssl).
      {{< /note >}}

   4. 为 Daemonset 和 Deployment 添加注解，从而触发较安全的滚动更新，替换 Pod。

      ```shell
      for namespace in $(kubectl get namespace -o jsonpath='{.items[*].metadata.name}'); do
          for name in $(kubectl get deployments -n $namespace -o jsonpath='{.items[*].metadata.name}'); do
              kubectl patch deployment -n ${namespace} ${name} -p '{"spec":{"template":{"metadata":{"annotations":{"ca-rotation": "1"}}}}}';
          done
          for name in $(kubectl get daemonset -n $namespace -o jsonpath='{.items[*].metadata.name}'); do
              kubectl patch daemonset -n ${namespace} ${name} -p '{"spec":{"template":{"metadata":{"annotations":{"ca-rotation": "1"}}}}}';
          done
      done
      ```

      {{< note >}}
      要限制应用可能受到的并发干扰数量，
      可以参阅[配置 Pod 干扰预算](/zh-cn/docs/tasks/run-application/configure-pdb/)。
      {{< /note >}}

      取决于你在如何使用 StatefulSet，你可能需要对其执行类似的滚动替换操作。

10. 如果你的集群使用启动引导令牌来添加节点，则需要更新 `kube-public` 名字空间下的
    ConfigMap `cluster-info`，使之包含新的 CA 证书。

    ```shell
    base64_encoded_ca="$(base64 -w0 /etc/kubernetes/pki/ca.crt)"

    kubectl get cm/cluster-info --namespace kube-public -o yaml | \
       /bin/sed "s/\(certificate-authority-data:\).*/\1 ${base64_encoded_ca}/" | \
       kubectl apply -f -
    ```
11. 验证集群的功能正常。

    1. 检查控制面组件以及 `kubelet` 和 `kube-proxy` 的日志，确保其中没有抛出 TLS 错误，
       参阅[查看日志](/zh-cn/docs/tasks/debug/debug-cluster/#looking-at-logs)。

    2. 验证被聚合的 API 服务器的日志，以及所有使用集群内配置的 Pod 的日志。

12. 完成集群功能的检查之后：

    1. 更新所有的服务账号令牌，使之仅包含新的 CA 证书。

       * 使用集群内 kubeconfig 的 Pod 最终也需要被重启，以获得新的服务账号 Secret
         数据，这样就不会有 Pod 再依赖老的集群 CA。

    1. 从 kubeconfig 文件和 `--client-ca-file` 以及 `--root-ca-file` 标志所指向的文件
       中去除老的 CA 数据，之后重启控制面组件。

    1. 在每个节点上，移除 `clientCAFile` 标志所指向的文件，以删除老的 CA 数据，并从
       kubelet kubeconfig 文件中去掉老的 CA，重启 kubelet。
       你应该用滚动更新的方式来执行这一步骤的操作。

       如果你的集群允许你执行这一变更，你也可以通过替换节点而不是重新配置节点的方式来将其上线。


