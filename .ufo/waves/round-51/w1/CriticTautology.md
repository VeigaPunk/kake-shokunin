# CriticTautology — is C1 anything other than the L1 certifying its own typing?

Scope: C1 only (operability). C2 is another seat's ground. Read-only; all scratch under `/tmp`.
Revision under judgement: lane tip `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (base `007d66e4`).

## 1. Verdict up front

- **At the measured revision C1 is 0/3, exit 1** — measured, not inferred:
  `python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768c` prints
  `C1 ledger 0/3 met=False`, `L1 FAIL: settlement receipt absent`, `L2 FAIL: route map absent`,
  `L3 FAIL: settlement receipt absent`. So nothing is certified yet; the claim is unverified, and
  the wave evidence is to be authored **after** the wave by the same seat that owns the claim.
- **Answer to the assigned question: no check in the ledger is independent of a number the L1
  typed.** Every sub-clause compares either one L1-authored file against another, or
  an L1-authored file against arithmetic replays of itself. The single input not produced by the
  L1's hand — the set of paths `git ls-tree` reports under `w1/` — enters only as a *file count*,
  is satisfiable with zero-byte files, and the settlement number it is compared to is derived from
  the same `isfile` test by the same L1 script. Empty evidence therefore satisfies it.
- **Evidence of the tautology (executed, not argued):** a fabricated repo with one 0-byte report,
  one hand-written 200, one 500 marked `ok:true`, and a wall clock typed as two timestamps that are
  0 s apart in git **scores `3/3 met=True`, exit 0** under the committed counter.

## 2. Who writes each figure

The counter reads committed bytes, but those bytes were produced like this (all confirmed by
reading the uncommitted producer `build_wave_evidence.py` and the committed receipt directory):

| Figure | Source | Author |
|---|---|---|
| `w51-taskcall.json` tasks / `counts.spawn` | `make_spec_w1.py` (L1 tool) | L1 |
| `settlement.spawn` | copied from `payload.counts.spawn` | L1 (copy) |
| `settled_count` + `dead_count` | `len()` of the builder's own two lists | L1 (identity) |
| `reports_written` | `#{[isfile(w1/<name>.md)]}` at build time | L1 (`isfile`, same dir the counter counts) |
| `settlement.settled[].seconds` | `mtime(w1/<name>.md)` − `wave-start-utc.txt` | L1 (typed stamp + worktree mtime) |
| `settlement.dead[].seconds` | `wall` for every dead seat | L1 (fabricated, identical for all dead) |
| `settlement.dead[].reason` | literal `"no-report"` | L1 |
| `settlement.timeout_seconds` | `KAKE_R51_TIMEOUT` env, default 3600 | L1 (unrecorded env) |
| `settlement[].model` | literal `"commandcode/deepseek/deepseek-v4.1-flash"` | L1 (hardcoded, never compared to route map) |
| `wave-timing.startedAt/settledAt` | `wave-start-utc.txt`, `settled-utc.txt` | **L1, typed by hand** |
| `round-time-accounting.*` | recomputed by the same builder from the same settlement | L1 (same arithmetic) |
| `route-map.roles[].kimiModel` | L1 | L1 |
| `route-probes/*.json` `alias/httpStatus/ok/bodyExcerpt` | **no committed script writes these** | L1, typed into JSON |
| `w1/*.md` report **contents** | 48 seat agents | external — **and never read by the counter** |

Two provenance facts that matter:

1. `grep -rn "route-probes" --include=*.py --include=*.sh .ufo/waves/round-51/` matches only
   `c51_wave_ledger.py:49` (its own constant). `build_wave_evidence.py` does not create receipts.
   The receipts are hand-authored JSON.
2. The per-seat `seconds` the ledger "re-derives" are not in git at all: they are
   `st_mtime` of worktree files minus a timestamp the L1 typed into a text file. A reader can
   re-sum the integers; a reader cannot recompute one of them. The contract's phrasing
   ("re-derivable from the committed settlement and wave-timing bytes") is true only of the sums.

## 3. Counterexamples (all executed; fixtures under `/tmp/r51forge`, `/tmp/r51B`, `/tmp/r51D`, `/tmp/r51E`, `/tmp/r51F`)

