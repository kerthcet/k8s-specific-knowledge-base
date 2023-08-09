---
title: 调试运行中的 Pod
content_type: task
---


本页解释如何在节点上调试运行中（或崩溃）的 Pod。

## {{% heading "prerequisites" %}}

* 你的 {{< glossary_tooltip text="Pod" term_id="pod" >}} 应该已经被调度并正在运行中，
  如果你的 Pod 还没有运行，请参阅[调试 Pod](/zh-cn/docs/tasks/debug/debug-application/)。

* 对于一些高级调试步骤，你应该知道 Pod 具体运行在哪个节点上，并具有在该节点上运行命令的 shell 访问权限。
  你不需要任何访问权限就可以使用 `kubectl` 去运行一些标准调试步骤。

## 使用 `kubectl describe pod` 命令获取 Pod 详情

与之前的例子类似，我们使用一个 Deployment 来创建两个 Pod。

{{< codenew file="application/nginx-with-request.yaml" >}}

使用如下命令创建 Deployment：

```shell
kubectl apply -f https://k8s.io/examples/application/nginx-with-request.yaml
```

```
deployment.apps/nginx-deployment created
```

使用如下命令查看 Pod 状态：

```shell
kubectl get pods
```

```
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-67d4bdd6f5-cx2nz   1/1     Running   0          13s
nginx-deployment-67d4bdd6f5-w6kd7   1/1     Running   0          13s
```

我们可以使用 `kubectl describe pod` 命令来查询每个 Pod 的更多信息，比如：

```shell
kubectl describe pod nginx-deployment-67d4bdd6f5-w6kd7
```

```none
Name:         nginx-deployment-67d4bdd6f5-w6kd7
Namespace:    default
Priority:     0
Node:         kube-worker-1/192.168.0.113
Start Time:   Thu, 17 Feb 2022 16:51:01 -0500
Labels:       app=nginx
              pod-template-hash=67d4bdd6f5
Annotations:  <none>
Status:       Running
IP:           10.88.0.3
IPs:
  IP:           10.88.0.3
  IP:           2001:db8::1
Controlled By:  ReplicaSet/nginx-deployment-67d4bdd6f5
Containers:
  nginx:
    Container ID:   containerd://5403af59a2b46ee5a23fb0ae4b1e077f7ca5c5fb7af16e1ab21c00e0e616462a
    Image:          nginx
    Image ID:       docker.io/library/nginx@sha256:2834dc507516af02784808c5f48b7cbe38b8ed5d0f4837f16e78d00deb7e7767
    Port:           80/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Thu, 17 Feb 2022 16:51:05 -0500
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     500m
      memory:  128Mi
    Requests:
      cpu:        500m
      memory:     128Mi
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-bgsgp (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  kube-api-access-bgsgp:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   Guaranteed
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  34s   default-scheduler  Successfully assigned default/nginx-deployment-67d4bdd6f5-w6kd7 to kube-worker-1
  Normal  Pulling    31s   kubelet            Pulling image "nginx"
  Normal  Pulled     30s   kubelet            Successfully pulled image "nginx" in 1.146417389s
  Normal  Created    30s   kubelet            Created container nginx
  Normal  Started    30s   kubelet            Started container nginx
```

在这里，你可以看到有关容器和 Pod 的配置信息（标签、资源需求等），
以及有关容器和 Pod 的状态信息（状态、就绪、重启计数、事件等）。

容器状态是 Waiting、Running 和 Terminated 之一。
根据状态的不同，还有对应的额外的信息 —— 在这里你可以看到，
对于处于运行状态的容器，系统会告诉你容器的启动时间。

Ready 指示是否通过了最后一个就绪态探测。
(在本例中，容器没有配置就绪态探测；如果没有配置就绪态探测，则假定容器已经就绪。)

Restart Count 告诉你容器已重启的次数；
这些信息对于定位配置了 “Always” 重启策略的容器持续崩溃问题非常有用。

目前，唯一与 Pod 有关的状态是 Ready 状况，该状况表明 Pod 能够为请求提供服务，
并且应该添加到相应服务的负载均衡池中。

最后，你还可以看到与 Pod 相关的近期事件。
“From” 标明记录事件的组件，
“Reason” 和 “Message” 告诉你发生了什么。

## 例子: 调试 Pending 状态的 Pod

