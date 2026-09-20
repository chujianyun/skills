# Interface: ChoiceResponse<T>

A selected label and its probabilities.

## Type Parameters

### T

`T` *extends* [`ChoiceCriteria`](../Type Aliases/Type Alias ChoiceCriteria.md) = [`ChoiceCriteria`](../Type Aliases/Type Alias ChoiceCriteria.md)

## Properties

<a id="sdk-choice" />

### choice

```ts
readonly choice: keyof T & string;
```

The selected label.

***

<a id="sdk-confidence" />

### confidence

```ts
readonly confidence: number;
```

Reported confidence in the selected label.

***

<a id="sdk-probabilities" />

### probabilities

```ts
readonly probabilities: { readonly [label in string | number | symbol]: number };
```

Probabilities keyed by label.

***

<a id="sdk-type" />

### type

```ts
readonly type: "choice";
```
