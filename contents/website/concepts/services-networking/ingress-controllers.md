---
title: Ingress 控制器
description: >-
  为了让 [Ingress](/zh-cn/docs/concepts/services-networking/ingress/) 在你的集群中工作，
  必须有一个 Ingress 控制器正在运行。你需要选择至少一个 Ingress 控制器并确保其已被部署到你的集群中。
  本页列出了你可以部署的常见 Ingress 控制器。
content_type: concept
weight: 50
---



为了让 Ingress 资源工作，集群必须有一个正在运行的 Ingress 控制器。

与作为 `kube-controller-manager` 可执行文件的一部分运行的其他类型的控制器不同，
Ingress 控制器不是随集群自动启动的。
基于此页面，你可选择最适合你的集群的 ingress 控制器实现。

Kubernetes 作为一个项目，目前支持和维护
[AWS](https://github.com/kubernetes-sigs/aws-load-balancer-controller#readme)、
[GCE](https://git.k8s.io/ingress-gce/README.md#readme)
和 [Nginx](https://git.k8s.io/ingress-nginx/README.md#readme) Ingress 控制器。


## 其他控制器  {#additional-controllers}

{{% thirdparty-content %}}

* [AKS 应用程序网关 Ingress 控制器](https://docs.microsoft.com/zh-cn/azure/application-gateway/tutorial-ingress-controller-add-on-existing?toc=https%3A%2F%2Fdocs.microsoft.com%2Fen-us%2Fazure%2Faks%2Ftoc.json&bc=https%3A%2F%2Fdocs.microsoft.com%2Fen-us%2Fazure%2Fbread%2Ftoc.json)
  是一个配置 [Azure 应用程序网关](https://docs.microsoft.com/zh-cn/azure/application-gateway/overview)
  的 Ingress 控制器。
* [Ambassador](https://www.getambassador.io/) API 网关是一个基于
  [Envoy](https://www.envoyproxy.io) 的 Ingress 控制器。
* [Apache APISIX Ingress 控制器](https://github.com/apache/apisix-ingress-controller)
  是一个基于 [Apache APISIX 网关](https://github.com/apache/apisix) 的 Ingress 控制器。
* [Avi Kubernetes Operator](https://github.com/vmware/load-balancer-and-ingress-services-for-kubernetes)
  使用 [VMware NSX Advanced Load Balancer](https://avinetworks.com/)
  提供第 4 到第 7 层的负载均衡。
* [BFE Ingress 控制器](https://github.com/bfenetworks/ingress-bfe)是一个基于
  [BFE](https://www.bfe-networks.net) 的 Ingress 控制器。
* [Cilium Ingress 控制器](https://docs.cilium.io/en/stable/network/servicemesh/ingress/)是一个由
  [Cilium](https://cilium.io/) 出品支持的 Ingress 控制器。
* [Citrix Ingress 控制器](https://github.com/citrix/citrix-k8s-ingress-controller#readme)
  可以用来与 Citrix Application Delivery Controller 一起使用。
* [Contour](https://projectcontour.io/) 是一个基于 [Envoy](https://www.envoyproxy.io/)
  的 Ingress 控制器。
* [EnRoute](https://getenroute.io/) 是一个基于 [Envoy](https://www.envoyproxy.io)
  的 API 网关，可以用作 Ingress 控制器。
* [Easegress IngressController](https://github.com/megaease/easegress/blob/main/doc/reference/ingresscontroller.md)
  是一个基于 [Easegress](https://megaease.com/easegress/) 的 API 网关，可以用作 Ingress 控制器。
* F5 BIG-IP 的
  [用于 Kubernetes 的容器 Ingress 服务](https://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest)
  让你能够使用 Ingress 来配置 F5 BIG-IP 虚拟服务器。
* [FortiADC Ingress 控制器](https://docs.fortinet.com/document/fortiadc/7.0.0/fortiadc-ingress-controller-1-0/742835/fortiadc-ingress-controller-overview)
  支持 Kubernetes Ingress 资源，并允许你从 Kubernetes 管理 FortiADC 对象。
* [Gloo](https://gloo.solo.io) 是一个开源的、基于 [Envoy](https://www.envoyproxy.io) 的
  Ingress 控制器，能够提供 API 网关功能。
* [HAProxy Ingress](https://haproxy-ingress.github.io/) 是一个针对
  [HAProxy](https://www.haproxy.org/#desc) 的 Ingress 控制器。
* [用于 Kubernetes 的 HAProxy Ingress 控制器](https://github.com/haproxytech/kubernetes-ingress#readme)
  也是一个针对 [HAProxy](https://www.haproxy.org/#desc) 的 Ingress 控制器。
* [Istio Ingress](https://istio.io/latest/zh/docs/tasks/traffic-management/ingress/kubernetes-ingress/)
  是一个基于 [Istio](https://istio.io/zh/) 的 Ingress 控制器。
* [用于 Kubernetes 的 Kong Ingress 控制器](https://github.com/Kong/kubernetes-ingress-controller#readme)
  是一个用来驱动 [Kong Gateway](https://konghq.com/kong/) 的 Ingress 控制器。
* [Kusk Gateway](https://kusk.kubeshop.io/) 是一个基于 [Envoy](https://www.envoyproxy.io) 的、
  OpenAPI 驱动的 Ingress 控制器。
* [用于 Kubernetes 的 NGINX Ingress 控制器](https://www.nginx.com/products/nginx-ingress-controller/)
  能够与 [NGINX](https://www.nginx.com/resources/glossary/nginx/)
  网页服务器（作为代理）一起使用。
* [ngrok Kubernetes Ingress 控制器](https://github.com/ngrok/kubernetes-ingress-controller)
  是一个开源控制器，通过使用 [ngrok 平台](https://ngrok.com)为你的 K8s 服务添加安全的公开访问权限。
* [Pomerium Ingress 控制器](https://www.pomerium.com/docs/k8s/ingress.html)
  基于 [Pomerium](https://pomerium.com/)，能提供上下文感知的准入策略。
* [Skipper](https://opensource.zalando.com/skipper/kubernetes/ingress-controller/) HTTP
  路由器和反向代理可用于服务组装，支持包括 Kubernetes Ingress
  这类使用场景，是一个用以构造你自己的定制代理的库。
* [Traefik Kubernetes Ingress 提供程序](https://doc.traefik.io/traefik/providers/kubernetes-ingress/)
  是一个用于 [Traefik](https://traefik.io/traefik/) 代理的 Ingress 控制器。
* [Tyk Operator](https://github.com/TykTechnologies/tyk-operator)
  使用自定义资源扩展 Ingress，为之带来 API 管理能力。Tyk Operator
  使用开源的 Tyk Gateway & Tyk Cloud 控制面。
* [Voyager](https://appscode.com/products/voyager) 是一个针对
  [HAProxy](https://www.haproxy.org/#desc) 的 Ingress 控制器。
* [Wallarm Ingress Controller](https://www.wallarm.com/solutions/waf-for-kubernetes) 是提供 WAAP（WAF）
  和 API 安全功能的 Ingress Controller。

## 使用多个 Ingress 控制器  {#using-multiple-ingress-controllers}

你可以使用
[Ingress 类](/zh-cn/docs/concepts/services-networking/ingress/#ingress-class)在集群中部署任意数量的
Ingress 控制器。
请注意你的 Ingress 类资源的 `.metadata.name` 字段。
当你创建 Ingress 时，你需要用此字段的值来设置 Ingress 对象的 `ingressClassName` 字段（请参考
[IngressSpec v1 reference](/zh-cn/docs/reference/kubernetes-api/service-resources/ingress-v1/#IngressSpec)）。
`ingressClassName`
是之前的[注解](/zh-cn/docs/concepts/services-networking/ingress/#deprecated-annotation)做法的替代。

如果你不为 Ingress 指定 IngressClass，并且你的集群中只有一个 IngressClass 被标记为默认，那么
Kubernetes 会将此集群的默认 IngressClass
[应用](/zh-cn/docs/concepts/services-networking/ingress/#default-ingress-class)到 Ingress 上。
IngressClass。
你可以通过将
[`ingressclass.kubernetes.io/is-default-class` 注解](/zh-cn/docs/reference/labels-annotations-taints/#ingressclass-kubernetes-io-is-default-class)
的值设置为 `"true"` 来将一个 IngressClass 标记为集群默认。

理想情况下，所有 Ingress 控制器都应满足此规范，但各种 Ingress 控制器的操作略有不同。

{{< note >}}
确保你查看了 ingress 控制器的文档，以了解选择它的注意事项。
{{< /note >}}

## {{% heading "whatsnext" %}}

* 进一步了解 [Ingress](/zh-cn/docs/concepts/services-networking/ingress/)。
* [在 Minikube 上使用 NGINX 控制器安装 Ingress](/zh-cn/docs/tasks/access-application-cluster/ingress-minikube)。

