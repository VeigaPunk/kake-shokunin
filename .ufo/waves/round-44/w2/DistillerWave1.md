# DistillerWave1 — wave-1 attack ledger (round 44, wave 2)

Axes: operability + freshness (lane-owned). This report distills the 24 wave-1 reports
in `.ufo/waves/round-44/w1/*.md` into a numbered attack ledger: one line per distinct
finding, each marked **DISPOSITIONED** (by a named SCORECARD pre-freeze amendment) or
**STILL-OPEN**. This is wave-2 evidence for the L1; it makes no round judgment.

## Amendment key (SCORECARD.md round-44 section, all recorded pre-freeze)

- **A** = "pre-freeze amendment, item A": C1 before-state replaced by the placebo counter
  (`c44_placebo.py`, sha `9ce3acd4…`) measuring k/27; "27/27 blind under fresh v4" premise
  abandoned; `control-v4blind.json` kept as inherited calibration evidence.
- **B** = "pre-freeze amendment, item B": C2 scope fixed — exact endpoint equality (not
  containment); three counted figures (§8.1 tally, §8.5 do-nothing ratios, §8.5 build
  range); §8.4 wave composition explicitly excluded (revision-dependent denominator);
  §8.7 carried by S131/S132 superseding rows; every repair line must name receipt + value.
- **F1** = "pre-freeze correction 2, item 1": witness classifier — `semantic_witness`
  changed from "all caughtBy keys are class runs" to `any(k in class_keys)`;
  `classCaught`/`legacyCaught` exposed per row; mixed-key + timing-only + legacy-only
  selftest fixtures; new audit sha `8ee2c8bf…`.
- **F2** = "pre-freeze correction 2, item 2": manifest row fix — `buildport-m6` relabelled
  `portdigit/G9` → `default_port/G2` (verified on disk: `controls-27.tsv:26`).
- **F3** = "pre-freeze correction 2, item 3": C2 counting command — checker takes no
  `--spec`; three-figure contract fixed in `contract_spec()`; command is
  `python3 -B scripts/ledger_latest_check.py --root .`; `--selftest` is the able-to-fail gate.
- **PR** = the frozen predicate-reading paragraph in correction 2: "no v4-corpus run does"
  reads as *a v4 divergence is never a class witness*, not *no v4 divergence may occur*.

Verified on disk this session: `c44_audit.py` sha256 is `8ee2c8bf…` (F1 landed);
`controls-27.tsv` row 26 reads `buildport-m6 default_port G2` (F2 landed); checker has no
`--spec` flag and `contract_spec()` pins the three figures plus strict
`master` receipt enumeration (F3 landed); all 10 class modules and all 10 placebo modules
exist; C2 checker exits 0 (evidence below).

## Attack ledger

Status codes: **D** = dispositioned (amendment named); **O** = still open;
**I** = informational/no defect (kept for completeness).

### A. Claim-design attacks (critics)

