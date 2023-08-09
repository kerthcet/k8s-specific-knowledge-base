---
title: "Kubernetes 和 Docker 简单的 leader election"
date: 2016-01-11
slug: simple-leader-election-with-kubernetes
---

#### 概述

Kubernetes 简化了集群上运行的服务的部署和操作管理。但是，它也简化了这些服务的发展。在本文中，我们将看到如何使用 Kubernetes 在分布式应用程序中轻松地执行 leader election。分布式应用程序通常为了可靠性和可伸缩性而复制服务的任务，但通常需要指定其中一个副本作为负责所有副本之间协调的负责人。


通常在 leader election 中，会确定一组成为领导者的候选人。这些候选人都竞相宣布自己为领袖。其中一位候选人获胜并成为领袖。一旦选举获胜，领导者就会不断地“信号”以表示他们作为领导者的地位，其他候选人也会定期地做出新的尝试来成为领导者。这样可以确保在当前领导因某种原因失败时，快速确定新领导。


实现 leader election 通常需要部署 ZooKeeper、etcd 或 Consul 等软件并将其用于协商一致，或者也可以自己实现协商一致算法。我们将在下面看到，Kubernetes 使在应用程序中使用 leader election 的过程大大简化。

####在 Kubernetes 实施领导人选举


Leader election 的首要条件是确定候选人的人选。Kubernetes 已经使用 _Endpoints_ 来表示组成服务的一组复制 pod，因此我们将重用这个相同的对象。（旁白：您可能认为我们会使用 _ReplicationControllers_，但它们是绑定到特定的二进制文件，而且通常您希望只有一个领导者，即使您正在执行滚动更新）

要执行 leader election，我们使用所有 Kubernetes api 对象的两个属性：


* ResourceVersions - 每个 API 对象都有一个惟一的 ResourceVersion，您可以使用这些版本对 Kubernetes 对象执行比较和交换
* Annotations - 每个 API 对象都可以用客户端使用的任意键/值对进行注释。

给定这些原语，使用 master election 的代码相对简单，您可以在这里找到[here][1]。我们自己来做吧。


```
$ kubectl run leader-elector --image=gcr.io/google_containers/leader-elector:0.4 --replicas=3 -- --election=example
```

这将创建一个包含3个副本的 leader election 集合：

```
$ kubectl get pods
NAME                   READY     STATUS    RESTARTS   AGE
leader-elector-inmr1   1/1       Running   0          13s
leader-elector-qkq00   1/1       Running   0          13s
leader-elector-sgwcq   1/1       Running   0          13s
```


要查看哪个pod被选为领导，您可以访问其中一个 pod 的日志，用您自己的一个 pod 的名称替换

```
${pod_name}, (e.g. leader-elector-inmr1 from the above)

$ kubectl logs -f ${name}
leader is (leader-pod-name)
```
…或者，可以直接检查 endpoints 对象：


_'example' 是上面 kubectl run … 命令_中候选集的名称
```
$ kubectl get endpoints example -o yaml
```
现在，要验证 leader election 是否实际有效，请在另一个终端运行：
```
$ kubectl delete pods (leader-pod-name)
```


这将删除现有领导。由于 pod 集由 replication controller 管理，因此新的 pod 将替换已删除的pod，确保复制集的大小仍为3。通过 leader election，这三个pod中的一个被选为新的领导者，您应该会看到领导者故障转移到另一个pod。因为 Kubernetes 的吊舱在终止前有一个 _grace period_，这可能需要30-40秒。

Leader-election container 提供了一个简单的 web 服务器，可以服务于任何地址(e.g. http://localhost:4040)。您可以通过删除现有的 leader election 组并创建一个新的 leader elector 组来测试这一点，在该组中，您还可以向 leader elector 映像传递--http=(host):(port) 规范。这将导致集合中的每个成员通过 webhook 提供有关领导者的信息。


```
# delete the old leader elector group
$ kubectl delete rc leader-elector

# create the new group, note the --http=localhost:4040 flag
$ kubectl run leader-elector --image=gcr.io/google_containers/leader-elector:0.4 --replicas=3 -- --election=example --http=0.0.0.0:4040

# create a proxy to your Kubernetes api server
$ kubectl proxy
```


然后您可以访问：




http://localhost:8001/api/v1/proxy/namespaces/default/pods/(leader-pod-name):4040/




你会看到：

```
{"name":"(name-of-leader-here)"}
```
####  有副手的 leader election


好吧，那太好了，你可以通过 HTTP 进行leader election 并找到 leader，但是你如何从自己的应用程序中使用它呢？这就是 sidecar 的由来。Kubernetes  中，Pods 由一个或多个容器组成。通常情况下，这意味着您将 sidecar containers 添加到主应用程序中以组成 pod。（关于这个主题的更详细的处理，请参阅我之前的博客文章）。
Leader-election container 可以作为一个 sidecar，您可以从自己的应用程序中使用。Pod 中任何对当前 master 感兴趣的容器都可以简单地访问http://localhost:4040，它们将返回一个包含当前 master 名称的简单 json 对象。由于 pod中 的所有容器共享相同的网络命名空间，因此不需要服务发现！


例如，这里有一个简单的 Node.js 应用程序，它连接到 leader election sidecar 并打印出它当前是否是 master。默认情况下，leader election sidecar 将其标识符设置为 `hostname`。

```
var http = require('http');
// This will hold info about the current master
var master = {};

  // The web handler for our nodejs application
  var handleRequest = function(request, response) {
    response.writeHead(200);
    response.end("Master is " + master.name);
  };

  // A callback that is used for our outgoing client requests to the sidecar
  var cb = function(response) {
    var data = '';
    response.on('data', function(piece) { data = data + piece; });
    response.on('end', function() { master = JSON.parse(data); });
  };

  // Make an async request to the sidecar at http://localhost:4040
  var updateMaster = function() {
    var req = http.get({host: 'localhost', path: '/', port: 4040}, cb);
    req.on('error', function(e) { console.log('problem with request: ' + e.message); });
    req.end();
  };

  / / Set up regular updates
  updateMaster();
  setInterval(updateMaster, 5000);

  // set up the web server
  var www = http.createServer(handleRequest);
  www.listen(8080);
  ```
 当然，您可以从任何支持 HTTP 和 JSON 的语言中使用这个 sidecar。


#### 结论


 希望我已经向您展示了使用 Kubernetes 为您的分布式应用程序构建 leader election 是多么容易。在以后的部分中，我们将向您展示 Kubernetes 如何使构建分布式系统变得更加容易。同时，转到[Google Container Engine][2]或[kubernetes.io][3]开始使用Kubernetes。

  [1]: https://github.com/kubernetes/contrib/pull/353
  [2]: https://cloud.google.com/container-engine/
  [3]: http://kubernetes.io/