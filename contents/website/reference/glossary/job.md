---
title: Job
id: job
date: 2018-04-12
full_link: /zh-cn/docs/concepts/workloads/controllers/job/
short_description: >
  Job 是需要运行完成的确定性的或批量的任务。

aka: 
tags:
- fundamental
- core-object
- workload
---


Job 是需要运行完成的确定性的或批量的任务。


创建一个或多个 {{< glossary_tooltip term_id="Pod" >}} 对象，并确保指定数量的 Pod 成功终止。
随着各 Pod 成功结束，Job 会跟踪记录成功完成的个数。
