# Common types

> Common types for TypeSafe API SDK.

export function SdkSignature({children}) {
  async function copy(event) {
    const button = event.currentTarget;
    const code = button.parentElement.querySelector("pre code");
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.setAttribute("aria-label", "Signature copied");
      button.dataset.copied = "true";
    } catch {
      button.setAttribute("aria-label", "Copy failed; select the signature to copy");
    }
    setTimeout(() => {
      button.setAttribute("aria-label", "Copy signature");
      delete button.dataset.copied;
    }, 2000);
  }
  return

        <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <rect x="8" y="8" width="12" height="12" rx="2" />
          <path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3" />
        </svg>

      `{children}`
    ;
}

<a id="common-types" />

### typesafe\_sdk.JSONValue

`module-attribute`

```python
JSONValue = TypeAliasType(
    "JSONValue",
    "str | int | float | bool | Sequence[JSONValue | None] | Mapping[str, JSONValue | None]",
)
```

A JSON-like value. May be nested and contain `None`.

### typesafe\_sdk.JSONContent

`module-attribute`

```python
JSONContent = TypeAliasType(
    "JSONContent",
    "str | Mapping[str, JSONValue | None] | Sequence[JSONValue | None]",
)
```

Either a plain string or a mapping/sequence of [`JSONValue`](Common types.md#typesafe_sdk.JSONValue) entries.
