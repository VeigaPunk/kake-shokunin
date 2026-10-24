# CriticDoNothingC1 — C1 cheapest do-nothing controls

**Seat:** CriticDoNothingC1 (critic, operability axis)
**Instrument under attack:** `.ufo/waves/round-47/c47_registry_count.py`
**Frozen predicate (verbatim, from the counter docstring, lines 4–12):** "Both round-46 gates are registered and receipted: `python3 -B .ufo/waves/round-47/c47_registry_count.py --root . --revision <commit>` decides: before = at base cd42e3c310ba442e89dde638ba6401adaefaf3e8 neither `scripts/redirect_audit.py` nor `scripts/citation_lint.py` has a SKILL.md gate-registry row nor a committed selftest receipt; after = at the round-47 tip both tools have a gate-registry row and a committed selftest receipt under `.ufo/waves/round-47/verification/` that names the tool path, the tool sha256, the selftest tally and exit=0."

All lane-side runs are read-only (`git show` / `git ls-tree` / `git status` + the counter itself, which shells only those two read-only commands — script lines 73–89). Mutation controls ran in a disposable clone at `/fast/scratch/hyaku/kake-r47/CriticDoNothingC1/lane`, never pushed.

## Baseline scores (verified, not inferred)

| Revision | Command result | Exit |
|---|---|---|
| base `cd42e3c…` | `registry_rows=0/2 receipts=0/2 C1_NOT_MET` | 1 |
| tip `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` | `registry_rows=2/2 receipts=2/2 C1_MET` | 0 |

Supporting facts at base: `git ls-tree -r --name-only cd42e3c .ufo/waves/round-47/verification` → empty, `LS_EXIT=0` (absent dir does not trip `InputError` at line 86 — before-leg evaluates honestly). Base `SKILL.md` contains **zero** occurrences of `redirect_audit`/`citation_lint` in any form (`grep -c` = 0), so the row check is not tripped by legacy tables (base SKILL.md has 21 other `|`-rows naming `scripts/` paths; none name these two tools). At tip, rows 1197–1198 of SKILL.md are real gate-registry rows (`redirect-expectation-audit`, `commit-citation-lint`) and `verification/selftest-{redirect-audit,citation-lint}.txt` exist.

The two committed receipts also pin **correct** shas: `tool_sha256` in each receipt equals `sha256sum` of both the working tree and `git show HEAD:scripts/<tool>` bytes (`1e1dff18…bb748a`, `3c78a0a8…962987f`). So C1's tip verdict is a **true positive** — but the instrument cannot tell it apart from fabrication.

## Control 1 — old LOG prose tallies: DEAD PATH (verified)

The counter reads exactly two artifacts: `SKILL.md` (line 99) and files under `RECEIPT_DIR` (lines 105, 118–119). LOG.md and SCORECARD.md are never opened. Tip LOG.md already carries near-complete receipt prose — e.g. LOG.md:1891 records `` `python3 -B scripts/citation_lint.py --selftest` → `selftest: 8/8 passed`, exit 0 `` and LOG.md:1880/1884 record `(23/23, exit 0, tool sha256 …)` / `(8/8, exit 0, tool sha256 …)` — and correctly contributes **nothing**. Docstring line 18–19 ("Prose tallies in LOG.md/SCORECARD.md are never receipts") is enforced by omission, not parsing. No false green through this path.

## Control 2 — junk tally-only file: FALSE GREEN (falsified, not hypothetical)

Sandbox clone at base `cd42e3c`; one commit adding only:
- `.ufo/waves/round-47/verification/junk.txt` containing `scripts/redirect_audit.py`, `scripts/citation_lint.py`, `selftest: 23/23 passed`, `selftest: 8/8 passed`, `exit=0`, and a **zero-pad** sha `000…000` (not either tool's real digest — no selftest ever ran);
- one appended `SKILL.md` line `| junk-decorative-note | … |` mentioning both `scripts/` paths in a non-registry table.

Result: `registry_rows=2/2 receipts=2/2 C1_MET`, `MUT_EXIT=0`.

Two independent weaknesses make this pass:
1. **Unbound digest.** Line 43 `SHA256_RE = re.compile(r"\b[0-9a-f]{64}\b")` matched against the receipt *file's own text* (line 123) — never compared to `sha256(git show rev:scripts/<tool>)`. Any 64-hex token works; `git show` is never invoked on the tool path.
2. **Unanchored row.** Line 114–116: any line whose lstrip starts with `|` and contains the literal `scripts/<tool>` counts — no table-header anchoring, so a decorative row anywhere in the 130KB SKILL.md suffices. (This yields zero base false-positives today only because the literal path strings are absent at base; it is name-collision luck, not structural resistance.)

Also note receipts accept **any** committed file under the dir — a report/JSON that quotes all four tokens would self-certify. At tip this does not currently collide: per-file grep shows the four needle classes co-occur only in the two `selftest-*.txt` files; the `c1-*.json`/`c2-*.json` counter outputs contain none of the needles (self-certification absent); `c2-r4-mutation.txt`/`census-*.txt` hit sha+`exit=0` only.

## Control 3 — stale-receipt carryover: FALSE GREEN (strongest instrument defect)

Sandbox clone at tip `766f461`; one commit appending `# stale mutation` to `scripts/redirect_audit.py` (tool sha changes `1e1dff18…` → `27826a53…`), receipts untouched. Result: `registry_rows=2/2 receipts=2/2 C1_MET`, `STALE_EXIT=0` — at a revision where the recorded receipt no longer describes the committed tool bytes. Consequence: once any receipt lands, **every later revision containing it scores receipts 2/2 forever** — post-receipt tool edits, including breaking ones, cannot flip C1. The "after" claim is permanent once planted; the sha256 field is decorative.

## Finding

C1's tip verdict is true and its base verdict is honest, but the counter is not a falsifiable gate: two of three do-nothing probes fail to fail.

- **False-green paths:** (a) junk tally-only file + junk `|` row → `C1_MET`; (b) stale receipt surviving tool mutation → `C1_MET`; (c) unanchored `scripts/<tool>` mention in any `|`-line → row credit.
- **Dead path:** LOG/SCORECARD prose tallies — unreachable by construction.
- **Impacted axis:** operability (the claim's *operable gate* property — an instrument that passes fabricated or stale receipts does not verify operability).

**Smallest safe correction (fixable defect, not a tradeoff):** in `main`, compute `sha256(git_show(root, rev, "scripts/<tool>"))` and require the receipt to carry that exact digest (binds sha, kills zero-pad junk AND stale carryover); require receipt filename or first-line `tool_path:` field to name the tool; anchor the row check to the gate-registry table (e.g. require the row under the known table header or match `scripts/<tool>` in an explicit command cell). Canonical judge should reject claims that rest on this counter until the digest is bound; the defect is a one-function patch, not a redesign.

**Not run / caveats:** no lane mutations performed (all controls in scratch clone); counter `--json` flag untested (irrelevant to verdict path); row 1197–1198 full text not needed — substring match confirmed by counter output itself.
