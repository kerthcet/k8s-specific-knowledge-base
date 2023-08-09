---
title: "Kubernetes 社区每周聚会笔记 - 2015 年 3 月 27 日"
date: 2015-03-28
slug: weekly-kubernetes-community-hangout
---

每个星期，Kubernetes 贡献者社区几乎都会在谷歌 Hangouts 上聚会。我们希望任何对此感兴趣的人都能了解这个论坛的讨论内容。

日程安排：


\- Andy - 演示远程执行和端口转发

\- Quinton - 联邦集群 - 延迟

\- Clayton - 围绕 Kubernetes 的 UI 代码共享和协作

从会议指出：


1\. Andy 从 RedHat：


* 演示远程执行


    * kubectl exec -p $POD -- $CMD

    * 作为代理与主机建立连接，找出 pod 所在的节点，代理与 kubelet 的连接，这一点很有趣。通过 nsenter。

    * 使用 SPDY 通过 HTTP 进行多路复用流式传输

    * 还有互动模式：

    * 假设第一个容器，可以使用 -c $CONTAINER 一个特定的。

    * 如果在容器中预先安装了 gdb，则可以交互地将其附加到正在运行的进程中

        * backtrace、symbol tbles、print 等。  使用gdb可以做的大多数事情。

    * 也可以用精心制作的参数在上面运行 rsync 或者在容器内设置 sshd。

    * 一些聊天反馈：


* Andy 还演示了端口转发
* nnsenter 与 docker exec


    * 想要在主机的控制下注入二进制文件，类似于预启动钩子

    * socat、nsenter，任何预启动钩子需要的


* 如果能在博客上发表这方面的文章就太好了
* wheezy 中的 nginx 版本太旧，无法支持所需的主代理功能


2\. Clayton: 我们的社区组织在哪里，例如 kubernetes UI 组件？

* google-containers-ui IRC 频道，邮件列表。
* Tim: google-containers 前缀是历史的，应该只做 "kubernetes-ui"
* 也希望将设计资源投入使用，并且 bower 期望自己的仓库。
* 通用协议


3\. Brian Grant:

* 测试 v1beta3，准备进入。
* Paul 致力于改变命令行的内容。
* 下周初至中旬，尝试默认启用v1beta3 ?
* 对于任何其他更改，请发出文件并抄送 thockin。


4\. 一般认为30分钟比60分钟好


* 不应该为了填满时间而人为地延长。
