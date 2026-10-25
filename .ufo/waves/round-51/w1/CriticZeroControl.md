# Critic — zero-control falsification, round 51 wave 1

Seat: `L1Kake51.CriticZeroControl-2`. Axes owned by this lane: operability (C1), freshness (C2).
Lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`, tip `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`,
base `007d66e4e8360a5f88d29a93eeedd8066dad4434`. Read-only on the lane; all scratch under `/tmp`
(`/tmp/c51zero`, `/tmp/c51zero2`, `/tmp/c52copy`, `/tmp/c51_qt_mirrorfix.py`). No tool installed or
upgraded this seat.

Those four `/tmp` paths are disposable scratch, not evidence: §§2–3 state the exact content of every
fixture file, so each repo is re-creatable from this report's own text, and the counters are runnable
against the rebuild. No `.ufo/` scratch tree (round 35 or otherwise) is cited by this report.

## 0. What I ran, and what it printed

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py   --root . --revision 9d13768  -> C1 ledger 0/3 met=False   exit 1
$ python3 -B .ufo/waves/round-51/c51_quote_truth.py   --root . --revision 9d13768  -> C2 quote-truth 8/8 met=True exit 0
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py   --root . --revision 007d66e  -> C1 ledger 0/3 met=False   exit 1
$ python3 -B .ufo/waves/round-51/c51_quote_truth.py   --root . --revision 007d66e  -> C2 quote-truth 0/8 met=False exit 1
```

The dispatch figures reproduce exactly. C1 at the tip reads `L1/L3 FAIL - settlement receipt absent
/ route map absent`; `route-map.json`, `route-probes/`, `settlement.json` are present in the worktree
but untracked, so the counter is right to score 0/3 at a commit. That 0/3 is **absence of bytes**, not
absence of work — which is the whole subject of this report.

