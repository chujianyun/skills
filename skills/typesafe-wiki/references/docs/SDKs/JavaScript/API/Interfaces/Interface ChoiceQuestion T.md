# Interface: ChoiceQuestion<T>

A question that selects between named alternatives.

## Type Parameters

### T

`T` *extends* [`ChoiceCriteria`](../Type Aliases/Type Alias ChoiceCriteria.md) = [`ChoiceCriteria`](../Type Aliases/Type Alias ChoiceCriteria.md)

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
type: "choice";
```
