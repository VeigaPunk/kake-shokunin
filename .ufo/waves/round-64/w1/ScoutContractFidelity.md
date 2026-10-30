# ScoutContractFidelity — round 64 contract-fidelity scout

Scope: verify the round-64 contract (`.ufo/waves/round-64/contract.md`) against the
committed bytes at the measured revision T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`
and the after-receipts commit `cc8add1fa740b920ea5179a71152680ab220c70c`:
(1) the four frozen instrument sha256s, (2) the fixture revisions vs
`controls/fixture-builds.txt`, (3) the predicate sentences vs the counter docstrings,
(4) every receipt path named in the contract at `cc8add1f`. Leaf member; no subagents.
All lane reads were `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show/rev-parse/log/diff/status`,
`git cat-file -e`, `git ls-tree`; the lane working tree was never written
(pre-existing untracked files `.ufo/waves/round-64/sources/S432.live.html`,
`w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1.ready.partial`, `w1/` left untouched).
Scratch: `/fast/scratch/hyaku/kake-r64/ScoutContractFidelity/` (created, then deleted
before this report was written). Tool installs: none. No tooling directive channel was used.

Method note (semantic vs grep): all checks here are byte/digest/ancestor checks over
committed git objects; no LSP server exists for this question type, so no `lsp` device was
used and no claim below rests on text-grep-as-semantic-proof — every quoted sentence is
shown verbatim with its file and line.

---

## V1 — The four frozen instrument sha256s at T0: PASS

Command (exact):

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin
for p in .ufo/waves/round-64/c64_calibration.py .ufo/waves/round-64/c64_quote_tool.py \
         .ufo/waves/round-64/fixtures/build_fixtures.py .ufo/waves/round-64/fixtures/stub_tool.py; do
  printf '%s  %s\n' "$(git show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:$p | sha256sum | cut -d' ' -f1)" "$p"
done
```

Output at T0:

```
5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf  .ufo/waves/round-64/c64_calibration.py
96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b  .ufo/waves/round-64/c64_quote_tool.py
7fbd8cbc67c17264096e44474a698b3f0d7702c3e1cc23f0b5bdaa26ee0271d3  .ufo/waves/round-64/fixtures/build_fixtures.py
7c78a05df78703044f8fe8fa02793a63b580f6353f58e8ebcee836038762edde  .ufo/waves/round-64/fixtures/stub_tool.py
```

All four equal the contract's freeze block (`contract.md` lines 8–15). Re-run at
`cc8add1f`: identical four hashes (instruments unchanged between measured and
after-receipts commits). `contract.md` itself and `controls/fixture-builds.txt` are
byte-identical between T0 and `cc8add1f` (`diff <(git show T0:…)` / `<(git show CC:…)` →
`IDENTICAL` for both).

## V2 — Fixture revisions named in the contract vs `controls/fixture-builds.txt`: FAIL for 1 of 5 (finding F1)

Receipt bytes at T0 (`git show T0:.ufo/waves/round-64/controls/fixture-builds.txt`, 4 lines):

```
{"name": "stub-repo",         "path": "/fast/scratch/hyaku/kake-r64/l1/fixtures/stub-repo",         "revision": "14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3"}
{"name": "marker-repo",       "path": "/fast/scratch/hyaku/kake-r64/l1/fixtures/marker-repo",       "revision": "4c666e7632cb2093fbed18117e460bf37d1d14ce"}
{"name": "fabrication-repo",  "path": "/fast/scratch/hyaku/kake-r64/l1/fixtures/fabrication-repo",  "revision": "f924538ede0d290d74af3126a40103887f4c8d46"}
{"name": "junk-repo",         "path": "/fast/scratch/hyaku/kake-r64/l1/fixtures/junk-repo",         "revision": "82dcba0d2f83bdd427c9566b33739af71fe84efc"}
```

`contract.md` lines 19–26 name **five** fixture revisions, attributing all of them to
`build_fixtures.py` in `/fast/scratch/hyaku/kake-r64/l1/fixtures/` with the above file as
their receipt — including `ledger-mut-repo 5b981bd0c43dd30c1546a1966d971f4227f60973`.

Observed facts:

1. The frozen `build_fixtures.py` (sha `7fbd8cbc…`, `main()` results list, lines ~150–186)
   builds and prints exactly four repos: `stub-repo`, `marker-repo`, `fabrication-repo`,
   `junk-repo`. No code path creates a ledger-mut repo; its docstring lists four fixtures.
2. `controls/fixture-builds.txt` has exactly four lines; no entry names `ledger-mut-repo`
   or `5b981bd0`. `git grep -n "5b981bd0" cc8add1f -- .` hits only the contract (l.26,40),
   `controls/control-ledger-mut.txt` (l.2,3) and `corpus/lessons/round-64.md` (l.70).