**Post-landing re-run.** The L1 landed the wave evidence during this review
(`907790c78008819fc95c988431188f90b81f0d5f`, "land the wave evidence, the ledger verdict and the mirror
repair"). At that tip both counters pass: **C1 `3/3 met=True` exit 0**, **C2 `8/8 met=True` exit 0**.
The landed wave is real and substantive: `spawn 48`, `settled 48`, `dead 0`, `reports_written 48`, 48
committed `.md` reports, **48 distinct sha256**, smallest 5,062 B, 749,513 B total, every settled seat
carries `report: true`, wall clock 897 s named in `LOG.md:2088`. Sections 2–5 are measurements of what
the *predicates* can and cannot distinguish; that the real wave scores the same 3/3 and 8/8 as the
fixtures below is the finding, not a contradiction of it.

## 1. The base control is only an absence control

`contract.json` declares `doNothingControl: "the base revision 007d66e scores 0 of 3 / 0 of 8; the
counter reads committed bytes only"`. That is true and I reproduced it. But it falsifies only the
proposition "a revision with no evidence files scores". It says nothing about the proposition that
matters: **a revision whose author did no work but wrote consistent evidence**. The committed control
files (`.ufo/waves/round-51/controls/`) cover the same two cases — base (absent) and junk
(`c1-junk-wave.txt`: 40 claimed vs 25 committed, revisions `d969fa2` / `cc57cb8`). Neither control is a
*consistent fabrication*. That gap is not theoretical; sections 2 and 3 close it with runnable repos.

## 2. C1 — could a round that committed nothing but the wave evidence reach 3/3? YES. No guard.

Scratch repo `/tmp/c51zero2` (git init, user unknown to the lane, evidence only, no seat work at all):

- 48 claimed seats in `settlement.json` and `w51-taskcall.json` (`counts.spawn=48`, 48 tasks),
  `reports_written=0`, `w1/` empty.
- one role in `route-map.json` bound to a fabricated alias, one hand-written receipt
  `{"alias":"fabricated/alias","httpStatus":200,"ok":true}`.
- `wave-timing.json`, `round-time-accounting.json`, `wave-grant.txt`, `LOG.md` written by the same hand.

```
--- 48 seats, zero committed reports ---
C1 ledger 3/3 met=True   L1 pass  L2 pass  L3 pass   exit=0
```

Variants, all 3/3 exit 0:

| fixture | what the wave actually produced | score |
|---|---|---|
| `/tmp/c51zero` empty wave: `spawn=0`, `tasks=[]`, `reports_written=0`, one fake role + fake receipt | nothing | **3/3** |
| `/tmp/c51zero2` 48 claimed seats, `w1/` empty | nothing | **3/3** |
| `/tmp/c51zero2` 48 **zero-byte** `w1/seat*.md` (`du -b w1` = `0`), settlement `report:true`, `reports_written=48` | 48 empty files | **3/3** |

Why each sub-check is vacuous:

- `L1` `reported == committed` is a set equality; with two empty sets it holds. `reports_written` is
  compared only against the *committed file count*, so `0 == 0` passes; nothing requires
  `spawn > 0` or `reports_written > 0`. The contract's own L1 sentence ("the committed seat-report
  count equals the settlement's `reports_written`") is satisfied by 0 = 0 in the same way.
- `L1` never opens a report. The 0-byte test above shows a stub is indistinguishable from a real
  report: no size, no hash, no seat-name-in-body check.
- `L2` needs one receipt claiming `ok:true` and an integer status. The failure path (excerpt, deviation)
  is only exercised if the author chooses to declare a failure.
- `L3` is arithmetic among three files the author wrote in the same pass, plus `str(wall) in LOG.md`.

**Guard that blocks "commit nothing but the wave evidence": none exists.** C1 is a self-consistency
ledger, and the claim text is honest about that ("re-derives … from committed bytes"); the falsified
proposition is the stronger one a reader will infer, that 3/3 means the wave's accounting is *true*.

### 2b. L3's LOG binding is a bare substring (reproduced)

`if wall > 0 and str(wall) not in log_text`. Fixture: `wall = 26 s`, `LOG.md = "# Round 51 log,
2026-10-25\nno wall clock figure stated\n"` → **3/3 exit 0**. The token `26` matched inside the year.
Any wall figure that occurs as a digit-run in a date, a byte count or a version string false-passes.

### 2c. C1 breaks its own exit-code contract

Docstring: `2 the evidence cannot be evaluated`. No `try/except` exists. A settlement seat missing
`name` crashes `check_l1` at `sorted(e["name"] …)` → `KeyError: 'name'`, **exit 1** — the same code a
genuine miss returns. An unevaluable ledger is reported as a failed predicate. Operability defect in
the instrument that is itself the operability claim.

### 2d. Smallest safe corrections for C1 (none changes the predicate arithmetic)

1. `spawn > 0` and `reports_written > 0`; and `len(reported) == len(settlement["settled"])` — every
   *settled* seat must carry `report:true` (dead seats stay reportless, which the real wave needs).
   Closes the empty wave and the 48-claimed/0-reports form.
2. Pin each report: settlement carries `sha256` per report, counter re-derives it and rejects a body
   with no non-blank line and duplicate digests. Closes the 0-byte-stub form.
3. LOG binding: require a labelled token (`wall_clock_seconds=1860` or `wall clock: 1860 s`), not
   `str(wall) in text`.
4. Wrap each check in `try/except` → exit 2, as documented.

Measured against the landed wave (`907790c`), not assumed: 1 passes (`settled 48`, every one
`report: true`, `reports_written 48`, `dead 0`); 2 passes (48 reports, 48 distinct sha256, smallest
5,062 B — no stub, no duplicate); 3 passes (`LOG.md:2088` names "wall clock **897 s**", and 897 is also
what `settlement`/`wave-timing` re-derive); 4 is a code change with no evidence dependency. So all four
are satisfied by the real round and would have to be defeated deliberately — the strengthening costs the
claim nothing, which is why the frozen predicate's silence about them is a defect rather than a
trade-off.

## 3. C2 — could a round that copied the bodies without opening the URLs reach 8/8? YES.

Scratch repo `/tmp/c52copy`: two **invented plain-text** "retained bodies" (no HTML, no network), a
lesson whose Gate quotes are substrings of them, rows shaped like the real ones, and a receipt file
carrying `httpStatus: 404` / `500`, `fetchedAt: 1999-01-01T00:00:00Z`, and `url` set to
`https://developers.google.com/` — a bare prefix, not the row's URL.

```
C2 quote-truth 8/8 met=True   exit=0     (all eight conditions pass)
```

Guards that do hold, named precisely:

- **C5+C6 bind quote → bytes → receipt.sha256.** A mis-transcribed quote (the round-50 defect class)
  fails; my fixture had to plant the quote *in* the fabricated body to pass. This is a real guard.
- **C8 ancestor check** (`git merge-base --is-ancestor <mirror> <rev>`) requires a mirror commit before
  the measuring revision. Real, and hard to fake without leaving history.
- **C3/C4** pin row shape (11 cells, `mined`, `2026-10-24`, normalized recheck) and `used-by`.

Holes:

- **C6 reads only `sha256` and `url`.** `url` is a substring test (`receipt.get("url") not in row[1]`),
  so a prefix passes. `httpStatus`, `bytes`, `declaredBytes` and the file-level `fetchedAt` — all
  present and *correct* in the committed `receipts.json` — are never read. Freshness is exactly the
  axis C2 owns, and the receipt already carries the freshness facts: `httpStatus 200/200`,
  `bytes 174926/175561 == len(body) == declaredBytes`, `fetchedAt 2026-10-24T23:16:49-03:00` inside
  `[base 23:02:31, tip 23:23:07]`. The predicate simply does not ask.
- **No provenance of the body itself**: no content-type, no response header, no requirement that the
  bytes are HTML. A local file passes. (I found no *earlier* committed copy of these two pages —
  `grep -rl 'crawling-indexing/googlebot' .ufo/waves` hits only round-51 sources plus pages that merely
  link the docs — so in this lane the copy path would be an author-local file or fabrication; both
  pass.)
- **C7's census receipt is self-reported**: argv text, stdout text, exit text; no hash of the mirror, no
  line count, no binding of stdout to bytes. My fixture's three hand-written files passed. Also
  `if MIRROR not in argv` is a substring test — a census run on any file whose path embeds the mirror's
  relative path satisfies it [code reading, `.ufo/waves/round-51/c51_quote_truth.py` C7 block].

Smallest safe correction for C2 (free for the real claim — every value already exists and agrees):

```
C6 += receipt["httpStatus"] == 200
      receipt["bytes"] == len(body)
      url_token(row[1]) == receipt["url"]           # exact, not substring
      round-start <= receipts["fetchedAt"] <= commit time
C7 += sha256(MIRROR bytes) pinned in the census receipt and re-derived by the counter
```

I re-ran those four additional checks by hand against the real bytes: 200/200, byte counts exact,
`fetchedAt` inside the window — the strengthening would leave C2 at 8/8 today and make the copy path
fail.

## 4. C8's condition sentence and C8's code check different things (the mirror is never read)

`code`: `mirror_rows = parse_registry(show(root, mirror_commit, REGISTRY))` — it reads
`corpus/SOURCES.md` at the mirror commit. It never reads `MIRROR`
(`.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md`), although the failure message says
"the mirror already carries the row". Evidence:

```
$ git show 19a99bd:corpus/SOURCES.md | grep -c '^| S26[23]'                                   -> 0
$ git show 19a99bd:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md | grep -c ... -> 2   (lines 152-153)
$ diff <(git show 19a99bd:corpus/SOURCES.md) <(git show 19a99bd:.ufo/.../pre-append/corpus/SOURCES.md)
151a152,153   (exactly the two adopted rows)
```

So the contract's C8 sentence — "**the mirror's registry carries none of the adopted ids**" — is
false on the committed bytes: the mirror carries both. The code's check (lane registry at the mirror
commit lacks the ids) is true and meaningful, and it is the property that actually proves ordering.

