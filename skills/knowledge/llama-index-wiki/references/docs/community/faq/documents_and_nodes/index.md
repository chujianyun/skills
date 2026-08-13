# developers.llamaindex.ai/python/framework/community/faq/documents_and_nodes/index.md
> https://developers.llamaindex.ai/python/framework/community/faq/documents_and_nodes/index.md

--- title: Documents and Nodes | Developer Documentation ---
##### FAQ
1. What is the default `chunk_size` of a Node object? 2. How to add information like name, url in a `Document` object? 3. How to update existing document in an Index?

##### 1. What is the default `chunk_size` of a Node object?
It’s 1024 by default. If you want to customize the `chunk_size`, You can follow Customizing Node

##### 2. How to add information like name, url in a `Document` object?
You can customize the Document object and add extra info in the form of metadata. To know more on this follow Customize Document.

##### 3. How to update existing document in an Index?
You can update/delete existing document in an Index with the help of `doc_id`. You can add new document to an existing Index too. To know more check [Document Management] (/python/framework/module_guides/indexing/document_management/index.md)
---