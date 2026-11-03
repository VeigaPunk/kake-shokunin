# ReviewerC1C3 — round 73 attack seat (C1 and C3)

Base `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`. Lane checkout read-only; every replication ran in a
scratch clone (`git clone --shared`) under `/fast/scratch/hyaku/kake-r73/ReviewerC1C3/`, deleted before yield.
No tool installed or upgraded. Frozen counters and `scripts/freshness-sweep.mjs` were run as-is, never edited.
Not run: `freshness-sweep --selftest` (C3 selftest) and the C1/C2 counters `c73_wave_pointers.py`, `c73_tmp_v3.py`
(not yet delivered at base).

## Verdicts in one place

- **C3 predicate: not contradicted.** In a scratch clone with only the `lineSha256` of the `corpus/SOURCES.md:140`
  entry changed, `freshness-sweep.mjs --offline` exits 1 with empty stderr (F4). Exit 1 is inside the frozen
  predicate. "Evaluable at the tip" holds; "clean" does not (a named `~/projects` drift, F4).
- **C3 legitimacy: the re-pin is a binding repair and does not weaken the binding check, but the absence annotation
  it re-certifies is contradicted on this host today.** The token `~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md`
  exists now (F5). The frozen predicate permits only the one `lineSha256` change that would not correct the note (F5).
  This does not flip the predicate; it limits what the C3 narrative may say.
- **C1 "the two dead tokens are the only dead round-72 wave tokens": confirmed** for the `controls/`, `sources/`,
  `w1/` grammar (2 of 9 unique tokens dead, F7). One out-of-grammar dead pointer exists (`.ufo/l0-questions.md`, F8).
  No verdict change.
- **C1 harm (4): no existing correction-tail rule is violated by the bytes, but the counter-required placement
  (file end) lands under `## Planned — round 73`, a heading that says it declares no claims (F9).** No verdict change.

## F1 — C3 cause: the round-71 edit `84dcc841` is the cause (yes)

Sentence attacked (contract C3 Before): "Cause: round-71 commit `84dcc841` appended a `used-by` cell to the S132 row on line 140."

```
$ git -C $R log -1 --format=%H 84dcc841 -- corpus/SOURCES.md
84dcc8414f94a04304372941f8eebe7eb9d6de16        (exit 0)
$ git -C $R blame -L140,140 --porcelain c1f3d8d4 -- corpus/SOURCES.md | head -1
84dcc8414f94a04304372941f8eebe7eb9d6de16 140 140 1   (exit 0)
$ git -C $R show 84dcc841 -- corpus/SOURCES.md | head -40
@@ -137,7 +137,7 @@ ... | S132 | ... | mined | 2026-10-23 | on-use | corpus/lessons/round-44.md, SCORECARD.md |
+ ... | corpus/lessons/round-44.md, SCORECARD.md, corpus/lessons/round-71.md |   (exit 0; one hunk, one line)
$ git -C $R show 84dcc841^:corpus/SOURCES.md | <line 140, sweep split rule, sha256, no trailing newline>
b3315f41997ae6881726be2a5258f3dc2ae815cde7e3a166617322caed4a8a47   (exit 0)
$ git -C $R show c1f3d8d4:corpus/knowledge/freshness-sidecar.json | grep -B1 -A2 '"line": 140,'  → lineSha256
"lineSha256": "b3315f41997ae6881726be2a5258f3dc2ae815cde7e3a166617322caed4a8a47"
```

The pre-84dcc841 line hashes to the pinned value. Base line 140 hashes to
`4e4081310d6ad17268d8120a29b0400c0edbe6fcee0c035af7c9341acc732e15` (exit 0; node and python agree).
Word-level diff of line 140 across the commit: only the last cell changed (`…SCORECARD.md` → `…SCORECARD.md, corpus/lessons/round-71.md`).
The token cell is unchanged. Later commit `999d208b` adds S439 at SOURCES.md line 185, after every SOURCES.md pin (max 140), so it shifts nothing.

Pitfall: `sed -n '140p' | sha256sum` gives `873efea2…508ca`, which includes the trailing newline and is not the sweep's
method. The sweep splits on `\n` and hashes the line bytes without a terminator.

**Verdict on F1: yes, the cause is the round-71 edit.**

