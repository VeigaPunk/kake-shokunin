# PriorGates — kake round 21 wave 1 (KakeR21.PriorGates)

Read-only review. No corpus file was edited, no command was run against the fleet, no commit was made. Reconstruction date for wording purposes: 2026-10-20.

Base: `5009ecaa1cce10b895617a585ddd3f7c7c923a84`. The working tree was changing while this review ran (sibling C2 seats were appending Gate sections and `round-21.md` appeared). Every line anchor below is a **base** line, verified with `git show 5009eca:<path>`. Where the working tree differs, that is noted as a sibling-state observation, not as base fact.

Tools: none installed or updated.

---

## 1. Population and heading state (base)

**C2 population: 15 lane-authored lessons.** Derived from directory names under `corpus/lessons/`, excluding aggregator and verifier files:

| Included (15) | Excluded (8, non-lane) |
|---|---|
| round-1, round-3, round-4, round-5, round-6, round-7, round-8, round-9, round-10, round-12, round-16, round-17, round-18, round-19-recensus, round-20 | round-1-aggregator-audit, round-4-aggregator-audit, round-5-aggregator-audit, round-5-aggregator-mirror-pathless-cli-invocation, round-6-aggregator-audit, round-8-aggregator-box3-coldrun, round-9-aggregator-corpus-verdict, round-20-verifier-spotcheck |

"14 other lessons" = the 15 minus round-20.

**Exact `## Gate` heading at base** (`grep -n '^## Gate$'`):
- `round-20.md:41` only. The other 14 have **no** Gate section at base.
- `round-20.md:182` is `## Gate — round-20 resume` (not an exact match).
- `round-8-aggregator-box3-coldrun.md:31` is `## Gated steps (cannot cold-execute)`. A prefix regex `^## Gate` matches it. It is an excluded file, but the counting regex must anchor with `$`.

**Sibling-state observation (working tree, not base):** at the time of the last scan, `round-4.md:44` used `## Gate — round-21 retrospective reconstruction`, which is not the exact heading the spec asks for. The spec says `## Gate`, with the retrospective label placed in the body. `round-8.md:60` and `round-10.md:64` had already switched to exact `## Gate`. Main should re-check the exact-heading count after integration.

---

## 2. Existing round-20 Gate sections (read only; leave unchanged)

Two sections exist at base.

**A. `## Gate` (`round-20.md:41-60`), original 2026-10-15 attempt.**
- Candidates considered: three items, each with an admitted or rejected status.
- Rejected, with reasons: re-pinning old misses; treating plan/render success as a dispatched wave.
- Outside spot-check: `unavailable` (`:58-60`).
- Assessment: complete for its date. Its status fields are historically true and should be quoted, not rewritten.

**B. `## Gate — round-20 resume` (`round-20.md:182-196`), 2026-10-19 resume.**
- Admitted: four knowledge entries (`crawl-scope-per-host`, `ghp-custom-domain`, `ghp-etag-anatomy`, `ghp-served-set`), seven `QUALITY.md` criteria, the C2 checker.
- Rejected: S017 (Astro `public/CNAME` as the Actions custom-domain mechanism; contradicted by S005) and S018 (DebugBear "Firefox 114"; Firefox 144.0 notes carry `interactionId`).
- Not admitted: the scout's eight GHP observations (`ghp-subpath-spotcheck.md:24-26,39-41,65-82`, `round-6.md:33-34`) stay frontier.
- Outside spot-check: `still owed` (`:194-196`).
- SOURCES rows S001–S018 at `:203-220`.

