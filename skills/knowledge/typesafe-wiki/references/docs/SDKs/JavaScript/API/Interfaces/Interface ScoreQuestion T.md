# Interface: ScoreQuestion<T>

A question that assigns a score using an ordered rubric.

## Type Parameters

### T

`T` *extends* [`ScoreCriteria`](../Type Aliases/Type Alias ScoreCriteria.md) = [`ScoreCriteria`](../Type Aliases/Type Alias ScoreCriteria.md)

## Properties

<a id="sdk-criteria" />

### criteria

```ts
criteria: T;
```

Descriptions of the available outcomes.

***

<a id="sdk-instructions" />

### instructions?

```ts
optional instructions?: EntryType;
```

The question as text, a JSON object, or an array; optional or `null`.

***

<a id="sdk-type" />

### type

```ts
type: "score";
```
