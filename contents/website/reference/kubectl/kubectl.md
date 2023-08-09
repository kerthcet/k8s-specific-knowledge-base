---
title: kubectl
content_type: tool-reference
weight: 30
---

## {{% heading "synopsis" %}}

kubectl 管理控制 Kubernetes 集群。

获取更多信息，请访问 [kubectl 概述](/zh-cn/docs/reference/kubectl/)。

```
kubectl [flags]
```

## {{% heading "options" %}}

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>
    <tr>
      <td colspan="2">--add-dir-header</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      设置为 true 表示添加文件目录到日志信息头中
      </td>
    </tr>
    <tr>
      <td colspan="2">--alsologtostderr</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      表示将日志输出到文件的同时输出到 stderr
      </td>
    </tr>
    <tr>
      <td colspan="2">--as string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      以指定用户的身份执行操作
      </td>
    </tr>
    <tr>
      <td colspan="2">--as-group stringArray</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      模拟指定的组来执行操作，可以使用这个标志来指定多个组。
      </td>
    </tr>
    <tr>
      <td colspan="2">--azure-container-registry-config string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      包含 Azure 容器仓库配置信息的文件的路径。
      </td>
    </tr>
    <tr>
      <td colspan="2">--cache-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: "$HOME/.kube/cache"</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      默认缓存目录
      </td>
    </tr>
    <tr>
      <td colspan="2">--certificate-authority string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      指向证书机构的 cert 文件路径
      </td>
    </tr>
    <tr>
      <td colspan="2">--client-certificate string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      TLS 使用的客户端证书路径
      </td>
    </tr>
    <tr>
      <td colspan="2">--client-key string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      TLS 使用的客户端密钥文件路径
      </td>
    </tr>
    <tr>
      <td colspan="2">--cloud-provider-gce-l7lb-src-cidrs cidrs&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: 130.211.0.0/22,35.191.0.0/16</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
        在 GCE 防火墙中开放的 CIDR，用来进行 L7 LB 流量代理和健康检查。
      </td>
    </tr>
    <tr>
      <td colspan="2">--cloud-provider-gce-lb-src-cidrs cidrs&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: 130.211.0.0/22,209.85.152.0/22,209.85.204.0/22,35.191.0.0/16</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      在 GCE 防火墙中开放的 CIDR，用来进行 L4 LB 流量代理和健康检查。
      </td>
    </tr>
    <tr>
      <td colspan="2">--cluster string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      要使用的 kubeconfig 集群的名称
      </td>
    </tr>
    <tr>
      <td colspan="2">--context string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      要使用的 kubeconfig 上下文的名称
      </td>
    </tr>
    <tr>
      <td colspan="2">--default-not-ready-toleration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: 300</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      表示 `notReady` 状态的容忍度秒数：默认情况下，`NoExecute` 被添加到尚未具有此容忍度的每个 Pod 中。
      </td>
    </tr>
    <tr>
      <td colspan="2">--default-unreachable-toleration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: 300</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      表示 `unreachable` 状态的容忍度秒数：默认情况下，`NoExecute` 被添加到尚未具有此容忍度的每个 Pod 中。
      </td>
    </tr>
    <tr>
      <td colspan="2">-h, --help</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      kubectl 操作的帮助命令
      </td>
    </tr>
    <tr>
      <td colspan="2">--insecure-skip-tls-verify</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      设置为 true，则表示不会检查服务器证书的有效性。这样会导致你的 HTTPS 连接不安全。
      </td>
    </tr>
    <tr>
      <td colspan="2">--kubeconfig string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      CLI 请求使用的 kubeconfig 配置文件的路径。
      </td>
    </tr>
    <tr>
      <td colspan="2">--log-backtrace-at traceLocation&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: 0</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      当日志机制运行到指定文件的指定行（file:N）时，打印调用堆栈信息
      </td>
    </tr>
    <tr>
      <td colspan="2">--log-dir string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      如果不为空，则将日志文件写入此目录
      </td>
    </tr>
    <tr>
      <td colspan="2">--log-file string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      如果不为空，则将使用此日志文件
      </td>
    </tr>
    <tr>
      <td colspan="2">--log-file-max-size uint&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: 1800</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      定义日志文件的最大尺寸。单位为兆字节。如果值设置为 0，则表示日志文件大小不受限制。
      </td>
    </tr>
    <tr>
      <td colspan="2">--log-flush-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: 5s</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      两次日志刷新操作之间的最长时间（秒）
      </td>
    </tr>
    <tr>
      <td colspan="2">--logtostderr&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: true</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      日志输出到 stderr 而不是文件中
      </td>
    </tr>
    <tr>
      <td colspan="2">--match-server-version</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      要求客户端版本和服务端版本相匹配
      </td>
    </tr>
    <tr>
      <td colspan="2">-n, --namespace string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      如果存在，CLI 请求将使用此命名空间
      </td>
    <tr>
      <td colspan="2">--one-output</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      如果为 true，则只将日志写入初始严重级别（而不是同时写入所有较低的严重级别）。
      </td>
    </tr>
    </tr>
    <tr>
      <td colspan="2">--password string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      API 服务器进行基本身份验证的密码
      </td>
    </tr>
    <tr>
      <td colspan="2">--profile string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: "none"</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      要记录的性能指标的名称。可取 (none|cpu|heap|goroutine|threadcreate|block|mutex) 其中之一。
      </td>
    </tr>
    <tr>
      <td colspan="2">--profile-output string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: "profile.pprof"</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      用于转储所记录的性能信息的文件名
      </td>
    </tr>
    <tr>
      <td colspan="2">--request-timeout string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: "0"</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      放弃单个服务器请求之前的等待时间，非零值需要包含相应时间单位（例如：1s、2m、3h）。零值则表示不做超时要求。
      </td>
    </tr>
    <tr>
      <td colspan="2">-s, --server string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      Kubernetes API 服务器的地址和端口
      </td>
    </tr>
    <tr>
      <td colspan="2">--skip-headers</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      设置为 true 则表示跳过在日志消息中出现 header 前缀信息
      </td>
    </tr>
    <tr>
      <td colspan="2">--skip-log-headers</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      设置为 true 则表示在打开日志文件时跳过 header 信息
      </td>
    </tr>
    <tr>
      <td colspan="2">--stderrthreshold severity&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值: 2</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      等于或高于此阈值的日志将输出到标准错误输出（stderr）
      </td>
    </tr>
    <tr>
      <td colspan="2">--token string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      用于对 API 服务器进行身份认证的持有者令牌
      </td>
    </tr>
    <tr>
      <td colspan="2">--user string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      指定使用 kubeconfig 配置文件中的用户名
      </td>
    </tr>
    <tr>
      <td colspan="2">--username string</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      用于 API 服务器的基本身份验证的用户名
      </td>
    </tr>
    <tr>
      <td colspan="2">-v, --v Level</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      指定输出日志的日志详细级别
      </td>
    </tr>
    <tr>
      <td colspan="2">--version version[=true]</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      打印 kubectl 版本信息并退出
      </td>
    </tr>
    <tr>
      <td colspan="2">--vmodule moduleSpec</td>
    </tr>
    <tr>
      <td></td><td style="line-height: 130%; word-wrap: break-word;">
      以逗号分隔的 pattern=N 设置列表，用于过滤文件的日志记录
      </td>
    </tr>
  </tbody>
