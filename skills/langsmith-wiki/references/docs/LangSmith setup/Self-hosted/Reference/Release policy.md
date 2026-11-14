# Release policy

> Release channels, cadence, and version support for self-hosted LangSmith.

Self-hosted LangSmith ships on two release channels: a stable channel that customers run in production, and a preview channel that tracks the next major version.

## Release channels

### Stable

The current generally available major version. LangSmith recommends this channel for production. Stable receives weekly patch releases containing critical bug fixes and security patches only. No new features, data migrations, or infrastructure changes land on stable between major versions.

Throughout this page, `N` refers to the current stable major version. Preview tracks the next major version, `N+1`.

### Preview

The development build of the next major version. Preview includes new features and fixes as they merge into LangSmith SaaS, so you can evaluate the next major version before it becomes stable. Preview builds may include data migrations, but never add or remove services or introduce breaking changes.

Preview is intended for evaluation in test and staging environments. LangSmith does not recommend running preview in production.

## Release cadence

| Channel | Cadence |
| - | - |
| Preview | Published mirroring the LangSmith SaaS release cadence |
| Stable: new major (`v0.X.0`) | Approximately every 6 weeks (two per quarter) |
| Stable: patch (`v0.X.Y`) | Weekly (typically Friday), skipped if no changes. Ad-hoc releases issued for critical customer issues. |

## What ships in each channel

| | Preview | Stable patch | Next major |
| - | :-: | :-: | :-: |
| New features | yes | no | yes |
| Bug fixes | yes | critical only | yes |
| Security patches | yes | yes | yes |
| Data migrations and backfills | yes | no | yes |
| New or removed services | no | no | yes |
| Breaking changes | no | no | yes |

Service additions, service removals, and breaking changes only land in a new major version, so plan upgrades to new majors with this in mind.

## Version numbering

Every self-hosted release has two version numbers:

* The **chart version** is the Helm chart version you install and pin. Releases are named after it, both in the [self-hosted changelog](Self-hosted%20LangSmith%20changelog.md) and as [Helm repository](https://github.com/langchain-ai/helm/releases) release tags, for example `langsmith-0.17.2`.
* The **LangSmith version** is the application version the chart deploys, recorded as `appVersion` in the chart.

| | Chart version | Example |
| - | - | - |
| Stable | `0.17.Y` | Chart `0.17.2` deploys LangSmith `0.17.30` |
| Preview (release candidate) | `0.18.0-rc.N` | Chart `0.18.0-rc.12` deploys LangSmith `0.18.4rc1` |

For the current patch and release candidate on each line, see the [self-hosted changelog](Self-hosted%20LangSmith%20changelog.md) or the Helm repository release tags.

* Stable chart versions are `0.X.Y`, where `X` is the major version and `Y` increments with each patch release.
* Preview chart versions are `0.X.0-rc.N`, where `N` increments with each release candidate.
* The two numbers advance independently. The chart patch number and the LangSmith patch number are not expected to match.

The `vX` shorthand used for release trains (`v16`, `v17`) refers to the major version, so `v17` means chart version `0.17.Y`.

## Pair the sandbox runtime chart

Installations that run [Sandboxes in a separate cluster](../Install%20an%20instance/Additional%20features/Enable%20Sandboxes/Run%20self-hosted%20Sandboxes%20in%20a%20separate%20cluster.md) install a second chart, `langsmith-sandbox`, for the sandbox runtime. The two charts pair by appVersion, the LangSmith version, never by chart version:

* Run the newest `langsmith-sandbox` chart whose appVersion equals the appVersion of your `langsmith` chart. The runtime chart shares the major version, such as `0.18`, but its patch and release candidate numbers advance independently of the `langsmith` chart's.
* Leave `images.sandboxHostImage.tag` empty in the runtime chart, so the runtime image follows the chart's appVersion.

To list the runtime chart versions with their appVersions, run:

```bash
helm search repo langchain/langsmith-sandbox --versions --devel
```

Each release in the [self-hosted changelog](Self-hosted%20LangSmith%20changelog.md) also links its runtime chart, for installations that mirror charts or cannot reach the Helm repository.

For the upgrade order, see [Upgrade separate sandbox clusters](../Manage%20an%20instance/Upgrade%20an%20installation.md#upgrade-separate-sandbox-clusters).

## Version support

LangSmith supports the current stable major version (`N`) and the previous stable major version (`N-1`):

* `N` receives active support: critical bug fixes, security patches, and weekly patch releases.
* `N-1` receives critical support only: critical bug fixes and security patches, released ad hoc rather than weekly.
* Versions older than `N-1` are end of life and do not receive new patch releases, bug fixes, or security updates.

Because a new major version ships approximately every 6 weeks, a version reaches end of life roughly 6 weeks after it is superseded as stable. Fixes are not backported to a version once it is end of life; upgrade to a supported major version to pick them up.

Alongside the two supported stable versions, the next major version is available on the preview channel as a series of release candidates, for example `0.18.0-rc.12`. Preview builds are published continuously and always carry the newest fixes, but they are intended for evaluation in test and staging environments rather than production. Running preview in a non-production environment is the recommended way to validate the next major version before it becomes stable.

## Recommendations

* **Run stable in production.** Preview is for evaluation only and may contain unreleased features still under validation.
* **Use preview in test or staging.** Running preview in a non-production environment is the best way to catch issues early and prepare for the next major upgrade.
* **Plan for major upgrades.** Data migrations, service additions or removals, and breaking changes only land in new major versions. Review the [self-hosted changelog](Self-hosted%20LangSmith%20changelog.md) before upgrading and plan for any required data or infrastructure changes.
* **Stay on a supported version.** LangSmith recommends upgrading to each new major version soon after it is released to pick up architectural improvements on the recommended cadence.

## Current version

To check the current stable and preview versions, refer to the [self-hosted changelog](Self-hosted%20LangSmith%20changelog.md).

## See also

* [Release stages](../../Cloud/Reference/Release%20stages.md) for how features move from alpha to GA
* [API and SDK deprecation policy](../../Cloud/Reference/API%20and%20SDK%20deprecation%20policy.md) for how deprecated endpoints and methods are removed
