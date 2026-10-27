# ScribeReportSources — round 63

Scope: draft of the round report's **Sources & frontier** section and its three
**Trend verdicts** lines. Facts below come only from committed bytes at the
measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` and base
`13d4519818db28cd0aa912e49020659140d7b9fa`, plus two census runs I performed
against those bytes (commands and exit codes pasted verbatim). Nothing was
edited outside this report file.

Lane root for every relative path below:
`/home/vgpnk/Projects/shokunin/kake-shokunin`.

---

## Draft — `## Sources & frontier`

Registry `corpus/SOURCES.md` is byte-identical at base and at the measured
commit (`git show 13d45198…:corpus/SOURCES.md | sha256sum` →
`63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2`, equal to
`sha256sum corpus/SOURCES.md`; `git diff --quiet 13d45198… 05b0d7f4… --
corpus/SOURCES.md` exit 0). The census therefore reads the same before and
after: **171 → 171 rows**.

Counting command (round-start form recorded at `corpus/lessons/round-63.md:69`,
re-run by this seat):

```text
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
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
exit 0
```

(16 `W04` cross-scope duplicate-URL warnings before and after; no `E` code.)

Row/tier census, before — run on the base blob
(`git show 13d45198…:corpus/SOURCES.md` written to
`/fast/scratch/hyaku/kake-r63/ScribeReportSources/SOURCES.base.md`):

```text
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file /fast/scratch/hyaku/kake-r63/ScribeReportSources/SOURCES.base.md --root /home/vgpnk/Projects/shokunin/kake-shokunin
file	rows	171
file	tier.A	148
file	tier.B	6
file	tier.C	17
file	status.mined	141
file	status.queued	8
file	status.rejected	22
FLEET	rows	171
FLEET	tier.A	148
FLEET	tier.B	6
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	8
FLEET	status.mined	141
FLEET	status.rejected	22
FLEET	status.invalid	0
FLEET	missing	0
exit 0
```

Row/tier census, after — same command on the lane registry at the measured
commit:

```text
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md --root /home/vgpnk/Projects/shokunin/kake-shokunin
file	rows	171
file	tier.A	148
file	tier.B	6
file	tier.C	17
file	status.mined	141
file	status.queued	8
file	status.rejected	22
FLEET	rows	171
FLEET	tier.A	148
FLEET	tier.B	6
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	8
FLEET	status.mined	141
FLEET	status.rejected	22
FLEET	status.invalid	0
FLEET	missing	0
exit 0
```

- **Rows added by tier:** A `+0`, B `+0`, C `+0` (171 → 171; 148/6/17 in both
  runs; `mined` 141, `queued` 8, `rejected` 22 unchanged).
- **Rows touched old→new:** none. No `SOURCES.md` cell changed, so there is no
  old→new pair to log. The row the round leans on is verbatim at both
  revisions — `corpus/SOURCES.md:178`:
  `| S432 | WHATWG Fetch — https://fetch.spec.whatwg.org/ | spec | A |
  X-Content-Type-Options nosniff value rule | Section 3.6 … | The field has one
  defined value, nosniff … | mined | 2026-10-27 | 180d |
  corpus/knowledge/response-header-expectations.md |` (status `mined`,
  recheck `180d`, used-by unchanged).
- **Frontier rows advanced:** none — `0` rows moved status, `recheck` or
  `used-by`. The round's frontier step is the re-open record, not an advance:
  S432 was re-opened 2026-10-27 (one GET, HTTP 200, 1,854,393 bytes, body
  byte-identical to the round-61 retained body `63b0a018…911b`) and the row
  stays `mined` (`corpus/lessons/round-63.md:53-59`).
- **Sourced claim (one):** the round's only sourced claim is C1's correction —
  the `[r63-correction 2026-10-27]` block at
  `corpus/knowledge/response-header-expectations.md:222-250` quotes the WHATWG
  Fetch §3.6 field-purpose sentence and names S432. The row entered the
  registry in round 61 (`LOG.md:2242` "… on S430–S433"; `LOG.md:2244`
  "Registry 167 → 171; S430–S433 are four tier-A rows"), so this round files a
  sourced claim on a **re-opened** row, not a newly opened one.
- **Mistakes mined (frontier-step duty):** one — the false-green class at
  `corpus/lessons/round-63.md:18-22` (evidence
  `.ufo/waves/round-62/controls/counter-false-green-l1.txt`).