可以使用事件来调试的一个常见的场景是，你创建 Pod 无法被调度到任何节点。
比如，Pod 请求的资源比较多，没有任何一个节点能够满足，或者它指定了一个标签，没有节点可匹配。
假定我们创建之前的 Deployment 时指定副本数是 5（不再是 2），并且请求 600 毫核（不再是 500），
对于一个 4 个节点的集群，若每个节点只有 1 个 CPU，这时至少有一个 Pod 不能被调度。
（需要注意的是，其他集群插件 Pod，比如 fluentd、skydns 等等会在每个节点上运行，
如果我们需求 1000 毫核，将不会有 Pod 会被调度。）

```shell
kubectl get pods
```

```none
NAME                                READY     STATUS    RESTARTS   AGE
nginx-deployment-1006230814-6winp   1/1       Running   0          7m
nginx-deployment-1006230814-fmgu3   1/1       Running   0          7m
nginx-deployment-1370807587-6ekbw   1/1       Running   0          1m
nginx-deployment-1370807587-fg172   0/1       Pending   0          1m
nginx-deployment-1370807587-fz9sd   0/1       Pending   0          1m
```

为了查找 Pod nginx-deployment-1370807587-fz9sd 没有运行的原因，我们可以使用
`kubectl describe pod` 命令描述 Pod，查看其事件：

```shell
kubectl describe pod nginx-deployment-1370807587-fz9sd
```

```none
  Name:		nginx-deployment-1370807587-fz9sd
  Namespace:	default
  Node:		/
  Labels:		app=nginx,pod-template-hash=1370807587
  Status:		Pending
  IP:
  Controllers:	ReplicaSet/nginx-deployment-1370807587
  Containers:
    nginx:
      Image:	nginx
      Port:	80/TCP
      QoS Tier:
        memory:	Guaranteed
        cpu:	Guaranteed
      Limits:
        cpu:	1
        memory:	128Mi
      Requests:
        cpu:	1
        memory:	128Mi
      Environment Variables:
  Volumes:
    default-token-4bcbi:
      Type:	Secret (a volume populated by a Secret)
      SecretName:	default-token-4bcbi
  Events:
    FirstSeen	LastSeen	Count	From			        SubobjectPath	Type		Reason			    Message
    ---------	--------	-----	----			        -------------	--------	------			    -------
    1m		    48s		    7	    {default-scheduler }			        Warning		FailedScheduling	pod (nginx-deployment-1370807587-fz9sd) failed to fit in any node
  fit failure on node (kubernetes-node-6ta5): Node didn't have enough resource: CPU, requested: 1000, used: 1420, capacity: 2000
  fit failure on node (kubernetes-node-wul5): Node didn't have enough resource: CPU, requested: 1000, used: 1100, capacity: 2000
```

这里你可以看到由调度器记录的事件，它表明了 Pod 不能被调度的原因是 `FailedScheduling`（也可能是其他值）。
其 message 部分表明没有任何节点拥有足够多的资源。

要纠正这种情况，可以使用 `kubectl scale` 更新 Deployment，以指定 4 个或更少的副本。
(或者你可以让 Pod 继续保持这个状态，这是无害的。)

你在 `kubectl describe pod` 结尾处看到的事件都保存在 etcd 中，
并提供关于集群中正在发生的事情的高级信息。
如果需要列出所有事件，可使用命令：

```shell
kubectl get events
```

但是，需要注意的是，事件是区分名字空间的。
如果你对某些名字空间域的对象（比如 `my-namespace` 名字下的 Pod）的事件感兴趣,
你需要显式地在命令行中指定名字空间：

```shell
kubectl get events --namespace=my-namespace
```

查看所有 namespace 的事件，可使用 `--all-namespaces` 参数。

除了 `kubectl describe pod` 以外，另一种获取 Pod 额外信息（除了 `kubectl get pod`）的方法
是给 `kubectl get pod` 增加 `-o yaml` 输出格式参数。
该命令将以 YAML 格式为你提供比 `kubectl describe pod` 更多的信息 —— 实际上是系统拥有的关于 Pod 的所有信息。
在这里，你将看到注解（没有标签限制的键值元数据，由 Kubernetes 系统组件在内部使用）、
重启策略、端口和卷等。

