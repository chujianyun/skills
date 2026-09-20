# Class: APITimeoutError

The full response did not arrive within the timeout. A kind of `APIConnectionError`.

## Extends

* [`APIConnectionError`](Class APIConnectionError.md)

## Constructors

<a id="sdk-constructor" />

### Constructor

```ts
new APITimeoutError(timeoutMs, options?): APITimeoutError;
```

#### Parameters

##### timeoutMs

`number`

##### options?

`ErrorOptions`

#### Returns

`APITimeoutError`

#### Overrides

[`APIConnectionError`](Class APIConnectionError.md).[`constructor`](Class APIConnectionError.md#sdk-constructor)

## Properties

<a id="sdk-timeoutms" />

### timeoutMs

```ts
readonly timeoutMs: number;
```

Configured timeout in milliseconds.
