<div align="center">

# AI Code Review Triage

**AI writes code faster than you can read it. Stop reading harder and review differently.**

**English** · [简体中文](README.zh-CN.md)

<img src="assets/social-preview.png" alt="AI Code Review Triage: catch bugs, align context, own the sign-off" width="760">

A [Claude Code](https://claude.com/claude-code) skill that reviews AI-generated pull requests by splitting "reading the code" into three separate jobs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-skill-d97757)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

</div>

---

## The problem

Agent-written PRs pile up faster than anyone can review them line by line. Reading harder doesn't help much either: the code is tidy on the surface, so the real problems hide well enough to survive a careful read. "Just merge and roll back if it breaks" works technically, but a human still answers for the incident.

## The idea

"Reviewing code" has always bundled three different jobs. That worked when code arrived slowly. At agent speed, each job needs its own process:

```mermaid
flowchart LR
    PR([AI-written PR]) --> T{Step 0<br/>Triage<br/>risk tier}
    T --> B["**1 · Catch bugs**<br/>fresh-context sub-agent<br/>+ tests / repro"]
    B --> C["**2 · Align context**<br/>orders of magnitude<br/>history & neighbors<br/>requirement match"]
    C --> S["**3 · Own the sign-off**<br/>explain · detect · undo<br/>scoped approval"]
    S --> R([Review report])
```

| Job | Question | Who does it best |
|---|---|---|
| **Catch bugs** | Is the code wrong? | Machines, with an *independent* second pass |
| **Align context** | Is this the right change for this product, today? | A human, checking angles the diff can't show |
| **Own the sign-off** | Will I put my name on this? | The approver, with an explicit scope |

Low-risk PRs only run Step 1. High-risk PRs (production behavior, data, security, money) run all three.

## What it catches that line-by-line review misses

> A PR changes `SESSION_TIMEOUT = 30` to `30000` and drops one line of unit conversion. Tests pass. The code is clean. A line-by-line reader approves it in 30 seconds.
>
> - **Step 1** has a fresh-context sub-agent add a boundary test. Result: sessions now expire after **30 seconds**.
> - **Step 2** checks history and callers. The same change was reverted once before, the mobile client hard-codes the old value, and the request was only for "remember me" users while the diff changes everyone.
> - **Step 3** blocks the approval. Nobody can explain what the PR actually does.
>
> Full run: [examples/session-timeout-walkthrough.md](examples/session-timeout-walkthrough.md)

## Install

**As a plugin** (inside Claude Code):

```
/plugin marketplace add laulauraluo/ai-code-review-triage
/plugin install ai-code-review-triage@ai-code-review-triage
```

**As a standalone skill:**

```bash
git clone https://github.com/laulauraluo/ai-code-review-triage.git
cp -r ai-code-review-triage/skills/ai-code-review-triage ~/.claude/skills/
```

## Usage

Ask Claude Code something like:

- *"Review this AI-generated PR before I merge it."*
- *"Can this diff be merged? Claude wrote it."*
- *"I'm about to approve #123. What should I verify first?"*

The skill triggers on its own and returns a report (illustrative example):

```markdown
## Extend session lifetime for "remember me" · Risk: High

### 1. Bugs (independent fresh-context review)
- [CONFIRMED] auth/session.py:3 — unit conversion dropped; sessions expire after 30 s. Repro: test_session_expires_after_timeout

### 2. Context
- Magnitudes: SESSION_TIMEOUT 30 → 30000 (comment says min, code treats as ms) — suspicious
- History / neighbors: reverted once before (a1b2c3d); mobile/src/config.ts hard-codes 30 min
- Requirement match: asked for remember-me users only; diff changes everyone

### 3. Sign-off
- Detection: login-rate and 401-rate alerts · Rollback: config revert
- Recommendation: request changes
- Verification scope: verified units and callers; did not load-test
```

## Repository layout

```
.claude-plugin/
  plugin.json          # plugin manifest
  marketplace.json     # lets /plugin marketplace add this repo
skills/
  ai-code-review-triage/
    SKILL.md           # the skill itself
examples/
  session-timeout-walkthrough.md   # end-to-end illustrative run
```

## Works well with

This skill organizes the review and decides what has to be true before you approve. It doesn't replace specialized checkers. Run them inside Step 1:

- correctness-focused review (e.g. Claude Code's built-in `/code-review`)
- security / performance checklists
- over-engineering reviews

## Acknowledgments

The three-job framing was inspired by a talk by [grapeot](https://www.bilibili.com/video/BV1mRn66JERc/) on reviewing AI-written code.

## License

[MIT](LICENSE)

---

<div align="center">

If this caught a bad merge for you, a ⭐ helps other reviewers find it.

</div>
