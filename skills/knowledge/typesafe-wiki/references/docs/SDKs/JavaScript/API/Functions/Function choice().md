# Function: choice()

```ts
function choice<T>(instructions, criteria): ChoiceQuestion<T>;
```

Create a question that selects between named alternatives.

## Type Parameters

### T

`T` *extends* [`ChoiceCriteria`](../Type Aliases/Type Alias ChoiceCriteria.md)

## Parameters

### instructions

[`EntryType`](../Type Aliases/Type Alias EntryType.md)

The question as text, a JSON object or array, or `null`.

### criteria

`T`

Labels mapped to descriptions, or `null` for undescribed labels.

## Returns

[`ChoiceQuestion`](../Interfaces/Interface ChoiceQuestion T.md)\<`T`>
