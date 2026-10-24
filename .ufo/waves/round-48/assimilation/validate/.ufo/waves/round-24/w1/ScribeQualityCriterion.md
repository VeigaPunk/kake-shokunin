# ScribeQualityCriterion — round 24 (w1)

Author-side scribe. Not an independent admission; no promotion is claimed. Lane read-only: this file is the only write. Observed 2026-10-21 ~08:43 -03. Lane HEAD observed: `f7de3ab4e9f030a15a857a5a08631bd8e690f436` (clean apart from untracked `.ufo/waves/round-24/`). Scratch (probe outputs, not durable evidence): `/tmp/kake-r24-ScribeQualityCriterion-TFN6`. Each probe below is reproduced verbatim in Appendices A–D so the report does not depend on that tmpfs path.

## Verdict

Both gaps are real at the base revision and both drafted criteria are below. Neither is appended to `corpus/QUALITY.md` (L1 appends).

1. **Timestamp criterion (operability, C2 axis):** the round-23 replay runners compare the date prefix lexically. In-process runs accept 6 of 7 malformed-or-future timestamps; the 7th (`2026-02-30`) is rejected only because it sorts before `2026-10-21`. `served()` raises on a non-string `contentType`.
2. **Pin re-arm criterion (freshness, C1 axis):** the four recovered `~/Projects/ds4cc-marketplace*` tokens remain in `pins.pathsMissSet`. The sweep does not fail on them, so an annotated target that reappears and then disappears again stays at exit 0 while pinned (hermetic run). Only a set-equality probe catches this.
3. **Restoration-note criterion (freshness):** the sweep's default annotation window (not strict) marks every token on a citing line when any ±2 window line carries an absence word, so restoration wording must be free of that vocabulary.

Preconditions before admission (L1): land the named probes (none exists in the lane at `f7de3ab`), add a tier-A RFC 3339 row to `corpus/SOURCES.md` (absent; only RFC 9110 rows exist), and in the C1 reconciliation commit remove the four recovered tokens from `pins.pathsMissSet` (do not re-pin them).

## Draft criteria (for L1 to append; NOT written to the lane)

Destination: end of `corpus/QUALITY.md` (file is 154 lines; append after line 154, after a blank line). Shape follows the round-22/23 sections: a `## … — round N` heading, a grounding line, and bullets, each with a `Fails if` predicate that names a probe and an exit code. No `~/` or `/home/vgpnk/` path is written in the draft text, so the sweep's citation scan adds no new cite.

````markdown

## Receipt grammar and absence re-arm — round 24

Grounding: `.ufo/waves/round-24/w1/ScribeQualityCriterion.md` (observations and probes, Appendices A–D); RFC 3339 §5.6 and §5.7 (row to be added to `corpus/SOURCES.md`); round-23 `measure_c1.py:55`, `measure_c2.py:37-39,56`; `scripts/freshness-sweep.mjs:122,324-334,477-480,1007`.

- A receipt timestamp (`observedAt`, `fetchedAt`) is admitted only if it matches the RFC 3339 §5.6 `date-time` grammar as a whole string (anchored; `T`/`t` and `Z`/`z` allowed; a numeric offset is required), names a real calendar date with hour at most 23 and no leap second, and denotes an instant in the closed interval [round-open instant, committer time of the measured revision] after offset normalization. A prefix or lexical comparison of the date part, `datetime.fromisoformat` alone (it accepts `2026-10-21` and `20261021`), and an unbounded future date are not the check. Fails if `python3 scripts/receipt_replay.py --root . --revision <commit>` exits 0 on any frozen timestamp case marked `expect: reject` (Appendix A vectors are the candidate cases).
- An absence pin is re-armed when its target is observed present: the token leaves `pins.pathsMissSet` in the commit that records the observation, so a later disappearance is a first-seen miss. A stale pin keeps the sweep at exit 0 for an annotated target that disappears again, so the sweep's own exit code is not the check. Fails if `python3 .ufo/waves/round-24/rearm_probe.py <sweep.json>` exits 1, where `<sweep.json>` is the output of `node scripts/freshness-sweep.mjs --section=paths --json --offline` (set equality of `pins.pathsMissSet` and `sections.paths.missSet`).
- A restoration correction for a recovered target starts with `*[r24 restoration 2026-10-21:` (or `<!-- r24 restoration 2026-10-21:` inside table rows or code), names what was observed present, says which part of the earlier line stays historical or unverified, and contains none of the words in the sweep's absence vocabulary (`scripts/freshness-sweep.mjs:122`), because the default ±2-line window would annotate neighbouring cites with it. Fails if `node .ufo/waves/round-24/restoration_vocab_probe.mjs <file>` exits 1 on the appended text.
````

