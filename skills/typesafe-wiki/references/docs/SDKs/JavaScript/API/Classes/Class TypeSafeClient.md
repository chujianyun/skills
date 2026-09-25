# Class: TypeSafeClient

Client for the TypeSafe AI API.

## Constructors

<a id="sdk-constructor" />

### Constructor

```ts
new TypeSafeClient(config?): TypeSafeClient;
```

Create a client for the TypeSafe AI API.

Explicit options take precedence over environment variables, then SDK defaults.
Empty or whitespace-only environment values are ignored.

#### Parameters

##### config?

[`TypeSafeClientConfig`](../Interfaces/Interface TypeSafeClientConfig.md) = `{}`

#### Returns

`TypeSafeClient`

#### Throws

The API key is missing, configuration is invalid, or the runtime is unsupported.

## Properties

<a id="sdk-baseurl" />

### baseURL

```ts
readonly baseURL: string;
```

API root with trailing slashes removed.

***

<a id="sdk-defaultheaders" />

### defaultHeaders

```ts
readonly defaultHeaders: Readonly<Record<string, string>>;
```

Additional headers sent with each request.

***

<a id="sdk-defaultmodel" />

### defaultModel

```ts
readonly defaultModel: string;
```

Model used when a request omits `model`.

***

<a id="sdk-fetch" />

### fetch

```ts
readonly fetch: Fetch;
```

HTTP fetch implementation.

***

<a id="sdk-logger" />

### logger

```ts
readonly logger: Logger;
```

The configured logger, filtered to `logLevel`.

***

<a id="sdk-loglevel" />

### logLevel

```ts
readonly logLevel: LogLevel;
```

Configured log verbosity.

***

<a id="sdk-models" />

### models

```ts
readonly models: Models;
```

The models available to the account.

***

<a id="sdk-retry" />

### retry

```ts
readonly retry: RetryPolicy;
```

Retry settings with constructor overrides applied.

***

<a id="sdk-timeout" />

### timeout

```ts
readonly timeout: number;
```

Timeout per attempt in milliseconds.

## Methods

<a id="sdk-systemone" />

### systemOne()

```ts
systemOne<Q>(request, options?): APIPromise<SystemOneResult<Q>>;
```

Answer named questions about text or structured state.

#### Type Parameters

##### Q

`Q` *extends* [`Questions`](../Interfaces/Interface Questions.md)

#### Parameters

##### request

[`SystemOneRequest`](../Interfaces/Interface SystemOneRequest Q.md)\<`Q`>

State, questions, and an optional model override.

##### options?

[`RequestOptions`](../Interfaces/Interface RequestOptions.md) = `{}`

Per-call timeout, retry, headers, and cancellation settings.

#### Returns

[`APIPromise`](Class APIPromise T.md)\<[`SystemOneResult`](../Interfaces/Interface SystemOneResult Q.md)\<`Q`>>

Answers typed by question name and criteria, with model and token usage.

#### Throws

Questions are empty, or score criteria are not a list of at least two entries.

#### Throws

The server returns a non-2xx response after retries.

#### Throws

The request cannot connect or times out after retries.

#### Throws

The caller aborts the request.

#### Example

```ts
const { answers } = await client.systemOne({
  state: "I was charged twice. Please help.",
  questions: { billing: noul("Is this about billing?") },
});
console.log(answers.billing.noul);
```
