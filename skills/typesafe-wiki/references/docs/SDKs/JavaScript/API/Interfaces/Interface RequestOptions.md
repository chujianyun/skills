# Interface: RequestOptions

Per-call options that override client settings.

## Properties

<a id="sdk-headers" />

### headers?

```ts
optional headers?: Record<string, string>;
```

Additional headers, merged over `defaultHeaders`.

***

<a id="sdk-retry" />

### retry?

```ts
optional retry?: Partial<RetryPolicy>;
```

Retry overrides for this call; omitted fields inherit client settings.

***

<a id="sdk-signal" />

### signal?

```ts
optional signal?: AbortSignal;
```

Cancellation signal for the request and pending retries.

***

<a id="sdk-timeout" />

### timeout?

```ts
optional timeout?: number;
```

Timeout per attempt in milliseconds; there is no total retry budget.
