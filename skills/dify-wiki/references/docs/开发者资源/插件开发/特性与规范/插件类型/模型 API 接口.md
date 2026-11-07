# 模型 API 接口

> 实现 Dify 模型插件所需的接口和数据结构，涵盖 LLM、TextEmbedding、Rerank、Speech2Text、Text2Speech 和 Moderation 模型

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/develop-plugin/features-and-specs/plugin-types/model-schema.md)。

## 简介

本文档是通过模型插件将 AI 模型集成到 Dify 时所需实现的接口和数据结构的技术参考。

> [!NOTE]
>
> 在深入阅读本 API 参考之前，建议先阅读 [模型设计规则](%E6%A8%A1%E5%9E%8B%E8%A7%84%E8%8C%83.md) 了解概念模型，并参考 [创建新模型供应商](../../%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97%E4%B8%8E%E7%A4%BA%E4%BE%8B/%E6%8C%89%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E6%A8%A1%E5%9E%8B%E4%BE%9B%E5%BA%94%E5%95%86%E6%8F%92%E4%BB%B6.md) 获取分步演示。

### 快速决策：我需要实现哪个方法？

| 如果你的模型是…… | 实现 |
| :- | :- |
| 对话/续写 LLM | `LargeLanguageModel._invoke`、`_get_num_tokens` |
| 嵌入模型 | `TextEmbeddingModel._invoke`、`_get_num_tokens` |
| 重排序模型 | `RerankModel._invoke` |
| 语音转文字 | `Speech2TextModel._invoke` |
| 文字转语音 | `Text2SpeechModel._invoke` |
| 内容审核 | `ModerationModel._invoke` |

此外，每个供应商都要实现 `validate_provider_credentials`（供应商级鉴权）；如果模型支持用户自行配置，还需为每种模型类型实现 `validate_credentials`。

