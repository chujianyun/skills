# Function: score()

```ts
function score<T>(instructions, criteria): ScoreQuestion<T>;
```

Create a score question using an ordered rubric.

## Type Parameters

### T

`T` *extends* [`ScoreCriteria`](../Type Aliases/Type Alias ScoreCriteria.md)

## Parameters

### instructions

[`EntryType`](../Type Aliases/Type Alias EntryType.md)

The question as text, a JSON object or array, or `null`.

### criteria

`T`

At least two descriptions indexed by score from zero; entries may be `null`.

## Returns

[`ScoreQuestion`](../Interfaces/Interface ScoreQuestion T.md)\<`T`>
