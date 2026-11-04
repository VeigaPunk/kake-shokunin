# Round 82 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)

Lane: `kake-shokunin` · round 82 · report `.ufo/reports/round-82/kake.md` · base
`419866015b1f58e01f061cde9a77d490653d3c76` · lane tip `9635bf015d443b8984f86251b7c38564862b21d8`.
Written 2026-11-04 by the hyaku closure seat, which did not author this round. Read-only over the
lane except this file; the lane's gates were **not executed** (PROTOCOL §Gate standard: the
integrator verifies committed evidence and re-derives claims with its own measurements). Every
command below was run by this seat; the outputs are what the run printed.

## 1. Step-1 conformance

- **Report committed by the lane identity.** `git log --format='%an <%ae> %H' -- .ufo/reports/round-82/kake.md`
  → `kake-shokunin <kake@shokunin.local> 2e3fcc7f3b4e792a3552611d60c017a1c89a052d`
  (2026-11-04 10:10:09 -03). It is an ancestor of the fleet `HEAD` and lands after the lane tip
  (`9635bf015d443b8984f86251b7c38564862b21d8`, 10:09:09 -03): report-last holds.
- **`SHONEN` heading.** The report carries `## SHONEN` with exactly four box lines —
  `[~]` box 1, `[ ]` box 2 (declared `gap`), `[~]` box 3, `[~]` box 4 — matching the four boxes of
  `SHONEN.md` (`grep -c '^- \[' SHONEN.md` → `4`; box lines in the report → `4`). No `[x]`.
- **Cited lane commits.** Every commit-shaped citation resolves and is an ancestor of `master`
  (`git merge-base --is-ancestor <h> master`): `082b7dd3`, `62061ff9`, `8abeccca`, `70c8241b`,
  `576cf76c`, `21deab2b`, `bde1d0b6`, `bd1dcac7`, `a30c08f2`, `b6ae0ba6`, `3aac1cbc`, `9635bf01`,
  `41986601`, `498a0969`. Non-commit hex tokens in the report are digests (`1ffc61f1`, `21c1cdce`,
  `d43c0231`, `d9302da6`), not hashes. `7678247a3c13b1dc03ed1cb8f80d2dba603ee0ca` is a **fleet**
  commit: it exists and is an ancestor of fleet `HEAD`.
- **Lane clean and pushed.** `scripts/hyaku/jj-lane.sh state …/kake-shokunin` →
  `branch=master local=9635bf015d443b8984f86251b7c38564862b21d8 remote=9635bf015d443b8984f86251b7c38564862b21d8 ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git status --porcelain` prints nothing. `git ls-remote origin refs/heads/master` prints
  `9635bf015d443b8984f86251b7c38564862b21d8`.
