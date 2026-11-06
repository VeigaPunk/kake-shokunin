# Round 100 — C1 one-row-per-tool registry calibration and C2 304 freshening contract v2

Round base `3989618d9f8310b2eb5fb456aa7c4e58fb0b5ff5`; instruments `d7b73d161173710d04efc5f66784779bce5746ff`;
freeze `69cdc1eb8e456b3a7e4db2b24c9e5c5dfc343e5e`; C1 repair `e84a18714b6be7fd2456a2dcc5f28c0cb0ab981f`.
One v1 wave of 14 seats (`.ufo/waves/round-100/w1/`); attempt 1's L1 (KakeR100) died after
dispatch, attempt 2 (KakeR100a2) integrated. The outside closure owns admission.

## Verdicts recorded by the L1

- **C1 calibration — met on the frozen predicate.** Counter: `duplicated=7 probe_mismatch=2
  exec_fail=1 mismatches=9 met=false` exit 1 at base `3989618d` (`controls/base-c1.txt`) →
  `unlisted=0 dangling=0 duplicated=0 probe_mismatch=0 mismatches=0 met=true` exit 0 at `e84a1871`
  (`controls/after-c1.txt`); C1 re-read at the C2 commit `06c81f08` still `met=true`
  (`controls/tip-c1-at-c2.txt`). Review conjunct: ReviewRegA `agree=8 disagree=0 of 8`, ReviewRegB
  `agree=8 disagree=0 of 8` — every unit carried by both seats (`w1/ReviewReg{A,B}/verdicts.tsv`).
  Instrument caveats (routed, never re-scored): CriticClaims A1-A5 (wrapper-prefix grammar, dropped
  tables, probe-token special-casing) and SentinelScope R1/R2/R3/R4/R12 (probe-aware tool,
  pid detection, read-write shared scored tree, bwrap fail-open) show that the counter alone can be
  driven to `met=true` by a hostile tree. Held-out check on the real tree: no committed tool names
  the probe token or `getpid`, and the repair changed no tool (`controls/post-freeze-heldout-c1-gaming-scan.txt`).
- **C2 freshness capability, contract v2 — met on the frozen predicate.** `hand=72/91
  generated=224/300 met=false` exit 1 on the landed v1 blob at base (`controls/base-c2.txt`) →
  `candidate=present sha256=00edf6c4… hand=91/91 generated=300/300 refusals=122/122 met=true` exit 0
  at `06c81f08`, scored sha256 = `git show 06c81f08:scripts/freshen_304.py | sha256sum`
  (`controls/after-c2.txt`). R95-D held-out column: ExecTwinFresh `inputs=3600 disagreements=0`;
  the landed candidate agrees with the frozen oracle on all four CriticClaims X1-X5 probe inputs
  (`controls/post-freeze-heldout-critic-probes-landed.txt`, `heldout_same=4/4`). Caveats: CriticClaims
  X1-X5 are escapes of the counter population by mutated candidates (not of the landed one);
  MutCounters fr-m14 (judge whitespace strictness) survives; ReviewFresh G3 (stored-side qualified
  Cache-Control copied verbatim) is a contract gap no case covers.

## Gate

> Fetch receipts: ScoutSources re-opened both RFCs on 2026-11-06T01:48:09Z, one GET each, HTTP 200
> (`w1/ScoutSources/report.md`): RFC 9111 84 477 bytes sha256 `aeb52adb…` byte-identical to
> `.ufo/waves/round-99/sources/rfc9111.txt`; RFC 9110 502 941 bytes sha256 `21c1cdce…`
> byte-identical to `.ufo/waves/round-100/sources/rfc9110.txt`. The L1 re-derived both digests and
> re-read the quotes below by line in the retained bodies (attempt 2, 2026-11-06). Rows landed at
> `06c81f08`, after the re-open, as the freeze requires.

### Row S486 (RFC 9111 §5.2, §5.2.2.4, §5.2.2.7, §5.2.3, §3.1 proxy sentence) — **admitted**

- **URL / access:** `https://www.rfc-editor.org/rfc/rfc9111.txt`, accessed 2026-11-06.
- **Kind / tier:** spec / A. **Scope:** Cache-Control directive grammar, case-insensitive names, both
  argument forms, qualified `no-cache`/`private` field-name forms, MUST-ignore for unrecognised
  directives; distinct from S484 (§3.1/§3.2/§4.3.4) and S456 (which excludes argument syntax).