**Completeness review (findings, not edits):**
1. **Stale "owed" statement.** `:194-196` says the outside spot-check is still owed. `corpus/lessons/round-20-verifier-spotcheck.md` (base, 17 lines, integrator-written) records a later non-author spot-check after landing at `9639ec7`: admit `crawl-scope-per-host` = agree; reject S017 and S018 = agree (`3/3 sampled gate decisions agree`), verifier `W3ReviewKake`, reviewer re-opened 18 of 18 rows. `round-20.md` contains no pointer to that file. Both statements are historically true at their dates and neither should be rewritten. A reconstruction must cite both, in order.
2. **Adjudication wording in the verifier file.** `round-20-verifier-spotcheck.md:17` says `ADMITTED after post-review fixes 9639ec7`. This is an integrator decision, not a lane gate decision. Quote it as the integrator's adjudication.
3. **Quantities checked against base.** "Seven new QUALITY.md criteria" matches the seven `(r20 resume)` rows in base `QUALITY.md`. "Four knowledge entries open with source/verified-at/recheck" matches base: exactly four of 21 knowledge `.md` files have the trio in the first 8 lines (the four named above). Both are consistent.
4. **Superseded number not to be quoted.** `round-20.md:161-163` reports "drift 7 → 0". The post-review result at `:289-293` is 22/26 cleared, with 4 unannotated locations and 3 drift targets remaining, and `missSet` 55 → 55. Any reconstruction must use the post-review figure.
5. **Heading decision for main.** The C2 instruction says leave an exact-heading lesson unchanged. Round-20 has an exact `## Gate` at `:41`, so under the spec it is left unchanged. The `:194` staleness is recorded here. Whether to add a pure-append pointer to the verifier file is a decision for main, not for this seat.

---

## 3. Independent verdicts on record (carry verbatim; do not reset)

"Non-author" below means the artifact's own header names a different lane from the lesson's author (kake). Nothing here re-executes a check.

| Artifact (base) | Scope | Verdict as recorded | Covers | Does not cover |
|---|---|---|---|---|
| `round-1-aggregator-audit.md` | round-1 corpus; aggregator L1 `m_qwen` + reviewer `m_composer`; 2026-09-28 | **NOT conformant** — 3 defects: registry 20→21 rows; "~40 clones" vs observed 50; `probe.mjs` "pruned" mechanism claim | 14 kimi rows, CNAME, render service, `ufofsdbeta` is runtime, commit exists | round-1 "Open" items (PQ-2 stale, plazir404s) |
| `round-4-aggregator-audit.md` | at `6b1cd07`; 16 citations re-executed | **NOT CONFORMANT** — 1 major (README "20 rows"), fixed in `18537e9`; minors: lucario row in `fire-journal-codes.md`, 3 malformed journals, round-4 commit cited by subject | exit-code table {1..8,64}; 21-row census; observed-outcome table (efc1830 success; plazir15 code 6; ds4cc code 7) | any round-4 claim beyond those tables |
| `round-5-aggregator-audit.md` | at `18537e9`; reviewer L2, 26 citations | **NOT conformant** — 1 major (keeper timer claimed running; `disabled`/`inactive`/no journal entries); 3 minors (flip window, xsnapshot "every run", `total−ok` formula) | probe timer enabled+active; 50 repos; credential sweep clean; append-only PASS | round-5 speedrun and CLI-surface claims |
| `round-6-aggregator-audit.md` | at `dd4eabf` (= round-10 commit); read-only | **not conformant** — CORPUS R4 (`ops-automation.md:25`, formula false on 11/76 rows) and R1 (`/tmp` sources); 5 majors, incl. future-dated labels `round-8.md:4` (~21:15Z) and `round-7.md:4` (~20:20Z) | round-10 rows 42–53 re-executed (6 events/0 phantom, exits 0/2/64, 76 rows, zip and maxBuffer anchors); 50 clones; 13 PQ rows | 2,352-path baseline (`cannot-verify`, live HTTP prohibited) |
| `round-8-aggregator-box3-coldrun.md` | non-author `labrat` Box3Kake; 15 free-read commands at `2a5502c` | box-3 **[x]** for `SKILL.md` cold executability | SKILL.md cites and exit contracts; `status --json` exit 0; `grokbots --check` exit 1; `sync-check` exit 1; sentinel sha `93ddca9a` | any `round-8.md` kimi-subpath claim; the round-9 verdict says box-3 decisive claims remain **provisional** |
| `round-9-aggregator-corpus-verdict.md` | corpus at `a209441`; rule-10 review | **not conformant — rules 1, 3, 4, 5, 6, 8, 9**; rule 8 = FAIL-literal / PASS-intent (`op://` in `round-5-aggregator-audit.md:54`, `round-6-aggregator-audit.md:56`) | corpus-wide rule review; read-only keeper-timer recheck consistent with `keeper-timer-inert.md` | claim-level check of `round-9.md`; the round-9 review file is in the main repo and was not read here |
| `round-20-verifier-spotcheck.md` | `9639ec7`; verifier `W3ReviewKake` (per file) | admit `crawl-scope-per-host` = **agree**; reject S017, S018 = **agree**; 3/3 sampled | one admit and two rejects | the other three round-20 knowledge entries and the QUALITY criteria |
| `round-19-recensus.md:42-44` (erratum) | "Independent audit", appended 2026-10-14 | gates re-ran green: 13/13, offline partial exit 0, explicit-bad exit 2, no HOME residue; **coverage finding**: write-region opens on the header BEGIN token; scratch mutant, not patched | gate behaviour and selftest count | **auditor is not named** in the lesson; identity not verified here. The dead-path sweep at `:50-60` is lane-granular (not independent) |
| `round-20.md:58-60` (original Gate) | 2026-10-15 | outside spot-check `unavailable` | — | — |

