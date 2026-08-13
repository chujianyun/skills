# developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/heroku/index.md

--- title: Heroku LLM Managed Inference Embedding | Developer Documentation ---

The `llama-index-embeddings-heroku` package contains LlamaIndex integrations for building applications with embeddings models on Heroku’s Managed Inference platform. This integration allows you to easily connect to and use AI models deployed on Heroku’s infrastructure.

## Installation
``` %pip install llama-index-embeddings-heroku ```
## Setup
### 1. Create a Heroku App
First, create an app in Heroku:

``` heroku create $APP_NAME ```
### 2. Create and Attach AI Models
Create and attach a chat model to your app:

``` heroku ai:models:create -a $APP_NAME cohere-embed-multilingual --as EMBEDDING ```
### 3. Export Configuration Variables
Export the required configuration variables:
Terminal window
``` export EMBEDDING_KEY=$(heroku config:get EMBEDDING_KEY -a $APP_NAME) export EMBEDDING_MODEL_ID=$(heroku config:get EMBEDDING_MODEL_ID -a $APP_NAME) export EMBEDDING_URL=$(heroku config:get EMBEDDING_URL -a $APP_NAME) ```

## Usage
### Basic Usage
``` # Initialize the Heroku LLM from llama_index.embeddings.heroku import HerokuEmbedding

# Initialize the Heroku Embedding embedding_model = HerokuEmbedding()

# Get a single embedding embedding = embedding_model.get_text_embedding("Hello, world!") print(f"Embedding dimension: {len(embedding)}")

# Get embeddings for multiple texts texts = ["Hello", "world", "from", "Heroku"] embeddings = embedding_model.get_text_embedding_batch(texts) print(f"Number of embeddings: {len(embeddings)}") ```

### Using Environment Variables
The integration automatically reads from environment variables:
``` import os

# Set environment variables os.environ["EMBEDDING_KEY"] = "your-embedding-key" os.environ["EMBEDDING_URL"] = "https://us.inference.heroku.com" os.environ["EMBEDDING_MODEL_ID"] = "claude-3-5-haiku"

# Initialize without parameters llm = HerokuEmbedding() ```
### Using Parameters
You can also pass parameters directly:
``` import os from llama_index.embeddings.heroku import HerokuEmbedding

embedding_model = HerokuEmbedding( model=os.getenv("EMBEDDING_MODEL_ID", "cohere-embed-multilingual"), api_key=os.getenv("EMBEDDING_KEY", "your-embedding-key"), base_url=os.getenv("EMBEDDING_URL", "https://us.inference.heroku.com"), timeout=60.0, )

print(embedding_model.get_text_embedding("Hello Heroku!")) ```
## Available Models

For a complete list of available models, see the Heroku Managed Inference documentation [1].

## Error Handling
The integration includes proper error handling for common issues:
- Missing API key - Invalid inference URL - Missing model configuration
## Additional Information
For more information about Heroku Managed Inference, visit the official documentation [2].

[1] https://devcenter.heroku.com/articles/heroku-inference#available-models
[2] https://devcenter.heroku.com/articles/heroku-inference