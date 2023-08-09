---
api_metadata:
  apiVersion: ""
  import: "k8s.io/apimachinery/pkg/apis/meta/v1"
  kind: "LabelSelector"
content_type: "api_reference"
description: "标签选择器是对一组资源的标签查询。"
title: "LabelSelector"
weight: 2
auto_generated: true
---


`import "k8s.io/apimachinery/pkg/apis/meta/v1"`


标签选择器是对一组资源的标签查询。

`matchLabels` 和 `matchExpressions` 的结果按逻辑与的关系组合。
一个 `empty` 标签选择器匹配所有对象。一个 `null` 标签选择器不匹配任何对象。

<hr>


- **matchExpressions** ([]LabelSelectorRequirement)
  
   `matchExpressions` 是标签选择器要求的列表，这些要求的结果按逻辑与的关系来计算。
   
   <a name="LabelSelectorRequirement"></a> 
   *标签选择器要求是包含值、键和关联键和值的运算符的选择器。*
 

  - **matchExpressions.key** (string)， 必填

    *补丁策略：按照键 `key` 合并*    
    
    `key` 是选择器应用的标签键。
  
   
  - **matchExpressions.operator** (string)，必填
 
    `operator` 表示键与一组值的关系。有效的运算符包括 `In`、`NotIn`、`Exists` 和 `DoesNotExist`。
    
   
  - **matchExpressions.values** ([]string)
  
    `values` 是一个字符串值数组。如果运算符为 `In` 或 `NotIn`，则 `values` 数组必须为非空。
    
    如果运算符是 `Exists` 或 `DoesNotExist`，则 `values` 数组必须为空。
    
    该数组在策略性合并补丁（Strategic Merge Patch）期间被替换。
  
  
 - **matchLabels** (map[string]string)
  
    `matchLabels` 是 {`key`,`value`} 键值对的映射。
    
    `matchLabels` 映射中的单个 {`key`,`value`} 键值对相当于 `matchExpressions` 的一个元素，其键字段为 `key`，运算符为 `In`，`values` 数组仅包含 `value`。
    
    所表达的需求最终要按逻辑与的关系组合。
   





