# CriticCapability — C1: capability acquisition or instrumentation theater?

Seat: `L1Kake51.CriticCapability-2`. Lane: `kake`. Round 51, wave 1.
Reviewed claim: **C1** (axis `operability`), frozen in `.ufo/waves/round-51/contract.json`.
Base: `007d66e4e8360a5f88d29a93eeedd8066dad4434`. Lane tip at dispatch: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`.
Mode: read-only. Every synthetic run below happened in `/tmp`; the lane was not written except this file.

---

## 0. Verdict (up front)

**Capability was acquired; the certificate is over-claimed.**

The lane gained something it did not have at base: a deterministic, read-only, third-party-runnable
falsifier over committed bytes, plus two committed-artifact types that did not exist
(`wave-timing.json`, `round-time-accounting.json`) and a receipt discipline for routes
(`route-probes/*.json`). That is a real 0→1 instrument delta, not a prose restatement.

But the predicate `ledger_checks_passed == 3 of 3` does **not** certify what the claim's title says it
certifies. It certifies that the L1's own JSON agrees with the L1's own JSON and with the presence of
files the L1 authored. I built a 48-seat wave in which **one seat vanishes entirely from
settled+dead and the counter still prints 3/3, exit 0** — the exact r50-1 defect class the condition
was written to close. I also built an **empty wave** (zero seats, zero seconds, `LOG.md` naming no
figure) that prints 3/3. Both survive the frozen L1 condition verbatim.

So: **instrument = capability; 3/3-as-wave-integrity-certificate = theater-capable.** The counter
faithfully implements the frozen conditions; the frozen L1 condition is too weak to carry the title.
Those are two separate defects and I keep them separate below.

Judge-facing: if the frozen predicate is honored as written, a future 3/3 should be recorded as
*internal consistency at a narrow aperture* — not as proof that the wave's seat accounting adds up.
If the predicate is meant to certify the title, it is currently falsifiable by X1 and X2 and should
be scored as an honest partial, with the corrections in §6 carried to round 52.

Measured staging note, so nothing is misread: at the named revision C1 is honestly **0/3, exit 1**
(the evidence set is untracked), so no false "met" has been recorded yet. The contract's C1 `after`
field ("3 of 3 at the measured commit … all committed") is a *prediction* at this revision and is
currently false; the only `after` measured so far is 0/3.

```
python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768c  -> 0/3 met=False exit 1
python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 007d66e4  -> 0/3 met=False exit 1
```

---

## 1. Axes named

| Axis | What it measures here | State after this review |
|---|---|---|
| **operability / capacity** | Is there a runnable artifact where none existed, that a non-author can execute against a foreign checkout? | **Improved, earned.** Absent at base; present and deterministic at tip. |
| **operability / fidelity** | Does the instrument reject *false* evidence, or only *missing* evidence? | **Not earned.** Rejects some falsehoods; certifies fabricated and empty waves. |
| **provenance / attribution** | Is each certified number traceable to a byte outside the certifier? | **Weak.** Only the seat-report *presence* is anchored in git; per-seat seconds are filesystem mtimes; receipts are self-authored. |
| **time-accounting integrity** | Are aggregate / dead / wall figures physically plausible? | **Not earned.** Negative wall clock passes; dead-seat duration-vs-reason clause is dead code against the real builder. |
| **route-deviation coverage** | Are deviations recorded where the schema says, or anywhere? | **Partly earned.** Real teeth on used-route receipts (B4/B5/B7); structured table ignored (X9). |
| **freshness (C2)** | Untouched by C1. | Control run only: `c51_quote_truth.py` → 8/8 met=True, rc 0. Separability holds (disjoint input sets). |

---

## 2. The case FOR capability acquisition (grounds, measured)

**2.1 The instrument did not exist at base.** `.ufo/waves/round-51` has **0** committed paths at
`007d66e4`; the counter itself is first committed at the tip (`git ls-tree` shows
`c51_wave_ledger.py`, `c51_quote_truth.py`). At base there was no way to mechanically falsify a
wave's seat accounting, no committed probe receipt anywhere, and the round-overrun figure lived in
prose (r50-1/2/3).

**2.2 It is a real instrument, not a wrapper.** 297 lines, `git show` + `json` + `datetime` only: no
network, no writes, no temp state, no clock dependence. Three runs at a fixed revision are
byte-identical (`md5 7db7a0a0172bd27366f1e39520d34414`, 308 bytes, rc 1 each). It runs against a bare
foreign repo — all my `/tmp` mutants were certified/refused by it without touching the lane.

**2.3 It has non-trivial, demonstrable bite.** These lies are caught (each a separate `/tmp` commit):

| Probe | Lie injected | Result |
|---|---|---|
| B1 | `settlement.spawn` 47 vs 1 payload seat | **L1 fail** — `spawn 47 != payload seats 1` |
| B2 | seat marked `report: true` but its `.md` uncommitted | **L1 fail** — `reports_written 1 != committed report files 0` + `seats marked with a report but no committed file: ['A']` |
| B3 | `startedAt/settledAt` unparsable | **L3 fail** — `wave timing does not carry a parsable startedAt/settledAt pair` |
| B4 | used route whose receipt is `ok:false` | **L2 fail** — 3 notes (not ok / used by a role / not recorded as deviation) |
| B5 | failing receipt with no `bodyExcerpt` | **L2 fail** — `carries no body excerpt` |
| B6 | wall 480s, `LOG.md` names no 480 | **L3 fail** — `LOG.md does not name the re-derived wall-clock figure 480` |
| B7 | counter retargeted at round 50's real evidence | **L2 fail** — `no committed probe receipt for used route devin/swe-2-max`, `… zai-coding-plan/glm-5.3-flash` |

B2 is the genuinely valuable one: it binds a claim to *committed* bytes rather than to the working
tree, which is the difference between a receipt and a note-to-self. B4/B5/B7 show L2 is a real check
against declared model bindings, not decoration.

**2.4 The real route evidence passes honestly.** Substituting the lane's actual `route-map.json` and
the two actual receipts into a consistent envelope yields 3/3 (T9). The used-route receipt is
well-typed (`httpStatus: 200`, `int`; `ok: true`, `bool`) with a provider body excerpt and a
`probedAt`; the 403 receipt carries its own excerpt. So the artifacts the L1 must commit are, so far,
of the right shape — the counter is not being fed junk.

**2.5 Credit where due on sequencing.** The evidence is *not* committed yet and the counter says so
(0/3). Nothing in this review found the counter claiming a pass it had not computed.

---

## 3. The case FOR instrumentation theater (counterexamples, all executed)

Each of the following is a `/tmp` git repo handed to the real counter. Every one printed
`C1 ledger 3/3 met=True` and exit 0.

**X1 — the vanished seat (the r50-1 defect class, alive).**
48 seats granted (`granted lane=kake wave=r51-w1 seats=48`), 48 in the payload, 47 reports committed,
`settled` = 47 entries, `dead` = [], `settled_count` 47, `spawn` 48. Seat `S47` is in neither list.
`L1` checks `settled_count + dead_count == len(seats)` — both sides of that equation are the L1's own
numbers, so it is satisfied at 47 == 47. Nothing ever compares `settled + dead` to `spawn`.
Result: **3/3, exit 0.** The seat accounting does not add up and the ledger certifies it.

**X2 — the empty wave.**
`tasks: []`, `spawn: 0`, `settled: []`, `dead: []`, all seconds 0, `startedAt == settledAt`,
`LOG.md` = `LOG: nothing happened.` Result: **3/3, exit 0.** A wave that never happened certifies.

**X3 — the fabricated dead seat.**
Payload of 2, plus `{"name":"GhostSeat","seconds":999999,"report":false,"reason":"crashed-alien-invasion"}`
with `timeout_seconds: 60`. `GhostSeat` is in no payload. 999999s = 11.6 days, 192× the timeout.
Result: **3/3, exit 0.** `check_l3` only branches on `reason.startswith("timeout-")` /
`"exit-"` (lines 230–235), so any other reason string — including one that does not exist in the
vocabulary — exempts the duration from every check.

**X4 — the double-counted seat, in the builder's own shape.**
`A` appears in `settled` (`report: true`) *and* in `dead` (`reason: "no-report"`, 480s).
L1 passes (`settled_count+dead_count == 2 == len(seats)`; the name sets still match because `reported`
only collects truthy reports). L3's dead-seat clause cannot fire: `"no-report"` matches neither prefix.
Result: **3/3, exit 0**, with 480s charged twice. This is not an exotic shape —
`build_wave_evidence.py` emits exactly `reason: "no-report"` and charges dead seats `seconds = wall`.

**X5 — zero wall clock.**
`startedAt == settledAt` → `wall = 0`. `check_l3` line 242: `if wall > 0 and str(wall) not in log_text`.
The `wall > 0` gate skips the LOG condition entirely. Result: **3/3 with a `LOG.md` that names no
figure at all.**

**X6 — time running backwards.**
`startedAt 00:08`, `settledAt 00:00`, `wall_clock_seconds: -480`, `LOG.md` = `no figures`.
`wall = -480`, `wall > 0` false → LOG skipped; accounting matches. Result: **3/3, exit 0.** A wave
whose clock runs backwards certifies. (Measured, not inferred.)

**X7 — the LOG substring leak, on the real file.**
The condition is `str(wall) not in log_text` — substring containment in a 169 386-byte committed
`LOG.md`. Measured against the actual committed `LOG.md`: **603 of 6 601** plausible wall clocks
(600–7200s) already occur as substrings (**9.1%**); 159 (**2.4%**) already occur as standalone
integers. Confirmed live: wall 480 authorized by a `LOG.md` containing only `total 14800 bytes moved`.
So for roughly one wall-clock value in eleven, the L3 LOG clause is satisfied by unrelated history.

**X8 — L2 vacuous pass.**
`{"roles":{"GhostRole":{}}}` with **zero** probe receipts and no `kimiModel` anywhere.
`used` is built only from truthy `kimiModel` values, so it is empty; an empty `used` set requires no
receipts. Result: **L2 pass, 3/3, exit 0.** "Every route the wave used has a committed probe receipt"
is satisfiable by declaring that no route was used.

**X9 — the structured deviation table is decorative; prose is the authority.**
On the lane's *real* route map, deleting the whole `"deviations": [...]` array still yields 3/3;
stripping only the alias from the roles' `probe` prose yields L2 fail (`not recorded as a deviation`).
`check_l2` never reads `route_map["deviations"]` (`grep -c "route_map.get"` = 1, for `roles`). Worse,
the actual test is `alias not in recorded`, a substring test over the concatenation of every role's
`probe` prose — so a prose sentence saying the route "was NOT used" satisfies "recorded as a
deviation". Confirmed with a failing `503` receipt for `fallback-model` whose only mention was
`"checked fallback-model only; it was NOT used"` → **3/3, exit 0**.

**X10 — the forged receipt.**
`{"alias":"forged","httpStatus":200,"ok":true}` — three fields, no `bodyExcerpt`, no `probedAt`, no
`endpoint`, no evidence a probe ever ran — satisfies "a committed probe receipt with an integer HTTP
status". Result: **3/3, exit 0.** Failing receipts need an excerpt; *passing* ones need nothing but
the word `true`, which is the asymmetry that matters, since only passing receipts are load-bearing
for `used` routes.

**X11 — `settlement.seats` is never read.**
A settlement whose `seats` list is `LIE1/LIE2/LIE3` against a payload of `A,B` yields **3/3**.
The one field that could carry an explicit seat roster is dead weight.

**X12 — "absent" and "broken" are indistinguishable.**
`--root /tmp` (not a repo) and `--revision deadbeef` both print
`settlement receipt absent at the measured revision`. `show()` discards `git`'s stderr and
return code and maps *any* failure to `None`. Fail-closed is the right direction, but the sentence
asserts a fact about a revision that was never read. Under load or a shallow/partial clone, a healthy
wave would be reported as missing evidence with no diagnostic.

**X13 — the instrument is single-use.**
`WAVE_DIR = ".ufo/waves/round-51"` is a module constant; argparse exposes only
`--root/--revision/--json`. Round 52 needs a new copy (the pattern is already visible: `c50_durable.py`,
`c50_quote_class.py`, `c51_*.py`), and the emitted JSON schema id stays `kake-r51-c1-wave-ledger-v1`
even when retargeted. What the lane acquired is a *per-round ritual script with real teeth*, not a
wave-evidence capability that generalizes. This is the single strongest structural argument for
"theater": the artifact that would make the next round cheaper does not exist.

**X14 — the real route evidence contains one synthetic deviation.**
The 403 receipt's own `note` reads "probed to exercise the failing-receipt path; no role is bound to
this route this wave". So r50-2's remediation ("route substitutions now carry committed receipts") is
exercised by a route that was deliberately probed, not by a substitution the wave needed. Honest and
disclosed, but L2's failing-receipt branch is being demonstrated rather than earned this wave.

---

## 4. The strongest counter-argument, stated fairly

The strongest case *against my verdict* — and it is genuinely strong:

> The conditions were frozen before scoring, and the counter implements them exactly. L1 says
> "the committed seat-report count equals the settlement's `reports_written`, the settlement's spawn
> equals the payload's seat count, and every seat marked as having a report has exactly one committed
> report file". The counter checks precisely those three things. X1 does not exploit a bug; it
> exploits the fact that the *frozen condition* never promised `settled+dead == spawn`. A critic who
> demands a check the claim never made is scoring a different claim, retroactively — exactly the
> "premature saturation" failure the role is supposed to avoid. Moreover: the L1 is one actor writing
> both the evidence and the counter, but that is unavoidable in a single-wave lane; the discipline that
> matters is that the counter is *committed, deterministic, byte-reading and externally runnable*, so
> any future reader can add the missing three lines and re-run them against the same revision. That is
> what a receipt is. Finally, the strongest place theater would show is a false pass being *scored* —
> and at the measured revision the honest answer is 0/3, exit 1. Nothing has been scored yet.

I accept most of this, and it changes the shape of the verdict rather than its substance:

- X1/X2/X4 are **condition-level** defects. They do not show the code is wrong; they show the frozen
  L1 condition is too weak for the claim's title ("re-derives the round's own **seat accounting**").
  A judge comparing title to condition should side with the code and fault the wording.
- X6/X7/X12/X13 **are counter-level** defects: `wall > 0`, substring containment, silent `git`
  failure, hardcoded wave dir. These are bugs in the artifact under review, not in the contract, and
  they are cheap to fix.
- The "nothing scored yet" point is correct and I do not treat the current 0/3 as evidence of
  dishonesty — but it also means the `after` clause in the frozen contract is presently false, and a
  judge must not read `"after": "3 of 3 at the measured commit"` as an observation.

So the fair reading is not "theater" as fraud. It is: **a real falsifier with a narrow aperture,
marketed at a wider aperture than its own conditions bought.** The gap is measurable (X1 is 3/3), and
it is exactly the gap that r50-1 was routed to close.

---

## 5. Impacted axes and frontier step

- **operability** (the claim's own axis): capacity improved and earned; fidelity not earned. At a
  declared 10/10 saturation line the obligation is to *hold*, not to advance; a 3/3 that certifies an
  empty wave does not hold the line at the strength the line is declared at.
- **provenance/attribution**: the only external anchor for the seat *set* is report *presence* in git
  (`wave-grant.txt` is checked only for the substring `granted lane=kake`; its `seats=48` is never
  read, so the grant does not anchor the count). Per-seat `seconds`
  are mtimes — reproducible only inside the L1's working tree, trivially altered with `touch`, and not
  recoverable from the commit. "Re-derived from committed bytes" is true of the arithmetic and false
  of the inputs.
- **time-accounting integrity**: negative and zero wall clocks certify (X5, X6); dead-seat
  duration-vs-reason is dead code against the builder's only reason string (X3, X4).
- **route-deviation coverage**: real teeth on declared bindings (B4/B5/B7), but the structured
  `deviations` table is unused and prose substrings are authoritative (X9).
- **freshness**: untouched. C2 control: 8/8 met=True, rc 0; input sets are disjoint from C1's
  (registry/lesson/sources/mirror vs wave-dir + `LOG.md`). Separability claim holds.
- **frontier step**: this wave's claims are a *hold* at saturation, so nothing here advances the
  frontier. The honest frontier statement is "instrument added (real), certificate enlarged (not yet)".

---

## 6. Smallest safe corrections

Ordered by (defects closed / lines changed). None of these may be applied to the frozen round-51
conditions mid-round; they are the shape a round-52 ledger should take, plus the one diagnostic fix
that is safe to apply to counter code without changing any condition's meaning.

1. **L1 closes the seat-accounting hole (3 lines, no new inputs).** In `check_l1`, after the existing
   notes:
   - `if settlement.get("settled_count",0) + settlement.get("dead_count",0) != spawn:` → note
     "accounted seats != spawn" (kills X1);
   - `if sorted(n for e in seats for n in [e["name"]]) != sorted(t["name"] for t in tasks):` → note
     the missing/extra seat names (kills X1, X4, X11's irrelevance by making the roster load-bearing);
   - `if spawn != len(tasks) or spawn <= 0:` → note (kills X2 unless the grant also says zero).
2. **Anchor spawn to the grant.** Parse `seats=(\d+)` out of `wave-grant.txt` and require it equals
   `len(tasks)` and `settlement.spawn`. The grant is the one document the L1 does not author alone;
   today it is checked only for the substring `granted lane=kake`.
3. **L2 reads `deviations`, not prose** (`check_l2`, line 190–196). Require each failing receipt's
   alias to appear as a `deviations[].route` with matching `receipt` path and `httpStatus`. Kills X9
   and removes the "it was NOT used" prose exploit. Optionally require `bodyExcerpt` and `probedAt`
   on *passing* receipts too (kills X10).
4. **L3 wall clock must be positive and the LOG match must be token-exact.** Replace
   `if wall > 0 and str(wall) not in log_text` with: fail when `wall <= 0`; then match
   `re.search(rf"(?<![0-9.]){wall}(?![0-9.])", log_text)`. Kills X5, X6 and cuts X7 from 9.1% to 2.4%.
5. **L3 dead-seat reasons fail closed.** Replace the two `startswith` branches with an allowed-
   vocabulary check (`timeout-*`, `exit-*`, `no-report`) and, for `no-report`, require
   `secs == wall`. Unknown reasons must fail, not skip. Kills X3/X4.
6. **`show()` must not launder `git` failure into absence.** Return stderr/rc and emit a distinct
   `"git show failed: <stderr>"` note. Kills X12's false diagnosis (this is the one fix safe to apply
   to counter code without touching a condition).
7. **Make the instrument reusable.** Replace the `WAVE_DIR` constant with `--wave` (default
   `round-51`) and derive the schema id from the wave. This is the difference between a capability and
   a per-round ritual (X13).

If only one change is authorized: **#1**, three lines, no new inputs, and it is the one that closes
the exact defect class (r50-1) the claim was routed to close.

---

## 7. Evidence index (all executed; commands verbatim)

`/tmp` paths below are disposable scratch. Each row records its injected lie and the counter's exact
output, so any row is rebuildable from the row text alone if the directory is swept — no row depends on
a surviving artifact. (No reference in this report points at `round-35/scratch/` or its relocated
`round-35/scratch-evidence/`; every input here is round-51 evidence or inlined output.)

| ID | Where | Command | Output |
|---|---|---|---|
| tip | lane | `c51_wave_ledger.py --root . --revision 9d13768c` | `0/3 met=False`, exit 1; L1/L2/L3 all "absent at the measured revision" |
| base | lane | same, `--revision 007d66e4` | `0/3 met=False`, exit 1 (identical text) |
| tree | lane | `git ls-tree -r --name-only <rev> -- .ufo/waves/round-51` | base 0 paths; tip 158 paths |
| det | lane | 3× same command, separate kernel | identical 308-byte output, `md5 7db7a0a0172bd27366f1e39520d34414` |
| X1 | `/tmp/c51t12` | 48 grant/payload, 47 accounted | **3/3, exit 0** |
| X2 | `/tmp/c51t6` | empty wave, zero seconds | **3/3, exit 0** |
| X3 | `/tmp/c51mut` | `GhostSeat` 999999s, `reason: crashed-alien-invasion` | **3/3, exit 0** |
| X4 | `/tmp/c51dup2` | same seat settled+dead, `reason: no-report` | **3/3, exit 0** |
| X5/X6 | `/tmp/c51mut`, `/tmp/c51neg` | wall 0; wall −480 | **3/3, exit 0** each, LOG figure never read |
| X7 | lane `LOG.md` | substring census over 600..7200 | 603/6601 (9.1%) substrings; 159 (2.4%) standalone |
| X8 | `/tmp/c51mut` | `{"roles":{"GhostRole":{}}}`, 0 receipts | **3/3, exit 0** |
| X9 | `/tmp/c51t5`, `/tmp/c51t9` | prose "was NOT used"; drop `deviations` | **3/3**; drop deviations **3/3**; strip prose **L2 fail** |
| X10 | `/tmp/c51t11` | `{"alias":"forged","httpStatus":200,"ok":true}` | **3/3, exit 0** |
| X11 | `/tmp/c51t7` | `seats` = `LIE1/LIE2/LIE3` | **3/3, exit 0** |
| X12 | `/tmp` root; `--revision deadbeef` | | `absent at the measured revision` |
| X13 | `/tmp/c51gen/round-49,round-50` | counter with `WAVE_DIR` swapped | both 0/3; round-50 L2 correctly flags 2 used routes with 0 receipts; L1 fails (no dispatch payload kept in round 50) |
| B1–B7 | `/tmp/c51b_*`, `/tmp/c51t2` | the six bite probes | L1/L2/L3 fail with the notes quoted in §2.3 |
| C2 control | lane | `c51_quote_truth.py --root . --revision 9d13768c` | `8/8 met=True`, exit 0 |

**Not run, and why:** `build_wave_evidence.py` was read but not executed — it writes into the lane
(forbidden by my bounds) and requires `.ufo/waves/round-51/settled-utc.txt`, which does not exist yet.
No tool was installed or upgraded (nothing needed; `python3`, `git` sufficed), so there is no
tool/version/channel entry to record.

**Incident, disclosed:** one earlier determinism measurement appeared non-deterministic
(`/tmp/a2` = 18 bytes of another command's output). That was shared-session shell interference, not
the counter: the redirects were clobbered by a concurrent command in the session shell. Re-measured in
an isolated kernel, three runs are byte-identical. I am recording it because I nearly reported a false
finding, and the honest record is that the first measurement failed for an infrastructure reason.
