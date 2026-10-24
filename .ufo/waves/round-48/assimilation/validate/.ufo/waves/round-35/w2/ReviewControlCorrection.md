# ReviewControlCorrection — round 35, wave 2

Attacked: the appended dcef39b5 correction in `corpus/lessons/round-35.md`
("Correction of round-34 mistake row 4") and `SCORECARD.md` round-35 appended
correction (lines 1522–1525): the claim that control `dcef39b5` does not key on
the case directory name, that renaming case directories leaves 28/28 on the
frozen round-34 counter, and that a one-comment HTML change drops it to 7/28.

## Result: no misstatement found; every claimed line number, quote and score reproduces.

Sandbox: `/fast/scratch/hyaku/kake-r35/w2/ReviewControlCorrection/` (clone +
probe). No tool installs.

## Commands, exit codes, observed output

1. `git clone -q <lane> clone` → rc 0; `git -C clone fetch
   r34-c1-lookup-dcef39b5.bundle 'refs/heads/*:refs/heads/r34/*'` → rc 0;
   `git rev-parse dcef39b5^{commit}` → `dcef39b5f4e8373970eb74858d2c6175524cdfd0`,
   parent `a2fe31b2d1d2bf…`, 18 insertions.
2. `git show dcef39b5:scripts/link_preview_audit.py` → 18-line blob, sha256
   `a2e274c0ce9168bb10d7217a8c9a09c2516aea1c2c148dbf583306dcc56730ec` (matches
   wave-1 `ScribeControlCorrection`).
3. Frozen round-34 counter (`c1_matrix_count.py` + `c1-matrix.json` copied from
   lane; matrix sha256 `246a6a3b…14f7` matches pinned digest), run via
   `probe_variants.py <mode> <clone> dcef39b5` (wave-1 method, plus renamed_case
   and single_comment variants):
   - `unchanged` → 28/28, rc 0
   - `renamed_parent` (case under `base/uuid4().hex`) → 28/28, rc 0
   - `renamed_case` (the per-case directory itself renamed) → 28/28, rc 0
   - `commented` (`<!-- closure perturbation -->` appended to every `.html`) →
     7/28, rc 1: control 6/6, defect 0/13, input 1/7, usage 0/2
   - `single_comment` (one `.html` per case) → 7/28, rc 1, same byKind
4. Sealed round-35 counter version 2 (sha256 `1b4d9d59…469b`, matches SCORECARD
   pin): `sealed_count.py c1 --root clone --revision dcef39b5 --key-revision
   4c6be2bd` → `passed 7 / 24`, `met false` → confirms "The round-35 sealed
   counter scores it 7 of 24".

## Line-number and quote checks (all pass)

- `corpus/lessons/round-34.md:68` (mistake row 4) says "keys on the case
  directory name the C1 counter chooses" ✓; carried-open `:130` "case identity
  leaks through the case directory name (mistake row 4)" ✓.
- `.ufo/waves/round-34/criteria/lookup_control_check.py:6` "reads the case
  directory name the counter chose" ✓.
- `SCORECARD.md` round-34 "Limits found by wave 1" (1254–1257) "replays the
  matrix by case directory name" ✓; appended correction 1522–1525 ✓.
- Tool blob: lines 5–8 walk `os.walk(".")` and keep every relative path and
  file content ✓; line 10 `h = hashlib.sha256(json.dumps(argv).encode())` exact
  ✓; line 12 exact ✓; line 15 exact ✓. `git show dcef39b5:…` with `nl -ba`.
- The round-34 closure measured the same 7/28 (`round-34-verifier-spotcheck.md:81-84`).

## Nitpicks (wording only; no behavioral error)

- "Line 15 … prints the stored row or a clean default": line 15 assigns; the
  print is lines 17–18.
- "hash the arguments plus every relative path and file content": under the
  manifest invocation line 14 substitutes `key("default")` for argv, so the
  arguments do not actually enter the key there; the conclusion (no case-dir
  name dependence) is unaffected.

## Not verified

- Did not rerun the round-34 closure's 12 held-out cases or the real-input run
  (out of scope for this item).
- Did not rerun the sealed C2 counter.

Verification gaps: none blocking.
