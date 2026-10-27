# ScribeScorecard — round-63 SCORECARD.md block draft

## Assignment

Draft the SCORECARD.md round-63 block: per-claim rows (axis, before → after,
counting command, verdict, evidence pointers) in the round-61/62 style, plus
any planned-row update. Facts only from committed files. Lane: leaf seat, no
commit, no push, no subagent dispatch, read-only against the fleet root.

Measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`; base
`13d4519818db28cd0aa912e49020659140d7b9fa`. SCORECARD.md currently ends at
line 4531 with the round-62 block; the draft below is an append after that line.

## Deliverable — draft block (append after SCORECARD.md:4531)

```markdown
## Round 63 — declared and measured claims

Contract `.ufo/waves/round-63/contract.md`; base
`13d4519818db28cd0aa912e49020659140d7b9fa` (round-62 tip); measured commit
`05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`. Counters and tool frozen before any
after-state measurement: `.ufo/waves/round-63/c63_calibration.py` sha256
`bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91`,
`.ufo/waves/round-63/c63_quote_tool.py` sha256
`9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e`,
`scripts/quote_class.py` sha256
`431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14`, and the
class ledger `.ufo/waves/round-63/quote-class/quote-classes.json` sha256
`5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d`.
C1 repairs the round-62 falsified counter family and works calibration (the
lowest scored owned axis, 2); C2 lands the quote-class tool and works
operability (HOLD 10). Score deltas: none — operability and freshness stay 10
and calibration stays 2, because admission of the calibration move belongs to
the non-author closure (round-62 precedent), so this block records the
author-side measured verdicts only.

| Claim | Axis / delta | Before → after | Counting command | Verdict |
|---|---|---|---|---|
| Repair the round-62 falsified counter family so every `resolved` component re-derives from committed bytes, and resolve the round-61 S432 disagreement as a `collapsed-only` span with a committed class ledger | calibration 2→2 (HOLD) | Base `13d45198`: `disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false`, exit 1 → measured `05b0d7f4`: `disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true`, exit 0. The disagreement count stays 1: the round-61 spot-check `Disagree` line is kept and resolved, not erased. `criterion` was already 1 at base, so the measured delta sits in `quote_correction` / `blobs_match` / `class_match` / `lesson_gate`. | `python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` | met (author-side; receipt `.ufo/waves/round-63/controls/after-c1.txt`). Red controls: the committed marker-only fixture prints `met=true`, exit 0 under the old c62 counter and `met=false`, exit 1 under c63 (`controls/control-marker-fixture.txt`, the routed defect `.ufo/waves/round-62/controls/counter-false-green-l1.txt`); adversarial markers with no retained blobs print `met=false`, exit 1 (`controls/control-junk-fixture.txt`); base prints `met=false`, exit 1 (`controls/base-c1.txt`). |
| The committed quote-class tool passes its four frozen selftest cases at the measured revision, deriving the same class C1 re-derives inline | operability 10→10 (HOLD) | Base `13d45198`: `present=0 selftest=unevaluable met=false`, exit 1 → measured `05b0d7f4`: `present=1 selftest=4/4 frozen_cases=ok met=true`, exit 0 | `python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` | met (receipt `.ufo/waves/round-63/controls/after-c2.txt`). Frozen case ids `inline_raw_substring`, `markup_collapsed_only`, `absent_everywhere`, `s432_real`; the stub-tool branch is code-enforced (`.ufo/waves/round-63/c63_quote_tool.py:77-85` requires all four ids present, `passed`, and `derived == expected`, with `total == passed == 4`) and has no separate committed stub-control receipt. |

Receipts `.ufo/waves/round-63/controls/`: base `base-c1.txt`, `base-c2.txt`
(both committed at `6d8c52a6`, before the measured commit); after `after-c1.txt`,
`after-c2.txt` (committed at `7f77d12b`, after `05b0d7f4`); C1 fixtures
`control-marker-fixture.txt`, `control-junk-fixture.txt`. The round-62 routed
defect receipt `.ufo/waves/round-62/controls/counter-false-green-l1.txt` and the
old `c62_calibration.py` stay committed as defect history.

No-harm: the only `corpus/` changes base → measured are appends —
`corpus/QUALITY.md` +4 lines (round-63 criterion), `corpus/knowledge/response-header-expectations.md`
+29 lines (the `[r63-correction 2026-10-27]` block, below the round-62 held
correction, which is preserved verbatim), and new `corpus/lessons/round-63.md`
+69 lines. `corpus/SOURCES.md` is byte-identical base → measured: no registry
row added or changed, and the S432 row (`corpus/SOURCES.md:178`) keeps
`status=mined`, `recheck=2026-10-27` and its existing used-by cell.
Separability holds in code: `c63_calibration.py` never reads `scripts/quote_class.py`
(its own `classify()` at `:62-68`), and `c63_quote_tool.py` reads only the tool
and its selftest.
```

### Planned-row update

None applicable, and the draft adds none. SCORECARD.md contains no round-63
planned block to revise: `grep -n -i "round 63\|round-63\|r63" SCORECARD.md LOG.md`
returns nothing, and the newest planned sections are `## Planned` (round 21,
line 21), `## Planned — round 48` (line 3989) and `### Planned — round 49`
(line 4047). A round-63 block appended at line 4531 therefore needs no
planned-row edit.

