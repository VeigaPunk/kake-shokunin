# Round 99 — C1 tool-registry calibration (unmet) and C2 304 freshening (met)

Round base `cde408e5817bf1376c701d8decc5469fa82b2985`; instruments `2345e309640adac6c36e41eca87409085ba3a276`;
freeze `ab35eacebf922f4f598237590f0220d63111dc94`; C1 repair `9d341d1b46f16dbfbb41af75dd6d4966808dfa5d`;
C2 content `998b6d5f6dd453d910b15c0bdf9e5ac124c84497`. One v1 wave of 13 seats (`.ufo/waves/round-99/w1/`).
The outside closure owns admission. Gate and mistakes 1-4 and criterion R99-A were drafted by the
ScribeLesson seat and integrated by the L1; mistake 5, R99-B and the verdicts are the L1's.

## Verdicts recorded by the L1

- **C1 calibration — unmet** under the frozen kill rule. Counter: `unlisted=26 … met=false` exit 1 at
  base (`controls/base-c1.txt`) → `unlisted=0 dangling=0 mismatches=0 met=true` exit 0 at `9d341d1b`
  (`controls/after-c1.txt`); review conjunct: ReviewRegA 24 agree / 2 disagree, ReviewRegB 23 agree /
  3 disagree (rows `quote_class.py`, `wave_seat_record.py`, `sitemap_audit_selftest.py`). Live
  `disagree` → unmet. Calibration stays 3. The three rows were corrected afterwards; the verdict does
  not flip.
- **C2 freshness capability — met** on the frozen predicate: `candidate=absent` exit 1 at base
  (`controls/base-c2.txt`) → `candidate=present sha256=db3a0f12… hand=50/50 generated=240/240
  refusals=47/47 met=true` exit 0 at `998b6d5f` (`controls/after-c2.txt`), scored sha256 = landed blob;
  10 extra seeds 10/10 met (`controls/after-c2-10seeds.txt`). Caveats: contract findings F1/F2/F10 and
  the LC6 case question (`w1/ReviewFresh/contract-findings.md`, `w1/ExecTwinFresh/disagreements.md`);
  the counter's candidate runner is not isolated (SentinelScope W1-W4) — the landed candidate imports
  only json/re/sys and opens nothing (`controls/c2-candidate-static.txt`).

## Gate

