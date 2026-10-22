# ScribeCarriedOpenNames — round-33 C2 counter hollow shapes, named and re-marked against round-34

Scope: named every hollow/escape shape in the three round-33 artifacts and marked each against
`.ufo/waves/round-34/c2_source_census.py`. No counter run, no product edit, no lane mutation beyond this report.
Counter content probed: sha256 `ee7461b9e3a33949174591c527ccbf2854ca178c41638f71b5128cbd57e5f892` (equals the lane file).

## Commands (all in /fast/scratch/hyaku/kake-r34/w1/ScribeCarriedOpenNames/)
- `cp .../round-34/c2_source_census.py ./c2_copy.py && sha256sum` — exit 0; hashes equal (above).
- `cp .../round-33/c2_pin_count.py ./r33_copy.py` — exit 0 (inside probe run).
- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=$PWD/tmp; python3 -B probe_shapes.py; echo exit=$?` — exit 0.
- Observed: `P1 r34 section_lines: ['| S067 | first |', '| S068 | second |']` / `P1 r33 section: (None, 2)`;
  `P2 r34: ['| S067 | first |', '```']`; `P3 r34: ['```', '| S900 | junk |']`;
  `P4 r34 cells=12 cells[7]='c5' cells[8]='2026-10-22' >=11=True` vs `P4 r33 cells=11 rendered[8]='queued'`;
  `P5 tree-regex mode accepted: 100755`; `P6 ValueError: Exceeds the limit (4300 digits)...`;
  `P7 next(): | S067 | https://x/S067 |`.
Pointer key: M = `.ufo/waves/round-33/w1/MutC2HollowCommit.md`, R = `.ufo/waves/round-33/w1/ReviewC2CounterCode.md`,
T = `.ufo/waves/round-33/w2/MutC2CounterAtTip.md`, C33 = `.ufo/waves/round-33/c2_pin_count.py`, C34 = `.ufo/waves/round-34/c2_source_census.py`.

## Shapes and marks
| # | Short name | One-line description | Origin | r34 |
|---|---|---|---|---|
| 1 | junk-row | Row passes on 11 parsed cells plus source-substring, status, date; no kind/tier/scope/anchor/taught-fact check | M:26; C33:119-126 | CARRY: C34:215-218 (`>=11` cells; used-by check C33:126 dropped) |
| 2 | copied-metrics | Exact stated numbers are indistinguishable from independently derived ones | M:27; C33:150-154 | CARRY (residual): C34:144-186,236 re-derives, so equality certifies arithmetic, not study |
| 3 | misplaced-section | Evidence accepted anywhere in the entry, only one exact heading required | M:28; C33:71-81 | CARRY (expanded): C34:208,219,234 — no heading required for the entry at all |
| 4 | escaped-pipe | Escape parity ignored; cell indices diverge from the rendered table | M:19, M:29; C33:119 | CARRY (regressed): C34:216 naive `.split("|")`; r33's `(?<!\\)\|` is gone (P4) |
| 5 | duplicate-heading | Duplicate section headings merge silently instead of failing | M:30; C33:73-75 | CARRY (regressed): C34:95-96 no uniqueness count (P1); line uniqueness at C34:221,235 limits blast radius |
| 6 | full-score-hollow | Fabricated row + copied metrics + one copied quote can reach full score | M:5, M:16 | CARRY: no C34 condition binds registry row or prose to source study; C34:219,224-228 only prove a substring of retained bytes |
| 7 | duplicate/decoy-row | More than one matching registry row is silently resolved, not rejected | R:9; C33:120-123 | CARRY: C34:215 `next()` takes the first match, no count (P7) |
| 8 | fence-blind-heading | A fenced literal `## Registry` opens the section window | R:10; C33:73 | CARRY: C34:95-101 has no fence state (P3); r33's duplicate count failed closed |
| 9 | fence-truncation | Any `## ` line, even fenced, closes the section window | R:12; C33:78 | CARRY: C34:95 (P2); entry evidence is exempt via C34:208 + 103-117 |
| 10 | path-blind-bytes | Retained bytes not bound to their exact path | R:13; C33:101-107 | AVOID: C34:168-169 exact path-set equality; C34:172-173 per-path blob hash |
| 11 | mode-blind-bytes | Retained blob mode not constrained to 100644 | R:14; C33:107 | CARRY (regressed): C34:152 captures six digits but never compares them (P5) |
| 12 | anywhere-cite | Source id cited outside the intended evidence context | R:15; C33:132-135 | CARRY (weakened): C34:219 word-boundary but no section anchor; intro excluded by C34:208 |
| 13 | non-utf8-crash | Strict decode turns non-UTF8 input into exit 1 with no JSON | R:19; C33:68 | AVOID: C34:147,175,199-201,225 decode with `errors="replace"`; receipts parse guarded C34:203-206 |
| 14 | bigint-crash | Oversized stated integer raises ValueError, uncaught | R:20; C33:154 | CARRY: C34:235 `int()` over `\d+` (C34:66); 5000 digits raise (P6) |
| 15 | substring-cite | Citation matched as substring, not identity | R:21; C33:126,135 | SPLIT: id cite AVOIDED by `\b` at C34:219; source URL still substring at C34:217-218 |
| 16 | heading-whitespace | Trailing space on an ATX heading defeats the match | R:22; C33:73 | AVOID: C34:96 compares `line.strip()` |
| 17 | unhandled-parse | Malformed retained input crashes the counter | R:23; C33:150 | AVOID for the archive (C34:158-166 catches LZMA/Tar/OS/EOF); the surviving unhandled conversion is shape 14 |
| 18 | self-consistent-pair | Census "byte-exactness" is exact only against the retained listing; receipt chain is self-attested | derived from M:5 | CARRY (new site): C34:148 only string-matches `commit <COMMIT>`; C34:152-173 check the archive against that same listing; C34:226-227 prove text == its own committed receipt |