Probe placement: the probes in Appendices A–C are not in the lane. L1 must land them at the paths named above (or the criteria must be reworded to the landed paths) before the criteria are admitted.

## Findings

### F1 — P1 — round-23 timestamp checks are prefix comparisons; malformed and future values pass (operability, C2)

- Impacted claim: C2 "after" (rejects every frozen malformed case, exit 1 or 2, no traceback) and draft criterion 1.
- Exact command (scratch, in-process; `sys.dont_write_bytecode = True`; each row calls the round-23 function `check_unit` / `check` with injected `git show` bytes; the lane is not written):
  `measure_c1.check_unit(".", "HEAD", unit)` with `observedAt` varied; `measure_c2.check(".", "HEAD", b"", surface)` with `fetchedAt` varied (status 404 not-served fixture).
- Exact observed output (C1, `observedAt`):
  ```
  C1 observedAt='2026-10-21T12:00:00Z'       accepted=True  | control: valid, in window
  C1 observedAt='2026-10-20T23:59:59Z'       accepted=False | control: before round open -> must reject
  C1 observedAt='not-a-date'                 accepted=True  | malformed, lexically > '2026-10-21'
  C1 observedAt='2026-10-21zz'               accepted=True  | malformed suffix
  C1 observedAt='2026-13-45T99:99:99Z'       accepted=True  | out-of-range fields, RFC 3339 invalid
  C1 observedAt='2026-02-30T00:00:00Z'       accepted=False | impossible calendar date
  C1 observedAt='2026-10-21T12:00:00'        accepted=True  | no offset (RFC 3339 requires one)
  C1 observedAt='2099-01-01T00:00:00Z'       accepted=True  | future, beyond lane HEAD commit time
  C1 observedAt='2026-10-21T23:00:00Z'       accepted=True  | future relative to commit 2026-10-21T09:00:18Z
  ```
  (`2026-02-30` is rejected only because `"2026-02-30"[:10] < "2026-10-21"`; it is not caught by parsing.)
- Exact observed output (C2, `fetchedAt`):
  ```
  C2 fetchedAt='2026-10-21T12:00:00Z'     accepted=True  verdict=not-served problems=[]
  C2 fetchedAt='2026-10-20T23:59:59Z'     accepted=False verdict=not-served problems=['fetchedAt missing or before 2026-10-21']
  C2 fetchedAt='not-a-date'               accepted=True  verdict=not-served problems=[]
  C2 fetchedAt='2099-01-01T00:00:00Z'     accepted=True  verdict=not-served problems=[]
  C2 fetchedAt='2026-10-21zz'             accepted=True  verdict=not-served problems=[]
  ```
- Source: `.ufo/waves/round-23/measure_c1.py:55` (`receipt["observedAt"][:10] < "2026-10-21"`); `.ufo/waves/round-23/measure_c2.py:56` (`fetchedAt[:10] < "2026-10-21"`).
- Smallest fix: in the maintained `scripts/receipt_replay.py`, replace the prefix test with the Appendix A admit rule (anchored RFC 3339 grammar, calendar validation, instant bounds). Leave the round-23 runners byte-intact.

### F2 — P1 — `served()` raises on a non-string `contentType`; the replay counter has no guard (operability, C2)

