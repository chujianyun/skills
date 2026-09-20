# Type Alias: ScoreOf<T>

```ts
type ScoreOf<T> = number extends T["length"] ? number : Extract<keyof T, `${number}`>;
```

Score keys inferred from the rubric; a fixed-length tuple yields its indices, otherwise `number`.

## Type Parameters

### T

`T` *extends* [`ScoreCriteria`](Type Alias ScoreCriteria.md)
