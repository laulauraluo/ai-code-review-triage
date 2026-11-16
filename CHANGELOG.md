# Changelog

All notable changes to AI Code Review Triage are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-11-15

### Added

- Support for agents beyond Claude Code. The skill follows the open [Agent Skills](https://agentskills.io/specification) format, and [docs/agents.md](docs/agents.md) documents installing and calling it in Codex, GitHub Copilot, Cursor, Gemini CLI, Antigravity, OpenCode, Windsurf, Cline, Roo Code, Kiro, Amp, Junie and Zed, plus Aider (as read-only context) and Continue (unverified), each with a link to that agent's documentation.
- One-command install with the `skills` CLI: `npx skills add laulauraluo/ai-code-review-triage`.
- `references/subagents.md`: how to start the fresh-context reviewer for Step 1 in each agent, and what to do in agents without sub-agents.
- `agents/openai.yaml` with a display name for the Codex and ChatGPT apps.
- `evals/evals.json` with test prompts and expected answers.
- `scripts/check.py` and a CI workflow: Agent Skills frontmatter rules, evals, local links and the pagination reproduction.
- `CONTRIBUTING.md`, issue forms and a pull request template.

### Changed

- Step 1 no longer names Claude Code's Agent tool as the only way to start a reviewer. It asks for the host agent's sub-agent or task feature, or a new session.
- `SKILL.md` frontmatter now carries `license` and `compatibility`.
- The README and the Chinese README were rewritten around the multi-agent install.

## [1.0.0] - 2026-10-22

### Added

- The skill: risk triage, three review steps (catch bugs, align context, own the sign-off) and a report template.
- Claude Code plugin and marketplace manifests.
- Session-timeout and pagination-limit walkthroughs, the second with a runnable reproduction.
- A Chinese README and a question-and-answer guide.
