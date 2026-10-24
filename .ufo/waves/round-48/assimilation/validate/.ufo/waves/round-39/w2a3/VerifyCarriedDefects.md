# Kake R39 W2 — VerifyCarriedDefects (re-check of ScribeCarriedDefects' ten carried items)

Axes: operability; freshness. Review target: ScribeCarriedDefects (wave 1) carried list, ten items, re-checked at lane tip. The tip moved during review: review opened at `77b2a86`; judged against final HEAD **`d8a20a99`** (parent chain includes `b78a1ea`, which commits the `source_recheck` (g) repair; `f2b70119`, which adds +10 robots selftest fixtures). Sandbox extraction of the tip tree: `/fast/scratch/hyaku/kake-r39a3w2/VerifyCarriedDefects`.

Verdicts per attacked statement (state at `d8a20a99`):

1. **source_recheck oversized body emits `moved`+`check_invalid` — wrong at tip (fixed).** Commit `b78a1ea`; `scripts/source_recheck.py:587-592` (docstring), `:617-620` (`return None` on over-cap/read fault), `:762-766` (one `check_invalid`, uncounted). `timeout 300s prlimit --as=4000000000 python3 -B scripts/source_recheck_hardening_selftest.py` → exit 0, 10/10, incl. fixture g36 (`:24,233,248`). Pointer `w2/ReviewRecheckCaps.md:7,11` now describes pre-fix behavior.
2. **Lone-surrogate URL — holds (open/underspecified).** `scripts/robots_audit.py:196-200` still `surrogatepass`; contract silent (SCORECARD `:1842-43`, `:2152-57`). Probe manifest `{"url":"http://x/\ud800","robotsStatus":400,"expect":"allow"}` → `clean`, `checksEvaluated:1`, exit 0 (independent rejects; no pin added in `f2b70119`).
3. **Bracket host — holds.** `scripts/robots_audit.py:513-531` unchanged; probe `https://[not-ipv6]/p` (status 400, expect allow) → `could-not-evaluate`, `check_invalid`, exit 2. Contract only demands non-empty host (`SCORECARD.md:1808`); no fixture/decision added.
4. **S011 cited outside scope — holds.** `corpus/SOURCES.md:19` scope unchanged (host-root, §§2.3/2.3.1.4); `corpus/knowledge/robots-txt-rules.md:31,33,49,57-63,69,77` still cite S011 for §§2.2/2.5; `corpus/lessons/round-38.md:132-134` still says carried. (S099 row exists at SOURCES `:107`, supersedes S011; entry not updated.)
5. **Symlinked manifest directory — holds (undecided).** `SCORECARD.md:2055` mentions the split only; `w1/ScoutPlanWalk.md:33` still "Carried; still undecided"; `scripts/robots_audit.py:550` still `realpath`; selftest symlink fixtures are manifest-internal files (f23/f24, `:719-727`), no parent-directory fixture.
6. **U+FFFD per invalid byte — holds.** `SCORECARD.md:1819` "invalid bytes becoming U+FFFD"; `scripts/robots_audit.py:213` `errors="replace"` — cardinality is per maximal subpart (`b"\xe2\x82"` → 1 U+FFFD; `b"\xe0\x80"` → 2). Selftest pins only single `\xff` (`:368,492,758`); the only multi-byte fixture covers a valid BOM (`\xef\xbb\xbf`, `:360`). No multi-byte malformed pin.
7. **Duplicate JSON member names — holds.** `scripts/robots_audit.py:464-466` `json.loads` without `object_pairs_hook`; `SCORECARD.md:2257` still "undecided and untested".
8. **Counter harm receipts lack `toolRevision` — holds.** `.ufo/waves/round-38/verification/harm/r36-counter-on-145a6468-tool.json` and `r37-counter-on-3ed8e15c-tool.json` unchanged (toolFile/toolSha256 only; no revision). Round-39 harm dir holds only `.txt`/`.patch` (recheck-hardening/recheck-selftest/robots-selftest); no regenerated counter receipts.
9. **`pinned_selftest.py` runner forgeable — holds.** `.ufo/waves/round-38/pinned_selftest.py:286-308`: `receipt.update(summary)` then pin block re-sets pins but never restores `runner`; `w2/ReviewPinnedSelftest.md:31` evidence unchanged.
10. **Timeline receipts omit invocation — holds.** `.ufo/waves/round-38/criteria/receipts/timeline-r38.txt:1-15` result blocks only (no repo/argv/wave/receipt paths); `w2/ReviewTimelineCheck.md:62-66` unchanged. No round-39 criteria receipts exist yet.

Checks/evidence:
- `git rev-parse HEAD` → `d8a20a99`; `git diff --stat 72edf212..HEAD` for the ten pointer files: only `corpus/SOURCES.md` (+5) and `scripts/robots_audit_selftest.py` (+89) changed; `robots_audit.py`, `pinned_selftest.py`, `timeline-r38.txt`, `w1/w2` reports unchanged.
- Tip artifact sha256: `robots_audit.py` `f4d057c4…baace`; `source_recheck.py` `2ce8c0d9…` (fixed); `robots_audit_selftest.py` `ea069396f5…`; `SCORECARD.md` `61f9b95f0d…`; `timeline-r38.txt` `2622ae135c…`.
- Commands above all ran with `timeout`/`prlimit`; probes under sandbox; no network; no builds; no counter; no lane mutation.

Residual risk/gaps: item 1 fix verified only via selftest (g36) and code reading, not a fresh oversized-body CLI run; source_recheck hardening selftest includes the post-fix contract. Items 2,3,6 depend on unchanged code; spot-probes confirmed.

Report: `.ufo/waves/round-39/w2a3/VerifyCarriedDefects.md`
