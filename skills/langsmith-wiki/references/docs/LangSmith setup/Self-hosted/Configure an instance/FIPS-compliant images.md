# FIPS-compliant images

> Run self-hosted LangSmith installation on FIPS 140 compliant container images

> [!NOTE]
>
> FIPS and airgapped LangSmith deployments require a conversation with your LangChain account executive before rollout. Reach out to scope licensing, supported configurations, and upgrade paths before you change your installation.

As of v15, every LangChain-authored LangSmith image has a `-fips` counterpart that runs in FIPS 140 mode. Use these images when your self-hosted deployment needs FIPS compliance, for example in federal agencies, defense contractors, and regulated industries.

## How the images are built

The `-fips` variants are built on top of [Chainguard FIPS container images](https://edu.chainguard.dev/chainguard/fips/fips-images/), which ship NIST-validated cryptographic modules (OpenSSL FIPS provider, Bouncy Castle FIPS, or BoringCrypto depending on the base). For the list of modules and their CMVP certificates, refer to [Chainguard's FIPS commitment](https://edu.chainguard.dev/chainguard/fips/fips-images/).

Every LangChain-authored image has a `-fips` counterpart published at the same tag as the non-FIPS version:

| Non-FIPS image | FIPS image |
| - | - |
| `langchain/langsmith-ace-backend` | `langchain/langsmith-ace-backend-fips` |
| `langchain/langsmith-backend` | `langchain/langsmith-backend-fips` |
| `langchain/langsmith-frontend` | `langchain/langsmith-frontend-fips` |
| `langchain/langgraph-operator` | `langchain/langgraph-operator-fips` |

> [!NOTE]
>
> **Fewer images from LangSmith 0.16.21 (chart `0.16.0-rc.17`) onward.** The platform backend, playground, host backend, and the Fleet tool and trigger servers now all run from the single `langsmith-backend` image, so `langsmith-go-backend-fips`, `langsmith-playground-fips`, `hosted-langserve-backend-fips`, `agent-builder-tool-server-fips`, and `agent-builder-trigger-server-fips` are no longer needed. The corresponding `values.yaml` keys: `platformBackendImage`, `playgroundImage`, `hostBackendImage`, `fleetToolServerImage`, and `fleetTriggerServerImage`, have been removed from the chart; any values you still set for them are ignored.
>
> On **earlier** versions those five images are published with `-fips` counterparts at the same tag as well; point each of those keys at its `-fips` repository too.

PostgreSQL, Redis, and ClickHouse are not published as FIPS variants by LangChain. If your deployment requires FIPS for these components, bring your own FIPS-mode service and connect via [external Postgres](../Connect%20external%20services/Connect%20to%20an%20external%20PostgreSQL%20database.md), [external Redis](../Connect%20external%20services/Connect%20to%20an%20external%20Redis%20or%20Valkey%20database.md), or [external ClickHouse](../Connect%20external%20services/Connect%20to%20an%20external%20ClickHouse%20database.md).

### ACE backend FIPS boundary note

`langsmith-ace-backend-fips` is built on the same Chainguard FIPS base as all other `-fips` images, but its code-execution runtimes (Deno and Pyodide/WebAssembly) bundle their own cryptographic libraries and do not dynamically link the system FIPS-validated OpenSSL, so the execution runtime itself falls technically outside the FIPS 140 module boundary.

We consider this acceptable for regulated environments: FIPS governs the platform's cryptographic operations on sensitive data, and ACE performs none. It injects no secrets into user code, persists no data and performs no data-at-rest cryptography, and its execution subprocesses have no network access. ACE is an in-cluster HTTP service called by the LangSmith backend; when TLS is terminated upstream by a FIPS-validated mesh or ingress, ACE performs no in-scope cryptographic operations.

## Use FIPS images

Update `values.yaml` in your LangSmith Helm installation to point each LangChain image repository at its `-fips` counterpart, keeping your existing tag. Replace `0.16.21` with the [LangSmith version](../Reference/Self-hosted%20LangSmith%20changelog.md) you want to deploy:

```yaml
images:
  aceBackendImage:
    repository: "langchain/langsmith-ace-backend-fips"
    pullPolicy: IfNotPresent
    tag: "0.16.21"
  backendImage:
    repository: "langchain/langsmith-backend-fips"
    pullPolicy: IfNotPresent
    tag: "0.16.21"
  frontendImage:
    repository: "langchain/langsmith-frontend-fips"
    pullPolicy: IfNotPresent
    tag: "0.16.21"
  operatorImage:
    repository: "langchain/langgraph-operator-fips"
    pullPolicy: IfNotPresent
    tag: "0.16.21"
```

Apply the change and upgrade following the [Upgrading LangSmith](../Manage%20an%20instance/Upgrade%20an%20installation.md) guide.

## Verify FIPS mode

Chainguard ships the `openssl-fips-test` tool inside every FIPS image. Running it against a pod prints the FIPS self-tests, the active FIPS provider version, and a link to the applicable CMVP certificate.

Check a running pod:

```bash
kubectl exec <pod-name> -- openssl-fips-test
```

Expected output (abridged):

```text
Checking OpenSSL lifecycle assurance.
	✓ Self-test KAT_Integrity HMAC ... passed.
	✓ Self-test Module_Integrity HMAC ... passed.
	...
	✓ 29 out of 29 self-tests passed.
	✓ Check FIPS cryptographic module is available... passed.
	✓ Check FIPS approved only mode (EVP_default_properties_is_fips_enabled)... passed.
Public OpenSSL API (libssl.so & libcrypto.so):
	name:      OpenSSL 3.6.0 1 Oct 2025
	version:   3.6.0
FIPS cryptographic module provider details (fips.so):
	name:      OpenSSL FIPS Provider
	version:   3.1.2
Locate applicable CMVP certificate(s) at: CMVP #4985
```

You can also verify an image outside Kubernetes:

```bash
docker run --rm --entrypoint openssl-fips-test langchain/langsmith-backend-fips:0.16.21
```

For more detail on interpreting the output, see [Chainguard's FIPS verification guide](https://edu.chainguard.dev/chainguard/fips/verify-fips/).

## Mirror for airgapped deployments

The `-fips` naming convention applies identically when mirroring images to a private registry. Follow the [image mirroring guide](Mirror%20images%20for%20your%20LangSmith%20installation.md) and substitute each repository with its `-fips` counterpart. Airgapped rollouts, with or without FIPS, require scoping with your LangChain account executive before you begin.