> Row bodies and fetch receipts: the scout seat's in-round GETs, integrated by the L1 into
> `corpus/SOURCES.md` rows S484/S485 at the C2 content commit `998b6d5f`. The retained bodies are already committed at
> `.ufo/waves/round-99/sources/rfc9111.txt` (sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`,
> 84 477 bytes) and `.ufo/waves/round-99/sources/eid9185.html` (sha256
> `83c3b795290e09842d1af973f73b52c98fd661bf77cafc17658eb5ac4df63dd3`, 10 655 bytes) — the digests
> were re-derived by this seat with `sha256sum` and match the freeze's stated RFC digest
> `aeb52adb…`. **The scout seat has since landed its own fetch receipts and its six located quotes**
> (`w1/ScoutRfc9111/report.md` §2–§3, `w1/ScoutRfc9111/rows.md`): RFC GET 2026-11-05T23:16:07Z,
> HTTP 200, 84 477 bytes, sha256 `aeb52adb…`, **byte-identical to the retained body**
> (`RFC_MATCHES_RETAINED=yes`); errata GET 2026-11-05T23:16:07Z → 302 → 301 → HTTP 200 at
> `https://errata.rfc-editor.org/eid9185/`, 10 655 bytes, sha256 `83c3b795…`, also byte-identical to
> the retained body; `quotes = 6/6 located and verified`; `errata-touching = 1` (EID 9185 only). This
> seat re-derived the digests independently and quotes the scout's receipts **as the scout's
> first-party evidence**, not as its own — this seat performed **no live GET**.

### Row S484 (RFC 9111, §3.1 / §3.2 / §4.3.4) — **admitted**

- **Source / URL:** RFC 9111, *HTTP Caching*, June 2022 —
  `https://www.rfc-editor.org/rfc/rfc9111.txt`
- **Kind / tier:** spec / A
- **Scope:** which stored responses a 304 freshens (RFC 9111 §4.3.4 first-match selection: strong →
  weak → no-validator) and which header fields their update adds, replaces or withholds (§3.2 with
  §3.1's storage exceptions). It is the §4.3.4 *initial set* the caller supplies; it does not
  compute that set (§4 reuse conditions, keys, Vary), does not decide freshness lifetime, storage,
  cache keys, serving stale, trailer fields, HEAD freshening (§4.3.5), invalidation (§4.4), and
  says nothing about any deployed cache.
- **Retained body:** `.ufo/waves/round-99/sources/rfc9111.txt`, sha256 `aeb52adb…`, 84 477 bytes
  (1 956 lines). Section anchors, re-derived by this seat with `grep -n` and matching the scout's
  §3 boundaries: §3.1 heading line 338 (section 338–366); §3.2 heading line 369 (section 369–414);
  §4.3.4 heading line 951 (section 951–988).
- **Located quotes (≤25 words each) — the scout's §3 quotes, verified by the entry's quote check (`w1/ScribeEntry/quotecheck-summary.txt`: 26 RFC + 9 erratum quotes found, 0 line mismatches):**
  1. §3.2 add/replace sentence, lines 375-377: «the cache MUST add each header field in the
     provided response to the stored response, replacing field values that are already present»
     (22 words).
  2. §3.2 Content-Length exception (bullet 4), line 387: «The Content-Length header field.».
  3. §4.3.4 strong-validator MUST NOT (bullet 1), lines 971-972: «the cache MUST NOT use the new
     response to update any stored responses» (13 words).
  4. §4.3.4 weak "most recent" sentence (bullet 2), lines 976-977: «then the most recent of those
     matching stored responses is identified for update» (13 words).
  5. §4.3.4 no-validator sentence (bullet 3), lines 979-984: «If the new response does not include
     any form of validator … then that stored response is identified for update» (19 words,
     parenthetical elided).
  6. §3.1 proxy-specific field (bullet 4), lines 361-363: «Effectively, this is limited to
     Proxy-Authenticate …, Proxy-Authentication-Info …, and Proxy-Authorization …» (21 words).
- **Status / opened / recheck:** `mined` / 2026-11-05 / 365d.
- **used-by:** `corpus/knowledge/freshening-304.md` (landed at `998b6d5f`).

### Row S485 (RFC Editor erratum EID 9185, on RFC 9111 §4.3.4) — **admitted**

- **Source / URL:** RFC Editor erratum EID 9185 —
  `https://www.rfc-editor.org/errata/eid9185` (302 → `https://errata.rfc-editor.org/eid9185` →
  301 → `https://errata.rfc-editor.org/eid9185/`, HTTP 200)
- **Kind / tier:** dataset / A
- **Scope:** the errata status of the RFC 9111 §4.3.4 *initial-set* paragraph, as of the fetch — a
  **Reported** (not Verified) erratum that proposes to replace that paragraph with a criteria list
  and to append a strong-ETag-match rule. Its scope is the status of the erratum, **not** the
  semantics of a deployed cache, and it does not change this round's contract (the contract does not
  compute the initial set).
- **Retained body:** `.ufo/waves/round-99/sources/eid9185.html`, sha256 `83c3b795…`, 10 655 bytes.
  The scout's fetch was byte-identical to it. Fields the scout read: `Errata-ID: 9185`;
  `Status: Reported`; `Type: Technical`; reported by Daniel Fox Franke; `Date Reported: 2026-09-24`.
- **Located quote (≤25 words):** the erratum's status line — «Status: Reported».
- **Errata census (the scout's, and only one erratum touches the contract's sections):** EID 9004
  (Reported, §3.5), **EID 9185 (Reported, §4.3.4 — the one that touches)**, EID 9166 (Held for
  Document Update, §5.2.3), EID 7695 (Rejected, §4.3.2). No erratum touches §3.1 or §3.2.
- **Status / opened / recheck:** `mined` / 2026-11-05 / 90d (errata status moves; recheck with the
  next errata sweep).
- **used-by:** `corpus/knowledge/freshening-304.md`.

### Reject — merge/kake package adoption

- **Rejected.** The `merge/kake` staging package is **not adopted** this round.
- **Evidence:** `.ufo/waves/round-99/assimilation/collisions` — 8 id collisions, re-derived by this
  seat with `grep -c .` (8 non-empty lines) and by reading the file: `S312 S329 S367 S372 S373 S374
  S390 S409`. The wave-time populations are `.ufo/waves/round-99/assimilation/reg-ids` (220 non-empty
  ids) and `staged-ids` (129 non-empty ids) — both counts re-derived by this seat; the delta against
  round 98's own receipt (218 ids, `.ufo/waves/round-98/assimilation/reg-ids`) is the two rows that
  landed in round 98 (`S482`, `S483`), which round 98's wave-time receipt predates.
- **Reason:** no renumber map exists and no entry is re-grounded, so an append would collide ids with
  divergent scope cells (CORPUS.md rule 1: a row is written only after the source is opened and
  re-grounded). `S312` exists on both sides with different scope text.
- **Flip:** a round that builds the renumber map in scratch and re-grounds each adopted entry against
  its own retained source.

---

## Mistakes

> Table shape follows `corpus/lessons/round-97.md` § Mistakes (`# | Class | Evidence | Captured-by |
> Fix`). Every **Evidence** cell is a `path:line` pointer to committed bytes; every **Fix** cell
> names how the fix was shown able to fail, or says plainly that it was not.

| # | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| 1 | **Registry drift (calibration).** 26 of the 54 committed tools directly under `scripts/` had **no conformant row in any registry table of `SKILL.md`** at the round-99 base — the lane's own self-assessment of what it owns was 26 tools short of the tools it actually owns. The drift accumulated over rounds, not in one round: the unlisted tools landed in rounds 27, 29, 31, 34, 36, 37, 39, 44, 56, 61, 63, 74, 81, 83, 89, 90, 93, 96 and 98 (per-tool landing commits re-derived with `git log --diff-filter=A -- scripts/<tool>`). The near-misses are the sharp part: a round that landed a *tool* usually registered that round's **counters** and left the tool itself unregistered. The round-96 landing commit `7dc9bf43` added two `SKILL.md` rows (`c96_selfassess.py` and `c96_reval.py`) in the same commit that added `scripts/reval_exchange.py` — and the tool got no row; the round-89 landing commit `9784ad54` (`scripts/cache_key.py`), the round-90 landing commit `7f6c68f1` (`scripts/cache_key_conformance.py`), the round-93 landing commit `5272c727` (`scripts/conditional_eval.py`) and the round-98 landing commit `0f48ada0` (`scripts/stale_extensions.py` **and** `scripts/knowledge_metatext_lint.py`) each added **no** `SKILL.md` row for the tool they carried (re-derived with `git show <commit> -- SKILL.md` and `grep '^+|'`). **The counter's "unlisted" is not one class.** Re-deriving each of the 26 against the frozen counter's own R1–R5 rules (this seat's `diagnose_unlisted.py`, which imports `c99_registry.py` and reuses its `tables`/`cells`/`SPAN`/`names_path`/`verdict_ok` helpers so the diagnosis cannot drift from the instrument) shows four distinct sub-classes: **(a) 11 tools no row mentions at all** — `citing_set_hostile_selftest.py`, `conditional_eval.py`, `header_change_class.py`, `knowledge_metatext_lint.py`, `landed_check.py`, `ledger_latest_check.py`, `probe-delta.mjs`, `reval_exchange.py`, `sidecar_reobserve.py`, `source_recheck_hardening_selftest.py`, `wave_seat_record.py`; **(b) 13 tools have a near-miss row that fails exactly one rule** — 7 on **R2** (the entry cell names the tool by a *different* label, not as a path token: `scripts/base_path_selftest.py` under the name `base-path-audit` at `SKILL.md:737`, `scripts/citing_set.py` under `citing-set` at `:628`, `scripts/link_preview_selftest.py` under `link-preview-audit` at `:1057`, `scripts/robots_audit_selftest.py` under `robots-expectation-audit` at `:1104`, `scripts/sitemap_audit_selftest.py` under `sitemap-file-audit` at `:1139`, `scripts/source_recheck_selftest.py` under `source-recheck-audit` at `:1078`, `scripts/stale_extensions.py` under `c98_stale.py` at `:224`), 3 on **R3** (the verdict map does not map both 0 and 1: `scripts/live_snapshot.py` at `:494`, `scripts/response_snapshot.py` at `:1370`, `scripts/source_snapshot.py` at `:1079`), 2 on **R5** (`scripts/cache_key_conformance.py` at `:1624`, whose self-test cell has no backtick span at all), and `scripts/cache_key.py`, whose two candidate rows (`:1621`, `:1623`) both point their self-test at `c89_key.py --selftest` — a counter, not a population tool with `selftest` in its name; **(c) 3 tools fail R3 and R5 together** (`scripts/live_snapshot.py`, `scripts/response_snapshot.py`, `scripts/source_snapshot.py` — their self-test spans name a counter or a *data* file, e.g. `.ufo/waves/round-61/capture/charter-ghp/response.json`); **(d) 1 tool is the only execution failure — `scripts/robots_audit.py`**, whose row at `SKILL.md:1104` passes R1–R4 but whose self-test span `python3 -B scripts/robots_audit_selftest.py [--tool PATH]` does not execute: `shlex.split` yields the literal argv `['python3','-B','scripts/robots_audit_selftest.py','[--tool','PATH]']` — the bracketed placeholder is **not** the counter's `<placeholder>` form, so it reaches the tool as a real argument and the tool exits **rc=2**. This seat reproduced that in a scratch extraction of the base tree: the bracketed form exits rc=2, the plain `python3 -B scripts/robots_audit_selftest.py` exits rc=0. The counter reports exactly this as `exec_fail 1104 scripts/robots_audit.py rc=2` at base **and** at the repair commit. | `.ufo/waves/round-99/controls/base-c1.txt:2` — `tools=54 rows=124 listed=28 unlisted=26 dangling=0 exec_fail=1 mismatches=26 met=false`, exit 1; the 26 named paths at `.ufo/waves/round-99/controls/base-c1.txt:3`–`:28`. The r98 closure's route line is `corpus/lessons/round-98-verifier-spotcheck.md:134` (**R98-C1**: "add a SKILL.md gate-registry row for `scripts/knowledge_metatext_lint.py`") — that route named **one** tool of the 26, and the same closure's conformance note at `corpus/lessons/round-98-verifier-spotcheck.md:28` ("**Gate without a registry row**") says the same of one tool. The same class had already been routed twice before: round 94, R94-9, `corpus/lessons/round-94-verifier-spotcheck.md:117` (three counters with no registry row) and round 91, K91-2, `corpus/lessons/round-91-verifier-spotcheck.md:189` (`c91_defects.py` has no registry row). Three routings of the same class, each naming a single tool, never a population check. | **Partly captured, and the capturing rule is the reason the drift survived.** PROTOCOL §Gate standard (fleet `PROTOCOL.md:398`, "**Registry.** … a child lane's *registry home* is its own `SKILL.md`", and `PROTOCOL.md:420`–`:421`, "closure grades no gate conformant until its registry row exists at the lane's *registry home*") requires *a gate* to be registered — but it binds **one row per gate**, never the population, so a tool is conformant the moment it has a row and nothing ever asks whether *every* tool has one. No lane criterion or instrument covered the population until this round's counter. The r98 closure's R98-C1 route (the only capture) is a **route, not a criterion**: it was satisfied by one row and the class remained open. | **Fix:** `.ufo/waves/round-99/c99_registry.py` (the frozen counter) plus the `## Round 99 — tool registry completion` section at `SKILL.md:1700` — 26 rows, 26 data rows (counted with `grep -c '^| [a-z]'` at the repair commit `9d341d1b`). **Shown able to fail, twice over.** (a) *At base* the counter is red: `controls/base-c1.txt:2` `unlisted=26 … met=false`, exit 1 — and this seat re-ran it read-only into its own scratch, `receipt-c1-base-reproduce.txt`, observing the same `tools=54 rows=124 listed=28 unlisted=26 … met=false` line and rc=1 (`controls/base-c1.txt` byte-identical to the reproduction apart from the trailing `exit=` line the reproduction prints as `rc=`). (b) *Four pre-freeze negative controls* each drive the counter red on a fixture commit: `controls/ctl-c1-namesonly.txt:3` (names-only rows → `listed=28 … met=false`, exit 1), `controls/ctl-c1-fenced.txt:3` (the real rows inside a fence → `rows=124 … met=false`, exit 1), `controls/ctl-c1-wrongowner.txt:3` (forged owner → `met=false`, exit 1), `controls/ctl-c1-falseselftest.txt:3` (a `--selftest` command the tool lacks → `exec_fail=8 … met=false`, exit 1). The positive control is green (`controls/ctl-c1-pos.txt:3` `met=true`, exit 0) and the counter's own battery is `controls/ctl-c1-selftest.txt:21` `selftest 20/20`. **Declared limit, not a defect:** a well-formed row whose prose is junk still reads `met=true` (`controls/ctl-c1-junkprose.txt:3`), which is what the frozen two-reviewer conjunct (`freeze.md:33`–`:39`) exists to catch. **Not shown able to fail:** nothing here falsifies a row's *truth* — the counter certifies structure, not semantics, and this lesson claims only the structural repair. **The four sub-classes matter for what a successor must fix:** only sub-class (a) is a genuinely missing row; (b) and (c) are *near-miss rows that a human would read as registered*, and (d) is a row whose self-test command is not runnable as written. A successor that only checks "is there a row mentioning the tool?" would call (b), (c) and (d) green. |
| 2 | **Population drift (calibration).** A lesson cites a registry-population count that does not match the receipt file it cites, and no closure re-derived it: the round-96 lesson quoted "**217 registry ids**" while the receipt it names (`w1/ExecReceipts/assimilation/reg-ids`) holds **216** non-empty ids — a one-row difference the round-96 closure itself flagged as a "count-accuracy note" and routed as a *note*, not as a defect. The same class reappears one round later: the round-98 lesson quotes "218 registry ids" citing round 98's own wave-time receipt, which is correct **for that receipt** but is one row behind the round-99 committed receipt (220 ids, the delta being `S482` and `S483`, which landed after round 98's wave-time snapshot). The number is right in one sense and stale in the other, and nothing states which. | `corpus/lessons/round-96.md:75` ("217 registry ids, 129 staged ids, 8 collisions") against `.ufo/waves/round-96/w1/ExecReceipts/assimilation/reg-ids` — 216 non-empty ids (re-derived by this seat, `red-control-A-count-accuracy.txt`); the closure's own flag at `corpus/lessons/round-96-verifier-spotcheck.md:62` ("**Assimilation count nit**") and its routing at `:185` ("**Count-accuracy note:** cite the assimilation receipt's wave-time number (216 registry ids) with the delta named, or re-derive at the tip (217)"). The round-98 instance: `corpus/lessons/round-98.md:55` ("218 registry ids vs 129 staged") against `.ufo/waves/round-99/assimilation/reg-ids` — 220 non-empty ids (re-derived by this seat). | **None.** No lane criterion, rule or instrument binds a cited count to the revision the count was measured at; CORPUS.md's index-row rule ("An index row is a claim") covers *rows*, not *counts*. The r96 closure routed it as a note in its prose (§6) with no owner and no check, so it was neither mined nor gated — and the r98 lesson repeated the shape one round later. | **Fix:** this round's lesson states the count **with its measurement basis** — "220 registry ids vs 129 staged (wave-time, `.ufo/waves/round-99/assimilation/reg-ids`; the delta against round 98's 218 is `S482`, `S483`)" — instead of a bare number. **Shown able to fail:** yes, by re-derivation. `red-control-A-count-accuracy.txt` re-derives the round-96 case from committed bytes (`grep -c .` over the named receipt = 216 against the lesson's 217) and shows the round-98 case against the round-99 receipt (218 against 220) — the mismatch is readable from the committed tree without any new instrument, which is the point: the class was never mined *because* it was never checked. **Not shown able to fail:** no instrument refuses the bad citation today; the discipline is documentary and this lesson does not claim otherwise. A counter that fails when a quoted count disagrees with its cited receipt is **routed, not delivered** (see Routed). |
| 3 | **Review-conjunct collapse (calibration).** The round-98 C1 review conjunct was designed for two reviewer seats and **ran on one**: `ReviewCapA` settled with an empty final output and produced no files at all, `ReviewCapB` alone judged 43 rows `agree` and 2 `disagree`, and the round recorded C1 as unmet under the frozen kill rule — but the *reason* the conjunct was thin (one seat dead) was carried as a route, and a lesson records the dead seat only as a routing line, so the failure mode was carried forward as "a seat died" rather than as "the conjunct must survive a dead seat". | `corpus/lessons/round-98.md:135` (**R98-5**: "`ReviewCapA` settled with an empty final output and no files (dead seat, `w1-results.json`); the C1 conjunct ran on `ReviewCapB` alone") and the closure's reading at `corpus/lessons/round-98-verifier-spotcheck.md:72` ("ReviewCapA: 0 files in the tree"). The round-97 lesson records the same class one round earlier at `corpus/lessons/round-97.md:101` ("**Dead seat**: ReviewReval ended without a report or verdict") — a lesson sentence, not a mistake row. | **None.** The r97 closure's route R98-D2 (`corpus/lessons/round-97-verifier-spotcheck.md:241`, "Make a dead review seat on a claim either replaced within the wave, or have the report name which surviving seat carries that claim's review"; the `D-b` defect it closes is at `:48`) asks that a dead review seat be *replaced within the wave* or that the report *name which surviving seat carries that claim's review* — a **routing requirement, not a criterion**, and one that the round-98 report did not satisfy (the report names ReviewCapB's verdicts but never states that ReviewCapA was dead). The same defect class is visible in round 97's lesson and was mined as prose, not as a mistake row. | **Fix (this round, by construction of the freeze — not by repair):** the round-99 freeze makes the conjunct **two seats by construction and states the kill rule for a dead one**: "two reviewer seats, ReviewRegA and ReviewRegB, each judge every one of the 26 rows the round-99 repair added" (`freeze.md:33`–`:34`), "Both review seats dead or verdict-less → unmet. A row missing from a live seat's file counts as no verdict from that seat" (`freeze.md:37`–`:40`). **Shown able to fail:** the predicate is written to fail closed — a missing row from a live seat is *no verdict*, not a pass — so the round-98 shape (one live seat, one dead) would now be recorded unmet rather than being scored on the survivor alone. **Not shown able to fail (this round):** **this seat did not read the reviewer verdict files and asserts no C1 verdict.** At this seat's last read the wave held `w1/ReviewRegA/verdicts.tsv` (a file exists, with per-row `agree`/`disagree` lines) and `w1/ReviewRegB/` was **empty** — i.e. the second reviewer had not yet landed, so the conjunct was, at that instant, in exactly the round-98 shape this row is about (one live seat, one not yet landed). The freeze's rule covers it: "Both review seats dead or verdict-less → unmet. A row missing from a live seat's file counts as no verdict from that seat" (`freeze.md:37`–`:40`). What this seat *has* shown is the counter half — the pre-freeze red at base and the four negative controls (row 1 above) — not the review half. |
| 4 | **Duplicate registry rows (calibration) — a class the counter cannot see, created by this round's own repair.** The repair does not supersede the near-miss rows it replaces: it **adds** 26 new rows while the older rows that mention the same tools stay where they are (the repair's own prose says so: "Older rows for some of these tools stay where they are; the rows below are the current registration and do not rewrite them"). The result is that at the repair commit **16 of the 26 repaired tools are named by two or more registry rows**, with the older row carrying a different Name cell, a different verdict map and (for `robots_audit.py`) a **self-test command that does not execute**. The registry home now answers "how do I run this tool?" with two answers, and the reader cannot tell which one the counter accepted. | Re-derived by this seat over committed bytes at the repair commit `9d341d1b` (`diagnose_unlisted.py`'s duplicate scan): `scripts/robots_audit.py` is named by **four** rows — `SKILL.md:1104` (`robots-expectation-audit`), `:1493` (`scripts/meta_robots_audit.py`), `:1730` (the new `robots_audit.py` row) and `:1731` (`robots_audit_selftest.py`); `scripts/cache_key.py` and `scripts/cache_key_conformance.py` and `scripts/quote_class.py` by three each (`:1621`/`:1623`/`:1624`/`:1359`/`:1374` plus the new rows); `scripts/citing_set.py`, `scripts/citing_set_selftest.py`, `scripts/base_path_selftest.py`, `scripts/link_preview_selftest.py`, `scripts/live_snapshot.py`, `scripts/probe-delta.mjs`, `scripts/response_snapshot.py`, `scripts/robots_audit_selftest.py`, `scripts/sitemap_audit_selftest.py`, `scripts/source_recheck_selftest.py`, `scripts/source_snapshot.py` and `scripts/stale_extensions.py` by two each. The counter's own receipt agrees that the older row is still live and still failing: `controls/after-c1.txt:3` — `exec_fail 1104 scripts/robots_audit.py rc=2` — **unchanged from base** (`controls/base-c1.txt:29`, same line, same rc). | **None, and the frozen counter is structurally unable to catch it.** `c99_registry.py`'s `score()` computes `listed` as a **set** of tools that have *at least one* conformant row (`listed.add(p)`), and `mismatches = len(unlisted) + len(dangling)`; a second, stale, non-conformant row naming the same tool is neither unlisted nor dangling, so it is invisible to the instrument. The counter's own docstring declares the limit only for *row truth* ("R1-R5 are structural plus one execution; a row whose verdict map or write scope is false but well-formed passes this counter"), not for **row multiplicity**. PROTOCOL's Registry clause says nothing about how many rows a tool may have. | **Fix: none delivered, and none is this seat's to deliver.** The repair commit is **frozen** — the L1 may not rewrite it after the freeze, and this seat does not edit the registry. What this round's counter *does* establish is that the repair met its frozen target (`unlisted=0 dangling=0 mismatches=0 met=true`, exit 0, `controls/after-c1.txt:2`), which it does; **the duplicate rows are not a violation of that target**, they are a residue the target does not name. **Shown able to fail:** the *residue* is shown, not a failure — the duplicate scan above is the evidence, and it is reproducible from committed bytes with the scan in `diagnose_unlisted.py`. The counter cannot be shown failing here, because by its own rules this state is `met=true`; that is the finding. **Not shown able to fail:** no instrument exists that would refuse a duplicate row, and building one is a round-100 task (routed below), not something this seat can deliver inside a frozen round. |
| 5 | **Registry rows written from docstrings, not code (calibration) — the mistake that killed this round's C1.** The L1 wrote the 26 repair rows' verdict maps from each tool's docstring; for three tools the docstring contradicts the code: `quote_class.py` (usage `ap.error` exits 2, `return 64` unreachable; `--json` is a top-level flag), `wave_seat_record.py` (plain `ap.parse_args()`, usage exits 2, no 64 path), `sitemap_audit_selftest.py` (the runner never returns 2; tool-not-found is 64). Both review seats caught `quote_class.py` and `wave_seat_record.py`, one caught `sitemap_audit_selftest.py`; the frozen kill rule made C1 unmet. A second instance of the same class sat in the wave design: the ExecRegProbe item told the probe to excuse "argparse's usage exit 2", which is exactly the code the three rows mis-mapped, so the probe reported 0 contradictions. | `.ufo/waves/round-99/w1/ReviewRegA/verdicts.tsv` (rows `quote_class.py`, `wave_seat_record.py`); `.ufo/waves/round-99/w1/ReviewRegB/verdicts.tsv` (+ `sitemap_audit_selftest.py`); `.ufo/waves/round-99/w1/ExecRegProbe/findings.md`; `.ufo/waves/round-99/make_spec_w1.py` (ExecRegProbe item: "nor explained by argparse's usage exit 2") | round-98 criterion R98-A (row prose from located spans) applied to prose rows, never to exit-code cells; the round's own probe exempted the failing class | Criterion R99-B below: an exit-code cell is written from the code path (path:line of each `return`/`exit`/`ap.error`/`parse_args`) and checked by a probe that runs the no-argument and unknown-flag paths **without** exempting exit 2. Shown able to fail: the three rows as first written (`9d341d1b`) against plain probes — `python3 -B scripts/quote_class.py` rc=2, `python3 -B scripts/wave_seat_record.py` rc=2, `python3 -B scripts/sitemap_audit_selftest.py --bogus` rc=64 — each contradicts its row's map (`2` for usage absent / `2 setup fault` claimed with no 2 path); the corrected rows (lane tip) map those codes. Receipts: the reviewers' rc columns in the two verdict files. |

### Not mined, and why

- **Round-97 D-a (the meta-text leak at `corpus/knowledge/revalidation-exchange.md:130`, recorded at
  `corpus/lessons/round-97-verifier-spotcheck.md:42`)** — already mined: `corpus/lessons/round-98.md:70`
  (M2) and fixed at `0f48ada0`; the line is gone from the current tree (the file's line 130 now reads
  the errata sweep's own prose under its real heading). Not a new row.
- **Round-97 D-c / round-96 §1 defect 1 (the `planner` seat the validator rejects)** — a
  driver/validator-side defect, recorded in the lane's lessons as a disclosed disclosure
  (`corpus/lessons/round-96-verifier-spotcheck.md:55`, `corpus/lessons/round-97-verifier-spotcheck.md:51`)
  and routed to the driver template owner (R97-D2). It is not a lane work mistake and it is not the
  lane's to repair; it is listed here so the L1 does not re-mine it.
- **Round-98 R98-C2 (the round-98 C2 capability row has no admitted closure)** — **resolved by the
  round itself**: the row was moved out of the `## Capabilities` table into
  `### Capability rows without an admitted closure` (`SCORECARD.md:244`, `:258`). Mining it again
  would re-report a fixed defect.
- **Round-98 R98-C3 (the report cited the tip C1 receipt at `77adb17e` when it was measured at
  `76f834aa`)** — a report-wording defect about a **fleet-repo** file this seat may not edit
  (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-98/kake.md:66`); it is reported to the L1 in
  § Findings below rather than mined as a lane mistake. (The lane-side lesson line that repeats the
  receipt's *content* is `corpus/lessons/round-98.md:94`, which names the receipt file, not the
  revision — that is not wrong.)
- **The r99 `unbacked=1` tail of the round-98 C1 tip receipt** — that is the round-98 C2 capability
  row, which the round moved out of the table (`SCORECARD.md:258`); at the round-99 tip the row is no
  longer in the table, so the old tail is stale rather than an open defect.

---

## Quality criterion added this round

- **R99-A (from `considerthese/2026-11-05.md` Part 2 **proposal 4**, "Open-frontier map from the
  Planned sections").** **Every ground that a `Planned — after round N` section of `SCORECARD.md`
  names as still open is carried in one running map in `corpus/README.md` (a `## Open frontier`
  section, one row per ground, with the round in which that ground was **first** named open), and the
  map's first-named round is never later than the round that named it open.** A ground that a round
  picks up is struck from the map in that round's own commit; a ground still open keeps its original
  first-named round, so a stale item that has been named open for k rounds is visible as such rather
  than re-stated from scratch each round. Reject: a named-open ground with no map row, a map row
  whose first-named round is later than the round that named it open, or a ground struck from the
  map without a round having named it closed.
  - **Grounding.** `considerthese/2026-11-05.md` Part 2 proposal 4: "Parse each round's 'Planned —
    after round N' frontier line into a running list (revalidation §4.3, serve-stale, browser
    behaviour, live cache) with the round it was first named, so stale-but-never-picked-up frontier
    items surface." The lane already has the input half and not the output half: `SCORECARD.md`
    carries 12 `Planned — after round N` sections (rounds 84–98, `SCORECARD.md:5376`–`:5919`), each
    ending in a `Frontier:` clause naming still-open grounds — and `corpus/README.md` has **no**
    `## Open frontier` section (verified: the string does not occur in the file), so no ground
    carries the round it was first named. The concrete instance this round re-derives: the merged
    304 field set (`§4.3.4`) was first named open in the **round-93** Planned section
    (`SCORECARD.md:5748`) and named open again in round 94 (`:5772`), round 96 (`:5851`) and round 97
    (`:5890`) — **four rounds of a ground that this round finally picks up (C2)** — and no artifact
    records that it was four rounds old. The 304 header set (`§15.4.5`) and the §13.2 method filter
    were named open in the same round-93 clause (`:5748`) and are still open; the revalidation
    exchange (`§4.3`) and storage key identity (`§4.1`) were named open in round 95 (`:5801`).
  - **Check command.**
    `python3 -B .ufo/waves/round-99/w1/ScribeLesson/frontier_first_named.py --root <lane>`
    — exit 0 iff every named-open ground has a map row whose first-named round is not later than the
    round that named it open; exit 1 otherwise, printing one `missing_open_ground <id>` or
    `wrong_first_named <id>` line per violation. It reads committed bytes only (`git show
    <rev>:<path>` with `--revision`, the working tree otherwise) and writes nothing. **The script
    is a draft this seat wrote for the L1; it is not a registered lane tool and carries no registry
    row** — the L1's choice whether to land it under `scripts/` (which would then require its own
    conformant `SKILL.md` row, per mistake 1 above) or to write another.
  - **Shown able to fail — three negative controls and one positive, all run by this seat.**
    `red-control-frontier-map.txt`:
    - *positive control* — a scratch clone of the lane with a conformant map appended and committed
      (`db0a7662e402690d5861daa231e73c31bb329efe`, fixture identity, in this seat's scratch, never
      the lane): `named_open=4 map_rows=4 missing=0 wrong=0 met=true`, rc 0.
    - *negative 1* — one map row deleted: `named_open=4 map_rows=3 missing=1 wrong=0 met=false`,
      `missing_open_ground 4.3.4 (named open in round 93)`, rc 1.
    - *negative 2* — the `4.3.4` row's first-named round moved **later** than the round that named
      it open (`r93` → `r97`): `named_open=4 map_rows=4 missing=0 wrong=1 met=false`,
      `wrong_first_named 4.3.4 map_says_r97 first_named_r93`, rc 1.
    - *negative 3* — the whole `## Open frontier` section removed: `map_rows=absent missing=4 …`, rc 1.
    - *the lane at its tip (the red state the criterion names)*: `named_open=4 map_rows=absent
      missing=4 wrong=0 met=false`, rc 1, listing the four grounds
      (`15.4.5` first named r93; `4.1` and `4.3` first named r95; `4.3.4` first named r93).
  - **The check command's own limits, stated rather than hidden.** (i) It reads *free prose*, so a
    ground phrased in a way the regex does not recognise is invisible to it; the criterion binds the
    **artefact** (the map) and the check is this seat's approximation of it, not the criterion
    itself. (ii) A map row naming a ground **earlier** than the round that named it open passes —
    correct by construction, but it means the check cannot detect a map that under-reports a ground's
    age by naming it too early; that is the review conjunct's job, not the check's. (iii) The check
    knows nothing about whether a ground is *still* open; it reads the last `Planned` section per
    ground's naming round, so a ground named open in round 93 and closed in round 94 still counts as
    named-open until the map row is struck.

