---
title: 周期调度任务（CronJob）
id: cronjob
date: 2018-04-12
full_link: /zh-cn/docs/concepts/workloads/controllers/cron-jobs/
short_description: >
  周期调度的任务（作业）。

aka: 
tags:
- core-object
- workload
---

管理定期运行的[任务](/zh-cn/docs/concepts/workloads/controllers/job/)。


与 **crontab** 文件中的一行命令类似，周期调度任务（CronJob）对象使用
[cron](https://zh.wikipedia.org/wiki/Cron) 格式设置排期表。
