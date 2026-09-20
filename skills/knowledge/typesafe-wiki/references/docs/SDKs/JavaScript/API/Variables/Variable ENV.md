# Variable: ENV

```ts
const ENV: object;
```

Environment variable names for client configuration. Explicit options take precedence.

## Type Declaration

<a id="sdk-apikey" />

### apiKey

```ts
readonly apiKey: string; // value is "TYPESAFE_API_KEY"
```

Required API key; used when `apiKey` is omitted.

<a id="sdk-baseurl" />

### baseURL

```ts
readonly baseURL: "TYPESAFE_BASE_URL" = "TYPESAFE_BASE_URL";
```

API root; defaults to `https://api.typesafe.ai`.

<a id="sdk-defaultmodel" />

### defaultModel

```ts
readonly defaultModel: "TYPESAFE_DEFAULT_MODEL" = "TYPESAFE_DEFAULT_MODEL";
```

Default model name; defaults to `jev-latest`.

<a id="sdk-loglevel" />

### logLevel

```ts
readonly logLevel: "TYPESAFE_LOG_LEVEL" = "TYPESAFE_LOG_LEVEL";
```

Log level; defaults to `warn`.
