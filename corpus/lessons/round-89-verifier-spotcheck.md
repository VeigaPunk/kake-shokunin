author: hyaku closure (non-author integrator, @m_zfl)
round: kake 89
date: 2026-11-04
report: .ufo/reports/round-89/kake.md
lane_base: 76225160d0dff8d2042fbcd037bd08b0971d5e07
lane_head: a33e20d41a4b13b71b45bb69a5d83c69da6426b4

# Round 89 verifier spot-check — kake (hyaku closure, non-author)

I re-ran the measurements below on committed bytes. I also ran the shipped
candidate `scripts/cache_key.py`, extracted from `a33e20d4`, on stdin payloads
that I wrote. The lane-owned counters `c89_defect_queue.py` and `c89_key.py`
were **not executed**. For those, I read the committed receipts and checked
which revision each one measured (`PROTOCOL.md` §Gate standard, Closure
consequence). I did not author this round and edited no lane-authored file.

## Conformance results

- Report commit `15146cdd46c0c60a87a5b68055eee0afd55e0955`, author
  `kake-shokunin <kake@shokunin.local>`, `2026-11-04 18:51:00 -0300`. It lands
  before the driver's completion line (`18:51:41`). ✓
- Driver digest (copied from the closure prompt):
  `18:04:14 launch attempt=1 pgid=65079`;
  `18:04:46 lane-dead-no-report` (attempt 1 left no report);
  `18:04:48 launch attempt=2 pgid=77853`; `18:51:41 complete attempt=2`.
  The report discloses attempt 1 (line 4).
- The `## SHONEN` heading appears once, with four box lines, all `[~]`.
  `SHONEN.md` did not change between base and tip. ✓
- All 18 cited lane commits resolve, and every one is an ancestor of `master`
  (`git merge-base --is-ancestor <full> master`; 18/18 ok). ✓
- `jj-lane.sh state` reported `branch=master local=remote=a33e20d4… ahead=0 behind=0`, and
  `ls-remote origin refs/heads/master` returned `a33e20d4…`. ✓
- **Defect D89-1 (scratch discipline):** `git status --porcelain` shows one
  untracked file at the lane root, `?? baseclean.out`. Its mtime is
  `2026-11-04 18:20:36 -0300`, inside attempt 2, and it holds census W04
  output. This is round scratch that was left at the lane root.
  Status-neutral.
- Prompt: `.ufo/prompts/kake-round-89.md` (83 362 B) carries template §§1–5,
  the hyaku addendum §6, and §7 scratch discipline. ✓
- The registry rows for `cache_key` (probe), `c89 defect queue` (gate) and
  `c89 key capability` (gate) are in `SKILL.md`, which is the lane's
  registry home. ✓

## Per-claim re-check

The tip was measured at `93475f7e`. `a33e20d4` adds receipts only:
`git diff --stat 93475f7e a33e20d4` lists four files under `controls/final2-*`.

