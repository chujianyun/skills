# Basic authentication with email and password

Basic authentication lets users log in to LangSmith [Self-hosted](../Self-hosted%20LangSmith.md) with an email and password, without configuring an external identity provider. [Organization Admins](../../Govern/Users%20%26%20access%20control/Role-based%20access%20control.md#organization-admin) manage users directly from LangSmith, so authentication runs self-contained without depending on [OAuth or SSO](Set%20up%20SSO%20with%20OAuth2.0%20and%20OIDC.md).

> [!TIP]
>
> For a description of the supported authentication methods in LangSmith Self-hosted, refer to the [Authentication methods](../../Govern/Users%20%26%20access%20control/Authentication%20methods.md#self-hosted) page.

## Considerations

* You can upgrade a basic auth installation to [OAuth with client secret](Set%20up%20SSO%20with%20OAuth2.0%20and%20OIDC.md#with-client-secret-recommended) by swapping the configuration parameters, but you cannot switch back to basic auth from any OAuth mode.
* You cannot switch between basic auth and OAuth with PKCE (deprecated), in either direction.
* A new basic auth installation requires a fresh installation including a separate PostgreSQL database/schema, unless migrating from an existing [None](../../Govern/Users%20%26%20access%20control/Authentication%20methods.md#none) auth installation (refer to [Migrating from none auth](#migrating-from-none-auth)).
* Users receive an auto-generated initial password when invited, which must be shared with them out of band. Any Organization Admin can change this password later.
* You cannot enable basic auth and OAuth with client secret at the same time.
* All basic auth users share a single `Default` [organization](../../Govern/Organization/Overview.md#organizations) that is provisioned at install time. Creating additional organizations is not supported.

## Requirements and features

* Your initial password must be at least 12 characters long and contain at least one lowercase, uppercase, and symbol (refer to [Configuration](#configuration)).
* The secret used for signing JWTs has no strict requirements, but should be a securely generated string of at least 32 characters. For example, [`openssl rand -base64 32`](https://docs.openssl.org/1.0.2/man1/rand/#description).

## Migrating from none auth

> [!NOTE]
>
> Only supported in [versions 0.7 and later](../Reference/Self-hosted%20LangSmith%20changelog.md).

Migrating from [None](../../Govern/Users%20%26%20access%20control/Authentication%20methods.md#none) auth mode to basic auth preserves your existing traces, datasets, and other resources. LangSmith replaces the single "default" user with a user created from the basic auth credentials you set up in your [configuration file](#configuration). The pre-existing workspace keeps its ID (`00000000-0000-0000-0000-000000000000`) so existing resources remain bound to it. Aside from the user swap, the resulting migrated installation behaves the same as a fresh basic auth install.

To migrate, apply the basic auth configuration shown in [Configuration](#configuration) and then run `helm upgrade`.

## Configuration

> [!NOTE]
>
> Changing the JWT secret will log out your users.

Enable basic auth by adding the following block to your LangSmith Helm values. On first install, LangSmith uses these values to create the initial Organization Admin user for the `Default` organization:

```yaml Helm
config:
  authType: mixed
  basicAuth:
    enabled: true
    initialOrgAdminEmail: <YOUR EMAIL ADDRESS>
    initialOrgAdminPassword: <PASSWORD> # Must be at least 12 characters long and contain at least one lowercase, uppercase, and symbol
    jwtSecret: <SECRET>
```

Once configured, LangSmith displays a login screen with email and password. Log in with the `initialOrgAdminEmail` and `initialOrgAdminPassword` values, and your user is auto-provisioned with the `Organization Admin` role. For more details, refer to [Organization roles](../../Govern/Organization/Overview.md#organization-roles).
