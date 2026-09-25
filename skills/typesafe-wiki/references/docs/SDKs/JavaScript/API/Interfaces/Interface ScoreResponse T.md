# Interface: ScoreResponse<T>

An expected score with its rubric and probabilities.

## Type Parameters

### T

`T` *extends* [`ScoreCriteria`](../Type Aliases/Type Alias ScoreCriteria.md) = [`ScoreCriteria`](../Type Aliases/Type Alias ScoreCriteria.md)

## Properties

<a id="sdk-confidence" />

### confidence

```ts
readonly confidence: number;
```

Reported confidence in the score.

***

<a id="sdk-legend" />

### legend

```ts
readonly legend: ScoreLegend<T>;
```

Rubric descriptions keyed by score.

***

<a id="sdk-probabilities" />

### probabilities

```ts
readonly probabilities: { readonly [score in number | `${number}`]: number };
```

Probabilities keyed by score.

***

<a id="sdk-score" />

### score

```ts
readonly score: number;
```

Expected score, which may fall between integer rubric levels.

***

<a id="sdk-type" />

### type

```ts
readonly type: "score";
```