Verdict-to-lesson map: round-1 → round-1-aggregator-audit; round-4 → round-4-aggregator-audit; round-5 → round-5-aggregator-audit; round-6 → round-6-aggregator-audit; round-7 → none (round-6 audit defect 3(b) only); round-8 → none for `round-8.md` (box-3 file is a different artifact); round-9 → round-9-aggregator-corpus-verdict (corpus-level); round-10 → round-6-aggregator-audit rows 42–53 (partial); round-12 → partial corroboration only (see §4); round-19 → "Independent audit" erratum; round-20 → verifier file (post-landing) plus original `unavailable`.

---

## 4. Per-lesson reconstruction inputs (14 lessons)

Vocabulary used in every entry below:
- **admitted with qualification** — a recorded non-author re-execution passed, and the qualifier is stated.
- **unverified** — no non-author check is recorded. This is the default; do not upgrade it.
- **superseded** — a later recorded artifact (lane or non-author) replaces the claim. Cite the artifact and keep the original text.
- **contradicted** — a recorded non-author check or later correction falsifies the claim. Say so, keep the original text.
- **rejected** — only when the lesson itself, or a cited artifact, records the rejection. Otherwise write `rejected: not recorded`.

"Documented in-lesson refutation" below means the lesson itself says a premise was wrong. It is not a gate rejection and must be labelled that way.

Date note: round-12, round-16 and round-17 state no date in the lesson body. Write `date: not stated in lesson`. Do not invent `verified-at` dates for them.

### round-1 (base 37 lines; 2026-09-28)
- Registry as ground truth; every claim cites a file (`:8-10`) → **admitted with qualification**. The 14 kimi rows reproduced. The count 20 is wrong: 21, per round-1-aggregator-audit defect 1, fixed in round-4 per the round-4 audit's "prior-audit defects" list.
- `sourceDir` null = republish hazard (`:11-13`) → **unverified**.
- Publish gate: click is human (`:14-16`) → **unverified** in this lesson. Corroborated only by the kimi-surface header quoted in round-1-aggregator-audit.
- "~40 site clones" (`:20`) → **contradicted**: observed 50 (round-1-aggregator-audit defect 2; round-6 audit re-executed 50). `round-1.md:20` is **still ~40 at base**; no correction is recorded. Do not write it as verified.
- `ufofsdbeta` is runtime (`:23-25`) → **admitted with qualification** (round-1 aggregator row).
- Byte equality is the wrong kimi drift primitive (`:26-28`) → **unverified**; later round-9.md:35-39 says the sdk-seed tag makes byte deltas carry no freshness signal, which is a superseding observation.
- Documented in-lesson refutations: name-matching site repos (`:23-25`), `ls ~/Projects` undercounting (`:20-22`), byte-equality instinct (`:26-28`).
- Rejected (gate): not recorded.
- Outside spot-check: **round-1-aggregator-audit.md — NOT conformant** (aggregator, non-author). Carry verbatim. Its defect 2 is not recorded as fixed.

