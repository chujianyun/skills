# Class: APIConnectionError

The request or response-body delivery failed (DNS, TLS, connection closed, etc.).

## Extends

* [`TypeSafeError`](Class TypeSafeError.md)

## Extended by

* [`APITimeoutError`](Class APITimeoutError.md)

## Constructors

<a id="sdk-constructor" />

### Constructor

```ts
new APIConnectionError(message?, options?): APIConnectionError;
```

#### Parameters

##### message?

`string` = `"Connection error."`

##### options?

`ErrorOptions`

#### Returns

`APIConnectionError`

#### Overrides

[`TypeSafeError`](Class TypeSafeError.md).[`constructor`](Class TypeSafeError.md#sdk-constructor)
