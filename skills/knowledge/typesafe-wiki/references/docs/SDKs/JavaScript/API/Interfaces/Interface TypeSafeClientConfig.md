# Interface: TypeSafeClientConfig

Client options. Explicit values take precedence over environment variables, then SDK defaults.

## Properties

<a id="sdk-apikey" />

### apiKey?

```ts
optional apiKey?: string;
```

Required API key; falls back to `TYPESAFE_API_KEY`.

***

<a id="sdk-baseurl" />

### baseURL?

```ts
optional baseURL?: string;
```

API root; falls back to `TYPESAFE_BASE_URL`, then `https://api.typesafe.ai`.

***

<a id="sdk-dangerouslyallowbrowser" />

### dangerouslyAllowBrowser?

```ts
optional dangerouslyAllowBrowser?: boolean;
```

Allow browser use, exposing the API key to page users. Default: false.

***

<a id="sdk-defaultheaders" />

### defaultHeaders?

```ts
optional defaultHeaders?: Record<string, string>;
```

Additional request headers; per-call headers take precedence.

***

<a id="sdk-defaultmodel" />

### defaultModel?

```ts
optional defaultModel?: string;
```

Default model; falls back to `TYPESAFE_DEFAULT_MODEL`, then `jev-latest`.

***

<a id="sdk-fetch" />

### fetch?

```ts
optional fetch?: Fetch;
```

Custom HTTP fetch implementation for transport configuration or tests. Default: global `fetch`.

***

<a id="sdk-logger" />

### logger?

```ts
optional logger?: Logger;
```

Logger filtered to `logLevel` and above. Default: prefixed `console`.

***

<a id="sdk-loglevel" />

### logLevel?

```ts
optional logLevel?: LogLevel;
```

Log level; falls back to `TYPESAFE_LOG_LEVEL`, then `warn`.
`info` logs request summaries; `debug` adds headers and bodies.
Known credential headers are redacted; bodies are not.

***

<a id="sdk-retry" />

### retry?

```ts
optional retry?: Partial<RetryPolicy>;
```

Retry overrides; omitted fields use the defaults in `RetryPolicy`.

***

<a id="sdk-timeout" />

### timeout?

```ts
optional timeout?: number;
```

Timeout per attempt in milliseconds, without a total retry budget. Default: 10000.