### round-3 (base 29 lines; 2026-09-28)
- `status:live` in config is an assertion (`:20-22`) → **unverified** as a rule; corroborated by a non-author observation that `lucario.kimi.page` returns 404 and the GHP canonical returns 200 (round-8-aggregator-box3-coldrun commands 10–11, 2026-09-28T23:31–23:36Z). This is corroboration, not a spot-check of round-3.
- Marker pins on rolling content decay (`:23-26`) → **superseded in part**: round-7.md:29-34 (second consecutive charter-ghp failure) and round-9.md:47-50 (pin lag). Corroborated by box-3 command 15 (live literal `2026-09-28 scribe beat (`). The `2026-09-26` pin death is dated.
- Self-audit via the playbook's own commands (`:27-29`) → **unverified** (lane-internal).
- Rejected (gate): not recorded.
- Outside spot-check: **not recorded**. No corpus artifact re-executes round-3's claims.

### round-4 (base 42 lines; 2026-09-28)
- Exit-code table complete (codes 1–8, 64) (`:21-22`) → **admitted with qualification**, round-4-aggregator-audit "What reproduced". Qualifier: the `kimi-surface.mjs` source path is absent since 2026-10-12 (r18 and r20 citation-local annotations at `:4-5`). The reproduction is a dated result at `6b1cd07`.
- Meter consumption is a journal fact (`:34-35`) → **admitted with qualification** for the three journal anomalies in the observed-outcome table only.
- Post-fire codes 6/7 are anomaly class; success looks like failure on the live URL (`:36-39`) → **admitted with qualification**. Observed-outcome table reproduces `efc1830` success, plazir15 code-6, ds4cc code-7. Qualifier: state at 2026-09-28, pre-publish only.
- Rejected (gate): not recorded. Documented in-lesson premise: "exit code alone does not reveal consumption" (`:13-17`).
- Outside spot-check: **round-4-aggregator-audit.md — NOT CONFORMANT at `6b1cd07`**; major fixed at `18537e9`; minors open. Carry verbatim. Note the open minor "round-4 commit cited by subject" applies to `round-4.md:7` (`commit \`round-4\``), which is still at base.

### round-5 (base 67 lines; 2026-09-28)
- "Ops layer already running" with probe timer (6h) and keeper timer (daily) (`:12-14`, `:20-21`) → **probe half admitted with qualification** (round-5 audit: enabled+active; history growing). **Keeper half contradicted** (round-5 audit major: disabled, inactive, no journal entries). Correction recorded at round-12.md:17-23 (lesson-level). Whether `SKILL.md` / `ops-automation.md` carry the correction is **not verified** here.
- veigapunk-page left `violated[]` between 09-21T04:14 and 09-22T22:58 (`:35-36`) → **contradicted** by round-5 audit minor 2 (last violated 03:32:06; first clean 04:14:50). Corrected at round-10.md:25-30. **`round-5.md:35-36` is still uncorrected at base.**
- xsnapshot-app `errors[]` "every run" = NXDOMAIN baseline (`:39-40`) → **contradicted in part** by round-5 audit minor 3 (constancy begins 09-21T01:34:20). Corrected at round-10.md:42-45.
- Repos 50/50 mapped (`:24-28`) → **admitted with qualification**: round-6 audit re-executed the count (`origin-repos.md:3`, 50). The byte-verdicts (`:41-46`) are **unverified**.
- Speedrun pipeline absent from `publish-channels` (`:29-31`) and CLI verb surface (`:47-50`) → **unverified**.
- Rejected (gate): not recorded. Documented in-lesson premise: README "known gaps" were already answered by disk evidence (`:61-64`).
- Outside spot-check: **round-5-aggregator-audit.md — NOT conformant at `18537e9`** (1 major, 3 minors). Carry verbatim, with the correction history above.