- **Located quotes (≤25 words):** lines 1098-1100 «Cache directives are identified by a token, to be
  compared case-insensitively, and have an optional argument that can use both token and
  quoted-string syntax.» (24 words); lines 1411-1412 «A cache MUST ignore unrecognized cache
  directives.» (7 words).
- **Status / opened / recheck / used-by:** `mined` / 2026-11-06 / 365d / `corpus/knowledge/freshening-304.md`.
- **Census:** W04 duplicate URL across scopes with S484 — intended, scopes disjoint (accepted warning).

### Row S487 (RFC 9110 §5.5, §5.6.1.2, §5.6.2, §5.6.4) — **admitted**

- **URL / access:** `https://www.rfc-editor.org/rfc/rfc9110.txt`, accessed 2026-11-06.
- **Kind / tier:** spec / A. **Scope:** field-value trimming, recipient list syntax with empty
  elements, token and quoted-string productions behind Cache-Control arguments; distinct sentences
  from S465/S466/S478 (ScoutSources finding, wording checked by the L1 against the row's scope cell).
- **Located quotes (≤25 words):** line 1591 «A field value does not include leading or trailing
  whitespace.» (10 words); line 1702 «#element => [ element ] *( OWS "," OWS [ element ] )»;
  lines 1786-1787 «quoted-string = DQUOTE *( qdtext / quoted-pair ) DQUOTE».
- **Status / opened / recheck / used-by:** `mined` / 2026-11-06 / 365d / `corpus/knowledge/freshening-304.md`.

### Reject — merge/kake package adoption

- **Rejected again.** Collision check re-derived (`.ufo/waves/round-100/assimilation/`): `reg-ids`
  222, `staged-ids` 129, `collisions` 8 (`S312 S329 S367 S372 S373 S374 S390 S409`). Guard proven on
  the indented fixture `guard-fixture.md` (`  | S002 | x |`) → `guard-collisions` = `S002` (nonempty).
  No renumber map, no per-entry re-grounding → nothing appended (`Assimilation: none`).
- **Quarantine slice:** 12 rows (9 `payload-absent`: S142 S143 S148 S156 S161 S193 S194 S195 S206;
  3 unverifiable "could not be fetched": S154 S178 S184) — not hand-checked this round; adoption stays closed.
- **Flip:** a round that builds the renumber map in scratch and re-grounds each adopted entry.

### considerthese

- `considerthese/2026-11-05.md` proposal 3 (held-out vs frozen divergence) — the freeze named it,
  but it is already `corpus/QUALITY.md` §Round 95 R95-D (Mistake 2). Applied, not re-landed: the
  verdicts above carry the held-out column. Proposals 2 and 4 are landed too (R98-B in
  `corpus/lessons/round-98.md`, R99-A in `corpus/lessons/round-99.md`); the markup-tolerant grep of
  Mistake 2 prints nothing only for proposals 1 and 5.
- **Mined: proposal 5 (branch triage with diffs)**, opened as read-only git
  (`.ufo/waves/round-100/considerthese-p5-branch-triage.txt`):
  `origin/considerthese-curation-20261103` (`0ed317e4`, 5 commits over merge-base `dbcfef0b`) adds
  five `considerthese/2026-11-03-curated-sources*.md` files (118 lines, 14 URLs) absent on master —
  operator-curated candidate sources, not corpus rows; `origin/cloud-reviewed-export-20261103`
  (`d3d744c9`) shares no history with master (merge-base rc 1) and carries 32 paths, among them ten
  knowledge entries absent on master (`corpus/knowledge/cloud-20261103/*`, two more). Neither
  touches master's `corpus/SOURCES.md`; nothing is adopted (each URL would need an in-round open
  under CORPUS.md rule 1). Routed R100-5: the 14 curated URLs are the next rounds' source
  candidates; the export entries need a lane review before any row cites them.

## Mistakes

| # | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| 1 | **Masking by an any-row-conforms rule (instrument design, calibration).** The round-99 registry counter lists a tool when **at least one** conformant row exists, so a second, broken row for the same tool is printed as `exec_fail` but never scored: the `robots_audit.py` row at `SKILL.md:1104` carried a self-test span that cannot run (`[--tool PATH]` reaches the tool as literal argv, rc 2) from round 37 to round 99, and the round-99 C1 after-receipt shows `exec_fail=1` on the same line that reports `met=true`. Six more tools had two rows that answered differently (verdict maps, self-test cells), invisible to the same rule. | `.ufo/waves/round-99/c99_registry.py:31` ("A tool is listed when at least one conformant row exists for it"); `.ufo/waves/round-99/controls/after-c1.txt:3` (`exec_fail 1104 scripts/robots_audit.py rc=2` beside `met=true`); `.ufo/waves/round-100/controls/base-c1.txt` (`duplicated=7 probe_mismatch=2 exec_fail=1`) | none — R99-5/R99-6 routed the residue but no criterion scored a shadowed row | Counter v2 `c100_registry.py` scores every row that invokes a tool: D1 `duplicated` (a tool invoked by ≥2 rows) and D2 `probe_mismatch` (every invoking row's verdict map must name the rc of an executed `--zz-bogus-r100` probe). Shown able to fail: `controls/base-c1.txt` exit 1 (`mismatches=9`), `controls/ctl-c1-keepold.txt` exit 1 (stale rows kept: `probe_mismatch=2 exec_fail=1`), selftest cases `v2-duplicate-rows`, `v2-shadow-nonconformant` (`controls/ctl-c1-selftest.txt`). |
| 2 | **Stale "unimplemented" pick (assimilation bookkeeping).** The freeze named `considerthese/2026-11-05.md` proposal 3 (held-out vs frozen divergence) as this round's mined proposal, but it already landed as `corpus/QUALITY.md` §Round 95 R95-D; §10 allows only a still-unimplemented proposal. | `.ufo/waves/round-100/freeze.md:94-95`; `corpus/QUALITY.md` §Round 95 (R95-D cites "proposal 3") | prompt §10 ("At most ONE still-unimplemented proposal") — no lane check ran it | Before naming a proposal, `grep -rlniE "<file>\.md.{0,30}proposal[^0-9]{0,4}<N>([^0-9]|$)" corpus/QUALITY.md corpus/lessons/` must print nothing. Shown able to fail twice: for proposal 3 it lists `corpus/QUALITY.md` and lessons r94/r95; for proposal 4 it lists `corpus/lessons/round-99.md` (R99-A) — a first, markup-blind pattern (`.{0,6}` with backticks) printed nothing there because R99-A writes "Part 2 **proposal 4**", and attempt 2 drafted a duplicate criterion before the tolerant pattern caught it (draft removed). Proposals 1 and 5 print nothing; 5 is mined. |
| 3 | **Attempt-1 L1 died after dispatch (wave health).** KakeR100 wrote `w1.ready` (taken 22:46:35) and died before WAVE-DONE; 13 of 14 seats filed reports, ScribeLesson none; attempt 2 inherited every artifact. | `.ufo/watchdog.log` `lane-dead-no-report kake round=100` 23:31:17; `.ufo/waves/round-100/w1.ready.dispatched` | none (provider/session failure, not a lane rule) | Inherited outputs re-verified before reuse: both after-receipts reproduce (`controls/after-c{1,2}.txt` rerun by CriticClaims/ReviewDeterminism `3/3 identical`); recorded, not a criterion. |

## Quality criteria added this round

See `corpus/QUALITY.md` §Round 100: **R100-A** (an executing registry probe uses a per-run random
token on a read-only, per-row tree and fails closed when the sandbox fails — SentinelScope
R1/R3/R4/R12, CriticClaims A5) and nothing from considerthese (proposal 5 lands as the Gate item above, R100-5).

## Routed to round 101

- R100-1 C1 counter hardening: `invoked()` grammar (env, `bash -c`, `uv run`, `-X <value>`),
  near-registry tables reported not dropped (CriticClaims A1-A4, A7); random probe token, `--ro-bind`
  per-row tree, `sandbox_ok()` gate, `.ufo/` excluded from the scored archive (SentinelScope R1-R5,
  R12); rlimits/total budget (R9/R10).
- R100-2 C2 counter: judge whitespace strictness forgery (MutCounters fr-m14), population classes
  X1-X5 (vertical tab trim, BOM, bare `=`, env-conditional, stored qualified CC) as hand cases;
  memory/pids cgroup for cases (SentinelScope F11/F12); provenance vs reformatted reference (Critic F2).
- R100-3 contract v3: stored-side qualified Cache-Control (ReviewFresh G3); LC marks for e2 and
  obs-text (G1/G2); F4-F9, F11 stay open.
- R100-4 mutation survivors registry 7, fresh304 4 (`w1/MutCounters/survivors.md`).
- R100-5 considerthese branches: 14 curated URLs (`considerthese-curation-20261103`) as source
  candidates; lane review of the unrelated `cloud-reviewed-export-20261103` entries.
- Carried: R99-*, R98-1…5, R97-1/2/3/5, R96-3, R95-6, L0 R95-2; quarantine slice of 12 rows.
