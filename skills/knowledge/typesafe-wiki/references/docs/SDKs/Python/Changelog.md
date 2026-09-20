# Changelog

> Python clients for the TypeSafe AI API

<a id="changelog" />

### v0.7.0 (2026-09-18)

#### Breaking Changes

* ser/de library has been changed from `msgspec` to `pydantic`

#### Bug fixes

* `str` subclasses are now correctly serialized as strings instead of lists of characters

#### Features

* the `system_one` method now accepts a new `response_model` argument that can be set to a desired `pydantic` model for additional *type-safety*

### v0.6.0 (2026-09-15)

#### Breaking Changes

* accept `Score.criteria` as an ordered sequence instead of a dictionary keyed by integers

#### Features

* improve type annotations on SDK inputs to accept abstract types like `Mapping` and `Sequence`
* improve error messages to include http details and metadata

#### Bug fixes

* handle invalid values in `RetryPolicy`
* make exceptions and responses picklable

#### Documentation

* link more concepts from main [docs](https://docs.typesafe.ai/)

### v0.5.7 (2026-09-14)

This is the initial public release of TypeSafe Python SDK. Learn more in the [documentation](TypeSafe Python SDK.md).