Convention check: round 49's mirror carries S273/S274 (2 rows, registry at its mirror commit 0) and
round 50's mirror carries S286 (1 row, registry at `33eec7f` 0). Three rounds, same shape. So
"pre-append" in this lane means *the mirror was committed before the append commit*; the mirror is the
prepared post-append copy that the census validated — which is the better coverage, but not what the
sentence says.

Proof that the counter cannot see it: patch one path only and run against the real lane read-only —

```
$ sed 's|mirror_commit, REGISTRY)|mirror_commit, MIRROR)|' c51_quote_truth.py > /tmp/c51_qt_mirrorfix.py
$ python3 -B /tmp/c51_qt_mirrorfix.py --root . --revision 9d13768
C2 quote-truth 7/8 met=False
  C8_append_after_mirror FAIL
    - S262: the mirror already carries the row
    - S263: the mirror already carries the row
```

Verdict: **the artifact at the measured revision contradicts the frozen sentence; the code silently
substitutes a different check so the mismatch is invisible.** A reader auditing C8 against its own
wording finds it false while the predicate prints 8/8.

### 4b. A repair is in flight (uncommitted) and it leaves a trap

While this review ran, another seat (`ExecRegistryDiff`, and `assimilation/pre-append/census-correction.txt`
in the worktree) reached the same contamination independently and rewrote the mirror from
`git show 19a99bd:corpus/SOURCES.md`:

