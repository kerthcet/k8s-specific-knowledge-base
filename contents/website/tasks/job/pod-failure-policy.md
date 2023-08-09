---
title: 使用 Pod 失效策略处理可重试和不可重试的 Pod 失效
content_type: task
min-kubernetes-server-version: v1.25
weight: 60
---

{{< feature-state for_k8s_version="v1.26" state="beta" >}}


本文向你展示如何结合默认的 [Pod 回退失效策略](/zh-cn/docs/concepts/workloads/controllers/job#pod-backoff-failure-policy)来使用
[Pod 失效策略](/zh-cn/docs/concepts/workloads/controllers/job#pod-failure-policy)，
以改善 {{<glossary_tooltip text="Job" term_id="job">}} 内处理容器级别或 Pod 级别的失效。

Pod 失效策略的定义可以帮助你：
* 避免不必要的 Pod 重试，以更好地利用计算资源。
* 避免由于 Pod 干扰（例如{{<glossary_tooltip text="抢占" term_id="preemption" >}}、
  {{<glossary_tooltip text="API 发起的驱逐" term_id="api-eviction" >}}或基于{{<glossary_tooltip text="污点" term_id="taint" >}}的驱逐）
  而造成的 Job 失败。

## {{% heading "prerequisites" %}}

你应该已熟悉了 [Job](/zh-cn/docs/concepts/workloads/controllers/job/) 的基本用法。

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

确保[特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates/)
`PodDisruptionConditions` 和 `JobPodFailurePolicy` 在你的集群中均已启用。

## 使用 Pod 失效策略以避免不必要的 Pod 重试  {#using-pod-failure-policy-to-avoid-unecessary-pod-retries}

借用以下示例，你可以学习在 Pod 失效表明有一个不可重试的软件漏洞时如何使用
Pod 失效策略来避免不必要的 Pod 重启。

首先，基于配置创建一个 Job：

{{< codenew file="/controllers/job-pod-failure-policy-failjob.yaml" >}}

运行以下命令：

```sh
kubectl create -f job-pod-failure-policy-failjob.yaml
```

大约 30 秒后，整个 Job 应被终止。通过运行以下命令来查看 Job 的状态：

```sh
kubectl get jobs -l job-name=job-pod-failure-policy-failjob -o yaml
```

在 Job 状态中，看到一个任务状况为 `Failed`，其 `reason` 字段等于 `PodFailurePolicy`。
此外，`message` 字段包含有关 Job 终止更详细的信息，例如：
`Container main for pod default/job-pod-failure-policy-failjob-8ckj8 failed with exit code 42 matching FailJob rule at index 0`。

为了比较，如果 Pod 失效策略被禁用，将会让 Pod 重试 6 次，用时至少 2 分钟。

### 清理

删除你创建的 Job：

```sh
kubectl delete jobs/job-pod-failure-policy-failjob
```

集群自动清理这些 Pod。

## 使用 Pod 失效策略来忽略 Pod 干扰  {#using-pod-failure-policy-to-ignore-pod-disruptions}

通过以下示例，你可以学习如何使用 Pod 失效策略将 Pod 重试计数器朝着 `.spec.backoffLimit` 限制递增来忽略 Pod 干扰。

{{< caution >}}
这个示例的时机比较重要，因此你可能需要在执行之前阅读这些步骤。
为了触发 Pod 干扰，重要的是在 Pod 在其上运行时（自 Pod 调度后的 90 秒内）腾空节点。
{{< /caution >}}

1. 基于配置创建 Job：

   {{< codenew file="/controllers/job-pod-failure-policy-ignore.yaml" >}}

   运行以下命令：

   ```sh
   kubectl create -f job-pod-failure-policy-ignore.yaml
   ```

2. 运行以下这条命令检查将 Pod 调度到的 `nodeName`：

   ```sh
   nodeName=$(kubectl get pods -l job-name=job-pod-failure-policy-ignore -o jsonpath='{.items[0].spec.nodeName}')
   ```

3. 腾空该节点以便在 Pod 完成任务之前将其驱逐（90 秒内）：

   ```sh
   kubectl drain nodes/$nodeName --ignore-daemonsets --grace-period=0
   ```

4. 查看 `.status.failed` 以检查针对 Job 的计数器未递增：

   ```sh
   kubectl get jobs -l job-name=job-pod-failure-policy-ignore -o yaml
   ```

5. 解除节点的保护：

   ```sh
   kubectl uncordon nodes/$nodeName
   ```

Job 恢复并成功完成。

为了比较，如果 Pod 失效策略被禁用，Pod 干扰将使得整个 Job 终止（随着 `.spec.backoffLimit` 设置为 0）。

### 清理

删除你创建的 Job：

```sh
kubectl delete jobs/job-pod-failure-policy-ignore
```

集群自动清理 Pod。

## 基于自定义 Pod 状况使用 Pod 失效策略避免不必要的 Pod 重试   {#avoid-pod-retries-based-on-custom-conditions}

根据以下示例，你可以学习如何基于自定义 Pod 状况使用 Pod 失效策略避免不必要的 Pod 重启。

{{< note >}}
以下示例自 v1.27 起开始生效，因为它依赖于将已删除的 Pod 从 `Pending` 阶段过渡到终止阶段
（参阅 [Pod 阶段](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase)）。
{{< /note >}}

1. 首先基于配置创建一个 Job：

   {{< codenew file="/controllers/job-pod-failure-policy-config-issue.yaml" >}}

   执行以下命令：

   ```sh
   kubectl create -f job-pod-failure-policy-config-issue.yaml
   ```

   请注意，镜像配置不正确，因为该镜像不存在。

2. 通过执行以下命令检查任务 Pod 的状态：

   ```sh
   kubectl get pods -l job-name=job-pod-failure-policy-config-issue -o yaml
   ```

   你将看到类似以下输出：

   ```yaml
   containerStatuses:
   - image: non-existing-repo/non-existing-image:example
      ...
      state:
      waiting:
         message: Back-off pulling image "non-existing-repo/non-existing-image:example"
         reason: ImagePullBackOff
         ...
   phase: Pending
   ```

   请注意，Pod 依然处于 `Pending` 阶段，因为它无法拉取错误配置的镜像。
   原则上讲这可能是一个暂时问题，镜像还是会被拉取。然而这种情况下，
   镜像不存在，因为我们通过一个自定义状况表明了这个事实。

3. 添加自定义状况。执行以下命令先准备补丁：

   ```sh
   cat <<EOF > patch.yaml
   status:
     conditions:
     - type: ConfigIssue
       status: "True"
       reason: "NonExistingImage"
       lastTransitionTime: "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
   EOF
   ```

   其次，执行以下命令选择通过任务创建的其中一个 Pod：

   ```
   podName=$(kubectl get pods -l job-name=job-pod-failure-policy-config-issue -o jsonpath='{.items[0].metadata.name}')
   ```

   随后执行以下命令将补丁应用到其中一个 Pod 上：

   ```sh
   kubectl patch pod $podName --subresource=status --patch-file=patch.yaml
   ```

   如果被成功应用，你将看到类似以下的一条通知：

   ```sh
   pod/job-pod-failure-policy-config-issue-k6pvp patched
   ```

4. 执行以下命令删除此 Pod 将其过渡到 `Failed` 阶段：

   ```sh
   kubectl delete pods/$podName
   ```

5. 执行以下命令查验 Job 的状态：

   ```sh
   kubectl get jobs -l job-name=job-pod-failure-policy-config-issue -o yaml
   ```

   在 Job 状态中，看到任务 `Failed` 状况的 `reason` 字段等于 `PodFailurePolicy`。
   此外，`message` 字段包含了与 Job 终止相关的更多详细信息，例如：
   `Pod default/job-pod-failure-policy-config-issue-k6pvp has condition ConfigIssue matching FailJob rule at index 0`。

{{< note >}}
在生产环境中，第 3 和 4 步应由用户提供的控制器进行自动化处理。
{{< /note >}}

### 清理

删除你创建的 Job：

```sh
kubectl delete jobs/job-pod-failure-policy-config-issue
```

集群自动清理 Pod。

## 替代方案  {#alternatives}

通过指定 Job 的 `.spec.backoffLimit` 字段，你可以完全依赖
[Pod 回退失效策略](/zh-cn/docs/concepts/workloads/controllers/job#pod-backoff-failure-policy)。
然而在许多情况下，难题在于如何找到一个平衡，为 `.spec.backoffLimit` 设置一个较小的值以避免不必要的 Pod 重试，
同时这个值又足以确保 Job 不会因 Pod 干扰而终止。
