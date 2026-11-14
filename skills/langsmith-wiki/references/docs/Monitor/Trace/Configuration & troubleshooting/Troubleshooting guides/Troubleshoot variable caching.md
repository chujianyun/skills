# Troubleshoot variable caching

If you're not seeing traces in your tracing project or notice traces logged to the wrong project/workspace, the issue might be due to LangSmith's default environment variable caching. This is especially common when running LangSmith within a Jupyter notebook. Follow these steps to diagnose and resolve the issue:

## 1. Verify your environment variables

First, check that the environment variables are set correctly by running:

```python
import os
print(os.getenv("LANGSMITH_PROJECT"))
print(os.getenv("LANGSMITH_TRACING"))
print(os.getenv("LANGSMITH_ENDPOINT"))
print(os.getenv("LANGSMITH_API_KEY"))
```

If the output does not match what's defined in your .env file, it's likely due to environment variable caching.

## 2. Clear the cache

Clear the cached environment variables with the following command:

```python
utils.get_env_var.cache_clear()
```

## 3. Reload the environment variables

Reload your environment variables from the .env file by executing:

```python
from dotenv import load_dotenv
import os
load_dotenv(<path to .env file>, override=True)
```

After reloading, your environment variables should be set correctly.

If you continue to experience issues, please reach out to us via a shared Slack channel or email support (available for Plus and Enterprise plans), or in the [LangChain Forum](https://forum.langchain.com/).
