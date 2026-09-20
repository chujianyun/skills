# Type Alias: ScoreLegend<T>

```ts
type ScoreLegend<T> = { readonly [score in ScoreOf<T>]: T[score] };
```

Rubric descriptions keyed by score.

## Type Parameters

### T

`T` *extends* [`ScoreCriteria`](Type Alias ScoreCriteria.md)