- Impacted claim: C2 "after" (no traceback on malformed input); draft criterion 1 scope.
- Exact command (scratch, in-process): `measure_c2.served({"status": 200, "contentType": X, "error": None, "truncated": False})`.
- Exact observed output:
  ```
  C2 served(contentType=5) -> UNCAUGHT AttributeError: 'int' object has no attribute 'split'
  C2 served(contentType=['text/html']) -> UNCAUGHT AttributeError: 'list' object has no attribute 'split'
  C2 served(contentType={'a': 1}) -> UNCAUGHT AttributeError: 'dict' object has no attribute 'split'
  C2 served(contentType='text/html; charset=utf-8') -> True
  ```
- Source: `.ufo/waves/round-23/measure_c2.py:37-39` (`ctype = fetch.get("contentType") or ""` then `ctype.split(...)`). The guard exists only on the producer: `scripts/live_snapshot.py:173` (`raise ValueError("snapshot contentType must be a string or null")`). `grep` finds no `contentType` type check in `measure_c2.py`.
- Exit status of `main()` on this input was not run. [INFERENCE] an uncaught exception ends the process with a traceback and status 1, which is the traceback case C2 forbids.
- Smallest fix: in `receipt_replay.py`, reject any `contentType` that is neither a string nor null, with exit 2 and the producer's diagnostic wording, before `served()` is called.

### F3 — P2 — `datetime.fromisoformat` is not the grammar; using it as the fix would still accept malformed input (operability trap)

- Impacted claim: any replacement of the prefix test that uses the standard library parser.
- Exact command: `dt.datetime.fromisoformat(s.replace("Z", "+00:00"))` on the listed strings (Python 3.14.8 on this host).
- Exact observed output:
  ```
  fromisoformat '2026-10-21'             -> accepted RFC3339-regex-match=False
  fromisoformat '20261021'               -> accepted RFC3339-regex-match=False
  fromisoformat '2026-10-21 12:00:00Z'   -> accepted RFC3339-regex-match=True
  fromisoformat '2026-02-30T00:00:00Z'   -> rejected RFC3339-regex-match=True
  fromisoformat '2026-10-21T12:00:00'    -> accepted RFC3339-regex-match=False
  ```
- Smallest fix: anchor the RFC 3339 §5.6 regex first; use the datetime constructor only for calendar validation; never accept on the parser alone. The space separator is allowed by the RFC NOTE but rejected by this draft's policy (stated in Appendix A).

### F4 — P1 — recovered tokens stay pinned; the sweep's exit code does not catch a stale pin (freshness, C1)

- Impacted claim: C1 "after" (`pins.pathsMissSet` equals the observed missSet) and draft criterion 2.
- Exact command: `node scripts/freshness-sweep.mjs --section=paths --json --offline > $S/sweep-paths.json` (lane root, read-only).
- Exact observed output (stdout reasons and counts):
  ```
  code 1 complete False reasons ['§paths: 3 unannotated miss · 12 NOT in pins.pathsMissSet']
  counts {'resolve': 19, 'declaredAbsent': 60, 'declaredAbsentIndirect': 4, 'drift': 3, 'unresolved': 10, 'newDrift': 0, 'newMissing': 12}
  setDelta.recovered ['~/Projects/ds4cc-marketplace', '~/Projects/ds4cc-marketplace/CNAME', '~/Projects/ds4cc-marketplace/burnerchrome', '~/Projects/ds4cc-marketplace/speedrun']
  setDelta.newMissing 12
  ```
