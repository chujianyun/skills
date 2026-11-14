# Configure AES encryption at rest

> Configure built-in AES encryption and lazy key rotation for Agent Server data.

Built-in AES encryption is the recommended approach for encrypting Agent Server data at rest. Use [custom encryption handlers](Configure%20custom%20encryption%20at%20rest.md) only when you need per-tenant keys or an external key management system.

## Configure AES encryption

Set `LANGGRAPH_AES_KEY` to encrypt checkpoint blobs automatically:

1. Add `pycryptodome` to your dependencies in `langgraph.json`:
   ```json
   {
     "dependencies": [".", "pycryptodome"],
     "graphs": {
       "agent": "./agent.py:graph"
     }
   }
   ```

2. Set `LANGGRAPH_AES_KEY` to a 16, 24, or 32-byte key for AES-128, AES-192, or AES-256, respectively.

### Encrypt JSON fields

Set `LANGGRAPH_AES_JSON_KEYS` to a comma-separated list of JSON keys to encrypt:

```bash
export LANGGRAPH_AES_KEY="your-16-24-or-32-byte-key"
export LANGGRAPH_AES_JSON_KEYS="api_key,secret_token,user_credentials"
```

These keys are encrypted wherever they appear in thread, assistant, run, cron, and store data.

> [!WARNING]
>
> Encrypted fields cannot be searched or filtered.

System fields cannot be encrypted: `langgraph_version`, `langgraph_api_version`, `langgraph_plan`, `langgraph_host`, `langgraph_api_url`, `langgraph_request_id`, `langgraph_auth_user_id`, and `langgraph_auth_permissions`.

## Rotate AES keys

> [!NOTE]
>
> AES key rotation requires Agent Server version `0.17.0.dev3` or later, the PostgreSQL checkpointer with `PREFER_GRPC_CHECKPOINTER=true`, and the Go store with `LANGGRAPH_STORE_BACKEND=grpc`. Python, custom, SQLite, and MongoDB checkpointers do not support rotation.

Agent Server encrypts new data with `LANGGRAPH_AES_KEY`. Key envelopes identify which configured key decrypts each value. When Agent Server reads data encrypted with an old key, it returns the plaintext and lazily re-encrypts the stored value with the current key.

To rotate a key:

1. Configure the current primary key and future key on every replica:

   ```bash
   export LANGGRAPH_AES_KEY="your-current-16-24-or-32-byte-key"
   export LANGGRAPH_AES_FALLBACK_KEYS="your-future-16-24-or-32-byte-key"
   ```

2. Roll out this configuration to every replica.

3. After every replica can decrypt both keys, switch `LANGGRAPH_AES_KEY` to the future key.

4. Retain the old key in both compatibility settings:

   ```bash
   export LANGGRAPH_AES_KEY="your-future-16-24-or-32-byte-key"
   export LANGGRAPH_AES_LEGACY_KEY="your-old-16-24-or-32-byte-key"
   export LANGGRAPH_AES_FALLBACK_KEYS="your-old-16-24-or-32-byte-key"
   ```

   `LANGGRAPH_AES_LEGACY_KEY` decrypts untagged historical ciphertext. `LANGGRAPH_AES_FALLBACK_KEYS` decrypts tagged ciphertext created with an old key.

5. Keep old keys configured until telemetry confirms they are no longer needed.

> [!WARNING]
>
> * Never change the primary key before every replica can decrypt both keys.
> * Lazy rotation updates only accessed rows. Cold rows and compare-and-swap misses may retain old ciphertext.
> * Removing keys early can make retained data unreadable.
> * Once key-envelope ciphertext exists, Agent Server versions without envelope support cannot read it.

## Related

* [Choose an encryption approach](Encryption%20at%20rest.md)
* [Configure custom encryption](Configure%20custom%20encryption%20at%20rest.md)
