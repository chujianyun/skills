# Class: APIUserAbortError

The caller cancelled the request through an `AbortSignal`.

## Extends

* [`TypeSafeError`](Class TypeSafeError.md)

## Constructors

<a id="sdk-constructor" />

### Constructor

```ts
new APIUserAbortError(message?, options?): APIUserAbortError;
```

#### Parameters

##### message?

`string` = `"Request was aborted."`

##### options?

`ErrorOptions`

#### Returns

`APIUserAbortError`

#### Overrides

[`TypeSafeError`](Class TypeSafeError.md).[`constructor`](Class TypeSafeError.md#sdk-constructor)
