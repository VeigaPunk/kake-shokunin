# ScoutCensusState — round-64 wave-1 attack report

Seat: `ScoutCensusState` (leaf; no subagents). Lane: `kake-shokunin`.
Scope: the registry census claim of the round-64 contract — that
`corpus/SOURCES.md` is untouched between base `1a481315` and measured T0
`4c8295fa`, and that the committed census receipts `controls/census-before.txt`
/ `controls/census-after.txt` are faithful reproductions of the frozen manual
census of `/home/vgpnk/Projects/shokunin/CORPUS.md` §"SOURCES.md — where a
shokunin learns" → "Census".

Verdict: **the census claim holds.** The registry diff base→T0 is empty, the
frozen manual census reproduces identically at base and at the live tree, both
committed receipts are byte-faithful to a fresh run of the command the round
lesson names, and the W04 count is **16**.

---

## 1. What I attacked

| # | Target | Attack | Result |
|---|---|---|---|
| A1 | registry diff base→T0 | `git diff 1a481315 4c8295fa -- corpus/SOURCES.md` | empty (no output) |
| A2 | registry identity across revisions | `git rev-parse <rev>:corpus/SOURCES.md` at base / T0 / HEAD, plus worktree `git hash-object` | one blob `3993185e5eb13ed51cd32ffd21b20c3a2815a261` everywhere; sha256 `63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2` for the worktree copy and for the base copy |
| A3 | frozen manual census (7 commands) | re-run verbatim from `CORPUS.md` at the live tree and at an extracted base copy | identical results |
| A4 | committed receipts | re-run the lesson's named command and diff against `census-before.txt` / `census-after.txt` | byte-identical (after stripping the trailing `census-*-exit=` label line) |
| A5 | W04 count | count of `W04` rows in the receipts + in a fresh run | 16 (and 16) |
| A6 | receipt pair | `diff census-before.txt census-after.txt` | differs only on line 18 (`census-before-exit=0` vs `census-after-exit=0`) |

---

## 2. Evidence

### 2.1 Registry diff base→T0 is empty

```
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a481315 4c8295fa -- corpus/SOURCES.md
(no output; diff-exit=0)
$ git -C ... diff --stat 1a481315 4c8295fa -- corpus/SOURCES.md
(no output)
$ git -C ... diff --numstat 1a481315 4c8295fa -- corpus/SOURCES.md
(no output)
$ git -C ... diff --numstat 1a481315 cc8add1fa740b920ea5179a71152680ab220c70c -- corpus/SOURCES.md
(no output)
```

Blob identity (the diff is empty because the file is the *same blob*, not a
no-op rewrite):

```
$ git -C ... rev-parse 1a481315:corpus/SOURCES.md      -> 3993185e5eb13ed51cd32ffd21b20c3a2815a261
$ git -C ... rev-parse 4c8295fa:corpus/SOURCES.md      -> 3993185e5eb13ed51cd32ffd21b20c3a2815a261
$ git -C ... rev-parse cc8add1fa:corpus/SOURCES.md     -> 3993185e5eb13ed51cd32ffd21b20c3a2815a261
$ git -C ... hash-object corpus/SOURCES.md             -> 3993185e5eb13ed51cd32ffd21b20c3a2815a261
$ sha256sum corpus/SOURCES.md -> 63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2
```

Commit file lists confirm the build commit never touched the registry
(`git show --stat 4c8295fa`): the 31 changed paths are the two counters, the
fixtures, the contract, the controls, `SKILL.md` (+2), `corpus/QUALITY.md` (+4),
`corpus/knowledge/freshness-sidecar.json` (the 7-entry re-pin) and
`corpus/lessons/round-64.md`. `corpus/SOURCES.md` is absent from that list.
`git show --stat cc8add1f` adds only the four green-after receipts.

### 2.2 Frozen manual census — live tree (== T0 content) and base copy