- **Assimilation:** none. `corpus/lessons/round-63.md:49-51` — no `merge/kake/`
  entry adopted this round; the round's calibration work admits nothing from
  the package. (No `merge/` directory exists anywhere in the lane tree at the
  measured commit — see finding 3.)

---

## Draft — `## Trend verdicts`

Verdict vocabulary and conditions: `/home/vgpnk/Projects/shokunin/LEARNING.md`
§"The three trends"; each line is author-side until the non-author closure.

- **Expansion: unchanged.** No `corpus/SOURCES.md` row was added by any tier
  (0/0/0; registry 171 → 171, blob sha `63af1594…` identical at base and
  measured), no `corpus/knowledge/` file entered (the round's corpus edit is a
  pure-append 29-line correction inside the existing
  `knowledge/response-header-expectations.md`, admitted in round 61 —
  `git diff --numstat 13d45198… 05b0d7f4… -- corpus/` = `29 0`
  `response-header-expectations.md`, `4 0` `QUALITY.md`, `69 0` new
  `lessons/round-63.md`), no capability row at the measured commit
  (`git diff --stat 13d45198… 05b0d7f4… -- SCORECARD.md` empty), and the
  coverage/frontier map is unchanged (`corpus/README.md:81,125` still date the
  response-header ground to r61; `corpus/README.md` untouched).
- **Quality: improved locally (author-side).** The C1 counter family is
  repaired on committed bytes — after receipt
  `.ufo/waves/round-63/controls/after-c1.txt:3-4`
  (`… blobs_match=1 derived=collapsed-only class_match=1 criterion=1
  lesson_gate=1 … met=true`, exit 0) against base
  `.ufo/waves/round-63/controls/base-c1.txt:3-4` (`… met=false`, exit 1) — and
  both falsifiers are red on the new counter:
  `controls/control-marker-fixture.txt:6-7` (old c62 `met=true` defect, new c63
  `met=false`, exit 1) and `controls/control-junk-fixture.txt:4`
  (`met=false`, exit 1). Operability moves countably:
  `controls/after-c2.txt:3-4` (`present=1 selftest=4/4 frozen_cases=ok
  met=true`, exit 0) against `controls/base-c2.txt:3-4` (`present=0 … exit 1`).
  A grounded criterion is added at `corpus/QUALITY.md:1416` (grounding: the
  round-62 routed defect receipt and `corpus/lessons/round-63.md` §Mistakes).
  Bound: whether the admitted collapsed-only span clears the round-62
  substantive-support criterion is the non-author closure's judgment
  (`corpus/lessons/round-63.md:61-65`), and the wave's attack results are not
  yet committed at the measured commit.
