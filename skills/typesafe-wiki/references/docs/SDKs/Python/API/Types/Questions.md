# Questions

> Provide state and ask yes/no, choice, and score questions using objects or dictionaries.

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

<a id="questions" />

### State

`state` is the text or JSON object you want to ask questions about. It cannot be `None`, but values inside an object may be `None`.

### Question objects

Use `Noul`, `Choice`, and `Score` to define questions with named arguments.

### typesafe\_sdk.NoulCriteria

Bases: `[TypedDict](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypedDict)`

Optional descriptions of the yes and no outcomes.

See the [noul primitive](../../../../Primitives/Noul.md) for details.

#### true

`instance-attribute`

```python
true: JSONContent | None
```

Description of the yes outcome as text, a JSON object, or an array; `None` leaves it undescribed.

#### false

`instance-attribute`

```python
false: JSONContent | None
```

Description of the no outcome as text, a JSON object, or an array; `None` leaves it undescribed.

### typesafe\_sdk.Noul

`pydantic-model`

Bases: `_Question`, `wire.NoulQuestion`

A yes/no question with optional descriptions for either outcome.

See the [noul primitive](../../../../Primitives/Noul.md) for details.

**Note:**

**Show JSON schema:**


#### Details

    ```json
    {
      "$defs": {
        "JSONContent": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "additionalProperties": {
                "anyOf": [
                  {
                    "$ref": "#/$defs/JSONValue"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "object"
            },
            {
              "items": {
                "anyOf": [
                  {
                    "$ref": "#/$defs/JSONValue"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "array"
            }
          ]
        },
        "JSONValue": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "integer"
            },
            {
              "type": "number"
            },
            {
              "type": "boolean"
            },
            {
              "items": {
                "anyOf": [
                  {
                    "$ref": "#/$defs/JSONValue"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "array"
            },
            {
              "additionalProperties": {
                "anyOf": [
                  {
                    "$ref": "#/$defs/JSONValue"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "object"
            }
          ]
        },
        "NoulCriteria": {
          "additionalProperties": false,
          "description": "Optional descriptions of the yes and no outcomes.\n\nSee the [noul primitive](../../../../Primitives/Noul.md) for details.",
          "properties": {
            "true": {
              "anyOf": [
                {
                  "$ref": "#/$defs/JSONContent"
                },
                {
                  "type": "null"
                }
              ]
            },
            "false": {
              "anyOf": [
                {
                  "$ref": "#/$defs/JSONContent"
                },
                {
                  "type": "null"
                }
              ]
            }
          },
          "title": "NoulCriteria",
          "type": "object"
        }
      },
      "additionalProperties": false,
      "description": "A yes/no question with optional descriptions for either outcome.\n\nSee the [noul primitive](../../../../Primitives/Noul.md) for details.",
      "properties": {
        "type": {
          "const": "noul",
          "default": "noul",
          "title": "Type",
          "type": "string"
        },
        "instructions": {
          "anyOf": [
            {
              "$ref": "#/$defs/JSONContent"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "criteria": {
          "anyOf": [
            {
              "$ref": "#/$defs/NoulCriteria"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "title": "Noul",
      "type": "object"
    }
    ```


Fields:

* `type` (`[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)\['noul']`)
* `[instructions](Questions.md#typesafe_sdk.Noul.instructions)` (`[JSONContent](Common types.md#typesafe_sdk.JSONContent) | None`)
* `[criteria](Questions.md#typesafe_sdk.Noul.criteria)` (`[NoulCriteria](Questions.md#typesafe_sdk.NoulCriteria) | None`)

#### instructions

`pydantic-field`

```python
instructions: JSONContent | None = None
```

The question to ask, expressed as text, a JSON object, or an array; optional.

#### criteria

`pydantic-field`

```python
criteria: NoulCriteria | None = None
```

Optional descriptions of the yes and no outcomes.

### typesafe\_sdk.Choice

`pydantic-model`

Bases: `_Question`, `wire.ChoiceQuestion`

A question that selects between named alternatives.

See the [choice primitive](../../../../Primitives/Choice.md) for details.

**Note:**

**Show JSON schema:**


#### Details

    ```json
    {
      "$defs": {
        "JSONContent": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "additionalProperties": {
                "anyOf": [
                  {
                    "$ref": "#/$defs/JSONValue"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "object"
            },
            {
              "items": {
                "anyOf": [
                  {
                    "$ref": "#/$defs/JSONValue"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "array"
            }
          ]
        },
        "JSONValue": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "integer"
            },
            {
              "type": "number"
            },
            {
              "type": "boolean"
            },
            {
              "items": {
                "anyOf": [
                  {
                    "$ref": "#/$defs/JSONValue"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "array"
            },
            {
              "additionalProperties": {
                "anyOf": [
                  {
                    "$ref": "#/$defs/JSONValue"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "object"
            }
          ]
        }
      },
      "additionalProperties": false,
      "description": "A question that selects between named alternatives.\n\nSee the [choice primitive](../../../../Primitives/Choice.md) for details.",
      "properties": {
        "type": {
          "const": "choice",
          "default": "choice",
          "title": "Type",
          "type": "string"
        },
        "instructions": {
          "anyOf": [
            {
              "$ref": "#/$defs/JSONContent"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "criteria": {
          "additionalProperties": {
            "anyOf": [
              {
                "$ref": "#/$defs/JSONContent"
              },
              {
                "type": "null"
              }
            ]
          },
          "title": "Criteria",
          "type": "object"
        }
      },
      "required": [
        "criteria"
      ],
      "title": "Choice",
      "type": "object"
    }
    ```


Fields:

* `type` (`[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)\['choice']`)
* `[criteria](Questions.md#typesafe_sdk.Choice.criteria)` (`[Mapping](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)\[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [JSONContent](Common types.md#typesafe_sdk.JSONContent) | None]`)
* `[instructions](Questions.md#typesafe_sdk.Choice.instructions)` (`[JSONContent](Common types.md#typesafe_sdk.JSONContent) | None`)

#### criteria

`pydantic-field`

```python
criteria: Mapping[str, JSONContent | None]
```

Labels mapped to text, object, or array descriptions, or `None` for undescribed labels.

#### instructions

`pydantic-field`

```python
instructions: JSONContent | None = None
```

The question to ask, expressed as text, a JSON object, or an array; optional.

### typesafe\_sdk.Score

`pydantic-model`

Bases: `_Question`, `wire.ScoreQuestion`

A question that assigns a score using an ordered rubric.

See the [score primitive](../../../../Primitives/Score.md) for details.

**Note:**

**Show JSON schema:**


#### Details

    ```json
    {
      "$defs": {
        "JSONContent": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "additionalProperties": {
                "anyOf": [
                  {
                    "$ref": "#/$defs/JSONValue"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "object"
            },
            {
              "items": {
                "anyOf": [
                  {
                    "$ref": "#/$defs/JSONValue"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "array"
            }
          ]
        },
        "JSONValue": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "integer"
            },
            {
              "type": "number"
            },
            {
              "type": "boolean"
            },
            {
              "items": {
                "anyOf": [
                  {
                    "$ref": "#/$defs/JSONValue"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "array"
            },
            {
              "additionalProperties": {
                "anyOf": [
                  {
                    "$ref": "#/$defs/JSONValue"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "type": "object"
            }
          ]
        }
      },
      "additionalProperties": false,
      "description": "A question that assigns a score using an ordered rubric.\n\nSee the [score primitive](../../../../Primitives/Score.md) for details.",
      "properties": {
        "type": {
          "const": "score",
          "default": "score",
          "title": "Type",
          "type": "string"
        },
        "instructions": {
          "anyOf": [
            {
              "$ref": "#/$defs/JSONContent"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "criteria": {
          "items": {
            "$ref": "#/$defs/JSONContent"
          },
          "title": "Criteria",
          "type": "array"
        }
      },
      "required": [
        "criteria"
      ],
      "title": "Score",
      "type": "object"
    }
    ```


Fields:

* `type` (`[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)\['score']`)
* `[criteria](Questions.md#typesafe_sdk.Score.criteria)` (`[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)\[[JSONContent](Common types.md#typesafe_sdk.JSONContent)]`)
* `[instructions](Questions.md#typesafe_sdk.Score.instructions)` (`[JSONContent](Common types.md#typesafe_sdk.JSONContent) | None`)

#### criteria

`pydantic-field`

```python
criteria: Sequence[JSONContent]
```

A nonempty, ordered list of text, object, or array descriptions, one per score from zero.

#### instructions

`pydantic-field`

```python
instructions: JSONContent | None = None
```

The question to ask, expressed as text, a JSON object, or an array; optional.

### typesafe\_sdk.Question

`module-attribute`

```python
Question: TypeAlias = (
    Noul | Choice | Score | QuestionModel
)
```

A question object or question dictionary.

### typesafe\_sdk.Questions

`module-attribute`

```python
Questions: TypeAlias = Mapping[str, Question]
```

Question inputs keyed by the names used to identify their answers.

### Question dictionaries

Question dictionaries include a `type` key: `"noul"`, `"choice"`, or `"score"`. You can mix dictionaries and question objects in the same request.

### typesafe\_sdk.NoulModel

Bases: `[TypedDict](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypedDict)`

A yes/no question dictionary with `type="noul"`.

See the [noul primitive](../../../../Primitives/Noul.md) for details.

#### type

`instance-attribute`

```python
type: Literal['noul']
```

#### instructions

`instance-attribute`

```python
instructions: NotRequired[JSONContent | None]
```

The question to ask, expressed as text, a JSON object, or an array; optional.

#### criteria

`instance-attribute`

```python
criteria: NotRequired[NoulCriteria | None]
```

Optional descriptions of the yes and no outcomes.

### typesafe\_sdk.ChoiceModel

Bases: `[TypedDict](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypedDict)`

A choice question dictionary with `type="choice"`.

See the [choice primitive](../../../../Primitives/Choice.md) for details.

#### type

`instance-attribute`

```python
type: Literal['choice']
```

#### instructions

`instance-attribute`

```python
instructions: NotRequired[JSONContent | None]
```

The question to ask, expressed as text, a JSON object, or an array; optional.

#### criteria

`instance-attribute`

```python
criteria: Mapping[str, JSONContent | None]
```

Labels mapped to text, object, or array descriptions, or `None` for undescribed labels.

### typesafe\_sdk.ScoreModel

Bases: `[TypedDict](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypedDict)`

A score question dictionary with `type="score"`.

See the [score primitive](../../../../Primitives/Score.md) for details.

#### type

`instance-attribute`

```python
type: Literal['score']
```

#### instructions

`instance-attribute`

```python
instructions: NotRequired[JSONContent | None]
```

The question to ask, expressed as text, a JSON object, or an array; optional.

#### criteria

`instance-attribute`

```python
criteria: Sequence[JSONContent]
```

A nonempty, ordered list of text, object, or array descriptions, one per score from zero.

### typesafe\_sdk.QuestionModel

`module-attribute`

```python
QuestionModel: TypeAlias = (
    NoulModel | ChoiceModel | ScoreModel
)
```

A question dictionary identified by its `type` key.
