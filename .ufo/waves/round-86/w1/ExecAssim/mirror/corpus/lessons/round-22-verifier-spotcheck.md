author: hyaku closure (non-author integrator, @m_opus)

# Round 22 — verifier spot-check (non-author closure, hyaku)

Date: 2026-10-21. Closure prompt: fleet `.ufo/prompts/closure/kake-round-22.md`.
Lane HEAD before `7c61c8cc791bde36dd5e3688bdfea2678d90146c`, after
`d5a03697c780fc6b5721ac0065fdb89ed4a7815c`. This reviewer authored no round-22
work and dispatched no seat for it (a request for 3 read-only re-check seats was
refused by the host job cap; every re-check below was run by this reviewer alone).
The lane's 136 seats and the recovery coordinator are author-side.

Driver digest (copied from mutable `.ufo/watchdog.log`):

```text
2026-10-20T18:30:56-03:00 launch kake round=22 pgid=1128758 driver=hyaku-inline attempt=1
2026-10-21T02:47:17-03:00 lane-dead-no-report kake round=22; retry same round (hyaku-inline attempt=1: attempt-1 coordinator ended before report (prior session SIGHUP/provider quota); operator-authorized recovery coordinator 2026-10-21 reuses retained round-22 work)
2026-10-21T02:47:18-03:00 launch kake round=22 pgid=538289 driver=hyaku-inline attempt=2
2026-10-21T03:19:54-03:00 complete kake round=22; hyaku-inline attempt=2
```

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane | `git log --format='%an %H' -- .ufo/reports/round-22/kake.md` (fleet) | `kake-shokunin 712c62043e3c…` (03:18:35) and `kake-shokunin d7ecdb599a84…` (03:19:35) | pass |
| Report not filed before its commits | `git log -1 --format=%cI` per hash | 712c620 cites tip adc04da (03:17:39); d7ecdb5 cites 1dc75e3 (03:18:55) and d5a0369 (03:19:21) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, all `[ ]`, each with a reason | pass |
| Cited commits exist and are ancestors of the branch | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> refs/heads/master` for c0fd6d53, 26b27af3, b539cc17, adc04dae, 1dc75e39, d5a03697 | all exit 0; all authored `kake-shokunin` | pass |
| Pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain` | `local=remote=d5a03697… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | pass |
| Prompt carries template contract | `diff templates/round-prompt.md .ufo/prompts/kake-round-22.md` (first 140 lines) | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions; §6 hyaku addendum appended | pass |
| Gate registry row | `SKILL.md:411` | `canonical-audit` row: gate, entry, verdict map 0/1/2/64, `--selftest`, pinned paths, write scope | pass |
| Marker? | — | real report naming checkable pushed commits | not a marker → `ok` |

No step-1 conformance defect found. Misroot: fleet root `err.txt`/`out.txt` are
absent now (`ls` → no such file); `git show d5a0369:out.txt` is the
could-not-evaluate usage JSON the lesson describes.

## Per-claim re-check — C1 operability (offline static canonical preflight)

Re-measured by this reviewer with jq over committed bytes (lane counter and
validator not executed — Gate standard, closure consequence):

```text
jq '.runs[].exit' measure-before-v2.json            → 0 0 ; runs identical (unique stdout = 1)
  .runs[0].stdout|fromjson                           → accepted 0, total 32, available false, instrumentValidated true, results 0
jq '.runs[].exit' measure-after-v2.json             → 0 0 ; runs identical
  rows with status PASS                              → 32
  rows with actualExit==expectedExit and sorted(actualFindings)==sorted(expectedFindings) → 32
  caseId set vs cases.json caseId set                → identical (32 unique)
  per-row expectedExit+expectedFindings vs cases.json → identical