> [card] [供应商实现](%E6%A8%A1%E5%9E%8B%20API%20%E6%8E%A5%E5%8F%A3.md#模型供应商)
>
> 了解如何为不同的 AI 服务供应商实现模型供应商类

> [card] [模型类型](%E6%A8%A1%E5%9E%8B%20API%20%E6%8E%A5%E5%8F%A3.md#模型)
>
> 五种受支持模型类型的实现细节：LLM、Embedding、Rerank、Speech2Text 和 Text2Speech

> [card] [数据结构](%E6%A8%A1%E5%9E%8B%20API%20%E6%8E%A5%E5%8F%A3.md#实体)
>
> 模型 API 中所用全部数据结构的完整参考

> [card] [错误处理](%E6%A8%A1%E5%9E%8B%20API%20%E6%8E%A5%E5%8F%A3.md#通用接口)
>
> 错误映射与异常处理的规范指南

## 模型供应商

每个模型供应商都必须继承 `__base.model_provider.ModelProvider` 基类，并实现凭据验证接口。

### 供应商凭据验证

```python Core Implementation theme={null}
def validate_provider_credentials(self, credentials: dict) -> None:
    """
    Validate provider credentials by making a test API call

    Parameters:
        credentials: Provider credentials as defined in `provider_credential_schema`

    Raises:
        CredentialsValidateFailedError: If validation fails
    """
    try:
        # Example implementation: validate using an LLM model instance
        model_instance = self.get_model_instance(ModelType.LLM)
        model_instance.validate_credentials(
            model="example-model",
            credentials=credentials
        )
    except Exception as ex:
        logger.exception(f"Credential validation failed")
        raise CredentialsValidateFailedError(f"Invalid credentials: {str(ex)}")
```

```python Custom Model Provider theme={null}
class XinferenceProvider(Provider):
    def validate_provider_credentials(self, credentials: dict) -> None:
        """
        For custom-only model providers, a simple implementation is sufficient
        as validation happens at the model level
        """
        pass
```

**credentials** `dict`

在供应商 YAML 配置中 `provider_credential_schema` 下定义的凭据信息，通常为 `api_key`、`organization_id` 等字段。

> [!WARNING]
>
> 验证失败时，你的实现必须抛出 `CredentialsValidateFailedError` 异常，以确保在 Dify UI 中正确处理错误。

> [!TIP]
>
> 对于预定义模型供应商，应实现完整的验证方法，对照你的 API 校验凭据。对于自定义模型供应商（每个模型各有自己的凭据），简化的实现即可。

## 模型

Dify 支持五种不同的模型类型，每种都有各自的接口。所有模型类型都共享以下通用要求。

### 通用接口

无论类型如何，每个模型实现都必须实现以下两个基础方法：

#### 1. 模型凭据验证

```python Implementation theme={null}
def validate_credentials(self, model: str, credentials: dict) -> None:
    """
    Validate that the provided credentials work with the specified model

    Parameters:
        model: The specific model identifier (e.g., "gpt-4")
        credentials: Authentication details for the model

    Raises:
        CredentialsValidateFailedError: If validation fails
    """
    try:
        # Make a lightweight API call to verify credentials
        # Example: List available models or check account status
        response = self._api_client.validate_api_key(credentials["api_key"])

        # Verify the specific model is available if applicable
        if model not in response.get("available_models", []):
            raise CredentialsValidateFailedError(f"Model {model} is not available")

    except ApiException as e:
        raise CredentialsValidateFailedError(str(e))
```

**model** `string` *required*

要验证的具体模型标识符（例如 "gpt-4"、"claude-3-opus"）

**credentials** `dict` *required*

在供应商配置中定义的凭据信息

#### 2. 错误映射

```python Implementation theme={null}
@property
def _invoke_error_mapping(self) -> dict[type[InvokeError], list[type[Exception]]]:
    """
    Map provider-specific exceptions to standardized Dify error types

    Returns:
        Dictionary mapping Dify error types to lists of provider exception types
    """
    return {
        InvokeConnectionError: [
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            ConnectionRefusedError
        ],
        InvokeServerUnavailableError: [
            ServiceUnavailableError,
            HTTPStatusError
        ],
        InvokeRateLimitError: [
            RateLimitExceededError,
            QuotaExceededError
        ],
        InvokeAuthorizationError: [
            AuthenticationError,
            InvalidAPIKeyError,
            PermissionDeniedError
        ],
        InvokeBadRequestError: [
            InvalidRequestError,
            ValidationError
        ]
    }
```

> [accordion] 可用的错误类型
>
> **InvokeConnectionError** `class`
>
> 网络连接失败、超时
>
> **InvokeServerUnavailableError** `class`
>
> 服务供应商宕机或不可用
>
> **InvokeRateLimitError** `class`
>
> 达到速率限制或配额限制
>
> **InvokeAuthorizationError** `class`
>
> 认证或权限问题
>
> **InvokeBadRequestError** `class`
>
> 无效的参数或请求

> [!TIP]
>
> 你也可以在代码中直接抛出这些标准化错误类型，而不依赖错误映射。这种方式让你对错误消息有更多控制。

### LLM 实现

要实现大语言模型供应商，请继承 `__base.large_language_model.LargeLanguageModel` 基类，并实现以下方法：

#### 1. 模型调用

这个核心方法同时处理对语言模型的流式和非流式 API 调用。

```python Core Implementation theme={null}
def _invoke(
    self,
    model: str,
    credentials: dict,
    prompt_messages: list[PromptMessage],
    model_parameters: dict,
    tools: Optional[list[PromptMessageTool]] = None,
    stop: Optional[list[str]] = None,
    stream: bool = True,
    user: Optional[str] = None
) -> Union[LLMResult, Generator[LLMResultChunk, None, None]]:
    """
    Invoke the language model
    """
    # Prepare API parameters
    api_params = self._prepare_api_parameters(
        model,
        credentials,
        prompt_messages,
        model_parameters,
        tools,
        stop
    )

    try:
        # Choose between streaming and non-streaming implementation
        if stream:
            return self._invoke_stream(model, api_params, user)
        else:
            return self._invoke_sync(model, api_params, user)

    except Exception as e:
        # Map errors using the error mapping property
        self._handle_api_error(e)

# Helper methods for streaming and non-streaming calls
def _invoke_stream(self, model, api_params, user):
    # Implement streaming call and yield chunks
    pass

def _invoke_sync(self, model, api_params, user):
    # Implement synchronous call and return complete result
    pass
```

> [accordion] 参数
>
> **model** `string` *required*
>
> 模型标识符（例如 "gpt-4"、"claude-3"）
>
> **credentials** `dict` *required*
>
> API 的认证凭据
>
> **prompt\_messages** `list[PromptMessage]` *required*
>
> Dify 标准格式的消息列表：
>
> * 对于 `completion` 模型：包含单个 `UserPromptMessage`。
> * 对于 `chat` 模型：按需包含 `SystemPromptMessage`、`UserPromptMessage`、`AssistantPromptMessage` 和 `ToolPromptMessage`。
>
> **model\_parameters** `dict` *required*
>
> 在模型 YAML 配置中定义的模型专属参数（temperature、top\_p 等）
>
> **tools** `list[PromptMessageTool]`
>
> 用于函数调用能力的工具定义
>
> **stop** `list[string]`
>
> 遇到时会终止模型生成的停止序列
>
> **stream** `boolean` (default: true)
>
> 是否返回流式响应
>
> **user** `string`
>
> 用于 API 监控的用户标识符

> [accordion] 返回值
>
> **stream=True** `Generator[LLMResultChunk, None, None]`
>
> 一个生成器，在响应分块可用时逐个产出
>
> **stream=False** `LLMResult`
>
> 包含完整生成文本的完整响应对象

> [!TIP]
>
> 建议为流式和非流式调用分别实现辅助方法，让代码保持清晰、易于维护。

#### 2. Token 计数

```python Implementation theme={null}
def get_num_tokens(
    self,
    model: str,
    credentials: dict,
    prompt_messages: list[PromptMessage],
    tools: Optional[list[PromptMessageTool]] = None
) -> int:
    """
    Calculate the number of tokens in the prompt
    """
    # Convert prompt_messages to the format expected by the tokenizer
    text = self._convert_messages_to_text(prompt_messages)

    try:
        # Use the appropriate tokenizer for this model
        tokenizer = self._get_tokenizer(model)
        return len(tokenizer.encode(text))
    except Exception:
        # Fall back to a generic tokenizer
        return self._get_num_tokens_by_gpt2(text)
```

> [!NOTE]
>
> 如果模型不提供分词器，可使用基类的 `_get_num_tokens_by_gpt2(text)` 方法得到合理的近似值。

#### 3. 自定义模型 Schema（可选）

```python Implementation theme={null}
def get_customizable_model_schema(
    self,
    model: str,
    credentials: dict
) -> Optional[AIModelEntity]:
    """
    Get parameter schema for custom models
    """
    # For fine-tuned models, you might return the base model's schema
    if model.startswith("ft:"):
        base_model = self._extract_base_model(model)
        return self._get_predefined_model_schema(base_model)

    # For standard models, return None to use the predefined schema
    return None
```

> [!NOTE]
>
> 此方法仅对支持自定义模型的供应商是必需的。它让自定义模型可以从基础模型继承参数规则。

### TextEmbedding 实现

> [!NOTE]
>
> 文本嵌入模型将文本转换为可捕获语义的高维向量，适用于检索、相似度搜索和分类等场景。

要实现文本嵌入供应商，请继承 `__base.text_embedding_model.TextEmbeddingModel` 基类：

#### 1. 核心嵌入方法

```python Implementation theme={null}
def _invoke(
    self,
    model: str,
    credentials: dict,
    texts: list[str],
    user: Optional[str] = None
) -> TextEmbeddingResult:
    """
    Generate embedding vectors for multiple texts
    """
    # Set up API client with credentials
    client = self._get_client(credentials)

    # Handle batching if needed
    batch_size = self._get_batch_size(model)
    all_embeddings = []
    total_tokens = 0
    start_time = time.time()

    # Process in batches to avoid API limits
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]

        # Make API call to the embeddings endpoint
        response = client.embeddings.create(
            model=model,
            input=batch,
            user=user
        )

        # Extract embeddings from response
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)

        # Track token usage
        total_tokens += response.usage.total_tokens

    # Calculate usage metrics
    elapsed_time = time.time() - start_time
    usage = self._create_embedding_usage(
        model=model,
        tokens=total_tokens,
        latency=elapsed_time
    )

    return TextEmbeddingResult(
        model=model,
        embeddings=all_embeddings,
        usage=usage
    )
```

> [accordion] 参数
>
> **model** `string` *required*
>
> 嵌入模型标识符
>
> **credentials** `dict` *required*
>
> 嵌入服务的认证凭据
>
> **texts** `list[string]` *required*
>
> 要嵌入的文本输入列表
>
> **user** `string`
>
> 用于 API 监控的用户标识符

> [accordion] 返回值
>
> **TextEmbeddingResult** `object` *required*
>
> 包含以下内容的结构化响应：
>
> * `model`：用于嵌入的模型。
> * `embeddings`：嵌入向量，顺序与输入文本一致。
> * `usage`：关于 token 用量和成本的元数据。

#### 2. Token 计数方法

```python Implementation theme={null}
def get_num_tokens(
    self,
    model: str,
    credentials: dict,
    texts: list[str]
) -> int:
    """
    Calculate the number of tokens in the texts to be embedded
    """
    # Join all texts to estimate token count
    combined_text = " ".join(texts)

    try:
        # Use the appropriate tokenizer for this model
        tokenizer = self._get_tokenizer(model)
        return len(tokenizer.encode(combined_text))
    except Exception:
        # Fall back to a generic tokenizer
        return self._get_num_tokens_by_gpt2(combined_text)
```

> [!TIP]
>
> 对于嵌入模型，准确的 token 计数对成本估算很重要，但对功能而言并不关键。`_get_num_tokens_by_gpt2` 方法可为大多数模型提供合理的近似值。

### Rerank 实现

> [!NOTE]
>
> 重排序模型在初次检索之后，根据候选文档与查询的相关性对其重新排序，从而提升搜索质量。

要实现重排序供应商，请继承 `__base.rerank_model.RerankModel` 基类：

```python Implementation theme={null}
def _invoke(
    self,
    model: str,
    credentials: dict,
    query: str,
    docs: list[str],
    score_threshold: Optional[float] = None,
    top_n: Optional[int] = None,
    user: Optional[str] = None
) -> RerankResult:
    """
    Rerank documents based on relevance to the query
    """
    # Set up API client with credentials
    client = self._get_client(credentials)

    # Prepare request data
    request_data = {
        "query": query,
        "documents": docs,
    }

    # Call reranking API endpoint
    response = client.rerank(
        model=model,
        **request_data,
        user=user
    )

    # Process results
    ranked_results = []
    for i, result in enumerate(response.results):
        # Create RerankDocument for each result
        doc = RerankDocument(
            index=result.document_index,  # Original index in docs list
            text=docs[result.document_index],  # Original text
            score=result.relevance_score  # Relevance score
        )
        ranked_results.append(doc)

    # Sort by score in descending order
    ranked_results.sort(key=lambda x: x.score, reverse=True)

    # Apply score threshold filtering if specified
    if score_threshold is not None:
        ranked_results = [doc for doc in ranked_results if doc.score >= score_threshold]

    # Apply top_n limit if specified
    if top_n is not None and top_n > 0:
        ranked_results = ranked_results[:top_n]

    return RerankResult(
        model=model,
        docs=ranked_results
    )
```

> [accordion] 参数
>
> **model** `string` *required*
>
> 重排序模型标识符
>
> **credentials** `dict` *required*
>
> API 的认证凭据
>
> **query** `string` *required*
>
> 搜索查询文本
>
> **docs** `list[string]` *required*
>
> 要重排序的文档文本列表
>
> **score\_threshold** `float`
>
> 文档进入结果所需达到的最低分数
>
> **top\_n** `int`
>
> 返回结果的最大数量
>
> **user** `string`
>
> 用于 API 监控的用户标识符

> [accordion] 返回值
>
> **RerankResult** `object` *required*
>
> 包含以下内容的结构化响应：
>
> * `model`：用于重排序的模型。
> * `docs`：包含索引、文本和分数的 `RerankDocument` 对象列表。

> [!WARNING]
>
> 重排序的计算开销可能很大，尤其是文档集较大时。对大型文档集合实现批处理，以免超时或消耗过多资源。

### Speech2Text 实现

> [!NOTE]
>
> 语音转文字模型将音频文件中的语音转换为书面文本，可用于转录服务、语音命令和无障碍功能等场景。

要实现语音转文字供应商，请继承 `__base.speech2text_model.Speech2TextModel` 基类：

```python Implementation theme={null}
def _invoke(
    self,
    model: str,
    credentials: dict,
    file: IO[bytes],
    user: Optional[str] = None
) -> str:
    """
    Convert speech audio to text
    """
    # Set up API client with credentials
    client = self._get_client(credentials)

    try:
        # Determine the file format
        file_format = self._detect_audio_format(file)

        # Prepare the file for API submission
        # Most APIs require either a file path or binary data
        audio_data = file.read()

        # Call the speech-to-text API
        response = client.audio.transcriptions.create(
            model=model,
            file=("audio.mp3", audio_data),  # Adjust filename based on actual format
            user=user
        )

        # Extract and return the transcribed text
        return response.text

    except Exception as e:
        # Map to appropriate error type
        self._handle_api_error(e)

    finally:
        # Reset file pointer for potential reuse
        file.seek(0)
```

```python Helper Methods theme={null}
def _detect_audio_format(self, file: IO[bytes]) -> str:
    """
    Detect the audio format based on file header
    """
    # Read the first few bytes to check the file signature
    header = file.read(12)
    file.seek(0)  # Reset file pointer

    # Check for common audio format signatures
    if header.startswith(b'RIFF') and header[8:12] == b'WAVE':
        return 'wav'
    elif header.startswith(b'ID3') or header.startswith(b'\xFF\xFB'):
        return 'mp3'
    elif header.startswith(b'OggS'):
        return 'ogg'
    elif header.startswith(b'fLaC'):
        return 'flac'
    else:
        # Default or additional format checks
        return 'mp3'  # Default assumption
```

> [accordion] 参数
>
> **model** `string` *required*
>
> 语音转文字模型标识符
>
> **credentials** `dict` *required*
>
> API 的认证凭据
>
> **file** `IO[bytes]` *required*
>
> 包含待转录音频的二进制文件对象
>
> **user** `string`
>
> 用于 API 监控的用户标识符

> [accordion] 返回值
>
> **text** `string` *required*
>
> 从音频文件转录得到的文本

> [!TIP]
>
> 音频格式检测对于正确处理不同文件类型很重要。可如示例所示，实现一个从文件头检测格式的辅助方法。

> [!WARNING]
>
> 有些语音转文字 API 对文件大小有限制。必要时可对大型音频文件实现分块处理。

### Text2Speech 实现

> [!NOTE]
>
> 文本转语音模型将书面文本转换为自然流畅的语音，可用于语音助手、屏幕阅读器和音频内容生成等场景。

要实现文本转语音供应商，请继承 `__base.text2speech_model.Text2SpeechModel` 基类：

```python Implementation theme={null}
def _invoke(
    self,
    model: str,
    credentials: dict,
    content_text: str,
    streaming: bool,
    user: Optional[str] = None
) -> Union[bytes, Generator[bytes, None, None]]:
    """
    Convert text to speech audio
    """
    # Set up API client with credentials
    client = self._get_client(credentials)

    # Get voice settings based on model
    voice = self._get_voice_for_model(model)

    try:
        # Choose implementation based on streaming preference
        if streaming:
            return self._stream_audio(
                client=client,
                model=model,
                text=content_text,
                voice=voice,
                user=user
            )
        else:
            return self._generate_complete_audio(
                client=client,
                model=model,
                text=content_text,
                voice=voice,
                user=user
            )
    except Exception as e:
        self._handle_api_error(e)
```

```python Helper Methods theme={null}
def _stream_audio(self, client, model, text, voice, user=None):
    """
    Implementation for streaming audio output
    """
    # Make API request with stream=True
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        stream=True,
        user=user
    )

    # Yield chunks as they arrive
    for chunk in response:
        if chunk:
            yield chunk

def _generate_complete_audio(self, client, model, text, voice, user=None):
    """
    Implementation for complete audio file generation
    """
    # Make API request for complete audio
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        user=user
    )

    # Get audio data as bytes
    audio_data = response.content
    return audio_data
```

> [accordion] 参数
>
> **model** `string` *required*
>
> 文本转语音模型标识符
>
> **credentials** `dict` *required*
>
> API 的认证凭据
>
> **content\_text** `string` *required*
>
> 要转换为语音的文本内容
>
> **streaming** `boolean` *required*
>
> 返回流式音频还是完整文件
>
> **user** `string`
>
> 用于 API 监控的用户标识符

> [accordion] 返回值
>
> **streaming=True** `Generator[bytes, None, None]`
>
> 一个生成器，在音频分块可用时逐个产出
>
> **streaming=False** `bytes`
>
> 以字节形式返回的完整音频数据

> [!TIP]
>
> 大多数文本转语音 API 要求在指定模型的同时指定语音。可在 Dify 的模型标识符与供应商的语音选项之间实现映射。

> [!WARNING]
>
> 较长的文本输入可能需要分块，以获得更好的语音合成质量。可实现文本预处理，妥善处理标点、数字和特殊字符。

### Moderation 实现

> [!NOTE]
>
> 内容审核模型分析内容中可能存在的有害、不当或不安全材料，帮助维护平台安全和内容政策。

要实现内容审核供应商，请继承 `__base.moderation_model.ModerationModel` 基类：

```python Implementation theme={null}
def _invoke(
    self,
    model: str,
    credentials: dict,
    text: str,
    user: Optional[str] = None
) -> bool:
    """
    Analyze text for harmful content

    Returns:
        bool: False if the text is safe, True if it contains harmful content
    """
    # Set up API client with credentials
    client = self._get_client(credentials)

    try:
        # Call moderation API
        response = client.moderations.create(
            model=model,
            input=text,
            user=user
        )

        # Check if any categories were flagged
        result = response.results[0]

        # Return True if flagged in any category, False if safe
        return result.flagged

    except Exception as e:
        # Log the error but default to safe if there's an API issue.
        # This is a conservative approach; production systems might want
        # different fallback behavior.
        logger.error(f"Moderation API error: {str(e)}")
        return False
```

```python Detailed Implementation theme={null}
def _invoke(
    self,
    model: str,
    credentials: dict,
    text: str,
    user: Optional[str] = None
) -> bool:
    """
    Analyze text for harmful content with detailed category checking
    """
    # Set up API client with credentials
    client = self._get_client(credentials)

    try:
        # Call moderation API
        response = client.moderations.create(
            model=model,
            input=text,
            user=user
        )

        # Get detailed category results
        result = response.results[0]
        categories = result.categories

        # Check specific categories based on your application's needs
        # For example, you might want to flag certain categories but not others
        critical_violations = [
            categories.harassment,
            categories.hate,
            categories.self_harm,
            categories.sexual,
            categories.violence
        ]

        # Flag content if any critical category is violated
        return any(critical_violations)

    except Exception as e:
        self._handle_api_error(e)
        # Default to safe in case of error
        return False
```

> [accordion] 参数
>
> **model** `string` *required*
>
> 内容审核模型标识符
>
> **credentials** `dict` *required*
>
> API 的认证凭据
>
> **text** `string` *required*
>
> 要分析的文本内容
>
> **user** `string`
>
> 用于 API 监控的用户标识符

> [accordion] 返回值
>
> **result** `boolean` *required*
>
> 表示内容安全性的布尔值：
>
> * `False`：内容安全。
> * `True`：内容包含有害材料。

> [!WARNING]
>
> 内容审核常被用作安全机制。实现方案时，请权衡漏报（放过有害内容）与误报（拦截安全内容）的影响。

> [!TIP]
>
> 许多内容审核 API 提供详细的分类分数，而不仅是二元结果。如果你的应用有需要，可扩展此实现，返回有关具体有害内容类别的更详细信息。

## 实体

### PromptMessageRole

会话中消息的角色。

```python theme={null}
class PromptMessageRole(Enum):
    """
    Enum class for prompt message.
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
```

### PromptMessageContentType

消息内容的类型：纯文本或图片。

```python theme={null}
class PromptMessageContentType(Enum):
    """
    Enum class for prompt message content type.
    """
    TEXT = 'text'
    IMAGE = 'image'
```

### PromptMessageContent

消息内容的基类，仅用于类型声明，请勿直接实例化。

```python theme={null}
class PromptMessageContent(BaseModel):
    """
    Model class for prompt message content.
    """
    type: PromptMessageContentType
    data: str  # Content data
```

内容目前支持文本和图片两种类型，单条消息可将文本与多张图片组合在一起。请实例化 `TextPromptMessageContent` 和 `ImagePromptMessageContent`。

### TextPromptMessageContent

```python theme={null}
class TextPromptMessageContent(PromptMessageContent):
    """
    Model class for text prompt message content.
    """
    type: PromptMessageContentType = PromptMessageContentType.TEXT
```

当消息同时包含文本和图片时，将文本包装为此实体并加入 `content` 列表。

### ImagePromptMessageContent

```python theme={null}
class ImagePromptMessageContent(PromptMessageContent):
    """
    Model class for image prompt message content.
    """
    class DETAIL(Enum):
        LOW = 'low'
        HIGH = 'high'

    type: PromptMessageContentType = PromptMessageContentType.IMAGE
    detail: DETAIL = DETAIL.LOW  # Resolution
```

当消息同时包含文本和图片时，将每张图片包装为此实体并加入 `content` 列表。`data` 接受图片 URL 或 base64 编码的图片字符串。

### PromptMessage

所有角色专属消息的基类，仅用于类型声明，请勿直接实例化。

```python theme={null}
class PromptMessage(ABC, BaseModel):
    """
    Model class for prompt message.
    """
    role: PromptMessageRole  # Message role
    content: Optional[str | list[PromptMessageContent]] = None  # Either a string or a content list; the list form supports multimodal input, see PromptMessageContent
    name: Optional[str] = None  # Optional name
```

### UserPromptMessage

表示一条用户消息。

```python theme={null}
class UserPromptMessage(PromptMessage):
    """
    Model class for user prompt message.
    """
    role: PromptMessageRole = PromptMessageRole.USER
```

### AssistantPromptMessage

表示一条模型回复，通常用于 few-shot 示例或聊天历史输入。

```python theme={null}
class AssistantPromptMessage(PromptMessage):
    """
    Model class for assistant prompt message.
    """
    class ToolCall(BaseModel):
        """
        Model class for assistant prompt message tool call.
        """
        class ToolCallFunction(BaseModel):
            """
            Model class for assistant prompt message tool call function.
            """
            name: str  # Tool name
            arguments: str  # Tool parameters

        id: str  # Tool call ID; only meaningful for OpenAI tool calls. Uniquely identifies one invocation, since the same tool can be called multiple times
        type: str  # Defaults to "function"
        function: ToolCallFunction  # Tool call information

    role: PromptMessageRole = PromptMessageRole.ASSISTANT
    tool_calls: list[ToolCall] = []  # Model's tool call results (only returned when tools are passed in and the model decides to call them)
```

当请求包含 `tools` 时，`tool_calls` 保存模型返回的工具调用。

### SystemPromptMessage

表示一条系统消息，通常用于为模型设置系统指令。

```python theme={null}
class SystemPromptMessage(PromptMessage):
    """
    Model class for system prompt message.
    """
    role: PromptMessageRole = PromptMessageRole.SYSTEM
```

### ToolPromptMessage

表示一条工具消息，将工具的执行结果回传给模型，用于下一步规划。

```python theme={null}
class ToolPromptMessage(PromptMessage):
    """
    Model class for tool prompt message.
    """
    role: PromptMessageRole = PromptMessageRole.TOOL
    tool_call_id: str  # Tool call ID; if the provider doesn't support OpenAI tool calls, you can pass the tool name instead
```

通过继承而来的 `content` 字段传入工具的执行结果。

### PromptMessageTool

```python theme={null}
class PromptMessageTool(BaseModel):
    """
    Model class for prompt message tool.
    """
    name: str  # Tool name
    description: str  # Tool description
    parameters: dict  # Tool parameters dict
```

### LLMResult

```python theme={null}
class LLMResult(BaseModel):
    """
    Model class for llm result.
    """
    model: str  # Model actually used
    prompt_messages: list[PromptMessage]  # Prompt message list
    message: AssistantPromptMessage  # Reply message
    usage: LLMUsage  # Token usage and cost information
    system_fingerprint: Optional[str] = None  # Request fingerprint; see OpenAI's parameter definition
```

### LLMResultChunkDelta

流式响应中每个分块内的增量 delta。

```python theme={null}
class LLMResultChunkDelta(BaseModel):
    """
    Model class for llm result chunk delta.
    """
    index: int  # Sequence number
    message: AssistantPromptMessage  # Reply message
    usage: Optional[LLMUsage] = None  # Token usage and cost information; only returned in the last chunk
    finish_reason: Optional[str] = None  # Completion reason; only returned in the last chunk
```

### LLMResultChunk

流式响应中的单个分块。

```python theme={null}
class LLMResultChunk(BaseModel):
    """
    Model class for llm result chunk.
    """
    model: str  # Model actually used
    prompt_messages: list[PromptMessage]  # Prompt message list
    system_fingerprint: Optional[str] = None  # Request fingerprint; see OpenAI's parameter definition
    delta: LLMResultChunkDelta  # Content changes in this chunk
```

### LLMUsage

```python theme={null}
class LLMUsage(ModelUsage):
    """
    Model class for llm usage.
    """
    prompt_tokens: int  # Tokens used by the prompt
    prompt_unit_price: Decimal  # Prompt unit price
    prompt_price_unit: Decimal  # Prompt price unit, i.e., the number of tokens the unit price applies to
    prompt_price: Decimal  # Prompt cost
    completion_tokens: int  # Tokens used by the completion
    completion_unit_price: Decimal  # Completion unit price
    completion_price_unit: Decimal  # Completion price unit, i.e., the number of tokens the unit price applies to
    completion_price: Decimal  # Completion cost
    total_tokens: int  # Total tokens used
    total_price: Decimal  # Total cost
    currency: str  # Currency unit
    latency: float  # Request latency in seconds
```

### TextEmbeddingResult

```python theme={null}
class TextEmbeddingResult(BaseModel):
    """
    Model class for text embedding result.
    """
    model: str  # Model actually used
    embeddings: list[list[float]]  # Embedding vectors, in the same order as the input texts
    usage: EmbeddingUsage  # Usage information
```

### EmbeddingUsage

```python theme={null}
class EmbeddingUsage(ModelUsage):
    """
    Model class for embedding usage.
    """
    tokens: int  # Tokens used
    total_tokens: int  # Total tokens used
    unit_price: Decimal  # Unit price
    price_unit: Decimal  # Price unit, i.e., the number of tokens the unit price applies to
    total_price: Decimal  # Total cost
    currency: str  # Currency unit
    latency: float  # Request latency in seconds
```

### RerankResult

```python theme={null}
class RerankResult(BaseModel):
    """
    Model class for rerank result.
    """
    model: str  # Model actually used
    docs: list[RerankDocument]  # List of reranked documents
```

### RerankDocument

```python theme={null}
class RerankDocument(BaseModel):
    """
    Model class for rerank document.
    """
    index: int  # Index in the original docs list
    text: str  # Document text
    score: float  # Relevance score
```

## 相关资源

* [模型设计规则](%E6%A8%A1%E5%9E%8B%E8%A7%84%E8%8C%83.md)：模型配置的标准。
* [模型插件介绍](%E6%A8%A1%E5%9E%8B%E8%A7%84%E8%8C%83.md)：模型插件的核心概念。
* [快速集成新模型](../../%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97%E4%B8%8E%E7%A4%BA%E4%BE%8B/%E6%8C%89%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E6%A8%A1%E5%9E%8B%E4%BE%9B%E5%BA%94%E5%95%86%E6%8F%92%E4%BB%B6.md)：向现有供应商添加新模型。
* [创建新模型供应商](../../%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97%E4%B8%8E%E7%A4%BA%E4%BE%8B/%E6%8C%89%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E6%A8%A1%E5%9E%8B%E4%BE%9B%E5%BA%94%E5%95%86%E6%8F%92%E4%BB%B6.md)：从零开发新的模型供应商。
