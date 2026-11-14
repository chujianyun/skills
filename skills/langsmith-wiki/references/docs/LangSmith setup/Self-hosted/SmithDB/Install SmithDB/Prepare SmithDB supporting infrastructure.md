# Prepare SmithDB supporting infrastructure

> Provide a dedicated PostgreSQL metastore, object storage, and cache storage before enabling SmithDB.

> [!NOTE]
>
> For failures such as pods stuck `Pending`, object-store access denied, or metastore connection errors, see [Troubleshoot SmithDB](Troubleshoot%20SmithDB.md#supporting-infrastructure).

SmithDB adds three infrastructure dependencies to a self-hosted LangSmith deployment: a PostgreSQL metastore, object storage, and cache storage for query, ingestion, and compaction worker.

These are integration requirements and practical recommendations, not a prescribed cloud architecture. For AWS (EKS), GCP (GKE), and Azure (AKS) setup, see [Provider setup](#provider-setup). The minimum LangSmith version depends on your cloud. See [Cloud support](../Overview/Enable%20SmithDB%20on%20self-hosted%20LangSmith.md#cloud-support).

## Requirements

Before enabling SmithDB, provide:

* A **dedicated, empty PostgreSQL database** for the SmithDB metastore. Do not use the PostgreSQL database that stores the rest of LangSmith operational data.
* A **dedicated object-storage bucket** for SmithDB durable data.
* **Cache storage** for query, ingestion, and compaction worker: network-attached disks, or local SSD for the best cache performance.
* Private network connectivity to the database and object store, plus credentials or workload identity for both.
* Network access from LangSmith to SmithDB pod IPs. If LangSmith uses an HTTP proxy or runs in a service mesh, see [Pod network access](#pod-network-access).

## PostgreSQL metastore

The metastore holds SmithDB catalog and coordination data. Create an empty database for the metastore. SmithDB initializes the schema during installation.

Use PostgreSQL 18 or later and allow database connections from the Kubernetes cluster. For database options and connectivity, see [Provider setup](#provider-setup).

### Metastore Secret

Create a Kubernetes Secret in the LangSmith release namespace containing the database host, name, username, and password. Map its keys through `smithdb.config.metastore`.

> [accordion] Metastore Secret and Helm values
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> apiVersion: v1
> kind: Secret
> metadata:
>   name: smithdb-metastore
>   namespace: NAMESPACE
> type: Opaque
> stringData:
>   smithdb_metastore_db_host: DB_HOST
>   smithdb_metastore_db_name: DB_NAME
>   smithdb_metastore_db_username: DB_USERNAME
>   smithdb_metastore_db_password: DB_PASSWORD
> ```
>
> Configure the chart to use the corresponding keys:
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   config:
>     existingSecretName: smithdb-metastore
>     metastore:
>       hostSecretKey: smithdb_metastore_db_host
>       databaseSecretKey: smithdb_metastore_db_name
>       usernameSecretKey: smithdb_metastore_db_username
>       passwordSecretKey: smithdb_metastore_db_password
>       port: "5432"
>       useSsl: true
> ```
>
> `DB_NAME` can be any name for the dedicated, empty database, such as `smithdb`. The chart does not require these exact Secret key names; the Helm values map whatever names you choose.

## Object storage

Object storage is SmithDB's durable data layer. Use a bucket reserved for SmithDB data, in the same region as the Kubernetes cluster, to minimize latency and transfer costs.

This bucket is separate from optional [LangSmith blob storage](../../Connect%20external%20services/Enable%20blob%20storage.md), which stores payloads and attachments for the broader LangSmith deployment.

Do not add bucket lifecycle rules that expire objects on their own schedule. Deleting live objects can make data unavailable.

### Use private object-storage connectivity

Use private connectivity to avoid unnecessary data-transfer and NAT gateway costs. Configure the endpoint for your cloud under [Provider setup](#provider-setup).

Configure access so SmithDB components can list the bucket and read, write, and delete objects.

### Select a ServiceAccount

SmithDB workloads share `smithdb.serviceAccount`.

* **Default**: The chart creates `<HELM_RELEASE>-smithdb`.
* **Custom**: Set `name` to create a differently named account.
* **Existing**: Set `create: false` and `name`, then configure workload identity externally.

Workload identity must target the selected namespace and name. With `create: false`, `name` is required. Otherwise pods use the `default` ServiceAccount.

### Migration source-bucket access

If your installation uses LangSmith blob storage, grant `smithdb.serviceAccount` read access to that bucket before migrating historical data.

## Cache storage

Query, ingestion, and compaction worker cache trace data on a volume mounted at `/data`. Object storage retains the durable copy; replacing a pod discards its cache.

> [!NOTE]
>
> `smithdb.cache` requires Helm chart `0.17.0` or later. The LangSmith 0.16 tabs show the equivalent configuration for earlier charts.

* **Network-attached disk**: The default on LangSmith 0.17. Kubernetes provisions a volume per pod from a StorageClass, so no dedicated node pool is needed.
* **Local SSD**: The default on LangSmith 0.16 and an explicit override on 0.17. Recommended for production, where it gives the best cache performance. Requires a node pool whose local disks back Kubernetes ephemeral storage.

Upgrading to 0.17 moves the default cache from `emptyDir` to a per-pod PersistentVolumeClaim. To stay on local SSD, add the [0.17 local SSD values](#local-ssd) to the same upgrade. If you carry custom cache volumes forward, rename them from `local-ssd-storage` to `cache`.

### Network-attached disk

The chart requests a [generic ephemeral volume](https://kubernetes.io/docs/concepts/storage/ephemeral-volumes/#generic-ephemeral-volumes) for each pod. Kubernetes creates the PersistentVolumeClaim with the pod and deletes it with the pod. Give the StorageClass `reclaimPolicy: Delete` so the backing disk goes with it.

Cluster default StorageClasses are usually too slow for the cache. Provision at least 7000 IOPS and 1000 MiB/s per volume, using the StorageClass for your provider under [Provider setup](#provider-setup).

The examples below use the `small` tier. Substitute the sizes for your tier.

> [tab] LangSmith 0.17
>
> Set `storageClassName`, or leave it empty to use the cluster default. The tier sets the volume size, CPU, and memory. The chart sets `fsGroup: 1001` and the query disk cache limit.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   resourceTier: small
>   cache:
>     storageClassName: smithdb-cache
> ```
>
> To give one component a different StorageClass or size, set its `deployment.volumes` to a generic ephemeral volume named `cache` with the class and size you want. Repeat for each component you change. Do not point `volumes` at an existing claim through `persistentVolumeClaim.claimName`; each replica needs its own volume.

> [tab] LangSmith 0.16
>
> On 0.16, replace the volume and resources on each component and set `fsGroup: 1001`. The chart derives the query disk cache limit from the `ephemeral-storage` limit, which this configuration omits, so set the limit in `extraEnv` as shown.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   query:
>     deployment:
>       extraEnv:
>         - name: SMITHDB_QUERY__VORTEX_CACHE__DISK__LIMIT
>           value: "200Gi"   # match the PVC size
>       podSecurityContext:
>         fsGroup: 1001
>       resources:
>         requests:
>           cpu: "4"
>           memory: "8Gi"
>         limits:
>           cpu: "4"
>           memory: "8Gi"
>       volumes:
>         - name: local-ssd-storage
>           ephemeral:
>             volumeClaimTemplate:
>               spec:
>                 accessModes: ["ReadWriteOnce"]
>                 storageClassName: smithdb-cache
>                 resources:
>                   requests:
>                     storage: 200Gi
>
>   ingestion:
>     deployment:
>       podSecurityContext:
>         fsGroup: 1001
>       resources:
>         requests:
>           cpu: "4"
>           memory: "8Gi"
>         limits:
>           cpu: "4"
>           memory: "8Gi"
>       volumes:
>         - name: local-ssd-storage
>           ephemeral:
>             volumeClaimTemplate:
>               spec:
>                 accessModes: ["ReadWriteOnce"]
>                 storageClassName: smithdb-cache
>                 resources:
>                   requests:
>                     storage: 100Gi
>
>   compactionWorker:
>     deployment:
>       podSecurityContext:
>         fsGroup: 1001
>       resources:
>         requests:
>           cpu: "8"
>           memory: "16Gi"
>         limits:
>           cpu: "8"
>           memory: "16Gi"
>       volumes:
>         - name: local-ssd-storage
>           ephemeral:
>             volumeClaimTemplate:
>               spec:
>                 accessModes: ["ReadWriteOnce"]
>                 storageClassName: smithdb-cache
>                 resources:
>                   requests:
>                     storage: 100Gi
> ```

No node selectors or tolerations are needed; SmithDB runs on your general node pool.

Confirm each pod has a bound claim and that `/data` uses it:

```bash
kubectl get pvc -n NAMESPACE
kubectl exec -n NAMESPACE POD_NAME -- df -h /data
```

### Local SSD

Configure the node's local SSDs to back Kubernetes ephemeral storage, with usable capacity reported as allocatable `ephemeral-storage`. SmithDB uses this storage for its `emptyDir` cache volumes.

Use scheduling controls to keep SmithDB cache workloads on SSD-backed nodes. Size nodes with headroom above pod requests, images, logs, and Kubernetes reservations.

The examples below use the `small` tier. Substitute the sizes for your tier.

> [tab] LangSmith 0.17
>
> On each disk-using component, set an `emptyDir` named `cache` and matching `ephemeral-storage` requests and limits. The chart derives the query disk cache limit from that limit.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   resourceTier: small
>   query:
>     deployment:
>       resources:
>         requests:
>           cpu: "4"
>           memory: "8Gi"
>           ephemeral-storage: "200Gi"
>         limits:
>           cpu: "4"
>           memory: "8Gi"
>           ephemeral-storage: "200Gi"
>       volumes:
>         - name: cache
>           emptyDir:
>             sizeLimit: 200Gi
>   ingestion:
>     deployment:
>       resources:
>         requests:
>           cpu: "4"
>           memory: "8Gi"
>           ephemeral-storage: "100Gi"
>         limits:
>           cpu: "4"
>           memory: "8Gi"
>           ephemeral-storage: "100Gi"
>       volumes:
>         - name: cache
>           emptyDir:
>             sizeLimit: 100Gi
>   compactionWorker:
>     deployment:
>       resources:
>         requests:
>           cpu: "8"
>           memory: "16Gi"
>           ephemeral-storage: "100Gi"
>         limits:
>           cpu: "8"
>           memory: "16Gi"
>           ephemeral-storage: "100Gi"
>       volumes:
>         - name: cache
>           emptyDir:
>             sizeLimit: 100Gi
> ```

> [tab] LangSmith 0.16
>
> On 0.16 the tier already sets `ephemeral-storage` requests and limits and an `emptyDir` named `local-ssd-storage`, so selecting a tier is enough.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   resourceTier: small
> ```

#### Schedule SmithDB workloads

Place query, ingestion, compaction worker, and migration on the local SSD pool. Place compaction and cluster manager on the general compute pool. Node-pool labels and taints must match the Helm selectors and tolerations. `metastoreMigration` can run on any node and does not need a selector.

The label and taint values in these examples match the provider samples on this page. SmithDB does not require these exact values; any labels and taints that keep cache workloads on SSD-backed nodes work.

> [accordion] Helm scheduling values
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> smithdb:
>   query:
>     deployment:
>       nodeSelector:
>         smithdb-local/instance-store: "true"
>       tolerations:
>         - key: smithdb-local/instance-store
>           operator: Equal
>           value: "true"
>           effect: NoSchedule
>
>   ingestion:
>     deployment:
>       nodeSelector:
>         smithdb-local/instance-store: "true"
>       tolerations:
>         - key: smithdb-local/instance-store
>           operator: Equal
>           value: "true"
>           effect: NoSchedule
>
>   compactionWorker:
>     deployment:
>       nodeSelector:
>         smithdb-local/instance-store: "true"
>       tolerations:
>         - key: smithdb-local/instance-store
>           operator: Equal
>           value: "true"
>           effect: NoSchedule
>
>   migration:
>     job:
>       nodeSelector:
>         smithdb-local/instance-store: "true"
>       tolerations:
>         - key: smithdb-local/instance-store
>           operator: Equal
>           value: "true"
>           effect: NoSchedule
>
>   compaction:
>     deployment:
>       nodeSelector:
>         smithdb-local/compute: "true"
>       tolerations:
>         - key: smithdb-local/compute
>           operator: Equal
>           value: "true"
>           effect: NoSchedule
>
>   clusterManager:
>     deployment:
>       nodeSelector:
>         smithdb-local/compute: "true"
>       tolerations:
>         - key: smithdb-local/compute
>           operator: Equal
>           value: "true"
>           effect: NoSchedule
> ```
>
> > [!NOTE]
> >
> > On LangSmith 0.16, the migration Job's pod settings live under `smithdb.migration.deployment` rather than `smithdb.migration.job`. All other keys are the same.

> [accordion] Verify local SSD capacity
>
> Confirm the intended labels, taints, scheduler-visible capacity, pod placement, and cache filesystem:
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> kubectl get nodes --show-labels
> kubectl describe node NODE_NAME
> kubectl get node NODE_NAME \
>   -o jsonpath='{.status.allocatable.ephemeral-storage}{"\n"}'
> kubectl get pods -n NAMESPACE -o wide
> kubectl exec -n NAMESPACE POD_NAME -- df -h /data
> ```
>
> For pods stuck `Pending`, slow cache I/O, or evictions, see [Troubleshoot SmithDB](Troubleshoot%20SmithDB.md#supporting-infrastructure).

## Provider setup

> [tab] AWS
>
> A common AWS mapping is EKS, RDS for PostgreSQL, S3, IRSA, and EC2 instance store or EBS gp3 for the cache.
>
> ### Configure the metastore
>
> Use RDS for PostgreSQL or Aurora PostgreSQL that meets the [metastore requirements](#postgresql-metastore).
>
> ### Configure S3 access
>
> Add an S3 Gateway VPC endpoint to the cluster's private route tables so bucket traffic stays off the public internet.
>
> Choose IRSA or EKS Pod Identity. IRSA requires the role annotation and trust for `system:serviceaccount:<NAMESPACE>:<HELM_RELEASE>-smithdb`. Pod Identity uses an external association and no annotation.
>
> Scope the role's S3 access to listing the bucket and reading its location, plus object read, write, delete, and multipart operations. For migration source reads, also grant `s3:ListBucket` and `s3:GetObject` on the LangSmith blob-storage bucket.
>
> > [accordion] IRSA Helm values
> >
> > ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > smithdb:
> >   serviceAccount:
> >     annotations:
> >       eks.amazonaws.com/role-arn: "arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME>"
> >   config:
> >     objectStore:
> >       type: s3
> >       bucket: "<BUCKET_NAME>"
> >       s3:
> >         region: "<AWS_REGION>"
> >         accessKeyIdSecretKey: ""
> >         secretAccessKeySecretKey: ""
> > ```
>
> ### Create a cache StorageClass
>
> For the [network-attached disk](#network-attached-disk) option, create a gp3 StorageClass with provisioned IOPS and throughput. The [EBS CSI driver](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html) must be installed.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> apiVersion: storage.k8s.io/v1
> kind: StorageClass
> metadata:
>   name: smithdb-cache
> provisioner: ebs.csi.aws.com
> parameters:
>   type: gp3
>   iops: "7000"
>   throughput: "1000"
> volumeBindingMode: WaitForFirstConsumer
> reclaimPolicy: Delete
> ```
>
> ### Provision EKS nodes with Karpenter
>
> The node examples that follow apply to the [local SSD](#local-ssd) option. Karpenter is the recommended way to provision SmithDB capacity on EKS, but it is not required. Other node provisioners must produce the same labels, taints, and Kubernetes-visible ephemeral-storage capacity.
>
> Install Karpenter v1 and its CRDs by following the [Karpenter EKS guide](https://karpenter.sh/docs/getting-started/getting-started-with-karpenter/). Before applying the example below:
>
> * Replace `CLUSTER_NAME` and `KarpenterNodeRole-CLUSTER_NAME`.
>
> * Tag the selected subnets and security group with `karpenter.sh/discovery: CLUSTER_NAME`, or replace the selectors with tags or IDs used by your environment.
>
> * Confirm the node IAM role and EKS access entry are configured for Karpenter-provisioned nodes.
>
> > [!NOTE]
> >
> > Applying these manifests creates provisioning configuration. EC2 nodes launch when matching SmithDB pods require capacity.
>
> > [accordion] Karpenter EC2NodeClass and NodePool example
> >
> > ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > apiVersion: karpenter.k8s.aws/v1
> > kind: EC2NodeClass
> > metadata:
> >   name: smithdb-instance-store
> > spec:
> >   amiSelectorTerms:
> >     - alias: al2023@latest
> >   role: KarpenterNodeRole-CLUSTER_NAME
> >   subnetSelectorTerms:
> >     - tags:
> >         karpenter.sh/discovery: CLUSTER_NAME
> >   securityGroupSelectorTerms:
> >     - tags:
> >         karpenter.sh/discovery: CLUSTER_NAME
> >   associatePublicIPAddress: false
> >   instanceStorePolicy: RAID0
> >   metadataOptions:
> >     httpEndpoint: enabled
> >     httpProtocolIPv6: disabled
> >     httpPutResponseHopLimit: 1
> >     httpTokens: required
> >   blockDeviceMappings:
> >     - deviceName: /dev/xvda
> >       ebs:
> >         volumeSize: 100Gi
> >         volumeType: gp3
> >         encrypted: true
> >         deleteOnTermination: true
> > ---
> > apiVersion: karpenter.sh/v1
> > kind: NodePool
> > metadata:
> >   name: smithdb-instance-store
> > spec:
> >   template:
> >     metadata:
> >       labels:
> >         smithdb-local/instance-store: "true"
> >     spec:
> >       taints:
> >         - key: smithdb-local/instance-store
> >           value: "true"
> >           effect: NoSchedule
> >       requirements:
> >         - key: kubernetes.io/os
> >           operator: In
> >           values: ["linux"]
> >         - key: kubernetes.io/arch
> >           operator: In
> >           values: ["amd64"]
> >         - key: karpenter.sh/capacity-type
> >           operator: In
> >           values: ["on-demand"]
> >         - key: karpenter.k8s.aws/instance-local-nvme
> >           operator: Gt
> >           values: ["799"]
> >         - key: karpenter.k8s.aws/instance-size
> >           operator: In
> >           values: ["4xlarge", "8xlarge"]
> >       nodeClassRef:
> >         group: karpenter.k8s.aws
> >         kind: EC2NodeClass
> >         name: smithdb-instance-store
> >   disruption:
> >     consolidationPolicy: WhenEmpty
> >     consolidateAfter: 2m
> > ---
> > apiVersion: karpenter.k8s.aws/v1
> > kind: EC2NodeClass
> > metadata:
> >   name: smithdb-compute
> > spec:
> >   amiSelectorTerms:
> >     - alias: al2023@latest
> >   role: KarpenterNodeRole-CLUSTER_NAME
> >   subnetSelectorTerms:
> >     - tags:
> >         karpenter.sh/discovery: CLUSTER_NAME
> >   securityGroupSelectorTerms:
> >     - tags:
> >         karpenter.sh/discovery: CLUSTER_NAME
> >   associatePublicIPAddress: false
> >   metadataOptions:
> >     httpEndpoint: enabled
> >     httpProtocolIPv6: disabled
> >     httpPutResponseHopLimit: 1
> >     httpTokens: required
> >   blockDeviceMappings:
> >     - deviceName: /dev/xvda
> >       ebs:
> >         volumeSize: 100Gi
> >         volumeType: gp3
> >         encrypted: true
> >         deleteOnTermination: true
> > ---
> > apiVersion: karpenter.sh/v1
> > kind: NodePool
> > metadata:
> >   name: smithdb-compute
> > spec:
> >   template:
> >     metadata:
> >       labels:
> >         smithdb-local/compute: "true"
> >     spec:
> >       taints:
> >         - key: smithdb-local/compute
> >           value: "true"
> >           effect: NoSchedule
> >       requirements:
> >         - key: kubernetes.io/os
> >           operator: In
> >           values: ["linux"]
> >         - key: kubernetes.io/arch
> >           operator: In
> >           values: ["amd64"]
> >         - key: karpenter.sh/capacity-type
> >           operator: In
> >           values: ["on-demand"]
> >         - key: karpenter.k8s.aws/instance-generation
> >           operator: Gt
> >           values: ["2"]
> >         - key: karpenter.k8s.aws/instance-size
> >           operator: In
> >           values: ["2xlarge", "4xlarge", "8xlarge"]
> >       nodeClassRef:
> >         group: karpenter.k8s.aws
> >         kind: EC2NodeClass
> >         name: smithdb-compute
> >   disruption:
> >     consolidationPolicy: WhenEmpty
> >     consolidateAfter: 2m
> > ```
> >
> > In this example, `instanceStorePolicy: RAID0` makes local NVMe available as node ephemeral storage. The `smithdb-instance-store` NodePool requires at least 800 GiB and consolidates only when empty, avoiding unnecessary churn of nodes with warm caches.
> >
> > That 800 GiB floor suits the `medium` tier. Size the requirement against the largest per-replica ephemeral-storage request in your chosen tier, plus node headroom. See [Configure SmithDB for scale](Configure%20SmithDB%20for%20scale.md).
>
> With custom AMIs, bootstrap must format and mount instance-store devices for kubelet and container-runtime storage.
>
> ### Provision EKS managed node groups
>
> If Karpenter is unavailable, use EKS Managed Node Groups instead. These examples configure instance-store NVMe as RAID0 and apply the label and taint used by the Helm scheduling values.
>
> > [!WARNING]
> >
> > Replace the uppercase placeholders. Choose the instance type and capacity from your sizing baseline and regional availability. Match `AMI_TYPE` to the instance architecture. For example, `i8g.4xlarge` uses `AL2023_ARM_64_STANDARD`.
>
> > [accordion] AWS CLI
> >
> > AWS CLI requires an EC2 launch template for the `nodeadm` configuration.
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > USER_DATA="$(
> >   base64 <<'EOF' | tr -d '\n'
> > MIME-Version: 1.0
> > Content-Type: multipart/mixed; boundary="BOUNDARY"
> >
> > --BOUNDARY
> > Content-Type: application/node.eks.aws
> >
> > ---
> > apiVersion: node.eks.aws/v1alpha1
> > kind: NodeConfig
> > spec:
> >   instance:
> >     localStorage:
> >       strategy: RAID0
> >
> > --BOUNDARY--
> > EOF
> > )"
> >
> > LT_ID="$(aws ec2 create-launch-template \
> >   --region AWS_REGION \
> >   --launch-template-name smithdb-instance-store \
> >   --launch-template-data "{
> >     \"InstanceType\": \"INSTANCE_TYPE\",
> >     \"UserData\": \"$USER_DATA\",
> >     \"MetadataOptions\": {
> >       \"HttpEndpoint\": \"enabled\",
> >       \"HttpTokens\": \"required\",
> >       \"HttpPutResponseHopLimit\": 2
> >     }
> >   }" \
> >   --query 'LaunchTemplate.LaunchTemplateId' \
> >   --output text)"
> >
> > aws eks create-nodegroup \
> >   --region AWS_REGION \
> >   --cluster-name CLUSTER_NAME \
> >   --nodegroup-name smithdb-instance-store \
> >   --node-role NODE_ROLE_ARN \
> >   --subnets SUBNET_ID_1 SUBNET_ID_2 \
> >   --launch-template id="$LT_ID",version=1 \
> >   --ami-type AMI_TYPE \
> >   --capacity-type ON_DEMAND \
> >   --scaling-config minSize=1,maxSize=NODE_COUNT,desiredSize=NODE_COUNT \
> >   --labels smithdb-local/instance-store=true \
> >   --taints key=smithdb-local/instance-store,value=true,effect=NO_SCHEDULE
> > ```
>
> > [accordion] eksctl 0.199.0+
> >
> > ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > apiVersion: eksctl.io/v1alpha5
> > kind: ClusterConfig
> >
> > metadata:
> >   name: CLUSTER_NAME
> >   region: AWS_REGION
> >
> > managedNodeGroups:
> >   - name: smithdb-instance-store
> >     amiFamily: AmazonLinux2023
> >     instanceType: INSTANCE_TYPE
> >     privateNetworking: true
> >     minSize: 1
> >     maxSize: NODE_COUNT
> >     desiredCapacity: NODE_COUNT
> >     labels:
> >       smithdb-local/instance-store: "true"
> >     taints:
> >       - key: smithdb-local/instance-store
> >         value: "true"
> >         effect: NoSchedule
> >     overrideBootstrapCommand: |
> >       apiVersion: node.eks.aws/v1alpha1
> >       kind: NodeConfig
> >       spec:
> >         instance:
> >           localStorage:
> >             strategy: RAID0
> > ```
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > eksctl create nodegroup --config-file=smithdb-nodegroup.yaml
> > ```
>
> > [accordion] Terraform
> >
> > ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > module "eks" {
> >   source = "terraform-aws-modules/eks/aws"
> >
> >   # Existing module version and cluster configuration...
> >
> >   eks_managed_node_groups = {
> >     # Existing node groups...
> >
> >     smithdb_instance_store = {
> >       ami_type       = "AMI_TYPE"
> >       instance_types = ["INSTANCE_TYPE"]
> >       min_size       = 1
> >       max_size       = NODE_COUNT
> >       desired_size   = NODE_COUNT
> >
> >       labels = {
> >         "smithdb-local/instance-store" = "true"
> >       }
> >
> >       taints = {
> >         smithdb = {
> >           key    = "smithdb-local/instance-store"
> >           value  = "true"
> >           effect = "NO_SCHEDULE"
> >         }
> >       }
> >
> >       cloudinit_pre_nodeadm = [{
> >         content_type = "application/node.eks.aws"
> >         content = <<-EOT
> >           apiVersion: node.eks.aws/v1alpha1
> >           kind: NodeConfig
> >           spec:
> >             instance:
> >               localStorage:
> >                 strategy: RAID0
> >         EOT
> >       }]
> >     }
> >   }
> > }
> > ```

> [tab] GCP
>
> A common GCP mapping is GKE Standard, AlloyDB or another compatible PostgreSQL service, Cloud Storage, Workload Identity, and Local SSD or Hyperdisk Balanced for the cache.
>
> ### Configure the metastore
>
> Use AlloyDB or Cloud SQL for PostgreSQL that meets the [metastore requirements](#postgresql-metastore).
>
> > [accordion] Connect through the AlloyDB Auth Proxy
> >
> > SmithDB can reach AlloyDB through the [AlloyDB Auth Proxy](https://docs.cloud.google.com/alloydb/docs/auth-proxy/overview) running as a sidecar in every SmithDB pod. SmithDB connects to the proxy on loopback; the proxy authenticates to Google Cloud and encrypts the upstream connection. The proxy does not create network connectivity, so GKE still needs a route to AlloyDB through private IP, Private Service Connect, or public IP.
> >
> > Grant `roles/alloydb.client` and `roles/serviceusage.serviceUsageConsumer` to the Google service account bound to the SmithDB ServiceAccount. Point the metastore Secret's host key at `127.0.0.1` and set `useSsl: false`. SmithDB cannot validate the certificate AlloyDB presents directly, and encryption begins at the proxy.
> >
> > `smithdb.commonInitContainers` applies to every SmithDB Deployment and Job. Set `restartPolicy: Always` so Kubernetes runs the proxy as a sidecar and lets migration Jobs complete.
> >
> > ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > smithdb:
> >   commonInitContainers:
> >     - name: alloydb-auth-proxy
> >       image: gcr.io/alloydb-connectors/alloydb-auth-proxy:PINNED_VERSION
> >       restartPolicy: Always
> >       args:
> >         - "--address=127.0.0.1"
> >         - "--port=5432"
> >         - "--structured-logs"
> >         - "--health-check"
> >         - "--http-address=0.0.0.0"
> >         - "--http-port=9090"
> >         - "projects/PROJECT_ID/locations/REGION/clusters/CLUSTER/instances/INSTANCE"
> >       ports:
> >         - name: proxy-health
> >           containerPort: 9090
> >       startupProbe:
> >         httpGet:
> >           path: /startup
> >           port: proxy-health
> >       readinessProbe:
> >         httpGet:
> >           path: /readiness
> >           port: proxy-health
> >       livenessProbe:
> >         httpGet:
> >           path: /liveness
> >           port: proxy-health
> >   config:
> >     metastore:
> >       useSsl: false
> > ```
> >
> > Add `--psc` for Private Service Connect, `--public-ip` for public IP, or `--auto-iam-authn` for IAM database authentication, which also needs `roles/alloydb.databaseUser` and a matching IAM database user. If a migration Job never finishes, confirm `restartPolicy: Always`. If the loopback connection fails with a TLS error, confirm `useSsl` is `false`.
>
> ### Configure Cloud Storage access
>
> Use Private Google Access with private Google APIs DNS to reach Cloud Storage.
>
> > [!NOTE]
> >
> > Use a single-region bucket to avoid data replication costs and provide predictable tail latencies.
>
> Grant a Google service account `roles/storage.objectAdmin`, or an equivalent custom role, on the SmithDB bucket, then allow `serviceAccount:<PROJECT_ID>.svc.id.goog[<NAMESPACE>/<HELM_RELEASE>-smithdb]` to impersonate it. For migration source reads, also grant `roles/storage.objectViewer` on the LangSmith blob-storage bucket.
>
> > [accordion] GKE Workload Identity Helm values
> >
> > ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > smithdb:
> >   serviceAccount:
> >     annotations:
> >       iam.gke.io/gcp-service-account: "<GSA_NAME>@<PROJECT_ID>.iam.gserviceaccount.com"
> >   config:
> >     objectStore:
> >       type: gcs
> >       bucket: "<BUCKET_NAME>"
> > ```
>
> > [accordion] GCS HMAC migration configuration
> >
> > Prefer Workload Identity for GCS blob access. If LangSmith must use GCS HMAC keys, set `smithdb.migration.job.extraEnv` (`smithdb.migration.deployment.extraEnv` on LangSmith 0.16) to force the S3-compatible source and reference the existing LangSmith secret (`blob_storage_access_key` / `blob_storage_access_key_secret`):
> >
> > ```yaml LangSmith 0.17 theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > smithdb:
> >   migration:
> >     job:
> >       extraEnv:
> >         - name: SMITHDB_MIGRATION__BLOB_STORE_DEFAULT__TYPE
> >           value: "s3"
> >         - name: SMITHDB_MIGRATION__BLOB_STORE_DEFAULT__S3__BUCKET
> >           value: "BLOB_BUCKET_NAME"
> >         - name: SMITHDB_MIGRATION__BLOB_STORE_DEFAULT__S3__ROOT_FOLDER
> >           value: "/"
> >         - name: SMITHDB_MIGRATION__BLOB_STORE_DEFAULT__S3__ENDPOINT
> >           value: "https://storage.googleapis.com"
> >         - name: SMITHDB_MIGRATION__BLOB_STORE_DEFAULT__S3__ACCESS_KEY_ID
> >           valueFrom:
> >             secretKeyRef:
> >               name: LANGSMITH_SECRETS_NAME
> >               key: blob_storage_access_key
> >         - name: SMITHDB_MIGRATION__BLOB_STORE_DEFAULT__S3__SECRET_ACCESS_KEY
> >           valueFrom:
> >             secretKeyRef:
> >               name: LANGSMITH_SECRETS_NAME
> >               key: blob_storage_access_key_secret
> > ```
> >
> > ```yaml LangSmith 0.16 theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > smithdb:
> >   migration:
> >     deployment:
> >       extraEnv:
> >         - name: SMITHDB_MIGRATION__BLOB_STORE_DEFAULT__TYPE
> >           value: "s3"
> >         - name: SMITHDB_MIGRATION__BLOB_STORE_DEFAULT__S3__BUCKET
> >           value: "BLOB_BUCKET_NAME"
> >         - name: SMITHDB_MIGRATION__BLOB_STORE_DEFAULT__S3__ROOT_FOLDER
> >           value: "/"
> >         - name: SMITHDB_MIGRATION__BLOB_STORE_DEFAULT__S3__ENDPOINT
> >           value: "https://storage.googleapis.com"
> >         - name: SMITHDB_MIGRATION__BLOB_STORE_DEFAULT__S3__ACCESS_KEY_ID
> >           valueFrom:
> >             secretKeyRef:
> >               name: LANGSMITH_SECRETS_NAME
> >               key: blob_storage_access_key
> >         - name: SMITHDB_MIGRATION__BLOB_STORE_DEFAULT__S3__SECRET_ACCESS_KEY
> >           valueFrom:
> >             secretKeyRef:
> >               name: LANGSMITH_SECRETS_NAME
> >               key: blob_storage_access_key_secret
> > ```
>
> ### Create a cache StorageClass
>
> For the [network-attached disk](#network-attached-disk) option, create a Hyperdisk Balanced StorageClass with provisioned IOPS and throughput. Hyperdisk availability depends on the node machine type; see [Hyperdisk on GKE](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/hyperdisk).
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> apiVersion: storage.k8s.io/v1
> kind: StorageClass
> metadata:
>   name: smithdb-cache
> provisioner: pd.csi.storage.gke.io
> parameters:
>   type: hyperdisk-balanced
>   provisioned-iops-on-create: "7000"
>   provisioned-throughput-on-create: "1000Mi"
> volumeBindingMode: WaitForFirstConsumer
> reclaimPolicy: Delete
> ```
>
> ### Provision GKE Local SSD nodes
>
> This applies to the [local SSD](#local-ssd) option. Use [Local SSD-backed ephemeral storage](https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/local-ssd), created with `--ephemeral-storage-local-ssd`, which backs `emptyDir`, container layers, and scheduler capacity. The raw block option, `--local-nvme-ssd-block`, does not back `emptyDir` and leaves SmithDB with no cache capacity.
>
> > [accordion] GKE Local SSD node-pool example
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > gcloud container node-pools create POOL_NAME \
> >   --cluster=CLUSTER_NAME \
> >   --machine-type=MACHINE_TYPE \
> >   --num-nodes=NODE_COUNT \
> >   --ephemeral-storage-local-ssd count=DISK_COUNT \
> >   --node-labels=smithdb-local/instance-store=true \
> >   --node-taints=smithdb-local/instance-store=true:NoSchedule
> > ```
>
> > [accordion] Terraform GKE Local SSD node-pool example
> >
> > > [!WARNING]
> > >
> > > This example only configures Local SSD and workload scheduling. Configure node IAM, networking, security settings, and scaling separately. Values are illustrative.
> >
> > ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > resource "google_container_node_pool" "smithdb_local_ssd" {
> >   name       = "POOL_NAME"
> >   cluster    = google_container_cluster.primary.id
> >   node_count = NODE_COUNT
> >
> >   node_config {
> >     machine_type = "MACHINE_TYPE"
> >
> >     ephemeral_storage_local_ssd_config {
> >       local_ssd_count = DISK_COUNT
> >     }
> >
> >     labels = {
> >       "smithdb-local/instance-store" = "true"
> >     }
> >
> >     taint {
> >       key    = "smithdb-local/instance-store"
> >       value  = "true"
> >       effect = "NO_SCHEDULE"
> >     }
> >   }
> > }
> > ```
>
> Supported disk counts and machine types vary by zone and machine generation. Verify availability in every zone used by the node pool.

> [tab] Azure
>
> A common Azure mapping is AKS, Azure Database for PostgreSQL, Azure Blob Storage, Workload Identity, and Premium SSD v2 or local NVMe through Azure Container Storage for the cache.
>
> ### Configure the metastore
>
> Use Azure Database for PostgreSQL that meets the [metastore requirements](#postgresql-metastore).
>
> ### Configure Blob Storage access
>
> Use a private endpoint for Blob Storage.
>
> `smithdb.config.objectStore.bucket` is the Blob container name. `azure.accountName` is required. Leave `accessKeySecretKey` empty when using Workload Identity.
>
> Grant the user-assigned managed identity `Storage Blob Data Contributor` on the SmithDB storage account, and `Storage Blob Data Reader` on the LangSmith blob-storage account for migration source reads. Annotate the SmithDB ServiceAccount with the identity's client ID, and add the `azure.workload.identity/use: "true"` label to every SmithDB workload.
>
> > [accordion] AKS Workload Identity Helm values
> >
> > ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > smithdb:
> >   serviceAccount:
> >     annotations:
> >       azure.workload.identity/client-id: "<CLIENT_ID>"
> >   config:
> >     objectStore:
> >       type: azure
> >       bucket: "<CONTAINER_NAME>"
> >       azure:
> >         accountName: "<STORAGE_ACCOUNT_NAME>"
> >         accessKeySecretKey: ""
> >   query:
> >     deployment:
> >       labels:
> >         azure.workload.identity/use: "true"
> >   ingestion:
> >     deployment:
> >       labels:
> >         azure.workload.identity/use: "true"
> >   compaction:
> >     deployment:
> >       labels:
> >         azure.workload.identity/use: "true"
> >   compactionWorker:
> >     deployment:
> >       labels:
> >         azure.workload.identity/use: "true"
> >   clusterManager:
> >     deployment:
> >       labels:
> >         azure.workload.identity/use: "true"
> >   metastoreMigration:
> >     job:
> >       labels:
> >         azure.workload.identity/use: "true"
> >   migration:
> >     job:
> >       labels:
> >         azure.workload.identity/use: "true"
> > ```
>
> ### Create a cache StorageClass
>
> For the [network-attached disk](#network-attached-disk) option, create a Premium SSD v2 StorageClass with provisioned IOPS and throughput. Premium SSD v2 disks are zonal and available in a subset of regions, so deploy the node pool across availability zones in a supported region. See [Premium SSD v2 on AKS](https://learn.microsoft.com/en-us/azure/aks/use-premium-v2-disks).
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> apiVersion: storage.k8s.io/v1
> kind: StorageClass
> metadata:
>   name: smithdb-cache
> provisioner: disk.csi.azure.com
> parameters:
>   skuName: PremiumV2_LRS
>   cachingMode: None
>   DiskIOPSReadWrite: "7000"
>   DiskMBpsReadWrite: "1000"
> volumeBindingMode: WaitForFirstConsumer
> reclaimPolicy: Delete
> ```
>
> ### Provision AKS nodes with local NVMe
>
> This applies to the [local SSD](#local-ssd) option. Use a node pool with local NVMe disks and expose them with [Azure Container Storage](https://learn.microsoft.com/en-us/azure/storage/container-storage/container-storage-introduction).
>
> Size the NVMe for every cache volume on the node. These examples use `Standard_L16s_v4`.
>
> > [accordion] Azure CLI node-pool example
> >
> > ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > az aks nodepool add \
> >   --resource-group RESOURCE_GROUP \
> >   --cluster-name CLUSTER_NAME \
> >   --name smithcache \
> >   --node-vm-size Standard_L16s_v4 \
> >   --labels smithdb-local/instance-store=true \
> >   --node-taints smithdb-local/instance-store=true:NoSchedule
> > ```
>
> > [accordion] Terraform AKS node-pool example
> >
> > > [!WARNING]
> > >
> > > This example only configures the cache pool. Configure node IAM, networking, security settings, and scaling separately, and confirm your VM size is available in your region.
> >
> > ```hcl theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > resource "azurerm_kubernetes_cluster_node_pool" "smithdb_cache" {
> >   name                  = "smithcache"
> >   kubernetes_cluster_id = azurerm_kubernetes_cluster.primary.id
> >   vm_size               = "Standard_L16s_v4"
> >   node_count            = NODE_COUNT
> >
> >   node_labels = {
> >     "smithdb-local/instance-store" = "true"
> >   }
> >
> >   node_taints = [
> >     "smithdb-local/instance-store=true:NoSchedule",
> >   ]
> > }
> > ```
>
> Enable Azure Container Storage on the pool. This requires the `k8s-extension` Azure CLI extension and creates the `local-csi` StorageClass.
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> az aks update \
>   --resource-group RESOURCE_GROUP \
>   --name CLUSTER_NAME \
>   --enable-azure-container-storage ephemeralDisk \
>   --container-storage-version 2 \
>   --azure-container-storage-nodepools smithcache
> ```
>
> Mount each cache as an ephemeral PVC on `local-csi` instead of an `emptyDir`. The chart sizes the query disk cache from the PVC, so skip the `ephemeral-storage` settings. Add the [scheduling controls](#schedule-smithdb-workloads) too.
>
> > [accordion] Azure Container Storage cache Helm values
> >
> > ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> > smithdb:
> >   resourceTier: small
> >   query:
> >     deployment:
> >       volumes:
> >         - name: cache
> >           ephemeral:
> >             volumeClaimTemplate:
> >               spec:
> >                 accessModes: ["ReadWriteOnce"]
> >                 storageClassName: local-csi
> >                 resources:
> >                   requests:
> >                     storage: 200Gi
> >   ingestion:
> >     deployment:
> >       volumes:
> >         - name: cache
> >           ephemeral:
> >             volumeClaimTemplate:
> >               spec:
> >                 accessModes: ["ReadWriteOnce"]
> >                 storageClassName: local-csi
> >                 resources:
> >                   requests:
> >                     storage: 100Gi
> >   compactionWorker:
> >     deployment:
> >       volumes:
> >         - name: cache
> >           ephemeral:
> >             volumeClaimTemplate:
> >               spec:
> >                 accessModes: ["ReadWriteOnce"]
> >                 storageClassName: local-csi
> >                 resources:
> >                   requests:
> >                     storage: 100Gi
> > ```

## Pod network access

The SmithDB cluster manager tells clients which ingestion or query pod holds the data they need, and clients connect to that pod by its IP. These connections bypass Kubernetes Services, so the cluster network must allow connections to SmithDB pod IPs.

The following table shows how clients reach each SmithDB component:

| SmithDB component (port) | Clients connect by | Clients |
| - | - | - |
| Ingestion (`8082`) | Pod IP | `ingest-queue`, `queue`, and SmithDB query |
| Query (`8080`) | Pod IP | `platform-backend`, `ingest-queue`, and `queue` |
| Cluster manager (`8091`) | Service name | LangSmith and SmithDB components |
| Compaction (`8071`) | Service name | SmithDB compaction worker |

The optional mutations, run rules, and stats query deployments also listen on port `8080`, and clients connect to them by pod IP. Connections by Service name need no extra configuration.

### HTTP proxy

If LangSmith uses an HTTP proxy, add the IP range assigned to SmithDB pods and the cluster's internal service domain to `NO_PROXY`.

### Service mesh

If LangSmith runs in a service mesh, the mesh must forward connections addressed to SmithDB pod IPs on ports `8082` and `8080`. A mesh drops these connections in two cases:

* The mesh only allows traffic to destinations in its service registry, and the SmithDB pods are not registered.
* The mesh routes the ports by hostname. A connection addressed to a pod IP matches no hostname. Handling the ports as TCP avoids routing by hostname.

> [accordion] Example: Register SmithDB pods with headless Services
>
> Meshes that build their service registry from Kubernetes Services register every pod IP behind a [headless Service](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services). The following manifest creates a headless Service for SmithDB ingestion and query. The names assume the Helm release is named `langsmith`.
>
> ```yaml theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> apiVersion: v1
> kind: Service
> metadata:
>   name: langsmith-smithdb-ingestion-headless
> spec:
>   clusterIP: None
>   selector:
>     app.kubernetes.io/component: langsmith-smithdb-ingestion
>   ports:
>     - name: tcp-grpc
>       port: 8082
>       targetPort: grpc
> ---
> apiVersion: v1
> kind: Service
> metadata:
>   name: langsmith-smithdb-query-headless
> spec:
>   clusterIP: None
>   selector:
>     app.kubernetes.io/component: langsmith-smithdb-query
>   ports:
>     - name: tcp-grpc
>       port: 8080
>       targetPort: grpc
> ```
>
> The `tcp-` prefix in each port name marks the port as TCP for meshes that select the protocol from the port name.
>
> If you enable the mutations, run rules, or stats query deployments, add a Service for each one on port `8080` that selects `langsmith-smithdb-mutations`, `langsmith-smithdb-run-rules`, or `langsmith-smithdb-stats-query`.