- **R99-B (from mistake 5).** Every exit-code cell in a SKILL.md registry row is written from the
  code (each `return`, `sys.exit`, `ap.error`, uncaught `parse_args`) with its path:line in the
  author's notes, and is checked by running the tool with no arguments and with an unknown flag;
  an observed rc absent from the cell is a defect, and argparse's exit 2 is never exempted. Check:
  `python3 -B scripts/<tool>; echo $?` and `python3 -B scripts/<tool> --zz-bogus </dev/null; echo $?`
  against the row's map. Red at `9d341d1b` for three rows (mistake 5), green at the corrected tip.

---

## Routed to round 100

- **R99-1 (from mistake 2).** A count cited in a lesson must name the receipt it was measured at,
  and a counter that refuses a quoted count which disagrees with its cited receipt. No instrument
  exists; the fix this round is documentary.
- **R99-2 (from mistake 3).** The two-reviewer conjunct's failure mode — one seat dead, one live,
  the conjunct scored on the survivor — needs a rule that the **report names which surviving seat
  carries the claim's review** (the r98 route R98-D2 asked for this in prose and it was not done).
  The freeze's kill rule closes the *verdict*; the *report's* disclosure is still open.
- **R99-3 (from mistake 1).** The C1 counter's declared limit — a well-formed row whose prose is
  junk reads `met=true` (`controls/ctl-c1-junkprose.txt:3`) — is caught only by the review conjunct.
  If a later round reuses `c99_registry.py`, that limit must travel with it, and a successor that
  wants to certify row *truth* needs a truth-checking instrument the current one does not provide.
