# ExecC1Repair — C1 SKILL.md tree-path repair (round 94, wave w1)

VERDICT: C1 counter reads mismatches=0 pins=ok battery=8/8 predecessor_admits=7/7 met=true, exit 0, at committed clone revision `06df6c624777bb084936af87af49c941530888a0`; the 15 base E5 findings are repaired in place, all 255 rows and first cells kept.

## Godspeed axes

1. **C1 mismatch count** (owned axis): 15 → 0.
2. **Row truthfulness**: each repaired token now names a concrete non-empty blob the row's entry actually describes, verified present at the measurement revision with `git cat-file -s` before the edit.
3. **Pin stability** (harm check): rows=255, first cells, identity surfaces (`frozen/c1-surfaces.json`, lessons 88 / entries 81 / criteria 39) unchanged — pins=ok on every run.

No move improved one axis while harming another; all three receipts are kept as evidence.

## Base control (re-measured on this host before editing)

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-94/c94_selfassess.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision 0f7d9bbcdd6a9ed36f5bc62b2116ddd040e871a8 --skip-battery \
  --work /fast/scratch/hyaku/kake-r94/ExecC1Repair/work-base
```
Exit 1; line 1 matched the frozen control `controls/base-c1.txt` field-for-field:
`mismatches=15 E1=0 E2=0 E3=0 E4=0 E5=15 pins=ok … met=false`; counter digest `58028584f1aab19a294d24147854f56a703b2442f5af2d32fed69a5a87a8306a` (equals the freeze's instrument sha). All 15 findings were E5 "names a tree, not a blob" over 12 distinct paths (`.ufo/waves/round-85/w1/ExecRegistry/` ×3).

## Repair table (15 repairs across 14 rows of SKILL.md)

| SKILL.md line | Row first cell | Old token | New token | Why this file is the one the row means |
|---|---|---|---|---|
| 617 | citing-set | `scripts/fixtures/citing-set/` | `scripts/fixtures/citing-set/01-single-literal-clean/expected.json` (34 B) | The row's self-test delegates the fixture runner over the case tree; `expected.json` is the per-case oracle the row's own next cell describes ("fixed exits/finding ids") and the one this SKILL.md prose (round-56 section) documents as the case's expectation file. Case 01 is the tree's first case. |
| 720 | base-path drift row | `.ufo/waves/round-29/real-input/out/` | `.ufo/waves/round-29/real-input/out/summary.json` (950 B) | The sentence is about the round-29 real-input run's finding record ("all 4 findings … three owned project sites"); `summary.json` is the run's aggregate and carries exactly those finding counts (charter-ghp 3 + lucario-ghp 0 + plazir15-ghp 1 = 4, verified by reading the blob). |
| 726 | base-path-audit | `scripts/fixtures/base-path/` | `scripts/fixtures/base-path/D1-root-relative-stylesheet/expected.json` (325 B) | Representative of the "30 matrix fixtures" the row counts; D1 is the matrix's first case and its `expected.json` is the per-case oracle the selftest compares ("exit, verdict and reason tuples"). |
| 1046 | link-preview-audit | `scripts/fixtures/link-preview/` | `scripts/fixtures/link-preview/canonical_first_mismatch/expected.json` (104 B) | Representative of the "45 fixture directories"; first directory in the tree listing at the measurement revision, oracle file of the same kind the row compares. |
| 1253 | selftest-tally-counter | `scripts/fixtures` (bare) | `scripts/fixtures/quote-class/inline.raw.html` (52 B), named as "first" of the four | The row's cause is "four `quote-class` fixture files gained … (round-63 commit `6d8c52a6`)"; `git diff-tree -r --name-only 6d8c52a6` returns exactly `inline.raw.html`, `inline.txt`, `markup.raw.html`, `markup.txt`. The first of those four is named; the four-file count and commit stay in the sentence. Minimal glue: dropped "tree" after the (removed) token and appended ", first `<file>`" inside the existing parenthetical. |
| 1254 | yahoo-crawl-handling-quote-truth-counter | `.ufo/waves/round-56/sources/` | `.ufo/waves/round-56/sources/S367.html` (8051 B) | The same cell pins the held-row body digest "HELD_BODY_SHA256 (S367)"; S367.html is that retained body. Glue: "bodies" → "body" for agreement with one named file; "with `receipts.json`" kept. |
| 1350 | canonical-crawler-identity-quote-truth-counter | `.ufo/waves/round-51/` | `.ufo/waves/round-51/sources/receipts.json` (909 B) | The cell already names "retained bodies and `sources/receipts.json` under" the directory; the concrete blob that binds those bodies is that receipts.json. Glue: merged the relative name and the directory into one full blob path ("adopted ids S262 and S263 with retained bodies and `.ufo/waves/round-51/sources/receipts.json`"). |
| 1359 | response-snapshot | `.ufo/waves/round-61/capture/` | `.ufo/waves/round-61/capture/manifest.json` (5125 B) | The row's own pinned cell says this manifest "binds 12 receipt paths"; it is the file that describes the 12-receipt population the sentence claims re-readable. Glue: "under" → "bound by" so the sentence stays true with a file token. |
| 1431 | c73_wave_pointers.py | `.ufo/waves/round-72/` | `.ufo/waves/round-72/controls/c56-pin-linux.txt` (712 B), as "the tree holding …" | The predicate is "token resolves under the round-72 tree"; `c56-pin-linux.txt` is an actual `controls/`-class token cited by the selftest-tally-counter row (line 1253), i.e. a live instance of exactly the token class this gate checks. Glue: "resolves under `DIR`" → "resolves under the tree holding `FILE`". |
| 1506 | scripts/x_robots_tag_audit.py (round-80 grammar) | `.ufo/waves/round-80/cases` | `.ufo/waves/round-80/cases/c32/manifest.json` (248 B) – `.ufo/waves/round-80/cases/c43/manifest.json` (252 B) | The 12-case amendment set is the twelve case manifests c32…c43 in that directory (ls-tree: exactly 12 dirs, one manifest.json each). The first–last blob range keeps the set description exact; en-dash range follows the row's own `X01`–`X15` idiom. |
| 1535 | c84_defect_queue.py | `.ufo/waves/round-85/w1/ExecRegistry/` | `.ufo/waves/round-85/w1/ExecRegistry/selftest-defect-queue.json` (728 B) | That receipt's `argv` is `python3 -B .ufo/waves/round-84/c84_defect_queue.py --selftest` — the execution receipt of this row's tool. Glue: "`DIR` execution receipts" → "execution receipt `FILE`". |
| 1536 | c84_policy_values.py | `.ufo/waves/round-85/w1/ExecRegistry/` | `.ufo/waves/round-85/w1/ExecRegistry/selftest-policy-values.json` (441 B) | Receipt `argv` = `c84_policy_values.py --selftest` — this row's tool. Same glue. |
| 1537 | policy_value_class.py | `.ufo/waves/round-85/w1/ExecRegistry/` | `.ufo/waves/round-85/w1/ExecRegistry/selftest-policy-value-class.json` (397 B) | Receipt `argv` = `scripts/policy_value_class.py --selftest --work …` — this row's tool. Same glue. |
| 1539 | count.py (round 85) | `.ufo/waves/round-85/controls/` | `.ufo/waves/round-85/controls/base-c1.txt` (230 B) | The row measures claims c1/c2 and its selftest cell stresses "controls are explicitly separate"; `base-c1.txt` is claim c1's base control in that directory. |
| 1588 | c87 finite claims | `.ufo/waves/round-87/{expected-ledger.json,age-cases.json,snapshots/}` | `.ufo/waves/round-87/{expected-ledger.json,age-cases.json,snapshots/round-86-verifier-spotcheck.md}` (8482 B) | The mismatch was the brace-expanded `snapshots/` member; the directory holds three verifier-spotcheck snapshots and the newest (round-86) is named. The other two brace members were already blobs. |

Every new token was verified a non-empty blob at the measurement revision before editing (`git cat-file -s ba667b24:<path>`, sizes in the table). No row was deleted or added; no first cell changed; no other file touched. The working-tree diff (`skill.diff`, 56,113 bytes) contains exactly 15 removed + 15 added lines.

## After-state measurement (the round's counting commands, clone-committed revision)

Fixture protocol per seat spec: `git clone -q --shared /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r94/ExecC1Repair/clone`; `git -C <clone> rev-parse --show-toplevel` printed exactly the clone path **before** the first commit; commit made only inside the clone (identity `ExecC1Repair fixture <ExecC1Repair@fixture.invalid>`); no git mutation anywhere in LANE.

```
REV=06df6c624777bb084936af87af49c941530888a0
python3 -B .ufo/waves/round-94/c94_selfassess.py --root <clone> --revision $REV \
  --skip-battery --work /fast/scratch/hyaku/kake-r94/ExecC1Repair/work   # SKIP_EXIT=0