### round-6 (base 47 lines; 2026-09-28)
- 0 true rot across 2,352 paths (`:18`) → **unverified**. Round-6 audit: `cannot-verify` (live HTTP prohibited); no baseline artifact exists in the corpus.
- 126 non-clean results all explained by git state (`:18-22`) → **unverified**. The repeated counts in round-9.md:44-46 (ds4cc +20, plazir +5, charter behind 2) are lane-internal repeats, not checks.
- `reconcile` covers one `index.html` (`:23-26`) → **unverified**; `reconcile.mjs` source is absent (r18 annotation at `:5`).
- `in-sync` masks byte drift (`:27-31`) → **unverified**.
- GHP serves dir indexes (`:32-34`) → **unverified**.
- Rejected (gate): not recorded.
- Outside spot-check: **round-6-aggregator-audit.md — not conformant at `dd4eabf`** (CORPUS R4, R1). The 2,352-path claim is `cannot-verify`. Carry verbatim. Note that round-6 audit's "/tmp not durable" defect applies to `ghp-subpath-spotcheck.md:3`, not to this file.

### round-7 (base 65 lines; 2026-09-28)
- 103 sitemap locs: 0 orphans, 0 dead, 0 listed-404 (`:16-18`) → **unverified**. Evidence is `/tmp/orphan-check.mjs` (`:4`), a session-local path. Round-6 audit defect 3(b) (label ~20:20Z vs mtime 19:35Z) is **open**; `round-7.md:4` still reads `~20:20Z` at base.
- "GHP live-only orphans are impossible by construction" (`:20-25`) → **contradicted** by the lane's own round-20 correction block (`:57-65`, base) citing S001/S004: a checkout walk does not establish live→source; the deployed artifact must be checked. This is a lane correction, not an independent verdict. Do not restate the original claim as current.
- `/` is `index.html`, classifier candidates (`:26-28`) → **unverified** (mechanical).
- charter-ghp second consecutive failure (`:29-34`) → **admitted with qualification** for the 2026-09-28 date (box-3 command 15 literal). The pin itself is dated.
- Staged-but-unpushed lookahead (`:47-49`) → **unverified**.
- Standing fleet state "re-verified" (`:50-53`) → **superseded**: round-9 and round-12 record later state changes. Dated, lane-internal.
- Rejected (gate): not recorded. Documented in-lesson refutation: "scary residual" premise, later itself contradicted by round-20 correction.
- Outside spot-check: **not recorded** for the orphan conclusion. The only aggregator item is round-6 audit defect 3(b), a label defect, not a verdict on the conclusion.

### round-8 (base 58 lines; 2026-09-28)
- ds4cc.kimi.page missing 74 of 93 canonical paths; every miss post-dates vintage (`:19-25`) → **superseded** in count: round-9.md:40-43 says 75 in-repo (commit `f3d2ecd`). The evidence is `/tmp/kimi_audit.py` (`:4`, session-local). Round-6 audit defect 3(a) (`~21:15Z` label vs `19:46Z` mtime) is **open**; `round-8.md:4` still reads `~21:15Z` at base.
- `dir/` hrefs dead on kimi (`:26-30`) → **unverified**.
- Other 9 kimi rows clean (`:31-34`) → **unverified**.
- Vault and veigapunk-page hide links client-side; DOM rot invisible without execution (`:35-40`) → **contradicted** by round-9.md:13-15 (the link surface is a static literal in the served body; the premise was false).
- Update vs recreate payloads (`:49-55`) → **unverified**; the source is absent.
- Rejected (gate): not recorded. Documented in-lesson correction: round-9.md:13-15.
- Outside spot-check: **not recorded** for round-8.md. `round-8-aggregator-box3-coldrun.md` is a different artifact (SKILL.md cold run). Its box-3 `[x]` is provisional per round-9 verdict. Do not cite the box-3 file as a spot-check of round-8.md.