```shell
kubectl get pod nginx-deployment-1006230814-6winp -o yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2022-02-17T21:51:01Z"
  generateName: nginx-deployment-67d4bdd6f5-
  labels:
    app: nginx
    pod-template-hash: 67d4bdd6f5
  name: nginx-deployment-67d4bdd6f5-w6kd7
  namespace: default
  ownerReferences:
  - apiVersion: apps/v1
    blockOwnerDeletion: true
    controller: true
    kind: ReplicaSet
    name: nginx-deployment-67d4bdd6f5
    uid: 7d41dfd4-84c0-4be4-88ab-cedbe626ad82
  resourceVersion: "1364"
  uid: a6501da1-0447-4262-98eb-c03d4002222e
spec:
  containers:
  - image: nginx
    imagePullPolicy: Always
    name: nginx
    ports:
    - containerPort: 80
      protocol: TCP
    resources:
      limits:
        cpu: 500m
        memory: 128Mi
      requests:
        cpu: 500m
        memory: 128Mi
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-bgsgp
      readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: kube-worker-1
  preemptionPolicy: PreemptLowerPriority
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: default
  serviceAccountName: default
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
  volumes:
  - name: kube-api-access-bgsgp
    projected:
      defaultMode: 420
      sources:
      - serviceAccountToken:
          expirationSeconds: 3607
          path: token
      - configMap:
          items:
          - key: ca.crt
            path: ca.crt
          name: kube-root-ca.crt
      - downwardAPI:
          items:
          - fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
            path: namespace
status:
  conditions:
  - lastProbeTime: null
    lastTransitionTime: "2022-02-17T21:51:01Z"
    status: "True"
    type: Initialized
  - lastProbeTime: null
    lastTransitionTime: "2022-02-17T21:51:06Z"
    status: "True"
    type: Ready
  - lastProbeTime: null
    lastTransitionTime: "2022-02-17T21:51:06Z"
    status: "True"
    type: ContainersReady
  - lastProbeTime: null
    lastTransitionTime: "2022-02-17T21:51:01Z"
    status: "True"
    type: PodScheduled
  containerStatuses:
  - containerID: containerd://5403af59a2b46ee5a23fb0ae4b1e077f7ca5c5fb7af16e1ab21c00e0e616462a
    image: docker.io/library/nginx:latest
    imageID: docker.io/library/nginx@sha256:2834dc507516af02784808c5f48b7cbe38b8ed5d0f4837f16e78d00deb7e7767
    lastState: {}
    name: nginx
    ready: true
    restartCount: 0
    started: true
    state:
      running:
        startedAt: "2022-02-17T21:51:05Z"
  hostIP: 192.168.0.113
  phase: Running
  podIP: 10.88.0.3
  podIPs:
  - ip: 10.88.0.3
  - ip: 2001:db8::1
  qosClass: Guaranteed
  startTime: "2022-02-17T21:51:01Z"
```

## 检查 Pod 的日志 {#examine-pod-logs}

首先，查看受到影响的容器的日志：

```shell
kubectl logs ${POD_NAME} ${CONTAINER_NAME}
```

如果你的容器之前崩溃过，你可以通过下面命令访问之前容器的崩溃日志：

```shell
kubectl logs --previous ${POD_NAME} ${CONTAINER_NAME}
```

## 使用容器 exec 进行调试 {#container-exec}

如果 {{< glossary_tooltip text="容器镜像" term_id="image" >}} 包含调试程序，
比如从 Linux 和 Windows 操作系统基础镜像构建的镜像，你可以使用 `kubectl exec` 命令
在特定的容器中运行一些命令：

```shell
kubectl exec ${POD_NAME} -c ${CONTAINER_NAME} -- ${CMD} ${ARG1} ${ARG2} ... ${ARGN}
```

{{< note >}}
`-c ${CONTAINER_NAME}` 是可选择的。如果 Pod 中仅包含一个容器，就可以忽略它。
{{< /note >}}

例如，要查看正在运行的 Cassandra Pod 中的日志，可以运行：

```shell
kubectl exec cassandra -- cat /var/log/cassandra/system.log
```

你可以在 `kubectl exec` 命令后面加上 `-i` 和 `-t` 来运行一个连接到你的终端的 Shell，比如：

```shell
kubectl exec -it cassandra -- sh
```

若要了解更多内容，可查看[获取正在运行容器的 Shell](/zh-cn/docs/tasks/debug/debug-application/get-shell-running-container/)。

