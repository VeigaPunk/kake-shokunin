# ExecKey — round 89, wave 1, seat C2 candidate

## Result

The C2 candidate passes the round's counter at the target values, on both counter
versions that exist in the lane:

- **Frozen counter** (`c89_key.py` at freeze commit `08ab46a1`, v1):
  `C2v1 revision=0666fd26… frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true`, exit 0.
- **Current committed counter** (`c89_key.py` at `46a43e94`, "freeze v2", sha `d4588d4b…`):
  same line, `met=true`, exit 0.

Candidate: `.ufo/waves/round-89/w1/ExecKey/cache_key.py`
(copy: `attempt3-final-cache_key.py`, byte-identical). Scored as commit
`0666fd26d62051547130ca02329d858c737e1c36` in a scratch clone (author `t <t@t>`).
Scratch deleted after copying.

Caveat on the claim: met=true is a property of this counter and its seed (89089).
The C2 contract's worked examples and the frozen cases are all satisfied by the
counter's own scoring, but no independent check beyond the counter was run.

## Counter drift: a finding for L1 (not fixed here)

The counter the lane scores with has been changed after the wave was dispatched.

| item | value |
|---|---|
| freeze v1 `c89_key.py` (`08ab46a1`) sha256 | `a72d5efc…` |
| dispatch evidence commit (`2e700b9a`, "w1 dispatch") | counter unchanged |
| freeze v2 `c89_key.py` (`46a43e94`, "freeze v2 — shortcut guard …") sha256 | `d4588d4b…` |

Diff v1→v2 is saved as `counter-drift.diff` (1323 bytes). It changes the textual
shortcut guard:

- `FORBIDDEN` goes from `('c89_key', '.ufo/waves', 'round-89', 'frozen', 'c2-cases', 'oracle')`
  to `('c89_key', 'c89_defect_queue', 'c2-cases')`;
- adds an `open(`-of-`.ufo` line check.

Why this matters for the round's own kill rule: `freeze.md` says the counter is
frozen before data and that item E of C1 measures freeze-after-dispatch (R88-E).
The C2 counter itself changed after `w1.ready.dispatched` was written. My seat
was scored by v2 for attempt 1 (see below) and by both versions for attempt 3,
so the verdict holds under both. But the round's claim "frozen before any
after-state data" is not literally true for the C2 counter, and the commit
message says so. L1 should decide whether v2 is an amendment (and disclosed as
one in `freeze.md`) or should be reverted.

## Counter defects found (for the round's own counter; no edits made to it)

1. **Substring guard false positive.** The guard uses plain `token in text`.
   The v1 token `frozen` matches `frozenset`, so any candidate that uses
   `frozenset` is refused. I hit this on attempt 2 and worked around it by
   writing the token set as a string. v2 removed `frozen` from `FORBIDDEN`, so
   the false positive is gone at the committed revision.
2. **Guard note printed one character per line.** `score_candidate` returns
   `(0, 0, 0, note)` for a guarded candidate. `main` then does
   `for f in fails[:12]: print('fail: ' + f)`, and `fails` is a string, so
   the receipt shows `fail: s`, `fail: h`, … instead of the reason. Seen in
   `receipt2-attempt2-frozen-counter.txt`. Cosmetic, but it hides the reason.
3. **Guard still textual.** The `open(`/`.ufo` check and the token checks are
   text-only, as the freeze already discloses. A candidate that reads files via
   other means, or that re-implements the reference, is not detected. I did
   not exploit this; my candidate reads only stdin.
4. **Control rejection reason depends on the version.** `ctl-table` is rejected
   by `'.ufo/waves'` in v1 and by `'c2-cases'` in v2. Both are shortcut-guard
   rejections, so `controls=5/5` holds either way; noted only as drift.

## Attempt history (all receipts copied to this directory)

