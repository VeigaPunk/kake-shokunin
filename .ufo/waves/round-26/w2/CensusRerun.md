# CensusRerun — round-26 C1 freshness falsification (lane: kake)

**Verdict: AGREE** (no defect found in scope). The census rerun reproduces `census-before.txt`
byte-for-byte with exit 0, and the new round-26 search-log paragraph introduces **no** census
hazard (no E01 pipes, no row-shaped lines, no E12 candidate, no change to registry parse).

Scope of this item: run the fleet census against the candidate tree, compare with the recorded
"before" baseline, and audit the new `## Search log` paragraph for census hazards.
Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.

---

## 1. Exact command, output and exit

```
$ cd /home/vgpnk/Projects/shokunin
$ ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake; echo "exit=$?"
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
exit=0
```

Exactly two stdout lines, exit status **0** (no E-code ⇒ `findings=0`; lane not `unlisted`;
registry present so no exit-2 path). No stderr output.

Census mode (same tree, for row-count invariance):

```
$ ./scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake; echo "census exit=$?"
kake	rows	35
kake	tier.A	33
kake	tier.C	2
kake	status.mined	31
kake	status.queued	2
kake	status.rejected	2
FLEET	rows	35
FLEET	tier.A	33
FLEET	tier.B	0
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	2
FLEET	status.mined	31
FLEET	status.rejected	2
FLEET	status.invalid	0
FLEET	missing	0
census exit=0
```

## 2. Comparison with `.ufo/waves/round-26/census-before.txt`

Baseline file (3 lines, whole content):

```
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
exit=0
```

```
$ printf '%s\n' "$OUT" | diff - <(grep -v '^exit=' kake-shokunin/.ufo/waves/round-26/census-before.txt)
IDENTICAL (content)      # diff produced no output
```

The rerun's stdout is byte-identical to the recorded baseline, and the baseline's recorded
`exit=0` matches the observed exit 0. `od -c` on the baseline confirms it is exactly
`<W04 line>\n<ok line>\nexit=0\n` (232 bytes) — i.e. the baseline is a faithful record of the
same validate mode, not of a different mode or a different lane.

