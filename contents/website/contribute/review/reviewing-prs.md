---
title: 评审 PR
content_type: concept
main_menu: true
weight: 10
---


任何人均可评审文档的拉取请求。
访问 Kubernetes 网站仓库的 [pull requests](https://github.com/kubernetes/website/pulls) 部分，
可以查看所有待处理的拉取请求（PR）。

评审文档 PR 是将你自己介绍给 Kubernetes 社区的一种很好的方式。
它将有助于你学习代码库并与其他贡献者之间建立相互信任关系。

在评审之前，可以考虑：

- 阅读[内容指南](/zh-cn/docs/contribute/style/content-guide/)和 
  [样式指南](/zh-cn/docs/contribute/style/style-guide/)以便给出有价值的评论。
- 了解 Kubernetes 文档社区中不同的[角色和职责](/zh-cn/docs/contribute/participate/roles-and-responsibilities/)。


## 准备工作 {#before-you-begin}

在你开始评审之前：

- 阅读 [CNCF 行为准则](https://github.com/cncf/foundation/blob/main/code-of-conduct.md)。
  确保你会始终遵从其中约定。
- 保持有礼貌、体谅他人，怀助人为乐初心。
- 评论时若给出修改建议，也要兼顾 PR 的积极方面。
- 保持同理心，多考虑他人收到评审意见时的可能反应。
- 假定大家都是好意的，通过问问题澄清意图。
- 如果你是有经验的贡献者，请考虑和新贡献者一起合作，提高其产出质量。

## 评审过程  {#review-process}

一般而言，应该使用英语来评审 PR 的内容和样式。
图 1 概述了评审流程的各个步骤。
每个步骤的详细信息如下。


{{< mermaid >}}
flowchart LR
    subgraph fourth[开始评审]
    direction TB
    S[ ] -.-
    M[添加评论] --> N[评审变更]
    N --> O[新手应该<br>选择 Comment]
    end
    subgraph third[选择 PR]
    direction TB
    T[ ] -.-
    J[阅读描述<br>和评论]--> K[通过 Netlify 预览构建<br>来预览变更]
    end
 
  A[查阅待处理的 PR 清单]--> B[通过标签过滤<br>待处理的 PR]
  B --> third --> fourth
     

classDef grey fill:#dddddd,stroke:#ffffff,stroke-width:px,color:#000000, font-size:15px;
classDef white fill:#ffffff,stroke:#000,stroke-width:px,color:#000,font-weight:bold
classDef spacewhite fill:#ffffff,stroke:#fff,stroke-width:0px,color:#000
class A,B,J,K,M,N,O grey
class S,T spacewhite
class third,fourth white
{{</ mermaid >}}

图 1. 评审流程步骤。

1. 前往 [https://github.com/kubernetes/website/pulls](https://github.com/kubernetes/website/pulls)，
   你会看到所有针对 Kubernetes 网站和文档的待处理 PR。

2. 使用以下标签（组合）对待处理 PR 进行过滤：

   - `cncf-cla: yes` （建议）：由尚未签署 CLA 的贡献者所发起的 PR 不可以合并。
     参考[签署 CLA](/zh-cn/docs/contribute/new-content/#sign-the-cla) 以了解更多信息。
   - `language/en` （建议）：仅查看英语语言的 PR。
   - `size/<尺寸>`：过滤特定尺寸（规模）的 PR。
     如果你刚入门，可以从较小的 PR 开始。

   此外，确保 PR 没有标记为尚未完成（Work in Progress）。
   包含 `work in progress` 的 PR 通常还没准备好被评审。

3. 选定 PR 评审之后，可以通过以下方式理解所作的变更：

   - 阅读 PR 描述以理解所作变更，并且阅读所有关联的 Issues。
   - 阅读其他评审人给出的评论。
   - 点击 **Files changed** Tab 页面，查看被改变的文件和代码行。
   - 滚动到 **Conversation** Tab 页面下端的 PR 构建检查节区，
     预览 Netlify 预览构建中的变更。
     以下是一个屏幕截图（这显示了 GitHub 的桌面版外观；
     如果你在平板电脑或智能手机设备上进行评审，
     GitHub 的 Web UI 会略有不同）：
     {{< figure src="/images/docs/github_netlify_deploy_preview.png" alt="GitHub PR 详细信息，包括 Netlify 预览链接" >}}
     要打开预览，请点击 **deploy/netlify** 行的 **Details** 链接。

4. 前往 **Files changed** Tab 页面，开始你的评审工作。

   1. 点击你希望评论的行旁边的 `+` 号。
   1. 填写你对该行的评论，
      之后选择 **Add single comment**（如果你只有一条评论）
      或者 **Start a review**（如果你还有其他评论要添加）。
   1. 评论结束时，点击页面顶部的 **Review changes**。
      这里你可以添加你的评论结语（记得留下一些正能量的评论！）、
      根据需要批准 PR、请求作者进一步修改等等。
      新手应该选择 **Comment**。

      - 避免在完成审查后点击 "Request changes（请求修改）"按钮。
        如果在完成进一步修改之前你想阻止某 PR 被合并。你可以在评论中留下一个 “/hold”。
        同时在评论中说明你为什么要设置 Hold，并且在必要时指定在什么条件下可以由你或其他评审人取消 Hold。
      - 避免在完成审查后直接点击 "Approve（批准）"按钮。
        在大多数情况下，建议在评论区留下一个"/approve（批准）"的评论。

## 评审清单  {#reviewing-checklist}

评审 PR 时可以从下面的条目入手。

### 语言和语法 {#language-and-grammar}

- 是否存在明显的语言或语法错误？对某事的描述有更好的方式？
  - 关注作者正在更改的页面部分的语言和语法。除非作者明确打算更新整个页面，否则他们没有义务修复页面上的所有问题。
  - 当一个 PR 更新现有页面时，你应专注于评审正在更新的页面部分。你应评审所更改内容的技术和编辑的正确性。
    如果你发现页面上的一些错误与 PR 作者尝试解决的问题没有直接关系，
    则应将其视为一个单独的 Issue（首先检查是否存在与此相关的 Issue）。
  - 要特别注意那些 **移动** 内容的 PR。如果作者重命名一个页面或合并两个页面，
    我们（Kubernetes SIG Docs）通常应避免要求该作者修复可能在所移动的内容中发现的所有语法或拼写错误。
- 是否存在一些过于复杂晦涩的用词，本可以用简单词汇来代替？
- 是否有些用词、术语或短语可以用不带歧视性的表达方式代替？
- 用词和大小写方面是否遵从了[样式指南](/zh-cn/docs/contribute/style/style-guide/)？
- 是否有些句子太长，可以改得更短、更简单？
- 是否某些段落过长，可以考虑使用列表或者表格来表达？

### 内容 {#content}

- Kubernetes 网站上是否别处已经存在类似的内容？
- 内容本身是否过度依赖于网站范畴之外、独立供应商或者非开源的文档？

### 网站 {#Website}

- PR 是否改变或者删除了某页面的标题、slug/别名或者链接锚点？
  如果是这样，PR 是否会导致出现新的失效链接？
  是否有其他的办法，比如改变页面标题但不改变其 slug？

- PR 是否引入新的页面？如果是：

  - 该页面是否使用了正确的[页面内容类型](/zh-cn/docs/contribute/style/page-content-types/)
    及相关联的 Hugo 短代码（shortcodes）？
  - 该页面能否在对应章节的侧面导航中显示？显示得正确么？
  - 该页面是否应出现在[网站主页面](/zh-cn/docs/home/)的列表中？

- 变更是否正确出现在 Netlify 预览中了？
  要对列表、代码段、表格、注释和图像等元素格外留心。

### 其他 {#other}

- 查阅 [Trivial Edits](https://www.kubernetes.dev/docs/guide/pull-requests/#trivial-edits)；
  如果你看到某个变更在你看来是一个 Trivial Edit，请向作者指明这项政策（如果该变更确实会有所改进，那仍然可以接受）。
- 鼓励作者们在第一次发 PR 时修复一些空格相关的问题，在随后的 PR 中增加其他更改。
  这样更便于合并和评审。尤其要注意在单个 commit 中大量空格清理附带的微小变更（如果你看到，请鼓励作者进行修复）。

作为一名 Reviewer，如果你发现 PR 有一些无关紧要的小问题，例如拼写错误或不正确的空格，
可以在你的评论前面加上 `nit:`。这样做可以让作者知道该问题不是一个不得了的大问题。

如果你正在考虑批准一个 PR，并且所有剩余的反馈都被标记为 nit，那么你确实可以合并该 PR。
在这种情况下，你需要针对剩余的 nit 发帖登记一个 Issue。
考虑一下是否能把这些新 Issue 标记为
[Good First Issue](https://www.kubernetes.dev/docs/guide/help-wanted/#good-first-issue)。
如果可以，这就是这类 Issue 的良好来源。

