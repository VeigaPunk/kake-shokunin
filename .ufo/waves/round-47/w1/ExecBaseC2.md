# ExecBaseC2 — do-nothing base reproduction for C2 (round 47, wave 1)

Seat: executor. Claim under test: **C2** (freshness — r46 closure-routed prose defects
R3–R6 repaired append-only).
Assigned target: run the counter at the frozen base and compare with
`.ufo/waves/round-47/verification/c2-before-cd42e3c.json`.
Verdict on the target: **CONFIRMED**, byte-identically — 4/4 outstanding, exit **1**.
Independent finding: the base red is real and not an instrument artifact (the R3 premise is
verifiable in base bytes, and the same binary flips to 0/4 at two later commits), but three
of the four clauses are looser than the predicate sentence they decide, and the counter never
opens `SCORECARD.md` at all. Details under Falsifiers.

Method: read-only committed bytes via `git show`/`git ls-tree`; no lane mutation, no
`jj`/`git` write, no clone needed this seat (see scratch note).

## Detector

`python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision <rev>`
(0 = `C2_MET`, 1 = `C2_NOT_MET`, 2 = could-not-evaluate, 64 = usage). Clauses as committed
at HEAD (script blob `9be35ef2452aaff0757a0c2839c17cb58e08a7a59f6a217a3489598c19a8359e`,
identical in worktree and `HEAD`, clean in `git status`):

| defect | clause | site |
|---|---|---|
| R3 | any LOG line where `"R3" in line and "20 data rows" in line` | `c47_routed_count.py:161` |
| R4 | `"## Round-47 corrections"` block in `corpus/quality/citation-adjudications.md`, then per-token `expected.lower() in entries[token].lower()` for five tokens | `:129-141`, table `:42-48` |
| R5 | any LOG line containing **both** `ee43e663…d9d1` and `861113eb…a843` | `:162`, tuple `:49-52` |
| R6 | same LOG line has `[r47-correction R6 withdrawal]`, `round-46`, `withdrawn`; **and** a `verification/offline-sweep-r47-rerun.txt` whose text has the non-retroactive label, `exit=0`/`OFFLINE_EXIT=0`, and `--offline` | `:163-176` |

`git ls-tree` failure on the receipt dir → exit 2, so a missing tree cannot masquerade as red
(`:154-158`, exercised below).

## Assigned run (lane repo, lane `HEAD` `766f4610b64f35a0f402b37eb1d8be2d4d634c0f`)

```
$ python3 -B .ufo/waves/round-47/c47_routed_count.py --root . \
    --revision cd42e3c310ba442e89dde638ba6401adaefaf3e8
outstanding=4/4 C2_NOT_MET
EXIT=1
```

- exit code **1**, stderr **0 bytes** — a genuine red, not a could-not-evaluate(2).
- `--json` payload (written to scratch) vs the committed artifact: **identical**,
  both sha256 `866b91be24d6f9c0b84df7d7cf132088ea21ceb219369bad3f871ef6321d7fb4`
  (verified twice; `sort_keys=True`/`indent=2`/trailing newline make a hand-authored
  receipt improbable).
- committed receipt content: `{"R3":false,"R4":false,"R5":false,"R6":false}`,
  `outstanding 4`, `verdict C2_NOT_MET`, `revision cd42e3c…`.
- SCORECARD's own do-nothing control (`SCORECARD.md:3954-3955`): "the base revision scores
  4/4 outstanding, exit 1" — matches the measurement.

## Independent confirmation of the base state (not trusting the counter)

`B=cd42e3c310ba442e89dde638ba6401adaefaf3e8`; base exists and is an ancestor of HEAD
(`git cat-file -t` → commit; `git merge-base --is-ancestor` → true).

| defect | probe on committed base bytes | result |
|---|---|---|
| R3 | `git show $B:LOG.md \| grep -c '20 data rows'` | **0** |
| R3 premise | `git show $B:SCORECARD.md \| grep -n '12 rows'` | **1**: line 3912 `committed ledger corpus/quality/citation-adjudications.md (12 rows, every` |
| R3 truth | base ledger rows `` ^\| *`<7–10 hex>` `` | **20 rows**, file column **12** `LOG.md` + **8** `SCORECARD.md` — the "12 rows" sentence is genuinely misstated, and the 20-row split in the predicate is factual |
| R4 | `grep -c 'Round-47 corrections'` in base ledger | **0**; all five tokens (`b74190e`, `d69dd22`, `0c767c2`, `b9db4b1`, `dc8e1adf`) already present **1× each** at base |
| R5 | `grep -c` each hash in base `LOG.md` | `ee43e663…` **0**, `861113eb…` **0**, both-on-one-line **0** |
| R6 | `grep -ci 'r47-correction R6 withdrawal'` base `LOG.md` | **0** |
| R6 side | `git ls-tree -r --name-only $B .ufo/waves/round-47/verification/ \| wc -l` | **0** — the whole round-47 receipt tree postdates base |

Non-constancy (why the 4/4 is evidential, not a stuck-false instrument):

