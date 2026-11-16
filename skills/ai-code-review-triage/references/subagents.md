# Starting a fresh-context reviewer

Step 1 needs a reviewer that has not seen the conversation that produced the code. Most agents can start one in their own context window. Give it three things only: the diff, the files it touches, and the one-sentence intent from Step 0. Use a neutral prompt such as:

```text
Find bugs in this diff. For each one, give the file and line, a concrete failure scenario, and a test or command that would show it. Intent: <one sentence>.
```

| Agent | How to start the reviewer | Source |
|---|---|---|
| Claude Code | The Agent tool (a sub-agent). Asking "use a sub-agent to review this diff" is enough. | [Sub-agents](https://code.claude.com/docs/en/sub-agents) |
| Codex | Ask in the prompt ("spawn an agent to review this diff"), or define a custom agent as TOML in `.codex/agents/`. Sub-agents inherit the parent's sandbox and approval settings. | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) |
| GitHub Copilot (VS Code) | Ask it to delegate the review to a subagent, or define a custom agent in `.github/agents/*.agent.md`. The subagent works in its own context. | [Subagents](https://code.visualstudio.com/docs/copilot/agents/subagents) |
| GitHub Copilot CLI | `/agent` or `--agent=<name>` with a custom agent in `.github/agents/` or `~/.copilot/agents/`. It also ships a code-review agent. | [Use Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli) |
| Cursor | A subagent in `.cursor/agents/` (set `readonly: true` for a reviewer). Subagents start with a clean context. | [Subagents](https://cursor.com/docs/context/subagents) |
| Gemini CLI | A subagent in `.gemini/agents/*.md`. Name it in your prompt to force the delegation. | [Subagents](https://geminicli.com/docs/core/subagents/) |
| Antigravity | A subagent in `.agents/agents/<name>.md`, started by the parent agent. | [Subagents](https://antigravity.google/docs/subagents) |
| OpenCode | An agent with `mode: subagent` in `.opencode/agents/`, or the built-in `general` agent. It runs in a child session. | [Agents](https://opencode.ai/docs/agents/) |
| Cline | `spawn_agent`, in the CLI and desktop app (not the VS Code extension). | [Subagents](https://docs.cline.bot/features/subagents) |
| Roo Code | Orchestrator mode with `new_task`. The subtask has its own history and returns a summary. | [Boomerang tasks](https://roocodeinc.github.io/Roo-Code/features/boomerang-tasks) |
| Kiro | A custom agent in `.kiro/agents/`: "Use the code-reviewer agent to …". | [Subagents](https://kiro.dev/docs/custom-agents/subagents/) |
| Amp | A Task subagent, which has its own context and a read-only role for reviewing a change. | [Models and subagents](https://ampcode.com/docs/markdown/models-and-subagents) |
| Junie | A subagent in `.junie/agents/*.md`; `permissionMode: plan` keeps it read-only. | [Subagents](https://junie.jetbrains.com/docs/junie-cli-subagents.html) |
| Windsurf, Zed, Aider, Continue | No documented sub-agent we could verify. Open a new chat or session and paste in only the diff, the files and the intent. | — |

Two rules hold everywhere:

- **The session that wrote the code is never the independent reviewer.** If you are that session, delegate or hand off.
- **A sub-agent that inherits the whole conversation is not fresh.** Some agents can fork the current context; for Step 1, start a clean one.
