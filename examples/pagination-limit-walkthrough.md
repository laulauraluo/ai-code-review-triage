# Walkthrough: a faster export that silently loses rows

An illustrative review of an invented AI-written PR. The API contract, dataset,
and review below are fictional; the Python reproduction is executable using only
the standard library. This is not a report of a production incident or a measured
skill run.

## The PR

> **Intent:** reduce API requests for the nightly export without losing records.
> **Existing tests:** small datasets and a mock that honors any requested limit.

```diff
 # export/config.py
-PAGE_SIZE = 100
+PAGE_SIZE = 1000
```

The unchanged caller keeps fetching pages until `len(page) < PAGE_SIZE`, then
marks the export complete. The unit tests pass: the mock returns up to 1000 rows,
and the small fixtures fit into one page.

## Step 0 · Triage

**High risk:** a shared constant changes a production data export. A successful
job can produce an incomplete file without raising an exception. Run all steps.

## Step 1 · Catch bugs

A fresh-context reviewer would receive the diff, changed file, and intent. From
those alone, an upstream cap is **PLAUSIBLE**, not confirmed. Passing mock tests
does not establish the real API's pagination contract.

The next check is to inspect the caller and the provider contract. If the reviewer
already does that in Step 1, record the evidence there; Step 2 is a checklist for
missing context, not a claim that only humans can discover this bug.

## Step 2 · Align context

**Magnitude:** `PAGE_SIZE: 100 → 1000 (rows/request)`, a 10× increase. Fewer requests
are possible only if the provider actually supports that page size.

**Neighbors and contract:** in this invented service, the provider silently caps
responses at 100 rows and supplies `next_offset` when more rows remain. The caller
ignores that field. Its old stopping rule only worked because its requested page
size matched the cap. Check provider documentation and a captured response in a
real review; do not assume this contract applies to every API.

**History:** inspect `git log -S'PAGE_SIZE'` and the export caller's history for the
reason behind the old value. No prior revert is assumed in this example.

### Reproduce the contract mismatch

Run from the repository root with Python 3; no credentials or network required:

```bash
python3 - <<'PY'
def api(rows, offset, limit):
    # Fictional provider: cap each response and advertise continuation.
    items = rows[offset:offset + min(limit, 100)]
    end = offset + len(items)
    return {"items": items, "next_offset": end if end < len(rows) else None}

def export(rows, page_size):
    result, offset = [], 0
    while True:
        page = api(rows, offset, page_size)["items"]
        result.extend(page)
        if len(page) < page_size:
            return result
        offset += len(page)

def export_with_continuation(rows, page_size):
    result, offset = [], 0
    while True:
        response = api(rows, offset, page_size)
        result.extend(response["items"])
        if response["next_offset"] is None:
            return result
        offset = response["next_offset"]

small = list(range(20))
assert export(small, 100) == export(small, 1000) == small
rows = list(range(250))
assert export(rows, 100) == rows
assert export(rows, 1000) == rows[:100]  # Reproduces silent truncation.
for count in (0, 20, 99, 100, 101, 200, 250):
    fixture = list(range(count))
    for size in (100, 1000):
        assert export_with_continuation(fixture, size) == fixture
print("small fixture: passes before and after")
print("250-row export: before=250, after=100, missing=150")
print("continuation fix: all 7 dataset sizes pass at both page sizes")
PY
```

**CONFIRMED in this reproduction:** the first response contains 100 rows. Since
`100 < 1000`, the exporter stops with 150 of 250 rows missing. This proves the
failure under the stated contract; confirming a real provider requires evidence
that it behaves the same way.

**Requirement match:** the goal was a complete export with fewer requests. The
changed constant stops early and violates completeness. Following continuation
restores correctness but cannot reduce request count under this provider's cap.

## Step 3 · Own the sign-off

| Question | Answer |
|---|---|
| Can I explain it? | Yes: requested size exceeds the provider cap, so the caller mistakes a capped page for the last page. |
| How would we notice? | Job success alone is insufficient. Reconcile exported IDs/counts against an authoritative snapshot or expected manifest. |
| How do we undo it? | Restore the old size for future runs. Identify incomplete exports and regenerate them from a consistent source; reverting code does not repair files already consumed. |
| Accepted risks | None for silent omission. Real API behavior and concurrent data changes remain unverified. |

**Recommendation: request changes.**

> The reproduction exports only 100 of 250 rows when the provider caps pages at
> 100. Keep the current size until the provider contract is verified, and use its
> documented continuation signal rather than the requested limit to detect the
> last page. Add coverage across the cap boundary. Verified: small-fixture blind
> spot, truncation, and continuation handling in the local model. Not verified:
> real API responses, dataset consistency during export, or performance gains.

## What this adds to the timeout example

No unit conversion is wrong. The failure comes from a constant interacting with
an upstream limit and a caller's stopping rule. Review the contract across that
boundary, and separate a successful job from a complete export.