- **R99-4 (from mistake 1, sub-classes (b)–(d)).** A successor registry counter that only asks "is
  there a row mentioning this tool?" would call 15 of the 26 green. It must apply the counter's own
  R1–R5 to **every** candidate row and treat a tool as unlisted when **no** candidate row conforms
  — not when the first one fails.
- **R99-5 (from mistake 4).** Duplicate registry rows: 16 of the 26 repaired tools are named by two
  or more rows at the repair commit, and the frozen counter is structurally blind to it (`listed` is
  a set; `mismatches = unlisted + dangling`). A successor should count rows per tool and report a
  tool with more than one *conformant* row, or with a non-conformant row shadowing a conformant one.
  The repair commit is **frozen** and is **not** a defect against its own target — this is a residue,
  routed for a future round, not a repair this seat or the L1 may make now.
- **R99-6 (from mistake 1, sub-class (d)).** `SKILL.md:1104`'s self-test span
  `python3 -B scripts/robots_audit_selftest.py [--tool PATH]` is not runnable as written — the
  bracketed placeholder is not the counter's `<placeholder>` form, so it reaches the tool as the
  literal argv `'[--tool' 'PATH]'` and the tool exits rc=2 (`controls/after-c1.txt:3`,
  `exec_fail 1104 scripts/robots_audit.py rc=2`, unchanged from base). The row is at the registry
  home; a future round may amend it. **The repair commit is frozen — this seat made no edit.**
