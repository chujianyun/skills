# Interface: SystemOneRequestPayload

Request body for `POST /v1/systemone`, with the model resolved.

## Extends

* [`SystemOneRequest`](Interface SystemOneRequest Q.md)

## Properties

<a id="sdk-model" />

### model

```ts
model: string;
```

Model override; omitted values inherit `defaultModel`.

#### Overrides

[`SystemOneRequest`](Interface SystemOneRequest Q.md).[`model`](Interface SystemOneRequest Q.md#sdk-model)

***

<a id="sdk-questions" />

### questions

```ts
questions: Questions;
```

Nonempty questions keyed by the names used to identify their answers.

#### Inherited from

[`SystemOneRequest`](Interface SystemOneRequest Q.md).[`questions`](Interface SystemOneRequest Q.md#sdk-questions)

***

<a id="sdk-state" />

### state

```ts
state: EntryType;
```

Text, a JSON object or array, or `null` to evaluate.

#### Inherited from

[`SystemOneRequest`](Interface SystemOneRequest Q.md).[`state`](Interface SystemOneRequest Q.md#sdk-state)