```
mirror at the measured rev 9d13768 : sha256 4ea81a5a…  145 data rows (S262/S263 present)
mirror in the worktree now         : sha256 cd9ee4cf…  143 data rows (absent)
census re-run, validate --file     : exit 0, W04 only, no E03/E04; attempt-1 receipts -> superseded/
```

That repair is the right artefact fix. Two residuals it does not close:

1. **`git log --diff-filter=A` still names `19a99bd`, whose blob is `4ea81a5a…` (contaminated).** A
   "corrected" C8 written as `show(add_commit, MIRROR)` would keep failing after the repair. The sound
   form is the mirror **at the measured revision** — `show(rev, MIRROR)`, ids absent — plus
   `sha256(receipt) == sha256(show(rev, MIRROR))` in the census receipt. That form fails on `9d13768`
   (as it should) and passes after the repair commit.
2. **The census receipt still binds nothing**: argv/stdout/exit are text; the corrected run has no
   sha256 line. Pin `cd9ee4cf…` in the receipt; otherwise the next repair can again leave receipt and
   bytes disagreeing, and C7 (which only greps `--file`, `--root`, `E03`, `E04`) cannot see it.

Because the contract and the counter are frozen, the smallest safe move this round is: land the repair
as a commit, record the corrected sha256 in the census receipt, and disclose in the verification report
that C8 at `9d13768` passed a sentence that the bytes contradicted.

**Status after the landing (`907790c`).** The repair did land: the mirror at the new tip is
`cd9ee4cf…`, 143 rows, **0** adopted rows, so the C8 sentence is now true of the committed artifact —
but only because a seat found the contamination by hand (`ExecRegistryDiff`), not because C8 can detect
it. Both residuals survive the landing, re-measured at `907790c`:

- `git log --diff-filter=A … -- MIRROR` still resolves to `19a99bd`, whose blob is `4ea81a5a…`
  (contaminated, 145 rows). Trap 1 is live.
- `grep -c 'cd9ee4cf\|sha256'` over `census-argv.txt` and `census-stdout.txt` = **0 / 0**. Trap 2 is
  live: the receipt still binds no bytes.

## 5. C2's entry labels two quotes as raw that derive collapsed-only

`corpus/knowledge/canonical-selection.md` says "The page lists the variant classes it recognises,
**each quoted raw from the page**:", then lists four bullets; only the last two carry
"(collapsed-only quote)". Derived class from both blobs (lane definition: script/style removed, tags
removed, entities decoded, whitespace collapsed — `corpus/lessons/round-49.md:34`,
`round-50-verifier-spotcheck.md:106`):

