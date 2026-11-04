# Round 83 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)

Lane: `kake-shokunin` · round 83 · report `.ufo/reports/round-83/kake.md` · base
`826b0061f233ce1dffb9bd6874abc1342a864247` · lane tip
`64847b5fc946c61c972b2ab33fa3f798053725cd`. Written 2026-11-04 by the hyaku closure seat, which did
not author this round. Read-only over the lane except this file; the lane's gates were **not
executed** (PROTOCOL §Gate standard: the integrator verifies committed evidence and re-derives
claims with its own measurements). Every command below was run by this seat; the outputs are what
the run printed.

## 1. Step-1 conformance

- **Report committed by the lane identity.** `git log --format='%an <%ae> %H' --
  .ufo/reports/round-83/kake.md` → `kake-shokunin <kake@shokunin.local>
  15ef915c315f777b3acac5964f10434d8be36c97` (2026-11-04 10:45:21 -0300). It is an ancestor of the
  fleet `origin/master` and lands after the lane tip (`64847b5f`, 10:44:43 -0300): report-last holds.
- **`SHONEN` heading.** The report carries `## SHONEN` with exactly four box lines — `[~]` box 1,
  `[ ]` box 2 (declared gap), `[~]` box 3, `[~]` box 4 — matching the four boxes of `SHONEN.md`
  (`grep -c '^- \[' SHONEN.md` → `4`; box lines in the report → `4`). No `[x]`.