## F2 — Only mismatch in the sidecar (committed bytes, all 174 entries, 62 files)

```
$ node -e '<split on \n, sha256 each entry's line, committed bytes at c1f3d8d4>'
entries 174 files 62 committed-bytes mismatches 1 ["corpus/SOURCES.md:140 ~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md"]   (exit 0)
$ python3 (same rule, hashlib on bytes)
python mismatches: [(140, '~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md')]   (exit 0)
```

Base sweep control: `node scripts/freshness-sweep.mjs --offline` at clone `c1f3d8d4` → exit 2, stderr
`freshness-sweep: Error: paths sidecar binding invalid: corpus/SOURCES.md:140`. Matches the contract control.

## F3 — C3 legitimacy: the sidecar's design (what a re-pin may be)

Design sources read at base (committed bytes):
- `corpus/knowledge/freshness-sweep.md:197`: the sidecar "binds each correction to file, line, token and original line SHA256 … **Stale hashes, wrong tokens, malformed notes and invalid sidecars fail closed (exit2).**" A stale hash is designed to stop the gate, not to be absorbed silently. The same paragraph requires a `kind=absent` note to carry "its date, an observed event or explicit unknown, and 'historical record, not an executable instruction.'"
- `SKILL.md:530` steps 3–4 and `corpus/QUALITY.md:162`: "Re-observe every newMissing/recovered target before changing a pin"; "each re-pin has a dated observation"; "later source changes require new dated observations, not retroactive rewrites."
- `corpus/QUALITY.md:1426` (round-64 criterion): "A round that edits a sidecar-pinned file re-runs the standing §paths sweep on its draft before landing." Round 71 did not do this for `84dcc841`; that is the M2 mistake in the contract.
- `corpus/QUALITY.md:1446` and commit `4c8295fa` (round 64): the only prior sidecar repair changed `line` cells and kept the digests, because the content had moved, not changed.

Reading: a `lineSha256` re-pin after a content edit is a binding repair only if the annotation's claim still holds for the new bytes. The round-64 precedent does not cover a content change. The sweep's binding check confirms what the re-pin touches: `tokens.includes(e.token)` still holds (token cell unchanged), and `kind`, `date`, `note` are unchanged. So the re-pin does not weaken the binding gate; it re-binds a claim whose truth the design requires to be re-observed.

## F4 — C3 predicate with the re-pin applied in scratch

Sentence attacked (contract C3 Predicate): "C3 met iff `freshness-sweep --offline` at the tip exits 0 or 1 with no `Error:` line."

```
$ node -e '<re-pin entry corpus/SOURCES.md:140 lineSha256 only, JSON.stringify(d,null,2)+"\n", scratch clone>'
entries re-pinned 1 new 4e4081310d6ad17268d8120a29b0400c0edbe6fcee0c035af7c9341acc732e15
$ git -C clone diff --stat
 corpus/knowledge/freshness-sidecar.json | 2 +-   1 insertion(+), 1 deletion(-)   (exit 0)
$ KAKE_REPO_ROOT=clone TMPDIR=… node scripts/freshness-sweep.mjs --offline
VERDICT: DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet (exit 1, partial: offline)   (exit 1)
$ wc -c < sweep-repin.err
0
```

Predicate reading: exit 1, empty stderr, one-field sidecar diff: **C3 predicate met.** The single finding is
`~/projects` (5 of 24 cites unannotated: `corpus/lessons/round-66-verifier-spotcheck.md:101`, `round-66.md:69`,
`round-70.md:119`, `round-71.md:73`). `test -e ~/projects` exits 1 and `test -e ~/Projects` exits 0 on this
host, so the drift is a case-sensitivity artefact of the host, not of the 140 entry. It was invisible at base
because the binding error (exit 2) stops the sweep before §paths runs. So "exit 2 at base → exit 1 at tip" hides a
second red; "evaluable with named drift" is the honest reading, and "clean" is not available.

## F5 — C3 legitimacy: the annotation the re-pin re-certifies is contradicted on this host

Sentence attacked (contract C3 Before): "The entry's `lineSha256` is the only field that no longer matches; the token, the kind, the date and the note are unchanged."
The field-level claim is true. The implicit claim that the absence annotation is still correct is not supported.

