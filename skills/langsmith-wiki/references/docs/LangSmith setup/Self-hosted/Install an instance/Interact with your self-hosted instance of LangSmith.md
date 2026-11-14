# Interact with your self-hosted instance of LangSmith

This guide will walk you through the process of using your self-hosted instance of LangSmith.

> [!NOTE]
>
> This guide assumes you have already deployed a self-hosted LangSmith instance. If you have not, please refer to the [kubernetes deployment guide](Self-host%20LangSmith%20on%20Kubernetes.md).

### Configuring the application you want to use with LangSmith

LangSmith has a single API for interacting with both the hub and the LangSmith backend.

1. Once you have deployed your instance, you can access the LangSmith UI at `http(s)://<host>`.
2. The LangSmith API will be available at `http(s)://<host>/api/v1`
3. The LangSmith Control Plane will be available at `http(s)://<host>/api-host`

To use the API of your instance, you will need to set the following environment variables in your application:

```bash
LANGSMITH_ENDPOINT=http://<host>/api/v1
LANGSMITH_API_KEY=foo # Set to a legitimate API key if using OAuth
```

You can also configure these variables directly in the LangSmith SDK client:

```python
import langsmith
langsmith_client = langsmith.Client(
    api_key='<api_key>',
    api_url='http(s)://<host>/api/v1',
)
```

After setting the above, you should be able to run your code and see the results in your self-hosted instance. We recommend running through the [*quickstart guide*](../../../Monitor/Trace/Tracing%20quickstart.md) to get a feel for how to use LangSmith.

### Self-Signed certificates

If you are using self-signed certificates for your self-hosted LangSmith instance, this can be problematic as Python comes with its own set of trusted certificates, which may not include your self-signed certificate. To resolve this, you may need to use something like `truststore` to load system certificates into your Python environment.

You can do this like so:

1. pip install truststore (or similar depending on the package manager you are using)

Then use the following code to load the system certificates:

```python
import truststore
truststore.inject_into_ssl()
# The rest of your code
import langsmith
langsmith_client = langsmith.Client(
    api_key='<api_key>',
    api_url='http(s)://<host>/api/v1',
)
```

***

## API reference

To access the API reference, navigate to `http://<host>/api/docs` in your browser.