- **Prompt fidelity.** Lines 1–140 of `.ufo/prompts/kake-round-82.md` render
  `templates/round-prompt.md` verbatim after the documented substitutions (the single diff line is
  the template's literal `<{{LANE}}-repo>` bracket rendered as the absolute lane path); the
  mutation/axes binding, the 1–3 claim rule with the lowest-axis clause, the frontier step, the L2
  floor (≥8 in one batched call, no hardcoded aliases; the route table decides), the report contract
  with its required sections and `SHONEN` item, commit-then-push ordering, push scope and the L0
  channel are all present. §6 campaign addendum and §7 scratch discipline follow the template body.
  The quoted run-15 route map (`reviewer` on the economy route, everything else on the
  fast-execution route) matches `MISSION.md`'s role-class buckets.
- **Dispatch/complete digest** (copied from the mutable `.ufo/watchdog.log`):
  `2026-11-04T09:42:58-03:00 launch kake round=82 pgid=756711 driver=hyaku-inline attempt=1`;
  `2026-11-04T10:10:59-03:00 complete kake round=82; hyaku-inline attempt=1`.

Conformance defects (status-neutral, §6) are recorded at the end.

## 2. Claim re-checks

### C1 — calibration: the round-81 routed-defect queue closes (`open=8 → open=0`)

The claim is decided by the lane's counter `c82_defect_queue.py`; this seat did not run it and
instead re-derived **every state conjunct** from committed bytes at `9635bf01`, plus the committed
receipts. Nothing below rests on a sentence in the lesson that says "closed".

| Item | My command | Observed at `9635bf01` |
|---|---|---|
| D1 | `git show <rev>:corpus/SOURCES.md \| grep '^\| *S433 *\|'` | base: `… \| mined \| 2026-10-27 \| 180d \| corpus/knowledge/response-header-expectations.md \|`; tip: `… \| 2026-10-27 \| 2027-05-03 \| corpus/knowledge/response-header-expectations.md, corpus/lessons/round-81.md \|` (only the two rule-2 cells moved) |
| D2 | `git show 9635bf01:.ufo/waves/round-81/controls/after-c1-final.txt \| tail -3` | `C1v1 revision=498a0969499f70830b7c992eb36ea364672f1a1b items=6 open=0 closed=6 met=true` / `exit=0` |
| D3 | `git cat-file -t 7678247a…`; `git diff --stat 7678247a^ 7678247a -- .ufo/reports/round-81/kake.md`; `git rev-parse 7678247a^:…` / `7678247a:…` | `commit`; `1 file changed, 12 insertions(+), 5 deletions(-)`; blobs `07b1238c4b8f1877…` ≠ `f39b6df22e305aad…` |
| D4 | `git show 9635bf01:.ufo/waves/round-81/seat-failures.json \| grep -A5 '"MutC"'` | `"output_bytes": 3801`; `corpus/lessons/round-82.md` carries `3801` + `superseded`; `grep -n '3771\|3,771' corpus/lessons/round-82.md` → none |
| D5 | `git cat-file -e 9635bf01:<path>` for both dead paths and the live receipt | `after-c81-defect-queue.txt` ABSENT, `after-c81-capture-audit.txt` ABSENT, `after-c1-final.txt` PRESENT |
| D6 | `git show …:c81-selftest-c2.txt \| tail -2`; `git show …:corpus/QUALITY.md \| grep -n '22/22'` | `selftest: 22/22 passed` / `exit=0`; `:1695: … reads \`22/22\`; this supersedes the round-81 …` |
| D7 | `git show 9635bf01:.ufo/waves/round-82/controls/after-c1-ledger-gate.txt` | `C1v2 revision=082b7dd3… events=40 undisclosed=0 … met=true` / `exit=0` |
| D8 | `git show 9635bf01:corpus/lessons/round-80.md \| grep -n 'r82-correction'` | `:221:**[r82-correction 2026-11-04]** … re-derived the \`S453\` registry row at \`corpus/SOURCES.md:200\`` |

Committed controls read `C1v1 … items=8 open=8 closed=0 met=false`, exit 1
(`controls/base-c82-defect-queue.txt`); the junk-prose tree reads `open=8 … met=false`, exit 1
(`controls/ctl-c82-junk-queue.txt`); the counter selftest ends `selftest: 11/11 passed`, exit 0
(`controls/c82-selftest-c1.txt`). **C1 verifies** (re-measured by this seat on the state conjuncts;
evidence-verified for the receipts/controls; the row conjuncts exist in `corpus/lessons/round-82.md`
§Corrections, which only prose can carry — the stated limit).

### C2 — freshness: a second dated capture feeds a capture-to-capture drift gate

Re-measured with my own script over the committed capture trees (no lane tool executed):
`receipts_ok` (GET, integer status 100..599, byte count equal to the retained body, body sha256
equal to the receipt digest, RFC 3339 fetch time, not truncated) → **True** in both trees;
order → `ds4cc-primary` 12:05:06Z→13:00:27Z, `ds4cc-robots` 12:05:06Z→13:00:28Z,
`ds4cc-sitemap` 12:05:06Z→13:00:28Z, all strictly later and all ≥ `2026-11-04T12:42:00Z`; header-map
comparison → primary `changed=4` (`date`, `x-fastly-request-id`, `x-served-by`, `x-timer`),
robots and sitemap `changed=5` (plus `x-cache`), body sha256 and status equal on all three; my
summary line

    surfaces=3 identical=0 changed=3 added=0 removed=0

equals the last line of `controls/after-c2-delta.txt` byte-for-byte. Both manifests carry exactly
the three frozen ids/urls in the frozen order with identical `expect` blocks. `grep -nE
'socket|urllib|requests|http\.client' scripts/capture_delta.py` matches only the docstring line
`usage. Offline: no socket is opened.` Committed receipts: `after-c2.txt`/`after-c2-tip.txt`
`met=true`, exit 0 at `8abeccca`/`3aac1cbc`; base `surfaces_b=0 … met=false`, exit 1; identical
capture `order_ok=0 floor_ok=0 met=false`, exit 1; one-byte-flipped `receipts_ok=0 met=false`,
exit 1; counter selftest `9/9 passed` and tool selftest `14/14` both exit 0. **C2 verifies**
(re-measured from the committed capture bytes; evidence-verified for the receipts).

## 3. Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration (2, lowest non-retired) | **improved** | C1: the eight routed defects close; every state conjunct re-derived at the tip, base control red, junk control red, no defect demoted to prose |
| freshness (10, held) | **improved** | C2: two dated captures and an offline delta whose record this seat reproduced exactly; base/identical/tampered controls red; score held by the lane as declared |
| operability | unchanged | two instruments and one tool registered (`SKILL.md` §Round 82) but no operability claim; no harm found |
| coverage | unchanged | outside this lane's scored ownership; no surface removed |
| depth | unchanged | outside this lane's scored ownership; no claim |
| adjacency | unchanged | connector's sibling scan found no competing capture-to-capture gate; two adjacencies (mori `Vary`/cache-selection, kumitate receipt-age) cited, not absorbed |

No owned axis is harmed: `git diff 41986601 9635bf01 -- SCORECARD.md` is additions only (42
insertions, 0 deletions); the axis rows are untouched and the round block adds the two claims, the
move-log rows and the drift-gate capability row.

## 4. Discernment spot-check (non-author)

Source re-opened: `https://www.rfc-editor.org/rfc/rfc9110.txt`, GET 2026-11-04T13:13:19Z,
HTTP/2 200, 502,941 bytes, sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`
— byte-identical to the lane's retained copies at
`.ufo/waves/round-82/w1/ScoutSources/rfc9110.txt` and `corpus/lessons/round-81-gate/rfc9110.txt`
(`cmp`-equal, both 502,941 B).

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S455 — RFC 9110 §8.8.1 + §8.8.3 as the drift gate's definitional ground | admit (tier A, `spec`, `mined`) | live RFC 9110 text, lines cited in the row and the lesson | **agree** | The admission quote is a raw substring at `:3572-3574` and 24 words — "The "ETag" field in a response provides the current entity tag for / the selected representation, as determined at the conclusion of / handling the request." The two supporting spans are raw substrings at `:3403-3404` (16 words) and `:3438-3439` (17 words); the 31-word full strong-validator sentence is raw-absent and collapsed-present, exactly as the lesson discloses. The row's `teaches` follows `:3428-3429` (hash-as-validator) and `:3463-3465` (shared validator weak unless data identical) |
| §8.8.3's trailer paragraph as an anchor for S455 | reject | live RFC 9110 `:3614-3617` | **agree** | "A sender MAY send the ETag field in a trailer section … unless the entity tag is generated while sending the content" is field placement; it states nothing about what a validator guarantees, and the row's own scope cell excludes trailer placement |
| §8.8.3.1 *Generation* as an anchor for S455 | reject | live RFC 9110 `:3619-3641` | **agree** | The section is mechanism selection ("only the service author knows the implementation … to select the most accurate and efficient validation mechanism"); read as a validator guarantee it would make the anchor wider than the row's scope |

New `SOURCES.md` row re-opened: **S455** at `corpus/SOURCES.md:202` — exactly eleven cells, `id` new
and unused, `kind=spec`, `tier=A`, `status=mined`, `opened=2026-11-04`, `recheck=365d`, `used-by`
naming two existing paths; `sources-census.sh validate` exits 0 (see §5). Its quote is the 24-word
admission quote above, within the ≤25-word cap.

## 5. Trend verdicts and frontier

- **expansion — improved.** One net-new admitted `knowledge/` entry on ground the coverage map did
  not hold (`corpus/knowledge/capture-drift-validators.md`, cross-instant drift plus RFC 9110
  validator semantics), its `source:` citing `S455` — a `mined` row opened this round — and the
  coverage map gained the matching row (`corpus/README.md` §Coverage — round 82). Registry
  **192 → 193** rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` over
  `41986601` and `9635bf01`), `W04` 21 → 22 in the committed census pair.
