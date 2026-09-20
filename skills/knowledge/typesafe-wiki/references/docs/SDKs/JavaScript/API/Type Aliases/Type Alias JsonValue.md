# Type Alias: JsonValue

```ts
type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | {
[key: string]: JsonValue;
};
```

A JSON-compatible value.