| attempt | commit | counter scored | receipt | outcome |
|---|---|---|---|---|
| 1 | `ca5a142e` | counter with the v2 guard, at its then working-tree sha `d4588d4b` (same bytes as `46a43e94`) | `receipt1-attempt1-worktree-counter.txt` | frozen 16/16, props 200/200, refuse 9/9, controls 5/5, met=true, exit 0 (first pass) |
| 2 | `9437236e` | frozen v1 (`08ab46a1`) | `receipt2-attempt2-frozen-counter.txt` | met=false; guard refused the source for `round-89`/`frozen` tokens in my own docstring (not a behaviour failure) |
| 3 (final) | `0666fd26` | frozen v1 **and** v2 | `receipt3-FINAL-frozen-counter.txt`, `receipt3-FINAL-worktree-counter.txt` | met=true, exit 0 under both |

Attempt 2 was not re-scored under v2, since attempt 1 already showed v2 accepts
the same logic. Attempt 1 was not re-scored under v1 (it would fail v1's guard
for the same docstring tokens). Attempt 3 is scored under both.

Attempt 1 and 2 sources are copied as `attempt1-cache_key.py` and
`attempt2-cache_key.py` (from the scratch clone commits, before deletion).
Attempt 1 differs from the final only in the docstring and in the
`frozenset(...)` token table; the logic is the same.

## Selftests

- `selftest-frozen-counter.txt`: `selftest: 43/43 passed`, exit 0 (v1).
- `selftest-worktree-counter.txt`: `selftest: 43/43 passed`, exit 0 (v2 = committed).

## Implementation notes (C2 contract)

- Standard library only; reads one JSON object from stdin; writes
  `{"key": …}\n` on success; `invalid_input: <reason>` on stderr with exit 1
  on refusal; invalid JSON is refused as `invalid_input: input is not valid JSON`.
- Members: split on `,`, trim SP/HTAB, `*` refused, non-token refused, lowercased,
  duplicates refused, sorted. `vary` absent or `""` means no members.
- Header names must be tokens, values must be strings without CR/LF, and
  case-insensitive duplicates are refused. Values are trimmed of SP/HTAB only;
  case is preserved.
- Escaping: `%`→`%25` first, then GS, US, RS and the fourth separator to `%1C`,
  `%1F`, `%1E`, `%1D`, applied to the URI, each name and each value.
- Layout: `ESC(uri) + US + join(US, ESC(name) + RS + (ESC(value) | GS))`, with
  absent fields giving GS and present-empty giving the empty string.
- The candidate contains no import of the counter, no reads of any file under
  `.ufo/waves`, no case table, and none of the counter's FORBIDDEN tokens as
  of attempt 3 (checked with `grep -F` for each v1 token).

## Commands run (exit codes)

- `git clone --shared <lane> clone` (scratch; toplevel asserted before commit).
- `git -C clone commit` ×3 (author/committer `t <t@t>`), attempts 1–3.
- `python3 -B <counter> --root <clone> --revision <rev> --work <scratch>` for
  attempt 1 (v2 bytes, exit 0), attempt 2 (frozen v1, exit 1, guard), attempt 3
  (frozen v1 exit 0; v2 exit 0).
- `python3 -B <counter> --selftest` for v1 and v2 (both exit 0, 43/43).
- `git archive 08ab46a1 .ufo/waves/round-89 | tar -x` to a scratch tree for the
  frozen v1 counter and its controls/cases.
- Read-only git only: `rev-parse`, `show`, `diff`, `log`, `merge-base
  --is-ancestor`, `status`.

## Honest limits

- The counter scores only the ten property classes, 20 cases each, from seed
  89089 plus the 16 frozen cases and 9 refusals. Passing it does not prove
  the candidate is correct on other inputs.
- I did not run any check beyond the counter's own scoring and selftest; no
  external tests were run.
- The C2 claim is key construction only (per the contract's Scope section): no
  claim about storability, freshness, revalidation or serving.

## Tooling

No tool was installed or upgraded. Nothing was installed under `~/.local/bin`,
no pacman use, no network GET, and no credentials touched.

## Copies in this directory

`cache_key.py` (final, same bytes as `attempt3-final-cache_key.py`), the
attempt sources, the receipts listed above, `selftest-*.txt`,
`counter-sha.txt`, `counter-drift.diff`, `revisions.txt`, `SHA256SUMS`.
