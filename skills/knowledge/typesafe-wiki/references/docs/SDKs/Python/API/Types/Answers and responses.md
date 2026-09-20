# Answers and responses

> Read answers, confidence scores, token usage, and available models returned by the TypeSafe API.

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

<a id="answers-and-responses" />

### Response

### typesafe\_sdk.SystemOneResponse

`pydantic-model`

Bases: `Response`

Answers grouped by question type with model and usage metadata.

See [System One](../../../../Concepts/System One.md) for details.

**Note:**

**Show JSON schema:**


#### Details

    ```json
    {
      "$defs": {
        "ChoiceAnswer": {
          "description": "A selected label and its probabilities.\n\nSee the [choice primitive](../../../../Primitives/Choice.md) for details.",
          "properties": {
            "type": {
              "const": "choice",
              "default": "choice",
              "title": "Type",
              "type": "string"
            },
            "choice": {
              "description": "The name of the choice with the highest probability among the question's criteria.",
              "examples": [
                "angry"
              ],
              "title": "Choice",
              "type": "string"
            },
            "confidence": {
              "description": "Confidence in the selected choice, from 0 to 1. Higher values indicate greater certainty; use lower values to flag uncertain selections for review.",
              "examples": [
                0.9
              ],
              "title": "Confidence",
              "type": "number"
            },
            "probabilities": {
              "additionalProperties": {
                "type": "number"
              },
              "description": "Probability of each choice in criteria, keyed by choice name, from 0 to 1. Shows how likely the alternatives are; values sum to approximately 1.",
              "examples": [
                {
                  "angry": 0.8,
                  "calm": 0.1,
                  "excited": 0.1
                }
              ],
              "title": "Probabilities",
              "type": "object"
            }
          },
          "required": [
            "choice",
            "confidence",
            "probabilities"
          ],
          "title": "ChoiceAnswer",
          "type": "object"
        },
        "NoulAnswer": {
          "description": "A yes/no answer.\n\nSee the [noul primitive](../../../../Primitives/Noul.md) for details.",
          "properties": {
            "type": {
              "const": "noul",
              "default": "noul",
              "title": "Type",
              "type": "string"
            },
            "noul": {
              "description": "Probability of a yes answer or a true statement, from 0 to 1. Values near 1 favor yes or true, values near 0 favor no or false, and values near 0.5 indicate uncertainty.",
              "examples": [
                0.98
              ],
              "title": "Noul",
              "type": "number"
            }
          },
          "required": [
            "noul"
          ],
          "title": "NoulAnswer",
          "type": "object"
        },
        "ScoreAnswer": {
          "description": "An expected score with its rubric and probabilities.\n\nSee the [score primitive](../../../../Primitives/Score.md) for details.",
          "properties": {
            "type": {
              "const": "score",
              "default": "score",
              "title": "Type",
              "type": "string"
            },
            "score": {
              "description": "Expected score: the probability-weighted average of the rubric levels. May fall between integer levels.",
              "examples": [
                1.7
              ],
              "title": "Score",
              "type": "number"
            },
            "confidence": {
              "description": "Confidence in the score, from 0 to 1. Higher values indicate greater certainty; use lower values to flag uncertain ratings for review.",
              "examples": [
                0.9
              ],
              "title": "Confidence",
              "type": "number"
            },
            "legend": {
              "additionalProperties": {
                "anyOf": [
                  {
                    "type": "string"
                  },
                  {
                    "additionalProperties": true,
                    "type": "object"
                  },
                  {
                    "items": {},
                    "type": "array"
                  }
                ]
              },
              "title": "Legend",
              "type": "object"
            },
            "probabilities": {
              "additionalProperties": {
                "type": "number"
              },
              "title": "Probabilities",
              "type": "object"
            }
          },
          "required": [
            "score",
            "confidence",
            "legend",
            "probabilities"
          ],
          "title": "ScoreAnswer",
          "type": "object"
        },
        "Usage": {
          "description": "Token counts for a request, when reported by the API.",
          "properties": {
            "input_tokens": {
              "anyOf": [
                {
                  "type": "integer"
                },
                {
                  "type": "null"
                }
              ],
              "default": null,
              "title": "Input Tokens"
            },
            "output_tokens": {
              "anyOf": [
                {
                  "type": "integer"
                },
                {
                  "type": "null"
                }
              ],
              "default": null,
              "title": "Output Tokens"
            }
          },
          "title": "Usage",
          "type": "object"
        }
      },
      "description": "Answers grouped by question type with model and usage metadata.\n\nSee [System One](../../../../Concepts/System One.md) for details.",
      "properties": {
        "model": {
          "title": "Model",
          "type": "string"
        },
        "usage": {
          "$ref": "#/$defs/Usage"
        },
        "answers": {
          "additionalProperties": {
            "discriminator": {
              "mapping": {
                "choice": "#/$defs/ChoiceAnswer",
                "noul": "#/$defs/NoulAnswer",
                "score": "#/$defs/ScoreAnswer"
              },
              "propertyName": "type"
            },
            "oneOf": [
              {
                "$ref": "#/$defs/NoulAnswer"
              },
              {
                "$ref": "#/$defs/ChoiceAnswer"
              },
              {
                "$ref": "#/$defs/ScoreAnswer"
              }
            ]
          },
          "title": "Answers",
          "type": "object"
        }
      },
      "required": [
        "model",
        "usage"
      ],
      "title": "SystemOneResponse",
      "type": "object"
    }
    ```