</table>

## {{% heading "envvars" %}}

<table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">KUBECONFIG</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
kubectl 的配置 ("kubeconfig") 文件的路径。默认值: "$HOME/.kube/config"
</td>
</tr>

<tr>
<td colspan="2">KUBECTL_COMMAND_HEADERS</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
设置为 false 时，将关闭额外的 HTTP 标头，不再详细说明被调用的 kubectl 命令（此变量适用于 Kubernetes v1.22 或更高版本）
</td>
</tr>

<tr>
<td colspan="2">KUBECTL_EXPLAIN_OPENAPIV3</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
切换对 `kubectl explain` 的调用是否使用可用的新 OpenAPIv3 数据源。OpenAPIV3 自 Kubernetes 1.24 起默认被启用。
</td>
</tr>

<tr>
<td colspan="2">KUBECTL_ENABLE_CMD_SHADOW</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
当设置为 true 时，如果子命令不存在，外部插件可以用作内置命令的子命令。
此功能处于 alpha 阶段，只能用于 create 命令（例如 kubectl create networkpolicy）。
</td>
</tr>

</tbody>
</table>

## {{% heading "seealso" %}}

* [kubectl annotate](/docs/reference/generated/kubectl/kubectl-commands#annotate)	 - 更新资源所关联的注解
* [kubectl api-resources](/docs/reference/generated/kubectl/kubectl-commands#api-resources)	 - 打印服务器上所支持的 API 资源
* [kubectl api-versions](/docs/reference/generated/kubectl/kubectl-commands#api-versions)	 - 以“组/版本”的格式输出服务端所支持的 API 版本
* [kubectl apply](/docs/reference/generated/kubectl/kubectl-commands#apply)	 - 基于文件名或标准输入，将新的配置应用到资源上
* [kubectl attach](/docs/reference/generated/kubectl/kubectl-commands#attach)	 - 连接到一个正在运行的容器
* [kubectl auth](/docs/reference/generated/kubectl/kubectl-commands#auth)	 - 检查授权信息
* [kubectl autoscale](/docs/reference/generated/kubectl/kubectl-commands#autoscale)	 - 对一个资源对象（Deployment、ReplicaSet 或 ReplicationController ）进行扩缩
* [kubectl certificate](/docs/reference/generated/kubectl/kubectl-commands#certificate)	 - 修改证书资源
* [kubectl cluster-info](/docs/reference/generated/kubectl/kubectl-commands#cluster-info)	 - 显示集群信息
* [kubectl completion](/docs/reference/generated/kubectl/kubectl-commands#completion)	 - 根据已经给出的 Shell（bash 或 zsh），输出 Shell 补全后的代码
* [kubectl config](/docs/reference/generated/kubectl/kubectl-commands#config)	 - 修改 kubeconfig 配置文件
* [kubectl convert](/docs/reference/generated/kubectl/kubectl-commands#convert)	 - 在不同的 API 版本之间转换配置文件
* [kubectl cordon](/docs/reference/generated/kubectl/kubectl-commands#cordon)	 - 标记节点为不可调度的
* [kubectl cp](/docs/reference/generated/kubectl/kubectl-commands#cp)	 - 将文件和目录拷入/拷出容器
* [kubectl create](/docs/reference/generated/kubectl/kubectl-commands#create)	 - 通过文件或标准输入来创建资源
* [kubectl debug](/docs/reference/generated/kubectl/kubectl-commands#debug)	 - 创建用于排查工作负载和节点故障的调试会话
* [kubectl delete](/docs/reference/generated/kubectl/kubectl-commands#delete)	 - 通过文件名、标准输入、资源和名字删除资源，或者通过资源和标签选择算符来删除资源
* [kubectl describe](/docs/reference/generated/kubectl/kubectl-commands#describe)	 - 显示某个资源或某组资源的详细信息
* [kubectl diff](/docs/reference/generated/kubectl/kubectl-commands#diff)	 - 显示目前版本与将要应用的版本之间的差异
* [kubectl drain](/docs/reference/generated/kubectl/kubectl-commands#drain)	 - 腾空节点，准备维护
* [kubectl edit](/docs/reference/generated/kubectl/kubectl-commands#edit)	 - 修改服务器上的某资源
* [kubectl events](/docs/reference/generated/kubectl/kubectl-commands#events)  - 列举事件
* [kubectl exec](/docs/reference/generated/kubectl/kubectl-commands#exec)	 - 在容器中执行相关命令
* [kubectl explain](/docs/reference/generated/kubectl/kubectl-commands#explain)	 - 显示资源文档说明
* [kubectl expose](/docs/reference/generated/kubectl/kubectl-commands#expose)	 - 给定副本控制器、服务、Deployment 或 Pod，将其暴露为新的 kubernetes Service
* [kubectl get](/docs/reference/generated/kubectl/kubectl-commands#get)	 - 显示一个或者多个资源信息
* [kubectl kustomize](/docs/reference/generated/kubectl/kubectl-commands#kustomize)	 - 从目录或远程 URL 中构建 kustomization
* [kubectl label](/docs/reference/generated/kubectl/kubectl-commands#label)	 - 更新资源的标签
* [kubectl logs](/docs/reference/generated/kubectl/kubectl-commands#logs)	 - 输出 Pod 中某容器的日志
* [kubectl options](/docs/reference/generated/kubectl/kubectl-commands#options)	 - 打印所有命令都支持的共有参数列表
* [kubectl patch](/docs/reference/generated/kubectl/kubectl-commands#patch)	 - 基于策略性合并修补（Stategic Merge Patch）规则更新某资源中的字段
* [kubectl plugin](/docs/reference/generated/kubectl/kubectl-commands#plugin)	 - 运行命令行插件
* [kubectl port-forward](/docs/reference/generated/kubectl/kubectl-commands#port-forward)	 - 将一个或者多个本地端口转发到 Pod
* [kubectl proxy](/docs/reference/generated/kubectl/kubectl-commands#proxy)	 - 运行一个 kubernetes API 服务器代理
* [kubectl replace](/docs/reference/generated/kubectl/kubectl-commands#replace)	 - 基于文件名或标准输入替换资源
* [kubectl rollout](/docs/reference/generated/kubectl/kubectl-commands#rollout)	 - 管理资源的上线
* [kubectl run](/docs/reference/generated/kubectl/kubectl-commands#run)	 - 在集群中使用指定镜像启动容器
* [kubectl scale](/docs/reference/generated/kubectl/kubectl-commands#scale)	 - 为一个 Deployment、ReplicaSet 或 ReplicationController 设置一个新的规模值
* [kubectl set](/docs/reference/generated/kubectl/kubectl-commands#set)	 - 为对象设置功能特性
* [kubectl taint](/docs/reference/generated/kubectl/kubectl-commands#taint)	 - 在一个或者多个节点上更新污点配置
* [kubectl top](/docs/reference/generated/kubectl/kubectl-commands#top)	 - 显示资源（CPU/内存/存储）使用率
* [kubectl uncordon](/docs/reference/generated/kubectl/kubectl-commands#uncordon)	 - 标记节点为可调度的
* [kubectl version](/docs/reference/generated/kubectl/kubectl-commands#version)	 - 打印客户端和服务器的版本信息
* [kubectl wait](/docs/reference/generated/kubectl/kubectl-commands#wait)	 - 实验性：等待一个或多个资源达到某种状态