1. **"27/27 blind under fresh `--classes v4`" is falsified.** `verification/freeze/control-v4blind.json` records `witnessed:2` (`buildscope-m5` on D, seed 181346457990762; `repeat-depth-deep` on C, seed 5994504518804) — stdout-hash divergences, not timing. Pointer: `w1/CriticClaimC1.md` (decisive counterexample + a1); `w1/CriticMathDenominator.md` (findings 3, strongest counterexample); `w1/ReviewInheritedLineage.md` F2. → **D by A** (before-state is now placebo k/27; the failed receipt is retained as evidence, and PR forecloses any universal-v4-blindness reading).
2. **`met:false` counted as witness; `all`-key classifier rejects mixed catches.** Initial audit counted not-met (incl. timing-only and cannot-evaluate rows, e.g. `ref41-base.json` 11/11-equal met:false T1 4.207/T5 7.047) as witnessed; intervening classifier required *every* caughtBy key to be a G key, so `["D","G3"]` was not witnessed. Pointer: `w1/CriticClaimC1.md` (a2); `w1/CriticMathDenominator.md` (finding 5). → **D by F1** (verified: `c44_audit.py:63-97` `any`-key semantics, `classCaught`/`legacyCaught` at `:199-200`, selftest asserts mixed-key true and timing/legacy-only false).
3. **`buildport-m6` misclassified `portdigit/G9`** — its source (`controls-r43/buildport-m6-default-branch.py:303-304`) inverts the default-port branch; mechanism is default-port, not port-digit memo. Pointer: `w1/CriticClaimC1.md` (a3); `w1/CriticMathDenominator.md` (finding 2 + row 25); `w1/ScoutBuildMutants.md` §m6; `w1/ExecG9PortDigits.md` (implicit-port note); `w1/ExecG1LongPort.md` (negative G1 benchmark). → **D by F2** (verified: TSV row reads `default_port G2`; hash unchanged `68f37500…`).
4. **"27" is a named cohort, not an exhaustive escape census.** Durable r43 reports contain additional *meeting* controls outside the manifest (`V5_tail_cache64` met at seed 238536594047229; `p45/p46/p64_noreval` and `p48_weakreval` met with witnesses) — an exhaustive reading of "the round-43 controls" is refuted. Pointer: `w1/CriticClaimC1.md` (b). → **O** — the declaration name-binds to "the 27 round-43 controls registered in controls-27.tsv", but no exclusions/late-report note or manifest-SHA binding sentence was added; the L1's exact "the 27 named tools in manifest SHA …" phrasing is not on the record.
5. **Unsandboxed class modules can read control files / environment at generation time** — `load_classes` imports seat-authored modules in-process (`c44_count_v5.py:136-152`); `cases(rng, h)` runs at `:1064` before `box.run` enters bwrap (`:920-978`); probe loads+runs the module at `c44_probe.py:58,77` before its sandbox. A module reading a control's file would make the capability circular (kill rule 4). Corollary: G8's 46/46/34-table fixed host population is targeted regression, not fresh-host blindness. Pointer: `w1/SentinelScope.md` (finding 1, High); `w1/CriticClaimC1.md` (c1); `w1/ExecG8Hosts.md` (self-disclosed bound). → **O** — no amendment addresses execution isolation or declares the "open-book targeted regression" scope in the claim text; kill rule 4 exists but is detection-by-review, not enforcement.
6. **Receipts do not pin class-module bytes; v4/v5 streams are not paired.** Receipts record `counterSha256` + class names, not class content hashes (`c44_count_v5.py:999-1003`); `build_v5.py --check` validates only the counter file; one shared RNG feeds A–F, G1–G10, T1–T5 so equal seeds give different T-stream inputs across modes. Pointer: `w1/CriticClaimC1.md` (c2); `w1/ReviewCounterContract.md` (residual nits). → **O** — no freeze manifest binds counter + 10 class modules + audit + TSV + control files to each tally.
7. **Build reuse framing + driver laxness.** `020bc457` is legitimate as a positive regression control but cannot reopen r42/r43 rejections or prove "no out-of-class harm" (H4 receipt shows `outOfClassChanged:21`); driver's `bool(build)` check accepts any `--build-runs N` and does not assert `len(rows)==27` (missing tool shrinks denominator silently — though `total==len(rows)` errors block ok=True). Pointer: `w1/CriticClaimC1.md` (d); `w1/CriticMathDenominator.md` (finding 4, fixable denominator presentation). → **O** — command line supplies `--build-runs 3` and canaries moved to a separate 5-row TSV (partial mitigation), but the driver still asserts neither `rows==27` nor `build-runs==3`, and no "audit-corpus discrimination" naming sentence landed.

### B. C2 design attacks (CriticClaimC2)

