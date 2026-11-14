# Route self-hosted Sandbox egress through a forward proxy

> Send outbound connections from self-hosted LangSmith Sandboxes through a corporate HTTP or HTTPS forward proxy, with a bypass list, Basic proxy authentication, and custom CA trust.

A self-hosted `sandbox-host` can send every outbound connection from Sandboxes through your corporate forward proxy instead of dialing destinations directly. Use this when your network allows outbound traffic only through a proxy, or when your security team needs all Sandbox traffic to pass a proxy's access policy and logging.

For how Sandbox traffic leaves a microVM, see [Sandbox architecture](Self-hosted%20Sandbox%20architecture.md). For installation, see [Enable Sandboxes](Enable%20Sandboxes%20on%20self-hosted%20LangSmith.md).

## Understand how proxied egress works

Each outbound TCP connection from a Sandbox reaches the [Sandbox auth proxy](../../../../../Deploy/Sandboxes/Sandbox%20auth%20proxy.md) on its host first. The host applies the Sandbox's allow and deny lists and auth proxy rules, then sends the traffic to your forward proxy the way a client configured with `HTTP_PROXY` and `HTTPS_PROXY` does:

* **Plain HTTP**: Sent as standard proxy requests, such as `GET http://example.com/path`. HTTP to an allow-listed IP address is the exception: it goes through a `CONNECT` tunnel to port 80, so the host checks the address the Sandbox connected to rather than its `Host` header.
* **HTTPS and other TCP**: Sent through `CONNECT` tunnels to the destination host and port, such as `CONNECT example.com:443` or `CONNECT github.com:22`.

The host also applies these rules:

* **No direct fallback**: When the forward proxy rejects a request or cannot open a tunnel, the request or connection fails. The host never retries it directly.
* **Bypass list**: The host dials destinations in `noProxy` directly, with the same Sandbox access checks.
* **LangSmith API**: The host dials HTTPS requests from a Sandbox to your LangSmith installation's API directly, not through the forward proxy.

Proxying happens on the host, outside the Sandbox. Code inside a Sandbox does not see the forward proxy address and does not need `HTTP_PROXY` or `HTTPS_PROXY` set.

## Check the requirements

Proxied egress requires:

* LangSmith 0.17.32 or later on the 0.17 release line, or 0.18.5rc1 or later on the 0.18 line, for the `sandbox-host` image.
* LangSmith Helm chart 0.17.10 or later on the 0.17 release line, or 0.18.0-rc.21 or later on the 0.18 line, for `sandboxes.authProxy.httpProxy.url`. Earlier charts configure the proxy with `enabled`, `scheme`, `host`, and `port` instead and cannot pass credentials.
* A forward proxy that accepts standard HTTP proxy requests and `CONNECT` to port 443. To reach other TCP services, such as Git over SSH on port 22, or HTTP on an allow-listed IP address, the proxy must also accept `CONNECT` to those ports.
* Network reachability from the Sandbox node pool to the proxy. The proxy address can be a private IP address or, on LangSmith 0.17.36 or later, an in-cluster Kubernetes Service name such as `squid.proxy.svc.cluster.local`.

The forward proxy can require Basic authentication, which needs LangSmith 0.17.37 or later on the 0.17 release line, or 0.18.11rc1 or later on the 0.18 line. `sandbox-host` does not support NTLM, Negotiate (Kerberos), or Digest proxy authentication, or client certificates (mTLS). An HTTPS proxy works when the host only needs to trust its server certificate.

## Configure the proxy

> [!NOTE]
>
> When Sandboxes run in a [separate cluster](Run%20self-hosted%20Sandboxes%20in%20a%20separate%20cluster.md), configure the proxy in the `langsmith-sandbox` chart instead: add the URL to its Secret under the key `sandbox_egress_proxy_url`, set `authProxy.httpProxy.noProxy`, and add a private CA to `config.customCa`. With an external runtime, the `langsmith` chart fails to render `sandboxes.authProxy.httpProxy`.

To route Sandbox egress through a forward proxy:

**1. Add the proxy settings to your values**

Set `sandboxes.authProxy.httpProxy` in your LangSmith Helm values:

```yaml
sandboxes:
  authProxy:
    httpProxy:
      url: http://proxy.corp.internal:3128
      noProxy:
        - .corp.internal
```

* **`url`**: The proxy URL, `http://host:port`, or `https://host:port` when the connection to the proxy itself uses TLS. The host can be a hostname, an IP address, or an in-cluster Service name. Leave it empty to send egress directly. The chart stores the URL in the LangSmith app Secret, because it can carry credentials (see the next step). When you set `config.existingSecretName`, leave `url` empty and add the URL to that Secret under the key `sandbox_egress_proxy_url` instead.
* **`noProxy`**: Destinations that the host dials directly instead of through the proxy, with the same matching as the `NO_PROXY` environment variable. An entry such as `corp.internal` matches that host and its subdomains, an entry with a leading dot such as `.corp.internal` matches only subdomains, and `*` matches every host. Entries can also be IP addresses, CIDR ranges such as `10.0.0.0/8`, or `host:port` pairs.

The chart fails the render when `url` is not an `http://` or `https://` URL without a path, or when you set `url` together with `config.existingSecretName` or `config.disableSecretCreation`. On LangSmith 0.17.36 or later, `sandbox-host` also checks the proxy address when it starts: a loopback or cloud metadata address stops the pod with `sandbox host config invalid` instead of failing each Sandbox creation.

