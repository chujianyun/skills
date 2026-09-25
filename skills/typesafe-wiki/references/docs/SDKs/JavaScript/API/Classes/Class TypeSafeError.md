# Class: TypeSafeError

Base class for SDK errors.

## Extends

* `Error`

## Extended by

* [`APIConnectionError`](Class APIConnectionError.md)
* [`APIError`](Class APIError.md)
* [`APIUserAbortError`](Class APIUserAbortError.md)

## Constructors

<a id="sdk-constructor" />

### Constructor

```ts
new TypeSafeError(message, options?): TypeSafeError;
```

#### Parameters

##### message

`string`

##### options?

`ErrorOptions`

#### Returns

`TypeSafeError`

#### Overrides

```ts
Error.constructor
```
