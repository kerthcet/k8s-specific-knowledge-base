---
title: Pod 安全性标准
description: >
  详细了解 Pod 安全性标准（Pod Security Standards）中所定义的不同策略级别。
content_type: concept
weight: 10
---


Pod 安全性标准定义了三种不同的**策略（Policy）**，以广泛覆盖安全应用场景。
这些策略是**叠加式的（Cumulative）**，安全级别从高度宽松至高度受限。
本指南概述了每个策略的要求。

| Profile | 描述 |
| ------ | ----------- |
| <strong style="white-space: nowrap">Privileged</strong> | 不受限制的策略，提供最大可能范围的权限许可。此策略允许已知的特权提升。 |
| <strong style="white-space: nowrap">Baseline</strong> | 限制性最弱的策略，禁止已知的策略提升。允许使用默认的（规定最少）Pod 配置。 |
| <strong style="white-space: nowrap">Restricted</strong> | 限制性非常强的策略，遵循当前的保护 Pod 的最佳实践。 |


## Profile 细节    {#profile-details}

### Privileged

**_Privileged_ 策略是有目的地开放且完全无限制的策略。**
此类策略通常针对由特权较高、受信任的用户所管理的系统级或基础设施级负载。

Privileged 策略定义中限制较少。默认允许的（Allow-by-default）实施机制（例如 gatekeeper）
可以缺省设置为 Privileged。
与此不同，对于默认拒绝（Deny-by-default）的实施机制（如 Pod 安全策略）而言，
Privileged 策略应该禁止所有限制。

### Baseline

**_Baseline_ 策略的目标是便于常见的容器化应用采用，同时禁止已知的特权提升。**
此策略针对的是应用运维人员和非关键性应用的开发人员。
下面列举的控制应该被实施（禁止）：

{{< note >}}
在下述表格中，通配符（`*`）意味着一个列表中的所有元素。
例如 `spec.containers[*].securityContext` 表示**所定义的所有容器**的安全性上下文对象。
如果所列出的任一容器不能满足要求，整个 Pod 将无法通过校验。
{{< /note >}}