### Capability-row question (not asserted)

Optionally, the closure may enter a capabilities row for `scripts/quote_class.py`
(new at `05b0d7f4`, sha256 `431e75e8…1f14`, selftest 4/4). Draft, if wanted:

```markdown
| Quote-class derivation tool | Reports whether a cited span is a raw substring of a retained body (`raw-substring`), survives only as a rendering of it (`collapsed-only`), or is `absent`, deriving the class from both committed blobs at a revision (`git show`) rather than asserting it, with a four-case selftest whose case set the round-63 counter pins | `scripts/quote_class.py` at `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14`; `python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` → `present=1 selftest=4/4 frozen_cases=ok met=true` exit 0 (`.ufo/waves/round-63/controls/after-c2.txt`); base `present=0 met=false` exit 1 (`controls/base-c2.txt`) | 63 |
```

Two precedents conflict, so this is a judgment, not evidence: round 61 added a
capability row for its new tooling, while round 58 explicitly added none because
its C2 deepened an existing capability. The round-50 row "Quote-class ledger for
cited source spans" already covers the *ledger*, but its evidence pointer is
`.ufo/waves/round-50/quote-classes.json` plus the round-50 counter, not a
reusable `scripts/` tool.

## Facts verified from committed files

Repo `/home/vgpnk/Projects/shokunin/kake-shokunin`, worktree clean at the
measured tree except untracked wave inputs (`.ufo/waves/round-63/w1*`).

```
$ sha256sum .ufo/waves/round-63/c63_calibration.py .ufo/waves/round-63/c63_quote_tool.py scripts/quote_class.py .ufo/waves/round-63/quote-class/quote-classes.json
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
```

All four match the contract's frozen digests.