### round-9 (base 66 lines; 2026-09-28)
- PQ-5 shortest path to green; rebuild `efc1830` verified card, `stillDead:true` (`:19-22`) → **admitted with qualification**: round-4 observed-outcome table reproduces `efc1830` success. The current preview facts are **unverified**.
- PQ-1 vault rot: 3 of 10 dead links (`:23-28`) → **unverified** (live state; not re-checked by this seat).
- `sourceDir:null` is the hard blocker; refusals at `kimi-surface.mjs:483` and `:845-849` (`:29-34`) → **unverified**; the source is absent.
- Platform shift: `sdk-seed.js` +157B; website-id on both kimi hosts (`:35-39`) → **unverified**.
- 6h cadence is the timer's (`:40-41`) and 74→75 correction (`:41-43`) → 75 **admitted with qualification** by the lane's own correction; not independently checked.
- 25 unpushed source commits (`:44-46`) → **unverified** repeat.
- Live-404 sentinels uniform, 13,409 B, sha `93ddca9a…` (`:61-63`) → **admitted with qualification**: box-3 command 11 observed the same bytes and sha for `lucario.kimi.page` (non-author, 2026-09-28).
- Cross-lane sweep found no contradictions (`:64-66`) → **unverified**.
- Rejected (gate): not recorded. Documented in-lesson refutation: "JS-rendered link surfaces need rendered DOM" (`:13-15`).
- Outside spot-check: **round-9-aggregator-corpus-verdict.md** — corpus-level rule-10 NOT conformant at `a209441` (rules 1, 3, 4, 5, 6, 8, 9). This is not a claim-level check of round-9.md. Carry verbatim.

### round-10 (base 62 lines; 2026-09-28)
- Naive diff unusable: 42 events, 40 phantom (`:19-20`) → **admitted with qualification** for 42 (round-6 audit row 43). The 40-phantom split is **[INFERENCE]** in the round-6 audit, not re-derived.
- Final run 6 events, 0 phantom; four r5 truths reproduced (`:21-24`) → **admitted with qualification** (round-6 audit row 42; state at 2026-09-28, dd4eabf).
- r5 veigapunk-page record was wrong (`:25-30`) → **admitted with qualification**: round-6 audit row 53 confirms the correction landed at `dd4eabf`; round-5 audit minor 2 agrees.
- Checklist executability: 33/33 SKILL commands and 60/60 paths (`:31-33`) → **unverified** in the count; `webzites status` exit-1 at `src/cli.mjs:99` is **admitted with qualification** (round-6 audit row 50).
- Citation drift fixed: zip-exclude `:903`, maxBuffer `:342` (`:37-41`) → **admitted with qualification** (round-6 audit rows 48–49).
- xsnapshot "every run" loose (`:42-45`) → **corrected in-lesson**, corroborated by round-5 audit minor 3.
- `total ≠ ok+|violated|+|errors|` on 11 rows (`:53-55`) → **acknowledged, uncorrected**: round-6 audit defect 4 still open at `ops-automation.md:25`.
- Cross-lane CDP-9222 lease unresolved (`:60-62`) → **unverified**; round-6 audit routed row remains open.
- Rejected (gate): not recorded. Documented in-lesson rejection: naive history diffing (`:19-20`, `:49-52`).
- Outside spot-check: **round-6-aggregator-audit.md rows 42–53** (non-author, dd4eabf = round-10 commit). Partial: covers the detector and selected anchors, not the whole lesson. The round-6 audit's own verdict (not conformant, R4/R1) applies to the corpus at dd4eabf.

### round-12 (base 62 lines; date not stated in lesson)
- Last four free-read verbs live-proven write-free (`:8-16`) → **admitted with qualification** for the exit predicates only (box-3 commands 4, 5, 6 reproduce `status --json` exit 0, `grokbots --check` exit 1, `bots list` exit 0). The write-free proof (31-file sha guard) is **unverified**; evidence is `/tmp/kake-r12/` (`:60`), session-local.
- Myth 1 fell: keeper timer disabled and inactive, never fired (`:17-23`) → **admitted with qualification** for 2026-09-28/29. Corroborated by round-5 audit (disabled/inactive/no entries), box-3 `SKILL`-cited observation (`:70-73`), and the round-9 verdict read-only recheck (consistent).
- Myth 2 fell: charter-ghp re-pin is operator config, not keeper work (`:25-32`) → **superseded**: round-9.md:50 says "keeper owns the edit" and round-9.md:58-60 says the re-pin is handed to the keeper. Round-12 reassigns ownership. "No webzites code writes `fleet.config.json`" (`:27`) is **unverified** (source absent).
- Roster arithmetic 21 / 20 / 18 (`:34-38`) → **admitted with qualification**: box-3 commands 2, 3, 6 (rows 21; 18 result rows; 20 keepers).
- The r11 F1 guard is wrong; the corrected patch is replica-verified (`:40-46`) → **unverified** by a non-author; artifact is `corpus/handoffs/cmdProbe-merge-fix.md`.
- Rejected (gate): not recorded. Documented in-lesson refutations: Myth 1, Myth 2, F1 proposal.
- Outside spot-check: **partial** only: box-3 commands 2–6 and round-9 verdict read-only timer recheck. No verdict on the write-free proof or the F1 replica.