3. The fixture does exist outside the repo:
   `/fast/scratch/hyaku/kake-r64/l1/fixtures/ledger-mut-repo` has
   `git rev-parse HEAD` = `5b981bd0c43dd30c1546a1966d971f4227f60973`, author
   `kake-r64-fixture`, date `Fri Oct 30 07:53:18 2026 -0300`, message `mutate locatedRawLines`,
   and a two-commit history whose parent is marker-repo's commit `4c666e76…` with
   `.ufo/waves/round-63/quote-class/quote-classes.json | 6 +++---` as the only change.
4. The actual mutation, from `diff -r marker-repo ledger-mut-repo --exclude=.git`:
   `"locatedRawLines": "6150-6154"` → `"6150-6156"`, plus a re-serialization of the ledger
   (quote `’` → `\u2019` escape, trailing newline dropped) — i.e. the file was rewritten by
   a JSON dumper, not byte-patched. Tree hashes: ledger-mut `1630678235cb4ca1e1150e9c8aa751848abf7fbc`
   vs marker `8cab4d289e94713f78fc87e8fe82756375bbca0d`.
5. The mutation *is* named in committed prose:
   `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/control-ledger-mut.txt`
   line 1 reads
   `$ python3 -B .ufo/waves/round-64/c64_calibration.py --root <marker-repo + ledger locatedRawLines mutated 6150-6156> --revision <its HEAD>`,
   and line 3 records the expected `met=false` exit-1 body at revision `5b981bd0…`.
6. **The named fixture revisions are not reproducible as revisions.** I re-ran the frozen
   driver into my own scratch:

   ```sh
   python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/fixtures/build_fixtures.py \
     /fast/scratch/hyaku/kake-r64/ScoutContractFidelity/fixtures \
     --lane /home/vgpnk/Projects/shokunin/kake-shokunin     # exit=0
   ```

   Output: stub `909f29988db30494739733552e2c3ad523a341b1`, marker
   `44cd18e97fb98db92e94ba92ff872424e2e481a1`, fabrication
   `c8558dadf35d517678bd58e2fd8bcaf87fa072e2`, junk `119727c789f9dd3b5d21720b5ac683fb3e6fc691`
   — different ids (commit time unpinned; the driver uses plain `git commit`), while
   `git rev-parse HEAD^{tree}` for all four originals vs my rebuilds is
   `f8271b1174dc955458fd2df8c7ba2e9ddf2b23ba` / `8cab4d289e94713f78fc87e8fe82756375bbca0d` /
   `c8dc2d141203a96e4f680e8d77af7241cc8ccd37` / `fe8c1cfa9c6ebb06c1d23eb2f032b177289d6e31`
   — **SAME-CONTENT** in every case. So the fixtures' bytes are reproducible; their commit
   ids are one-shot artifacts of the build session, attested only by the receipt (for four
   of five) and by out-of-repo scratch repos.
7. No late removal: dangling commits `95de4aec` and `dd3d31ce` (dated `Tue Oct 27 11:05:13
   2026 -0300`, on no branch) have tree `34dcbc9a88f7c2ee8d1b5b1fc4e495b5caa50dff` —
   byte-identical to T0's tree — so `fixture-builds.txt` never contained a ledger-mut line.

**F1 (moderate, provenance/documentation — does not falsify the C1 predicate):** the
contract's attribution sentence is false for the fifth fixture: `build_fixtures.py` does
not build `ledger-mut-repo` and `controls/fixture-builds.txt` does not record it. The
control's evidence still stands on its own (`control-ledger-mut.txt`: exit 1,
`pins=0 pin_drift=drift:ledger … met=false` at `5b981bd0…`, and the recipe named in that
receipt's prose), and no kill rule references the fixture-builds receipt — but a verifier
re-running the frozen driver cannot regenerate the fixture revision the contract names,
and the C1 control set is thus 4-of-5 receipt-attested, 5-of-5 evidenced.

## V3 — Predicate sentences vs counter docstrings: semantically matching, NOT literally identical (finding F2)

All three predicates were extracted verbatim from committed bytes and diffed word-level
(normalizing only `**`, backticks and line wrapping).

- **C1** (`contract.md` l.35–42 vs `c64_calibration.py` docstring l.37–41): claims identical —
  met=true (exit 0) at the measured revision; met=false (exit 1) on each committed control
  fixture (marker-only / digest-consistent fabrication / junk / ledger-mutation); met=false
  (exit 1) at the base. Both sides state exactly these three clauses with the same four
  fixture families and the same base `1a481315`. Differences are wording only: contract
  spells the invocation `c64_calibration.py --root . --revision <measured>` and the fixture
  revision prefixes (`4c666e76`, `f924538e`, `82dcba0d`, `5b981bd0`), docstring says
  "this counter" / "the round-63 base" and omits revs; contract uses ", and" joiners,
  docstring semicolons. **Not literally identical; substantively identical.**