The fixtures are throwaway `/tmp` repos and may be swept; nothing below depends on them
surviving. Every fixture's content and the counter's exact output are transcribed here, and each
fixture is rebuildable from this section with `git init` plus the quoted files.

### 3.1 A wholly fictitious wave scores 3/3

`/tmp/r51forge` is a fresh `git init` containing only: one task name, a settlement with
`spawn:1`, one settled seat `seconds:5`, one dead seat `reason:"no-report"`, `seconds:60`,
`reports_written:1`; an **empty** `w1/Seat1.md`; a route map binding `critic → fake/model` and
`sentinel` to a receipt with `{"httpStatus":500,"ok":true}`; receipts including a **failing
receipt for a used alias** (`z_fail.json`, `500`, `ok:false`, `bodyExcerpt:"quota expired"`);
timing `00:00:00 → 00:01:00`; accounting `60/65/60`; `LOG.md: "the wave wall clock was 60 seconds"`.

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root /tmp/r51forge --revision HEAD
C1 ledger 3/3 met=True  (met: ledger_checks_passed == 3 of 3)
  L1 pass
  L2 pass
  L3 pass
exit=0
```

The repo's only commit is 0 s from the claimed 60 s wall clock:

```
commit span = 0 s   claimed wall = 60 s
```

So: zero seats ran, no model was called, the only report is 0 bytes (`wc -c` → `0`), a role is
bound to a 500, and a committed failing receipt for a used route is ignored. `3/3`.

### 3.2 The verdict depends on the filename sort order

Same bytes, one rename — `z_fail.json` → `0_fail.json`:

```
$ python3 -B …c51_wave_ledger.py --root /tmp/r51B --revision HEAD
C1 ledger 2/3 met=False
  L2 FAIL
    - route fake/model was used but its receipt is not ok
    - failing route fake/model was used by a role
exit=1
```

`receipts.setdefault(alias, receipt)` keeps the **first** receipt in `git ls-tree` order and
silently discards the rest. Same evidence, opposite verdict; the *passing* direction is the one
that drops a committed failing receipt. `setdefault` is the whole of L2's duplicate handling.

### 3.3 The `ok` boolean is unbound to `httpStatus`

`broken.json` = `{"alias":"broken/model","httpStatus":500,"ok":true}`, bound to a role, is never
noted: the used-route path only demands `isinstance(status,int)` and `ok is True`. A 500 route is
certified as a live route. (`L2` reads `ok`; it never computes `ok` from the status.)

### 3.4 L3's LOG clause is a substring, and is skipped when the wall clock is 0

```
$ … --root /tmp/r51D   # startedAt == settledAt, LOG.md names no figure
C1 ledger 3/3 met=True
$ … --root /tmp/r51F   # wall 48 s, LOG.md = "A 48-seat batch was dispatched; the wall clock figure is not stated anywhere."
C1 ledger 3/3 met=True
```

`if wall > 0 and str(wall) not in log_text` — zero disables the check, and any incidental
occurrence of the decimal string ("48 seats") satisfies it. The contract clause "LOG.md names the
wall-clock figure" is not implemented as written.

### 3.5 The dead-seat rule is keyword-gated, and the only honest reason is exempt

```
$ … --root /tmp/r51E   # reason changed from "no-report" to "timed out"
C1 ledger 3/3 met=True
```

The duration rule fires only on `reason.startswith("timeout-")` or `("exit-")`. The builder's sole
dead-seat reason is `"no-report"`, which matches neither, so "every dead seat's duration matches
its recorded reason" is vacuously true for every dead seat this round can produce — while
`dead.seconds` is simply set equal to the wall clock for each of them, making
`dead_seat_seconds == wall × dead_count` an identity rather than a measurement.

## 4. The real evidence already contradicts itself — and the counter cannot see it

The route the wave actually binds (all ten roles → one alias) has two committed artifacts in the
same directory that disagree:

- `route-probes/commandcode_deepseek-v4.1-flash.json`: `httpStatus:200`, `ok:true`,
  `endpoint:"https://api.commandcode.ai/"` — the provider's **edge root**, not a completion call —
  plus a `detail` string asserting the completion leg "answered PONG via
  `omp -p --mode json --model @m_flash`".
- `route-probes/commandcode_deepseek_deepseek-v4.1-flash.txt` (same alias, committed, unread by
  the ledger): `error: failed to run prompt: Model "commandcode/deepseek/deepseek-v4.1-flash" is
  not configured in config.toml.` / `# exit=1`.

