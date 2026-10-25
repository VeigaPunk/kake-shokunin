# ConnectorSiblingOverlap — kake round 51, wave 1

Seat: `L1Kake51.ConnectorSiblingOverlap-2` (connector, leaf, read-only). Judged on: operability, freshness.
Lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`, base `007d66e4e8360a5f88d29a93eeedd8066dad4434`,
lane tip at dispatch `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`. Date 2026-10-25.

Nothing installed or upgraded (no pacman, no `uv tool`, no `npx`). No `git add/commit/stash/checkout/switch/reset/pull/push`,
no mutating `jj`. Every sibling read is `git -C <lane> log|show|grep|ls-tree|rev-parse` at HEAD. Scratch: none needed.
No lane file was written except this report. No file I was asked to read was unreadable.

Axes named for the scan: **operability** (does a sibling already ship the wave-evidence accounting, route-probe
receipt, or instrument shape C1 buys?) and **freshness** (does a sibling already hold the canonical-selection /
crawler-identity ground C2 buys, or contradict it?). Both are no-harm constraints for the other claim.

## What the two counters printed (ran, read-only)

```
$ python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768c...
C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)
  C1_entries_exist pass   C2_entry_cites_id pass   C3_row_shape pass   C4_used_by pass
  C5_gate_quote_truth pass   C6_receipt_pins pass   C7_validate_before_append pass
  C8_append_after_mirror pass
C2 exit=0

$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768c...
C1 ledger 0/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 FAIL - settlement receipt absent at the measured revision
  L2 FAIL - route map absent at the measured revision
  L3 FAIL - settlement receipt absent at the measured revision