- **C2** (`contract.md` l.71–80 vs `c64_quote_tool.py` docstring l.27–35): claims identical —
  met=true (exit 0) at the measured revision over the lane tree; on the committed stub
  fixture `tool_sha=mismatch met=false` (exit 1); `c63_quote_tool.py` on that same stub
  fixture prints met=true (exit 0) — the routed defect reproduced. Both include the same
  parenthetical that at the base the real tool already exists so the base tree also prints
  met=true. Differences: contract cites the stub by revision `14fe2eab`, docstring cites it
  by recipe path `.ufo/waves/round-64/fixtures/build_fixtures.py` (which does build that
  stub — verified in V2); minor punctuation. **Not literally identical; substantively identical.**
- **C3** (`contract.md` l.104–110 claims the identical sentence is in the lesson §Mistakes):
  the closest lesson statements are the claim bullet `corpus/lessons/round-64.md` line 24
  "(`paths sidecar binding invalid: SKILL.md:364`, exit 2 → exit 0)" and the §Mistakes Fix
  cell (line 30) "This round's re-pin (7 entries, old→new recorded below) returns the sweep
  to exit 0 (`.ufo/waves/round-64/controls/sweep-after.txt`)". The literal strings of the
  contract predicate — "VERDICT: OK", "seven-entry" — appear **nowhere** in the lesson
  (checked: `lesson contains 'VERDICT: OK': False`; `Mistakes contains 'VERDICT': False`,
  `'exit 0': True`, `'old→new': True`, `'sidecar-repin-map.txt': True`,
  `'paths sidecar binding invalid': True`). **F2 (minor):** the contract's parenthetical
  "identical sentence in …" is overstated in all three claims; the substance (instrument,
  command, expected verdicts, exit codes, the seven-entry re-pin, the resolver table, the
  failure string) is present and consistent on both sides, so no predicate is changed —
  but the cross-reference should not be read as a literal duplicate.

Corroborating constants (contract pins vs counter constants vs blobs): raw
`63b0a018…911b`, text `8b90d096…2a69`, ledger `5f48e26b…c42d`, recipe `6b0a88cd…2405`,
located `6150-6154`, spot verdict span "is only a generic lead-in, not substantive
evidence for a response-header expectation" — `c64_calibration.py` lines 61–79
(`RAW_SHA/TEXT_SHA/LEDGER_SHA/RECIPE_SHA/EXPECTED_LOCATED/FROZEN_QUOTE/SPOT_VERDICT_SPAN`)
match the contract §C1 pin list (l.45–50) string-for-string, and I re-hashed the four
blobs at T0, `cc8add1f` and base `1a481315`: all `OK` (12/12) — the kill rule "any pinned
sha differs at the measured revision" is not triggered. `FROZEN_TOOL_SHA`
`431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14`
(`c64_quote_tool.py` l.47) equals `sha256(git show <rev>:scripts/quote_class.py)` at base,
T0 and `cc8add1f` — the tool is unchanged, as the contract asserts. The counter binds the
lesson's `## Gate` section block-level (`gate = section(lesson, "Gate")`;
`SPOT_VERDICT_SPAN in gate`), and that span is present in the committed lesson
(`corpus/lessons/round-64.md`, §Gate "Outside verdict" paragraph).

## V4 — Receipt paths named in the contract at `cc8add1f`: PASS

`git cat-file -e cc8add1fa740b920ea5179a71152680ab220c70c:<path>` for every path the
contract names under `controls/` — `base-c1.txt`, `control-marker.txt`,
`control-fabrication.txt`, `control-junk.txt`, `control-ledger-mut.txt`, `selftest-c1.txt`,
`stub-c64.txt`, `stub-c63-defect.txt`, `selftest-c2.txt`, `sidecar-repin-map.txt`,
`after-c1.txt`, `after-c2.txt`, `sweep-after.txt`, `sweep-before.txt`, `census-before.txt`,
`census-after.txt`, `fixture-builds.txt` — **17/17 OK, 0 missing**. All other paths the
contract names also exist at `cc8add1f`: `corpus/knowledge/freshness-sidecar.json`,
`corpus/lessons/round-64.md`, `scripts/freshness-sweep.mjs`, `corpus/SOURCES.md`,
`scripts/quote_class.py`, `.ufo/waves/round-63/c63_quote_tool.py`,
`.ufo/waves/round-61/sources/S432.html`, `.ufo/waves/round-63/quote-class/{S432.txt,quote-classes.json,extract_text.py}`,
`corpus/lessons/round-61-verifier-spotcheck.md`, `corpus/QUALITY.md`, `SKILL.md`,
`.ufo/waves/round-64/sources/receipts.json` — **14/14 OK**.

