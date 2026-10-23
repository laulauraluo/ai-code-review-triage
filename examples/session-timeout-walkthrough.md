# Walkthrough: the "harmless" timeout change

An illustrative, end-to-end run of the skill on a small AI-written PR. The code is invented. The failure pattern shows up in real incidents all the time.

## The PR

> **Title:** Extend session lifetime for "remember me" users
> **Author:** coding agent · **Tests:** ✅ all passing · **Diff:** +3 −1

```diff
 # auth/config.py
-SESSION_TIMEOUT = 30          # minutes
+SESSION_TIMEOUT = 30000       # extended for remember-me
```

```diff
 # auth/session.py
 def is_expired(session, now_ms):
-    return now_ms - session.created_ms > SESSION_TIMEOUT * 60 * 1000
+    return now_ms - session.created_ms > SESSION_TIMEOUT
```

The code is clean, it's short, and the tests pass. A line-by-line reader approves it in 30 seconds.

## Step 0 · Triage

- **Intent:** let "remember me" sessions last longer.
- **Touches:** an auth constant and expiry logic → **High** risk (auth behavior, every user, hard to notice). Run all three steps.

## Step 1 · Catch bugs (fresh-context sub-agent)

The sub-agent gets only the diff, the two files, and the intent. It reports:

- `[PLAUSIBLE] auth/session.py:3` — the unit conversion (`* 60 * 1000`) was removed, so `SESSION_TIMEOUT` is now compared directly against milliseconds. Unconfirmed: no test covers expiry near the boundary.

Adding a boundary test turns it into a confirmed bug:

```python
def test_session_expires_after_timeout():
    s = Session(created_ms=0)
    assert is_expired(s, now_ms=31_000)   # 31 s later: expired under the new code
```

`[CONFIRMED]` Sessions now expire after **30 seconds**, not longer. The existing tests never crossed the boundary, so they passed.

## Step 2 · Align context

**Magnitudes**

```
SESSION_TIMEOUT: 30 → 30000 (comment says minutes; code now treats it as ms)
  as minutes: 30000 min ≈ 20.8 days  → plausible for remember-me? arguable
  as ms:      30000 ms  = 30 s       → logs every user out mid-session
```

Neither reading matches the stated intent cleanly. The comment, the value, and the code disagree.

**History and neighbors**

```bash
git log -S'SESSION_TIMEOUT' --oneline
#   a1b2c3d Revert "Increase session timeout"   ← tried before, rolled back
grep -rn 'SESSION_TIMEOUT\|sessionTimeout' .
#   mobile/src/config.ts: const sessionTimeout = 30 * 60   ← client hard-codes the old value
```

- A previous attempt was reverted. Why? (Ask before repeating it.)
- The mobile client keeps its own copy and will disagree with the server.

**Requirement match:** the request was longer sessions *for remember-me users*. The diff changes the timeout for *everyone*.

None of these findings come from reading the diff. They come from units, history, and callers.

## Step 3 · Own the sign-off

| Question | Answer |
|---|---|
| Can I explain it? | No: the value, unit, and scope don't match the intent |
| How would we notice? | Login-rate and 401-rate alerts exist |
| How do we undo it? | Config-only revert, but every logged-out user has to log in again |
| Accepted risks | None at this point |

**Recommendation: request changes.**

> Unit conversion was dropped in `is_expired` (confirmed by a boundary test). The change applies to all users, not only remember-me. The mobile client hard-codes 30 min. A prior attempt was reverted in a1b2c3d, so please link the reason. Verified: units, callers, history. Not verified: load behavior with longer sessions.

## What the skill changed

| Line-by-line review | Triage review |
|---|---|
| "Short diff, tests pass, LGTM" | 1 confirmed bug, 3 context issues, scoped decision |
| Approver can't say what they checked | Approval comment states what was and wasn't verified |