Retained blobs (the ledger's pinned bytes re-hash to what the ledger records):

```
$ sha256sum .ufo/waves/round-63/quote-class/S432.txt .ufo/waves/round-61/sources/S432.html .ufo/waves/round-63/sources/S432.live.html
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .ufo/waves/round-63/quote-class/S432.txt
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-63/sources/S432.live.html
```

`8b90d096…2a69` = the ledger's `textSha256`; `63b0a018…911b` = its `rawSha256`
and also the live re-fetch body, which is byte-identical to the round-61
retained body (both 1,854,393 bytes). Direct membership test of the frozen
sentence (curly apostrophe, exactly as in `c63_calibration.py:51-55`):

```
$ python3 - <<'EOF'   # read-only
q="The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request."
print('in_text', q in open('.ufo/waves/round-63/quote-class/S432.txt').read(), 'in_raw', q in open('.ufo/waves/round-61/sources/S432.html').read())
EOF
in_text True in_raw False
```

That is the `collapsed-only` class the after receipt prints as `derived=collapsed-only`.

Base → measured change set (19 files, +19669/-0):

```
$ git diff --stat 13d4519818db28cd0aa912e49020659140d7b9fa 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
 ... c63_calibration.py 177, c63_quote_tool.py 92, contract.md 89, controls/{base-c1,base-c2,control-junk-fixture,control-marker-fixture}, quote-class/{S432.txt,extract_text.py,quote-classes.json}, sources/S432.live.html 18915, corpus/QUALITY.md 4, corpus/knowledge/response-header-expectations.md 29, corpus/lessons/round-63.md 69, scripts/fixtures/quote-class/4 files, scripts/quote_class.py 147
$ git diff --numstat 13d45198..05b0d7f4 -- corpus/
4	0	corpus/QUALITY.md
29	0	corpus/knowledge/response-header-expectations.md
69	0	corpus/lessons/round-63.md
$ git diff --name-only 13d45198..05b0d7f4 | grep SOURCES || echo "SOURCES.md untouched"
SOURCES.md untouched
$ grep -n "^| S432 " corpus/SOURCES.md
178:| S432 | WHATWG Fetch — https://fetch.spec.whatwg.org/ | spec | A | ... | mined | 2026-10-27 | 180d | corpus/knowledge/response-header-expectations.md |
```

Receipt contents (verbatim, exit lines included):

- `controls/base-c1.txt`: `revision=13d45198… disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false` / `exit=1`
- `controls/after-c1.txt`: `revision=05b0d7f4… disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true` / `exit=0`
- `controls/base-c2.txt`: `revision=13d45198… present=0 selftest=unevaluable met=false` / `exit=1`
- `controls/after-c2.txt`: `revision=05b0d7f4… present=1 selftest=4/4 frozen_cases=ok met=true` / `exit=0`
- `controls/control-marker-fixture.txt`: fixture rev `7833be88…`, old c62 → `… unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true` / `exit=0`; new c63 → `… quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 unresolved=1 met=false` / `exit=1`
- `controls/control-junk-fixture.txt`: fixture rev `7da479c2…` → `… quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false` / `exit=1`

Counter logic actually read (not inferred from receipts): `resolved =
quote_correction and criterion and lesson_gate and source_row`
(`.ufo/waves/round-63/c63_calibration.py:164`); `quote_correction` requires the
`[r63-correction` block, the frozen sentence and the ledger path in the
knowledge file (`:121-127`), ledger sha256s re-derived from `git show` blobs
(`:133-139`), and `class_match` requiring `derived == "collapsed-only" ==
row["matchClass"]` (`:142-143`); `classify()` is inline at `:62-68` and the file
never opens `scripts/quote_class.py`. C2's `met` requires `ok`, all four frozen
cases `passed` with `derived == expected`, and `total == passed == 4`
(`.ufo/waves/round-63/c63_quote_tool.py:77-85`); the tool's own four case ids
are at `scripts/quote_class.py:42,49,56,63`.

Commit order (facts, not a freeze audit):

```
13d45198 2026-10-27 09:54:45 -0300  round-62 verifier spot-check (base)
6d8c52a6 2026-10-27 10:18:15 -0300  freeze contract; counter; tool; correction
05b0d7f4 2026-10-27 10:19:30 -0300  measured commit
7f77d12b 2026-10-27 10:19:59 -0300  green-after receipts at measured commit
15eb965c 2026-10-27 10:24:56 -0300  w1 wave spec + dispatch (64 seats)
```

`base-c1.txt` / `base-c2.txt` / both control fixtures were added by `6d8c52a6`.

## Flags — not verified, or verified only in the weaker sense

1. **Stub-tool control has no committed receipt.** The contract's C2 kill rule
   names stub rejection; `controls/` holds only `base-c2.txt` and `after-c2.txt`
   for C2. The branch is verified by reading the frozen counter at
   `c63_quote_tool.py:77-85`, not by a receipt. `ExecStubControl` /
   `ExecC2CounterAttack` own the fixture evidence; the draft says
   "code-enforced" and must not be upgraded to "control receipt".
2. **No score-delta rule is written in SCORECARD.md.** "Calibration stays 2
   pending the non-author closure" is `[INFERENCE]` from the round-62 block
   ("admission belongs to the non-author closure") and the round-60/61 pattern;
   no committed file states a rule for who may move the calibration score. If
   the closure rules otherwise, only that sentence changes.
3. **Capability row is offered, not claimed.** See "Capability-row question"
   above; round-58 and round-61 precedents conflict.
4. **I did not re-run either counter.** The before/after numbers above are the
   committed receipts plus a read of the counter source; independent re-runs
   belong to `ExecCounterRerun` / `ExecReceiptReproduce`. Nothing in the draft
   depends on my own execution of the counters.
5. **`criterion=1` at base.** The criterion component was already green at the
   base revision, so the C1 row's delta is in `quote_correction`, `blobs_match`,
   `class_match`, `lesson_gate`. A skeleton that prints only `met` would hide
   this; the draft prints the full field line for both revisions.
6. **`disagreements=1` after the fix.** The counter reports the spot-check
   `Disagree` line at both revisions and sets `unresolved=0` only because
   `resolved` is true. The draft states this so the block cannot be read as
   "the disagreement disappeared".
7. **Round-63 adds no registry row** (S432 pre-existed at `mined`), so the
   block claims no freshness movement and no census delta. Census receipts for
   this round, if any, belong to the report's Sources & frontier section
   (`ScribeReportSources`, `ScoutCensusState`), not to this block.

## Touched surfaces / out of scope

- Written: this report only
  (`.ufo/waves/round-63/w1/ScribeScorecard.md`). No fleet-root tracked file,
  no `scripts/`, no `.ufo/state`, no `considerthese/`, no `MANIFEST.json`, no
  commit/push/jj, no scratch fixture, no install.
- Read-only reads of SCORECARD.md, LOG.md grep, the contract, the two counters,
  `scripts/quote_class.py`, the ledger, both retained S432 blobs, the before/after
  and control receipts, `corpus/knowledge/response-header-expectations.md`,
  `corpus/QUALITY.md`, `corpus/lessons/round-63.md`, `corpus/SOURCES.md:178`,
  `w1-spec.json`, and the peer report `.ufo/waves/round-63/w1/ScoutAppendOnly.md`.
- Out of scope by lane bounds and left to their owners: LOG.md entry
  (`ScribeLog`), report Work/Measurements/Sources sections, counter re-runs,
  fixture attacks, mutation tests, append-only tool verification, and any
  judgement on the S432 semantic-support question.