sha256sum measure.py matrix.py cases.json           → fa916ada… / d7de622c… / 28a49013… (equal to runnerSha256 and the PINNED_INSTRUMENT_SHA256 constants)
git show b539cc1:scripts/canonical_audit.py | sha256sum = git show d5a0369:… = frozen/expected.json validator pin 5de32200…
git diff --stat c0fd6d5 d5a0369 -- cases.json fixtures matrix.py contract.json → empty (frozen population unchanged)
git diff --stat b539cc1 d5a0369 → only evidence, LOG, SCORECARD, lesson, err.txt, out.txt (no validator/instrument bytes)
```

0/32 → 32/32 reproduced; finding distribution: clean 15, canonical_mismatch 3,
canonical_url_invalid 3, canonical_href_missing 2, canonical_multiple 2,
input_invalid 2, one each of the other five ids.

**Counter fix (the prior counter accepted the matrix's own declared total).**
`git diff c0fd6d5 b539cc1 -- .ufo/waves/round-22/measure.py`: c0fd6d5 returned
`accepted` from the matrix JSON and failed only on `accepted != total`. b539cc1
adds `reconcile_rows()` (numerator = rows whose `actualExit`/`actualFindings`
equal the pinned `cases.json` oracle; PASS status must agree with that comparison;
declared `accepted`, `executed`, `discrepancies` and matrix exit are cross-checked),
`PINNED_INSTRUMENT_SHA256` for matrix.py/cases.json (stub matrix rejected before
rows are read), exit 2 for an unvalidated baseline, and `total` forced equal to
`BASELINE_TOTAL = len(EXPECTED_CASES)` with a duplicate/missing/extra case-id
check. Committed `postfix/counter-probe-before.json` (c0fd6d5 runner): CE1
accepted 32 exit 0, CE2 exit 0, CE3 accepted 32 exit 0 → `passed:false`;
`-after.json`: all three exit 2, `rejected:true`, `passed:true`. Fix is real.

**Gate evidence (evidence-verified, not executed):** `postfix/selftest-after.json`
62/62 cases passed (c0fd6d5: 56/56, none of the new cases);
`postfix/defect-probe-before.json` 2/8 met → `-after.json` 8/8 (probe
`network_path_empty_authority` feeds `href='///project/a.html'`, after: exit 1
`canonical_url_invalid`); `postfix/replay-after.json` `frozen_replay_match`,
69 inputs verified (= 69 sha256 pins in `frozen/expected.json`), 32 cases compared.

**Reuse honesty.** `w1-dispatch.json`/`w2-dispatch.json` registry members vs
report files: w1 64 dispatched, 60 reports, missing exactly the 4 scribes
(Knowledge, LessonDraft, RegistryDraft, TrendDraft) with the 429 text in
`w1-deaths.json`; w2 64 dispatched, 43 reports, missing exactly the 21 names in
lesson §Reuse and discard (9 reviewer, 8 scout, 4 connector by registry role);
residual 8 reports. 64+64+8 = 136. w2 reports land only in checkpoint 26b27af and
are byte-unchanged to the tip. No artifact credits a dead seat; the four last
fixes are disclosed as probe-verified only; S020–S027 non-re-open is disclosed.

**Web-property probes stayed read-only.** `scripts/canonical_audit.py` imports no
socket/urllib.request/http.client; `subprocess` and `open(...,"w")` occur only in
the `--selftest` path (lines 797–929, temp dir). The only owned-property bytes are
`domain-snapshot/index.html`, whose sha256 `43d321f9…` equals
`git show 31c465f1:docs/charter-ufo-fsd/index.html` in `~/Projects/ufo-fsd-alpha`
(file last changed 2026-09-25, before the round); `provenance.json` states no
deployment/live URL. Seat network use found by `git grep curl|wget` is GETs of
public spec/doc URLs (rfc-editor, WHATWG, Python, Google docs); no POST/PUT,
deploy, publish or DNS action in any round-22 seat report, lesson or LOG entry.

**No owned-axis harm.** `git diff 7c61c8c d5a0369 -- SCORECARD.md` is a pure
append (capability row + round-22 section, operability HOLD 10); SKILL, PROVINCE,
QUALITY, LOG and the knowledge entry are pure appends from the base. Committed
`final-suite.txt` at b539cc1: corpus-contract exit 0; paths gate exit 1 with the
carried red (3 targets, missSet 55, no new miss) — identical to round 21's routed
debt.

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| operability | improved | C1 re-derived 0/32 → 32/32 from committed per-case rows against the pinned oracle; registered gate with committed selftest 62/62 and frozen per-case replay; score HOLD 10 |
| freshness | unchanged | no pin or sweep change; carried paths red identical; no live re-verification claimed |
| coverage | improved | knowledge entries 21 → 22 (`git ls-tree corpus/knowledge`), on canonical-signal ground PROVINCE listed as Frontier; not a declared claim |
| depth | unchanged | no pre-existing entry deepened |
| adjacency | unchanged | browser execution left to tabi, publishing operator-owned (PROVINCE append) |
| calibration | unchanged | gaps disclosed honestly (dead seats, probe-only fixes); no calibration claim |

## Discernment spot-check (round-22 `## Gate` and recovery receipts)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S020 RFC 6596 §3 “Specify a relative IRI (see [RFC3986], Section 4.2).” | admit | https://www.rfc-editor.org/rfc/rfc6596.html (fetched 2026-10-21) | agree | text present under “The target (canonical) IRI MAY:” in §3; supports permitting relative canonicals |
| S028 RFC 9110 §4.2.1/4.2.2 “A recipient that processes such a URI reference MUST reject it as invalid.” | admit (recovery) | https://www.rfc-editor.org/rfc/rfc9110.txt, sha256 `21c1cdce…7232a` | agree | quote present in both §4.2.1 (http) and §4.2.2 (https) after the empty-host sentence; digest equals the row |
| S029 RFC 3986 §3 “When authority is not present, the path cannot begin with two slash characters ("//").” | admit (recovery) | https://www.rfc-editor.org/rfc/rfc3986.txt, sha256 `3102dae4…b2d683` (line 876–878) | agree | quote exact; digest equals the row |
| S027 Python urllib.parse “urlsplit() does not perform validation.” | admit | https://docs.python.org/3/library/urllib.parse.html | agree | warning text present verbatim |
| Calling an HTML-policy match search-engine selection | reject | S022 https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting (last updated 2026-08-21) | agree | opening paragraph: “Even if you explicitly designate a canonical page, Google might choose a different canonical…” |
| WHATWG URL slash-skipping not opened as a row | reject | https://url.spec.whatwg.org/ “special authority ignore slashes state”; committed selftest `network_path_empty_authority(_four)`, `base_empty_authority` | agree | WHATWG skips extra slashes for special schemes, RFC reads an empty authority; the validator rejects `///` and `////` either way, so the row would not change a decision |

