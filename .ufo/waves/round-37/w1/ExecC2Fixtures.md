# ExecC2Fixtures — C2 fixture repair (round-36 routed defect 3; non-claim, evidence only)

No claim, no verdict. Deliverables stay in `/fast/scratch/hyaku/kake-r37w1/ExecC2Fixtures/`; the
only lane file I wrote is this report. No secret tree touched, no network, no installs.

## Built

Five fixtures appended through the existing `add(...)` helper in `build_fixtures()` of
`scripts/source_recheck_selftest.py`. No existing fixture, expectation or tool byte changed
(`git diff --numstat 4b089da… ad7dbd9…` → `35 0 scripts/source_recheck_selftest.py` only).

| Fixture (clone line) | Contract | Contract sentence it pins | Expected |
|---|---|---|---|
| `b12-relative-redirect-resolved-against-previous-hop` (:342) | (b) | "resolved against the URL that hop answered … then the previous resolved location"; from `/dir/page`, 301 `next/step` then 301 `final` | moved `https://example.com/dir/next/final`, exit 1 |
| `b13-dot-segments-in-relative-location-removed` (:349) | (b) | "by RFC 3986 section 5.2"; relative `../final` from `/dir/page` merges to `/dir/../final`, §5.2.4 gives `/final` | moved `https://example.com/final`, exit 1 |
| `c11-comment-with-inner-greater-than-removed-whole` (:405) | (c) | "comments removed (`<!--` to the next `-->`)"; `<!-- x > hidden note -->` | quote_missing, exit 1 |
| `c12-tag-between-text-removed-before-match` (:412) | (c) | "every remaining tag removed"; `<b>Hel</b>lo world`, quote `Hello world` | clean, exit 0 |
| `f17-utf8-bom-mark-dropped-from-text` (:555) | (f) | "decoded in that encoding with the mark dropped"; `EF BB BF` body, quote starts U+FEFF | quote_missing, exit 1 |

Expectations were written from the SCORECARD contract text before either tool ran; tool runs only
confirmed them. Each fixture carries a comment naming the mutant rule it discriminates.

## Commands and observed results

Sandbox `/fast/scratch/hyaku/kake-r37w1/ExecC2Fixtures`; `TMPDIR=…/tmp`; `GIT_DIR`,
`GIT_WORK_TREE`, `GIT_INDEX_FILE` unset; every run under `timeout`.

1. `git clone -q <lane> clone && git -C clone checkout -q 4b089da699cfaaf5ebeb6a0746b7e4238602e20a` — exit 0. Commit of repair: `ad7dbd9d107165151eef6dc7c1ef2dd79801e0e1` (clone only).
2. `python3 -B clone/scripts/source_recheck_selftest.py --tool e1.py` (E1 = `4d5b3d55:scripts/source_recheck.py`, sha256 `577b2d7d…0d48`, extracted byte-equal) — **exit 0, `106/106`, failed 0** (`selftest-e1.json`, sha256 `8e33d789…4f32`).
3. Same selftest `--tool e2.py` (E2 = `1a16b8e3:.ufo/waves/round-36/retained/independent/selftest-seat-reference.py`, sha256 `a5176fee…221f`) — **exit 0, `106/106`** (`selftest-e2.json`, sha256 `694c71e2…c46`).
4. `timeout 900 python3 -B <lane>/.ufo/waves/round-37/c2_mutkill.py --root $PWD/clone --revision ad7dbd9d… --jobs 8` — **exit 0**, `met true`, `killed 32`, `survivors []`, `fixtures 106`, `validFixtures 106`, `failedOnE1 []`, `failedOnE2 []`, `selftestSha256 9a554004…a8e3` → `c2-after.json` sha256 `d88ea78e…95a2`. A second identical run produced a byte-identical file (`c2-after-rerun.json`, same sha256).
5. Same counter `--revision 4b089da699cfaaf5ebeb6a0746b7e4238602e20a` (before) — **exit 1**, `killed 27`, `survivors ["M07","M08","M09","M11","M24"]`, `fixtures 101`, `failedOnE1/E2 []` → `c2-before.json` sha256 `8decc585…1ede`. Reproduces the declared base exactly.
6. Per-fixture attribution from `c2-after.json`: M07, M08, M09, M11, M24 each `killed`, `killerCount 1`, and their single killer is the matching new fixture. `c12` also kills nothing else; `b12` additionally kills M06 (`killerCount 2`); `f17` additionally kills M23 (`killerCount 4`).
7. `python3 -B clone/scripts/source_recheck_selftest.py --tool <lane>/.ufo/waves/round-37/c2/mutants/Mxx.py` for the five survivors — each **exit 1, 106 cases, 1 failure**, the expected one, with the observed divergence:

   | Mutant | Failing fixture | Observed |
   |---|---|---|
   | M07 | b12 | moved `https://example.com/dir/final` (expected `…/dir/next/final`) |
   | M08 | b13 | moved `https://example.com/dir/../final` (expected `https://example.com/final`) |
   | M09 | c11 | exit 0 (expected 1) |
   | M11 | c12 | exit 1 (expected 0) |
   | M24 | f17 | exit 0 (expected 1) |
