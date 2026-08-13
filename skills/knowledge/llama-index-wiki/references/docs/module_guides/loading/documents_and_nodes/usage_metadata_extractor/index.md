# developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_metadata_extractor/index.md
> https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_metadata_extractor/index.md

--- title: Metadata Extraction Usage Pattern | Developer Documentation ---
You can use LLMs to automate metadata extraction with our `Metadata Extractor` modules.
Our metadata extractor modules include the following “feature extractors”:
- `SummaryExtractor` - automatically extracts a summary over a set of Nodes - `QuestionsAnsweredExtractor` - extracts a set of questions that each Node can answer - `TitleExtractor` - extracts a title over the context of each Node - `EntityExtractor` - extracts entities (i.e. names of places, people, things) mentioned in the content of each Node

Then you can chain the `Metadata Extractor`s with our node parser:
``` from llama_index.core.extractors import ( TitleExtractor, QuestionsAnsweredExtractor, ) from llama_index.core.node_parser import TokenTextSplitter

text_splitter = TokenTextSplitter( separator=" ", chunk_size=512, chunk_overlap=128 ) title_extractor = TitleExtractor(nodes=5) qa_extractor = QuestionsAnsweredExtractor(questions=3)

# assume documents are defined -> extract nodes from llama_index.core.ingestion import IngestionPipeline
pipeline = IngestionPipeline( transformations=[text_splitter, title_extractor, qa_extractor] )

nodes = pipeline.run( documents=documents, in_place=True, show_progress=True, ) ```

or insert into an index:
``` from llama_index.core import VectorStoreIndex
index = VectorStoreIndex.from_documents( documents, transformations=[text_splitter, title_extractor, qa_extractor] ) ```

## Resources
- SEC Documents Metadata Extraction - LLM Survey Extraction - Entity Extraction - Marvin Metadata Extraction - Pydantic Metadata Extraction