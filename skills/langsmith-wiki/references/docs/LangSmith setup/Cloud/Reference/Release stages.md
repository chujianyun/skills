# Release stages

> How LangSmith labels features as alpha, beta, or generally available, and what each stage means for stability, support, and availability

LangSmith ships features through three release stages: alpha, beta, and generally available (GA). Each stage sets a consistent expectation for how stable a feature is, where it runs, and how it is supported, so you can decide when to adopt it.

A feature advances through the stages as it matures, though smaller features may skip alpha or beta and launch directly as GA. The following table summarizes each stage.

| Stage | Availability | Changes | Self-hosted / BYOC | Support |
| - | - | - | - | - |
| [Alpha](#alpha) | Design partners only | Breaking changes expected; the feature may change significantly or never ship | Not guaranteed | No formal SLA |
| [Beta](#beta) | Public or a private group | Interface or behavior may still change; GA expected within a few months | Typically added during beta | Actively maintained; SLA varies by feature |
| [GA](#generally-available-ga) | Public | Stable; breaking changes require a deprecation period | Supported | Fully supported |

## Alpha

Alpha is the earliest release stage, used to validate a feature with a small audience before wider release.

* **Availability**: Available to design partners only. Alpha features are not publicly announced.
* **Readiness**: May be incomplete or partial, and is intended for early validation rather than production use.
* **Changes**: Breaking changes are expected. The feature may change significantly, and it may never ship as GA.
* **Pricing**: No pricing commitment.
* **Deployments**: Not necessarily available in self-hosted or BYOC environments.
* **Support**: No SLA applies.

Alpha is optional. A feature may skip this stage.

## Beta

Beta makes a feature available for real use while its interface and behavior are being finalized. Beta features are functional end to end, not partial implementations, so you can adopt them in production workflows and help shape them before general availability.

* **Availability**: Available publicly or to a private group, and tagged `Beta` in the product UI and documentation where applicable.
* **Readiness**: Functional end to end and suitable for real workflows.
* **Changes**: The interface or behavior may still change before the feature reaches GA, which is expected within a few months.
* **Pricing**: Pricing may be available, but is not yet finalized.
* **Deployments**: Support for self-hosted and BYOC environments is typically added during beta.
* **Support**: Beta features are actively maintained and refined based on feedback. SLA coverage varies by feature.

Beta is optional. Smaller features may skip this stage.

## Generally available (GA)

GA features are stable and fully supported for production use.

* **Availability**: Publicly available.
* **Readiness**: Complete and production-ready.
* **Changes**: API behavior is stable. Breaking changes require a deprecation period.
* **Pricing**: Pricing is finalized.
* **Deployments**: Supported in all environments, including self-hosted and BYOC.
* **Support**: Fully supported and thoroughly documented.

Any feature that is not marked alpha or beta is GA, and is supported immediately and permanently. LangSmith may occasionally deprecate a generally available feature, but this is uncommon.

## See also

* [Release policy](../../Self-hosted/Reference/Release%20policy.md) for self-hosted release channels, cadence, and version support
* [API and SDK deprecation policy](API%20and%20SDK%20deprecation%20policy.md) for how deprecated endpoints and methods are removed
* [Changelog](LangSmith%20Cloud%20changelog.md) for recent LangSmith updates
