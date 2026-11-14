# Configure custom encryption at rest

Custom encryption lets Agent Server use your encryption handlers for per-tenant keys and external key management systems. Use [built-in AES encryption](Configure%20AES%20encryption%20at%20rest.md) unless you need these capabilities.

> [!WARNING]
>
> Agent Server versions 0.5.34–0.6.21 included a pre-release version of custom encryption. Data encrypted with these versions will be corrupted when upgrading to 0.6.22+. Do not use custom encryption on these versions.

> [!WARNING]
>
> Only use custom encryption if built-in AES encryption does not meet your needs. Custom encryption requires you to implement and maintain encryption handlers, and adds operational complexity. If you only need a static key, key rotation, or optional selective field encryption, use [built-in AES encryption](Configure%20AES%20encryption%20at%20rest.md) instead.

Use custom encryption when you need:

* **Per-tenant key isolation**—different encryption keys for different customers
* **KMS integration**—AWS KMS, Google Cloud KMS, or HashiCorp Vault for key management, rotation, and audit logging

## Configure custom encryption

### How it works

1. [Configure](#configuration) the encryption module path in `langgraph.json`
2. [Define an encryption context handler](#define-encryption-context) that derives values such as a tenant ID from the authenticated user
3. [Define your encryption module](#defining-your-encryption-module) with handlers for blob and JSON encryption
4. Agent Server calls your handlers before storing and after retrieving data

For production deployments with key rotation and audit logging, see [Envelope encryption with AWS Encryption SDK](#envelope-encryption-with-aws-encryption-sdk).

### Configuration

Add your encryption module to `langgraph.json`:

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./agent.py:graph"
  },
  "encryption": {
    "path": "./encryption.py:encryption"
  }
}
```

> [!NOTE]
>
> If you're migrating from basic encryption, keep `LANGGRAPH_AES_KEY` configured. Custom encryption handles new writes while existing AES-encrypted data remains readable.

### Define encryption context

Use `@encryption.context` to derive encryption context from the authenticated user:

```python
from langgraph_sdk import Encryption, EncryptionContext
from starlette.authentication import BaseUser

encryption = Encryption()


@encryption.context
async def get_encryption_context(user: BaseUser, ctx: EncryptionContext) -> dict:
    return {
        **ctx.metadata,
        "tenant_id": user.identity,
    }
```

This handler runs once per request after authentication. The returned dictionary becomes `ctx.metadata` for every encryption operation in the request and is stored in plaintext so Agent Server can restore it during decryption. Include only non-secret identifiers and routing metadata, never keys, tokens, or credentials.

### Defining your encryption module

#### Blob encryption (checkpoints)

Blob handlers encrypt checkpoint data—the serialized state from graph execution. Here's a simplified example using per-tenant keys with [Fernet](https://cryptography.io/en/latest/fernet/) (a symmetric encryption scheme from the `cryptography` library):

```python
import os
from cryptography.fernet import Fernet
from langgraph_sdk import EncryptionContext

# In production, fetch from a secrets manager
TENANT_KEYS = {
    "tenant-a": Fernet(os.environ["TENANT_A_KEY"]),
    "tenant-b": Fernet(os.environ["TENANT_B_KEY"]),
}


def _get_fernet(ctx: EncryptionContext) -> Fernet:
    tenant_id = ctx.metadata.get("tenant_id")
    if not tenant_id or tenant_id not in TENANT_KEYS:
        raise ValueError(f"Unknown tenant: {tenant_id}")
    return TENANT_KEYS[tenant_id]


@encryption.encrypt.blob
async def encrypt_blob(ctx: EncryptionContext, data: bytes) -> bytes:
    return _get_fernet(ctx).encrypt(data)


@encryption.decrypt.blob
async def decrypt_blob(ctx: EncryptionContext, data: bytes) -> bytes:
    return _get_fernet(ctx).decrypt(data)
```

The `ctx.metadata` dictionary comes from the context handler, so each encryption handler can select the correct key.

#### JSON encryption (metadata)

JSON handlers encrypt structured data like thread metadata, assistant context, and run kwargs. Unlike blob encryption, you choose which fields to encrypt—keeping some unencrypted for search and filtering.

```python
import json
import os
from cryptography.fernet import Fernet
from langgraph_sdk import EncryptionContext

TENANT_KEYS = {
    "tenant-a": Fernet(os.environ["TENANT_A_KEY"]),
    "tenant-b": Fernet(os.environ["TENANT_B_KEY"]),
}

SKIP_FIELDS = {
    "tenant_id", "owner",
    "run_id", "thread_id", "graph_id", "assistant_id", "user_id", "checkpoint_id",
    "source", "step", "parents", "run_attempt",
    "langgraph_version", "langgraph_api_version", "langgraph_plan", "langgraph_host",
    "langgraph_api_url", "langgraph_request_id", "langgraph_auth_user",
    "langgraph_auth_user_id", "langgraph_auth_permissions",
}
ENCRYPTED_PREFIX = "encrypted:"


def _get_fernet(ctx: EncryptionContext) -> Fernet:
    tenant_id = ctx.metadata.get("tenant_id")
    if not tenant_id or tenant_id not in TENANT_KEYS:
        raise ValueError(f"Unknown tenant: {tenant_id}")
    return TENANT_KEYS[tenant_id]


@encryption.encrypt.json
async def encrypt_json(ctx: EncryptionContext, data: dict) -> dict:
    fernet = _get_fernet(ctx)
    result = {}
    for k, v in data.items():
        if k in SKIP_FIELDS or v is None:
            result[k] = v
        else:
            value_json = json.dumps(v)
            encrypted = fernet.encrypt(value_json.encode()).decode()
            result[k] = ENCRYPTED_PREFIX + encrypted
    return result


@encryption.decrypt.json
async def decrypt_json(ctx: EncryptionContext, data: dict) -> dict:
    fernet = _get_fernet(ctx)
    result = {}
    for k, v in data.items():
        if isinstance(v, str) and v.startswith(ENCRYPTED_PREFIX):
            encrypted_value = v[len(ENCRYPTED_PREFIX):]
            decrypted = fernet.decrypt(encrypted_value.encode()).decode()
            result[k] = json.loads(decrypted)
        else:
            result[k] = v
    return result
```

#### JSON encryption considerations

> [!WARNING]
>
> **Encrypted fields cannot be searched or filtered.** Design your metadata schema so that fields you need to query remain unencrypted.

> [!WARNING]
>
> **JSON encryptors must preserve key structure.** SQL JSONB merge operations work at the key level. Encryptors that change keys—whether by consolidating fields (e.g., moving sensitive data into `__encrypted__`) or by encrypting key names themselves—cause data loss during merges. Use per-key encryption: transform values in-place while preserving keys.

> [!NOTE]
>
> **Migration consideration:** Use a recognizable prefix or format in encrypted values so your decryptor can detect and skip unencrypted data. This allows you to encrypt additional fields in the future without re-encrypting existing records. The example above uses this pattern.

> [!NOTE]
>
> **Performance consideration:** Per-key encryption means one encryption call per field. If your encryption involves round-trips to an external service (e.g., KMS), this can significantly impact latency. Consider caching data keys locally or using envelope encryption where you encrypt a local data key with KMS and use it for multiple fields.

Fields used by authorization filters (e.g., `tenant_id`, `owner`) must remain unchanged and **unencrypted**, as must fields used for search and filtering. Agent Server rejects writes if a custom encryptor changes an authorization-filter field. Additionally, **some system-managed fields will never be encrypted**:

* Resource identifiers (`thread_id`, `run_id`, `assistant_id`, `graph_id`, `checkpoint_id`, `task_id`)
* Named LangGraph system fields (`langgraph_version`, `langgraph_api_version`, `langgraph_plan`, `langgraph_host`, `langgraph_api_url`, `langgraph_request_id`, `langgraph_auth_user`, `langgraph_auth_user_id`, `langgraph_auth_permissions`)
* Required checkpoint metadata (`source`, `step`, `parents`, `run_attempt`)
* Named internal fields used for scheduling and orchestration, including `__after_seconds__` and `__request_start_time_ms__`
* Run-level execution limits (`max_concurrency`, `recursion_limit`) specified in a run's `config`
* Thread TTL updates (`ttl`) specified in a run's `config.configurable`

#### What gets encrypted

**JSON handlers** (`@encryption.encrypt.json` / `@encryption.decrypt.json`) are applied recursively to fields including:

* `thread.metadata`, `thread.values`
* `assistant.metadata`, `assistant.context`
* `run.metadata`, `run.kwargs`
* `cron.metadata`, `cron.payload`
* `store.value`

[Some fields are excluded from encryption.](#json-encryption-considerations) Unless otherwise noted, these exclusions apply at every level of a nested JSON object, not just the root level.

**Blob handlers** (`@encryption.encrypt.blob` / `@encryption.decrypt.blob`) are applied to checkpoint blobs (graph execution state).

### Rotate custom encryption keys lazily

> [!NOTE]
>
> Lazy re-encryption requires Agent Server version `0.14.0` or later, Python SDK version `langgraph-sdk>=0.4.3`, the PostgreSQL checkpointer, `PREFER_GRPC_CHECKPOINTER=true`, and `LANGGRAPH_STORE_BACKEND=grpc`.

Return `DecryptResult` from a blob or JSON decrypt handler when the handler decrypts data with an old key. Its `plaintext` value is returned to the caller, and its `replacement` value is new ciphertext for Agent Server to persist.

For example, replace the blob decrypt handler above with one that tries the current tenant key first, then returns replacement ciphertext when a legacy key succeeds:

```python
import os

from cryptography.fernet import Fernet, InvalidToken
from langgraph_sdk import DecryptResult, EncryptionContext

LEGACY_TENANT_KEYS = {
    "tenant-a": [Fernet(os.environ["TENANT_A_LEGACY_KEY"])],
    "tenant-b": [Fernet(os.environ["TENANT_B_LEGACY_KEY"])],
}


@encryption.decrypt.blob
async def decrypt_blob(
    ctx: EncryptionContext, data: bytes
) -> bytes | DecryptResult[bytes]:
    current_key = _get_fernet(ctx)
    try:
        return current_key.decrypt(data)
    except InvalidToken:
        tenant_id = ctx.metadata["tenant_id"]
        for legacy_key in LEGACY_TENANT_KEYS.get(tenant_id, []):
            try:
                plaintext = legacy_key.decrypt(data)
                return DecryptResult(
                    plaintext=plaintext,
                    replacement=current_key.encrypt(plaintext),
                )
            except InvalidToken:
                continue
        raise
```

JSON decrypt handlers can return `DecryptResult[dict]` in the same way. The replacement must have the same shape as a normal result from the corresponding encrypt handler.

Agent Server writes the replacement with a compare-and-swap operation, so it does not overwrite a concurrent update. Re-encryption is best effort: a read still succeeds if the stored value changes before writeback or if writeback fails.

> [!WARNING]
>
> Lazy re-encryption only updates data as it is read. Keep old keys available while unread data may still require them.

### Monitor lazy re-encryption

Agent Server emits the following INFO-tier [internal metrics](../../../Deploy%20to%20Self-hosted/Configure/Agent%20Server%20metrics.md#internal-metrics) for replacement writebacks:

| Metric | Meaning |
| - | - |
| `lg_api_reencrypt_writeback_succeeded_counter` | The replacement ciphertext was stored. |
| `lg_api_reencrypt_writeback_cas_skipped_counter` | A concurrent update changed the stored value before writeback. Agent Server left the newer value unchanged. |
| `lg_api_reencrypt_writeback_failed_counter` | Agent Server could not write the replacement. The read still succeeded. |

Each metric includes `reencryption_table` and `reencryption_column` attributes. Use them to find surfaces that still read old ciphertext and to isolate writeback failures.

CAS skips produce warning logs with `Re-encryption writeback skipped due to concurrent update`. Failures produce error logs with `Re-encryption writeback failed`. Both include the table and column. Successful writebacks do not produce logs.

For Prometheus, set `EXPOSE_INTERNAL_METRICS_PROMETHEUS=true` and scrape the Agent Server `/metrics` endpoint. Internal metrics are also available through the documented Datadog export.

These counters measure writeback outcomes, not the amount of old ciphertext remaining. A period without new writebacks does not prove that every record has been read and rotated. Keep old keys available until your retention policy or a separate exhaustive migration confirms that no unread data requires them.

### Envelope encryption with AWS Encryption SDK

For production deployments on AWS, use the [AWS Encryption SDK](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/python.html) with AWS KMS, or an equivalent within your cloud provider. This approach:

* Handles envelope encryption automatically (no manual key packing)
* Provides key rotation and audit logging
* Binds ciphertext to encryption context (tenant isolation)
* Caches data keys locally to avoid repeated KMS calls, latency and rate limits

#### Complete example

```python
import base64
import json
import os

import aws_encryption_sdk
from aws_encryption_sdk import (
    CachingCryptoMaterialsManager,
    CommitmentPolicy,
    LocalCryptoMaterialsCache,
    StrictAwsKmsMasterKeyProvider,
)
from langgraph_sdk import Encryption, EncryptionContext

encryption = Encryption()

# The SDK uses envelope encryption: one KMS API call generates a data key,
# then encrypts/decrypts locally. The cache reuses data keys across operations.
client = aws_encryption_sdk.EncryptionSDKClient(
    commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT
)
key_provider = StrictAwsKmsMasterKeyProvider(key_ids=[os.environ["KMS_KEY_ARN"]])
cache = LocalCryptoMaterialsCache(capacity=100)
cmm = CachingCryptoMaterialsManager(
    master_key_provider=key_provider,
    cache=cache,
    max_age=300.0,
    max_messages_encrypted=100,
)

SKIP_FIELDS = {
    "tenant_id", "owner",
    "run_id", "thread_id", "graph_id", "assistant_id", "user_id", "checkpoint_id",
    "source", "step", "parents", "run_attempt",
    "langgraph_version", "langgraph_api_version", "langgraph_plan", "langgraph_host",
    "langgraph_api_url", "langgraph_request_id", "langgraph_auth_user",
    "langgraph_auth_user_id", "langgraph_auth_permissions",
}
ENCRYPTED_PREFIX = "encrypted:"


@encryption.encrypt.blob
async def encrypt_blob(ctx: EncryptionContext, data: bytes) -> bytes:
    ciphertext, _ = client.encrypt(
        source=data,
        materials_manager=cmm,
        encryption_context={"tenant_id": ctx.metadata["tenant_id"]},
    )
    return ciphertext


@encryption.decrypt.blob
async def decrypt_blob(ctx: EncryptionContext, data: bytes) -> bytes:
    plaintext, _ = client.decrypt(source=data, key_provider=key_provider)
    return plaintext


@encryption.encrypt.json
async def encrypt_json(ctx: EncryptionContext, data: dict) -> dict:
    tenant_id = ctx.metadata["tenant_id"]
    result = {}
    for k, v in data.items():
        if k in SKIP_FIELDS or v is None:
            result[k] = v
        else:
            ciphertext, _ = client.encrypt(
                source=json.dumps(v).encode(),
                materials_manager=cmm,
                encryption_context={"tenant_id": tenant_id},
            )
            result[k] = ENCRYPTED_PREFIX + base64.b64encode(ciphertext).decode()
    return result


@encryption.decrypt.json
async def decrypt_json(ctx: EncryptionContext, data: dict) -> dict:
    result = {}
    for k, v in data.items():
        if isinstance(v, str) and v.startswith(ENCRYPTED_PREFIX):
            ciphertext = base64.b64decode(v[len(ENCRYPTED_PREFIX):])
            plaintext, _ = client.decrypt(source=ciphertext, key_provider=key_provider)
            result[k] = json.loads(plaintext.decode())
        else:
            result[k] = v
    return result
```

The `encryption_context` is cryptographically bound to the ciphertext via KMS—decryption fails if the context doesn't match. The context is embedded in the ciphertext, so decrypt handlers don't need to reference `ctx.metadata`.

#### Key rotation

KMS rotates backing material for the same key ID automatically. Old encrypted data keys remain decryptable, so existing data does not need re-encryption.

## Related

* [Custom authentication](../../Auth%20%26%20access%20control/Add%20custom%20authentication.md)