No committed artifact captures the `omp -p` run that the `detail` prose claims; the positive
attestation for the used route exists only as a sentence. The counter reads `*.json` only, so the
`exit=1` transcript and every other `.txt` (including `devin/swe-2-max` exit 0 and
`zai-coding-plan/glm-5.3-flash` exit 0 — routes **no role uses**) are invisible to it.

Even the one genuinely measured failure is typed, not captured: the `xai-oauth` receipt's
`bodyExcerpt` is not a raw substring of its own transcript — it is the transcript's two leading
lines reflowed with a space and truncated mid-word at exactly 200 chars:

```
excerpt len 200, ends repr ' upgrade at https://grok.'
'kimi version 2.3.1 error: failed to run prompt: …' in transcript -> False
'failed to run prompt: provider.auth_error: 403 …'    in transcript -> True
'kimi version 2.3.1\nerror: failed to run prompt: …'  in transcript -> True
```

So the 403 is real, but the field the receipt presents as a body excerpt is a hand-edit. L2's "a
failing receipt carries a body excerpt" is satisfied by any non-empty string.

Also unused but free: `route-map.json` has a structured `deviations` array (one entry, the 403).
L2 ignores it and instead does a substring test against role `probe` prose, so a proper deviation
record and a passing mention in a sentence are equally acceptable.

## 5. Clause-by-clause: which side of each comparison is external

L1 — `spawn` vs payload seat count: identity (the builder copies it). `settled+dead` vs entries:
identity. `reports_written` vs committed report count: **tree-backed, but both sides come from the
same `isfile` test and an empty file passes**; no report byte is ever read, no name/sha/nonzero
size is required. `reported == committed` names: identity modulo files added between build and
commit.

L2 — receipt presence: two L1 artifacts agreeing on a string. Status integer: L1-typed. `ok`: L1
boolean, unbound to status. Excerpt: L1 prose. Deviation: substring of L1 prose, with a duplicate-
dropping `setdefault` that can discard the failing receipt entirely.

L3 — aggregate/dead/wall vs accounting: the same arithmetic in a different file. Wall vs LOG: a
decimal substring, disabled at 0. Dead duration vs reason: keyword-gated, the real reason exempt.
Grant line: a static string.

Net: **no sub-clause compares two independently produced quantities.** The one external
thing in the whole loop — 48 agents' report bytes — is counted by name and never read.

## 6. Impacted axes

