---
title: ConfigMap
id: configmap
date: 2018-04-12
full_link: /zh-cn/docs/tasks/configure-pod-container/configure-pod-configmap/
short_description: >
  ConfigMap 是一种 API 对象，用来将非机密性的数据保存到键值对中。使用时可以用作环境变量、命令行参数或者存储卷中的配置文件。
   
aka: 
tags:
- core-object
---

 ConfigMap 是一种 API 对象，用来将非机密性的数据保存到键值对中。使用时， {{< glossary_tooltip text="Pods" term_id="pod" >}} 可以将其用作环境变量、命令行参数或者存储卷中的配置文件。


ConfigMap 将你的环境配置信息和 {{< glossary_tooltip text="容器镜像" term_id="image" >}} 解耦，便于应用配置的修改。
