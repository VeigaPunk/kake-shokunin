# ReviewerSourcesFrontier — round-63 frontier-step (§2b) conformance

## Assignment

Review the frontier-step conformance of round 63 (kake lane): census
before/after recorded with commands and exit codes, exactly one sourced claim
resting on a row opened this round (the S432 re-open), the mistake mined, no
registry-cell edits without old→new logging. Name any §2b conformance gap.

Authority: `templates/round-prompt.md` section 2b "Frontier step — every
child-lane round" items 1–4 (`/home/vgpnk/Projects/shokunin/templates/round-prompt.md:42-78`),
reinforced by `PROTOCOL.md:138-145` (frontier step) and `PROTOCOL.md:156-162`
(report "Sources & frontier" section: rows before→after with the counting
command, rows added by tier, rows touched old→new, frontier rows advanced).
Precedent shape: `.ufo/reports/round-62/kake.md:32-64`.

## Verdict

PASS on the three decidable items — the mistake is mined in the required
shape, the registry is provably untouched (old→new logging vacuous), and
exactly one sourced claim (C1) rests on the re-opened S432 row. One open
conformance duty: the round-**end** census is not yet recorded anywhere
observable — the lesson defers it to the round report, which has not been
filed (`.ufo/reports/round-63/` does not exist). That is §2b.2's exit-0
requirement still pending, not a breach: a defect only if the round report
lands without it.

## Evidence

### §2b.2 — census before/after

Round-**start** census is recorded in the lesson with the exact command and
exit code: `corpus/lessons/round-63.md:69` records

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
→ 171 rows, 16 W04 warnings, **exit 0**, dated 2026-10-27 "before any
registry edit".

I re-ran it read-only and it reproduces exactly:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
kake	W04	S033 ... S433	(16 W04 cross-scope duplicate-url warnings)
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
exit=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
171
```

16 W04 lines + `ok` line, exit 0, 171 rows — matches the recorded summary.

Round-**end** census: `corpus/lessons/round-63.md:69` states "The round-end
census output is pasted in the round report." No round-63 lane report exists
yet (`ls /home/vgpnk/Projects/shokunin/.ufo/reports/round-63/` shows only
audio.md, game-dev-2d.md, kotoba.md, kotodama.md, kumitate.md, revenger.md —
no kake.md). The §2b.2 "paste both outputs and their exit codes; exit 0 at
round end" duty is therefore **open, not evidenced**. Since the report lands
last by design, this is a pending duty; the §2b conformance gap is named
below.

### §2b.4 — exactly one sourced claim on a row opened this round

The round has exactly two claims (contract.md: C1 calibration, C2
operability).

- C1 is the sourced claim: its landing evidence
  `corpus/knowledge/response-header-expectations.md:1` cites `S430, S431,
  S432, S433` and the round-63 correction block (`:222-250`) grounds the
  `xcto_nosniff_value` proposition on **S432** with the admitted
  `collapsed-only` span. S432's source was opened this round — the lesson's
  "S432 re-open record" (`corpus/lessons/round-63.md:53-59`) documents a
  dated live GET with a located quote, and the retrieved body is committed at
  `.ufo/waves/round-63/sources/S432.live.html`. Byte-identity to the
  round-61 retained body verifies:

  ```
  sha256 .ufo/waves/round-61/sources/S432.html      = 63b0a018…bad911b
  sha256 .ufo/waves/round-63/sources/S432.live.html = 63b0a018…bad911b  (identical)
  ```

- C2 is a tool-operability claim resting on `scripts/quote_class.py` and its
  selftest — not on a SOURCES row; it is not a sourced claim.
- No other row was opened this round: `git diff
  13d45198..05b0d7f4 -- corpus/SOURCES.md` is empty, and the S432 row
  (SOURCES.md:178) was added in round-61 (`git log -S 'S432'` → d2da25de).
  Reading §2b.4's "row opened this round" as "row whose source was opened
  this round" — the reading the seat item itself takes ("the S432 re-open") —
  exactly one sourced claim rests on it. If "opened" were instead read as
  "row written," zero rows were written and the item would be unmet; the
  re-open record is what makes the former reading honest (dated live GET,
  byte-identical body, located quote).
- Gate decisions for the rejected spans and `considerthese/` items
  (lesson:26-51) stay inside `## Gate`, not in the registry — correct for
  registry candidates under contract v1's "opened rows only" curation.

### §2b.3 — the mistake mined

`corpus/lessons/round-63.md:18-22` `## Mistakes` records the routed
round-62 defect in the required class · evidence · captured-by · fix shape:

- class: `false-green (marker-only counter predicate)`;
- evidence pointer: `.ufo/waves/round-62/controls/counter-false-green-l1.txt`
  plus the round-62 w1 `ReviewerCounterControls` attack — the receipt exists
  and records the old counter's `met=true` on a marker-only fixture;
