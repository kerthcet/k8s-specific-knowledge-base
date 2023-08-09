---
layout: blog
title: "Kubernetes 的容器检查点分析"
date: 2023-03-10
slug: forensic-container-analysis
---

**作者:** [Adrian Reber](https://github.com/adrianreber) (Red Hat)

**译者**：[Paco Xu](https://github.com/pacoxu) (Daocloud)

在我之前的文章 [Kubernetes 中的取证容器检查点][forensic-blog] 中，我介绍了检查点以及如何创建和使用它。
该特性的名称是取证容器检查点，但我没有详细介绍如何对 Kubernetes 创建的检查点进行实际分析。
在本文中，我想提供如何分析检查点的详细信息。

检查点仍然是 Kubernetes 中的一个 alpha 功能，本文希望提供该功能未来如何工作的预览。

## 准备

有关如何配置 Kubernetes 和底层 CRI 实现以启用检查点支持的详细信息，请参阅 [Kubernetes 中的取证容器检查点][forensic-blog]文章。

作为示例，我准备了一个容器镜像（`quay.io/adrianreber/counter:blog`），我想对其进行检查点，然后在本文中进行分析。
这个容器允许我在容器中创建文件，并将信息存储在内存中，稍后我想在检查点中找到这些信息。

要运行该容器，我需要一个 pod，在本示例中，我使用以下 Pod 清单：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: counters
spec:
  containers:
  - name: counter
    image: quay.io/adrianreber/counter:blog
```

这会导致一个名为 `counter` 的容器在名为 `counters` 的 Pod 中运行。

容器运行后，我将对该容器执行以下操作：

```console
$ kubectl get pod counters --template '{{.status.podIP}}'
10.88.0.25
$ curl 10.88.0.25:8088/create?test-file
$ curl 10.88.0.25:8088/secret?RANDOM_1432_KEY
$ curl 10.88.0.25:8088
```

1. 第一次访问在容器中创建一个名为 `test-file` 的文件，其内容为 `test-file`;
2. 第二次访问将我的秘密信息（`RANDOM_1432_KEY`）存储在容器内存中的某处;
3. 最后一次访问在内部日志文件中添加了一行。

在分析检查点之前的最后一步是告诉 Kubernetes 创建检查点。如上一篇文章所述，这需要访问 **kubelet** 唯一的“检查点” API 端点。

对于 **default** 命名空间中 **counters** Pod 中名为 **counter** 的容器，
可通过以下方式访问 **kubelet** API 端点：

```shell
# 在运行 Pod 的节点上运行这条命令
curl -X POST "https://localhost:10250/checkpoint/default/counters/counter"
```

为了完整起见，以下 curl 命令行选项对于让 curl 接受 **kubelet** 的自签名证书并授权使用 **kubelet** 检查点 API 是必要的：

```shell
--insecure --cert /var/run/kubernetes/client-admin.crt --key /var/run/kubernetes/client-admin.key
```

检查点操作完成后，检查点应该位于 `/var/lib/kubelet/checkpoints/checkpoint-<pod-name>_<namespace-name>-<container-name>-<timestamp>.tar`

在本文的以下步骤中，我将在分析检查点归档时使用名称 `checkpoint.tar`。

## 使用 `checkpointctl` 进行检查点归档分析

我使用工具 [checkpointctl][checkpointctl] 获取有关检查点容器的一些初始信息，如下所示：

```console
$ checkpointctl show checkpoint.tar --print-stats
+-----------+----------------------------------+--------------+---------+---------------------+--------+------------+------------+-------------------+
| CONTAINER |              IMAGE               |      ID      | RUNTIME |       CREATED       | ENGINE |     IP     | CHKPT SIZE | ROOT FS DIFF SIZE |
+-----------+----------------------------------+--------------+---------+---------------------+--------+------------+------------+-------------------+
| counter   | quay.io/adrianreber/counter:blog | 059a219a22e5 | runc    | 2023-03-02T06:06:49 | CRI-O  | 10.88.0.23 | 8.6 MiB    | 3.0 KiB           |
+-----------+----------------------------------+--------------+---------+---------------------+--------+------------+------------+-------------------+
CRIU dump statistics
+---------------+-------------+--------------+---------------+---------------+---------------+
| FREEZING TIME | FROZEN TIME | MEMDUMP TIME | MEMWRITE TIME | PAGES SCANNED | PAGES WRITTEN |
+---------------+-------------+--------------+---------------+---------------+---------------+
| 100809 us     | 119627 us   | 11602 us     | 7379 us       |          7800 |          2198 |
+---------------+-------------+--------------+---------------+---------------+---------------+
```

这展示了有关该检查点归档中的检查点的一些信息。我们可以看到容器的名称、有关容器运行时和容器引擎的信息。
它还列出了检查点的大小（`CHKPT SIZE`）。
这主要是检查点中包含的内存页的大小，同时也有有关容器中所有更改文件的大小的信息（`ROOT FS DIFF SIZE`）。

使用附加参数 `--print-stats` 可以解码检查点归档中的信息并将其显示在第二个表中（**CRIU 转储统计信息**）。
此信息是在检查点创建期间收集的，并概述了 CRIU 对容器中的进程生成检查点所需的时间以及在检查点创建期间分析和写入了多少内存页。

## 深入挖掘
借助 `checkpointctl`，我可以获得有关检查点归档的一些高级信息。为了能够进一步分析检查点归档，我必须将其提取。
检查点归档是 **tar** 归档文件，可以借助 `tar xf checkpoint.tar` 进行解压。

展开检查点存档时，将创建以下文件和目录：

* `bind.mounts` - 该文件包含有关绑定挂载的信息，并且需要在恢复期间需要将所有外部文件和目录挂载到正确的位置。
* `checkpoint/` - 该目录包含 CRIU 创建的实际检查点，
* `config.dump` 和 `spec.dump` - 这些文件包含恢复期间所需的有关容器的元数据。
* `dump.log` - 该文件包含在检查点期间创建的 CRIU 的调试输出。
* `stats-dump` - 此文件包含 `checkpointctl` 用于通过 `--print-stats` 显示转储统计信息的数据。
* `rootfs-diff.tar` - 该文件包含容器文件系统上所有已更改的文件。

### 更改文件系统 - `rootfs-diff.tar`

进一步分析容器检查点的第一步是查看容器内已更改的文件。这可以通过引用 `rootfs-diff.tar` 文件来完成。

```console
$ tar xvf rootfs-diff.tar
home/counter/logfile
home/counter/test-file
```

现在你可以检查容器内已更改的文件。

```console
$ cat home/counter/logfile
10.88.0.1 - - [02/Mar/2023 06:07:29] "GET /create?test-file HTTP/1.1" 200 -
10.88.0.1 - - [02/Mar/2023 06:07:40] "GET /secret?RANDOM_1432_KEY HTTP/1.1" 200 -
10.88.0.1 - - [02/Mar/2023 06:07:43] "GET / HTTP/1.1" 200 -
$ cat home/counter/test-file
test-file 
```

与该容器所基于的容器镜像（`quay.io/adrianreber/counter:blog`）相比，
它包含容器提供的服务的所有访问信息以及预期创建的 `logfile` 可以检查 `test-file` 文件。

在 `rootfs-diff.tar` 的帮助下，可以根据容器的基本镜像检查所有创建或修改的文件。

### 分析检查点进程 - `checkpoint/`

目录 `checkpoint/` 包含 CRIU 在容器内对进程进行检查点时创建的数据。
目录 `checkpoint/` 的内容由各种[镜像文件][image-files] 组成，可以使用作为 CRIU 一部分分发的 [CRIT][crit] 工具进行分析。

首先，我们先了解一下容器的内部流程。

```console
$ crit show checkpoint/pstree.img | jq .entries[].pid
1
7
8
```

此输出意味着容器的 PID 命名空间内有 3 个进程（PID 为 1、7 和 8）。

这只是容器 PID 命名空间的内部视图。这些 PID 在恢复过程中会准确地重新创建。从容器的 PID 命名空间外部，PID 将在恢复后更改。

下一步是获取有关这三个进程的更多信息。

```console
$ crit show checkpoint/core-1.img | jq .entries[0].tc.comm
"bash"
$ crit show checkpoint/core-7.img | jq .entries[0].tc.comm
"counter.py"
$ crit show checkpoint/core-8.img | jq .entries[0].tc.comm
"tee"
```

这意味着容器内的三个进程是 `bash`、`counter.py`（Python 解释器）和 `tee`。
`checkpoint/pstree.img` 中有更多数据可供分析，以获取有关进程起源的详细信息。

让我们将目前为止收集到的信息与仍在运行的容器进行比较。

```console
$ crictl inspect --output go-template --template "{{(index .info.pid)}}" 059a219a22e56
722520
$ ps auxf | grep -A 2 722520
fedora    722520  \_ bash -c /home/counter/counter.py 2>&1 | tee /home/counter/logfile
fedora    722541      \_ /usr/bin/python3 /home/counter/counter.py
fedora    722542      \_ /usr/bin/coreutils --coreutils-prog-shebang=tee /usr/bin/tee /home/counter/logfile
$ cat /proc/722520/comm
bash
$ cat /proc/722541/comm
counter.py
$ cat /proc/722542/comm
tee
```

在此输出中，我们首先获取容器中第一个进程的 PID。在运行容器的系统上，它会查找其 PID 和子进程。
你应该看到三个进程，第一个进程是 `bash`，容器 PID 命名空间中的 PID 为 1。
然后查看 `/proc/<PID>/comm`，可以找到与检查点镜像完全相同的值。

需要记住的重点是，检查点包含容器的 PID 命名空间内的视图。因为这些信息对于恢复进程非常重要。

`crit` 告诉我们有关容器的最后一个例子是有关 UTS 命名空间的信息。

```console
$ crit show checkpoint/utsns-12.img
{
    "magic": "UTSNS",
    "entries": [
        {
            "nodename": "counters",
            "domainname": "(none)"
        }
    ]
}
```

这里输出表示 UTS 命名空间中的主机名是 `counters`。

对于检查点创建期间收集的每个资源 CRIU，`checkpoint/` 目录包含相应的镜像文件。可以使用 `crit` 来分析该镜像文件。

#### 查看内存页面

除了可以借助 CRIT 解码的 CRIU 信息之外，还有包含 CRIU 写入磁盘的原始内存页的文件：

```console
$ ls  checkpoint/pages-*
checkpoint/pages-1.img  checkpoint/pages-2.img  checkpoint/pages-3.img
```

当我最初使用该容器时，我在内存中的某个位置存储了一个随机密钥。让我看看是否能找到它：

```console
$ grep -ao RANDOM_1432_KEY checkpoint/pages-*
checkpoint/pages-2.img:RANDOM_1432_KEY
```

确实有我的数据。通过这种方式，我可以轻松查看容器中进程的所有内存页面的内容，
但需要注意的是可以访问检查点存档的任何人都可以访问存储在容器进程内存中的所有信息。

#### 使用 gdb 进行进一步分析

查看检查点镜像的另一种方法是 `gdb`。CRIU 存储库包含脚本 [coredump][criu-coredump]，它可以将检查点转换为 coredump 文件：

```console
$ /home/criu/coredump/coredump-python3
$ ls -al core*
core.1  core.7  core.8
```

运行 `coredump-python3` 脚本会将检查点镜像转换为容器中每个进程一个的 coredump 文件。 使用 `gdb` 我还可以查看进程的详细信息：

```console
$ echo info registers | gdb --core checkpoint/core.1 -q

[New LWP 1]

Core was generated by `bash -c /home/counter/counter.py 2>&1 | tee /home/counter/logfile'.

#0  0x00007fefba110198 in ?? ()
(gdb)
rax            0x3d                61
rbx            0x8                 8
rcx            0x7fefba11019a      140667595587994
rdx            0x0                 0
rsi            0x7fffed9c1110      140737179816208
rdi            0xffffffff          4294967295
rbp            0x1                 0x1
rsp            0x7fffed9c10e8      0x7fffed9c10e8
r8             0x1                 1
r9             0x0                 0
r10            0x0                 0
r11            0x246               582
r12            0x0                 0
r13            0x7fffed9c1170      140737179816304
r14            0x0                 0
r15            0x0                 0
rip            0x7fefba110198      0x7fefba110198
eflags         0x246               [ PF ZF IF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0
```

In this example I can see the value of all registers as they were during
checkpointing and I can also see the complete command-line of my container's PID
1 process: `bash -c /home/counter/counter.py 2>&1 | tee /home/counter/logfile`

在这个例子中，我可以看到所有寄存器的值，因为它们在检查点，我还可以看到容器的 PID 1 进程的完整命令行：
`bash -c /home/counter/counter.py 2>&1 | tee /home/counter/logfile`。

## 总结

借助容器检查点，可以在不停止容器且在容器不知情的情况下，为正在运行的容器创建检查点。
在 Kubernetes 中对容器创建一个检查点的结果是检查点存档文件；
使用不同的工具，如 `checkpointctl`、`tar`、`crit` 和 `gdb`，可以分析检查点。
即使使用像 `grep` 这样的简单工具，也可以在检查点存档中找到信息。

我在本文中展示的如何分析检查点的不同示例，这只是一个起点。
根据你的需求，可以更详细地查看某些内容，本文向你介绍了如何开始进行检查点分析。

## 如何参与？

你可以通过多种方式联系到 SIG Node。

* Slack: [#sig-node][slack-sig-node]
* Slack: [#sig-security][slack-sig-security]
* [邮件列表][sig-node-ml]

[forensic-blog]: https://kubernetes.io/zh-cn/blog/2022/12/05/forensic-container-checkpointing-alpha/
[checkpointctl]: https://github.com/checkpoint-restore/checkpointctl
[image-files]: https://criu.org/Images
[crit]: https://criu.org/CRIT
[slack-sig-node]: https://kubernetes.slack.com/messages/sig-node
[slack-sig-security]: https://kubernetes.slack.com/messages/sig-security
[sig-node-ml]: https://groups.google.com/forum/#!forum/kubernetes-sig-node
[criu-coredump]: https://github.com/checkpoint-restore/criu/tree/criu-dev/coredump
