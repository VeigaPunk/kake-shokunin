# ScribeSkillRegistry

Measured at lane HEAD `143e592938967ac6a1eb7d9e6f7055bde5b59ed4` (worktree dirty with sibling
`w1/*.md` reports only). Counters read: `.ufo/waves/round-55/c55_readme_index.py`
(sha256 `dfa4b37083dc3bc437daffac1db56428627c6013096d980b15dc69956f444660`),
`.ufo/waves/round-55/c55_quote_truth.py`
(sha256 `f27acce8e935115008f414cb04af9906e2ef9662f912ba32b42aeac05ebac477`). No file outside this
report was written; no git or jj mutation; no tool installed (nothing needed).

SECTION:

```markdown
### Round 55 gate registry additions

Round 55 ships two counters whose predicates are frozen in `contract.json` before any data. This
section registers both at the registry home in the round-52 cell schema; both are offline and read
committed bytes only. Receipts: `.ufo/waves/round-55/controls/`.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| readme-index-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision <commit>` | `0=met` (`index_mismatches == 0 AND knowledge_files >= 46`); `1=not met` (any unindexed, thin or dangling item, or `knowledge_files < 46`); `2=could-not-evaluate` (`corpus/README.md` or the tree unreadable at the revision, or no `## Coverage map` section); `64=usage` (declared in the docstring; `ap.error` exits 2, so usage and could-not-evaluate share exit 2) | `python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest` (10 fixtures, generated sandbox repos; receipt `.ufo/waves/round-55/controls/c1-selftest.txt`, 10/10) | `.ufo/waves/round-55/contract.json` `claims.C1.predicate` carries the predicate sentence (the counter does not read the file; it holds `PREDICATE` and `FLOOR = 46` inline); base control `.ufo/waves/round-55/controls/base-c1-readme-index.txt`: `index_mismatches=21 knowledge_files=46 met=False`, exit 1 at `fcaf4b85…`; `FLOOR = 46` is the deletion guard | none in the repo: read-only `git show` and `git ls-tree`; `--selftest` writes only throwaway repos under `tempfile.mkdtemp` and removes them | kake |
| yahoo-robots-quote-truth-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root . --revision <commit>` | `0=met` (`conditions_passed == 8 of 8`); `1=not met` (any C1–C8 sub-condition fails); `2=could-not-evaluate` (missing or malformed receipt, mirror-pin or census evidence, or an exception); `64=usage` (declared in the docstring; `ap.error` exits 2, so usage and could-not-evaluate share exit 2) | `python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` (30 fixtures, sandbox repos built from the committed round-55 evidence at `HEAD` or `KAKE_R55_SELFTEST_REV`; no receipt committed yet) | `.ufo/waves/round-55/contract.json` `claims.C2` freezes the eight conditions; `.ufo/waves/round-55/sources/receipts.json` pins each retained body (sha256, bytes, integer `httpStatus` 200, `fetchedAt` on the round date) and C6 requires the receipt URL to equal the row URL; `.ufo/waves/round-55/assimilation/mirror-pin.json` pins the mirror (`sha256 f4e6cc88…517d`, 144364 bytes, 155 rows, `sourceRevision` = base); C8 requires the mirror bytes to equal the base-revision registry, the add-commit to be a strict ancestor of the measured revision, and the measured registry minus the S418 row with S372/S373 `used-by` restored to reproduce those bytes | none in the repo: read-only `git show`, `git ls-tree` and `git log`; `--selftest` writes only throwaway sandbox repos under `tempfile.mkdtemp` and removes them | kake |

No round-55 completeness counter exists at this writing (round 52 shipped
`c52_gate_registry.py`), so the eight-cell requirement above is not yet checked by code.
Withdrawal rule: a row goes when its counter leaves the tree. Two open registry notes:
(i) `64=usage` is docstring text in both counters and neither returns it — a missing
`--revision` exits 2; (ii) the C2 `--selftest` reads the committed round-55 evidence, so it
exits 2 until that evidence lands and no `c2-quote-selftest.txt` receipt is committed.
```

CODE CHECK:

