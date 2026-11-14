# AWS Terraform troubleshooting

> Common issues, fixes, and diagnostic commands for LangSmith self-hosted on AWS EKS deployed with the LangChain Terraform modules.

This page documents common issues, fixes, and diagnostic commands for LangSmith deployments provisioned with the [AWS Terraform modules](https://github.com/langchain-ai/terraform/tree/main/modules/aws).

> [!TIP]
>
> Before upgrading, review the [LangSmith self-hosted changelog](../../Reference/Self-hosted%20LangSmith%20changelog.md) for breaking changes and required variable updates. Run `source infra/scripts/set-kubeconfig.sh` from `modules/aws/`, or `aws eks update-kubeconfig --region <region> --name <cluster-name>`, before running any `kubectl` commands.

For a copy-paste reference of the `kubectl`, `helm`, and `aws` calls used throughout this page, skip to [Diagnostic commands](#diagnostic-commands).

## Automated diagnostics

Before running individual commands, try the bundled scripts:

```bash
# Deployment status across all layers + next-step guidance
make status

# SSM parameter validation
./infra/scripts/manage-ssm.sh validate
```

## Known issues

### EKS node group creation fails: CREATE\_FAILED

**Symptom**

```
Error: waiting for EKS Node Group creation: unexpected state 'CREATE_FAILED'
```

**Cause:** The EKS control plane is not yet fully active when node group creation begins. Common after an interrupted apply.

**Fix**

```bash
aws eks wait cluster-active --name <cluster-name> --region <region>

aws eks describe-nodegroup \
  --cluster-name <cluster-name> \
  --nodegroup-name <nodegroup-name> \
  --region <region> \
  --query "nodegroup.health"

make apply
```

### kubectl fails: "You must be logged in to the server"

**Symptom:** All `kubectl` commands fail with `error: You must be logged in to the server (Unauthorized)`.

**Cause:** The kubeconfig is stale, the AWS credentials differ from those that created the cluster, or the token has expired.

**Fix**

```bash
aws eks update-kubeconfig --region <region> --name <cluster-name>
kubectl cluster-info

aws sts get-caller-identity
```

If the cluster was created with a different IAM principal, grant access through EKS access entries, which is how the module manages cluster access. Have the cluster creator or another cluster admin run:

```bash
aws eks create-access-entry \
  --cluster-name <cluster-name> \
  --principal-arn <iam-role-or-user-arn> \
  --region <region>

aws eks associate-access-policy \
  --cluster-name <cluster-name> \
  --principal-arn <iam-role-or-user-arn> \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy \
  --access-scope type=cluster \
  --region <region>
```

### ALB not created after Helm install

This entry applies to classic ALB Ingress mode (`enable_envoy_gateway = false` with no other gateway). In the default Envoy Gateway mode, an empty `kubectl get ingress` is expected: the Terraform-managed ALB forwards to Envoy through a `TargetGroupBinding`. Check `make status` and `kubectl get gateway,httproute -n langsmith` instead.

**Symptom:** `kubectl get ingress -n langsmith` shows no ADDRESS after several minutes.

**Cause:** AWS Load Balancer Controller is not running or lacks IRSA permissions, or `alb_scheme = "internal"` is set (internal ALBs have no public address; see [ALB has no public address](#alb-has-no-public-address-internal-scheme)).

**Fix**

```bash
kubectl get pods -n kube-system | grep aws-load-balancer
kubectl logs -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller --tail=50
kubectl get sa -n kube-system aws-load-balancer-controller -o yaml | grep eks.amazonaws.com

kubectl get ingress -n langsmith \
  -o jsonpath='{.items[0].status.loadBalancer.ingress[0].hostname}'
aws elbv2 describe-load-balancers --query "LoadBalancers[?DNSName=='<alb-dns-name>'].State"
```

### RDS connection refused from EKS pods

**Symptom:** Backend logs show `connection refused` or `timeout` for the RDS endpoint.

**Cause:** The RDS security group does not allow inbound TCP 5432 from the VPC CIDR. The module's security group allows the VPC CIDR. With `postgres_existing_security_group_id` set, Terraform does not manage the rules, so your security group must allow it.

**Fix**

```bash
aws eks describe-cluster --name <cluster-name> \
  --query "cluster.resourcesVpcConfig.clusterSecurityGroupId"

aws rds describe-db-instances \
  --db-instance-identifier <db-id> \
  --query "DBInstances[0].VpcSecurityGroups"

aws ec2 describe-security-group-rules \
  --filter "Name=group-id,Values=<rds-sg-id>"
```

The `postgres` module sets up the security group automatically. If the rule is missing, re-apply:

```bash
make apply ARGS="-target=module.postgres"
```

### S3 access denied from pods (IRSA not configured)

**Symptom:** Backend logs show `AccessDenied` when reading or writing S3.

**Cause:** IRSA annotation missing from the component service accounts, or the S3 VPC Gateway Endpoint is not routing correctly.

**Fix**

```bash
kubectl get sa -n langsmith -o yaml | grep eks.amazonaws.com

aws ec2 describe-vpc-endpoints \
  --filters "Name=service-name,Values=com.amazonaws.<region>.s3" \
  --query "VpcEndpoints[].State"

# Run the test pod as an annotated service account; other service accounts have no AWS credentials
kubectl run s3-test --rm -it --image=amazon/aws-cli -n langsmith \
  --overrides='{"spec":{"serviceAccountName":"<annotated-service-account>"}}' -- \
  s3 ls s3://<bucket-name>
```

`make init-values` annotates each component's service account (backend, platform-backend, queue, ingest-queue, playground, and the Agent Server hosting services). If the annotations are missing, verify `create_langsmith_irsa_role = true` in `terraform.tfvars`, then run `make init-values && make deploy`.

### ElastiCache Redis connection timeout

**Symptom:** Pods cannot connect to Redis. Logs show `dial tcp: i/o timeout`.

**Cause:** The ElastiCache security group does not allow inbound TCP 6379 from the VPC CIDR. The module's security group allows the VPC CIDR; with `redis_existing_security_group_id` set, your security group must allow it.

**Fix**

```bash
aws elasticache describe-cache-clusters \
  --cache-cluster-id <cluster-id> \
  --query "CacheClusters[0].SecurityGroups"

kubectl run redis-test --rm -it --image=redis:7 -n langsmith -- \
  redis-cli --tls -h <elasticache-endpoint> -a <auth-token> ping
```

ElastiCache has transit encryption enabled, so `redis-cli` needs `--tls`.

### Image pulls time out in a VPC without internet egress

**Symptom:** Pods stay in `ImagePullBackOff` or `ErrImagePull`. `kubectl describe pod` shows `dial tcp <ip>:443: i/o timeout` while pulling from `<account-id>.dkr.ecr.<region>.amazonaws.com`.

**Cause:** The module creates only an S3 Gateway endpoint in the VPC, with no ECR interface endpoints. A VPC created by the module sends egress through a NAT gateway. A bring-your-own VPC (`create_vpc = false`) with no NAT gateway gives nodes no route to the ECR API and registry.

**Fix:** Create `ecr.api` and `ecr.dkr` interface endpoints in the private subnets with private DNS enabled, behind a security group that allows TCP 443 from the VPC CIDR. Image layers download from S3 through the existing Gateway endpoint.

```bash
aws ec2 create-security-group --group-name <name>-ecr-endpoints \
  --description "ECR interface endpoints" --vpc-id <vpc-id> --region <region>
aws ec2 authorize-security-group-ingress --group-id <endpoint-sg-id> \
  --protocol tcp --port 443 --cidr <vpc-cidr> --region <region>
aws ec2 create-vpc-endpoint --vpc-id <vpc-id> --vpc-endpoint-type Interface \
  --service-name com.amazonaws.<region>.ecr.api --subnet-ids <private-subnet-ids> \
  --security-group-ids <endpoint-sg-id> --private-dns-enabled --region <region>
aws ec2 create-vpc-endpoint --vpc-id <vpc-id> --vpc-endpoint-type Interface \
  --service-name com.amazonaws.<region>.ecr.dkr --subnet-ids <private-subnet-ids> \
  --security-group-ids <endpoint-sg-id> --private-dns-enabled --region <region>
```

Images hosted outside ECR still need egress or a copy in a private ECR repository.

### EKS nodes not autoscaling

**Symptom:** Pods remain `Pending`. Node count does not increase.

**Cause:** Cluster Autoscaler lacks IAM permissions, targets the wrong ASG, or `min_size = max_size` on the node group.

**Fix**

```bash
kubectl logs -n kube-system -l app=cluster-autoscaler --tail=50

aws autoscaling describe-auto-scaling-groups \
  --query "AutoScalingGroups[?contains(Tags[].Key, 'k8s.io/cluster-autoscaler/<cluster-name>')].[AutoScalingGroupName]" \
  --output table
```

### cert-manager fails to issue Let's Encrypt certificate

**Symptom:** `kubectl get certificate -n langsmith` shows `READY=False`. HTTP01 challenge is failing.

**Cause:** The ALB is not forwarding port 80 to the cert-manager solver pod, or the DNS record for the domain does not point to the ALB.

**Fix**

```bash
kubectl describe certificate <cert-name> -n langsmith
kubectl get challenges -n langsmith

aws elbv2 describe-listeners --load-balancer-arn <alb-arn>

dig +short <your-langsmith-domain>
# Expected: CNAME to the ALB DNS name
```

### postgres\_deletion\_protection blocks terraform destroy

**Symptom**

```
Error: deleting RDS DB Instance: InvalidParameterCombination:
Cannot delete, DeletionProtection is enabled.
```

**Fix:** Disable deletion protection in `terraform.tfvars`, apply, then destroy:

```hcl
postgres_deletion_protection          = false
smithdb_metastore_deletion_protection = false   # only if SmithDB is enabled
```

```bash
source infra/scripts/setup-env.sh
make apply
make destroy
make purge-secrets
make clean
```

If you have not uninstalled LangSmith yet, run `make uninstall` before `make destroy`. For the full sequence, see [Teardown](AWS%20Terraform%20quick%20reference.md#teardown).

RDS takes a final snapshot named `<identifier>-final` unless `postgres_skip_final_snapshot = true`. With SmithDB enabled, the metastore RDS also takes a `-final` snapshot unless `smithdb_metastore_skip_final_snapshot = true`. A repeat destroy fails with `DBSnapshotAlreadyExists` while that snapshot exists; delete the old snapshot or set `postgres_skip_final_snapshot = true`.

### ESO fails to sync: langsmith-config secret missing

**Symptom:** Pods stuck in `CreateContainerConfigError`. `kubectl get secret langsmith-config -n langsmith` returns `NotFound`.

**Cause:** ESO sync is all-or-nothing. If any single SSM parameter referenced by the `ExternalSecret` is missing, ESO refuses to create the Kubernetes Secret. All pods fail, including those unrelated to the missing parameter.

**Fix**

```bash
kubectl get externalsecret langsmith-config -n langsmith
kubectl describe externalsecret langsmith-config -n langsmith

./infra/scripts/manage-ssm.sh validate
./infra/scripts/manage-ssm.sh list

source ./infra/scripts/setup-env.sh
make apply-eso
```

`validate` does not check `langsmith-admin-email`, which the `ExternalSecret` always requires, and treats `sandbox-callback-signing-jwk` as optional, though it is required when `enable_sandboxes = true`. Confirm both keys in the `list` output.

The `describe` output shows which `remoteRef.key` failed. Match it against the SSM prefix `/langsmith/{name_prefix}-{environment}/`.

### SSM parameter prefix mismatch

**Symptom:** `manage-ssm.sh validate` passes but ESO still cannot sync. Or `setup-env.sh` wrote parameters under a different prefix than ESO expects.

**Cause:** The SSM prefix is derived from `name_prefix` and `environment` in `terraform.tfvars`. If these changed after initial setup, the old parameters live under the old prefix and ESO looks under the new one.

**Fix**

```bash
kubectl get externalsecret langsmith-config -n langsmith -o yaml | grep 'key:'

./infra/scripts/manage-ssm.sh list

# Preview the copy, then re-run without --dry-run (add --delete-old to remove the old parameters)
./infra/scripts/migrate-ssm.sh --old-prefix /langsmith/<old-name-prefix>-<old-environment> --dry-run
```

In the `v0.17.0` and `v0.16.*` module releases, the live copy in `migrate-ssm.sh` fails: its `put-parameter` call passes `--output none`, which the AWS CLI rejects, so every parameter reports `FAILED`. On bash 4.1 or later, the script can also exit after the first parameter. Use `--dry-run` to list the keys, then copy each one with the AWS CLI:

```bash
OLD=/langsmith/<old-name-prefix>-<old-environment>
NEW=/langsmith/<name_prefix>-<environment>
for key in <key-1> <key-2>; do
  aws ssm put-parameter --region <region> --type SecureString --overwrite \
    --name "$NEW/$key" \
    --value "$(aws ssm get-parameter --region <region> --name "$OLD/$key" \
      --with-decryption --query Parameter.Value --output text)" >/dev/null
done
```

> [!WARNING]
>
> Never change `name_prefix` or `environment` on an existing deployment.

### Postgres password rejected by Terraform validation

**Symptom**

```
Error: Invalid value for variable "postgres_password"
RDS master password must be 8-128 characters and must not contain '/', '@', '"', single quotes, or spaces.
```

**Cause:** The password is shorter than 8 or longer than 128 characters, or contains characters RDS does not allow in the master password.

**Fix:** Generate a password without restricted characters. `setup-env.sh` produces a compliant password automatically. To replace an invalid value, unset the exported variable first, because `setup-env.sh` keeps a `TF_VAR_postgres_password` that is already set:

```bash
./infra/scripts/manage-ssm.sh set postgres-password "$(openssl rand -hex 32)"
unset TF_VAR_postgres_password
source ./infra/scripts/setup-env.sh
make apply
kubectl rollout restart deployment -n langsmith
```

Run a full `make apply`, not `-target=module.postgres`: the target skips the `langsmith-postgres` Secret, so RDS and LangSmith would hold different passwords. Skip the restart on a new deployment that has no running pods.

### Private EKS cluster unreachable (bastion required)

**Symptom:** `kubectl` and `terraform apply` time out when `enable_public_eks_cluster = false`.

**Cause:** The EKS API endpoint is private. Commands must run from within the VPC, either via the bastion host or a VPN connection.

**Fix**

```bash
# If the bastion was provisioned (create_bastion = true)
aws ssm start-session --target <bastion-instance-id>

# From the bastion
aws eks update-kubeconfig --region <region> --name <cluster-name>
kubectl get nodes
```

If no bastion was provisioned, set `create_bastion = true` and re-apply, or temporarily set `enable_public_eks_cluster = true`.

### ALB has no public address (internal scheme)

**Symptom:** The ALB hostname from `make status` or `make tf ARGS="output alb_dns_name"` starts with `internal-` and resolves only within the VPC.

**Cause:** `alb_scheme = "internal"` was set in `terraform.tfvars`. Internal ALBs are only reachable from within the VPC (VPN, peering, or PrivateLink).

**Fix:** Intentional for private deployments. To make the ALB publicly reachable:

```hcl
alb_scheme = "internet-facing"
```

```bash
make apply
make init-values
make deploy
```

With `create_vpc = false`, an internet-facing ALB also needs `public_subnets`.

### ALB hostname changed after ingress recreation

This entry applies to classic ALB Ingress mode, where the ALB controller owns the ALB. In that mode `alb_dns_name` refers to the unused Terraform-managed ALB.

**Symptom:** The LangSmith URL stops working. Agent deployments stuck in `DEPLOYING`. DNS records or bookmarks point to an old ALB hostname that no longer resolves.

**Cause:** Deleting the Kubernetes ingress (via `helm uninstall`, `kubectl delete ingress`, or namespace deletion) deprovisions the ALB. When the ingress is recreated, a new ALB with a different hostname is issued. The `config.deployment.url` in Helm values still points to the old hostname, so the operator's health checks fail and deployments stay stuck.

**Prevention**

* Keep the `group.name` annotation that `init-values.sh` sets on the ingress.
* Do not delete the ingress unless you plan to update all hostname-dependent config.
* On Helm 4, avoid `helm rollback` without `--server-side=false`. The ingress SSA conflict can trigger a delete/recreate cycle.

**Fix**

```bash
# 1. Check what hostname the ingress currently has
kubectl get ingress langsmith-ingress -n langsmith \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

# 2. Redeploy: deploy detects the live hostname, updates the values file, and re-upgrades
make deploy
```

When `langsmith_domain` is set, `make deploy` does not rewrite the hostname; update the DNS record to the new ALB instead.

### Chart v16 sandbox values rejected

**Symptom:** `make deploy` exits with `ERROR: langsmith-values-overrides.yaml carries sandboxes.juicefs.csi, the chart 0.16 sandbox schema.`

**Cause:** The values file was generated by a `v0.16.*` module release. Chart v17 has no JuiceFS CSI driver and ignores the `sandboxes.juicefs.csi` block.

**Fix:** Regenerate the values in the chart v17 schema, then redeploy:

```bash
make init-values
make deploy
```

### Deploy stops on chart v16 JuiceFS volumes

**Symptom:** `make deploy` exits with `ERROR: namespace langsmith still mounts sandbox volumes through the chart 0.16 JuiceFS CSI driver.` followed by `kubectl delete` commands.

**Cause:** Chart v17 removes the JuiceFS CSI driver. Upgrading while chart v16 sandbox volumes are still mounted leaves the old `sandbox-host` pods stuck in `Terminating`, so `deploy.sh` stops before the upgrade.

**Fix:** Run the printed `kubectl delete` commands while the driver still runs. Wait until only `juicefs-csi-*` pods remain, then redeploy:

```bash
kubectl get pods -n langsmith | grep juicefs
make deploy
```

Running sandboxes stop during the drain. Their data stays in S3 and Redis, and chart v17 mounts the same JuiceFS volume.

### Chart v15 values files rejected

**Symptom:** `make deploy` exits with `ERROR: these values files use the chart 0.15 schema, which chart 0.16 rejects:` followed by a list of files.

**Cause:** Chart v16 removed `config.insights`, `config.polly`, and `backend.agentBootstrap`. `make init-values` creates add-on values files only when they are missing, so files generated on chart v15 survive the upgrade.

**Fix:** Delete the listed files from `helm/values/`, then regenerate and redeploy:

```bash
make init-values
make deploy
```

### setup-env.sh run without AWS credentials

**Symptom:** After sourcing `setup-env.sh`, `make secrets` shows every parameter as `✗ MISSING`, and `aws sts get-caller-identity` fails.

**Cause:** No AWS credentials were active. The script still exports `TF_VAR_*` and prints only a warning.

**Fix:** Log in, then re-source the script in the same shell. It backfills the exported values to SSM without prompting again. Run `make preflight` first to catch this.

```bash
aws sso login --profile <profile>
export AWS_PROFILE=<profile>
aws sts get-caller-identity
source infra/scripts/setup-env.sh
```

Without SSM access, the script also writes plaintext fallback files in `infra/`: `.pg_password`, `.api_key_salt`, `.jwt_secret`, `.license_key`, and `.admin_password`. Delete them once `make secrets` shows every parameter in SSM.

### Node group scaling changes not applied by Terraform

**Symptom:** Changing `min_size` or `max_size` in `terraform.tfvars` shows "No changes" on `terraform plan`.

**Cause:** The ASG was changed out-of-band (AWS CLI, console, or cluster autoscaler) and the Terraform state already reflects the new values. The community EKS module ignores `desired_size` changes so the autoscaler can manage it; `min_size` and `max_size` should propagate normally.

**Fix**

```bash
terraform refresh
terraform plan

# For an immediate change, use the AWS CLI directly
aws eks update-nodegroup-config \
  --cluster-name <cluster> \
  --nodegroup-name <nodegroup> \
  --scaling-config minSize=3,maxSize=8,desiredSize=5 \
  --region <region>
```

## Diagnostic commands

### Cluster access

```bash
aws eks update-kubeconfig --region <region> --name <cluster-name>
kubectl config current-context
kubectl get nodes -o wide
aws sts get-caller-identity
```

### Pods

```bash
kubectl get pods -n langsmith
kubectl get pods -n langsmith -w
kubectl describe pod <pod-name> -n langsmith
kubectl logs <pod-name> -n langsmith --tail=50
kubectl logs <pod-name> -n langsmith --previous --tail=50
kubectl logs -n langsmith deploy/langsmith-backend --tail=100 -f
```

### ALB and ingress

```bash
# Default Envoy Gateway mode
kubectl get gateway,httproute -n langsmith
kubectl get targetgroupbinding -A

# Classic ALB Ingress mode
kubectl get ingress -n langsmith
kubectl describe ingress -n langsmith
aws elbv2 describe-load-balancers --query "LoadBalancers[?contains(LoadBalancerName, '<name_prefix>-<environment>')]"
```

### TLS and certificates

```bash
kubectl get certificate -n langsmith
kubectl describe certificate <cert-name> -n langsmith
kubectl get challenges -n langsmith
kubectl get clusterissuer
```

### ESO and secrets

```bash
kubectl get externalsecret -n langsmith
kubectl describe externalsecret langsmith-config -n langsmith
kubectl get clustersecretstore langsmith-ssm
kubectl get secret langsmith-config -n langsmith -o jsonpath='{.data}' | jq 'keys'
./infra/scripts/manage-ssm.sh validate
./infra/scripts/manage-ssm.sh diff
```

### Helm

```bash
helm status langsmith -n langsmith
helm history langsmith -n langsmith
helm get values langsmith -n langsmith
```

### IRSA and IAM

```bash
kubectl get sa -n langsmith -o yaml | grep eks.amazonaws.com
make tf ARGS="output langsmith_irsa_role_arn"
aws iam get-role --role-name <irsa-role-name>
```

### Agent Server hosting

```bash
kubectl get pods -n langsmith | grep -E "host-backend|listener|operator"
kubectl get lgp -n langsmith
kubectl get crd | grep langchain
kubectl get pods -n keda
```

### Quick health check

```bash
echo "=== Context ===" && kubectl config current-context
echo "=== Nodes ===" && kubectl get nodes
echo "=== Pods ===" && kubectl get pods -n langsmith
echo "=== Routes ===" && kubectl get gateway,httproute,ingress -n langsmith
echo "=== Helm ===" && helm status langsmith -n langsmith 2>/dev/null | grep -E "STATUS|LAST DEPLOYED"
```