Config:

* `extra`: `ignore`
* `frozen`: `True`
* `strict`: `True`

Fields:

* `[model](Answers and responses.md#typesafe_sdk.SystemOneResponse.model)` (`[str](https://docs.python.org/3/builtins/stdtypes.html#str)`)
* `[usage](Answers and responses.md#typesafe_sdk.SystemOneResponse.usage)` (`[Usage](Answers and responses.md#typesafe_sdk.Usage)`)
* `[answers](Answers and responses.md#typesafe_sdk.SystemOneResponse.answers)` (`[dict](https://docs.python.org/3/builtins/stdtypes.html#dict)\[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [Answer](Answers and responses.md#typesafe_sdk.Answer)]`)

#### request\_id

`cached` `property`

```python
request_id: str
```

The `x-typesafe-request-id` response header.

#### raw\_http\_response

`property`

```python
raw_http_response: httpx2.Response
```

The underlying `httpx2.Response`, exposing status, headers, and body.

#### model\_config

`class-attribute` `instance-attribute`

```python
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

#### model

`pydantic-field`

```python
model: str
```

The model used to answer the request.

#### usage

`pydantic-field`

```python
usage: Usage
```

Token usage for the request.

#### answers

`pydantic-field`

```python
answers: dict[str, Answer]
```

All answer objects keyed by question name.

#### nouls

`cached` `property`

```python
nouls: dict[str, NoulAnswer]
```

Yes/no answers keyed by question name.

#### choices

`cached` `property`

```python
choices: dict[str, ChoiceAnswer]
```

Choice answers keyed by question name.

#### scores

`cached` `property`

```python
scores: dict[str, ScoreAnswer]
```

Score answers keyed by question name.

### typesafe\_sdk.Usage

`pydantic-model`

Bases: `wire.Usage`

Token counts for a request, when reported by the API.

**Note:**

**Show JSON schema:**


#### Details

    ```json
    {
      "description": "Token counts for a request, when reported by the API.",
      "properties": {
        "input_tokens": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Input Tokens"
        },
        "output_tokens": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Output Tokens"
        }
      },
      "title": "Usage",
      "type": "object"
    }
    ```


Config:

* `extra`: `ignore`
* `frozen`: `True`
* `strict`: `True`

Fields:

* `[input\_tokens](Answers and responses.md#typesafe_sdk.Usage.input_tokens)` (`[int](https://docs.python.org/3/builtins/functions.html#int) | None`)
* `[output\_tokens](Answers and responses.md#typesafe_sdk.Usage.output_tokens)` (`[int](https://docs.python.org/3/builtins/functions.html#int) | None`)

#### model\_config

`class-attribute` `instance-attribute`

```python
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

#### input\_tokens

`pydantic-field`

```python
input_tokens: int | None = None
```

Number of input tokens used, or `None` when the API did not report it.

#### output\_tokens

`pydantic-field`

```python
output_tokens: int | None = None
```

Number of output tokens used, or `None` when the API did not report it.

### Answers

### typesafe\_sdk.NoulAnswer

`pydantic-model`

Bases: `wire.NoulAnswer`

A yes/no answer.

See the [noul primitive](../../../../Primitives/Noul.md) for details.

**Note:**

**Show JSON schema:**


#### Details

    ```json
    {
      "description": "A yes/no answer.\n\nSee the [noul primitive](../../../../Primitives/Noul.md) for details.",
      "properties": {
        "type": {
          "const": "noul",
          "default": "noul",
          "title": "Type",
          "type": "string"
        },
        "noul": {
          "description": "Probability of a yes answer or a true statement, from 0 to 1. Values near 1 favor yes or true, values near 0 favor no or false, and values near 0.5 indicate uncertainty.",
          "examples": [
            0.98
          ],
          "title": "Noul",
          "type": "number"
        }
      },
      "required": [
        "noul"
      ],
      "title": "NoulAnswer",
      "type": "object"
    }
    ```


Config:

* `extra`: `ignore`
* `frozen`: `True`
* `strict`: `True`

Fields:

* `[noul](Answers and responses.md#typesafe_sdk.NoulAnswer.noul)` (`[float](https://docs.python.org/3/builtins/functions.html#float)`)
* `type` (`[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)\['noul']`)

#### noul

`pydantic-field`

```python
noul: float
```

Probability of a yes answer or a true statement, from 0 to 1. Values near 1 favor yes or true, values near 0 favor no or false, and values near 0.5 indicate uncertainty.

#### model\_config

`class-attribute` `instance-attribute`

```python
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

### typesafe\_sdk.ChoiceAnswer

`pydantic-model`

Bases: `wire.ChoiceAnswer`

A selected label and its probabilities.

See the [choice primitive](../../../../Primitives/Choice.md) for details.

**Note:**

**Show JSON schema:**


#### Details

    ```json
    {
      "description": "A selected label and its probabilities.\n\nSee the [choice primitive](../../../../Primitives/Choice.md) for details.",
      "properties": {
        "type": {
          "const": "choice",
          "default": "choice",
          "title": "Type",
          "type": "string"
        },
        "choice": {
          "description": "The name of the choice with the highest probability among the question's criteria.",
          "examples": [
            "angry"
          ],
          "title": "Choice",
          "type": "string"
        },
        "confidence": {
          "description": "Confidence in the selected choice, from 0 to 1. Higher values indicate greater certainty; use lower values to flag uncertain selections for review.",
          "examples": [
            0.9
          ],
          "title": "Confidence",
          "type": "number"
        },
        "probabilities": {
          "additionalProperties": {
            "type": "number"
          },
          "description": "Probability of each choice in criteria, keyed by choice name, from 0 to 1. Shows how likely the alternatives are; values sum to approximately 1.",
          "examples": [
            {
              "angry": 0.8,
              "calm": 0.1,
              "excited": 0.1
            }
          ],
          "title": "Probabilities",
          "type": "object"
        }
      },
      "required": [
        "choice",
        "confidence",
        "probabilities"
      ],
      "title": "ChoiceAnswer",
      "type": "object"
    }
    ```


Config:

* `extra`: `ignore`
* `frozen`: `True`
* `strict`: `True`

Fields:

* `[choice](Answers and responses.md#typesafe_sdk.ChoiceAnswer.choice)` (`[str](https://docs.python.org/3/builtins/stdtypes.html#str)`)
* `[confidence](Answers and responses.md#typesafe_sdk.ChoiceAnswer.confidence)` (`[float](https://docs.python.org/3/builtins/functions.html#float)`)
* `[probabilities](Answers and responses.md#typesafe_sdk.ChoiceAnswer.probabilities)` (`[dict](https://docs.python.org/3/builtins/stdtypes.html#dict)\[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [float](https://docs.python.org/3/builtins/functions.html#float)]`)
* `type` (`[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)\['choice']`)

#### choice

`pydantic-field`

```python
choice: str
```

The name of the choice with the highest probability among the question's criteria.

#### confidence

`pydantic-field`

```python
confidence: float
```

Confidence in the selected choice, from 0 to 1. Higher values indicate greater certainty; use lower values to flag uncertain selections for review.

#### probabilities

`pydantic-field`

```python
probabilities: dict[str, float]
```

Probability of each choice in criteria, keyed by choice name, from 0 to 1. Shows how likely the alternatives are; values sum to approximately 1.

#### model\_config

`class-attribute` `instance-attribute`

```python
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

### typesafe\_sdk.ScoreAnswer

`pydantic-model`

Bases: `wire.ScoreAnswer`

An expected score with its rubric and probabilities.

See the [score primitive](../../../../Primitives/Score.md) for details.

**Note:**

**Show JSON schema:**


#### Details

    ```json
    {
      "description": "An expected score with its rubric and probabilities.\n\nSee the [score primitive](../../../../Primitives/Score.md) for details.",
      "properties": {
        "type": {
          "const": "score",
          "default": "score",
          "title": "Type",
          "type": "string"
        },
        "score": {
          "description": "Expected score: the probability-weighted average of the rubric levels. May fall between integer levels.",
          "examples": [
            1.7
          ],
          "title": "Score",
          "type": "number"
        },
        "confidence": {
          "description": "Confidence in the score, from 0 to 1. Higher values indicate greater certainty; use lower values to flag uncertain ratings for review.",
          "examples": [
            0.9
          ],
          "title": "Confidence",
          "type": "number"
        },
        "legend": {
          "additionalProperties": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "additionalProperties": true,
                "type": "object"
              },
              {
                "items": {},
                "type": "array"
              }
            ]
          },
          "title": "Legend",
          "type": "object"
        },
        "probabilities": {
          "additionalProperties": {
            "type": "number"
          },
          "title": "Probabilities",
          "type": "object"
        }
      },
      "required": [
        "score",
        "confidence",
        "legend",
        "probabilities"
      ],
      "title": "ScoreAnswer",
      "type": "object"
    }
    ```


Config:

* `extra`: `ignore`
* `frozen`: `True`
* `strict`: `True`

Fields:

* `[score](Answers and responses.md#typesafe_sdk.ScoreAnswer.score)` (`[float](https://docs.python.org/3/builtins/functions.html#float)`)
* `[confidence](Answers and responses.md#typesafe_sdk.ScoreAnswer.confidence)` (`[float](https://docs.python.org/3/builtins/functions.html#float)`)
* `type` (`[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)\['score']`)
* `[legend](Answers and responses.md#typesafe_sdk.ScoreAnswer.legend)` (`[dict](https://docs.python.org/3/builtins/stdtypes.html#dict)\[[int](https://docs.python.org/3/builtins/functions.html#int), [str](https://docs.python.org/3/builtins/stdtypes.html#str) | [dict](https://docs.python.org/3/builtins/stdtypes.html#dict)\[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | [list](https://docs.python.org/3/builtins/stdtypes.html#list)\[[Any](https://docs.python.org/3/library/typing.html#typing.Any)]]`)
* `[probabilities](Answers and responses.md#typesafe_sdk.ScoreAnswer.probabilities)` (`[dict](https://docs.python.org/3/builtins/stdtypes.html#dict)\[[int](https://docs.python.org/3/builtins/functions.html#int), [float](https://docs.python.org/3/builtins/functions.html#float)]`)

#### score

`pydantic-field`

```python
score: float
```

Expected score: the probability-weighted average of the rubric levels. May fall between integer levels.

#### confidence

`pydantic-field`

```python
confidence: float
```

Confidence in the score, from 0 to 1. Higher values indicate greater certainty; use lower values to flag uncertain ratings for review.

#### model\_config

`class-attribute` `instance-attribute`

```python
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

#### legend

`pydantic-field`

```python
legend: dict[
    int, str | dict[str, Any] | list[Any]
]
```

Rubric descriptions keyed by integer score.

#### probabilities

`pydantic-field`

```python
probabilities: dict[int, float]
```

Probabilities keyed by integer score.

### typesafe\_sdk.Answer

`module-attribute`

```python
Answer: TypeAlias = Annotated[
    NoulAnswer | ChoiceAnswer | ScoreAnswer,
    Field(discriminator="type"),
]
```

An answer to a single question, identified by its `type`.

### Available models

### typesafe\_sdk.ListModelsResponse

`pydantic-model`

Bases: `Response`

The models available to the account.

**Note:**

**Show JSON schema:**


#### Details

    ```json
    {
      "$defs": {
        "ModelMetadata": {
          "description": "Metadata describing a single available model.",
          "properties": {
            "name": {
              "title": "Name",
              "type": "string"
            },
            "description": {
              "title": "Description",
              "type": "string"
            },
            "release_date": {
              "title": "Release Date",
              "type": "string"
            }
          },
          "required": [
            "name",
            "description",
            "release_date"
          ],
          "title": "ModelMetadata",
          "type": "object"
        }
      },
      "description": "The models available to the account.",
      "properties": {
        "models": {
          "items": {
            "$ref": "#/$defs/ModelMetadata"
          },
          "title": "Models",
          "type": "array"
        }
      },
      "required": [
        "models"
      ],
      "title": "ListModelsResponse",
      "type": "object"
    }
    ```


Fields:

* `[models](Answers and responses.md#typesafe_sdk.ListModelsResponse.models)` (`[tuple](https://docs.python.org/3/builtins/stdtypes.html#tuple)\[[ModelMetadata](Answers and responses.md#typesafe_sdk.ModelMetadata), ...]`)

#### request\_id

`cached` `property`

```python
request_id: str
```

The `x-typesafe-request-id` response header.

#### raw\_http\_response

`property`

```python
raw_http_response: httpx2.Response
```

The underlying `httpx2.Response`, exposing status, headers, and body.

#### model\_config

`class-attribute` `instance-attribute`

```python
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

#### models

`pydantic-field`

```python
models: tuple[ModelMetadata, ...]
```

The available models.

### typesafe\_sdk.ModelMetadata

`pydantic-model`

Bases: `Schema`

Metadata describing a single available model.

**Note:**

**Show JSON schema:**


#### Details

    ```json
    {
      "description": "Metadata describing a single available model.",
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "description": {
          "title": "Description",
          "type": "string"
        },
        "release_date": {
          "title": "Release Date",
          "type": "string"
        }
      },
      "required": [
        "name",
        "description",
        "release_date"
      ],
      "title": "ModelMetadata",
      "type": "object"
    }
    ```


Fields:

* `[name](Answers and responses.md#typesafe_sdk.ModelMetadata.name)` (`[str](https://docs.python.org/3/builtins/stdtypes.html#str)`)
* `[description](Answers and responses.md#typesafe_sdk.ModelMetadata.description)` (`[str](https://docs.python.org/3/builtins/stdtypes.html#str)`)
* `[release\_date](Answers and responses.md#typesafe_sdk.ModelMetadata.release_date)` (`[str](https://docs.python.org/3/builtins/stdtypes.html#str)`)

#### name

`pydantic-field`

```python
name: str
```

Model name or alias accepted by a request's model field.

#### description

`pydantic-field`

```python
description: str
```

Human-readable description of the model and its capabilities.

#### release\_date

`pydantic-field`

```python
release_date: str
```

Model release date, formatted as YYYY-MM-DD.