8. **Bare numerical suffix masquerades as a correction.** A regex counting numbers can green on an example or unlabelled line. Pointer: `w1/CriticClaimC2.md` (a). → **D by B** (each repair line must name receipt + derived value — the landed LOG/SCORECARD repair lines do).
9. **Mutable spec / mutable expected source.** A JSON spec edit or worktree glob could shrink the claim (50→51 report dir demonstrated). Pointer: `w1/CriticClaimC2.md` (b). → **D by F3+B** (verified: `contract_spec()` pins the three figures, `load_spec` raises InputError on any JSON deviation, `rescore_receipts` enumerates `master` strictly and InputErrors on empty set; §8.4's mutable-glob figure excluded). Ledger read still prefers worktree file over `master:` — a deliberate mixed-source design point the critic flagged; recorded, accepted by the amendment's scope.
10. **"Last statement wins" ≠ latest operative correction.** Last-regex-match can select quoted/incidental text; wrapped statements and mixed-record pairs need negative fixtures beyond one-green/one-red. Pointer: `w1/CriticClaimC2.md` (c). → **O** — implemented checker is exactly `matches[-1]` on `re.S` (`ledger_latest_check.py:192-201`); the claim-level "repair line names receipt" mitigates socially but the grammar/negative-fixture hardening the critic asked for was not adopted; selftest remains 2/2 basic fixtures.
11. **Whole routed set exceeds the three counted figures.** §8.3 (fleet-report attribution error) and §8.8 (QUALITY capture for Mistakes 7/9/10/11 — grep found no round-43/44 cite in `corpus/QUALITY.md`) remain routed work; §8.4 needs its own pinned-revision correction of *both* ledgers. Pointer: `w1/CriticClaimC2.md` (d, including the "5 assertions for 4 families" note — mooted by scope cut but still unrouted). → **Partially D by B** (§8.4 exclusion declared; §8.7 carried by S131/S132 — verified rows 139-140 in `corpus/SOURCES.md` opening `supersedes S129 —`/`supersedes S130 —`); **O for §8.3 and §8.8** — no checker or amendment covers them.
12. **Containment accepts any enclosing range.** 0–999 would "contain" the build ratios. Pointer: `w1/CriticClaimC2.md` (equality/precision attack). → **D by B** (exact rounded equality; verified live: checker compares quoted vs ROUND_HALF_UP-derived endpoint strings).
13. **Append-only correction is possible** — SCORECARD `:3334-3339` precedent; no impossibility premise. Pointer: `w1/CriticClaimC2.md` (e). → **D by B** (corrections were appended, prior bytes preserved).

### C. Class-generator correctness attacks (scouts/revenger → executor outcomes)

14. **G1–G4/G9 blueprints as specified do not witness; `layout_f` quirks decisive.** `derived_smu("https://host")` yields `https://hostsitemap.xml` (no `/` after authority → `find`=-1 path); `segment_smu("…/sitemap.xml")` yields `…/sitemap.xml/sitemap.xml`; out-of-range port on sitemapUrl → `check_invalid` (exit 2) not `loc_not_absolute`. G2 needed pairfile (explicit-`:443` member 1, implicit https later); G3 needed pairfile/`?`-form for pathless loc; G4 needed shared first segment, one scheme; m6 needed two *explicit* differing ports in one pairfile (implicit port stays `None`). Pointer: `w1/ScoutBuildMutants.md` (all §); `w1/ScoutRef41Semantics.md` (falsifications 2,3,4). → **D** — G2/G3/G4 modules shipped in corrected forms and each probe-witnessed on two seeds (`w1/ExecG2DefaultPort.md`, `w1/ExecG3EmptyPath.md`, `w1/ExecG4PortScope.md`); m6 reassigned to G2's witness shape by F2.
15. **G9 planned shape (a) — two `value` units, same port digits, different hosts — cannot witness the port-digit memo**: the second check's derived sitemapUrl carries the same digits and hits the same poisoned cache slot, keeping `parsed[:3]` self-consistent (observed: both clean). Required: one `pairfile`, same port digits, host₂≠host₁, sitemapUrl anchored on member 1. Pointer: `w1/RevengerControls.md` (§2 + hand-off); `w1/ExecG9PortDigits.md` (implicit-port source note). → **D** — shipped G9 emits pairfile same-check shapes; `portvalue-digits` and `portvalue-digits-67` witness on seeds 4401/4402 (exit 1, `equal:false`).
16. **G6 fold-pair shape cannot witness any casememo control.** U+212A (Kelvin) and U+017F (long s) are legal path codepoints under ref41's `_URI_RE` (`_UNRESERVED` includes U+0080–U+10FFFF) — all 8 probes returned `equal:true`, both exits 0; `.lower()`/`.casefold()` collapse them to `k`/`s` (`k k s`), so no `loc_not_absolute` difference can arise within the stated constraints. Pointer: `w1/ExecG6Fold.md` (blocker); `w1/ScoutRef41Semantics.md` (falsification 1). → **O** — **the one open build item**: casememo-v3/v4/v7/v8 unwitnessed; needs a genuinely rejectable defect shape or a fold-class reassignment; constraints named (ref41 accepts these letters; assignment named no alternative).
17. **G7 band-memo constraints** (enumerated, all load-bearing): len-band needs equal length in 6001–199999 → always `loc_too_long` on both → stdout-only divergence, never "control says clean"; depth/defpos band pairs must stay ≤1799 cp; defpos clean member must carry a valid `%HH` at the shared index; out-of-window len≥1800 witnesses only the uncapped deep/late controls. Pointer: `w1/ScoutBandFamily.md`; `w1/RevengerControls.md` (§3, comment-vs-code discrepancy: 1799 bounds `len`, not '%' index). → **D** — shipped G7 uses 6001–6040 lengths (constraint conflict recorded), 64–103 slash counts, (1600–1639, 1000–1039) defpos keys; all 5 controls witness on both seeds (`w1/ExecG7Bands.md`).
18. **G8 host-table constraints**: copy the union (A=B 46 hosts; F is a 34-subset — 12 A/B-only hosts are not F witnesses); defect in path after first `/`, `loc` field only; `%HH` and clean paths are non-witnesses. Pointer: `w1/ScoutHostFamily.md`; `w1/RevengerControls.md` (§1 confirms G5 covers V2). → **D** — shipped G8 covers all three tables; all 3 controls witness on seeds 44/45 (`w1/ExecG8Hosts.md`); fixed-population bound disclosed (feeds finding 5).
19. **G10 `loc_out_of_scope` path-window shape unreachable under frozen `layout_f`**: every `value`/`loc` goes through `derived_smu` (authority-root sitemapUrl), so a truncated crossing path cannot produce the scope divergence. Hidden-defect cases *did* witness both G10 controls on both seeds; the specified scope-witness shape needs a per-value segment sitemapUrl the freeze forbids. Pointer: `w1/ExecG10Windows.md` (scope-shape blocker); `w1/ScoutRef41Semantics.md` (4). → **Partially D / O** — the *item's* witness was achieved (both headtail-V4/V8 probed exit 1 ×2 seeds); the *specified shape variant* remains unreachable under the frozen layout — recorded design boundary, not remediated.
20. **G1 covers the three portlen controls; not m6.** Probes: portlen-v1/v5/v4 witness on seeds 44001/44002; `buildport-m6` equal on both (supports F2). Pointer: `w1/ExecG1LongPort.md`. → **I/D by F2**.
21. **G5 prefix/head-tail coverage** incl. headtail-V2's >96-cp shared first48+last48 window (RevengerControls independently probe-verified V2 on seeds 101/202 before the module landed). Pointer: `w1/ExecG5Prefix.md`, `w1/RevengerControls.md` §1, `w1/CriticMathDenominator.md` (V2-not-a-second-defect note). → **D** — all 4 prefix-family controls witness on both seeds.

### D. Instrument/build attacks (reviews, sentinel)

22. **`c44_audit.py` was a live-edited moving target mid-wave** (unparseable at 20:10, compiling at 20:11; duplicate-keyword SyntaxError observed in a concurrent-read window). Pointer: `w1/ReviewInheritedLineage.md` (F1); `w1/SentinelScope.md` (finding 4 — freeze-vs-"Harden" contradiction in seat prompts); `w1/CriticClaimC1.md` (AST step transient failure). → **D by F1** — classifier edit landed, file froze at sha `8ee2c8bf…`; the authority contradiction resolved by the L1 taking the correction itself.
23. **`control-v4blind.json` proves less than a passing gate**: `ok:false`, `build:[]` (no build rows), `tools/` populated — supports neither C1 v5-witness nor build-meets-v5; proves only 2-of-27 seed-dependent v4 divergence. Pointer: `w1/ReviewInheritedLineage.md` (F2). → **D by A** — re-scoped to inherited calibration evidence, re-scored with frozen bytes; not a claim receipt.
24. **G9 module missing at review time** — `load_classes` hard-requires all 10 (`:144-145`); only placebo existed. Pointer: `w1/ReviewInheritedLineage.md` (F3). → **D** — `classes/g9_port_digits.py` now present (verified) and witnessing.
25. **v5 counter = strict superset of v4**: `--check` byte-exact (`5cedaa3b…`), 8-hunk diff confined to class wiring, v4 mode generates zero class runs, equality/timing semantics unchanged; 21 vs 11 run keys confirmed by replay. Pointer: `w1/ReviewCounterContract.md`. → **I** (supports claim; residual nits folded into finding 6).
26. **`controls-27.tsv` verified clean**: 27/27 sha256 match, paths exist, seat reports exist, family/class sums 27; 14 l1-rescore receipts' `toolSha256` all match their rows; 13 rows have no rescore receipt (evidence gap, not mismatch). Pointer: `w1/ScoutRegistry.md`. → **I**.
27. **Sentinel scope findings** — pointer: `w1/SentinelScope.md`:
    - (1) High: class modules execute unsandboxed → folded into **finding 5 (O)**.
    - (2) Medium: no size/count quota on generated class input (`layout_f` writes unbounded XML; `OUT_CAP`/`AS_CAP`/`RUN_TIMEOUT` only bound the sandboxed tool) → **O**.
    - (3) Medium: audit `--out` opens mode `"w"` with no existence/path check; probe `--keep DIR` uses `dirs_exist_ok=True` — receipts can be overwritten by a chosen destination → **O**.
    - (4) Medium: `c44_audit.py` freeze-vs-edit contradiction → **D** (finding 22).
    - (5) Low: tool-install exception exceeds file allowlist → **O** (policy note).
    - Note: registry `.items|length` = 35 vs advertised 36 → **I**.
28. **Wave-1 coverage gap (this seat's observation)**: registry lists 35 member seats; `w1/` contains 24 reports. **11 registered seats left no wave-1 report**: ExecAudit, ScoutPortFamily, ScoutFoldFamily, ScoutWindowFamily, ReviewAuditDriver, ReviewLedgerCheck, ConnectorSibling, MutationTesterAudit, LabratKelvin, LabratScopeSmu, SimplifierInherited. Their assigned attack surfaces (audit-driver hardening, ledger-check review, audit mutation testing, port/fold/window families, scope-SMU lab) are unreported — treat as unrun coverage, not as absence of defects. → **O** (wave-2 should either regenerate or explicitly waive these probes).

### E. Freshness-side items

29. **C2 checker landed and passes**: `contract_spec()` pins 3 figures; receipts read via `git show master:`; last-match `re.S` selection; ROUND_HALF_UP at quoted precision; selftest 2/2. Before-state `3 figures, 3 mismatches` recorded at `verification/ledger-before.txt`. Pointer: `w1/ExecLedgerCheck.md`. → **D by F3+B**; residual hardening ask → finding 10.
30. **S129/S130 anchor locators corrected via superseding rows** per spot-check §8.7. Pointer: `w1/ScribeSources.md` (Gate text + quote word counts 6/8/10). → **D by B** (S131/S132 rows verified present in `corpus/SOURCES.md`).

## Decisive command output (run by this seat)

```text
$ python3 -B scripts/ledger_latest_check.py --selftest
ledger_latest_check --selftest
  PASS matching fixture MATCH quoted=14 derived=14
  RED MISMATCH mismatching fixture quoted=18 derived=14
selftest: 2/2 passed
```

```text
$ python3 -B scripts/ledger_latest_check.py --root .
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:3575
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:1703
build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1706
ledger-quotes: 3 figures, 0 mismatches
EXIT=0
```

```text
$ sha256sum .ufo/waves/round-44/{c44_audit.py,c44_count_v5.py,c44_placebo.py,controls-27.tsv}
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  c44_audit.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  c44_count_v5.py
9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27  c44_placebo.py
a1f0e364dad5ff937666966a16622e6895591a2eb3db714d6ecf3f3948c31bf8  controls-27.tsv
$ grep -n "buildport-m6" .ufo/waves/round-44/controls-27.tsv
26:buildport-m6	default_port	G2	…	68f3750025531d7815d6ec665432536abc3b0c78a036fdb49339e1f73bcbe87e	w1/MutBuildPort.md
```

**Pass/fail against this item's named attack** (distill the 24 wave-1 reports into a
dispositioned attack ledger): **PASS** — 24/24 reports read in full; 30 numbered ledger
entries; every entry carries a report pointer and a disposition vs the named amendments.

## Disposition summary

- **Dispositioned:** 1, 2, 3, 8, 9, 11(partial), 12, 13, 14, 15, 17, 18, 20, 21, 22, 23, 24, 27(4), 29, 30.
- **Still open:** 4 (cohort-exhaustiveness/exclusions note), 5 (unsandboxed class execution + open-book scope), 6 (instrument-identity binding), 7 (build-run/row-count assertions + naming), 10 (operative-statement grammar + negative fixtures), 11 (§8.3, §8.8 routed work), 16 (**G6 casememo ×4 — the one open build item**), 19 (G10 scope-shape variant unreachable under frozen layout), 27(2,3,5) (input quota, output confinement, install-allowlist), 28 (11 unreported seats).
- **Informational:** 20, 25, 26, 27(note).

## Files written by this seat

- `.ufo/waves/round-44/w2/DistillerWave1.md` (this report)
- `/fast/scratch/hyaku/kake-r44/DistillerWave1/` (created; empty — no scratch artifacts needed)

## Bounds and unrun checks

- No frozen artifact edited; no class module, counter, audit, TSV, control, receipt, ledger, or sibling file touched. No git/jj/commit/push. No installs (system python3 + coreutils sufficed). No peer messages needed.
- **Unrun by this seat** (not required by the item): the C1 audit pair (`c44_audit.py` v4/v5 runs — 20+ min each), `c44_probe.py`, `build_v5.py --check`, the canary run, and any full counter execution. The G6 open item is reported from wave-1 seat evidence, not re-probed.
- LSP: no `lsp` device is exposed in this session's tool inventory; caller/reference checks were done by direct file reads of the small named files (checker, TSV, probe, counter fragments) — recorded as the literal fallback.