- `operability` (C1): the whole of this report. The claim as frozen ("re-derives … from committed
  bytes") is stronger than the instrument: it re-sums L1 integers and re-counts L1 file names.
- `freshness` (C2): untouched by this seat; no claim here.

## 7. Smallest safe corrections, in cost order

1. **Anchor the wall clock to a timestamp git wrote** (the cheapest genuinely independent
   cross-check, one command, no new artifacts, no new files):
   require `wall_clock_seconds <= ct(evidence commit) − ct(commit that first added
   w51-taskcall.json)`, the second obtainable as
   `git log --diff-filter=A --format=%ct -1 <rev> -- .ufo/waves/round-51/w51-taskcall.json`.
   Against the forgery this is `60 <= 0` → fails, and it needs the payload committed *before*
   dispatch (today it is untracked, so the anchor is not yet available). It bounds inflation only;
   that is the direction a self-attesting author has an incentive to abuse.
2. **L2 coherence, 2 lines:** drop `ok` as an independent field — require
   `ok == (200 <= httpStatus < 300)`, and make a receipt's `leg` part of its identity so a
   duplicate `(alias, leg)` is a failure rather than a silent first-wins.
3. **L2's positive leg:** the receipt must name a re-runnable argv and the committed path of its
   captured stdout/exit (as the `.txt` files already are), and the excerpt must be a raw substring
   of that capture. Then the 200-vs-`exit=1` contradiction above becomes a red result instead of an
   invisible one.
4. **L1, 2 lines:** require each `report:true` seat's file to be non-empty and to contain its own
   seat name (or a sha256 pinned in the settlement). Today `touch w1/Seat1.md` certifies a seat.
5. **L3:** require `wall > 0` unconditionally; match LOG on a labelled pattern (e.g.
   `wall clock` within the same line as the figure), not a bare decimal; close the reason
   vocabulary and parse the number out of `timeout-<n>` / `exit-<n>` instead of exempting
   everything else.
6. **Free consistency check the ledger already has both sides for:** every
   `settlement.settled[].model` must equal its role's `route-map.roles[role].kimiModel`. The
   builder hardcodes one string for all 48 seats; nothing compares it.

No tool installs or upgrades were made for this review; no file in the lane was written except
this report.

## Appendix — the section 3.1 fixture, as a recipe

The report body is the durable evidence locus; the `/tmp` repos are a convenience copy. Running
this block in an empty directory and then the committed counter reproduces `3/3 met=True`, exit 0,
with no surviving scratch of mine. (This block is the fixture, not a measurement: it is exactly
the set of typed files that should *not* convince a reader.)

```sh
set -e
git init -q .; git config user.email a@b; git config user.name forged
W=.ufo/waves/round-51; mkdir -p "$W/w1" "$W/route-probes"
cat > "$W/w51-taskcall.json" <<'J'
{"taskCall":{"tasks":[{"name":"Seat1","role":"critic"}]},"counts":{"spawn":1}}
J
cat > "$W/settlement.json" <<'J'
{"schema":"kake-r51-settlement-v1","spawn":1,"timeout_seconds":3600,
 "settled":[{"name":"Seat1","role":"critic","exit":0,"seconds":5,"report":true}],
 "dead":[{"name":"Ghost","role":"sentinel","exit":-1,"seconds":60,"report":false,"reason":"no-report"}],
 "settled_count":1,"dead_count":1,"reports_written":1}
J
: > "$W/w1/Seat1.md"
cat > "$W/route-map.json" <<'J'
{"roles":{
 "critic":{"kimiModel":"fake/model","probe":"fake/model answered (exit 0); ghost/model unreachable, deviation recorded"},
 "sentinel":{"kimiModel":"broken/model","probe":"broken/model answered (exit 0)"}}}
J
cat > "$W/route-probes/a_ok.json" <<'J'
{"alias":"fake/model","httpStatus":200,"ok":true}
J
cat > "$W/route-probes/z_fail.json" <<'J'
{"alias":"fake/model","httpStatus":500,"ok":false,"bodyExcerpt":"quota expired"}
J
cat > "$W/route-probes/broken.json" <<'J'
{"alias":"broken/model","httpStatus":500,"ok":true}
J
cat > "$W/route-probes/ghost.json" <<'J'
{"alias":"ghost/model","httpStatus":503,"ok":false,"bodyExcerpt":"upstream unavailable"}
J
cat > "$W/wave-timing.json" <<'J'
{"startedAt":"2026-10-25T00:00:00+00:00","settledAt":"2026-10-25T00:01:00+00:00"}
J
cat > "$W/round-time-accounting.json" <<'J'
{"wall_clock_seconds":60,"aggregate_seat_seconds":65,"dead_seat_seconds":60}
J
echo 'granted lane=kake wave=r51-w1 seats=1' > "$W/wave-grant.txt"
echo 'the wave wall clock was 60 seconds' > LOG.md
git add -A; git commit -qm forged
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/c51_wave_ledger.py \
  --root . --revision HEAD
```

What the block deliberately contains, and what the ledger accepts: a 0-byte seat report; a role
bound to `broken/model` at `httpStatus:500` with `ok:true`; a committed `500`/`ok:false` receipt
for the used alias `fake/model` (`z_fail.json`) that the ledger never sees because `a_ok.json`
sorts first; a dead seat whose reason is `no-report` and whose duration equals the wall clock;
and a 60 s wall clock produced only by two literals. Recorded output on a rebuilt copy of this
block: `C1 ledger 3/3 met=True`, `L1 pass`, `L2 pass`, `L3 pass`, `exit=0`.