| Claim | Reported | Re-check (mine) | Mode |
|---|---|---|---|
| C1 six routed r88 defects close | `open=6 closed=0` → `open=1 closed=5 met=false` | `controls/base-c1.txt` line 1: `revision=76225160… open=6 closed=0 met=false`. `controls/final2-c1-at-tip.txt` line 1: `revision=93475f7e… open=1 closed=5 met=false`. Item A still lists `SCORECARD.md:5469`, `:5488` and `round-88.md:265`. Selftest receipt: `selftest: 12/12 passed`. The lane's own wave review says the counter is unsound: RC-1…RC-10, and CriticClaims found that a mirror control reaches `met=true`. | evidence-verified; predicate **not met** |
| C2 Vary-nominated cache-key constructor | absent → `frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true` (v1 and v2) | `base-c2.txt` line 1 reads `candidate absent … met=false`. `final2-c2-at-tip.txt` and `final2-c2-frozen-v1-at-tip.txt` line 1 read `revision=93475f7e… 16/16 200/200 9/9 5/5 met=true`. Selftest receipt: `43/43 passed`. `git ls-tree a33e20d4 scripts/cache_key.py` → blob `13ea9374`. The counter admits non-conforming stubs (ReviewCounterC2, ExecControls: seven uncovered clauses), so `met=true` does not establish conformance. | evidence-verified, plus my own probes of the candidate (below) |
| Registry/knowledge counts | 201→202 rows, tier A 176→177, knowledge 76→77 | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` gives 201 → 202. The tier-A filter gives 176 → 177. `git ls-tree -r --name-only <rev> -- corpus/knowledge \| grep -c '\.md$'` gives 76 → 77. | re-measured, matches |

Candidate probes. I wrote eight stdin payloads and ran them against
`git show a33e20d4:scripts/cache_key.py`. All eight results conform to
`c2-contract.md`:
- `%` in the URI becomes `%25`.
- A value is SP-trimmed and otherwise byte-exact.
- An absent field gives `RS GS`, while an empty value gives `RS` alone, so the two are distinct keys.
- A case-duplicate header name is refused with exit 1.
- CR in a *non-nominated* header value is refused with exit 1.
- `Vary: *` is refused with exit 1.
- `Vary: a,` is refused with exit 1.
- Members are sorted by lowercased name: `vary:"b, A"` gives `a…2`, then `b…1`.

Eight probes cover only part of the contract. They do not close the seven
contract clauses that have no coverage.

**No-harm check.** `git diff --numstat 76225160 a33e20d4` gives:

| File | Added | Deleted |
|---|---|---|
| `SCORECARD.md` | 46 | 0 |
| `LOG.md` | 57 | 0 |
| `PROVINCE.md` | 11 | 0 |
| `SKILL.md` | 3 | 0 |
| `corpus/README.md` | 1 | 0 |
| `corpus/lessons/round-88.md` | 16 | 0 |
| `corpus/SOURCES.md` | 2 | 1 |

The one deleted line is the S463 row: only its `used-by` value changed, and the
lesson's §Registry logs the old → new value. No file was deleted, and
`SHONEN.md` and `corpus/QUALITY.md` are unchanged. The SCORECARD change only
appends a round-89 section, and every owned score stays at HOLD. No owned axis
is harmed.

**Defect D89-2 (ledger inconsistency):** `SCORECARD.md` (round-89 C1 row and
move log) and `LOG.md:3040` both state C1 as `open=5 closed=1` at
`f62e7954`. However:
- `SCORECARD.md` also says "items B, C, D, E, F closed", which would be
  `closed=5`, not `closed=1`.
- No committed receipt measures C1 at `f62e7954`. The C1 receipts are
  `base-c1`, `final-c1-at-tip` at `658f72f8` (`open=1`) and `final2-c1-at-tip`
  at `93475f7e` (`open=1`).
- The report states `open=1 closed=5` at the tip.

Round 90 should append a correction tail that names a receipted revision.

**Defect D89-3 (scope column):** The S463 row's scope still reads "not
cache-key construction". Its `used-by` now includes
`cache-key-construction.md`, and the lesson admits §4.1 as the construction
ground. Round 90 should reconcile this with a superseding note; filed bytes are
not to be rewritten.

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| calibration (C1) | unchanged | The frozen predicate is `met ⇔ open==0`, and the tip reads `open=1`, so the claim fails on its own instrument. The instrument is also unsound (RC-1…RC-10). The score stays 2 HOLD. |
| freshness (C2, bounded capability; axis label disputed by CriticClaims) | unprovable-but-better | The capability is real: a 132-line stdlib constructor, grounded in S463 and S465, conformed on 8/8 of my probes. The counter cannot prove it, because it admits reference copies, import shortcuts and hybrid tables, and seven clauses have no coverage. As the non-author reviewer, I judge it better but not proven. |

## Spot-check (`corpus/lessons/round-89.md` `## Gate`, all four rows sampled)

Both URLs were re-fetched on 2026-11-04. Both returned HTTP 200.
- `rfc9111.txt`: 84 477 B, sha256 `aeb52adb…302cf3e`.
- `rfc9110.txt`: 502 941 B, sha256 `21c1cdce…ff47232a`.

