# ReviewQualityAndSkill — QUALITY round-36 criteria (a)–(f) + SKILL round-36 registry

Falsification pass on `corpus/QUALITY.md:860-887` and `SKILL.md:1056-1078` at `f3a38bf`. All runs in
`/fast/scratch/hyaku/kake-r36w2/ReviewQualityAndSkill/clone` (clone at `f3a38bf`), TMPDIR beside it.

## Per-criterion verdicts

- **(a) resolves; check runs; receipt exists.** Grounding `round-35-verifier-spotcheck.md:185-189` is
  defect 1 verbatim. Reran `knowledge_control_check.py` (r35 bundles fetched into the sandbox clone):
  exit 1, output identical to `round-35/verification/criterion-knowledge-controls-r35-c2.txt`
  (dc8e1adf 12 probes met, 0b7779dc 11 met). Gap: the bare-id-only control run the criterion
  requires ("must likewise produce its failing result") has **no receipt anywhere** — the recorded
  failure covers only the two named controls, both of which *did* earn cites.
- **(b) resolves; check runs; overstatement.** Grounding :190-193 correct. Reran all three receipts
  identically: r35 v1→v2 exit 1 (cap), r36 v1→v2 exit 0, r36 v2→v3 exit 1 (KEY_SHA256 pin) — the v2→v3
  run doubles as the pinned-value negative fixture. **But** the tool exits 1 on *every* scored diff
  and has no input for the round's note; it can never "pass only a change whose forcing control and
  score are documented." The documentation half of the predicate is enforced by nothing (human read
  of SCORECARD:1681-1698 names `CtlShortcut` and its 17-of-28 score, so the substance holds).
- **(c) resolves; check runs; receipts exact.** Grounding :194-196 correct. Reran: r35-shape exit 1
  (ablation-c_skip 22/24 ≥ 22 — the claimed negative fixture exists and fails), r36 ablations exit 0,
  "36 ablation receipts scored, all below target 25, bullets abcdefg each covered".
- **(d) resolves; check runs; claimed receipt missing.** Grounding :197-198 correct. Reran r35
  receipt: exit 1 **on "records no tree listing"** — not on "a negative listing containing
  `sealed/c2-probes.json`" as the criterion and lesson line claim. I synthesized the claimed fixture
  (`tmp/neg-report3.md`, bare `ls -la` lines incl. `sealed/c2-probes.json`): the tool *does* fail it
  ("lists a key path … matching pattern"), exit 1 — so the capability is real but the recorded
  evidence shows a different failure mode. Reran r36 receipt: exit 0 on the five ctl reports.
  Recorded limit stands (w1/ExecCriterionControlTree.md): an own-commit-tree listing passes even if
  the build tree held the key.
- **(e) resolves; check runs; receipts exact.** Reran identically: exit 1 on the 3555f63f section
  (unresolved `b720d79976a1fb8fe6a8eb4b9f50e946b0cd5e07` — confirms the "Base" hash names no object;
  real base is `b720d799ae99c19a…`), exit 0 on the r35 declaration at cd321279.
- **(f) resolves; evidence exact.** `v2/control-CtlShortcut.json` passed=17, `control-CtlShortcut.json`
  passed=9, `ablation-s_ctkey.json`=13, `ablation-s_unsure.json`=24 — all four numbers as claimed;
  lesson mistake row 2 (round-36.md:79) matches.

## SKILL registry rows (`SKILL.md:1064-1078`)

- `source-recheck-audit` entry `python3 -B scripts/source_recheck.py --manifest PATH`: ran on the
  realrun manifest (bodies extracted): **exit 1, JSON byte-identical to `realrun/audit.json`**
  (failed-policy, 14 findings on 13 rows). No-arg run: exit **64** + usage line. Write scope "none"
  holds (only `open(path,"rb")` at :513,:538).
- Verdict map **matches code exactly**: `EXIT_*` constants :42-45; `BLOCKING_REASONS` :52 =
  `input_invalid, check_invalid, charset_unsupported` → exit 2 (:561-567,:615,:621); `gone,
  http_error, moved, quote_missing, unsupported_type` → exit 1 (:493-531); emit :570-582.
- Self-test row: `python3 -B scripts/source_recheck_selftest.py` → `{"passed": 101, "failed": 0,
  "verdict": "clean"}` exit 0; "(101 fixtures)" accurate.
- Frozen proof command runs as written (bwrap present): `--revision 4d5b3d55` → passed 28/28, met,
  exit 0; `--revision b720d799` → 0/28, exit 1; `--revision fd1fb723` → "key visible at the measured
  revision", exit 2 (short `--key-revision fd1fb723` accepted). Predicate string verbatim.
- `source-snapshot` row: ran the entry command on a loopback input (no network fetch made):
  `checks 0 of 1`, exit 0, wrote **only** `manifest.json` (`version:1`) + `receipts.json` with the
  skipped check — verdict map accurate. Nit: `--manifest` accepts a path outside `--out-dir`, so the
  literal "`--out-dir` only" write scope holds for the command as written but not the flag pair.
- Procedure steps 1-6 consistent; freshness-pins.json exists; `w1/ExecSnapshotFetcher.md` exists;
  tool sha256 `577b2d7d…0d48` and build commit `4d5b3d55` verified.

## Findings (advisory)

1. (d): receipt for the *claimed* shown-able-to-fail mode (listing containing a key path) does not
   exist; the recorded failure is the missing-listing mode. Capability confirmed ad hoc; receipt gap.
2. (b): the check cannot honor "pass only a change whose forcing control and score are documented" —
   every diff fails; criterion text overstates the mechanism.
3. (a): no bare-id-only control run is on record; "must likewise produce its failing result" is
   unreceipted.
4. SKILL nit: `source_snapshot --manifest` can write outside `--out-dir`.

Not verified: the r35 counter's treatment of a bare-id-only cite (no such control exists), live GET
behavior of source_snapshot (no URL item was mine to open). No installs; bwrap/git/python3 already
present. Sandbox: `/fast/scratch/hyaku/kake-r36w2/ReviewQualityAndSkill/`.