- **Discernment: improved locally (author-side; own spot-check owed).** A
  non-author finding (round-62 verifier routed defect 1, reproduced at
  `.ufo/waves/round-62/controls/counter-false-green-l1.txt`) is mined at
  `corpus/lessons/round-63.md:18-22` and converted into a grounded
  `corpus/QUALITY.md:1416` criterion — the LEARNING.md `improved` condition
  ("a disagreement becomes a lesson that adds a grounded `QUALITY.md`
  criterion"). The round-61 outside `Disagree` is recorded as this gate's
  outside verdict and the round's own admits/rejects are labelled author-side
  (`corpus/lessons/round-63.md:61-65`); the round-63 non-author spot-check has
  not been filed, so the trend is not closed by this line.

---

## Evidence

| Fact | Pointer |
|---|---|
| registry blob identical base vs measured | `sha256sum` both = `63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2`; `git diff --quiet 13d45198 05b0d7f4 -- corpus/SOURCES.md` exit 0 |
| 171 rows, tiers 148/6/17, statuses 141/8/22 | census runs above (before on base blob, after on lane registry), both exit 0 |
| 16 `W04`, no `E` | `validate` run above, exit 0; matches `corpus/lessons/round-63.md:69` |
| S432 row verbatim, `mined`/`180d` | `corpus/SOURCES.md:178` |
| no registry-cell edit | identical blob sha; `corpus/lessons/round-63.md:58-59` ("No registry row added or changed; S432 stays `mined`") |
| sourced claim cites S432 | `corpus/knowledge/response-header-expectations.md:222-250` |
| S432 entered round 61 | `LOG.md:2242`, `LOG.md:2244` |
| rule-1 re-open record | `corpus/lessons/round-63.md:53-59` |
| mistake mined | `corpus/lessons/round-63.md:18-22` |
| assimilation none | `corpus/lessons/round-63.md:49-51` |
| C1 before/after | `.ufo/waves/round-63/controls/base-c1.txt:3-4`, `after-c1.txt:3-4` |
| C2 before/after | `.ufo/waves/round-63/controls/base-c2.txt:3-4`, `after-c2.txt:3-4` |
| controls red | `controls/control-marker-fixture.txt:6-7`, `controls/control-junk-fixture.txt:4` |
| new QUALITY criterion | `corpus/QUALITY.md:1414` heading, `:1416` criterion |
| round-62 defect receipt | `.ufo/waves/round-62/controls/counter-false-green-l1.txt` |
| corpus change shape | `git diff --name-status/--numstat 13d45198… 05b0d7f4… -- corpus/` (M QUALITY +4, M knowledge +29, A lessons/round-63 +69; all additions, 0 deletions) |
| SCORECARD/SKILL/LOG/PROVINCE/README unchanged | `git diff --stat 13d45198… 05b0d7f4… -- <files>` empty |
| coverage map dating | `corpus/README.md:81`, `corpus/README.md:125` (response-header ground = r61) |

## Findings and limits (for the report author — not fixed here)

1. **The round-start census line credits a command that prints no row count.**
   `corpus/lessons/round-63.md:69` reads "`sources-census.sh validate …` → 171
   rows, 16 W04 … exit 0", but `validate` mode emits only `W`/`E` findings plus
   the `ok` line (script: `scripts/sources-census.sh:737-743`); the `rows`
   metric is printed only by `census` mode (`scripts/sources-census.sh:21`,
   `:691`). The 171 figure is correct and re-derivable, but the cited command
   does not produce it. Recommended: paste the `census --file …` form for the
   row count and keep `validate` for the W04 line, or word the line as "171
   rows (census mode), 16 W04 (validate mode)".
2. **Expansion is "unchanged" only at the measured commit.** `SCORECARD.md`,
   `SKILL.md`, `LOG.md`, `PROVINCE.md` and `corpus/README.md` are all untouched
   between base and measured commit, so no capability row and no gate-registry
   row for `scripts/quote_class.py` or the two c63 counters exists in committed
   bytes. If the scorecard/LOG seat later lands a capability row or a
   `SKILL.md` gate row for C2's tool, this expansion line must be restated (a
   capability row admitted through a demonstrated run is the LEARNING.md
   `improved` trigger). As it stands the report must not claim expansion.
3. **No `merge/` package is on disk.** `find /home/vgpnk/Projects/shokunin
   -maxdepth 3 -type d -name merge` and `ls -d */merge` return nothing, so
   "the package stays staged" (`corpus/lessons/round-63.md:50-51`) has no
   on-disk artifact to point at in this tree. "Assimilation: none" is
   trivially true; the staging sentence is a narrative, not a citable path.
4. **The sourced claim rests on a re-opened row (round 61), not a row opened
   this round.** Stated explicitly in the draft above so a reviewer comparing
   against the "row opened this round" phrasing does not read it as a defect
   against the registry (PROTOCOL's duty is a sourced claim citing an `S###`
   row; this round's evidence cites S432).
5. **Frontier "advance" is zero by construction.** With the registry blob
   unchanged there is no old→new cell to show; do not present the S432 re-open
   as a row advance. All trend lines here are author-side; the round-63
   non-author spot-check is still owed (`corpus/lessons/round-63.md:63-65`).

## Commands this seat ran (all read-only)

```text
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake            # exit 0
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md --root /home/vgpnk/Projects/shokunin/kake-shokunin   # exit 0
git show 13d4519818db28cd0aa912e49020659140d7b9fa:corpus/SOURCES.md > /fast/scratch/hyaku/kake-r63/ScribeReportSources/SOURCES.base.md
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file /fast/scratch/hyaku/kake-r63/ScribeReportSources/SOURCES.base.md --root /home/vgpnk/Projects/shokunin/kake-shokunin   # exit 0
git diff --quiet 13d4519818db28cd0aa912e49020659140d7b9fa 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f -- corpus/SOURCES.md    # exit 0
git diff --name-status / --numstat 13d45198… 05b0d7f4… -- corpus/
```

No tool was installed; no pacman transaction; no commit, push, or git/jj
mutation outside reading. The only write outside this report was the base-blob
copy `/fast/scratch/hyaku/kake-r63/ScribeReportSources/SOURCES.base.md`, removed
after the census run (`rm -rf`).
