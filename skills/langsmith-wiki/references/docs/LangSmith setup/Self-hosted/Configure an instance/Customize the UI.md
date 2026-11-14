# Customize the UI

> Customize your LangSmith self-hosted deployment.

Self-hosted LangSmith deployments allow for some UI customization.

## Set a custom logo

For self-hosted deployments, you can replace the LangSmith logo with your own. The logo appears in the navigation sidebar and on error screens, next to the LangSmith wordmark.

Set `config.customLogo` in your Helm values:

```yaml Helm
config:
  customLogo:
    enabled: true
    logoUrl: "https://example.com/logo.svg"
```

`logoUrl` accepts a PNG, JPG, or SVG. Data URIs are rejected.

### Use a different logo for light and dark mode

```yaml Helm
config:
  customLogo:
    enabled: true
    lightModeLogoUrl: "https://example.com/logo-dark-text.svg"
    darkModeLogoUrl: "https://example.com/logo-white-text.svg"
```

Each name refers to the scheme the logo appears in. When you set only one value, LangSmith uses it in both schemes. Requires Helm chart version 0.17.0 or later.

### Serve a logo from a file

Each logo value also accepts a root-relative path, such as `/logos/acme.svg`. Use a path when the browser cannot reach an external host. LangSmith requests the path from its own origin, so the file must exist inside the frontend container.

To mount a logo file:

1. Store the image in a ConfigMap. The filename becomes the last segment of the URL:

   ```bash
   kubectl create configmap langsmith-custom-logo \
     --from-file=acme.svg=./your-logo.svg \
     -n <your-namespace>
   ```

2. Mount the ConfigMap into the frontend pod and point `logoUrl` at the path:

   ```yaml Helm
   config:
     customLogo:
       enabled: true
       logoUrl: "/logos/acme.svg"

   frontend:
     deployment:
       volumes:
         - name: custom-logo
           configMap:
             name: langsmith-custom-logo
       volumeMounts:
         - name: custom-logo
           mountPath: /usr/share/nginx/html/build/logos
           readOnly: true
   ```

3. Upgrade the release, then confirm the file is served:

   ```bash
   curl -sI https://<your-langsmith-host>/logos/acme.svg
   ```

   A `content-type` of `image/svg+xml` confirms the logo is in place. A missing file returns HTTP 200 with the application's HTML rather than a 404, so check the content type and not the status code.

> [!NOTE]
>
> When your values already set `frontend.deployment.volumes` or `frontend.deployment.volumeMounts`, append to those lists. Replacing them removes mounts that other settings depend on.

When you serve LangSmith under a base path, include it in the value: `/<base-path>/logos/acme.svg`. For the full list of Helm values, see [Environment variables](Configure%20environment%20variables%20in%20the%20Helm%20chart.md).

## Set a custom error support message

By default, error messages in LangSmith direct users to the [Support Portal](https://support.langchain.com). You can replace this with your own support contact information.

When set, all error and support messages throughout the UI will display your custom text instead of the default LangChain support email.

> [!NOTE]
>
> The custom message is rendered as **plain text** only. HTML tags will not be interpreted and will display as literal text.

```yaml Helm
config:
  customErrorSupportMessage: "For help, contact your internal IT team at helpdesk@example.com"
```

To revert to the default behavior, remove the setting or set it to an empty string.