Commands are the verbatim frozen block at
`/home/vgpnk/Projects/shokunin/CORPUS.md` lines 131–148 (§"SOURCES.md — where a
shokunin learns" → "### Census — run from the lane root"), run with cwd =
lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`.

Live tree:

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md          -> 171
$ awk -F'|' '...NF!=13 {n++} END{print n+0}' corpus/SOURCES.md                   -> 0
$ awk -F'|' '...tier histogram...' corpus/SOURCES.md                              -> A=148 B=6 C=17
$ awk -F'|' '...status histogram...' corpus/SOURCES.md                            -> mined=141 queued=8 rejected=22
$ awk -F'|' '...ids...' corpus/SOURCES.md | sort | uniq -d                        -> (empty)
$ awk -F'|' '...enum violations/tier inflation...' corpus/SOURCES.md              -> (empty)
$ awk -F'|' '...mined used-by paths...' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
                                                                                  -> (empty: 0 missing)
```

Base copy (`git -C <lane> show 1a481315:corpus/SOURCES.md` extracted to
`/fast/scratch/hyaku/kake-r64/ScoutCensusState/base-lane/corpus/SOURCES.md`):

```
rows=171  malformed=0  tier: A=148 B=6 C=17  status: mined=141 queued=8 rejected=22
duplicate ids: (none)   enum violations / tier inflation: (none)
sha256(base copy) = 63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2
sha256(live tree) = 63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2
```

Base and T0 are therefore indistinguishable to every frozen census command —
the "171 rows before and after" clause of the contract's no-harm section
(`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/contract.md`,
§No-harm: "`corpus/SOURCES.md` untouched (171 rows before and after)") is
literally true at byte level.

Cross-checks on the same file: no row is indented 1–3 spaces
(`grep -cE '^ {1,3}\|'` → 0) and none 4+ (→ 0), so the maintained parser's
indentation tolerance and the frozen column-zero examples see the same 171
rows; 0 `S###`-shaped rows fall outside the `## Registry` section (the
maintained CLI's E12 check), so the frozen census is not silently skipping
rows the maintained validator would flag.

### 2.3 The committed receipts are faithful

The round lesson names the exact command
(`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-64.md:103-109`,
§Sources census: "`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin kake` → 171 rows, 16 W04
cross-scope duplicate-URL warnings, exit 0"). Re-running it:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
      --root /home/vgpnk/Projects/shokunin kake
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	W04	S416 duplicate url ziyuan.baidu.com/college/courseinfo?id=1399 across scopes
kake	W04	S417 duplicate url ziyuan.baidu.com/college/courseinfo?id=267&page=15 across scopes
kake	W04	S427 duplicate url developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers across scopes
kake	W04	S433 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
exit=0
```

Diff vs the committed receipts:

```
$ diff <(grep -v '^census-after-exit='  .../controls/census-after.txt)  wt-validate.tsv   -> no differences (exit 0)
$ diff <(grep -v '^census-before-exit=' .../controls/census-before.txt)  wt-validate.tsv   -> no differences (exit 0)
$ diff .../controls/census-before.txt .../controls/census-after.txt
18c18
< census-before-exit=0
---
> census-after-exit=0
```

Both committed receipts are therefore faithful reproductions of the *current*
tree, and — because the registry blob is identical at base — of the base tree
as well. I also re-ran the validator against an extracted base copy
(`--file` mode); its W04 set is the same 16 ids in the same order (only the
lane label differs, `file` vs `kake`). The `--file` run reported E11
"missing used-by" rows — that is an artifact of my scratch copy living outside
the lane (used-by paths are lane-relative), not a registry finding; the
lane-relative check inside the real lane root prints nothing (2.2).

### 2.4 W04 count

**16** duplicate-URL-across-scopes warnings. Identical in
`controls/census-before.txt` (16), `controls/census-after.txt` (16), and my
fresh run (16):

```
$ grep -c 'W04' /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/census-after.txt
16
$ grep -c 'W04' /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/census-before.txt
16
```

Per `scripts/sources-census.sh` header (lines 22–33), `W04 same URL across
scopes` is a **warning**: "warnings do not affect clean lanes", so validate
exits 0 and the lane stays `ok`. No `E0x`/`E1x` error code appears anywhere in
either receipt.

---

## 3. Judgment

- The registry-diff clause of the census claim is **confirmed**: empty diff,
  identical blob, 171 rows at base and at T0, and the build commit's file
  list never mentions `corpus/SOURCES.md`.
- The census receipts are **faithful**, not hand-written: a fresh run of the
  lesson's named command reproduces them byte-for-byte apart from the
  trailing exit-label line, and the before/after pair is identical in every
  content line — exactly what "no row added or changed this round" predicts.
- The W04 count named by the lesson (16) is **confirmed** against both
  receipts and a live run.
- The manual frozen census is clean on every clause: 171 rows, 0 malformed,
  0 duplicate ids, 0 enum violations, 0 tier inflation, 0 missing mined
  used-by paths; tier and status histograms both sum to 171.
- No green was reachable by attack: there is no counter here to game, and
  every number in the receipt is independently re-derivable from the frozen
  commands.

Confidence: **high** for the diff/identity facts (git object ids and sha256
are exact) and for the receipt fidelity (byte diffs). The only inference is
causal — that the `census-before.txt` receipt was *captured* at the base
revision; because the registry blob is identical at base and at T0, its
content is necessarily valid at both, but the capture-time provenance of the
committed file is asserted by the build commit, not derivable from its bytes.

Remaining unknowns: none material for this seat. (Not audited here, by
scope: the C1/C2 counters and the freshness sidecar re-pin — other seats.)

---

## 4. Discipline

- No git/jj mutating command was run; the lane repo working tree is untouched.
  `git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain`
  shows only the orchestrator's untracked wave files
  (`.ufo/waves/round-64/sources/S432.live.html`, `w1-dispatch.json`,
  `w1-spec.json`, `w1.ready`, `w1.ready.partial`, `w1/`) — the same set as
  before this seat started; this seat added only its own report file.
- No frozen claim, counter, receipt, contract or lesson was edited.
- Scratch: `/fast/scratch/hyaku/kake-r64/ScoutCensusState/` (base registry
  copy + captured TSVs), deleted before yield.
- **No tools installed or upgraded** for this seat (bash, git, grep, awk, sed
  only — all pre-existing); no `/home/vgpnk/.omp/agent/RULES.md` action needed.
