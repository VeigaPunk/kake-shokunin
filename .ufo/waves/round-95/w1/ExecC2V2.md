# ExecC2V2 — round-95 wave w1 (kake, hyaku run 15, attempt 1)

Seat: ExecC2V2 (leaf executor). Target: the contract-v2 candidate diff for
`scripts/conditional_eval.py` (R94-6 / R93-10), delivered as a patch the L1 can
apply and score. Round base `fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3`;
freeze commit `8f638b591e739e1863f5fa22334d5e15178189ed`; instruments commit
`43cdd9fc899a2613d8ba7b55edf820825e57b4d1`.

## Verdict

```
C2-CANDIDATE hand=66/66 generated=120/120
```

Supporting conjoints, same run: `anti_table=ok`, `forgeries_refused=7/7`,
`positive=admitted`, `mutants=40/40 survivors=none` (no equivalence receipts
needed — `frozen/c2-equiv-receipts.json` is `[]`), population pins 12/12
fixtures digest-ok, pins-file digest ok, reference selfcheck ok. Driver verdict
`met=true`, driver rc=0.

## Deliverables (this directory, flat)

| File | sha256 | What |
|---|---|---|
| `conditional_eval-v2.diff` | `a7448c42a9caa603ff108aa61740e263f4d6a60ba8a77ca5638d272ae494feea` | unified diff, headers `a/scripts/conditional_eval.py` / `b/scripts/conditional_eval.py`; `patch -p1` from the lane root applies onto the round-base v1 bytes |
| `selftest-notes.md` | `1944f0eef26886188e3b62ed7caa33862c8e736cfd3c03fdedebe7b9fb261a02` | per-clause change notes, selftest churn, divergences |
| `scoring-v2.txt` | `a38f005b6f9fa09bb15dfc4b3547362f3991701da5f6219432c7db23ce51bfe9` | full scoring receipt of the run described below |

## Candidate identity

- v1 base: `git show fdd5fdbe:scripts/conditional_eval.py`, sha256
  `d3bac7de1c2d04fc355db795aebdf6012030ea5c5793d9362bc9cd8e0b8cac5e` (matches
  the sha recorded in SCORECARD's capability row).
- Patched candidate: sha256
  `9cff0c34128477dbe98e1449e074206e80b0985d223de720e1453fcc6b608848`.
- Changes: clause C1 empty-member handling in `_precondition_members` (empty
  members accepted and ignored, whitespace-only value still refused, `*` mixed
  with any member — tag or empty — still refused), clause C2 obs-text
  (0x80–0xFF) added to the opaque-tag character checks (both `_entity_tag` and
  the inline member scan), clause C3 `"role": null` mapped to origin in
  `evaluate`, clause C4 `_no_duplicate_keys` object-pairs hook in `_process`
  refusing duplicate object keys through the real stdin path with
  `invalid_input:` exit 1, clause C5 no code change (already implemented;
  pinned by selftest cases). Selftest extended with one pinning case per
  clause plus two in-place flips of v1 refusal cases the contract v2 reverses;
  `python3 -B conditional_eval.py --selftest` → observed `selftest 99/99`,
  rc=0.

## Scoring method (no lane file was read or written at scoring time)

Instrument digest check first, as ordered:

- `sha256sum LANE/.ufo/waves/round-95/c95_conditional.py` →
  `f09f84090fdda405992d7b51191be8838549e3df402b0898eb2ca00c4c3ff312` — equal
  to the pinned value in `controls/instrument-sha256.txt` and equal to
  `git show 8f638b59:.ufo/waves/round-95/c95_conditional.py | sha256sum`.
  Attack license confirmed; nothing was patched in the instruments.

Scoring run (all under `/fast/scratch/hyaku/kake-r95/ExecC2V2/`, since
removed):

- Frozen counter bytes and all 12 pinned fixtures copied into scratch via
  `git show 8f638b59:<path>`; `python3 -B driver.py` (driver text is my own
  work product) imported the frozen counter module read-only by path
  (`importlib.util.spec_from_file_location`, never modified), verified the
  pins-file digest (`93f7067c…`, ok) and every pinned fixture digest (12
  checked, 0 drift), then called the counter's own `hand_cases()`,
  `generate(95, 120)` + `reference()` and scored the candidate through the
  counter's own `score_subject` / `SANDBOX` runner (subprocess per case,
  refusal = nonzero rc), exactly the counter's scoring path. Full receipt:
  `scoring-v2.txt`; command `python3 -B driver.py 2>&1 | tee scoring-v2.txt`,
  observed rc 0.
