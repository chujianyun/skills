# Mirror images for your LangSmith installation

By default, LangSmith will pull images from our public Docker registry. However, if you are running LangSmith in an environment that does not have internet access, or if you would like to use a private Docker registry, you can mirror the images to your own registry and then configure your LangSmith installation to use those images.

> [!TIP]
>
> To build Agent Server images on the same network, see [Set up a build machine on a restricted network](../../../Deploy/Deploy%20to%20Self-hosted/Configure/Set%20up%20a%20build%20machine%20on%20a%20restricted%20network.md).

## Requirements

* Authenticated access to a Docker registry that your Kubernetes cluster/machine has access to.
* Docker installed on your local machine or a machine that has access to the Docker registry.
* A Kubernetes cluster where you can run LangSmith.

## Mirroring the images

> [!NOTE]
>
> **Fewer images from LangSmith 0.16.21 (chart `0.16.0-rc.17`) onward.** The platform backend, playground, host backend, and the Fleet tool and trigger servers now all run from the single `langsmith-backend` image, so you no longer need to mirror `langsmith-go-backend`, `langsmith-playground`, `hosted-langserve-backend`, `agent-builder-tool-server`, or `agent-builder-trigger-server` (or their `-fips` variants). The corresponding `values.yaml` keys: `platformBackendImage`, `playgroundImage`, `hostBackendImage`, `fleetToolServerImage`, and `fleetTriggerServerImage`, have been removed from the chart; any values you still set for them are ignored.
>
> If you are installing an **earlier** version, keep mirroring those images and setting those keys as before.

The [LangSmith Helm chart repository](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/scripts/mirror_langsmith_images.sh) includes a script that mirrors the images.

> [!WARNING]
>
> The script does not yet reflect the image consolidation in LangSmith 0.16.21. It still pulls `langsmith-go-backend`, `langsmith-playground`, `hosted-langserve-backend`, `agent-builder-tool-server`, and `agent-builder-trigger-server`, which are not published for 0.16.21 and later, so it exits at the first missing image. It also defaults the operator image to `0.1.37`, while chart 0.17.0 uses `0.1.60`. For 0.16.21 and later, mirror the images manually as described below.

To use the script, you will need to run the script with the following command specifying your registry and platform:

```bash
bash mirror_langsmith_images.sh <your-registry> [<platform>]
```

Where `<your-registry>` is the URL of your Docker registry (e.g. `myregistry.com`) and `<platform>` is the platform you are using (e.g. `linux/amd64`, `linux/arm64`, etc.). If you do not specify a platform, it will default to `linux/amd64`.

For example, if your registry is `myregistry.com`, your platform is `linux/arm64`, and your LangSmith app version is `0.17.29`, run:

```bash
bash mirror_langsmith_images.sh --registry myregistry --platform linux/arm64 --version 0.17.29
```

Note that this script will assume that you have Docker installed and that you are authenticated to your registry. It will also push the images to the specified registry with the same repository/tag as the original images.

For LangSmith images, use the `appVersion` from your Helm chart release as the image tag. Do not use `latest`: it is mutable, and pulling images while a release is being published can result in mismatched service versions.

