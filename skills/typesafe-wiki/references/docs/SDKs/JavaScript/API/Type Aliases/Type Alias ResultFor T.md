# Type Alias: ResultFor<T>

```ts
type ResultFor<T> = T extends NoulQuestion ? NoulResponse : T extends ScoreQuestion<infer S> ? ScoreResponse<S> : T extends ChoiceQuestion<infer E> ? ChoiceResponse<E> : never;
```

The answer type for a question, preserving its criteria keys.

## Type Parameters

### T

`T` *extends* [`Question`](Type Alias Question.md)