- Exact command: `python3 $S/rearm_probe.py $S/sweep-paths.json` (Appendix B).
- Exact observed output: `{"ok": false, "stalePinned": ["~/Projects/ds4cc-marketplace", "~/Projects/ds4cc-marketplace/CNAME", "~/Projects/ds4cc-marketplace/burnerchrome", "~/Projects/ds4cc-marketplace/speedrun"], "missUnpinned": 12, "duplicates": false}`; `exit=1`.
- Why the sweep's exit code is not enough: `scripts/freshness-sweep.mjs:480` computes `recovered` as informational; the exit code (`:1007`) counts only drift and newMissing. Hermetic reproduction under a scratch `HOME` (Appendix D), using the sweep's own `KAKE_REPO_ROOT` and `KAKE_FRESHNESS_PINS`:
  ```
  1-absent-pinned (pins=pinned) exit=0     declaredAbsent ['~/rearm/x.md']  newMissing []  recovered []
  2-recovered-still-pinned (pins=pinned) exit=0   declaredAbsent []  newMissing []  recovered ['~/rearm/x.md']
  3-redisappears-still-pinned (pins=pinned) exit=0  declaredAbsent ['~/rearm/x.md']  newMissing []  recovered []
  3b-control-redisappears-unpinned (pins=unpinned) exit=1  declaredAbsent ['~/rearm/x.md']  newMissing ['~/rearm/x.md']  recovered []
  ```
  Run 2 is the stale-pin state: the sweep is green, and `rearm_probe.py` on it exits 1 (`stalePinned ["~/rearm/x.md"]`). Run 3 is the masked re-disappearance: exit 0 while still pinned.
- Pin location: `corpus/knowledge/freshness-pins.json:57` (`"pathsMissSet": [`).
- Smallest fix: in the C1 reconciliation commit, remove the four `~/Projects/ds4cc-marketplace*` tokens from `pins.pathsMissSet`, and do not re-pin them (the contract credits re-pins only for targets whose receipt observes the miss this round). Add `rearm_probe.py` as a gate. Owner: L1 (pins and sidecar writes).

### F5 — P2 — restoration notes with absence words would silently annotate neighbouring cites (freshness, C1)

- Impacted claim: contract C1 "after" (restoration corrections for recovered targets) and draft criterion 3.
- Source: `scripts/freshness-sweep.mjs:324-334`. In the non-strict default, when any line within ±2 matches `ABSENT_RE`, every token of the citing line is marked annotated (`if (strict && !mentions) continue;` at `:333` is skipped). The `mentions` flag is only enforced with the opt-in `pathsAbsenceStrictSameLine` pin. The sweep's own fixture F (`scripts/freshness-sweep.mjs:1183-1188`) documents the bleed as a limitation.
- Exact command: `node .ufo/waves/round-24/restoration_vocab_probe.mjs <file>` (Appendix C) against candidate restoration text, plus the sweep's regex `freshness-sweep.mjs:122`.
- Exact observed output:
  ```
  {"ok":true,"headerOk":true,"absenceWord":null}      exit=0   (clean restoration note)
  {"ok":false,"headerOk":true,"absenceWord":"absent"} exit=1   (note says "the earlier line said the tree was absent")
  {"ok":false,"headerOk":false,"absenceWord":null}    exit=1   (header missing)
  ```
  Regex-only check of three further wordings: `observed present; the earlier missing-path note is superseded.` MATCH `missing`; `it is no longer a dangling cite.` MATCH `no longer`.
- Smallest fix: write restoration notes with the header from draft criterion 3 and no `ABSENT_RE` word; land `restoration_vocab_probe.mjs`. Apply the same wording rule to sidecar notes for non-author files (`corpus/lessons/*aggregator*.md`, `*verifier-spotcheck*.md`).

### F6 — P2 — no RFC 3339 source row; the named grammar is not yet admissible (admission, C2)

- Impacted claim: contract C2 `sourced` field ("RFC 3339 date-time grammar … opened this round (new SOURCES rows)"), and draft criterion 1's grammar citation.
- Exact command: `grep -n -i "RFC 3339\|rfc3339\|RFC 9110\|rfc9110" corpus/SOURCES.md`.
- Exact observed output:
  ```
  18:| S010 | RFC 9110: HTTP Semantics — https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8 | spec | A | HTTP validator semantics for entity tags | …
  36:| S028 | RFC 9110: HTTP Semantics, http and https URI schemes — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | Validity of http(s) URIs with an empty host; … 
  ```
  No RFC 3339 row.