## 使用临时调试容器来进行调试 {#ephemeral-container}

{{< feature-state state="stable" for_k8s_version="v1.25" >}}

当由于容器崩溃或容器镜像不包含调试程序（例如[无发行版镜像](https://github.com/GoogleContainerTools/distroless)等）
而导致 `kubectl exec` 无法运行时，{{< glossary_tooltip text="临时容器" term_id="ephemeral-container" >}}对于排除交互式故障很有用。

## 使用临时容器来调试的例子 {#ephemeral-container-example}

你可以使用 `kubectl debug` 命令来给正在运行中的 Pod 增加一个临时容器。
首先，像示例一样创建一个 pod：

```shell
kubectl run ephemeral-demo --image=registry.k8s.io/pause:3.1 --restart=Never
```

本节示例中使用 `pause` 容器镜像，因为它不包含调试程序，但是这个方法适用于所有容器镜像。

如果你尝试使用 `kubectl exec` 来创建一个 shell，你将会看到一个错误，因为这个容器镜像中没有 shell。

```shell
kubectl exec -it ephemeral-demo -- sh
```

```
OCI runtime exec failed: exec failed: container_linux.go:346: starting container process caused "exec: \"sh\": executable file not found in $PATH": unknown
```


你可以改为使用 `kubectl debug` 添加调试容器。
如果你指定 `-i` 或者 `--interactive` 参数，`kubectl` 将自动挂接到临时容器的控制台。

```shell
kubectl debug -it ephemeral-demo --image=busybox:1.28 --target=ephemeral-demo
```

```
Defaulting debug container name to debugger-8xzrl.
If you don't see a command prompt, try pressing enter.
/ #
```

此命令添加一个新的 busybox 容器并将其挂接到该容器。`--target` 参数指定另一个容器的进程命名空间。
这个指定进程命名空间的操作是必需的，因为 `kubectl run` 不能在它创建的 Pod
中启用[共享进程命名空间](/zh-cn/docs/tasks/configure-pod-container/share-process-namespace/)。

{{< note >}}
{{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}必须支持 `--target` 参数。
如果不支持，则临时容器可能不会启动，或者可能使用隔离的进程命名空间启动，
以便 `ps` 不显示其他容器内的进程。
{{< /note >}}

你可以使用 `kubectl describe` 查看新创建的临时容器的状态：

```shell
kubectl describe pod ephemeral-demo
```

```
...
Ephemeral Containers:
  debugger-8xzrl:
    Container ID:   docker://b888f9adfd15bd5739fefaa39e1df4dd3c617b9902082b1cfdc29c4028ffb2eb
    Image:          busybox
    Image ID:       docker-pullable://busybox@sha256:1828edd60c5efd34b2bf5dd3282ec0cc04d47b2ff9caa0b6d4f07a21d1c08084
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Wed, 12 Feb 2020 14:25:42 +0100
    Ready:          False
    Restart Count:  0
    Environment:    <none>
    Mounts:         <none>
...
```

使用 `kubectl delete` 来移除已经结束掉的 Pod：

```shell
kubectl delete pod ephemeral-demo
```

## 通过 Pod 副本调试 {#debugging-using-a-copy-of-the-pod}

有些时候 Pod 的配置参数使得在某些情况下很难执行故障排查。
例如，在容器镜像中不包含 shell 或者你的应用程序在启动时崩溃的情况下，
就不能通过运行 `kubectl exec` 来排查容器故障。
在这些情况下，你可以使用 `kubectl debug` 来创建 Pod 的副本，通过更改配置帮助调试。

### 在添加新的容器时创建 Pod 副本

当应用程序正在运行但其表现不符合预期时，你会希望在 Pod 中添加额外的调试工具，
这时添加新容器是很有用的。

例如，应用的容器镜像是建立在 `busybox` 的基础上，
但是你需要 `busybox` 中并不包含的调试工具。
你可以使用 `kubectl run` 模拟这个场景:

```shell
kubectl run myapp --image=busybox:1.28 --restart=Never -- sleep 1d
```

通过运行以下命令，建立 `myapp` 的一个名为 `myapp-debug` 的副本，
新增了一个用于调试的 Ubuntu 容器，

```shell
kubectl debug myapp -it --image=ubuntu --share-processes --copy-to=myapp-debug
```

```
Defaulting debug container name to debugger-w7xmf.
If you don't see a command prompt, try pressing enter.
root@myapp-debug:/#
```

{{< note >}}
* 如果你没有使用 `--container` 指定新的容器名，`kubectl debug` 会自动生成的。
* 默认情况下，`-i` 标志使 `kubectl debug` 附加到新容器上。
  你可以通过指定 `--attach=false` 来防止这种情况。
  如果你的会话断开连接，你可以使用 `kubectl attach` 重新连接。
* `--share-processes` 允许在此 Pod 中的其他容器中查看该容器的进程。
  参阅[在 Pod 中的容器之间共享进程命名空间](/zh-cn/docs/tasks/configure-pod-container/share-process-namespace/)
  获取更多信息。
{{< /note >}}

不要忘了清理调试 Pod：

```shell
kubectl delete pod myapp myapp-debug
```

### 在改变 Pod 命令时创建 Pod 副本

有时更改容器的命令很有用，例如添加调试标志或因为应用崩溃。

为了模拟应用崩溃的场景，使用 `kubectl run` 命令创建一个立即退出的容器：

```
kubectl run --image=busybox:1.28 myapp -- false
```

使用 `kubectl describe pod myapp` 命令，你可以看到容器崩溃了：

```
Containers:
  myapp:
    Image:         busybox
    ...
    Args:
      false
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       Error
      Exit Code:    1
```

你可以使用 `kubectl debug` 命令创建该 Pod 的一个副本，
在该副本中命令改变为交互式 shell：

```
kubectl debug myapp -it --copy-to=myapp-debug --container=myapp -- sh
```

```
If you don't see a command prompt, try pressing enter.
/ #
```

现在你有了一个可以执行类似检查文件系统路径或者手动运行容器命令的交互式 shell。 

{{< note >}}
* 要更改指定容器的命令，你必须用 `--container` 命令指定容器的名字，
  否则 `kubectl debug` 将建立一个新的容器运行你指定的命令。
* 默认情况下，标志 `-i` 使 `kubectl debug` 附加到容器。
  你可通过指定 `--attach=false` 来防止这种情况。
  如果你的断开连接，可以使用 `kubectl attach` 重新连接。
{{< /note >}} 

不要忘了清理调试 Pod：

```shell
kubectl delete pod myapp myapp-debug
```

### 在更改容器镜像时拷贝 Pod

在某些情况下，你可能想要改动一个行为异常的 Pod，即从其正常的生产容器镜像更改为包含调试构建程序或其他实用程序的镜像。

下面的例子，用 `kubectl run` 创建一个 Pod：

```
kubectl run myapp --image=busybox:1.28 --restart=Never -- sleep 1d
```

现在可以使用 `kubectl debug` 创建一个拷贝并将其容器镜像更改为 `ubuntu`：

```
kubectl debug myapp --copy-to=myapp-debug --set-image=*=ubuntu
```

`--set-image` 与 `container_name=image` 使用相同的 `kubectl set image` 语法。
`*=ubuntu` 表示把所有容器的镜像改为 `ubuntu`。

```shell
kubectl delete pod myapp myapp-debug
```

## 在节点上通过 shell 来进行调试 {#node-shell-session}

如果这些方法都不起作用，你可以找到运行 Pod 的节点，然后创建一个 Pod 运行在该节点上。
你可以通过 `kubectl debug` 在节点上创建一个交互式 Shell：

```shell
kubectl debug node/mynode -it --image=ubuntu
```

```
Creating debugging pod node-debugger-mynode-pdx84 with container debugger on node mynode.
If you don't see a command prompt, try pressing enter.
root@ek8s:/#
```

当在节点上创建调试会话，注意以下要点：
* `kubectl debug` 基于节点的名字自动生成新的 Pod 的名字。
* 节点的根文件系统会被挂载在 `/host`。
* 新的调试容器运行在主机 IPC 名字空间、主机网络名字空间以及主机 PID 名字空间内，
  Pod 没有特权，因此读取某些进程信息可能会失败，并且 `chroot /host` 也可能会失败。
* 如果你需要一个特权 Pod，需要手动创建。

当你完成节点调试时，不要忘记清理调试 Pod：

```shell
kubectl delete pod node-debugger-mynode-pdx84
```