T (MutC2CounterAtTip) names no hollow/escape shape: seven single-field mutants (sitemap byte, mode, status, date,
heading suffix, loc count, verdict) were all killed with `met<4`, and the report itself says
"No mutation survived or was inconclusive." It corroborates field sensitivity at tip only.

## Draft for corpus/lessons/round-34.md (sandbox copy: draft-lesson-carried-open.md)
**Carried open — round-33 C2 counter shapes.** The round-34 C2 counter inherits six of the round-33
hollow shapes and regresses three closed ones, all in the registry/entry layer rather than the retained-bytes
layer:
- junk-row (C34:215-218): cells[0]/cells[1]-substring/cells[7]/cells[8] only; the round-33 used-by check is gone.
- duplicate-row and duplicate-heading (C34:215 `next()`; C34:95-96): ambiguity resolved silently, not rejected.
- fence-blind sections (C34:95-101): a fenced `## Registry` opens the window and a fenced `## ` closes it.
- escaped-pipe (C34:216): naive split plus `>= 11` cells, so checked indices need not be rendered columns.
- anywhere-cite (C34:208,219): source citations have no required section, only a position after line 8.
- bigint-crash (C34:235): an oversized census integer still aborts with no JSON.
- self-consistent-pair (C34:148-173,226-227): archive == listing == its own first line, and text == its own
  committed receipt; nothing binds either to upstream or to the live URL. This is round-33's full-score-hollow shape
  (M:5,16) at a new site, so `met=5/5` cannot certify that a human read the pages.
Avoided and worth keeping: path-set and per-path blob equality (C34:168-173), `errors="replace"` reads
(C34:199-201), whitespace-tolerant heading match (C34:96), word-boundary id cite (C34:219), archive exception
handling (C34:158-166). Mode is captured but unchecked (C34:152), so a 100755 retained blob still passes.

## Not verified
- No counter run and no full-score hollow commit was constructed for round 34; marks 1-18 rest on code reading plus
  the function-level probes above, not on a fabricated manifest. Anything about the retained ds4cc archive, receipts
  or upstream identity is outside this seat and unobserved here.
- `unfenced()` behavior on nested or indented fences, and `urljoin`/`Head` behavior on malformed HTML, were not
  exercised. No tool installed.
