# Publish one classified Skill

Publish the Skill named in `$ARGUMENTS` through the repository's mandatory quality gate.

Execute these steps in order. Do not skip a step and do not represent a stopped or failed run as a successful publication.

1. Read `AGENTS.md` and `config/skill-categories.json`. Resolve exactly one directory at `skills/<category>/$ARGUMENTS/`. Stop if the Skill is missing, duplicated, or in the wrong category.
2. Use the `skill-optimizer` Skill to review only the target Skill. Cover triggering, workflow order, failure handling, confirmation gates, output contract, progressive disclosure, external dependencies, sensitive information, and high-impact actions.
3. For a newly created Skill, this `/publish-skill` invocation is explicit authorization to apply safe, in-scope optimizer changes automatically. Stop and ask before destructive changes, secret handling, external publication, or changes outside the target Skill. For an existing Skill, retain the optimizer's normal review-plan-confirmation gate.
4. Apply all approved optimizer fixes. If any required review item remains unresolved, stop before recording a pass.
5. Run `python3 scripts/validate_skill.py $ARGUMENTS`. Fix in-scope failures and rerun it. Do not continue until it exits successfully.
6. Only after the semantic review and deterministic validation both pass, run `python3 scripts/record_optimizer_review.py $ARGUMENTS --status passed`.
7. Run `python3 scripts/publish_skill.py $ARGUMENTS`.

`SKILLS_MARKET_PUBLISHER` must point to the configured internal-market executable. A missing adapter, rejected upload, stale optimizer report, validation failure, Git failure, or push failure is a hard stop. Market upload must complete before Git commit or push.
