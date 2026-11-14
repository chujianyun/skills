# Encryption at rest

> Choose between built-in AES encryption and custom encryption handlers for Agent Server data.

Agent Server supports two approaches to application-level encryption at rest. Use built-in AES encryption unless you need per-tenant keys or an external key management system.

## Choose an encryption approach

> [card] [Built-in AES encryption](Configure%20AES%20encryption%20at%20rest.md)
>
> Recommended for most deployments. Configure an AES key to encrypt checkpoint data and selected JSON fields. Supports lazy key rotation.

> [card] [Custom encryption](Configure%20custom%20encryption%20at%20rest.md)
>
> Use only when built-in AES does not meet your requirements. Supports per-tenant keys and external key management systems through custom handlers.

Choose [built-in AES encryption](Configure%20AES%20encryption%20at%20rest.md) if you need:

* One encryption key for the deployment
* Key rotation
* Selective encryption of JSON fields

Choose [custom encryption](Configure%20custom%20encryption%20at%20rest.md) only if you need:

* Different encryption keys for different tenants
* An external key management system
* Custom encryption logic or audit behavior
