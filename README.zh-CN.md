<div align="center">

# AI Code Review Triage

**AI 写代码比你读得快。别再硬读了，换个方式 review。**

一个 [Claude Code](https://claude.com/claude-code) skill：把「读代码」拆成三件事，专门用来 review AI 写的 PR。

[English](README.md) · **简体中文**

<img src="assets/social-preview.png" alt="AI Code Review Triage: catch bugs, align context, own the sign-off" width="760">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-skill-d97757)

</div>

---

## 问题

Agent 提 PR 的速度远超人逐行 review 的速度。更麻烦的是，读得再认真也不一定有用：AI 写的代码表面很整齐，真正的问题藏得深，逐行读完也看不出来。「不读，出事就回滚」技术上可行，但出了事背锅的还是人。

## 思路

「review 代码」一直混着三件不同的事。代码来得慢的时候，混着做没问题；到了 agent 的速度，每件事都需要自己的流程：

| 事情 | 回答什么问题 | 谁最擅长 |
|---|---|---|
| **挑错** | 代码写错了吗？ | 机器，并且要有*独立*的第二遍 |
| **对齐上下文** | 这个改动放在这个产品、这个时间点，对吗？ | 人，从 diff 看不到的角度核对 |
| **担责** | 我愿意在上面签字吗？ | approve 的人，并写明核对范围 |

低风险 PR 只跑第一步；高风险 PR（线上行为、数据、安全、钱）三步全跑。

## 一个例子

> 一个 PR 把 `SESSION_TIMEOUT = 30` 改成 `30000`，测试全过，代码很干净。
>
> - **挑错**：独立的 sub-agent 补了一个边界测试，发现单位换算被删了，session 30 秒就过期。
> - **对齐上下文**：查历史，同样的改动之前被 revert 过；移动端还写死着旧值；而且需求只要求 remember-me 用户，diff 却改了所有人。
> - **担责**：说不清这个 PR 到底改了什么，就不签。
>
> 完整过程见 [examples/session-timeout-walkthrough.md](examples/session-timeout-walkthrough.md)。

## 安装

**作为 plugin**（在 Claude Code 里）：

```
/plugin marketplace add laulauraluo/ai-code-review-triage
/plugin install ai-code-review-triage@ai-code-review-triage
```

**作为单独的 skill：**

```bash
git clone https://github.com/laulauraluo/ai-code-review-triage.git
cp -r ai-code-review-triage/skills/ai-code-review-triage ~/.claude/skills/
```

## 用法

直接对 Claude Code 说：

- 「帮我 review 这个 AI 写的 PR，看能不能 merge」
- 「我要 approve #123 了，签字前该核对什么？」

skill 会自动触发，输出一份三段式报告：挑错 / 上下文 / 签字。

## License

[MIT](LICENSE)

---

如果它帮你拦下过一次坏的 merge，点个 ⭐ 能让更多人看到它。