### round-16 (base 75 lines; date not stated in lesson)
- 160 claims: 117 HOLDS / 15 STALE / 7 UNVERIFIABLE / 21 HISTORICAL-OK (`:9-19`) → **unverified as a standing tally**. It is a dated run, as the lesson's own rule (`:47-49`) requires. Do not cite it without its run timestamp; none is recorded in the body.
- verb-outcome literals stale (`:24-27`) → **dated**: box-3 command 14 gives a different `sync-check` tally on 2026-09-28. The timestamps differ; do not read them as contradiction without the run times.
- Journal structure keys (`:29-31`) → **corrected in-lesson**: the claim was wrong when written. Verification in base is absent.
- Fire counts: recreate plazir15 ×2 undercount (`:31-34`) → **unverified**; journal source absent.
- ETag literal (`:35-38`) → **superseded in principle**: round-20.md:257-260 (A1 "validator is not identity") is a lane correction. Not a non-author check.
- plazir15-ghp 5 ahead (`:56-64`) → **unverified** repeat.
- `freshness-sweep` selftest 9/9 (`:68-73`) → **superseded**: 10/10 (round-17.md:47), 13/13 (round-19-recensus.md:22), 15/15 (round-20.md:169).
- Rejected (gate): not recorded.
- Outside spot-check: **not recorded**.

### round-17 (base 56 lines; date not stated in lesson)
- W6 explains the new `§paths` drift (`:8-23`) → **unverified mechanism**. Absence of `~/projects` and `~/DIRMAP.md` is annotated historical at `:14`, `:16`, `:23`, `:25`. Do not restate the event as present-tense.
- `pathsFiles` pinned as count, inert by type (`:30-34`) → **unverified**; the fact is a fix recorded in-lesson.
- `loadPins` degraded silently; now exit 2 (`:35-38`) → **unverified**; selftest 10/10 at `:47` (lane run).
- Classification header fix (`:39-41`) → **unverified**.
- Rule: a pin whose type does not match is silently inert (`:52-56`) → rule, unverified.
- Rejected (gate): not recorded.
- Outside spot-check: **not recorded**.

### round-18 (base 64 lines; 2026-10-14)
- W7 prune: 33 of 36 pinned children removed, 11 added (`:11-19`) → **absence annotated historical** (`:16`). The removal facts are lane observations, **unverified** by a non-author.
- `§paths` 36 unannotated + 45 beyond miss set (`:23-24`) → **unverified** (lane run output, dated).
- PQ-12 armed watch fired; live marker `2026-09-30` (`:25-28`) → **unverified**; source absent.
- Selftest regressed 10 → 8 (`:32-35`) → fixture defect recorded in-lesson; **superseded** by later selftests (round-19: 13/13).
- 63 cite lines across 22 files annotated (`:39-43`) → **unverified** count.
- Pins re-measured, `pathsMissSet` 10 → 55 (`:44-47`) → **admitted with qualification** for continuity: round-20.md:293 and the verifier file report `missSet 55 → 55`.
- Final state "selftest 10/10" (`:63-64`) → **superseded**: round-19 13/13; round-20 15/15.
- Rejected (gate): not recorded.
- Outside spot-check: **not recorded**.

