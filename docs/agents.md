# Install and use in each agent

Looks Good to AI is an [Agent Skill](https://agentskills.io/specification): a folder, `skills/looks-good-to-ai/`, with a `SKILL.md` at its root. Every agent below loads that folder as is. Nothing is rewritten per agent; only the install path and the way you call it differ.

Paths were checked against each agent's own documentation on 2026-11-15. Agents change these quickly. If a path here disagrees with the linked page, the page wins, and an [issue](https://github.com/laulauraluo/looks-good-to-ai/issues/new?template=bug_report.yml) is welcome.

## The fast way: the skills CLI

The [`skills`](https://github.com/vercel-labs/skills) CLI finds `skills/looks-good-to-ai/SKILL.md` in this repository and copies it to the right folder for the agents you pick:

```sh
npx skills add laulauraluo/looks-good-to-ai           # this project, asks which agents
npx skills add laulauraluo/looks-good-to-ai -g        # for your user
npx skills add laulauraluo/looks-good-to-ai -g -a codex -a cursor
```

The `-a` ids are in the table below and in the CLI's [agent list](https://github.com/vercel-labs/skills/blob/main/docs/agents.md). The CLI's folders sometimes differ from the ones an agent documents first, but each agent reads the CLI's folder too.

## With the agent's own installer

Four agents can install the repository directly. Each command was run against this repository on 2026-11-17.

| Agent | Commands | Source |
|---|---|---|
| **Claude Code** | `/plugin marketplace add laulauraluo/looks-good-to-ai`, then `/plugin install looks-good-to-ai@looks-good-to-ai` | [Plugins](https://code.claude.com/docs/en/plugins) |
| **Codex** | `codex plugin marketplace add laulauraluo/looks-good-to-ai`, then `codex plugin add looks-good-to-ai@looks-good-to-ai` | [Build plugins](https://developers.openai.com/codex/plugins/build) |
| **GitHub Copilot CLI** | `copilot plugin marketplace add laulauraluo/looks-good-to-ai`, then `copilot plugin install looks-good-to-ai@looks-good-to-ai` | [CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) |
| **Gemini CLI** | `gemini extensions install https://github.com/laulauraluo/looks-good-to-ai` | [Extensions](https://geminicli.com/docs/extensions/reference/) |

Codex and Copilot CLI read the same `.claude-plugin/` manifests as Claude Code. Gemini CLI reads `gemini-extension.json` and finds the skill under `skills/`. Copilot CLI also accepts `copilot plugin install laulauraluo/looks-good-to-ai`, but warns that direct installs are deprecated.

## By hand

Copy or clone the skill folder so that `SKILL.md` ends up at `<skills folder>/looks-good-to-ai/SKILL.md`:

```sh
git clone https://github.com/laulauraluo/looks-good-to-ai.git /tmp/acrt
cp -r /tmp/acrt/skills/looks-good-to-ai <skills folder>/
```

For a project install, commit the folder so your team gets it too.

| Agent | `-a` id | User folder | Project folder | How to call it | Source |
|---|---|---|---|---|---|
| **Claude Code** | `claude-code` | `~/.claude/skills/` | `.claude/skills/` | `/looks-good-to-ai`, or just ask | [Skills](https://code.claude.com/docs/en/skills) |
| **Codex** | `codex` | `~/.agents/skills/` | `.agents/skills/` | `$looks-good-to-ai`, `/skills`, or just ask | [Build skills](https://learn.chatgpt.com/docs/build-skills) |
| **GitHub Copilot** (VS Code, CLI, coding agent) | `github-copilot` | `~/.copilot/skills/` or `~/.agents/skills/` | `.github/skills/`, `.agents/skills/` or `.claude/skills/` | `/looks-good-to-ai` in VS Code and the CLI; the coding agent loads it when relevant | [VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills), [GitHub](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |
| **Cursor** | `cursor` | `~/.cursor/skills/` or `~/.agents/skills/` | `.cursor/skills/` or `.agents/skills/` | `/looks-good-to-ai`, or just ask | [Skills](https://cursor.com/docs/context/skills) |
| **Gemini CLI** | `gemini-cli` | `~/.gemini/skills/` or `~/.agents/skills/` | `.gemini/skills/` or `.agents/skills/` | Just ask; it asks to activate the skill. `/skills list` shows it | [Skills](https://geminicli.com/docs/cli/skills/) |
| **Antigravity** | `antigravity` | `~/.gemini/config/skills/` | `.agents/skills/` | `/looks-good-to-ai`, or just ask | [Skills](https://antigravity.google/docs/skills.md) |
| **OpenCode** | `opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` (also reads `.claude/skills/`, `.agents/skills/`) | Just ask, or mention `@looks-good-to-ai` | [Skills](https://opencode.ai/docs/skills/) |
| **Windsurf** (docs now under Devin Desktop) | `windsurf` | `~/.config/devin/skills/` or `~/.agents/skills/` | `.devin/skills/`, `.agents/skills/` or `.windsurf/skills/` | `/looks-good-to-ai`, or just ask | [Skills](https://docs.devin.ai/desktop/cascade/skills) |
| **Cline** | `cline` | `~/.cline/skills/` | `.cline/skills/` or `.claude/skills/` | `/looks-good-to-ai`, or just ask | [Skills](https://docs.cline.bot/customization/skills) |
| **Roo Code** | `roo` | `~/.roo/skills/` or `~/.agents/skills/` | `.roo/skills/` or `.agents/skills/` | Just ask (no slash command for skills) | [Skills](https://roocodeinc.github.io/Roo-Code/features/skills) |
| **Kiro** | `kiro-cli` | `~/.kiro/skills/` | `.kiro/skills/` | `/looks-good-to-ai`, or just ask | [Skills](https://kiro.dev/docs/skills/) |
| **Amp** | `amp` | `~/.config/agents/skills/` or `~/.agents/skills/` | `.agents/skills/` | Just ask | [Skills](https://ampcode.com/docs/markdown/customize/skills) |
| **Junie** | `junie` | `~/.junie/skills/` | `.junie/skills/` | `/looks-good-to-ai`, or just ask | [Skills](https://junie.jetbrains.com/docs/agent-skills.html) |
| **Zed** | `zed` | `~/.agents/skills/` | `.agents/skills/` (trusted worktrees only) | The `/` menu, `@looks-good-to-ai`, or just ask | [Skills](https://zed.dev/docs/ai/skills) |

Notes:

- <a id="cline"></a>**Cline.** The skills CLI installs Cline skills to `.agents/skills/`, which [Cline's documentation](https://docs.cline.bot/customization/skills) does not list (it lists `.cline/skills/`, `.clinerules/skills/` and `.claude/skills/`). Copy the folder by hand to `.cline/skills/` or `~/.cline/skills/`.
- **Gemini CLI.** Its documentation carries a notice that, for unpaid and Google One users, Gemini CLI was replaced by Antigravity CLI on 2026-06-18. Use the Antigravity row in that case.
- **Codex.** `agents/openai.yaml` in the skill folder only sets the display name for the Codex and ChatGPT apps. Codex works without it.

## Agents without skill folders

### Aider

Aider has no skill loader. It reads conventions files as read-only context, so load the skill that way. Per session:

```sh
aider --read path/to/looks-good-to-ai/SKILL.md
```

Or for every session, in `.aider.conf.yml`:

```yaml
read: [path/to/looks-good-to-ai/SKILL.md]
```

Then ask: *"Review this diff with the Looks Good to AI workflow."* Aider has no sub-agents, so for Step 1 open a second `aider` session with only the diff and the intent. Source: [Specifying coding conventions](https://aider.chat/docs/usage/conventions.html).

### Continue

**Unverified.** Continue's documentation does not describe skills, although the skills CLI has a `continue` id that installs to `.continue/skills/`. What Continue does document is [rules](https://docs.continue.dev/customize/deep-dives/rules) in `.continue/rules/*.md`. Copy `SKILL.md` there to load it as a rule, and call the workflow by asking for it.

### Anything else

Any agent that reads a Markdown file can follow the workflow: attach or paste `SKILL.md` and ask it to review the diff with it. The method needs a shell with `git` for Step 2 and a second, clean context for Step 1. [`references/subagents.md`](../skills/looks-good-to-ai/references/subagents.md) shows how each agent starts that second context.

## Claude Code plugin

Claude Code can also install the skill as a plugin, which keeps it updated through the marketplace:

```text
/plugin marketplace add laulauraluo/looks-good-to-ai
/plugin install looks-good-to-ai@looks-good-to-ai
```

Source: [Plugins](https://code.claude.com/docs/en/plugins).