- **quality — improved.** Two instruments with committed base/red-path controls and green selftest
  receipts (11/11 and 9/9 counters, 14/14 tool); the D6 criterion supersedes the stale `18/18`
  tally with the receipt's `22/22` and names the row it supersedes; the cache-fill erratum narrows
  `body=same` to stored objects; the standing instrument-receipt rebind is real (this seat checked
  the receipt against the revision's blobs: 30/30 present, 0 digest mismatches; at base the receipt
  held 23 files with `x_robots_tag_audit.py` stale and four round-80 instruments unbound, matching
  the report's red-at-base description). No admitted entry was found false or stale and left
  unmarked; the `[r82-note]` imprecision was corrected by an appended erratum.
- **discernment — improved.** This non-author spot-check agrees with the round's Gate on the one
  admit and both rejects (table above), with the quoted spans re-opened in the live source and the
  registry row re-validated by the census; that is the `LEARNING.md` condition for `improved`.
- **Census.** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
  exits **0** at the tip with 22 `W04` duplicate-URL warnings (one more than the 21 in
  `controls/census-before.txt`) and no `E` finding.

## 6. Routed defects (lane to fix next round; status-neutral)

1. **Attack floor unmet.** All four requested attack seats (`ReviewC1`, `ReviewC2`,
   `CriticClaims`, `MutC`) returned empty; settled attack share `0/7 = 0.0 %` against the run-15
   ≥ 25 % floor. Requested shape met it (4/13 = 30.8 %). The lane reported this as a defect; next
   round must settle adversarial seats and record settlement, not relabel.
2. **Wave-prose byte counts are character counts.** The report's §Wave accounting prints
   `(4,871 B)`, `(7,888 B)`, `(6,392 B)`, `(6,664 B)`, `(3,811 B)`; the committed
   `.ufo/waves/round-82/w1-accounting.json`, produced by `make_accounting.py`
   (`len(output.encode("utf-8"))`), records UTF-8 bytes `4,899`, `7,902`, `6,402`, `6,669`,
   `3,813` (`ConnectorC` 13,375 matches). Classification (7 settled / 6 substantive / 6 empty) is
   unaffected. Cite the JSON's numbers or label them as characters.
3. **Instrument-receipt rebind has no dedicated receipt.** The report asserts the standing gate was
   red at base and that `--check` at `576cf76c` exits 0, with no receipt path; the rebind itself
   re-derives (30/30 blobs bound, 0 mismatches; base receipt 23 files, one stale digest, four
   round-80 instruments unbound). Commit the `--check` receipt next round or cite the re-derivation.
4. **D3 erratum names categories, not the superseded text.** `corpus/lessons/round-82.md` D3 names
   the four rewritten statements by kind (lane-tip line, wave bullet, landed-changes row, claim
   row) but does not quote the superseded strings the PROTOCOL erratum clause asks for. The
   counter's frozen conjunct does not require it; add the superseded text as an append-only erratum.
5. **Counter mutation survivors stay open.** C1: 3/5 mutants killed, survivors `m3` (constant `3801`
   indistinguishable from the derivation) and `m5` (a `met=false` receipt with `undisclosed=0` has no
   fixture). C2: 1/5 killed, 1 equivalent, survivors `m2` (equal instants), `m4` (hard-coded
   `selftest_ok`), `m5` (dropped capture-A surface). The killer fixtures are routed to round 83;
   keep them queued — the counters are frozen and measured.
6. **Gate-summary provenance.** The report's Sources & frontier lists "the `merge/kake` package" in
   the Gate's rejects, while `corpus/lessons/round-82.md` §Gate's rejects are the two S455 anchor
   spans and the package is an assimilation non-adoption. Prose-only; cite the lesson section.

## 7. Verdict and limits

**Admitted.** Both claims verify by this seat's own re-derivation (C1: eight of eight state
conjuncts closed at `9635bf01`, base and junk controls red; C2: receipt verification, order, floor
and the committed record reproduced exactly), and no axis is harmed. Conformance defects — the
unmet settled attack floor, six dead seats, and the numbering defects above — are recorded and
routed; they do not change the lane status, which is `ok` (a real report with real, checkable work
and a resolvable tip commit).

Limits inherited and confirmed: C1's row conjuncts are textual, so a records-only tree with correct
arithmetic could reach `open=0`; this spot-check re-derived only the state conjuncts. C2 decides
the capture chain, not the property, and a well-formed fabrication with real digests passes —
provenance remains the capture transcript's claim, narrowed further by the cache-fill erratum
(`body=same` compares stored objects, not origin reads). SHONEN: three boxes are `[~]` author-side
and box 2 is a declared `[ ]` gap; no box is `[x]`, so this round supplies no promotion evidence
(promotion is operator-owned).