- **R99-7 (from the frontier map, R99-A).** The `## Open frontier` map does not exist. The
  criterion's check command is red on the lane tip by four grounds. A future round that lands it
  must decide whether the map lives in `corpus/README.md` (as this draft assumes) or in a new
  `corpus/` file, and must strike each ground in the round that picks it up.
- **R99-8 (CriticClaims, C2).** Seven contract-violating candidates score `met=true` under the
  frozen `c99_fresh304.py` (`w1/CriticClaims/receipts/c2-e1…e7-*.txt`: stored hop-field stripping,
  lazy ETag validation, Last-Modified space trimming, whitespace on stdout, crash on bad JSON, Age
  exclusion, Last-Modified tie picks first). The landed candidate is not one of them (2400
  independent-generator inputs, 0 disagreements with the reference:
  `controls/c2-landed-vs-oracle-twin-generator.txt`), but the counter cannot tell; a successor adds
  hand cases for each class.
- **R99-9 (SentinelScope).** `c99_fresh304.py` runs candidates without filesystem, procfs or network
  isolation (W1 oracle theft via `/proc/<ppid>`, W2 writes outside the case dir, W3 shared state,
  W4 sockets); `c99_registry.py` `run_span` can be steered by a row (V1 single `&`, V2
  placeholder-masked redirects). Landed-candidate mitigation this round: static check
  (`controls/c2-candidate-static.txt`: imports json/re/sys only; the grep hits are docstring prose).
  Successor: namespace isolation, candidate bytes per case, `&` and placeholder hardening.
