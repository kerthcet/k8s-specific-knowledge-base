---
title: " 将端到端的 Kubernetes 测试引入 Azure （第二部分） "
date: 2016-07-18
slug: bringing-end-to-end-kubernetes-testing-to-azure-2
---

_作者标注：今天的邀请帖子是 Travis Newhouse 的 [系列](https://kubernetes.io/blog/2016/06/bringing-end-to-end-testing-to-azure) 中的第二部分，他是 AppFormix 的首席架构师，这篇文章介绍了他们对 Kubernetes 的贡献。_


历史上，Kubernetes 测试一直由谷歌托管，在 [谷歌计算引擎](https://cloud.google.com/compute/) (GCE) 和 [谷歌容器引擎](https://cloud.google.com/container-engine/) (GKE) 上运行端到端测试。实际上，提交队列的选通检查是在这些测试平台上执行测试的子集。联合测试旨在通过使组织托管各种平台的测试作业并贡献测试结果，从而让 Kubernetes 项目受益来扩大测试范围。谷歌和 SIG-Testing 的 Kubernetes 测试小组成员已经创建了一个 [Kubernetes 测试历史记录仪表板](http://storage.googleapis.com/kubernetes-test-history/static/index.html)，可以发布所有联合测试作业（包括谷歌托管的作业）的全部结果。

在此博客文章中，我们介绍了扩展 Azure 的端到端测试工作，并展示了如何为 Kubernetes 项目贡献联合测试。

**Azure 的端到端集成测试**

成功实现 [在 Azure 上自动部署 Kubernetes 的 “development distro” 脚本](https://kubernetes.io/blog/2016/06/bringing-end-to-end-testing-to-azure) 之后，我们的下一个目标是运行端到端集成测试，并与 Kubernetes 社区共享结果。

通过在私有 Jenkins 服务器中定义夜间工作，我们自动化了在 Azure 上执行 Kubernetes 端到端测试的工作流程。图2显示了使用 kube-up.sh 在运行于 Azure 的 Ubuntu 虚拟机上部署 Kubernetes，然后执行端到端测试的工作流程。测试完成后，该作业将测试结果和日志上传到 Google Cloud Storage 目录中，其格式可以由 [生成测试历史记录仪表板的脚本](https://github.com/kubernetes/test-infra/tree/master/jenkins/test-history) 进行处理。我们的 Jenkins 作业使用 hack/jenkins/e2e-runner.sh 和 hack/jenkins/upload-to-gcs.sh 脚本生成正确格式的结果。

| ![Kubernetes on Azure - Flow Chart - New Page.png](https://lh6.googleusercontent.com/TZiUu4sQ7G0XDvJgv9a1a4UEdxntOZDT9I3S42c8BOAyigxaysKmhJMen8vLaJ3UYaYKPIG9h-cyBOvTSI6kBgqnUQabe4xxZXhrUyVxinKGEaCDUnmNlBo__HNjzoYc_U7zM77_Dxe) |
| 图 2 - 夜间测试工作流程 |

**如何进行端到端测试** 

在创建 Azure 端到端测试工作的整个过程中，我们与 [SIG-Testing](https://github.com/kubernetes/community/tree/master/sig-testing) 的成员进行了合作，找到了一种将结果发布到 Kubernetes 社区的方法。合作的结果是以文档和简化的流程从联合测试工作中贡献结果。贡献端到端测试结果的过程可以归纳为4个步骤。

1. 创建一个 [Google Cloud Storage](https://cloud.google.com/storage/) 空间用来发布结果。
2. 定义一个自动化作业来运行端到端测试，通过设置一些环境变量，使用 hack/jenkins/e2e-runner.sh 部署 Kubernetes 二进制文件并执行测试。
3. 使用 hack/jenkins/upload-to-gcs.sh 上传结果。
4. 通过提交对 [kubernetes/test-infra](https://github.com/kubernetes/test-infra) 中的几个文件进行修改的请求，将结果合并到测试历史记录仪表板中。

联合测试文档更详细地描述了这些步骤。运行端到端测试并上传结果的脚本简化了贡献新联合测试作业的工作量。设置自动化测试作业的具体步骤以及在其中部署 Kubernetes 的合适环境将留给读者进行选择。对于使用 Jenkins 的组织，用于 GCE 和 GKE 测试的 jenkins-job-builder 配置可能会提供有用的示例。


**回顾**

Azure 上的端到端测试已经运行了几周。在此期间，我们在 Kubernetes 中发现了两个问题。Weixu Zhuang 立即发布了修补程序并已合并到 Kubernetes master 分支中。

当我们想用 Ubuntu VM 在 Azure 上用 SaltStack 打开 Kubernetes 集群时，发生了第一个问题。一个提交 (07d7cfd3) 修改了 OpenVPN 证书生成脚本，使用了一个仅由集群或者ubuntu中的脚本初始化的变量。证书生成脚本对参数是否存在进行严格检查会导致其他使用该脚本的平台失败（例如，为支持 Azure 而进行的更改）。我们提交了一个[解决问题的请求](https://github.com/kubernetes/kubernetes/pull/21357) ，通过使用默认值初始化变量让证书生成脚本在所有平台类型上都更加健壮，。

第二个 [清理未使用导入的请求](https://github.com/kubernetes/kubernetes/pull/22321) 在 Daemonset 单元测试文件中。import 语句打破了 golang 1.4 的单元测试。我们的夜间 Jenkins 工作帮助我们找到错误并且迅速完成修复。

**结论与未来工作**  

在 Azure 上为 Kubernetes 添加了夜间端到端测试工作，这有助于定义为 Kubernetes 项目贡献联合测试的过程。在工作过程中，当 Azure 测试工作发现兼容性问题时，我们还发现了将测试覆盖范围扩展到更多平台的直接好处。

我们要感谢 Aaron Crickenberger, Erick Fejta, Joe Finney 和 Ryan Hutchinson 的帮助，将我们的 Azure 端到端测试结果纳入了 Kubernetes 测试历史。如果您想参与测试来创建稳定的、高质量的 Kubernetes 版本，请加入我们的 [Kubernetes Testing SIG (sig-testing)](https://github.com/kubernetes/community/tree/master/sig-testing)。


_--Travis Newhouse, AppFormix 首席架构师_