`readme-index-counter` claims → code lines:
- entry command / flags → `c55_readme_index.py:206-209` (`--root`, `--revision`, `--selftest`, `--json`); `--selftest` short-circuits at `:211-212`; `:213-214` `ap.error("--revision is required unless --selftest is used")`.
- `0=met` predicate text → `:41` `PREDICATE = "met: index_mismatches == 0 AND knowledge_files >= 46"`; `:133` `met = mismatches == 0 and len(know) >= FLOOR`; `:134` returns 0/1.
- `1=not met` components → `:105-124`: `unindexed` (`:109-111`), `thin` (coverage cell `< 5` whitespace tokens or no shared 5+ letter word, `:112-118`), `dangling` (brace-expanded tokens that resolve under no candidate base, `:119-123`), sum at `:124`.
- `2=could-not-evaluate` → `:96-101` returns 2 for `cannot read tree or corpus/README.md at <rev>` and `no '## Coverage map' section`; `:97` is the tree/README read gate.
- `64=usage` declared, not implemented → `:28` docstring only; `grep -n 64` matches that line alone; observed `python3 -B … --root .` (no `--revision`) → rc 2 from `:214`.
- 10 fixtures → `:166-185` `cases` dict with 10 keys (`pass`, `fail_unindexed`, `fail_thin_short`, `fail_thin_offtopic`, `fail_prefix_name`, `fail_dangling`, `pass_brace_expands`, `fail_brace_member_missing`, `fail_deleted_population`, `fail_no_section`); tally printed at `:198`. Exercised: `--selftest` → `c55 readme-index selftest: 10/10`, rc 0. Receipt `.ufo/waves/round-55/controls/c1-selftest.txt` (33 bytes) holds exactly that line.
- `contract.json` pin → `.ufo/waves/round-55/contract.json` `claims.C1.predicate` is the same sentence; the counter reads no JSON config (no `json.load` of contract; `json` is imported for `--json` output at `:220-223`), matching the docstring's "the same sentence appears in `contract.md`, here and in every receipt" (`:9`).
- base control receipt → `.ufo/waves/round-55/controls/base-c1-readme-index.txt` line 1 `C1 readme-index index_mismatches=21 knowledge_files=46 met=False  (met: index_mismatches == 0 AND knowledge_files >= 46)`, `unindexed=21 thin=0 dangling=0 coverage_rows=27`, `revision: fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`, `EXIT=1`.
- `FLOOR = 46` deletion guard → `:42`; population counted at `:102`.
- write scope none → `:50-63` only `git -C root show` and `git -C root ls-tree -r --name-only`; fixture `git add -A` at `:151` targets the throwaway dir `d` created at `:141`, removed at `:193`.

`yahoo-robots-quote-truth-counter` claims → code lines:
- entry command / flags → `:668-673` (`--root`, `--revision`, `--selftest`, `--json`); `:674-675` `--selftest` short-circuit; `:676-677` `ap.error` on a missing `--revision`.
- `0=met` → `:57` `PREDICATE = "met: conditions_passed == 8 of 8"`; `:679` counts `state == "pass"` over the eight `add(...)` checks; `:461-463` returns 0 iff all pass.
- `1=not met` → `:463` (`0 if all(...) else 1`).
- `2=could-not-evaluate` → `:190-191` `unevaluable(...)` returns 2; used for malformed `receipts.json` (`:328-329`) and `mirror-pin.json` (`:405-406`); exception path `:457-459`.
- `64=usage` declared, not implemented → `:42` docstring only (`grep -n 64` otherwise matches the sha256 padding at `:588` and `:630`); observed `python3 -B …` with no `--revision` → rc 2 from `:677`.
- 30 fixtures → 29 `@case(...)` decorators (grep count 29) plus the `"pass"` entry at `:532`; tally at `:661`. Not exercised green: `--selftest` at HEAD printed `selftest: missing round-55 evidence corpus/lessons/round-55.md`, rc 2.
- selftest is evidence-coupled → `:498-510`: revision is `KAKE_R55_SELFTEST_REV` or `git(cwd, "rev-parse", "HEAD")`, and every key (registry, lesson, receipts, mirror, pin, census receipts, three entries, three retained bodies) must be readable at it, else return 2 at `:509-510`. Fixtures are then sandbox repos: `:471-493` (`mkdtemp`, `init`, three commits with throwaway `user.name=selftest` identity), removed at `:654`.
- receipts pin → `:66` `RECEIPTS`; `:339-343` body sha256 and bytes equal the receipt; `:344-351` integer (non-bool) `httpStatus == 200` and ISO `fetchedAt` whose date equals `ROUND_DATE` (`:59`); `:352-357` receipt URL equals the registry row URL; `:280-281` also enforces the 1000-byte body floor.
- mirror pin → `:415-420` mirror bytes equal the base-revision registry, carry no `S418`, hash to `pin.sha256`, row count equals `pin.rows`; `:421-432` measured registry minus new rows with S372/S373 `used-by` restored must equal the mirror bytes; `:434-451` add-commit strictly earlier (`merge-base --is-ancestor`, `add_commit != rev`) and its blob hashes to the pin. Pin values read from `.ufo/waves/round-55/assimilation/mirror-pin.json` (`sha256 f4e6cc8830c1d963218a31e5745c0c892a30a83d0d758fcd412a5c201bdc517d`, `bytes 144364`, `rows 155`, `sourceRevision fcaf4b85…`).
- 25-unit ceiling → `:70` `UNIT_CEILING = 25`; `units()` at `:137-139` = one unit per CJK character plus one per non-CJK whitespace token, applied to Gate quotes (`:293-298`) and entry spans of 6+ units (`:306-316`).
- write scope none → read-only `git show` (`:98`, `:103`), `git log --diff-filter=A` (`:434`), `git merge-base --is-ancestor` (`:440`); fixture writes go to the `mkdtemp` dir from `:471`, removed at `:654`.

Gates: none run beyond the two `--selftest` invocations above and the two usage invocations; no
`--root . --revision` measurement was run, so no verdict on either predicate is claimed here.

Touched surfaces: this report only.

Out of scope (not done, per seat bounds): no edit to `SKILL.md`, no counter change, no receipt
creation, no commit.

Findings: (1) both counters document `64=usage` but implement no such exit — usage is exit 2,
colliding with could-not-evaluate; (2) no round-55 completeness counter exists, so the eight-cell
requirement is unenforced; (3) the C2 selftest cannot be green before the round-55 evidence is
committed, so its 30-fixture count is code-counted, not observed.

VERDICT: section drafted with both rows in the round-52 schema; every cell matched to counter lines; two declared-vs-implemented exit-64 gaps and one unexercised selftest recorded.