Alternatively, you can pull, mirror, and push the images manually. The images that you will need to mirror are found in the `values.yaml` file of the LangSmith Helm Chart. These can be found here: [LangSmith Helm Chart values.yaml](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/values.yaml#L14)

Here is an example of how to mirror the images using Docker:

```bash
# Pull the images from the public registry
docker pull langchain/langsmith-backend:0.17.29
docker tag langchain/langsmith-backend:0.17.29 <your-registry>/langsmith-backend:0.17.29
docker push <your-registry>/langsmith-backend:0.17.29
```

You will need to repeat this for each image that you want to mirror.

## Configuration

Once the images are mirrored, you will need to configure your LangSmith installation to use the mirrored images. You can do this by modifying the `values.yaml` file for your LangSmith Helm Chart installation. Replace tag with the [LangSmith version](../Reference/Self-hosted%20LangSmith%20changelog.md) you want to deploy. The following example uses `0.17.29`, the app version for chart 0.17.0.

```yaml
images:
  imagePullSecrets: [] # Add your image pull secrets here if needed
  registry: "" # Set this to your registry URL if you mirrored all images to the same registry using our script. Then you can remove the repository prefix from the images below.
  aceBackendImage:
    repository: "(your-registry)/langchain/langsmith-ace-backend"
    pullPolicy: IfNotPresent
    tag: "0.17.29"
  backendImage:
    repository: "(your-registry)/langchain/langsmith-backend"
    pullPolicy: IfNotPresent
    tag: "0.17.29"
  frontendImage:
    repository: "(your-registry)/langchain/langsmith-frontend"
    pullPolicy: IfNotPresent
    tag: "0.17.29"
  operatorImage:
    repository: "(your-registry)/langchain/langgraph-operator"
    pullPolicy: IfNotPresent
    tag: "0.1.60"
  postgresImage:
    repository: "(your-registry)/postgres"
    pullPolicy: IfNotPresent
    tag: "14.7"
  redisImage:
    repository: "(your-registry)/redis"
    pullPolicy: IfNotPresent
    tag: "7"
  clickhouseImage:
    repository: "(your-registry)/clickhouse/clickhouse-server"
    pullPolicy: Always
    tag: "25.12"
  agentBuilderImage: # Fleet
    repository: "(your-registry)/langchain/agent-builder-deep-agent"
    pullPolicy: IfNotPresent
    tag: "0.17.29"
  pollyAgentImage: # Polly, on by default
    repository: "(your-registry)/langchain/langsmith-polly"
    pullPolicy: IfNotPresent
    tag: "0.17.29"
  engineInsightsAgentImage: # Insights (on by default) and Engine
    repository: "(your-registry)/langchain/langsmith-insights-engine"
    pullPolicy: IfNotPresent
    tag: "0.17.29"
  smithdbImage: # SmithDB
    repository: "(your-registry)/langchain/smithdb"
    pullPolicy: IfNotPresent
    tag: "0.17.29"
  presidioAnalyzerImage: # Only when presidioAnalyzer.enabled is true
    repository: "(your-registry)/presidio-analyzer"
    pullPolicy: IfNotPresent
    tag: "2.2.354"
```

Chart 0.17 turns on Polly (`polly.enabled`) and Insights (`insights.enabled`) by default, so a default install also pulls `langsmith-polly` and `langsmith-insights-engine`. Mirror both unless you turn those features off. Mirror the Fleet and SmithDB images only if you enable those features. The Presidio analyzer image comes from `mcr.microsoft.com/presidio-analyzer`.

## Additional images for Sandboxes

If you enable [Sandboxes](../Install%20an%20instance/Additional%20features/Enable%20Sandboxes/Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md), also mirror the sandbox runtime image. The sandbox runtime image is published for `linux/amd64`.

```bash
bash mirror_langsmith_images.sh --registry myregistry --platform linux/amd64 --version 0.17.29 --include-sandboxes
```

Then, configure the sandbox runtime image in your `values.yaml`:

```yaml
images:
  sandboxHostImage:
    repository: "(your-registry)/langchain/sandbox-host"
    pullPolicy: IfNotPresent
    tag: "0.17.29"
```

The `sandbox-host` image contains the compressed ext4 filesystem used to generate the default sandbox snapshot. See [Inspect the default snapshot filesystem](../../../Deploy/Sandboxes/Sandbox%20snapshots.md#inspect-the-default-snapshot-filesystem-in-self-hosted-deployments) to extract and scan it independently.

If your mirrored registry requires authentication, configure `images.imagePullSecrets`. The sandbox runtime uses the same image pull secrets as the other LangSmith images.

The `--include-sandboxes` flag mirrors the LangSmith-owned sandbox runtime image. On chart 0.17, that is the only sandbox image to mirror: `sandbox-host` mounts JuiceFS itself, and the JuiceFS format Job runs the same image.

### JuiceFS CSI images on chart 0.16

On chart 0.16, sandboxes use the JuiceFS CSI driver. If your cluster cannot pull public images at all, also mirror the JuiceFS images the driver uses:

* `docker.io/juicedata/juicefs-csi-driver:v0.31.4`
* `registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.9.0`
* `docker.io/juicedata/mount:ce-v1.3.0` for JuiceFS mount pods

Then, configure the corresponding image overrides:

```yaml
images:
  juicefsCSIImage:
    repository: "(your-registry)/juicedata/juicefs-csi-driver"
    tag: "v0.31.4"
  juicefsCSINodeDriverRegistrarImage:
    repository: "(your-registry)/sig-storage/csi-node-driver-registrar"
    tag: "v2.9.0"
  juicefsMountImage:
    repository: "(your-registry)/juicedata/mount"
    tag: "ce-v1.3.0"
```

Chart 0.16 defaults `images.juicefsMountImage` to `docker.io/juicedata/mount:ce-v1.3.0` and passes it to the CSI driver as `JUICEFS_CE_MOUNT_IMAGE`. In private-registry or air-gapped environments, set both `images.juicefsMountImage.repository` and `images.juicefsMountImage.tag` so mount pods pull from your mirrored registry instead of the public default.

## Additional images for Engine

If you mirror images to a private registry, [Engine](../../../Engine/Self-hosted%20and%20BYOC/LangSmith%20Engine%20on%20Self-hosted%20and%20BYOC.md) uses a single combined image: `langsmith-insights-engine`. Engine also requires sandboxes, which use a separate image described in [Additional images for sandboxes](#additional-images-for-sandboxes).

To mirror the required images:

1. Mirror `langsmith-insights-engine` to your private registry using the [manual mirroring process](#mirroring-the-images).
2. Mirror the sandbox runtime image with `--include-sandboxes` and configure it as described in [Additional images for sandboxes](#additional-images-for-sandboxes).

Override `images.engineInsightsAgentImage.repository` to use your mirrored Engine and Insights image:

```yaml
images:
  engineInsightsAgentImage:
    repository: "(your-registry)/langchain/langsmith-insights-engine"
    pullPolicy: IfNotPresent
    tag: "0.17.29"
```

> [!NOTE]
>
> Do not use `langsmith-clio`. If you are upgrading an existing installation that points to this retired Insights-only image, replace the image repository. The repository name must end in `langsmith-insights-engine`; the chart validates this requirement.

Image mirroring does not remove Engine's LangSmith Intelligence egress requirement, so fully air-gapped installations cannot run Engine. See [LangSmith Intelligence for Engine](Egress%20for%20billing%20and%20operational%20telemetry.md#langsmith-intelligence-for-engine).

## Additional images for Fleet

If you are using Fleet, the LangGraph operator dynamically creates Redis and PostgreSQL (pgvector) pods for each deployment. These pods use images defined in operator templates that require separate configuration.

You must mirror these additional images:

* `docker.io/redis:7`
* `docker.io/pgvector/pgvector:pg15`

Then override the operator templates in your `values.yaml` to use your mirrored images:

```yaml
operator:
  templates:
    redis: |
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: ${service_name}
        namespace: ${namespace}
      spec:
        replicas: 1
        selector:
          matchLabels:
            app: ${service_name}
        template:
          metadata:
            labels:
              app: ${service_name}
          spec:
            enableServiceLinks: false
            containers:
            - name: redis
              image: (your-registry)/redis:7
              ports:
              - containerPort: 6379
                name: redis
              livenessProbe:
                exec:
                  command:
                  - redis-cli
                  - ping
                initialDelaySeconds: 30
                periodSeconds: 10
              readinessProbe:
                tcpSocket:
                  port: 6379
                initialDelaySeconds: 10
                periodSeconds: 5
    db: |
      apiVersion: apps/v1
      kind: StatefulSet
      metadata:
        name: ${service_name}
      spec:
        serviceName: ${service_name}
        selector:
          matchLabels:
            app: ${service_name}
        persistentVolumeClaimRetentionPolicy:
          whenDeleted: Delete
          whenScaled: Retain
        template:
          metadata:
            labels:
              app: ${service_name}
          spec:
            containers:
            - name: postgres
              image: (your-registry)/pgvector/pgvector:pg15
              ports:
              - containerPort: 5432
              command: ["docker-entrypoint.sh"]
              args:
                - postgres
                - -c
                - max_connections=${max_connections}
              env:
              - name: PGDATA
                value: /var/lib/postgresql/data/pgdata
              volumeMounts:
              - name: postgres-data
                mountPath: /var/lib/postgresql/data
            enableServiceLinks: false
        volumeClaimTemplates:
        - metadata:
            name: postgres-data
          spec:
            accessModes: ["ReadWriteOnce"]
            resources:
              requests:
                storage: "${storage_gi}Gi"
```

Replace `(your-registry)` with your registry URL. The template variables (`${service_name}`, `${namespace}`, `${max_connections}`, `${storage_gi}`) are replaced by the operator at runtime and must be kept as-is.

Once configured, you will need to update your LangSmith installation. You can follow our upgrade guide here: [Upgrading LangSmith](../Manage%20an%20instance/Upgrade%20an%20installation.md). If your upgrade is successful, your LangSmith instance should now be using the mirrored images from your Docker registry.

## Additional images for Agent Server builds

The [LangGraph CLI](../../../Deploy/Get%20started/Reference/LangGraph%20CLI.md) builds each Agent Server image on top of a public base image. When your build machine cannot reach Docker Hub, mirror the base image and point `base_image` in `langgraph.json` at the mirror. For the rest of the build setup, see [Build Agent Server images on a restricted network](../../../Deploy/Deploy%20to%20Self-hosted/Configure/Set%20up%20a%20build%20machine%20on%20a%20restricted%20network.md).

The base image repository depends on the project language:

* **Python**: `langchain/langgraph-api`
* **JavaScript**: `langchain/langgraphjs-api`

The CLI picks the tag from `langgraph.json`, so mirror the tag that matches your configuration:

| `langgraph.json` settings | Python tag | JavaScript tag |
| - | - | - |
| `python_version` or `node_version` only | `3.12` | `20` |
| With `api_version` | `0.8.1-py3.12` | `0.8.1-node20` |
| With `image_distro` | Append `-wolfi` or `-bookworm`, for example `3.12-wolfi` | Append `-wolfi` or `-bookworm`, for example `20-wolfi` |

To mirror a base image:

```bash
docker pull langchain/langgraph-api:3.12
docker tag langchain/langgraph-api:3.12 <your-registry>/langchain/langgraph-api:3.12
docker push <your-registry>/langchain/langgraph-api:3.12
```

Then set `base_image` to the mirrored repository without a tag:

```json
{
  "base_image": "<your-registry>/langchain/langgraph-api"
}
```

* The CLI appends the tag itself, so a `base_image` value that includes a tag produces an invalid image reference.
* Set `api_version` to an exact version such as `0.8.1`. A version range makes the CLI query pypi.org at build time to resolve it.

## Verifying image signatures

> [!NOTE]
>
> Image signatures are available **starting with v15** (LangSmith app version `0.15.x` and later). Earlier releases on the `v14-stable` and older channels are not signed and cannot be verified with the steps below.

Stable-channel LangSmith images on `docker.io/langchain/*` are signed at release time using keyless [Sigstore/Cosign](https://docs.sigstore.dev/cosign/overview/) from the release workflow. The signing identity is bound to a specific GitHub Actions workflow, run, and commit, so the signature attests that the image is authentic and that the stable-branch release pipeline produced it running in `langchain-ai/langchainplus`. You can verify a signature before pulling or mirroring an image, and again after mirroring to confirm the digest you mirrored matches the signed one.

Install `cosign` ([installation guide](https://docs.sigstore.dev/cosign/system_config/installation/)), then verify any tag:

```bash
cosign verify \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp 'https://github\.com/langchain-ai/langchainplus/\.github/workflows/release_self_hosted_on_version_bump\.yaml@refs/heads/v[0-9]+-stable' \
  docker.io/langchain/langsmith-backend:<tag>
```

A successful verification confirms:

* The cosign claims on the signature are valid.
* The certificate chains to the Sigstore root and is logged in the [Rekor](https://docs.sigstore.dev/rekor/overview/) transparency log.
* The signing certificate was issued to the stable-branch release workflow via GitHub Actions OIDC.

The same command works against any of the released images by substituting the repository (`langsmith-frontend`, `langsmith-go-backend`, `agent-builder-deep-agent`, `langsmith-insights-engine`, `langsmith-polly`, `agent-builder-tool-server`, `agent-builder-trigger-server`, `hosted-langserve-backend`, `langsmith-playground`, `langsmith-ace-backend`, plus their `*-fips` variants).

### Pinning to a specific release

For stricter verification, such as pinning to a single stable branch or a specific commit, drop the regex and supply the exact certificate identity. Each signature's certificate also carries the workflow run ID and commit SHA as Subject Alternative Name extensions, so you can constrain to a specific release:

```bash
cosign verify \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity 'https://github.com/langchain-ai/langchainplus/.github/workflows/release_self_hosted_on_version_bump.yaml@refs/heads/v15-stable' \
  docker.io/langchain/langsmith-backend:0.15.9
```

To inspect the certificate's claims (workflow run, commit, runner), download the attestation and decode the embedded certificate:

```bash
cosign download attestation docker.io/langchain/langsmith-backend:<tag>
```

### Verifying SBOM attestations

Released images also carry signed CycloneDX software bill of materials (SBOM) attestations, one per architecture in the image index.

The per-architecture SBOMs are also attached to the multi-architecture index digest, so you can verify against a bare tag directly:

```bash
cosign verify-attestation \
  --type cyclonedx \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp 'https://github\.com/langchain-ai/langchainplus/\.github/workflows/release_self_hosted_on_version_bump\.yaml@refs/heads/v[0-9]+-stable' \
  docker.io/langchain/langsmith-backend:<tag>
```

The command returns one verified statement per architecture. A successful verification gives the same guarantees as the image signature: the attestation was produced by the stable-branch release workflow, and its claims are logged in the [Rekor](https://docs.sigstore.dev/rekor/overview/) transparency log.

### Fetching SBOMs

To feed an SBOM into a vulnerability scanner or SBOM management tool, extract the verified CycloneDX document to a file. Because the index carries one statement per architecture, resolve a single architecture's child digest first so you get one CycloneDX document rather than one per architecture.

List the per-architecture digests for a tag:

```bash
docker buildx imagetools inspect --raw docker.io/langchain/langsmith-backend:<tag> \
  | jq -r '.manifests[] | select(.platform.os == "linux") | .digest + "  " + .platform.architecture'
```

Then verify that digest and save the decoded predicate to a file. The predicate is a standard CycloneDX document that lists every package in the image:

```bash
cosign verify-attestation \
  --type cyclonedx \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp 'https://github\.com/langchain-ai/langchainplus/\.github/workflows/release_self_hosted_on_version_bump\.yaml@refs/heads/v[0-9]+-stable' \
  docker.io/langchain/langsmith-backend@<digest> \
  | jq -r '.payload' | base64 -d | jq '.predicate' > langsmith-backend.cdx.json
```

You can pass the resulting `langsmith-backend.cdx.json` directly to scanners such as [Grype](https://github.com/anchore/grype) (`grype sbom:langsmith-backend.cdx.json`) or [Trivy](https://trivy.dev/) (`trivy sbom langsmith-backend.cdx.json`).

> [!NOTE]
>
> Extracting the SBOM through `cosign verify-attestation`, rather than `cosign download attestation`, ensures you only ever consume an SBOM whose signature and signing identity have been verified.