8. `git apply --check ../c2-fixtures.patch` then `git apply` in a **fresh clone at 4b089da** — both exit 0; resulting `scripts/source_recheck_selftest.py` sha256 `9a554004…a8e3` equals the clone's; that clone's `git status --porcelain` = ` M scripts/source_recheck_selftest.py` only.

## Deliverables (absolute paths, sha256)

- Patch against `4b089da699cfaaf5ebeb6a0746b7e4238602e20a`: `/fast/scratch/hyaku/kake-r37w1/ExecC2Fixtures/c2-fixtures.patch` — `88544a0faca2623aefc658a78f8901cb2cbb4f40c440255809cc0f4690178c57`, 60 lines, touches `scripts/source_recheck_selftest.py` only.
- Patched selftest: `/fast/scratch/hyaku/kake-r37w1/ExecC2Fixtures/clone/scripts/source_recheck_selftest.py` — `9a5540045a32694c1a4a26b4c669d06e397a4c7f7f910e49aa6626d672aca8e3`, commit `ad7dbd9d107165151eef6dc7c1ef2dd79801e0e1` in `/fast/scratch/hyaku/kake-r37w1/ExecC2Fixtures/clone`.
- Counter outputs: `c2-after.json` `d88ea78e…95a2` (met), `c2-before.json` `8decc585…1ede` (27/32).
- Selftest receipts: `selftest-e1.json`, `selftest-e2.json`, `selftest-clonetool.json` (lane tool at 4b089da also 106/106, exit 0), `selftest-M07/M08/M09/M11/M24.json` in the same directory.

## Risks and limits

- **Not blind.** I read E1 and the five mutant diffs to choose discriminating inputs; the expected
  outputs were derived from contract text, and E2 (an independent implementation) plus E1 agree on
  all 106 fixtures, but input selection is author-informed, not blind-authored.
- The fixtures pin narrow readings: c12 requires text to be joined across removed tags; f17 requires
  U+FEFF to survive NFKC and whitespace deletion in the quote (true: U+FEFF is neither). Both E1 and
  E2 read them that way; a future reimplementation with a different reading would need a contract
  clarification, not a fixture change.
- Fixture count moved 101 → 106; the selftest's `MIN_FIXTURES = 40` floor is unaffected. The counter
  counts only fixtures valid on both E1 and E2 (`validFixtures 106`), so no new fixture is
  implementation-specific.
- Not verified: the lane's gate, the C1 sealed counter (no key), freshness behavior, or any mutant
  outside the 32. No lane file, index or jj state touched; `git -C <lane> status --porcelain` shows
  only the L1's wave-1 dispatch artifacts (` M .ufo/waves/round-37/make_w1_spec.py`, untracked
  `w1-*` files and `w1/`) plus this report.
- No tools installed or upgraded.