Both match the lesson digests byte for byte.

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| RFC 9111 §4.1 as the key-construction ground (S463) | admit, A, scope-limited | `rfc9111.txt` line 526 title "4.1. Calculating Cache Keys with the Vary Header Field"; line 530 begins "…the cache MUST NOT use that stored" and the sentence continues as quoted | agree | The title and the reuse condition support the construction half only, as the lesson scopes it. |
| RFC 9110 §5.6.2 token alphabet (S465) | admit, A, scope-limited | `rfc9110.txt` line 1730 "Tokens are short textual identifiers that do not include whitespace" / 1731 "or delimiters." | agree | The quote is verbatim (12 words), and the `tchar` production at 1734–1737 grounds the refusal alphabet. |
| "the C2 pass shows the reader implements RFC 9111 §4.1" | reject (proposition) | `rfc9111.txt` §4.1, lines 528–533 | agree | §4.1 conditions reuse but specifies no byte layout. The escaping, separators and absent marker are adapter conventions, and the counter's weakness (ReviewCounterC2) strengthens the rejection. |
| "refusing `Vary: a,` is an RFC requirement" | reject (proposition) | `rfc9110.txt` line 1696 "recipient MUST parse and ignore a reasonable number of empty list" | agree | The RFC says to ignore empty elements. The candidate refuses `Vary: a,` (my probe, exit 1), which is a lane convention, as the lesson says. |

New `corpus/SOURCES.md` row S465, re-opened:
- Its anchor cites plain-text lines 1730–1738 and 1695–1699, a fetch at
  21:16:52Z, and sha256 `21c1cdce…`. Lines and digest match my fetch.
- The row has no quote column. Its `teaches` field is a paraphrase consistent
  with the source.
- The lesson's ≤25-word quote for S465 (12 words) is verbatim at line 1730.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
exited 0 with `kake ok …/corpus/SOURCES.md` and 26 × W04. The base had 25 × W04.
The new W04 is S465's rfc9110.txt URL, which is shared with S033 across scopes.

## Trend verdicts

- **expansion: unprovable-but-better.** One new knowledge entry,
  `cache-key-construction.md`, is on ground the coverage map did not hold, and
  it cites mined tier-A rows S463 and S465. The registry grew 201 → 202 and the
  census is clean. The round is not admitted, so the entry is not an admitted
  expansion.
- **quality: unchanged.** Corrections were appended as tails: round-88 stale
  S463 statements (`2342c3a4`) and tagged tails. No filed bytes were rewritten.
  D89-3 is a minor scope-column tension, not a false entry.
- **discernment: unchanged.** The outside spot-check agrees with the gate on
  4/4 sampled items (2 admits, 2 rejects). On its own that would read as
  improved. It is offset by first-draft `met` verdicts on two unsound
  instruments. The lane's wave review caught both, the lesson §Wave review
  recorded them, and they were routed, so the disagreement is not left
  unlearned. However, no grounded `QUALITY.md` criterion was added.

## Routed defects (lane fixes next round)

- D89-1: remove or relocate the untracked `baseclean.out` at the lane root,
  and keep round scratch out of the lane root.
- D89-2: append a correction for the SCORECARD/LOG C1 `open=5 closed=1 @f62e7954`
  rows. They are unreceipted, and their item list contradicts their count.
- D89-3: the S463 scope column conflicts with its new construction use.
  Supersede it by note.
- Carried from the lane's own routing: R89-1 and RC-1…RC-10 (C1 counter); the
  seven uncovered C2 contract clauses; a C2 shortcut guard that runs in an
  execution-time sandbox; property classes that assert key strings; the
  U+001D/"four separators" contract wording (the contract names three
  separators in the layout); the C2 axis label; the MutKey survivors.
- Turn the instrument-calibration lesson (two first-draft `met` verdicts
  falsified by the round's own attack seats) into a grounded `QUALITY.md`
  criterion.
