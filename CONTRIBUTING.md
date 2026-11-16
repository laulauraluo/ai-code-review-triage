# Contributing

Thanks for helping. This repository is one Markdown skill plus its docs, so most changes are to prose. The bar is that every claim is checkable: a path comes with a link to the agent's documentation, and a number in an example comes from the example itself.

## Try your working copy

Link the skill folder into your agent's skills folder (move any installed copy out of the way first). From the repository root:

```sh
ln -s "$PWD/skills/ai-code-review-triage" ~/.claude/skills/ai-code-review-triage
```

Use the folder for your agent from [docs/agents.md](docs/agents.md) instead of `~/.claude/skills`, for example `~/.agents/skills` for Codex or `~/.cursor/skills` for Cursor. Then run one of the prompts in [`evals/evals.json`](evals/evals.json) and compare the answer with its `expected_output`.

## Checks

```sh
python3 scripts/check.py
```

It needs only Python 3 and checks that:

- `SKILL.md` frontmatter follows the [Agent Skills spec](https://agentskills.io/specification): `name` is lowercase with hyphens, at most 64 characters and the same as its folder; `description` is 1 to 1024 characters; `compatibility` is at most 500.
- every eval has a `prompt` and an `expected_output`;
- every relative link in a Markdown file points to a file that exists;
- the Python reproduction in the pagination walkthrough still runs.

CI runs the same script on every pull request.

## House rules

- **Keep the method.** The three steps, the risk tiers, `CONFIRMED` versus `PLAUSIBLE`, and the scoped sign-off are the point of the skill. A change that weakens one needs a reason in the pull request.
- **Stay agent-neutral in `SKILL.md`.** Name a tool from one agent only as an example. Agent-specific detail goes in `references/subagents.md` or `docs/agents.md`.
- **Every agent path needs a source.** Link the agent's own documentation. If you can't find a page that says it, mark it unverified rather than guess.
- **Keep `SKILL.md` short.** The spec suggests under 500 lines; long material goes in `references/`.
- **Examples stay invented and labeled as such.** No real company code, incidents or customer names.
- **Update [`CHANGELOG.md`](CHANGELOG.md)** under a new version or `Unreleased`.

## Adding an agent

Open an [agent support issue](https://github.com/laulauraluo/ai-code-review-triage/issues/new?template=agent_support.yml) or send a pull request that adds a row to the table in [docs/agents.md](docs/agents.md) and, if the agent has sub-agents, to [`references/subagents.md`](skills/ai-code-review-triage/references/subagents.md). Include the user and project folders, how the agent calls a skill, and a link to its documentation.

By taking part you agree to keep discussion respectful and on topic.
