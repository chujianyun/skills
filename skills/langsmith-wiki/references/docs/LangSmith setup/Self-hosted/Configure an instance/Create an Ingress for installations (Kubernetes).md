# Create an Ingress for installations (Kubernetes)

By default, LangSmith will provision a LoadBalancer service for the `langsmith-frontend`. Depending on your cloud provider, this may result in a public IP address being assigned to the service. If you would like to use a custom domain or have more control over the routing of traffic to your LangSmith installation, you can configure an Ingress, Gateway API, or Istio Gateway.

## Requirements

* An existing Kubernetes cluster
* One of the following installed in your Kubernetes cluster:
  * An Ingress Controller (for standard Ingress)
  * Gateway API CRDs and a Gateway resource (for Gateway API)
  * Istio (for Istio Gateway)

## Parameters

You may need to provide certain parameters to your LangSmith installation to configure the Ingress. Additionally, we will want to convert the `langsmith-frontend` service to a ClusterIP service.

* *Hostname (optional)*: The hostname that you would like to use for your LangSmith installation. E.g `"langsmith.example.com"`. If you leave this empty, the ingress will serve all traffic to the LangSmith installation.

* *BasePath (optional)*: If you would like to serve LangSmith under a URL basePath, you can specify it here. For example, adding `"langsmith"` will serve the application at `"example.hostname.com/langsmith"`. This will apply to UI paths as well as API endpoints.

* *IngressClassName (optional)*: The name of the Ingress class that you would like to use. If not set, the default Ingress class will be used.

* *Annotations (optional)*: Additional annotations to add to the Ingress. Certain providers like AWS may use annotations to control things like TLS termination.

  For example, you can add the following annotations using the AWS ALB Ingress Controller to attach an ACM certificate to the Ingress:

  ```yaml
  annotations:
    alb.ingress.kubernetes.io/certificate-arn: "<your-certificate-arn>"
  ```

* *Labels (optional)*: Additional labels to add to the Ingress.

* *TLS (optional)*: If you would like to serve LangSmith over HTTPS, you can add TLS configuration here (many Ingress controllers may have other ways of controlling TLS so this is often not needed). This should be an array of TLS configurations. Each TLS configuration should have the following fields:

  * hosts: An array of hosts that the certificate should be valid for. E.g \["langsmith.example.com"]

  * secretName: The name of the Kubernetes secret that contains the certificate and private key. This secret should have the following keys:

    * tls.crt: The certificate
    * tls.key: The private key

  * For more information, see [creating a TLS secret](https://kubernetes.io/docs/concepts/services-networking/ingress/#tls).

## Configuration

You can configure your LangSmith instance to use one of three routing options: standard Ingress, Gateway API, or Istio Gateway. Choose the option that best fits your infrastructure.

### Option 1: Standard ingress

With these parameters in hand, you can configure your LangSmith instance to use an Ingress. You can do this by modifying the `config.yaml` file for your LangSmith Helm Chart installation.

```yaml
config:
  hostname: "" # Main domain for LangSmith
  basePath: "" # If you want to serve langsmith under a URL base path (e.g., /langsmith)
ingress:
  enabled: true
  hostname: "" # Deprecated: Use config.hostname instead after v0.12.0
  subdomain: "" # Deprecated: Use config.hostname instead after v0.12.0
  ingressClassName: "" # If not set, the default ingress class will be used
  annotations: {} # Add annotations here if needed
  labels: {} # Add labels here if needed
  tls: [] # Add TLS configuration here if needed
frontend:
  service:
    type: ClusterIP
```

Once configured, you will need to update your LangSmith installation. If everything is configured correctly, your LangSmith instance should now be accessible via the Ingress. You can run the following to check the status of your Ingress:

```bash
kubectl get ingress
```

You should see something like this in the output:

```
NAME                         CLASS   HOSTS    ADDRESS          PORTS     AGE
langsmith-ingress            nginx   <host>   35.227.243.203   80, 443   95d
```

> [!WARNING]
>
> If you do not have automated DNS setup, you will need to add the IP address to your DNS provider manually.

### Option 2: Gateway API

> [!NOTE]
>
> Gateway API support is available as of LangSmith v0.12.0

If your cluster uses the [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/), you can configure LangSmith to provision HTTPRoute resources. This will create an HTTPRoute for LangSmith and an HTTPRoute for each [agent deployment](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md).

#### Parameters

* *name (required)*: The name of the Gateway resource to reference
* *namespace (required)*: The namespace where the Gateway resource is located
* *hostname (optional)*: The hostname that you would like to use for your LangSmith installation. E.g `"langsmith.example.com"`
* *basePath (optional)*: If you would like to serve LangSmith under a base path, you can specify it here. E.g "example.com/langsmith"
* *sectionName (optional)*: The name of a specific listener section in the Gateway to use
* *annotations (optional)*: Additional annotations to add to the HTTPRoute resources
* *labels (optional)*: Additional labels to add to the HTTPRoute resources

#### Configuration

```yaml
config:
  hostname: "" # Main domain for LangSmith
  basePath: "" # If you want to serve langsmith under a base path. E.g "example.com/langsmith"
gateway:
  enabled: true
  name: "my-gateway" # Name of your Gateway resource
  namespace: "gateway-system" # Namespace of your Gateway resource
  sectionName: "" # Optional: specific listener section name
  annotations: {} # Add annotations here if needed
  labels: {} # Add labels here if needed
frontend:
  service:
    type: ClusterIP
```

Once configured, you can check the status of your HTTPRoutes:

```bash
kubectl get httproute
```

### Option 3: Istio Gateway

> [!NOTE]
>
> Istio Gateway support is available as of LangSmith v0.12.0

If your cluster uses [Istio](https://istio.io/), you can configure LangSmith to provision VirtualService resources. This will create a VirtualService for LangSmith and a VirtualService for each [agent deployment](../../../Deploy/Get%20started/LangSmith%20Agent%20Server.md).

#### Parameters

* *name (optional)*: The name of the Istio Gateway resource to reference. Defaults to `"istio-gateway"`
* *namespace (optional)*: The namespace where the Istio Gateway resource is located. Defaults to `"istio-system"`
* *hostname (optional)*: The hostname that you would like to use for your LangSmith installation. E.g `"langsmith.example.com"`
* *basePath (optional)*: If you would like to serve LangSmith under a base path, you can specify it here. E.g "example.com/langsmith"
* *annotations (optional)*: Additional annotations to add to the VirtualService resources
* *labels (optional)*: Additional labels to add to the VirtualService resources

#### Configuration

```yaml
config:
  hostname: "" # Main domain for LangSmith
  basePath: "" # If you want to serve langsmith on a separate basePath. E.g "example.com/langsmith"
istioGateway:
  enabled: true
  name: "istio-gateway" # Name of your Istio Gateway resource
  namespace: "istio-system" # Namespace of your Istio Gateway resource
  annotations: {} # Add annotations here if needed
  labels: {} # Add labels here if needed
frontend:
  service:
    type: ClusterIP
```

Once configured, you can check the status of your VirtualServices:

```bash
kubectl get virtualservice
```