```
--revision 714e7074110469a9ed2a3594677197baa0890905  → outstanding=0/4 C2_MET   EXIT=0
--revision HEAD (766f461…)                            → outstanding=0/4 C2_MET   EXIT=0
```
Both match the committed after-receipts (`c2-after-714e707.json` reports 0/4, `C2_MET`).

Exit taxonomy exercised: bogus revision →
`could-not-evaluate: missing population file at 0000…0000`, exit **2**; missing `--root` →
exit **64**.

Receipt digests match SCORECARD's claims to the byte (`SCORECARD.md:3976-3978`):

| artifact | measured sha256 |
|---|---|
| `verification/c2-before-cd42e3c.json` | `866b91be…1d7fb4` ✔ matches SCORECARD |
| `verification/c2-after-714e707.json` | `141ede64…9d1b5dba` ✔ |
| `verification/c2-r4-mutation.txt` | `1e7636ec…cd507c3` ✔ |
| `verification/offline-sweep-r47-rerun.txt` | `b86bc459…822a717` ✔ |

Frozen-sentence identity: normalizing whitespace, the C2 sentence in `SCORECARD.md:3933-3953`
and the docstring of `c47_routed_count.py:4-22` are **identical after stripping backticks**;
the sole divergence is markdown quoting of the base hash (`` `cd42e3c…` `` vs bare) — formatting,
not predicate drift. The "…and the report" leg of that identity claim is **not checkable at
this wave**: no round-47 report exists yet (only `w1/` seat reports).

## Falsifiers / risks (measured, bounded)

1. **`revision` is echoed, not attested.** `:189` `result["revision"] = args.revision` copies
   argv into the receipt. The `fixed` flags are revision-bound because every read goes through
   `git show <rev>:…`, but the receipt field itself proves nothing; a receipt cannot be
   distinguished by that field alone. Low severity, worth knowing when citing receipts as
   self-validating.
2. **R3's `"R3"` is a substring test.** Base `LOG.md` has **9** lines containing the substring
   `R3` (from `KakeR30`, `KakeR31`, `KakeR34`, …). Base is safe only because it has **0** lines
   with `20 data rows`, so the conjunction is 0 today; tip has exactly **1** satisfier
   (`LOG.md:1793`, the intended `[r47-correction R3]` line). Latent, not live: any future line
   pairing "20 data rows" with an unrelated `R3x` label would turn R3 green without a
   correction.
3. **R4's base redness rests on marker absence, not on cell wrongness.** The five misattributed
   reason cells already exist at base; the counter never inspects them, it only requires the
   appended `## Round-47 corrections` block plus five corrected phrases. That is exactly the
   frozen predicate ("an R4 '## Round-47 corrections' block … naming all five tokens and the
   corrected reason phrase for each"), so it is not a defect — but the before→after delta
   measures *appended prose*, never whether the original cells were in fact wrong. Reason-truth
   is covered separately by `w1/CriticReasonFidelity.md`; the counter adds no independent
   check of it.
4. **The counter never opens `SCORECARD.md`.** R3's real misstatement lives at
   `SCORECARD.md:3912` ("12 rows"), and the round-47 fix to that sentence is
   `SCORECARD.md:3963-3965`. Neither the before nor the after clause reads that file, so the
   SCORECARD half of R3 (8 of the 20 rows, and the sentence that was actually wrong) is
   unmeasured by the instrument. The predicate's parenthetical "(12 LOG.md + 8 SCORECARD.md)"
   is asserted in prose only.
5. **R6's before-side is history-guaranteed, not searched.** The receipt tree is empty at base,
   so `r6_rerun_receipted` is false by absence of the directory, not by a failed content match.
   Same shape as the sibling C1 caveat. The after-side does discriminate: the same matcher
   requires the exact non-retroactive label *and* `--offline` *and* `exit=0` in
   `offline-sweep-r47-rerun.txt`, whose committed text carries all three
   (`R47 rerun only; not contemporaneous r46 verdict-time evidence and not a retroactive
   receipt for it.` / `command: node scripts/freshness-sweep.mjs --offline`).
6. `parse_cli` de-duplicates `--root` (`:74-75`) but not `--revision`; last wins silently.

## Not done (stated, not claimed)

- No mutation control was needed this seat: the base receipt is byte-reproducible from committed
  bytes and the after-side is already exercised by the two committed after-receipts. I did not
  create a scratch clone; `/fast/scratch/hyaku/kake-r47/ExecBaseC2/` holds only
  `measured-base.json`, `m2.json` and `stderr.txt`.
- Did **not** execute `node scripts/freshness-sweep.mjs` (offline or otherwise). The R6 rerun's
  `exit=0` is read from the committed receipt, not re-run; its truth is bounded by the receipt
  and the withdrawal prose, not by re-execution. Gate execution belongs to the parent.
- No lane `jj`/`git` writes, no push, no sibling-repo or fleet-root reads, no `.ufo/state/` touch.
- No tool installs or updates in this seat; the host pacman pause was irrelevant (nothing needed).

## Files changed

- `.ufo/waves/round-47/w1/ExecBaseC2.md` (this report) — the only write in the lane.
- Scratch only: `/fast/scratch/hyaku/kake-r47/ExecBaseC2/{measured-base.json,m2.json,stderr.txt}`.