```
S262 'Device variants : for example, …'   -> collapsed-only      (raw: <b>Device variants</b>:)
S262 'Protocol variants : for example, …' -> collapsed-only      (raw: <b>Protocol variants</b>:)
S262 'Site functions …' / 'Accidental variants …' -> collapsed-only   (marked)
S263 'Googlebot Smartphone : …' / '… Desktop : …' -> collapsed-only   (marked)
```

So "each quoted raw" is false for the first two bullets, and the lesson's "each entry marks the class
of every other quote it carries" (`corpus/lessons/round-51.md:13-14`) is false. This is precisely the
"quote class blurred" defect round 50 closed with `c50_quote_class.py` (derive from both blobs, swapped
label fails); round 51's counter has **no quote-class condition at all**, so the regression is invisible.
Everything else is clean: all 10 blockquotes are tag-strip substrings, and the two Gate quotes are raw —
`S262 10 words in body: True`, `S263 9 words in body: True`, independently re-derived with the counter's
own `gate_quote` parser.

Fix (small, no predicate change): move "(collapsed-only quote)" onto those two bullets or drop "raw"
from the sentence; carry the class derivation into the counter as a ninth condition next round.

State at the measured revision vs the worktree: the finding is measured on `9d13768` (the committed
entry still said "each quoted raw"). A worktree repair of the same sentence appeared during this review
and **landed at `907790c`**: `canonical-selection.md` now reads "each quoted below as rendered text —
the inline markup is removed … (round-51 correction; see § Quote classes)", and `crawler-identity.md`
relabels its two bullets the same way. The artifact is fixed; the predicate still has no condition that
would have caught the original label, so the same mislabel can pass again next round.

## 6. Claim facts I could confirm

- Entries are genuinely new: absent at `007d66e`, present at tip.
- Append is additive: `git diff --numstat 007d66e 9d13768 -- corpus/SOURCES.md` = `2 0`; 143 → 145 rows;
  zero removed lines.
- Gate quotes: 10 and 9 words, raw substrings, `sha256` and byte counts match the committed bodies
  (`7922243…`, 174926; `6afbdc8…`, 175561) and `declaredBytes == bytes == len`.
- Separability holds as declared: C2 reads `corpus/` + `sources/` + `assimilation/pre-append/`; C1 reads
  wave evidence + `LOG.md`. Neither reads the other's inputs.
- Freshness window: the only network fetch is the L1's `2026-10-24T23:16:49-03:00`, inside
  `[base commit 23:02:31, tip commit 23:23:07]` and ~4 h before the wave (`wave-start-utc
  2026-10-25T06:32:17Z`). "Re-grounded this round" is true at round level; no wave seat opened the URL,
  and per §3 the counter could not tell if one had.

## 7. Verdict

| proposition | verdict | guard |
|---|---|---|
| base `007d66e` scores 0/3 and 0/8 | holds, reproduced | absence of evidence |
| landed tip `907790c` scores 3/3 and 8/8 on a real 48-seat wave (48 distinct reports, 0 dead) | holds, reproduced | — |
| a round that commits nothing but the wave evidence reaches C1 3/3 | **holds (hole)** — 3 fixtures, incl. 48 zero-byte reports | **none** |
| a round that copies/fabricates bodies without opening the URLs reaches C2 8/8 | **holds (hole)** — 8/8 with 404/500 receipts and 1999 fetch time | none for provenance; C5/C6 bind quote→bytes only |
| C2's C8 sentence "the mirror carries none of the adopted ids" | **false at `9d13768`, true at `907790c` after a hand-found repair** | counter reads `REGISTRY`, not `MIRROR`; it can see neither state |