C1 exit=1
```

Cause, measured: `.ufo/waves/round-51/route-map.json`, `route-probes/*.json`, `wave-grant.txt` and
`wave-start-utc.txt` exist only as **untracked worktree files**; `git ls-tree -r --name-only 9d13768c -- .ufo/waves/round-51/route-probes`
prints nothing. The ledger reads `git show <rev>:<path>` only (`c51_wave_ledger.py:64-67`), so C1 is 0/3 for a
mechanical reason (nothing committed yet), not a design failure. `.ufo/waves/round-51/w1/` holds only
`swarm-registry.json` — no seat report, no `settlement.json`, no `wave-timing.json`, no `round-time-accounting.json`.

## Command set (reproducible)

```
for d in kumitate kotoba kotodama tabi revenger chousa souji mado kasegi; do git -C $d-shokunin log --oneline -18; done
for p in *; do git -C <lane> log --oneline --all --grep='round-5[01]'; done
git -C <lane> ls-files | grep -iE 'ledger|route-map|route_probe|route-probe|receipt'
git -C <lane> grep -lniE 'httpStatus|http_status|route.?probe|provider.?route|route-map' HEAD -- '.ufo/**round-5[01]**'
git -C <lane> grep -lniE 'canonicali[sz]|googlebot|google crawler' HEAD -- 'corpus' 'SOURCES*' '*.md'
git -C <lane> grep -lniE 'googlebot' HEAD -- 'corpus/knowledge'        # fleet-wide, all *-shokunin
git -C <lane> ls-tree -r --name-only HEAD -- .ufo/waves/round-51
```

Round reach at HEAD (why the window is three lanes, not nine): kumitate r60, kotoba r68, kotodama r69, revenger r68,
chousa r44, mado r35, tabi r22, souji r22, kasegi r23. Only kumitate, kotoba and kotodama have committed
round-50/round-51 material; revenger has none in that window (`git log --all --grep='round-5[01]'` prints nothing).

---

## Class 1 — wave-evidence ledger

**1a. In-window, same seat, same round number: kumitate r51 `.ufo/waves/round-51/w1/ConnSiblingOverlap.md:1-10`
(`:45` carries the kake row).** Duplicate of *this seat's* form, not of kake's claim. It names its axes, states read-only, and
tabulates each sibling's newest wave. Its kake row reads:

> `| kake | round-44 | 22:57 | ledger_latest_check=51 inside the round-44 wave. No receipt-attest, clock_gettime, getrandom, cap-run. |`

Two consequences for kake r51, both operational:
- The fleet's only recorded kake ledger hit is the needle `ledger_latest_check=51` inside kake's round-44 wave (that row). Kake's C1
  instrument `.ufo/waves/round-51/c51_wave_ledger.py` is invisible to every sibling scanner, including the two
  that ran this round (kumitate r51 above; kotoba r51 `.ufo/waves/round-51/build/SiblingOverlapScan.md:1-6`).
- No contradiction with C1: that row predates kake r51 and is a stale roster, not a competing claim.

**1b. Substantive analogue (out of window by round, exact in capability): kumitate `scripts/wave-census.mjs:1-47`,
contract `kumitate-wave-census-v1` (round 41).** It derives exactly kake L1's three clauses from committed evidence:
per-wave seat counts and roles (`:14-17`), `COUNT_MISMATCH` payload `counts.spawn` vs task count (`:30`, emitted `:202`),
`REGISTRY_MISMATCH` registry names vs task names (`:31`, `:212`), `STRAY_REPORT` a report naming no task (`:32`, `:226`).
Kake L1 is `c51_wave_ledger.py:97-142`: `reports_written` vs committed report files, settlement spawn vs payload seats,
`missing`/`extra` seat sets. The overlap is real and partial.
Difference that survives, and is the only defensible novelty claim: kumitate reads the **worktree** (`--round N --root DIR`,
`:41`); kake reads **revision-addressed committed bytes** — `git show <rev>:<path>` (`:64-67`), `git ls-tree` (`:79-85`) — and never opens the worktree.
That is not a cosmetic difference — today's 0/3 is precisely a worktree/commit split. C1 should claim *revision-addressed*
accounting, not "accounting", or it is buying a round-41 capability.

**1c. Same class, out of window: kumitate `scripts/dispatch-evidence.mjs:6-20`** (`kumitate-dispatch-evidence-v1`, r60):
`REPORT_ABSENT` (`:124`), `DEAD_SEAT_UNCREDITED` (`:126`), `NOT_A_DISPATCH` (`:130`), fail-closed `PROGRESS_ABSENT` (`:91-99`).
Its "a prepared spec is not a dispatch" rule (`:13-15`) is the same distinction kake L1 draws between payload spawn and
settlement spawn. Kake L1 is a strict subset of this instrument plus the revision addressing.

**1d. No sibling has L3's object.** Time accounting has no duplicate: kumitate r51 re-derives *SCORECARD terms*
(`.ufo/waves/round-51/plan.md:125`, "Stanza re-derivation (A/C/C2 terms + `pin.receipt-attest`)" at close), not seat
seconds; kumitate r51 commits no settlement/timing/accounting file (`ls-tree ... round-51 | awk -F/ '{print $4}'` →
`base build close plan.md probe receipts w1 …`, no time artifact); kotodama r51 `.ufo/waves/round-51/` holds
`build-spec.json`, `build-dispatch.json`, `build-swarm-registry.json`, `build-task-result.raw.txt` and seat reports —
no settlement, no timing, no accounting (`ls-tree ... | grep -iE 'settle|account|timing'` prints nothing); kotoba r51 has
only `build/` and `falsify/` (`ls-tree -r --name-only HEAD -- .ufo/waves/round-51 | awk -F/ '{NF--; print}'` → two dirs).
**L3 appears to be genuinely new fleet-wide.** That is the strongest single sentence C1 can say.

**Contradiction: none found** for class 1. One naming hazard, named above (1a): two instruments in one lane
(`scripts/ledger_latest_check.py` and `c51_wave_ledger.py`) with no reader-facing statement of which is the round's ledger.

## Class 2 — route-probe receipt shape

**2a. Same rule, weaker artifact, in-window: kotoba r51 `.ufo/waves/round-51/build/LeverOtherPages.md:69-75`** —
"Route probes that did not resolve (recorded, not used)" listing four 404s with byte sizes. That is kake L2's deviation
rule (`c51_wave_ledger.py:186-196`: failing receipt must carry an excerpt and be recorded as a deviation) stated for
documentation routes. Kotoba's record is **prose in a seat report** and its fetch receipts live in
`/fast/scratch/hyaku/kotoba-r51/build/LeverOtherPages/sources/` (`:76-78`, quoted from kotoba's own report as the record
that their fetch receipts are uncommitted; not a path this seat relies on), i.e. uncommitted. Kake's committed JSON
receipt with an integer `httpStatus` is strictly stronger; kotoba r51 is precedent for the rule, not competition for the
capability. Not a contradiction.

**2b. Same fetch-receipt convention, in-window: kotoba r51 `.ufo/waves/round-51/build/ReviewOverlapRows.md:115`**
(`curl -sS -w 'HTTP_STATUS %{http_code}'` ×3 → `HTTP_STATUS 200`, `EXIT 0`) and
`.ufo/waves/round-51/falsify/ReopenS031.md:105-106` (`HTTP_STATUS=200, curl_exit=0`, then `wc -c`, then `sha256sum`),
versus kake `.ufo/waves/round-51/sources/receipts.json:4-5` (`curl -sS -L -o <body> -w 'http=%{http_code} bytes=%{size_download}'`).
Same invocation family, same evidence triple (status, bytes, sha256). Consistent, no conflict; kake's is the committed form.

**2c. No sibling commits a *provider/model-route* probe receipt.** Command:
`git -C <lane> grep -lniE 'httpStatus|http_status|route.?probe|provider.?route|route-map' HEAD -- '.ufo/**round-5[01]**'`
over kumitate, kotoba, kotodama, revenger, chousa → kotodama and kumitate and revenger and chousa: **no output**;
kotoba: the four doc-fetch files in 2a/2b only. Nearest shapes, both in kumitate:
- `.ufo/waves/round-47/probe/caproute-probe.mjs:2-25` (out of window). Named "route" but means *capability* route: it
  proves the actual exec chain under `strace` (node → `systemd-run --scope` → `bwrap`), prints one `SITE … label=ROUTED_HELD|ROUTED_MISS`
  per frozen site, and **exit 2 when it cannot evaluate** (`:18-19`, `:25-26`). Kake's L2 has no exit-2 leg at all: `c51_wave_ledger.py`
  returns a note and the claim reads 0/3 or 3/3, so "the receipt is missing" and "the route is broken" collapse into one verdict.
- kotodama r50 `reports/round-50/jj-colocation-probe.py` + `reports/round-50/telemetry/jj-probe-v3.txt:1-3` (in window).
  Committed JSON-lines receipts per case (`exit`, `kind`, `name`, `flagged`, `evidence`), version ladder `v1/v2/v3` retained,
  and the first line pins the probe's own sha256 (`probe v3 sha256 dee0c65b… — R1 requires landed_sha == origin/main tip and
  a refusal`). Subject is a jj/git receipt guard, not a model route.
**Contradiction: none.** One gap the comparison exposes: kake's route-map `probe` strings are prose
(`route-map.json`, `"completion leg answered PONG via \`omp -p --mode json --model @m_flash\`"`), and the probe command's
identity/sha is not in any receipt — kotodama's v3 header is the sibling counter-example.

## Class 3 — canonical / crawler-identity knowledge entry

**None found.** Commands and output:

```
$ for p in *-shokunin; do git -C "$p" grep -lniE 'googlebot' HEAD -- 'corpus/knowledge'; done
kake-shokunin: corpus/knowledge/crawl-error-status-table.md, corpus/knowledge/crawler-identity.md,
               corpus/knowledge/dynamic-rendering-workaround-limits.md, corpus/knowledge/js-rendering-queue.md
(no other lane prints a line)

$ git -C <nine lanes> grep -niE 'canonicali[sz]|googlebot|google crawler' HEAD -- 'corpus' 'SOURCES*' '*.md'
```

Every nine-lane hit outside kake is a different sense of "canonical": filesystem/argv `realpath` canonicalization
(kumitate `.ufo/waves/round-50/r50/SentTmpPath.md:25`, kotoba `.ufo/round-40/scouts/P6.md:324`), URL/authority
canonicalization in a fetcher boundary (kotodama `.ufo/waves/round-63/w1/CtlORedirectEdge.md:442`), or snapshot bytes.
No sibling holds or claims Google's canonical selection or Googlebot identity.

Ownership is settled by the provinces, not by inference: kake `PROVINCE.md:22-23` ("Crawl hygiene per host (robots.txt,
sitemap scope, canonical signals) … canonical/JS rendering open") and `:34-35` ("`tabi` drives browsers and owns
client-side crawler discipline; kake owns publisher-side placement"); kotodama `PROVINCE.md:19-20` refuses "web publishing
(kake)". tabi's own knowledge base carries `User-Agent` only as CDP evidence (`corpus/knowledge/cdp-evidence-patterns.md:41`)
and a fixture (`external-class-fixture-v2.md:181`), not crawler identity.

**Adjacent, outside the scan window — name, do not absorb.** kotodama `.ufo/waves/round-53/build/ScribeSec04Pointing.md:163`
(a gated PDF requested with `?crawler=true` and with "a Googlebot user agent"; both HTTP 403) and
`.ufo/waves/round-53/build/CriticSourceTiers.md:71` (recorded as "an attempt on an access control, not an ordinary request
… should be recorded as attempted and not passed"). This is *publisher access control observing a user-agent string*.
It neither supports nor contradicts S263, which is Google's own account of how its crawler identifies itself. If S263's
body is ever read as "sites should treat a Googlebot UA as Googlebot", this sibling record refutes the inference from the
other side — cite it as a boundary, never as evidence for the entry.

**Name-only collision.** kumitate `corpus/knowledge/receipt-identity-canonicalization.md:1-5` (receipt identity
canonicalization, RFC 8785 + coreutils sha256sum). Same word, different subject; no reader should merge them, and neither
lane should cite the other's row for it.

## Attack that survived, and one that did not

- *Survived:* duplicate-URL reuse for S262/S263. At `9d13768`, `grep -oE 'https://developers\.google\.com/search/docs/crawling-indexing/[a-z-]+' corpus/SOURCES.md | sort | uniq -c`
  gives `…/canonicalization` ×1 and `…/googlebot` ×1, while the registry already tolerates duplicates elsewhere
  (`…/javascript` ×4, `…/canonicalization-troubleshooting` ×2). So C3/C6 are not tripped by URL reuse. C2's 8/8 is not a
  duplicate-row artifact.
- *Disclosure, not a predicate failure:* the theme was already partly held at base. `git show 007d66e:corpus/SOURCES.md` carries
  S021 (`…/consolidate-duplicate-urls`) and S022 (`…/canonicalization-troubleshooting`), both used-by
  `corpus/knowledge/static-canonical-preflight.md`. C2's "before: neither entry" is true **for the two entry paths**
  (`canonical-selection.md` and `crawler-identity.md` are absent at base; only `static-canonical-preflight.md` exists) and the
  counter scores exactly that. The freshness claim must be read as *re-grounding two new entries on new rows*, not as
  "first canonical ground in the lane". Stating it that way costs nothing and forecloses the obvious critic reading.

---

## Proposed move (one, bounded)

**Make L2 leg-aware without adding a pass condition this round, and commit the receipt for the leg the wave actually used.**

Evidence it is needed:
1. `c51_wave_ledger.py:169` keys receipts with `receipts.setdefault(alias, receipt)` and never reads `receipt["leg"]`
   (no `leg` reference anywhere in `check_l2`, `:145-197`). The two committed probes are explicitly typed:
   `route-probes/commandcode_deepseek-v4.1-flash.json:8` `"leg": "http-edge"`, `route-probes/xai-oauth_grok-4.7-fast.json:8`
   `"leg": "cli-completion"`. The role binding that L2 certifies is `kimiModel` (`:171`), and the receipt that certifies it
   proves only that `https://api.commandcode.ai/` answers `{"success":true,"message":"Command Code API"}` — not that
   `@m_flash` completes. The wave's real leg is named only in prose in `route-map.json`.
2. The instrument punishes the honest fix. `list_paths` returns path-sorted order; between
   `route-probes/commandcode_deepseek-v4.1-flash-completion.json` and `route-probes/commandcode_deepseek-v4.1-flash.json`
   the first difference is `-` (0x2d) vs `.` (0x2e), so the completion receipt sorts **first** (verified:
   `sorted([a,b])` → completion path first). `setdefault` then keeps the completion receipt, a CLI completion carries no
   integer `httpStatus`, and `:177-179` appends "carries no integer httpStatus" → **L2 FAIL**. `[INFERENCE]` from those three
   code lines; the consequence is mechanical, not speculative. So the L1 cannot strengthen L2's evidence by adding the
   truthful receipt — the counter silently aliases one receipt per route and is order-sensitive.

The move: (i) accumulate receipts per alias instead of `setdefault`, so no receipt is discarded and the verdict does not
depend on filename order — verdict-neutral on today's one-receipt-per-alias set; (ii) print `legs=<alias>:<leg>[,…]` and a
`leg_without_receipt=<alias>` fact naming any leg the route map's `probe` text asserts but no receipt carries — a fact, not a
pass condition, so the frozen predicate `ledger_checks_passed == 3 of 3` and L1/L2/L3's texts are untouched; (iii) commit the
completion-leg receipt `route-probes/commandcode_deepseek-v4.1-flash-completion.json` with `ok`, `answer`, `exit`, `probedAt`
and the probing command's sha256 (kotodama `jj-probe-v3.txt:1` precedent), so r52 can tighten the check with material in hand.

Affected axes: **operability** (L2 stops certifying a leg it did not probe, and stops discarding receipts). **Freshness
untouched**: the ledger reads no C2 input — contract `separability` already states the two counters share no bytes, so an
L2 change cannot move C2's 8/8.

Risks:
- The counter is frozen. Changing it after the wave is the "instrument revised after scoring" attack. Mitigation, and the
  reason the change is bounded to facts+robustness: commit it as `c51_wave_ledger.py` revision 1 with a forcing receipt that
  runs rev 0 and rev 1 **at the same revision** and shows identical pass/fail (kotodama r50 `52b92a6` is the fleet precedent
  for a post-wave counter revision with a forcing receipt and no leg trusting the harness self-report).
- If the completion receipt is left uncommitted, the limitation disclosure has no support — then say `leg_without_receipt`
  explicitly in the lesson instead of implying coverage.
- A stricter leg requirement is *not* proposed for this round. Adding one would amend a condition frozen in
  `contract.json`, which no seat may do after data; it belongs in r52's freeze.

Verification (run by the L1, not by this seat):
1. `python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 007d66e4e8360a5f88d29a93eeedd8066dad4434`
   → `0/3 met=False` exit 1, identical to today's reading.
2. Same command at the wave-evidence tip → `3/3 met=True` exit 0, and the output carries `legs=` and no
   `leg_without_receipt=` for `commandcode/deepseek/deepseek-v4.1-flash`.
3. Rev 0 vs rev 1 at that same revision → identical pass/fail; the diff touches no pass condition.
4. /tmp fixture (never the lane): two receipts for one alias, completion-first and status-less → rev 1 must **not** fail L2 on
   it and must print the leg fact; this is the arm that fails today.
5. `git ls-tree -r --name-only <tip> -- .ufo/waves/round-51/route-probes` lists both receipts.

## Limits of this report

- I did not re-run another seat's counter conclusions; the two `C1`/`C2` readings above are my own executions at `9d13768`.
- The `[INFERENCE]` in the move (completion receipt breaking L2 today) rests on three code lines plus a string-order check;
  I could not execute it, because demonstrating it requires writing a file into the lane, which this seat may not do.
- Out-of-window sibling material (kumitate r41/r47/r60, kotodama r50/r53) is cited to bound the overlap, never as kake r51
  evidence.