python3 -B .ufo/waves/round-94/c94_selfassess.py --root <clone> --revision $REV \
  --work /fast/scratch/hyaku/kake-r94/ExecC1Repair/work                  # FULL_EXIT=0
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff -- SKILL.md > skill.diff  # DIFF_EXIT=0
```

Receipts (all under `.ufo/waves/round-94/w1/ExecC1Repair/`):

- `after-c1-skip.txt` — line 1: `… counter=58028584… lessons=88 entries=81 rows=255 criteria=39 mismatches=0 E1=0 E2=0 E3=0 E4=0 E5=0 pins=ok … met=true`, exit 0.
- `after-c1-full.txt` — line 1: same plus `battery=8/8 predecessor_admits=7/7 floor=2 self_pin=ok met=true`, exit 0 (7/7 ≥ floor 2). Battery detail: F1 shadow-subprocess refused (self_rc 2, "shadowed"), F2 canned wrapper refused (true digest absent), F3–Fv all refused; predecessor admits 7/8 fixtures.

Acceptance met: `mismatches=0` with `pins=ok` on the skip run; `battery=8/8` and `predecessor_admits=7/7 ≥ 2` on the full run; no row was left unrepaired, so no honest-unmet clause applies.

## Findings and honest limits

1. **Counter scope (finding, not edited):** the E5 predicate scans only SKILL.md lines that start with `|`. Prose occurrences of the same directory references remain in SKILL.md (e.g. the round-27/56 sections' "over `scripts/fixtures/citing-set/`" prose sentences, the round-29 §paths prose). The frozen counter does not audit prose, and the seat spec scoped my edits to the flagged table rows, so I left prose untouched. A future counter version could widen the surface to all lines; that is a contract change, not a round-94 repair.
2. **Population vs representative:** five repaired tokens named populations, not single files (citing-set cases, base-path 45-fixture matrix, link-preview 45 fixtures, the four quote-class files, the 12-case round-80 set, the round-87 snapshots set, the 12 round-61 receipts). Where the population has a natural single descriptor, the row now names that descriptor (round-29 `summary.json`, round-61 `manifest.json`, round-51 `sources/receipts.json`); where it has not, the row names one concrete member (or first–last range for the 12-case set) and keeps the population count in its prose. The rows remain true as written; the counter's blob requirement is satisfied. This is the seat spec's sanctioned "representative file" choice.
3. **Wording glue inventory (all inside the repaired sentence, nothing else):** "under"→"bound by" (1359); "bodies"→"body" (1254); "tree" dropped and ", first `<file>`" added inside the existing parenthetical (1253); "under `DIR`"→"under the tree holding `FILE`" (1431); relative+directory mention merged into one absolute blob path (1350); "`DIR` execution receipts"→"execution receipt `FILE`" (1535–1537).
4. **No row turned out unrepairable:** every flagged directory had a blob its row's meaning could name; the open-finding clause of the seat spec was not needed.
5. **Instrument digests:** the counter's own sha256 printed on all three runs equals the freeze's `c94_selfassess.py` digest `58028584…`; surfaces digest drift check passed implicitly (no Unevaluable raised). No defect observed in the frozen instruments beyond finding 1's scope note.
6. **Read-first compliance:** freeze.md, QUALITY.md (first 300 lines; the file is 1809 lines — I read the admission criteria relevant to receipts and append-only rules), PROVINCE.md (first 300 lines), SOURCES.md registry contract tail plus rows S471–S476 (RFC 9110 §13 conditional-request rows and RFC 9111 §4.3.2 — C2's grounding, context only for this seat).
7. **Tooling record:** no tools installed or upgraded (nothing needed; pacman paused host-wide per orchestrator ruling 2026-10-20, and uv/npx were unnecessary). No sysctl or service changes. No network access (all evidence local; GET authorization unused).
8. **Scratch:** `/fast/scratch/hyaku/kake-r94/ExecC1Repair/` (clone, work dirs) deleted before yielding; all citable receipts were first written under `.ufo/waves/round-94/w1/ExecC1Repair/`. No `/tmp` writes.
