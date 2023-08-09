---
title: 发起拉取请求（PR）
content_type: concept
weight: 10
card:
  name: contribute
  weight: 40
---


{{< note >}}
**代码开发者们**：如果你在为下一个 Kubernetes 发行版本中的某功能特性撰写文档，
请参考[为发行版本撰写功能特性文档](/zh-cn/docs/contribute/new-content/new-features/)。
{{< /note >}}

要贡献新的内容页面或者改进已有内容页面，请发起拉取请求（PR）。
请确保你满足了[开始之前](/zh-cn/docs/contribute/new-content/)一节中所列举的所有要求。

如果你所提交的变更足够小，或者你对 git 工具不熟悉，
可以阅读[使用 GitHub 提交变更](#changes-using-github)以了解如何编辑页面。

如果所提交的变更较大，
请阅读[基于本地克隆副本开展工作](#fork-the-repo)以学习如何在你本地计算机上进行修改。


## 使用 GitHub 提交变更   {#changes-using-github}

如果你在 git 工作流方面欠缺经验，这里有一种发起拉取请求的更为简单的方法。
图 1 勾勒了后续的步骤和细节。


{{< mermaid >}}
flowchart LR
A([fa:fa-user 新的<br>贡献者]) --- id1[(kubernetes/website<br>GitHub)]
subgraph tasks[使用 GitHub 提交变更]
direction TB
    0[ ] -.-
    1[1. 编辑此页] --> 2[2. 使用 GitHub markdown<br>编辑器进行修改]
    2 --> 3[3. 填写 Propose file change]

end
subgraph tasks2[ ]
direction TB
4[4. 选择 Propose file change] --> 5[5. 选择 Create pull request] --> 6[6. 填写 Open a pull request]
6 --> 7[7. 选择 Create pull request] 
end

id1 --> tasks --> tasks2

classDef grey fill:#dddddd,stroke:#ffffff,stroke-width:px,color:#000000, font-size:15px;
classDef white fill:#ffffff,stroke:#000,stroke-width:px,color:#000,font-weight:bold
classDef k8s fill:#326ce5,stroke:#fff,stroke-width:1px,color:#fff;
classDef spacewhite fill:#ffffff,stroke:#fff,stroke-width:0px,color:#000
class A,1,2,3,4,5,6,7 grey
class 0 spacewhite
class tasks,tasks2 white
class id1 k8s
{{</ mermaid >}}

图 1. 使用 GitHub 发起一个 PR 的步骤。

1. 在你发现问题的页面上，选择右侧导航面板中的**编辑此页面**选项。

2. 在 GitHub 的 Markdown 编辑器中修改内容。

3. 在编辑器的下方，填写 **Propose file change** 表单。
   在第一个字段中，为你的提交消息取一个标题。
   在第二个字段中，为你的提交写一些描述文字。

   {{< note >}}
   不要在提交消息中使用 [GitHub 关键词](https://help.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)。
   你可以在后续的 PR 描述中使用这些关键词。
   {{< /note >}}

4. 选择 **Propose File Change**。

5. 选择 **Create pull request**。

6. 出现 **Open a pull request** 界面。填写表单：

   - **Subject** 字段默认为提交的概要信息，你可以根据需要进行修改。
   - **Body** 字段包含更为详细的提交消息（如果你之前有填写过的话）和一些模板文字。
     填写模板所要求的详细信息，之后删除多余的模板文字。
   - 确保 **Allow edits from maintainers** 复选框被勾选。

   {{< note >}}
   PR 描述信息是帮助 PR 评阅人了解你所提议的变更的重要途径。
   更多信息请参考[发起一个 PR](#open-a-pr)。
   {{< /note >}}

7. 选择 **Create pull request**。

### 在 GitHub 上处理反馈意见   {#addressing-feedback-in-github}

在合并 PR 之前，Kubernetes 社区成员会评阅并批准它。
`k8s-ci-robot` 会基于页面中最近提及的属主来建议评阅人（reviewers）。
如果你希望特定某人来评阅，可以留下评论，提及该用户的 GitHub 用户名。

如果某个评阅人请你修改 PR：

1. 前往 **Files changed** Tab 页面；
1. 选择 PR 所修改的任何文件所对应的铅笔（edit）图标；
1. 根据建议作出修改；
1. 提交所作修改。

如果你希望等待评阅人的反馈，可以每 7 天左右联系一次。
你也可以在 `#sig-docs` Slack 频道发送消息。

当评阅过程结束，某个评阅人会合并你的 PR。
几分钟之后，你所做的变更就会上线了。

## 基于本地克隆副本开展工作   {#fork-the-repo}

如果你有 git 的使用经验，或者你要提议的修改不仅仅几行，请使用本地克隆副本来开展工作。

首先要确保你在本地计算机上安装了 [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)。
你也可以使用 git 的带用户界面的应用。

图 2 显示了基于本地克隆副本开展工作的步骤。每个步骤的细节如下。


{{< mermaid >}}
flowchart LR
1[派生 kubernetes/website<br>仓库] --> 2[创建本地克隆副本<br>并指定 upstream 仓库]
subgraph changes[你的变更]
direction TB
S[ ] -.-
3[创建一个分支<br>例如: my_new_branch] --> 3a[使用文本编辑器<br>进行修改] --> 4["使用 Hugo 在本地<br>预览你的变更<br>(localhost:1313)<br>或构建容器镜像"]
end
subgraph changes2[提交 / 推送]
direction TB
T[ ] -.-
5[提交你的变更] --> 6[将提交推送到<br>origin/my_new_branch]
end

2 --> changes --> changes2

classDef grey fill:#dddddd,stroke:#ffffff,stroke-width:px,color:#000000, font-size:15px;
classDef white fill:#ffffff,stroke:#000,stroke-width:px,color:#000,font-weight:bold
classDef k8s fill:#326ce5,stroke:#fff,stroke-width:1px,color:#fff;
classDef spacewhite fill:#ffffff,stroke:#fff,stroke-width:0px,color:#000
class 1,2,3,3a,4,5,6 grey
class S,T spacewhite
class changes,changes2 white
{{</ mermaid >}}

图 2. 使用本地克隆副本进行修改。

### 派生 kubernetes/website 仓库   {#fork-the-kubernetes-website-repository}

1. 前往 [`kubernetes/website`](https://github.com/kubernetes/website/) 仓库；
1. 选择 **Fork**.

### 创建一个本地克隆副本并指定 upstream 仓库   {#create-a-local-clone-and-set-the-upstream}

1. 打开终端窗口，克隆你所派生的副本，并更新 [Docsy Hugo 主题](https://github.com/google/docsy#readme)：

   ```shell
   git clone git@github.com:<github_username>/website
   cd website
   git submodule update --init --recursive --depth 1
   ```

2. 前往新的 `website` 目录，将 `kubernetes/website` 仓库设置为 `upstream`
   远端：

   ```shell
   cd website

   git remote add upstream https://github.com/kubernetes/website.git
   ```

3. 确认你现在有两个仓库 `origin` 和 `upstream`：

   ```shell
   git remote -v
   ```

   输出类似于：

   ```none
   origin	git@github.com:<github_username>/website.git (fetch)
   origin	git@github.com:<github_username>/website.git (push)
   upstream	https://github.com/kubernetes/website.git (fetch)
   upstream	https://github.com/kubernetes/website.git (push)
   ```

4. 从你的克隆副本取回 `origin/main` 分支，从 `kubernetes/website` 取回 `upstream/main`：

   ```shell
   git fetch origin
   git fetch upstream
   ```

   这样可以确保你本地的仓库在开始工作前是最新的。

   {{< note >}}
   此工作流程与 [Kubernetes 社区 GitHub 工作流](https://github.com/kubernetes/community/blob/master/contributors/guide/github-workflow.md)有所不同。
   在推送你的变更到你的远程派生副本库之前，你不需要将你本地的 `main` 与 `upstream/main` 合并。
   {{< /note >}}

### 创建一个分支   {#create-a-branch}

1. 决定你要基于哪个分支来开展工作：

   - 针对已有内容的改进，请使用 `upstream/main`。
   - 针对已有功能特性的新文档内容，请使用 `upstream/main`。
   - 对于本地化内容，请基于本地化的约定。
     可参考[本地化 Kubernetes 文档](/zh-cn/docs/contribute/localization/)了解详细信息。
   - 对于在下一个 Kubernetes 版本中新功能特性的文档，使用独立的功能特性分支。
     参考[为发行版本撰写功能特性文档](/zh-cn/docs/contribute/new-content/new-features/)了解更多信息。
   - 对于很多 SIG Docs 共同参与的，需较长时间才完成的任务，例如内容的重构，
     请使用为该任务创建的特性分支。

   如果你在选择分支上需要帮助，请在 `#sig-docs` Slack 频道提问。

2. 基于第 1 步中选定的分支，创建新分支。
   下面的例子假定基础分支是 `upstream/main`：

   ```shell
   git checkout -b <my_new_branch> upstream/main
   ```

3. 使用文本编辑器进行修改。

在任何时候，都可以使用 `git status` 命令查看你所改变了的文件列表。

### 提交你的变更   {#commit-your-changes}

当你准备好发起拉取请求（PR）时，提交你所做的变更。

1. 在你的本地仓库中，检查你要提交的文件：

   ```shell
   git status
   ```

   输出类似于：

   ```none
   On branch <my_new_branch>
   Your branch is up to date with 'origin/<my_new_branch>'.

   Changes not staged for commit:
   (use "git add <file>..." to update what will be committed)
   (use "git checkout -- <file>..." to discard changes in working directory)

   modified:   content/en/docs/contribute/new-content/contributing-content.md

   no changes added to commit (use "git add" and/or "git commit -a")
   ```

2. 将 **Changes not staged for commit** 下列举的文件添加到提交中：

   ```shell
   git add <your_file_name>
   ```

   针对每个文件重复此操作。

3. 添加完所有文件之后，创建一个提交（commit）：

   ```shell
   git commit -m "Your commit message"
   ```

   {{< note >}}
   不要在提交消息中使用任何 [GitHub 关键词](https://help.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)。
   你可以在后续的 PR 描述中使用这些关键词。
   {{< /note >}}

4. 推送你本地分支及其中的新提交到你的远程派生副本库：

   ```shell
   git push origin <my_new_branch>
   ```

### 在本地预览你的变更   {#preview-locally}

在推送变更或者发起 PR 之前在本地查看一下预览是个不错的主意。
通过预览你可以发现构建错误或者 Markdown 格式问题。

你可以构建网站的容器镜像或者在本地运行 Hugo。
构建容器镜像的方式比较慢，不过能够显示 [Hugo 短代码（shortcodes）](/zh-cn/docs/contribute/style/hugo-shortcodes/)，
因此对于调试是很有用的。

{{< tabs name="tab_with_hugo" >}}
{{% tab name="在容器内执行 Hugo" %}}

{{< note >}}
下面的命令中使用 Docker 作为默认的容器引擎。
如果需要重载这一行为，可以设置 `CONTAINER_ENGINE` 环境变量。
{{< /note >}}

1. 在本地构建容器镜像
   _如果你正在测试对 Hugo 工具本身的更改，则仅需要此步骤_

   ```shell
   # 在终端窗口中执行（如果有需要）
   make container-image
   ```

2. 在容器中启动 Hugo：

   ```shell
   # 在终端窗口中执行
   make container-serve
   ```

3. 启动浏览器，浏览 `https://localhost:1313`。
   Hugo 会监测文件的变更并根据需要重新构建网站。

4. 要停止本地 Hugo 实例，可返回到终端并输入 `Ctrl+C`，或者关闭终端窗口。

{{% /tab %}}
{{% tab name="在命令行执行 Hugo" %}}

另一种方式是，在你的本地计算机上安装并使用 `hugo` 命令：

1. 安装 [`website/netlify.toml`](https://raw.githubusercontent.com/kubernetes/website/main/netlify.toml)
   文件中指定的 [Hugo](https://gohugo.io/getting-started/installing/) 版本。

2.  如果你尚未更新你的网站仓库，则 `website/themes/docsy` 目录是空的。
    如果本地缺少主题的副本，则该站点无法构建。
    要更新网站主题，运行以下命令：

   ```shell
   git submodule update --init --recursive --depth 1
   ```

3. 启动一个终端窗口，进入 Kubernetes 网站仓库目录，启动 Hugo 服务器：

   ```shell
   cd <path_to_your_repo>/website
   hugo server --buildFuture
   ```

4. 在浏览器的地址栏输入： `https://localhost:1313`。
   Hugo 会监测文件的变更并根据需要重新构建网站。

5. 要停止本地 Hugo 实例，返回到终端窗口并输入 `Ctrl+C` 或者关闭终端窗口。

{{% /tab %}}
{{< /tabs >}}

### 从你的克隆副本向 kubernetes/website 发起拉取请求（PR）   {#open-a-pr}

图 3 显示了从你的克隆副本向 kubernetes/website 发起 PR 的步骤。
详细信息如下。


{{< mermaid >}}
flowchart LR
subgraph first[ ]
direction TB
1[1. 前往 kubernetes/website 仓库] --> 2[2. 选择 New Pull Request]
2 --> 3[3. 选择 compare across forks]
3 --> 4[4. 从 head repository 下拉菜单<br>选择你的克隆副本]
end
subgraph second [ ]
direction TB
5[5. 从 compare 下拉菜单<br>选择你的分支] --> 6[6. 选择 Create Pull Request]
6 --> 7[7. 为你的 PR<br>添加一个描述]
7 --> 8[8. 选择 Create pull request]
end

first --> second

classDef grey fill:#dddddd,stroke:#ffffff,stroke-width:px,color:#000000, font-size:15px;
classDef white fill:#ffffff,stroke:#000,stroke-width:px,color:#000,font-weight:bold
class 1,2,3,4,5,6,7,8 grey
class first,second white
{{</ mermaid >}}

图 3. 从你的克隆副本向 kubernetes/website 发起一个 PR 的步骤。

1. 在 Web 浏览器中，前往 [`kubernetes/website`](https://github.com/kubernetes/website/) 仓库；
1. 点击 **New Pull Request**；
1. 选择 **compare across forks**；
1. 从 **head repository** 下拉菜单中，选取你的派生仓库；
1. 从 **compare** 下拉菜单中，选择你的分支；
1. 点击 **Create Pull Request**；
1. 为你的拉取请求添加一个描述：

    - **Title** （不超过 50 个字符）：总结变更的目的；
    - **Description**：给出变更的详细信息；

      - 如果存在一个相关联的 GitHub Issue，可以在描述中包含 `Fixes #12345` 或
        `Closes #12345`。GitHub 的自动化设施能够在当前 PR 被合并时自动关闭所提及
        的 Issue。如果有其他相关联的 PR，也可以添加对它们的链接。
      - 如果你特别希望获得某方面的建议，可以在描述中包含你希望评阅人思考的问题。

1. 点击 **Create pull request** 按钮。

祝贺你！你的拉取请求现在出现在 [Pull Requests](https://github.com/kubernetes/website/pulls) 列表中了！

在发起 PR 之后，GitHub 会执行一些自动化的测试，并尝试使用
[Netlify](https://www.netlify.com/) 部署一个预览版本。

- 如果 Netlify 构建操作失败，可选择 **Details** 了解详细信息。
- 如果 Netlify 构建操作成功，选择 **Details** 会打开 Kubernetes 的一个预览版本，
  其中包含了你所作的变更。评阅人也使用这一功能来检查你的变更。

GitHub 也会自动为 PR 分派一些标签，以帮助评阅人。
如果有需要，你也可以向 PR 添加标签。
欲了解相关详细信息，可以参考
[添加和删除 Issue 标签](/zh-cn/docs/contribute/review/for-approvers/#adding-and-removing-issue-labels)。

### 在本地处理反馈   {#addressing-feedback-locally}

1. 在本地完成修改之后，可以修补（amend）你之前的提交：

   ```shell
   git commit -a --amend
   ```

   - `-a`：提交所有修改
   - `--amend`：对前一次提交进行增补，而不是创建新的提交

2. 如果有必要，更新你的提交消息；

3. 使用 `git push origin <my_new_branch>` 来推送你的变更，重新触发 Netlify 测试。

   {{< note >}}
   如果你使用 `git commit -m` 而不是增补参数，在 PR 最终合并之前你必须
   [squash 你的提交](#squashing-commits)。
   {{< /note >}}

#### 来自评阅人的修改   {#changes-from-reviewers}

有时评阅人会向你的 PR 中提交修改。在作出其他修改之前，请先取回这些提交。

1. 从你的远程派生副本仓库取回提交，让你的工作分支基于所取回的分支：

   ```shell
   git fetch origin
   git rebase origin/<your-branch-name>
   ```

2. 变更基线（rebase）操作完成之后，强制推送本地的新改动到你的派生仓库：

   ```shell
   git push --force-with-lease origin <your-branch-name>
   ```

#### 合并冲突和重设基线   {#merge-conflicts-and-rebasing}

{{< note >}}
要了解更多信息，可参考
[Git Branching - Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging#_basic_merge_conflicts)、
[Advanced Merging](https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging)，
或者在 `#sig-docs` Slack 频道寻求帮助。
{{< /note >}}

如果另一个贡献者在别的 PR 中提交了对同一文件的修改，这可能会造成合并冲突。
你必须在你的 PR 中解决所有合并冲突。

1. 更新你的派生副本，重设本地分支的基线：

   ```shell
   git fetch origin
   git rebase origin/<your-branch-name>
   ```

   之后强制推送修改到你的派生副本仓库：

   ```shell
   git push --force-with-lease origin <your-branch-name>
   ```

2. 从 `kubernetes/website` 的 `upstream/main` 分支取回更改，然后重设本地分支的基线：

   ```shell
   git fetch upstream
   git rebase upstream/main
   ```

3. 检查重设基线操作之后的状态：

   ```shell
   git status
   ```

   你会看到一组存在冲突的文件。

4. 打开每个存在冲突的文件，查找冲突标记：`>>>`、`<<<` 和 `===`。
   解决完冲突之后删除冲突标记。

   {{< note >}}
   进一步的详细信息可参见
   [冲突是怎样表示的](https://git-scm.com/docs/git-merge#_how_conflicts_are_presented).
   {{< /note >}}

5. 添加文件到变更集合：

   ```shell
   git add <filename>
   ```

6. 继续执行基线变更（rebase）操作：

   ```shell
   git rebase --continue
   ```

7. 根据需要重复步骤 2 到 5。

   在应用完所有提交之后，`git status` 命令会显示 rebase 操作完成。

8. 将分支强制推送到你的派生仓库：

   ```shell
   git push --force-with-lease origin <your-branch-name>
   ```

   PR 不再显示存在冲突。

### 压缩（Squashing）提交   {#squashing-commits}

{{< note >}}
要了解更多信息，可参看
[Git Tools - Rewriting History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)，
或者在 `#sig-docs` Slack 频道寻求帮助。
{{< /note >}}

如果你的 PR 包含多个提交（commits），你必须将其压缩成一个提交才能被合并。
你可以在 PR 的 **Commits** Tab 页面查看提交个数，也可以在本地通过
`git log` 命令查看提交个数。

{{< note >}}
本主题假定使用 `vim` 作为命令行文本编辑器。
{{< /note >}}

1. 启动一个交互式的 rebase 操作：

   ```shell
   git rebase -i HEAD~<number_of_commits_in_branch>
   ```


   压缩提交的过程也是一种重设基线的过程。
   这里的 `-i` 开关告诉 git 你希望交互式地执行重设基线操作。
   `HEAD~<number_of_commits_in_branch` 表明在 rebase 操作中查看多少个提交。


   输出类似于；

   ```none
   pick d875112ca Original commit
   pick 4fa167b80 Address feedback 1
   pick 7d54e15ee Address feedback 2

   # Rebase 3d18sf680..7d54e15ee onto 3d183f680 (3 commands)

   ...

   # These lines can be re-ordered; they are executed from top to bottom.
   ```


   输出的第一部分列举了重设基线操作中的提交。
   第二部分给出每个提交的选项。
   改变单词 `pick` 就可以改变重设基线操作之后提交的状态。

   就重设基线操作本身，我们关注 `squash` 和 `pick` 选项。

   {{< note >}}
   进一步的详细信息可参考 [Interactive Mode](https://git-scm.com/docs/git-rebase#_interactive_mode)。
   {{< /note >}}


2. 开始编辑文件。

   修改原来的文本：

   ```none
   pick d875112ca Original commit
   pick 4fa167b80 Address feedback 1
   pick 7d54e15ee Address feedback 2
   ```

   使之成为：

   ```none
   pick d875112ca Original commit
   squash 4fa167b80 Address feedback 1
   squash 7d54e15ee Address feedback 2
   ```

   以上编辑操作会压缩提交 `4fa167b80 Address feedback 1` 和 `7d54e15ee Address feedback 2`
   到 `d875112ca Original commit` 中，只留下 `d875112ca Original commit` 成为时间线中的一部分。

3. 保存文件并退出编辑器。

4. 推送压缩后的提交：

   ```shell
   git push --force-with-lease origin <branch_name>
   ```

## 贡献到其他仓库   {#contribute-to-other-repos}

[Kubernetes 项目](https://github.com/kubernetes)包含大约 50 多个仓库。
这些仓库中很多都有文档：提供给最终用户的帮助文本、错误信息、API 参考或者代码注释等。

如果你发现有些文本需要改进，可以使用 GitHub 来搜索 Kubernetes 组织下的所有仓库。
这样有助于发现要在哪里提交 Issue 或 PR。

每个仓库有其自己的流程和过程。在登记 Issue 或者发起 PR 之前，
记得阅读仓库可能存在的 `README.md`、`CONTRIBUTING.md` 和
`code-of-conduct.md` 文件。

大多数仓库都有自己的 Issue 和 PR 模板。
通过查看一些待解决的 Issue 和 PR，
你可以大致了解协作的流程。
在登记 Issue 或提出 PR 时，务必尽量填充所给的模板，多提供详细信息。

## {{% heading "whatsnext" %}}

- 阅读[评阅](/zh-cn/docs/contribute/review/reviewing-prs)节，学习评阅过程。