Newly written `SOURCES.md` rows re-opened: S028 (13-word quote) and S029
(15-word quote), both ≤25 words and located; digests match. S020/S022/S027
re-opened here as well, partially closing the lane's disclosed S020–S027 gap
(S021, S023–S026 still not independently re-opened).

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
→ `kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`, exit 0.
Rows 19 (7c61c8c) → 27 (c0fd6d5) → 29 (d5a0369) by `grep -cE '^\| *S[0-9]{3} '`.

## Trend verdicts

- **expansion: improved** — one new knowledge entry on Frontier ground whose
  `source:` cites mined rows S020/S021/S026/S027/S028/S029, and a capability row
  whose run evidence verifies (above).
- **quality: improved** — bounded: the attempt-1 entry was superseded in-round by
  a stronger one (empty-authority, symlink-scope and usage-JSON boundaries
  grounded on S028/S029), five re-opened rows agree, and no admitted entry failed
  re-check.
- **discernment: improved** — this outside spot-check agrees with the gate on
  four admits and two rejects; the two new QUALITY criteria cite recovery
  mistakes (one carries an inverted fail predicate, routed below).

## Admission

C1 re-derived and verified; no axis harmed → **admitted**.

## Routed defects / notes for the lane (next round)

1. `corpus/QUALITY.md` “Derived counts” criterion says it “Fails if
   `postfix/counter-probe.py` against the counter exits 0”, but counter-probe.py
   returns 0 when all three counter-examples are rejected (`passed:true`) —
   the predicate is inverted. Append a named correction (should read nonzero/1).
2. Misroot copies `err.txt`/`out.txt` were committed at the lane root; move them
   under `.ufo/waves/round-22/residual/` (or record why root placement is kept).
3. `postfix/{counter,defect}-probe-before.json` name `/tmp/kake-r22a2/*_c0fd6d5.py`
   runners; reproducible via `git show c0fd6d5:<path>`, but record that command
   with the receipt (tmpfs paths are not evidence).
4. Four last fixes (`..` split, help synopsis, fd ownership, counter digest pin /
   executed floor) are probe-verified, not seat-reviewed; 21 dead w2 items
   (incl. S021, S023–S026 re-opens and nine Boundary attacks) remain unattacked.
5. Carried: paths gate red (3 targets, missSet 55) — restore or retire, operator-owned.
6. SHONEN: all four boxes `[ ]`; no box is yet fully checkable by a non-author
   (no end-to-end domain task logged). Promotion stays operator-owned.
