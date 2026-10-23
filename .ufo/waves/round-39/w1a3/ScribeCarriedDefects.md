Key-blindness incident: an accidental read-only `git ls-tree` listing printed `.ufo/waves/round-38/sealed/cases.json`; it was not opened/read and no counter ran. This is disclosed; I avoided further broad listings.

Axes: operability; freshness. Scope: defect 6, ten carried items, assessed at lane revision `72edf2123f92b9dc546494cbffcc777ed3c3cd3a`.

Behavior: all ten remain open at that revision. Findings and smallest fixes are grounded in committed source/review artifacts; the complete draft is `/fast/scratch/hyaku/kake-r39a3w1/ScribeCarriedDefects/carried.md` (SHA-256 `398a70a1de354eed47e1c885c69cdf251cbe4e8e355ca5ad1ba8e5fb3b302e50`).

| # | Status | Pointer | Smallest fix |
|---|---|---|---|
| 1 Oversized recheck body | Open | `scripts/source_recheck.py:587-613,750-756`; `w2/ReviewRecheckCaps.md:7,11` | Body-invalid result must be only `check_invalid`, and excluded from `checksEvaluated`; pin redirect+oversize case. |
| 2 Lone-surrogate URL | Open / underspecified | `w2/DiffToolVsIndependent.md:8-19`; `scripts/robots_audit.py:196-200` | Specify reject-vs-encode in contract and pin it in selftest/key. |
| 3 Bracket host | Open | `w2/ReviewToolDiff.md:7,23`; `SCORECARD.md:1807-1809`; `scripts/robots_audit.py:513-531` | Align parser with non-empty-host rule or explicitly tighten contract; pin bracket case. |
| 4 S011 scope | Open | `corpus/SOURCES.md:19`; `corpus/knowledge/robots-txt-rules.md:31,33,49,57-63,69,77`; `corpus/lessons/round-38.md:132-134` | Replace citations outside S011's registered scope with S099 where supported. |
| 5 Symlinked manifest directory | Open / undecided | `SCORECARD.md:2054-2055`; `w1/ScoutPlanWalk.md:33`; `scripts/robots_audit.py:550` | Declare allow/reject behavior and add a symlinked-parent fixture. |
| 6 U+FFFD per byte | Open | `SCORECARD.md:1819`; `scripts/robots_audit.py:213`; `scripts/robots_audit_selftest.py:333-336,457-460`; `w1/ScoutPlanWalk.md:27` | Specify/source replacement cardinality, then pin a multi-byte malformed sequence. |
| 7 Duplicate JSON names | Open / undecided | `SCORECARD.md:2257`; `scripts/robots_audit.py:464-466`; `w2/ReviewKnowledgeEntry.md:34` | Reject duplicate object members with an `object_pairs_hook` and pin `input_invalid`. |
| 8 Counter harm receipt revisions | Open | `.ufo/waves/round-38/verification/harm/r36-counter-on-145a6468-tool.json:5-7`; `r37-counter-on-3ed8e15c-tool.json:5-7`; `w2/ReviewPinnedSelftest.md:20-23,41` | Regenerate both receipts with `toolRevision` and generator support. |
| 9 Forgeable runner field | Open | `.ufo/waves/round-38/pinned_selftest.py:286-305`; `w2/ReviewPinnedSelftest.md:31` | Restore `runner = RUNNER` after summary merge; pin hostile-summary case. |
| 10 Timeline receipts omit invocation | Open | `.ufo/waves/round-38/criteria/receipts/timeline-r38.txt:1-15`; `w2/ReviewTimelineCheck.md:62-66` | Record exact argv, repo, wave directory and receipt path with each result. |

Gates: read-only review only. No product-code changes, build, tests, counter, network requests, or installs. No round verdict. The working-copy files cited above matched the requested revision in the listed-path `git diff --quiet` check.

Commands run (exact; exits):
- `timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin ls-tree --name-only 72edf2123f92b9dc546494cbffcc777ed3c3cd3a` — 0.
- `timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 72edf2123f92b9dc546494cbffcc777ed3c3cd3a:corpus/lessons/round-38-verifier-spotcheck.md` — 0; confirms the ten items at lines 181-185.
- `timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin ls-tree -r --name-only 72edf2123f92b9dc546494cbffcc777ed3c3cd3a .ufo/waves/round-38` — 0; this is the accidental listing disclosed above.
- `timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin ls-tree -r --name-only 72edf2123f92b9dc546494cbffcc777ed3c3cd3a scripts` — 0.
- `timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --quiet 72edf2123f92b9dc546494cbffcc777ed3c3cd3a -- corpus/lessons/round-38-verifier-spotcheck.md corpus/lessons/round-38.md corpus/SOURCES.md corpus/knowledge/robots-txt-rules.md scripts/robots_audit.py scripts/robots_audit_selftest.py scripts/source_recheck.py scripts/source_recheck_hardening_selftest.py .ufo/waves/round-38/w1/ScoutPlanWalk.md .ufo/waves/round-38/w2/ReviewRecheckCaps.md .ufo/waves/round-38/w2/ReviewToolDiff.md .ufo/waves/round-38/w2/DiffToolVsIndependent.md .ufo/waves/round-38/w2/ReviewPinnedSelftest.md .ufo/waves/round-38/w2/ReviewTimelineCheck.md .ufo/waves/round-38/w2/ReviewKnowledgeEntry.md .ufo/waves/round-38/criteria/receipts/timeline-r38.txt .ufo/waves/round-38/verification/harm/r36-counter-on-145a6468-tool.json .ufo/waves/round-38/verification/harm/r37-counter-on-3ed8e15c-tool.json` — 0 (no differences).
- `timeout 20s mkdir -p /fast/scratch/hyaku/kake-r39a3w1/ScribeCarriedDefects` — 0.
- `timeout 20s sha256sum /fast/scratch/hyaku/kake-r39a3w1/ScribeCarriedDefects/carried.md` — 0; hash above.

Affected surfaces: read-only review of lane sources, lessons, receipts and review reports; writes only the sandbox draft and this scoped report. No tools installed or updated.

Report: `.ufo/waves/round-39/w1a3/ScribeCarriedDefects.md`