The base entry: `kind: absent`, `date: 2026-10-31`, note "`~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md` absent on this host — an old-host home path; the Windows host migration removed every former home tree…".

Evidence, today, same host (`~` = `/home/vgpnk`):

```
$ test -e ~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md
(exit 0)                                                       # token PRESENT
$ stat -c '  birth=%w  mtime=%y' <that file>
  birth=2026-10-23 16:07:07 -0300  mtime=2026-10-23 16:07:07 -0300   # file exists before the note date 2026-10-31
$ stat -c '  birth=%w' ~/Projects/shokunin/kama-shokunin
  birth=2026-10-13 16:51:08 -0300                                  # directory exists before the note date
$ git -C ~/Projects/shokunin/kama-shokunin log -1 --format='%h %ad %s'
6035e952 Sun Nov 1 13:46:24 2026 +0000 round-69 verifier spot-check …   (exit 0; tree live on 2026-11-01)
```

Distinguishing evidence:
- **"Still true"** requires: the token absent now (`test -e` exit 1), and the note's observation made on this host (or a host-neutral observation). Observed: `test -e` exit 0 (present). Birth times show the file existed on this filesystem before, and continuously across, the claimed absence date, so the 2026-10-31 "absent" observation cannot describe this filesystem.
- **"Silently invalidated"** is what this host shows: the token resolves, and the absence claim cannot be reproduced here at any date after the file's birth. Either the note was written on another host or the observation was wrong; either way the claim does not describe this host.

Why the gate cannot catch it: `freshness-sweep.mjs:517-518` checks `fs.existsSync(abs)` first and puts a resolving token into `resolve`; the `kind=absent` sidecar annotation is consulted only in the citation scan (`:481-487`) and only changes the absent branch. So an absent note on a present token is inert and never flagged. The re-pin makes the gate evaluable without the annotation being true.

Why the frozen predicate cannot correct it: the design's proper correction (QUALITY:162, SKILL.md:530) is a new dated observation — `kind` flipping to `restored` with a present-state note, i.e. a changed `kind`/`note` or a second entry. The C3 predicate permits only one `lineSha256` change, so the only permitted repair leaves a false absence note in place.

**Verdict on F5: C3's predicate is met (F4). The re-pin is an evaluation fix, not a weakening of the binding gate, and it does not make the annotation true. The C3 narrative should say "evaluable; the 140 absence note is contradicted on this host and inert", not "freshness restored".**

## F6 — Systemic: the absent annotations are host-dependent (affects the reading of C3's freshness score)

```
$ node -e '<for each sidecar entry: kind vs fs.existsSync(expandHome(token)) on this host>'
absent/ABSENT 4
restored/PRESENT 26
absent/PRESENT 144
restored/ABSENT 0
```

144 of 148 `kind=absent` entries name a path that exists on this host today, including the 140 entry and its
siblings at `SOURCES.md:137/138/139`. The four that are absent (`corpus/knowledge/drift-detection.md:77`,
`fleet-registry.md:57`, `free-read-verbs.md:321`, `lessons/round-6-aggregator-audit.md:48`) are the only absent annotations that still describe this host. The sweep stays
evaluable on this host because absent annotations are inert when the token resolves (F5). No frozen kill rule is triggered,
but the offline freshness green is not evidence that the absence annotations are true here. This changes how the freshness claim may be
read; it does not change C3's predicate verdict.

## F7 — C1 (3): dead round-72 wave tokens in LOG section and SCORECARD round-72 rows

Scope read: `LOG.md` lines 2498–2507 (`## Round 72` to EOF); `SCORECARD.md` rows whose first cell is 72 (lines 4818–4819, two rows).

