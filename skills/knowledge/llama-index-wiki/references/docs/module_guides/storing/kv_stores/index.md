# developers.llamaindex.ai/python/framework/module_guides/storing/kv_stores/index.md
> https://developers.llamaindex.ai/python/framework/module_guides/storing/kv_stores/index.md

--- title: Key-Value Stores | Developer Documentation ---
Key-Value stores are the underlying storage abstractions that power our Document Stores and [Index Stores] (/python/framework/module_guides/storing/index_stores/index.md).
We provide the following key-value stores:
- **Simple Key-Value Store**: An in-memory KV store. The user can choose to call `persist` on this kv store to persist data to disk. - **MongoDB Key-Value Store**: A MongoDB KV store. - **Tablestore Key-Value Store**: A Tablestore KV store.
See the API Reference for more details.
Note: At the moment, these storage abstractions are not externally facing.