---
title: 从 PodSecurityPolicy 映射到 Pod 安全性标准
content_type: concept
weight: 95
---



下面的表格列举了 `PodSecurityPolicy`
对象上的配置参数，这些字段是否会变更或检查 Pod 配置，以及这些配置值如何映射到
[Pod 安全性标准（Pod Security Standards）](/zh-cn/docs/concepts/security/pod-security-standards/)
之上。

对于每个可应用的参数，表格中给出了
[Baseline](/zh-cn/docs/concepts/security/pod-security-standards/#baseline) 和
[Restricted](/zh-cn/docs/concepts/security/pod-security-standards/#restricted)
配置下可接受的取值。
对这两种配置而言不可接受的取值均归入
[Privileged](/zh-cn/docs/concepts/security/pod-security-standards/#privileged)
配置下。“无意见”意味着对所有 Pod 安全性标准而言所有取值都可接受。

如果想要了解如何一步步完成迁移，可参阅[从 PodSecurityPolicy 迁移到内置的 PodSecurity 准入控制器](/zh-cn/docs/tasks/configure-pod-container/migrate-from-psp/)。


## PodSecurityPolicy 规约   {#podsecuritypolicy-spec}

下面表格中所列举的字段是 `PodSecurityPolicySpec` 的一部分，是通过 `.spec`
字段路径来设置的。

<table class="no-word-break">
    <tbody>
      <tr>
      <th><code>PodSecurityPolicySpec</code></th>
    </tr>
    <tr>
      <td><code>privileged</code></td>
      <td><b>Baseline & Restricted</b>: <code>false</code> / 未定义 / nil</td>
    </tr>
    <tr>
      <td><code>defaultAddCapabilities</code></td>
    </tr>
    <tr>
      <td><code>allowedCapabilities</code></td>
      <td>
        <p><b>Baseline</b>：下面各项的子集</p>
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
        <p><b>Restricted</b>：空 / 未定义 / nil 或<i>仅</i>包含 <code>NET_BIND_SERVICE</code> 的列表</p>
      </td>
    </tr>
    <tr>
      <td><code>requiredDropCapabilities</code></td>
      <td>
      </td>
    </tr>
    <tr>
      <td><code>volumes</code></td>
      <td>
        <ul>
          <li><code>hostPath</code></li>
          <li><code>*</code></li>
        </ul>
        <ul>
          <li><code>configMap</code></li>
          <li><code>csi</code></li>
          <li><code>downwardAPI</code></li>
          <li><code>emptyDir</code></li>
          <li><code>ephemeral</code></li>
          <li><code>persistentVolumeClaim</code></li>
          <li><code>projected</code></li>
          <li><code>secret</code></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>hostNetwork</code></td>
      <td><b>Baseline & Restricted</b>：<code>false</code> / 未定义 / nil</td>
    </tr>
    <tr>
      <td><code>hostPorts</code></td>
      <td><b>Baseline & Restricted</b>：未定义 / nil / 空</td>
    </tr>
    <tr>
      <td><code>hostPID</code></td>
      <td><b>Baseline & Restricted</b>：<code>false</code> / 未定义 / nil</td>
    </tr>
    <tr>
      <td><code>hostIPC</code></td>
      <td><b>Baseline & Restricted</b>：<code>false</code> / 未定义 / nil</td>
    </tr>
    <tr>
      <td><code>seLinux</code></td>
      <td>
        <p><b>Baseline & Restricted</b>：
        <code>seLinux.rule</code> 为 <code>MustRunAs</code>，且 <code>options</code> 如下：
        </p>
        <ul>
          <li><code>user</code> 未设置（<code>""</code> / 未定义 / nil）</li>
          <li><code>role</code> 未设置（<code>""</code> / 未定义 / nil）</li>
          <li><code>type</code> 未设置或者取值为 <code>container_t</code>、<code>container_init_t</code> 或 <code>container_kvm_t</code> 之一</li>
          <li><code>level</code> 是任何取值</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>runAsUser</code></td>
      <td>
      </td>
    </tr>
    <tr>
      <td><code>runAsGroup</code></td>
      <td>
      </td>
    </tr>
    <tr>
      <td><code>supplementalGroups</code></td>
      <td>
      </td>
    </tr>
    <tr>
      <td><code>fsGroup</code></td>
      <td>
      </td>
    </tr>
    <tr>
      <td><code>readOnlyRootFilesystem</code></td>
      <td>
      </td>
    </tr>
    <tr>
      <td><code>defaultAllowPrivilegeEscalation</code></td>
      <td>
      </td>
    </tr>
    <tr>
      <td><code>allowPrivilegeEscalation</code></td>
      <td>
        <p><i>只有设置为 <code>false</code> 时才执行变更动作</i></p>
        <p><b>Baseline</b>：无意见</p>
        <p><b>Restricted</b>：<code>false</code></p>
      </td>
    </tr>
    <tr>
      <td><code>allowedHostPaths</code></td>
    </tr>
    <tr>
      <td><code>allowedFlexVolumes</code></td>
    </tr>
    <tr>
      <td><code>allowedCSIDrivers</code></td>
    </tr>
    <tr>
      <td><code>allowedUnsafeSysctls</code></td>
      <td><b>Baseline & Restricted</b>：未定义 / nil / 空</td>
    </tr>
    <tr>
      <td><code>forbiddenSysctls</code></td>
    </tr>
    <tr>
      <td><code>allowedProcMountTypes</code><br><i>(alpha feature)</i></td>
      <td><b>Baseline & Restricted</b>：<code>["Default"]</code> 或者未定义 / nil / 空</td>
    </tr>
    <tr>
      <td><code>runtimeClass</code><br><code>&nbsp;.defaultRuntimeClassName</code></td>
    </tr>
    <tr>
      <td><code>runtimeClass</code><br><code>&nbsp;.allowedRuntimeClassNames</code></td>
    </tr>
  </tbody>
</table>

## PodSecurityPolicy 注解    {#podsecuritypolicy-annotations}

下面表格中所列举的[注解](/zh-cn/docs/concepts/overview/working-with-objects/annotations/)可以通过
`.metadata.annotations` 设置到 PodSecurityPolicy 对象之上。

<table class="no-word-break">
  <tbody>
    <tr>
    </tr>
    <tr>
      <td><code>seccomp.security.alpha.kubernetes.io</code><br><code>/defaultProfileName</code></td>
    </tr>
    <tr>
      <td><code>seccomp.security.alpha.kubernetes.io</code><br><code>/allowedProfileNames</code></td>
      <td>
        <p><b>Baseline</b>：<code>"runtime/default,"</code> <i>（其中尾部的逗号允许取消设置）</i></p>
        <p><b>Restricted</b>：<code>"runtime/default"</code> <i>（没有尾部逗号）</i></p>
        <p><i><code>localhost/*</code> 取值对于 Baseline 和 Restricted 都是可接受的</i></p>
      </td>
    </tr>
    <tr>
      <td><code>apparmor.security.beta.kubernetes.io</code><br><code>/defaultProfileName</code></td>
    </tr>
    <tr>
      <td><code>apparmor.security.beta.kubernetes.io</code><br><code>/allowedProfileNames</code></td>
      <td>
        <p><b>Baseline</b>：<code>"runtime/default,"</code> <i>（其中尾部的逗号允许取消设置）</i></p>
        <p><b>Restricted</b>：<code>"runtime/default"</code> <i>（没有尾部逗号）</i></p>
        <p><i><code>localhost/*</code> 取值对于 Baseline 和 Restricted 都是可接受的</i></p>
      </td>
    </tr>
  </tbody>
</table>

