# Class: UnprocessableEntityError

HTTP 422: request validation failed.

## Extends

* [`APIError`](Class APIError.md)

## Constructors

<a id="sdk-constructor" />

### Constructor

```ts
new UnprocessableEntityError(
   status,
   body,
   headers,
   message?
): UnprocessableEntityError;
```

#### Parameters

##### status

`number`

##### body

`unknown`

##### headers

`Headers`

##### message?

`string`

#### Returns

`UnprocessableEntityError`

#### Inherited from

[`APIError`](Class APIError.md).[`constructor`](Class APIError.md#sdk-constructor)

## Properties

<a id="sdk-body" />

### body

```ts
readonly body: unknown;
```

Parsed JSON, response text, or `undefined` for an empty body.

#### Inherited from

[`APIError`](Class APIError.md).[`body`](Class APIError.md#sdk-body)

***

<a id="sdk-headers" />

### headers

```ts
readonly headers: Headers;
```

HTTP response headers.

#### Inherited from

[`APIError`](Class APIError.md).[`headers`](Class APIError.md#sdk-headers)

***

<a id="sdk-requestid" />

### requestId

```ts
readonly requestId: string | undefined;
```

Request ID from `x-typesafe-request-id`, or `undefined` when absent.

#### Inherited from

[`APIError`](Class APIError.md).[`requestId`](Class APIError.md#sdk-requestid)

***

<a id="sdk-status" />

### status

```ts
readonly status: number;
```

HTTP response status code.

#### Inherited from

[`APIError`](Class APIError.md).[`status`](Class APIError.md#sdk-status)

## Methods

<a id="sdk-fromresponse" />

### fromResponse()

```ts
static fromResponse(
   status,
   body,
   headers
): APIError;
```

Create the error subclass for an HTTP status code.

#### Parameters

##### status

`number`

##### body

`unknown`

##### headers

`Headers`

#### Returns

[`APIError`](Class APIError.md)

#### Inherited from

[`APIError`](Class APIError.md).[`fromResponse`](Class APIError.md#sdk-fromresponse)