- `python3 -B conditional_eval.py --selftest` → `selftest 99/99`, rc=0
  (the immediately preceding run printed `selftest 98/99`, rc=1, single
  failure r42 — the star/trailing-empty fix is documented in
  `selftest-notes.md`; the receipt preserved here is the passing rerun).

Per Round-92 (QUALITY.md): the numbers above are a **verdict about the
delivered candidate at scratch**, measured against the frozen counter's
reference. The frozen do-nothing base control (`controls/base-c2.txt`,
revision `43cdd9fc…`, candidate still v1) reads `met=false hand=57/66
generated=79/120 forgeries_refused=7/7 positive=admitted mutants=40/40` —
**by design**: the nine hand failures and 41 generated failures are exactly
the v2 clauses v1 refuses, so the delta this patch closes is the claimed
work, not instrument drift.

## Findings and notes for the reviewer

1. `r42` (`If-Match: *,`) refused reason changed under v2: the star now
   shares the field with an empty member, so the refusal message is
   `"if_match mixes '*' with other members"` (was `"has an empty list
   member"`). This matches the frozen reference, whose `parse_list` splits on
   commas and refuses `*,` as mixed. Documented in `selftest-notes.md`.
2. Known reading divergence, outside the frozen population: the candidate
   keeps the sequential parser, so an opaque-tag containing a comma inside a
   list member (`If-Match: "a,b"`) stays accepted (RFC-exact; v1 behaviour,
   d43–d45 unchanged). The frozen reference would refuse that shape (its
   split-on-comma is a simplification). No hand case and no generated case
   embeds a comma inside an opaque-tag (the generator's tags are
   `'"a"' 'W/"a"' '"b"' 'W/"b"' '"c"' '"a\x80"'`, joined with plain commas),
   so the divergence is unobservable by `c95_conditional.py`. Recorded, not
   silently kept; the L1 may direct it to the round gate.
3. Forgery detail worth noting: `neg-refuse-empty-member.py` (the v1-shaped
   tool that still refuses empty members) fails exactly the v2 acceptance
   cases (`inm/empty-member-middle-ignored` first) — the forged posture is
   killed by the new clauses, 7/7 refused overall.
4. No tool was installed or upgraded (seat rule: record anyway). No sysctl
   was touched. No mutating git/jj command was run anywhere; fixtures came
   from `git show` at the freeze commit; no lane tree file outside
   `.ufo/waves/round-95/w1/ExecC2V2{,.md}` was written.

## Risks / blockers

- The diff is delivered unapplied: the landed-tip score is the L1's frozen
  counting command
  (`python3 -B .ufo/waves/round-95/c95_conditional.py --root . --revision
  <landed> --work <scratch>`). My scratch driver replicates its scoring path
  (same module functions, same SANDBOX) but is not the frozen command.
- The candidate's anti-table non-hit depends on its own source bytes; the
  selftest's new raw-bytes C4 fixture is not a sorted-JSON digest of any hand
  case, and the run confirmed `anti_table=ok`.
- No blockers.

## Scratch cleanup

`/fast/scratch/hyaku/kake-r95/ExecC2V2/` deleted after receipts were copied
into this directory; verified absent (`test -e` → rc 1) before this report
was written. The seat ends with no scratch tree on disk.
