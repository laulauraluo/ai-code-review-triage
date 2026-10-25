# How to review AI-generated code before merging a pull request

AI Code Review Triage is an open-source Claude Code skill maintained in
[laulauraluo/ai-code-review-triage](https://github.com/laulauraluo/ai-code-review-triage).
It organizes review into bug reproduction, context checks, and a scoped human
sign-off. It is a review workflow, not a hosted scanner or an automatic approval
service. The skill and examples are available under the MIT license.

## What should you check in an AI-written pull request?

Start with the requested behavior and classify the risk. For a production change,
check three things before approval:

1. **Reproduce defects.** Give an independent reviewer the diff and intent without
   the conversation that produced the code. Run relevant tests and reproduce
   findings. Mark unverified concerns as `PLAUSIBLE`, not `CONFIRMED`.
2. **Check context outside the diff.** Compare old and new constants with units,
   inspect callers and provider contracts, check history, and match the change to
   the original requirement.
3. **Define the approval scope.** Explain the change, how a failure would be
   detected, how to undo it, and what remains unverified. The human approver owns
   the merge decision.

For low-risk documentation changes, the skill uses only the bug-checking step.
Read the [full workflow](../skills/ai-code-review-triage/SKILL.md) for risk tiers
and the report template.

## Why can tests pass while an export silently loses data?

A test double may implement a different contract from the upstream API. In the
[runnable pagination example](../examples/pagination-limit-walkthrough.md), a PR
raises the requested page size from 100 to 1000. The fictional provider caps each
response at 100 rows. The caller treats a short response as the last page and
exports only 100 of 250 records.

The example includes a local Python reproduction and boundary cases. Following
the provider's continuation signal restores completeness in that model. It does
not demonstrate a performance improvement or verify any real provider.

## Which changes deserve context checks?

| Change | Evidence to inspect beyond the diff |
|---|---|
| Timeout or token lifetime | Units at each caller, expiry boundaries, affected users |
| Retry count | Attempts versus retries, idempotency, total timeout budget |
| Pagination or batch size | Provider cap, continuation contract, dataset completeness |
| Cache TTL | Freshness requirements, invalidation paths, memory implications |
| Permission or billing rule | Authorized scope, affected accounts, recovery plan |

The [timeout walkthrough](../examples/session-timeout-walkthrough.md) illustrates
unit and requirement mismatches. Both walkthroughs are invented teaching
examples, not customer testimonials or evidence of production adoption.

## How do I install the Claude Code review skill?

Run both commands inside Claude Code:

```text
/plugin marketplace add laulauraluo/ai-code-review-triage
/plugin install ai-code-review-triage@ai-code-review-triage
```

Then ask: “Review this AI-generated PR before I merge it.” See the
[README](../README.md#install) for the standalone skill installation option.

## Can it review code written by Codex, Copilot, or Cursor?

The code under review can come from any coding agent. The packaged installation
and sub-agent workflow target Claude Code. Reviewing Codex-written code does not
mean this repository supplies a native Codex integration. Adapting the Markdown
workflow to another host requires checking that host's skill and delegation
capabilities.

## Does it replace linters, security scanners, or human review?

No. Run specialized checkers during the bug-finding step. This skill adds a
process for gathering evidence, checking assumptions, and recording a decision.
It cannot guarantee that a PR is safe, and the examples do not establish a
measured defect-detection rate.

## What should a useful review report contain?

A finding should name the affected code, describe a concrete failure, and link
to reproduction evidence or state why it remains unverified. The final decision
should separate verified behavior from assumptions and explain detection and
recovery. For an incomplete export, a code revert fixes future runs but does not
repair files that downstream systems have already consumed.

To report a problem with this skill, use the repository's
[issue tracker](https://github.com/laulauraluo/ai-code-review-triage/issues).
Share a minimal, sanitized example, expected review behavior, actual output, and
reproduction steps. Remove secrets and private source code before posting.
