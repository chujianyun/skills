# LangSmith API reference

> The LangSmith REST API provides programmatic access to tracing, datasets, experiments, annotations, and other LangSmith platform features.

The LangSmith REST API provides programmatic access to LangSmith platform features including tracing, datasets, experiments, annotations, and more.

Browse the full API reference in the **LangSmith REST API** section in the sidebar.

## Authentication

Pass the `X-Api-Key` header with each request. The value should be a valid [LangSmith API key](../../../LangSmith%20setup/Account/Create%20an%20account%20and%20API%20key.md).

```shell
curl --request GET \
  --url https://api.smith.langchain.com/api/v1/workspaces \
  --header 'X-Api-Key: LANGSMITH_API_KEY'
```
