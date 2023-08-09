---
layout: blog
title: "Kubernetes 机密：使用机密虚拟机和安全区来增强你的集群安全性"
date: 2023-07-06
slug: "confidential-kubernetes"
---


**作者**：Fabian Kammel (Edgeless Systems), Mikko Ylinen (Intel), Tobin Feldman-Fitzthum (IBM)

**译者**：[顾欣](https://github.com/asa3311)

在这篇博客文章中，我们将介绍机密计算（Confidential Computing，简称 CC）的概念，
以增强任何计算环境的安全和隐私属性。此外，我们将展示云原生生态系统，
特别是 Kubernetes，如何从新的计算范式中受益。

机密计算是一个先前在云原生领域中引入的概念。
[机密计算联盟](https://confidentialcomputing.io/)(Confidential Computing Consortium，简称 CCC) 
是 Linux 基金会中的一个项目社区，
致力于[定义和启用机密计算](https://confidentialcomputing.io/wp-content/uploads/sites/85/2019/12/CCC_Overview.pdf)。
在[白皮书](https://confidentialcomputing.io/wp-content/uploads/sites/85/2023/01/CCC-A-Technical-Analysis-of-Confidential-Computing-v1.3_Updated_November_2022.pdf)中，
他们为使用机密计算提供了很好的动机。

   > 数据存在于三种状态：传输中、静态存储和使用中。保护所有状态下的敏感数据比以往任何时候都更加关键。
   > 现在加密技术常被部署以提供数据机密性（阻止未经授权的查看）和数据完整性（防止或检测未经授权的更改）。
   > 虽然现在通常部署了保护传输中和静态存储中的数据的技术，但保护使用中的数据是新的前沿。

机密计算主要通过引入硬件强制执行的可信执行环境（TEE）来解决**保护使用中的数据**的问题。

## 可信执行环境  {#trusted-execution-environments}

在过去的十多年里，可信执行环境（Trusted Execution Environments，简称 TEEs）
以[硬件安全模块](https://zh.wikipedia.org/zh-cn/%E7%A1%AC%E4%BB%B6%E5%AE%89%E5%85%A8%E6%A8%A1%E5%9D%97)（Hardware Security Modules，简称 HSMs）
和[可信平台模块](https://www.iso.org/standard/50970.html)（Trusted Platform Modules，简称 TPMs）
的形式在商业计算硬件中得以应用。这些技术提供了可信的环境来进行受保护的计算。
它们可以存储高度敏感的加密密钥，并执行关键的加密操作，如签名或加密数据。

TPMs 的优化为降低成本，使它们能够集成到主板中并充当系统的物理根信任。
为了保持低成本，TPMs 的范围受到限制，即它们只能存储少量的密钥，并且仅能执行一小部分的加密操作。

相比之下，HSMs 的优化为提高性能，为更多的密钥提供安全存储，并提供高级物理攻击检测机制。
此外，高端 HSMs 可以编程，以便可以编译和执行任意代码。缺点是它们的成本非常高。
来自 AWS 的托管 CloudHSM 的费用大约是[每小时 1.50 美元](https://aws.amazon.com/cloudhsm/pricing/)，
或者约每年 13,500 美元。

近年来，一种新型的 TEE 已经变得流行。
像 [AMD SEV](https://developer.amd.com/sev/)、
[Intel SGX](https://www.intel.com/content/www/us/en/developer/tools/software-guard-extensions/overview.html)
和 [Intel TDX](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-trust-domain-extensions.html)
这样的技术提供了与用户空间紧密集成的 TEE。与支持特定的低功耗或高性能设备不同，
这些 TEE 保护普通进程或虚拟机，并且可以以相对较低的开销执行此操作。
这些技术各有不同的设计目标、优点和局限性，
并且在不同的环境中可用，包括消费者笔记本电脑、服务器和移动设备。

此外，我们应该提及 [ARM TrustZone](https://www.arm.com/technologies/trustzone-for-cortex-a)，
它针对智能手机、平板电脑和智能电视等嵌入式设备进行了优化，
以及 [AWS Nitro Enclaves](https://aws.amazon.com/ec2/nitro/nitro-enclaves/)，
它们只在 [Amazon Web Services](https://aws.amazon.com/) 上可用，
并且与 Intel 和 AMD 的基于 CPU 的解决方案相比，具有不同的威胁模型。

[IBM Secure Execution for Linux](https://www.ibm.com/docs/en/linux-on-systems?topic=virtualization-secure-execution)
允许你在 IBM Z 系列硬件的可信执行环境内以 KVM 客户端的形式运行 Kubernetes 集群的节点。
你可以使用这种硬件增强的虚拟机隔离机制为集群中的租户之间提供稳固的隔离，
并通过硬件验证提供关于（虚拟）节点完整性的信息。

### 安全属性和特性功能  {#security-properties-and-feature-set}

下文将回顾这些新技术所带来的安全属性和额外功能。
只有部分解决方案会提供所有属性；我们将在各自的小节中更详细地讨论每项技术。

**机密性**属性确保在使用 TEE 时信息无法被查看。这为我们提供了非常需要的的功能以保护**使用中的数据**。
根据使用的特定 TEE，代码和数据都可能受到外部查看者的保护。
TEE 架构的差异以及它们在云原生环境中的使用是在设计端到端安全性时的重要考虑因素，
目的是为敏感工作负载提供最小的**可信计算基础**（Trusted Computing Base, 简称 TCB）。
CCC 最近致力于**通用术语和支持材料**，以帮助解释在不同的 TEE 架构下机密性边界的划分，
以及这如何影响 TCB 的大小。

机密性是一个很好的特性，但攻击者仍然可以操纵或注入任意代码和数据供 TEE 执行，
因此，很容易泄露关键信息。**完整性**保证 TEE 拥有者在运行关键计算时，代码和数据都不能被篡改。

**可用性**是在信息安全背景下经常讨论的一项基本属性。然而，这一属性超出了大多数 TEE 的范围。
通常，它们可以被一些更高级别的抽象控制（关闭、重启...）。这可以是 CPU 本身、虚拟机监视器或内核。
这是为了保持整个系统的可用性，而不是 TEE 本身。在云环境中运行时，
可用性通常由云提供商以服务级别协议（Service Level Agreements，简称 SLAs）的形式保证，
并且不能通过加密强制执行。

仅凭机密性和完整性在某些情况下是有帮助的。例如，考虑一个在远程云中运行的 TEE。
你如何知道 TEE 是真实的并且正在运行你预期的软件？一旦你发送数据，
它可能是一个冒名顶替者窃取你的数据。这个根本问题通过**可验证性**得到解决。
验证允许我们基于硬件本身签发的加密证书来验证 TEE 的身份、机密性和完整性。
这个功能也可以以远程验证的形式提供给机密计算硬件之外的客户端使用。

TEEs 可以保存和处理早于或超出可信环境存在时间的信息。这可能意味着重启、跨不同版本或平台迁移的信息。
因此，**可恢复性**是一个重要的特性。在将数据和 TEE 的状态写入持久性存储之前，需要对它们进行封装，
以维护保证机密性和完整性。对这种封装数据的访问需要明确定义。在大多数情况下，
解封过程与 TEE 绑定的身份有关。因此，确保恢复只能在相同的机密环境中进行。

这不必限制整个系统的灵活性。
[AMD SEV-SNP 的迁移代理 (MA)](https://www.amd.com/system/files/TechDocs/SEV-SNP-strengthening-vm-isolation-with-integrity-protection-and-more.pdf)
允许用户将机密虚拟机迁移到不同的主机系统，同时保持 TEE 的安全属性不变。

## 功能比较  {#feature-comparison}

本文的这部分将更深入地探讨具体的实现，比较支持的功能并分析它们的安全属性。

### AMD SEV  {#amd-sev}

AMD 的[安全加密虚拟化 (SEV)](https://developer.amd.com/sev/)技术是一组功能，
用于增强 AMD 服务器 CPU 上虚拟机的安全性。SEV 透明地用唯一密钥加密每个 VM 的内存。
SEV 还可以计算内存内容的签名，该签名可以作为证明初始客户机内存没有被篡改的依据发送给 VM 的所有者。

SEV 的第二代，称为[加密状态](https://www.amd.com/system/files/TechDocs/Protecting%20VM%20Register%20State%20with%20SEV-ES.pdf)
或 SEV-ES，通过在发生上下文切换时加密所有 CPU 寄存器内容，提供了对虚拟机管理程序的额外保护。

SEV 的第三代，[安全嵌套分页](https://www.amd.com/system/files/TechDocs/SEV-SNP-strengthening-vm-isolation-with-integrity-protection-and-more.pdf)
或 SEV-SNP，旨在防止基于软件的完整性攻击并降低受损内存完整性相关的风险。
SEV-SNP 完整性的基本原则是，如果虚拟机可以读取私有（加密）内存页，
那么它必须始终读取它最后写入的值。

此外，通过允许客户端动态获取远程验证声明，SNP 增强了 SEV 的远程验证能力。

AMD SEV 是以增量方式实施的。每个新的 CPU 代都增加了新功能和改进。
Linux 社区将这些功能作为 KVM 虚拟机管理程序的一部分提供，适用于主机和客户机内核。
第一批 SEV 功能在 2016 年被讨论并实施 - 参见 2016 年 Usenix 安全研讨会的 
[AMD x86 内存加密技术](https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/kaplan)。
最新的重大补充是 [Linux 5.19 中的 SEV-SNP 客户端支持](https://cloud.google.com/compute/confidential-vm/docs/about-cvm)。

自 2022 年 7 月以来，Microsoft Azure 提供基于 
[AMD SEV-SNP 的机密虚拟机](https://azure.microsoft.com/en-us/updates/azureconfidentialvm/)。
类似地，Google Cloud Platform (GCP) 提供基于 
[AMD SEV-ES 的机密虚拟机](https://cloud.google.com/compute/confidential-vm/docs/about-cvm)。

### Intel SGX  {#intel-sgx}

Intel 的[软件防护扩展](https://www.intel.com/content/www/us/en/developer/tools/software-guard-extensions/overview.html)
自 2015 年起便已推出，并在 Skylake 架构中首次亮相。

SGX 是一套指令集，它使用户能够创建一个叫做 *Enclave* 的受保护且隔离的进程。
它提供了一个反沙箱机制，保护 Enclave 不受操作系统、固件以及任何其他特权执行上下文的影响。

Enclave 内存无法从 Enclave 外部读取或写入，无论当前的权限级别和 CPU 模式如何。
调用 Enclave 功能的唯一方式是通过一条执行多个保护检查的新指令。Enclave 的内存是加密的。
窃听内存或将 DRAM 模块连接到另一个系统只会得到加密数据。内存加密密钥在每次上电周期时随机更改。
密钥存储在 CPU 内部，无法访问。

由于 Enclave 是进程隔离的，操作系统的库不能直接使用；
因此，需要 SGX Enclave SDK 来编译针对 SGX 的程序。
这也意味着应用程序需要在设计和实现时考虑受信任/不受信任的隔离边界。
另一方面，应用程序的构建具有非常小的 TCB。

一种新兴的方法，利用库操作系统（library OSes）来轻松过渡到基于进程的机密计算并避免需要构建自定义应用程序。
这些操作系统有助于在 SGX 安全 Enclave 内运行原生的、未经修改的 Linux 应用程序。
操作系统库会拦截应用对宿主机操作系统的所有请求，并在应用不知情的情况下安全地处理它们，
而应用实际上是在一个受信执行环境（TEE）中运行。

第三代 Xeon 处理器（又称为 Ice Lake 服务器 - "ICX"）及其后续版本采用了一种名为
[全内存加密 - 多密钥](https://www.intel.com/content/www/us/en/developer/articles/news/runtime-encryption-of-memory-with-intel-tme-mk.html)（TME-MK）的技术，
该技术使用 AES-XTS，从消费者和 Xeon E 处理器使用的[内存加密引擎](https://eprint.iacr.org/2016/204.pdf)中脱离出来。
这可能增加了 [Enclave 页面缓存](https://sgx101.gitbook.io/sgx101/sgx-bootstrap/enclave#enclave-page-cache-epc)
（EPC）大小（每个 CPU 高达 512 GB）并提高了性能。关于多插槽平台上的 SGX 的更多信息可以在
[白皮书](https://www.intel.com/content/dam/www/public/us/en/documents/white-papers/supporting-intel-sgx-on-mulit-socket-platforms.pdf)中找到。

可以从 Intel 获取[支持的平台列表](https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html?productType=873)。

SGX 在 [Azure](https://azure.microsoft.com/de-de/updates/intel-sgx-based-confidential-computing-vms-now-available-on-azure-dedicated-hosts/)、
[阿里云](https://www.alibabacloud.com/help/en/elastic-compute-service/latest/build-an-sgx-encrypted-computing-environment)、
[IBM](https://cloud.ibm.com/docs/bare-metal?topic=bare-metal-bm-server-provision-sgx) 以及更多平台上可用。

### Intel TDX  {#intel-tdx}

Intel SGX 旨在保护单个进程的上下文，而
[Intel 的可信域扩展](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-trust-domain-extensions.html)保护整个虚拟机，
因此，它与 AMD SEV 最为相似。

与 SEV-SNP 一样，对 TDX 的客户端支持已经在
[Linux Kernel 5.19版本中合并](https://www.phoronix.com/news/Intel-TDX-For-Linux-5.19)。
然而，硬件支持将在 2023 年与 [Sapphire Rapids](https://en.wikipedia.org/wiki/Sapphire_Rapids) 一同发布：
[阿里云提供](https://www.alibabacloud.com/help/en/elastic-compute-service/latest/build-a-tdx-confidential-computing-environment)
邀请预览实例，同时，[Azure 已经宣布](https://techcommunity.microsoft.com/t5/azure-confidential-computing/preview-introducing-dcesv5-and-ecesv5-series-confidential-vms/ba-p/3800718)
其 TDX 预览机会。

## 开销分析  {#overhead-analysis}

通过强隔离和增强的安全性，机密计算技术为客户数据和工作负载提供的好处并非免费。
量化这种影响是具有挑战性的，并且取决于许多因素：TEE 技术，基准测试，
度量标准以及工作负载的类型都对预期的性能开销有巨大的影响。

基于 Intel SGX 的 TEE 很难进行基准测试，
正如[不同的论文](https://dl.acm.org/doi/fullHtml/10.1145/3533737.3535098)所
[展示](https://arxiv.org/pdf/2205.06415.pdf)的[一样](https://www.ibr.cs.tu-bs.de/users/mahhouk/papers/eurosec2021.pdf)。
所选择的 SDK/操作系统库，应用程序本身以及资源需求（特别是大内存需求）对性能有巨大的影响。
如果应用程序非常适合在 Enclave 内运行，那么通常可以预期会有一个个位数的百分比的开销。

基于 AMD SEV-SNP 的机密虚拟机不需要对执行的程序和操作系统进行任何更改，
因此更容易进行基准测试。一个来自 
[Azure 和 AMD 的基准测试](https://community.amd.com/t5/business/microsoft-azure-confidential-computing-powered-by-3rd-gen-epyc/ba-p/497796)显示，
SEV-SNP VM 的开销 < 10%，有时甚至低至 2%。

尽管存在性能开销，但它应该足够低，以便使真实世界的工作负载能够在这些受保护的环境中运行，
并提高我们数据的安全性和隐私性。

## 机密计算与 FHE、ZKP 和 MPC 的比较  {#confidential-computing-compared-to-fhe-zkp-and-mpc}

全同态加密（FHE），零知识证明/协议（ZKP）和多方计算（MPC）都是加密或密码学协议的形式，
提供与机密计算类似的安全保证，但不需要硬件支持。

全同态加密（也包括部分和有限同态加密）允许在加密数据上执行计算，例如加法或乘法。
这提供了在使用中加密的属性，但不像机密计算那样提供完整性保护或认证。因此，这两种技术可以
[互为补充](https://confidentialcomputing.io/2023/03/29/confidential-computing-and-homomorphic-encryption/)。

零知识证明或协议是一种隐私保护技术（PPT），它允许一方证明其数据的事实而不泄露关于数据的任何其他信息。
ZKP 可以替代或与机密计算一起使用，以保护相关方及其数据的隐私。同样，
多方计算使多个参与方能够共同进行计算，即每个参与方提供其数据以得出结果，
但不会泄露给任何其他参与方。

## 机密计算的应用场景  {#use-cases-of-confidential-computing}

前面介绍的机密计算平台表明，既可以实现单个容器进程的隔离，从而最小化可信计算单元，
也可以实现整个虚拟机的隔离。这已经促使很多有趣且安全的项目涌现：

### 机密容器  {#confidential-containers}

机密容器 (CoCo) 是一个 CNCF 沙箱项目，它在机密虚拟机内隔离 Kubernetes Pod。

CoCo 可以通过 operator 安装在 Kubernetes 集群上。operator 将创建一组运行时类，
这些类可以用于在多个不同的平台上的 Enclave 内部署 Pod，
包括 AMD SEV，Intel TDX，IBM Z 的安全执行和 Intel SGX。

CoCo 通常与签名和/或加密的容器镜像一起使用，这些镜像在 Enclave 内部被拉取、验证和解密。
密钥信息，比如镜像解密密钥，经由受信任的 Key Broker 服务有条件地提供给 Enclave，
这个服务在释放任何敏感信息之前验证 TEE 的硬件认证。

CoCo 有几种部署模型。由于 Kubernetes 控制平面在 TCB 之外，因此 CoCo 适合于受管理的环境。
在不支持嵌套的虚拟环境中，CoCo 可以借助 API 适配器运行，该适配器在云中启动 Pod VM。
CoCo 还可以在裸机上运行，在多租户环境中提供强大的隔离。

### 受管理的机密 Kubernetes  {#managed-confidential-kubernetes} 

[Azure](https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-node-pool-aks)
和 [GCP](https://cloud.google.com/blog/products/identity-security/announcing-general-availability-of-confidential-gke-nodes)
都支持将机密虚拟机用作其受管理的 Kubernetes 的工作节点。

这两项服务通过启用容器工作负载的内存加密，旨在提供更好的工作负载保护和安全保证。
然而，它们并没有寻求完全隔离集群或工作负载以防止服务提供者或基础设施的访问。
具体来说，它们不提供专用的机密控制平面，也不为机密集群/节点提供可验证的能力。

Azure 在其托管的 Kubernetes 服务中也启用了
[机密容器](https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-nodes-aks-overview)。
他们支持基于 [Intel SGX Enclave](https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-containers-enclaves)
和基于 [AMD SEV 虚拟机](https://techcommunity.microsoft.com/t5/azure-confidential-computing/microsoft-introduces-preview-of-confidential-containers-on-azure/ba-p/3410394)
创建的机密容器。

### Constellation  {#constellation}

[Constellation](https://github.com/edgelesssys/constellation) 
是一个旨在提供最佳数据安全的 Kubernetes 引擎。
Constellation 将整个 Kubernetes 集群包装到一个机密上下文中，使其免受底层云基础设施的影响。
其中的所有内容始终是加密的，包括在内存中的运行时数据。它保护工作节点和控制平面节点。
此外，它已经与流行的 CNCF 软件（如 Cilium，用于安全网络）集成，
并提供扩展的 CSI 动程序来安全地写入数据。

### Occlum 和 Gramine  {#occlum-and-gramine}

[Occlum](https://occlum.io/) 和 [Gramine](https://gramineproject.io/)
是两个开源的操作系统库项目，它们允许在 SGX 信任执行环境（Enclave）中运行未经修改的应用程序。
它们是 CCC（Confidential Computing Consortium）下的成员项目，
但也存在由公司维护的类似项目和产品。通过使用这些操作系统库项目，
现有的容器化应用可以轻松转换为支持机密计算的容器。还有许多经过筛选的预构建容器可供使用。

## 我们现在处于哪个阶段？供应商、局限性和开源软件生态  {#where-are-we-today-vendors-limitations-and-foss-landscape}

正如我们希望你从前面的章节中看到的，机密计算是一种强大的新概念，
用于提高安全性，但我们仍处于（早期）阶段。新产品开始涌现，以利用这些独特的属性。

谷歌和微软是首批能够让客户在一个受保护的环境内运行未经修改的应用程序的机密计算服务的主要云提供商。
然而，这些服务仅限于计算，而对于机密数据库、集群网络和负载均衡器的端到端解决方案则需要自行管理。

这些技术为极其敏感的工作负载部署到云中提供了可能，并使其能够充分利用 CNCF 领域中的各种工具。

## 号召行动  {#call-to-action}

如果你目前正在开发一个高安全性的产品，但由于法律要求在公共云上运行面临困难，
或者你希望提升你的云原生项目的隐私和安全性：请联系我们强调的所有出色项目！
每个人都渴望提高我们生态系统的安全性，而你可以在这个过程中扮演至关重要的角色。

* [机密容器](https://github.com/confidential-containers)
* [Constellation：始终加密的 Kubernetes](https://github.com/edgelesssys/constellation)
* [Occlum](https://occlum.io/)
* [Gramine](https://gramineproject.io/)
* CCC 还维护了一个[项目列表](https://confidentialcomputing.io/projects/)
