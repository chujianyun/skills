# developers.llamaindex.ai/python/framework/integrations/embeddings/openvino/index.md
> https://developers.llamaindex.ai/python/framework/integrations/embeddings/openvino/index.md

--- title: Local Embeddings with OpenVINO | Developer Documentation ---

OpenVINO™ [1] is an open-source toolkit for optimizing and deploying AI inference. The OpenVINO™ Runtime supports various hardware [devices] [2] including x86 and ARM CPUs, and Intel GPUs. It can help to boost deep learning performance in Computer Vision, Automatic Speech Recognition, Natural Language Processing and other common tasks.

Hugging Face embedding model can be supported by OpenVINO through `OpenVINOEmbedding` or `OpenVINOGENAIEmbedding`class, and OpenClip model can be through `OpenVINOClipEmbedding` class.

If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-embeddings-openvino ```
``` !pip install llama-index ```
## Model Exporter
It is possible to export your model to the OpenVINO IR format with `create_and_save_openvino_model` function, and load the model from local folder.
``` from llama_index.embeddings.huggingface_openvino import OpenVINOEmbedding
OpenVINOEmbedding.create_and_save_openvino_model( "BAAI/bge-small-en-v1.5", "./bge_ov" ) ```

``` /home2/ethan/intel/llama_index/llama_test/lib/python3.10/site-packages/openvino/runtime/__init__.py:10: DeprecationWarning: The `openvino.runtime` module is deprecated and will be removed in the 2026.0 release. Please replace `openvino.runtime` with `openvino`. warnings.warn(

Saved OpenVINO model to ./bge_ov. Use it with `embed_model = OpenVINOEmbedding(model_id_or_path='./bge_ov')`. ```
## Model Loading
If you have an Intel GPU, you can specify `device="gpu"` to run inference on it.
``` ov_embed_model = OpenVINOEmbedding(model_id_or_path="./bge_ov", device="cpu") ```

## Model Loading with OpenVINO GenAI
To avoid the dependencies of PyTorch in runtime, you can load your local embedding model with `OpenVINOGENAIEmbedding`class.
``` %pip install llama-index-embeddings-openvino-genai ```
``` from llama_index.embeddings.openvino_genai import OpenVINOGENAIEmbedding
ov_embed_model = OpenVINOGENAIEmbedding(model_path="./bge_ov", device="CPU") ```

``` /home2/ethan/intel/llama_index/llama_test/lib/python3.10/site-packages/openvino/runtime/__init__.py:10: DeprecationWarning: The `openvino.runtime` module is deprecated and will be removed in the 2026.0 release. Please replace `openvino.runtime` with `openvino`. warnings.warn( ```

``` embeddings = ov_embed_model.get_text_embedding("Hello World!") print(len(embeddings)) print(embeddings[:5]) ```

``` 384 [-0.0030246784444898367, -0.012189766392111778, 0.04163273051381111, -0.037758368998765945, 0.02439723163843155] ```

## OpenClip Model Exporter
Class `OpenVINOClipEmbedding` can support exporting and loading open\_clip models with OpenVINO runtime.
``` %pip install open_clip_torch ```
``` from llama_index.embeddings.huggingface_openvino import ( OpenVINOClipEmbedding, )

OpenVINOClipEmbedding.create_and_save_openvino_model( "laion/CLIP-ViT-B-32-laion2B-s34B-b79K", "ViT-B-32-ov", ) ```

## MultiModal Model Loading
If you have an Intel GPU, you can specify `device="GPU"` to run inference on it.
``` ov_clip_model = OpenVINOClipEmbedding( model_id_or_path="./ViT-B-32-ov", device="CPU" ) ```

## Embed images and queries with OpenVINO
``` from PIL import Image import requests from numpy import dot from numpy.linalg import norm

image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStMP8S3VbNCqOQd7QQQcbvC_FLa1HlftCiJw&s" im = Image.open(requests.get(image_url, stream=True).raw) print("Image:") display(im)

im.save("logo.jpg") image_embeddings = ov_clip_model.get_image_embedding("logo.jpg") print("Image dim:", len(image_embeddings)) print("Image embed:", image_embeddings[:5])

text_embeddings = ov_clip_model.get_text_embedding( "Logo of a pink blue llama on dark background" ) print("Text dim:", len(text_embeddings)) print("Text embed:", text_embeddings[:5])

cos_sim = dot(image_embeddings, text_embeddings) / ( norm(image_embeddings) * norm(text_embeddings) ) print("Cosine similarity:", cos_sim) ```

``` Image: ```
png
``` Image dim: 512 Image embed: [-0.03019799292087555, -0.09727513045072556, -0.6659489274024963, -0.025658488273620605, 0.05379948765039444] Text dim: 512 Text embed: [-0.15816599130630493, -0.25564345717430115, 0.22376027703285217, -0.34983670711517334, 0.31968361139297485] Cosine similarity: 0.27307014923203976 ```

For more information refer to:
- OpenVINO LLM guide [3].
- OpenVINO Documentation [4].
- OpenVINO Get Started Guide [5].
- RAG example with LlamaIndex [6].

[1] https://github.com/openvinotoolkit/openvino
[2] https://github.com/openvinotoolkit/openvino?tab=readme-ov-file#supported-hardware-matrix
[3] https://docs.openvino.ai/2024/learn-openvino/llm_inference_guide.html
[4] https://docs.openvino.ai/2024/home.html
[5] https://www.intel.com/content/www/us/en/content-details/819067/openvino-get-started-guide.html
[6] https://github.com/openvinotoolkit/openvino_notebooks/tree/latest/notebooks/llm-rag-llamaindex