```
$ grep -o -E '(^|[^A-Za-z0-9./_-])(controls|sources|w1)/[A-Za-z0-9._/-]+' (LOG 2498-2507 + the 72-rows) | sort -u
  controls/c1-base.txt  controls/c1-tip.txt  controls/c2-base-red.txt  controls/c2-j3-control-r3.txt
  controls/c2-j3-control.txt  controls/c2-selftest.txt  controls/c2-tip.txt  controls/c56-tip-linux.txt  controls/j3-control.sh
$ git -C $R cat-file -e c1f3d8d4:.ufo/waves/round-72/<token>
  controls/c1-base.txt          RESOLVES (exit 0)
  controls/c1-tip.txt           DEAD     (fatal: path does not exist, exit 128)   # LOG line 2505; SCORECARD line 4818
  controls/c2-base-red.txt      RESOLVES (exit 0)
  controls/c2-j3-control-r3.txt RESOLVES (exit 0)
  controls/c2-j3-control.txt    RESOLVES (exit 0)
  controls/c2-selftest.txt      RESOLVES (exit 0)
  controls/c2-tip.txt           DEAD     (fatal: path does not exist, exit 128)   # LOG line 2505; SCORECARD line 4819
  controls/c56-tip-linux.txt    RESOLVES (exit 0)
  controls/j3-control.sh        RESOLVES (exit 0)
$ git -C $R cat-file -e c1f3d8d4:.ufo/waves/round-72/controls/c1-tip-final.txt   → exit 0
$ git -C $R cat-file -e c1f3d8d4:.ufo/waves/round-72/controls/c2-tip-final.txt   → exit 0
```

No `sources/` or `w1/` token appears in either section. The two dead tokens are the only dead wave-relative tokens.
**Verdict on F7: the C1 premise "dead ≥ 2, and these two are the only dead round-72 wave tokens" holds.** The
live files the tip wrote are `controls/c1-tip-final.txt` and `controls/c2-tip-final.txt`.

## F8 — C1 out of grammar: a dead lane-relative pointer

Sentence attacked (LOG round 72, line 2506): "the operator's dangling-id ruling (`.ufo/l0-questions.md`, kake round-72 line)".

```
$ git -C $R cat-file -e c1f3d8d4:.ufo/l0-questions.md
fatal: path does not exist (exit 128)                 # DEAD relative to the lane
$ ls ~/Projects/shokunin/.ufo/l0-questions.md ; wc -l
283   (exit 0)                                        # exists at the fleet root, not the lane
```

The counter's grammar (`controls/…`, `sources/…`, `w1/…`) excludes `.ufo/…`, so C1 does not count it.
**Verdict on F8: no C1 verdict change.** Disclose: the pointer resolves only from the fleet root; from the lane it is dead.

## F9 — C1 harm (4): SCORECARD tail convention

Last 30 lines of `SCORECARD.md` at base: the round-72 table (`| 72 | calibration …`, `| 72 | operability …`), then
`## Planned — round 73` (line 4825), whose text says "No claims are declared in this section; round 73 declares its own
claims when it opens. Carried routes: …". The file has no end-of-file correction rule. Its correction practice is
in-section appended prose (`Correction (appended, round 32)` line 1058; `Corrections and limits found by wave 1 (appended …)` line 1153;
`Corrections from wave 2 … (append-only; earlier lines stand as written)` line 2524; `Corrections (appended; the freeze section above is not rewritten)` line 3347) and, for round 69, a correction
*row* in the next round's table (line 4726: "C1 tip met=true exit 0 via one correction row").

Harm: the counter's annotation rule needs the correction line appended after the base line count at the end of the same
file. At the file end that line lands under `## Planned — round 73`, a heading that says it declares no claims. That is a
misfiling risk, not a violation of an existing rule. The round-72 rows and the scores (calibration 2, operability 10,
freshness 10, unchanged) are not contradicted by an appended correction.
**Verdict on F9: no C1 verdict change.** Recommended placement (compatible with the counter's rule): a dated block with its
own heading (e.g. `## Correction (appended, round 73) — round-72 pointers`) at the file end, so no planned-section text is over-read.

LOG check for comparison: the LOG file ends inside `## Round 72` (lines 2498 to EOF 2507), so a LOG erratum appended at the
tail stays in the round-72 section. No misfile.

## Residual risk and verification gaps

- Not run: `freshness-sweep --selftest` (C3 predicate); `c73_wave_pointers.py` and `c73_tmp_v3.py` (not yet delivered; the C1 counter's behaviour on the errata is not replicated).
- The F4 re-pin was applied to a scratch clone only; the lane was not touched. The F4 result is one replication on this host.
- F5 and F6 rest on host-state observations today (`test -e`, `stat`, `existsSync`). They describe this host; the note's source host is not in evidence.
- Counter-side check for when the C1 counter lands: an errata line that is itself a `| 72 |` row would contain the dead token it annotates; the counter's self-annotation behaviour is untested here.
