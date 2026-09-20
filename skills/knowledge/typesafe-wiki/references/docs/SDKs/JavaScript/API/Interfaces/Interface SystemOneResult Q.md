# Interface: SystemOneResult<Q>

Answers keyed by question name, with model and usage metadata.

## Type Parameters

### Q

`Q` *extends* [`Questions`](Interface Questions.md)

## Properties

<a id="sdk-answers" />

### answers

```ts
readonly answers: { readonly [K in string | number | symbol]: ResultFor<Q[K]> };
```

Answers with types inferred from the supplied questions.

***

<a id="sdk-model" />

### model

```ts
readonly model: string;
```

The model used to answer the request.

***

<a id="sdk-usage" />

### usage

```ts
readonly usage: Usage;
```

Token usage for the request.