- captured-by: `none` (explicitly allowed: "the criterion or rule that should
  have caught it, or `none`") — it names the round-60 freeze rule gap;
- fix: the semantics-binding counter plus the committed QUALITY round-63
  criterion (`corpus/QUALITY.md` +4 append at 1413-1416, "A frozen
  calibration counter's `resolved` predicate binds semantic evidence, not
  marker strings").

"A fix counts only once shown able to fail" — shown: the fix is demonstrably
able to fail. `controls/control-marker-fixture.txt` records the same
marker-only fixture printing `met=true` under the old c62 counter and
`met=false` exit 1 under the new c63 counter; `controls/base-c1.txt`
(red-before, exit 1) and `controls/control-junk-fixture.txt` (exit 1) are the
fail sides; `controls/after-c1.txt` records `met=true` exit 0 at the measured
commit. Frozen-counter sha matches the contract
(`bcd16f68…5ea3fc91` for `c63_calibration.py`).

### §2b.1 — registry cells, old→new logging, no-harm

`git diff --name-only 13d45198..05b0d7f4 | grep -cE 'considerthese|merge/|SKILL.md|SOURCES.md'` → **0**.
Zero registry-cell edits means the old→new logging duty is vacuously met;
the lesson records the fact explicitly ("No registry row added or changed;
S432 stays `mined`", :58-59; "No registry cell changed" at
knowledge:249-250). Consistent with the contract no-harm clause (S432
`status`/`recheck`/`used-by` untouched).

## §2b conformance gaps named

1. **§2b.2 pending (open duty):** the round-end census paste with exit code
   exists nowhere yet — the lesson defers it to a report not yet filed. If
   the round report lands without the after-census (or with a nonzero exit),
   that is the conformance defect §2b.2 names ("not a pass"). Watch item for
   whoever reviews the filed report. The start-census record itself is also
   thinner than the r62 precedent (summary + row count vs. full pasted
   output), though my replay confirms every recorded figure — cosmetic, not
   a defect.
2. **Cosmetic precision:** the Gate's re-open record labels the located
   quote "(raw lines 6150–6154, ≤25 words)". The sentence does span retained
   HTML 6150–6154 (verified), but the quoted text is a *collapsed* rendering
   across inline markup, not a raw substring — the same paragraph
   (`lesson:53-59`) and `quote-classes.json` (`locatedRawLines: 6150-6154`,
   note) honestly say `collapsed-only`, so this is labeling looseness, not
   misrepresentation. (QUALITY.md's r62 criterion cites 6151–6154 — both
   ranges cover the sentence, which begins mid-line 6150; no contradiction.)
3. The full PROTOCOL "Sources & frontier" report fields (rows before→after
   with counting command, added by tier, touched old→new, frontier rows
   advanced) are likewise unverifiable until the report exists — same
   pending-duty status as (1), folded into that gap rather than counted
   twice.

## Commands used (all read-only; cwd /home/vgpnk/Projects/shokunin unless noted)

- `git -C kake-shokunin log --oneline -8` ; `git diff --stat|--name-only|-- corpus/SOURCES.md|-- corpus/QUALITY.md 13d45198..05b0d7f4` ; `git log -S 'S432' -- corpus/SOURCES.md` ; `git status --porcelain`
- `grep -n 'S432' corpus/SOURCES.md` ; `grep -rln 'S432' corpus/` ; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`
- `sha256sum .ufo/waves/round-61/sources/S432.html .ufo/waves/round-63/sources/S432.live.html .ufo/waves/round-63/quote-class/S432.txt scripts/quote_class.py .ufo/waves/round-63/c63_calibration.py .ufo/waves/round-63/c63_quote_tool.py .ufo/waves/round-63/quote-class/quote-classes.json`
- `sed -n '6145,6160p' .ufo/waves/round-61/sources/S432.html` ; `grep -n 'destination of a request' .ufo/waves/round-63/quote-class/S432.txt`
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` (replay, exit 0)
- `cat .ufo/waves/round-63/controls/{after-c1,base-c1,control-marker-fixture,control-junk-fixture}.txt` ; `ls .ufo/reports/round-62/ .ufo/reports/round-63/` ; `grep -n -B2 -A30 'Sources' .ufo/reports/round-62/kake.md`

No installs, no fixtures, no mutations; only this report was written.

## Confidence and remaining unknowns

High on every decidable item: the empty SOURCES.md diff and the
sha256-verified blob identity are dispositive. Unknowns: whether the round
report will carry the after-census at exit 0 (the one open conformance duty),
and whether the round-63 non-author closure agrees the author-side gate
decisions — the lesson itself defers that correctly.