- **R99-10 (ReviewFresh, ExecTwinFresh).** Contract v2 clauses: token-form qualified `no-cache` /
  `private` (F1), the substring test catching unrecognised directives (F10), output values keeping
  leading/trailing OWS (F2), and an explicit case rule for LC6.
- **R99-11 (C1 re-entry).** Re-claim registry calibration with exit-code cells derived from code
  (R99-B) and a probe that does not exempt exit 2; keep the two-reviewer conjunct.
- **R99-12 (MutCounters).** `c99_registry.py`: 12 of 29 mutants killed, 10 confirmed survivors, 7
  not run (host `/fast` ENOSPC mid-run voided a batch); `c99_fresh304.py`: 13 of 23 killed (not
  re-run after the ENOSPC), 6 survivors, 4 not run (`w1/MutCounters/mutants.tsv`, `survivors.md`).
  Also F1: an `OSError` traceback in the registry counter exits 1, indistinguishable from
  `met=false`. Successor batteries take the survivors' separating inputs as fixtures.
- **Seat yield (R98-B).** 13/13 seats settled with a non-empty final output (`w1-results.json`);
  none dead. ExecFresh's final line notes the scored-blob clause was open at its own scoring
  (it scored `--candidate-file`); the L1 scored the committed blob at `998b6d5f`.
- **Carried unchanged** from the lane's own routes: R98-1…R98-5, R97-1…R97-5, R96-3, R95-6, and
  L0 R95-2.
