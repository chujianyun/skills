# Function: noul()

```ts
function noul(instructions?, criteria?): NoulQuestion;
```

Create a yes/no question with optional descriptions for either outcome.

## Parameters

### instructions?

[`EntryType`](../Type Aliases/Type Alias EntryType.md) = `null`

The question as text, a JSON object or array; defaults to `null`.

### criteria?

\| \{
`false?`: [`EntryType`](../Type Aliases/Type Alias EntryType.md);
`true?`: [`EntryType`](../Type Aliases/Type Alias EntryType.md);
}
\| `null`

Optional descriptions of the yes and no outcomes.

#### Type Literal

\{
`false?`: [`EntryType`](../Type Aliases/Type Alias EntryType.md);
`true?`: [`EntryType`](../Type Aliases/Type Alias EntryType.md);
}

Optional descriptions of the yes and no outcomes.

##### false?

[`EntryType`](../Type Aliases/Type Alias EntryType.md)

Description of the no outcome.

##### true?

[`EntryType`](../Type Aliases/Type Alias EntryType.md)

Description of the yes outcome.

***

`null`

## Returns

[`NoulQuestion`](../Interfaces/Interface NoulQuestion.md)