### round-19-recensus (base 60 lines; 2026-10-14)
- §history suspends only the canonical default; explicit bad override fails closed (`:9-17`, `:28`) → **admitted with qualification**: the independent audit erratum (`:44`) reports `explicit-bad exit 2` and offline partial exit 0.
- Selftest 13/13; region marks; "0 write sites outside the region" (`:22-24`) → selftest count **admitted with qualification** (`:44`). The "0 write sites outside the region" confinement claim is **contradicted** for the header-BEGIN case by the audit's scratch mutant (`:44`). Carried as M4 at round-20.md:252; C2 closes the reported class, and residual bypasses are named at round-20.md:172-174.
- Dead-path sweep: 77 live citations vs 8 fleet-level (`:50-60`) → **lane-granular, not independent**. Population dispute carried as M5 (round-20.md:253), named debt, owner kake.
- `SCORECARD.md:22` "every origin-work cite is marked" (`:55-58`) → **contradicted** in the same lesson (`keeper-timer-inert.md:91`, `publish-queue.md:167` unmarked).
- Documented in-lesson refutation: "describe-don't-pin" (`:47-48`).
- Rejected (gate): not recorded.
- Outside spot-check: **"Independent audit" erratum (`:42-44`)**. Auditor not named in the lesson; identity not verified in this read. Treat as independent per its own wording, not as a named non-author seat.

---

## 5. Honest reconstruction wording (template for the 14)

Use exact `## Gate` as the heading. Put the label in the body. Append after base EOF only.

```
## Gate

Retrospective round-21 reconstruction, not original admission. The original round recorded no Gate section (base <sha>). Written 2026-10-20 from this lesson's sections and the artifacts named below. No live-state re-verification. No new independent review.

Candidates (lesson claims, base line):
- <claim> (:N) — historical outcome: <admitted with qualification: <qualifier> | unverified | superseded by <path:line> | contradicted by <path:line>>. Evidence: <path:line>.

Rejected: <in-lesson refutations with line refs, labelled "in-lesson"> | rejected: not recorded.

Outside spot-check: <verdict as recorded, artifact path, lane, commit, scope> | not recorded.

Cites: this lesson (base sections); corpus/lessons/round-21.md; S019 (metadata/gate contract — see §6).
```

Forbidden wording in any appended block (for this lesson set):
- `admitted` without a qualifier.
- `Outside spot-check: agree` or `independently verified` for any lesson in §4 except where §3 records it.
- `verified-at:` or `recheck:` as a metadata line in a lesson body (C1 scope is knowledge entries only).
- `re-verified`, `live`, `currently`, `now` as present-tense state.
- Any `verified` on a claim marked `unverified` above.
- Any rewritten base line (the appended block is the only change).

---

## 6. Gaps, blockers, and checks for main (not run here)

Blockers / unknowns:
- **S019 is not at base.** `corpus/SOURCES.md` at base has zero `S019` rows. A working-tree row exists (added by a sibling seat). Do not cite S019 in appended text until the row lands and is verified.
- **Round-19 erratum auditor is unnamed.** Identity not verified here.
- **Session-local evidence.** Pointers to `/tmp/kake-r10/`, `/tmp/kake-r12/`, `/tmp/kake-r16/`, `/tmp/kake-r17/`, `/tmp/kake-r18/`, `/tmp/orphan-check.mjs`, `/tmp/kimi_audit.py`, `/tmp/kimi-subpath-audit.json`, `/tmp/vault.html` do not resolve from a fresh checkout. Reconstruction must call them session-local, not evidence.
- **Round-6 2,352-path baseline has no artifact.** Mark it `cannot-verify`.
- **Dates.** Round-12, 16, 17 have no body date. Do not invent.

Checks main should run once after integration (listed, not run):
1. `grep -c '^## Gate$' corpus/lessons/round-{1,3,4,5,6,7,8,9,10,12,16,17,18,19-recensus,20}.md` → each file exactly 1. The aggregator and verifier files must not gain a Gate.
2. Byte-prefix check: for each of the 14, `git show 5009eca:<path>` must equal the first N bytes of the current file (N = base size from §1 sizes). Only appended text may follow.
3. Confirm `round-4.md:44` heading is exact `## Gate` (it was em-dash at last scan).
4. Confirm `round-20.md` unchanged in bytes at `:41-60` and `:182-196`.
5. Confirm no appended block contains a forbidden phrase in §5.
6. Confirm the verdict strings in §3 appear verbatim (e.g. `NOT conformant`, `NOT CONFORMANT`, `agree`) only in blocks that cite the artifact.

Scope notes:
- Not checked: any live URL, any fleet state, any `webzites` tree (absent), any `.ufo/waves/*` artifact outside this wave, any credential or auth file.
- No edits, no commits, no subagent dispatch (leaf member).