<table>
	<caption style="display:none">Baseline 策略规范</caption>
	<tbody>
		<tr>
			<td>控制（Control）</td>
			<td>策略（Policy）</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">HostProcess</td>
			<td>
                                Windows Pod 提供了运行 <a href="/zh-cn/docs/tasks/configure-pod-container/create-hostprocess-pod">HostProcess 容器</a> 的能力，这使得对 Windows 节点的特权访问成为可能。Baseline 策略中禁止对宿主的特权访问。{{< feature-state for_k8s_version="v1.26" state="stable" >}}
                                </p>
				<ul>
					<li><code>spec.securityContext.windowsOptions.hostProcess</code></li>
					<li><code>spec.containers[*].securityContext.windowsOptions.hostProcess</code></li>
					<li><code>spec.initContainers[*].securityContext.windowsOptions.hostProcess</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.windowsOptions.hostProcess</code></li>
				</ul>
				<ul>
					<li><code>false</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<ul>
					<li><code>spec.hostNetwork</code></li>
					<li><code>spec.hostPID</code></li>
					<li><code>spec.hostIPC</code></li>
				</ul>
				<ul>
					<li><code>false</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<ul>
					<li><code>spec.containers[*].securityContext.privileged</code></li>
					<li><code>spec.initContainers[*].securityContext.privileged</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.privileged</code></li>
				</ul>
				<ul>
					<li><code>false</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<ul>
					<li><code>spec.containers[*].securityContext.capabilities.add</code></li>
					<li><code>spec.initContainers[*].securityContext.capabilities.add</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.capabilities.add</code></li>
				</ul>
				<ul>
					<li><code>AUDIT_WRITE</code></li>
					<li><code>CHOWN</code></li>
					<li><code>DAC_OVERRIDE</code></li>
					<li><code>FOWNER</code></li>
					<li><code>FSETID</code></li>
					<li><code>KILL</code></li>
					<li><code>MKNOD</code></li>
					<li><code>NET_BIND_SERVICE</code></li>
					<li><code>SETFCAP</code></li>
					<li><code>SETGID</code></li>
					<li><code>SETPCAP</code></li>
					<li><code>SETUID</code></li>
					<li><code>SYS_CHROOT</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<ul>
					<li><code>spec.volumes[*].hostPath</code></li>
				</ul>
				<ul>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<ul>
					<li><code>spec.containers[*].ports[*].hostPort</code></li>
					<li><code>spec.initContainers[*].ports[*].hostPort</code></li>
					<li><code>spec.ephemeralContainers[*].ports[*].hostPort</code></li>
				</ul>
				<ul>
					<li><code>0</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">AppArmor</td>
			<td>
				<ul>
					<li><code>metadata.annotations["container.apparmor.security.beta.kubernetes.io/*"]</code></li>
				</ul>
				<ul>
					<li><code>runtime/default</code></li>
					<li><code>localhost/*</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">SELinux</td>
			<td>
				<ul>
					<li><code>spec.securityContext.seLinuxOptions.type</code></li>
					<li><code>spec.containers[*].securityContext.seLinuxOptions.type</code></li>
					<li><code>spec.initContainers[*].securityContext.seLinuxOptions.type</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.seLinuxOptions.type</code></li>
				</ul>
				<ul>
					<li><code>container_t</code></li>
					<li><code>container_init_t</code></li>
					<li><code>container_kvm_t</code></li>
				</ul>
				<hr />
				<ul>
					<li><code>spec.securityContext.seLinuxOptions.user</code></li>
					<li><code>spec.containers[*].securityContext.seLinuxOptions.user</code></li>
					<li><code>spec.initContainers[*].securityContext.seLinuxOptions.user</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.seLinuxOptions.user</code></li>
					<li><code>spec.securityContext.seLinuxOptions.role</code></li>
					<li><code>spec.containers[*].securityContext.seLinuxOptions.role</code></li>
					<li><code>spec.initContainers[*].securityContext.seLinuxOptions.role</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.seLinuxOptions.role</code></li>
				</ul>
				<ul>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<ul>
					<li><code>spec.containers[*].securityContext.procMount</code></li>
					<li><code>spec.initContainers[*].securityContext.procMount</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.procMount</code></li>
				</ul>
				<ul>
					<li><code>Default</code></li>
				</ul>
			</td>
		</tr>
		<tr>
  			<td>Seccomp</td>
  			<td>
				<ul>
					<li><code>spec.securityContext.seccompProfile.type</code></li>
					<li><code>spec.containers[*].securityContext.seccompProfile.type</code></li>
					<li><code>spec.initContainers[*].securityContext.seccompProfile.type</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.seccompProfile.type</code></li>
				</ul>
				<ul>
					<li><code>RuntimeDefault</code></li>
					<li><code>Localhost</code></li>
				</ul>
  			</td>
  		</tr>
		<tr>
			<td style="white-space: nowrap">Sysctls</td>
			<td>
				<ul>
					<li><code>spec.securityContext.sysctls[*].name</code></li>
				</ul>
				<ul>
					<li><code>kernel.shm_rmid_forced</code></li>
					<li><code>net.ipv4.ip_local_port_range</code></li>
					<li><code>net.ipv4.ip_unprivileged_port_start</code></li>
					<li><code>net.ipv4.tcp_syncookies</code></li>
					<li><code>net.ipv4.ping_group_range</code></li>
				</ul>
			</td>
		</tr>
	</tbody>
</table>

### Restricted

**_Restricted_ 策略旨在实施当前保护 Pod 的最佳实践，尽管这样作可能会牺牲一些兼容性。**
该类策略主要针对运维人员和安全性很重要的应用的开发人员，以及不太被信任的用户。
下面列举的控制需要被实施（禁止）：

{{< note >}}
在下述表格中，通配符（`*`）意味着一个列表中的所有元素。
例如 `spec.containers[*].securityContext` 表示 **所定义的所有容器** 的安全性上下文对象。
如果所列出的任一容器不能满足要求，整个 Pod 将无法通过校验。
{{< /note >}}

<table>
	<tbody>
		<tr>
		</tr>
		<tr>
		</tr>
		<tr>
			<td>
				<ul>
					<li><code>spec.volumes[*]</code></li>
				</ul>
				<ul>
					<li><code>spec.volumes[*].configMap</code></li>
					<li><code>spec.volumes[*].csi</code></li>
					<li><code>spec.volumes[*].downwardAPI</code></li>
					<li><code>spec.volumes[*].emptyDir</code></li>
					<li><code>spec.volumes[*].ephemeral</code></li>
					<li><code>spec.volumes[*].persistentVolumeClaim</code></li>
					<li><code>spec.volumes[*].projected</code></li>
					<li><code>spec.volumes[*].secret</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<ul>
					<li><code>spec.containers[*].securityContext.allowPrivilegeEscalation</code></li>
					<li><code>spec.initContainers[*].securityContext.allowPrivilegeEscalation</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.allowPrivilegeEscalation</code></li>
				</ul>
				<ul>
					<li><code>false</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td>
				<ul>
					<li><code>spec.securityContext.runAsNonRoot</code></li>
					<li><code>spec.containers[*].securityContext.runAsNonRoot</code></li>
					<li><code>spec.initContainers[*].securityContext.runAsNonRoot</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.runAsNonRoot</code></li>
				</ul>
				<ul>
					<li><code>true</code></li>
				</ul>
				<small>
				</small>
			</td>
		</tr>
		<tr>
			<td>
				<ul>
					<li><code>spec.securityContext.runAsUser</code></li>
          <li><code>spec.containers[*].securityContext.runAsUser</code></li>
					<li><code>spec.initContainers[*].securityContext.runAsUser</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.runAsUser</code></li>
				</ul>
				<ul>
					<li><code>undefined/null</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Seccomp (v1.19+)</td>
			<td>
				<ul>
					<li><code>spec.securityContext.seccompProfile.type</code></li>
					<li><code>spec.containers[*].securityContext.seccompProfile.type</code></li>
					<li><code>spec.initContainers[*].securityContext.seccompProfile.type</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.seccompProfile.type</code></li>
				</ul>
				<ul>
					<li><code>RuntimeDefault</code></li>
					<li><code>Localhost</code></li>
				</ul>
				<small>
          如果 Pod 级别的 <code>spec.securityContext.seccompProfile.type</code>
          已设置得当，容器级别的安全上下文字段可以为未定义/<code>nil</code>。
          反之如果 <bold>所有的</bold> 容器级别的安全上下文字段已设置，
          则 Pod 级别的字段可为 未定义/<code>nil</code>。
				</small>
  			</td>
  		</tr>
		  <tr>
			<td>
				<p>
          容器必须弃用 <code>ALL</code> 权能，并且只允许添加
          <code>NET_BIND_SERVICE</code> 权能。<em><a href="#policies-specific-to-linux">这是 v1.25+ 中仅针对 Linux 的策略</a> <code>(.spec.os.name != "windows")</code></em>
				</p>
				<ul>
					<li><code>spec.containers[*].securityContext.capabilities.drop</code></li>
					<li><code>spec.initContainers[*].securityContext.capabilities.drop</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.capabilities.drop</code></li>
				</ul>
				<ul>
				</ul>
				<hr />
				<ul>
					<li><code>spec.containers[*].securityContext.capabilities.add</code></li>
					<li><code>spec.initContainers[*].securityContext.capabilities.add</code></li>
					<li><code>spec.ephemeralContainers[*].securityContext.capabilities.add</code></li>
				</ul>
				<ul>
					<li><code>NET_BIND_SERVICE</code></li>
				</ul>
			</td>
		</tr>
	</tbody>
</table>

## 策略实例化   {#policy-instantiation}

将策略定义从策略实例中解耦出来有助于形成跨集群的策略理解和语言陈述，
以免绑定到特定的下层实施机制。

随着相关机制的成熟，这些机制会按策略分别定义在下面。特定策略的实施方法不在这里定义。

[**Pod 安全性准入控制器**](/zh-cn/docs/concepts/security/pod-security-admission/)

- {{< example file="security/podsecurity-privileged.yaml" >}}Privileged 名字空间{{< /example >}}
- {{< example file="security/podsecurity-baseline.yaml" >}}Baseline 名字空间{{< /example >}}
- {{< example file="security/podsecurity-restricted.yaml" >}}Restricted 名字空间{{< /example >}}

### 替代方案   {#alternatives}

{{% thirdparty-content %}}

在 Kubernetes 生态系统中还在开发一些其他的替代方案，例如：

- [Kubewarden](https://github.com/kubewarden)
- [Kyverno](https://kyverno.io/policies/pod-security/)
- [OPA Gatekeeper](https://github.com/open-policy-agent/gatekeeper)

## Pod OS 字段   {#pod-os-field}

Kubernetes 允许你使用运行 Linux 或 Windows 的节点。你可以在一个集群中混用两种类型的节点。
Kubernetes 中的 Windows 与基于 Linux 的工作负载相比有一些限制和差异。
具体而言，许多 Pod `securityContext`
字段[在 Windows 上不起作用](/zh-cn/docs/concepts/windows/intro/#compatibility-v1-pod-spec-containers-securitycontext)。


{{< note >}}
v1.24 之前的 Kubelet 不强制处理 Pod OS 字段，如果集群中有些节点运行早于 v1.24 的版本，
则应将限制性的策略锁定到 v1.25 之前的版本。
{{< /note >}}

### 限制性的 Pod Security Standard 变更   {#restricted-pod-security-standard-changes}

Kubernetes v1.25 中的另一个重要变化是**限制性的（Restricted）** Pod 安全性已更新，
能够处理 `pod.spec.os.name` 字段。根据 OS 名称，专用于特定 OS 的某些策略对其他 OS 可以放宽限制。

#### OS 特定的策略控制

仅当 `.spec.os.name` 不是 `windows` 时，才需要对以下控制进行限制：
- 特权提升
- Seccomp
- Linux 权能

## 常见问题    {#faq}

### 为什么不存在介于 Privileged 和 Baseline 之间的策略类型

这里定义的三种策略框架有一个明晰的线性递进关系，从最安全（Restricted）到最不安全，
并且覆盖了很大范围的工作负载。特权要求超出 Baseline 策略者通常是特定于应用的需求，
所以我们没有在这个范围内提供标准框架。
这并不意味着在这样的情形下仍然只能使用 Privileged 框架，
只是说处于这个范围的策略需要因地制宜地定义。

SIG Auth 可能会在将来考虑这个范围的框架，前提是有对其他框架的需求。

### 安全配置与安全上下文的区别是什么？

[安全上下文](/zh-cn/docs/tasks/configure-pod-container/security-context/)在运行时配置 Pod
和容器。安全上下文是在 Pod 清单中作为 Pod 和容器规约的一部分来定义的，
所代表的是传递给容器运行时的参数。

安全策略则是控制面用来对安全上下文以及安全性上下文之外的参数实施某种设置的机制。
在 2020 年 7 月，
[Pod 安全性策略](/zh-cn/docs/concepts/security/pod-security-policy/)已被废弃，
取而代之的是内置的 [Pod 安全性准入控制器](/zh-cn/docs/concepts/security/pod-security-admission/)。

### 沙箱（Sandboxed）Pod 怎么处理？  {#what-about-sandboxed-pods}

现在还没有 API 标准来控制 Pod 是否被视作沙箱化 Pod。
沙箱 Pod 可以通过其是否使用沙箱化运行时（如 gVisor 或 Kata Container）来辨别，
不过目前还没有关于什么是沙箱化运行时的标准定义。

沙箱化负载所需要的保护可能彼此各不相同。例如，当负载与下层内核直接隔离开来时，
限制特权化操作的许可就不那么重要。这使得那些需要更多许可权限的负载仍能被有效隔离。

此外，沙箱化负载的保护高度依赖于沙箱化的实现方法。
因此，现在还没有针对所有沙箱化负载的建议配置。

