---
title: 校验节点设置
weight: 30
---

{{< toc >}}

## 节点一致性测试    {#node-conformance-test}

**节点一致性测试** 是一个容器化的测试框架，提供了针对节点的系统验证和功能测试。
测试验证节点是否满足 Kubernetes 的最低要求；通过测试的节点有资格加入 Kubernetes 集群。

该测试主要检测节点是否满足 Kubernetes 的最低要求，通过检测的节点有资格加入 Kubernetes 集群。

## 节点的前提条件    {#node-prerequisite}

要运行节点一致性测试，节点必须满足与标准 Kubernetes 节点相同的前提条件。节点至少应安装以下守护程序：

* 容器运行时 (Docker)
* Kubelet

## 运行节点一致性测试    {#running-node-conformance-test}

要运行节点一致性测试，请执行以下步骤：

1. 得出 kubelet 的 `--kubeconfig` 的值；例如：`--kubeconfig=/var/lib/kubelet/config.yaml`。
   由于测试框架启动了本地控制平面来测试 kubelet，因此使用 `http://localhost:8080`
   作为API 服务器的 URL。
   一些其他的 kubelet 命令行参数可能会被用到：
   * `--cloud-provider`：如果使用 `--cloud-provider=gce`，需要移除这个参数来运行测试。


2. 使用以下命令运行节点一致性测试：

   ```shell
   # $CONFIG_DIR 是你 Kubelet 的 pod manifest 路径。
   # $LOG_DIR 是测试的输出路径。
   sudo docker run -it --rm --privileged --net=host \
     -v /:/rootfs -v $CONFIG_DIR:$CONFIG_DIR -v $LOG_DIR:/var/result \
     registry.k8s.io/node-test:0.2
   ```

## 针对其他硬件体系结构运行节点一致性测试    {#running-node-conformance-test-for-other-architectures}

Kubernetes 也为其他硬件体系结构的系统提供了节点一致性测试的 Docker 镜像：

  架构  |       镜像        |
--------|:-----------------:|
 amd64  |  node-test-amd64  |
  arm   |    node-test-arm  |
 arm64  |  node-test-arm64  |

## 运行特定的测试    {#running-selected-test}

要运行特定测试，请使用你希望运行的测试的特定表达式覆盖环境变量 `FOCUS`。

```shell
sudo docker run -it --rm --privileged --net=host \
  -v /:/rootfs:ro -v $CONFIG_DIR:$CONFIG_DIR -v $LOG_DIR:/var/result \
  -e FOCUS=MirrorPod \ # Only run MirrorPod test
  registry.k8s.io/node-test:0.2
```

要跳过特定的测试，请使用你希望跳过的测试的常规表达式覆盖环境变量 `SKIP`。

```shell
sudo docker run -it --rm --privileged --net=host \
  -v /:/rootfs:ro -v $CONFIG_DIR:$CONFIG_DIR -v $LOG_DIR:/var/result \
  -e SKIP=MirrorPod \ # 运行除 MirrorPod 测试外的所有一致性测试内容
  registry.k8s.io/node-test:0.2
```


节点一致性测试是[节点端到端测试](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-node/e2e-node-tests.md)的容器化版本。
默认情况下，它会运行所有一致性测试。

理论上，只要合理地配置容器和挂载所需的卷，就可以运行任何的节点端到端测试用例。但是这里**强烈建议只运行一致性测试**，因为运行非一致性测试需要很多复杂的配置。

## 注意事项    {#caveats}


* 测试会在节点上遗留一些 Docker 镜像，包括节点一致性测试本身的镜像和功能测试相关的镜像。
* 测试会在节点上遗留一些死的容器。这些容器是在功能测试的过程中创建的。