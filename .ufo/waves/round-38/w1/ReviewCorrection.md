# ReviewCorrection — round 38, wave 1

Scope: SCORECARD and routed defects 1, 2, 5 at `2dab7f3114f3e9dcf072b524c88816ab05fdfcf1`, compared with `corpus/lessons/round-37-verifier-spotcheck.md`. SCORECARD SHA-256 `b7432d69ffc4302bf0f5f6604913699f1d9ad996846e866230ceb257d7b31841`; lesson SHA-256 `b58d9ab342454ce1952090503de95c9e1095f2e3217460460d8e6cf429ac04fa`.

## Finding

- **Low — the file diff is not literally additions-only.** The requested diff reports `193 insertions(+), 2 deletions(-)`; zero-context hunks replace the existing Capabilities rows at `SCORECARD.md:198` and `:2010`, and append the correction starting at `:2069` (heading `:2070`). The row replacements preserve their prior text and add the suffix `37 — **not admitted** (round-37 closure; "Round 37 — closure correction")`; they are not substantive rewrites. Thus the correction is appended and the row contents are extended, but the parenthetical “git diff … shows only additions” is technically false. **Fix/clarification:** describe the diff as an appended section plus two suffix-only row extensions; if zero deleted lines is mandatory, reconcile that with routed defect 1's requirement that both existing rows carry the status (`lesson:139–140`).

## Routed-defect review

- **Defect 1 — handled accurately.** The appended closure states “**not admit round-37 C1**” and “no capability was admitted in round 37” (`SCORECARD.md:2072–2083`). Both existing rows carry the exact not-admitted suffix (`:198`, `:2010`), as requested by the lesson. The cited shortcut met 28/28 before the build; the lesson independently records this and its consequence (`lesson:60–63, 75–76`). No admission or harm claim is overstated.
- **Defect 2 — handled, with the round-37 rule preserved.** The correction says `.ufo/waves/round-37/sealed_count.py`, key `424aa248`, “stays the rule of record” (`SCORECARD.md:2081–2082`); the round-38 declaration reiterates that it does not replace that counter (`:2171–2172`). C2's pre-declaration measurement says the stdlib-plus-six-patches shortcut scored 7 (`:2237–2241`); the committed v3 receipt records `passed: 7`, `target: 20`, `met: false`, and a tool SHA-256. This supports the stated below-target separation; I read the receipt and did not run a counter.
- **Defect 5 — specified prospectively; not yet verified as a build result.** The declaration says “Every post-measurement receipt names the tool's sha256” (`SCORECARD.md:2133–2135`), inherited by C2 at `:2258–2259`. The v3 counter receipt is pinned, but the cited round-37 selftest receipt remains path-only (no tool revision or SHA-256). C2 is explicitly pre-build (`:2211`), so no post-build selftest receipt exists here to verify. Do not treat this declaration as retroactively pinning that old receipt; if the routed item requires that historical measurement itself to be pinned, add a supplemental pinned receipt.

## Commands and verification

- `git diff af43a50fa399881eead9381d835b78a015e277a6 2dab7f3114f3e9dcf072b524c88816ab05fdfcf1 -- SCORECARD.md` — exit 0; 193 insertions, 2 deletions.
- Same diff with `--unified=0` — exit 0; hunks at old lines 198 and 2010, appended block at new lines 2069–2259.
- `git show 2dab7f3114f3e9dcf072b524c88816ab05fdfcf1:<v3 shortcut receipt>` — exit 0; 7/20, not met, tool SHA present (receipt SHA-256 `f202f36a160b48d98aea6cb0053b2b2e2441e96787151cac222f134519abaa89`).
- `git show 2dab7f3114f3e9dcf072b524c88816ab05fdfcf1:<round-37 postfix selftest receipt>` — exit 0; tool path present, no tool SHA (receipt SHA-256 `079e29c1d1bd732ddc152d5c71e50533b9edcba8fb37aae8a041edb6e46f60b2`). `git diff --check ... -- SCORECARD.md` — exit 0.
- No tests or round-38 counters run; no sealed-key directories accessed.