- **Cited lane commits.** Every commit-shaped citation resolves and is an ancestor of
  `refs/heads/master` (`git merge-base --is-ancestor <h> refs/heads/master`):
  `64b71992`, `304c0f87`, `2586243e`, `64847b5f`, `826b0061`; `70c8241b57ceec…` (the instrument
  receipt's declared revision) also exists and is an ancestor of `64b71992`. `7678247a…` is a
  **fleet** commit and an ancestor of fleet `HEAD`. Non-commit hex tokens in the report are a digest
  prefix (`aeb52adb`) and a date-shaped tag (`wip/operator-save-20261023`), not hashes.
- **Lane clean and pushed.** `scripts/hyaku/jj-lane.sh state …/kake-shokunin` →
  `branch=master local=64847b5fc946c61c972b2ab33fa3f798053725cd
  remote=64847b5fc946c61c972b2ab33fa3f798053725cd ahead=0 behind=0 head=detached tracked=0
  untracked=0`; `git status --porcelain` prints nothing. `git ls-remote origin refs/heads/master`
  prints `64847b5fc946c61c972b2ab33fa3f798053725cd`.
- **Prompt fidelity.** `.ufo/prompts/kake-round-83.md` lines 1–140 render `templates/round-prompt.md`
  verbatim after the documented substitutions (`{{LANE}}`→`kake`, `{{ROUND}}`→`83`,
  `{{FLEET_ROOT}}`, `{{AXES}}`, and the `<kake-repo>` bracket rendered as the absolute lane path):
  the structured diff over those 140 lines is empty except the appended `## 6` heading. The
  addendum supplies the remaining child-lane items the template body leaves implicit: the lane
  **write scope** (line 446, `/home/vgpnk/Projects/shokunin/kake-shokunin`), the report-last rule
  with the pushed-lane-hash citation rule (line 514, "The report lands last and cites the pushed
  lane hash"; "Cite ONLY the helper's final `landed <hash>` line"), and the pre-report
  `grep -c '^## SHONEN'` gate (lines 519–520). The quoted run-15 route map is the operator's host
  route table (`task.agentModelOverrides` is named as the authority) and `MISSION.md` §L2's
  role-class bucket table is explicitly advisory, so no MISSION bucket is contradicted.
- **Dispatch/complete digest** (copied from the mutable `.ufo/watchdog.log`):
  `2026-11-04T10:18:12-03:00 launch kake round=83 pgid=1801362 driver=hyaku-inline attempt=1`;
  `2026-11-04T10:46:33-03:00 complete kake round=83; hyaku-inline attempt=1`.

Conformance defects (status-neutral) are recorded at the end, §6.

## 2. Claim re-checks

### C1 — calibration: the round-82 routed-defect queue closes

The claim is decided by the lane's counter `c83_defect_queue.py`; this seat did not run it and
instead re-derived every state conjunct from committed bytes at `64847b5f` (the counter's inputs),
plus the committed receipts. Nothing below rests on a sentence in the lesson that says "closed".

| Item | My command | Observed |
|---|---|---|
| D1 | python3 over `.ufo/waves/round-83/w1-spec.json` + `w1-results.json`, cross-checked against `w1-accounting.json` | items `14` (scout 2, executor 4, scribe 3, reviewer 2, mutation-tester 2, critic 1); requested attack `5`; settled (non-empty output) `14`; settled attack `5`; share `0.3571`; the accounting's `settled`, `settled_names`, `settled_attack`, `settled_share` all equal my derivation; its `spec_sha256`/`results_sha256` recompute to the committed files |
| D2 | `len(output.encode("utf-8"))` for every results row vs `w1-accounting.json` `seats[].output_bytes` | `mismatched=[]`; `bytes_basis="utf-8"`; total `81,754`; smallest settled `3,581`; no empty output row |
| D3 | read `.ufo/waves/round-83/controls/after-c83-instrument-check.txt`; `git merge-base --is-ancestor 70c8241b… 64b71992` | line `C2v1 revision=64b7199281e5457df0e08652977f698c4f34f46e population=30 bound=30 mismatches=0 met=true`; the declared receipt revision `70c8241b` exists and is an ancestor of the measured revision (the receipt itself discloses `declared_match=false` as subject-vs-carrier) |
| D4 | `git diff cb02b705 7678247a -- .ufo/reports/round-81/kake.md`; substring test of the lesson's five `> ` quotes against both blobs | removed physical lines longer than 40 chars: `5`; quoted lines: `5`; all five are raw substrings of `cb02b705:…` and **absent** from `7678247a:…` (`in pre 5 / in post 0`) |
| D5 | `.ufo/waves/round-83/w1/ExecKillers/rows.txt` + `check.txt`; anchor-uniqueness count over the frozen round-82 counters; re-read of `c82_capture_delta.py:239` and `:268` | rows `C1-m3`, `C1-m5`, `C2-m2`, `C2-m4` read `killed`, `C2-m5` reads `equivalent` with guard; `distinguished=5/5`; each of the five patch anchors occurs exactly once; `C2-m5`'s dropped clause is implied because `receipts_ok` (a `met` conjunct) re-derives `surfaces_a == declared` and `declared == 3` is itself a `met` conjunct — the equivalence proof holds. `population.json`'s counter/tool hashes recompute exactly (`1082c691…`, `b93693df…`, `4b0dc252…`) |
| D6 | `corpus/QUALITY.md:1701` | carries `corpus/lessons/round-82.md`, `Gate` and `round-83` in one line: the standing Gate-provenance criterion |

Committed receipts: `controls/after-c1.txt` reads `C1v1 revision=304c0f87… items=6 open=0 closed=6
met=true`, `after_c1_exit=0`; `controls/after-c1-tip.txt` reads the same at `2586243e`,
`tip_c1_exit=0`; `controls/base-c83-defect-queue.txt` reads `items=6 open=6 closed=0 met=false`,
`base_c1_exit=1`; `controls/ctl-c83-junk-queue.txt` (a prose-only tree) reads `open=6 … met=false`,
`junk_exit=1`; `controls/c83-selftest-c1.txt` ends `selftest: 9/9 passed`, `selftest_c1_exit=0`.
**C1 verifies** — re-measured on D1, D2, D4, D5 and D6; evidence-verified for the D3 receipt (its
own fields and the ancestry of its declared revision) and the selftest tally. Score held at 2 by the
lane as declared.

### C2 — freshness: header changes are classified and the verdict re-derives

Re-measured with my own script over the committed capture trees (no lane tool executed):

- **Receipts.** All six (`round-81/capture` and `round-82/capture`) are `method=GET`, integer
  `status=200`, `bytes == len(body.bin)`, `sha256 == sha256(body.bin)`, `truncated=false`,
  `error=null`, `redirects=[]`.
- **Bodies.** Capture A and capture B bodies are byte-identical on all three surfaces
  (`sha256` equal per surface), so `same-object` is substantively right.
- **Header diffs** (my canonicalisation, name-keyed, values joined): primary `4`, robots `5`,
  sitemap `5` → `diffs=14`; changed names are `date`, `x-cache`, `x-fastly-request-id`,
  `x-served-by`, `x-timer`. All five are in the tool's `PER_REQUEST` table
  (`scripts/header_change_class.py:46-51`), so `per_request=14 validator=0 representation=0
  policy=0 unknown=0` and `verdict=same-object`.
- **Control pair** (`.ufo/waves/round-83/capture-control`): receipts verify; each surface's body
  differs by exactly one byte with a matching digest; the primary `ETag` also differs →
  `validator=1` and `representation-changed`, i.e. the verdict can flip.
- **Offline.** `grep -nE '^\s*(import|from)' scripts/header_change_class.py` lists only
  `argparse, hashlib, json, shutil, sys, tempfile, pathlib`; the only `socket|urllib|requests|
  http.client` match is the docstring line 8 ("opens no socket").
- **Record.** `controls/after-c2-classes.txt` per-surface lines and its
  `summary surfaces=3 diffs=14 per_request=14 validator=0 representation=0 policy=0 unknown=0
  verdict=same-object` equal my computed counts.

Committed receipts: `controls/after-c2.txt` at `304c0f87` and `after-c2-tip.txt` at `2586243e`
both read `met=true`, exit 0, with `# control=verdict=representation-changed validator=1`; base
`controls/base-c83-drift-class.txt` reads `tool_absent=1 … met=false`, exit 1; the identical-pair
control `controls/ctl-c83-control-class.txt` reads `control_ok=0 … met=false`, exit 1; counter
selftest `9/9` with the tool's nested `6/6`, exit 0. `record_equal` and `determinism` are
evidence-verified from those receipts. **C2 verifies** (re-measured from the committed capture
bytes; the receipts for the conjuncts that need a tool run are evidence-verified). Score held at 10.

## 3. Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration (2, lowest non-retired) | **improved** | C1: all six routed round-82 defects have their state conjunct re-derived from committed non-lesson bytes (D1, D2, D4, D5, D6) or a committed receipt with a resolvable revision (D3); base and junk controls red, selftest 9/9 green |
| freshness (10, held) | **improved** | C2: the round-82 drift count becomes a classified verdict that re-derives offline; receipts verify, bodies equal, all 14 moved fields per-request, and a one-byte/ETag control pair flips the verdict. Score held by the lane as declared |
| operability | unchanged | no operability claim; the round adds instruments (`header_change_class.py`, `run_killers.py`) but claims neither as an operability move |
| coverage | unchanged | outside this lane's scored ownership; the new `knowledge/` entry is counted under expansion |
| depth | unchanged | outside this lane's scored ownership; no claim |
| adjacency | unchanged | no sibling-overlap seat this wave (disclosed); the new entry cites no sibling path and `PROVINCE.md` §Round 83 claims no sibling ground |

No owned axis is harmed: `git diff --numstat 826b0061 64847b5f` shows the only modified tracked
files are append-only — `LOG.md` 12/0, `PROVINCE.md` 23/0, `SCORECARD.md` 44/0,
`corpus/QUALITY.md` 4/0, `corpus/README.md` 15/0, `corpus/SOURCES.md` 1/0 (adds/removals). Every
score cell in `SCORECARD.md` is untouched.

## 4. Discernment spot-check (non-author)

Source re-opened twice: the retained copy `.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt`
(84,477 bytes, sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`) and a
fresh GET of `https://www.rfc-editor.org/rfc/rfc9111.txt` on 2026-11-04 (`http_code=200`,
`size=84477`) — the live body is **byte-identical** to the retained copy.

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| `S456` — RFC 9111 as the ground for reading two dated captures of one URI | admit (tier A, `spec`, `mined`) | retained `rfc9111.txt` `:583-585`; `corpus/SOURCES.md:203` | **agree** | The admission quote (`A "fresh" response is one whose age has not yet exceeded its freshness lifetime. Conversely, a "stale" response is one where it has.`) is 23 words — inside the ≤25-word cap — and a whitespace-normalized substring of the retained bytes with exactly one occurrence; it grounds the freshness/stale fact in the row's `teaches`. The row is `S456`, eleven cells, `kind=spec`, `tier=A`, `status=mined`, `opened=2026-11-04`, `recheck=365d`, `used-by corpus/knowledge/header-change-classes.md` (exists) |
| the 65-word `:587-592` freshness-lifetime paragraph as the admission quote | reject | retained `:587-592` | **agree** | My count of that span is exactly 65 words — past the ≤25-word cap — and it restates the admitted `:583-585` definition; admitting it would break the cap or force a truncation |
| `:838-839` / `:840-844` (entity tag as "another validator") as `S456`'s anchor | reject | retained `:838-844`; `corpus/SOURCES.md:202` | **agree** | `S455` at `:202` already owns strong/weak validator semantics (RFC 9110 §8.8.1/§8.8.3, admitted round 82); the classifier's `validator` class is a naming decision over two header names, not a claim about validator strength, so re-anchoring it here would count one source twice |
| RFC 9111's invalidation and Cache-Control-directive sections as anchors | reject (decision) | retained `:1017` (§4.4 *Invalidating Stored Responses*) and the `:1051`/`:1081`/`:1111`/`:1203`/`:1408` headings | **agree on the decision, disagree on the cited title** | The decision holds: the tool compares two GET captures, evaluates no directive and models no store, so either anchor would claim a rule the code does not implement. But the lesson names a "*Common Cache-Control Directives*" section that does not exist in RFC 9111 — the real headings are §5.2 *Cache-Control*, §5.2.1 *Request Directives*, §5.2.2 *Response Directives*, §5.2.3 *Extension Directives*. Routed (§6, item 1) |

New `SOURCES.md` row re-opened: **S456** at `corpus/SOURCES.md:203` — eleven cells, `id` new and
unused, `kind=spec`, `tier=A`, `status=mined`, `opened=2026-11-04`, `recheck=365d`, `used-by` naming
one existing path; its ≤25-word admission quote is the 23-word `:583-585` span above. Census
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exits **0** with 22
`W04` warnings and one `ok` line (identical to `controls/census-after.txt`); rows
`193 → 194` (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at `826b0061` and `64847b5f`),
and my replication of the census W04 rule over the base blob gives 22 as well.

Also verified in the same pass: `corpus/knowledge/header-change-classes.md` opens with
`source:`/`verified-at:`/`recheck:` and its 18 claimed quote spans are each a literal substring of
the named physical line in the retained RFC (my script: 18/18), plus the fenced `:340-342` block is
byte-equal to those lines.

## 5. Trend verdicts and frontier

- **expansion — improved.** One net-new admitted `knowledge/` entry on ground the coverage map did
  not hold (`corpus/knowledge/header-change-classes.md`, absent at `826b0061`, present at
  `64847b5f`), its `source:` citing `S456` — a `mined` row opened this round — and the coverage map
  gained the matching row (`corpus/README.md` §Coverage — round 83). Registry **193 → 194**.
- **quality — improved.** Both claims are decided by counters with committed base/junk/control
  pairs and green selftest tallies (9/9 and 9/9 with the tool's 6/6); D5 closes the five round-82
  mutation survivors (four kills, one proven equivalence with the guarding conjunct re-read); D6
  adds a standing `QUALITY.md` criterion against Gate-summary drift; no admitted entry was found
  false or stale and left unmarked.
- **discernment — improved.** This non-author spot-check agrees with the round's Gate on the one
  admit and all three rejects at the decision level, with the source re-opened live and the registry
  row re-validated by the census; that is the `LEARNING.md` condition for `improved`. One defect it
  found — a reject's cited section title absent from RFC 9111 — is recorded and routed (§6 item 1),
  not left silent, and it does not overturn the reject.

## 6. Routed defects (lane to fix next round; status-neutral)

1. **Gate citation title (discernment).** `corpus/lessons/round-83.md` §Gate rejects "RFC 9111's
   *Invalidating Stored Responses* and *Common Cache-Control Directives* sections"; the second title
   does not exist in the retained RFC (headings: §5.2 *Cache-Control*, §5.2.1 *Request Directives*,
   §5.2.2 *Response Directives*, §5.2.3 *Extension Directives*). The reject stands; append a
   named correction in the next lesson and cite the real headings.
2. **Gate word-count line (quality).** The same Gate says the `:838-839`/`:840-844` quotes are
   "22 + 44 words" but its check line records "word counts 14 / 23 / 21 / 48"; my count of the
   `:838-844` span is 66 words (48 only if the final parenthetical is dropped). State one
   measurement and the span boundary next time.
3. **Connector seat (L2 floor).** Prompt §3's minimum role split asks for 1× connector; wave `w1`
   carried none (disclosed in the report). Either carry one connector seat or file the waiver with
   the wave's claimed-shape rationale in the report.
4. **Round-start census receipt (frontier step).** The report gives the round-start census as prose
   ("exit 0, 22 `W04`") while only `controls/census-after.txt` is committed; the round-82 precedent
   committed a before receipt. Commit the start-run output next round (my base replication over
   `826b0061:corpus/SOURCES.md` gives 193 rows / 22 `W04`, consistent with the prose).

## 7. Verdict and limits

**Admitted.** Both claims verify by this seat's own re-derivation against the committed bytes at
`64847b5f` (C1: five of six state conjuncts re-measured, the sixth evidence-verified from its
receipt and revision ancestry; C2: receipt verification, body equality, class counts, control flip
and offline property re-measured, the tool-run conjuncts evidence-verified), and no axis is harmed
(`SCORECARD.md` additions only). The conformance defects above — the connector-seat deviation, the
uncommitted start census, two Gate citation/precision slips — are recorded and routed; they do not
change the lane status, which is `ok` (a real report naming real, checkable work and a resolvable
tip commit).

Limits inherited and confirmed: C1's D3 is decided by the lane's own gate receipt, which this seat
did not re-execute; C1's row conjuncts are textual, so a records-only tree with the right sentences
opens nothing but a transcription is this closure's catch; C2 decides the capture chain, not the
property — a well-formed fabrication with real digests would pass — and value-level reading of a
changed `policy` header stays frontier; the freshness score is held and was not re-measured live.
SHONEN: three boxes are `[~]` author-side and box 2 is a declared `[ ]` gap; no box is `[x]`, so
this round supplies no promotion evidence (promotion is operator-owned).
