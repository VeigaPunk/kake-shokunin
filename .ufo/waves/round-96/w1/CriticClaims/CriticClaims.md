# CriticClaims — scoped findings (round 96, attempt 1)

Verdict line and route table: `claims.md` in this directory. Receipts are the `*.out` files beside it.
The seat's report trailer named `.ufo/waves/round-96/w1/CriticClaims.md`; that path is outside the seat's
write bound, so the same findings are written here, inside `w1/CriticClaims/`.

## C1 (calibration) — falsified

1. **The do-nothing base satisfies the frozen predicate.** `c96_selfassess.py` at `bde9869…` reports
   `pins=ok mismatches=0 battery=23/23 admit=5/5 shadow=absent predecessor_admits=6/22 ng_pred_admits=3/3 met=true`
   (`base-c1-successor.out`, identical to `controls/c1-successor-at-base.txt`). The predecessor at the same
   revision reports `pins=identity met=false` (`base-c1-predecessor.out`). The freeze's statement that the
   do-nothing lane "stays uncertifiable" is contradicted by the round's own committed control. The C1
   predicate is met with zero landed work.
2. **The differential is not evidence of the R95-5/R95-7 closure.** The predecessor's `pins=identity` at base
   comes from three entry-content digests (`crawl-budget-consequences.md`, `crux-keyless-check.md`,
   `kimi-subpath-audit.md`). Every tested lane state shares that failure (base, `c1-head`, `c1-stuff`,
   `c1-launder`), and a one-line head edit to an entry also flips it (`c1-head-*.out`). The differential
   therefore holds whatever the lane contains.
3. **Shape-level shortcuts reach `met=true`.**
   - Absence annotation: a SKILL row naming a missing path inside `[r96-absence …]` yields `E5=0` (`c1-launder.out`).
   - Gate vocabulary: a new round-96 lesson whose Gate body is `admit.` / `reject.` passes E1 (`c1-stuff.out`).
     The E1 rule checks only whole-word tokens, not that the Gate says anything.
4. **`git show` honours replace refs.** The counter reads committed bytes through `git show rev:path`. With a
   `refs/replace` entry in the repository, a broken SKILL row is audited as its replacement blob
   (`v4-c1-replace-broken-skill-served-base.out` rc=0 `met=true`; control without replace `rc=1`). The
   counter neither sets `GIT_NO_REPLACE_OBJECTS` nor verifies the object it reads. Routed.
5. **Forgeable receipt line.** `self_pin=ok` is printed on every run even with no pin supplied and is not part
   of `met`. The F2 battery item only checks that a wrapper lacks the public counter digest, which is
   circular (the digest is `sha256` of a file in the lane). A wrapper that prints a counter-shaped line with
   the digest is indistinguishable from real output (`sandbox-and-refusal-probes.txt`). Routed.
6. **Unpinned oracle (code-read only, not exercised).** `main()` accepts `--base-pins-json`, which sets the
   cardinality floors used for `pins=short`. The frozen command does not pass it, but the flag exists in the
   frozen file. Identity pins cover most of the same surfaces, so impact is narrow.
7. **Refused as designed:** `--surfaces-file` (argparse rc=2); surfaces-file substitution in the scratch clone
   (`unevaluable=surfaces digest drift` rc=2, file restored afterwards).

## C2 (freshness) — falsified (with the instrument crash below)

1. **Instrument defect, routed, not repaired: `NameError`.** Every candidate that reaches the mutant stage
   crashes: `c96_reval.py:624` calls `mutant_cases(… mutants, tree)` inside `main()`, but `mutants` is never
   bound in `main()` (it is bound only in `selftest()` and in the `n_mut` line, which uses a different name).
   The committed controls (`base-c2`, `ctl-c2-selftest`) never reach that line, so they did not expose it.
   As committed, the counter cannot print `met=true` for any revision (`c2-*.out`, `frozen-*.out`,
   `v4-*-frozen-unpatched.out`). Routed to round 97 owner; not repaired.
2. **The anti-table digests only lowercase hex SHA-256 of canonical input.** A memorizing table keyed by
   the canonical JSON text (`C2-02`), or by base64 of the digest (`C2-04`), every second hex character
   (`C2-05`), or the digest of minified-separator output (`C2-06`), passes `anti_table=ok`, and then the
   hand (37/37) and generated (112/112) cases pass too. The K2 control (hex digest table) is caught
   (`anti_table=hit`). R95-8's fix is real but covers one encoding.
3. **Positional memorization needs no digests (C2-07).** Generated answers in the seed-96 order, plus the
   hand table as text, reach `met=true`.
4. **The stem check is literal substring.** A candidate that assembles `pos-good-reval.py` at runtime (C2-11)
   or executes the counter's own `reference()` (C2-12) passes the stem check. The literal path (C2-10) is caught.
5. **Sandbox escape by hardlink (same device only).** `os.link` is not audited, and `realpath` checks do not
   stop a hardlink into the tree. Reads of the frozen pins and of the counter reference both succeed
   (`C2-17`, `C2-18`). Under the lane's device layout (lane `/home` btrfs dev 56; `/tmp` dev 66305; `/fast`
   dev 66306) this needs the work tree on the lane's device. The default `TMPDIR=/tmp` and the `/fast`
   scratch do not satisfy that, so today the boundary is the filesystem, not the sandbox.
6. **Other sandbox gaps.** `os.forkpty()` is not in the denial list and returns `forkpty-ok` (`C2-14`).
   Extension-module loading is blocked by the import audit (`C2-15`). In-tree symlinks to outside files are
   refused via realpath (`C2-16`).
7. **The mutant clause and `positive=admitted` do not depend on the candidate.** Both are computed from the
   frozen positive control. A refuse-all candidate still prints `mutants=14/14 positive=admitted`
   (`v3-bad-candidate.out`). The clause tests the scorer, not the candidate. `met` as written therefore
   reduces to hand, generated, forgery and anti-table outcomes.
8. **"All 120 generated cases" is 112.** The reference refuses 8 of the 120 seeded inputs (status without a
   validator); `generate` drops them from the population instead of scoring them as refusals. Frozen
   population; routed.
9. **Harness note (not claim-affecting).** The sandbox sets `sys.path=[root]`, so subjects cannot import
   `hashlib`, `base64` or `random`; candidates must hand-roll them (the K1–K10 candidates do).

## Outside the seat

- The lane tree has an untracked `scripts/reval_exchange.py` that is not at `HEAD` and was not part of my
  clone. The counter reads committed bytes at `--revision`, so that file is invisible to it. Not mine; noted
  for L1.
- No lane file was written by this seat. Scratch removed after receipts were copied.
