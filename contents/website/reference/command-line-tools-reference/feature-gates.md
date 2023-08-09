---
title: 特性门控
weight: 10
content_type: concept
card:
  name: reference
  weight: 60
---


本页详述了管理员可以在不同的 Kubernetes 组件上指定的各种特性门控。

关于特性各个阶段的说明，请参见[特性阶段](#feature-stages)。


## 概述 {#overview}

特性门控是描述 Kubernetes 特性的一组键值对。你可以在 Kubernetes 的各个组件中使用
`--feature-gates` 标志来启用或禁用这些特性。

每个 Kubernetes 组件都支持启用或禁用与该组件相关的一组特性门控。
使用 `-h` 参数来查看所有组件支持的完整特性门控。
要为诸如 kubelet 之类的组件设置特性门控，请使用 `--feature-gates` 参数，
并向其传递一个特性设置键值对列表：

```shell
--feature-gates=...,GracefulNodeShutdown=true
```

下表总结了在不同的 Kubernetes 组件上可以设置的特性门控。

- 引入特性或更改其发布阶段后，"开始（Since）" 列将包含 Kubernetes 版本。
- "结束（Until）" 列（如果不为空）包含最后一个 Kubernetes 版本，你仍可以在其中使用特性门控。
- 如果某个特性处于 Alpha 或 Beta 状态，你可以在
  [Alpha 和 Beta 特性门控表](#feature-gates-for-alpha-or-beta-features)中找到该特性。
- 如果某个特性处于稳定状态，
  你可以在[已毕业和废弃特性门控表](#feature-gates-for-graduated-or-deprecated-features)中找到该特性的所有阶段。
- [已毕业和废弃特性门控表](#feature-gates-for-graduated-or-deprecated-features)还列出了废弃的和已被移除的特性。

{{< note >}}
有关已移除的原有特性门控的参考信息，
请参阅[已移除的特性门控](/zh-cn/docs/reference/command-line-tools-reference/feature-gates-removed/)。
{{< /note >}}

### Alpha 和 Beta 状态的特性门控  {#feature-gates-for-alpha-or-beta-features}

{{< table caption="处于 Alpha 或 Beta 状态的特性门控" >}}

| 特性    | 默认值  | 状态  | 开始（Since） | 结束（Until） |
|---------|---------|-------|---------------|---------------|
| `APIListChunking` | `false` | Alpha | 1.8 | 1.8 |
| `APIListChunking` | `true` | Beta | 1.9 | |
| `APIPriorityAndFairness` | `false` | Alpha | 1.18 | 1.19 |
| `APIPriorityAndFairness` | `true` | Beta | 1.20 | |
| `APIResponseCompression` | `false` | Alpha | 1.7 | 1.15 |
| `APIResponseCompression` | `true` | Beta | 1.16 | |
| `APISelfSubjectReview` | `false` | Alpha | 1.26 | 1.26 |
| `APISelfSubjectReview` | `true` | Beta | 1.27 | |
| `APIServerIdentity` | `false` | Alpha | 1.20 | 1.25 |
| `APIServerIdentity` | `true` | Beta | 1.26 | |
| `APIServerTracing` | `false` | Alpha | 1.22 | 1.26 |
| `APIServerTracing` | `true` | Beta | 1.27 | |
| `AdmissionWebhookMatchConditions` | `false` | Alpha | 1.27 | |
| `AggregatedDiscoveryEndpoint` | `false` | Alpha | 1.26 | 1.26 |
| `AggregatedDiscoveryEndpoint` | `true` | Beta | 1.27 | |
| `AnyVolumeDataSource` | `false` | Alpha | 1.18 | 1.23 |
| `AnyVolumeDataSource` | `true` | Beta | 1.24 | |
| `AppArmor` | `true` | Beta | 1.4 | |
| `CPUManagerPolicyAlphaOptions` | `false` | Alpha | 1.23 | |
| `CPUManagerPolicyBetaOptions` | `true` | Beta | 1.23 | |
| `CPUManagerPolicyOptions` | `false` | Alpha | 1.22 | 1.22 |
| `CPUManagerPolicyOptions` | `true` | Beta | 1.23 | |
| `CSIMigrationPortworx` | `false` | Alpha | 1.23 | 1.24 |
| `CSIMigrationPortworx` | `false` | Beta | 1.25 | |
| `CSIMigrationRBD` | `false` | Alpha | 1.23 | |
| `CSINodeExpandSecret` | `false` | Alpha | 1.25 | 1.26 |
| `CSINodeExpandSecret` | `true` | Beta | 1.27 | |
| `CSIVolumeHealth` | `false` | Alpha | 1.21 | |
| `CloudControllerManagerWebhook` | false | Alpha | 1.27 | |
| `CloudDualStackNodeIPs` | false | Alpha | 1.27 | |
| `ClusterTrustBundle` | false | Alpha | 1.27 | |
| `ComponentSLIs` | `false` | Alpha | 1.26 | 1.26 |
| `ComponentSLIs` | `true` | Beta | 1.27 | |
| `ContainerCheckpoint` | `false` | Alpha | 1.25 | |
| `ContextualLogging` | `false` | Alpha | 1.24 | |
| `CrossNamespaceVolumeDataSource` | `false` | Alpha| 1.26 | |
| `CustomCPUCFSQuotaPeriod` | `false` | Alpha | 1.12 | |
| `CustomResourceValidationExpressions` | `false` | Alpha | 1.23 | 1.24 |
| `CustomResourceValidationExpressions` | `true` | Beta | 1.25 | |
| `DisableCloudProviders` | `false` | Alpha | 1.22 | |
| `DisableKubeletCloudCredentialProviders` | `false` | Alpha | 1.23 | |
| `DynamicResourceAllocation` | `false` | Alpha | 1.26 | |
| `ElasticIndexedJob` | `true` | Beta` | 1.27 | |
| `EventedPLEG` | `false` | Alpha | 1.26 | 1.26 |
| `EventedPLEG` | `false` | Beta | 1.27 | - |
| `ExpandedDNSConfig` | `false` | Alpha | 1.22 | 1.25 |
| `ExpandedDNSConfig` | `true` | Beta | 1.26 | |
| `ExperimentalHostUserNamespaceDefaulting` | `false` | Beta | 1.5 | |
| `GracefulNodeShutdown` | `false` | Alpha | 1.20 | 1.20 |
| `GracefulNodeShutdown` | `true` | Beta | 1.21 | |
| `GracefulNodeShutdownBasedOnPodPriority` | `false` | Alpha | 1.23 | 1.23 |
| `GracefulNodeShutdownBasedOnPodPriority` | `true` | Beta | 1.24 | |
| `HPAContainerMetrics` | `false` | Alpha | 1.20 | 1.26 |
| `HPAContainerMetrics` | `true` | Beta | 1.27 | |
| `HPAScaleToZero` | `false` | Alpha | 1.16 | |
| `HonorPVReclaimPolicy` | `false` | Alpha | 1.23 |  |
| `IPTablesOwnershipCleanup` | `false` | Alpha | 1.25 | 1.26 |
| `IPTablesOwnershipCleanup` | `true` | Beta | 1.27 | |
| `InPlacePodVerticalScaling` | `false` | Alpha | 1.27 | |
| `InTreePluginAWSUnregister` | `false` | Alpha | 1.21 | |
| `InTreePluginAzureDiskUnregister` | `false` | Alpha | 1.21 | |
| `InTreePluginAzureFileUnregister` | `false` | Alpha | 1.21 | |
| `InTreePluginGCEUnregister` | `false` | Alpha | 1.21 | |
| `InTreePluginOpenStackUnregister` | `false` | Alpha | 1.21 | |
| `InTreePluginPortworxUnregister` | `false` | Alpha | 1.23 | |
| `InTreePluginRBDUnregister` | `false` | Alpha | 1.23 | |
| `InTreePluginvSphereUnregister` | `false` | Alpha | 1.21 | |
| `JobPodFailurePolicy` | `false` | Alpha | 1.25 | 1.25 |
| `JobPodFailurePolicy` | `true` | Beta | 1.26 | |
| `JobReadyPods` | `false` | Alpha | 1.23 | 1.23 |
| `JobReadyPods` | `true` | Beta | 1.24 | |
| `KMSv2` | `false` | Alpha | 1.25 | 1.26 |
| `KMSv2` | `true` | Beta | 1.27 | |
| `KubeletInUserNamespace` | `false` | Alpha | 1.22 | |
| `KubeletPodResources` | `false` | Alpha | 1.13 | 1.14 |
| `KubeletPodResources` | `true` | Beta | 1.15 | |
| `KubeletPodResourcesDynamicResources` | `false` | Alpha | 1.27 | |
| `KubeletPodResourcesGet` | `false` | Alpha | 1.27 | |
| `KubeletPodResourcesGetAllocatable` | `false` | Alpha | 1.21 | 1.22 |
| `KubeletPodResourcesGetAllocatable` | `true` | Beta | 1.23 | |
| `KubeletTracing` | `false` | Alpha | 1.25 | 1.26 |
| `KubeletTracing` | `true` | Beta | 1.27 | |
| `LegacyServiceAccountTokenTracking` | `false` | Alpha | 1.26 | 1.26 |
| `LegacyServiceAccountTokenTracking` | `true` | Beta | 1.27 | |
| `LocalStorageCapacityIsolationFSQuotaMonitoring` | `false` | Alpha | 1.15 | - |
| `LogarithmicScaleDown` | `false` | Alpha | 1.21 | 1.21 |
| `LogarithmicScaleDown` | `true` | Beta | 1.22 | |
| `LoggingAlphaOptions` | `false` | Alpha | 1.24 | - |
| `LoggingBetaOptions` | `true` | Beta | 1.24 | - |
| `MatchLabelKeysInPodTopologySpread` | `false` | Alpha | 1.25 | 1.26 |
| `MatchLabelKeysInPodTopologySpread` | `true` | Beta | 1.27 | - |
| `MaxUnavailableStatefulSet` | `false` | Alpha | 1.24 | |
| `MemoryManager` | `false` | Alpha | 1.21 | 1.21 |
| `MemoryManager` | `true` | Beta | 1.22 | |
| `MemoryQoS` | `false` | Alpha | 1.22 | |
| `MinDomainsInPodTopologySpread` | `false` | Alpha | 1.24 | 1.24 |
| `MinDomainsInPodTopologySpread` | `false` | Beta | 1.25 | 1.26 |
| `MinDomainsInPodTopologySpread` | `true` | Beta | 1.27 | |
| `MinimizeIPTablesRestore` | `false` | Alpha | 1.26 | 1.26 |
| `MinimizeIPTablesRestore` | `true` | Beta | 1.27 | |
| `MultiCIDRRangeAllocator` | `false` | Alpha | 1.25 | |
| `MultiCIDRServiceAllocator` | `false` | Alpha | 1.27 | |
| `NetworkPolicyStatus` | `false` | Alpha | 1.24 |  |
| `NewVolumeManagerReconstruction` | `true` | Beta | 1.27 |  |
| `NodeInclusionPolicyInPodTopologySpread` | `false` | Alpha | 1.25 | 1.25 |
| `NodeInclusionPolicyInPodTopologySpread` | `true` | Beta | 1.26 | |
| `NodeLogQuery` | `false` | Alpha | 1.27 | |
| `NodeOutOfServiceVolumeDetach` | `false` | Alpha | 1.24 | 1.25 |
| `NodeOutOfServiceVolumeDetach` | `true` | Beta | 1.26 | |
| `NodeSwap` | `false` | Alpha | 1.22 | |
| `OpenAPIEnums` | `false` | Alpha | 1.23 | 1.23 |
| `OpenAPIEnums` | `true` | Beta | 1.24 | |
| `PDBUnhealthyPodEvictionPolicy` | `false` | Alpha | 1.26 | 1.26 |
| `PDBUnhealthyPodEvictionPolicy` | `true` | Beta | 1.27 | |
| `PodAndContainerStatsFromCRI` | `false` | Alpha | 1.23 | |
| `PodDeletionCost` | `false` | Alpha | 1.21 | 1.21 |
| `PodDeletionCost` | `true` | Beta | 1.22 | |
| `PodDisruptionConditions` | `false` | Alpha | 1.25 | 1.25 |
| `PodDisruptionConditions` | `true` | Beta | 1.26 | |
| `PodHasNetworkCondition` | `false` | Alpha | 1.25 | |
| `PodSchedulingReadiness` | `false` | Alpha | 1.26 | 1.26 |
| `PodSchedulingReadiness` | `true` | Beta | 1.27 | |
| `ProbeTerminationGracePeriod` | `false` | Alpha | 1.21 | 1.21 |
| `ProbeTerminationGracePeriod` | `false` | Beta | 1.22 | 1.24 |
| `ProbeTerminationGracePeriod` | `true` | Beta | 1.25 | |
| `ProcMountType` | `false` | Alpha | 1.12 | |
| `ProxyTerminatingEndpoints` | `false` | Alpha | 1.22 | 1.25 |
| `ProxyTerminatingEndpoints` | `true` | Beta | 1.26 | |
| `QOSReserved` | `false` | Alpha | 1.11 | |
| `ReadWriteOncePod` | `false` | Alpha | 1.22 | 1.26 |
| `ReadWriteOncePod` | `true` | Beta | 1.27 | |
| `RecoverVolumeExpansionFailure` | `false` | Alpha | 1.23 | |
| `RemainingItemCount` | `false` | Alpha | 1.15 | 1.15 |
| `RemainingItemCount` | `true` | Beta | 1.16 | |
| `RetroactiveDefaultStorageClass` | `false` | Alpha | 1.25 | 1.25 |
| `RetroactiveDefaultStorageClass` | `true` | Beta | 1.26 | |
| `RotateKubeletServerCertificate` | `false` | Alpha | 1.7 | 1.11 |
| `RotateKubeletServerCertificate` | `true` | Beta | 1.12 | |
| `SELinuxMountReadWriteOncePod` | `false` | Alpha | 1.25 | 1.26 |
| `SELinuxMountReadWriteOncePod` | `true` | Beta | 1.27 | |
| `SecurityContextDeny` | `false` | Alpha | 1.27 | |
| `ServiceNodePortStaticSubrange` | `false` | Alpha | 1.27 | |
| `SizeMemoryBackedVolumes` | `false` | Alpha | 1.20 | 1.21 |
| `SizeMemoryBackedVolumes` | `true` | Beta | 1.22 | |
| `StableLoadBalancerNodeSet` | `true` | Beta | 1.27 | |
| `StatefulSetAutoDeletePVC` | `false` | Alpha | 1.23 | 1.26 |
| `StatefulSetAutoDeletePVC` | `false` | Beta | 1.27 | |
| `StatefulSetStartOrdinal` | `false` | Alpha | 1.26 | 1.26 |
| `StatefulSetStartOrdinal` | `true` | Beta | 1.27 | |
| `StorageVersionAPI` | `false` | Alpha | 1.20 | |
| `StorageVersionHash` | `false` | Alpha | 1.14 | 1.14 |
| `StorageVersionHash` | `true` | Beta | 1.15 | |
| `TopologyAwareHints` | `false` | Alpha | 1.21 | 1.22 |
| `TopologyAwareHints` | `false` | Beta | 1.23 | 1.23 |
| `TopologyAwareHints` | `true` | Beta | 1.24 | |
| `TopologyManagerPolicyAlphaOptions` | `false` | Alpha | 1.26 | |
| `TopologyManagerPolicyBetaOptions` | `false` | Beta | 1.26 | |
| `TopologyManagerPolicyOptions` | `false` | Alpha | 1.26 | |
| `UserNamespacesStatelessPodsSupport` | `false` | Alpha | 1.25 | |
| `ValidatingAdmissionPolicy` | `false` | Alpha | 1.26 | |
| `VolumeCapacityPriority` | `false` | Alpha | 1.21 | - |
| `WatchList` | false | Alpha | 1.27 | |
| `WinDSR` | `false` | Alpha | 1.14 | |
| `WinOverlay` | `false` | Alpha | 1.14 | 1.19 |
| `WinOverlay` | `true` | Beta | 1.20 | |
| `WindowsHostNetwork` | `false` | Alpha | 1.26| |
{{< /table >}}

### 已毕业和已废弃的特性门控  {#feature-gates-for-graduated-or-deprecated-features}

{{< table caption="已毕业或不推荐使用的特性门控" >}}

| 特性    | 默认值  | 状态  | 开始（Since） | 结束（Until） |
|---------|---------|-------|---------------|---------------|
| `AdvancedAuditing` | `false` | Alpha | 1.7 | 1.7 |
| `AdvancedAuditing` | `true` | Beta | 1.8 | 1.11 |
| `AdvancedAuditing` | `true` | GA | 1.12 | - |
| `CPUManager` | `false` | Alpha | 1.8 | 1.9 |
| `CPUManager` | `true` | Beta | 1.10 | 1.25 |
| `CPUManager` | `true` | GA | 1.26 | - |
| `CSIInlineVolume` | `false` | Alpha | 1.15 | 1.15 |
| `CSIInlineVolume` | `true` | Beta | 1.16 | 1.24 |
| `CSIInlineVolume` | `true` | GA | 1.25 | - |
| `CSIMigration` | `false` | Alpha | 1.14 | 1.16 |
| `CSIMigration` | `true` | Beta | 1.17 | 1.24 |
| `CSIMigration` | `true` | GA | 1.25 | - |
| `CSIMigrationAWS` | `false` | Alpha | 1.14 | 1.16 |
| `CSIMigrationAWS` | `false` | Beta | 1.17 | 1.22 |
| `CSIMigrationAWS` | `true` | Beta | 1.23 | 1.24 |
| `CSIMigrationAWS` | `true` | GA | 1.25 | - |
| `CSIMigrationAzureDisk` | `false` | Alpha | 1.15 | 1.18 |
| `CSIMigrationAzureDisk` | `false` | Beta | 1.19 | 1.22 |
| `CSIMigrationAzureDisk` | `true` | Beta | 1.23 | 1.23 |
| `CSIMigrationAzureDisk` | `true` | GA | 1.24 | |
| `CSIMigrationAzureFile` | `false` | Alpha | 1.15 | 1.20 |
| `CSIMigrationAzureFile` | `false` | Beta | 1.21 | 1.23 |
| `CSIMigrationAzureFile` | `true` | Beta | 1.24 | 1.25 |
| `CSIMigrationAzureFile` | `true` | GA | 1.26 | |
| `CSIMigrationGCE` | `false` | Alpha | 1.14 | 1.16 |
| `CSIMigrationGCE` | `false` | Beta | 1.17 | 1.22 |
| `CSIMigrationGCE` | `true` | Beta | 1.23 | 1.24 |
| `CSIMigrationGCE` | `true` | GA | 1.25 | - |
| `CSIMigrationvSphere` | `false` | Alpha | 1.18 | 1.18 |
| `CSIMigrationvSphere` | `false` | Beta | 1.19 | 1.24 |
| `CSIMigrationvSphere` | `true` | Beta | 1.25 | 1.25 |
| `CSIMigrationvSphere` | `true` | GA | 1.26 | - |
| `CSIStorageCapacity` | `false` | Alpha | 1.19 | 1.20 |
| `CSIStorageCapacity` | `true` | Beta | 1.21 | 1.23 |
| `CSIStorageCapacity` | `true` | GA | 1.24 | - |
| `ConsistentHTTPGetHandlers` | `true` | GA | 1.25 | - |
| `CronJobTimeZone` | `false` | Alpha | 1.24 | 1.24 |
| `CronJobTimeZone` | `true` | Beta | 1.25 | 1.26 |
| `CronJobTimeZone` | `true` | GA | 1.27 | - |
| `DelegateFSGroupToCSIDriver` | `false` | Alpha | 1.22 | 1.22 |
| `DelegateFSGroupToCSIDriver` | `true` | Beta | 1.23 | 1.25 |
| `DelegateFSGroupToCSIDriver` | `true` | GA | 1.26 |-|
| `DevicePlugins` | `false` | Alpha | 1.8 | 1.9 |
| `DevicePlugins` | `true` | Beta | 1.10 | 1.25 |
| `DevicePlugins` | `true` | GA | 1.26 | - |
| `DisableAcceleratorUsageMetrics` | `false` | Alpha | 1.19 | 1.19 |
| `DisableAcceleratorUsageMetrics` | `true` | Beta | 1.20 | 1.24 |
| `DisableAcceleratorUsageMetrics` | `true` | GA | 1.25 |- |
| `DownwardAPIHugePages` | `false` | Alpha | 1.20 | 1.20 |
| `DownwardAPIHugePages` | `false` | Beta | 1.21 | 1.21 |
| `DownwardAPIHugePages` | `true` | Beta | 1.22 | 1.26 |
| `DownwardAPIHugePages` | `true` | GA | 1.27 | - |
| `DryRun` | `false` | Alpha | 1.12 | 1.12 |
| `DryRun` | `true` | Beta | 1.13 | 1.18 |
| `DryRun` | `true` | GA | 1.19 | - |
| `EfficientWatchResumption` | `false` | Alpha | 1.20 | 1.20 |
| `EfficientWatchResumption` | `true` | Beta | 1.21 | 1.23 |
| `EfficientWatchResumption` | `true` | GA | 1.24 | - |
| `EndpointSliceTerminatingCondition` | `false` | Alpha | 1.20 | 1.21 |
| `EndpointSliceTerminatingCondition` | `true` | Beta | 1.22 | 1.25 |
| `EndpointSliceTerminatingCondition` | `true` | GA | 1.26 | |
| `ExecProbeTimeout` | `true` | GA | 1.20 | - |
| `GRPCContainerProbe` | `false` | Alpha | 1.23 | 1.23 |
| `GRPCContainerProbe` | `true` | Beta | 1.24 | 1.26 |
| `GRPCContainerProbe` | `true` | GA | 1.27 | |
| `JobMutableNodeSchedulingDirectives` | `true` | Beta | 1.23 | 1.26 |
| `JobMutableNodeSchedulingDirectives` | `true` | GA | 1.27 | |
| `JobTrackingWithFinalizers` | `false` | Alpha | 1.22 | 1.22 |
| `JobTrackingWithFinalizers` | `false` | Beta | 1.23 | 1.24 |
| `JobTrackingWithFinalizers` | `true` | Beta | 1.25 | 1.25 |
| `JobTrackingWithFinalizers` | `true` | GA | 1.26 | - |
| `KubeletCredentialProviders` | `false` | Alpha | 1.20 | 1.23 |
| `KubeletCredentialProviders` | `true` | Beta | 1.24 | 1.25 |
| `KubeletCredentialProviders` | `true` | GA | 1.26 | - |
| `LegacyServiceAccountTokenNoAutoGeneration` | `true` | Beta | 1.24 | 1.25 |
| `LegacyServiceAccountTokenNoAutoGeneration` | `true` | GA | 1.26 | - |
| `MixedProtocolLBService` | `false` | Alpha | 1.20 | 1.23 |
| `MixedProtocolLBService` | `true` | Beta | 1.24 | 1.25 |
| `MixedProtocolLBService` | `true` | GA | 1.26 | - |
| `OpenAPIV3` | `false` | Alpha | 1.23 | 1.23 |
| `OpenAPIV3` | `true` | Beta | 1.24 | 1.26 |
| `OpenAPIV3` | `true` | GA | 1.27 | - |
| `PodSecurity` | `false` | Alpha | 1.22 | 1.22 |
| `PodSecurity` | `true` | Beta | 1.23 | 1.24 |
| `PodSecurity` | `true` | GA | 1.25 | |
| `RemoveSelfLink` | `false` | Alpha | 1.16 | 1.19 |
| `RemoveSelfLink` | `true` | Beta | 1.20 | 1.23 |
| `RemoveSelfLink` | `true` | GA | 1.24 | - |
| `SeccompDefault` | `false` | Alpha | 1.22 | 1.24 |
| `SeccompDefault` | `true` | Beta | 1.25 | 1.26 |
| `SeccompDefault` | `true` | GA | 1.27 | - |
| `ServerSideApply` | `false` | Alpha | 1.14 | 1.15 |
| `ServerSideApply` | `true` | Beta | 1.16 | 1.21 |
| `ServerSideApply` | `true` | GA | 1.22 | - |
| `ServerSideFieldValidation` | `false` | Alpha | 1.23 | 1.24 |
| `ServerSideFieldValidation` | `true` | Beta | 1.25 | 1.26 |
| `ServerSideFieldValidation` | `true` | GA | 1.27 | - |
| `ServiceIPStaticSubrange` | `false` | Alpha | 1.24 | 1.24 |
| `ServiceIPStaticSubrange` | `true` | Beta | 1.25 | 1.25 |
| `ServiceIPStaticSubrange` | `true` | GA | 1.26 | - |
| `ServiceInternalTrafficPolicy` | `false` | Alpha | 1.21 | 1.21 |
| `ServiceInternalTrafficPolicy` | `true` | Beta | 1.22 | 1.25 |
| `ServiceInternalTrafficPolicy` | `true` | GA | 1.26 | - |
| `TopologyManager` | `false` | Alpha | 1.16 | 1.17 |
| `TopologyManager` | `true` | Beta | 1.18 | 1.26 |
| `TopologyManager` | `true` | GA | 1.27 | - |
| `WatchBookmark` | `false` | Alpha | 1.15 | 1.15 |
| `WatchBookmark` | `true` | Beta | 1.16 | 1.16 |
| `WatchBookmark` | `true` | GA | 1.17 | - |
| `WindowsHostProcessContainers` | `false` | Alpha | 1.22 | 1.22 |
| `WindowsHostProcessContainers` | `true` | Beta | 1.23 | 1.25 |
| `WindowsHostProcessContainers` | `true` | GA | 1.26 | - |
{{< /table >}}

## 使用特性   {#using-a-feature}

### 特性阶段    {#feature-stages}

处于 **Alpha** 、**Beta** 、 **GA** 阶段的特性。

**Alpha** 特性代表：

* 默认禁用。
* 可能有错误，启用此特性可能会导致错误。
* 随时可能删除对此特性的支持，恕不另行通知。
* 在以后的软件版本中，API 可能会以不兼容的方式更改，恕不另行通知。
* 建议将其仅用于短期测试中，因为开启特性会增加错误的风险，并且缺乏长期支持。

**Beta** 特性代表：

* 默认启用。
* 该特性已经经过良好测试。启用该特性是安全的。
* 尽管详细信息可能会更改，但不会放弃对整体特性的支持。
* 对象的架构或语义可能会在随后的 Beta 或稳定版本中以不兼容的方式更改。
  当发生这种情况时，我们将提供迁移到下一版本的说明。此特性可能需要删除、编辑和重新创建 API 对象。
  编辑过程可能需要慎重操作，因为这可能会导致依赖该特性的应用程序停机。
* 推荐仅用于非关键业务用途，因为在后续版本中可能会发生不兼容的更改。如果你具有多个可以独立升级的，则可以放宽此限制。

{{< note >}}
请试用 **Beta** 特性并提供相关反馈！
一旦特性结束 Beta 状态，我们就不太可能再对特性进行大幅修改。
{{< /note >}}

**General Availability** (GA) 特性也称为 **稳定** 特性，**GA** 特性代表着：

* 此特性会一直启用；你不能禁用它。
* 不再需要相应的特性门控。
* 对于许多后续版本，特性的稳定版本将出现在发行的软件中。


### 特性门控列表 {#feature-gates}

每个特性门控均用于启用或禁用某个特定的特性：

- `AdmissionWebhookMatchConditions`: 在转换和验证准入 Webhook
  上启用[匹配条件](/zh-cn/docs/reference/access-authn-authz/extensible-admission-controllers/#matching-requests-matchconditions)
- `APIListChunking`：启用 API 客户端以块的形式从 API 服务器检索（`LIST` 或 `GET`）资源。
- `APIPriorityAndFairness`：在每个服务器上启用优先级和公平性来管理请求并发（由 `RequestManagement` 重命名而来）。
- `APIResponseCompression`：压缩 `LIST` 或 `GET` 请求的 API 响应。
- `APISelfSubjectReview`：激活 `SelfSubjectReview` API，允许用户查看请求主体的身份验证信息。
  更多细节请参阅 [API 访问客户端的身份验证信息](/zh-cn/docs/reference/access-authn-authz/authentication/#self-subject-review)。
- `APIServerIdentity`：使用[租约](/zh-cn/docs/concepts/architecture/leases)为集群中的每个
  API 服务器赋予一个 ID。
- `APIServerTracing`：为集群中的每个 API 服务器添加对分布式跟踪的支持。
  参阅[针对 Kubernetes 系统组件的追踪](/zh-cn/docs/concepts/cluster-administration/system-traces/)
  获取更多详细信息。
- `AdvancedAuditing`：启用[高级审计功能](/zh-cn/docs/tasks/debug/debug-cluster/audit/#advanced-audit)。
- `AggregatedDiscoveryEndpoint`：启用单个 HTTP 端点 `/discovery/<version>`，
  支持用 ETag 进行原生 HTTP 缓存，包含 API 服务器已知的所有 APIResource。
- `AnyVolumeDataSource`：允许使用任何自定义的资源来做作为
  {{< glossary_tooltip text="PVC" term_id="persistent-volume-claim" >}} 中的 `DataSource`。
- `AppArmor`：在 Linux 节点上为 Pod 启用 AppArmor 机制的强制访问控制。
  请参见 [AppArmor 教程](/zh-cn/docs/tutorials/security/apparmor/)获取详细信息。
- `ContainerCheckpoint`：启用 kubelet `checkpoint` API。
  参阅 [Kubelet Checkpoint API](/zh-cn/docs/reference/node/kubelet-checkpoint-api/) 获取更多详细信息。
- `ControllerManagerLeaderMigration`：为
  [kube-controller-manager](/zh-cn/docs/tasks/administer-cluster/controller-manager-leader-migration/#initial-leader-migration-configuration) 和
  [cloud-controller-manager](/zh-cn/docs/tasks/administer-cluster/controller-manager-leader-migration/#deploy-cloud-controller-manager)
  启用 Leader 迁移，它允许集群管理者在没有停机的高可用集群环境下，实时把 kube-controller-manager
  迁移到外部的 controller-manager (例如 cloud-controller-manager) 中。
- `CPUManager`：启用容器级别的 CPU 亲和性支持，有关更多详细信息，请参见
  [CPU 管理策略](/zh-cn/docs/tasks/administer-cluster/cpu-management-policies/)。
- `CPUManagerPolicyAlphaOptions`：允许对 CPUManager 策略进行微调，针对试验性的、Alpha 质量级别的选项。
  此特性门控用来保护一组质量级别为 Alpha 的 CPUManager 选项。
  此特性门控永远不会被升级为 Beta 或者稳定版本。
- `CPUManagerPolicyBetaOptions`：允许对 CPUManager 策略进行微调，针对试验性的、Beta 质量级别的选项。
  此特性门控用来保护一组质量级别为 Beta 的 CPUManager 选项。
  此特性门控永远不会被升级为稳定版本。
- `CPUManagerPolicyOptions`：允许微调 CPU 管理策略。
- `CSIInlineVolume`：为 Pod 启用 CSI 内联卷支持。
- `CSIMigration`：确保封装和转换逻辑能够将卷操作从内嵌插件路由到相应的预安装 CSI 插件。
- `CSIMigrationAWS`：确保填充和转换逻辑能够将卷操作从 AWS-EBS 内嵌插件路由到 EBS CSI 插件。
  如果节点禁用了此特性门控或者未安装和配置 EBS CSI 插件，支持回退到内嵌 EBS 插件来执行卷挂载操作。
  不支持回退到这些插件来执行卷制备操作，因为需要安装并配置 CSI 插件。
- `CSIMigrationAzureDisk`：确保填充和转换逻辑能够将卷操作从 AzureDisk 内嵌插件路由到
  Azure 磁盘 CSI 插件。对于禁用了此特性的节点或者没有安装并配置 AzureDisk CSI
  插件的节点，支持回退到内嵌（in-tree）AzureDisk 插件来执行磁盘挂载操作。
  不支持回退到内嵌插件来执行磁盘制备操作，因为对应的 CSI 插件必须已安装且正确配置。
  此特性需要启用 CSIMigration 特性标志。
- `CSIMigrationAzureFile`：确保封装和转换逻辑能够将卷操作从 AzureFile 内嵌插件路由到
  AzureFile CSI 插件。对于禁用了此特性的节点或者没有安装并配置 AzureFile CSI
  插件的节点，支持回退到内嵌（in-tree）AzureFile 插件来执行卷挂载操作。
  不支持回退到内嵌插件来执行卷制备操作，因为对应的 CSI 插件必须已安装且正确配置。
  此特性需要启用 CSIMigration 特性标志。
- `CSIMigrationGCE`：启用填充和转换逻辑，将卷操作从 GCE-PD 内嵌插件路由到
  PD CSI 插件。对于禁用了此特性的节点或者没有安装并配置 PD CSI 插件的节点，
  支持回退到内嵌（in-tree）GCE 插件来执行挂载操作。
  不支持回退到内嵌插件来执行制备操作，因为对应的 CSI 插件必须已安装且正确配置。
  此特性需要启用 CSIMigration 特性标志。
- `CSIMigrationRBD`：启用填充和转换逻辑，将卷操作从 RBD 的内嵌插件路由到 Ceph RBD
  CSI 插件。此特性要求 CSIMigration 和 csiMigrationRBD 特性标志均被启用，
  且集群中安装并配置了 Ceph CSI 插件。此标志已被弃用，以鼓励使用
  `InTreePluginRBDUnregister` 特性标志。后者会禁止注册内嵌的 RBD 插件。
- `CSIMigrationvSphere`：允许封装和转换逻辑将卷操作从 vSphere 内嵌插件路由到
  vSphere CSI 插件。如果节点禁用了此特性门控或者未安装和配置 vSphere CSI 插件，
  则支持回退到 vSphere 内嵌插件来执行挂载操作。
  不支持回退到内嵌插件来执行制备操作，因为对应的 CSI 插件必须已安装且正确配置。
  这需要启用 CSIMigration 特性标志。
- `CSIMigrationPortworx`：启用填充和转换逻辑，将卷操作从 Portworx 内嵌插件路由到
  Portworx CSI 插件。需要在集群中安装并配置 Portworx CSI 插件.
- `CSINodeExpandSecret`：允许在 `NodeExpandVolume` CSI 操作期间将 Secret
  身份验证数据传递到 CSI 驱动以供后者使用。
- `CSIStorageCapacity`：使 CSI 驱动程序可以发布存储容量信息，并使 Kubernetes
  调度程序在调度 Pod 时使用该信息。参见[存储容量](/zh-cn/docs/concepts/storage/storage-capacity/)。
  详情请参见 [`csi` 卷类型](/zh-cn/docs/concepts/storage/volumes/#csi)。
- `CSIVolumeHealth`：启用对节点上的 CSI 卷运行状况监控的支持。
- `CloudControllerManagerWebhook`：启用在云控制器管理器中的 Webhook。
- `CloudDualStackNodeIPs`：允许在外部云驱动中通过 `kubelet --node-ip` 设置双协议栈。
   有关详细信息，请参阅[配置 IPv4/IPv6 双协议栈](/zh-cn/docs/concepts/services-networking/dual-stack/#configure-ipv4-ipv6-dual-stack)。
- `ClusterTrustBundle`：启用 ClusterTrustBundle 对象和 kubelet 集成。
- `ComponentSLIs`: 在 kubelet、kube-scheduler、kube-proxy、kube-controller-manager、cloud-controller-manager
  等 Kubernetes 组件上启用 `/metrics/slis` 端点，从而允许你抓取健康检查指标。
- `ConsistentHTTPGetHandlers`：使用探测器为生命周期处理程序规范化 HTTP get URL 和标头传递。
- `ContainerCheckpoint`： 启用 kubelet `checkpoint` API。
  详情见 [Kubelet Checkpoint API](/zh-cn/docs/reference/node/kubelet-checkpoint-api/)。
- `ContextualLogging`：当你启用这个特性门控，支持日志上下文记录的 Kubernetes
  组件会为日志输出添加额外的详细内容。
- `ControllerManagerLeaderMigration`：为 `kube-controller-manager` 和 `cloud-controller-manager`
  开启领导者迁移功能。
- `CronJobTimeZone`：允许在 [CronJobs](/zh-cn/docs/concepts/workloads/controllers/cron-jobs/)
  中使用 `timeZone` 可选字段。
- `CrossNamespaceVolumeDataSource`：启用跨名字空间卷数据源，以允许你在 PersistentVolumeClaim
  的 `dataSourceRef` 字段中指定一个源名字空间。
- `CustomCPUCFSQuotaPeriod`：使节点能够更改
  [kubelet 配置](/zh-cn/docs/tasks/administer-cluster/kubelet-config-file/)中的 `cpuCFSQuotaPeriod`。
- `CustomResourceValidationExpressions`：启用 CRD 中的表达式语言合法性检查，
  基于 `x-kubernetes-validations` 扩展中所书写的合法性检查规则来验证定制资源。
- `DaemonSetUpdateSurge`：使 DaemonSet 工作负载在每个节点的更新期间保持可用性。
  参阅[对 DaemonSet 执行滚动更新](/zh-cn/docs/tasks/manage-daemon/update-daemon-set/)。
- `DelegateFSGroupToCSIDriver`：如果 CSI 驱动程序支持，则通过 NodeStageVolume 和
  NodePublishVolume CSI 调用传递 `fsGroup`，将应用 `fsGroup` 从 Pod 的
  `securityContext` 的角色委托给驱动。
- `DevicePlugins`：在节点上启用基于[设备插件](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)的资源制备。
- `DisableAcceleratorUsageMetrics`：
  [禁用 kubelet 收集加速器指标](/zh-cn/docs/concepts/cluster-administration/system-metrics/#disable-accelerator-metrics)。
- `DisableCloudProviders`：禁用 `kube-apiserver`，`kube-controller-manager` 和
  `kubelet` 组件的 `--cloud-provider` 标志相关的所有功能。
- `DisableKubeletCloudCredentialProviders`：禁用 kubelet 中为拉取镜像内置的凭据机制，
  该凭据用于向某云提供商的容器镜像仓库执行身份认证。
- `DownwardAPIHugePages`：
  允许在[下行（Downward）API](/zh-cn/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information)
  中使用巨页信息。
- `DryRun`：启用在服务器端对请求进行[试运行（Dry Run）](/zh-cn/docs/reference/using-api/api-concepts/#dry-run)，
  以便测试验证、合并和修改，同时避免提交更改。
- `DynamicResourceAllocation`：启用对具有自定义参数和生命周期的资源的支持。
- `DynamicResourceAllocation`：启用对具有自定义参数和独立于 Pod 生命周期的资源的支持。
- `ElasticIndexedJob`：通过同时改变 `spec.completions` 和 `spec.parallelism`
  使得 `spec.completions == spec.parallelism` 来对带索引的 Job 执行扩容或缩容。
  有关详细信息，请参阅有关[弹性的带索引的 Job](/zh-cn/docs/concepts/workloads/controllers/job#elastic-indexed-jobs) 的文档。
- `EndpointSliceTerminatingCondition`：允许使用 EndpointSlice 的 `terminating` 和
  `serving` 状况字段。
- `EfficientWatchResumption`：允许将存储发起的书签（进度通知）事件传递给用户。
  这仅适用于监视操作。
- `EphemeralContainers`：启用添加
  {{< glossary_tooltip text="临时容器" term_id="ephemeral-container" >}}
  到正在运行的 Pod 的特性。
- `EventedPLEG`：启用此特性后，kubelet 能够通过 {{<glossary_tooltip term_id="cri" text="CRI">}}
  扩展从{{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}接收容器生命周期事件。
  （PLEG 是 `Pod lifecycle event generator` 的缩写，即 Pod 生命周期事件生成器）。
  要使用此特性，你还需要在集群中运行的每个容器运行时中启用对容器生命周期事件的支持。
  如果容器运行时未宣布支持容器生命周期事件，即使你已启用了此特性门控，kubelet 也会自动切换到原有的通用 PLEG 机制。
- `ExecProbeTimeout`：确保 kubelet 会遵从 exec 探针的超时值设置。
  此特性门控的主要目的是方便你处理现有的、依赖于已被修复的缺陷的工作负载；
  该缺陷导致 Kubernetes 会忽略 exec 探针的超时值设置。
  参阅[就绪态探针](/zh-cn/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes).
- `ExpandCSIVolumes`：启用扩展 CSI 卷。
- `ExpandedDNSConfig`：在 kubelet 和 kube-apiserver 上启用后，
  允许使用更多的 DNS 搜索域和搜索域列表。此功能特性需要容器运行时
  （Containerd：v1.5.6 或更高，CRI-O：v1.22 或更高）的支持。
  参阅[扩展 DNS 配置](/zh-cn/docs/concepts/services-networking/dns-pod-service/#expanded-dns-configuration).
- `ExpandInUsePersistentVolumes`：启用扩充使用中的 PVC 的尺寸。
  请查阅[调整使用中的 PersistentVolumeClaim 的大小](/zh-cn/docs/concepts/storage/persistent-volumes/#resizing-an-in-use-persistentvolumeclaim)。
- `ExpandPersistentVolumes`：允许扩充持久卷。
  请查阅[扩展持久卷申领](/zh-cn/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims)。
- `ExperimentalHostUserNamespaceDefaulting`：启用主机默认的用户名字空间。
  这适用于使用其他主机名字空间、主机安装的容器，或具有特权或使用特定的非名字空间功能
  （例如 MKNODE、SYS_MODULE 等）的容器。
  如果在 Docker 守护程序中启用了用户名字空间重新映射，则启用此选项。
- `GracefulNodeShutdown`：在 kubelet 中启用体面地关闭节点的支持。
  在系统关闭时，kubelet 会尝试监测该事件并体面地终止节点上运行的 Pod。
  参阅[体面地关闭节点](/zh-cn/docs/concepts/architecture/nodes/#graceful-node-shutdown)以了解更多细节。
- `GracefulNodeShutdownBasedOnPodPriority`：允许 kubelet 在体面终止节点时检查
  Pod 的优先级。
- `GRPCContainerProbe`：为 LivenessProbe、ReadinessProbe、StartupProbe 启用 gRPC 探针。
  参阅[配置活跃态、就绪态和启动探针](/zh-cn/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-grpc-liveness-probe)。
- `HonorPVReclaimPolicy`：无论 PV 和 PVC 的删除顺序如何，当持久卷申领的策略为 `Delete`
  时，确保这种策略得到处理。
  更多详细信息，请参阅 [PersistentVolume 删除保护 finalizer](/zh-cn/docs/concepts/storage/persistent-volumes/#persistentvolume-deletion-protection-finalizer) 文档。
- `HPAContainerMetrics`：允许 `HorizontalPodAutoscaler` 基于目标 Pods 中各容器的度量值来执行扩缩操作。
- `HPAScaleToZero`：使用自定义指标或外部指标时，可将 `HorizontalPodAutoscaler`
  资源的 `minReplicas` 设置为 0。
- `IPTablesOwnershipCleanup`：这使得 kubelet 不再创建传统的 iptables 规则。
- `InPlacePodVerticalScaling`：启用就地 Pod 垂直扩缩。
- `IdentifyPodOS`：允许设置 Pod 的 OS 字段。这一设置有助于在 API 服务器准入期间确定性地辨识
  Pod 的 OS。在 Kubernetes {{< skew currentVersion >}} 中，`pod.spec.os.name` 可选的值包括
  `windows` 和 `linux`。
- `ImmutableEphemeralVolumes`：允许将各个 Secret 和 ConfigMap 标记为不可变更的，
  以提高安全性和性能。
- `IngressClassNamespacedParams`：允许在 `IngressClass` 资源中使用名字空间范围的参数引用。
  此功能为 `IngressClass.spec.parameters` 添加了两个字段 - `scope` 和 `namespace`。
- `Initializers`：允许使用 Intializers 准入插件来异步协调对象创建操作。
- `InTreePluginAWSUnregister`：在 kubelet 和卷控制器上关闭注册 aws-ebs 内嵌插件。
- `InTreePluginAzureDiskUnregister`：在 kubelet 和卷控制器上关闭注册 azuredisk 内嵌插件。
- `InTreePluginAzureFileUnregister`：在 kubelet 和卷控制器上关闭注册 azurefile 内嵌插件。
- `InTreePluginGCEUnregister`：在 kubelet 和卷控制器上关闭注册 gce-pd 内嵌插件。
- `InTreePluginOpenStackUnregister`：在 kubelet 和卷控制器上关闭注册 OpenStack cinder 内嵌插件。
- `InTreePluginPortworxUnregister`：在 kubelet 和卷控制器上关闭注册 Portworx 内嵌插件。
- `InTreePluginRBDUnregister`：在 kubelet 和卷控制器上关闭注册 RBD 内嵌插件。
- `InTreePluginvSphereUnregister`：在 kubelet 和卷控制器上关闭注册 vSphere 内嵌插件。
- `IndexedJob`：允许 [Job](/zh-cn/docs/concepts/workloads/controllers/job/)
  控制器根据完成索引来管理 Pod 完成。
- `IngressClassNamespacedParams`：允许在 `IngressClass` 资源中引用名字空间范围的参数。
  该特性增加了两个字段 —— `scope`、`namespace` 到 `IngressClass.spec.parameters`。
- `Initializers`： 使用 Initializers 准入插件允许异步协调对象创建。
- `JobMutableNodeSchedulingDirectives`：允许在 [Job](/zh-cn/docs/concepts/workloads/controllers/job)
  的 Pod 模板中更新节点调度指令。
- `JobPodFailurePolicy`：允许用户根据容器退出码和 Pod 状况来指定 Pod 失效的处理方法。
- `JobReadyPods`：允许跟踪[状况](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#pod-conditions)为
  `Ready` 的 Pod 的个数。`Ready` 的 Pod 记录在
  [Job](/zh-cn/docs/concepts/workloads/controllers/job) 对象的
  [status](/zh-cn/docs/reference/kubernetes-api/workload-resources/job-v1/#JobStatus) 字段中。
- `JobTrackingWithFinalizers`：启用跟踪 [Job](/zh-cn/docs/concepts/workloads/controllers/job)
  完成情况，而不是永远从集群剩余 Pod 来获取信息判断完成情况。Job 控制器使用
  Pod finalizers 和 Job 状态中的一个字段来跟踪已完成的 Pod 以计算完成。
- `KMSv2`：启用 KMS v2 API 以实现静态加密。
  详情参见[使用 KMS 驱动进行数据加密](/zh-cn/docs/tasks/administer-cluster/kms-provider)。
- `KubeletCredentialProviders`：允许使用 kubelet exec 凭据提供程序来设置镜像拉取凭据。
- `KubeletInUserNamespace`：支持在{{<glossary_tooltip text="用户名字空间" term_id="userns">}}里运行 kubelet。
  请参见[使用非 Root 用户来运行 Kubernetes 节点组件](/zh-cn/docs/tasks/administer-cluster/kubelet-in-userns/)。
- `KubeletPodResources`：启用 kubelet 上 Pod 资源 GRPC 端点。更多详细信息，
  请参见[支持设备监控](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/compute-device-assignment.md)。
- `KubeletPodResourcesGet`：在 kubelet 上为 Pod 资源启用 `Get` gRPC 端点。
  此 API 增强了[资源分配报告](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources)。
- `KubeletPodResourcesGetAllocatable`：启用 kubelet 的 Pod 资源的 `GetAllocatableResources` 功能。
  该 API 增强了[资源分配报告](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources)
  包含有关可分配资源的信息，使客户端能够正确跟踪节点上的可用计算资源。
- `KubeletPodResourcesDynamiceResources`：扩展 kubelet 的 pod 资源 gRPC 端点以包括通过 `DynamicResourceAllocation` API 在 `ResourceClaims` 中分配的资源。
   有关详细信息，请参阅[资源分配报告](/zh-cn/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources)。
- `KubeletTracing`：新增在 Kubelet 中对分布式追踪的支持。
  启用时，kubelet CRI 接口和经身份验证的 http 服务器被插桩以生成 OpenTelemetry 追踪 span。
  参阅[针对 Kubernetes 系统组件的追踪](/zh-cn/docs/concepts/cluster-administration/system-traces/)
  获取更多详细信息。
- `LegacyServiceAccountTokenNoAutoGeneration`：停止基于 Secret
  自动生成[服务账号令牌](/zh-cn/docs/reference/access-authn-authz/authentication/#service-account-tokens)。
- `LegacyServiceAccountTokenTracking`：跟踪使用基于 Secret
  的[服务账号令牌](/zh-cn/docs/reference/access-authn-authz/authentication/#service-account-tokens)。
- `LocalStorageCapacityIsolation`：允许使用
  [本地临时存储](/zh-cn/docs/concepts/configuration/manage-resources-containers/)
  以及 [emptyDir 卷](/zh-cn/docs/concepts/storage/volumes/#emptydir)的 `sizeLimit` 属性。
- `LocalStorageCapacityIsolationFSQuotaMonitoring`：如果
  [本地临时存储](/zh-cn/docs/concepts/configuration/manage-resources-containers/)启用了
  `LocalStorageCapacityIsolation`，并且
  [emptyDir 卷](/zh-cn/docs/concepts/storage/volumes/#emptydir)的后备文件系统支持项目配额，
  并且启用了这些配额，将使用项目配额来监视
  [emptyDir 卷](/zh-cn/docs/concepts/storage/volumes/#emptydir)的存储消耗而不是遍历文件系统，
  以此获得更好的性能和准确性。
- `LogarithmicScaleDown`：启用 Pod 的半随机（semi-random）选择，控制器将根据 Pod
  时间戳的对数桶按比例缩小去驱逐 Pod。
- `LoggingAlphaOptions`：允许微调实验性的、Alpha 质量的日志选项。
- `LoggingBetaOptions`：允许微调实验性的、Beta 质量的日志选项。
- `MatchLabelKeysInPodTopologySpread`：为
  [Pod 拓扑分布约束](/zh-cn/docs/concepts/scheduling-eviction/topology-spread-constraints/)
  启用 `matchLabelKeys` 字段。
- `MaxUnavailableStatefulSet`：启用为 StatefulSet
  的[滚动更新策略](/zh-cn/docs/concepts/workloads/controllers/statefulset/#rolling-updates)设置
  `maxUnavailable` 字段。该字段指定更新过程中不可用 Pod 个数的上限。
- `MemoryManager`：允许基于 NUMA 拓扑为容器设置内存亲和性。
- `MemoryQoS`：使用 cgroup v2 内存控制器在 Pod / 容器上启用内存保护和使用限制。
- `MinDomainsInPodTopologySpread`：在
  [Pod 拓扑分布约束](/zh-cn/docs/concepts/scheduling-eviction/topology-spread-constraints/)中启用 `minDomains`。
- `MinimizeIPTablesRestore`：在 kube-proxy iptables 模式中启用新的性能改进逻辑。
- `MixedProtocolLBService`：允许在同一 `LoadBalancer` 类型的 Service 实例中使用不同的协议。
- `MultiCIDRRangeAllocator`：启用 MultiCIDR 网段分配机制。
- `MultiCIDRServiceAllocator`: 使用 IPAddress 对象跟踪 Service 的集群 IP 的 IP 地址分配。
- `NetworkPolicyStatus`：为 NetworkPolicy 对象启用 `status` 子资源。
- `NewVolumeManagerReconstruction`: 在 kubelet 启动期间启用改进的挂载卷的发现。
  由于这段代码已经进行了重大重构，我们允许在 kubelet 在启动时被卡住或没有从终止的 Pod 上卸载卷的情况下选择退出。
  请注意，此重构是在 Kubernetes 1.25 中的 `SELinuxMountReadWriteOncePod` alpha 特性门控背后进行的。
  在 Kubernetes v1.25 之前，kubelet 在启动期间使用不同的默认行为来发现挂载的卷。
  如果禁用此特性门控（默认启用），则选择传统的发现方式。

  在Kubernetes v1.25 和 v1.26 中，此行为切换是 `SELinuxMountReadWriteOncePod` 特性门控的一部分。
- `NodeInclusionPolicyInPodTopologySpread`：在计算 Pod 拓扑分布偏差时启用在
  [Pod 拓扑分布约束](/zh-cn/docs/concepts/scheduling-eviction/topology-spread-constraints/)中使用
  `nodeAffinityPolicy` and `nodeTaintsPolicy`。
- `NodeOutOfServiceVolumeDetach`：当使用 `node.kubernetes.io/out-of-service`
  污点将节点标记为停止服务时，节点上不能容忍这个污点的 Pod 将被强制删除，
  并且该在节点上被终止的 Pod 将立即进行卷分离操作。
- `NodeSwap`：启用 kubelet 为节点上的 Kubernetes 工作负载分配交换内存的能力。
  必须将 `KubeletConfiguration.failSwapOn` 设置为 false 的情况下才能使用。
  更多详细信息，请参见[交换内存](/zh-cn/docs/concepts/architecture/nodes/#swap-memory)。
- `OpenAPIEnums`：允许在从 API 服务器返回的 spec 中填充 OpenAPI 模式的 "enum" 字段。
- `OpenAPIV3`：允许 API 服务器发布 OpenAPI V3。
- `PDBUnhealthyPodEvictionPolicy`：启用 `PodDisruptionBudget` 的 `unhealthyPodEvictionPolicy` 字段。
  此字段指定何时应考虑驱逐不健康的 Pod。
  更多细节请参阅[不健康 Pod 驱逐策略](/zh-cn/docs/tasks/run-application/configure-pdb/#unhealthy-pod-eviction-policy)。
- `PodDeletionCost`：启用 [Pod 删除成本](/zh-cn/docs/concepts/workloads/controllers/replicaset/#pod-deletion-cost)功能。
  该功能使用户可以影响 ReplicaSet 的降序顺序。
- `PodAndContainerStatsFromCRI`：配置 kubelet 从 CRI 容器运行时中而不是从 cAdvisor 中采集容器和 Pod 统计信息。
  从 1.26 开始，这还包括从 CRI 收集指标并通过 `/metrics/cadvisor` 输出这些指标（而不是让 cAdvisor 直接输出）。
- `PodDisruptionConditions`：启用支持追加一个专用的 Pod 状况，以表示 Pod 由于某个干扰正在被删除。
- `PodHasNetworkCondition`：使得 kubelet 能够对 Pod 标记
  [PodHasNetwork](/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#pod-has-network) 状况。
- `PodSchedulingReadiness`：启用设置 `schedulingGates` 字段以控制 Pod 的[调度就绪](/zh-cn/docs/concepts/scheduling-eviction/pod-scheduling-readiness)。
- `PodSecurity`: 开启 `PodSecurity` 准入控制插件。
- `ProbeTerminationGracePeriod`：在 Pod 上启用 
  [设置探测器级别 `terminationGracePeriodSeconds`](/zh-cn/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#probe-level-terminationgraceperiodseconds)。
  有关更多信息，请参见[改进提案](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/2238-liveness-probe-grace-period)。
- `ProcMountType`：允许容器通过设置 SecurityContext 的 `procMount` 字段来控制对
  proc 文件系统的挂载方式。
- `ProxyTerminatingEndpoints`：当 `ExternalTrafficPolicy=Local` 时，
  允许 kube-proxy 来处理终止过程中的端点。
- `QOSReserved`：允许在 QoS 级别进行资源预留，以防止处于较低 QoS 级别的 Pod
  突发进入处于较高 QoS 级别的请求资源（目前仅适用于内存）。
- `ReadWriteOncePod`: 允许使用 `ReadWriteOncePod` 访问模式的 PersistentVolume。
- `RecoverVolumeExpansionFailure`：允许用户编辑其 PVC 来缩小其尺寸，
  从而从之前卷扩容发生的失败中恢复。更多细节可参见
  [从卷扩容失效中恢复](/zh-cn/docs/concepts/storage/persistent-volumes/#recovering-from-failure-when-expanding-volumes)。
- `RemainingItemCount`：允许 API 服务器在
  [分块列表请求](/zh-cn/docs/reference/using-api/api-concepts/#retrieving-large-results-sets-in-chunks)
  的响应中显示剩余条目的个数。
- `RemoveSelfLink`：将所有对象和集合的 `.metadata.selfLink` 字段设置为空（空字符串）。
  该字段自 Kubernetes v1.16 版本以来已被弃用。
  启用此功能后，`.metadata.selfLink` 字段仍然是 Kubernetes API 的一部分，但始终未设置。
- `RetroactiveDefaultStorageClass`：允许以追溯方式分配 StorageClass 给未绑定的 PVC。
- `RotateKubeletServerCertificate`：在 kubelet 上启用服务器 TLS 证书的轮换。
  更多详细信息，请参见
  [kubelet 配置](/zh-cn/docs/reference/access-authn-authz/kubelet-tls-bootstrapping/#kubelet-configuration)。
- `SELinuxMountReadWriteOncePod`：通过允许 kubelet 直接用正确的 SELinux
  标签为 Pod 挂载卷而不是以递归方式更改这些卷上的每个文件来加速容器启动。最初的实现侧重 ReadWriteOncePod 卷。
- `SeccompDefault`: 允许将所有工作负载的默认  seccomp 配置文件为 `RuntimeDefault`。
  seccomp 配置在 Pod 或者容器的 `securityContext` 字段中指定。
- `SecurityContextDeny`: 此门控表示 `SecurityContextDeny` 准入控制器已弃用。
- `ServerSideApply`：在 API 服务器上启用[服务器端应用（SSA）](/zh-cn/docs/reference/using-api/server-side-apply/)。
- `ServerSideFieldValidation`：启用服务器端字段验证。
  这意味着验证资源模式在 API 服务器端而不是客户端执行
  （例如，`kubectl create` 或 `kubectl apply` 命令行）。
- `ServiceInternalTrafficPolicy`：为服务启用 `internalTrafficPolicy` 字段。
- `ServiceIPStaticSubrange`：启用服务 ClusterIP 分配策略，从而细分 ClusterIP 范围。
  动态分配的 ClusterIP 地址将优先从较高范围分配，以低冲突风险允许用户从较低范围分配静态 ClusterIP。
  更多详细信息请参阅[避免冲突](/zh-cn/docs/reference/networking/virtual-ips/#avoiding-collisions)
- `SizeMemoryBackedVolumes`：允许 kubelet 检查基于内存制备的卷的尺寸约束（目前主要针对 `emptyDir` 卷）。
- `StableLoadBalancerNodeSet`: 允许服务控制器（KCCM）根据节点状态变化来减少负载均衡器的重新配置。
- `StatefulSetMinReadySeconds`: 允许 StatefulSet 控制器采纳 `minReadySeconds` 设置。
- `StatefulSetStartOrdinal`：允许在 StatefulSet 中配置起始序号。
  更多细节请参阅[起始序号](/zh-cn/docs/concepts/workloads/controllers/statefulset/#start-ordinal)。
- `StorageVersionAPI`：
  启用[存储版本 API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#storageversion-v1alpha1-internal-apiserver-k8s-io)。
- `StorageVersionHash`：允许 API 服务器在版本发现中公开存储版本的哈希值。
- `TopologyAwareHints`： 在 EndpointSlices 中启用基于拓扑提示的拓扑感知路由。
  更多详细信息可参见[拓扑感知提示](/zh-cn/docs/concepts/services-networking/topology-aware-hints/)。
- `TopologyManager`：启用一种机制来协调 Kubernetes 不同组件的细粒度硬件资源分配。
  详见[控制节点上的拓扑管理策略](/zh-cn/docs/tasks/administer-cluster/topology-manager/)。
- `TopologyManagerPolicyAlphaOptions`：允许微调拓扑管理器策略的实验性的、Alpha 质量的选项。
  此特性门控守护 **一组** 质量级别为 Alpha 的拓扑管理器选项。
  此特性门控绝对不会进阶至 Beta 或稳定版。
- `TopologyManagerPolicyBetaOptions`：允许微调拓扑管理器策略的实验性的、Beta 质量的选项。
  此特性门控守护 **一组** 质量级别为 Beta 的拓扑管理器选项。
  此特性门控绝对不会进阶至稳定版。
- `TopologyManagerPolicyOptions`: Allow fine-tuning of topology manager policies,
- `UserNamespacesStatelessPodsSupport`：为无状态 Pod 启用用户名字空间的支持。
- `ValidatingAdmissionPolicy`：启用准入控制中所用的对 CEL 校验的 [ValidatingAdmissionPolicy](/zh-cn/docs/reference/access-authn-authz/validating-admission-policy/) 支持。
- `VolumeCapacityPriority`: 基于可用 PV 容量的拓扑，启用对不同节点的优先级支持。
- `WatchBookmark`：启用对 watch 操作中 bookmark 事件的支持。
- `WatchList` : 启用对
  [在 watch 请求中流式传输对象的初始状态](/zh-cn/docs/reference/using-api/api-concepts/#streaming-lists)的支持。
- `WinDSR`：允许 kube-proxy 为 Windows 创建 DSR 负载均衡。
- `WinOverlay`：允许在 Windows 的覆盖网络模式下运行 kube-proxy。

- `WindowsHostNetwork`：启用对 Windows 容器接入主机网络名字空间的支持。
- `WindowsHostProcessContainers`：启用对 Windows HostProcess 容器的支持。

## {{% heading "whatsnext" %}}

* Kubernetes 的[弃用策略](/zh-cn/docs/reference/using-api/deprecation-policy/)介绍了项目针对已移除特性和组件的处理方法。
* 从 Kubernetes 1.24 开始，默认不启用新的 Beta API。
  启用 Beta 功能时，还需要启用所有关联的 API 资源。
  例如：要启用一个特定资源，如 `storage.k8s.io/v1beta1/csistoragecapacities`，
  请设置 `--runtime-config=storage.k8s.io/v1beta1/csistoragecapacities`。
  有关命令行标志的更多详细信息，请参阅 [API 版本控制](/zh-cn/docs/reference/using-api/#api-versioning)。