**2. (Optional) Authenticate to the proxy**

When the proxy requires a username and password, add them to the URL:

```text
http://svc-sandboxes:p%40ssw0rd@proxy.corp.internal:3128
```

Percent-encode reserved characters in the username and password, such as `@` as `%40`, `:` as `%3A`, and `/` as `%2F`. Set the URL as `url` in your values, or as the `sandbox_egress_proxy_url` key in `config.existingSecretName`.

`sandbox-host` sends the credentials to the proxy as a Basic `Proxy-Authorization` header on every `CONNECT` and plain HTTP proxy request. Sandboxes never see them: the host opens the tunnels, and it drops any `Proxy-Authorization` header that code in a Sandbox sends. Basic credentials are not encrypted, so use an `https` proxy URL when the network between the Sandbox nodes and the proxy is not trusted.

When the proxy rejects the credentials, connections from Sandboxes fail and the `sandbox-host` logs show `upstream proxy CONNECT rejected: 407`. After you rotate the password, update the Secret and restart the `sandbox-host` Deployment; it reads the URL only when it starts.

**3. (Optional) Trust a private CA for an HTTPS proxy**

When the proxy URL uses `https` and a private CA issues the proxy's certificate, add that CA to the bundle in `config.customCa`. The `sandbox-host` pods trust the same bundle as other LangSmith services, in addition to the system roots. See [Mount internal CAs for TLS](../../../Platform%20auth%20%26%20access%20control/Configure%20custom%20TLS%20certificates.md#mount-internal-cas-for-tls).

**4. Apply the change**

Upgrade the Helm release. Changing these settings rolls the `sandbox-host` Deployment, so each host drains its running Sandboxes before it restarts. See [Understand a rolling upgrade](Operate%20self-hosted%20Sandboxes.md#understand-a-rolling-upgrade).

**5. Verify egress**

Create a Sandbox and request a public URL from inside it:

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://www.langchain.com/
```

The command prints `200`, and your forward proxy logs a `CONNECT www.langchain.com:443` request from a Sandbox node. A request to an `http://` URL appears in the proxy log as a `GET http://...` request instead.

## Reach private services directly

By default, `sandbox-host` refuses to connect to private addresses, so a Sandbox cannot reach an internal service even when `noProxy` sends the connection direct. On a self-hosted installation, a Sandbox reaches a private address when its `allow_list` lets that destination through: a hostname, a glob such as `*.corp.internal`, or a regular expression. A literal IP address needs an IP or CIDR entry. Sandboxes with a `deny_list` or no `access_control` never reach private addresses. See [Allow and deny lists](../../../../../Deploy/Sandboxes/Sandbox%20auth%20proxy.md#allow-and-deny-lists).

For example, a Sandbox that needs Git and a database on the internal network, plus public HTTP and HTTPS through the forward proxy, uses this `proxy_config`:

```json
{
  "access_control": {
    "allow_list": ["*:80", "*:443", "git.corp.internal", "db.corp.internal:5432"]
  }
}
```

The host checks the address it connects to after resolving the hostname. Loopback and cloud metadata addresses stay blocked even when listed. This needs no Helm setting.

A Sandbox can also reach a Service in your cluster by its Kubernetes name, such as `api.team.svc.cluster.local`, when its `allow_list` names it. Your forward proxy cannot resolve cluster names, so add `.svc.cluster.local` to `noProxy` when you use one.

> [!WARNING]
>
> Every matching entry counts, including `*` and `*:443`. On a self-hosted installation, an `allow_list` such as `["*:80", "*:443"]` also opens private destinations on those ports. Anyone who can create or update a Sandbox can allow-list a private address, including addresses inside your cluster, so limit who can create Sandboxes accordingly.

## Secure the proxy

The forward proxy, not the host, resolves the destination hostname. The host checks hostnames against the Sandbox access lists and, by default, blocks literal private, loopback, and cloud metadata IP addresses, but it cannot see the address the proxy resolves a hostname to. A Sandbox that requests a hostname resolving to an internal address reaches that address if the proxy allows it.

Configure the proxy's access policy to block the destinations Sandboxes must not reach, such as internal networks and cloud metadata endpoints.

## Understand the limitations

* **Private services need connectivity**: A forward proxy reaches only the destinations the proxy itself can reach. It does not provide VPN or network peering to private services.
* **TLS-inspecting proxies**: When the proxy decrypts and re-encrypts HTTPS inside the tunnel, the client sees a certificate from your inspection CA. For hosts that auth proxy rules match, `sandbox-host` is that client, so add the CA to `config.customCa`. For other hosts, programs in the Sandbox are the client, so add the CA to the Sandbox image's trust store. Alternatively, exempt Sandbox traffic from inspection.

## See also

* [Sandbox auth proxy](../../../../../Deploy/Sandboxes/Sandbox%20auth%20proxy.md)
* [Sandbox architecture](Self-hosted%20Sandbox%20architecture.md)
* [Upgrades and operations](Operate%20self-hosted%20Sandboxes.md)
* [Configure custom TLS certificates](../../../Platform%20auth%20%26%20access%20control/Configure%20custom%20TLS%20certificates.md)