- Primary text read this round (read-only GET, `https://www.rfc-editor.org/rfc/rfc3339`; metadata line reads "Updated by: RFC9557"). Quoted from §5.6 (NOTE): "the "T" and "Z" characters in this syntax may alternatively be lower case "t" or "z" respectively." and "Applications using this syntax may choose, for the sake of readability, to specify a full-date and full-time separated by (say) a space character." From §5.7: "The grammar element time-second may have the value "60" at the end of months in which a leap second occurs" and "this profile of ISO 8601 only allows values between "00" and "23" for the hour". Draft Appendix A rejects leap seconds and the space separator by policy; this is a stricter local rule, not the RFC's requirement. RFC 9557 (which updates RFC 3339) was not read; any suffix beyond the 3339 grammar is rejected.
- Smallest fix: L1 appends a tier-A row (`spec`, RFC 3339 §5.6/§5.7, URL above, access date 2026-10-21, located quotes as above) to `corpus/SOURCES.md` before draft criterion 1 is admitted.

### F7 — P3 — decisions for L1 (not defects)

- Lower bound: the draft uses the round-open instant `2026-10-21T11:33:15Z` (contract `worldChangeAtOpen`). Round-23 used the calendar day `2026-10-21`. L1 chooses.
- Upper bound: "committer time of the measured revision" is `git show -s --format=%cI <commit>`. It is set by the committer, so the bound is a consistency check on structure, not authentication of the observation (matches the contract's limits).
- Draft criterion 2 relies on set equality. It does not check that a recovered target's own restoration note exists; criterion 3 and the non-author review cover that.

## Checked and held

- C1 population: 19 targets, classes T01–T03 drift, T04–T15 newMissing, T16–T19 recovered (`.ufo/waves/round-24/c1-population.json`; `python3` count of `class`). Matches the contract's `3 drift, 12 newMissing, 4 recovered`.
- Sweep at round open reproduces: `code 1`, reason `§paths: 3 unannotated miss · 12 NOT in pins.pathsMissSet`, counts drift 3 / newMissing 12 (F4).
- Lane tree: `git --no-optional-locks status --short` shows only `?? .ufo/waves/round-24/` before and after my work. No `__pycache__` was written (`find . -name __pycache__` empty; `sys.dont_write_bytecode = True` set before importing round-23 modules).
- Round-23 runners not edited; `measure_c1.py` and `measure_c2.py` read only via `importlib` in scratch.
- Proposed admit rule (Appendix A): 20/20 vectors match the stated expectation (run output below).
- Restoration probe (Appendix C): 3/3 cases behave as stated.
- Re-arm probe (Appendix B): on the lane sweep, exit 1 (stale pins and unpinned misses); on the hermetic runs, exit 1 for the stale-pin state and 0 for the clean states.
- Draft text adds no `~/` or `/home/vgpnk/` path, so the citation scan does not gain a cite. The drafts contain no restoration-type absence word outside the quoted sweep regex.
- Sweep is read-only by construction per its header (`scripts/freshness-sweep.mjs:1-40`); the sweep was run with `--offline --section=paths` only.

## Limits

- Author-side scribe only: no independent admission; no promotion claimed.
- Lane not written: nothing appended to `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/freshness-pins.json`, or any script. No commit, push, or git mutation.
- The probes named in the drafts do not yet exist in the lane at `f7de3ab`: `scripts/receipt_replay.py` (C2 deliverable), `.ufo/waves/round-24/rearm_probe.py`, `.ufo/waves/round-24/restoration_vocab_probe.mjs`. Source for the last two is in Appendices B–C; the timestamp rule is in Appendix A and must be wrapped in `receipt_replay.py`. The `--root . --revision <commit>` argv in criterion 1 mirrors the round-23 runners and is NOT confirmed for the C2 deliverable; L1 substitutes its real argv before admission. All must land before the "Fails if" predicates are runnable.
- Round-23 counts were measured by in-process calls with injected bytes, not by a sandbox commit and CLI run. The exit code for the `served()` traceback path was not observed (F2).
- Hermetic re-arm runs used a scratch `HOME` for `~` resolution and the sweep's `KAKE_REPO_ROOT` / `KAKE_FRESHNESS_PINS` environment overrides; they do not exercise the real `~/Projects` tree.
- Web: one read-only GET of the RFC 3339 primary text. No other external fetch.
- Tools installed or updated: none. Pre-existing: Node v24.21.0, Python 3.14.8. No pacman transaction, no host service change.
- Scratch outputs in `/tmp/kake-r24-ScribeQualityCriterion-TFN6` are not evidence; the Appendices are the recreation path.

## Appendix A — proposed admit rule and vectors (`timestamp_vectors` candidate)

Run in scratch on Python 3.14.8. Round-open `2026-10-21T11:33:15Z` and an illustrative measured-revision commit instant `2026-10-21T13:00:00Z` (the real bound is read from `git show -s --format=%cI <commit>` for the revision under test).

```python
import re, datetime as dt
RFC3339 = re.compile(r"^(\d{4})-(\d{2})-(\d{2})[Tt](\d{2}):(\d{2}):(\d{2})(\.\d+)?([Zz]|[+-](\d{2}):(\d{2}))$")
ROUND_OPEN = dt.datetime(2026, 10, 21, 11, 33, 15, tzinfo=dt.timezone.utc)
COMMIT = dt.datetime(2026, 10, 21, 13, 0, 0, tzinfo=dt.timezone.utc)  # illustrative
def admit(s):
    m = RFC3339.match(s) if isinstance(s, str) else None
    if not m: return False, "grammar"
    y, mo, d, H, M, S = (int(x) for x in m.groups()[:6])
    if S == 60: return False, "leap second (policy reject)"
    try: base = dt.datetime(y, mo, d, H, M, S)
    except ValueError: return False, "calendar/range"
    tz = m.group(8)
    if tz in ("Z", "z"): off = dt.timedelta(0)
    else:
        oh, om = int(m.group(9)), int(m.group(10))
        if oh > 23 or om > 59: return False, "offset range"
        off = dt.timedelta(hours=oh, minutes=om) * (1 if tz[0] == "+" else -1)
    inst = (base - off).replace(tzinfo=dt.timezone.utc)
    if inst < ROUND_OPEN: return False, "before round open"
    if inst > COMMIT: return False, "after commit time"
    return True, "ok"
```

Observed (20 vectors): `mismatches: 0 of 20`. Per row: `2026-10-21T12:00:00Z` admit; `2026-10-21T12:00:00.123456Z` admit; `2026-10-21t12:00:00z` admit; `2026-10-21T10:00:00-03:00` admit (equals commit, inclusive); `2026-10-21T09:59:59-03:00` admit; `2026-10-21T08:00:00-03:00` reject (11:00Z is before round open 11:33:15Z); `2026-10-21T08:00:00Z` reject (before round open); `2026-10-20T23:59:59Z` reject; `2026-10-21T23:00:00Z` reject (after commit); `2099-01-01T00:00:00Z` reject (after commit); `not-a-date`, `2026-10-21zz`, `2026-10-21`, `20261021T120000Z`, `2026-10-21 12:00:00Z` (space: RFC NOTE allows, draft rejects by policy), `2026-10-21T12:00:00` (no offset) reject (grammar); `2026-13-45T99:99:99Z`, `2026-02-30T00:00:00Z` reject (calendar/range); `2026-10-21T12:00:60Z` reject (leap second, policy); `2026-10-21T12:00:00+24:00` reject (offset range).

## Appendix B — re-arm probe (`rearm_probe.py`; candidate for `.ufo/waves/round-24/rearm_probe.py`)

```python
#!/usr/bin/env python3
"""rearm_probe.py SWEEP_JSON -- exit 1 iff pins.pathsMissSet differs from sections.paths.missSet.

Stale pins = pinned tokens no longer missing (a recovered target must leave the pin).
Unpinned = observed misses not pinned. Duplicates are a pin-file defect. Exit 2 = unreadable.
"""
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    pinned = d["pins"]["pathsMissSet"]
    miss = d["sections"]["paths"]["missSet"]
except (OSError, ValueError, KeyError, TypeError) as exc:
    print(json.dumps({"error": type(exc).__name__, "detail": str(exc)})); sys.exit(2)
stale = sorted(set(pinned) - set(miss))
unpinned = sorted(set(miss) - set(pinned))
dups = len(pinned) != len(set(pinned))
ok = not stale and not unpinned and not dups
print(json.dumps({"ok": ok, "stalePinned": stale, "missUnpinned": len(unpinned), "duplicates": dups}, ensure_ascii=False))
sys.exit(0 if ok else 1)
```

Observed: lane sweep `ok=false`, `stalePinned` = four `ds4cc-marketplace` tokens, `missUnpinned` 12, exit 1. Hermetic run 1 (absent, pinned): `ok true`, exit 0. Run 2 (recovered, pinned): `ok false`, `stalePinned ["~/rearm/x.md"]`, exit 1. Run 3 (re-disappeared, pinned): `ok true`, exit 0 (the probe checks pin/miss equality at the recovery step; the masked-disappearance case is caught by run 2's state, which is why the criterion names the recovery commit).

## Appendix C — restoration vocabulary probe (`restoration_vocab_probe.mjs`; candidate for `.ufo/waves/round-24/`)

```js
#!/usr/bin/env node
// usage: node restoration_vocab_probe.mjs FILE   (FILE = the appended restoration text only)
// exit 0 iff header matches and no absence word (same regex as scripts/freshness-sweep.mjs:122)
import fs from 'node:fs';
const ABSENT_RE = /absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing/i;
const text = fs.readFileSync(process.argv[2], 'utf8');
const headerOk = /^(\*\[r24 restoration 2026-10-21:|<!-- r24 restoration 2026-10-21:)/.test(text.trimStart());
const m = text.match(ABSENT_RE);
const ok = headerOk && !m;
console.log(JSON.stringify({ ok, headerOk, absenceWord: m ? m[0] : null }));
process.exit(ok ? 0 : 1);
```

Observed: clean note `{"ok":true,"headerOk":true,"absenceWord":null}` exit 0; note with `absent` `{"ok":false,"headerOk":true,"absenceWord":"absent"}` exit 1; missing header `{"ok":false,"headerOk":false,"absenceWord":null}` exit 1.

## Appendix D — hermetic re-arm reproduction (recreate under a fresh `mktemp -d`)

```sh
R="$(mktemp -d /tmp/kake-r24-rearm-XXXX)"; mkdir -p "$R/home/rearm" "$R/repo"
printf '# fixture\n\nThe cited recipe `~/rearm/x.md` was absent on 2026-10-21 (historical record, not an executable instruction).\n' > "$R/repo/SKILL.md"
printf '{"schema":"kake-freshness-pins-v1","round":0,"pins":{"pathsMissSet":["~/rearm/x.md"]}}\n' > "$R/pins-pinned.json"
printf '{"schema":"kake-freshness-pins-v1","round":0,"pins":{"pathsMissSet":[]}}\n' > "$R/pins-unpinned.json"
run(){ HOME="$R/home" KAKE_REPO_ROOT="$R/repo" KAKE_FRESHNESS_PINS="$R/pins-$1.json" node scripts/freshness-sweep.mjs --offline --section=paths --json > "$R/out-$2.json" 2>/dev/null; echo "$2 exit=$?"; }
run pinned 1; printf 'present\n' > "$R/home/rearm/x.md"; run pinned 2; rm -f "$R/home/rearm/x.md"; run pinned 3; run unpinned 3b
```
(Run from the lane root so `scripts/freshness-sweep.mjs` resolves.) Expected: `1 exit=0`, `2 exit=0`, `3 exit=0`, `3b exit=1`. The `rearm_probe.py` exit on `out-2.json` is 1.