Receipt contents agree with the contract's stated expectations (`git show cc8add1f:…`):
`after-c1.txt` → `…met=true` / `exit=0`; `base-c1.txt`, `control-marker.txt`,
`control-fabrication.txt`, `control-junk.txt`, `control-ledger-mut.txt` → `met=false` /
`exit=1` with exactly the contract-named revisions in their `$ …` command lines and
`revision=` fields; `selftest-c1.txt` → `selftest 26/26`, `c1=0`;
`after-c2.txt` → `tool_sha=ok … met=true` / `exit=0`; `stub-c64.txt` →
`tool_sha=mismatch … met=false` / `exit=1`; `stub-c63-defect.txt` → `met=true` / `exit=0`;
`selftest-c2.txt` → `selftest 11/11`, `c2=0`; `sweep-after.txt` → `VERDICT: OK (exit 0,
partial: offline)` / `exit=0`; `sweep-before.txt` → `paths sidecar binding invalid:
SKILL.md:364` / `sweep-before-exit=2`. All five contract-named fixture revisions resolve
to real repos on disk whose HEADs equal the named ids (stub `14fe2eab…`, marker
`4c666e76…`, fabrication `f924538e…`, junk `82dcba0d…`, ledger-mut `5b981bd0…`).

Adjacent check supporting C3's §113–115 bullet (cell-level diff of
`corpus/knowledge/freshness-sidecar.json`, base → T0, via `git show` + JSON walk):
exactly 7 of 30 entries changed, **only the `line` cell** (364→365, 445→446, 448→449,
449→450, 450→451, 423→424, 431→432); no `lineSha256`, `note`, `kind`, `date` or `token`
cell changed anywhere; `corpus/SOURCES.md` has no diff base→T0. Counts corroborate the
contract's "23 further entries verified byte-identical" (30 − 7 = 23) and the re-pin map's
old→new pairs (`controls/sidecar-repin-map.txt`, 7 rows). **F3 (minor, informational):**
because the `lineSha256` cells were already the post-shift values, the contract's wording
"changes only `line` and `lineSha256`" holds only as a permission statement — zero
`lineSha256` cells actually changed — so the re-pin map's "sha256(new line)" column
restates pre-existing values rather than recording new ones.

---

## Findings summary

| id | severity | statement |
|---|---|---|
| F1 | moderate (provenance) | `contract.md` l.19–26 attributes all five fixture revisions to the frozen `build_fixtures.py` and to `controls/fixture-builds.txt`; the frozen script builds four, the receipt records four. `ledger-mut-repo 5b981bd0…` exists only as an out-of-repo scratch repo; its mutation (`locatedRawLines` 6150-6154→6150-6156 plus JSON re-serialization) is named only in prose in `controls/control-ledger-mut.txt` l.1. No kill rule cites the fixture-builds receipt; the C1 control evidence itself stands. |
| F2 | minor (wording) | The contract's "(identical sentence in …)" parentheticals are not literally true: C1/C2 docstrings paraphrase (same claims, same fixtures, same exit codes); C3's claimed §Mistakes sentence does not exist verbatim (no "VERDICT: OK" in the lesson). Substance consistent on both sides; no predicate drift. |
| F3 | minor (informational) | Sidecar re-pin changed only the 7 `line` cells; no `lineSha256` cell changed (already post-shift values), so the re-pin map's "sha256(new line)" column restates old values. Contract's restriction and 7/23 counts hold. |
| — | info | Fixture commit ids are not reproducible (unpinned commit times; rebuild → different ids, identical trees). Receipts attest a one-shot build; the named ids are only verifiable against the on-disk scratch repos. Dangling commits `95de4aec`/`dd3d31ce` share T0's tree — `fixture-builds.txt` never listed the ledger-mut fixture. |

## Verdict

Contract-fidelity verdict: **verified with one provenance defect (F1)**. The four frozen
instrument sha256s, the pin/tool-sha constants, the 17 named control/after receipt paths
and their verdicts, and the C3 seven-entry re-pin claim all match the committed bytes at
T0 `4c8295fa…` and `cc8add1f…`. The single falsified statement is the contract's fixture
provenance sentence for `ledger-mut-repo 5b981bd0…` (built by `build_fixtures.py` /
recorded in `controls/fixture-builds.txt` — neither true); the predicate sentences are
paraphrases, not duplicates, of the counter docstrings. Nothing I inspected was modified:
lane tree untouched, frozen claims/counters/receipts/contract/lesson untouched.

Tooling installs: none (no `pacman`, no `uv`/`npm`/binary installs; nothing to record
under the 2026-10-19 tooling directive).

Report: .ufo/waves/round-64/w1/ScoutContractFidelity.md
