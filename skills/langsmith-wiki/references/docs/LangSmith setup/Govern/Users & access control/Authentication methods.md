# Authentication methods

LangSmith supports multiple authentication methods for easy sign-up and login.

## Cloud

### Email/Password

Users can use an email address and password to sign up and login to LangSmith.

### Social providers

Users can alternatively use their credentials from GitHub or Google.

### SAML SSO

Enterprise customers can configure [SAML SSO](User%20management.md) and [SCIM](User%20management.md). [Get a demo](https://www.langchain.com/contact-sales) to learn more.

## Self-Hosted

Self-hosted customers have more control over how their users can login to LangSmith. For more in-depth coverage of configuration options, see [the self-hosting docs](../../Self-hosted/Self-hosted%20LangSmith.md) and [Helm chart](https://github.com/langchain-ai/helm/tree/main/charts/langsmith).

### SSO with OAuth 2.0 and OIDC

Production installations should configure SSO in order to use an external identity provider. This enables users to login through an identity platform like Auth0/Okta. LangSmith supports almost any OIDC-compliant provider. Learn more about configuring SSO in the [SSO configuration guide](../../Self-hosted/Platform%20auth%20%26%20access%20control/Set%20up%20SSO%20with%20OAuth2.0%20and%20OIDC.md)

### Email/Password a.k.a. basic auth

This auth method requires very little configuration as it does not require an external identity provider. It is most appropriate to use for self-hosted trials. Learn more in the [basic auth configuration guide](../../Self-hosted/Platform%20auth%20%26%20access%20control/Basic%20authentication%20with%20email%20and%20password.md)

### None

> [!WARNING]
>
> This authentication mode will be removed after the launch of Basic Auth.

If zero authentication methods are enabled, a self-hosted installation does not require any login/sign-up. This configuration should only be used for verifying installation at the infrastructure level, as the feature set supported in this mode is restricted with only a single organization and workspace.