**Baseline provenance check** — is `census-before.txt` a true "before" of the candidate, or
merely a copy of the candidate's own output? Resolved by re-running the *script's own* registry
parser over the **base** file and over the **candidate** file and diffing. The parser program was
extracted verbatim from `scripts/sources-census.sh` (`row_pass()`'s gawk body, 5114 chars) and
piped via process substitution — no file was written and no lane/git state was touched:

```
$ gawk -F'|' -v lane=kake -v mode=validate -v today_s=$TODAY_S -f <(extract) \
      <(git show 97404de4...:corpus/SOURCES.md)
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
$ gawk ... -f <(extract) corpus/SOURCES.md          # candidate working tree
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
$ diff <(gawk ... base) <(gawk ... candidate)
NO PARSE-DIFF (base == candidate)
```

So the base tree and the candidate tree yield **identical** census parses: the W04 finding is
pre-existing at base (S028 and S033 share `www.rfc-editor.org/rfc/rfc9110.txt` across scopes),
and round-26 changed nothing the census can see. Working tree is clean against the candidate
commit for `corpus/` (`git status --short` lists only untracked `.ufo/waves/round-26/**` wave
artifacts), so the census saw exactly candidate bytes.

**Tooling provenance** (same for baseline and rerun): `scripts/sources-census.sh` working-tree
blob `3f314620b2395eeb70d8405410132027dfe608e4` == `HEAD:scripts/sources-census.sh`; last change
`6a1dd8c` (2026-10-19, "ops: vendor canonical e737d2e…"), i.e. **unchanged across round 26**, so
the baseline and this rerun were produced by the same parser. `scripts/` is not dirty in the
fleet repo. Interpreter: GNU Awk 5.4.1, bash 5.3.20(1), UTC date `2026-10-21` (census `--today`
default, used for the E08 "opened in the future" test; all rows opened `2026-10-21` ⇒ not future).
**No packages were installed or upgraded** for this item (the census toolchain was already
present; nothing was missing).

## 3. Census-hazard audit of the new search-log paragraph

The paragraph added by the candidate is exactly one line — `corpus/SOURCES.md:79`, inside
`## Search log` (heading at `:57`), i.e. **outside** the `## Registry` section (`:5`–`:43`):

```
$ git diff 97404de4... e28312b1... -- corpus/SOURCES.md
corpus/SOURCES.md | 2 ++
1 file changed, 2 insertions(+), 0 deletions(-)
  @@ -76,6 +76,8 @@
  +Round 26 bounded recheck (2026-10-21): do the 32 previously opened external rows …
  +
```

Hazard rules taken from the script itself (`scripts/sources-census.sh`, `row_pass()` gawk body):

* **E01** (`fields=%d`, malformed row) is reachable **only** for a line that (a) starts with
  `^ {0,3}\|` and (b) is inside the `## Registry` section — `if (line !~ /^ {0,3}\|/) next;` then
  `if (!in_registry) { …E12 only…; next }` then `if (NF!=13) → E01`.
* **E12** (`row outside Registry section`) requires, outside Registry, a line matching
  `^\|[ \t]*S[0-9]{3,}[ \t]*\|`.

Audit of the added line:

```
$ awk 'NR>=74 && NR<=80' corpus/SOURCES.md | cat -A | grep -c '|'
0                                     # the added region contains no pipe character at all
$ grep -n "Round 26 bounded recheck" corpus/SOURCES.md
79:Round 26 bounded recheck (2026-10-21): do the 32 previously opened external rows (S001–S034 minus ow…
$ grep -n "^## " corpus/SOURCES.md
5:## Registry
45:## Paths
57:## Search log
81:## Leads (unopened)
```

The added line is prose: it does not begin with `|` (so neither E01 nor E12 can match it), it is
not a `##`/`#` heading (so it cannot re-open or close a section and mask/unmask registry rows),
and it contains **zero** pipe characters, hence it cannot be parsed as a table row at all.
Whole-file scan for the same hazard class:

```
pipe-starting lines in corpus/SOURCES.md : 37
sections those lines live in              : ['Registry']      # only Registry
E12 candidates (row-shaped outside Registry): []
```

⇒ **No E01, no E12, no row-count, tier or status drift** from the new paragraph. Confirmed
empirically by the byte-identical rerun (§2).

## 4. Cross-check of every numeric claim the paragraph makes

The paragraph asserts several counts. Each was re-derived from retained evidence:

| Paragraph claim | Verification | Result |
|---|---|---|
| "32 … rows (S001–S034 minus own-work S014/S019)" | 34 − 2 = 32; registry rows in scope = 32 | ✅ |
| "every recorded URL with one public GET (**34 fetches**)" | 34 distinct URLs recorded in those 32 rows (S001 and S002 each carry two) ; `fetched/manifest.json` has **34** entries covering exactly those 34 URLs, none missing | ✅ |
| "S008 one retry after a 60 s timeout" | `fetched/manifest-retry.json`: `"reason": "first attempt TimeoutError at 60s; single retry with 240s timeout"`, `S008-1.raw.gz` (failed attempt, 0 retained bytes) + `S008-1-retry.raw.gz` | ✅ |
| "retained gzip bytes and sha256 under round26 `fetched/`" | 35 `*.raw.gz` files; **35/35** sha256 recomputed from the retained bytes match the manifest digests (0 mismatches) | ✅ |
| "rechecked 32: HOLD 32, STALE 0, UNVERIFIABLE 0 at row level" | 32 receipts in `rechecks/`; `verdict` histogram = `{HOLD: 32}` | ✅ |
| "…at their anchors" | all 32 receipts carry a non-empty `anchorObserved`; all 32 receipt quotes are re-findable in the retained text views (`fetched/text/S0NN-<fetchIndex>.txt`, 34 views, all committed) — 32/32 found, 0 missing | ✅ |
| "Knowledge-statement corrections (8) are appended in the citing entries" | 8 `^- \[r26-recheck …\]` lines across `corpus/knowledge/*.md` (S003×2, S010×2, S021, S026, S030×2) | ✅ |
| "No row added, rejected or changed; no status/recheck/used-by cell changed" | `git diff base..candidate -- corpus/SOURCES.md` = 2 insertions, both in the search-log region (`:79` + blank); registry rows 35 at base and candidate; census tier/status histograms identical | ✅ |
| "Lead noted, not a row: RFC 9557 updates RFC 3339 §4.3 (… PairS032)" | grounded in `w1/PairS032StaticCanonicalPrefl.md:34-36` (RFC Editor info pages read 2026-10-21, §4.3 = "Unknown Local Offset Convention"); the lead is not a registry row, consistent with "no row added" | ✅ |

Nothing in the paragraph overstates what the receipts show: the 8 statement-level STALE
corrections are disclosed in the same sentence ("Knowledge-statement corrections (8) are appended
in the citing entries, not here"), so "STALE 0 … at row level" is scoped honestly and is not used
to hide the statement-level failures.

## 5. Findings

No actionable defect found in scope.

* No E01/E12 hazard from the new paragraph, no row-shaped lines anywhere outside `## Registry`.
* Census output identical to the recorded baseline, exit 0, W04 pre-existing at base.
* Every count asserted in the paragraph is corroborated by the retained bytes, receipts and
  appended corrections.

## 6. Residual risk / verification gaps

1. **Wording ambiguity (low, cosmetic, not a defect):** "34 fetches" counts *distinct recorded
   URLs fetched* (34); the number of actual HTTP requests was 35 (the S008 retry is the extra
   request and is disclosed in the same parenthesis). The manifest (34 entries) plus
   `manifest-retry.json` (1 entry, same S008 URL) is consistent with the paragraph under the
   natural reading; no correction needed, but a reader could mis-derive request counts.
2. **Derived text views are not themselves digest-pinned:** `manifest.json`/`manifest-retry.json`
   pin the 35 raw payloads (all 35 re-verified here); `fetched/text/*.txt` (34 views) are derived
   artifacts without their own manifest digests. I verified quote-level presence in the text
   views (32/32) but did **not** re-derive the views from the raw bytes with
   `.ufo/waves/round-26/source_text.py` (not a command named by this item).
3. **Date sensitivity:** E08 compares `opened` against the UTC today used by the run
   (`2026-10-21`). All 35 registry rows are opened in the past — 18 rows `2026-10-19`, 9 rows
   `2026-10-20`, 8 rows `2026-10-21` — so no row is future-dated and a later run date cannot
   turn any of them into an E08 finding.
4. **Out-of-item commands not run:** `measure.py` (the wave counter) and `sources-census.sh
   selftest` were not executed — the item names only the validate run. The counter's published
   observation (candidate 32/32, 8/8 STALE corrections) is consistent with everything re-derived
   above.
5. **Freshness of the fleet parser:** the census script has not changed since 2026-10-19, so this
   rerun and `census-before.txt` are comparable; a future script change would invalidate the
   comparison without any lane-side edit.

## 7. Files touched by this item

Only this report: `.ufo/waves/round-26/w2/CensusRerun.md`. No corpus, script, fleet-repo, sibling
lane, or lane git/jj index mutation; no files created outside the report; scratch was kept in
memory (process substitution only, no temp files). `git status --short` on the lane shows only
untracked wave artifacts (`w2/`, `w2-*.json`, `verification/` and the `__pycache__/` directories
whose mtimes — 13:30 and 13:35 −0300, i.e. minutes before this report — come from concurrent
sibling peers importing `source_text.py`; they are not tracked content and were left untouched).

```json
{"target":"round-26 C1 freshness — census rerun + search-log paragraph hazard audit (kake)","verdict":"AGREE","severity":"none"}
```
