# Interface: WithResponse<T>

Parsed data with its HTTP response and request ID.

## Type Parameters

### T

`T`

## Properties

<a id="sdk-data" />

### data

```ts
data: T;
```

The parsed response body.

***

<a id="sdk-requestid" />

### requestId

```ts
requestId: string | undefined;
```

Request ID from `x-typesafe-request-id`, or `undefined` when absent.

***

<a id="sdk-response" />

### response

```ts
response: Response;
```

The HTTP response, with its body consumed by parsing.
