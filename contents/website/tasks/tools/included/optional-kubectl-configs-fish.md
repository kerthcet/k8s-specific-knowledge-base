---
title: "fish 自动补全"
description: "启用 fish 自动补全的可选配置。"
headless: true
_build:
  list: never
  render: never
  publishResources: false
---

{{< note >}}
自动补全 Fish 需要 kubectl 1.23 或更高版本。
{{< /note >}}

kubectl 通过命令 `kubectl completion fish` 生成 Fish 自动补全脚本。
在 shell 中导入（Sourcing）该自动补全脚本，将启动 kubectl 自动补全功能。

为了在所有的 shell 会话中实现此功能，请将下面内容加入到文件 `~/.config/fish/config.fish` 中。

```shell
kubectl completion fish | source
```

重新加载 shell 后，kubectl 自动补全功能将立即生效。