Impacted axes: **operability** (C1's vacuity, the LOG substring, exit-code contract, uncounted stub
reports) and **freshness** (C2's unpinned fetch time/status/URL, unread mirror, blurred quote class).

The two claims' *counted artifacts* exist and the counters do what their code says. What the predicates
cannot do is distinguish a wave from a well-formed account of one (C1), or a fetched page from a
well-formed copy of one (C2). Both claim-level defects found by reading bytes were repaired in artefacts
at `907790c` — the mirror regenerated from the pre-append registry (`9d13768` blob `4ea81a5a…` →
`cd9ee4cf…`), the two quote labels corrected — **without the frozen predicate moving**. That is the
right shape of repair, and it is also the proof that the predicates do not perform it: each repair came
from a seat reading bytes, not from a counter condition. C1's 3/3 and C2's 8/8 stand as declared; the
residual exposure is that next round's fabricated-but-consistent evidence would score identically.

## Appendix A — the fixtures, reproducible from this report alone

Scratch is not durable (a round-35 sweep moved and re-created seat dirs during this round; `/tmp` is
worse). The two counterexample repos are therefore specified here as an executable builder, so a reader
can re-run both holes without any file this report does not carry. Verified: run from a clean directory,
it prints `C1 ledger 3/3 met=True exit=0` and `C2 quote-truth 8/8 met=True exit=0`.

```
$ python3 -B repro_critic_zerocontrol.py /tmp/cc-repro-test
--- C1 (48 claimed seats, zero reports)
exit=0
C1 ledger 3/3 met=True  (met: ledger_checks_passed == 3 of 3)
--- C2 (fabricated bodies, 404/500 receipts, 1999 fetch)
exit=0
C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)
```

Builder as measured: 124 lines, 6071 bytes, sha256
`a4f36e52414ee06442bf2762de896e6d252dbb740244cdcb48e43d129382af30`. The empty-wave variant in §2 is the
same builder with `n = 0` and no `w1/` directory.

```python
#!/usr/bin/env python3
"""Rebuild the two /tmp counterexample repos from round-51 w1/CriticZeroControl.md.

Usage: python3 repro_critic_zerocontrol.py <scratch-dir>
Prints the two counter invocations and their scores.
"""
import hashlib, json, pathlib, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
C1 = f"{LANE}/.ufo/waves/round-51/c51_wave_ledger.py"
C2 = f"{LANE}/.ufo/waves/round-51/c51_quote_truth.py"


def sh(*args, cwd):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout


def init(root):
    root = pathlib.Path(root)
    if root.exists():
        subprocess.run(["rm", "-rf", str(root)], check=True)
    root.mkdir(parents=True)
    sh("git", "init", "-q", cwd=root)
    sh("git", "config", "user.email", "fixture@invalid", cwd=root)
    sh("git", "config", "user.name", "fixture", cwd=root)
    return root


def commit(root, msg):
    sh("git", "add", "-A", cwd=root)
    sh("git", "commit", "-qm", msg, cwd=root)
    return sh("git", "rev-parse", "HEAD", cwd=root).strip()


def build_c1(root):
    w = root / ".ufo/waves/round-51"
    (w / "route-probes").mkdir(parents=True)
    (w / "w1").mkdir(parents=True)
    n = 48
    (w / "settlement.json").write_text(json.dumps({
        "spawn": n, "settled": [{"name": f"seat{i}", "seconds": 40} for i in range(n)],
        "dead": [], "reports_written": 0, "settled_count": n, "dead_count": 0,
        "timeout_seconds": 600}))
    (w / "w51-taskcall.json").write_text(json.dumps({
        "taskCall": {"tasks": [{"name": f"seat{i}"} for i in range(n)]},
        "counts": {"spawn": n}}))
    (w / "route-map.json").write_text(json.dumps({
        "roles": {"scout": {"kimiModel": "fabricated/alias"}}}))
    (w / "route-probes/p.json").write_text(json.dumps({
        "alias": "fabricated/alias", "httpStatus": 200, "ok": True}))
    (w / "wave-timing.json").write_text(json.dumps({
        "startedAt": "2026-10-25T00:00:00+00:00", "settledAt": "2026-10-25T00:31:00+00:00"}))
    (w / "round-time-accounting.json").write_text(json.dumps({
        "aggregate_seat_seconds": 1920, "dead_seat_seconds": 0, "wall_clock_seconds": 1860}))
    (w / "wave-grant.txt").write_text("granted lane=kake wave=r51-w1 seats=48\n")
    (root / "LOG.md").write_text("wall clock 1860s\n")
    return commit(root, "c1 fixture: 48 claimed seats, zero reports")


def build_c2(scratch):
    root = init(pathlib.Path(scratch) / "c52copy")
    for d in ("corpus/knowledge", "corpus/lessons", ".ufo/waves/round-51/sources",
              ".ufo/waves/round-51/assimilation/pre-append/corpus"):
        (root / d).mkdir(parents=True, exist_ok=True)
    reg = root / "corpus/SOURCES.md"
    reg.write_text(
        "# SOURCES\n\n## Registry\n\n"
        "| id | title — url | kind | tier | note | section | gist | status | opened | recheck | used-by |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
        "| S001 | Old — https://example.com/old | docs | A | x | y | z | mined | 2026-01-01 | on-release | corpus/knowledge/old.md |\n")
    mirror = root / ".ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md"
    mirror.write_text(reg.read_text())
    cen = root / ".ufo/waves/round-51/assimilation/pre-append"
    (cen / "census-argv.txt").write_text(
        "--file .ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md\n")
    (cen / "census-stdout.txt").write_text("census: 0 findings\n")
    (cen / "census-exit.txt").write_text("0\n")
    commit(root, "mirror + census receipt")
    bodies = {
        "S262": "local text copied from anywhere, never fetched: the engine treats a "
                "canonical declaration as a hint\n",
        "S263": "local text copied from anywhere, never fetched: the crawler identity is "
                "declared in the request header\n",
    }
    for sid, text in bodies.items():
        (root / f".ufo/waves/round-51/sources/{sid}.html").write_text(text)
    receipts = {"sources": {
        sid: {"url": "https://developers.google.com/",
              "httpStatus": 404 if sid == "S262" else 500,
              "fetchedAt": "1999-01-01T00:00:00Z",
              "sha256": hashlib.sha256(text.encode()).hexdigest()}
        for sid, text in bodies.items()}}
    (root / ".ufo/waves/round-51/sources/receipts.json").write_text(json.dumps(receipts))
    reg.write_text(reg.read_text() +
        "| S262 | What is URL canonicalization — https://developers.google.com/search/docs/crawling-indexing/canonicalization | docs | A | gist | § x | y | mined | 2026-10-24 | 180d | corpus/knowledge/canonical-selection.md |\n"
        "| S263 | Googlebot — https://developers.google.com/search/docs/crawling-indexing/googlebot | docs | A | gist | § x | y | mined | 2026-10-24 | 180d | corpus/knowledge/crawler-identity.md |\n")
    head = "# t\n\n" + "\n" * 8
    (root / "corpus/knowledge/canonical-selection.md").write_text(head + "S262 body\n")
    (root / "corpus/knowledge/crawler-identity.md").write_text(head + "S263 body\n")
    (root / "corpus/lessons/round-51.md").write_text(
        '## Gate\n\n'
        '- S262 — x — quote: "the engine treats a canonical declaration as a hint" (9 words)\n'
        '- S263 — x — quote: "the crawler identity is declared in the request header" (9 words)\n')
    return commit(root, "fabricated bodies + 404/500 receipts")


def main():
    scratch = sys.argv[1] if len(sys.argv) > 1 else "/tmp/critic-zerocontrol-repro"
    base = pathlib.Path(scratch) / "c51zero2"
    init(base)
    c1_rev = build_c1(base)
    c2_rev = build_c2(scratch)
    for label, cmd, root, rev in (
        ("C1 (48 claimed seats, zero reports)", C1, base, c1_rev),
        ("C2 (fabricated bodies, 404/500 receipts, 1999 fetch)", C2,
         pathlib.Path(scratch) / "c52copy", c2_rev),
    ):
        out = subprocess.run([sys.executable, "-B", cmd, "--root", str(root), "--revision", rev],
                             capture_output=True, text=True)
        print(f"--- {label}\nexit={out.returncode}\n{out.stdout}")


if __name__ == "__main__":
    main()
```
